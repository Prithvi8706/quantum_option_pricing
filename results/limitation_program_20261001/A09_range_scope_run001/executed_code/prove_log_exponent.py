"""Prove a seven-bit signed ln(2) operand contract from each archived SSA graph.

This analysis never changes a compiler, arithmetic precision, loading law or
archived result. It records provenance and checks small arithmetic/leaf interfaces.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
import sys
import time
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COEFFICIENT = 762123384786
INVERSE_LN2 = 1586259972792
WIDTH, FRACTION, ACTIVE_SIGNED_BITS = 72, 40, 7
EXPECTED = {"B4x12": {"log": 30, "exp": 48}, "B8x52": {"log": 234, "exp": 416}}
PROOF_VERSION = "same-ssa-log-exponent-signed7-v1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )


def signed(raw: int, width: int) -> int:
    raw &= (1 << width) - 1
    return raw - (1 << width) if raw & (1 << (width - 1)) else raw


def index_graph(target: dict) -> tuple[dict, dict]:
    """Validate unique, ordered SSA provenance before any structural dispatch."""
    width, fraction = target.get("width"), target.get("fraction_bits")
    if type(width) is not int or type(fraction) is not int:
        raise ValueError("integer width/fraction metadata required")
    if not 0 <= fraction < width:
        raise ValueError("invalid word/fraction metadata")
    producers, locations = {}, {}
    for index, node in enumerate(target["nodes"]):
        if not isinstance(node, dict) or not isinstance(node.get("params"), dict):
            raise ValueError("malformed node")
        args, outs = node.get("args"), node.get("out")
        if not isinstance(args, list) or not isinstance(outs, list) or not outs:
            raise ValueError("invalid SSA arguments or outputs")
        if any(type(value) is not int for value in args + outs):
            raise ValueError("SSA identifiers must be integers, not booleans")
        if any(value not in producers for value in args):
            raise ValueError("argument lacks an earlier same-graph producer")
        if any(value in producers for value in outs) or len(set(outs)) != len(outs):
            raise ValueError("duplicate SSA output")
        for value in outs:
            producers[value], locations[value] = node, index
    if set(producers) != set(range(len(producers))):
        raise ValueError("SSA values are not a complete contiguous register domain")
    return producers, locations


def canonical(node: dict, op: str, arity: int) -> bool:
    return (
        node.get("op") == op
        and len(node.get("args", [])) == arity
        and len(node.get("out", [])) == 1
    )


def bit_extract(node: dict, shift: int, width: int, signed_input: bool) -> bool:
    params = node.get("params", {})
    return (
        canonical(node, "bits", 1)
        and type(params.get("shift")) is int
        and type(params.get("width")) is int
        and type(params.get("signed")) is bool
        and params == {"shift": shift, "width": width, "signed": signed_input}
    )


def literal(node: dict, value: int) -> bool:
    return (
        canonical(node, "const", 0)
        and type(node["params"].get("value")) is int
        and node["params"] == {"value": value}
    )


def coefficient_product(node: dict, value: int) -> bool:
    return (
        canonical(node, "cmul", 1)
        and type(node["params"].get("c")) is int
        and node["params"] == {"c": value}
    )


class SSAContext:
    """Own one validated graph snapshot; never accept a foreign producer map."""

    def __init__(self, target: dict):
        self.target = copy.deepcopy(target)
        self.producers, self.locations = index_graph(self.target)


def prove_log_site(target: dict | SSAContext, node_index: int) -> dict | None:
    """Return a proof only for this target's canonical guarded-log producer chain.

    A coefficient match or a zero-low-bit promise alone cannot pass this guard.
    The dispatch interface is a node index, so a caller cannot supply foreign
    producer dictionaries or a detached same-coefficient node.
    """
    context = target if isinstance(target, SSAContext) else SSAContext(target)
    target, producers, locations = context.target, context.producers, context.locations
    if (target["width"], target["fraction_bits"]) != (WIDTH, FRACTION):
        return None
    if type(node_index) is not int or not 0 <= node_index < len(target["nodes"]):
        return None
    product = target["nodes"][node_index]
    if not coefficient_product(product, COEFFICIENT):
        return None
    shifted = producers[product["args"][0]]
    if not bit_extract(shifted, -FRACTION, WIDTH, False):
        return None
    exponent = producers[shifted["args"][0]]
    if not canonical(exponent, "sub", 2) or exponent["params"]:
        return None
    top, fraction = [producers[value] for value in exponent["args"]]
    if not canonical(top, "msb", 1) or top["params"] or not literal(fraction, FRACTION):
        return None
    guarded = producers[top["args"][0]]
    if not canonical(guarded, "select", 3) or guarded["params"]:
        return None
    comparison, unit, raw = [producers[value] for value in guarded["args"]]
    if not canonical(comparison, "lt", 2) or comparison["params"]:
        return None
    if not literal(unit, 1):
        return None
    if comparison["args"] != [guarded["args"][2], guarded["args"][1]]:
        return None
    chain = [product, shifted, exponent, top, guarded, comparison, unit, fraction, raw]
    unique = {node["out"][0]: node for node in chain}
    provenance = [
        {"node_index": locations[value], "node": node}
        for value, node in sorted(unique.items(), key=lambda item: locations[item[0]])
    ]
    return {
        "proof_version": PROOF_VERSION,
        "cmul_node_index": node_index,
        "cmul_output": product["out"][0],
        "argument_value": shifted["out"][0],
        "exponent_value": exponent["out"][0],
        "msb_value": top["out"][0],
        "guarded_input_value": guarded["out"][0],
        "raw_guard_argument": guarded["args"][2],
        "coefficient": COEFFICIENT,
        "conservative_exponent_range": [-40, 31],
        "actual_signed_guard_exponent_range": [-40, 30],
        "input_contract": {
            "word_width": WIDTH,
            "zero_low_bits": FRACTION,
            "active_signed_bits": ACTIVE_SIGNED_BITS,
            "active_bit_positions": [40, 46],
            "sign_extension_positions": [47, 71],
            "sign_source_bit": 46,
            "upper_operand_interpretation": "signed7(input[40:47])",
        },
        "output_contract": {
            "width": WIDTH,
            "fraction_bits": FRACTION,
            "xor_arbitrary_initial_output": True,
            "financial_precision_or_law_changed": False,
            "function": "signed7(input[40:47]) * 762123384786 mod 2^72",
        },
        "provenance": provenance,
    }


def prove_exp_site(target: dict | SSAContext, node_index: int) -> dict | None:
    """Record the independent signed32 primitive bound, not a signed7 claim."""
    context = target if isinstance(target, SSAContext) else SSAContext(target)
    target, producers, locations = context.target, context.producers, context.locations
    if (target["width"], target["fraction_bits"]) != (WIDTH, FRACTION):
        return None
    if type(node_index) is not int or not 0 <= node_index < len(target["nodes"]):
        return None
    product = target["nodes"][node_index]
    if not coefficient_product(product, COEFFICIENT):
        return None
    shifted = producers[product["args"][0]]
    if not bit_extract(shifted, -FRACTION, WIDTH, False):
        return None
    quotient = producers[shifted["args"][0]]
    if not bit_extract(quotient, FRACTION, WIDTH, True):
        return None
    scaled = producers[quotient["args"][0]]
    if not coefficient_product(scaled, INVERSE_LN2):
        return None
    return {
        "cmul_node_index": node_index,
        "cmul_output": product["out"][0],
        "argument_value": shifted["out"][0],
        "range_reduction_value": quotient["out"][0],
        "known_primitive_signed_range": [-(1 << 31), (1 << 31) - 1],
        "known_active_signed_bits": 32,
        "zero_low_bits": 40,
        "signed7_proved": False,
        "reason": "A signed72 arithmetic right shift by40 yields signed32; no "
        "separate reachable-exponential-domain certificate is supplied here.",
        "provenance": [
            {"node_index": locations[node["out"][0]], "node": node}
            for node in (scaled, quotient, shifted, product)
        ],
    }


def fixture(width: int = WIDTH, fraction: int = FRACTION, coefficient: int = COEFFICIENT):
    nodes = [
        {"op": "input", "args": [], "params": {"name": "x", "bits": width}, "out": [0]},
        {"op": "const", "args": [], "params": {"value": 1}, "out": [1]},
        {"op": "lt", "args": [0, 1], "params": {}, "out": [2]},
        {"op": "select", "args": [2, 1, 0], "params": {}, "out": [3]},
        {"op": "msb", "args": [3], "params": {}, "out": [4]},
        {"op": "const", "args": [], "params": {"value": fraction}, "out": [5]},
        {"op": "sub", "args": [4, 5], "params": {}, "out": [6]},
        {
            "op": "bits", "args": [6],
            "params": {"shift": -fraction, "width": width, "signed": False}, "out": [7],
        },
        {"op": "cmul", "args": [7], "params": {"c": coefficient}, "out": [8]},
    ]
    return {
        "width": width, "fraction_bits": fraction, "nodes": nodes,
        "inputs": [0], "outputs": {"Y": 8}, "tables": {},
    }


def exponent_checks() -> dict:
    mask = (1 << WIDTH) - 1
    rows = []
    for index in range(WIDTH):
        exponent = index - FRACTION
        raw = exponent & mask
        # bits(signed=False, shift=-40, width=72) wraps the raw unsigned word.
        shifted = (raw << FRACTION) & mask
        reconstructed = signed((shifted >> FRACTION) & 127, ACTIVE_SIGNED_BITS)
        assert reconstructed == exponent
        assert shifted & ((1 << FRACTION) - 1) == 0
        assert (shifted >> 47) == (
            (1 << 25) - 1 if (shifted >> 46) & 1 else 0
        )
        product_old = (signed(shifted, WIDTH) * COEFFICIENT) >> FRACTION
        product_new = reconstructed * COEFFICIENT
        assert product_old == product_new
        assert -(1 << 71) <= product_new < (1 << 71)
        rows.append({
            "msb_index": index, "exponent": exponent,
            "input_word": shifted, "exact_product": product_new,
        })
    negative = -40
    naive = ((negative & 127) << FRACTION) & mask
    correct = ((negative & mask) << FRACTION) & mask
    assert signed(naive, WIDTH) != signed(correct, WIDTH)
    return {
        "all_msb_indices_checked": len(rows),
        "range": [min(row["exponent"] for row in rows), max(row["exponent"] for row in rows)],
        "rows": rows,
        "naive_unsigned7_negative_control": {
            "exponent": negative, "naive_word": naive, "correct_word": correct,
            "naive_effective_integer": signed(naive, WIDTH) >> FRACTION,
            "correct_effective_integer": signed(correct, WIDTH) >> FRACTION,
            "detected": True,
        },
    }


def finite_and_leaf_checks() -> dict:
    from research.controlled_source_completion.ir import evaluate
    from research.controlled_source_completion.primitives import basis_run, build

    exhaustive = 0
    for width in range(4, 9):
        fraction = width // 2
        target = fixture(width, fraction, 11)
        mask = (1 << width) - 1
        for raw in range(1 << width):
            guard = 1 if signed(raw, width) < 1 else raw
            exponent = max(0, guard.bit_length() - 1) - fraction
            _, trace = evaluate(target, {"x": raw}, True)
            assert signed(trace[6], width) == exponent
            assert trace[8] == (exponent * 11) & mask
            exhaustive += 1

    mask = (1 << WIDTH) - 1
    raw_cases = {0, 1, mask, 1 << 71, (1 << 71) + 1, (1 << 71) - 1}
    for index in range(WIDTH):
        raw_cases.add(1 << index)
        raw_cases.add(((1 << (index + 1)) - 1) & mask)
    target = fixture()
    guard_rows = []
    for raw in sorted(raw_cases):
        source = signed(raw, WIDTH)
        guard = 1 if source < 1 else raw
        exponent = max(0, guard.bit_length() - 1) - FRACTION
        _, trace = evaluate(target, {"x": raw}, True)
        assert trace[3] == guard and signed(trace[6], WIDTH) == exponent
        assert -40 <= exponent <= 30
        assert trace[8] == (exponent * COEFFICIENT) & mask
        guard_rows.append({"raw": raw, "signed": source, "guard": guard, "exponent": exponent})

    nonzero = int("a5" * 9, 16)
    programs = {
        "msb": build("msb", WIDTH, FRACTION),
        "sub": build("sub", WIDTH, FRACTION),
        "bits": build(
            "bits", WIDTH, FRACTION,
            {"shift": -FRACTION, "width": WIDTH, "signed": False},
        ),
    }
    leaf_calls = 0
    for index in range(WIDTH):
        exponent = index - FRACTION
        cases = [
            ("msb", [1 << index], index),
            ("sub", [index, FRACTION], exponent & mask),
            ("bits", [exponent & mask], ((exponent & mask) << FRACTION) & mask),
        ]
        for name, inputs, expected in cases:
            program, args, outs = programs[name]
            for inverse in (False, True):
                actual, clean, preserved, _ = basis_run(
                    program, args, outs, inputs, [nonzero], inverse
                )
                assert actual == [expected ^ nonzero] and clean and preserved
                leaf_calls += 1
    for raw in (0, mask, 1 << 71, (1 << 71) + 1, (1 << 71) - 1):
        program, args, outs = programs["msb"]
        expected = max(0, raw.bit_length() - 1)
        for inverse in (False, True):
            actual, clean, preserved, _ = basis_run(
                program, args, outs, [raw], [nonzero], inverse
            )
            assert actual == [expected ^ nonzero] and clean and preserved
            leaf_calls += 1
    return {
        "small_guarded_chain_exhaustive_inputs": exhaustive,
        "small_widths": [4, 5, 6, 7, 8],
        "production_guarded_raw_patterns": len(guard_rows),
        "production_negative_raw_patterns": sum(row["signed"] < 0 for row in guard_rows),
        "guard_rows": guard_rows,
        "production_exact_leaf_replays": leaf_calls,
        "leaf_interfaces": ["msb", "sub", "bits-left40"],
        "arbitrary_output": nonzero,
        "inverse_and_cleanup_checked": True,
        "scope": "Small chains and production primitives only; no full-source gate replay.",
    }


def negative_controls() -> dict:
    good = fixture()
    assert prove_log_site(good, 8) is not None
    mutations = {
        "coefficient_only_direct_input": lambda t: t["nodes"][8].update(args=[0]),
        "wrong_left_shift": lambda t: t["nodes"][7]["params"].update(shift=-39),
        "wrong_extraction_width": lambda t: t["nodes"][7]["params"].update(width=71),
        "wrong_signed_flag_type": lambda t: t["nodes"][7]["params"].update(signed=0),
        "wrong_subtract_constant": lambda t: t["nodes"][5]["params"].update(value=39),
        "non_msb_producer": lambda t: t["nodes"][4].update(op="bits", params={
            "shift": 0, "width": WIDTH, "signed": False,
        }),
        "swapped_guard_branches": lambda t: t["nodes"][3].update(args=[2, 0, 1]),
        "reversed_guard_comparison": lambda t: t["nodes"][2].update(args=[1, 0]),
        "wrong_guard_unit": lambda t: t["nodes"][1]["params"].update(value=0),
        "different_coefficient": lambda t: t["nodes"][8]["params"].update(c=COEFFICIENT + 1),
        "different_fraction": lambda t: t.update(fraction_bits=39),
    }
    rejected = []
    for name, mutate in mutations.items():
        target = copy.deepcopy(good)
        mutate(target)
        assert prove_log_site(target, 8) is None
        rejected.append(name)
    malformed = copy.deepcopy(good)
    malformed["nodes"][8]["out"] = [7]
    try:
        prove_log_site(malformed, 8)
    except ValueError:
        rejected.append("duplicate_ssa_output")
    else:
        raise AssertionError("Duplicate SSA output was accepted")
    malformed = copy.deepcopy(good)
    malformed["nodes"][4]["args"] = [999999]
    try:
        prove_log_site(malformed, 8)
    except ValueError:
        rejected.append("foreign_or_dangling_producer")
    else:
        raise AssertionError("Foreign producer was accepted")

    # A signed-right-shift pattern alone admits k=100 and cannot prove signed7.
    scaled = 100 << FRACTION
    quotient = signed(scaled, WIDTH) >> FRACTION
    assert quotient == 100 and not -64 <= quotient <= 63
    exp_bounds = [
        signed((1 << 71), WIDTH) >> FRACTION,
        signed((1 << 71) - 1, WIDTH) >> FRACTION,
    ]
    assert exp_bounds == [-(1 << 31), (1 << 31) - 1]
    return {
        "canonical_fixture_accepted": True,
        "rejected_structural_controls": rejected,
        "exp_pattern_signed7_counterexample": {
            "scaled_word": scaled, "range_reduction_integer": quotient,
            "scope": "Generic signed-right-shift pattern; this is not claimed "
            "reachable in the archived clipped financial graph.",
        },
        "exp_primitive_signed32_endpoints": exp_bounds,
    }


def prove_case(target: dict, source: dict, target_hash: str) -> dict:
    context = SSAContext(target)
    target, producers = context.target, context.producers
    if source["word_width"] != WIDTH or source["fraction_bits"] != FRACTION:
        raise ValueError("source precision differs from target proof interface")
    noninputs = [(index, node) for index, node in enumerate(target["nodes"])
                 if node["op"] != "input"]
    if len(noninputs) != len(source["forward_calls"]):
        raise ValueError("target/source invocation count mismatch")
    call_indices = {}
    for call_index, ((node_index, node), call) in enumerate(
        zip(noninputs, source["forward_calls"])
    ):
        if (node["args"], node["out"]) != (call["args"], call["out"]):
            raise ValueError("same-graph call binding mismatch")
        call_indices[node_index] = (call_index, call["leaf"])
    logs, exps, unknown = [], [], []
    for node_index, node in enumerate(target["nodes"]):
        if not coefficient_product(node, COEFFICIENT):
            continue
        proof = prove_log_site(context, node_index)
        if proof is not None:
            proof.update(
                target_sha256=target_hash,
                forward_call_index=call_indices[node_index][0],
                current_leaf=call_indices[node_index][1],
            )
            logs.append(proof)
            continue
        proof = prove_exp_site(context, node_index)
        if proof is not None:
            proof.update(
                target_sha256=target_hash,
                forward_call_index=call_indices[node_index][0],
                current_leaf=call_indices[node_index][1],
            )
            exps.append(proof)
        else:
            unknown.append({"node_index": node_index, "node": node})
    return {
        "log": logs, "exp": exps, "unclassified_ln2_calls": unknown,
        "counts": {"log": len(logs), "exp": len(exps), "unclassified": len(unknown)},
        "ssa_values": len(producers),
    }


def run(source_root: Path, output: Path) -> None:
    output = output.resolve()
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    output.mkdir(parents=True, exist_ok=False)
    selected, inputs = {}, {}
    for case in EXPECTED:
        comparison_path = source_root / case / "comparison.json"
        strategy = json.loads(comparison_path.read_text())["best"]["strategy"]
        directory = source_root / case / strategy
        selected[case] = directory
        inputs[case] = {
            "strategy": strategy,
            "target_path": str(directory / "target.json"),
            "target_sha256": digest(directory / "target.json"),
            "source_path": str(directory / "source.json"),
            "source_sha256": digest(directory / "source.json"),
            "comparison_sha256": digest(comparison_path),
        }
    # This prospective protocol is saved before theorem assertions, graph
    # classification, negative controls, numerical checks or gate execution.
    protocol = {
        "task": "A07/A10 signed7 logarithm-exponent metadata proof",
        "source_family": "unchanged archived B4/B8 72/40 knock-out arithmetic",
        "proof_version": PROOF_VERSION,
        "producer_path": str(Path(__file__).resolve()),
        "producer_sha256": digest(Path(__file__)),
        "inputs": inputs,
        "expected_counts": EXPECTED,
        "hypothesis": "Canonical msb-minus40 log chains fit signed7; exponent "
        "left40 operands have low40 zeros plus sign extension above bit46.",
        "conservative_range": [-40, 31],
        "actual_guard_refinement_to_check": [-40, 30],
        "candidate_scope": "One structural theorem and one canonical dispatch guard.",
        "acceptance": [
            "Every ln2 call is classified from same-graph provenance and bound to its source call.",
            "Expected log/exp counts hold and no call is unclassified.",
            "All72 possible raw msb indices, zero/negative patterns, small exhaustive chains, "
            "signed shift semantics and clean production primitive leaves pass.",
            "Invalid coefficient-only, shift, sign, guard, constant and provenance "
            "matches are rejected.",
            "Exp signed32 bound remains separate, with no unproved signed7 dispatch.",
        ],
        "stop_rule": "Stop and record a counterexample/mismatch at the first failed assertion; "
        "do not edit archived graphs or relax the guard to recover expected counts.",
        "exclusions": "No new multiplier, compiler integration, full-source replay, resource "
        "gain, precision change, input-law change, price certificate or advantage claim.",
    }
    save(output / "protocol.json", protocol)
    started = time.perf_counter()
    try:
        cases = {}
        for case, directory in selected.items():
            target = json.loads((directory / "target.json").read_text())
            source = json.loads((directory / "source.json").read_text())
            proof = prove_case(target, source, inputs[case]["target_sha256"])
            assert proof["counts"] == {**EXPECTED[case], "unclassified": 0}
            cases[case] = proof
            save(output / (case + "_provenance.json"), proof)
        checks = {
            "all_index_theorem": exponent_checks(),
            "structural_negative_controls": negative_controls(),
            "integer_and_primitive_checks": finite_and_leaf_checks(),
        }
        save(output / "checks.json", checks)
        result = {
            "passed": True, "proof_version": PROOF_VERSION,
            "counts": {case: row["counts"] for case, row in cases.items()},
            "conservative_log_range": [-40, 31],
            "actual_signed_guard_log_range": [-40, 30],
            "ln2_input_contract": cases["B4x12"]["log"][0]["input_contract"],
            "exp_known_signed_bits": 32,
            "signed7_log_product_range": [-40 * COEFFICIENT, 31 * COEFFICIENT],
            "product_fits_signed46": True,
            "financial_function_changed": False,
            "new_circuit_integrated": False,
            "resource_gain_measured": False,
            "seconds": time.perf_counter() - started,
        }
        assert -(1 << 45) <= -40 * COEFFICIENT <= 31 * COEFFICIENT < (1 << 45)
        save(output / "result.json", result)
        versions = {}
        for package in ("numpy", "numba", "qiskit"):
            versions[package] = metadata.version(package)
        verification = {
            "passed": True, "python": sys.version, "platform": platform.platform(),
            "executable": sys.executable, "packages": versions,
            "producer_sha256": digest(Path(__file__)),
            "protocol_saved_before_checks": True,
            "check_counts": {
                "all_msb_indices": len(checks["all_index_theorem"]["rows"]),
                "small_exhaustive_inputs": checks["integer_and_primitive_checks"][
                    "small_guarded_chain_exhaustive_inputs"
                ],
                "production_guard_patterns": checks["integer_and_primitive_checks"][
                    "production_guarded_raw_patterns"
                ],
                "production_primitive_leaf_replays": checks["integer_and_primitive_checks"][
                    "production_exact_leaf_replays"
                ],
                "rejected_structural_controls": len(
                    checks["structural_negative_controls"]["rejected_structural_controls"]
                ),
            },
            "command": sys.argv,
            "scope": protocol["exclusions"],
        }
        save(output / "verification.json", verification)
        (output / "NEXT.md").write_text(
            "# Next exact specialization interface\n\n"
            "The logarithm subset may use a proof-dispatched seven-bit signed operand, "
            "with all72 output bits and original40 fractional bits retained. "
            "The operand is bits40–46; bits0–39 are zero and bits47–71 equal bit46. "
            "This is sign redundancy, not a high-zero possible-one-mask proof. "
            "Do not alias dirty sign bits or narrow the exponential subset by this theorem.\n\n"
            "Next: emit an exact signed7 coefficient leaf under this input contract, "
            "including arbitrary output XOR and clean inverse; exhaust all128 signed7 "
            "values, verify static proof/cache dispatch and fallback, then compare the "
            "complete capped sources after the compact-storage integration. "
            "Retain the existing signed32 specialization if the measured source gain "
            "is absent or resource-dominated. No gain is predicted or credited here.\n",
            encoding="utf-8",
        )
    except Exception as error:
        save(output / "result.json", {
            "passed": False, "error_type": type(error).__name__, "error": str(error),
            "seconds": time.perf_counter() - started,
            "financial_function_changed": False,
        })
        raise
    hashes = {
        path.name: digest(path)
        for path in output.iterdir() if path.is_file() and path.name != "manifest.json"
    }
    save(output / "manifest.json", {
        "producer_sha256": digest(Path(__file__)), "inputs": inputs, "sha256": hashes,
    })
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root", type=Path,
        default=ROOT / "results/limitation_audit_20261001/constant_multiplier_v1",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_root.resolve(), args.output)
