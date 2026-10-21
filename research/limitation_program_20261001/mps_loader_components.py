"""Exact finite-literal MPS preparation ledger, without synthesis or adoption.

Every floating result is a proposal whose exact binary64 literals are charged.
CDF enclosures concern the distinct q10 conditional Gaussian law. Neither a
floating unitary predicate nor a discarded-SVD diagnostic supplies a proof.
All expensive functions are explicit calls; importing this module runs none.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import factorial, isfinite, isqrt

import mpmath as mp
import numpy as np

from research.limitation_program_20261001.financial_bounded_schedule import pi_interval
from research.limitation_program_20261001.mps_sequential_structure_v2 import (
    Primitive,
    validate_cores,
)

BITS = 10
SIZE = 1 << BITS
CUTOFF = Fraction(6)
DPS = 160
PI_TERMS = 240
CDF_DEGREE = 256
ROOT_BITS = 256
BONDS = (2, 4, 8)
TARGETS = tuple(Fraction(1, 18720000 * scale) for scale in (1, 10, 100))
SYNTHESIS_RESERVE = TARGETS[-1] / 4
MAX_ROTATIONS = 4096
EXPECTED_BONDS = {
    2: (2, 2, 2, 2, 2, 2, 2, 2, 2),
    4: (2, 4, 4, 4, 4, 4, 4, 4, 2),
    8: (2, 4, 8, 8, 8, 8, 8, 4, 2),
}


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ValueError("An exact integer or Fraction is required")
    return Fraction(value)


def pair(value):
    value = rational(value)
    return [value.numerator, value.denominator]


def endpoint(value):
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def bounds(value):
    return tuple(endpoint(item) for item in value._mpi_)


def iv(value):
    mp.iv.dps = DPS
    if isinstance(value, (tuple, list)):
        if len(value) != 2:
            raise ValueError("Two exact ordered interval endpoints are required")
        lo, hi = map(rational, value)
        if lo > hi:
            raise ValueError("Ordered interval endpoints are required")
        lower = mp.iv.mpf(lo.numerator) / lo.denominator
        upper = mp.iv.mpf(hi.numerator) / hi.denominator
        return mp.iv.mpf([lower.a, upper.b])
    value = rational(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def enclosed(value):
    lo, hi = value
    return {"lower_exact": pair(lo), "upper_exact": pair(hi)}


def sqrt_upper(value, bits=ROOT_BITS):
    value = rational(value)
    if value < 0 or type(bits) is not int or not 1 <= bits <= ROOT_BITS:
        raise ValueError("Nonnegative rational and bounded root precision are required")
    scale = 1 << bits
    n = isqrt((value.numerator * scale * scale) // value.denominator)
    if n * n * value.denominator < value.numerator * scale * scale:
        n += 1
    return Fraction(n, scale)


def literal(value):
    value = complex(value)
    if not (isfinite(value.real) and isfinite(value.imag)):
        raise ValueError("Finite binary64 real and imaginary literals are required")
    return Fraction.from_float(value.real), Fraction.from_float(value.imag)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def mul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def conjugate(a):
    return a[0], -a[1]


def squared(a):
    return a[0] ** 2 + a[1] ** 2


def dot(left, right):
    if len(left) != len(right):
        raise ValueError("Equal vector dimensions are required")
    value = (Fraction(0), Fraction(0))
    for a, b in zip(left, right):
        value = add(value, mul(conjugate(a), b))
    return value


def norm_squared(vector):
    return sum((squared(value) for value in vector), Fraction(0))


def literal_vector(values):
    return tuple(literal(value) for value in np.asarray(values).reshape(-1))


def save_literals(values):
    values = np.asarray(values)
    return {
        "shape": list(values.shape),
        "binary64_complex_rationals": [
            [pair(real), pair(imag)] for real, imag in literal_vector(values)
        ],
    }


def exact_contract(cores, checkpoint=lambda: None):
    """Contract saved rational literals in lexicographic, MSB-first site order."""
    cores = validate_cores(cores)
    active = [((Fraction(1), Fraction(0)),)]
    for core in cores:
        checkpoint()
        left, _, right = core.shape
        flat = literal_vector(core)
        following = []
        for previous in active:
            if len(previous) != left:
                raise ValueError("Consecutive exact bond dimensions are required")
            for bit in (0, 1):
                outputs = []
                for beta in range(right):
                    value = (Fraction(0), Fraction(0))
                    for alpha in range(left):
                        coefficient = flat[(alpha * 2 + bit) * right + beta]
                        value = add(value, mul(previous[alpha], coefficient))
                    outputs.append(value)
                following.append(tuple(outputs))
        active = following
    return tuple(value[0] for value in active)


def normalized_trace_distance(left, right):
    """Pure-state distance; all contractions and overlaps are exact rationals."""
    nl, nr = norm_squared(left), norm_squared(right)
    if nl <= 0 or nr <= 0:
        raise ValueError("Positive finite-literal vector norms are required")
    overlap = squared(dot(left, right))
    deficit = 1 - overlap / (nl * nr)
    if not 0 <= deficit <= 1:
        raise ValueError("Exact Cauchy-Schwarz identity was violated")
    return sqrt_upper(deficit), deficit


def gauge_distance(canonical, compressed):
    """Distance to the normalized original literal tensor, with its phase."""
    nc = norm_squared(compressed)
    if nc <= 0:
        raise ValueError("Positive compressed literal norm is required")
    value = (
        iv(norm_squared(canonical)) + 1 - 2 * iv(dot(canonical, compressed)[0]) / mp.iv.sqrt(iv(nc))
    )
    return sqrt_upper(max(Fraction(0), bounds(value)[1]))


@lru_cache(maxsize=1)
def pi_bounds():
    return pi_interval(PI_TERMS)


@lru_cache(maxsize=SIZE // 2 + 1)
def cdf_positive(x):
    x = rational(x)
    if not 0 <= x <= CUTOFF:
        raise ValueError("Fixed positive CDF domain0..6 is required")
    if x == 0:
        return (Fraction(1, 2),) * 2
    # Exact Horner evaluation of integral_0^x exp(-t^2/2) dt.
    polynomial = Fraction(0)
    for k in reversed(range(CDF_DEGREE + 1)):
        polynomial = polynomial * x * x + Fraction((-1) ** k, 2**k * factorial(k) * (2 * k + 1))
    integral = x * polynomial
    remainder = x ** (2 * CDF_DEGREE + 3) / (
        2 ** (CDF_DEGREE + 1) * factorial(CDF_DEGREE + 1) * (2 * CDF_DEGREE + 3)
    )
    value = iv(Fraction(1, 2)) + iv((integral - remainder, integral + remainder)) / mp.iv.sqrt(
        2 * iv(pi_bounds())
    )
    lo, hi = bounds(value)
    return max(Fraction(0), lo), min(Fraction(1), hi)


def cdf(x):
    x = rational(x)
    if x < 0:
        lo, hi = cdf_positive(-x)
        return 1 - hi, 1 - lo
    return cdf_positive(x)


def certify_rounded_target(probabilities, amplitudes):
    if len(probabilities) != len(amplitudes) or not probabilities:
        raise ValueError("Matching nonempty probability and amplitude vectors are required")
    literals = tuple((Fraction.from_float(float(a)), Fraction(0)) for a in amplitudes)
    if any(a[0] < 0 for a in literals):
        raise ValueError("Nonnegative binary64 target amplitudes are required")
    total_norm = norm_squared(literals)
    if total_norm <= 0:
        raise ValueError("Positive rounded target norm is required")
    if (
        not sum((p[0] for p in probabilities), Fraction(0))
        <= 1
        <= sum((p[1] for p in probabilities), Fraction(0))
    ):
        raise ValueError("The probability enclosures must contain a normalized law")
    lower_overlap = Fraction(0)
    for probability, (amplitude, _) in zip(probabilities, literals):
        lo, hi = map(rational, probability)
        if not 0 <= lo <= hi <= 1:
            raise ValueError("Normalized probability enclosures are required")
        lower_overlap += amplitude * bounds(mp.iv.sqrt(iv((lo, hi))))[0]
    # The exact ideal bin probabilities telescope to one; their interval
    # midpoints are not renormalized into a different target law.
    deficit = max(Fraction(0), 1 - lower_overlap**2 / total_norm)
    return {
        "rounded_target_norm_squared_exact": pair(total_norm),
        "ideal_CDF_to_normalized_literal_target_trace_upper_exact": pair(sqrt_upper(deficit)),
        "probability_normalization_is_the_exact_CDF_telescoping_identity": True,
    }


def build_target(checkpoint=lambda: None):
    positive = []
    for index in range(SIZE // 2 + 1):
        checkpoint()
        positive.append(cdf_positive(CUTOFF * index / (SIZE // 2)))
    edges = [(1 - hi, 1 - lo) for lo, hi in reversed(positive[1:])] + positive
    normalization = (2 * positive[-1][0] - 1, 2 * positive[-1][1] - 1)
    if normalization[0] <= 0 or len(edges) != SIZE + 1:
        raise ValueError("Positive full conditional target mass is required")
    masses, amplitudes = [], []
    for left, right in zip(edges, edges[1:]):
        checkpoint()
        unnormalized = right[0] - left[1], right[1] - left[0]
        probability = bounds(iv(unnormalized) / iv(normalization))
        if not 0 < probability[0] <= probability[1] < 1:
            raise ValueError("Fixed CDF precision failed a strictly positive bin enclosure")
        masses.append(probability)
        root = bounds(mp.iv.sqrt(iv(probability)))
        # Conversion proposes a binary64 number. Its exact literal is certified
        # below, so neither rounding nor a square-root midpoint is free.
        amplitudes.append(float((root[0] + root[1]) / 2))
    amplitudes = np.asarray(amplitudes, dtype=np.float64)
    certificate = certify_rounded_target(masses, amplitudes)
    certificate.update(
        {
            "bits": BITS,
            "cutoff_exact": pair(CUTOFF),
            "distinct_nonnegative_CDF_boundaries": len(positive),
            "normalization": enclosed(normalization),
            "nonnegative_CDF_boundaries": [enclosed(value) for value in positive],
            "probability_enclosures": [enclosed(value) for value in masses],
            "amplitude_literals": save_literals(amplitudes),
            "CDF_degree": CDF_DEGREE,
            "pi_arctan_terms": PI_TERMS,
            "decimal_interval_precision": DPS,
            "law": "q10 uniform-x Gaussian bins on[-6,6], conditionally normalized",
            "this_law_is_the_accepted_Box_Muller_law": False,
        }
    )
    return amplitudes, certificate


def compress_once(amplitudes, bond):
    """The archived fixed left-to-right truncated SVD, with saved raw cores."""
    if bond not in BONDS or np.shape(amplitudes) != (SIZE,):
        raise ValueError("The one q10 target and one of the three fixed bonds are required")
    tensor, rank, cores = np.asarray(amplitudes).copy().reshape(1, -1), 1, []
    discarded = 0.0
    for _ in range(BITS - 1):
        u, s, vh = np.linalg.svd(tensor.reshape(rank * 2, -1), full_matrices=False)
        keep = min(bond, len(s))
        discarded += float(np.sum(s[keep:] ** 2))
        cores.append(u[:, :keep].reshape(rank, 2, keep))
        tensor, rank = s[:keep, None] * vh[:keep], keep
    cores.append(tensor.reshape(rank, 2, 1))
    cores = validate_cores(cores)
    if tuple(core.shape[-1] for core in cores[:-1]) != EXPECTED_BONDS[bond]:
        raise ValueError("The fixed bond pattern was not emitted; no rank adaptation")
    return cores, {
        "discarded_SVD_norm_squared_numeric_not_a_certificate": discarded,
        "normalization": (
            "exact literal-vector norm in the certificate; "
            "one numeric norm in canonicalization"
        ),
    }


def gram_norm_upper(columns):
    columns = np.asarray(columns)
    if columns.ndim != 2 or max(columns.shape) > 16:
        raise ValueError("Bounded local core columns are required")
    vectors = [literal_vector(columns[:, i]) for i in range(columns.shape[1])]
    # Hermitian Gram spectral radius <= the largest absolute row sum.
    row_sums = [
        sum((abs(dot(a, b)[0]) + abs(dot(a, b)[1]) for b in vectors), Fraction(0)) for a in vectors
    ]
    return sqrt_upper(max(row_sums))


def completion_error_upper(columns, completed):
    columns, completed = np.asarray(columns), np.asarray(completed)
    if (
        columns.ndim != 2
        or not 1 <= columns.shape[1] <= columns.shape[0] <= 16
        or (completed.shape != (len(columns), len(columns)))
    ):
        raise ValueError("Matching bounded completed matrix is required")
    completed_literals = literal_vector(completed[:, : columns.shape[1]])
    column_literals = literal_vector(columns)
    if len(completed_literals) != len(column_literals):
        raise ValueError("Matching completed and original column literals are required")
    difference = [
        add(a, (-b[0], -b[1]))
        for a, b in zip(completed_literals, column_literals)
    ]
    return sqrt_upper(norm_squared(difference))


def operation_data(operation):
    return {
        "gate": operation.gate,
        "wires": list(operation.wires),
        "angle_exact": pair(operation.angle) if operation.angle is not None else None,
    }


def local_operation_blocks(plan, operations, records):
    if len(records) != len(plan.transitions):
        raise ValueError("One native decomposition record per saved transition is required")
    cursor, blocks = 0, []
    for transition, record in zip(plan.transitions, records):
        if record["site"] != transition.site:
            raise ValueError("Native decomposition site order changed")
        if transition.swap_before is not None:
            if cursor >= len(operations) or operations[cursor] != Primitive(
                "swap", transition.swap_before
            ):
                raise ValueError("The emitted shrink SWAP was changed")
            cursor += 1
        phase = Fraction(*record["recorded_global_phase_exact"])
        block = []
        if phase:
            if cursor >= len(operations) or operations[cursor] != Primitive("phase", (), phase):
                raise ValueError("The emitted SDK global phase was changed or omitted")
            block.append(operations[cursor])
            cursor += 1
        count = record["native_slots"]
        if type(count) is not int or count < 0 or cursor + count > len(operations):
            raise ValueError("The bounded native local operation count is invalid")
        block.extend(operations[cursor : cursor + count])
        cursor += count
        blocks.append(tuple(block))
    if cursor != len(operations):
        raise ValueError("Unbound native operations remain after the last local record")
    return tuple(blocks)


def native_local_matrix(operations, wires, checkpoint=lambda: None):
    wires = tuple(wires)
    if not 1 <= len(wires) <= 4 or len(set(wires)) != len(wires):
        raise ValueError("At most four distinct local wires are required")
    size = 1 << len(wires)
    value = [[mp.iv.mpc(int(i == j)) for j in range(size)] for i in range(size)]
    index = {wire: bit for bit, wire in enumerate(wires)}
    for operation in operations:
        checkpoint()
        if operation.gate not in ("ry", "rz", "cx", "phase"):
            raise ValueError("The fixed SDK native basis is required")
        if operation.gate == "phase":
            if operation.wires or not isinstance(operation.angle, Fraction):
                raise ValueError("An exact recorded scalar phase is required")
            c, s = mp.iv.cos(iv(operation.angle)), mp.iv.sin(iv(operation.angle))
            scalar = mp.iv.mpc(c, s)
            value = [[scalar * entry for entry in row] for row in value]
            continue
        if any(wire not in index for wire in operation.wires):
            raise ValueError("A native operation escapes its local wire map")
        if len(operation.wires) != (2 if operation.gate == "cx" else 1):
            raise ValueError("The fixed native gate arity is required")
        first = index[operation.wires[0]]
        if operation.gate == "cx":
            if (
                len(operation.wires) != 2
                or operation.wires[0] == operation.wires[1]
                or operation.angle is not None
            ):
                raise ValueError("Two distinct local CX wires and no angle are required")
            second = index[operation.wires[1]]
            old = value
            value = [old[row ^ (1 << second) if row & (1 << first) else row] for row in range(size)]
        else:
            if len(operation.wires) != 1 or not isinstance(operation.angle, Fraction):
                raise ValueError("One local rotation wire and an exact rational angle are required")
            c, s = mp.iv.cos(iv(operation.angle / 2)), mp.iv.sin(iv(operation.angle / 2))
            if operation.gate == "rz":
                value = [
                    [mp.iv.mpc(c, s if row & (1 << first) else -s) * entry for entry in entries]
                    for row, entries in enumerate(value)
                ]
            else:
                following = [list(row) for row in value]
                for zero in range(size):
                    if zero & (1 << first):
                        continue
                    one = zero | (1 << first)
                    for column in range(size):
                        following[zero][column] = c * value[zero][column] - s * value[one][column]
                        following[one][column] = s * value[zero][column] + c * value[one][column]
                value = following
    return value


def sdk_operator_error_upper(operations, wires, matrix, checkpoint=lambda: None):
    matrix = np.asarray(matrix)
    if matrix.shape != (1 << len(wires),) * 2:
        raise ValueError("A matching full saved local matrix is required")
    actual = native_local_matrix(operations, wires, checkpoint)
    norm2 = Fraction(0)
    for row in range(len(matrix)):
        for column in range(len(matrix)):
            real, imag = literal(matrix[row, column])
            difference = actual[row][column] - mp.iv.mpc(iv(real), iv(imag))
            re, im = bounds(difference.real), bounds(difference.imag)
            norm2 += max(abs(re[0]), abs(re[1])) ** 2 + max(abs(im[0]), abs(im[1])) ** 2
    return sqrt_upper(norm2)


def validate_plan_binding(canonical, plan):
    cores = validate_cores(canonical.cores)
    count = len(cores)
    largest = max(max(core.shape[0], core.shape[2]) for core in cores)
    scratch = tuple(range(count, count + largest.bit_length() - 1))
    if plan.output_wires_msb_first != tuple(reversed(range(count))) or (
        plan.bond_wires_low_bit_first != scratch
        or plan.num_wires != count + len(scratch)
        or plan.required_initial_zero_wires != tuple(range(plan.num_wires))
        or plan.final_bond_rank != 1
        or len(plan.transitions) != count
    ):
        raise ValueError("The exact fresh-output/bond structure plan is required")
    for site, (core, transition) in enumerate(zip(cores, plan.transitions)):
        left, _, right = core.shape
        right_bits = right.bit_length() - 1
        output = count - site - 1
        cleared = scratch[left.bit_length() - 2] if left == 2 * right else None
        swap = (cleared, output) if cleared is not None else None
        if (
            transition.site,
            transition.output_wire,
            transition.left_rank,
            transition.right_rank,
            transition.local_wires,
            transition.swap_before,
            transition.newly_cleared_wire,
        ) != (
            site,
            output,
            left,
            right,
            scratch[:right_bits] + (output,),
            swap,
            cleared,
        ) or not np.array_equal(transition.isometry_columns, core.reshape(left, -1).T):
            raise ValueError("A transition no longer binds its exact canonical core or wire map")
    return True


def certify_emission(
    compressed_cores, canonical, plan, operations, records, checkpoint=lambda: None
):
    validate_plan_binding(canonical, plan)
    original = exact_contract(compressed_cores, checkpoint)
    canonical_vector = exact_contract(canonical.cores, checkpoint)
    if len(plan.transitions) != len(canonical.cores):
        raise ValueError("Every saved canonical core needs its exact transition")
    blocks = local_operation_blocks(plan, operations, records)
    if len(blocks) != len(canonical.cores):
        raise ValueError("One native block per canonical core and transition is required")
    gauge = gauge_distance(canonical_vector, original)
    error, preceding_norm, rows = gauge, Fraction(1), []
    for core, transition, block in zip(canonical.cores, plan.transitions, blocks):
        checkpoint()
        expected = core.reshape(core.shape[0], -1).T
        if not np.array_equal(transition.isometry_columns, expected):
            raise ValueError("A saved transition no longer binds its canonical core literals")
        columns = transition.isometry_columns
        completion = completion_error_upper(columns, transition.matrix)
        sdk = sdk_operator_error_upper(block, transition.local_wires, transition.matrix, checkpoint)
        norm = gram_norm_upper(columns)
        error += preceding_norm * (completion + sdk)
        rows.append(
            {
                "site": transition.site,
                "dimension": len(transition.matrix),
                "active_columns": columns.shape[1],
                "preceding_core_norm_product_upper_exact": pair(preceding_norm),
                "core_operator_norm_upper_exact": pair(norm),
                "completion_active_column_Frobenius_upper_exact": pair(completion),
                "SDK_full_operator_Frobenius_upper_exact": pair(sdk),
                "saved_global_phase_included": True,
            }
        )
        preceding_norm *= norm
    return {
        "canonical_gauge_vector_distance_upper_exact": pair(gauge),
        "compressed_to_exact_native_preparation_trace_upper_exact": pair(min(Fraction(1), error)),
        "uncapped_preparation_vector_error_upper_exact": pair(error),
        "telescoping_uses_actual_rounded_core_norm_products": True,
        "each_native_primitive_is_exactly_unitary_for_its_saved_rational_angle": True,
        "literal_inverse_unitarity_is_separate_from_fresh_preparation_error": True,
        "full_SDK_operator_error_is_not_a_single_column_check": True,
        "float_unitarity_predicate_or_zero_gauge_assumed": False,
        "local_operator_rows": rows,
    }


def assessment_rows(bond, table_error, compression_error, emission_error, rotations):
    if bond not in BONDS or type(rotations) is not int or rotations < 0:
        raise ValueError(
            "One of the three fixed bonds and a nonnegative rotation count are required"
        )
    values = tuple(map(rational, (table_error, compression_error, emission_error)))
    if any(value < 0 for value in values):
        raise ValueError("Every charged error component must be nonnegative")
    paid_sum = sum(values, Fraction(0)) + SYNTHESIS_RESERVE
    return [
        {
            "bond": bond,
            "scalar_target_exact": pair(target),
            "table_trace_upper_exact": pair(values[0]),
            "compression_trace_upper_exact": pair(values[1]),
            "native_emission_trace_upper_exact": pair(values[2]),
            "paid_reserved_synthesis_operator_upper_exact": pair(SYNTHESIS_RESERVE),
            "prospective_component_sum_with_synthesis_reserve_exact": pair(paid_sum),
            "component_ledger_eligible_for_one_future_registry": paid_sum <= target
            and rotations <= MAX_ROTATIONS,
            "complete_preparation_trace_certificate": None,
            "complete_Clifford_T_cost": None,
            "conditional_disjoint_factor_budget_rows": [
                {
                    "case": case,
                    "hypothetical_disjoint_scalar_factors": factors,
                    "bounded_observable_span_exact": [40, 1],
                    "prospective_joint_trace_upper_with_synthesis_reserve_exact": pair(
                        min(Fraction(1), factors * paid_sum)
                    ),
                    "prospective_preparation_dollars_with_synthesis_reserve_exact": pair(
                        40 * min(Fraction(1), factors * paid_sum)
                    ),
                    "requires_complete_future_synthesis_and_disjoint_lane_construction": True,
                    "actual_financial_price_law_error_certified": False,
                }
                for case, factors in (("B4x12", 60), ("B8x52", 468))
            ],
            "q10_continuous_price_law_certificate_passed": False,
            "product_factor_purity_refinement_used": False,
            "original_Box_Muller_source_or_price_ledger_adopted": False,
        }
        for target in TARGETS
    ]
