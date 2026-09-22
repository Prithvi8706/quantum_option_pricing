"""Bind emitted wave sources, explicit estimators and verified rotation strings.

These are executable hierarchical recipes, not a simulation of the full price
or a device layout. Classical control and all repeated powers are explicit.
"""

from collections import Counter
import copy
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import mpmath as mp

from research.controlled_source_completion.envelope import controlled_U, inverse_qft
from research.controlled_source_completion.run import dump


ROOT = Path("results/controlled_priority_completion")
PHASE_SOURCE = Path(
    "results/controlled_completion_followup/arithmetic_v1/compile_v2/phase_f64/source.json"
)
PHASE_SCHEDULE = ROOT / "parallel_v1/phase_f64_limit_all.json"
SYNTHESIS = Path("results/controlled_completion_followup/synthesis_rotations.json")


def read(path):
    return json.loads(path.read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wave_source(manifest_path, schedule_path):
    source, schedule = read(manifest_path), read(schedule_path)
    assert schedule["source_sha256"] == sha256(manifest_path)
    source = copy.deepcopy(source)
    source["resources"] = schedule["resources"]
    source["path"] = manifest_path.as_posix()
    return source


def exact_mpf(value):
    """Convert an mpmath binary endpoint tuple into an exact rational."""
    sign, mantissa, exponent, _ = value
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def decode_bounded(measurements, allocation):
    """Median QAE decoding with a deterministic classical rounding certificate."""
    values = list(measurements)
    M, repetitions, span = allocation["M"], allocation["repetitions"], allocation["span"]
    if len(values) != repetitions or any(type(k) is not int or not 0 <= k < M for k in values):
        raise ValueError("Expected exactly the allocated number of QPE integers")
    if repetitions % 2 != 1:
        raise ValueError("The certified median schedule requires odd repetitions")
    mp.iv.dps = 80
    intervals = []
    for k in values:
        angle = mp.iv.pi * k / M
        price = span * mp.iv.sin(angle) ** 2 - mp.iv.mpf(span) / 2
        intervals.append(tuple(exact_mpf(endpoint) for endpoint in price._mpi_))
    lo = sorted(interval[0] for interval in intervals)[repetitions // 2]
    hi = sorted(interval[1] for interval in intervals)[repetitions // 2]
    estimate = float((lo + hi) / 2)
    rounding = max(abs(Fraction(estimate) - lo), abs(Fraction(estimate) - hi))
    assert rounding <= Fraction(1, 10**10)
    ideal = span * (mp.iv.pi / M + mp.iv.pi**2 / M**2)
    total = exact_mpf(ideal._mpi_[1]) + rounding
    assert total <= Fraction(allocation["error"])
    return dict(
        estimate=estimate,
        decoded_median_interval_exact=[
            [lo.numerator, lo.denominator],
            [hi.numerator, hi.denominator],
        ],
        rounding_error_bound=math.nextafter(float(rounding), math.inf),
        ideal_plus_rounding_error_bound=math.nextafter(float(total), math.inf),
        ideal_failure=allocation["ideal_test_failure"],
    )


def make_hadamard_wrapper(model):
    source_path = ROOT / "range_compile_v1" / (model + "_f40") / "source.json"
    schedule_path = ROOT / "range_parallel_v1" / (model + "_f40_limit_all.json")
    source = wave_source(source_path, schedule_path)
    phase = wave_source(PHASE_SOURCE, PHASE_SCHEDULE)
    wrapper = controlled_U(source, phase, fused=True)
    schedules = {source_path.as_posix(): schedule_path, PHASE_SOURCE.as_posix(): PHASE_SCHEDULE}
    for operation in wrapper["operations"]:
        if operation["gate"] == "call_graph_half":
            manifest = Path(operation["manifest"])
            schedule = schedules[operation["manifest"]]
            operation.update(
                gate="call_wave_half",
                wave_schedule=schedule.as_posix(),
                wave_schedule_sha256=sha256(schedule),
                source_manifest_sha256=sha256(manifest),
            )
        elif operation["gate"] == "cp":
            half = Fraction(*operation["angle_radians"]) / 2
            magnitude = abs(half)
            operation["synthesis_key"] = "radian_%d_%d" % (
                magnitude.numerator,
                magnitude.denominator,
            )
            operation["half_angle_sign"] = 1 if half > 0 else -1
    wrapper.update(
        format="controlled-complex-phase-wave-wrapper-v1",
        call_semantics=(
            "call_wave_half invokes parallel_source.apply_half with the indicated manifest, "
            "schedule, base and inverse flag. Inverse reverses wave groups and repeats clean "
            "XOR leaves. Every workspace is initially clean."
        ),
        phase_classical_input_width=96,
        physical_mapping=None,
    )
    return wrapper


def audit_wrapper(wrapper):
    """Check address validity, exact source/schedule binding and call structure."""
    limit = wrapper["qpe_register_base"]
    calls = []
    for op in wrapper["operations"]:
        wires = op.get("wires", [])
        assert len(wires) == len(set(wires))
        assert all(wire == "control" or 0 <= wire < limit for wire in wires)
        if op["gate"] != "call_wave_half":
            continue
        manifest_path, schedule_path = Path(op["manifest"]), Path(op["wave_schedule"])
        source, schedule = read(manifest_path), read(schedule_path)
        assert schedule["source_sha256"] == sha256(manifest_path)
        if "source_manifest_sha256" in op:
            assert op["source_manifest_sha256"] == sha256(manifest_path)
            assert op["wave_schedule_sha256"] == sha256(schedule_path)
        assert op["base"] >= 0
        assert op["base"] + schedule["resources"]["logical_qubits"] <= limit
        calls.append((op["manifest"], op["base"], op["inverse"]))
        assert source["word_width"] in (72, 96)
    assert len(calls) in (2, 4)
    for forward, inverse in zip(calls[: len(calls) // 2], reversed(calls[len(calls) // 2 :])):
        assert forward[:2] == inverse[:2]
        assert forward[2] is False and inverse[2] is True
    assert wrapper["operations"][-1] == dict(gate="z", wires=["control"])
    return dict(
        hierarchical_calls=len(calls),
        explicit_operations=len(wrapper["operations"]),
        internal_wire_limit=limit,
        matched_source_and_schedule_hashes=True,
    )


def main():
    cost_path = ROOT / "combined_cost.json"
    costs = read(cost_path)
    synthesis = read(SYNTHESIS)
    hadamard_records = read(ROOT / "estimator_hadamard.json")
    bounded_records = read(ROOT / "estimator_bounded.json")
    wrappers = {}
    for model in ("C4", "H8"):
        path = ROOT / ("combined_" + model + "_hadamard_wrapper.json")
        wrapper = make_hadamard_wrapper(model)
        dump(path, wrapper)
        wrappers[model, "hadamard"] = path, wrapper
        bounded_path = ROOT / ("combined_" + model + "_bounded_wrapper.json")
        wrappers[model, "bounded_QAE"] = bounded_path, read(bounded_path)
    rows, checks = [], []
    for cost in costs["rows"]:
        model, method = cost["model"], cost["method"]
        path, wrapper = wrappers[model, method]
        check = audit_wrapper(wrapper)
        check.update(model=model, method=method)
        checks.append(check)
        base = wrapper["qpe_register_base"]
        if method == "hadamard":
            record = next(
                r for r in hadamard_records if r["model"] == model and r["mode"] == cost["mode"]
            )
            allocation = record["allocation"]
            controls = [base]
            measured = allocation["hadamard_test_executions"]
            expected_usage = Counter()
            for operation in wrapper["operations"]:
                if operation["gate"] == "cp":
                    expected_usage[operation["synthesis_key"]] += (
                        3 * allocation["controlled_U_calls"]
                    )
            control = dict(
                implementation="research.controlled_priority_completion.estimator_hadamard.controller",
                adaptive_target=(
                    "Exact target=a+c*width/(1+3*c); nearest f64 raw load to phase input named left"
                ),
                normalizer_load="Unscaled integer log2(allocation.normalizer) in scale_exponent",
                one_test_operations=[
                    "Reset all random and control wires; verify arithmetic workspace clean",
                    "H on random_wires and on control wire",
                    "X-load target and scale_exponent in phase_classical_input_offsets",
                    "Run this controlled wrapper T times with control replaced by the control wire",
                    "H on control; measure computational zero as plus=True",
                    "Unload classical constants; reset measured/random registers before next test",
                ],
                repetitions=(
                    "Exactly each stage's repetitions; threshold and rational interval "
                    "update in allocation"
                ),
                IQFT_operations=[],
            )
            allocation_path = ROOT / "estimator_hadamard.json"
        else:
            record = next(r for r in bounded_records if r["model"] == model)
            allocation = record["allocation"]
            controls = list(range(base, base + allocation["qpe_bits"]))
            measured = allocation["repetitions"] * len(controls)
            qft = inverse_qft(controls)
            expected_usage = Counter()
            exact_cp = 0
            for operation in qft:
                if operation["gate"] != "cp":
                    continue
                half = abs(Fraction(*operation["angle_pi"]) / 2)
                if half == Fraction(1, 4):
                    operation["exact_T_count"] = 3
                    exact_cp += 1
                else:
                    key = "pi_%d_%d" % (half.numerator, half.denominator)
                    operation["synthesis_key"] = key
                    operation["half_angle_sign"] = -1
                    expected_usage[key] += 3 * allocation["repetitions"]
            assert 3 * exact_cp * allocation["repetitions"] == (
                record["arithmetic_T_count"]
                - allocation["controlled_grover_calls"] * record["single_iterate_T_count"]
            )
            control = dict(
                implementation="fixed QPE, independent repetition, median amplitude decoding",
                decoder="research.controlled_priority_completion.combined_wrappers.decode_bounded",
                one_test_preparation=(
                    "Reset random_wires and controls, then H on every such wire; "
                    "arithmetic workspace clean"
                ),
                powers=[
                    dict(control=wire, repetitions_of_wrapper=1 << j)
                    for j, wire in enumerate(controls)
                ],
                IQFT_operations=qft,
                measurement=(
                    "Measure controls with the explicit IQFT swap/bit convention; "
                    "decode p=sin(pi*k/M)^2"
                ),
                final_output=(
                    "decode_bounded computes the median price interval at 80-digit interval "
                    "precision, certifies binary64 output rounding <=1e-10, and checks "
                    "ideal QAE error plus that rounding stays inside allocation.error"
                ),
                repetitions=allocation["repetitions"],
                reset=(
                    "Reset every random/selector/control wire before each independent QPE execution"
                ),
            )
            allocation_path = ROOT / "estimator_bounded.json"
        assert dict(expected_usage) == cost["synthesis_usage"]
        assert measured == cost["measured_bits"]
        assert max(controls) < cost["logical_qubits_upper"]
        assert all(key in synthesis["rotations"] for key in expected_usage)
        rows.append(
            dict(
                model=model,
                method=method,
                mode=cost["mode"],
                wrapper=path.as_posix(),
                wrapper_sha256=sha256(path),
                allocation_source=allocation_path.as_posix(),
                allocation_source_sha256=sha256(allocation_path),
                allocation=allocation,
                control_wires=controls,
                random_wires=wrapper["random_wires"],
                classical_controller=control,
                synthesis_usage=dict(expected_usage),
                complete_logical_T_count=cost["complete_logical_T_count"],
                allocated_logical_qubits_upper=cost["logical_qubits_upper"],
                full_price_and_physical_runtime=None,
            )
        )
    payload = dict(
        format="bound-controlled-compound-estimators-v1",
        cost_artifact=cost_path.as_posix(),
        cost_artifact_sha256=sha256(cost_path),
        synthesis_library=SYNTHESIS.as_posix(),
        synthesis_library_sha256=sha256(SYNTHESIS),
        synthesized_controlled_phase_recipe=(
            "CP(theta): P(theta/2) on control, P(theta/2) on target, CX(control,target), "
            "P(-theta/2) on target, CX(control,target). Replace P by verified Rz up to "
            "an overall input-independent global phase. Matrix-product gate strings "
            "execute in reverse order; negative angles use their conjugate transpose. "
            "Track/remove each global W consistently with the existing certificate."
        ),
        wave_call_implementation="research.controlled_priority_completion.parallel_source.apply_half",
        rows=rows,
        scope=(
            "Executable hierarchical binding and resource reconciliation only; "
            "no full-QPE simulation, device mapping or financial-price certification."
        ),
    )
    dump(ROOT / "combined_estimators.json", payload)
    dump(ROOT / "combined_wrapper_checks.json", dict(status="passed", checks=checks))
    print(json.dumps(dict(bound_estimators=len(rows), wrapper_checks=len(checks))))


if __name__ == "__main__":
    main()
