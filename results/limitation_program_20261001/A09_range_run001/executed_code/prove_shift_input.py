"""Same-target integer interval guards for native signed-count shift leaves."""

import hashlib

from research.controlled_source_completion.narrow_shift import LOWERING, leaf_spec
from research.limitation_program_20261001.constant_library import canonical

INTEGRATION_LOWERING = "same-target-signed-count-shift-library-v1"


def is_narrow_shift_entry(entry):
    """Recognize typed leaves even when one promise/spec marker was removed."""
    outer = entry.get("input_contract")
    if isinstance(outer, dict) and "signed_shift_count_bits" in outer:
        return True
    spec = entry.get("spec", {})
    if not isinstance(spec, dict):
        return False
    contract = spec.get("input_contract")
    return (
        spec.get("lowering") == LOWERING
        or spec.get("integration_lowering") == INTEGRATION_LOWERING
        or isinstance(contract, dict) and "signed_shift_count_bits" in contract
    )


def prove_shift_site(target, node, bounds, count_bits=7):
    """Use bounds from bound_graph on this validated graph, never sample values.

    Compiler dispatch binds the actual node to its immutable SSA snapshot before
    this call. Scheduling validates that same whole target before bound_graph.
    The membership check also rejects a differently bound standalone request.
    """
    width = target["width"]
    if type(count_bits) is not int or not 1 <= count_bits <= width:
        raise ValueError("invalid signed shift count width")
    if (
        node["op"] != "shift"
        or node["params"] != {}
        or len(node["args"]) != 2
        or len(node["out"]) != 1
    ):
        return None
    if node not in target["nodes"]:
        raise ValueError("requested shift node is not bound to the validated target")
    low, high = bounds[node["args"][1]]
    limit = 1 << (count_bits - 1)
    if not -limit <= low <= high < limit:
        return None
    return {
        "data_value": node["args"][0],
        "count_value": node["args"][1],
        "output_value": node["out"][0],
        "count_bounds": [low, high],
        "signed_shift_count_bits": count_bits,
        "all_declared_input_patterns": True,
        "maximum_count_magnitude": limit,
        "data_width": width,
        "proof": "Inductive exact integer intervals in the same validated SSA graph",
        "directions": "Nonnegative count: modular left; negative: arithmetic right",
    }


def validate_shift_entry(target, node, entry, bounds):
    contract = entry.get("input_contract")
    if not isinstance(contract, dict) or set(contract) != {"signed_shift_count_bits"}:
        raise ValueError("unsupported signed shift count input contract")
    bits = contract["signed_shift_count_bits"]
    proof = prove_shift_site(target, node, bounds, bits)
    if proof is None:
        raise ValueError("signed shift count input contract is not proved by this graph")
    spec = entry.get("spec", {})
    if not isinstance(spec, dict):
        raise ValueError("invalid signed shift leaf specification")
    expected = dict(
        leaf_spec(target["width"], target["fraction_bits"], bits),
        integration_lowering=INTEGRATION_LOWERING,
    )
    key = hashlib.sha256(canonical(expected).encode()).hexdigest()[:20]
    if canonical(spec) != canonical(expected) or entry.get("key") != key:
        raise ValueError("signed shift leaf specification/key mismatch")
    width = target["width"]
    if (
        entry.get("op") != "shift"
        or entry.get("params") != {}
        or entry.get("args") != [list(range(width)), list(range(width, 2 * width))]
        or entry.get("outs") != [list(range(2 * width, 3 * width))]
    ):
        raise ValueError("signed shift requires two full-width native inputs and XOR output")
    return proof
