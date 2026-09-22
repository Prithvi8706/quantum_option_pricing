"""Auditable conditional surface-code scenarios, not a hardware demonstration.

All logical gates are serialized. One dedicated tree of 15-to-1 factories feeds
one T at a time, with finite retry caps and their failure probability charged.
Distances include the idle exposure of every provisioned patch for the entire
upper schedule. Empirical hardware formulas remain explicit assumptions.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import time

from research.controlled_completion_followup.synthesis_rotations import ROOT, OUTPUT as SYNTHESIS
from research.controlled_source_completion.modern_mean import controller

ORIGINAL = ROOT / "results/controlled_source_completion/cost_v3_phase64"
BUDGET = dict(
    logical_faults=0.001,
    magic_state_errors=0.0005,
    exhausted_retries=0.0001,
    classical_controller_faults=0.0004,
)


def logical_error(p, d):
    """Fowler--Gidney 2019 Sec. XV empirical per-patch-round fit."""
    return 0.1 * (100 * p) ** ((d + 1) // 2)


def distillation(n_t, p):
    """Loose rigorous stochastic-Z bound, conditioned on no logical faults.

    15-to-1 detects weight-1/2 errors. Union over triples bounds an undetected
    error by C(15,3)*e^3. No input errors implies acceptance with (1-e)^15.
    This bounds all higher orders, unlike using 35*e^3 as an exact certificate.
    Independence of accepted inputs to distinct nodes is an explicit condition.
    """
    errors = [p]
    while n_t * errors[-1] > BUDGET["magic_state_errors"]:
        e = errors[-1]
        errors.append(math.comb(15, 3) * e**3 / (1 - e) ** 15)
        if len(errors) > 8:
            raise ValueError("Unsupported factory regime")
    levels = len(errors) - 1
    q = 1 - (1 - p) ** 15
    retries = 1
    while True:
        distill_invocations = n_t * sum((15 * retries) ** j for j in range(levels))
        if distill_invocations * q**retries <= BUDGET["exhausted_retries"] / 2:
            break
        retries += 1
    raw_invocations = n_t * (15 * retries) ** levels
    raw_retries = math.ceil(math.log2(raw_invocations / (BUDGET["exhausted_retries"] / 2)))
    return dict(
        levels=levels,
        conditional_error_bounds_by_level=errors,
        magic_error_union_bound=n_t * errors[-1],
        retries_per_distillation=retries,
        raw_injection_retries=raw_retries,
        raw_injection_success_probability_assumption=0.5,
        distillation_invocations_upper=distill_invocations,
        raw_injection_invocations_upper=raw_invocations,
        retry_exhaustion_union_bound=distill_invocations * q**retries
        + raw_invocations * 2.0 ** (-raw_retries),
        tree_factory_blocks=sum(15**j for j in range(levels)),
        raw_injection_lanes=15**levels,
        note=(
            "One full 15-ary tree; siblings run in parallel, algorithm gates and "
            "root outputs are serial. No logical fault is permitted in this "
            "stochastic-input calculation; those faults are union-bounded "
            "separately over every provisioned patch-round."
        ),
    )


def factory_cycles(factory, d, feedback_cycles):
    cycles = factory["raw_injection_retries"] * (3 + feedback_cycles)
    for _ in range(factory["levels"]):
        cycles = factory["retries_per_distillation"] * (cycles + 15 * d + feedback_cycles)
    return cycles


def logical_counts(row, synthesis, uses):
    ledger = row["ledger"]
    synthesis_t = sum(count * synthesis[key]["t_count"] for key, count in uses.items())
    synthesis_clifford = sum(
        count * synthesis[key]["clifford_count"] for key, count in uses.items()
    )
    exact_qft_t = ledger["additional_exact_inverse_qft_t_count"]
    assert sum(uses.values()) == ledger["unsynthesized_single_qubit_phase_gates"]
    cx = (
        ledger["arithmetic_clifford_cx"]
        + ledger["controlled_phase_decomposition_cx"]
        + ledger["qft_swap_cx"]
    )
    single_clifford = (
        sum(
            ledger[key]
            for key in (
                "arithmetic_clifford_h",
                "arithmetic_x",
                "reflection_control_z",
                "uniform_preparation_h",
                "qpe_preparation_and_qft_h",
                "classical_constant_load_and_unload_x_upper",
            )
        )
        + synthesis_clifford
    )
    n_t = ledger["arithmetic_t_count"] + exact_qft_t + synthesis_t
    return dict(
        t_count=n_t,
        synthesis_t_count=synthesis_t,
        synthesis_clifford_count=synthesis_clifford,
        clifford_cx=cx,
        single_qubit_cliffords=single_clifford,
        # Serial synthesized rotations are an explicit valid local
        # schedule; no parallelism among their T gates is assumed.
        t_depth_serial_rotations_plus_archived_arithmetic=(
            ledger["serial_arithmetic_t_depth"]
            + ledger["additional_serial_exact_inverse_qft_t_depth"]
            + synthesis_t
        ),
        synthesis_over_arithmetic_t_ratio=synthesis_t / ledger["arithmetic_t_count"],
    )


def scenario(row, counts, p, cycle_seconds, routing_hops, feedback_seconds):
    q = row["ledger"]["logical_qubits"]
    factory = distillation(counts["t_count"], p)
    # 11 protocol tiles + 16 input/output buffers per factory node. Two tiles
    # per raw lane and a further equal routing/spare allowance are assumptions.
    factory_tiles = 27 * factory["tree_factory_blocks"] + 2 * factory["raw_injection_lanes"]
    tiles = 2 * (q + factory_tiles)
    feedback_cycles = math.ceil(feedback_seconds / cycle_seconds)
    ledger = row["ledger"]
    schedule = json.loads(
        (ORIGINAL / ("%s_f%d_%s_schedule.json" % (row["model"], row["f"], row["mode"]))).read_text()
    )
    stages = len(schedule["stages"])
    for d in range(3, 202, 2):
        production = factory_cycles(factory, d, feedback_cycles)
        # 2*hops SWAPs restore placement; each SWAP is three adjacent CNOTs,
        # each adjacent CNOT takes 2*d rounds. The additional gate takes 2*d.
        cx_cycles = (12 * routing_hops + 2) * d
        t_cycles = production + (12 * routing_hops + 4) * d + feedback_cycles
        measure_cycles = (
            ledger["measured_bits"]
            + ledger["random_input_qubit_resets"]
            + ledger["qpe_qubit_resets"]
        ) * d
        controller_cycles = (stages + ledger["qpe_executions"]) * feedback_cycles
        total_cycles = (
            q * d
            + counts["t_count"] * t_cycles
            + counts["clifford_cx"] * cx_cycles
            + counts["single_qubit_cliffords"] * 4 * d
            + measure_cycles
            + controller_cycles
        )
        exposure = tiles * total_cycles
        fault_bound = exposure * logical_error(p, d)
        if fault_bound <= BUDGET["logical_faults"]:
            break
    else:
        raise ValueError("Code distance search exhausted")
    return dict(
        physical_error_probability_assumption=p,
        code_cycle_seconds_assumption=cycle_seconds,
        feedback_seconds_assumption=feedback_seconds,
        routing_hops_per_gate_assumption=routing_hops,
        distance=d,
        provisioned_tiles=tiles,
        factory_tiles_before_routing_allowance=factory_tiles,
        physical_qubits_upper_formula_2d2=2 * d * d * tiles,
        serial_execution_cycles_upper_conditional=total_cycles,
        serial_execution_seconds_upper_conditional=total_cycles * cycle_seconds,
        logical_patch_round_exposure_upper=exposure,
        per_patch_round_logical_error_fit=logical_error(p, d),
        logical_fault_union_bound=fault_bound,
        factory=factory,
        factory_output_cycles_upper=production,
        factory_delivered_T_per_second_guaranteed_on_no_abort=1 / (production * cycle_seconds),
        measurement_reset_cycles=measure_cycles,
        interval_controller_and_qpe_feedback_cycles=controller_cycles,
        conditional_physical_failure_upper=fault_bound
        + factory["magic_error_union_bound"]
        + factory["retry_exhaustion_union_bound"]
        + BUDGET["classical_controller_faults"],
        conditional_serial_schedule=(
            "One logical gate at a time, one T output at a time. All patches "
            "remain live throughout. Factory siblings may run in parallel. No "
            "unlimited algorithm/QPE repetition parallelism."
        ),
        geometry_status=(
            "Distance-preserving local primitives, factory interfaces, decoder "
            "reliability and stated hop bound are assumptions, not an emitted "
            "layout or measured device. Hop Q-1 is a deliberately slow line-route "
            "alternative; hop 1 requires every interaction adjacent."
        ),
    )


def run(ledger_path, output):
    rows = json.loads(ledger_path.read_text())
    payload = json.loads(SYNTHESIS.read_text())
    uses = {record["tag"]: record["usage"] for record in payload["usage"]}
    output_rows = []
    for row in rows:
        tag = "%s_f%d_%s" % (row["model"], row["f"], row["mode"])
        counts = logical_counts(row, payload["rotations"], uses[tag])
        schedule = json.loads((ORIGINAL / (tag + "_schedule.json")).read_text())
        timings = []
        for _ in range(5):
            start = time.perf_counter()
            controller(schedule, lambda stage, left: [0] * stage["repetitions"])
            timings.append(time.perf_counter() - start)
        scenarios = [
            scenario(row, counts, p, 1e-6, hops, 1e-5)
            for p in (1e-3, 1e-4)
            for hops in (1, row["ledger"]["logical_qubits"] - 1)
        ]
        output_rows.append(
            dict(
                tag=tag,
                model=row["model"],
                f=row["f"],
                mode=row["mode"],
                counts=counts,
                scenarios=scenarios,
                logical_gate_parallelism_note=(
                    "Archived arithmetic depth retained as a comparison coordinate; "
                    "conditional upper execution serializes all gates and includes their "
                    "Clifford operations."
                ),
                controller_cpu_diagnostic_seconds=timings,
                controller_cpu_diagnostic_scope=(
                    "Five all-small-result schedule replays only; excludes device IO and "
                    "real-time decoder throughput, not a certified worst-case classical "
                    "execution time."
                ),
                full_price_budget=dict(
                    reusable_rotation_library_generation_seconds=payload["generation_seconds"],
                    synthesis_setup_policy=(
                        "Charge this recorded one-time CPU generation cost unless reusing the "
                        "same verified angle library; it is not device time."
                    ),
                    classical_full_price_seconds=row["classical_full_price_seconds"],
                    tenfold_total_budget_seconds=row["tenfold_total_budget_seconds"],
                    archived_certificate_and_training_seconds=row["ledger"][
                        "preprocessing_seconds"
                    ],
                    online_surrogate_and_regret_certificate_seconds=None,
                    digital_bridge_certificate_seconds=None,
                    policy_training_if_not_in_archived_certificate_seconds=None,
                    device_decoder_and_output_seconds=None,
                    formula=(
                        "T_train + T_certificates + T_surrogate + T_device + T_decoder_IO + "
                        "T_outputs <= T_classical/10"
                    ),
                    status=(
                        "Unclosed full-price cost/correctness certificate; null terms must not "
                        "be treated as zero."
                    ),
                ),
            )
        )
    result = dict(
        format="conditional-ft-scenarios-v1",
        ledger_path=ledger_path.relative_to(ROOT).as_posix(),
        ledger_sha256=hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        synthesis_sha256=hashlib.sha256(SYNTHESIS.read_bytes()).hexdigest(),
        physical_failure_allocation=BUDGET,
        rows=output_rows,
        primary_sources=[
            "https://arxiv.org/pdf/1808.06709",
            "https://quantum-journal.org/papers/q-2019-03-05-128/",
        ],
        assumptions=(
            "Independent stochastic raw magic-state Z errors; empirical pL fit "
            "applies to all provisioned patch-rounds and distance-preserving "
            "operations; one logical single-qubit Clifford <=4d rounds; adjacent "
            "CNOT <=2d; T injection/correction <=4d+feedback; higher distillation "
            "<=15d+feedback; raw successful injection error <=p and success "
            "probability >=1/2 within 3 rounds; adequate decoder throughput; "
            "independent accepted inputs; routing/interface tiles and hop "
            "assumptions suffice. No physical mapping or physical runtime "
            "demonstration."
        ),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    for row in output_rows:
        print(
            row["tag"],
            "T",
            row["counts"]["t_count"],
            [
                (
                    s["distance"],
                    s["factory"]["levels"],
                    s["serial_execution_seconds_upper_conditional"],
                )
                for s in row["scenarios"]
            ],
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=ORIGINAL / "ledger.json")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results/controlled_completion_followup/ft_scenarios.json",
    )
    args = parser.parse_args()
    run(args.ledger.resolve(), args.output.resolve())
