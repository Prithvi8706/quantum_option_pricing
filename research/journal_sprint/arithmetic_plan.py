"""Non-enumerative raw Asian-call arithmetic design; no loading certificate."""

from decimal import ROUND_FLOOR
from .decimal_enclosure import Interval
from .fixed_exp_budget import exp_budget


def raw_plan(means, factor, *, cutoff=4, normal_bits=10, fraction_bits=40,
             width=64, degree=32, spot=100, strike=100, discount="1"):
    for value in (normal_bits, fraction_bits, width, degree):
        if type(value) is not bool and type(value) is int and value > 0:
            continue
        raise ValueError("positive integer precision required")
    if normal_bits > 32 or fraction_bits >= width or width > 256 or degree > 128:
        raise ValueError("unsupported precision")
    d = len(means)
    if not 1 <= d <= 32 or len(factor) != d or any(len(row) != d for row in factor):
        raise ValueError("square nonempty Gaussian factor required")
    if type(spot) is not int or type(strike) is not int or spot <= 0 or strike <= 0:
        raise ValueError("positive integer spot/strike required")
    l, discount = Interval(cutoff), Interval.coerce(discount)
    if l.lo <= 0 or discount.lo <= 0:
        raise ValueError("positive cutoff/discount required")
    scale = 1 << fraction_bits
    rows, row_errors = [], []
    radius, largest_prefix = 0, 0
    upper_spot_sum = Interval(0)
    for mean, row in zip(means, factor):
        # Float endpoints mean exact binary archived coefficients, as in the
        # frozen enclosure producer. log(spot) is itself outward enclosed.
        relative = Interval(mean) - Interval(spot).ln()
        factors = [Interval(b) for b in row]
        radius = max(radius, (relative.absolute() + l*sum((b.absolute() for b in factors), Interval(0))).hi)
        upper_log = relative + l*sum((b.absolute() for b in factors), Interval(0))
        upper_spot_sum += spot*upper_log.exp()
        intercept = relative + (-l + l/(1 << normal_bits))*sum(factors, Interval(0))
        bit_values = [2*l*b*(1 << k)/(1 << normal_bits)
                      for b in factors for k in range(normal_bits)]
        values = [intercept] + bit_values
        encoded = [int((v*scale).lo.to_integral_value(rounding=ROUND_FLOOR)) for v in values]
        error = sum(((v-Interval(c)/scale).absolute() for v, c in zip(values, encoded)), Interval(0))
        row_errors.append(error.hi)
        rows.append((encoded[0], tuple(encoded[1:])))
        largest_prefix = max(largest_prefix, sum(abs(c) for c in encoded))
    budget = exp_budget(radius, max(row_errors), degree, fraction_bits, width, spot)
    error = Interval(budget["total_error_upper"])
    payoff_upper = upper_spot_sum + d*error - d*strike
    upper_integer = int((payoff_upper*scale).hi.to_integral_value(rounding=ROUND_FLOOR))
    # Strictly larger power of two, including an exact integer endpoint.
    selector_bits = max(1, max(0, upper_integer).bit_length())
    limit = (1 << (width-1))-1
    signed_safe = (budget["overflow_safe"] and largest_prefix <= limit
                   and (d*Interval(budget["intermediate_magnitude_upper"])*scale).hi <= limit
                   and d*strike*scale <= limit and selector_bits < width)
    return dict(schema="raw_arithmetic_plan_v1", affine_rows=rows,
                exp_budget=budget, normal_bits=normal_bits, normal_qubits=d*normal_bits,
                fraction_bits=fraction_bits, width=width, degree=degree,
                strike_sum=d*strike*scale, selector_bits=selector_bits,
                discount_lower=str(discount.lo), discount_upper=str(discount.hi),
                arithmetic_price_error_upper=str((discount*error).hi),
                sensitivity_upper=str((discount*(1 << selector_bits)/scale/d).hi),
                overflow_safe=signed_safe, payoff_upper_integer=upper_integer,
                log_quantization_error_upper=str(max(row_errors)),
                application_admitted=False,
                missing=["Gaussian state preparation", "full six-component composition",
                         "production circuit verification/resources", "statistical design and human review"])
