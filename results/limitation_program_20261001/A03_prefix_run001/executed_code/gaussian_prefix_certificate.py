"""Three certified q10 conditional nodes; the rest of the loader stays open.

The archived target is the standard normal binned on [-6,6], conditional
on that interval. It is a different law from the accepted paired Box-Muller.
All serialization endpoints are exact rationals, rounded outwards by mpmath.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import factorial
import re

import mpmath as mp

from research.limitation_program_20261001.financial_bounded_schedule import pi_interval

DPS = 140
PI_TERMS = 240
TAYLOR_DEGREE = 256
BISECTION_STEPS = 160
MIDPOINT_BITS = 128
BITS = 10
ROTATIONS = (1 << BITS) - 1
MAX_FACTORS = 468
LOADING_DOLLARS = Fraction(1, 1000)
PAYOFF_SPAN = Fraction(40)
ROTATION_EPSILON = LOADING_DOLLARS / (PAYOFF_SPAN * MAX_FACTORS * ROTATIONS)


def exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ValueError("Exact integer or Fraction required")
    return Fraction(value)


def pair(value):
    value = exact(value)
    return [value.numerator, value.denominator]


def endpoint(value):
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def bounds(value):
    return tuple(endpoint(item) for item in value._mpi_)


def interval(value):
    mp.iv.dps = DPS
    if isinstance(value, (tuple, list)):
        if len(value) != 2:
            raise ValueError("Two rational endpoints required")
        lo, hi = map(exact, value)
        if lo > hi:
            raise ValueError("Ordered interval required")
        lower = mp.iv.mpf(lo.numerator) / lo.denominator
        upper = mp.iv.mpf(hi.numerator) / hi.denominator
        return mp.iv.mpf([lower.a, upper.b])
    value = exact(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def serialized(value):
    lo, hi = value
    return dict(lower_exact=pair(lo), upper_exact=pair(hi))


@lru_cache(maxsize=1)
def pi_bounds():
    return pi_interval(PI_TERMS)


def gaussian_cdf(x, degree=TAYLOR_DEGREE):
    """Integrated exp Taylor polynomial with its derivative remainder.

    For s>=0, the degree-n remainder of exp(-s) has magnitude at most
    s**(n+1)/(n+1)! since every derivative has magnitude <=1 there.
    Integrating with s=t*t/2 supplies the displayed exact remainder.
    """
    x = exact(x)
    if abs(x) > 6 or type(degree) is not int or degree < 1:
        raise ValueError("Fixed bounded Gaussian domain required")
    if x < 0:
        lo, hi = gaussian_cdf(-x, degree)
        return 1 - hi, 1 - lo
    if x == 0:
        return Fraction(1, 2), Fraction(1, 2)
    integral = sum(
        (
            Fraction((-1) ** k, 2**k * factorial(k) * (2 * k + 1)) * x ** (2 * k + 1)
            for k in range(degree + 1)
        ),
        Fraction(0),
    )
    remainder = x ** (2 * degree + 3) / (
        2 ** (degree + 1) * factorial(degree + 1) * (2 * degree + 3)
    )
    enclosed = interval(Fraction(1, 2)) + interval(
        (integral - remainder, integral + remainder)
    ) / mp.iv.sqrt(2 * interval(pi_bounds()))
    lo, hi = bounds(enclosed)
    return max(Fraction(0), lo), min(Fraction(1), hi)


def quotient(numerator, denominator):
    if denominator[0] <= 0:
        raise ValueError("Positive mass denominator required")
    return bounds(interval(numerator) / interval(denominator))


def angle_over_pi(right_probability, steps=BISECTION_STEPS):
    """Invert sin(theta/2)^2 monotonically, theta/pi in [0,1]."""
    p_lo, p_hi = map(exact, right_probability)
    if not 0 < p_lo <= p_hi < 1 or type(steps) is not int or steps < 1:
        raise ValueError("Interior ordered probability enclosure required")
    lo, hi = Fraction(0), Fraction(1)
    for _ in range(steps):
        center = (lo + hi) / 2
        image = bounds(mp.iv.sin(interval(center / 2) * interval(pi_bounds())) ** 2)
        if image[1] < p_lo:
            lo = center
        elif image[0] > p_hi:
            hi = center
        else:
            # Retaining the existing bracket is sound if intervals cannot
            # resolve this split. It never licenses a precision retry.
            break
    return lo, hi


def rounded_midpoint(enclosure, bits=MIDPOINT_BITS):
    lo, hi = map(exact, enclosure)
    if lo > hi or type(bits) is not int or bits < 1:
        raise ValueError("Ordered enclosure and positive integer precision required")
    center, scale = (lo + hi) / 2, 1 << bits
    numerator = (center * scale + Fraction(1, 2)).numerator
    denominator = (center * scale + Fraction(1, 2)).denominator
    target = Fraction(numerator // denominator, scale)
    error = max(abs(target - lo), abs(target - hi)) / 2
    return target, error


def certificate():
    cdf = {x: gaussian_cdf(x) for x in (-6, -3, 0, 3, 6)}
    pi_lo, pi_hi = pi_bounds()
    normalization = bounds(2 * interval(cdf[6]) - 1)
    half_mass = bounds(interval(cdf[6]) - interval(Fraction(1, 2)))
    outer = bounds(interval(cdf[6]) - interval(cdf[3]))
    inner = bounds(interval(cdf[3]) - interval(Fraction(1, 2)))
    p_outer, p_inner = quotient(outer, half_mass), quotient(inner, half_mass)
    ratio = angle_over_pi(p_inner)
    theta_left = ratio[0] * pi_lo, ratio[1] * pi_hi
    theta_right = (1 - ratio[1]) * pi_lo, (1 - ratio[0]) * pi_hi
    beta = (ratio[0] - Fraction(1, 2)) * pi_lo, (ratio[1] - Fraction(1, 2)) * pi_hi
    target, point_error = rounded_midpoint(beta)
    if point_error > ROTATION_EPSILON / 4:
        raise ArithmeticError("Fixed angle precision did not meet the declared allowance")
    return dict(
        cdf_boundaries={str(x): serialized(value) for x, value in cdf.items()},
        normalization=serialized(normalization),
        unnormalized_half_mass=serialized(half_mass),
        unnormalized_outer_quarter_mass=serialized(outer),
        unnormalized_inner_quarter_mass=serialized(inner),
        normalized_four_prefix_blocks=[
            dict(
                boundaries_exact=[[left, 1], [right, 1]],
                probability=serialized(quotient(mass, normalization)),
            )
            for left, right, mass in ((-6, -3, outer), (-3, 0, inner), (0, 3, inner), (3, 6, outer))
        ],
        nodes=[
            dict(
                prefix="",
                left_probability=serialized((Fraction(1, 2),) * 2),
                theta_exact_pi_multiple=[1, 2],
            ),
            dict(
                prefix="0",
                left_probability=serialized(p_outer),
                theta_radians=serialized(theta_left),
            ),
            dict(
                prefix="1",
                left_probability=serialized(p_inner),
                theta_radians=serialized(theta_right),
            ),
        ],
        theta_left_over_pi=serialized(ratio),
        walsh_rotations=[
            dict(level=0, target=9, exact_pi_multiple=[1, 2]),
            dict(level=1, target=8, exact_pi_multiple=[1, 2]),
            dict(
                level=1,
                target=8,
                angle_radians=serialized(beta),
                synthesis_target_radians_exact=pair(target),
                target_midpoint_operator_error_upper_exact=pair(point_error),
            ),
        ],
        root_symmetry_exact=True,
        child_angles_sum_exact="pi",
        walsh_mean_exact="pi/2",
        conditional_nodes_certified=3,
        numerical_method=dict(
            decimal_interval_precision=DPS,
            pi_arctan_terms=PI_TERMS,
            integrated_exp_Taylor_degree=TAYLOR_DEGREE,
            angle_bisection_steps=BISECTION_STEPS,
            synthesis_midpoint_bits=MIDPOINT_BITS,
        ),
    )


def archive_counts(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines[:3] != ["OPENQASM 3.0;", 'include "stdgates.inc";', "qubit[10] q;"]:
        raise ValueError("Original q10 Gaussian QASM header required")
    operations = lines[3:]
    for line in operations:
        if not re.fullmatch(r"(?:ry\([^;]+\) q\[\d+\]|cx q\[\d+\], q\[\d+\]);", line):
            raise ValueError("Unexpected archived preparation operation")
        if any(int(wire) >= BITS for wire in re.findall(r"q\[(\d+)\]", line)):
            raise ValueError("Archived preparation operation escapes its scalar lane")
    prefix = [
        "ry(pi/2) q[9];",
        "ry(pi/2) q[8];",
        "cx q[9], q[8];",
        "ry(1.466830424129055) q[8];",
        "cx q[9], q[8];",
    ]
    if operations[:5] != prefix:
        raise ValueError("Archived first-two-level convention changed")
    counts = dict(
        ry=sum(line.startswith("ry(") for line in operations),
        cx=sum(line.startswith("cx ") for line in operations),
    )
    return dict(
        archived_operation_counts=counts,
        full_tree_conditional_nodes=ROTATIONS,
        potential_Walsh_Ry_rotations=ROTATIONS,
        theoretical_multiplexor_CX_count=sum(1 << level for level in range(1, BITS)),
        first_two_levels_conditional_nodes=3,
        first_two_levels_emitted_Walsh_Ry_rotations=3,
        first_two_levels_CX_count=2,
        remaining_conditional_nodes_without_angle_certificates=ROTATIONS - 3,
        potential_minus_archived_Ry_count=ROTATIONS - counts["ry"],
        omitted_float_Walsh_values_proved_zero=False,
        full_tree_synthesis_T_count=None,
        full_preparation_trace_error=None,
    )


def budget_rows(a05_rows):
    rows = []
    for case, factors in (("B4x12", 60), ("B8x52", 468)):
        source = next(row for row in a05_rows if row["case"] == case)
        scalar = LOADING_DOLLARS / (PAYOFF_SPAN * factors)
        if source["conservative_scalar_trace_allowance_exact"] != pair(scalar):
            raise ValueError("A05 scalar allowance binding disagrees")
        joint = factors * ROTATIONS * ROTATION_EPSILON
        if PAYOFF_SPAN * joint > LOADING_DOLLARS:
            raise ArithmeticError("Full-tree conservative error allocation exceeds budget")
        rows.append(
            dict(
                case=case,
                hypothetical_disjoint_scalar_factors=factors,
                reserved_loading_dollars_exact=pair(LOADING_DOLLARS),
                scalar_trace_allowance_exact=pair(scalar),
                per_potential_rotation_operator_allowance_exact=pair(ROTATION_EPSILON),
                worst_case_full_tree_operator_allowance_exact=pair(ROTATIONS * ROTATION_EPSILON),
                conditional_joint_preparation_trace_allowance_exact=pair(joint),
                conditional_bounded_observable_dollars_exact=pair(PAYOFF_SPAN * joint),
                full_tree_rotations_all_within_allowance=None,
                pure_product_refinement_used=False,
                current_Box_Muller_coordinates_assumed_independent=False,
                q10_law_equals_accepted_Box_Muller_law=False,
                loading_budget_adopted_in_financial_ledger=False,
            )
        )
    return rows


def multiply(left, right):
    n = len(left)
    return [
        [sum((left[i][k] * right[k][j] for k in range(n)), mp.iv.mpc(0)) for j in range(n)]
        for i in range(n)
    ]


def gate_table():
    mp.iv.dps = DPS
    one, zero = mp.iv.mpc(1), mp.iv.mpc(0)
    root = mp.iv.sqrt(2)
    omega = mp.iv.mpc(1 / root, 1 / root)
    return {
        "H": [[one / root, one / root], [one / root, -one / root]],
        "Z": [[one, zero], [zero, -one]],
        "T": [[one, zero], [zero, omega]],
        "S": [[one, zero], [zero, mp.iv.mpc(0, 1)]],
        "D": [[one, zero], [zero, mp.iv.mpc(0, -1)]],
        "X": [[zero, one], [one, zero]],
        "W": [[omega, zero], [zero, omega]],
    }


def matrix_product(gates):
    if set(gates) - set("HTSXW"):
        raise ValueError("Unsupported synthesis token")
    one, zero = mp.iv.mpc(1), mp.iv.mpc(0)
    result = [[one, zero], [zero, one]]
    table = gate_table()
    for token in gates:
        result = multiply(result, table[token])
    return result


def squared_frobenius(left, right):
    squared = mp.iv.mpf(0)
    for i in range(len(left)):
        for j in range(len(left)):
            delta = left[i][j] - right[i][j]
            squared += delta.real**2 + delta.imag**2
    return bounds(squared)[1]


def ry(angle):
    cosine, sine = mp.iv.cos(angle / 2), mp.iv.sin(angle / 2)
    return [[mp.iv.mpc(cosine), mp.iv.mpc(-sine)], [mp.iv.mpc(sine), mp.iv.mpc(cosine)]]


def rz(angle):
    zero = mp.iv.mpc(0)
    return [[mp.iv.exp(mp.iv.mpc(0, -angle / 2)), zero], [zero, mp.iv.exp(mp.iv.mpc(0, angle / 2))]]


def tensor(left, right):
    return [[left[i // 2][j // 2] * right[i % 2][j % 2] for j in range(4)] for i in range(4)]


def prefix_unitary_error(beta_enclosure, gates):
    """Check the complete four-dimensional multiplexor, including phase W."""
    table = gate_table()
    one, zero = mp.iv.mpc(1), mp.iv.mpc(0)
    identity = [[one, zero], [zero, one]]
    half_pi = interval(pi_bounds()) / 2
    root = multiply(table["H"], table["Z"])
    synthesized_ry = multiply(
        multiply(multiply(multiply(table["S"], table["H"]), matrix_product(gates)), table["H"]),
        table["D"],
    )
    cx = [[mp.iv.mpc(int(j == (i if i < 2 else i ^ 1))) for j in range(4)] for i in range(4)]
    actual = tensor(root, root)
    actual = multiply(cx, actual)
    actual = multiply(tensor(identity, synthesized_ry), actual)
    actual = multiply(cx, actual)
    theta0, theta1 = half_pi + interval(beta_enclosure), half_pi - interval(beta_enclosure)
    left, right = ry(theta0), ry(theta1)
    ideal_controlled = [[zero for _ in range(4)] for _ in range(4)]
    for block, value in enumerate((left, right)):
        for i in range(2):
            for j in range(2):
                ideal_controlled[2 * block + i][2 * block + j] = value[i][j]
    ideal = multiply(ideal_controlled, tensor(ry(half_pi), identity))
    return squared_frobenius(actual, ideal)


def verify_string(beta_enclosure, target, gates):
    point_squared = squared_frobenius(matrix_product(gates), rz(interval(target)))
    whole_squared = squared_frobenius(matrix_product(gates), rz(interval(beta_enclosure)))
    complete_squared = prefix_unitary_error(beta_enclosure, gates)
    if point_squared > (ROTATION_EPSILON / 2) ** 2:
        raise ArithmeticError("Generated string failed exact point certification")
    if whole_squared > ROTATION_EPSILON**2:
        raise ArithmeticError("Generated string failed whole-angle enclosure certification")
    if complete_squared > 2 * ROTATION_EPSILON**2:
        raise ArithmeticError("Generated prefix failed complete unitary certification")
    return dict(
        point_Frobenius_error_squared_upper_exact=pair(point_squared),
        whole_angle_Frobenius_error_squared_upper_exact=pair(whole_squared),
        complete_prefix_Frobenius_error_squared_upper_exact=pair(complete_squared),
        scalar_W_phase_included_in_interval_verification=True,
        physically_omit_W_and_track_its_global_phase=True,
        physical_operator_error_is_phase_aligned=True,
        controlled_use_requires_tracked_global_phase_compensation=True,
        controlled_prefix_implementation=None,
        per_rotation_operator_error_upper_exact=pair(ROTATION_EPSILON),
        complete_prefix_operator_error_upper_exact=pair(ROTATION_EPSILON),
        complete_unitary_bound_reason=(
            "One embedded non-Clifford Ry substitution; tensor identity and Clifford "
            "conjugation preserve its operator error. All other prefix gates are exact."
        ),
    )
