"""Independent algebra/coverage checks plus decision regression tests."""

import math

import numpy as np
import pytest
from scipy.stats import binom

from research.journal_sprint.encoding_decision import (
    Encoding, Rectangle, calibration_menu, fixed_price_interval, plan_menu, radius_bound,
)


def test_known_readout_recovers_hoeffding_budget():
    e = Encoding("a", 10.0, -2.0, 0.1, 5.0)
    r = Rectangle(0.02, 0.02, 0.07, 0.07)
    plan = plan_menu([e], {"a": r}, 1, {"a": 100000}, 100, 2)
    expected = math.ceil(math.log(80) / 2 * (10 / (0.91 * 0.9)) ** 2)
    assert plan["shots"] == expected
    assert plan["total_shots"] == expected + 200
    assert plan["total_cost"] == expected * 5 + 400
    assert radius_bound(e, r, expected) <= 1
    assert radius_bound(e, r, expected - 1) > 1


def test_encoding_selection_is_not_gate_count_alone():
    a, b = Encoding("cheap_gate", 20, 0, 0.5, 1), Encoding("smaller_scale", 2, 0, 0, 5)
    r = Rectangle(0, 0, 0, 0)
    plan = plan_menu([a, b], {a.name: r, b.name: r}, 1,
                     {a.name: 100000, b.name: 100000}, 100, 1)
    assert plan["selected"] == "smaller_scale"
    assert plan["calibration_shots"] == 400


@pytest.mark.parametrize("r", [Rectangle(.01, .04, .05, .09), Rectangle(0, .1, 0, .2)])
def test_uniform_propagation_at_nuisance_corners(r):
    e = Encoding("e", 3, -7, .2, 1)
    n = 500
    h = math.sqrt(math.log(80) / (2 * n))
    for a in np.linspace(0, 1, 31):
        for f in (r.fl, r.fu):
            for g in (r.gl, r.gu):
                q = f + (1 - f - g) * a
                for sign in (-1, 1):
                    qhat = min(1, max(0, q + sign * h))
                    ahat = min(1, max(0, (qhat - (r.fl + r.fu) / 2) / r.contrast))
                    assert abs(a - ahat) <= (h + r.uncertainty) / r.contrast + 1e-14
                    for bias in (-e.bias, e.bias):
                        assert abs(3 * ahat - (3 * a + bias)) <= radius_bound(e, r, n) + 1e-14


@pytest.mark.parametrize("a", [0, .01, .3, .5, .99, 1])
def test_exact_binomial_noncoverage_below_validation_alpha(a):
    e, r, n = Encoding("e", 5, -2, .1, 1), Rectangle(.01, .04, .05, .09), 100
    for f, g in [(r.fl, r.gl), (r.fl, r.gu), (r.fu, r.gl), (r.fu, r.gu)]:
        q = f + (1 - f - g) * a
        for deterministic_error in [-e.bias, e.bias]:
            truth = e.offset + e.sensitivity * a + deterministic_error
            miss = 0
            for s in range(n + 1):
                lo, hi = fixed_price_interval(e, r, s, n)
                if not lo <= truth <= hi:
                    miss += binom.pmf(s, n, q)
            assert miss <= .025 + 1e-12


def test_more_uncertainty_cannot_improve_certificate():
    e = Encoding("a", 10, 0, .1, 1)
    tight, wide = Rectangle(.02, .02, .07, .07), Rectangle(.01, .03, .06, .08)
    assert radius_bound(e, wide, 1000) > radius_bound(e, tight, 1000)


@pytest.mark.parametrize("bias,r,status", [
    (1, Rectangle(0, 0, 0, 0), "bias_bound_exhausts_tolerance"),
    (0, Rectangle(.4, .6, .4, .6), "contrast_uncertified"),
    (0, Rectangle(0, .4, 0, .4), "calibration_bound_exhausts_tolerance"),
    (0, Rectangle(0, 0, 0, 0), "budget_not_certified"),
])
def test_refusal_reasons_and_sunk_calibration(bias, r, status):
    e = Encoding("a", 10, 0, bias, 1)
    plan = plan_menu([e], {"a": r}, 1, {"a": 1}, 10, 1)
    assert plan["selected"] is None
    assert plan["scores"][0]["status"] == status
    assert plan["total_shots"] == plan["total_cost"] == 20


def test_menu_correction_widens_calibration():
    one = calibration_menu({"a": [2, 7]}, 100)["a"]
    two = calibration_menu({"a": [2, 7], "b": [2, 7]}, 100)["a"]
    assert two.fl < one.fl < one.fu < two.fu
    assert two.gl < one.gl < one.gu < two.gu


@pytest.mark.parametrize("bad", [True, -1, float("nan"), float("inf")])
def test_invalid_sensitivity_rejected(bad):
    with pytest.raises(ValueError):
        Encoding("e", bad, 0, 0, 1)


def test_counts_and_menu_rejected():
    for counts in ([True, 2], [101, 2], [1.5, 2]):
        with pytest.raises(ValueError):
            calibration_menu({"e": counts}, 100)
    e, r = Encoding("a", 1, 0, 0, 1), Rectangle(0, 0, 0, 0)
    with pytest.raises(ValueError):
        plan_menu([e, e], {"a": r}, 1, {"a": 100}, 10, 1)
    with pytest.raises(ValueError):
        fixed_price_interval(e, r, 101, 100)


def test_tie_is_deterministic_and_no_truth_interface():
    a, b, r = Encoding("a", 1, 0, 0, 1), Encoding("b", 1, 0, 0, 1), Rectangle(0, 0, 0, 0)
    assert plan_menu([b, a], {"a": r, "b": r}, 1, {"a": 100, "b": 100}, 10, 0)[
        "selected"
    ] == "a"
    assert set(Encoding.__dataclass_fields__) == {
        "name", "sensitivity", "offset", "bias", "cost_per_shot",
    }


def test_nested_manifest_is_checked_not_excluded(tmp_path):
    from research.journal_sprint.run_encoding_decision import verify_inventory
    from research.journal_sprint.storage import finish_run, write_json

    (tmp_path / "input").mkdir()
    write_json(tmp_path / "input/complete.json", {"source": "fixture"})
    finish_run(tmp_path)
    assert verify_inventory(tmp_path) == 1
    (tmp_path / "input/complete.json").unlink()
    with pytest.raises(ValueError, match="inventory"):
        verify_inventory(tmp_path)


def test_calibration_coordinate_exact_coverage():
    # Reference sum over every possible outcome, not a Monte Carlo success count.
    n = 20
    for f in (.01, .1, .5, .9, .99):
        miss = 0.0
        for s in range(n + 1):
            rect = calibration_menu({"a": [s, 0], "b": [0, 0]}, n)["a"]
            if not rect.fl <= f <= rect.fu:
                miss += binom.pmf(s, n, f)
        assert miss <= .025 / 4 + 1e-12
