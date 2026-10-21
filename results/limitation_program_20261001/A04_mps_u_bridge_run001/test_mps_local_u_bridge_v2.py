"""Six fixed bridge fixtures; actual rows come from the sole saved SDK call."""

from copy import deepcopy
from fractions import Fraction
import json
import os
from pathlib import Path

import pytest

from research.limitation_program_20261001.mps_local_u_bridge_v2 import (
    ALLOWANCE,
    binary64_pair,
    bridge,
    certify,
    exact,
    identity,
    interval_operator,
    interval_tools,
    inverse,
    iv_exact,
    residual,
)


def actual():
    directory = Path(os.environ["MPS_LOCAL_U_BRIDGE_SOURCE"])
    return [
        json.loads((directory / name).read_text(encoding="utf-8"))
        for name in ("sdk_operations.json", "native_operations.json", "native_inverse.json")
    ]


def small_source(n=1):
    return dict(
        schema="one-local-SDK-U-CX-v1",
        local_qubits=n,
        global_wires=list(range(n)),
        sdk_calls=1,
        sdk_global_phase_exact=[0, 1],
        operations=[dict(op="u", wires=[0], params_exact=[[0, 1], [2, 1], [0, 1]])],
    )


def phase_reference():
    iv = interval_tools()
    zero, one, angle = iv.mpf(0), iv.mpf(1), iv_exact(iv, 2)
    return [[(one, zero), (zero, zero)], [(zero, zero), (iv.cos(angle), iv.sin(angle))]]


def test_actual_source_mapping_and_complete_phase_inventory():
    sdk, native, saved_inverse = actual()
    assert native == bridge(sdk)
    assert sdk["local_qubits"] == 3 and sdk["global_wires"] == [10, 11, 8]
    assert saved_inverse["operations"] == inverse(native["operations"])
    paid = exact(sdk["sdk_global_phase_exact"])
    for row in sdk["operations"]:
        if row["op"] == "u":
            paid += (exact(row["params_exact"][1]) + exact(row["params_exact"][2])) / 2
    assert exact(native["aggregate_phase_exact"]) == paid
    assert native["operations"][-1] == dict(
        op="phase", wires=[], angle_exact=[paid.numerator, paid.denominator]
    )


def test_actual_emitted_native_inverse_restores_complete_operator():
    _, native, saved_inverse = actual()
    restored = interval_operator(native["operations"] + saved_inverse["operations"], 3)
    assert exact(residual(restored, identity(3), True)["operator_error_upper_exact"]) <= ALLOWANCE


def test_paid_phase_matches_small_explicit_full_operator():
    native = bridge(small_source())
    assert native["aggregate_phase_exact"] == [1, 1]
    operator = interval_operator(native["operations"], 1)
    assert exact(residual(operator, phase_reference())["operator_error_upper_exact"]) <= ALLOWANCE


def test_missing_scalar_phase_is_detected_on_full_operator():
    native = bridge(small_source())
    operator = interval_operator(native["operations"][:-1], 1)
    assert exact(residual(operator, phase_reference())["squared_Frobenius_lower_exact"]) > Fraction(
        1, 100
    )


def test_exact_parameter_wire_arity_and_alphabet_mutations_reject():
    for angle in ([True, 1], [2, 2], [1, -1], [1, 3]):
        changed = small_source()
        changed["operations"][0]["params_exact"][0] = angle
        with pytest.raises(ValueError):
            bridge(changed)
    for wires in ([-1], [0, 0], [True], [1]):
        changed = small_source()
        changed["operations"][0]["wires"] = wires
        with pytest.raises(ValueError):
            bridge(changed)
    changed = deepcopy(small_source())
    changed["operations"][0]["op"] = "h"
    with pytest.raises(ValueError, match="Only actual SDK u/cx"):
        bridge(changed)
    changed = small_source()
    changed["sdk_global_phase_exact"] = binary64_pair(float("0.25"))
    assert (
        bridge(changed)["aggregate_phase_exact"] != bridge(small_source())["aggregate_phase_exact"]
    )
    with pytest.raises(ValueError, match="Exact SDK-to-native mapping"):
        certify(changed, bridge(small_source()), {})


def test_small_cx_full_basis_reference_and_literal_inverse():
    source = small_source(2)
    source["operations"] = [dict(op="cx", wires=[0, 1], params_exact=[])]
    native = bridge(source)
    expected = [
        [
            (Fraction(row == (column ^ 2 if column & 1 else column)), Fraction(0))
            for column in range(4)
        ]
        for row in range(4)
    ]
    operator = interval_operator(native["operations"], 2)
    assert exact(residual(operator, expected, True)["operator_error_upper_exact"]) <= ALLOWANCE
    restored = interval_operator(native["operations"] + inverse(native["operations"]), 2)
    assert exact(residual(restored, identity(2), True)["operator_error_upper_exact"]) <= ALLOWANCE
