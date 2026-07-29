import math

import pytest

from research.paper_a.benchmark import (
    BENCHMARK, DomainError, by_id, validate_domain,
)


def test_benchmark_has_fifty_rows_with_unique_ids():
    assert len(BENCHMARK) == 50
    assert len({c.id for c in BENCHMARK}) == 50
    assert [c.id for c in BENCHMARK] == [f"E{i:03d}" for i in range(1, 51)]


def test_every_s0_reproduces_the_construction_rule():
    """S0 = 100 * m_F * exp(-0.05 T), stored to 8 decimals."""
    for c in BENCHMARK:
        expected = round(100.0 * c.m_F * math.exp(-0.05 * c.T), 8)
        assert c.S0 == expected, f"{c.id}: stored {c.S0}, rule gives {expected}"


def test_weights_are_equal_and_sum_to_one():
    assert all(c.weight == 0.02 for c in BENCHMARK)
    assert math.isclose(sum(c.weight for c in BENCHMARK), 1.0, abs_tol=1e-12)


def test_canonical_order_is_moneyness_then_maturity_then_volatility():
    keys = [(c.m_F, c.T, c.sigma) for c in BENCHMARK]
    assert keys == sorted(keys)


def test_grid_is_the_full_cartesian_product():
    assert sorted({c.m_F for c in BENCHMARK}) == [0.80, 0.90, 1.00, 1.10, 1.20]
    assert sorted({c.T for c in BENCHMARK}) == [0.25, 0.50, 1.00, 1.50, 2.00]
    assert sorted({c.sigma for c in BENCHMARK}) == [0.15, 0.30]


def test_fixed_parameters_are_frozen():
    assert all(c.K == 100 and c.r == 0.05 for c in BENCHMARK)


def test_by_id_round_trips():
    assert by_id("E022").sigma == 0.30
    assert by_id("E022").T == 0.25
    with pytest.raises(KeyError):
        by_id("E051")


def test_spot_check_against_frozen_annex_a_values():
    assert by_id("E001").S0 == 79.00622404
    assert by_id("E025").S0 == 95.12294245
    assert by_id("E050").S0 == 108.58049016


@pytest.mark.parametrize("kwargs,code", [
    (dict(S0=0.0), "NONPOSITIVE_SPOT"),
    (dict(S0=-1.0), "NONPOSITIVE_SPOT"),
    (dict(K=0.0), "NONPOSITIVE_STRIKE"),
    (dict(r=-0.01), "RATE_OUT_OF_RANGE"),
    (dict(r=0.11), "RATE_OUT_OF_RANGE"),
    (dict(T=0.24), "MATURITY_OUT_OF_RANGE"),
    (dict(T=2.01), "MATURITY_OUT_OF_RANGE"),
    (dict(sigma=0.1499), "VOLATILITY_OUT_OF_RANGE"),
    (dict(sigma=0.3001), "VOLATILITY_OUT_OF_RANGE"),
    (dict(dividend=0.01), "NONZERO_DIVIDEND_UNSUPPORTED"),
])
def test_out_of_domain_inputs_raise_named_errors(kwargs, code):
    base = dict(S0=100.0, K=100.0, r=0.05, T=1.0, sigma=0.20, dividend=0.0)
    base.update(kwargs)
    with pytest.raises(DomainError) as exc:
        validate_domain(**base)
    assert exc.value.code == code


def test_domain_boundaries_are_inclusive():
    for kwargs in (dict(T=0.25), dict(T=2.00), dict(sigma=0.15),
                   dict(sigma=0.30), dict(r=0.0), dict(r=0.10)):
        base = dict(S0=100.0, K=100.0, r=0.05, T=1.0, sigma=0.20)
        base.update(kwargs)
        validate_domain(**base)  # must not raise


def test_no_clamping_occurs():
    """The research package rejects low sigma; it never silently clamps
    to 0.15 the way the dashboard's src/quantum.py does."""
    with pytest.raises(DomainError):
        validate_domain(S0=100.0, K=100.0, r=0.05, T=1.0, sigma=0.10)


def test_every_benchmark_row_is_in_domain():
    for c in BENCHMARK:
        validate_domain(S0=c.S0, K=c.K, r=c.r, T=c.T, sigma=c.sigma)


def test_strata_labels_are_consistent_with_parameters():
    m_expected = {0.80: "M1", 0.90: "M2", 1.00: "M3", 1.10: "M4", 1.20: "M5"}
    t_expected = {0.25: "T1", 0.50: "T2", 1.00: "T3", 1.50: "T4", 2.00: "T5"}
    for c in BENCHMARK:
        assert c.m_stratum.startswith(m_expected[c.m_F])
        assert c.t_stratum.startswith(t_expected[c.T])
        assert c.vol_stratum.startswith("V1" if c.sigma == 0.15 else "V2")


def test_contract_is_immutable():
    with pytest.raises(Exception):
        BENCHMARK[0].S0 = 1.0
