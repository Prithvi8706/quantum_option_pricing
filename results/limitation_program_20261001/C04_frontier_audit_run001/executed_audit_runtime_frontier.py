"""Independent exact audit of six measured rows and twelve necessary rates."""

import argparse
import ast
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
PRODUCER = PROGRAM / "C04_frontier_run002"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path, decimal=False):
    return json.loads(path.read_text(encoding="utf-8"), parse_float=Decimal if decimal else float)


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def relative(path):
    return path.relative_to(ROOT).as_posix()


def exact(pair):
    result = Fraction(*pair)
    assert [result.numerator, result.denominator] == pair
    return result


def verify(frozen):
    assert all(digest(ROOT / name) == expected for name, expected in frozen.items())


def prepare(output):
    output = output.resolve()
    output.relative_to(PROGRAM)
    files = [Path(__file__).resolve()]
    for name in ("C04_frontier_run002", "C04_frontier_run001"):
        directory = PROGRAM / name
        files += [p for p in directory.rglob("*") if p.is_file()]
    files += [
        PROGRAM / "C09_audit_run001/summary.json",
        PROGRAM / "C09_audit_run001/manifest.json",
        PROGRAM / "H17_demand_run002/summary.json",
        PROGRAM / "H17_demand_run002/manifest.json",
        PROGRAM / "H17_demand_audit_run001/summary.json",
    ]
    files += [
        PROGRAM / "H17_demand_run002" / case / "hardware_demand.json" for case in ("B4x12", "B8x52")
    ]
    frozen = {relative(path): digest(path) for path in sorted(set(files))}
    output.mkdir()
    shutil.copy2(Path(__file__).resolve(), output / "executed_audit_runtime_frontier.py")
    create(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            before_independent_exact_audit=True,
            local_only=True,
            frozen_inputs=frozen,
            fixed_measured_rows=6,
            necessary_supply_rates=12,
            primary_decimal_receipt_values_converted_exactly=True,
            new_prices_gates_observations_tests=0,
            no_producer_function_imports=True,
            complete_runtime_and_advantage_claim=False,
        ),
    )


def run(output):
    protocol = read(output / "protocol.json")
    verify(protocol["frozen_inputs"])
    producer_manifest = read(PRODUCER / "manifest.json")
    verify(producer_manifest["files"])
    verify(producer_manifest["frozen_inputs"])
    comparison, summary = read(PRODUCER / "comparison.json"), read(PRODUCER / "summary.json")
    assert comparison == read(PROGRAM / "C04_frontier_run001/comparison.json")
    trees = [
        ast.dump(ast.parse((PROGRAM / name / script).read_text(encoding="utf-8")))
        for name, script in (
            ("C04_frontier_run001", "experiment_runtime_frontier.py"),
            ("C04_frontier_run002", "experiment_runtime_frontier_v2.py"),
        )
    ]
    assert trees[0] == trees[1]
    candidates = [
        row
        for row in read(PROGRAM / "C09_audit_run001/summary.json", True)["candidate_timing_rows"]
        if row["recorded_primary_convention"] == "measured confirmation"
    ]
    assert len(candidates) == len(comparison["rows"]) == 6
    audits = []
    for source, saved in zip(candidates, comparison["rows"]):
        assert source["scale"] == 1
        case = source["case"]
        demand = read(PROGRAM / "H17_demand_run002" / case / "hardware_demand.json")
        tc = Fraction(source["measured_median_wall_seconds"])
        assert tc == Fraction(source["recorded_primary_t_c_seconds"]) > 0
        assert saved["case"] == case and saved["classical_method"] == source["method"]
        assert exact(saved["measured_classical_wall_seconds_exact"]) == tc
        assert exact(saved["measured_classical_pooled_halfwidth_exact"]) == Fraction(
            source["pooled_hw16_dollars"]
        )
        epsilon = Fraction(source["epsilon_dollars"])
        assert exact(saved["classical_accuracy_target_dollars_exact"]) == epsilon
        assert saved["same_nominal_accuracy_target"] == (epsilon == Fraction(1, 100))
        assert saved["classical_n_run_per_scramble"] == source["actual_n_run_per_scramble"]
        nt = demand["consumed_T_states"]
        assert saved["complete_logical_T_state_demand"] == nt
        assert (
            saved["native_financial_subroutine_T_count_per_G_iteration"]
            == demand["source_batch_profile"]["financial_resources_per_iterate"]["t_count"]
        )
        one = exact(saved["conditional_required_accepted_T_states_per_second_onefold_exact"])
        ten = exact(saved["conditional_required_accepted_T_states_per_second_tenfold_exact"])
        assert one * tc == nt and ten * tc == 10 * nt and ten == 10 * one
        for field in (
            "source_only_quantum_seconds",
            "complete_quantum_seconds",
            "actual_complete_speedup_ratio",
            "actual_complete_slowdown_ratio",
            "actual_tenfold_budget_miss_ratio",
            "actual_onefold_reached",
            "actual_tenfold_reached",
        ):
            assert saved[field] is None
        for field in (
            "classical_full_coverage_qualification",
            "common_continuous_or_finite_input_law_certified",
            "comparable_complete_runtimes_available",
            "rate_is_measured_or_architecture_certified",
        ):
            assert not saved[field]
        assert saved["classical_evidence_is_measured_confirmation"]
        assert saved["supply_threshold_is_necessary_not_sufficient"]
        assert saved["logical_T_depth_is_not_physical_reaction_depth"]
        assert saved["tenfold_target_miss_does_not_imply_quantum_slowdown"]
        for pair, identity in zip(((2, 1), (2, 4), (20, 1)), saved["hypothetical_identity_checks"]):
            classical, quantum = pair
            speed = exact(identity["speedup_exact"])
            slow = exact(identity["slowdown_exact"])
            miss = exact(identity["tenfold_budget_miss_exact"])
            assert quantum * speed == classical and classical * slow == quantum
            assert speed * slow == 1 and miss == 10 * slow == 10 / speed
            assert identity["onefold_reached"] == (quantum <= classical)
            assert identity["tenfold_reached"] == (10 * quantum <= classical)
        assert len(saved["hypothetical_identity_checks"]) == 3
        audits.append(dict(case=case, method=source["method"], exact_rate_identities_passed=True))
    assert sum(row["same_nominal_accuracy_target"] for row in comparison["rows"]) == 4
    assert summary["passed"] and summary["measured_confirmation_rows"] == 6
    assert summary["conditional_supply_thresholds"] == 12
    assert (
        summary["same_nominal_accuracy_rows"] == 4 and summary["finer_classical_accuracy_rows"] == 2
    )
    assert summary["actual_complete_runtime_ratios_available"] == 0
    assert not summary["quantum_advantage_established"]
    verify(protocol["frozen_inputs"])
    create(
        output / "summary.json",
        dict(
            passed=True,
            local_only=True,
            independent_measured_rows_audited=6,
            independent_exact_necessary_supply_rates_audited=12,
            same_nominal_accuracy_rows=4,
            finer_accuracy_rows=2,
            preserved_v1_numerical_output_identical=True,
            v1_v2_AST_identical=True,
            actual_source_and_complete_runtime_and_ratios_null=True,
            complete_law_coverage_and_physical_qualifications_open=True,
            new_prices_gates_observations_tests=0,
            quantum_advantage_claim=False,
            rows=audits,
        ),
    )
    create(
        output / "manifest.json",
        dict(
            files={relative(path): digest(path) for path in output.rglob("*") if path.is_file()},
            frozen_inputs=protocol["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )
    print("C04 independent exact consistency audit PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "C04_frontier_audit_run001")
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output.resolve())
