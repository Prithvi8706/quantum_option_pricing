"""Same-SSA unsigned square-root promises for versioned exact leaves."""

import hashlib

from research.controlled_source_completion.narrow_sqrt import LOWERING, leaf_spec
from research.limitation_program_20261001.constant_library import canonical

INTEGRATION_LOWERING = "same-target-unsigned-sqrt-range-v1"


def is_narrow_sqrt_entry(entry):
    """A removed outer promise must not disguise a narrowed archived leaf."""
    spec = entry.get("spec", {})
    if not isinstance(spec, dict):
        return False
    contracts = (entry.get("input_contract"), spec.get("input_contract"))
    return (
        spec.get("lowering") == LOWERING
        or spec.get("integration_lowering") == INTEGRATION_LOWERING
        or any(isinstance(c, dict) and "unsigned_input_bits" in c for c in contracts)
    )


def prove_sqrt_site(target, node, bounds, active_bits=46):
    width = target["width"]
    if type(active_bits) is not int or not 1 <= active_bits <= width:
        raise ValueError("invalid unsigned input width")
    if node["op"] != "sqrt" or node["params"] != {} or len(node["args"]) != 1:
        return None
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


def validate_sqrt_entry(target, node, entry, bounds):
    contract = entry.get("input_contract")
    if not isinstance(contract, dict) or set(contract) != {"unsigned_input_bits"}:
        raise ValueError("unsupported unsigned sqrt input contract")
    bits = contract["unsigned_input_bits"]
    proof = prove_sqrt_site(target, node, bounds, bits)
    if proof is None:
        raise ValueError("unsigned sqrt input contract is not proved by this graph")
    spec = entry.get("spec", {})
    expected = dict(
        leaf_spec(
            target["width"],
            target["fraction_bits"],
            bits,
            spec.get("algorithm"),
            spec.get("embedding"),
        ),
        integration_lowering=INTEGRATION_LOWERING,
    )
    key = hashlib.sha256(canonical(expected).encode()).hexdigest()[:20]
    if canonical(spec) != canonical(expected) or entry.get("key") != key:
        raise ValueError("unsigned sqrt leaf specification/key mismatch")
    width = target["width"]
    if entry["args"] != [list(range(width))] or entry["outs"] != [list(range(width, 2 * width))]:
        raise ValueError("unsigned sqrt requires the full-width native interface")
    return proof
