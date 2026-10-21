"""Prospectively freeze one Gaussian-prefix certificate and one synthesis call."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.metadata
import json
from pathlib import Path
import random
import sys
import threading
import time
import traceback
import _thread
import xml.etree.ElementTree as ET

import mpmath as mp

from research.limitation_program_20261001 import gaussian_prefix_certificate as prefix

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
RESEARCH = ROOT / "research/limitation_program_20261001"
ARCHIVE = ROOT / "results/limitation_audit_20261001/gaussian_v3"
DECLARED_TESTS = 18
CPU_LIMIT = 300
ADMISSION_INTERRUPT_CPU = 270
WALL_LIMIT = 600


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def create(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def verify(frozen):
    for name, expected in frozen.items():
        if sha(ROOT / name) != expected:
            raise ValueError("Frozen input changed: " + name)


def prepare(output):
    import pygridsynth

    if importlib.metadata.version("pygridsynth") != "1.1.0" or mp.__version__ != "1.3.0":
        raise ValueError("Only the existing primary local synthesis package is admitted")
    output = output.resolve()
    output.relative_to(PROGRAM)
    output.mkdir(exist_ok=False)
    own = Path(__file__).resolve()
    code = [
        own,
        RESEARCH / "gaussian_prefix_certificate.py",
        RESEARCH / "test_gaussian_prefix_certificate.py",
        RESEARCH / "financial_bounded_schedule.py",
    ]
    inputs = code + [
        ARCHIVE / name for name in ("summary.json", "gaussian_10.json", "gaussian_10.qasm")
    ]
    inputs += [
        ROOT / "research/limitation_audit_20261001/experiment_gaussian.py",
        ROOT / "research/controlled_completion_followup/synthesis_rotations.py",
        ROOT / "docs/controlled_completion_followup/FT_SYNTHESIS_AND_MODEL.md",
        ROOT / "docs/limitation_audit_20261001/implementation_plan/roadmap.json",
    ]
    a05 = PROGRAM / "A05_loading_run001"
    inputs += [
        a05 / name
        for name in (
            "protocol.json",
            "summary.json",
            "certificate.json",
            "manifest.json",
            "tests.xml",
        )
    ]
    a05_manifest = read(a05 / "manifest.json")
    for name in ("certificate.json", "summary.json"):
        path = a05 / name
        if sha(path) != a05_manifest["files"][relative(path)]:
            raise ValueError("Source A05 receipt integrity failed")
    numerical_package_files = []
    for module in (mp, pygridsynth):
        directory = Path(module.__file__).parent
        numerical_package_files += list(directory.rglob("*.py"))
    inputs += numerical_package_files + [Path(sys.executable)]
    frozen = {relative(path): sha(path) for path in sorted(set(inputs))}
    snapshot_dir = output / "executed_code"
    snapshot_dir.mkdir()
    executed = []
    for path in code:
        destination = snapshot_dir / path.name
        destination.write_bytes(path.read_bytes())
        executed.append(
            dict(
                original=relative(path),
                snapshot=destination.relative_to(output).as_posix(),
                sha256=sha(destination),
            )
        )
    create(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_tests_probabilities_angles_or_synthesis=True,
            executed_dependencies=executed,
            declared_tests=DECLARED_TESTS,
            archived_grid_bits=10,
            archived_cutoff_exact=[6, 1],
            fixed_boundaries_exact=[[-6, 1], [-3, 1], [0, 1], [3, 1], [6, 1]],
            fixed_prefix_levels=[0, 1],
            conditional_nodes=3,
            emitted_Walsh_rotations=3,
            exact_pi_half_Walsh_rotations=2,
            fixed_non_Clifford_targets=1,
            decimal_interval_precision=prefix.DPS,
            Machin_arctan_terms=prefix.PI_TERMS,
            integrated_exp_Taylor_degree=prefix.TAYLOR_DEGREE,
            monotone_sin_squared_bisections=prefix.BISECTION_STEPS,
            synthesis_midpoint_bits=prefix.MIDPOINT_BITS,
            loading_dollars_exact=prefix.pair(prefix.LOADING_DOLLARS),
            bounded_payoff_span_dollars_exact=prefix.pair(prefix.PAYOFF_SPAN),
            worst_case_scalar_factors=prefix.MAX_FACTORS,
            all_potential_full_tree_Walsh_rotations=prefix.ROTATIONS,
            per_rotation_operator_allowance_exact=prefix.pair(prefix.ROTATION_EPSILON),
            generator="pygridsynth",
            generator_version="1.1.0",
            mpmath_version=mp.__version__,
            pytest_version=importlib.metadata.version("pytest"),
            synthesis_calls_maximum=1,
            synthesis_fixed_seed=0,
            synthesis_requested_epsilon_exact=prefix.pair(prefix.ROTATION_EPSILON / 16),
            synthesis_diophantine_timeout=20,
            synthesis_factoring_timeout=5,
            synthesis_algorithm=(
                "one direct Rz(midpoint) gridsynth call; no shifted targets or retries"
            ),
            independent_whole_angle_and_full_four_dimensional_unitary_checks=True,
            process_CPU_limit_seconds=CPU_LIMIT,
            new_work_interrupt_CPU_seconds=ADMISSION_INTERRUPT_CPU,
            cleanup_CPU_reserve_seconds=CPU_LIMIT - ADMISSION_INTERRUPT_CPU,
            elapsed_wall_limit_seconds=WALL_LIMIT,
            numerical_package_source_paths=len(numerical_package_files),
            pure_product_refinement_used=False,
            full_table_angle_generation=False,
            full_loader_or_MPS_adoption=False,
            financial_law_change=False,
            financial_replays=0,
        ),
    )
    create(output / "frozen_inputs.json", frozen)
    verify(frozen)
    print(
        "A03 first-two-level prefix protocol frozen before tests or angle evaluations", flush=True
    )


def finish_manifest(output):
    create(
        output / "manifest.json",
        dict(
            files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            frozen_inputs=read(output / "frozen_inputs.json"),
            manifest_self_hash_excluded=True,
        ),
    )


def run(output):
    import pygridsynth
    import pygridsynth.ring as ring
    import pytest

    output = output.resolve()
    protocol = read(output / "protocol.json")
    frozen = read(output / "frozen_inputs.json")
    verify(frozen)
    if (output / "summary.json").exists():
        raise ValueError("An executed prospective receipt cannot be rerun")
    cpu_started, wall_started = time.process_time(), time.monotonic()
    stopped, interrupted = threading.Event(), threading.Event()

    def watchdog():
        while not stopped.wait(0.1):
            if (
                time.process_time() - cpu_started >= ADMISSION_INTERRUPT_CPU
                or time.monotonic() - wall_started >= WALL_LIMIT
            ):
                interrupted.set()
                _thread.interrupt_main()
                return

    thread = threading.Thread(target=watchdog, daemon=True)
    thread.start()
    passed, failure, tests, synthesis = False, None, None, None
    calls = 0
    try:
        rc = pytest.main(
            [
                str(RESEARCH / "test_gaussian_prefix_certificate.py"),
                "-q",
                "-p",
                "no:cacheprovider",
                "--junitxml=" + str(output / "tests.xml"),
            ]
        )
        suites = list(ET.parse(output / "tests.xml").getroot().iter("testsuite"))
        tests = {
            field: sum(int(s.attrib.get(field, 0)) for s in suites)
            for field in ("tests", "failures", "errors", "skipped")
        }
        if rc or tests != dict(tests=DECLARED_TESTS, failures=0, errors=0, skipped=0):
            raise AssertionError("Frozen prefix fixtures failed; no candidate synthesis admitted")
        a05 = read(PROGRAM / "A05_loading_run001/certificate.json")
        if not read(PROGRAM / "A05_loading_run001/summary.json")["passed"]:
            raise ValueError("Source A05 loading receipt failed")
        budget = prefix.budget_rows(a05["rows"])
        archive = read(ARCHIVE / "gaussian_10.json")
        if (
            archive["bits"] != 10
            or archive["cutoff"] != 6
            or Fraction(str(archive["grid_spacing"])) != Fraction(12, 1024)
        ):
            raise ValueError("Original q10 binned target metadata differs")
        counts = prefix.archive_counts((ARCHIVE / "gaussian_10.qasm").read_text(encoding="utf-8"))
        if counts["archived_operation_counts"] != archive["operations"]:
            raise ValueError("Actual full-QASM operations do not match the archived row")
        probability_angles = prefix.certificate()
        create(output / "prefix_probability_angles.json", probability_angles)
        create(output / "full_tree_and_budget.json", dict(counts=counts, rows=budget))
        spec = probability_angles["walsh_rotations"][2]
        enclosure = tuple(
            Fraction(*spec["angle_radians"][key]) for key in ("lower_exact", "upper_exact")
        )
        target = Fraction(*spec["synthesis_target_radians_exact"])
        archived_beta = Fraction("1.466830424129055")
        legacy_difference = max(abs(archived_beta - value) for value in enclosure)
        create(
            output / "archive_convention_binding.json",
            dict(
                ideal_archived_q10_target=(
                    "standard Gaussian binned on[-6,6], normalized by its mass"
                ),
                Ry_convention="Ry(theta)|0>=cos(theta/2)|0>+sin(theta/2)|1>",
                original_angle_convention="theta=2*acos(sqrt(left conditional mass))",
                q9_control_bit_is_MSB=True,
                q8_child_bit_is_next=True,
                Gray_Walsh_angles=["pi/2", "pi/2", "theta_left-pi/2"],
                archived_binary64_Walsh_value_exact=prefix.pair(archived_beta),
                archived_value_vs_certified_angle_absolute_difference_upper_exact=prefix.pair(
                    legacy_difference
                ),
                archived_float_precision_is_not_the_new_certificate=True,
                two_exact_Ry_pi_half_Clifford_execution=["z", "h"],
                Rz_to_Ry_execution="sdg, h, reverse Rz matrix-product string, h, s",
                complete_prefix_order="Ry(pi/2)q9; Ry(pi/2)q8; CX9,8; Ry(beta)q8; CX9,8",
                product_factor_structure=(
                    "A hypothetical loader uses a fresh|0^10> lane per scalar and offsets "
                    "every archived wire by10*i. All validated operations stay within0..9; "
                    "lanes are disjoint. Unitaires therefore tensor-factor and preserve purity. "
                    "No complete compiled loader or accepted paired-BM independence is asserted."
                ),
                hypothetical_product_structure_proved_from_lane_support=True,
                pure_product_refinement_used=False,
            ),
        )
        if time.process_time() - cpu_started >= ADMISSION_INTERRUPT_CPU:
            raise TimeoutError("CPU admission guard stopped the single synthesis call")
        mp.mp.dps = prefix.DPS
        ring.ntz = lambda n: 0 if n == 0 else (n & -n).bit_length() - 1
        random.seed(protocol["synthesis_fixed_seed"])
        before = time.process_time()
        calls += 1
        gates = pygridsynth.gridsynth_gates(
            mp.mpf(target.numerator) / target.denominator,
            mp.mpf(prefix.ROTATION_EPSILON.numerator) / prefix.ROTATION_EPSILON.denominator / 16,
            diophantine_timeout=protocol["synthesis_diophantine_timeout"],
            factoring_timeout=protocol["synthesis_factoring_timeout"],
        )
        synthesis = dict(
            fixed_seed=protocol["synthesis_fixed_seed"],
            matrix_product_gates=gates,
            synthesis_target_radians_exact=prefix.pair(target),
            generation_process_CPU_seconds=time.process_time() - before,
            T_count=gates.count("T"),
            synthesized_Rz_Clifford_count=sum(gates.count(token) for token in "HSX"),
            scalar_W_count=gates.count("W"),
            complete_prefix_CX_count=2,
            complete_prefix_single_qubit_Clifford_count=(
                sum(gates.count(token) for token in "HSX") + 8
            ),
            complete_prefix_Clifford_count=sum(gates.count(token) for token in "HSX") + 10,
            complete_prefix_T_count=gates.count("T"),
            complete_prefix_executed_gate_count=len(gates) - gates.count("W") + 10,
            full_loader_synthesis_T_count=None,
            full_loader_preparation_trace_error=None,
            completed_remaining_prefix_angle_certificates=None,
        )
        physical = [dict(gate=gate, wires=[wire]) for wire in (9, 8) for gate in ("z", "h")]
        physical.append(dict(gate="cx", wires=[9, 8]))
        physical += [dict(gate=gate, wires=[8]) for gate in ("sdg", "h")]
        token_gates = dict(H="h", T="t", S="s", X="x")
        physical += [
            dict(gate=token_gates[token], wires=[8]) for token in reversed(gates) if token != "W"
        ]
        physical += [dict(gate=gate, wires=[8]) for gate in ("h", "s")]
        physical.append(dict(gate="cx", wires=[9, 8]))
        synthesis["actual_prefix_execution_operations"] = physical
        synthesis["tracked_global_omega_power"] = gates.count("W") % 8
        if len(physical) != synthesis["complete_prefix_executed_gate_count"]:
            raise ValueError("Explicit execution string disagrees with prefix operation count")
        create(output / "synthesis_candidate.json", synthesis)
        checked = prefix.verify_string(enclosure, target, gates)
        create(output / "synthesis_interval_verification.json", checked)
        passed = True
    except BaseException as exception:
        failure = dict(
            type=type(exception).__name__,
            message=str(exception),
            budget_interrupt=interrupted.is_set(),
        )
        (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
    finally:
        stopped.set()
    elapsed_cpu, elapsed_wall = time.process_time() - cpu_started, time.monotonic() - wall_started
    unchanged = all(sha(ROOT / name) == expected for name, expected in frozen.items())
    passed = passed and unchanged and elapsed_cpu <= CPU_LIMIT and elapsed_wall <= WALL_LIMIT
    create(
        output / "summary.json",
        dict(
            passed=passed,
            local_only=True,
            tests=tests,
            failure=failure,
            frozen_inputs_unchanged=unchanged,
            elapsed_process_CPU_seconds=elapsed_cpu,
            elapsed_wall_seconds=elapsed_wall,
            synthesis_calls=calls,
            certified_conditional_nodes=3
            if (output / "prefix_probability_angles.json").exists()
            else 0,
            exact_Walsh_Clifford_rotations=2,
            synthesized_non_Clifford_Walsh_rotations=1 if synthesis else 0,
            complete_prefix_unitary_certified=(
                output / "synthesis_interval_verification.json"
            ).exists(),
            full_tree_potential_rotations=1023,
            remaining_uncertified_conditional_nodes=1020,
            full_loader_T_count=None,
            full_loader_preparation_trace_error=None,
            loading_law_adopted=False,
            MPS_adopted=False,
            full_continuous_price_certificate=False,
            full_physical_execution_certificate=False,
            financial_paths_or_gate_replays=0,
            current_price_ledger_changed=False,
        ),
    )
    finish_manifest(output)
    print(
        json.dumps(dict(passed=passed, tests=tests, synthesis_calls=calls, failure=failure)),
        flush=True,
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "A03_prefix_run001")
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output)
