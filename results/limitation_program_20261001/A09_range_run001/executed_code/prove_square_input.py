"""Exact same-SSA guards and native-interface binding for signed square leaves."""

import hashlib

from research.controlled_source_completion.signed_square import LOWERING, leaf_spec
from research.limitation_program_20261001.constant_library import canonical

INTEGRATION_LOWERING = "same-target-signed-square-library-v1"


def is_square_entry(entry):
    outer = entry.get("input_contract")
    if isinstance(outer, dict) and "same_ssa_arguments" in outer:
        return True
    spec = entry.get("spec", {})
    if not isinstance(spec, dict):
        return False
    contracts = (entry.get("input_contract"), spec.get("input_contract"))
    return (
        spec.get("lowering") == LOWERING
        or spec.get("integration_lowering") == INTEGRATION_LOWERING
        or any(isinstance(c, dict) and "same_ssa_arguments" in c for c in contracts)
    )


def prove_square_site(target, node):
    """Caller binds node to the validated target; sample equality is insufficient."""
    if (
        node["op"] != "mul"
        or node["params"] != {}
        or len(node["args"]) != 2
        or len(node["out"]) != 1
        or node["args"][0] != node["args"][1]
    ):
        return None
    return {
        "input_value": node["args"][0],
        "output_value": node["out"][0],
        "actual_same_ssa_alias": list(node["args"]),
        "same_ssa_arguments": True,
        "all_signed_input_patterns": True,
        "width": target["width"],
        "fraction_bits": target["fraction_bits"],
        "proof": "Both native argument copies originate at the same validated SSA value",
    }


def validate_square_entry(target, node, entry):
    contract = entry.get("input_contract")
    if (
        not isinstance(contract, dict)
        or set(contract) != {"same_ssa_arguments"}
        or contract["same_ssa_arguments"] is not True
    ):
        raise ValueError("invalid same-SSA square input contract")
    proof = prove_square_site(target, node)
    if proof is None:
        raise ValueError("same-SSA square input contract is not proved by this graph")
    spec = entry.get("spec", {})
    if not isinstance(spec, dict):
        raise ValueError("invalid square leaf specification")
    expected = dict(
        leaf_spec(target["width"], target["fraction_bits"], "brent-kung"),
        integration_lowering=INTEGRATION_LOWERING,
    )
    key = hashlib.sha256(canonical(expected).encode()).hexdigest()[:20]
    if canonical(spec) != canonical(expected) or entry.get("key") != key:
        raise ValueError("same-SSA square leaf specification/key mismatch")
    width = target["width"]
    if (
        entry.get("op") != "mul"
        or entry.get("params") != {}
        or entry["args"] != [list(range(width)), list(range(width, 2 * width))]
        or entry["outs"] != [list(range(2 * width, 3 * width))]
    ):
        raise ValueError("square requires the native two full-width mul arguments and XOR output")
    return proof
