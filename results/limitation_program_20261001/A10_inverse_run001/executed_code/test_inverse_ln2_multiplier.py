"""Generic signed inverse-ln(2) leaf tests and a fresh local receipt runner."""

from __future__ import annotations

# Protocol/report prose keeps complete lines for faithful generated receipts.
# ruff: noqa: E501

import argparse
from collections import Counter
from datetime import datetime, timezone
from functools import lru_cache
import os
from pathlib import Path
import random
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

import numpy as np
import pytest

from research.controlled_source_completion.constant_multiplier import (
    STRATEGIES,
    build_constant_multiplier,
    signed_digits,
)
from research.controlled_source_completion.primitives import (
    array_gates,
    basis_run,
    build,
    resources,
)
from research.limitation_program_20261001.baseline import ROOT, dump, environment, load, sha


WIDTH, FRACTION, COEFFICIENT = 72, 40, 1586259972792
OLD_KEY = "18e3e6a4b0b5c576252e"
OLD_LIBRARY = ROOT / "results/limitation_audit_20261001/constant_multiplier_v1/leaves"
RECEIPT_ENV = "INVERSE_LN2_RECEIPT_ROOT"


def independent_reference(width, fraction, coefficient, raw, initial):
    """Integer floor division, not floating point or a circuit-derived rule."""
    signed = raw if raw < (1 << (width - 1)) else raw - (1 << width)
    quotient = (signed * coefficient) // (1 << fraction)
    return initial ^ (quotient % (1 << width))


def assert_basis(program, arguments, outputs, width, fraction, coefficient, raw, initial, inverse):
    actual, clean, preserved, state = basis_run(
        program, arguments, outputs, [raw], [initial], inverse
    )
    expected = independent_reference(width, fraction, coefficient, raw, initial)
    assert actual == [expected]
    assert clean and preserved
    # Independently check all non-interface wires, not only the returned flags.
    interface = set(arguments[0]) | set(outputs[0])
    assert all(state[wire] == 0 for wire in range(program.qubits) if wire not in interface)
    assert all(int(state[wire]) == ((raw >> bit) & 1) for bit, wire in enumerate(arguments[0]))
    return actual, clean, preserved


@lru_cache(maxsize=1)
def historical_leaf():
    program, args, outs = build("cmul", WIDTH, FRACTION, {"c": COEFFICIENT})
    entry = load(OLD_LIBRARY / (OLD_KEY + ".json"))
    gate_file = OLD_LIBRARY / entry["gate_file"]
    assert sha(gate_file) == entry["sha256"]
    actual = np.load(gate_file, mmap_mode="r")
    assert np.array_equal(array_gates(program), actual)
    assert resources(program) == entry["resources"]
    assert [list(reg) for reg in args] == entry["args"]
    assert [list(reg) for reg in outs] == entry["outs"]
    return program, args, outs, entry


@lru_cache(maxsize=None)
def candidate(strategy):
    return build_constant_multiplier(WIDTH, FRACTION, COEFFICIENT, 0, strategy)


@lru_cache(maxsize=1)
def production_vectors():
    mask = (1 << WIDTH) - 1
    values = {0, 1, 2, 3, mask, mask - 1, mask - 2, 1 << (WIDTH - 1)}
    for power in (1, 15, 31, 39, 40, 41, 63, 70, 71):
        for difference in (-1, 0, 1):
            values.add(((1 << power) + difference) & mask)
            values.add((-(1 << power) + difference) & mask)
    values.add(int("a5" * 9, 16))
    values.add(int("5a" * 9, 16))
    edges = sorted(values)
    rng = random.Random(20261001072)
    values = edges + [rng.getrandbits(WIDTH) for _ in range(128)]
    return [(raw, rng.getrandbits(WIDTH)) for raw in values], len(edges)


@lru_cache(maxsize=None)
def historical_observation(raw, initial, inverse):
    program, args, outs, _ = historical_leaf()
    return assert_basis(program, args, outs, WIDTH, FRACTION, COEFFICIENT, raw, initial, inverse)


@pytest.mark.parametrize("strategy", STRATEGIES)
def test_exhaustive_small_signed_full_domain(strategy):
    checks = 0
    for width in range(1, 6):
        mask = (1 << width) - 1
        for fraction in range(width + 1):
            for coefficient in (-17, -7, -3, -1, 0, 1, 3, 7, 17):
                program, args, outs = build_constant_multiplier(
                    width, fraction, coefficient, 0, strategy
                )
                for raw in range(1 << width):
                    initials = sorted({0, mask, (raw * 5 + coefficient) & mask})
                    for initial in initials:
                        for inverse in (False, True):
                            assert_basis(
                                program,
                                args,
                                outs,
                                width,
                                fraction,
                                coefficient,
                                raw,
                                initial,
                                inverse,
                            )
                            checks += 1
    folder = os.environ.get(RECEIPT_ENV)
    if folder:
        dump(
            Path(folder) / (strategy + "_small_checks.json"),
            {
                "passed": True,
                "strategy": strategy,
                "basis_direction_checks": checks,
                "widths": [1, 2, 3, 4, 5],
                "fractions": "every integer from zero to width",
                "coefficients": [-17, -7, -3, -1, 0, 1, 3, 7, 17],
                "input_domain": "every full-width signed raw bit pattern; zero_bits=0",
                "outputs": "zero, all ones and a deterministic arbitrary pattern, deduplicated",
                "directions": "both complete gate-list directions for every input/output case",
            },
        )


def test_historical_default_reproduces_actual_archived_leaf():
    program, _, _, entry = historical_leaf()
    assert program.qubits == entry["resources"]["qubits"]


@pytest.mark.parametrize("strategy", STRATEGIES)
def test_generic_72_bit_edges_random_arbitrary_outputs_inverse_and_cleanup(strategy):
    program, args, outs = candidate(strategy)
    vectors, edge_count = production_vectors()
    assert any(raw & ((1 << FRACTION) - 1) for raw, _ in vectors)
    assert any(raw >= (1 << (WIDTH - 1)) for raw, _ in vectors)
    checked = 0
    for raw, initial in vectors:
        for inverse in (False, True):
            actual = assert_basis(
                program, args, outs, WIDTH, FRACTION, COEFFICIENT, raw, initial, inverse
            )
            assert actual == historical_observation(raw, initial, inverse)
            checked += 1
        # Applying the clean XOR function twice restores arbitrary output words.
        target = independent_reference(WIDTH, FRACTION, COEFFICIENT, raw, initial)
        restored, clean, preserved, _ = basis_run(program, args, outs, [raw], [target])
        assert restored == [initial] and clean and preserved
    gates = array_gates(program)
    output_wires = set(outs[0])
    assert all(int(a) not in output_wires for kind, a, _, _ in gates if kind >= 2)
    assert all(int(b) not in output_wires for kind, _, b, _ in gates if kind == 3)
    counts = Counter(map(int, gates[:, 0]))
    measured = resources(program)
    assert measured["source_gates"] == len(gates)
    assert measured["x"] == counts[1] and measured["cx"] == counts[2]
    assert measured["ccx"] == counts[3] and measured["t_count"] == 7 * counts[3]
    folder = os.environ.get(RECEIPT_ENV)
    if folder:
        path = Path(folder)
        binary = path / (strategy + ".npy")
        with binary.open("xb") as handle:
            np.save(handle, gates)
        entry = {
            "op": "cmul",
            "params": {"c": COEFFICIENT},
            "width": WIDTH,
            "fraction_bits": FRACTION,
            "zero_bits": 0,
            "strategy": strategy,
            "domain": "All signed 72-bit inputs, with no narrowing/zero-low promise",
            "args": [list(reg) for reg in args],
            "outs": [list(reg) for reg in outs],
            "resources": measured,
            "gate_file": binary.name,
            "sha256": sha(binary),
            "passed": True,
            "signed_edge_inputs": edge_count,
            "seeded_full_width_random_inputs": 128,
            "complete_direction_checks": checked,
            "xor_involution_checks": len(vectors),
            "all_input_and_workspace_bits_preserved": True,
            "comparison": "Independent integer floor division plus actual archived/default historical leaf",
        }
        dump(path / (strategy + ".json"), entry)


def test_no_zero_low_or_unsigned_substitution_is_permitted():
    # A generic one-LSB input must survive; the earlier zero-low specialization
    # would incorrectly return zero if its static promise were silently assumed.
    promised, args, outs = build_constant_multiplier(WIDTH, FRACTION, COEFFICIENT, FRACTION)
    assert basis_run(promised, args, outs, [1], [0])[0] == [0]
    assert independent_reference(WIDTH, FRACTION, COEFFICIENT, 1, 0) == 1
    negative_one = (1 << WIDTH) - 1
    unsigned = ((negative_one * COEFFICIENT) // (1 << FRACTION)) % (1 << WIDTH)
    signed = independent_reference(WIDTH, FRACTION, COEFFICIENT, negative_one, 0)
    assert unsigned != signed
    assert signed == ((-2) % (1 << WIDTH))  # Negative division rounds down.
    for strategy in STRATEGIES:
        program, args, outs = candidate(strategy)
        assert_basis(program, args, outs, WIDTH, FRACTION, COEFFICIENT, 1, 0, False)
        assert_basis(program, args, outs, WIDTH, FRACTION, COEFFICIENT, negative_one, 0, False)


def test_exact_coefficient_expansions():
    for form in ("binary", "signed-digit"):
        digits = signed_digits(COEFFICIENT, form)
        assert sum(sign * (1 << position) for position, sign in digits) == COEFFICIENT


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    report = ROOT / "docs/limitation_program_20261001/INVERSE_LN2_LEAF.md"
    assert not report.exists()
    code = Path(__file__).resolve()
    original = load(OLD_LIBRARY / (OLD_KEY + ".json"))
    inputs = {
        (OLD_LIBRARY / (OLD_KEY + ".json")).relative_to(ROOT).as_posix(): sha(
            OLD_LIBRARY / (OLD_KEY + ".json")
        ),
        (OLD_LIBRARY / original["gate_file"]).relative_to(ROOT).as_posix(): sha(
            OLD_LIBRARY / original["gate_file"]
        ),
        "research/controlled_source_completion/constant_multiplier.py": sha(
            ROOT / "research/controlled_source_completion/constant_multiplier.py"
        ),
        "research/controlled_source_completion/primitives.py": sha(
            ROOT / "research/controlled_source_completion/primitives.py"
        ),
        code.relative_to(ROOT).as_posix(): sha(code),
    }
    dump(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "item": "A10",
            "coefficient": COEFFICIENT,
            "width": WIDTH,
            "fraction_bits": FRACTION,
            "zero_bits": 0,
            "domain": "All signed 72-bit raw inputs; no range or zero-low promise",
            "strategies": list(STRATEGIES),
            "frozen_inputs": inputs,
            "selection": "Report the full leaf Pareto set in T-depth/T-count/qubits; no default source replacement before capped complete-source measurement",
            "small_tests": "Widths1..5, every fractional width, coefficients -17,-7,-3,-1,0,1,3,7,17; every raw input, arbitrary/zero/all-ones outputs, both gate directions",
            "production_tests": "Signed extrema, every nominated binary boundary +/-1, nonzero low40 bits, 128 seeded full72 random inputs; both gate directions, arbitrary XOR outputs, full cleanup and input restoration",
            "historical_control": "Build default historical cmul once; require identical gate array/registers/resources to archived leaf18e3e6a4b0b5c576252e; cache its observations across all strategies",
            "acceptance": "Every independent signed floor/modular XOR, historical equivalence and cleanup check passes; emitted gate/resource metadata and hashes agree",
            "stop_rule": "Four strategies and one frozen test suite. Reject any failing candidate before full-source integration; keep archived source unchanged.",
            "exclusions": "No full financial-source replay, loading-law change, estimator, physical resource time, cloud/package/push action or achieved full-source depth gain",
            "random_seed": 20261001072,
            "local_only": True,
        },
    )
    dump(output / "environment.json", environment())
    env = os.environ.copy()
    env[RECEIPT_ENV] = str(output)
    command = [
        sys.executable,
        "-m",
        "pytest",
        str(code),
        "-q",
        "--maxfail=1",
        "--junitxml",
        str(output / "pytest_junit.xml"),
    ]
    started = time.perf_counter()
    process = subprocess.run(
        command, cwd=ROOT, env=env, text=True, capture_output=True, check=False
    )
    elapsed = time.perf_counter() - started
    with (output / "pytest_stdout.txt").open("x", encoding="utf-8") as handle:
        handle.write(process.stdout + process.stderr)
    print(process.stdout, end="")
    print(process.stderr, end="")
    parsed = ET.parse(output / "pytest_junit.xml").getroot()
    suites = list(parsed.iter("testsuite"))
    observed = {
        field: sum(int(s.attrib.get(field, 0)) for s in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }
    passed = (
        process.returncode == 0
        and observed["failures"] == observed["errors"] == observed["skipped"] == 0
    )
    entries = [load(output / (strategy + ".json")) for strategy in STRATEGIES] if passed else []
    pareto = [
        entry["strategy"]
        for entry in entries
        if not any(
            all(
                other["resources"][field] <= entry["resources"][field]
                for field in ("t_depth", "t_count", "qubits")
            )
            and any(
                other["resources"][field] < entry["resources"][field]
                for field in ("t_depth", "t_count", "qubits")
            )
            for other in entries
        )
    ]
    summary = {
        "passed": passed,
        "decision": "validated_leaf_candidates" if passed else "rejected_test_failure",
        "historical": original["resources"],
        "candidates": entries,
        "pareto_strategies": pareto,
        "coefficient": COEFFICIENT,
        "width": WIDTH,
        "fraction_bits": FRACTION,
        "zero_bits": 0,
        "observed_tests": observed,
        "test_wall_seconds": elapsed,
        "full_source_improvement": None,
        "full_source_selection": None,
        "scope": "Exact standalone full-domain leaf validation only; complete packed source/physical costs unknown",
    }
    dump(output / "summary.json", summary)
    dump(output / "result.json", summary)
    dump(
        output / "verification.json",
        {
            "passed": passed,
            "command": command,
            "observed": observed,
            "subprocess_returncode": process.returncode,
            "wall_seconds": elapsed,
            "producer_sha256": sha(code),
            "environment_sha256": sha(output / "environment.json"),
            "new_full_source_replays": 0,
            "historical_gate_and_resource_identity": passed,
            "scope": "CPU gate simulation durations are reproducibility metadata, not quantum hardware latency",
        },
    )
    with (output / "NEXT.md").open("x", encoding="utf-8") as handle:
        handle.write(
            "# Next local action\n\n"
            + (
                "Integrate only this coefficient's generic-domain leaf alternatives into a fresh library, preserving all other leaf bytes, the financial target and the latest signed-seven-bit/compact source. Measure at the original caps, retain failed/scratch tradeoff screens and replay the selected complete sources with nonzero outputs. Choose by actual capped full-source depth/T-count/qubits; standalone leaf gains and zero-cost ceilings are not full-source gains.\n"
                if passed
                else "Stop full-source integration. Inspect the saved counterexample/JUnit failure, correct only a justified candidate in a new receipt, and retain the previous accepted source.\n"
            )
        )
    lines = [
        "# Generic inverse-ln(2) constant multiplier: standalone leaf result\n\n",
        f"Local A10 experiment, 1 October 2026. Coefficient `{COEFFICIENT}`, 72-bit signed inputs, 40 fractional bits, zero_bits=0. The independent target is `floor(signed72(x)*c/2^40) mod2^72`, XORed into an arbitrary existing output, with input preservation and zero restored workspace. No zero-low or narrow input assumption is used.\n\n",
        f"The observed pytest run completed {observed['tests']} tests with {observed['failures']} failures, {observed['errors']} errors and {observed['skipped']} skips. The historical default cmul was built once and compared byte-for-byte, including registers/resources, with the actual archived leaf. Production checks include nonzero low fractional bits, signed extrema and boundaries, negative floor rounding, 128 seeded full72 randoms, both gate directions, arbitrary outputs and XOR involution. Small-width checks exhaust every input and fractional width across the frozen coefficient family.\n\n",
        "| Leaf | Qubits | T gates | T-depth | Clifford+T depth |\n|---|---:|---:|---:|---:|\n",
    ]
    old = original["resources"]
    lines.append(
        f"| Historical actual/default | {old['qubits']:,} | {old['t_count']:,} | {old['t_depth']:,} | {old['clifford_t_depth']:,} |\n"
    )
    for entry in entries:
        r = entry["resources"]
        lines.append(
            f"| {entry['strategy']} | {r['qubits']:,} | {r['t_count']:,} | {r['t_depth']:,} | {r['clifford_t_depth']:,} |\n"
        )
    lines.append(
        "\nLeaf Pareto set: "
        + (", ".join(pareto) if pareto else "none; validation failed")
        + ". Selection for the complete financial source is unresolved. Larger carry-save workspace can change cap-limited packing; the quickest leaf is not automatically the quickest complete source.\n\n"
    )
    lines.append(
        "The original coefficient is unchanged: this is exact integer lowering, with no new logarithm approximation or payoff/law change. Seven-T CCX/all-to-all logical accounting is the same convention used for the baseline. No physical time, estimator completion, continuous-price certification or quantum advantage follows from these leaf counts. The earlier zero-cost full-source screens are not credited as achieved reductions.\n\n"
    )
    lines.append(
        "Next: compare the surviving leaves in fresh complete compact source schedules, preserving the latest accepted target, signed-seven-bit implementation and original caps. Only subsequent actual source resources and cleanup replays can select an adopted default. All work remained local.\n\n"
    )
    lines.append(
        "Receipts: [summary](../../results/limitation_program_20261001/A10_inverse_leaf_run001/summary.json), [verification](../../results/limitation_program_20261001/A10_inverse_leaf_run001/verification.json), [candidate gates and prospective protocol](../../results/limitation_program_20261001/A10_inverse_leaf_run001/), [test/producer](../../research/limitation_program_20261001/test_inverse_ln2_multiplier.py).\n"
    )
    with report.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))
    assert all(sha(ROOT / p) == digest for p, digest in inputs.items())
    files = {
        p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(output.rglob("*")) if p.is_file()
    }
    dump(
        output / "manifest.json",
        {
            "files": files,
            "frozen_inputs": inputs,
            "report": {report.relative_to(ROOT).as_posix(): sha(report)},
            "manifest_self_hash_excluded": True,
        },
    )
    assert all(sha(ROOT / p) == digest for p, digest in files.items())
    if not passed:
        raise SystemExit(process.returncode or 1)
    print("Leaf candidates validated; full-source integration remains unmeasured.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
