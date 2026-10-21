"""Freeze eight controller settings and two exact tiny laws before observations."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import time

from research.limitation_program_20261001 import finite_iqae_controller as controller


ROOT = controller.ROOT
RESEARCH = ROOT / "research/limitation_program_20261001"
DECLARED_TESTS = 18
BASE_SEED = 20261002


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def run(directory):
    directory = directory.resolve()
    if not directory.is_relative_to(ROOT):
        raise ValueError("Local workspace receipt required")
    directory.mkdir(parents=True, exist_ok=False)
    executed = directory / "executed_code"
    executed.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "finite_iqae_controller.py",
        RESEARCH / "test_finite_iqae_controller.py",
        RESEARCH / "audit_barrier_band.py",
    ]
    inputs = []
    for name in (
        "E04_theorem_run001",
        "E07_schedule_run001",
        "E02_financial_run002",
        "E02_IQFT_run001",
        "E02_IQFT_audit_run001",
    ):
        historical = controller.RESULTS / name
        if controller.audit.read(historical / "summary.json")["passed"] is not True:
            raise ValueError("Passed source/controller prerequisite required")
        inputs += [p for p in historical.rglob("*") if p.is_file()]
        inputs += [
            ROOT / name
            for name in controller.audit.read(historical / "manifest.json")["frozen_inputs"]
        ]
    frozen = {
        p.relative_to(ROOT).as_posix(): controller.audit.sha(p) for p in sorted(set(code + inputs))
    }
    snapshots = []
    for path in code:
        snapshot = executed / path.name
        snapshot.write_bytes(path.read_bytes())
        snapshots.append(
            dict(
                original=path.relative_to(ROOT).as_posix(),
                snapshot=snapshot.relative_to(directory).as_posix(),
                sha256=controller.audit.sha(snapshot),
            )
        )
    create(
        directory / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            item="E04 finite confidence-spending controller adapters",
            before_meaningful_tests_and_toy_observations=True,
            executed_dependencies=snapshots,
            declared_tests=DECLARED_TESTS,
            span_dollars=64,
            error_dollars_exact=[9, 2000],
            amplitude_error_exact=[9, 128000],
            ideal_failure_exact=[3, 1000],
            retained_canonical_Q_calls=983025,
            settings=list(controller.SETTINGS),
            setting_count=8,
            exact_toy_laws=list(controller.TOY_LAWS),
            law_count=2,
            replicates_per_setting_law=1,
            total_controller_attempts=16,
            seed_rule="20261002+2*setting_index+law_index",
            base_seed=BASE_SEED,
            max_admitted_rounds=controller.MAX_ROUNDS,
            max_fresh_looks_per_round=controller.MAX_LOOKS_PER_ROUND,
            max_Q_plus_terminal_clean_pairs_per_attempt=controller.MAX_PAID_SOURCE_PAIRS,
            max_power_search_events_per_attempt=controller.MAX_POWER_SEARCH_EVENTS,
            inversion_bisections=controller.INVERSE_BISECTIONS,
            interval_digits=controller.IV_DIGITS,
            proof=controller.PROOF,
            preparation_and_terminal_marking_cleanup_paid=True,
            paper_native_controller_or_query_bound_automatically_transferred=False,
            stop_rule=(
                "Exactly eight declared settings on the two declared laws. "
                "Preserve every non-delivery; no tuning or extra laws."
            ),
            coverage_is_simultaneous_for_delivered_intervals=True,
            uniform_financial_delivery_within_budget_proved=False,
            future_finance_requires_independent_controller_cost_and_delivery_audit=True,
            financial_samples_or_gate_replays=0,
            quantum_circuit_jobs=0,
            full_G2_and_physical_runtime_certificates=False,
        ),
    )
    create(directory / "frozen_inputs.json", frozen)
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_finite_iqae_controller.py"),
            "--junitxml=" + str(directory / "tests.xml"),
            "-p",
            "no:cacheprovider",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    (directory / "pytest_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (directory / "pytest_stderr.txt").write_text(completed.stderr, encoding="utf-8")
    tests = controller.audit.xml_counts(directory / "tests.xml")
    wrapper_path = controller.RESULTS / "E02_financial_run002/B4x12/iterate.json"
    baseline_path = controller.RESULTS / "E02_IQFT_run001/B4x12/synthesized_estimator_ledger.json"
    rows, error = [], None
    started = time.process_time()
    if completed.returncode == 0:
        try:
            wrapper, baseline = (
                controller.audit.read(wrapper_path),
                controller.audit.read(baseline_path),
            )
            create(
                directory / "source_cost_binding.json",
                dict(
                    wrapper=dict(path=str(wrapper_path), sha256=controller.audit.sha(wrapper_path)),
                    canonical_synthesized_ledger=dict(
                        path=str(baseline_path), sha256=controller.audit.sha(baseline_path)
                    ),
                    source_pinned_active_control=True,
                    uniform_random_bits=len(wrapper["random_wires"]),
                    Q_resources=wrapper["resources"],
                    terminal_financial_both_directions=wrapper["financial_resources"],
                    terminal_selector_directions=wrapper["selector_costs"],
                    terminal_flag_measurement_then_literal_inverse=True,
                ),
            )
            for setting_index, setting in enumerate(controller.SETTINGS):
                for law_index, law in enumerate(controller.TOY_LAWS):
                    seed = BASE_SEED + 2 * setting_index + law_index
                    observer = controller.ExactToyObserver(Fraction(*law["amplitude_exact"]), seed)
                    result = controller.controller(observer, setting)
                    result.update(
                        setting_index=setting_index,
                        law_index=law_index,
                        law=law,
                        seed=seed,
                        observation_model="exact-binomial rational Grover toy",
                        quantum_circuit_jobs=0,
                        conditional_original_financial_cost=controller.conditional_financial_cost(
                            result, wrapper, baseline
                        ),
                    )
                    covered = None
                    if result["status"] == "delivered":
                        lo, hi = map(controller.audit.exact, result["amplitude_interval_exact"])
                        covered = lo <= Fraction(*law["amplitude_exact"]) <= hi
                    result["toy_ground_truth_in_delivered_interval"] = covered
                    filename = f"setting{setting_index:02d}_law{law_index}.json"
                    create(directory / filename, result)
                    rows.append(
                        dict(
                            file=filename,
                            family=setting["family"],
                            first_batch_shots=setting["first_batch_shots"],
                            law=law["name"],
                            status=result["status"],
                            stop_reason=result["stop_reason"],
                            batches=result["admitted_batches"],
                            total_Q_calls=result["total_Q_calls"],
                            terminal_clean_pairs=result["total_terminal_F_selector_clean_pairs"],
                            paid_source_pairs=result["paid_source_pairs"],
                            toy_ground_truth_in_delivered_interval=covered,
                            conditional_logical_T_count=result[
                                "conditional_original_financial_cost"
                            ]["logical_T_count"],
                            conditional_logical_T_depth=result[
                                "conditional_original_financial_cost"
                            ]["logical_serial_unitary_T_depth"],
                            toy_delivered_with_lower_conditional_logical_work=result[
                                "conditional_original_financial_cost"
                            ]["toy_delivered_and_conditional_logical_T_work_below_canonical"],
                        )
                    )
                    print(json.dumps(rows[-1]), flush=True)
        except Exception as exception:
            error = dict(type=type(exception).__name__, message=str(exception))
            create(directory / "controller_error.json", error)
    unchanged = all(controller.audit.sha(ROOT / name) == digest for name, digest in frozen.items())
    passed = (
        completed.returncode == 0
        and tests == dict(tests=DECLARED_TESTS, failures=0, errors=0, skipped=0)
        and len(rows) == 16
        and error is None
        and unchanged
    )
    create(
        directory / "summary.json",
        dict(
            passed=passed,
            tests=tests,
            controller_error=error,
            frozen_inputs_unchanged=unchanged,
            historical_receipts_unchanged=unchanged,
            local_only=True,
            settings=8,
            exact_toy_laws=2,
            controller_attempts=len(rows),
            rows=rows,
            delivered=sum(row["status"] == "delivered" for row in rows),
            censored=sum(row["status"] != "delivered" for row in rows),
            elapsed_controller_cpu_seconds=time.process_time() - started,
            uniform_financial_delivery_within_budget_proved=False,
            financial_controller_cost_measured=False,
            financial_samples_or_gate_replays=0,
            quantum_circuit_jobs=0,
            full_G2_closed=False,
            physical_latency_certified=False,
            next=(
                "Independent simultaneous-coverage/branch/budget/full source-cost audit "
                "before considering any actual financial observation adapter"
            ),
        ),
    )
    create(
        directory / "manifest.json",
        dict(
            files={
                p.relative_to(ROOT).as_posix(): controller.audit.sha(p)
                for p in sorted(directory.rglob("*"))
                if p.is_file()
            },
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
        ),
    )
    print(json.dumps(dict(passed=passed, tests=tests, error=error, attempts=len(rows))))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=controller.RESULTS / "E04_controller_run001")
    run(parser.parse_args().output)
