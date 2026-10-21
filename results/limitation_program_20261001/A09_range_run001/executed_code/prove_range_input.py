"""Bind both signed active-operand promises to the actual immutable SSA graph."""

import hashlib

from research.controlled_source_completion.range_multiplier import ALGORITHM, LOWERING, leaf_spec
from research.limitation_program_20261001.constant_library import canonical

INTEGRATION_LOWERING = "same-target-signed-range-multiplier-library-v1"


def is_range_entry(entry):
    """Recognize remaining markers even when one promise/spec field was removed."""
    contract, spec = entry.get("input_contract"), entry.get("spec")
    return (isinstance(contract, dict) and "signed_operand_bits" in contract) or (
        isinstance(spec, dict)
        and (
            spec.get("lowering") == LOWERING
            or spec.get("integration_lowering") == INTEGRATION_LOWERING
            or spec.get("algorithm") == ALGORITHM
            or "active_operand_bits" in spec
            or (
                isinstance(spec.get("input_contract"), dict)
                and "signed_operand_bits" in spec["input_contract"]
            )
        )
    )


def signed_interval_bits(low, high, width):
    """Minimum signed width containing the complete inclusive integer interval."""
    if (
        type(width) is not int
        or width < 1
        or type(low) is not int
        or type(high) is not int
        or not -(1 << (width - 1)) <= low <= high < 1 << (width - 1)
    ):
        raise ValueError("ordered signed native-width interval required")
    return next(
        bits for bits in range(1, width + 1) if -(1 << (bits - 1)) <= low <= high < 1 << (bits - 1)
    )


def validate_allowed_bits(allowed_bits, width):
    if (
        not isinstance(allowed_bits, (list, tuple))
        or not allowed_bits
        or any(type(bits) is not int or not 1 <= bits <= width for bits in allowed_bits)
        or list(allowed_bits) != sorted(set(allowed_bits))
        or allowed_bits[-1] != width
    ):
        raise ValueError("strictly increasing signed operand bins ending in native width required")
    return tuple(allowed_bits)


def _validate_node_binding(target, node, locations):
    if locations is None:
        bound = node in target["nodes"]
    else:
        index = locations.get(node["out"][0])
        bound = (
            type(index) is int
            and 0 <= index < len(target["nodes"])
            and target["nodes"][index] == node
        )
    if not bound:
        raise ValueError("requested multiplier node is not bound to the validated target")


def prove_range_site(target, node, bounds, left_bits, right_bits, *, locations=None):
    width = target["width"]
    if any(type(bits) is not int or not 1 <= bits <= width for bits in (left_bits, right_bits)):
        raise ValueError("invalid signed operand width")
    if (
        node["op"] != "mul"
        or node["params"] != {}
        or len(node["args"]) != 2
        or len(node["out"]) != 1
    ):
        return None
    _validate_node_binding(target, node, locations)
    intervals = [bounds[value] for value in node["args"]]
    minimum = [signed_interval_bits(*pair, width) for pair in intervals]
    if any(required > bits for required, bits in zip(minimum, (left_bits, right_bits))):
        return None
    return {
        "input_values": list(node["args"]),
        "output_value": node["out"][0],
        "input_bounds": [list(pair) for pair in intervals],
        "minimum_signed_operand_bits": minimum,
        "signed_operand_bits": [left_bits, right_bits],
        "both_operand_guards_proved": True,
        "all_declared_input_patterns": True,
        "proof": "Inductive exact integer intervals in the same validated SSA graph",
    }


def select_range_site(target, node, bounds, allowed_bits, *, locations=None):
    bins = validate_allowed_bits(allowed_bits, target["width"])
    if (
        node["op"] != "mul"
        or node["params"] != {}
        or len(node["args"]) != 2
        or len(node["out"]) != 1
    ):
        return None
    _validate_node_binding(target, node, locations)
    minimum = [signed_interval_bits(*bounds[value], target["width"]) for value in node["args"]]
    selected = [next(bits for bits in bins if bits >= required) for required in minimum]
    if selected == [target["width"], target["width"]]:
        return None
    return prove_range_site(target, node, bounds, *selected, locations=locations)


def validate_range_entry(target, node, entry, bounds, *, locations=None):
    contract = entry.get("input_contract")
    if not isinstance(contract, dict) or set(contract) != {"signed_operand_bits"}:
        raise ValueError("unsupported signed operand input contract")
    bits = contract["signed_operand_bits"]
    if not isinstance(bits, list) or len(bits) != 2:
        raise ValueError("signed operand contract requires an ordered pair of widths")
    proof = prove_range_site(target, node, bounds, *bits, locations=locations)
    if proof is None:
        raise ValueError("both signed operand contracts are not proved by this graph")
    spec = entry.get("spec")
    if not isinstance(spec, dict):
        raise ValueError("invalid signed range multiplier leaf specification")
    expected = dict(
        leaf_spec(target["width"], target["fraction_bits"], *bits),
        integration_lowering=INTEGRATION_LOWERING,
    )
    key = hashlib.sha256(canonical(expected).encode()).hexdigest()[:20]
    if canonical(spec) != canonical(expected) or entry.get("key") != key:
        raise ValueError("signed range multiplier leaf specification/key mismatch")
    width = target["width"]
    if (
        entry.get("op") != "mul"
        or entry.get("params") != {}
        or entry.get("args") != [list(range(width)), list(range(width, 2 * width))]
        or entry.get("outs") != [list(range(2 * width, 3 * width))]
    ):
        raise ValueError("signed range multiplier requires the full-width native XOR interface")
    return proof
