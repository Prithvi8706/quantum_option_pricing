import pytest

from research.paper_a.benchmark import BENCHMARK, by_id
from research.paper_a.errors import (
    deterministic_ladder, identity_residual, total_mean_error,
)
from research.paper_a.payoff import C_RESCALING

# The value select_support_rule() actually returns over the 50-contract
# benchmark (established in Task 5). 1e-4 is NOT the frozen rule: at 1e-4,
# 14/50 contracts breach the 1e-4*S0 support-bias bound.
Q = 1e-5


def test_ladder_layers_are_stored_separately():
    lad = deterministic_ladder(by_id("E022"), Q, 3, C_RESCALING)
    values = [lad.P_BS, lad.P_support, lad.P_grid, lad.P_circuit]
    assert len(set(values)) == 4, "layers must not collapse onto each other"


def test_signed_components_telescope_to_p_circuit_minus_p_bs():
    for cid in ("E001", "E022", "E025", "E050"):
        lad = deterministic_ladder(by_id(cid), Q, 3, C_RESCALING)
        total = lad.e_support + lad.e_grid + lad.e_encode
        assert abs(total - (lad.P_circuit - lad.P_BS)) <= 1e-10 * max(
            1.0, by_id(cid).S0)


def test_each_component_is_the_difference_of_its_own_two_layers():
    lad = deterministic_ladder(by_id("E025"), Q, 3, C_RESCALING)
    assert abs(lad.e_support - (lad.P_support - lad.P_BS)) < 1e-14
    assert abs(lad.e_grid - (lad.P_grid - lad.P_support)) < 1e-14
    assert abs(lad.e_encode - (lad.P_circuit - lad.P_grid)) < 1e-14


def test_full_identity_residual_is_within_the_frozen_tolerance():
    c = by_id("E025")
    lad = deterministic_ladder(c, Q, 3, C_RESCALING)
    e_est, d_noise = 0.031, -0.017
    e_total = total_mean_error(lad, e_est, d_noise)
    residual = identity_residual(lad, e_est, d_noise, e_total)
    assert abs(residual) <= 1e-10 * max(1.0, c.S0)


def test_identity_detects_a_corrupted_total():
    c = by_id("E025")
    lad = deterministic_ladder(c, Q, 3, C_RESCALING)
    bad = total_mean_error(lad, 0.031, -0.017) + 0.5
    assert abs(identity_residual(lad, 0.031, -0.017, bad)) > 1e-10 * c.S0


def test_signs_are_preserved_so_cancellation_stays_visible():
    """Components must be able to cancel. If any contract has mixed-sign
    components, stacking absolute magnitudes must give a different answer
    from the signed sum -- that difference IS the cancellation the paper
    reports, and it is destroyed if signs are dropped anywhere."""
    found_mixed = False
    for c in BENCHMARK:
        lad = deterministic_ladder(c, Q, 3, C_RESCALING)
        parts = (lad.e_support, lad.e_grid, lad.e_encode)
        if len({p > 0 for p in parts}) > 1:
            found_mixed = True
            assert abs(sum(parts) - sum(abs(p) for p in parts)) > 1e-9, c.id
    assert found_mixed, "no mixed-sign contract found; cancellation untested"


def test_support_error_is_small_under_the_frozen_rule():
    for cid in ("E001", "E025", "E050"):
        c = by_id(cid)
        lad = deterministic_ladder(c, Q, 3, C_RESCALING)
        assert abs(lad.e_support) <= 1e-4 * c.S0


@pytest.mark.slow
def test_identity_holds_for_every_contract_and_qubit_count():
    for c in BENCHMARK:
        for n in (3, 4):
            lad = deterministic_ladder(c, Q, n, C_RESCALING)
            total = lad.e_support + lad.e_grid + lad.e_encode
            assert abs(total - (lad.P_circuit - lad.P_BS)) <= 1e-10 * max(
                1.0, c.S0), f"{c.id} n={n}"
