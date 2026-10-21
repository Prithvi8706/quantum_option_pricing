"""One fixed source-bound AS241/native-financial bias method, not a compiler.

No intervals, proof classes, graphs or financial observations are evaluated on
import. The producer admits only the complete new source and its exact ledger.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial
import time

import mpmath as mp

from research.limitation_program_20261001.as241_financial_native_v2 import (
    EPS,
    S,
    ceildiv,
    check_word,
    exact,
    financial_word_bounds,
    native_support,
    pair,
    polynomial_intervals,
    polynomial_model,
    polynomial_template,
    producers,
    require,
)

DIGITS = 90
GRID_N = 1 << 32
G = Fraction(13, 2)
ALLOWANCE = Fraction(11, 2000)
EXPONENTS = tuple(range(-17, 13))
CDF_DEGREE = 160
CPU_LIMIT = 180

PROOF = """
The target consists of independent copies of the saved signed-restored scalar
AS241 SSA followed by a verbatim, boundary-normalized original financial DAG.
For each raw word use the same exact Gaussian midpoint driver X and native Z.
The scalar receipt proves |Z-X|<=E. The endpoint CDF proof, symmetry and
monotonicity prove |X|<=13/2 for every q32 midpoint. Actual increment literals,
their two signed multiplication floors and exact prefixes give Lambda_j.

The actual degree12 Estrin DAG is expanded as a polynomial. Its exact integer
coefficients, every multiplication floor and Taylor remainder are bounded on
all30 native exponent classes. Actual k is floor(x_raw*Cinv/S^2), not the real
logarithm's exponent. k*Cln has no extra floor. The paid final right-shift floor
is at most1/S; left shifts need full-word safety. Thus nativeExp(x) lies between
(1-alpha)exp(x)-beta and (1+alpha)exp(x)+beta, alpha<1,beta=1/S.

Raw prefixes are not recursively clipped. Lower stock clipping is paid by the
deterministic additive l=(1+alpha)exp(lo_hat)+beta. An upper-clamp event may be
removed only if nativeExp(hi_hat)>=na*H and exp(hi_hat-Lambda_j)>na*H. Each
then forces the corresponding monitored basket to knock out in BOTH paths.
Without that event, a_j*S-beta<=S_native<=b_j*S+l, where
a_j=(1-alpha)exp(-Lambda_j), b_j=(1+alpha)exp(Lambda_j).

The actual binary basket coefficient and its floor imply disagreement only in
the closed ideal band [(H-l)/b_j,(H+beta+1/S)/a_j]. Under continuous Gaussian
drivers, condition only on idiosyncratic drivers: log basket has an independent
normal common factor of variance sigma^2*rho*t_j. Its unconditional density
bound is log(U/L)/sqrt(2*pi*sigma^2*rho*t_j). For the exact independent midpoint
grid, each fixed-coordinate closed-band indicator has total variation<=2.
The product telescope pays d_j/2^32, including endpoint ties. A union bound
over dates gives p_switch. No conditioning on survival/clamps is used.

On both-alive paths the ideal mean and unrounded native mean are below H.
Native Asian coefficient rounding and its output floor are explicitly paid;
native discount coefficient error and its output floor are paid once. The
actual integer alive-only support calculation includes that same Asian
coefficient and proves 0<=Y_native<40. Every eagerly evaluated financial
register, including dead paths, is separately proved free of native wrapping.
Hence |P_native-P_cont|<=40*d/2^32+zeta+40*p_switch.

This is a NEW source-matched bias ledger. It neither fills the accepted joint
Box-Muller obligation nor transfers source/wrapper costs, compiler dispatch,
hardware time or quantum advantage. The scalar KS(E) law is not an extra term.
"""


class BudgetCensoredError(RuntimeError):
    pass


def check_cpu(started):
    if time.process_time() - started > CPU_LIMIT:
        raise BudgetCensoredError("Fixed180-second process CPU limit")


def iv(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoint(value):
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def bounds(value):
    return tuple(endpoint(part) for part in value._mpi_)


def interval(lower, upper):
    require(lower <= upper, "Ordered outward interval")
    return mp.iv.mpf([iv(lower).a, iv(upper).b])


def upper(value):
    return bounds(value)[1]


def abs_upper(value):
    return max(map(abs, bounds(value)))


def pi_interval():
    """Exact100-term Machin alternating-series enclosure, then outward mp.iv."""
    pieces = []
    for denominator in (5, 239):
        lower = sum(
            (Fraction((-1) ** j, (2 * j + 1) * denominator ** (2 * j + 1)) for j in range(100)),
            Fraction(0),
        )
        pieces.append((lower, lower + Fraction(1, 201 * denominator**201)))
    return interval(16 * pieces[0][0] - 4 * pieces[1][1], 16 * pieces[0][1] - 4 * pieces[1][0])


def true_midpoint_quantile_bracket(started):
    """Fixed analytic endpoint evaluation; no normal quantile library calls."""
    check_cpu(started)
    pi = pi_interval()
    x = iv(G)
    s = x * x / 2
    term = total = iv(1)
    for k in range(1, CDF_DEGREE + 1):
        term = term * s / k
        total += (-1) ** k * term / (2 * k + 1)
    remainder = G ** (2 * CDF_DEGREE + 3) / (
        2 ** (CDF_DEGREE + 1) * factorial(CDF_DEGREE + 1) * (2 * CDF_DEGREE + 3)
    )
    cdf_negative = iv(Fraction(1, 2)) - (x * total + interval(-remainder, remainder)) / mp.iv.sqrt(
        2 * pi
    )
    lo, hi = bounds(cdf_negative)
    require(
        0 < lo <= hi < Fraction(1, 2 * GRID_N), "TRUE extreme midpoint quantile6.5 bracket failed"
    )
    return {
        "true_quantile_absolute_upper_exact": pair(G),
        "Phi_minus_6p5_interval_exact": [pair(lo), pair(hi)],
        "smallest_midpoint_exact": pair(Fraction(1, 2 * GRID_N)),
        "integrated_exp_Taylor_degree": CDF_DEGREE,
        "integrated_derivative_remainder_upper_exact": pair(remainder),
        "Machin_pi_interval_exact": [pair(v) for v in bounds(pi)],
        "symmetry_and_strict_CDF_monotonicity_cover_all_q32_midpoints": True,
        "approximate_quantile_range_used_as_true_range": False,
    }


def raw_log_errors(scope, error, started):
    require(Fraction(0) <= error <= Fraction(1, 100000000), "Accepted all-input scalar E required")
    nt = scope["dates"]
    sigma, rho, rate = Fraction(3, 10), Fraction(2, 5), Fraction(3, 100)
    dt = Fraction(1, nt)
    a = iv(sigma) * mp.iv.sqrt(iv(dt * rho))
    b = iv(sigma) * mp.iv.sqrt(iv(dt * (1 - rho)))
    mu = (rate - sigma * sigma / 2) * dt
    initial_error = abs_upper(iv(Fraction(scope["initial_log_raw"], S)) - mp.iv.ln(iv(100)))
    running = initial_error
    dates = []
    for date in range(nt):
        check_cpu(started)
        ahat = Fraction(scope["common_coefficients"][date], S)
        bhat = Fraction(scope["idiosyncratic_coefficients"][date], S)
        mhat = Fraction(scope["drift_literals"][date], S)
        da, db = abs_upper(iv(ahat) - a), abs_upper(iv(bhat) - b)
        dm = abs(mhat - mu)
        inc = (abs(ahat) + abs(bhat)) * error + (da + db) * G + 2 * EPS + dm
        running += inc
        dates.append(
            {
                "date": date + 1,
                "common_coefficient_raw": scope["common_coefficients"][date],
                "idiosyncratic_coefficient_raw": scope["idiosyncratic_coefficients"][date],
                "drift_literal_raw": scope["drift_literals"][date],
                "common_literal_error_upper_exact": pair(da),
                "idiosyncratic_literal_error_upper_exact": pair(db),
                "drift_literal_error_exact": pair(dm),
                "increment_error_upper_exact": pair(inc),
                "raw_log_error_upper_exact": pair(running),
            }
        )
    return {
        "initial_log_literal_error_upper_exact": pair(initial_error),
        "dates": dates,
        "same_input_quantile_error_upper_exact": pair(error),
        "signed_constant_multiplication_floors_per_increment": 2,
        "prefix_addition_rounding_terms": 0,
        "AS241_KS_E_or_Box_Muller_coupling_added": False,
    }


def stock_exponential_proof(target, scope, started, record_class=None):
    source = producers(target)
    site = scope["sites"][0]
    template, _, _ = polynomial_template(target, site, source)
    for actual in scope["sites"]:
        check_cpu(started)
        require(
            polynomial_template(target, actual, source)[0] == template
            and (actual["inverse_ln2"], actual["ln2"]) == (site["inverse_ln2"], site["ln2"]),
            "Every actual exponential template/literal must match",
        )
    cinv, cln = site["inverse_ln2"], site["ln2"]
    lo, hi = scope["lower_log_raw"], scope["upper_log_raw"]
    require(cinv > 0 and cln > 0 and lo < hi, "Actual stock reduction literals")
    require(
        lo * cinv // (S * S) == -17 and hi * cinv // (S * S) == 12,
        "Fixed30-class actual exponent domain",
    )
    inverse_bounds = check_word((lo * cinv // S, hi * cinv // S))
    require(-(1 << 143) <= lo * cinv <= hi * cinv < 1 << 143, "Inverse ln2 product144 safety")
    ln_error = abs_upper(iv(Fraction(cln, S)) - mp.iv.ln(iv(2)))
    classes, covered, union = [], [], {}
    alpha = Fraction(0)
    point_high = None
    for k in EXPONENTS:
        check_cpu(started)
        left = max(lo, ceildiv(k * S * S, cinv))
        right = min(hi, ceildiv((k + 1) * S * S, cinv) - 1)
        if left > right:
            row = {"k": k, "empty": True, "clipped_log_raw_bounds": [left, right]}
            classes.append(row)
            if record_class is not None:
                record_class(k, row)
            continue
        remainder = left - k * cln, right - k * cln
        check_word((k * S, k * S))
        check_word((k * cln, k * cln))
        require(-(1 << 143) <= k * S * cln < 1 << 143, "Exact k*ln2 product144")
        polynomial, value_bounds, products = polynomial_intervals(target, site, remainder, source)
        require(polynomial[0] > 0, "All supported-domain polynomial words positive")
        shifted = (
            tuple(v << k for v in polynomial) if k >= 0 else tuple(v >> (-k) for v in polynomial)
        )
        check_word(shifted)
        require(shifted[0] > 0, "All supported-domain stock words strictly positive")
        radius = Fraction(max(map(abs, remainder)), S)
        coefficients, floor_error, coefficient_error, steps = polynomial_model(
            target, site, radius, source
        )
        require(len(coefficients) == 13, "Actual degree12")
        taylor = upper(mp.iv.exp(iv(radius)) * iv(radius) ** 13 / factorial(13))
        min_exp = bounds(mp.iv.exp(iv(Fraction(remainder[0], S))))[0]
        relative = (floor_error + coefficient_error + taylor) / min_exp
        q = abs(k) * ln_error
        ratio_lo = bounds(iv(1 - relative) * mp.iv.exp(-iv(q)))[0]
        ratio_hi = upper(iv(1 + relative) * mp.iv.exp(iv(q)))
        cell_alpha = max(Fraction(0), 1 - ratio_lo, ratio_hi - 1)
        alpha = max(alpha, cell_alpha)
        for value, word_bounds in value_bounds.items():
            if value in union:
                old = union[value]
                union[value] = min(old[0], word_bounds[0]), max(old[1], word_bounds[1])
            else:
                union[value] = word_bounds
        row = {
            "k": k,
            "empty": False,
            "clipped_log_raw_bounds": [left, right],
            "remainder_raw_bounds": list(remainder),
            "polynomial_raw_bounds": list(polynomial),
            "stock_raw_bounds": list(shifted),
            "radius_exact": pair(radius),
            "coefficient_error_upper_exact": pair(coefficient_error),
            "polynomial_floor_error_upper_exact": pair(floor_error),
            "degree12_Taylor_remainder_upper_exact": pair(taylor),
            "relative_polynomial_error_upper_exact": pair(relative),
            "ln2_literal_error_upper_exact": pair(ln_error),
            "relative_stock_error_upper_exact": pair(cell_alpha),
            "polynomial_floor_and_magnitude_steps": steps,
            "product144_checks": products,
            "scaled_exponent_exact": True,
            "ln2_multiply_additional_floor": 0,
        }
        classes.append(row)
        covered.append(row)
        if record_class is not None:
            record_class(k, row)
        if left <= hi <= right:
            p, _, _ = polynomial_intervals(target, site, (hi - k * cln, hi - k * cln), source)
            point_high = p[0] << k if k >= 0 else p[0] >> (-k)
    require(
        len(classes) == 30 and [r["k"] for r in classes] == list(EXPONENTS),
        "All30 classes recorded",
    )
    require(
        covered[0]["clipped_log_raw_bounds"][0] == lo
        and covered[-1]["clipped_log_raw_bounds"][1] == hi,
        "Complete clipped word endpoints",
    )
    require(
        all(
            a["clipped_log_raw_bounds"][1] + 1 == b["clipped_log_raw_bounds"][0]
            for a, b in zip(covered, covered[1:])
        ),
        "No integer gap/overlap between classes",
    )
    require(
        Fraction(0) <= alpha < 1 and point_high is not None, "Positive multiplicative stock bound"
    )
    return {
        "stock_sites": len(scope["sites"]),
        "actual_template_sha256": template,
        "classes": classes,
        "completed_classes": 30,
        "whole_clipped_word_domain_covered": True,
        "alpha_upper_exact": pair(alpha),
        "beta_upper_exact": pair(EPS),
        "stock_raw_bounds": [
            min(r["stock_raw_bounds"][0] for r in covered),
            max(r["stock_raw_bounds"][1] for r in covered),
        ],
        "remainder_raw_bounds": [
            min(r["remainder_raw_bounds"][0] for r in covered),
            max(r["remainder_raw_bounds"][1] for r in covered),
        ],
        "exponent_bounds": [-17, 12],
        "inverse_value_raw_bounds": list(inverse_bounds),
        "scaled_exponent_raw_bounds": [-17 * S, 12 * S],
        "ln_value_raw_bounds": [-17 * cln, 12 * cln],
        "polynomial_value_union_bounds": {str(value): list(v) for value, v in union.items()},
        "native_exp_upper_clamp_raw": point_high,
        "all_positive_stored72_product144_shift_safe": True,
        "native_right_shift_floor_charged_additively": True,
    }


def barrier_band(scope, exp_proof, logs, started):
    alpha, beta = exact(exp_proof["alpha_upper_exact"]), exact(exp_proof["beta_upper_exact"])
    h = Fraction(scope["barrier_raw"], S)
    pi = pi_interval()
    ell = upper(iv(1 + alpha) * mp.iv.exp(iv(Fraction(scope["lower_log_raw"], S))) + iv(beta))
    require(0 <= ell < h, "Paid deterministic lower clamp must be below H")
    require(
        exp_proof["native_exp_upper_clamp_raw"] >= scope["assets"] * scope["barrier_raw"],
        "Native upper-clamp stock must force knockout",
    )
    rows, switch = [], Fraction(0)
    for date, row in enumerate(logs["dates"], 1):
        check_cpu(started)
        lam = exact(row["raw_log_error_upper_exact"])
        a = bounds(iv(1 - alpha) * mp.iv.exp(-iv(lam)))[0]
        b = upper(iv(1 + alpha) * mp.iv.exp(iv(lam)))
        require(0 < a <= 1 <= b, "Positive expanded stock sandwich")
        high_stock = bounds(mp.iv.exp(iv(Fraction(scope["upper_log_raw"], S) - lam)))[0]
        require(high_stock > scope["assets"] * h, "Ideal upper-clamp event must also knock out")
        lower, upper_band = (h - ell) / b, (h + beta + EPS) / a
        require(0 < lower <= h <= upper_band, "Closed band covers both strict decisions")
        variance = Fraction(9, 250) * Fraction(date, scope["dates"])
        # 0.3^2*0.4 = 9/250; accumulated date time, not one-step dt.
        density_bound = upper(mp.iv.ln(iv(upper_band / lower)) / mp.iv.sqrt(2 * pi * iv(variance)))
        continuous = min(Fraction(1), density_bound)
        d_j = (scope["assets"] + 1) * date
        grid = min(Fraction(1), continuous + Fraction(d_j, GRID_N))
        switch += grid
        rows.append(
            {
                "date": date,
                "raw_log_error_upper_exact": pair(lam),
                "a_lower_exact": pair(a),
                "b_upper_exact": pair(b),
                "lower_clamp_additive_upper_exact": pair(ell),
                "ideal_band_lower_exact": pair(lower),
                "ideal_band_upper_exact": pair(upper_band),
                "accumulated_common_variance_exact": pair(variance),
                "continuous_unconditional_band_probability_upper_exact": pair(continuous),
                "grid_band_law_allowance_exact": pair(Fraction(d_j, GRID_N)),
                "grid_closed_band_probability_upper_exact": pair(grid),
                "ideal_upper_clamp_stock_lower_exact": pair(high_stock),
                "both_path_upper_knockout": True,
                "native_equality_included": True,
                "conditioning_on_survival_or_no_clamp": False,
            }
        )
    return {
        "dates": rows,
        "switch_probability_upper_exact": pair(min(Fraction(1), switch)),
        "lower_clamp_additive_upper_exact": pair(ell),
        "exact_grid_closed_band_BV_per_coordinate": 2,
        "AS241_KS_E_added": False,
        "accumulated_common_variance_not_one_step": True,
    }


def smooth_payoff_bound(scope, exp_proof, bands):
    h, m = Fraction(scope["barrier_raw"], S), scope["assets"] * scope["dates"]
    beta = exact(exp_proof["beta_upper_exact"])
    ell = exact(bands["lower_clamp_additive_upper_exact"])
    mean = (
        sum(
            (
                h * max(1 - exact(row["a_lower_exact"]), exact(row["b_upper_exact"]) - 1)
                + max(beta, ell)
                for row in bands["dates"]
            ),
            Fraction(0),
        )
        / scope["dates"]
    )
    average_rounding = m * h * abs(Fraction(scope["average_coefficient"], S) - Fraction(1, m))
    asian = mean + average_rounding + EPS
    discount = Fraction(scope["discount_coefficient"], S)
    require(0 < discount <= 1, "Original positive native discount")
    discount_error = abs_upper(iv(discount) - mp.iv.exp(iv(Fraction(-3, 100))))
    zeta = discount * asian + 40 * discount_error + EPS
    return {
        "both_alive_mean_stock_error_upper_exact": pair(mean),
        "actual_Asian_coefficient_error_upper_exact": pair(average_rounding),
        "native_Asian_floor_upper_exact": pair(EPS),
        "Asian_error_upper_exact": pair(asian),
        "actual_discount_literal_error_upper_exact": pair(discount_error),
        "native_discount_floor_upper_exact": pair(EPS),
        "already_discounted_smooth_error_upper_exact": pair(zeta),
        "discount_applied_again": False,
    }


def bias_components(dimension, smooth, switch):
    require(type(dimension) is int and dimension > 0, "Actual independent driver dimension")
    require(smooth >= 0 and 0 <= switch <= 1, "Nonnegative paid discrepancy terms")
    grid = Fraction(40 * dimension, GRID_N)
    switched = 40 * switch
    return grid, smooth, switched, grid + smooth + switched


def certify_case(
    target,
    scope,
    financial_values,
    error,
    true_bracket,
    started,
    record_stage=None,
    record_class=None,
):
    mp.iv.dps = DIGITS
    require(
        exact(true_bracket["true_quantile_absolute_upper_exact"]) == G, "TRUE grid driver bracket"
    )
    logs = raw_log_errors(scope, error, started)
    if record_stage is not None:
        record_stage("raw_log_error_proof", logs)
    exponential = stock_exponential_proof(target, scope, started, record_class)
    if record_stage is not None:
        record_stage("stock_exponential_proof", exponential)
    support = native_support(scope)
    if record_stage is not None:
        record_stage("native_support_proof", support)
    normal_bound = ceildiv((G + error).numerator * S, (G + error).denominator)
    safety = financial_word_bounds(
        target, scope, financial_values, normal_bound, exponential, lambda: check_cpu(started)
    )
    if record_stage is not None:
        record_stage("all_dead_path_native_safety", safety)
    check_cpu(started)
    bands = barrier_band(scope, exponential, logs, started)
    if record_stage is not None:
        record_stage("barrier_band_proof", bands)
    smooth = smooth_payoff_bound(scope, exponential, bands)
    if record_stage is not None:
        record_stage("smooth_payoff_proof", smooth)
    d = (scope["assets"] + 1) * scope["dates"]
    smooth_bias = exact(smooth["already_discounted_smooth_error_upper_exact"])
    grid_bias, smooth_bias, switch_bias, total = bias_components(
        d, smooth_bias, exact(bands["switch_probability_upper_exact"])
    )
    check_cpu(started)
    return {
        "case": scope["case"],
        "new_source_matched_native_financial_bias_certified": True,
        "complete_original_contract_bias_upper_exact": pair(total),
        "bias_fits_frozen_residual_financial_allowance": total <= ALLOWANCE,
        "residual_financial_allowance_dollars_exact": pair(ALLOWANCE),
        "ideal_continuous_to_exact_grid_bias_upper_exact": pair(grid_bias),
        "already_discounted_smooth_bias_upper_exact": pair(smooth_bias),
        "barrier_switch_bias_upper_exact": pair(switch_bias),
        "raw_log_error_proof": logs,
        "stock_exponential_proof": exponential,
        "native_support_proof": support,
        "all_dead_path_native_safety": safety,
        "barrier_band_proof": bands,
        "smooth_payoff_proof": smooth,
        "same_input_quantile_error_upper_exact": pair(error),
        "ideal_true_grid_normal_bound_exact": pair(G),
        "accepted_joint_Box_Muller_obligation_filled": False,
        "old_E02_source_or_wrapper_costs_transferred": False,
        "AS241_KS_E_or_previous_quantile_ULP_added": False,
        "coherent_financial_source_or_estimator_adopted": False,
        "actual_new_source_or_wrapper_quantum_cost": None,
        "physical_runtime_or_error": None,
        "quantum_advantage_established": False,
        "proof": PROOF,
    }
