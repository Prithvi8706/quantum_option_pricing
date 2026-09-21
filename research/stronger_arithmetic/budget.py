"""Directed certificates for the range-reduced, raw Asian-call integer map.

Fixed products use signed double-width scratch, as in fixed_multiply; their
floor-rescaled results and all stored constants use signed ``width`` words.
No loading, circuit/resource, statistical, or physical admission is implied.
"""

from decimal import ROUND_FLOOR
from math import factorial

from research.journal_sprint.decimal_enclosure import Interval as I  # noqa: N817


def _integer(value, minimum, name):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _parameters(degree, fraction_bits, width, reductions, spot):
    for name, value in (
        ("degree", degree),
        ("fraction_bits", fraction_bits),
        ("width", width),
        ("spot", spot),
    ):
        _integer(value, 1, name)
    _integer(reductions, 0, "reductions")
    if fraction_bits >= width or width > 256 or degree > 128 or reductions > 256:
        raise ValueError("unsupported precision")


def _floor(value):
    return int(value.to_integral_value(rounding=ROUND_FLOOR))


def _product(a, b):
    values = [x * y for x in a for y in b]
    return min(values), max(values)


def evaluate_reduced_integer(x, coefficients, fraction_bits, reductions, spot=100):
    """Unbounded integer map: signed floor shift, Horner, floor squares, spot."""
    _integer(fraction_bits, 1, "fraction_bits")
    _integer(reductions, 0, "reductions")
    _integer(spot, 1, "spot")
    if type(x) is not int or not coefficients or any(type(c) is not int for c in coefficients):
        raise ValueError("integer input and nonempty integer coefficients required")
    scale = 1 << fraction_bits
    reduced = x // (1 << reductions)
    y = coefficients[-1]
    for c in reversed(coefficients[:-1]):
        y = reduced * y // scale + c
    for _ in range(reductions):
        y = y * y // scale
    return spot * y


def reduced_exp_budget(radius, input_error, degree, fraction_bits, width, reductions, spot=100):
    """Certify |integer_map(X)/2**f - spot*exp(x)| on |x|<=radius,
    |X/2**f-x|<=input_error. Endpoints and all error arithmetic are directed.

    The signed shift error is at most (2**s-1)/(2**s*2**f), including
    negative X. Squaring compares to exp(X/2**f/2**s), then the separate
    Lipschitz input term compares exp(X/2**f) to exp(x).
    """
    _parameters(degree, fraction_bits, width, reductions, spot)
    h, dx = I.coerce(radius), I.coerce(input_error)
    if h.lo < 0 or dx.lo < 0:
        raise ValueError("nonnegative radius and input error required")
    scale, divisor = 1 << fraction_bits, 1 << reductions
    unit, domain = I(1) / scale, h + dx
    shift = I(divisor - 1) / (divisor * scale)
    reduced_domain = domain / divisor + shift
    coefficients = tuple(scale // factorial(k) for k in range(degree + 1))
    error = (I(1) / factorial(degree) - I(coefficients[-1]) / scale).absolute()
    for k in reversed(range(degree)):
        error = (
            reduced_domain * error
            + unit
            + (I(1) / factorial(k) - I(coefficients[k]) / scale).absolute()
        )
    horner_error = error
    remainder = reduced_domain.exp() * reduced_domain ** (degree + 1) / factorial(degree + 1)
    shift_error = reduced_domain.exp() * shift
    error += remainder + shift_error
    exact = (domain / divisor).exp()

    limit = (1 << (width - 1)) - 1
    wide_limit = (1 << (2 * width - 1)) - 1
    safe = True
    maximum = 0
    product_maximum = 0

    def word(bounds):
        nonlocal safe, maximum
        lo, hi = bounds
        maximum = max(maximum, abs(lo), abs(hi))
        safe = safe and -limit - 1 <= lo <= hi <= limit
        return bounds

    def product(bounds):
        nonlocal safe, product_maximum
        lo, hi = bounds
        product_maximum = max(product_maximum, abs(lo), abs(hi))
        safe = safe and -wide_limit - 1 <= lo <= hi <= wide_limit
        return bounds

    x_bound = _floor((domain * scale).hi)
    x_range = word((-x_bound, x_bound))
    reduced_range = word(tuple(x // divisor for x in x_range))
    for c in coefficients:
        word((c, c))
    y = (coefficients[-1], coefficients[-1])
    horner_ranges = []
    for c in reversed(coefficients[:-1]):
        raw = product(_product(reduced_range, y))
        multiplied = word(tuple(v // scale for v in raw))
        y = word(tuple(v + c for v in multiplied))
        horner_ranges.append(
            dict(
                product_integer_bounds=raw,
                multiplied_integer_bounds=multiplied,
                output_integer_bounds=y,
            )
        )
    stages = []
    for j in range(reductions):
        lo, hi = y
        squared = product((0 if lo <= 0 <= hi else min(lo * lo, hi * hi), max(lo * lo, hi * hi)))
        y = word(tuple(v // scale for v in squared))
        error = 2 * exact * error + error**2 + unit
        exact = exact**2
        stages.append(
            dict(
                stage=j + 1,
                exact_magnitude_upper=str(exact.hi),
                error_upper=str(error.hi),
                product_integer_bounds=squared,
                output_integer_bounds=y,
                approximate_magnitude_upper=str((I(max(abs(v) for v in y)) / scale).hi),
            )
        )
    # Spot is an exact integer multiply, without a rescaling/rounding step.
    # A shift/add implementation adds only the set-bit terms 2**k*y. Since
    # spot > 0, each term and every prefix (in any order) is m*y for an
    # integer 0 <= m <= spot. Thus all shifted words and accumulator prefixes
    # lie between zero and the final product, even when y is negative.
    word((spot, spot))
    final_product = product(tuple(spot * v for v in y))
    output = word(final_product)
    spot_prefix = word((min(0, output[0]), max(0, output[1])))
    input_term = spot * domain.exp() * dx
    total = spot * error + input_term
    return dict(
        coefficients=coefficients,
        reductions=reductions,
        spot=spot,
        domain_upper=str(domain.hi),
        reduced_domain_upper=str(reduced_domain.hi),
        shift_error_upper=str(shift_error.hi),
        shift_rounding_upper=str(shift.hi),
        horner_error_upper=str(horner_error.hi),
        remainder_upper=str(remainder.hi),
        input_error_upper=str(input_term.hi),
        total_error_upper=str(total.hi),
        spot_rounding_error_upper="0",
        squaring_stages=stages,
        horner_stages=horner_ranges,
        output_integer_bounds=output,
        output_nonnegative=output[0] >= 0,
        spot_prefix_integer_bounds=spot_prefix,
        intermediate_magnitude_upper=str((I(maximum) / scale).hi),
        intermediate_integer_magnitude_upper=maximum,
        product_integer_magnitude_upper=product_maximum,
        product_width=2 * width,
        overflow_safe=safe,
        scope="scalar range-reduced exponential only; not application admission",
    )


def reduced_plan(
    means,
    factor,
    *,
    cutoff=4,
    normal_bits=10,
    fraction_bits=40,
    width=64,
    degree=32,
    spot=100,
    strike=100,
    discount="1",
    reductions=1,
):
    """Raw positive-payoff plan with directed affine, exp and decoder metadata.

    Polynomial prices may be signed; only the final positive part is assumed
    nonnegative. Sum/prefix and poststrike certificates cover both signs.
    """
    _parameters(degree, fraction_bits, width, reductions, spot)
    _integer(normal_bits, 1, "normal_bits")
    _integer(strike, 1, "strike")
    d = len(means)
    if normal_bits > 32 or not 1 <= d <= 32 or len(factor) != d or any(len(r) != d for r in factor):
        raise ValueError("unsupported normal precision or nonsquare Gaussian factor")
    cutoff, discount = I.coerce(cutoff), I.coerce(discount)
    if cutoff.lo <= 0 or discount.lo <= 0:
        raise ValueError("positive cutoff/discount required")
    scale = 1 << fraction_bits
    rows, errors = [], []
    radius, largest_prefix = 0, 0
    upper_spot_sum = I(0)
    for mean, row in zip(means, factor):
        relative = I(mean) - I(spot).ln()
        factors = [I(b) for b in row]
        spread = cutoff * sum((b.absolute() for b in factors), I(0))
        radius = max(radius, (relative.absolute() + spread).hi)
        upper_spot_sum += spot * (relative + spread).exp()
        intercept = relative + (-cutoff + cutoff / (1 << normal_bits)) * sum(factors, I(0))
        values = [intercept] + [
            2 * cutoff * b * (1 << k) / (1 << normal_bits)
            for b in factors
            for k in range(normal_bits)
        ]
        encoded = [_floor((v * scale).lo) for v in values]
        errors.append(
            sum(((v - I(c) / scale).absolute() for v, c in zip(values, encoded)), I(0)).hi
        )
        rows.append((encoded[0], tuple(encoded[1:])))
        largest_prefix = max(largest_prefix, sum(abs(c) for c in encoded))
    budget = reduced_exp_budget(radius, max(errors), degree, fraction_bits, width, reductions, spot)
    error = I(budget["total_error_upper"])
    lo, hi = budget["output_integer_bounds"]
    sum_bounds = (d * lo, d * hi)
    strike_sum = d * strike * scale
    poststrike = (sum_bounds[0] - strike_sum, sum_bounds[1] - strike_sum)
    # Both the direct integer range and true-price-plus-error are universal.
    upper_integer = max(
        0, min(poststrike[1], _floor(((upper_spot_sum + d * error) * scale).hi) - strike_sum)
    )
    selector_bits = max(1, upper_integer.bit_length())
    limit = (1 << (width - 1)) - 1
    safe = (
        budget["overflow_safe"]
        and largest_prefix <= limit
        and strike_sum <= limit
        and -limit - 1 <= min(0, sum_bounds[0])
        and max(0, sum_bounds[1]) <= limit
        and -limit - 1 <= poststrike[0] <= poststrike[1] <= limit
        and selector_bits < width
    )
    return dict(
        schema="reduced_raw_arithmetic_plan_v1",
        affine_rows=rows,
        exp_budget=budget,
        reductions=reductions,
        spot=spot,
        normal_bits=normal_bits,
        normal_qubits=d * normal_bits,
        fraction_bits=fraction_bits,
        width=width,
        degree=degree,
        strike_sum=strike_sum,
        selector_bits=selector_bits,
        discount_lower=str(discount.lo),
        discount_upper=str(discount.hi),
        arithmetic_price_error_upper=str((discount * error).hi),
        sensitivity_upper=str((discount * (1 << selector_bits) / scale / d).hi),
        overflow_safe=safe,
        payoff_upper_integer=upper_integer,
        sum_integer_bounds=sum_bounds,
        poststrike_integer_bounds=poststrike,
        affine_prefix_magnitude_upper=largest_prefix,
        log_quantization_error_upper=str(max(errors)),
        application_admitted=False,
        missing=[
            "Gaussian state preparation",
            "full six-component composition",
            "production circuit verification/resources",
            "statistical design and human review",
        ],
    )
