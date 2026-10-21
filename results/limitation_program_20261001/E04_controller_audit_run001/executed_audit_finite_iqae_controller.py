"""Independent simultaneous-confidence, transcript and paid-cost controller audit.

The producer/controller are never imported or rerun. Stored observations are
reconciled from their fixed RNG seeds and independently powered integer
Chebyshev recurrence; no new candidate, financial or quantum observations are
acquired. Confidence remains an ideal-observation statement, with explicit
non-delivery, terminal measurement/cleanup and unknown physical durations.
"""

from __future__ import annotations

# Explanations in receipts are prose, not compressed identifiers.
# ruff: noqa: E501

import argparse
import ast
from datetime import datetime, timezone
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import random
import shutil
import sys
import traceback
import xml.etree.ElementTree as ET

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
ALPHA = Fraction(3, 1000)
EPSILON = Fraction(9, 128000)
PAID_CAP = 983024
PI = None


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def pair(value):
    return [value.numerator, value.denominator]


def exact(value):
    result = Fraction(*value)
    assert pair(result) == value
    return result


def verify(files):
    for name, digest in files.items():
        assert sha(ROOT / name) == digest, ("frozen dependency changed", name)


def iv(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoint(value):
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def bounds(value):
    return tuple(endpoint(part) for part in value._mpi_)


def independent_pi():
    # The two positive arctangents sum below pi/2, with tangent addition equal 1.
    assert (Fraction(1, 2) + Fraction(1, 3)) / (1 - Fraction(1, 6)) == 1
    intervals = []
    for denominator in (2, 3):
        power, total = Fraction(1, denominator), Fraction(0)
        for j in range(240):
            total += (-1 if j % 2 else 1) * power / (2 * j + 1)
            power /= denominator**2
        intervals.append((total, total + power / 481))
    lo, hi = (4 * sum(row[k] for row in intervals) for k in (0, 1))
    assert hi - lo < Fraction(1, 10**140)
    return lo, hi, mp.iv.mpf([iv(lo).a, iv(hi).b])


@lru_cache(maxsize=None)
def probability(theta):
    assert 0 <= theta <= Fraction(1, 2)
    if theta in (0, Fraction(1, 2)):
        return (Fraction(0) if theta == 0 else Fraction(1),) * 2
    return bounds(mp.iv.sin(PI * iv(theta)) ** 2)


@lru_cache(maxsize=None)
def inverse_interval(p):
    assert 0 <= p <= 1
    known = {
        Fraction(0): Fraction(0),
        Fraction(1, 4): Fraction(1, 6),
        Fraction(1, 2): Fraction(1, 4),
        Fraction(3, 4): Fraction(1, 3),
        Fraction(1): Fraction(1, 2),
    }
    if p in known:
        return (known[p],) * 2
    left, right = Fraction(0), Fraction(1, 2)
    for _ in range(80):
        mid = (left + right) / 2
        lo, hi = probability(mid)
        if hi < p:
            left = mid
        elif lo > p:
            right = mid
        else:
            break
    # Independent endpoint tests prove the inverse is bracketed, even if an
    # interval comparison stopped before the full80 iterations.
    assert probability(left)[0] <= p <= probability(right)[1]
    return left, right


def matrix_product(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2)
    )


@lru_cache(maxsize=None)
def exact_toy_probability(amplitude, K):
    """Integer matrix power of the scaled T recurrence."""
    assert type(K) is int and K >= 1 and K % 2 == 1
    c = 1 - 2 * amplitude
    n, d = c.numerator, c.denominator
    # S_j=d^j*T_j(n/d): S_j=2n*S_(j-1)-d^2*S_(j-2).
    matrix, product, exponent = ((2 * n, -d * d), (1, 0)), ((1, 0), (0, 1)), K - 1
    while exponent:
        if exponent & 1:
            product = matrix_product(product, matrix)
        matrix = matrix_product(matrix, matrix)
        exponent >>= 1
    scaled = product[0][0] * n + product[0][1]
    denominator = d**K
    p = Fraction(denominator - scaled, 2 * denominator)
    assert 0 <= p <= 1
    return p


def recorded_binomial_hits(rng, p, shots):
    if p in (0, 1):
        return shots * int(p)
    numerator, denominator = p.numerator, p.denominator
    bits = (denominator - 1).bit_length()
    successes = 0
    for _ in range(shots):
        word = rng.getrandbits(bits)
        while word >= denominator:
            word = rng.getrandbits(bits)
        successes += word < numerator
    return successes


def branch_selection(prior, K, ratio, Kcap, search_events):
    left, right = prior
    proposed = min(Kcap, math.floor(Fraction(1, 2) / (right - left)))
    proposed -= proposed % 2 == 0
    while proposed >= ratio * K:
        if search_events >= 100000:
            return None, None, search_events
        search_events += 1
        lower, upper = proposed * left, proposed * right
        quadrant = math.floor(2 * lower)
        if upper <= Fraction(quadrant + 1, 2):
            assert Fraction(quadrant, 2) <= lower <= upper <= Fraction(quadrant + 1, 2)
            return proposed, quadrant, search_events
        proposed -= 2
    return None, None, search_events


def audit_attempt(saved, setting_index, law_index, Kcap):
    family = "original-IQAE-adapter" if setting_index < 4 else "modified-IQAE-adapter"
    first_shots = (16, 32, 64, 128)[setting_index % 4]
    setting = dict(family=family, first_batch_shots=first_shots)
    ratio = 2 if setting_index < 4 else 3
    truth = Fraction(1, 8) if law_index == 0 else Fraction(1, 4)
    seed = 20261002 + 2 * setting_index + law_index
    assert saved["setting_index"] == setting_index and saved["law_index"] == law_index
    assert saved["setting"] == setting and saved["seed"] == seed
    assert exact(saved["law"]["amplitude_exact"]) == truth
    assert exact(saved["law"]["mean_Y_dollars_exact"]) == 64 * truth
    assert saved["law"]["Y_dollars"] == [0, 16 if law_index == 0 else 32]
    assert saved["law"]["probabilities_exact"] == [[1, 2], [1, 2]]
    assert saved["observation_model"] == "exact-binomial rational Grover toy"
    transcript, rng = saved["transcript"], random.Random(seed)
    theta = (Fraction(0), Fraction(1, 2))
    K, quadrant, round_number, look = 1, 0, 1, 1
    pair_count, Q, shots_total, cursor, search_events = 0, 0, 0, 0, 0
    round_failures, round_powers, look_failures, independent_steps = [], [], [], []
    outcome, reason = "censored", "round-cap"
    amplitude = None
    while round_number <= 20:
        round_delta = ALPHA / 20 if ratio == 2 else Fraction(2, 3) * ALPHA * K / Kcap
        if look == 1:
            round_failures.append(round_delta)
            round_powers.append(K)
        batch_shots = first_shots * (1 << (look - 1))
        power = (K - 1) // 2
        # Prospective guard: no stored observation may exist after an overcap
        # batch is proposed. Even an unacquired round allocation is retained.
        if pair_count + batch_shots * (power + 1) > PAID_CAP:
            reason = "paid-source-pair-cap-before-acquisition"
            break
        assert cursor < len(transcript)
        batch = transcript[cursor]
        for name, expected in dict(
            round=round_number, look=look, K=K, power=power, quadrant=quadrant, shots=batch_shots
        ).items():
            assert batch[name] == expected, (setting_index, law_index, cursor, name)
        assert 1 <= look <= 8 and K % 2 == 1 and K <= Kcap
        assert Fraction(quadrant, 2) <= K * theta[0] <= K * theta[1] <= Fraction(quadrant + 1, 2)
        delta = round_delta / (look * (look + 1))
        assert exact(batch["failure_exact"]) == delta
        look_failures.append(delta)
        assert type(batch["hits"]) is int and 0 <= batch["hits"] <= batch_shots
        p = exact_toy_probability(truth, K)
        assert recorded_binomial_hits(rng, p, batch_shots) == batch["hits"]
        raw_radius = bounds(mp.iv.sqrt(mp.iv.log(2 / iv(delta)) / (2 * batch_shots)))[1]
        radius = Fraction(math.ceil(raw_radius * (1 << 64)), 1 << 64)
        assert exact(batch["hoeffding_radius_upper_exact"]) == radius
        # A direct, separately evaluated tail exponent validates the two-sided
        # failure spending without a binomial or variance plug-in.
        assert bounds(2 * mp.iv.exp(-2 * batch_shots * iv(radius) ** 2))[1] <= delta
        empirical = Fraction(batch["hits"], batch_shots)
        pl, pu = max(Fraction(0), empirical - radius), min(Fraction(1), empirical + radius)
        if quadrant % 2:
            pl, pu = 1 - pu, 1 - pl
        lower = (Fraction(quadrant, 2) + inverse_interval(pl)[0]) / K
        upper = (Fraction(quadrant, 2) + inverse_interval(pu)[1]) / K
        theta = (max(theta[0], lower), min(theta[1], upper))
        assert [pair(v) for v in theta] == batch["theta_over_pi_interval_exact"]
        Q += power * batch_shots
        shots_total += batch_shots
        pair_count += (power + 1) * batch_shots
        independent_steps.append(
            dict(
                round=round_number,
                look=look,
                K=K,
                quadrant=quadrant,
                exact_toy_probability_binary_sha256=hashlib.sha256(
                    p.numerator.bit_length().to_bytes(8, "little")
                    + p.numerator.to_bytes((p.numerator.bit_length() + 7) // 8, "little")
                    + p.denominator.bit_length().to_bytes(8, "little")
                    + p.denominator.to_bytes((p.denominator.bit_length() + 7) // 8, "little")
                ).hexdigest(),
                exact_toy_probability_denominator_bits=p.denominator.bit_length(),
                fresh_batch_counts_reconciled=True,
                failure_exact=pair(delta),
                outward_radius_verified=True,
                correct_monotone_inverse_branch=True,
                original_paid_source_pairs_after_batch=pair_count,
            )
        )
        cursor += 1
        if theta[0] > theta[1]:
            reason = "inconsistent-confidence-intersection"
            break
        amplitude = (
            max(Fraction(0), probability(theta[0])[0]),
            min(Fraction(1), probability(theta[1])[1]),
        )
        if amplitude[1] - amplitude[0] <= 2 * EPSILON:
            outcome, reason = "delivered", "outward-amplitude-interval-within-tolerance"
            break
        if theta[0] == theta[1]:
            reason = "unresolved-outward-amplitude-rounding"
            break
        new_K, new_quadrant, search_events = branch_selection(theta, K, ratio, Kcap, search_events)
        if search_events >= 100000 and new_K is None:
            reason = "power-search-event-cap"
            break
        if new_K is None:
            look += 1
            if look > 8:
                reason = "look-cap"
                break
        else:
            assert new_K >= ratio * K
            K, quadrant, round_number, look = new_K, new_quadrant, round_number + 1, 1
    assert cursor == len(transcript) == saved["admitted_batches"]
    assert outcome == saved["status"] and reason == saved["stop_reason"]
    assert saved["admitted_rounds"] == len(round_failures)
    assert (
        saved["total_Q_calls"] == Q
        and saved["total_terminal_F_selector_clean_pairs"] == shots_total
    )
    assert saved["paid_source_pairs"] == pair_count == Q + shots_total <= PAID_CAP
    assert saved["power_search_events"] == search_events <= 100000
    assert saved["longest_single_shot_Q_chain"] == max((b["power"] for b in transcript), default=0)
    assert (
        exact(saved["failure_allocation_upper_exact"]) == sum(round_failures, Fraction(0)) <= ALPHA
    )
    assert sum(look_failures, Fraction(0)) <= sum(round_failures, Fraction(0))
    if ratio == 3:
        assert all(b >= 3 * a for a, b in zip(round_powers, round_powers[1:]))
        assert sum(round_powers) <= Fraction(3, 2) * Kcap
    else:
        assert len(round_powers) <= 20
    assert exact(saved["simultaneous_ideal_failure_upper_exact"]) == ALPHA
    assert (
        not saved["uniform_financial_delivery_within_budget_proved"]
        and not saved["censored_result_is_certified_estimate"]
    )
    assert not saved["paper_native_controller_reproduced"] and saved["quantum_circuit_jobs"] == 0
    if outcome == "delivered":
        charged = tuple(exact(v) for v in saved["amplitude_interval_exact"])
        assert charged[0] <= amplitude[0] <= amplitude[1] <= charged[1]
        assert charged[1] - charged[0] <= 2 * EPSILON
        assert charged[0] <= truth <= charged[1] and saved["toy_ground_truth_in_delivered_interval"]
        assert saved["dollar_interval_exact"] == [pair(64 * v) for v in charged]
        assert exact(saved["delivered_midpoint_amplitude_error_at_most_exact"]) == EPSILON
        assert abs(sum(charged) / 2 - truth) <= EPSILON
    else:
        assert (
            saved["amplitude_interval_exact"]
            is saved["dollar_interval_exact"]
            is saved["delivered_midpoint_amplitude_error_at_most_exact"]
            is saved["toy_ground_truth_in_delivered_interval"]
            is None
        )
    return dict(
        passed=True,
        setting_index=setting_index,
        law_index=law_index,
        status=outcome,
        stop_reason=reason,
        recorded_batches_reconciled=cursor,
        exact_toy_probabilities_and_recorded_rng_counts_verified=True,
        monotone_branches_and_adaptive_transitions_verified=True,
        total_Q_calls=Q,
        terminal_clean_pairs=shots_total,
        paid_source_pairs=pair_count,
        admitted_failure_spending_upper_exact=pair(sum(round_failures, Fraction(0))),
        actual_fresh_look_spending_exact=pair(sum(look_failures, Fraction(0))),
        unconditional_probability_delivered_and_wrong_upper_exact=pair(ALPHA),
        conditional_coverage_given_delivery_claimed=False,
        uniform_financial_delivery_claimed=False,
        steps=independent_steps,
    )


def audit_cost(saved, wrapper, baseline):
    cost = saved["conditional_original_financial_cost"]
    Q, shots = saved["total_Q_calls"], saved["total_terminal_F_selector_clean_pairs"]
    selector = wrapper["selector_costs"]
    terminal_T = (
        wrapper["financial_resources"]["t_count"]
        + selector["forward"]["t_count"]
        + selector["inverse"]["t_count"]
    )
    terminal_depth = (
        wrapper["financial_resources"]["t_depth"]
        + selector["forward"]["t_depth"]
        + selector["inverse"]["t_depth"]
    )
    random_bits = len(wrapper["random_wires"])
    expected = dict(
        financial_forwards=Q + shots,
        financial_literal_inverses=Q + shots,
        selector_forwards=Q + shots,
        selector_literal_inverses=Q + shots,
        original_pinned_active_Grover_reflections=Q,
        terminal_flag_measurements=shots,
        uniform_preparation_H=shots * random_bits,
        control_X_preparations=shots,
        control_X_cleanup=shots,
        required_random_reset_bits=shots * random_bits,
        adaptive_feedback_updates=saved["admitted_batches"],
        logical_qubits=wrapper["resources"]["logical_qubits"],
        logical_T_count=Q * wrapper["resources"]["t_count"] + shots * terminal_T,
        logical_serial_unitary_T_depth=Q * wrapper["resources"]["t_depth"] + shots * terminal_depth,
    )
    for name, value in expected.items():
        assert cost[name] == value, name
    assert cost["conditional_on_same_original_ideal_digital_source"]
    assert cost["source_and_selector_clean_after_terminal_literal_inverse"]
    assert cost["total_physical_readout_reset_feedback_seconds"] is None
    assert cost["finance_measurements_or_gate_replays_executed"] == 0
    assert (
        not cost["actual_financial_controller_cost_measured"]
        and not cost["full_G2_or_physical_certificate"]
    )
    lower = (
        saved["status"] == "delivered"
        and expected["logical_T_count"] < baseline["full_T_count"]
        and expected["logical_serial_unitary_T_depth"] < baseline["full_T_depth"]
    )
    assert cost["toy_delivered_and_conditional_logical_T_work_below_canonical"] == lower
    return dict(
        passed=True,
        paid_invocation_counts=expected,
        terminal_financial_literal_inverse_T_charged=True,
        terminal_selector_literal_inverse_T_charged=True,
        original_active_reflections_and_final_control_Z_retained=True,
        initial_uniform_and_control_preparations_charged=True,
        measured_terminal_flag_followed_by_inverse_cleanup=True,
        conditioned_random_register_reset_required=True,
        coherent_random_state_not_assumed_restored_by_flagmeasurement=True,
        pinned_active_source_implementation_bound_to_prior_native_array_audit=True,
        new_financial_cost_measurement=False,
        observed_toy_lower_conditional_T_work=lower,
        full_Clifford_routing_reset_feedback_latency_seconds=None,
        physical_speedup_claim=False,
    )


def xml_count(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    names = [
        (case.get("classname"), case.get("name"))
        for suite in suites
        for case in suite.findall("testcase")
    ]
    assert len(names) == len(set(names)) == sum(int(suite.get("tests", 0)) for suite in suites)
    assert all(
        int(suite.get(field, 0)) == 0
        for suite in suites
        for field in ("failures", "errors", "skipped")
    )
    return len(names)


def prepare(producer, output):
    producer, output = Path(producer).resolve(), Path(output).resolve()
    producer.relative_to(PROGRAM)
    output.relative_to(PROGRAM)
    assert read(producer / "summary.json")["passed"] and not output.exists()
    frozen = {}
    for directory in (
        producer,
        PROGRAM / "E02_financial_audit_run001",
        PROGRAM / "E02_IQFT_audit_run001",
    ):
        manifest = read(directory / "manifest.json")
        frozen.update(manifest["files"])
        frozen.update(manifest["frozen_inputs"])
        frozen[relative(directory / "manifest.json")] = sha(directory / "manifest.json")
    own = Path(__file__).resolve()
    frozen[relative(own)] = sha(own)
    verify(frozen)
    output.mkdir()
    shutil.copy2(own, output / "executed_audit_finite_iqae_controller.py")
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_independent_audit=True,
            producer=relative(producer),
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            interval_precision=140,
            independent_pi="Rational 4*(atan(1/2)+atan(1/3)), 240 terms each",
            exact_toy_probability_method="Binary powering of an integer 2 by 2 scaled Chebyshev recurrence, independent of the producer's recursive doubling",
            observed_transcripts="Reconcile all 16 saved histories and fixed-seed RNG counts; no fresh candidate attempts",
            prospective_constraints=dict(
                settings=8,
                laws=2,
                alpha_exact=pair(ALPHA),
                amplitude_error_exact=pair(EPSILON),
                paid_source_pairs_cap=PAID_CAP,
                round_cap=20,
                fresh_look_cap=8,
                search_event_cap=100000,
            ),
            check_scope="Conditional fresh-batch Hoeffding bounds, pathwise round/look spending, 80-step monotone inverses, all original adaptive decisions and budget guards, and terminal measurement/inverse cleanup/preparation/reset costs bound to audited native arrays; preserve censoring and null physical durations",
            confidence_theorem=(
                "Assume that, conditional on the past, each admitted batch is a fresh collection of independent Bernoulli observations with probability sin^2(K*theta). "
                "The predictable batch allocation delta gives a two-sided Hoeffding error at most delta. "
                "The union bound followed by expectation bounds any admitted failure by E[sum delta] <= alpha: the original adapter admits at most 20 rounds, "
                "and the modified adapter's round K values grow by at least three and remain <= Kcap, so their sum is <= 3*Kcap/2. "
                "The look weights 1/(l*(l+1)) telescope to at most one within every round. "
                "Before the first failed batch, the true angle belongs to the previous interval, which lies within the selected monotone half-period. "
                "The outward inverse and intersection therefore retain the true angle. "
                "Consequently P(delivered and incorrect) <= alpha. No conditional-on-delivery coverage, delivery-probability, physical noise or financial uniform-delivery theorem follows. "
                "The saved seeded pseudorandom toy records demonstrate implementation behavior; the confidence theorem concerns the stated ideal fresh-observation model."
            ),
            unconditional_delivered_and_incorrect_probability_bound=True,
            conditional_coverage_given_delivery_not_claimed=True,
            uniform_financial_delivery_not_claimed=True,
            new_financial_observations=0,
            new_quantum_jobs=0,
            new_controller_candidate_attempts=0,
            original_receipts_immutable=True,
        ),
    )
    print("E04 independent adaptive-controller audit frozen", flush=True)


def run(output):
    global PI
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    mp.iv.dps = 140
    pi_lo, pi_hi, PI = independent_pi()
    assert math.floor(pi_lo / (4 * EPSILON)) == math.floor(pi_hi / (4 * EPSILON))
    Kcap = math.floor(pi_lo / (4 * EPSILON))
    assert Kcap == 11170
    producer = ROOT / protocol["producer"]
    summary, prospective = read(producer / "summary.json"), read(producer / "protocol.json")
    assert (
        summary["passed"]
        and summary["frozen_inputs_unchanged"]
        and summary["historical_receipts_unchanged"]
    )
    assert xml_count(producer / "tests.xml") == prospective["declared_tests"] == 18
    assert prospective["before_meaningful_tests_and_toy_observations"]
    assert prospective["settings"] == [
        dict(family=f, first_batch_shots=n)
        for f in ("original-IQAE-adapter", "modified-IQAE-adapter")
        for n in (16, 32, 64, 128)
    ]
    assert prospective["total_controller_attempts"] == summary["controller_attempts"] == 16
    assert prospective["replicates_per_setting_law"] == 1
    assert prospective["max_Q_plus_terminal_clean_pairs_per_attempt"] == PAID_CAP
    assert (
        exact(prospective["ideal_failure_exact"]) == ALPHA
        and exact(prospective["amplitude_error_exact"]) == EPSILON
    )
    assert exact(prospective["error_dollars_exact"]) == 64 * EPSILON
    assert (
        prospective["financial_samples_or_gate_replays"] == prospective["quantum_circuit_jobs"] == 0
    )
    assert (
        not prospective["uniform_financial_delivery_within_budget_proved"]
        and not prospective["paper_native_controller_or_query_bound_automatically_transferred"]
    )
    for dependency in prospective["executed_dependencies"]:
        assert (
            sha(ROOT / dependency["original"])
            == sha(producer / dependency["snapshot"])
            == dependency["sha256"]
        )
    # Validate the actual guard-before-observation ordering and independence of
    # control decisions from hidden toytruth in the frozen implementation AST.
    source = (producer / "executed_code/finite_iqae_controller.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    controller = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "controller"
    )
    text = ast.unparse(controller)
    assert text.index("paid + shots * (power + 1)") < text.index("hits = observe(power, shots)")
    assert not any(
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "observe"
        for node in ast.walk(controller)
    )
    cost_binding = read(producer / "source_cost_binding.json")
    wrapper_path, baseline_path = (
        Path(cost_binding["wrapper"]["path"]),
        Path(cost_binding["canonical_synthesized_ledger"]["path"]),
    )
    assert wrapper_path.resolve() == (PROGRAM / "E02_financial_run002/B4x12/iterate.json").resolve()
    assert (
        baseline_path.resolve()
        == (PROGRAM / "E02_IQFT_run001/B4x12/synthesized_estimator_ledger.json").resolve()
    )
    assert (
        sha(wrapper_path) == cost_binding["wrapper"]["sha256"]
        and sha(baseline_path) == cost_binding["canonical_synthesized_ledger"]["sha256"]
    )
    wrapper, baseline = read(wrapper_path), read(baseline_path)
    assert cost_binding["Q_resources"] == wrapper["resources"]
    assert cost_binding["terminal_financial_both_directions"] == wrapper["financial_resources"]
    assert cost_binding["terminal_selector_directions"] == wrapper["selector_costs"]
    assert cost_binding["uniform_random_bits"] == len(wrapper["random_wires"]) == 1966
    assert (
        cost_binding["source_pinned_active_control"]
        and cost_binding["terminal_flag_measurement_then_literal_inverse"]
    )
    assert read(PROGRAM / "E02_financial_audit_run001/summary.json")["passed"]
    assert read(PROGRAM / "E02_IQFT_audit_run001/summary.json")["passed"]
    assert (
        wrapper["resources"]["t_count"] == 520750804 and wrapper["resources"]["t_depth"] == 571034
    )
    # The finite source has literal Toffoli arithmetic and the original exact
    # controlled marker/reflection. RetargetedIQFT is only the comparisonrow.
    reports = []
    for setting in range(8):
        for law in range(2):
            filename = "setting%02d_law%d.json" % (setting, law)
            saved = read(producer / filename)
            transcript = audit_attempt(saved, setting, law, Kcap)
            cost = audit_cost(saved, wrapper, baseline)
            row = summary["rows"][2 * setting + law]
            assert (
                row["file"] == filename
                and row["status"] == saved["status"]
                and row["stop_reason"] == saved["stop_reason"]
            )
            for field, expected in dict(
                batches=saved["admitted_batches"],
                total_Q_calls=saved["total_Q_calls"],
                terminal_clean_pairs=saved["total_terminal_F_selector_clean_pairs"],
                paid_source_pairs=saved["paid_source_pairs"],
                toy_ground_truth_in_delivered_interval=saved[
                    "toy_ground_truth_in_delivered_interval"
                ],
                conditional_logical_T_count=saved["conditional_original_financial_cost"][
                    "logical_T_count"
                ],
                conditional_logical_T_depth=saved["conditional_original_financial_cost"][
                    "logical_serial_unitary_T_depth"
                ],
                toy_delivered_with_lower_conditional_logical_work=cost[
                    "observed_toy_lower_conditional_T_work"
                ],
            ).items():
                assert row[field] == expected
            report = dict(transcript=transcript, paid_cost=cost)
            save(output / (filename[:-5] + "_audit.json"), report)
            reports.append(report)
            print(
                filename, saved["status"], "confidence/branch/exactcounts/paidcost PASS", flush=True
            )
    delivered = sum(r["transcript"]["status"] == "delivered" for r in reports)
    censored = 16 - delivered
    assert delivered == summary["delivered"] == 15 and censored == summary["censored"] == 1
    assert reports[9]["transcript"]["status"] == "censored"
    assert not summary["uniform_financial_delivery_within_budget_proved"]
    verify(protocol["frozen_inputs"])
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            producer_distinct_tests_reconciled=18,
            saved_controller_attempts_audited=16,
            fixed_settings=8,
            fixed_toy_laws=2,
            delivered=delivered,
            censored=censored,
            recorded_batches_audited=sum(
                r["transcript"]["recorded_batches_reconciled"] for r in reports
            ),
            independent_integer_Grover_probability_checks=True,
            original_recorded_rng_transcripts_reconciled=True,
            adaptive_past_only_decisions_verified=True,
            simultaneous_conditional_fresh_batch_spending_verified=True,
            unconditional_probability_delivered_and_incorrect_upper_exact=pair(ALPHA),
            conditional_coverage_given_delivery_claimed=False,
            terminal_marking_measurement_and_inverse_cleanup_paid=True,
            all_initial_preparations_and_random_reset_bits_counted=True,
            original_active_control_marker_reflection_sign_retained=True,
            censored_price_interval_null_preserved=True,
            price_error_for_delivered_ideal_intervals_exact=pair(64 * EPSILON),
            uniform_financial_delivery_proved=False,
            actual_financial_controller_delivery_or_cost_measured=False,
            censored_outcome_counted_as_success=False,
            paper_native_controller_or_query_bound_transferred=False,
            new_controller_candidate_attempts=0,
            new_financial_observations=0,
            new_financial_gate_replays=0,
            new_quantum_jobs=0,
            physical_readout_reset_feedback_seconds=None,
            full_continuous_price_certificate=False,
            quantum_advantage_claim=False,
        ),
    )
    finish_manifest(output)
    print("E04 independent finite controller audit PASS", flush=True)


def finish_manifest(output):
    save(
        output / "manifest.json",
        dict(
            files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            frozen_inputs=read(output / "protocol.json")["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--producer", type=Path, default=PROGRAM / "E04_controller_run001")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.producer, args.output)
    else:
        try:
            run(args.output)
        except Exception as failure:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    local_only=True,
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    new_controller_candidate_attempts=0,
                    new_financial_observations=0,
                    new_quantum_jobs=0,
                    uniform_financial_delivery_proved=False,
                ),
            )
            finish_manifest(output)
            raise
