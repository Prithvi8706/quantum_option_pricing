"""Reject an insufficient uniform-error budget without claiming financial bias.

This evaluates an optimistic cost of the already chosen certificate method.
An enclosure of a probability UPPER-BOUND FORMULA is not a lower bound on the
actual barrier-switch probability. Nothing here certifies the full native path.
"""

from fractions import Fraction

from research.limitation_program_20261001.barrier_band_certificate import (
    bounds_for_log_length,
    exact,
    pair,
)


def optimistic_terms(beta, common, idiosyncratic, cutoff, dates=12, pairs=30, cap=40):
    values = tuple(map(exact, (beta, common, idiosyncratic, cutoff, cap)))
    beta, common, idiosyncratic, cutoff, cap = values
    if beta <= 0 or common <= 0 or idiosyncratic <= 0 or not 0 < cutoff < 1 or cap <= 0:
        raise ValueError("Positive original coupling terms required")
    if (dates, pairs) != (12, 30):
        raise ValueError("This fixed screen covers only original B4x12 and30 pairs")
    per_increment = (common + idiosyncratic) * beta
    rows = []
    sums = {name: [Fraction(0), Fraction(0)] for name in ("density", "centered_interval_maximum")}
    for date in range(1, dates + 1):
        log_error = date * per_increment
        bounds = bounds_for_log_length((2 * log_error, 2 * log_error), Fraction(3 * date, 1000))
        for name, total in sums.items():
            interval = list(map(exact, bounds[name]["interval_exact"]))
            total[0] += interval[0]
            total[1] += interval[1]
        rows.append(
            dict(
                date=date,
                optimistic_log_discrepancy_exact=pair(log_error),
                common_log_variance_exact=[3 * date, 1000],
                formula_enclosures=bounds,
            )
        )
    tail = cap * min(Fraction(1), pairs * cutoff)
    totals = {}
    allowance = Fraction(11, 2000)
    for name, total in sums.items():
        union = [min(Fraction(1), value) for value in total]
        dollars = [cap * value + tail for value in union]
        totals[name] = dict(
            union_formula_interval_exact=list(map(pair, union)),
            barrier_and_tail_formula_dollars_interval_exact=list(map(pair, dollars)),
            formula_floor_exceeds_remaining_headroom=dollars[0] > allowance,
            actual_probability_lower_bound_claimed=False,
            actual_price_bias_lower_bound_claimed=False,
        )
    return dict(
        dates=rows,
        tail_formula_dollars_exact=pair(tail),
        remaining_headroom_exact=pair(allowance),
        methods=totals,
        omitted_nonnegative_costs=[
            "coefficient and drift/log-spot rounding",
            "native increment multiplication floors",
            "native exponential approximation and reconstruction",
            "clipping and full-path arithmetic effects",
            "surviving Asian-payoff discrepancy",
        ],
        omitted_terms_credited_as_certified_zero=False,
        full_path_stock_or_basket_discrepancy_certified=False,
        complete_continuous_price_certificate=False,
        interpretation=(
            "Even if the unproved full native multiplicative path bound attained "
            "this optimistic value, these two fixed uniform-error union formulas "
            "could not fit the remaining headroom. This rejects a certificate "
            "method at its two declared cutoffs; actual financial bias may be smaller."
        ),
    )
