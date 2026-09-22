"""Join emitted range/wave source costs to explicit estimator and rotation counts."""

from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from research.controlled_source_completion.run import dump

ROOT = Path("results/controlled_priority_completion")
OLD = Path("results/controlled_completion_followup/arithmetic_v1/compile_v2")


def read(path):
    return json.loads(path.read_text())


def main():
    synthesis_path = Path("results/controlled_completion_followup/synthesis_rotations.json")
    synthesis = read(synthesis_path)
    rotations = synthesis["rotations"]
    phase = read(ROOT / "parallel_v1/phase_f64_limit_all.json")["resources"]
    old_phase = read(OLD / "phase_f64/source.json")["resources"]
    rows = []
    for method, records in (
        ("hadamard", read(ROOT / "estimator_hadamard.json")),
        ("bounded_QAE", read(ROOT / "estimator_bounded.json")),
    ):
        for record in records:
            model = record["model"]
            mode = record.get("mode", "unconditional_digital_support")
            schedule_path = ROOT / "range_parallel_v1" / (model + "_f40_limit_all.json")
            schedule = read(schedule_path)
            source = schedule["resources"]
            previous = read(OLD / (model + "_f40") / "source.json")["resources"]
            allocation = record["allocation"]
            usage = Counter()
            if method == "hadamard":
                calls = allocation["controlled_U_calls"]
                stage_count = len(allocation["stages"])
                one = record["single_U"]
                unit_t = one["t_count"] - previous["t_count"] + source["t_count"]
                unit_depth = (
                    one["t_depth"]
                    - previous["t_depth"]
                    - old_phase["t_depth"]
                    + source["t_depth"]
                    + phase["t_depth"]
                )
                qubits = (
                    record["logical_qubits_upper"]
                    - previous["logical_qubits"]
                    - old_phase["logical_qubits"]
                    + source["logical_qubits"]
                    + phase["logical_qubits"]
                )
                # Three single-qubit phase factors per controlled phase bit.
                for bit in range(67):
                    angle = Fraction(1 << bit, 2 << 64)
                    usage["radian_%d_%d" % (angle.numerator, angle.denominator)] += 3 * calls
                extra_t = 0
                serial_depth = calls * unit_depth
                preparations = allocation["hadamard_test_executions"]
                measurements = preparations
                longest = allocation["longest_single_chain"]
                required_phase_error = record["required_uniform_phase_function_error"]
            else:
                calls = allocation["controlled_grover_calls"]
                stage_count = 1
                unit_t = record["single_iterate_T_count"] - previous["t_count"] + source["t_count"]
                unit_depth = (
                    record["single_iterate_T_depth"] - previous["t_depth"] + source["t_depth"]
                )
                qubits = (
                    record["logical_qubits_upper"]
                    - previous["logical_qubits"]
                    + source["logical_qubits"]
                )
                b, repetitions = allocation["qpe_bits"], allocation["repetitions"]
                for gap in range(2, b):
                    usage["pi_1_%d" % (1 << (gap + 1))] += 3 * (b - gap) * repetitions
                extra_t = record["arithmetic_T_count"] - calls * record["single_iterate_T_count"]
                serial_depth = record["serial_arithmetic_T_depth"] + calls * (
                    unit_depth - record["single_iterate_T_depth"]
                )
                preparations = repetitions
                measurements = repetitions * b
                longest = allocation["M"] - 1
                required_phase_error = None
            synthesis_t = sum(count * rotations[key]["t_count"] for key, count in usage.items())
            synthesis_clifford = sum(
                count * rotations[key]["clifford_count"] for key, count in usage.items()
            )
            arithmetic_t = calls * unit_t + extra_t
            # Serialize the actual rotation strings. This is a valid scheduling
            # upper bound, not an optimized depth or a runtime lower bound.
            depth_with_synthesis = serial_depth + synthesis_t
            budget = record["tenfold_total_budget_seconds"]
            error = Fraction(*synthesis["common_operator_epsilon_exact"])
            coherent_failure = 2 * sum(usage.values()) * error
            assert coherent_failure <= Fraction(5, 10000)
            rows.append(
                dict(
                    model=model,
                    method=method,
                    mode=mode,
                    controlled_iterations=calls,
                    sequential_adaptive_stages=stage_count,
                    fresh_preparations=preparations,
                    measured_bits=measurements,
                    logical_qubits_upper=qubits,
                    arithmetic_T_count=arithmetic_t,
                    synthesized_rotation_T_count=synthesis_t,
                    complete_logical_T_count=arithmetic_t + synthesis_t,
                    synthesized_rotation_Clifford_count=synthesis_clifford,
                    arithmetic_wave_T_depth=serial_depth,
                    wave_plus_serial_rotations_T_depth=depth_with_synthesis,
                    source_wave_T_depth=source["t_depth"],
                    single_iterate_arithmetic_T_depth=unit_depth,
                    longest_coherent_chain_arithmetic_T_depth=longest * unit_depth,
                    required_phase_function_error=required_phase_error,
                    synthesis_total_variation_bound=float(coherent_failure),
                    synthesis_usage=dict(usage),
                    tenfold_budget_seconds=budget,
                    seconds_at_hypothetical_1ns_T_layer=depth_with_synthesis * 1e-9,
                    scheduled_T_layer_seconds_to_meet_budget=budget / depth_with_synthesis,
                    scheduled_shortfall_factor_at_1ns=depth_with_synthesis * 1e-9 / budget,
                    independent_test_parallelism="Tests can run in parallel within a stage, "
                    "paying a full source workspace per copy. Reported schedule uses one copy.",
                    full_price_latency_seconds=None,
                    scope="Logical schedule; Clifford time, routing, setup and correction "
                    "excluded from 1ns sensitivity. No hardware timing or universal lower bound.",
                    source_schedule_sha256=hashlib.sha256(schedule_path.read_bytes()).hexdigest(),
                )
            )
    output = dict(
        format="controlled-compound-combined-cost-v1",
        rows=rows,
        synthesis_sha256=hashlib.sha256(synthesis_path.read_bytes()).hexdigest(),
        resource_contract="One strike, Kc=6, residual mean error .002/discount, "
        "ideal estimator failure .003. Classical screening times charge three strikes.",
        omitted_full_price_terms=[
            "classical training and policy baseline estimate",
            "policy-regret certificate",
            "moment acquisition/transfer for conditional Hadamard",
            "input/output classical time",
            "device layout, decoder, physical gates and factory supply",
        ],
        significance_gate_passed=False,
    )
    dump(ROOT / "combined_cost.json", output)
    for row in rows:
        print(
            json.dumps(
                {
                    k: row[k]
                    for k in (
                        "model",
                        "method",
                        "mode",
                        "complete_logical_T_count",
                        "logical_qubits_upper",
                        "seconds_at_hypothetical_1ns_T_layer",
                        "scheduled_shortfall_factor_at_1ns",
                    )
                }
            )
        )


if __name__ == "__main__":
    main()
