"""Bounded same-target signed operand range multiplication integration, executed locally."""

import argparse
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
import shutil
import sys
import time

import pytest

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compact_parallel_v6 import (
    execute_compact_parallel,
    make_compact_schedule,
)
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.ir import evaluate

from research.limitation_program_20261001.constant_library import digest
from research.limitation_program_20261001.experiment_constants import changed_calls
from research.limitation_program_20261001.experiment_prefix_multiplier import (
    CASES,
    CPU_LIMIT_SECONDS,
    ROOT,
    ensure_cpu,
    read,
    save,
    verify_frozen,
)
from research.limitation_program_20261001.range_library import (
    RangeIntegrationLibrary,
    compile_range_graph,
)

VARIANTS = ("mixed40", "mixed24-40")
PORTFOLIOS = {"mixed40": (40, 72), "mixed24-40": (24, 40, 72)}


def label(variant):
    return variant


def dependencies():
    return [
        ROOT / name
        for name in (
            "research/limitation_program_20261001/experiment_range.py",
            "research/limitation_program_20261001/range_library.py",
            "research/limitation_program_20261001/prove_range_input.py",
            "research/controlled_source_completion/range_multiplier.py",
            "research/limitation_program_20261001/nonrestoring_library.py",
            "research/limitation_program_20261001/prove_nonrestoring_input.py",
            "research/controlled_source_completion/nonrestoring_sqrt.py",
            "research/limitation_program_20261001/shift_library.py",
            "research/limitation_program_20261001/prove_shift_input.py",
            "research/controlled_source_completion/narrow_shift.py",
            "research/controlled_source_completion/prefix_multiplier.py",
            "research/controlled_source_completion/carry_lookahead.py",
            "research/limitation_program_20261001/prove_square_input.py",
            "research/controlled_source_completion/signed_square.py",
            "research/limitation_program_20261001/sqrt_library.py",
            "research/limitation_program_20261001/prove_sqrt_input.py",
            "research/limitation_program_20261001/test_range_integration.py",
            "research/controlled_source_completion/narrow_sqrt.py",
            "research/controlled_source_completion/compact_parallel_v6.py",
            "research/limitation_program_20261001/interval_bounds.py",
            "research/limitation_program_20261001/constant_library.py",
            "research/limitation_program_20261001/prove_log_exponent.py",
            "research/limitation_program_20261001/experiment_prefix_multiplier.py",
            "research/limitation_program_20261001/experiment_constants.py",
            "research/controlled_source_completion/compact_parallel.py",
            "research/controlled_source_completion/compact_storage.py",
            "research/controlled_source_completion/compiler.py",
            "research/controlled_source_completion/primitives.py",
            "research/controlled_source_completion/exact_lookup.py",
            "research/controlled_source_completion/constant_multiplier.py",
            "research/controlled_source_completion/log_constant_multiplier.py",
            "research/controlled_priority_completion/parallel_source.py",
            "research/controlled_source_completion/ir.py",
            "research/antithetic_feasibility/reversible.py",
            "research/journal_sprint/reversible_fixed_point.py",
        )
    ]


def prepare(source_root, leaf_root, output):
    baseline_summary, leaf_summary = (
        read(source_root / "summary.json"),
        read(leaf_root / "summary.json"),
    )
    if (
        not baseline_summary["passed"]
        or not baseline_summary["accepted"]
        or not leaf_summary["passed"]
        or not leaf_summary["source_screen_allowed"]
    ):
        raise ValueError("verified accepted source and exact leaf receipts required")
    output.relative_to((ROOT / "results/limitation_program_20261001").resolve())
    output.mkdir(parents=True, exist_ok=False)
    baseline_hashes = {"summary.json": digest(source_root / "summary.json")}
    baseline_leaves = {}
    for name in CASES:
        for filename in ("target.json", "source.json", "schedule_capped.json"):
            baseline_hashes[name + "/" + filename] = digest(source_root / name / filename)
        source = read(source_root / name / "source.json")
        archive = resolve_library(source)
        for key, entry in entries(source).items():
            for path in (archive / (key + ".json"), archive / entry["gate_file"]):
                baseline_leaves[str(path.relative_to(ROOT))] = digest(path)
            if digest(archive / entry["gate_file"]) != entry["sha256"]:
                raise ValueError("accepted baseline gate SHA mismatch")
    frozen = []
    for path in dependencies():
        snapshot = output / "executed_code" / path.name
        snapshot.parent.mkdir(exist_ok=True)
        shutil.copy2(path, snapshot)
        frozen.append(
            {
                "source": str(path.relative_to(ROOT)),
                "snapshot": str(snapshot.relative_to(output)),
                "sha256": digest(snapshot),
            }
        )
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "local_only": True,
        "item": "A09 proved signed-width multiplication",
        "baseline": str(source_root.relative_to(ROOT)),
        "leaf_receipt": str(leaf_root.relative_to(ROOT)),
        "leaf_receipt_manifest_sha256": digest(leaf_root / "manifest.json"),
        "family": [label(variant) for variant in VARIANTS],
        "width": 72,
        "fraction_bits": 40,
        "active_widths": [24, 40, 72],
        "allowed_pairs": [
            c["active_bits"] for c in leaf_summary["candidates"] if c["source_screen_allowed"]
        ],
        "portfolios": {name: list(bits) for name, bits in PORTFOLIOS.items()},
        "semantics": "Exact native two72 inputs and arbitrary72 output XOR floor(signed(a)*signed(b)/2^40) mod2^72; retain low carries, full112-bit modular sign extension and literal inverse cleanup.",
        "guard": "Immutable actual target/call binding; prove both complete signed SSA intervals fit each selected active width. Choose minimum declared bin per operand; skip72x72 and leaf-ineligible pairs. Every other leaf retains accepted metadata and actual gate bytes.",
        "tests": "Frozen exact leaf receipt plus independent integration tests before "
        "source screening; full financial replay remains required for adoption.",
        "threshold_percent": 2,
        "cases": list(CASES),
        "eligibility": "One variant must reduce capped full-source T-depth by at least2% "
        "for both cases, CT-depth<=baseline and actual qubits<=current cap. The clean leaf "
        "must improve T work or scratch. SSA storage widths and copy accounting stay identical.",
        "selection": "Minimum sum of both-case T-depth, then T count and actual qubits; "
        "ties retain declared variant order; a portfolio dominated across all four resource dimensions in both cases cannot be selected",
        "replays_on_pass": "Selected eligible nondominated portfolio only, all four previously frozen "
        "accepted non-restoring-source case vectors with arbitrary nonzero72-bit output XOR "
        "and complete cleanup",
        "replay_inputs": {case["case"]: case["replays"] for case in baseline_summary["cases"]},
        "stop_rule": "One exact signed CSA/Brent-Kung family, three widths24/40/72 and two portfolios only; "
        "no replay if both-case "
        "threshold fails; no candidate adopted on a semantic failure;30 process CPU minutes",
        "cpu_limit_seconds": CPU_LIMIT_SECONDS,
        "unchanged": "Financial target bytes/input law/precision, all non-specialized leaves including "
        "accepted unsigned46 non-restoring roots and signed7 shifts, "
        "32-row coefficient lookup, old modules and original compact masks",
        "exclusions": "Continuous-dollar error, phase estimation, matched classical timings "
        "and physical advantage remain unproved; G2-G5 stay open",
        "executed_dependencies": frozen,
        "baseline_hashes": baseline_hashes,
        "baseline_leaf_hashes": baseline_leaves,
        "environment": {
            "python": sys.version,
            "executable": sys.executable,
            "executable_sha256": digest(Path(sys.executable)),
            "packages": {name: version(name) for name in ("numpy", "numba", "pytest")},
        },
    }
    save(output / "protocol.json", protocol)
    return protocol, baseline_summary


def source_screen(source_root, output, started, allowed_pairs, leaf_root):
    cases = []
    for name in CASES:
        target, original = (
            read(source_root / name / "target.json"),
            read(source_root / name / "source.json"),
        )
        baseline_schedule = read(source_root / name / "schedule_capped.json")
        baseline, trials = baseline_schedule["resources"], []
        for variant in VARIANTS:
            ensure_cpu(started)
            name_variant = label(variant)
            directory = output / name / name_variant
            library = RangeIntegrationLibrary(
                directory / "leaves",
                target,
                original,
                allowed_bits=PORTFOLIOS[variant],
                eligible_pairs=[
                    pair
                    for pair in allowed_pairs
                    if all(bits in PORTFOLIOS[variant] for bits in pair)
                ],
            )
            source, _ = compile_range_graph(target, directory, library)
            shutil.copy2(source_root / name / "target.json", directory / "target.json")
            attribution = changed_calls(original, source)
            expected = sum(row["type"] != "fallback" for row in library.decisions)
            if len(attribution["changes"]) != expected or any(
                row["op"] != "mul" for row in attribution["changes"]
            ):
                raise AssertionError(
                    "Only both-proved signed operand multiplication sites may change"
                )
            standalone = {
                tuple(row["active_bits"]): row["metadata"]["sha256"]
                for row in read(leaf_root / "summary.json")["candidates"]
            }
            for entry in entries(source).values():
                contract = entry.get("input_contract", {})
                if (
                    "signed_operand_bits" in contract
                    and entry["sha256"] != standalone[tuple(contract["signed_operand_bits"])]
                ):
                    raise AssertionError(
                        "Integrated range gate bytes differ from tested standalone leaf"
                    )
            save(directory / "changed_calls.json", attribution)
            save(directory / "site_decisions.json", library.decisions)
            schedule = make_compact_schedule(target, source, baseline["logical_qubits"])
            for field in (
                "widths",
                "offsets",
                "retained_ssa_qubits",
                "proof_masks",
                "proof_reasons",
                "argument_and_output_copy_cx",
                "baseline_argument_and_output_copy_cx",
            ):
                if schedule[field] != baseline_schedule[field]:
                    raise AssertionError(
                        "Multiplier range experiment must not claim new storage/copy savings"
                    )
            save(directory / "schedule_capped.json", schedule)
            observed = schedule["resources"]
            leaf_improved = bool(attribution["changes"]) and all(
                row["new_resources"]["t_count"] < row["old_resources"]["t_count"]
                or row["new_resources"]["qubits"] < row["old_resources"]["qubits"]
                for row in attribution["changes"]
            )
            eligible = (
                100 * observed["t_depth"] <= 98 * baseline["t_depth"]
                and observed["logical_qubits"] <= baseline["logical_qubits"]
                and observed["clifford_t_depth"] <= baseline["clifford_t_depth"]
                and leaf_improved
            )
            row = {
                "variant": name_variant,
                "resources": observed,
                "eligible": eligible,
                "full_t_depth_gain_percent": 100 * (1 - observed["t_depth"] / baseline["t_depth"]),
                "t_count_change": observed["t_count"] - baseline["t_count"],
                "t_count_change_percent": 100 * (observed["t_count"] / baseline["t_count"] - 1),
                "batches": len(schedule["groups"]),
                "changed_calls": expected,
                "target_bytes_unchanged": True,
                "ssa_storage_and_copy_accounting_unchanged": True,
                "fallback_metadata_and_gate_bytes_unchanged": True,
                "clean_leaf_work_or_scratch_improved": leaf_improved,
            }
            trials.append(row)
            print(
                name,
                name_variant,
                "T-depth",
                observed["t_depth"],
                "gain%",
                round(row["full_t_depth_gain_percent"], 4),
                "eligible",
                eligible,
                flush=True,
            )
            save(output / name / "screen.json", trials)
        cases.append(
            {
                "case": name,
                "baseline": baseline,
                "trials": trials,
                "accepted": False,
                "replay_passed": False,
                "replays": [],
            }
        )
    return cases


def replay(output, baseline_summary, cases, selected, started):
    for case in cases:
        name, directory = case["case"], output / case["case"] / selected
        target, source, schedule = (
            read(directory / filename)
            for filename in ("target.json", "source.json", "schedule_capped.json")
        )
        trial = next(row for row in case["trials"] if row["variant"] == selected)
        case.update(selected=trial, candidate=trial["resources"])
        prior = next(row for row in baseline_summary["cases"] if row["case"] == name)
        initial = {key: int("a5" * 9, 16) for key in source["outputs"]}
        for sample in prior["replays"]:
            ensure_cpu(started)
            wall_started = time.perf_counter()
            _, trace = evaluate(target, sample["inputs"], True)
            expected = {
                key: trace[value] ^ initial[key] for key, value in source["outputs"].items()
            }
            actual = execute_compact_parallel(target, source, schedule, sample["inputs"], initial)
            if actual["values"] != expected or not actual["all_input_and_workspace_bits_restored"]:
                raise AssertionError("Full financial signed range multiplier gate replay failed")
            case["replays"].append(
                {
                    "label": sample["label"],
                    "inputs": sample["inputs"],
                    "initial": initial,
                    "expected": expected,
                    "actual": actual,
                    "passed": True,
                    "seconds": time.perf_counter() - wall_started,
                }
            )
            save(output / name / "comparison.json", case)
            print(name, selected, sample["label"], "complete gate replay PASS", flush=True)
        for filename in ("target.json", "source.json", "schedule_capped.json"):
            shutil.copy2(directory / filename, output / name / filename)
        case.update(accepted=True, replay_passed=True)
        save(output / name / "comparison.json", case)


def run(source_root, leaf_root, output):
    source_root, leaf_root, output = source_root.resolve(), leaf_root.resolve(), output.resolve()
    wall_started, cpu_started = time.perf_counter(), time.process_time()
    protocol, baseline_summary = prepare(source_root, leaf_root, output)
    print("Prospective signed range multiplier source protocol and snapshots saved", flush=True)
    try:
        exit_code = pytest.main(
            [
                str(ROOT / "research/limitation_program_20261001/test_range_integration.py"),
                "-q",
                "--junitxml=" + str(output / "integration_tests.xml"),
            ]
        )
        if exit_code:
            raise AssertionError("Independent signed range multiplier integration tests failed")
        ensure_cpu(cpu_started)
        cases = source_screen(
            source_root, output, cpu_started, protocol["allowed_pairs"], leaf_root
        )
        eligible = [
            label(variant)
            for variant in VARIANTS
            if all(
                next(row for row in case["trials"] if row["variant"] == label(variant))["eligible"]
                for case in cases
            )
        ]

        # Declare and reconcile complete-source Pareto eligibility before selection.
        def dominates(left, right):
            dimensions = ("t_count", "t_depth", "clifford_t_depth", "logical_qubits")
            comparisons = [
                (
                    next(r for r in c["trials"] if r["variant"] == left)["resources"][field],
                    next(r for r in c["trials"] if r["variant"] == right)["resources"][field],
                )
                for c in cases
                for field in dimensions
            ]
            return all(a <= b for a, b in comparisons) and any(a < b for a, b in comparisons)

        nondominated = [
            v for v in VARIANTS if not any(dominates(other, v) for other in VARIANTS if other != v)
        ]
        for case in cases:
            for row in case["trials"]:
                row["source_nondominated"] = row["variant"] in nondominated
            save(output / case["case"] / "screen.json", case["trials"])
        eligible = [v for v in eligible if v in nondominated]
        selected = (
            min(
                eligible,
                key=lambda variant: tuple(
                    sum(
                        next(row for row in case["trials"] if row["variant"] == variant)[
                            "resources"
                        ][field]
                        for case in cases
                    )
                    for field in ("t_depth", "t_count", "logical_qubits")
                ),
            )
            if eligible
            else None
        )
        if selected:
            replay(output, baseline_summary, cases, selected, cpu_started)
        else:
            for case in cases:
                save(output / case["case"] / "comparison.json", case)
        verify_frozen(source_root, output, protocol)
        if digest(leaf_root / "manifest.json") != protocol["leaf_receipt_manifest_sha256"]:
            raise AssertionError("Exact leaf receipt changed after protocol freeze")
        ensure_cpu(cpu_started)
        accepted = selected is not None and all(case["accepted"] for case in cases)
        result = {
            "passed": True,
            "accepted": accepted,
            "selected": selected,
            "cases": cases,
            "decision": "Exact signed range multiplication passes both-case source threshold and replays"
            if accepted
            else "No eligible exact both-case source gain; accepted non-restoring baseline retained",
            "financial_gate_replays_run": selected is not None,
            "leaf_candidates": len(read(leaf_root / "summary.json")["candidates"]),
            "source_portfolios": len(VARIANTS),
            "financial_function_changed": False,
            "precision_or_input_law_changed": False,
            "new_external_input_promise": False,
            "internal_both_signed_operand_promises_proved_at_actual_sites": True,
            "ssa_storage_or_copy_savings_claimed": False,
            "gates_G2_to_G5_closed": False,
            "seconds": time.perf_counter() - wall_started,
            "cpu_seconds": time.process_time() - cpu_started,
        }
        save(output / "summary.json", result)
        save(output / "result.json", result)
        save(
            output / "range_semantics.json",
            dict(
                integer_function="out XOR floor(signed(a)*signed(b)/2^40) mod2^72",
                external_width=72,
                fraction_bits=40,
                active_widths=[24, 40, 72],
                native_argument_count=2,
                full_native_output_xor_bits=72,
                both_actual_operand_sign_extension_guards=True,
                low_carry_columns_retained=True,
                full112_bit_sign_correction=True,
                input_and_workspace_restored=True,
            ),
        )
        save(
            output / "range_frontier.json",
            dict(
                selected=selected,
                cases=cases,
                variants=list(VARIANTS),
                nondominated=nondominated,
                measured_at_current_caps=True,
                storage_and_copy_model_unchanged=True,
                A09_entire_limitation_closed=False,
                no_adoption_if_depth_threshold_fails=True,
            ),
        )
        save(
            output / "verification.json",
            {
                "passed": True,
                "pytest_exit_code": int(exit_code),
                "prospective_protocol_before_source_tests_and_screens": True,
                "baseline_target_source_schedule_and_leaves_unchanged": True,
                "executed_dependencies_and_snapshots_unchanged": True,
                "financial_replay_count": sum(len(case["replays"]) for case in cases),
                "full_output_xor_and_input_workspace_cleanup": accepted,
                "same_target_all_pattern_both_signed_operand_guards": True,
            },
        )
        (output / "NEXT.md").write_text(
            "Reconcile the range multiplier source and unchanged storage. Keep G2-G5 open. "
            "Then select the next dominant arithmetic limitation from the measured schedule.\n",
            encoding="utf-8",
        )
    except Exception as error:
        save(
            output / "failure.json",
            {
                "passed": False,
                "type": type(error).__name__,
                "message": str(error),
                "seconds": time.perf_counter() - wall_started,
                "cpu_seconds": time.process_time() - cpu_started,
            },
        )
        save(
            output / "manifest.json",
            {
                str(path.relative_to(output)): digest(path)
                for path in output.rglob("*")
                if path.is_file() and path.name != "manifest.json"
            },
        )
        raise
    save(
        output / "manifest.json",
        {
            str(path.relative_to(output)): digest(path)
            for path in output.rglob("*")
            if path.is_file() and path.name != "manifest.json"
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--leaf-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    run(args.source_root, args.leaf_root, args.output)
