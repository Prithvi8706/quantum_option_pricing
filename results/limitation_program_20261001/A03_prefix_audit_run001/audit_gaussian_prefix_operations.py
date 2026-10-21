"""Independent interval audit of actual prefix operations, including phase.

No producer imports or new synthesis attempts. Certifies one uncontrolled
two-qubit prefix; the remaining tree, law bridge and controlled use stay open.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import factorial
from pathlib import Path
import shutil
import sys
import time
import traceback

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "A03_prefix_run001"
DPS = 190
ARCTAN_TERMS = 300
CDF_DEGREE = 300
CPU_LIMIT = 60


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def pair(value):
    return [value.numerator, value.denominator]


def endpoint(value):
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def bounds(value):
    return tuple(endpoint(item) for item in value._mpi_)


def iv(value):
    if isinstance(value, tuple):
        low, high = value
        assert low <= high
        return mp.iv.mpf([iv(low).a, iv(high).b])
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def saved_bounds(value):
    return Fraction(*value["lower_exact"]), Fraction(*value["upper_exact"])


def enclosed(outer, inner):
    assert outer[0] <= inner[0] <= inner[1] <= outer[1]


def serialized(value):
    return {"lower_exact": pair(value[0]), "upper_exact": pair(value[1])}


def pi_enclosure():
    # Alternating rational series, separately implemented from producer.
    enclosures = []
    for base in (5, 239):
        total = sum(
            (Fraction((-1) ** k, (2 * k + 1) * base ** (2 * k + 1))
             for k in range(ARCTAN_TERMS)), Fraction(0)
        )
        following = total + Fraction(
            (-1) ** ARCTAN_TERMS,
            (2 * ARCTAN_TERMS + 1) * base ** (2 * ARCTAN_TERMS + 1),
        )
        enclosures.append((min(total, following), max(total, following)))
    first, second = enclosures
    return 16 * first[0] - 4 * second[1], 16 * first[1] - 4 * second[0]


def cdf_enclosure(x, pi):
    # Exact integrated Taylor terms and a derivative-bound remainder.
    if x < 0:
        lo, hi = cdf_enclosure(-x, pi)
        return 1 - hi, 1 - lo
    if x == 0:
        return Fraction(1, 2), Fraction(1, 2)
    polynomial = sum(
        (Fraction((-1) ** k * x ** (2 * k + 1),
                  2**k * factorial(k) * (2 * k + 1))
         for k in range(CDF_DEGREE + 1)), Fraction(0)
    )
    remainder = Fraction(
        x ** (2 * CDF_DEGREE + 3),
        2 ** (CDF_DEGREE + 1) * factorial(CDF_DEGREE + 1) * (2 * CDF_DEGREE + 3),
    )
    return bounds(iv(Fraction(1, 2)) + iv(
        (polynomial - remainder, polynomial + remainder)
    ) / mp.iv.sqrt(2 * iv(pi)))


def matmul(left, right):
    size = len(left)
    return [[sum((left[row][k] * right[k][col] for k in range(size)),
                 mp.iv.mpc(0)) for col in range(size)] for row in range(size)]


def tensor(left, right):
    return [[left[i // 2][j // 2] * right[i % 2][j % 2]
             for j in range(4)] for i in range(4)]


def frobenius_squared(left, right):
    result = mp.iv.mpf(0)
    for i in range(len(left)):
        for j in range(len(left)):
            delta = left[i][j] - right[i][j]
            result += delta.real**2 + delta.imag**2
    return bounds(result)


def ry(angle):
    c, s = mp.iv.cos(angle / 2), mp.iv.sin(angle / 2)
    return [[mp.iv.mpc(c), mp.iv.mpc(-s)], [mp.iv.mpc(s), mp.iv.mpc(c)]]


def verify_frozen(frozen):
    for name, expected in frozen.items():
        assert sha(ROOT / name) == expected, ("Changed frozen dependency", name)


def prepare(output):
    output.relative_to(PROGRAM)
    assert not output.exists()
    prior = read(SOURCE / "manifest.json")
    frozen = dict(prior["frozen_inputs"])
    frozen.update(prior["files"])
    paths = [Path(__file__), SOURCE / "manifest.json", Path(sys.executable)]
    paths.extend(Path(mp.__file__).parent.rglob("*.py"))
    frozen.update({relative(path): sha(path) for path in paths})
    verify_frozen(frozen)
    output.mkdir()
    shutil.copy2(Path(__file__), output / Path(__file__).name)
    create(output / "protocol.json", dict(
        created_utc=datetime.now(timezone.utc).isoformat(), local_only=True,
        before_independent_CDF_angle_or_gate_matrix_checks=True,
        frozen_inputs=frozen, independent_decimal_interval_precision=DPS,
        independent_Machin_terms=ARCTAN_TERMS, independent_CDF_degree=CDF_DEGREE,
        fixed_CDF_boundaries=[-6, -3, 0, 3, 6], fixed_prefix_levels=2,
        actual_saved_operations=310, CPU_limit_seconds=CPU_LIMIT,
        exact_global_phase_is_required=True, new_synthesis_attempts=0,
        new_tests_gates_prices_or_financial_replays=0,
        full_loader_law_and_controlled_adoption=False,
    ))


def audit(output):
    started = time.process_time()
    protocol = read(output / "protocol.json")
    verify_frozen(protocol["frozen_inputs"])
    mp.iv.dps = DPS
    pi = pi_enclosure()
    probability = read(SOURCE / "prefix_probability_angles.json")
    cdfs = {x: cdf_enclosure(x, pi) for x in (-6, -3, 0, 3, 6)}
    for x, result in cdfs.items():
        enclosed(saved_bounds(probability["cdf_boundaries"][str(x)]), result)
    norm = 2 * iv(cdfs[6]) - 1
    half = iv(cdfs[6]) - iv(Fraction(1, 2))
    outer = iv(cdfs[6]) - iv(cdfs[3])
    inner = iv(cdfs[3]) - iv(Fraction(1, 2))
    for key, result in (("normalization", norm), ("unnormalized_half_mass", half),
                        ("unnormalized_outer_quarter_mass", outer),
                        ("unnormalized_inner_quarter_mass", inner)):
        enclosed(saved_bounds(probability[key]), bounds(result))
    for row, mass in zip(probability["normalized_four_prefix_blocks"],
                         (outer, inner, inner, outer), strict=True):
        enclosed(saved_bounds(row["probability"]), bounds(mass / norm))
    ratio = saved_bounds(probability["theta_left_over_pi"])
    p_inner = bounds(inner / half)
    lo_image = bounds(mp.iv.sin(iv(ratio[0]) * iv(pi) / 2)**2)
    hi_image = bounds(mp.iv.sin(iv(ratio[1]) * iv(pi) / 2)**2)
    assert lo_image[1] < p_inner[0] <= p_inner[1] < hi_image[0]
    assert 0 < ratio[0] < ratio[1] < 1
    beta = saved_bounds(probability["walsh_rotations"][2]["angle_radians"])
    # Saved angle endpoints are exact rational products. An interval-rounded
    # product would widen the coincident endpoint beyond its exact margin.
    assert ratio[0] > Fraction(1, 2)
    enclosed(beta, ((ratio[0] - Fraction(1, 2)) * pi[0],
                    (ratio[1] - Fraction(1, 2)) * pi[1]))
    for row, result in zip(probability["nodes"][1:], (outer / half, inner / half), strict=True):
        enclosed(saved_bounds(row["left_probability"]), bounds(result))
    theta_values = ((ratio[0] * pi[0], ratio[1] * pi[1]),
                    ((1 - ratio[1]) * pi[0], (1 - ratio[0]) * pi[1]))
    for row, result in zip(probability["nodes"][1:], theta_values, strict=True):
        enclosed(saved_bounds(row["theta_radians"]), result)
    candidate = read(SOURCE / "synthesis_candidate.json")
    operations = candidate["actual_prefix_execution_operations"]
    counts = Counter(op["gate"] for op in operations)
    assert len(operations) == 310 and counts["t"] == 116 and counts["cx"] == 2
    assert sum(v for k, v in counts.items() if k != "t") == 194
    zero, one = mp.iv.mpc(0), mp.iv.mpc(1)
    identity = [[one, zero], [zero, one]]
    root = mp.iv.sqrt(2)
    omega = mp.iv.mpc(1 / root, 1 / root)
    gates = dict(
        h=[[one / root, one / root], [one / root, -one / root]],
        z=[[one, zero], [zero, -one]], t=[[one, zero], [zero, omega]],
        s=[[one, zero], [zero, mp.iv.mpc(0, 1)]],
        sdg=[[one, zero], [zero, mp.iv.mpc(0, -1)]], x=[[zero, one], [one, zero]],
    )
    actual = tensor(identity, identity)
    for op in operations:
        gate, wires = op["gate"], op["wires"]
        if gate == "cx":
            assert wires == [9, 8]
            matrix = [[mp.iv.mpc(int(j == (i if i < 2 else i ^ 1)))
                       for j in range(4)] for i in range(4)]
        else:
            assert wires in ([9], [8]) and gate in gates
            matrix = (
                tensor(gates[gate], identity) if wires == [9]
                else tensor(identity, gates[gate])
            )
        actual = matmul(matrix, actual)
    theta0, theta1 = iv(pi) / 2 + iv(beta), iv(pi) / 2 - iv(beta)
    controlled = [[zero for _ in range(4)] for _ in range(4)]
    for block, matrix in enumerate((ry(theta0), ry(theta1))):
        for i in range(2):
            for j in range(2):
                controlled[2 * block + i][2 * block + j] = matrix[i][j]
    ideal = matmul(controlled, tensor(ry(iv(pi) / 2), identity))
    assert candidate["tracked_global_omega_power"] == 5
    assert candidate["matrix_product_gates"].count("W") == 5
    phase = omega**5
    aligned = [[phase * item for item in row] for row in actual]
    aligned_error = frobenius_squared(aligned, ideal)
    unaligned_error = frobenius_squared(actual, ideal)
    eps = Fraction(1, 19150560000)
    assert aligned_error[1] < 2 * eps**2
    assert unaligned_error[0] > 1
    budgets = read(SOURCE / "full_tree_and_budget.json")
    assert budgets["counts"]["remaining_conditional_nodes_without_angle_certificates"] == 1020
    assert budgets["counts"]["potential_minus_archived_Ry_count"] == 47
    for row, factors in zip(budgets["rows"], (60, 468), strict=True):
        expected = 40 * factors * 1023 * eps
        assert Fraction(*row["conditional_bounded_observable_dollars_exact"]) == expected
        assert expected <= Fraction(1, 1000)
        assert row["loading_budget_adopted_in_financial_ledger"] is False
    create(output / "independent_prefix_checks.json", dict(
        CDF_boundary_intervals={str(x): serialized(v) for x, v in cdfs.items()},
        probability_and_monotone_angle_brackets_passed=True,
        actual_operation_counts=dict(counts), actual_operations_checked=len(operations),
        phase_aligned_full_interval_Frobenius_squared=serialized(aligned_error),
        unaligned_Frobenius_squared=serialized(unaligned_error), tracked_global_omega_power=5,
        coherent_control_requires_additional_phase_compensation=True,
        full_tree_remaining_nodes=1020, omitted_float_rotations_still_unproved_zero=47,
        loading_budget_adopted=False, physical_cost_or_full_price_certificate=False,
    ))
    verify_frozen(protocol["frozen_inputs"])
    cpu = time.process_time() - started
    assert cpu < CPU_LIMIT
    create(output / "summary.json", dict(passed=True, local_only=True, CPU_seconds=cpu,
        actual_operations_checked=310, new_tests_or_synthesis_attempts=0,
        producer_functions_imported=False, frozen_inputs_unchanged=True,
        full_loader_or_controlled_use_or_law_adopted=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if args.mode == "prepare":
        prepare(output)
        print("Independent prefix audit prospectively frozen")
        return
    output.relative_to(PROGRAM)
    assert not (output / "summary.json").exists()
    try:
        audit(output)
    except Exception:
        create(output / "failure.json", dict(passed=False, traceback=traceback.format_exc()))
        raise
    finally:
        protocol = read(output / "protocol.json")
        create(output / "manifest.json", dict(
            files={relative(p): sha(p) for p in sorted(output.rglob("*"))
                   if p.is_file() and p.name != "manifest.json"},
            frozen_inputs=protocol["frozen_inputs"], manifest_self_hash_excluded=True,
        ))
    print("Independent actual-operation prefix audit passed")


if __name__ == "__main__":
    main()
