"""Continuous-GBM barrier anti-concentration with explicit missing error proofs.

The finite paired Box-Muller law is not asserted to be Gaussian or independent.
All probability bounds here concern the original continuous model. A coupled
digital path needs separately proved discrepancy, clipping and tail bounds.
"""

from __future__ import annotations

import ast
from fractions import Fraction
import hashlib
import json
from math import factorial, isqrt
from pathlib import Path

from research.limitation_program_20261001.financial_bounded_schedule import pi_interval


ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
FORMAT = "continuous-gbm-one-date-barrier-band-certificate-v1"
PRECISION = 224
TAYLOR_TERMS = 192
PROOF = {
    "factorization": (
        "At date t>0, S_i(t)=S0*exp((r-sigma^2/2)t+sigma*sqrt(rho*t)Z"
        "+sigma*sqrt((1-rho)*t)Z_i). Conditioning on all idiosyncratic Brownian"
        " shocks gives B(t)=exp(s_c Z)W, s_c=sigma*sqrt(rho*t)>0, W>0 finite"
        " almost surely. The original independent continuous common Brownian"
        " driver makes Z standard Gaussian and independent of W."
    ),
    "density": (
        "For 0<=eta<H, the event H-eta<=B<=H+eta restricts Z to an interval"
        " of length L/s_c, L=log((H+eta)/(H-eta)). Its probability is at most"
        " min(1,L/(s_c*sqrt(2*pi))) for every W, hence also unconditionally."
    ),
    "interval_maximum": (
        "Writing d=L/(2*s_c), a shifted interval has probability"
        " g(c)=Phi(c+d)-Phi(c-d). Its derivative is phi(c+d)-phi(c-d),"
        " nonpositive for c>=0 and nonnegative for c<=0. Thus its exact"
        " shift-independent supremum is g(0)=2*Phi(d)-1. No observed W or"
        " financial sample enters this bound."
    ),
    "strict_barrier": (
        "Conditional on any finite positive W, B has a continuous lognormal"
        " law. Every deterministic endpoint, including B=H, has probability"
        " zero after averaging over W. The original alive test B<H and"
        " knockout convention B>=H are preserved; digital equality is not"
        " claimed to have probability zero."
    ),
    "coupling": (
        "If |B_digital-B_continuous|<=eta outside a separately bounded bad"
        " event E, then differing one-date barrier decisions imply E or"
        " |B_continuous-H|<=eta. Apply the unconditional Gaussian band bound"
        " plus P(E). Conditioning on E's complement can destroy Gaussian"
        " independence and is never used."
    ),
    "relative_log_band": (
        "If a proved per-stock multiplicative/log discrepancy, including"
        " native exp and clipping, bounds each stock ratio between exp(-delta)"
        " and exp(delta), the positive equal-weight basket obeys the same"
        " ratio bounds. Different barrier decisions require"
        " H*exp(-delta)<=B_continuous<=H*exp(delta), whose log length is"
        " exactly 2*delta. The symmetric dollar radius H*(exp(delta)-1) also"
        " covers this band because 2-exp(delta)<=exp(-delta)."
    ),
    "dollar_bias": (
        "Given separately proved already-discounted smooth-payoff error"
        " zeta on the good domain, a discounted cap on the barrier-switch"
        " payoff difference, an any-contractual-date band probability and"
        " discounted bad-domain tail dollars, triangle inequality gives"
        " dollar_bias<=zeta+cap*P(any band)+tail_dollars. A one-date band"
        " alone supplies none of the remaining terms or full-path coverage."
        " The original native output is already discounted: no second"
        " discount is applied."
    ),
    "numerics": (
        "Exact rational Machin pi intervals, integer-square-root enclosures"
        " and dyadic outward arithmetic are used. log((1+x)/(1-x)) is"
        " enclosed by its positive atanh series and geometric remainder."
        " The centered Gaussian integral uses the integrated Taylor series"
        " for exp(-z^2/2); Taylor's derivative bound gives remainder"
        " <=8^(2m+3)/(2^(m+1)*(m+1)!*(2m+3)) for 0<=z<=8. Larger"
        " arguments use monotonicity and the rigorous probability cap one."
    ),
}


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def exact(value):
    if isinstance(value, (float, bool)):
        raise ValueError("Exact rational input required")
    if isinstance(value, (list, tuple)):
        if len(value) != 2 or any(type(item) is not int for item in value) or value[1] <= 0:
            raise ValueError("Exact rational input required")
        return Fraction(*value)
    if not isinstance(value, (Fraction, int, str)):
        raise ValueError("Exact rational input required")
    return Fraction(value)


def original_model(case="B4x12", builder_path=BUILDER):
    if case not in ("B4x12", "B8x52"):
        raise ValueError("Original B4/B8 model required")
    builder_path = Path(builder_path)
    names = ("SIGMA", "CORR", "S0", "RATE", "T", "K", "H")
    bindings = []
    for node in ast.parse(builder_path.read_text(encoding="utf-8")).body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Tuple) and all(
            isinstance(item, ast.Name) for item in target.elts
        ):
            if tuple(item.id for item in target.elts) == names:
                bindings.append(tuple(Fraction(str(item)) for item in ast.literal_eval(node.value)))
    expected = (
        Fraction(3, 10),
        Fraction(2, 5),
        Fraction(100),
        Fraction(3, 100),
        Fraction(1),
        Fraction(100),
        Fraction(140),
    )
    if bindings != [expected]:
        raise ValueError("Original builder financial parameters changed")
    assets, dates = (4, 12) if case == "B4x12" else (8, 52)
    return {
        "case": case,
        "assets": assets,
        "dates": dates,
        "volatility_exact": pair(expected[0]),
        "correlation_exact": pair(expected[1]),
        "spot_dollars_exact": pair(expected[2]),
        "rate_exact": pair(expected[3]),
        "maturity_years_exact": pair(expected[4]),
        "strike_dollars_exact": pair(expected[5]),
        "barrier_dollars_exact": pair(expected[6]),
        "equal_asset_volatility": True,
        "basket": "positive equal-weight arithmetic spot basket",
        "builder_path": str(builder_path.resolve()),
        "builder_sha256": hashlib.sha256(builder_path.read_bytes()).hexdigest(),
        "continuous_driver_law": "independent common and idiosyncratic Brownian drivers",
        "digital_paired_outputs_claimed_independent_gaussian": False,
    }


def common_variance(model, date=1):
    if type(date) is not int or not 1 <= date <= model["dates"]:
        raise ValueError("Original contractual observation date required")
    sigma, rho, maturity = (
        exact(model[name])
        for name in ("volatility_exact", "correlation_exact", "maturity_years_exact")
    )
    if sigma <= 0 or not 0 < rho <= 1 or maturity <= 0 or not model["equal_asset_volatility"]:
        raise ValueError("Positive common Gaussian factor with equal volatility required")
    return sigma**2 * rho * maturity * date / model["dates"]


def sqrt_interval(value, precision=PRECISION):
    value = exact(value)
    if value < 0 or type(precision) is not int or precision < 16:
        raise ValueError("Nonnegative square root and positive precision required")
    scale = 1 << precision
    floor = isqrt(value.numerator * scale**2 // value.denominator)
    lower = Fraction(floor, scale)
    return lower, lower if lower**2 == value else Fraction(floor + 1, scale)


def _round(interval, precision):
    scale = 1 << precision
    lower, upper = interval
    lo = lower.numerator * scale // lower.denominator
    hi = -((-upper.numerator * scale) // upper.denominator)
    return Fraction(lo, scale), Fraction(hi, scale)


def _multiply(a, b, precision):
    products = [x * y for x in a for y in b]
    return _round((min(products), max(products)), precision)


def log_ratio_interval(eta, barrier, terms=TAYLOR_TERMS):
    eta, barrier = exact(eta), exact(barrier)
    if barrier <= 0 or not 0 <= eta < barrier or type(terms) is not int or terms < 1:
        raise ValueError("A band with 0<=eta<H is required")
    if eta == 0:
        return Fraction(0), Fraction(0)
    x = eta / barrier
    lower = 2 * sum((x ** (2 * k + 1) / (2 * k + 1) for k in range(terms)), Fraction(0))
    remainder = 2 * x ** (2 * terms + 1) / ((2 * terms + 1) * (1 - x**2))
    return _round((lower, lower + remainder), PRECISION)


def _centered_normal_interval(argument, terms=TAYLOR_TERMS):
    lower, upper = argument
    if not 0 <= lower <= upper:
        raise ValueError("Nonnegative ordered Gaussian interval argument required")
    if upper == 0:
        return Fraction(0), Fraction(0)
    if upper > 8:
        inside = _centered_normal_interval((min(lower, Fraction(8)),) * 2, terms)
        return inside[0], Fraction(1)
    work_precision = PRECISION + 8 * terms
    z = _multiply(argument, argument, work_precision)
    z = (z[0] / 2, z[1] / 2)
    polynomial = (Fraction((-1) ** terms, factorial(terms) * (2 * terms + 1)),) * 2
    for k in range(terms - 1, -1, -1):
        product = _multiply(polynomial, z, work_precision)
        coefficient = Fraction((-1) ** k, factorial(k) * (2 * k + 1))
        polynomial = _round((product[0] + coefficient, product[1] + coefficient), work_precision)
    integral = _multiply(argument, polynomial, work_precision)
    remainder = Fraction(
        8 ** (2 * terms + 3), 2 ** (terms + 1) * factorial(terms + 1) * (2 * terms + 3)
    )
    pi_lo, pi_hi = pi_interval()
    prefactor = (sqrt_interval(2 / pi_hi)[0], sqrt_interval(2 / pi_lo)[1])
    enclosed = _multiply((integral[0] - remainder, integral[1] + remainder), prefactor, PRECISION)
    return max(Fraction(0), enclosed[0]), min(Fraction(1), enclosed[1])


def bounds_for_log_length(log_length, variance):
    """The two proved bounds, for any positive conditional W and exact variance."""
    if not isinstance(log_length, (list, tuple)) or len(log_length) != 2:
        raise ValueError("Ordered exact log-length interval required")
    lower, upper = map(exact, log_length)
    variance = exact(variance)
    if not 0 <= lower <= upper or variance <= 0:
        raise ValueError("Positive variance and nonnegative ordered log length required")
    sc_lo, sc_hi = sqrt_interval(variance)
    pi_lo, pi_hi = pi_interval()
    denominator = (sqrt_interval(2 * pi_lo * variance)[0], sqrt_interval(2 * pi_hi * variance)[1])
    if sc_lo == 0 or denominator[0] == 0:
        raise ArithmeticError("Exact variance is too small for the declared enclosure precision")
    density = (min(Fraction(1), lower / denominator[1]), min(Fraction(1), upper / denominator[0]))
    maximum = _centered_normal_interval((lower / (2 * sc_hi), upper / (2 * sc_lo)))
    maximum = (maximum[0], min(maximum[1], density[1]))
    return {
        "log_length_interval_exact": [pair(lower), pair(upper)],
        "common_log_variance_exact": pair(variance),
        "common_log_standard_deviation_interval_exact": [pair(sc_lo), pair(sc_hi)],
        "density": {
            "formula": "min(1,L/(s_c*sqrt(2*pi)))",
            "interval_exact": [pair(density[0]), pair(density[1])],
            "probability_upper_exact": pair(density[1]),
        },
        "centered_interval_maximum": {
            "formula": "2*Phi(L/(2*s_c))-1",
            "interval_exact": [pair(maximum[0]), pair(maximum[1])],
            "probability_upper_exact": pair(maximum[1]),
            "uniform_over_all_positive_W": True,
        },
        "finite_financial_samples_used": 0,
        "bound_methods": 2,
    }


def band_bounds(eta_dollars, barrier_dollars, variance):
    result = bounds_for_log_length(log_ratio_interval(eta_dollars, barrier_dollars), variance)
    result.update(
        eta_dollars_exact=pair(exact(eta_dollars)),
        barrier_dollars_exact=pair(exact(barrier_dollars)),
    )
    return result


def radius_from_log_discrepancy(delta, barrier):
    """Rigorous H*expm1(delta) enclosure, without supplying a discrepancy proof."""
    delta, barrier = exact(delta), exact(barrier)
    if not 0 <= delta <= Fraction(1, 2) or barrier <= 0:
        raise ValueError("Local relative-log radius needs 0<=delta<=1/2 and H>0")
    lower = sum((delta**k / factorial(k) for k in range(1, 81)), Fraction(0))
    remainder = delta**81 / factorial(81) / (1 - delta / 82)
    return [pair(barrier * lower), pair(barrier * (lower + remainder))]


def _external_claim(pointer, kind, model, date=None):
    if pointer is None:
        return None
    path = Path(pointer["path"]).resolve()
    if hashlib.sha256(path.read_bytes()).hexdigest() != pointer["sha256"]:
        raise ValueError("External proof artifact changed")
    claim = json.loads(path.read_text(encoding="utf-8"))["claims"][pointer["claim"]]
    scope = (
        {"case": model["case"], "date": date}
        if date is not None
        else {"case": model["case"], "all_contractual_dates": True}
    )
    if (
        claim["kind"] != kind
        or claim["scope"] != scope
        or claim.get("proved") is not True
        or claim.get("measure") != "continuous-underlying-uniform-coupling"
        or not isinstance(claim.get("coupling_id"), str)
        or not claim["coupling_id"]
    ):
        raise ValueError("External proof claim kind, measure, scope or status changed")
    value = exact(claim["upper_exact"])
    if value < 0 or (kind in ("bad-event-probability", "any-date-band-probability") and value > 1):
        raise ValueError("External proof bound outside its domain")
    if kind in ("basket-absolute-error", "all-stocks-log-relative-error") and (
        claim.get("native_exp_and_clipping_included") is not True
    ):
        raise ValueError("Native exponential and clipping discrepancy proof required")
    if kind in (
        "discounted-smooth-payoff-error",
        "discounted-path-payoff-cap",
        "discounted-tail-dollars",
    ):
        if claim.get("already_discounted") is not True:
            raise ValueError("Proved dollar bound must already include the original discount")
    return {
        "upper_exact": pair(value),
        "coupling_id": claim["coupling_id"],
        "artifact": pointer,
        "theorem_externally_proved": True,
        "external_theorem_reproved_here": False,
    }


def assemble_dollar_bias(
    model, zeta_proof=None, cap_proof=None, any_band_proof=None, tail_proof=None
):
    pointers = (zeta_proof, cap_proof, any_band_proof, tail_proof)
    kinds = (
        "discounted-smooth-payoff-error",
        "discounted-path-payoff-cap",
        "any-date-band-probability",
        "discounted-tail-dollars",
    )
    components = {
        kind: _external_claim(pointer, kind, model)
        for kind, pointer in zip(kinds, pointers, strict=True)
    }
    present = [claim for claim in components.values() if claim is not None]
    if len({claim["coupling_id"] for claim in present}) > 1:
        raise ValueError("Dollar error terms bind different couplings")
    bound = None
    if len(present) == 4:
        zeta, cap, bands, tail = (exact(components[kind]["upper_exact"]) for kind in kinds)
        bound = pair(zeta + cap * bands + tail)
    return {
        "components": components,
        "dollar_bias_upper_exact": bound,
        "formula": (
            "discounted_zeta+discounted_payoff_cap*P(any contractual-date band)"
            "+discounted_tail_dollars"
        ),
        "second_discount_applied": False,
        "missing_bounds_are_zero": False,
        "full_G2_certificate": False,
    }


def certify_one_date(
    case="B4x12", date=1, eta_proof=None, log_proof=None, bad_probability_proof=None
):
    model = original_model(case)
    variance = common_variance(model, date)
    if eta_proof is not None and log_proof is not None:
        raise ValueError("One proved discrepancy route required per certificate")
    eta = _external_claim(eta_proof, "basket-absolute-error", model, date)
    log = _external_claim(log_proof, "all-stocks-log-relative-error", model, date)
    bad = _external_claim(bad_probability_proof, "bad-event-probability", model, date)
    present = [claim for claim in (eta, log, bad) if claim is not None]
    if len({claim["coupling_id"] for claim in present}) > 1:
        raise ValueError("Barrier discrepancy and bad event bind different couplings")
    actual = None
    if eta is not None:
        actual = band_bounds(eta["upper_exact"], model["barrier_dollars_exact"], variance)
    elif log is not None:
        delta = exact(log["upper_exact"])
        actual = bounds_for_log_length((2 * delta, 2 * delta), variance)
        actual["delta_log_upper_exact"] = pair(delta)
        if delta <= Fraction(1, 2):
            actual["derived_symmetric_eta_interval_exact"] = radius_from_log_discrepancy(
                delta, model["barrier_dollars_exact"]
            )
    disagreement = None
    if actual is not None and bad is not None:
        disagreement = pair(
            min(
                Fraction(1),
                exact(bad["upper_exact"])
                + exact(actual["centered_interval_maximum"]["probability_upper_exact"]),
            )
        )
    return {
        "format": FORMAT,
        "model": model,
        "date": date,
        "observation_time_exact": pair(
            exact(model["maturity_years_exact"]) * date / model["dates"]
        ),
        "common_log_variance_exact": pair(variance),
        "proof": PROOF,
        "eta": eta,
        "path_log_discrepancy": log,
        "bad_event_probability": bad,
        "proved_discrepancy_band_bounds": actual,
        "one_date_decision_disagreement_upper_exact": disagreement,
        "discounted_smooth_payoff_zeta": None,
        "discounted_tail_dollars": None,
        "any_contractual_date_band_probability": None,
        "dollar_bias_upper_exact": None,
        "full_G2_certificate": False,
        "digital_paired_outputs_claimed_independent_gaussian": False,
        "gaussian_law_conditioned_on_coupling_good_event": False,
        "all_contractual_dates_covered": False,
        "finite_financial_samples_used": 0,
        "missing_bounds_are_zero": False,
        "second_discount_applied": False,
    }
