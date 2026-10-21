"""Exact continuous-band enclosures and null-aware coupling/error composition."""

from fractions import Fraction
import hashlib
import json

import mpmath as mp
import pytest

from research.limitation_program_20261001.barrier_band_certificate import (
    assemble_dollar_bias,
    band_bounds,
    bounds_for_log_length,
    certify_one_date,
    common_variance,
    exact,
    log_ratio_interval,
    original_model,
    pair,
    radius_from_log_discrepancy,
    sqrt_interval,
)


def _mp(value):
    value = exact(value)
    return mp.mpf(value.numerator) / value.denominator


def _inside(value, interval):
    lower, upper = map(_mp, interval)
    assert lower <= value <= upper


@pytest.mark.parametrize(
    "case,variance", [("B4x12", Fraction(3, 1000)), ("B8x52", Fraction(9, 13000))]
)
def test_original_continuous_model_parameters_and_first_date_common_factor(case, variance):
    model = original_model(case)
    assert common_variance(model, 1) == variance
    assert common_variance(model, model["dates"]) == Fraction(9, 250)
    assert model["barrier_dollars_exact"] == [140, 1]
    assert not model["digital_paired_outputs_claimed_independent_gaussian"]


@pytest.mark.parametrize("date", [0, 13, True, 1.0])
def test_common_factor_rejects_noncontractual_dates(date):
    with pytest.raises(ValueError, match="contractual"):
        common_variance(original_model(), date)


@pytest.mark.parametrize(
    "field,value",
    [
        ("volatility_exact", [0, 1]),
        ("correlation_exact", [0, 1]),
        ("correlation_exact", [6, 5]),
        ("maturity_years_exact", [-1, 1]),
    ],
)
def test_conditional_model_requires_positive_common_factor(field, value):
    model = original_model()
    model[field] = value
    with pytest.raises(ValueError, match="Positive common"):
        common_variance(model)


def test_original_builder_parameter_change_is_rejected(tmp_path):
    path = tmp_path / "builder.py"
    path.write_text(
        "SIGMA, CORR, S0, RATE, T, K, H = .3, .4, 100., .03, 1., 100., 141.\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="parameters changed"):
        original_model(builder_path=path)


@pytest.mark.parametrize("value", [0, 1, Fraction(3, 1000), Fraction(2), Fraction(1, 10**12)])
def test_integer_square_root_enclosure_is_exact(value):
    lower, upper = sqrt_interval(value)
    assert lower**2 <= value <= upper**2
    assert upper - lower <= Fraction(1, 1 << 224)


@pytest.mark.parametrize(
    "eta",
    [Fraction(0), Fraction(1, 10000), Fraction(1, 10), Fraction(10), Fraction(50), Fraction(139)],
)
def test_two_rigorous_band_enclosures_contain_independent_transcendentals(eta):
    with mp.workdps(120):
        barrier, variance = Fraction(140), Fraction(3, 1000)
        actual = band_bounds(eta, barrier, variance)
        length = mp.log((_mp(barrier) + _mp(eta)) / (_mp(barrier) - _mp(eta)))
        scale = mp.sqrt(_mp(variance))
        density = min(mp.mpf(1), length / (scale * mp.sqrt(2 * mp.pi)))
        maximum = mp.erf(length / (2 * scale * mp.sqrt(2)))
        _inside(density, actual["density"]["interval_exact"])
        _inside(maximum, actual["centered_interval_maximum"]["interval_exact"])
        assert exact(actual["centered_interval_maximum"]["probability_upper_exact"]) <= exact(
            actual["density"]["probability_upper_exact"]
        )
        assert actual["bound_methods"] == 2 and actual["finite_financial_samples_used"] == 0


def test_fixed_small_band_has_tighter_gaussian_maximum():
    result = band_bounds(Fraction(1, 10000), 140, Fraction(3, 1000))
    density_lower = exact(result["density"]["interval_exact"][0])
    gaussian_upper = exact(result["centered_interval_maximum"]["probability_upper_exact"])
    assert 0 < gaussian_upper < density_lower < Fraction(1, 10000)


def test_zero_band_is_exactly_zero_in_continuous_model():
    result = band_bounds(0, 140, Fraction(3, 1000))
    assert (
        result["density"]["interval_exact"]
        == result["centered_interval_maximum"]["interval_exact"]
        == [[0, 1], [0, 1]]
    )


@pytest.mark.parametrize("eta", [-1, 140, 141])
def test_radius_domain_rejects_nonpositive_lower_endpoint(eta):
    with pytest.raises(ValueError, match="0<=eta<H"):
        band_bounds(eta, 140, Fraction(3, 1000))


def test_shift_independent_maximum_encloses_every_selected_positive_w():
    # These analytic shifts test implementation. The derivative theorem, not
    # the finite list, establishes the uniform supremum over all positive W.
    eta, barrier, variance = Fraction(1), Fraction(140), Fraction(3, 1000)
    result = band_bounds(eta, barrier, variance)
    with mp.workdps(100):
        scale = mp.sqrt(_mp(variance))
        lower = mp.log(_mp(barrier - eta))
        upper = mp.log(_mp(barrier + eta))
        center = (lower + upper) / 2
        bound = _mp(result["centered_interval_maximum"]["probability_upper_exact"])

        def phi(x):
            return (1 + mp.erf(x / mp.sqrt(2))) / 2

        for shift in (-10, -1, 0, 1, 10):
            log_W = center + shift * scale
            probability = phi((upper - log_W) / scale) - phi((lower - log_W) / scale)
            assert 0 <= probability <= bound


@pytest.mark.parametrize(
    "delta", [Fraction(0), Fraction(1, 10**8), Fraction(1, 10), Fraction(1, 2)]
)
def test_local_relative_log_radius_covers_both_barrier_sides(delta):
    interval = radius_from_log_discrepancy(delta, 140)
    with mp.workdps(1000):
        exact_radius = 140 * mp.expm1(_mp(delta))
        _inside(exact_radius, interval)
        assert 140 * (1 - mp.exp(-_mp(delta))) <= _mp(interval[1])
    assert exact(interval[1]) < 140


@pytest.mark.parametrize("value", [0.1, True, [1, 0], [1.0, 2], [1, 2, 3]])
def test_certificate_inputs_require_exact_rationals(value):
    with pytest.raises(ValueError, match="Exact rational"):
        exact(value)


def _artifact(tmp_path, name, kind, upper, date=1, **changes):
    scope = (
        {"case": "B4x12", "date": date}
        if date is not None
        else {"case": "B4x12", "all_contractual_dates": True}
    )
    claim = {
        "kind": kind,
        "upper_exact": pair(upper),
        "scope": scope,
        "proved": True,
        "coupling_id": "synthetic-exact-theorem-fixture",
        "measure": "continuous-underlying-uniform-coupling",
        "native_exp_and_clipping_included": True,
        "already_discounted": True,
    }
    claim.update(changes)
    path = tmp_path / (name + ".json")
    path.write_text(json.dumps({"claims": {name: claim}}), encoding="utf-8")
    return {
        "path": str(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "claim": name,
    }


def test_no_radius_or_bad_event_is_silently_replaced_with_zero():
    result = certify_one_date()
    for field in (
        "eta",
        "path_log_discrepancy",
        "bad_event_probability",
        "proved_discrepancy_band_bounds",
        "one_date_decision_disagreement_upper_exact",
        "discounted_smooth_payoff_zeta",
        "discounted_tail_dollars",
        "any_contractual_date_band_probability",
        "dollar_bias_upper_exact",
    ):
        assert result[field] is None
    assert not result["full_G2_certificate"] and not result["missing_bounds_are_zero"]
    assert not result["gaussian_law_conditioned_on_coupling_good_event"]
    assert not result["digital_paired_outputs_claimed_independent_gaussian"]


def test_proved_one_date_radius_adds_separate_bad_probability(tmp_path):
    eta = _artifact(tmp_path, "eta", "basket-absolute-error", Fraction(1, 10000))
    bad = _artifact(tmp_path, "bad", "bad-event-probability", Fraction(3, 1 << 20))
    result = certify_one_date(eta_proof=eta, bad_probability_proof=bad)
    band = result["proved_discrepancy_band_bounds"]["centered_interval_maximum"]
    assert exact(result["one_date_decision_disagreement_upper_exact"]) == (
        exact(band["probability_upper_exact"]) + Fraction(3, 1 << 20)
    )
    assert result["dollar_bias_upper_exact"] is None and not result["all_contractual_dates_covered"]


def test_proved_log_radius_uses_exact_log_length_and_keeps_full_path_open(tmp_path):
    delta = Fraction(1, 100000)
    proof = _artifact(tmp_path, "log", "all-stocks-log-relative-error", delta)
    result = certify_one_date(log_proof=proof)
    actual = result["proved_discrepancy_band_bounds"]
    assert actual["log_length_interval_exact"] == [pair(2 * delta), pair(2 * delta)]
    assert actual["derived_symmetric_eta_interval_exact"] == radius_from_log_discrepancy(delta, 140)
    assert result["one_date_decision_disagreement_upper_exact"] is None


@pytest.mark.parametrize(
    "changes",
    [
        {"proved": False},
        {"native_exp_and_clipping_included": False},
        {"scope": {"case": "B8x52", "date": 1}},
        {"measure": "finite-digital-Gaussian-independence"},
    ],
)
def test_incomplete_or_wrong_discrepancy_proof_is_rejected(tmp_path, changes):
    proof = _artifact(tmp_path, "eta", "basket-absolute-error", Fraction(1, 10000), **changes)
    with pytest.raises(ValueError):
        certify_one_date(eta_proof=proof)


def test_changed_external_artifact_is_rejected(tmp_path):
    proof = _artifact(tmp_path, "eta", "basket-absolute-error", Fraction(1, 10000))
    from pathlib import Path

    Path(proof["path"]).write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="artifact changed"):
        certify_one_date(eta_proof=proof)


def test_discrepancy_and_bad_event_cannot_use_different_couplings(tmp_path):
    eta = _artifact(tmp_path, "eta", "basket-absolute-error", Fraction(1, 10000))
    bad = _artifact(
        tmp_path, "bad", "bad-event-probability", Fraction(3, 1 << 20), coupling_id="different"
    )
    with pytest.raises(ValueError, match="different couplings"):
        certify_one_date(eta_proof=eta, bad_probability_proof=bad)


def test_dollar_bias_requires_every_full_path_term_and_discounts_once(tmp_path):
    model = original_model()
    missing = assemble_dollar_bias(model)
    assert missing["dollar_bias_upper_exact"] is None and not missing["missing_bounds_are_zero"]
    zeta = _artifact(
        tmp_path, "zeta", "discounted-smooth-payoff-error", Fraction(1, 1000), date=None
    )
    cap = _artifact(tmp_path, "cap", "discounted-path-payoff-cap", 40, date=None)
    bands = _artifact(tmp_path, "bands", "any-date-band-probability", Fraction(1, 10000), date=None)
    tail = _artifact(tmp_path, "tail", "discounted-tail-dollars", Fraction(1, 1000), date=None)
    assert assemble_dollar_bias(model, zeta, cap, bands)["dollar_bias_upper_exact"] is None
    complete = assemble_dollar_bias(model, zeta, cap, bands, tail)
    assert exact(complete["dollar_bias_upper_exact"]) == Fraction(3, 500)
    assert not complete["second_discount_applied"] and not complete["full_G2_certificate"]


def test_dollar_term_must_already_include_discount(tmp_path):
    zeta = _artifact(
        tmp_path,
        "zeta",
        "discounted-smooth-payoff-error",
        Fraction(1, 1000),
        date=None,
        already_discounted=False,
    )
    with pytest.raises(ValueError, match="already include"):
        assemble_dollar_bias(original_model(), zeta_proof=zeta)


def test_bad_event_claim_cannot_be_called_smooth_payoff_zeta(tmp_path):
    bad = _artifact(tmp_path, "bad", "bad-event-probability", Fraction(3, 1 << 20), date=None)
    with pytest.raises(ValueError, match="claim kind"):
        assemble_dollar_bias(original_model(), zeta_proof=bad)


def test_log_ratio_remainder_contains_true_value_near_radius_boundary():
    interval = log_ratio_interval(139, 140)
    with mp.workdps(100):
        _inside(mp.log(279), [pair(value) for value in interval])


def test_unresolvable_variance_cannot_create_division_by_zero_certificate():
    with pytest.raises(ArithmeticError, match="too small"):
        bounds_for_log_length((1, 1), Fraction(1, 1 << 1000))
