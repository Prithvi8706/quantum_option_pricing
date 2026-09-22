"""Explicit known-moment mean estimation with certified Hadamard tests.

Kothari--O'Donnell (arXiv:2208.07544), Theorem 3.21 and Section 3.6,
with balanced overlapping interval updates.  This is a concrete constant
optimization of known components, not a new quantum mean-estimation theorem.
"""

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.stats import binom

from research.controlled_source_completion.modern_mean import spectral_law


ROOT = Path("results/controlled_priority_completion")
OLD_LEDGER = Path(
    "results/controlled_completion_followup/arithmetic_v1/cost_v3_phase64/ledger.json"
)


def fraction_pair(x):
    return [x.numerator, x.denominator]


def root_upper(moment, bits=64):
    scaled = Fraction(moment) * (1 << (2 * bits))
    root = math.isqrt(scaled.numerator // scaled.denominator)
    if root * root * scaled.denominator < scaled.numerator:
        root += 1
    return Fraction(root, 1 << bits)


def power_two_at_least(x):
    answer = 1
    while answer < x:
        answer *= 2
    return answer


def intervals(moment, error, normalizer_factor, c):
    radius = root_upper(moment)
    # Preserve the already proved f64 phase-source range contract.
    normalizer = max(16, power_two_at_least(normalizer_factor * radius))
    width = 2 * radius
    contraction = (1 + c) / (1 + 3 * c)
    rows = []
    while width / 2 > Fraction(error):
        epsilon = width / ((1 + 3 * c) * normalizer)
        rows.append((width, epsilon))
        width *= contraction
    return radius, normalizer, contraction, rows


def probability_bounds(rms, epsilon, c, C, T, certify=False):
    """Return conservative rational bounds for P(+ | small/large promise).

    On the spectral good event (failure <= 2/C**2), Theorem 3.21
    gives angular bounds; multiplying them by integer T certifies the
    Hadamard-test probabilities.  80-digit interval arithmetic certifies
    each selected bound, including the angular monotonicity conditions.
    """
    if not 0 < C * rms < 1:
        return None
    s, e, cc = float(rms), float(epsilon), float(c)
    upper_arg = (1 + 2 * cc) * e / (1 - C * s)
    if upper_arg >= 1:
        return None
    low = 2 * e / (math.sqrt(1 + s * s) * (1 + C * s))
    high = 2 * math.asin(upper_arg)
    small = 2 * math.asin(cc * e / (1 - C * s))
    if not (0 <= T * small < math.pi and 0 < T * low <= T * high < 2 * math.pi):
        return None
    eta = 2 / C**2
    p_small = (1 - eta) * (1 + math.cos(T * small)) / 2
    p_large = eta + (1 - eta) * (1 + max(math.cos(T * low), math.cos(T * high))) / 2
    # A 2^-30 mesh leaves much more than binary64 roundoff as slack.
    den = 1 << 30
    a = Fraction(math.floor(p_small * den) - 1, den)
    b = Fraction(math.ceil(p_large * den) + 1, den)
    if a <= b or b < 0 or a > 1:
        return None
    if certify:
        mp.iv.dps = 80

        def iv(x):
            x = Fraction(x)
            return mp.iv.mpf(x.numerator) / x.denominator

        si, ei, ci = iv(rms), iv(epsilon), iv(c)
        alpha = 2 * ei / (mp.iv.sqrt(1 + si * si) * (1 + C * si))

        # mpmath.iv has no asin in the pinned version; atan(x/sqrt(1-x^2))
        # is asin(x) on these certified positive arguments.
        def asin(x):
            return mp.iv.atan2(x, mp.iv.sqrt(1 - x * x))

        beta = 2 * asin((1 + 2 * ci) * ei / (1 - C * si))
        gamma = 2 * asin(ci * ei / (1 - C * si))
        assert (T * gamma < mp.iv.pi) is True
        assert (T * alpha > 0) is True
        assert (T * beta < 2 * mp.iv.pi) is True
        fail = iv(Fraction(2, C * C))
        small_interval = (1 - fail) * (1 + mp.iv.cos(T * gamma)) / 2
        large_low = fail + (1 - fail) * (1 + mp.iv.cos(T * alpha)) / 2
        large_high = fail + (1 - fail) * (1 + mp.iv.cos(T * beta)) / 2
        assert (iv(a) < small_interval) is True
        assert (iv(b) > large_low) is True
        assert (iv(b) > large_high) is True
    return a, b


def threshold_for(r, p_small, p_large):
    """Minimize the larger of the two exact binomial tail probabilities."""
    a, b = float(p_small), float(p_large)
    left, right = 0, r + 1
    while right - left > 1:
        k = (left + right) // 2
        if binom.cdf(k - 1, r, a) > binom.sf(k - 1, r, b):
            right = k
        else:
            left = k
    candidates = (left, right)
    return min(
        candidates,
        key=lambda k: max(binom.cdf(k - 1, r, a), binom.sf(k - 1, r, b)),
    )


def repetitions(p_small, p_large, failure):
    """Find an integer repetition/threshold pair, then certify its tails."""

    def accepted(r):
        k = threshold_for(r, p_small, p_large)
        return max(
            binom.cdf(k - 1, r, float(p_small)),
            binom.sf(k - 1, r, float(p_large)),
        ) <= float(failure) * (1 - 1e-10)

    lo, hi = 0, 1
    while not accepted(hi):
        hi *= 2
        if hi > 100000:
            raise ValueError("No useful test separation")
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if accepted(mid):
            hi = mid
        else:
            lo = mid
    k = threshold_for(hi, p_small, p_large)
    return hi, k


def exact_tail(r, p, lower=None, upper=None):
    """Exact rational binomial probability, including endpoints."""
    lo = 0 if lower is None else lower
    hi = r if upper is None else upper
    n, d = p.numerator, p.denominator
    total = sum(math.comb(r, j) * n**j * (d - n) ** (r - j) for j in range(lo, hi + 1))
    return Fraction(total, d**r)


def candidate(moment, error, failure, normalizer_factor, c, C, certify=False):
    radius, normalizer, contraction, interval_rows = intervals(moment, error, normalizer_factor, c)
    rms = 2 * radius / normalizer
    preliminary = []
    for width, epsilon in interval_rows:
        if C * rms >= 1:
            return None
        s, e, cc = float(rms), float(epsilon), float(c)
        arg = (1 + 2 * cc) * e / (1 - C * s)
        if arg >= 1:
            return None
        lo = 2 * e / (math.sqrt(1 + s * s) * (1 + C * s))
        hi = 2 * math.asin(arg)
        mid = 2 * math.pi / (lo + hi)
        possibilities = []
        for T in range(max(1, math.floor(mid) - 1), math.ceil(mid) + 2):
            bounds = probability_bounds(rms, epsilon, c, C, T)
            if bounds is not None:
                a, b = bounds
                # Hoeffding is a cheap search score, not the final certificate.
                possibilities.append((T / float(a - b) ** 2, T, a, b))
        if not possibilities:
            return None
        _, T, a, b = min(possibilities)
        preliminary.append((width, epsilon, T, a, b))
    if not preliminary:
        return None
    total_T = sum(row[2] for row in preliminary)
    rows = []
    for j, (width, epsilon, T, a, b) in enumerate(preliminary):
        delta = Fraction(failure) * T / total_T
        if not certify:
            # Safe Hoeffding upper schedule guides a bounded design search.
            count = math.ceil(2 * math.log(1 / float(delta)) / float(a - b) ** 2) + 2
            k = None
        else:
            a, b = probability_bounds(rms, epsilon, c, C, T, certify=True)
            count, k = repetitions(a, b, delta)
            small_fail = exact_tail(count, a, upper=k - 1)
            large_fail = exact_tail(count, b, lower=k)
            assert max(small_fail, large_fail) <= delta
        row = dict(
            stage=j,
            width_exact=fraction_pair(width),
            test_epsilon_exact=fraction_pair(epsilon),
            anchor_fraction_exact=fraction_pair(c / (1 + 3 * c)),
            T=T,
            repetitions=count,
            small_if_plus_count_at_least=k,
            p_plus_small_lower_exact=fraction_pair(a),
            p_plus_large_upper_exact=fraction_pair(b),
            failure_allocation_exact=fraction_pair(delta),
            controlled_U_calls=T * count,
        )
        if certify:
            row.update(
                small_failure=float(small_fail),
                large_failure=float(large_fail),
                exact_binomial_tail_certificate=True,
                interval_transcendental_certificate=True,
            )
        rows.append(row)
    return dict(
        method="known-moment complex phase with integer Hadamard tests",
        moment=moment,
        error=error,
        ideal_test_failure=failure,
        endpoint_bits=64,
        initial_radius_exact=fraction_pair(radius),
        normalizer=normalizer,
        normalized_RMS_upper_exact=fraction_pair(rms),
        normalizer_factor=normalizer_factor,
        C=C,
        c_exact=fraction_pair(c),
        contraction_exact=fraction_pair(contraction),
        final_radius=float(Fraction(*rows[-1]["width_exact"]) * contraction / 2),
        stages=rows,
        controlled_U_calls=sum(row["controlled_U_calls"] for row in rows),
        hadamard_test_executions=sum(row["repetitions"] for row in rows),
        longest_single_chain=max(row["T"] for row in rows),
        certificates_complete=certify,
    )


def optimized_plan(moment, error, failure=0.003):
    """Finite design search using only a supplied moment and requested accuracy."""
    designs = []
    for scale in (8, 16, 32, 64, 128):
        for C in (3, 4, 5, 6, 8):
            for c in (
                Fraction(1, 10),
                Fraction(1, 8),
                Fraction(1, 6),
                Fraction(1, 5),
                Fraction(1, 4),
                Fraction(1, 3),
                Fraction(1, 2),
            ):
                result = candidate(moment, error, failure, scale, c, C)
                if result is not None:
                    designs.append(result)
    # Refine the best Hoeffding-scored designs with exact binomial tails.
    # No assertion of globally optimal constants is made.
    selected = []
    for row in sorted(designs, key=lambda x: x["controlled_U_calls"])[:8]:
        selected.append(
            candidate(
                moment,
                error,
                failure,
                row["normalizer_factor"],
                Fraction(*row["c_exact"]),
                row["C"],
                certify=True,
            )
        )
    best = min(selected, key=lambda x: x["controlled_U_calls"])
    best["searched_designs"] = len(designs)
    best["binomial_refined_designs"] = len(selected)
    return best


def controller(allocation, measure):
    """Classical controller; a device supplies independent plus/minus bits.

    The normalized oracle is (Y - target)/normalizer.  The existing phase
    circuit's input named 'left' receives target.  Endpoint rounding is
    charged to the separate coherent approximation budget.
    """
    radius = Fraction(*allocation["initial_radius_exact"])
    left, width = -radius, 2 * radius
    c = Fraction(*allocation["c_exact"])
    contraction = Fraction(*allocation["contraction_exact"])
    history = []
    for stage in allocation["stages"]:
        assert width == Fraction(*stage["width_exact"])
        target = left + c * width / (1 + 3 * c)
        raw_target = round(target * (1 << allocation["endpoint_bits"]))
        outcomes = list(measure(stage, raw_target))
        if len(outcomes) != stage["repetitions"] or any(type(x) is not bool for x in outcomes):
            raise ValueError("Hadamard results must be exactly repetitions booleans")
        small = sum(outcomes) >= stage["small_if_plus_count_at_least"]
        if not small:
            left += 2 * c * width / (1 + 3 * c)
        width *= contraction
        history.append(
            dict(
                stage=stage["stage"],
                small=small,
                target_raw=raw_target,
                left_exact=fraction_pair(left),
            )
        )
    exact_center = left + width / 2
    estimate = float(exact_center)
    rounding = abs(Fraction(estimate) - exact_center)
    radius = math.nextafter(float(width / 2 + rounding), math.inf)
    assert radius <= allocation["error"]
    return dict(
        estimate=estimate,
        radius=radius,
        rounding_error_bound=math.nextafter(float(rounding), math.inf),
        history=history,
    )


def hadamard_plus_probability(values, probabilities, T):
    phases, weights = spectral_law(values, probabilities)
    return float(np.dot(weights, (1 + np.cos(T * phases)) / 2))


def main():
    source_rows = json.loads(OLD_LEDGER.read_text())
    output = []
    for old in source_rows:
        if old["f"] != 40:
            continue
        discount = math.exp(-0.03 * (0.5 if old["model"] == "C4" else 1.5))
        allocation = optimized_plan(old["moment"], 0.002 / discount)
        one = old["single_U"]
        calls = allocation["controlled_U_calls"]
        depth = calls * one["t_depth"]
        phases = calls * one["controlled_bit_phases"]
        rotations = 3 * phases
        row = dict(
            model=old["model"],
            mode=old["mode"],
            financial_fraction_bits=40,
            phase_fraction_bits=64,
            allocation=allocation,
            previous_controlled_U_calls=old["ledger"]["controlled_U_calls"],
            query_reduction=old["ledger"]["controlled_U_calls"] / calls,
            arithmetic_T_count=calls * one["t_count"],
            arithmetic_serial_T_depth=depth,
            single_U=one,
            hadamard_test_controls=1,
            logical_qubits_upper=one["logical_qubits"] - one["qpe_bits"] + 1,
            IQFT_gates=0,
            uniform_preparation_H=allocation["hadamard_test_executions"]
            * one["initial_random_hadamards"],
            additional_single_qubit_rotations=rotations,
            controlled_phase_decomposition_CX=2 * phases,
            arithmetic_clifford_CX=calls * one["clifford_cx"],
            arithmetic_clifford_H=calls * one["clifford_h"],
            arithmetic_X=calls * one["x"],
            reflection_control_Z=calls,
            test_preparation_and_measurement_H=2 * allocation["hadamard_test_executions"],
            measured_control_bits=allocation["hadamard_test_executions"],
            classical_constant_load_and_unload_X_upper=4
            * 96
            * allocation["hadamard_test_executions"],
            required_each_rotation_operator_error=0.0005 / (2 * rotations),
            required_uniform_phase_function_error=0.0005 / (2 * calls),
            longest_single_chain_arithmetic_T_depth=allocation["longest_single_chain"]
            * one["t_depth"],
            optimistic_serial_seconds_at_1ns_T_layer=depth * 1e-9,
            optimistic_serial_seconds_at_100ns_T_layer=depth * 1e-7,
            required_T_layer_seconds_for_10x=old["tenfold_total_budget_seconds"] / depth,
            tenfold_total_budget_seconds=old["tenfold_total_budget_seconds"],
            actual_full_price_seconds=None,
            gate_passes=False,
            scope=(
                "Same compiled financial and phase oracle; arithmetic-only implementation "
                "schedule, not a hardware runtime or universal lower bound. Full "
                "financial/physical obligations remain."
            ),
        )
        output.append(row)
        ROOT.mkdir(parents=True, exist_ok=True)
        (ROOT / "estimator_hadamard.json").write_text(json.dumps(output, indent=2) + "\n")
        print(
            json.dumps(
                {
                    k: row[k]
                    for k in (
                        "model",
                        "mode",
                        "query_reduction",
                        "optimistic_serial_seconds_at_1ns_T_layer",
                        "required_T_layer_seconds_for_10x",
                    )
                }
            ),
            flush=True,
        )
    reading_path = Path(".context/advantage_reading_20260922/kothari.txt")
    provenance = dict(
        primary_source="https://arxiv.org/abs/2208.07544",
        exact_sections="Theorem 3.21 and proof (eqs.48-55), Section 3.6, Lemma 4.3",
        local_primary_reading_present=reading_path.is_file(),
        local_primary_sha256=(
            hashlib.sha256(reading_path.read_bytes()).hexdigest()
            if reading_path.is_file()
            else None
        ),
        compiled_cost_input=str(OLD_LEDGER),
        compiled_cost_sha256=hashlib.sha256(OLD_LEDGER.read_bytes()).hexdigest(),
    )
    (ROOT / "estimator_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    main()
