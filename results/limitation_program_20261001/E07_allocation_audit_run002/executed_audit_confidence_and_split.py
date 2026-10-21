"""Independent RMSE confidence conversion and fixed error-allocation audit.

No producer functions are imported. Derive the two elementary confidence
conversions and six declared canonical schedules, then reconcile their existing
terminal IQFT tokens and paid primitive counts. No estimates or gates are run.
"""

from __future__ import annotations

# Receipt explanations are deliberately readable prose.
# ruff: noqa: E501

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path
import shutil
import sys
import traceback
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
CONVERSION = PROGRAM / "E21_conversion_run001"
GRID = PROGRAM / "E24_grid_run001"
SHARES = (Fraction(1, 4), Fraction(9, 20), Fraction(13, 20))
ALPHA = Fraction(3, 1000)
ERROR = Fraction(9, 2000)
OBLIGATIONS = [
    "finite_input_law_and_joint_Box_Muller",
    "clipped_log_tail",
    "native_arithmetic_and_polynomial",
    "physical_execution",
]


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
    value = Fraction(value)
    return [value.numerator, value.denominator]


def exact(value):
    result = Fraction(*value)
    assert pair(result) == value
    return result


def verify(files):
    for name, digest in files.items():
        assert sha(ROOT / name) == digest, ("frozen dependency changed", name)


def independent_pi():
    # atan(1/2)+atan(1/3)=pi/4 by tangent addition and positive angles.
    assert (Fraction(1, 2) + Fraction(1, 3)) / (1 - Fraction(1, 6)) == 1
    intervals = []
    for denominator in (2, 3):
        total = Fraction(0)
        for j in range(240):
            total += Fraction((-1) ** j, (2 * j + 1) * denominator ** (2 * j + 1))
        intervals.append((total, total + Fraction(1, 481 * denominator**481)))
    lo, hi = (4 * sum(row[k] for row in intervals) for k in (0, 1))
    assert hi - lo < Fraction(1, 10**140)
    return lo, hi


def majority_tail(repetitions, probability):
    assert repetitions > 0 and repetitions % 2 == 1
    return sum(
        (
            Fraction(comb(repetitions, k)) * probability**k * (1 - probability) ** (repetitions - k)
            for k in range(repetitions // 2 + 1, repetitions + 1)
        ),
        Fraction(0),
    )


def xml_count(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    cases = [
        (case.get("classname"), case.get("name"))
        for suite in suites
        for case in suite.findall("testcase")
    ]
    assert len(cases) == len(set(cases)) == sum(int(suite.get("tests", 0)) for suite in suites)
    assert all(
        int(suite.get(field, 0)) == 0
        for suite in suites
        for field in ("failures", "errors", "skipped")
    )
    return len(cases)


def audit_conversions():
    protocol, result, summary = (
        read(CONVERSION / name) for name in ("protocol.json", "certificate.json", "summary.json")
    )
    assert protocol["before_tests_and_two_conversions"]
    assert exact(protocol["statistical_error_dollars_exact"]) == ERROR
    assert exact(protocol["failure_exact"]) == ALPHA
    assert protocol["families"] == ["one-run squared-error Markov", "independent odd median"]
    assert protocol["finite_odd_repetition_cap"] == 101
    assert (
        protocol["new_financial_prices_or_gates"] == 0
        and not protocol["RMSE_construction_or_query_cost_provided"]
    )
    assert xml_count(CONVERSION / "tests.xml") == 8
    assert (
        exact(result["statistical_error_dollars_exact"]) == ERROR
        and exact(result["failure_allowance_exact"]) == ALPHA
    )
    one, median = result["one_run"], result["independent_median"]
    squared_threshold = ERROR**2 * ALPHA
    assert (
        exact(one["RMSE_target_squared_dollars_exact"])
        == squared_threshold
        == Fraction(243, 4000000000)
    )
    left, right = map(exact, one["RMSE_target_dollars_interval_exact"])
    assert 0 <= left**2 <= squared_threshold <= right**2 and right - left < Fraction(1, 1 << 220)
    assert exact(one["safe_rational_RMSE_target_dollars_exact"]) == left
    assert (
        one["repetitions"] == 1
        and not one["requires_unbiasedness"]
        and one["quantum_query_or_runtime_cost"] is None
    )
    tails = [(r, majority_tail(r, Fraction(1, 4))) for r in range(1, 102, 2)]
    repetitions, failure = next((r, bound) for r, bound in tails if bound <= ALPHA)
    assert repetitions == median["repetitions"] == 27
    assert majority_tail(25, Fraction(1, 4)) > ALPHA >= failure
    assert exact(median["per_run_RMSE_target_dollars_exact"]) == ERROR / 2
    assert exact(median["per_run_bad_probability_upper_exact"]) == Fraction(1, 4)
    assert exact(median["certified_failure_upper_exact"]) == failure
    assert median["independent_fresh_runs_required"]
    assert median["source_inverse_preparation_readout_reset_multiplicity"] == 27
    assert median["complete_quantum_cost"] is None
    assert (
        not result["construction_with_proved_RMSE_cost_supplied"]
        and not result["cheaper_complete_conversion_selected"]
    )
    assert (
        result["RMSE_equals_dollar_allowance_is_not_a_failure_certificate"]
        and not result["original_continuous_price_bias_covered"]
    )
    assert (
        summary["passed"]
        and summary["conversion_families"] == 2
        and summary["median_repetitions"] == 27
    )
    assert exact(summary["median_failure_upper_exact"]) == failure
    assert (
        summary["actual_E20_finite_RMSE_constructions_supplied"] == 0
        and summary["new_financial_prices_or_gates"] == 0
    )
    assert (
        not summary["complete_cost_winner_selected"]
        and not summary["full_price_confidence_certified"]
    )
    return dict(
        passed=True,
        producer_distinct_tests_reconciled=8,
        squared_Markov_RMSE_threshold_exact=pair(squared_threshold),
        safe_one_run_RMSE_exact=pair(left),
        independent_median_per_run_RMSE_exact=pair(ERROR / 2),
        minimal_odd_repetitions=27,
        median_failure_upper_exact=pair(failure),
        preceding_odd_failure_exact=pair(majority_tail(25, Fraction(1, 4))),
        preparation_inverse_readout_reset_paid_multiplicity=27,
        proof=(
            "Squared-error Markov applies to a proved RMSE including bias. With per-run RMSE <= e/2, each unconditional bad probability is <= 1/4. For independent fresh runs, an incorrect odd median implies at least (r+1)/2 bad runs, dominated by Binomial(r,1/4). No unbiasedness or conditional-on-delivery theorem is needed."
        ),
        finite_RMSE_construction_supplied=False,
        complete_query_runtime_cost=None,
        complete_conversion_winner=False,
        continuous_price_bias_certified=False,
    )


def audit_schedule(schedule, allowance, pi):
    pi_lo, pi_hi = pi
    source_lo, source_hi = map(exact, schedule["pi_enclosure_exact"])
    # Containment in a tighter independently proved interval validates the
    # saved enclosure without importing its Machin implementation.
    assert source_lo <= pi_lo <= pi_hi <= source_hi
    M = 1
    while 64 * (pi_hi / M + pi_hi**2 / M**2) > allowance:
        M *= 2
    assert 64 * (pi_lo / (M // 2) + pi_lo**2 / (M // 2) ** 2) > allowance
    elementary_lo, elementary_hi = 1 - 8 / pi_lo**2, 1 - 8 / pi_hi**2
    ceiling_lo = (elementary_lo * (1 << 40)).__ceil__()
    ceiling_hi = (elementary_hi * (1 << 40)).__ceil__()
    assert ceiling_lo == ceiling_hi
    bad = Fraction(ceiling_hi, 1 << 40)
    repetitions = next(r for r in range(1, 102, 2) if majority_tail(r, bad) <= ALPHA)
    assert repetitions == 15
    expected = dict(
        normalization_span_dollars=64,
        M=M,
        qpe_bits=M.bit_length() - 1,
        repetitions=15,
        controlled_grover_calls=15 * (M - 1),
        longest_single_shot_grover_chain=M - 1,
        fresh_preparations=15,
        adaptive_quantum_rounds=0,
        median_classical_comparisons_upper=105,
        output_already_discounted=True,
        further_discount_factor=[1, 1],
        synthesis_and_physical_failure_included=False,
    )
    for name, value in expected.items():
        assert schedule[name] == value, name
    assert exact(schedule["statistical_error_dollars_exact"]) == allowance
    assert exact(schedule["requested_failure_exact"]) == ALPHA
    assert exact(schedule["amplitude_tolerance_exact"]) == allowance / 64
    assert exact(schedule["elementary_failure_upper_exact"]) == bad
    assert exact(schedule["ideal_failure_upper_exact"]) == majority_tail(15, bad) <= ALPHA
    ideal_error = 64 * (source_hi / M + source_hi**2 / M**2)
    assert exact(schedule["ideal_error_upper_exact"]) == ideal_error
    assert ideal_error + Fraction(2, 1 << 40) <= allowance
    return expected


def audit_operations(actual, controls, rotations):
    cursor, counts = 0, Counter()

    def consume(gate, wires):
        nonlocal cursor
        assert actual[cursor] == dict(gate=gate, wires=wires), cursor
        assert len(set(wires)) == len(wires) and set(wires) <= set(controls)
        counts[gate] += 1
        cursor += 1

    def rotation(wire, gap, positive):
        if gap == 1:
            consume("t" if positive else "tdg", [wire])
        else:
            tokens = rotations["pi_1_%d" % (1 << (gap + 1))]["matrix_product_gates"]
            for token in tokens[::-1] if positive else tokens:
                if token != "W":
                    consume(
                        {
                            "H": "h",
                            "X": "x",
                            "S": "s" if positive else "sdg",
                            "T": "t" if positive else "tdg",
                        }[token],
                        [wire],
                    )

    for position in range(len(controls) // 2):
        consume("swap", [controls[position], controls[-1 - position]])
    for target_index, target in enumerate(controls):
        for control_index in range(target_index):
            control, gap = controls[control_index], target_index - control_index
            rotation(control, gap, False)
            rotation(target, gap, False)
            consume("cx", [control, target])
            rotation(target, gap, True)
            consume("cx", [control, target])
        consume("h", [target])
    assert cursor == len(actual)
    return counts


def audit_grid_row(case, share, saved_summary, rotations, pi):
    folder = GRID / case / (str(share.numerator) + "_of_" + str(share.denominator))
    schedule, row = read(folder / "schedule.json"), read(folder / "digital_estimator_row.json")
    wrapper = read(PROGRAM / "E02_financial_run002" / case / "iterate.json")
    complete = read(PROGRAM / "E07_complete_run001" / (case + "_complete_price_ledger.json"))
    allowance = share / 100
    schedule_expected = audit_schedule(schedule, allowance, pi)
    bits, Q, repetitions = (
        schedule_expected["qpe_bits"],
        schedule_expected["controlled_grover_calls"],
        15,
    )
    unit, n_random = wrapper["resources"], len(wrapper["random_wires"])
    assert row["binding"] == wrapper["binding"] and row["source_iterate_resources"] == unit
    assert row["case"] == case and row["wrapper_format"] == wrapper["format"]
    assert row["probability_law"] == wrapper["probability_law"]
    assert row["qpe_register_wires"] == wrapper["allowed_qpe_control_wires"][:bits]
    controls = row["qpe_register_wires"]
    assert len(set(controls)) == len(controls) == bits
    assert not set(controls).intersection(wrapper["random_wires"] + [wrapper["selector_flag_wire"]])
    assert row["price_output_already_discounted"] and not row["second_discount_applied"]
    assert not row["binding"]["continuous_financial_error_certified"]
    assert row["binding"]["word_width"] == 72 and row["binding"]["fraction_bits"] == 40
    assert row["binding"]["selector_bits"] == 46 and row["normalization_span_dollars"] == 64
    for name, digest in row["binding"]["hashes"].items():
        assert sha(row["binding"]["paths"][name]) == digest
    cp, exact_cp = repetitions * bits * (bits - 1) // 2, repetitions * (bits - 1)
    arbitrary = 3 * (cp - exact_cp)
    expected = dict(
        fresh_preparations=15,
        financial_forwards=Q,
        financial_literal_inverses=Q,
        source_graph_directions=2 * Q,
        selector_forwards=Q,
        selector_literal_inverses=Q,
        controlled_predicate_CZ=Q,
        controlled_signed_reflections=Q,
        uniform_preparation_H=15 * n_random,
        qpe_preparation_H=15 * bits,
        iqft_H=15 * bits,
        iqft_controlled_phase_gates=cp,
        iqft_exact_CS_gates=exact_cp,
        iqft_exact_CS_T_count=3 * exact_cp,
        iqft_controlled_phase_CX=2 * cp,
        iqft_swaps_CX=45 * (bits // 2),
        iqft_arbitrary_Rz_rotations=arbitrary,
        measured_QPE_bits=15 * bits,
        source_and_selector_reset_bits=15 * n_random,
        qpe_reset_bits=15 * bits,
        adaptive_quantum_rounds=0,
        serial_shots=15,
        longest_single_shot_grover_chain=schedule["M"] - 1,
        longest_single_shot_known_T_depth=(schedule["M"] - 1) * unit["t_depth"] + 3 * (bits - 1),
        complete_known_T_count_excluding_arbitrary_rotation_synthesis=Q * unit["t_count"]
        + 3 * exact_cp,
        serial_known_T_depth_excluding_arbitrary_rotation_synthesis=Q * unit["t_depth"]
        + 3 * exact_cp,
        complete_known_clifford_CX=Q * unit["clifford_cx"] + 2 * cp + 45 * (bits // 2),
        complete_known_clifford_H=Q * unit["clifford_h"] + 15 * n_random + 30 * bits,
        complete_known_clifford_CZ=Q * unit["clifford_cz"],
        complete_known_clifford_Z=Q * unit["clifford_z"],
        complete_known_X=Q * unit["x"],
        financial_selector_reflection_T_depth=Q * unit["t_depth"],
        logical_qubits=unit["logical_qubits"],
    )
    for name, value in expected.items():
        assert row[name] == value, (case, share, name)
    assert exact(row["statistical_error_dollars_exact"]) == allowance
    assert exact(row["ideal_failure_upper_exact"]) == exact(schedule["ideal_failure_upper_exact"])
    assert exact(row["classical_readout_error_allowance"]) == Fraction(2, 1 << 40)
    assert exact(row["ideal_error_plus_readout_upper_exact"]) == exact(
        schedule["ideal_error_upper_exact"]
    ) + Fraction(2, 1 << 40)
    assert exact(row["required_each_rotation_operator_error"]) == Fraction(1, 2000 * arbitrary)
    assert exact(row["synthesis_observation_failure_allowance"]) == Fraction(1, 1000)
    required = ["pi_1_%d" % (1 << (gap + 1)) for gap in range(2, bits)]
    missing = [key for key in required if key not in rotations]
    assert missing == (["pi_1_131072"] if bits == 17 else [])
    costs = None
    if missing:
        assert not (folder / "iqft_operations.json").exists()
        assert row["synthesis_certificate"] is row["full_T_count"] is row["full_T_depth"] is None
    else:
        actual = read(folder / "iqft_operations.json")
        counts = audit_operations(actual, controls, rotations)
        assert row["iqft_per_shot_physical_gate_counts"] == dict(counts)
        usage = {"pi_1_%d" % (1 << (gap + 1)): 45 * (bits - gap) for gap in range(2, bits)}
        assert row["synthesized_rotation_usage"] == usage and sum(usage.values()) == arbitrary
        synth_T = sum(rotations[key]["t_count"] * count for key, count in usage.items())
        synth_C = sum(rotations[key]["clifford_count"] * count for key, count in usage.items())
        assert (
            row["synthesized_single_qubit_T_count"] == synth_T
            and row["synthesized_single_qubit_clifford_count"] == synth_C
        )
        actual_iqft_T = 15 * (counts["t"] + counts["tdg"])
        assert actual_iqft_T == 3 * exact_cp + synth_T
        assert row["full_T_count"] == Q * unit["t_count"] + actual_iqft_T
        assert row["full_T_depth"] == Q * unit["t_depth"] + actual_iqft_T
        actual_CT = Q * unit["clifford_t_depth"] + 15 * (2 + len(actual) + 2 * counts["swap"])
        assert row["full_known_clifford_t_depth_upper"] == actual_CT
        total_error = 2 * sum(
            (
                exact(rotations[key]["operator_error_upper_exact"]) * count
                for key, count in usage.items()
            ),
            Fraction(0),
        )
        assert (
            exact(row["synthesis_total_observation_perturbation_upper_exact"])
            == total_error
            <= Fraction(1, 1000)
        )
        assert row["ideal_digital_estimator_with_synthesis_certificate"]
        assert row["synthesis_certificate"] == relative(folder / "iqft_operations.json")
        costs = dict(
            full_T_count=row["full_T_count"],
            full_serial_T_depth=row["full_T_depth"],
            full_serial_clifford_T_depth_upper=actual_CT,
            complete_primitive_counts=dict(
                t=row["full_T_count"],
                cx=Q * unit["clifford_cx"] + 15 * (counts["cx"] + 3 * counts["swap"]),
                h=Q * unit["clifford_h"] + 15 * n_random + 15 * bits + 15 * counts["h"],
                s_or_sdg=15 * (counts["s"] + counts["sdg"]),
                x=Q * unit["x"] + 15 * counts["x"],
                cz=Q * unit["clifford_cz"],
                z=Q * unit["clifford_z"],
            ),
            actual_saved_IQFT_tokens=len(actual),
            per_shot_gate_counts=dict(counts),
        )
    for field in ("total_readout_or_reset_seconds", "full_physical_runtime_seconds"):
        assert row[field] is None
    if not missing:
        assert row["physical_runtime_seconds"] is None
    assert (
        not row["full_continuous_price_certificate"]
        and not row["full_physical_execution_certificate"]
        and row["G2_to_G5"] == "open"
    )
    assert row["ideal_digital_mean_error_confidence_certificate"]
    assert (
        complete["assessment"]["open_obligations"] == OBLIGATIONS
        and not complete["assessment"]["complete_price_certified"]
    )
    assert (
        exact(
            next(
                term["bound"]
                for term in complete["dollar_terms"]
                if term["name"] == "statistical_digital_mean"
            )
        )
        == ERROR
    )
    base_T = read(PROGRAM / "E02_IQFT_run001" / case / "synthesized_estimator_ledger.json")[
        "full_T_count"
    ]
    expected_summary = dict(
        case=case,
        statistical_share_exact=pair(share),
        statistical_allowance_dollars_exact=pair(allowance),
        remaining_deterministic_headroom_dollars_exact=pair(Fraction(1, 100) - allowance),
        controlled_G_calls=Q,
        qpe_bits=bits,
        missing_rotation_certificates=missing,
        full_logical_T_count=row["full_T_count"],
        conditional_logical_work_smaller=row["full_T_count"] is not None
        and row["full_T_count"] < base_T,
        source_compatible_digital_estimator_certified=not missing,
        complete_price_feasible=False,
        open_obligations=OBLIGATIONS,
        other_sampler_law_bounds_transferred=False,
    )
    assert saved_summary == expected_summary
    if share == Fraction(9, 20):
        accepted = read(PROGRAM / "E02_IQFT_run001" / case / "synthesized_estimator_ledger.json")
        assert (
            row["full_T_count"] == accepted["full_T_count"]
            and row["full_T_depth"] == accepted["full_T_depth"]
        )
        assert actual == read(PROGRAM / "E02_IQFT_run001" / case / "iqft_operations.json")
    return dict(
        passed=True,
        case=case,
        statistical_share_exact=pair(share),
        qpe_bits=bits,
        controlled_G_calls=Q,
        missing_rotation_certificates=missing,
        actual_paid_full_costs=costs,
        four_full_price_obligations_preserved=OBLIGATIONS,
        full_price_feasible=False,
    )


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    assert not output.exists()
    frozen = {}
    for directory in (
        CONVERSION,
        GRID,
        PROGRAM / "E02_financial_audit_run001",
        PROGRAM / "E02_IQFT_audit_run001",
    ):
        assert read(directory / "summary.json")["passed"]
        receipt = read(directory / "manifest.json")
        frozen.update(receipt["files"])
        frozen.update(receipt["frozen_inputs"])
        frozen[relative(directory / "manifest.json")] = sha(directory / "manifest.json")
    own = Path(__file__).resolve()
    frozen[relative(own)] = sha(own)
    verify(frozen)
    output.mkdir()
    shutil.copy2(own, output / "executed_audit_confidence_and_split.py")
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_independent_audit=True,
            frozen_inputs=frozen,
            interpreter_sha256=sha(sys.executable),
            fixed_conversions=2,
            fixed_source_share_rows=6,
            fixed_shares_exact=list(map(pair, SHARES)),
            independent_derivations="Squared Markov, direct rational binomial sums, alternating atan(1/2)+atan(1/3) pi enclosure, independent powers-of-two schedule and actual saved IQFT token expansion",
            native_rotation_interval_proof_reused_only_from_hash_bound_prior_independent_audit=True,
            no_audited_producer_functions_imported=True,
            source_allocation_immutable=True,
            new_financial_prices=0,
            new_gate_replays=0,
            new_toys=0,
            new_settings=0,
            new_pytest_cases=0,
            full_price_certificate_not_claimed=True,
        ),
    )
    print("E21/E24 independent allocation audit frozen", flush=True)


def run(output):
    output = Path(output).resolve()
    assert not (output / "summary.json").exists()
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    assert sha(sys.executable) == protocol["interpreter_sha256"]
    save(output / "confidence_conversion_audit.json", audit_conversions())
    grid_protocol, summary = read(GRID / "protocol.json"), read(GRID / "summary.json")
    assert grid_protocol["before_finite_grid_reconciliation"]
    assert grid_protocol["represented_source_widths"] == [
        dict(native=72, fraction=40, midpoint_uniform=32)
    ]
    assert grid_protocol["statistical_shares_exact"] == list(map(pair, SHARES))
    assert exact(grid_protocol["epsilon_dollars_exact"]) == Fraction(1, 100)
    assert exact(grid_protocol["estimator_failure_exact"]) == ALPHA
    assert grid_protocol["cases"] == ["B4x12", "B8x52"] and grid_protocol["source_variants"] == 1
    assert not grid_protocol["continuous_bound_interpolation_or_different_law_transfer_allowed"]
    rotations = read(PROGRAM / "E02_IQFT_run001/rotations.json")
    assert set(rotations) == {"pi_1_%d" % (1 << exponent) for exponent in range(3, 17)}
    for exponent in range(3, 17):
        record = rotations["pi_1_%d" % (1 << exponent)]
        tokens = record["matrix_product_gates"]
        assert set(tokens) <= set("HTSXW") and tokens
        assert record["target"] == dict(kind="pi", numerator=1, denominator=1 << exponent)
        assert record["t_count"] == tokens.count("T")
        assert record["clifford_count"] == sum(tokens.count(token) for token in "HSX")
        assert record["physical_clifford_t_depth"] == len(tokens) - tokens.count("W")
    assert read(PROGRAM / "E02_IQFT_audit_run001/summary.json")["passed"]
    pi, audits = independent_pi(), []
    for case_index, case in enumerate(("B4x12", "B8x52")):
        for share_index, share in enumerate(SHARES):
            result = audit_grid_row(
                case, share, summary["candidates"][3 * case_index + share_index], rotations, pi
            )
            save(
                output
                / (
                    case
                    + "_"
                    + str(share.numerator)
                    + "_of_"
                    + str(share.denominator)
                    + "_audit.json"
                ),
                result,
            )
            audits.append(result)
            print(case, pair(share), "schedule/tokens/full costs/open obligations PASS", flush=True)
    assert summary["passed"] and len(summary["candidates"]) == 6
    assert summary["full_price_feasible_rows"] == 0 and summary[
        "adopted_statistical_share_exact"
    ] == [9, 20]
    for key in (
        "accepted_source_or_allocation_changed",
        "unsupported_bias_interpolation_or_quantile_law_transfer",
        "full_G2_closed",
        "physical_execution_certificate",
    ):
        assert not summary[key]
    assert summary["financial_prices_or_gate_replays"] == summary["new_pytest_cases"] == 0
    verify(protocol["frozen_inputs"])
    save(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            producer_distinct_tests_reconciled=8,
            exact_confidence_conversions_audited=2,
            fixed_source_share_rows_audited=6,
            minimal_odd_quarter_failure_median_repetitions=27,
            actual_finite_RMSE_constructions_supplied=0,
            complete_RMSE_cost_winner=False,
            saved_15_or_16_bit_IQFT_recipes_fully_reconciled=4,
            missing_17_bit_rotation_rows=2,
            missing_rotation="pi_1_131072",
            full_price_feasible_rows=0,
            original_adopted_statistical_share_exact=[9, 20],
            accepted_source_or_split_changed=False,
            four_full_price_obligations_preserved=OBLIGATIONS,
            conditional_on_delivery_confidence_claim=False,
            new_financial_prices=0,
            new_gate_replays=0,
            new_toys=0,
            new_settings=0,
            physical_runtime_seconds=None,
            continuous_price_certificate=False,
            quantum_advantage_claim=False,
        ),
    )
    finish_manifest(output)
    print("E21/E24 independent allocation audit PASS", flush=True)


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
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
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
                    new_financial_prices=0,
                    new_gate_replays=0,
                    full_price_certificate=False,
                ),
            )
            finish_manifest(output)
            raise
