"""Pre-acquisition week-12 checks; no development observations acquired."""

import inspect
import math

import pytest
from scipy.optimize import brentq
from scipy.stats import binom

from research.journal_sprint.allocation_rule import allocate, cp_decision
from research.journal_sprint.encoding_decision import Encoding
from research.journal_sprint.unequal_allocation import (
    ARMS, PILOT, TARGET_FRACTION, candidate_counts, choose_batch,
    forecast_radius, terminal_decision,
)


E = Encoding("fixture", 20., -2., .1, 1.)


@pytest.mark.parametrize("arm", ARMS)
@pytest.mark.parametrize("successes", [0, 512, 1024])
def test_plan_counts_and_repeatability(arm, successes):
    pilot = successes if arm in ("pilot_cp", "unequal_full", "unequal_target") else None
    plan = choose_batch(E, arm, pilot)
    assert plan == choose_batch(E, arm, pilot)
    assert 0 < plan.total_shots <= 65536
    assert min(plan.m0, plan.m1, plan.n) >= 256
    assert plan.pilot_shots == (PILOT if pilot is not None else 0)
    if arm in ("fixed_cp", "pilot_cp", "unequal_full"):
        assert plan.total_shots == 65536
    assert math.isfinite(plan.forecast_radius)


def test_historical_arms_preserved():
    fixed = choose_batch(E, "fixed_cp")
    assert (fixed.m0, fixed.m1, fixed.n) == (16384, 16384, 32768)
    old = allocate(E, 38, guard=.003)
    paid = choose_batch(E, "pilot_cp", 38, guard=.003)
    assert (paid.m0, paid.m1, paid.n) == (
        old['calibration_per_state'], old['calibration_per_state'], old['pricing_shots'])


@pytest.mark.parametrize("arm", ["unequal_target", "fixed_target"])
def test_target_is_cheapest_eligible_not_best_after_observation(arm):
    e = Encoding("easy", 2., 0., .01, 1.)
    pilot = 28 if arm == 'unequal_target' else None
    plan = choose_batch(e, arm, pilot)
    q = (28.5/1025) if pilot is not None else .475
    candidates = [(forecast_radius(e, q, *c), c) for c in candidate_counts(plan.pilot_shots)]
    eligible = [(r, c) for r, c in candidates if r <= TARGET_FRACTION]
    assert eligible
    _, c = min(eligible, key=lambda x: (sum(x[1])+plan.pilot_shots, x[0], *x[1]))
    assert (plan.m0, plan.m1, plan.n) == c
    assert plan.total_shots == 8192


def test_infeasible_forecast_executes_honest_fallback():
    e = Encoding("large", 1000., 0., .99, 1.)
    plan = choose_batch(e, "unequal_target", 30, guard=.03)
    assert not plan.forecast_target_met
    assert plan.n > 0 and plan.total_shots <= 65536
    assert 'no delivery promise' in plan.rationale


@pytest.mark.parametrize("bad", [None, True, -1, 1025, .5, float('nan')])
def test_invalid_paid_pilot(bad):
    with pytest.raises(ValueError):
        choose_batch(E, 'unequal_target', bad)


@pytest.mark.parametrize("arm", ['fixed_cp', 'fixed_target'])
def test_fixed_arm_rejects_pilot(arm):
    with pytest.raises(ValueError):
        choose_batch(E, arm, 42)


@pytest.mark.parametrize("guard", [-1, 1.01, True, float('nan'), float('inf')])
def test_bad_guard(guard):
    with pytest.raises(ValueError):
        choose_batch(E, 'fixed_target', guard=guard)


def test_unknown_bias_and_exhausted_bias_rejected():
    with pytest.raises(ValueError):
        Encoding('unknown', 1, 0, None, 1)
    with pytest.raises(ValueError):
        choose_batch(Encoding('exhausted', 1, 0, 1, 1), 'fixed_target')
    with pytest.raises(ValueError):
        choose_batch(E, 'unknown')
    with pytest.raises(ValueError):
        candidate_counts(True)


def binomial_interval(s, n, alpha):
    lo = 0. if s == 0 else brentq(lambda p: binom.sf(s-1, n, p)-alpha/2, 0., 1.)
    hi = 1. if s == n else brentq(lambda p: binom.cdf(s, n, p)-alpha/2, 0., 1.)
    return lo, hi


@pytest.mark.parametrize('cal', [(0, 0), (10, 120), (128, 200)])
@pytest.mark.parametrize('s', [0, 350, 2000])
@pytest.mark.parametrize('guard', [0., .003, .03])
def test_unequal_endpoints_against_binomial_tail_inversion(cal, s, guard):
    m0, m1, n = 512, 2048, 2000
    actual = terminal_decision(E, s, n, list(cal), m0, m1, guard)
    fl, fu = binomial_interval(cal[0], m0, .0125)
    gl, gu = binomial_interval(cal[1], m1, .0125)
    ql, qu = binomial_interval(s, n, .025)
    fl, gl = max(0., fl-guard), max(0., gl-guard)
    fu, gu = min(1., fu+guard), min(1., gu+guard)
    assert fu+gu < 1
    lo = max(0., (ql-fu)/(1-fu-gl))
    hi = min(1., (qu-fl)/(1-fl-gu))
    if lo > hi:
        assert actual['interval'] is None
    else:
        expected = [E.offset+E.sensitivity*lo-E.bias, E.offset+E.sensitivity*hi+E.bias]
        assert actual['interval'] == pytest.approx(expected, abs=2e-8)


def test_equal_count_terminal_matches_old_inference():
    old = cp_decision(E, 300, 4096, [20, 70], 1024, .003)
    new = terminal_decision(E, 300, 4096, [20, 70], 1024, 1024, .003)
    assert {key: new[key] for key in old} == old


def test_nonidentifiable_readout_does_not_narrow_set():
    actual = terminal_decision(E, 0, 100, [90, 90], 100, 100)
    assert actual['interval'] == pytest.approx([-2.1, 18.1])
    assert actual['status'] != 'precision_met'


@pytest.mark.parametrize('args', [
    (True, 10, [0, 0], 10, 20), (11, 10, [0, 0], 10, 20),
    (1, 10, [11, 0], 10, 20), (1, 10, [0, 21], 10, 20),
    (1, 10, [0], 10, 20), (1, 10, [0, 0], 0, 20),
])
def test_invalid_terminal_counts(args):
    with pytest.raises(ValueError):
        terminal_decision(E, *args)


def test_no_truth_or_pilot_pooling_interface():
    assert set(inspect.signature(choose_batch).parameters) == {
        'encoding', 'arm', 'pilot_successes', 'guard', 'tolerance'}
    assert 'pilot_successes' not in inspect.signature(terminal_decision).parameters


@pytest.mark.parametrize('n', [5, 13])
def test_cp_coordinate_coverage_by_exhaustive_binomial_sum(n):
    for probability in (.01, .2, .5, .99):
        misses = sum(binom.pmf(s, n, probability) for s in range(n+1)
                     if not (lambda bounds: bounds[0] <= probability <= bounds[1])(
                         binomial_interval(s, n, .0125)))
        assert misses <= .0125+1e-10
