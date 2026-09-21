import math
from collections import Counter

import pytest

from research.paper_a.benchmark import (
    BENCHMARK, C6, C12, DomainError, N5, VALIDATION_SET, by_id,
    replacement_id, validate_domain,
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


def test_frozen_subsets_have_exactly_the_annex_a1_members():
    assert C12 == ("E001", "E006", "E009", "E014", "E017", "E022",
                   "E025", "E030", "E033", "E038", "E042", "E049")
    assert C6 == ("E001", "E014", "E025", "E030", "E038", "E049")
    assert N5 == ("E001", "E009", "E030", "E042")


def test_subsets_are_nested_inside_the_benchmark():
    ids = {c.id for c in BENCHMARK}
    assert set(C12) <= ids
    assert set(C6) <= set(C12)
    assert set(N5) <= set(C12)


def test_c12_balance_matches_the_documented_claim():
    rows = [by_id(i) for i in C12]
    assert Counter(r.m_stratum[:2] for r in rows) == {
        "M1": 3, "M2": 2, "M3": 3, "M4": 2, "M5": 2}
    assert Counter(r.vol_stratum[:2] for r in rows) == {"V1": 6, "V2": 6}
    t_counts = Counter(r.t_stratum[:2] for r in rows)
    assert set(t_counts) == {"T1", "T2", "T3", "T4", "T5"}
    assert min(t_counts.values()) >= 2


def test_c6_covers_every_moneyness_and_maturity_stratum():
    rows = [by_id(i) for i in C6]
    assert len({r.m_stratum[:2] for r in rows}) == 5
    assert len({r.t_stratum[:2] for r in rows}) == 5
    assert Counter(r.vol_stratum[:2] for r in rows) == {"V1": 3, "V2": 3}


def test_c6_contains_the_moneyness_maturity_diagonal():
    diagonal = {("M1", "T1"), ("M2", "T2"), ("M3", "T3"),
                ("M4", "T4"), ("M5", "T5")}
    present = {(by_id(i).m_stratum[:2], by_id(i).t_stratum[:2]) for i in C6}
    assert diagonal <= present


def test_n5_has_balanced_volatility_and_corner_coverage():
    rows = [by_id(i) for i in N5]
    assert Counter(r.vol_stratum[:2] for r in rows) == {"V1": 2, "V2": 2}
    assert {r.t_stratum[:2] for r in rows} == {"T1", "T5"}


def test_validation_set_is_disjoint_from_the_benchmark():
    """V01-V12 are deterministic fixtures only; they carry no stochastic
    claim and must never be mistaken for benchmark rows."""
    assert len(VALIDATION_SET) == 12
    assert {c.S0 for c in VALIDATION_SET} <= {80.0, 90.0, 100.0, 110.0, 120.0}
    assert not ({c.S0 for c in VALIDATION_SET} & {c.S0 for c in BENCHMARK})


def test_validation_set_is_in_domain():
    for c in VALIDATION_SET:
        validate_domain(S0=c.S0, K=c.K, r=c.r, T=c.T, sigma=c.sigma)


def test_replacement_pool_covers_every_broad_cell_uniquely():
    seen = set()
    for m in ("M1", "M2", "M3", "M4", "M5"):
        for t in ("S", "M", "L"):
            for v in ("V1", "V2"):
                rid = replacement_id(m, t, v)
                assert rid == f"R-{m}-{t}-{v}"
                assert rid not in seen
                seen.add(rid)
    assert len(seen) == 30
