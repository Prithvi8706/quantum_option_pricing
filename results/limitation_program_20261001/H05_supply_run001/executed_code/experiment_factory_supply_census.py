"""Freeze the two-method H05 comparison and conditional H06 interface census."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

from research.limitation_program_20261001 import factory_supply_census as factory


ROOT = factory.ROOT
RESEARCH = ROOT / "research/limitation_program_20261001"
PRIMARY = RESEARCH / "factory_census_primary_20261002"
DECLARED_TESTS = 18


def relative(path):
    return path.relative_to(ROOT).as_posix()


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def run(output):
    output = output.resolve()
    output.relative_to(factory.PROGRAM)
    output.mkdir(exist_ok=False)
    snapshots = output / "executed_code"
    snapshots.mkdir()
    code = [
        Path(__file__).resolve(),
        RESEARCH / "factory_supply_census.py",
        RESEARCH / "test_factory_supply_census.py",
    ]
    inputs = code + [path for path in PRIMARY.iterdir() if path.is_file()]
    inputs += [
        ROOT / "docs/limitation_audit_20261001/implementation_plan/roadmap.json",
        ROOT / "docs/limitation_audit_20261001/HARDWARE_AND_COST_MODEL.md",
    ]
    for name in ("H17_demand_run002", "H17_demand_audit_run001", "E02_IQFT_audit_run001"):
        folder = factory.PROGRAM / name
        manifest = factory.read(folder / "manifest.json")
        inputs += [folder / "manifest.json", folder / "summary.json", folder / "protocol.json"]
        if name == "H17_demand_run002":
            selected = [folder / case / "hardware_demand.json" for case in ("B4x12", "B8x52")]
        elif name == "E02_IQFT_audit_run001":
            selected = [folder / (case + "_IQFT_audit.json") for case in ("B4x12", "B8x52")]
        else:
            selected = []
        for path in selected:
            if factory.digest(path) != manifest["files"][relative(path)]:
                raise ValueError("Declared demand/audit input hash differs")
        inputs += selected
    frozen = {relative(path): factory.digest(path) for path in sorted(set(inputs))}
    executed = []
    for path in code:
        snapshot = snapshots / path.name
        snapshot.write_bytes(path.read_bytes())
        executed.append(
            dict(
                original=relative(path),
                snapshot=snapshot.relative_to(output).as_posix(),
                sha256=factory.digest(snapshot),
            )
        )
    create(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_meaningful_tests_and_census_expansion=True,
            executed_dependencies=executed,
            declared_tests=DECLARED_TESTS,
            H05_primary_demand_case="B4x12",
            H05_factory_methods=["15-to-1", "cultivation-with-escape"],
            H05_stop_rule=(
                "Two methods on one demand profile; absent finite matched output/noise "
                "makes physical supply conditional"
            ),
            H06_separate_interface_category="CCZ-and-catalysis-interface",
            actual_demand_companion_cases=["B4x12", "B8x52"],
            B8_physical_factory_comparison=False,
            fixed_ideal_raw_input_Z_error_exact=factory.pair(factory.RAW_Z_ERROR),
            fixed_maximum_cascade_levels=factory.LEVELS,
            fixed_upward_dyadic_enclosure_bits=factory.ENCLOSURE_BITS,
            fixed_ideal_eight_to_CCZ_input_Z_error_exact=factory.pair(factory.CCZ_INPUT_Z_ERROR),
            exact_all_orders_bound="binom(n,d)*p**d/(1-p)**n capped at1",
            denominator_proof="An error-free attempt is accepted; probability at least(1-p)**n",
            ideal_factory_Clifford_and_measurement_error_zero_is_assumption=True,
            successive_disjoint_independent_input_blocks_and_fresh_iid_retries_required=True,
            accepted_current_magic_failure_allowance_exact=[1, 1000],
            prospective_native_CCZ_and_residual_T_allowances_exact=[[1, 2000], [1, 2000]],
            catalytic_seed_conversion_storage_allocations=None,
            paper_modeled_output_errors_are_not_device_certificates=True,
            source_docs_and_public_primary_artifacts_frozen=True,
            publication_table_rates_or_footprints_adopted=False,
            physical_architecture_rows=0,
            no_C4_H8_cap_clock_rate_or_depth_transferred=True,
            new_factory_simulations_financial_prices_gate_replays=0,
        ),
    )
    create(output / "frozen_inputs.json", frozen)
    completed = subprocess.run(
        [
            str(ROOT / ".context/frontier_t0_env/Scripts/python.exe"),
            "-m",
            "pytest",
            "-q",
            str(RESEARCH / "test_factory_supply_census.py"),
            "--junitxml=" + str(output / "tests.xml"),
            "-p",
            "no:cacheprovider",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    (output / "pytest_stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (output / "pytest_stderr.txt").write_text(completed.stderr, encoding="utf-8")
    suites = list(ET.parse(output / "tests.xml").getroot().iter("testsuite"))
    tests = {
        field: sum(int(suite.attrib.get(field, 0)) for suite in suites)
        for field in ("tests", "failures", "errors", "skipped")
    }
    result, error = None, None
    if completed.returncode == 0:
        try:
            result = factory.census()
            create(output / "factory_census.json", result)
        except Exception as exception:
            error = dict(type=type(exception).__name__, message=str(exception))
            create(output / "census_error.json", error)
    unchanged = all(factory.digest(ROOT / name) == expected for name, expected in frozen.items())
    passed = (
        completed.returncode == 0
        and tests == dict(tests=DECLARED_TESTS, failures=0, errors=0, skipped=0)
        and result is not None
        and unchanged
    )
    create(
        output / "summary.json",
        dict(
            passed=passed,
            local_only=True,
            tests=tests,
            census_error=error,
            frozen_inputs_unchanged=unchanged,
            H05_factory_methods=2,
            H05_actual_compared_demand_profiles=1,
            H06_separate_conditional_interface_categories=1,
            primary_public_papers=3,
            retained_primary_HTML_artifacts=4,
            actual_H17_and_IQFT_demand_cases_bound=2,
            rigorous_finite_p_bounds_are_conditional_on_ideal_independent_Z_model=True,
            fixed_ideal_B4_cascade_target_reached_at_level=result["method_rows"][0][
                "fixed_ideal_input_Z_cascade"
            ]["first_fixed_level_meeting_target"]
            if result
            else None,
            published_model_quality_candidate_selected_for_future_mapping_only=True,
            physical_architectures_admitted=0,
            accepted_usable_state_delivery_rate=None,
            physical_factory_data_routing_capacity=None,
            executable_latency_seconds=None,
            complete_device_error_certificate=None,
            source_or_factory_runtime_advantage_claim=False,
            G5_closed=False,
            new_factory_simulations_financial_prices_gate_replays=0,
        ),
    )
    create(
        output / "manifest.json",
        dict(
            files={
                relative(path): factory.digest(path) for path in output.rglob("*") if path.is_file()
            },
            frozen_inputs=frozen,
            manifest_self_hash_excluded=True,
        ),
    )
    print(
        json.dumps(dict(passed=passed, tests=tests, error=error, physical_architectures_admitted=0))
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=factory.PROGRAM / "H05_supply_run001")
    run(parser.parse_args().output)
