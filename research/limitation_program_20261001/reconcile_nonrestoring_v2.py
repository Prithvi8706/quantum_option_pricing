"""Independent local audit of signed-remainder non-restoring square root.

No gates or pricing paths are replayed here. This checks the actual arrays,
the recurrence and saved tests, then either the preregistered leaf stop or the
complete source decision. Historical code and receipts remain immutable.
"""

from __future__ import annotations

# Receipt prose and exact specification literals intentionally stay readable.
# ruff: noqa: E501

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from math import isqrt
from pathlib import Path
import random
import shutil
import sys
import time
import xml.etree.ElementTree as ET

import numpy as np

from research.controlled_source_completion.primitives import gate_resources
from research.limitation_program_20261001.baseline import ROOT, dump, environment, load, sha
from research.limitation_program_20261001.interval_bounds import bound_graph
from research.limitation_program_20261001.reconcile_constants import (
    ORIGINAL,
    library_path,
    relative,
)
from research.limitation_program_20261001.reconcile_shift import Auditor, eligibility
from research.limitation_program_20261001.reconcile_sqrt import (
    check_manifest,
    independently_pack,
    input_files,
)

BASELINE = ROOT / "results/limitation_program_20261001/A07_shift_run001"
CASES = ("B4x12", "B8x52")
CAPS = {"B4x12": 550141, "B8x52": 4460481}
VARIANT = "nonrestoring-signed-remainder"
LOWERING = "unsigned-nonrestoring-sqrt-signed-remainder-v1"
INTEGRATION = "same-target-nonrestoring-unsigned-sqrt-library-v1"
DIMENSIONS = ("t_count", "t_depth", "clifford_t_depth", "qubits")


def arithmetic_certificate():
    """Check bookkeeping against independent isqrt; document the induction."""
    checks = stages = negative_old = negative_new = wrapped_shift = 0

    def check(number, radicand_bits):
        nonlocal checks, stages, negative_old, negative_new, wrapped_shift
        k = (radicand_bits + 1) // 2
        r, q, remainder, prefix = k + 2, 0, 0, 0
        modulus, sign_bit = 1 << r, 1 << (r - 1)
        for position in reversed(range(k)):
            digit = (number >> (2 * position)) & 3
            prefix = 4 * prefix + digit
            old_sign = int(remainder < 0)
            negative_old += old_sign
            shifted = 4 * remainder + digit
            wrapped_shift += not -sign_bit <= shifted < sign_bit
            operand = 4 * q + 3 if old_sign else -(4 * q + 1)
            bits_operand = 3
            for bit in range(2, r):
                bits_operand |= (1 ^ old_sign ^ ((q >> (bit - 2)) & 1)) << bit
            assert bits_operand == operand % modulus
            exact_next = shifted + operand
            modular_next = (shifted + bits_operand) % modulus
            interpreted = modular_next - modulus if modular_next & sign_bit else modular_next
            assert interpreted == exact_next
            remainder = exact_next
            q = 2 * q + int(remainder >= 0)
            assert q == isqrt(prefix)
            assert remainder == prefix - (q * q if remainder >= 0 else (q + 1) ** 2)
            assert -(2 * q + 1) <= remainder <= 2 * q
            assert -sign_bit <= remainder < sign_bit
            negative_new += remainder < 0
            stages += 1
        assert q == isqrt(number)
        checks += 1

    # Every unsigned 16-bit radicand, including leading-zero pairs.
    for number in range(1 << 16):
        check(number, 16)
    # Check scaled-input wiring independently, including odd fractional widths.
    for active in range(1, 8):
        for fraction in range(9):
            for number in range(1 << active):
                check(number << fraction, active + fraction)
    rng = random.Random(0xA110C057)
    production = {0, 1, (1 << 46) - 1, 1 << 45, (1 << 45) - 1}
    production.update(1 << bit for bit in range(46))
    production.update(rng.randrange(1 << 46) for _ in range(256))
    for number in sorted(production):
        check(number << 40, 86)
    assert negative_old and negative_new and wrapped_shift
    return dict(
        passed=True,
        input_formula="isqrt(unsigned_x << fraction_bits)",
        recurrence="R'=4R+d-(4Q+1) if old R>=0; R'=4R+d+(4Q+3) otherwise; Q'=2Q+int(R'>=0)",
        initial="N=Q=R=0",
        invariant="Q=isqrt(N); R=N-Q² if nonnegative, else N-(Q+1)²",
        induction="In either old-sign branch the trial equals M-(2Q+1)², with M=4N+d. If trial>=0 choose new Q=2Q+1 and R=M-Q'²; otherwise choose Q'=2Q and R=M-(Q'+1)². Since Q²<=N<(Q+1)², M lies between (2Q)² and (2Q+2)², so this choice is exactly isqrt(M).",
        signed_bound="-(2Q+1)<=R<=2Q, Q<2**stage. At final k stages, R lies strictly within [-2**(k+1),2**(k+1)), representable in signed k+2 bits.",
        intermediate_policy="4R+d may overflow signed k+2. All updates are modulo2**(k+2); the proved final exact remainder fits that signed word, so the final sign is correct. No promise that every pre-add intermediate fits.",
        operand_identity="Low bits11; each higher bit is Q_bit XOR NOT(old_R_sign). This equals -(4Q+1) or +(4Q+3) modulo2**(k+2), respectively.",
        scaling="Read radicand pair at original source indices 2*position+bit-fraction_bits; absent indices are zero. Leading padding and all lower fractional zeros are retained.",
        remainder_correction="No remainder is externally output. A negative final R would become the usual nonnegative remainder after adding 2Q+1; root-only clean-XOR emission may reverse the uncorrected signed history directly.",
        cleanup="All k+1 remainder snapshots, private k root bits, operand and helper are charged. Operand construction is reversed per stage; complete compute is reversed after copying root bits to arbitrary output.",
        algebraic_all_guarded_input_identity=True,
        finite_bookkeeping_inputs=checks,
        finite_bookkeeping_stages=stages,
        negative_old_cases=negative_old,
        negative_new_cases=negative_new,
        overflowing_preadd_shift_cases=wrapped_shift,
        proof_scope="Algebraic induction covers every guarded input. Finite bookkeeping and emitted tests check realization; no exhaustive72-bit enumeration, continuous-dollar or physical-speedup certification.",
    )


def expected_spec(width, fraction, active):
    k = (active + fraction + 1) // 2
    return dict(
        op="sqrt",
        params={},
        width=width,
        fraction_bits=fraction,
        active_input_bits=active,
        domain="unsigned high bits zero; highest active bit may be one",
        radicand_bits=active + fraction,
        result_bits=k,
        remainder_bits=k + 2,
        remainder_history_count=k + 1,
        operand_bits=k + 2,
        adder_helper_bits=1,
        arithmetic="modulo 2**(k+2); final remainder exact signed integer",
        recurrence={
            "initial": "Q=0,R=0",
            "nonnegative_old_R": "R'=4*R+digit-(4*Q+1)",
            "negative_old_R": "R'=4*R+digit+(4*Q+3)",
            "new_root": "Q'=2*Q+int(R'>=0)",
            "operand": "bits0,1=1; higher bits=Q_bit XOR NOT(old_R_sign)",
            "invariant": "R=N-Q**2 if nonnegative else N-(Q+1)**2; Q=isqrt(N)",
            "signed_bound": "-(2*Q+1)<=R<=2*Q; Q<2**stage<=2**k",
        },
        cleanup="native output XOR; literal inverse of complete compute",
        input_contract={"unsigned_input_bits": active},
        algorithm="signed-remainder-single-cuccaro-add",
        lowering=LOWERING,
    )


def structure(entry, path):
    """Parse every actual stage and MAJ/UMA gate, without circuit generation."""
    assert sha(path) == entry["sha256"]
    spec = entry["spec"]
    width, fraction, active = spec["width"], spec["fraction_bits"], spec["active_input_bits"]
    assert (width, fraction, active) == (72, 40, 46)
    base_spec = expected_spec(width, fraction, active)
    expected = dict(base_spec)
    if "integration_lowering" in spec:
        expected["integration_lowering"] = INTEGRATION
    assert spec == expected
    assert (
        entry["key"]
        == hashlib.sha256(
            json.dumps(expected, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        ).hexdigest()[:20]
    )
    assert entry["op"] == "sqrt" and entry["params"] == {}
    assert entry["input_contract"] == {"unsigned_input_bits": active}
    assert entry["args"] == [list(range(width))]
    assert entry["outs"] == [list(range(width, 2 * width))]
    gates = np.load(path, mmap_mode="r")
    k, r = (active + fraction + 1) // 2, (active + fraction + 1) // 2 + 2
    assert (len(gates) - k) % 2 == 0
    half = (len(gates) - k) // 2
    before, copied, after = gates[:half], gates[half : half + k], gates[half + k :]
    assert np.array_equal(before, after[::-1])
    assert not np.isin(before[:, 1:], np.arange(width, 2 * width)).any()
    cursor, position = 2 * width, 0

    def allocate(size):
        nonlocal cursor
        register = list(range(cursor, cursor + size))
        cursor += size
        return register

    def expect(wires):
        nonlocal position
        row = before[position]
        assert int(row[0]) == len(wires)
        assert tuple(map(int, row[1 : 1 + len(wires)])) == tuple(wires), (
            position,
            row.tolist(),
            wires,
        )
        assert wires[-1] >= 2 * width, ("Input/output targeted by compute", position)
        position += 1

    roots = allocate(k)
    remainders = [allocate(r) for _ in range(k + 1)]
    operand, helper = allocate(r), allocate(1)[0]

    def maj(x, y, z):
        expect((x, y))
        expect((x, z))
        expect((z, y, x))

    def uma(x, y, z):
        expect((z, y, x))
        expect((x, z))
        expect((z, y))

    for stage in range(k):
        root_position = k - 1 - stage
        previous, following = remainders[stage : stage + 2]
        for bit in range(r - 2):
            expect((previous[bit], following[bit + 2]))
        for bit in (0, 1):
            source = 2 * root_position + bit - fraction
            if 0 <= source < active:
                expect((source, following[bit]))
        construction = [(operand[0],), (operand[1],)]
        for bit in range(2, r):
            construction.extend([(operand[bit],), (previous[-1], operand[bit])])
            index = root_position + bit - 1
            if index < k:
                construction.append((roots[index], operand[bit]))
        for wires in construction:
            expect(wires)
        maj(operand[0], following[0], helper)
        for bit in range(r - 1):
            maj(operand[bit + 1], following[bit + 1], operand[bit])
        for bit in reversed(range(r - 1)):
            uma(operand[bit + 1], following[bit + 1], operand[bit])
        uma(operand[0], following[0], helper)
        for wires in reversed(construction):
            expect(wires)
        expect((roots[root_position],))
        expect((following[-1], roots[root_position]))
    assert position == half
    assert np.array_equal(copied[:, 0], np.full(k, 2))
    assert np.array_equal(copied[:, 1], roots)
    assert np.array_equal(copied[:, 2], np.arange(width, width + k))
    assert cursor == entry["resources"]["qubits"]
    return dict(
        passed=True,
        parsed_forward_gates=half,
        all_stages=k,
        signed_remainder_bits=r,
        retained_remainder_history_count=k + 1,
        operand_bits=r,
        one_clean_Cuccaro_helper=True,
        complete_operand_complements_and_sign_controls_charged=True,
        full_native_argument_bits=width,
        full_native_output_bits=width,
        input_high_bits_untouched=True,
        output_high_bits_unchanged=True,
        arbitrary_output_xor=True,
        literal_forward_reverse_cleanup=True,
        qubits=cursor,
        algorithm="independent actual-gate recurrence and MAJ/UMA parser",
    )


def scan(entry, path):
    gates = np.load(path, mmap_mode="r")
    assert gates.ndim == 2 and gates.shape[1] == 4 and sha(path) == entry["sha256"]
    counts = Counter(map(int, gates[:, 0]))
    assert set(counts) <= {1, 2, 3}
    qubits = entry["resources"]["qubits"]
    for op in (1, 2, 3):
        wires = gates[gates[:, 0] == op, 1 : 1 + op]
        assert not wires.size or 0 <= wires.min() <= wires.max() < qubits
        for left in range(op):
            for right in range(left + 1, op):
                assert not np.any(wires[:, left] == wires[:, right])
    observed, td, ctd = gate_resources(gates, qubits)
    assert list(map(int, observed)) == [counts[1], counts[2], counts[3]]
    result = dict(
        source_gates=len(gates),
        x=counts[1],
        cx=counts[2],
        ccx=counts[3],
        t_count=7 * counts[3],
        clifford_cx=counts[2] + 6 * counts[3],
        clifford_h=2 * counts[3],
        t_depth=int(td),
        clifford_t_depth=int(ctd),
    )
    assert all(entry["resources"][name] == value for name, value in result.items())
    return result


def actual_leaf(leaf_root):
    rows = []
    for path in leaf_root.rglob("*.json"):
        entry = load(path)
        if (
            isinstance(entry, dict)
            and entry.get("spec", {}).get("lowering") == LOWERING
            and "gate_file" in entry
            and "resources" in entry
        ):
            rows.append((path, entry))
    assert len(rows) == 1, ("Expected one recorded leaf metadata", [str(p) for p, _ in rows])
    path, entry = rows[0]
    assert load(leaf_root / "summary.json")["best"] == entry
    return path, entry


def leaf_eligibility(candidate, baseline):
    dominated = all(baseline[d] <= candidate[d] for d in DIMENSIONS) and any(
        baseline[d] < candidate[d] for d in DIMENSIONS
    )
    improves = any(candidate[d] < baseline[d] for d in DIMENSIONS)
    work_or_scratch = (
        candidate["t_count"] < baseline["t_count"] or candidate["qubits"] < baseline["qubits"]
    )
    return dict(
        dominated_by_accepted=dominated,
        strict_any_metric_improvement=improves,
        leaf_nondominated=not dominated,
        clean_leaf_work_or_scratch_improved=work_or_scratch,
        source_screen_allowed=not dominated and improves and work_or_scratch,
    )


def xml_receipts(roots):
    rows = []
    for root in roots:
        for path in root.rglob("*.xml"):
            document = ET.parse(path).getroot()
            suites = [document] if document.tag == "testsuite" else document.findall("testsuite")
            assert suites and all(
                int(s.get(field, "0")) == 0
                for s in suites
                for field in ("failures", "errors", "skipped")
            )
            rows.append(
                dict(path=relative(path), tests=sum(int(s.get("tests", "0")) for s in suites))
            )
    assert rows
    return rows


def freeze(leaf_root, source_root):
    frozen = {}
    roots = [BASELINE, leaf_root] + ([source_root] if source_root else [])
    for directory in roots:
        check_manifest(directory)
        for path in directory.rglob("*"):
            if path.is_file():
                frozen[relative(path)] = sha(path)
        manifest = load(directory / "manifest.json")
        for field in ("external_files", "frozen_inputs", "dependency_sha256"):
            for name, expected in manifest.get(field, {}).items():
                assert sha(ROOT / name) == expected
                frozen[name.replace("\\", "/")] = expected
        for row in load(directory / "protocol.json").get("executed_dependencies", []):
            assert sha(directory / row["snapshot"]) == row["sha256"]
            assert sha(ROOT / row["source"]) == row["sha256"]
            frozen[row["source"].replace("\\", "/")] = row["sha256"]
    for case in CASES:
        for path in input_files(BASELINE / case):
            frozen[relative(path)] = sha(path)
        if source_root:
            for path in input_files(source_root / case / VARIANT):
                frozen[relative(path)] = sha(path)
        path = ORIGINAL / (case + "_accounting.json")
        frozen[relative(path)] = sha(path)
    frozen[relative(ORIGINAL / "manifest.json")] = sha(ORIGINAL / "manifest.json")
    for name in (
        "research.controlled_source_completion.primitives",
        "research.limitation_program_20261001.baseline",
        "research.limitation_program_20261001.interval_bounds",
        "research.limitation_program_20261001.reconcile_constants",
        "research.limitation_program_20261001.reconcile_sqrt",
        "research.limitation_program_20261001.reconcile_shift",
        "research.limitation_program_20261001.compact_ledger",
    ):
        path = Path(sys.modules[name].__file__)
        frozen[relative(path)] = sha(path)
    frozen[relative(Path(__file__))] = sha(Path(__file__))
    return frozen


def source_changes(auditor, source_root, leaf_entry, case):
    directory = source_root / case / VARIANT
    before, after = (load(path / "source.json") for path in (BASELINE / case, directory))
    target = load(directory / "target.json")
    assert sha(directory / "target.json") == sha(BASELINE / case / "target.json")
    for field in (
        "format",
        "word_width",
        "fraction_bits",
        "values",
        "inputs",
        "outputs",
        "clean_schedule",
        "invocation_semantics",
        "inverse_semantics",
        "exact_clifford_t",
        "arbitrary_rotations",
    ):
        assert before[field] == after[field]
    old_entries, new_entries = auditor.leafs(before), auditor.leafs(after)
    old_archive, new_archive = library_path(before), library_path(after)
    bounds, _ = bound_graph(target)
    noninputs = [i for i, node in enumerate(target["nodes"]) if node["op"] != "input"]
    changed, unchanged, structures, proofs = [], set(), {}, []
    for call_index, (old, new) in enumerate(
        zip(before["forward_calls"], after["forward_calls"], strict=True)
    ):
        assert {k: v for k, v in old.items() if k != "leaf"} == {
            k: v for k, v in new.items() if k != "leaf"
        }
        old_entry, new_entry = old_entries[old["leaf"]], new_entries[new["leaf"]]
        node_index = noninputs[call_index]
        node = target["nodes"][node_index]
        intended = node["op"] == "sqrt" and node["params"] == {} and len(node["args"]) == 1
        assert (old["leaf"] != new["leaf"]) == intended
        if not intended:
            key = old["leaf"]
            if key not in unchanged:
                assert sha(old_archive / (key + ".json")) == sha(new_archive / (key + ".json"))
                assert sha(old_archive / old_entry["gate_file"]) == sha(
                    new_archive / new_entry["gate_file"]
                )
                unchanged.add(key)
            continue
        low, high = bounds[node["args"][0]]
        assert 0 <= low <= high < 1 << 46
        assert new_entry["resources"] == leaf_entry["resources"]
        assert new_entry["sha256"] == leaf_entry["sha256"]
        assert {
            k: v for k, v in new_entry["spec"].items() if k != "integration_lowering"
        } == leaf_entry["spec"]
        proofs.append(auditor.unsigned_proof(target, node_index, new_entry["input_contract"]))
        if new["leaf"] not in structures:
            structures[new["leaf"]] = structure(new_entry, new_archive / new_entry["gate_file"])
        changed.append(
            dict(
                call_index=call_index,
                args=new["args"],
                out=new["out"],
                old_key=old["leaf"],
                new_key=new["leaf"],
                op="sqrt",
                params={},
                old_resources=old_entry["resources"],
                new_resources=new_entry["resources"],
                input_contract=new_entry["input_contract"],
            )
        )
    assert len(changed) == (30 if case == "B4x12" else 234)
    assert load(directory / "changed_calls.json") == dict(
        changes=changed, unchanged_leaf_keys=sorted(unchanged)
    )
    decisions = load(directory / "site_decisions.json")
    assert len(decisions) == len(after["forward_calls"])
    assert {d["forward_call_index"] for d in decisions} == set(range(len(after["forward_calls"])))
    for row in decisions:
        index = row["forward_call_index"]
        assert row["node_index"] == noninputs[index]
        node = target["nodes"][row["node_index"]]
        assert row["outputs"] == node["out"] and row["op"] == node["op"]
        assert row["old_key"] == before["forward_calls"][index]["leaf"]
        assert row["new_key"] == after["forward_calls"][index]["leaf"]
        if row["old_key"] != row["new_key"]:
            low, high = bounds[node["args"][0]]
            assert row["proof"]["input_bounds"] == [low, high]
            assert row["proof"]["input_value"] == node["args"][0]
            assert row["proof"]["output_value"] == node["out"][0]
            assert row["proof"]["unsigned_input_bits"] == 46
            assert row["proof"]["all_declared_input_patterns"] is True
        else:
            assert row["type"] == "fallback"
    schedule, old_schedule = (
        load(path / "schedule_capped.json") for path in (directory, BASELINE / case)
    )
    assert schedule["format"] == "compact-clean-xor-capped-wave-schedule-v5"
    for field in (
        "widths",
        "offsets",
        "retained_ssa_qubits",
        "proof_masks",
        "proof_reasons",
        "argument_and_output_copy_cx",
        "baseline_argument_and_output_copy_cx",
    ):
        assert schedule[field] == old_schedule[field], (case, field)
    independently_pack(after, new_entries, schedule)
    improved = all(
        row["new_resources"]["t_count"] < row["old_resources"]["t_count"]
        or row["new_resources"]["qubits"] < row["old_resources"]["qubits"]
        for row in changed
    )
    return dict(
        changed_calls=len(changed),
        unchanged_leaf_keys=len(unchanged),
        actual_same_ssa_unsigned_proofs=proofs,
        structural_leaf_proofs=structures,
        storage_and_copy_allocation_unchanged=True,
        exact_first_fit_groups_recomputed=True,
        clean_leaf_work_or_scratch_improved=bool(changed) and improved,
    )


def run(leaf_root, source_root, output):
    leaf_root, output = leaf_root.resolve(), output.resolve()
    source_root = source_root.resolve() if source_root else None
    frozen = freeze(leaf_root, source_root)
    output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    dump(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            before_analysis=True,
            local_only=True,
            leaf_root=relative(leaf_root),
            source_root=relative(source_root) if source_root else None,
            baseline=relative(BASELINE),
            frozen_inputs=frozen,
            producer_sha256=sha(Path(__file__)),
            family=[VARIANT],
            width=72,
            fraction_bits=40,
            active_input_bits=46,
            scope="Independent read-only actual-array recurrence, cleanup and cost audit; no new gate or financial replay",
            checks="Every signed-remainder stage, scaling pair, complete operand, actual Cuccaro gates, native output copy and literal reverse; matched accepted leaf gate resources; preregistered leaf stop; if source exists, every actual unsigned46 guard, immutable nonsqrt metadata/gate bytes including signed7 shift and32row lookup, unchanged masks/native copies/SSA storage, complete counts/DAG/first-fit groups/caps, fixed both-case adoption rule and four saved financial replays",
            selection="Leaf proceeds only if nondominated with strict improvement and T-work or scratch improvement; source adoption requires>=2% complete capped T-depth separately in both cases, CT-depth<=baseline, actual qcaps and four complete financial replays",
            no_new_emitted_replays=True,
            G2_G5="unresolved",
        ),
    )
    dump(output / "environment.json", environment())
    executed = output / "executed_code"
    executed.mkdir()
    shutil.copyfile(Path(__file__), executed / "reconcile_nonrestoring_v2.py")
    certificate = arithmetic_certificate()
    dump(output / "nonrestoring_arithmetic_certificate.json", certificate)
    leaf_summary, leaf_protocol = (
        load(leaf_root / name) for name in ("summary.json", "protocol.json")
    )
    assert leaf_summary["passed"]
    assert leaf_protocol["candidates"] == [VARIANT]
    assert (
        leaf_protocol["width"],
        leaf_protocol["fraction_bits"],
        leaf_protocol["active_input_bits"],
    ) == (72, 40, 46)
    assert leaf_protocol["promise"] == {"unsigned_input_bits": 46}
    assert leaf_protocol["resource_dimensions"] == list(DIMENSIONS)
    assert leaf_protocol["local_only"] is True
    leaf_verification = load(leaf_root / "verification.json")
    assert leaf_verification["passed"] and leaf_verification["pytest_exit_code"] == 0
    leaf_path, leaf_entry = actual_leaf(leaf_root)
    leaf_scan = scan(leaf_entry, leaf_path.parent / leaf_entry["gate_file"])
    leaf_structure = structure(leaf_entry, leaf_path.parent / leaf_entry["gate_file"])
    auditor = Auditor(frozen)
    auditor.array_scans[leaf_entry["sha256"], leaf_entry["resources"]["qubits"]] = leaf_scan
    baseline_ledgers, accepted_root_entries = {}, []
    for case in CASES:
        baseline_ledgers[case] = auditor.costs(case, BASELINE / case)
        source = load(BASELINE / case / "source.json")
        entries = auditor.leafs(source)
        roots = [entry for entry in entries.values() if entry["op"] == "sqrt"]
        assert len(roots) == 1
        accepted_root_entries.append(roots[0])
    assert accepted_root_entries[0] == accepted_root_entries[1]
    old_resources = accepted_root_entries[0]["resources"]
    assert leaf_summary["baseline_root"] == old_resources
    leaf_decision = leaf_eligibility(leaf_entry["resources"], old_resources)
    assert leaf_summary["leaf_nondominated"] == leaf_decision["leaf_nondominated"]
    assert leaf_summary["source_screen_allowed"] == leaf_decision["source_screen_allowed"]
    assert (
        leaf_summary["any_resource_improvement"] == leaf_decision["strict_any_metric_improvement"]
    )
    assert (
        leaf_summary["clean_leaf_work_or_scratch_improved"]
        == leaf_decision["clean_leaf_work_or_scratch_improved"]
    )
    assert (
        not leaf_summary["financial_gate_replays_run"] and not leaf_summary["source_gain_claimed"]
    )
    assert bool(source_root) == leaf_decision["source_screen_allowed"]
    dump(
        output / "leaf_audit.json",
        dict(
            passed=True,
            actual_gate_scan=leaf_scan,
            structural_parser=leaf_structure,
            baseline_resources=old_resources,
            candidate_resources=leaf_entry["resources"],
            decision=leaf_decision,
        ),
    )
    selected, final_cases, trials = None, [], []
    if source_root:
        summary, protocol = (load(source_root / name) for name in ("summary.json", "protocol.json"))
        assert summary["passed"] and protocol["family"] == [VARIANT]
        assert (ROOT / protocol["baseline"]).resolve() == BASELINE.resolve()
        assert protocol["threshold_percent"] == 2 and protocol["promise"] == {
            "unsigned_input_bits": 46
        }
        assert protocol["cases"] == list(CASES) and protocol["cpu_limit_seconds"] == 1800
        assert protocol["local_only"] is True and summary["cpu_seconds"] <= 1800
        for name, digest in protocol["baseline_hashes"].items():
            assert sha(BASELINE / name) == digest
        for name, digest in protocol["baseline_leaf_hashes"].items():
            assert sha(ROOT / name) == digest
        assert protocol["replay_inputs"] == {
            row["case"]: row["replays"] for row in load(BASELINE / "summary.json")["cases"]
        }
        assert sha(leaf_root / "manifest.json") == protocol["leaf_receipt_manifest_sha256"]
        for case in CASES:
            comparison = next(row for row in summary["cases"] if row["case"] == case)
            assert comparison == load(source_root / case / "comparison.json")
            screens = load(source_root / case / "screen.json")
            assert (
                screens == comparison["trials"]
                and len(screens) == 1
                and screens[0]["variant"] == VARIANT
            )
            row = screens[0]
            attribution = source_changes(auditor, source_root, leaf_entry, case)
            ledger = auditor.costs(case, source_root / case / VARIANT)
            baseline = baseline_ledgers[case]["resources"]
            assert baseline["logical_qubits"] == CAPS[case]
            assert row["resources"] == ledger["resources"] and comparison["baseline"] == baseline
            eligible = eligibility(
                ledger["resources"],
                baseline,
                CAPS[case],
                attribution["clean_leaf_work_or_scratch_improved"],
            )
            assert row["eligible"] == eligible
            assert row["changed_calls"] == attribution["changed_calls"]
            assert (
                row["clean_leaf_work_or_scratch_improved"]
                == attribution["clean_leaf_work_or_scratch_improved"]
            )
            assert row["batches"] == ledger["batch_count"]
            assert row["t_count_change"] == ledger["resources"]["t_count"] - baseline["t_count"]
            assert (
                abs(
                    row["t_count_change_percent"]
                    - 100 * (ledger["resources"]["t_count"] / baseline["t_count"] - 1)
                )
                < 1e-9
            )
            assert (
                abs(
                    row["full_t_depth_gain_percent"]
                    - 100 * (1 - ledger["resources"]["t_depth"] / baseline["t_depth"])
                )
                < 1e-9
            )
            assert all(
                row[field] is True
                for field in (
                    "target_bytes_unchanged",
                    "ssa_storage_and_copy_accounting_unchanged",
                    "fallback_metadata_and_gate_bytes_unchanged",
                )
            )
            ledger.update(
                variant=VARIANT, eligible=eligible, changes=attribution, baseline_resources=baseline
            )
            trials.append(ledger)
            dump(output / (case + "_trial_ledger.json"), ledger)
        selected = VARIANT if all(row["eligible"] for row in trials) else None
        assert summary["selected"] == selected and summary["accepted"] == bool(selected)
        assert summary["financial_gate_replays_run"] == bool(selected)
        baseline_summary = load(BASELINE / "summary.json")
        for case in CASES:
            comparison = next(row for row in summary["cases"] if row["case"] == case)
            if selected:
                trial = next(row for row in trials if row["case"] == case)
                assert comparison["selected"] == comparison["trials"][0]
                assert (
                    comparison["candidate"] == trial["resources"]
                    and comparison["replay_passed"]
                    and comparison["accepted"]
                )
                old_replays = next(row for row in baseline_summary["cases"] if row["case"] == case)[
                    "replays"
                ]
                assert len(comparison["replays"]) == len(old_replays)
                for replay, old in zip(comparison["replays"], old_replays, strict=True):
                    for field in ("label", "inputs", "initial", "expected"):
                        assert replay[field] == old[field]
                    assert replay["passed"] and replay["actual"]["values"] == replay["expected"]
                    assert replay["actual"]["all_input_and_workspace_bits_restored"]
                    assert any(replay["initial"].values())
                for name in ("source.json", "target.json", "schedule_capped.json"):
                    assert sha(source_root / case / name) == sha(
                        source_root / case / selected / name
                    )
                final, effective = trial, source_root / case
            else:
                assert comparison.get("replays", []) == [] and not comparison.get("accepted", False)
                assert not (source_root / case / "source.json").exists()
                final, effective = baseline_ledgers[case], BASELINE / case
            final_cases.append(
                dict(final, effective_source=relative(effective), selected_variant=selected)
            )
        source_verification = load(source_root / "verification.json")
        assert source_verification["passed"] and source_verification["pytest_exit_code"] == 0
        assert sum(len(row["replays"]) for row in baseline_summary["cases"]) == 4
        assert sum(len(row["replays"]) for row in summary["cases"]) == (4 if selected else 0)
    else:
        assert not leaf_decision["source_screen_allowed"]
        for case in CASES:
            final_cases.append(
                dict(
                    baseline_ledgers[case],
                    effective_source=relative(BASELINE / case),
                    selected_variant=None,
                )
            )
    for row in final_cases:
        dump(output / (row["case"] + "_accepted_ledger.json"), row)
    receipts = xml_receipts([leaf_root] + ([source_root] if source_root else []))
    assert sum(row["tests"] for row in receipts) == (88 if source_root else 28)
    next_action = (
        "Use the accepted complete-source owner ranking for the next bounded local experiment. Keep G2-G5 open and all work local."
        if selected
        else "Retain the accepted signed7-shift baseline. Preserve the exact root leaf and its measured decision, then choose the next bounded alternative under a new frozen protocol. Keep G2-G5 open."
    )
    result = dict(
        passed=True,
        decision="independent_nonrestoring_sqrt_audit",
        accepted=bool(selected),
        selected=selected,
        source_root=relative(source_root) if source_root else None,
        leaf_root=relative(leaf_root),
        baseline=relative(BASELINE),
        source_screen_run=bool(source_root),
        leaf_decision=leaf_decision,
        cases=final_cases,
        trials=trials,
        actual_unique_gate_arrays_scanned=len(auditor.array_scans),
        metadata_locations_checked=len(auditor.leaf_cache) + 1,
        frozen_input_count=len(frozen),
        exact_arithmetic_certificate=True,
        pytest_xml_receipts=receipts,
        new_gate_replays=0,
        new_producer_full_source_replays=4 if selected else 0,
        G2_G5="unresolved",
        next_action=next_action,
        seconds=time.perf_counter() - started,
    )
    dump(output / "summary.json", result)
    dump(
        output / "verification.json",
        dict(
            passed=True,
            producer_sha256=sha(Path(__file__)),
            command=[
                str(Path(sys.executable).resolve()),
                "-m",
            "research.limitation_program_20261001.reconcile_nonrestoring_v2",
                "--leaf-root",
                relative(leaf_root),
                "--output",
                relative(output),
            ]
            + (["--source-root", relative(source_root)] if source_root else []),
            checks=[
                "Frozen receipts and executed code",
                "Independent non-restoring induction and signed modular bounds",
                "Actual signed-remainder recurrence/Cuccaro/copy/reverse gate parsing",
                "Matched accepted leaf resource and predeclared stop",
                "Complete source guards, immutable fallbacks, native copies/masks, costs/DAG/caps/schedules when emitted",
                "Fixed both-case selection and saved financial replays",
            ],
            new_replays=0,
        ),
    )
    with (output / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write("# Next local action\n\n" + next_action + "\n")
    report = ROOT / "docs/limitation_program_20261001/NONRESTORING_SOURCE_COSTS.md"
    with report.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("# Independent non-restoring square-root audit\n\n")
        handle.write(
            certificate["recurrence"]
            + ".\n\n"
            + certificate["induction"]
            + "\n\n"
            + certificate["signed_bound"]
            + "\n\n"
            + certificate["intermediate_policy"]
            + "\n\n"
            + certificate["operand_identity"]
            + "\n\n"
            + certificate["scaling"]
            + "\n\n"
            + certificate["cleanup"]
            + "\n\n"
        )
        handle.write(
            f"The actual signed-remainder gate array was parsed completely, including every Cuccaro MAJ/UMA, operand inverse, new-sign root bit, output XOR and exact reverse. Finite arithmetic bookkeeping checked {certificate['finite_bookkeeping_inputs']:,} radicands; that enumeration is separate from the algebraic all-domain proof.\n\n"
        )
        handle.write(
            "| Resource | Accepted restoring leaf | Non-restoring leaf |\n|---|---:|---:|\n"
        )
        for name in DIMENSIONS:
            handle.write(
                f"| {name} | {old_resources[name]:,} | {leaf_entry['resources'][name]:,} |\n"
            )
        handle.write(
            "\nThe predeclared leaf screen "
            + (
                "allowed full-source testing.\n\n"
                if source_root
                else "stopped before full-source testing. No new financial replay was run.\n\n"
            )
        )
        if trials:
            handle.write(
                "| Case | T gates | T-depth | T-depth gain | CT-depth | Qubits / cap | Eligible |\n|---|---:|---:|---:|---:|---:|---|\n"
            )
            for row in trials:
                r, b = row["resources"], row["baseline_resources"]
                handle.write(
                    f"| {row['case']} | {r['t_count']:,} | {r['t_depth']:,} | {100 * (1 - r['t_depth'] / b['t_depth']):.4f}% | {r['clifford_t_depth']:,} | {r['logical_qubits']:,} / {row['qubit_cap']:,} | {row['eligible']} |\n"
                )
            handle.write(
                "\nAll30 B4 and234 B8 sqrt sites have unsigned46 intervals in their actual validated SSA graph. Every other leaf metadata and gate array matches the accepted baseline bytes, including signed7 shift and all32 lookup rows. Native copies, masks and retained SSA storage are unchanged. Counts, complete DAG, first-fit groups and actual caps were independently reconciled.\n\n"
            )
        handle.write(
            (
                "Adopted after both-case eligibility and four saved complete financial gate replays.\n\n"
                if selected
                else "Accepted signed7-shift baseline retained; no non-restoring source adoption.\n\n"
            )
            + next_action
            + "\n\nG2 continuous-dollar certification, G3 compatible99% estimator schedule, G4 matched classical timing and G5 physical10x runtime accounting remain unresolved. This audit establishes no quantum advantage. Everything stayed local.\n\n"
        )
        handle.write(
            f"Receipts: [summary](../../{relative(output)}/summary.json), [complete audit](../../{relative(output)}/), [auditor](../../research/limitation_program_20261001/reconcile_nonrestoring_v2.py).\n"
        )
    assert all(sha(ROOT / name) == digest for name, digest in frozen.items())
    files = {relative(path): sha(path) for path in output.rglob("*") if path.is_file()}
    files[relative(report)] = sha(report)
    dump(
        output / "manifest.json",
        dict(files=files, frozen_inputs=frozen, manifest_self_hash_excluded=True),
    )
    print(
        "PASS independent non-restoring audit",
        selected or "signed7-shift-retained",
        len(auditor.array_scans),
        "actual arrays",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    run(arguments.leaf_root, arguments.source_root, arguments.output)
