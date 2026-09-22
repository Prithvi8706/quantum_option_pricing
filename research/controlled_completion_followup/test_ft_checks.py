"""Regression checks for synthesis conventions and conditional resource accounting."""

import json
from fractions import Fraction
from pathlib import Path

import mpmath as mp

from research.controlled_completion_followup.ft_model import BUDGET, logical_error
from research.controlled_completion_followup.synthesis_rotations import (
    OUTPUT,
    ROOT,
    interval_error_squared,
    target_angle,
    verify,
)


def test_every_archived_sequence_has_directed_interval_certificate():
    assert verify(json.loads(OUTPUT.read_text())) == 95


def test_malformed_rotation_is_rejected_at_actual_tolerance():
    record = json.loads(OUTPUT.read_text())["rotations"]["radian_1_2"]
    assert interval_error_squared(record["target"], "") > Fraction(1, 10**30)


def test_signed_controlled_phase_and_global_phase_conventions():
    mp.mp.dps = 100
    payload = json.loads(OUTPUT.read_text())
    epsilon = mp.mpf(1) / payload["common_operator_epsilon_exact"][1]
    rt = mp.sqrt(2)
    omega = mp.exp(mp.j * mp.pi / 4)
    matrices = {
        "H": mp.matrix([[1, 1], [1, -1]]) / rt,
        "T": mp.diag([1, omega]),
        "S": mp.diag([1, mp.j]),
        "X": mp.matrix([[0, 1], [1, 0]]),
        "W": mp.eye(2) * omega,
    }
    cx = mp.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])

    def kron(a, b):
        return mp.matrix(
            [[a[i // 2, j // 2] * b[i % 2, j % 2] for j in range(4)] for i in range(4)]
        )

    for record in payload["rotations"].values():
        unitary = mp.eye(2)
        for gate in record["matrix_product_gates"]:
            unitary = unitary * matrices[gate]
        for sign in (-1, 1):
            angle = sign * target_angle(record["target"], mp.mp)
            u = unitary if sign == 1 else unitary.H
            actual = kron(u, u) * cx * kron(mp.eye(2), u.H) * cx * mp.exp(mp.j * angle / 2)
            desired = mp.diag([1, 1, 1, mp.exp(2 * mp.j * angle)])
            # Certificate is in the interval test above. This independent
            # high-precision diagnostic checks the signed two-qubit wiring.
            assert mp.norm(actual - desired) <= 6 * epsilon


def test_distances_cover_whole_live_exposure_and_budget():
    path = ROOT / "results/controlled_completion_followup/ft_scenarios.json"
    payload = json.loads(path.read_text())
    assert sum(BUDGET.values()) == 0.002
    assert Path(payload["ledger_path"].replace("\\", "/")).name == "ledger.json"
    for row in payload["rows"]:
        for scenario in row["scenarios"]:
            d = scenario["distance"]
            assert d % 2 == 1
            assert scenario["logical_fault_union_bound"] <= BUDGET["logical_faults"]
            assert scenario["conditional_physical_failure_upper"] <= 0.002
            factory = scenario["factory"]
            assert factory["magic_error_union_bound"] <= BUDGET["magic_state_errors"]
            assert factory["retry_exhaustion_union_bound"] <= BUDGET["exhausted_retries"]
            # Holding the actual exposure fixed, two fewer code-distance
            # units fail. The runtime itself also depends on distance.
            assert (
                scenario["logical_patch_round_exposure_upper"]
                * logical_error(scenario["physical_error_probability_assumption"], d - 2)
                > BUDGET["logical_faults"]
            )
