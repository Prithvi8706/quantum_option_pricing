"""Independent static cost/proof audit of a completed A09 prefix source screen.

Reuses the frozen A01 cost auditor, never changes historical modules or evidence,
and never runs a financial or gate replay. All current and rejected candidates
are checked before using the preregistered both-case selection.
"""

from __future__ import annotations

# ruff: noqa: E501

import argparse
from collections import Counter
from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys
import time
import xml.etree.ElementTree as ET

import numpy as np

from research.controlled_source_completion.primitives import gate_resources
from research.limitation_program_20261001.baseline import (
    ROOT,
    dump,
    environment,
    load,
    sha,
)
from research.limitation_program_20261001.reconcile_constants import (
    Auditor,
    ORIGINAL,
    library_path,
    relative,
)


VARIANTS = ("brent-kung", "kogge-stone")
BASELINE = ROOT / "results/limitation_program_20261001/A10_inverse_run001"
LOWERING = "signed-complement-csa-prefix-final-v1"
CASES = ("B4x12", "B8x52")


def source_files(directory):
    files = [directory / name for name in ("target.json", "source.json", "schedule_capped.json")]
    source = load(directory / "source.json")
    library = library_path(source)
    for key in source["library_keys"]:
        meta = library / (key + ".json")
        files.extend((meta, library / load(meta)["gate_file"]))
    return files


def check_producer_manifest(source_root):
    manifest = load(source_root / "manifest.json")
    # A09 uses paths relative to its result root; support a structured manifest
    # as well when a root completion receipt supplies one.
    if "files" in manifest and isinstance(manifest["files"], dict):
        manifest = manifest["files"]
    for path, expected in manifest.items():
        assert isinstance(expected, str) and len(expected) == 64
        candidate = source_root / path
        if not candidate.exists():
            candidate = ROOT / path
        assert sha(candidate) == expected, ("Producer manifest mismatch", path)
    return len(manifest)


def freeze(source_root):
    result = load(source_root / "summary.json")
    assert result["passed"] and len(result["cases"]) == 2
    protocol = load(source_root / "protocol.json")
    baseline = ROOT / protocol["baseline"].replace("\\", "/")
    assert baseline.resolve() == BASELINE.resolve()
    assert load(baseline / "summary.json")["passed"] and load(baseline / "summary.json")["accepted"]
    check_producer_manifest(source_root)
    frozen = {relative(path): sha(path) for path in source_root.rglob("*") if path.is_file()}
    for path in (
        baseline / "summary.json",
        ORIGINAL / "manifest.json",
        *[ORIGINAL / (case + "_accounting.json") for case in CASES],
    ):
        frozen[relative(path)] = sha(path)
    for case in CASES:
        for path in source_files(baseline / case):
            frozen[relative(path)] = sha(path)
        for variant in VARIANTS:
            for path in source_files(source_root / case / variant):
                frozen[relative(path)] = sha(path)
    for path, expected in protocol["baseline_hashes"].items():
        assert sha(baseline / path) == expected
    for path, expected in protocol["baseline_leaf_hashes"].items():
        assert sha(ROOT / path) == expected
    for dependency in protocol["executed_dependencies"]:
        snapshot = source_root / dependency["snapshot"]
        assert sha(snapshot) == dependency["sha256"]
        assert sha(ROOT / dependency["source"]) == dependency["sha256"]
    for module in (
        sys.modules[Auditor.__module__],
        sys.modules["research.limitation_program_20261001.baseline"],
        sys.modules["research.limitation_program_20261001.compact_ledger"],
        sys.modules["research.controlled_source_completion.primitives"],
    ):
        path = Path(module.__file__)
        frozen[relative(path)] = sha(path)
    frozen[relative(Path(__file__))] = sha(Path(__file__))
    return frozen, protocol


def normal_form(width, fraction, producer):
    """Check integer polynomial coefficients, proving the Boolean input identity."""
    n, modulus = width + fraction, 1 << (width + fraction)
    expected_terms = []
    constant = 0
    for b in range(width):
        for a in range(width):
            column = a + b
            signed_coefficient = (-1 if a == width - 1 else 1) * (-1 if b == width - 1 else 1)
            if column >= n:
                assert (signed_coefficient * (1 << column)) % modulus == 0
                continue
            negative = signed_coefficient < 0
            expected_terms.append((a, b, column, negative))
            if negative:
                constant += 1 << column
            encoded_coefficient = -1 if negative else 1
            assert (encoded_coefficient - signed_coefficient) * (1 << column) % modulus == 0
    terms, correction = producer(width, fraction)
    assert terms == expected_terms
    assert (constant + correction) % modulus == 0
    assert correction == (-constant) % modulus
    # Arithmetic extraction follows Euclidean division, including negatives:
    # P = q*2**f+r, 0<=r<2**f; reducing P modulo2**(w+f) preserves q modulo2**w.
    for value in (-(1 << (2 * width)), -(1 << width) - 1, -1, 0, 1, (1 << (2 * width)) - 1):
        assert ((value % modulus) >> fraction) == (value // (1 << fraction)) % (1 << width)
    # This verifies every full-adder truth-table row used by the CSA layers.
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                summed, carry = x ^ y ^ z, (x & y) ^ ((x ^ y) & z)
                assert summed + 2 * carry == x + y + z
    return dict(
        width=width,
        fraction_bits=fraction,
        product_width=n,
        partial_terms=len(terms),
        negative_terms=sum(term[3] for term in terms),
        correction=correction,
        correction_bit_positions=[bit for bit in range(n) if correction >> bit & 1],
        all_boolean_inputs_normal_form_identity=True,
        low_columns_retained=True,
        floor_extraction_identity="(P mod 2^(w+f)) >> f = floor(P/2^f) mod 2^w for every signed integer P",
        scope="Coefficient/correction and extraction identity plus8 CSA truth rows; circuit functionality relies on the frozen producer and its saved finite semantic tests. Cleanup/output XOR also have a separate structural gate proof.",
    )


def producer_terms(source_root, protocol):
    dependencies = [
        row
        for row in protocol["executed_dependencies"]
        if Path(row["source"]).name == "prefix_multiplier.py"
    ]
    assert len(dependencies) == 1
    path = source_root / dependencies[0]["snapshot"]
    spec = importlib.util.spec_from_file_location("_frozen_a09_prefix_producer", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.signed_partial_terms


def scan_and_structure(entry, path, auditor, producer):
    assert sha(path) == entry["sha256"]
    resources = entry["resources"]
    gates = np.load(path, mmap_mode="r")
    assert gates.ndim == 2 and gates.shape[1] == 4
    counts = Counter(map(int, gates[:, 0]))
    assert set(counts) <= {1, 2, 3}
    for kind in (1, 2, 3):
        wires = gates[gates[:, 0] == kind, 1 : 1 + kind]
        assert not wires.size or (wires.min() >= 0 and wires.max() < resources["qubits"])
        if kind > 1:
            assert not np.any(wires[:, 0] == wires[:, 1])
            if kind == 3:
                assert not np.any(wires[:, 0] == wires[:, 2]) and not np.any(
                    wires[:, 1] == wires[:, 2]
                )
    cache_key = (entry["sha256"], resources["qubits"])
    if cache_key not in auditor.array_scans:
        observed, td, ctd = gate_resources(gates, resources["qubits"])
        assert list(map(int, observed)) == [counts[1], counts[2], counts[3]]
        auditor.array_scans[cache_key] = dict(
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
    assert all(resources[field] == value for field, value in auditor.array_scans[cache_key].items())
    spec = entry["spec"]
    width, fraction = spec["width"], spec["fraction_bits"]
    assert entry["op"] == spec["op"] == "mul" and spec["params"] == {}
    assert spec["lowering"] == LOWERING and spec["variant"] in VARIANTS
    assert (
        spec["product_width"] == width + fraction
        and "input_contract" not in entry
        and "input_contract" not in spec
    )
    assert entry["args"] == [list(range(width)), list(range(width, 2 * width))]
    assert entry["outs"] == [list(range(2 * width, 3 * width))]
    out = np.asarray(entry["outs"][0])
    involved = np.flatnonzero(np.isin(gates[:, 1:], out).any(axis=1))
    assert len(involved) == width and np.array_equal(
        involved, np.arange(involved[0], involved[0] + width)
    )
    copy = gates[involved]
    assert np.all(copy[:, 0] == 2) and np.array_equal(copy[:, 2], out)
    assert not np.isin(copy[:, 1], out).any()
    assert np.array_equal(gates[: involved[0]], gates[involved[-1] + 1 :][::-1])
    terms, correction = producer(width, fraction)
    cursor = 0
    value_wire = 3 * width
    for a, b, _, negative in terms:
        if negative:
            assert gates[cursor, 0] == 1 and gates[cursor, 1] == value_wire
            cursor += 1
        assert np.array_equal(gates[cursor], np.asarray([3, a, width + b, value_wire]))
        cursor += 1
        value_wire += 1
    for bit in range(width + fraction):
        if correction >> bit & 1:
            assert gates[cursor, 0] == 1 and gates[cursor, 1] == value_wire
            cursor += 1
            value_wire += 1
    return dict(
        width=width,
        fraction_bits=fraction,
        variant=spec["variant"],
        partial_prefix_gates=cursor,
        full_width_archival_register_binding=True,
        no_input_contract=True,
        contiguous_output_copy_gates=width,
        output_never_controls=True,
        reverse_identical_compute_uncompute=True,
        universal_arbitrary_output_xor_and_input_workspace_restoration=True,
    )


def changed(auditor, source_root, case, variant, producer):
    directory = source_root / case / variant
    before = load(BASELINE / case / "source.json")
    after = load(directory / "source.json")
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
    assert after["format"] == "hierarchical-clean-xor-source-v1"
    left, right = auditor.leafs(before), auditor.leafs(after)
    old_library, new_library = library_path(before), library_path(after)
    indices = [i for i, node in enumerate(target["nodes"]) if node["op"] != "input"]
    changes, unchanged, structural = [], set(), {}
    for index, (old_call, call) in enumerate(
        zip(before["forward_calls"], after["forward_calls"], strict=True)
    ):
        assert {k: v for k, v in old_call.items() if k != "leaf"} == {
            k: v for k, v in call.items() if k != "leaf"
        }
        old, new = left[old_call["leaf"]], right[call["leaf"]]
        assert old["op"] == new["op"] and old["params"] == new["params"]
        intended = target["nodes"][indices[index]]["op"] == "mul"
        assert (old_call["leaf"] != call["leaf"]) == intended
        if not intended:
            key = old_call["leaf"]
            if key not in unchanged:
                assert sha(old_library / (key + ".json")) == sha(new_library / (key + ".json"))
                assert sha(old_library / old["gate_file"]) == sha(new_library / new["gate_file"])
                unchanged.add(key)
            continue
        assert new["spec"]["variant"] == variant and "input_contract" not in new
        if call["leaf"] not in structural:
            structural[call["leaf"]] = scan_and_structure(
                new, new_library / new["gate_file"], auditor, producer
            )
        changes.append(
            dict(
                call_index=index,
                args=call["args"],
                out=call["out"],
                old_key=old_call["leaf"],
                new_key=call["leaf"],
                op="mul",
                params={},
                old_resources=old["resources"],
                new_resources=new["resources"],
                input_contract={},
            )
        )
    assert load(directory / "changed_calls.json") == dict(
        changes=changes, unchanged_leaf_keys=sorted(unchanged)
    )
    decisions = load(directory / "site_decisions.json")
    assert len(decisions) == len(after["forward_calls"])
    assert {d["forward_call_index"] for d in decisions} == set(range(len(after["forward_calls"])))
    for decision in decisions:
        index = decision["forward_call_index"]
        assert decision["node_index"] == indices[index]
        assert (
            decision["old_key"] == before["forward_calls"][index]["leaf"]
            and decision["new_key"] == after["forward_calls"][index]["leaf"]
        )
        if after["forward_calls"][index]["leaf"] != before["forward_calls"][index]["leaf"]:
            assert "prefix" in decision["type"] and "mul" in decision["type"]
        else:
            assert decision["type"] == "fallback"
    return dict(
        changed_calls=len(changes),
        unchanged_leaf_keys=len(unchanged),
        structural_leaf_proofs=structural,
    )


def run(source_root, output):
    source_root, output = source_root.resolve(), output.resolve()
    frozen, producer_protocol = freeze(source_root)
    output.mkdir(parents=True, exist_ok=False)
    report = ROOT / "docs/limitation_program_20261001/PREFIX_SOURCE_COSTS.md"
    assert not report.exists()
    started = time.perf_counter()
    dump(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            before_analysis=True,
            local_only=True,
            source_root=relative(source_root),
            baseline=relative(BASELINE),
            frozen_inputs=frozen,
            producer_sha256=sha(Path(__file__)),
            scope="Independent read-only actual-array arithmetic/resource audit; no pricing or gate replay",
            selection="One common variant eligible in both cases; at least2% complete capped T-depth reduction each, Clifford+T depth no larger and current actual qubit caps. Total T increases are allowed but priced explicitly. Minimum summed T-depth, then summed T gates, then summed logical qubits.",
            checks="Signed coefficient/correction normal form, retained low-column floor semantics; physical partial gates; contiguous outer copy and reversed computation; no input contracts; unchanged target/fallback bytes and format; all actual gate resources, full counts, compact widths/copies/DAG/batches/peak caps; fixed categories and same-SSA squares; saved replay/pytest receipts.",
            stop_rule="Exactly two existing variants in two cases, abort at first mismatch; no source/progress/history edits or forecast speedup credit.",
            proof_scope="Signed arithmetic normal form and extraction are identities for all Boolean inputs; output XOR/restoration follows from literal reverse-identical gates. Remaining emitted functional circuit equivalence is supported by saved finite tests/replays, not exhaustive signed72 enumeration. G2-G5 unresolved.",
        ),
    )
    dump(output / "environment.json", environment())
    auditor = Auditor(frozen)
    producer = producer_terms(source_root, producer_protocol)
    proofs = [
        normal_form(width, fraction, producer)
        for width in range(1, 9)
        for fraction in range(width + 1)
    ]
    proofs.append(normal_form(72, 40, producer))
    dump(
        output / "signed_arithmetic_certificate.json",
        dict(passed=True, cases=proofs, new_gate_replays=0),
    )
    leaf_results = []
    for row in load(source_root / "leaf_screen.json"):
        entry = dict(row, op="mul")
        leaf_results.append(
            scan_and_structure(entry, source_root / row["gate_file"], auditor, producer)
        )
    dump(output / "standalone_leaf_structure.json", dict(passed=True, leaves=leaf_results))
    summary = load(source_root / "summary.json")
    result_cases = []
    trial_results = {}
    for case in CASES:
        comparison = next(row for row in summary["cases"] if row["case"] == case)
        if (source_root / case / "comparison.json").exists():
            assert load(source_root / case / "comparison.json") == comparison
        screens = load(source_root / case / "screen.json")
        assert comparison["trials"] == screens and [row["variant"] for row in screens] == list(
            VARIANTS
        )
        baseline = load(BASELINE / case / "schedule_capped.json")["resources"]
        assert comparison["baseline"] == baseline
        for row in screens:
            variant = row["variant"]
            directory = source_root / case / variant
            attribution = changed(auditor, source_root, case, variant, producer)
            ledger = auditor.costs(case, directory)
            assert (
                row["resources"] == ledger["resources"]
                and ledger["qubit_cap"] == baseline["logical_qubits"]
            )
            eligible = (
                100 * ledger["resources"]["t_depth"] <= 98 * baseline["t_depth"]
                and ledger["resources"]["clifford_t_depth"] <= baseline["clifford_t_depth"]
                and ledger["resources"]["logical_qubits"] <= baseline["logical_qubits"]
            )
            delta_t = ledger["resources"]["t_count"] - baseline["t_count"]
            assert (
                row["eligible"] == eligible and row["changed_calls"] == attribution["changed_calls"]
            )
            assert row["batches"] == ledger["batch_count"] and row["t_count_change"] == delta_t
            if "work_depth_tradeoff_requires_physical_costing" in row:
                assert row["work_depth_tradeoff_requires_physical_costing"] == (delta_t > 0)
            ledger.update(
                variant=variant,
                eligible=eligible,
                changes=attribution,
                t_count_change=delta_t,
                baseline_resources=baseline,
                t_depth_change=ledger["resources"]["t_depth"] - baseline["t_depth"],
                clifford_t_depth_change=ledger["resources"]["clifford_t_depth"]
                - baseline["clifford_t_depth"],
            )
            trial_results[case, variant] = ledger
            dump(output / (case + "_" + variant + "_ledger.json"), ledger)
    eligible_variants = [
        variant
        for variant in VARIANTS
        if all(trial_results[case, variant]["eligible"] for case in CASES)
    ]
    selected = (
        min(
            eligible_variants,
            key=lambda variant: tuple(
                sum(trial_results[case, variant]["resources"][field] for case in CASES)
                for field in ("t_depth", "t_count", "logical_qubits")
            ),
        )
        if eligible_variants
        else None
    )
    assert summary["selected"] == selected and summary["accepted"] == (selected is not None)
    baseline_summary = load(BASELINE / "summary.json")
    for case in CASES:
        comparison = next(row for row in summary["cases"] if row["case"] == case)
        if selected is not None:
            chosen = next(row for row in comparison["trials"] if row["variant"] == selected)
            assert (
                comparison["selected"] == chosen and comparison["candidate"] == chosen["resources"]
            )
            assert comparison["accepted"] and comparison["replay_passed"]
            replays = comparison["replays"]
            prior = next(row for row in baseline_summary["cases"] if row["case"] == case)["replays"]
            assert len(replays) == len(prior)
            if (source_root / case / "replays.json").exists():
                assert replays == load(source_root / case / "replays.json")
            for replay, old in zip(replays, prior, strict=True):
                for key in ("label", "inputs", "initial", "expected"):
                    assert replay[key] == old[key]
                assert replay["passed"] and replay["actual"]["values"] == replay["expected"]
                assert replay["actual"]["all_input_and_workspace_bits_restored"]
                assert all(
                    0 <= initial < (1 << 72) for initial in replay["initial"].values()
                ) and any(replay["initial"].values())
            for filename in ("source.json", "target.json", "schedule_capped.json"):
                assert sha(source_root / case / filename) == sha(
                    source_root / case / selected / filename
                )
            final = trial_results[case, selected]
            effective_source = source_root / case
        else:
            assert not comparison.get("accepted", False) and not comparison.get(
                "replay_passed", False
            )
            assert not (source_root / case / "source.json").exists()
            final = auditor.costs(case, BASELINE / case)
            effective_source = BASELINE / case
        final = dict(
            final,
            effective_source=relative(effective_source),
            selected_variant=selected,
            prior_full_source_replays=len(comparison.get("replays", [])),
        )
        result_cases.append(final)
        dump(output / (case + "_accepted_ledger.json"), final)
        print(
            case, "PASS", selected or "baseline-retained", final["resources"]["t_depth"], flush=True
        )
    xml_receipts = []
    for path in source_root.rglob("*.xml"):
        document = ET.parse(path).getroot()
        suites = [document] if document.tag == "testsuite" else document.findall("testsuite")
        assert suites and all(
            int(suite.get("failures", "0")) == 0 and int(suite.get("errors", "0")) == 0
            for suite in suites
        )
        xml_receipts.append(
            dict(path=relative(path), tests=sum(int(suite.get("tests", "0")) for suite in suites))
        )
    verification = load(source_root / "verification.json")
    assert verification["passed"] and verification["pytest_exit_code"] == 0
    next_action = "Use the recomputed full-source owner ranking to screen square root or remaining cmul/shift separately at the current accepted caps. Exact self-products remain a squaring alternative; any circuit replacement needs its own bounded proof/tests and complete-source selection. If extra T work was accepted for shallower multiplication, carry that exact increase into the physical factory/runtime ledger before claiming speedup."
    result = dict(
        passed=True,
        decision="independent_prefix_source_audit",
        accepted=selected is not None,
        selected=selected,
        source_root=relative(source_root),
        baseline=relative(BASELINE),
        cases=result_cases,
        actual_unique_gate_arrays_scanned=len(auditor.array_scans),
        metadata_locations_checked=len(auditor.leaf_cache),
        frozen_input_count=len(frozen),
        standalone_leaf_proofs=len(leaf_results),
        signed_normal_form_certificates=len(proofs),
        pytest_xml_receipts=xml_receipts,
        new_gate_replays=0,
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
                "research.limitation_program_20261001.reconcile_prefix",
                "--source-root",
                relative(source_root),
                "--output",
                relative(output),
            ],
            checks=[
                "Frozen input and producer manifest hashes",
                "Every actual leaf array/count/depth and full signed input interface",
                "Signed partial normal form/floor extraction and actual partial gate prefix",
                "Literal compute-copy-reverse proof for arbitrary outputs and cleanup",
                "All source formats, target bytes, register bindings and fallback bytes",
                "Full counts, compact masks/copies/DAG/groups/qubits and fixed categories",
                "Both-case2% threshold, shared selection and explicit T-work delta",
                "Saved finite test/replay receipts only",
            ],
            new_replays=0,
        ),
    )
    with (output / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write("# Next local action\n\n" + next_action + "\n")
    lines = [
        "# Independent prefix-multiplier source audit\n\n",
        "The completed local A09 screen was independently checked against actual leaf arrays and frozen task/call categories. Both variants were checked at both accepted baseline caps. This audit adds no financial or gate replay.\n\n",
        "| Case | Selected variant | T gates | T change | Compact T-depth | Clifford+T depth | Logical qubits / cap |\n|---|---|---:|---:|---:|---:|---:|\n",
    ]
    for row in result_cases:
        resources = row["resources"]
        old = load(BASELINE / row["case"] / "schedule_capped.json")["resources"]
        lines.append(
            f"| {row['case']} | {selected or 'baseline retained'} | {resources['t_count']:,} | {resources['t_count'] - old['t_count']:+,} | {resources['t_depth']:,} | {resources['clifford_t_depth']:,} | {resources['logical_qubits']:,} / {row['qubit_cap']:,} |\n"
        )
    lines.append(
        f"\nThe predeclared rule requires at least 2% complete-source T-depth reduction separately in both cases, no Clifford+T depth increase and the prior actual qubit caps. A single variant is chosen by summed T-depth, then T gates, then qubits. Extra T gates are permitted by that experiment and are fully reported; a shallower source does not establish a faster physical runtime. Actual scans covered {len(auditor.array_scans)} unique arrays and {len(auditor.leaf_cache)} metadata locations.\n\n"
    )
    production = proofs[-1]
    lines.append(
        f"For the full signed72/f40 product, the independent coefficient certificate matches {production['partial_terms']:,} retained partial terms and {production['negative_terms']} negative terms. Complementing each negative Boolean term adds a fixed weight; correction {production['correction']} (bits {production['correction_bit_positions']}) cancels it modulo 2^112. Every low column is retained through carrying. Euclidean division proves bit extraction implements floor(signed(a)*signed(b)/2^40) modulo 2^72, including negative products. No narrowed input or zero-low-bit promise is introduced.\n\n"
    )
    lines.append(
        "Actual emitted partial gates match those coefficients and correction. The outer output is touched by exactly one contiguous full-width CX copy block, never controls a gate, and the surrounding computation/uncomputation segments are literal reverses. This proves arbitrary-output XOR behavior and complete input/workspace restoration structurally for the compute-copy-reverse circuit. Remaining functional circuit equivalence is supported by the saved finite leaf tests and selected full-source replay receipts; signed72 inputs are not exhaustively enumerated.\n\n"
    )
    for row in result_cases:
        lines.append(
            f"## Final {row['case']} ledger\n\nIndependent forward DAG T-depth: {row['independent_forward_dependency_t_depth']:,}; compact argument/output copy CX: {row['compact_total_copy_cx']:,}. Retained SSA qubits: {row['retained_ssa_qubits']:,}, external output: {row['named_output_qubits']}, peak private scratch: {row['peak_private_scratch_qubits']:,}. Actual same-SSA self-products: {row['same_ssa_self_products']['count']:,}; complete signatures and occurrences are saved.\n\n| Category | T gates | Overlapping capped T-depth diagnostic |\n|---|---:|---:|\n"
        )
        for name, category in row["category_costs"].items():
            lines.append(
                f"| {name} | {category.get('t_count', 0):,} | {category.get('overlapping_capped_t_depth_diagnostic', 0):,} |\n"
            )
        lines.append("\nTop three deterministic depth-owner leaves:\n\n")
        for leaf in row["top_three_depth_owner_leaves"]:
            lines.append(
                f"- `{leaf['leaf']}`: {leaf['op']}, {leaf['params']}, {leaf['exclusive_batch_t_depth']:,} attributed layers; hypothetical fixed-batch zero-cost saving {leaf['optimistic_fixed_batch_zero_cost_saving']:,}.\n"
            )
    lines.append(
        "\nEvery call is attributed once using frozen categories; category depths overlap and cannot be serially summed. Batch owners and zero-cost diagnostics guide the next bounded screen and do not represent attainable independent speedups. Canonical serial source resources and actual compact executed resources were reconciled as separate scopes. The source format, financial target bytes, precision, law and fallback leaves remain unchanged.\n\n"
        + next_action
        + "\n\nG2 continuous-dollar certification, G3 the explicit compatible 99% estimator schedule, G4 matched classical target timing and G5 physical 10× runtime accounting remain unresolved. All work stayed local.\n\n"
    )
    lines.append(
        f"Receipts: [summary](../../{relative(output)}/summary.json), [complete audit](../../{relative(output)}/), [producer](../../research/limitation_program_20261001/reconcile_prefix.py).\n"
    )
    with report.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))
    assert all(sha(ROOT / path) == digest for path, digest in frozen.items())
    files = {relative(path): sha(path) for path in output.rglob("*") if path.is_file()}
    files[relative(report)] = sha(report)
    dump(
        output / "manifest.json",
        dict(files=files, frozen_inputs=frozen, manifest_self_hash_excluded=True),
    )
    print(
        "PASS independent prefix source audit",
        len(auditor.array_scans),
        "actual arrays",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_root, args.output)
