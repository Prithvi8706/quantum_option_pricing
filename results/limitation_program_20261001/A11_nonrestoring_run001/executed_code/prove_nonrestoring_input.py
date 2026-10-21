"""Bind exact non-restoring root promises to the actual immutable SSA graph."""

import hashlib

from research.controlled_source_completion.nonrestoring_sqrt import ALGORITHM, LOWERING, leaf_spec
from research.limitation_program_20261001.constant_library import canonical

INTEGRATION_LOWERING = "same-target-nonrestoring-unsigned-sqrt-library-v1"


def is_nonrestoring_entry(entry):
    """Recognize the new algorithm even when its outer promise was removed.

    The common unsigned-input contract also describes historical restoring
    roots, so the scheduler independently recognizes that contract and routes
    an ambiguous or malformed specification through historical validation.
    """
    spec = entry.get("spec")
    return isinstance(spec, dict) and (
        spec.get("lowering") == LOWERING
        or spec.get("integration_lowering") == INTEGRATION_LOWERING
        or spec.get("algorithm") == ALGORITHM
    )


def prove_nonrestoring_site(target, node, bounds, active_bits=46):
    width = target["width"]
    if type(active_bits) is not int or not 1 <= active_bits <= width:
        raise ValueError("invalid unsigned non-restoring input width")
    if (
        node["op"] != "sqrt"
        or node["params"] != {}
        or len(node["args"]) != 1
        or len(node["out"]) != 1
    ):
        return None
    if node not in target["nodes"]:
        raise ValueError("requested root node is not bound to the validated target")
    low, high = bounds[node["args"][0]]
    if not 0 <= low <= high < (1 << active_bits):
        return None
    return {
        "input_value": node["args"][0],
        "output_value": node["out"][0],
        "input_bounds": [low, high],
        "unsigned_input_bits": active_bits,
        "all_declared_input_patterns": True,
        "proof": "Inductive exact integer intervals in the same validated SSA graph",
    }


def validate_nonrestoring_entry(target, node, entry, bounds):
    contract = entry.get("input_contract")
    if not isinstance(contract, dict) or set(contract) != {"unsigned_input_bits"}:
        raise ValueError("unsupported unsigned non-restoring sqrt input contract")
    bits = contract["unsigned_input_bits"]
    proof = prove_nonrestoring_site(target, node, bounds, bits)
    if proof is None:
        raise ValueError("unsigned non-restoring sqrt contract is not proved by this graph")
    spec = entry.get("spec")
    if not isinstance(spec, dict):
        raise ValueError("invalid unsigned non-restoring sqrt leaf specification")
    expected = dict(
        leaf_spec(target["width"], target["fraction_bits"], active_bits=bits),
        integration_lowering=INTEGRATION_LOWERING,
    )
    key = hashlib.sha256(canonical(expected).encode()).hexdigest()[:20]
    if canonical(spec) != canonical(expected) or entry.get("key") != key:
        raise ValueError("non-restoring sqrt leaf specification/key mismatch")
    width = target["width"]
    if (
        entry.get("op") != "sqrt"
        or entry.get("params") != {}
        or entry.get("args") != [list(range(width))]
        or entry.get("outs") != [list(range(width, 2 * width))]
    ):
        raise ValueError("non-restoring sqrt requires the full-width native XOR interface")
    return proof
