"""Canonical admission for exact full-domain coefficient frontier leaves."""

import hashlib

from research.controlled_source_completion.constant_multiplier import (
    LOWERING as CONSTANT_LOWERING,
    STRATEGIES as ORIGINAL_STRATEGIES,
)
from research.controlled_source_completion.prefix_constant_multiplier import (
    ALGORITHM as PREFIX_ALGORITHM,
    LOWERING as PREFIX_LOWERING,
    STRATEGIES as PREFIX_STRATEGIES,
    leaf_spec as prefix_leaf_spec,
)
from research.limitation_program_20261001.constant_library import canonical

INTEGRATION_LOWERING = "same-target-full-domain-coefficient-library-v1"
FRONTIER = "full-native-unrestricted-signed-v1"
STRATEGIES = ORIGINAL_STRATEGIES + PREFIX_STRATEGIES


def frontier_leaf_spec(width, fraction_bits, coefficient, strategy):
    """Canonical standalone frontier specification for either exact circuit family."""
    if (
        any(type(value) is not int for value in (width, fraction_bits, coefficient))
        or width < 1
        or not 0 <= fraction_bits <= width
        or not isinstance(strategy, str)
        or strategy not in STRATEGIES
    ):
        raise ValueError("native integer precision, coefficient and known strategy required")
    if strategy in PREFIX_STRATEGIES:
        spec = prefix_leaf_spec(width, fraction_bits, coefficient, strategy)
    else:
        spec = {
            "op": "cmul",
            "width": width,
            "fraction_bits": fraction_bits,
            "params": {"c": coefficient},
            "coefficient": coefficient,
            "zero_bits": 0,
            "strategy": strategy,
            "lowering": CONSTANT_LOWERING,
            "input_contract": {"zero_low_bits": 0},
        }
    return dict(spec, coefficient_frontier=FRONTIER)


def coefficient_leaf_spec(width, fraction_bits, coefficient, strategy):
    """Bind the standalone specification to this immutable-source integration."""
    return dict(
        frontier_leaf_spec(width, fraction_bits, coefficient, strategy),
        integration_lowering=INTEGRATION_LOWERING,
    )


def is_coefficient_entry(entry):
    """Notice any surviving unique family marker, including a partial specification."""
    spec = entry.get("spec")
    return "coefficient_frontier" in entry or (
        isinstance(spec, dict)
        and (
            spec.get("integration_lowering") == INTEGRATION_LOWERING
            or "coefficient_frontier" in spec
            or spec.get("lowering") == PREFIX_LOWERING
            or spec.get("algorithm") == PREFIX_ALGORITHM
            or spec.get("strategy") in PREFIX_STRATEGIES
        )
    )


def validate_coefficient_entry(target, node, entry, *, locations=None):
    """Require the exact coefficient, canonical key and full native XOR interface."""
    width = target["width"]
    spec, contract = entry.get("spec"), entry.get("input_contract")
    if entry.get("coefficient_frontier") != FRONTIER:
        raise ValueError("coefficient leaf family marker is missing or invalid")
    if (
        not isinstance(contract, dict)
        or set(contract) != {"zero_low_bits"}
        or type(contract["zero_low_bits"]) is not int
        or contract["zero_low_bits"] != 0
    ):
        raise ValueError("coefficient leaf requires the unrestricted zero-low contract")
    if not isinstance(spec, dict):
        raise ValueError("invalid coefficient leaf specification")
    coefficient = node.get("params", {}).get("c")
    if (
        node.get("op") != "cmul"
        or type(coefficient) is not int
        or node.get("params") != {"c": coefficient}
        or len(node.get("args", ())) != 1
        or len(node.get("out", ())) != 1
    ):
        raise ValueError("coefficient leaf must bind to the native cmul operation")
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
        raise ValueError("coefficient invocation is not bound to the validated target")
    expected = coefficient_leaf_spec(
        width, target["fraction_bits"], coefficient, spec.get("strategy")
    )
    key = hashlib.sha256(canonical(expected).encode()).hexdigest()[:20]
    if canonical(spec) != canonical(expected) or entry.get("key") != key:
        raise ValueError("coefficient leaf specification/key mismatch")
    if (
        entry.get("op") != "cmul"
        or canonical(entry.get("params")) != canonical({"c": coefficient})
        or canonical(entry.get("args")) != canonical([list(range(width))])
        or canonical(entry.get("outs")) != canonical([list(range(width, 2 * width))])
    ):
        raise ValueError("coefficient leaf requires the full native clean-XOR interface")
    return {
        "coefficient": coefficient,
        "strategy": spec["strategy"],
        "input_contract": {"zero_low_bits": 0},
        "no_narrowed_input_promise": True,
        "all_native_signed_patterns": True,
        "theorem": "Exact floor(signed(x) * c / 2**fraction_bits), modulo 2**width",
    }
