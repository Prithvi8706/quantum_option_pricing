"""Independent actual-gate coefficient audit with actual per-case presence.

No circuit builder is imported, and no emitted gate or pricing path is replayed.
The coefficient identities, six actual circuit structures, complete accounting,
prospective stopping decisions and saved financial receipts are checked here.
The global top-three frontier is matched across the union of actual cases;
an absent coefficient cannot require an invented case-local source entry.
The first auditor and failed A01_run013 receipt remain frozen.
"""

from __future__ import annotations

# ruff: noqa: E501

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import shutil
import sys
import time

import numpy as np

from research.limitation_program_20261001.baseline import ROOT, dump, environment, load, sha
from research.limitation_program_20261001.reconcile_constants import (
    ORIGINAL,
    library_path,
    relative,
)
from research.limitation_program_20261001.reconcile_nonrestoring_v2 import scan, xml_receipts
from research.limitation_program_20261001.reconcile_range import (
    Auditor,
    structure as range_structure,
)
from research.limitation_program_20261001.reconcile_shift import eligibility
from research.limitation_program_20261001.reconcile_sqrt import (
    check_manifest,
    independently_pack,
    input_files,
)

BASELINE = ROOT / "results/limitation_program_20261001/A09_range_run001"
FAILED_AUDIT = ROOT / "results/limitation_program_20261001/A01_run013"
CASES = ("B4x12", "B8x52")
CAPS = {"B4x12": 550141, "B8x52": 4460479}
COEFFICIENTS = (1067016148260, 60222732077, 22906492245)
PORTFOLIOS = ("min-depth", "min-work")
STRATEGIES = (
    "binary-shift-add",
    "signed-digit-shift-add",
    "binary-carry-save",
    "signed-digit-carry-save",
    "binary-prefix-carry-save",
    "signed-digit-prefix-carry-save",
)
DIMENSIONS = ("t_count", "t_depth", "clifford_t_depth", "qubits")


def digits(coefficient, form):
    """Integer expansion proved here independently of the producer module."""
    assert type(coefficient) is int and form in ("binary", "signed-digit")
    polarity, magnitude = (-1 if coefficient < 0 else 1), abs(coefficient)
    if form == "binary":
        result = [
            (bit, polarity) for bit in range(magnitude.bit_length()) if magnitude & (1 << bit)
        ]
    else:
        result, position, remainder = [], 0, magnitude
        while remainder:
            if remainder % 2:
                digit = 1 if remainder % 4 == 1 else -1
                result.append((position, polarity * digit))
                remainder -= digit
            remainder //= 2
            position += 1
    assert sum(sign * (1 << bit) for bit, sign in result) == coefficient
    assert all(sign in (-1, 1) and type(bit) is int and bit >= 0 for bit, sign in result)
    if form == "signed-digit":
        assert all(right[0] - left[0] > 1 for left, right in zip(result, result[1:]))
    return result


def arithmetic_certificate():
    checks = negative = tiny_negative = 0

    def check(width, fraction, coefficient, value, form):
        nonlocal checks, negative, tiny_negative
        n, modulus = width + fraction, 1 << (width + fraction)
        raw, correction, plane = value % (1 << width), 0, 0
        for position, digit in digits(coefficient, form):
            for index in range(min(width, max(0, n - position))):
                column = position + index
                bit = (raw >> index) & 1
                weight = -digit if index == width - 1 else digit
                if weight < 0:
                    plane += (1 - bit) << column
                    correction -= 1 << column
                else:
                    plane += bit << column
        encoded = (plane + correction % modulus) % modulus
        assert encoded == value * coefficient % modulus
        assert (encoded >> fraction) == (value * coefficient // (1 << fraction)) % (1 << width)
        negative += value * coefficient < 0
        tiny_negative += -(1 << fraction) < value * coefficient < 0
        checks += 1

    for width in range(1, 7):
        for fraction in range(width + 1):
            for coefficient in range(-15, 16):
                for value in range(-(1 << (width - 1)), 1 << (width - 1)):
                    for form in ("binary", "signed-digit"):
                        check(width, fraction, coefficient, value, form)
    rng = random.Random(0xA10C057)
    edges = (
        -(1 << 71),
        -(1 << 71) + 1,
        -((1 << 40) + 1),
        -(1 << 40),
        -1,
        0,
        1,
        (1 << 40) - 1,
        1 << 40,
        (1 << 71) - 2,
        (1 << 71) - 1,
    )
    for coefficient in COEFFICIENTS:
        for value in edges + tuple(rng.randrange(-(1 << 71), 1 << 71) for _ in range(32)):
            for form in ("binary", "signed-digit"):
                check(72, 40, coefficient, value, form)
    assert negative and tiny_negative
    return dict(
        passed=True,
        finite_bookkeeping_inputs=checks,
        negative_products=negative,
        tiny_negative_products=tiny_negative,
        coefficient_identity="Each binary or nonadjacent signed-digit expansion sums exactly to c; no coefficient rounding occurs",
        signed_identity="signed(x)=sum(low xi*2**i)-x_sign*2**(w-1); distributing exact coefficient digits yields each signed bit weight",
        complement_identity="For t in {0,1}, -t*2**column=(1-t)*2**column-2**column. Corrections are reduced modulo the full 2**(w+f), never only an active product width",
        carry_identity="Fresh sum=x XOR y XOR z; carry=(x AND y) XOR ((x XOR y) AND z). Carry terms are disjoint; sum+2*carry=x+y+z. Every low column is retained",
        prefix_identity="Pair (G,P) satisfies G*P=0; concatenation produces (Gh XOR Ph*Gl, Ph*Pl), and result bit is propagate XOR preceding G",
        ripple_identity="Cuccaro MAJ/UMA gives modular addition, preserves the addend and restores its zero helper; reversal gives modular subtraction",
        slice_identity="For all integer products p, (p mod2**(w+f)) >> f equals floor(p/2**f) mod2**w, including tiny negative products",
        cleanup="Native input/output full width; output XOR occurs between actual compute and its literal reverse. Retained partial/correction/compressor/prefix scratch is fully counted",
        unrestricted_signed_native_input=True,
        all_input_algebraic_identity=True,
        proof_scope="Algebra covers all signed native inputs. Finite arithmetic and saved emitted tests check realization; no exhaustive72-bit, continuous-dollar or advantage certification",
    )


def expected_spec(width, fraction, coefficient, strategy):
    """Filled from the prospectively fixed schema, without a producer import."""
    spec = dict(
        op="cmul",
        width=width,
        fraction_bits=fraction,
        params={"c": coefficient},
        strategy=strategy,
        zero_bits=0,
        input_contract={"zero_low_bits": 0},
        coefficient_frontier="full-native-unrestricted-signed-v1",
    )
    if "prefix" not in strategy:
        spec.update(coefficient=coefficient, lowering="signed-constant-zero-low-v1")
    else:
        spec.update(
            variant="brent-kung",
            lowering="signed-constant-complement-csa-prefix-final-v1",
            algorithm="full-domain-signed-constant-planes-brent-kung",
            product_width=width + fraction,
            digit_form="binary" if strategy.startswith("binary-") else "signed-digit",
            domain="all native signed input words; no narrowed or zero-low promise",
            signed_partial_rule="digit polarity times native two's-complement bit weight",
            negative_bit_encoding="complement plus fixed negative weight correction",
            correction_modulus="full native width plus fractional width",
            discarded_low_columns="retained through CSA and final prefix carry",
            cleanup="native output XOR; literal inverse of complete compute",
        )
    return spec


def structure(entry, path):
    """Parse all actual coefficient gates without generating a circuit."""
    assert sha(path) == entry["sha256"]
    spec = entry["spec"]
    width, fraction, coefficient, strategy = (
        spec["width"],
        spec["fraction_bits"],
        spec["params"]["c"],
        spec["strategy"],
    )
    assert (width, fraction) == (72, 40) and coefficient in COEFFICIENTS and strategy in STRATEGIES
    canonical = expected_spec(width, fraction, coefficient, strategy)
    if "integration_lowering" in spec:
        canonical["integration_lowering"] = "same-target-full-domain-coefficient-library-v1"
    assert spec == canonical, (spec, canonical)
    assert (
        entry["key"]
        == hashlib.sha256(
            json.dumps(canonical, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        ).hexdigest()[:20]
    )
    assert entry["op"] == "cmul" and entry["params"] == {"c": coefficient}
    assert (
        entry["input_contract"] == {"zero_low_bits": 0}
        and type(entry["input_contract"]["zero_low_bits"]) is int
    )
    assert entry["coefficient_frontier"] == "full-native-unrestricted-signed-v1"
    assert entry["args"] == [list(range(width))] and entry["outs"] == [
        list(range(width, 2 * width))
    ]
    assert all(type(wire) is int for register in entry["args"] + entry["outs"] for wire in register)
    gates = np.load(path, mmap_mode="r")
    assert (len(gates) - width) % 2 == 0
    half = (len(gates) - width) // 2
    before, copied, after = gates[:half], gates[half : half + width], gates[half + width :]
    assert np.array_equal(before, after[::-1])
    assert not np.isin(before[:, 1:], np.arange(width, 2 * width)).any()
    cursor, position, n = 2 * width, 0, width + fraction

    def allocate(size):
        nonlocal cursor
        result = list(range(cursor, cursor + size))
        cursor += size
        return result

    def expect(wires):
        nonlocal position
        row = before[position]
        assert int(row[0]) == len(wires) and tuple(map(int, row[1 : 1 + len(wires)])) == tuple(
            wires
        ), (position, row.tolist(), wires)
        assert wires[-1] >= 2 * width, ("Native input/output targeted by compute", position)
        position += 1

    def ripple(left, right, helper, subtract=False):
        pattern = []

        def maj(x, y, z):
            pattern.extend(((x, y), (x, z), (z, y, x)))

        def uma(x, y, z):
            pattern.extend(((z, y, x), (x, z), (z, y)))

        maj(left[0], right[0], helper)
        for bit in range(len(left) - 1):
            maj(left[bit + 1], right[bit + 1], left[bit])
        for bit in reversed(range(len(left) - 1)):
            uma(left[bit + 1], right[bit + 1], left[bit])
        uma(left[0], right[0], helper)
        for wires in reversed(pattern) if subtract else pattern:
            expect(wires)

    form = "binary" if strategy.startswith("binary-") else "signed-digit"
    expanded = digits(coefficient, form)
    partials = negatives = correction_wires = layers = compressors = prefix_nodes = 0
    correction = 0
    if strategy.endswith("shift-add"):
        product, extended = allocate(n), allocate(n)
        helper = allocate(1)[0]
        for bit, wire in enumerate(extended):
            expect((min(bit, width - 1), wire))
        for column, digit in expanded:
            if column < n:
                ripple(extended[: n - column], product[column:], helper, digit < 0)
    else:
        columns = [[] for _ in range(n)]
        for shift, digit in expanded:
            for bit in range(min(width, max(0, n - shift))):
                wire, column = allocate(1)[0], shift + bit
                weight_sign = -digit if bit == width - 1 else digit
                if weight_sign < 0:
                    expect((wire,))
                    correction -= 1 << column
                    negatives += 1
                expect((bit, wire))
                columns[column].append(wire)
                partials += 1
        correction %= 1 << n
        for column in range(n):
            if correction & (1 << column):
                wire = allocate(1)[0]
                expect((wire,))
                columns[column].append(wire)
                correction_wires += 1
        while max(map(len, columns)) > 2:
            following = [[] for _ in range(n)]
            for column, values in enumerate(columns):
                consumed = 0
                for offset in range(0, len(values) - 2, 3):
                    x, y, z = values[offset : offset + 3]
                    summed = allocate(1)[0]
                    expect((x, summed))
                    expect((y, summed))
                    if column + 1 < n:
                        carry = allocate(1)[0]
                        expect((x, y, carry))
                        expect((summed, z, carry))
                        following[column + 1].append(carry)
                    expect((z, summed))
                    following[column].append(summed)
                    consumed = offset + 3
                    compressors += 1
                following[column].extend(values[consumed:])
            columns, layers = following, layers + 1
        if "prefix" not in strategy:
            left, product = allocate(n), allocate(n)
            helper = allocate(1)[0]
            for column, values in enumerate(columns):
                if values:
                    expect((values[0], left[column]))
                if len(values) == 2:
                    expect((values[1], product[column]))
            ripple(left, product, helper)
        else:
            left, right, product = (allocate(n) for _ in range(3))
            for column, values in enumerate(columns):
                if values:
                    expect((values[0], left[column]))
                if len(values) == 2:
                    expect((values[1], right[column]))
            propagate, generate = allocate(n), allocate(n - 1)
            prefix_start = position
            for bit in range(n):
                expect((left[bit], propagate[bit]))
                expect((right[bit], propagate[bit]))
                if bit < n - 1:
                    expect((left[bit], right[bit], generate[bit]))
            pairs = list(zip(generate, propagate[: n - 1]))

            def compose(high, low):
                nonlocal prefix_nodes
                g, p = allocate(2)
                gh, ph = high
                gl, pl = low
                expect((gh, g))
                expect((ph, gl, g))
                expect((ph, pl, p))
                prefix_nodes += 1
                return g, p

            distance = 1
            while distance < len(pairs):
                previous, updated = pairs, pairs.copy()
                for bit in range(2 * distance - 1, len(pairs), 2 * distance):
                    updated[bit] = compose(previous[bit], previous[bit - distance])
                pairs, distance = updated, distance * 2
            distance //= 4
            while distance >= 1:
                previous, updated = pairs, pairs.copy()
                for bit in range(3 * distance - 1, len(pairs), 2 * distance):
                    updated[bit] = compose(previous[bit], previous[bit - distance])
                pairs, distance = updated, distance // 2
            prefix_end = position
            for bit, target in enumerate(product):
                expect((propagate[bit], target))
                if bit:
                    expect((pairs[bit - 1][0], target))
            reverse_count = prefix_end - prefix_start
            assert np.array_equal(
                before[position : position + reverse_count], before[prefix_start:prefix_end][::-1]
            )
            position += reverse_count
    assert position == half
    assert np.array_equal(copied[:, 0], np.full(width, 2))
    assert np.array_equal(copied[:, 1], product[fraction : fraction + width])
    assert np.array_equal(copied[:, 2], np.arange(width, 2 * width))
    assert cursor == entry["resources"]["qubits"]
    return dict(
        passed=True,
        coefficient=coefficient,
        strategy=strategy,
        exact_digits=[list(v) for v in expanded],
        parsed_forward_gates=half,
        full_modular_product_bits=n,
        signed_bit_terms=partials,
        complemented_negative_terms=negatives,
        fixed_full_modulus_correction=correction,
        charged_correction_wires=correction_wires,
        csa_layers=layers,
        compressors=compressors,
        prefix_nodes=prefix_nodes,
        every_low_column_and_carry_retained=True,
        unrestricted_signed_input_bits=width,
        full_native_output_bits=width,
        native_input_untouched=True,
        arbitrary_output_xor=True,
        literal_forward_reverse_cleanup=True,
        qubits=cursor,
        algorithm="independent exact digits, Cuccaro/CSA/Brent-Kung actual-gate parser",
    )


def dominated(resources, alternatives, dimensions=DIMENSIONS):
    return any(
        all(other[d] <= resources[d] for d in dimensions)
        and any(other[d] < resources[d] for d in dimensions)
        for other in alternatives
    )


def leaf_decision(resources, baseline, siblings):
    is_dominated = dominated(resources, [baseline] + list(siblings))
    improves = any(resources[d] < baseline[d] for d in DIMENSIONS)
    work_or_scratch = (
        resources["t_count"] < baseline["t_count"] or resources["qubits"] < baseline["qubits"]
    )
    return dict(
        leaf_nondominated=not is_dominated,
        any_resource_improvement=improves,
        clean_leaf_work_or_scratch_improved=work_or_scratch,
        source_screen_allowed=not is_dominated and improves and work_or_scratch,
    )


def portfolio_maps(eligible):
    """At most two prospectively specified coefficient-wise tie-break policies."""
    result = {name: {} for name in PORTFOLIOS}
    for coefficient in COEFFICIENTS:
        available = [entry for (c, _), entry in eligible.items() if c == coefficient]
        for name in PORTFOLIOS:
            if not available:
                continue
            dimensions = (
                ("t_depth", "t_count", "clifford_t_depth", "qubits")
                if name == "min-depth"
                else ("t_count", "qubits", "t_depth", "clifford_t_depth")
            )
            selected = min(
                available,
                key=lambda entry: (
                    tuple(entry["resources"][d] for d in dimensions)
                    + (STRATEGIES.index(entry["spec"]["strategy"]),)
                ),
            )
            result[name][str(coefficient)] = selected["spec"]["strategy"]
    emitted = []
    for name in PORTFOLIOS:
        if result[name] and all(result[name] != result[other] for other in emitted):
            emitted.append(name)
    return result, emitted


def inventory(auditor, ledgers):
    """Reconstruct the fixed owner ranking and all declared sites independently."""
    cases, combined = {}, Counter()
    for case in CASES:
        source = load(BASELINE / case / "source.json")
        target = load(BASELINE / case / "target.json")
        entries = auditor.leafs(source)
        owners = Counter()
        for batch in ledgers[case]["batches"]:
            entry = entries[batch["dominant_leaf"]]
            if entry["op"] == "cmul":
                coefficient = entry["params"]["c"]
                owners[coefficient] += 2 * batch["t_depth"]
                combined[coefficient] += 2 * batch["t_depth"]
        nodes = [node for node in target["nodes"] if node["op"] != "input"]
        sites = []
        for index, (node, call) in enumerate(zip(nodes, source["forward_calls"], strict=True)):
            coefficient = node["params"].get("c")
            if node["op"] == "cmul" and coefficient in COEFFICIENTS:
                entry = entries[call["leaf"]]
                sites.append(
                    dict(
                        call_index=index,
                        coefficient=coefficient,
                        args=call["args"],
                        out=call["out"],
                        leaf=call["leaf"],
                        gate_sha256=entry["sha256"],
                    )
                )
        schedule = load(BASELINE / case / "schedule_capped.json")
        ceilings = {}
        for coefficient in COEFFICIENTS:
            without = 0
            for group in schedule["groups"]:
                alternatives = [
                    entries[source["forward_calls"][index]["leaf"]]
                    for index in group["call_indices"]
                ]
                without += 2 * max(
                    (
                        entry["resources"]["t_depth"]
                        for entry in alternatives
                        if not (entry["op"] == "cmul" and entry["params"]["c"] == coefficient)
                    ),
                    default=0,
                )
            ceilings[str(coefficient)] = schedule["resources"]["t_depth"] - without
        cases[case] = dict(
            actual_declared_sites=sites,
            optimistic_fixed_batch_zero_cost_saving=ceilings,
            accepted_full_t_depth=schedule["resources"]["t_depth"],
            constant_depth_owners=[
                dict(coefficient=c, owned_t_depth=value)
                for c, value in sorted(owners.items(), key=lambda row: (-row[1], row[0]))
            ],
        )
    ranking = sorted(combined, key=lambda c: (-combined[c], c))
    assert tuple(ranking[:3]) == COEFFICIENTS
    assert all(
        any(
            1000 * row["optimistic_fixed_batch_zero_cost_saving"][str(c)]
            >= row["accepted_full_t_depth"]
            for row in cases.values()
        )
        for c in COEFFICIENTS
    )
    return dict(
        cases=cases,
        combined_ranking=[dict(coefficient=c, owned_t_depth=combined[c]) for c in ranking],
        selected_coefficients=list(COEFFICIENTS),
    )


def source_changes(auditor, source_root, leaf_entries, replacements, case, portfolio):
    directory = source_root / case / portfolio
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
        assert before[field] == after[field], field
    old_entries, new_entries = auditor.leafs(before), auditor.leafs(after)
    old_archive, new_archive = library_path(before), library_path(after)
    noninputs = [i for i, node in enumerate(target["nodes"]) if node["op"] != "input"]
    changed, unchanged, structures, coefficients = [], set(), {}, Counter()
    assert len(before["forward_calls"]) == len(after["forward_calls"]) == len(noninputs)
    for call_index, (old, new) in enumerate(
        zip(before["forward_calls"], after["forward_calls"], strict=True)
    ):
        assert {k: v for k, v in old.items() if k != "leaf"} == {
            k: v for k, v in new.items() if k != "leaf"
        }
        old_entry, new_entry = old_entries[old["leaf"]], new_entries[new["leaf"]]
        node = target["nodes"][noninputs[call_index]]
        coefficient = node["params"].get("c") if node["op"] == "cmul" else None
        strategy = replacements.get(str(coefficient))
        assert (old["leaf"] != new["leaf"]) == (strategy is not None), (
            case,
            portfolio,
            call_index,
            coefficient,
        )
        if strategy is None:
            key = old["leaf"]
            if key not in unchanged:
                assert sha(old_archive / (key + ".json")) == sha(new_archive / (key + ".json"))
                assert sha(old_archive / old_entry["gate_file"]) == sha(
                    new_archive / new_entry["gate_file"]
                )
                unchanged.add(key)
            continue
        assert coefficient in COEFFICIENTS and node["params"] == {"c": coefficient}
        assert len(node["args"]) == len(node["out"]) == 1
        leaf_entry = leaf_entries[coefficient, strategy]
        assert (
            new_entry["resources"] == leaf_entry["resources"]
            and new_entry["sha256"] == leaf_entry["sha256"]
        )
        assert {
            k: v for k, v in new_entry["spec"].items() if k != "integration_lowering"
        } == leaf_entry["spec"]
        if new["leaf"] not in structures:
            structures[new["leaf"]] = structure(new_entry, new_archive / new_entry["gate_file"])
        coefficients[coefficient] += 1
        changed.append(
            dict(
                call_index=call_index,
                args=new["args"],
                out=new["out"],
                old_key=old["leaf"],
                new_key=new["leaf"],
                op="cmul",
                params={"c": coefficient},
                old_resources=old_entry["resources"],
                new_resources=new_entry["resources"],
                input_contract=new_entry["input_contract"],
            )
        )
    assert load(directory / "changed_calls.json") == dict(
        changes=changed, unchanged_leaf_keys=sorted(unchanged)
    )
    decisions = load(directory / "site_decisions.json")
    assert len(decisions) == len(after["forward_calls"])
    assert {row["forward_call_index"] for row in decisions} == set(
        range(len(after["forward_calls"]))
    )
    for row in decisions:
        index = row["forward_call_index"]
        assert row["node_index"] == noninputs[index]
        node = target["nodes"][row["node_index"]]
        assert row["outputs"] == node["out"] and row["op"] == node["op"]
        assert row["old_key"] == before["forward_calls"][index]["leaf"]
        assert row["new_key"] == after["forward_calls"][index]["leaf"]
        if row["old_key"] != row["new_key"]:
            assert row["type"] == "coefficient-full-domain"
            proof = row["proof"]
            coefficient = node["params"]["c"]
            assert (
                proof["coefficient"] == coefficient
                and proof["strategy"] == replacements[str(coefficient)]
            )
            assert proof["input_contract"] == {"zero_low_bits": 0}
            assert (
                proof["no_narrowed_input_promise"] is True
                and proof["all_native_signed_patterns"] is True
            )
            assert (
                proof["theorem"] == "Exact floor(signed(x) * c / 2**fraction_bits), modulo 2**width"
            )
        else:
            assert row["type"] == "fallback"
    schedule, old_schedule = (
        load(path / "schedule_capped.json") for path in (directory, BASELINE / case)
    )
    assert schedule["format"] == "compact-clean-xor-capped-wave-schedule-v7"
    for field in (
        "widths",
        "offsets",
        "retained_ssa_qubits",
        "proof_masks",
        "proof_reasons",
        "argument_and_output_copy_cx",
        "baseline_argument_and_output_copy_cx",
    ):
        assert schedule[field] == old_schedule[field], (case, portfolio, field)
    independently_pack(after, new_entries, schedule)
    improved = all(
        row["new_resources"]["t_count"] < row["old_resources"]["t_count"]
        or row["new_resources"]["qubits"] < row["old_resources"]["qubits"]
        for row in changed
    )
    return dict(
        changed_calls=len(changed),
        changed_coefficient_counts=[
            dict(coefficient=c, calls=count) for c, count in sorted(coefficients.items())
        ],
        unchanged_leaf_keys=len(unchanged),
        structural_leaf_proofs=structures,
        unrestricted_native_signed_input=True,
        storage_and_copy_allocation_unchanged=True,
        preserved_range_root_shift_lookup_metadata_and_gates=True,
        exact_first_fit_groups_recomputed=True,
        clean_leaf_work_or_scratch_improved=bool(changed) and improved,
    )


def freeze(leaf_root, source_root):
    frozen = {}
    roots = [BASELINE, leaf_root, FAILED_AUDIT] + ([source_root] if source_root else [])
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
    emitted = load(source_root / "protocol.json")["emitted_family"] if source_root else []
    for case in CASES:
        for path in input_files(BASELINE / case):
            frozen[relative(path)] = sha(path)
        if source_root:
            for portfolio in emitted:
                for path in input_files(source_root / case / portfolio):
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
        "research.limitation_program_20261001.reconcile_nonrestoring_v2",
        "research.limitation_program_20261001.reconcile_range",
        "research.limitation_program_20261001.compact_ledger",
    ):
        path = Path(sys.modules[name].__file__)
        frozen[relative(path)] = sha(path)
    frozen[relative(Path(__file__))] = sha(Path(__file__))
    first_auditor = Path(__file__).with_name("reconcile_coefficients.py")
    assert sha(first_auditor) == sha(FAILED_AUDIT / "executed_code/reconcile_coefficients.py")
    frozen[relative(first_auditor)] = sha(first_auditor)
    return frozen


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
            preserved_failed_audit=relative(FAILED_AUDIT),
            corrected_audit_assumption="The coefficient frontier is global across cases; require one matched leaf only where the immutable actual target contains that coefficient, and zero where it is absent. The union must still contain exactly the fixed three coefficients",
            frozen_inputs=frozen,
            producer_sha256=sha(Path(__file__)),
            family=list(PORTFOLIOS),
            coefficients=list(COEFFICIENTS),
            strategies=list(STRATEGIES),
            width=72,
            fraction_bits=40,
            scope="Read-only independent exact digit identities, all six actual circuit structures, complete capped costs, sibling and source frontiers and saved financial receipts; no new gate or financial replay",
            selection="Same-coefficient baseline and all six siblings define the leaf frontier; any improvement and T-work or scratch improvement against baseline required. At most two distinct deterministic source replacement maps, >=2% T-depth in each case, CT-depth<=baseline, actual caps and no full-source domination. Minimize sum T-depth, sum T-count, sum qubits, declared order",
            no_new_emitted_replays=True,
            G2_G5="unresolved",
        ),
    )
    dump(output / "environment.json", environment())
    executed = output / "executed_code"
    executed.mkdir()
    shutil.copyfile(Path(__file__), executed / "reconcile_coefficients_v2.py")
    certificate = arithmetic_certificate()
    dump(output / "coefficient_arithmetic_certificate.json", certificate)
    leaf_summary, leaf_protocol = (
        load(leaf_root / name) for name in ("summary.json", "protocol.json")
    )
    assert leaf_summary["passed"] and leaf_protocol["local_only"] is True
    assert (leaf_protocol["width"], leaf_protocol["fraction_bits"]) == (72, 40)
    assert leaf_protocol["coefficients"] == list(COEFFICIENTS)
    assert leaf_protocol["strategies"] == list(STRATEGIES)
    assert leaf_protocol["resource_dimensions"] == list(DIMENSIONS)
    assert (ROOT / leaf_protocol["baseline"]).resolve() == BASELINE.resolve()
    verification = load(leaf_root / "verification.json")
    assert verification["passed"] and verification["pytest_exit_code"] == 0
    auditor = Auditor(frozen)
    baseline_ledgers = {case: auditor.costs(case, BASELINE / case) for case in CASES}
    independent_inventory = inventory(auditor, baseline_ledgers)
    assert load(leaf_root / "coefficient_inventory.json") == independent_inventory
    assert leaf_protocol["inventory"] == independent_inventory
    dump(output / "coefficient_inventory_audit.json", independent_inventory)
    matched = {}
    actual_case_presence = {}
    preserved_range = {}
    for case in CASES:
        source = load(BASELINE / case / "source.json")
        target = load(BASELINE / case / "target.json")
        archive = library_path(source)
        entries = auditor.leafs(source)
        assert baseline_ledgers[case]["resources"]["logical_qubits"] == CAPS[case]
        declared_calls = Counter(
            node["params"]["c"]
            for node in target["nodes"]
            if node["op"] == "cmul" and node["params"].get("c") in COEFFICIENTS
        )
        actual_case_presence[case] = {str(c): declared_calls[c] for c in COEFFICIENTS}
        for coefficient in COEFFICIENTS:
            matches = [
                entry
                for entry in entries.values()
                if entry["op"] == "cmul" and entry["params"] == {"c": coefficient}
            ]
            assert len(matches) == int(declared_calls[coefficient] > 0), (
                "Case-local coefficient leaves must match actual target presence",
                case,
                coefficient,
                declared_calls[coefficient],
                len(matches),
            )
            if not matches:
                continue
            assert not matches[0].get("input_contract")
            entry = matches[0]
            if coefficient in matched:
                assert matched[coefficient]["resources"] == entry["resources"]
                assert matched[coefficient]["sha256"] == entry["sha256"]
            else:
                matched[coefficient] = entry
        for key, entry in entries.items():
            if (
                entry.get("input_contract", {}).get("signed_operand_bits")
                and key not in preserved_range
            ):
                preserved_range[key] = range_structure(entry, archive / entry["gate_file"])
    assert set(matched) == set(COEFFICIENTS), (
        "Every globally declared coefficient must occur in at least one actual case"
    )
    assert leaf_summary["baseline_coefficients"] == {
        str(c): matched[c]["resources"] for c in COEFFICIENTS
    }
    all_entries, leaf_rows = {}, []
    assert [(row["coefficient"], row["strategy"]) for row in leaf_summary["candidates"]] == [
        (c, s) for c in COEFFICIENTS for s in STRATEGIES
    ]
    for row in leaf_summary["candidates"]:
        coefficient, strategy, entry = row["coefficient"], row["strategy"], row["metadata"]
        assert (
            type(coefficient) is int
            and entry["params"] == {"c": coefficient}
            and entry["spec"]["strategy"] == strategy
        )
        matches = [path for path in leaf_root.rglob(entry["key"] + ".json") if load(path) == entry]
        assert len(matches) == 1
        path = matches[0].parent / entry["gate_file"]
        scanned, parsed = scan(entry, path), structure(entry, path)
        auditor.array_scans[entry["sha256"], entry["resources"]["qubits"]] = scanned
        all_entries[coefficient, strategy] = entry
        leaf_rows.append(
            dict(
                coefficient=coefficient,
                strategy=strategy,
                actual_gate_scan=scanned,
                structural_parser=parsed,
            )
        )
    eligible_entries = {}
    for row, audited in zip(leaf_summary["candidates"], leaf_rows, strict=True):
        coefficient, strategy, entry = row["coefficient"], row["strategy"], row["metadata"]
        decision = leaf_decision(
            entry["resources"],
            matched[coefficient]["resources"],
            [other["resources"] for (c, _), other in all_entries.items() if c == coefficient],
        )
        for key, expected in decision.items():
            assert row[key] == expected, (coefficient, strategy, key, row[key], expected)
        audited["decision"] = decision
        if decision["source_screen_allowed"]:
            eligible_entries[coefficient, strategy] = entry
    assert leaf_summary["source_screen_allowed"] == bool(eligible_entries)
    assert (
        not leaf_summary["financial_gate_replays_run"] and not leaf_summary["source_gain_claimed"]
    )
    assert bool(source_root) == bool(eligible_entries)
    replacements, emitted = portfolio_maps(eligible_entries)
    dump(
        output / "leaf_audit.json",
        dict(
            passed=True,
            baseline_coefficients={str(c): matched[c]["resources"] for c in COEFFICIENTS},
            actual_case_coefficient_call_counts=actual_case_presence,
            candidates=leaf_rows,
            eligible_candidates=[dict(coefficient=c, strategy=s) for c, s in eligible_entries],
            preserved_actual_range_leaf_parsers=preserved_range,
            portfolio_replacements=replacements,
            emitted_family=emitted,
        ),
    )
    selected, final_cases, trials = None, [], {}
    if source_root:
        summary, protocol = (load(source_root / name) for name in ("summary.json", "protocol.json"))
        assert summary["passed"] and protocol["family"] == list(PORTFOLIOS)
        assert (ROOT / protocol["baseline"]).resolve() == BASELINE.resolve()
        assert protocol["threshold_percent"] == 2 and protocol["coefficients"] == list(COEFFICIENTS)
        assert protocol["strategies"] == list(STRATEGIES)
        assert (
            protocol["portfolio_replacements"] == replacements
            and protocol["emitted_family"] == emitted
        )
        assert protocol["cases"] == list(CASES) and protocol["cpu_limit_seconds"] == 1800
        assert protocol["local_only"] is True and summary["cpu_seconds"] <= 1800
        for name, digest in protocol["baseline_hashes"].items():
            assert sha(BASELINE / name) == digest
        for name, digest in protocol["baseline_leaf_hashes"].items():
            assert sha(ROOT / name) == digest
        baseline_summary = load(BASELINE / "summary.json")
        assert protocol["replay_inputs"] == {
            row["case"]: row["replays"] for row in baseline_summary["cases"]
        }
        assert sha(leaf_root / "manifest.json") == protocol["leaf_receipt_manifest_sha256"]
        for case in CASES:
            comparison = next(row for row in summary["cases"] if row["case"] == case)
            assert comparison == load(source_root / case / "comparison.json")
            screens = load(source_root / case / "screen.json")
            assert (
                screens == comparison["trials"] and [row["variant"] for row in screens] == emitted
            )
            baseline = baseline_ledgers[case]["resources"]
            assert comparison["baseline"] == baseline
            for row in screens:
                portfolio = row["variant"]
                attribution = source_changes(
                    auditor, source_root, eligible_entries, replacements[portfolio], case, portfolio
                )
                ledger = auditor.costs(case, source_root / case / portfolio)
                assert row["resources"] == ledger["resources"] and ledger["qubit_cap"] == CAPS[case]
                eligible = eligibility(
                    ledger["resources"],
                    baseline,
                    CAPS[case],
                    attribution["clean_leaf_work_or_scratch_improved"],
                )
                assert (
                    row["eligible"] == eligible
                    and row["changed_calls"] == attribution["changed_calls"]
                )
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
                    variant=portfolio,
                    eligible=eligible,
                    changes=attribution,
                    baseline_resources=baseline,
                )
                trials[case, portfolio] = ledger
                dump(output / (case + "_" + portfolio + "_trial_ledger.json"), ledger)

        def source_dominated(portfolio):
            dimensions = ("t_count", "t_depth", "clifford_t_depth", "logical_qubits")
            return any(
                other != portfolio
                and all(
                    trials[case, other]["resources"][d] <= trials[case, portfolio]["resources"][d]
                    for case in CASES
                    for d in dimensions
                )
                and any(
                    trials[case, other]["resources"][d] < trials[case, portfolio]["resources"][d]
                    for case in CASES
                    for d in dimensions
                )
                for other in emitted
            )

        nondominated = [portfolio for portfolio in emitted if not source_dominated(portfolio)]
        for comparison in summary["cases"]:
            for row in comparison["trials"]:
                assert row["source_nondominated"] == (row["variant"] in nondominated)
        frontier = load(source_root / "coefficient_frontier.json")
        assert frontier["nondominated"] == nondominated and frontier["variants"] == emitted
        candidates = [
            portfolio
            for portfolio in emitted
            if all(trials[case, portfolio]["eligible"] for case in CASES)
            and not source_dominated(portfolio)
        ]
        selected = (
            min(
                candidates,
                key=lambda portfolio: (
                    tuple(
                        sum(trials[case, portfolio]["resources"][d] for case in CASES)
                        for d in ("t_depth", "t_count", "logical_qubits")
                    )
                    + (PORTFOLIOS.index(portfolio),)
                ),
            )
            if candidates
            else None
        )
        assert summary["selected"] == selected and summary["accepted"] == bool(selected)
        assert summary["financial_gate_replays_run"] == bool(selected)
        for case in CASES:
            comparison = next(row for row in summary["cases"] if row["case"] == case)
            if selected:
                trial = trials[case, selected]
                chosen = next(row for row in comparison["trials"] if row["variant"] == selected)
                assert (
                    comparison["selected"] == chosen
                    and comparison["candidate"] == trial["resources"]
                )
                assert comparison["replay_passed"] and comparison["accepted"]
                prior = next(row for row in baseline_summary["cases"] if row["case"] == case)[
                    "replays"
                ]
                assert len(comparison["replays"]) == len(prior)
                for replay, old in zip(comparison["replays"], prior, strict=True):
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
                assert not comparison.get("replay_passed", False)
                assert not (source_root / case / "source.json").exists()
                final, effective = baseline_ledgers[case], BASELINE / case
            final_cases.append(
                dict(final, effective_source=relative(effective), selected_variant=selected)
            )
        source_verification = load(source_root / "verification.json")
        assert source_verification["passed"] and source_verification["pytest_exit_code"] == 0
        replay_count = sum(len(row["replays"]) for row in baseline_summary["cases"])
        assert replay_count == 4
        assert sum(len(row["replays"]) for row in summary["cases"]) == (
            replay_count if selected else 0
        )
    else:
        assert not emitted
        final_cases = [
            dict(
                baseline_ledgers[case],
                effective_source=relative(BASELINE / case),
                selected_variant=None,
            )
            for case in CASES
        ]
    for row in final_cases:
        dump(output / (row["case"] + "_accepted_ledger.json"), row)
    receipts = xml_receipts([leaf_root] + ([source_root] if source_root else []))
    next_action = (
        "Use the accepted full-source owner ranking for the next bounded local limitation. Keep G2-G5 open and everything local."
        if selected
        else "Retain A09_range_run001. Preserve exact coefficient leaves and the measured stopping result, then move to the next bounded limitation under a fresh protocol. Keep G2-G5 open."
    )
    result = dict(
        passed=True,
        decision="independent_full_domain_coefficient_frontier_audit",
        accepted=bool(selected),
        selected=selected,
        source_root=relative(source_root) if source_root else None,
        leaf_root=relative(leaf_root),
        baseline=relative(BASELINE),
        source_screen_run=bool(source_root),
        coefficients=list(COEFFICIENTS),
        actual_case_coefficient_call_counts=actual_case_presence,
        eligible_candidates=[dict(coefficient=c, strategy=s) for c, s in eligible_entries],
        portfolio_replacements=replacements,
        emitted_family=emitted,
        cases=final_cases,
        trials=list(trials.values()),
        actual_unique_gate_arrays_scanned=len(auditor.array_scans),
        metadata_locations_checked=len(auditor.leaf_cache) + len(all_entries),
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
    command = [
        str(Path(sys.executable).resolve()),
        "-m",
        "research.limitation_program_20261001.reconcile_coefficients_v2",
        "--leaf-root",
        relative(leaf_root),
        "--output",
        relative(output),
    ] + (["--source-root", relative(source_root)] if source_root else [])
    dump(
        output / "verification.json",
        dict(
            passed=True,
            producer_sha256=sha(Path(__file__)),
            command=command,
            checks=[
                "Frozen receipts and executed code",
                "Independent binary/NAF signed polynomial, full-modulus complement, carry and slice identities",
                "All six actual coefficient circuit strategies, native XOR copy and literal inverse",
                "Same-coefficient sibling frontier and deterministic distinct portfolio maps",
                "Actual per-case coefficient presence, global union of all three, and cross-case equality wherever a coefficient occurs",
                "Unchanged fallback metadata/gates including ranges, root, shift and lookup; unchanged SSA masks and native copies",
                "Complete serial/parallel counts, DAG, first-fit packing and actual caps",
                "Both-case source frontier, fixed threshold, tie-break and baseline-derived saved replay cardinality",
            ],
            new_replays=0,
        ),
    )
    with (output / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write("# Next local action\n\n" + next_action + "\n")
    report = ROOT / "docs/limitation_program_20261001/COEFFICIENT_SOURCE_COSTS.md"
    lines = [
        "# Independent full-domain coefficient audit\n\n",
        "The fixed top-three coefficient frontier uses the same native signed 72-bit input and arbitrary 72-bit XOR output, with all 112 product columns retained. Each exact binary or signed-digit expansion, complemented sign/correction term, Cuccaro or compressor/prefix gate, native output copy and literal inverse was independently parsed from actual arrays. Existing guarded multiplication, root, shift and 32-row lookup metadata and gates remain byte-identical. This audit ran no new emitted gate or pricing replay.\n\n",
        "| Portfolio | Case | T gates | T-depth | T-depth gain | CT-depth | Qubits / cap | Eligible |\n|---|---|---:|---:|---:|---:|---:|---|\n",
    ]
    for row in trials.values():
        resources, baseline = row["resources"], row["baseline_resources"]
        lines.append(
            f"| {row['variant']} | {row['case']} | {resources['t_count']:,} | {resources['t_depth']:,} | {100 * (1 - resources['t_depth'] / baseline['t_depth']):.4f}% | {resources['clifford_t_depth']:,} | {resources['logical_qubits']:,} / {row['qubit_cap']:,} | {row['eligible']} |\n"
        )
    lines.append(
        "\n"
        + (
            f"Adopted `{selected}` after both-case eligibility and four saved complete-source replays.\n\n"
            if selected
            else "The accepted narrowed multiplication baseline is retained. No new complete-source financial replay was run.\n\n"
        )
    )
    lines.append(
        next_action
        + "\n\nG2 continuous-dollar certification, G3 compatible 99% estimator schedule, G4 matched classical timing and G5 physical runtime accounting remain unresolved. This audit establishes no quantum advantage. Everything stayed local.\n\n"
    )
    lines.append(
        f"Receipts: [summary](../../{relative(output)}/summary.json), [complete audit](../../{relative(output)}/), [auditor](../../research/limitation_program_20261001/reconcile_coefficients_v2.py).\n"
    )
    with report.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))
    assert all(sha(ROOT / name) == digest for name, digest in frozen.items())
    files = {relative(path): sha(path) for path in output.rglob("*") if path.is_file()}
    files[relative(report)] = sha(report)
    dump(
        output / "manifest.json",
        dict(files=files, frozen_inputs=frozen, manifest_self_hash_excluded=True),
    )
    print(
        "PASS independent coefficient audit",
        selected or "range-retained",
        len(auditor.array_scans),
        "actual arrays",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        run(args.leaf_root, args.source_root, args.output)
    except Exception as error:
        if args.output.exists():
            dump(
                args.output / "failure.json",
                dict(
                    passed=False, error_type=type(error).__name__, error=str(error), local_only=True
                ),
            )
            dump(
                args.output / "manifest.json",
                dict(
                    files={
                        relative(path): sha(path)
                        for path in args.output.rglob("*")
                        if path.is_file() and path.name != "manifest.json"
                    },
                    manifest_self_hash_excluded=True,
                ),
            )
        raise
