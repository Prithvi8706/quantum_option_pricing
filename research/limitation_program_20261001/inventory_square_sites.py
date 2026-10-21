"""Read-only exact same-SSA square scope and signed normal-form feasibility."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from research.controlled_source_completion.prefix_multiplier import signed_partial_terms
from research.limitation_program_20261001.interval_bounds import bound_graph
from research.limitation_program_20261001.prove_log_exponent import SSAContext

ROOT = Path(__file__).resolve().parents[2]
CASES = ("B4x12", "B8x52")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def signed_square_terms(width, fraction):
    """One diagonal bit, one doubled off-diagonal product; retain all low columns."""
    if type(width) is not int or type(fraction) is not int or width < 1:
        raise ValueError("positive integer width and integer fraction required")
    if not 0 <= fraction <= width:
        raise ValueError("fraction must be in [0,width]")
    product_bits = width + fraction
    terms, correction = [], 0
    for first in range(width):
        column = 2 * first
        if column < product_bits:
            terms.append((first, first, column, False))
        for second in range(first + 1, width):
            column = first + second + 1
            if column >= product_bits:
                continue
            negative = second == width - 1
            terms.append((first, second, column, negative))
            if negative:
                correction -= 1 << column
    return terms, correction & ((1 << product_bits) - 1)


def polynomial(terms, product_bits):
    coefficients = defaultdict(int)
    modulus = 1 << product_bits
    for first, second, column, negative in terms:
        # On Boolean inputs, a_i*a_i equals a_i.
        monomial = tuple(sorted({first, second}))
        coefficients[monomial] += (-1 if negative else 1) << column
    return {str(key): value % modulus for key, value in coefficients.items() if value % modulus}


def term_counts(terms, correction, product_bits):
    columns = Counter(term[2] for term in terms)
    for column in range(product_bits):
        columns[column] += correction >> column & 1
    return {
        "total_terms": len(terms),
        "diagonal_boolean_copy_terms": sum(first == second for first, second, _, _ in terms),
        "off_diagonal_bit_product_terms": sum(first != second for first, second, _, _ in terms),
        "negative_terms": sum(negative for _, _, _, negative in terms),
        "fixed_correction": correction,
        "fixed_correction_set_bits": correction.bit_count(),
        "initial_columns_including_correction": [columns[column] for column in range(product_bits)],
        "maximum_initial_column_height": max(columns.values(), default=0),
        "emitted_circuit_cost_claimed": False,
    }


def arithmetic_certificate(width, fraction):
    bits = width + fraction
    modulus, word_mask = 1 << bits, (1 << width) - 1
    generic, generic_correction = signed_partial_terms(width, fraction)
    square, square_correction = signed_square_terms(width, fraction)
    assert polynomial(generic, bits) == polynomial(square, bits)
    for terms, correction in ((generic, generic_correction), (square, square_correction)):
        assert (
            sum(1 << column for _, _, column, negative in terms if negative) + correction
        ) % modulus == 0
    tested, premature_truncation_mismatches = 0, 0
    first_negative_control = None
    if width <= 6:
        for raw in range(1 << width):
            signed = raw - (1 << width) if raw & (1 << (width - 1)) else raw
            mathematical = (signed * signed) % modulus
            direct = 0
            complemented = square_correction
            prematurely_truncated = 0
            for first, second, column, negative in square:
                value = (raw >> first & 1) * (raw >> second & 1)
                direct += (-1 if negative else 1) * (value << column)
                complemented += ((1 - value) if negative else value) << column
                if column >= fraction:
                    prematurely_truncated += (-1 if negative else 1) * (value << column)
            assert direct % modulus == mathematical
            assert complemented % modulus == mathematical
            expected = ((signed * signed) >> fraction) & word_mask
            assert (direct % modulus >> fraction) & word_mask == expected
            assert (complemented % modulus >> fraction) & word_mask == expected
            broken = (prematurely_truncated % modulus >> fraction) & word_mask
            if broken != expected:
                premature_truncation_mismatches += 1
                first_negative_control = first_negative_control or {
                    "raw_input": raw,
                    "signed_input": signed,
                    "expected": expected,
                    "broken_discard_low_before_carry": broken,
                }
            tested += 1
    return {
        "width": width,
        "fraction_bits": fraction,
        "product_bits": bits,
        "passed": True,
        "universal_boolean_coefficient_identity": True,
        "fixed_complement_correction_identity": True,
        "exhaustive_signed_inputs": tested,
        "premature_low_truncation_mismatches": premature_truncation_mismatches,
        "first_low_truncation_negative_control": first_negative_control,
        "generic_signed_partial_terms": term_counts(generic, generic_correction, bits),
        "symmetric_signed_square_terms": term_counts(square, square_correction, bits),
        "all_columns_below_fraction_retained": True,
        "only_columns_at_or_above_product_bits_discarded": True,
    }


def producer_pattern(context, value):
    node = context.producers[value]
    depth = 0
    current = node
    while current["op"] == "mul" and current["args"][0] == current["args"][1]:
        depth += 1
        current = context.producers[current["args"][0]]
    signature = {
        "producer_op": node["op"],
        "consecutive_same_ssa_square_ancestors": depth,
        "root_op_after_square_chain": current["op"],
        "producer_argument_ops": [context.producers[value]["op"] for value in current["args"]],
    }
    return signature


def inventory_case(case, directory):
    target, source = read(directory / "target.json"), read(directory / "source.json")
    schedule = read(directory / "schedule_capped.json")
    assert target["width"] == source["word_width"] == 72
    assert target["fraction_bits"] == source["fraction_bits"] == 40
    context = SSAContext(target)
    bounds, rules = bound_graph(target)
    library = Path(source["library"]).resolve()
    entries = {key: read(library / (key + ".json")) for key in source["library_keys"]}
    nodes = [
        (index, node) for index, node in enumerate(context.target["nodes"]) if node["op"] != "input"
    ]
    calls = source["forward_calls"]
    assert len(nodes) == len(calls)
    squares, square_indices, multiplications = [], set(), 0
    patterns = Counter()
    input_ranges = Counter()
    for call_index, ((node_index, node), call) in enumerate(zip(nodes, calls, strict=True)):
        entry = entries[call["leaf"]]
        assert call["args"] == node["args"] and call["out"] == node["out"]
        assert entry["op"] == node["op"] and entry["params"] == node["params"]
        if node["op"] != "mul":
            continue
        multiplications += 1
        assert entry["spec"]["variant"] == "brent-kung"
        if node["args"][0] != node["args"][1]:
            continue
        argument = node["args"][0]
        low, high = bounds[argument]
        square_indices.add(call_index)
        pattern = producer_pattern(context, argument)
        pattern_key = json.dumps(pattern, sort_keys=True)
        patterns[pattern_key] += 1
        input_ranges[(low, high)] += 1
        raw_minimum = 0 if low <= 0 <= high else min(low * low, high * high)
        raw_maximum = max(low * low, high * high)
        result = [raw_minimum >> 40, raw_maximum >> 40]
        fits = result[1] < 1 << 71
        squares.append(
            {
                "call_index": call_index,
                "node_index": node_index,
                "input_value": argument,
                "output_value": node["out"][0],
                "actual_same_ssa_alias": node["args"],
                "leaf": call["leaf"],
                "pattern": pattern,
                "existing_signed_input_bounds": [low, high],
                "existing_bound_rule": rules[argument],
                "existing_output_bounds": list(bounds[node["out"][0]]),
                "square_specific_endpoint_bounds_before_word_wrap": result,
                "square_specific_bounds_fit_signed72": fits,
                "narrower_input_promise_adopted": False,
            }
        )
    batches, square_tied, square_only, mul_tied, square_owner = [], 0, 0, 0, 0
    total_depth, zero_square_depth, covered = 0, 0, []
    for batch_index, group in enumerate(schedule["groups"]):
        indices = group["call_indices"]
        covered.extend(indices)
        depths = {index: entries[calls[index]["leaf"]]["resources"]["t_depth"] for index in indices}
        peak = max(depths.values(), default=0)
        maxima = [index for index in indices if depths[index] == peak]
        square_maxima = [index for index in maxima if index in square_indices]
        other_maxima = [index for index in maxima if index not in square_indices]
        generic_mul_maxima = [
            index
            for index in maxima
            if index not in square_indices and entries[calls[index]["leaf"]]["op"] == "mul"
        ]
        without = max(
            (depth for index, depth in depths.items() if index not in square_indices), default=0
        )
        owner = min(maxima) if maxima else None
        square_tied += bool(square_maxima)
        square_only += bool(square_maxima) and not other_maxima
        mul_tied += bool(square_maxima and generic_mul_maxima)
        square_owner += owner in square_indices
        total_depth += 2 * peak
        zero_square_depth += 2 * without
        batches.append(
            {
                "batch": batch_index,
                "wave": group["wave"],
                "peak_leaf_t_depth": peak,
                "square_calls": sum(index in square_indices for index in indices),
                "same_ssa_squares_at_maximum": square_maxima,
                "distinct_mul_at_maximum": generic_mul_maxima,
                "other_calls_at_maximum": other_maxima,
                "deterministic_smallest_index_owner": owner,
                "owner_is_square": owner in square_indices,
                "peak_without_squares_fixed_batch_diagnostic": without,
                "zero_cost_square_fixed_batch_saving_diagnostic": 2 * (peak - without),
            }
        )
    assert sorted(covered) == list(range(len(calls))) and len(covered) == len(set(covered))
    assert total_depth == schedule["resources"]["t_depth"]
    return {
        "case": case,
        "passed": True,
        "mul_calls": multiplications,
        "same_ssa_square_calls": len(squares),
        "distinct_operand_mul_calls": multiplications - len(squares),
        "square_operation_patterns": [
            {"pattern": json.loads(key), "calls": count} for key, count in sorted(patterns.items())
        ],
        "square_input_interval_classes": [
            {"bounds": list(pair), "calls": count} for pair, count in sorted(input_ranges.items())
        ],
        "square_sites": squares,
        "batches": batches,
        "schedule_diagnostics": {
            "actual_capped_t_depth": total_depth,
            "batch_count": len(batches),
            "batches_with_square_at_maximum": square_tied,
            "batches_with_only_squares_at_maximum": square_only,
            "batches_square_tied_with_distinct_mul": mul_tied,
            "batches_deterministically_owned_by_square": square_owner,
            "optimistic_fixed_batch_all_squares_zero_cost_t_depth": zero_square_depth,
            "optimistic_fixed_batch_all_squares_zero_cost_saving": total_depth - zero_square_depth,
            "diagnostic_is_not_achievable_gain_or_global_bound": True,
        },
        "narrow_input_contract_or_emitted_circuit_claimed": False,
    }


def run(source_root, output):
    source_root, output = source_root.resolve(), output.resolve()
    source_root.relative_to(ROOT)
    output.relative_to(ROOT / "results/limitation_program_20261001")
    output.mkdir(parents=True, exist_ok=False)
    producer = Path(__file__).resolve()
    dependencies = [
        producer,
        ROOT / "research/controlled_source_completion/prefix_multiplier.py",
        ROOT / "research/limitation_program_20261001/interval_bounds.py",
        ROOT / "research/limitation_program_20261001/prove_log_exponent.py",
    ]
    snapshot = output / "executed_code"
    snapshot.mkdir()
    for path in dependencies:
        (snapshot / path.name).write_bytes(path.read_bytes())
    inputs = [source_root / "summary.json"]
    for case in CASES:
        directory = source_root / case
        inputs.extend(
            directory / name for name in ("target.json", "source.json", "schedule_capped.json")
        )
        source = read(directory / "source.json")
        library = Path(source["library"]).resolve()
        library.relative_to(ROOT)
        inputs.extend(library / (key + ".json") for key in source["library_keys"])
    frozen = {str(path.relative_to(ROOT)): sha(path) for path in inputs}
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "frozen_before_inventory_and_arithmetic_tests": True,
        "local_only": True,
        "source_root": str(source_root.relative_to(ROOT)),
        "target": "accepted A09 Brent-Kung source",
        "producer_sha256": sha(producer),
        "dependencies": {str(path.relative_to(ROOT)): sha(path) for path in dependencies},
        "frozen_inputs": frozen,
        "environment": {
            "python": platform.python_version(),
            "executable": sys.executable,
            **{name: importlib.metadata.version(name) for name in ("numpy", "numba")},
        },
        "arithmetic": "Independent symmetric signed square: diagonal a_i at column2i, "
        "off-diagonal a_i*a_j at columni+j+1, negative sign-cross complemented with "
        "fixed modular correction. Retain all low columns; drop only columns>=w+f.",
        "tests": "All signed inputs width1..6, all fractions0..w, universal coefficient "
        "comparison to existing signed_partial_terms, low-column truncation negative control.",
        "inventory": "Exact same SSA args equality only; interval/producer patterns and "
        "actual saved batch maxima versus distinct-operand multiplication. "
        "No leaf ratio extrapolation.",
        "stop_rule": "One mathematical normal form and two fixed source inventories; "
        "report a bounded emitted-leaf experiment or reject scope; no integrations.",
        "exclusions": "No emitted circuit or resource saving claim, full-source replay, "
        "new narrowed promise, precision/law changes, physical timing or quantum advantage.",
    }
    save(output / "protocol.json", protocol)
    started = time.perf_counter()
    try:
        accepted = read(source_root / "summary.json")
        assert accepted["passed"] and accepted["accepted"] and accepted["selected"] == "brent-kung"
        certificates = [
            arithmetic_certificate(width, fraction)
            for width in range(1, 7)
            for fraction in range(width + 1)
        ]
        production = arithmetic_certificate(72, 40)
        explicit = next(
            row for row in certificates if row["width"] == 3 and row["fraction_bits"] == 3
        )
        assert explicit["premature_low_truncation_mismatches"] > 0
        save(
            output / "arithmetic_certificate.json",
            {
                "passed": True,
                "small_cases": certificates,
                "production": production,
                "exhaustive_signed_inputs_checked": sum(
                    row["exhaustive_signed_inputs"] for row in certificates
                ),
                "low_column_negative_control": {
                    "width": 3,
                    "fraction_bits": 3,
                    "signed_input": 3,
                    "expected": 1,
                    "broken": 0,
                },
                "new_emitted_gate_replays": 0,
            },
        )
        cases = []
        for case in CASES:
            result = inventory_case(case, source_root / case)
            save(output / (case + "_inventory.json"), result)
            cases.append(
                {
                    key: value
                    for key, value in result.items()
                    if key not in ("square_sites", "batches")
                }
            )
        worthwhile = any(row["same_ssa_square_calls"] for row in cases)
        summary = {
            "passed": True,
            "cases": cases,
            "production_term_comparison": production,
            "decision": "Proceed to one exact full72 signed square leaf screen"
            if worthwhile
            else "Stop square specialization: no exact same-SSA sites",
            "recommended_next_experiment": "Emit symmetric signed square with existing "
            "CSA plus Brent-Kung final adder, retain all112 product columns, validate "
            "arbitrary72 output XOR/input-workspace cleanup and historical equivalence. "
            "Use a one-input specialized leaf only when args[0]==args[1] in validated "
            "same target SSA. Keep generic mul fallback. Full-source capped scheduling "
            "and replay must decide adoption; mathematical term reduction is not a gain.",
            "financial_function_changed": False,
            "circuit_or_source_gain_claimed": False,
            "elapsed_seconds": time.perf_counter() - started,
        }
        save(output / "summary.json", summary)
        for path, expected in frozen.items():
            assert sha(ROOT / path) == expected
        for path, expected in protocol["dependencies"].items():
            assert sha(ROOT / path) == expected
        save(
            output / "verification.json",
            {
                "passed": True,
                "all_frozen_source_inputs_unchanged": True,
                "prospective_code_dependencies_unchanged": True,
                "new_gate_replays": 0,
                "full_source_gain_claimed": False,
            },
        )
        print(
            json.dumps(
                {
                    "passed": True,
                    "cases": [
                        {
                            "case": row["case"],
                            "square_calls": row["same_ssa_square_calls"],
                            "schedule": row["schedule_diagnostics"],
                        }
                        for row in cases
                    ],
                    "terms": {
                        "generic": production["generic_signed_partial_terms"]["total_terms"],
                        "symmetric": production["symmetric_signed_square_terms"]["total_terms"],
                    },
                }
            )
        )
    except Exception as error:
        save(
            output / "failure.json",
            {"passed": False, "error": str(error), "type": type(error).__name__},
        )
        raise
    finally:
        save(
            output / "manifest.json",
            {
                "files": {
                    str(path.relative_to(output)): sha(path)
                    for path in sorted(output.rglob("*"))
                    if path.is_file() and path.name != "manifest.json"
                }
            },
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-root", type=Path, default=ROOT / "results/limitation_program_20261001/A09_run001"
    )
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    run(arguments.source_root, arguments.output)
