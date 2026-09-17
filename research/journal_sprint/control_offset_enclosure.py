"""Directed degree-four control expectation for an ideal finite midpoint model.

The basket is A = sum_i exp(means[i] + factor[i] @ Z) / d. Independent
coordinates Z have exact normal cell masses on [-4, 4], normalized by the
exact truncated mass, and exact uniform midpoints. Archived numeric inputs
are interpreted as binary floats, not decimal spellings. This does not certify
state preparation, arithmetic, phase synthesis, or the continuous model.
"""

from decimal import Decimal
from math import comb, factorial, prod

from .decimal_enclosure import Interval as I, normal_cdf  # noqa: N817
from .polynomial_residual import compositions


def _archived(value):
    if isinstance(value, bool) or type(value).__name__ == "bool_":
        raise ValueError("boolean is not an archived numeric parameter")
    return I(float(value))


def _probability(value):
    # Intersect with a known mathematical range; never renormalize by the
    # rounded sum of the individual cell enclosures.
    return I(max(Decimal(0), value.lo), min(Decimal(1), value.hi))


def _poly_add(left, right):
    return [
        (left[k] if k < len(left) else I(0))
        + (right[k] if k < len(right) else I(0))
        for k in range(max(len(left), len(right)))
    ]


def _poly_mul(left, right):
    result = [I(0) for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def moment_enclosure(means, factor, q, L=4, degree=4):
    """Return reusable outward moments E[A**k], k=0,...,4, once per q.

    Supports signed archived means/factor, 1<=d<=4, integer 1<=q<=10,
    L=4, degree=4. Returns ``moments`` (five Intervals), ``terms``, ``scope``,
    and ``work``. Archive every moment using ``moment.record()``.

    There are C(d+4,4)<=70 multinomial terms. At most d*(terms-1)
    nonzero marginal loadings require 2**q cell visits and TWO exponentials
    each. Mean terms require at most terms-1 further exponentials. Thus at
    d=4,q=10 there are <=282624 cell visits and <=621 exp calls, plus
    1025 CDF boundary enclosures. No product grid is enumerated.
    """
    if type(q) is not int or not 1 <= q <= 10:
        raise ValueError("q must be an integer in [1,10]")
    if isinstance(L, bool) or L != 4:
        raise ValueError("only cutoff L=4 is supported")
    if type(degree) is not int or degree != 4:
        raise ValueError("only degree=4 is supported")
    d = len(means)
    if not 1 <= d <= 4 or len(factor) != d or any(len(row) != d for row in factor):
        raise ValueError("means and square factor must have dimension 1 through 4")
    means = [_archived(v) for v in means]
    factor = [[_archived(v) for v in row] for row in factor]
    # Check the supported exp domain before doing CDF/grid work. Every alpha
    # has sum<=4; both the mean and each loaded midpoint then lie in [-1000,1000].
    if any(v.absolute().hi > 250 for v in means) or any(
        v.absolute().hi > Decimal("62.5") for row in factor for v in row
    ):
        raise ValueError("means/factor outside bounded exponential domain")

    cells = 2**q
    step = I(8) / cells
    first = I(-4) + step / 2
    cdfs = [normal_cdf(I(-4) + j * step) for j in range(cells + 1)]
    mass = _probability(cdfs[-1] - cdfs[0])
    weights = [_probability((b - a) / mass) for a, b in zip(cdfs, cdfs[1:])]
    marginal_cache = {}
    exp_calls = 0
    cell_visits = 0

    def marginal(loading):
        nonlocal exp_calls, cell_visits
        # Floating loading keys could identify distinct exact alpha @ factor
        # values. Endpoint pairs preserve the actual directed combination.
        key = (loading.lo, loading.hi)
        if key not in marginal_cache:
            if loading.lo == loading.hi == 0:
                marginal_cache[key] = I(1)
            else:
                node_exp = (loading * first).exp()
                ratio = (loading * step).exp()
                exp_calls += 2
                total = I(0)
                for j, weight in enumerate(weights):
                    total += weight * node_exp
                    if j + 1 < cells:
                        node_exp *= ratio
                cell_visits += cells
                marginal_cache[key] = total
        return marginal_cache[key]

    moments = [I(1)]
    terms = 1
    for power in range(1, 5):
        moment = I(0)
        for alpha in compositions(power, d):
            coefficient = factorial(power) // prod(factorial(a) for a in alpha)
            mean = sum((a * m for a, m in zip(alpha, means)), I(0))
            term = mean.exp() * coefficient / d**power
            exp_calls += 1
            for j in range(d):
                loading = sum((alpha[i] * factor[i][j] for i in range(d)), I(0))
                term *= marginal(loading)
            moment += term
            terms += 1
        moments.append(moment)

    term_bound = comb(d + 4, 4)
    return dict(
        moments=tuple(moments),
        terms=terms,
        scope="ideal_finite_midpoint_model",
        work=dict(
            cells=cells,
            cdf_boundaries=cells + 1,
            marginal_loadings=len(marginal_cache),
            cell_visits=cell_visits,
            cell_visits_bound=d * (term_bound - 1) * cells,
            exp_calls=exp_calls,
            exp_calls_bound=(2 * d + 1) * (term_bound - 1),
        ),
    )


def control_enclosure(moments, strike, B, discount, lowcoeff):
    """Evaluate the degree-four control using five precomputed Interval moments.

    Returns ``value`` (Interval) and ``scope``. All scalar inputs and the five
    Chebyshev coefficients are archived binary floats. Strike/discount must
    be nonnegative and B positive. No CDFs or exponentials are evaluated.
    The caller is responsible for supplying moments of the matching model.
    For a runner-selected float offset, bound its error with
    ``(Interval(float_offset) - result['value']).absolute().hi``.
    """
    if len(moments) != 5 or any(not isinstance(m, I) or m.lo < 0 for m in moments):
        raise ValueError("five nonnegative finite Interval moments required")
    if moments[0] != I(1):
        raise ValueError("zeroth moment must be exactly one")
    if len(lowcoeff) != 5:
        raise ValueError("five degree-four Chebyshev coefficients required")
    low = [_archived(v) for v in lowcoeff]
    strike, radius, discount = map(_archived, (strike, B, discount))
    if strike.lo < 0 or discount.lo < 0 or radius.lo <= 0:
        raise ValueError("nonnegative strike/discount and positive radius required")
    x = [-strike / radius, I(1) / radius]
    previous, current = [I(1)], x
    polynomial = _poly_add([low[0]], [low[1] * v for v in current])
    for k in range(2, 5):
        following = _poly_add(
            [2 * v for v in _poly_mul(x, current)], [-v for v in previous]
        )
        polynomial = _poly_add(polynomial, [low[k] * v for v in following])
        previous, current = current, following
    polynomial = _poly_add(polynomial, x)
    value = discount * radius / 2 * sum(
        (coefficient * moment for coefficient, moment in zip(polynomial, moments)), I(0)
    )
    return dict(value=value, scope="ideal_finite_midpoint_model")


def control_offset_enclosure(
    means, factor, q, strike, radius, discount, low_coefficients,
    actual_float_offset=None, *, cutoff=4,
):
    """Convenience composition; use the split API to reuse moments across B.

    The optional actual archived float offset is compared to the ideal
    expectation, including any old floating monomial conversion discrepancy.
    """
    offset = None if actual_float_offset is None else _archived(actual_float_offset)
    result = moment_enclosure(means, factor, q, cutoff)
    result.update(control_enclosure(result["moments"], strike, radius, discount, low_coefficients))
    result["actual_float_offset_error_upper"] = (
        None if offset is None else (offset - result["value"]).absolute().hi
    )
    return result
