"""Read-only Stage C handoff inspection; no new statistical or timing runs.

Capture completed coverage and explicitly partial timing evidence. Observed
live files may legitimately evolve; their immutable snapshots are the inputs.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
CLASSICAL = ROOT / "results/frontier_classical_20261001"
SPEC = "manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md"
LOCK = "research/frontier_replay_20261001/t0_requirements.lock"
STATUS = "manuscript/advantage-frontier-2026-09-23/STAGE_C_STATUS.md"


def sha_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def create(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def prepare(output):
    output.relative_to(PROGRAM)
    assert not output.exists()
    paths = list((CLASSICAL / "c4").glob("*"))
    paths += list((CLASSICAL / "c4_score").glob("*"))
    paths += [CLASSICAL / "c3_refa/ref_a.json", CLASSICAL / "c3_refb/B4x12/ref_b.json",
              CLASSICAL / "c3_refb/B8x52/ref_b.json", CLASSICAL / "c2/c2_timing.json",
              CLASSICAL / "decision_interim_v2/decision_interim.json",
              CLASSICAL / "c5/timing/c5_timing.json", CLASSICAL / "c5/timing/meta.json",
              CLASSICAL / "c7/oracle_d12/c7_oracle.json", ROOT / SPEC, ROOT / LOCK,
              ROOT / STATUS]
    output.mkdir()
    observations = []
    frozen = {relative(Path(__file__)): sha(Path(__file__)),
              relative(Path(sys.executable)): sha(Path(sys.executable))}
    shutil.copy2(Path(__file__), output / Path(__file__).name)
    for source in paths:
        assert source.is_file()
        data = source.read_bytes()
        destination = output / "snapshots" / relative(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        expected = sha_bytes(data)
        assert sha(destination) == expected
        frozen[relative(destination)] = expected
        observations.append(dict(live_path=relative(source), snapshot=relative(destination),
                                 observed_sha256=expected))
    create(output / "protocol.json", dict(
        created_utc=datetime.now(timezone.utc).isoformat(), local_only=True,
        before_interpreting_snapshots=True, frozen_inputs=frozen,
        observations=observations, live_files_are_observations_not_future_hash_requirements=True,
        fixed_inspection=(
            "Completed C4 arms/score, unchanged C2, partial C5, D12 and interim decision"
        ),
        statistical_recomputation=False, new_tests_or_timing_or_price_runs=0,
        score_method_certification=False, CPU_limit_seconds=60,
    ))


def observed(output, name):
    return output / "snapshots" / name


def classical(output, name):
    return observed(output, "results/frontier_classical_20261001/" + name)


def inspect(output):
    started = time.process_time()
    protocol = read(output / "protocol.json")
    for name, expected in protocol["frozen_inputs"].items():
        assert sha(ROOT / name) == expected
    raw = read(classical(output, "c4/c4_raw.json"))
    score = read(classical(output, "c4_score/c4_coverage.json"))
    assert raw["replications"] == 1000 and raw["scrambles"] == 16
    assert raw["levels"] == [10, 11, 12, 13]
    assert set(raw["seconds"]) == {"B4x12", "B8x52", "B4x12_2^17"}
    cases = {}
    for name, expected_levels in (("B4x12", {"1024", "2048", "4096", "8192", "131072"}),
                                  ("B8x52", {"1024", "2048", "4096", "8192"})):
        saved = score["cases"][name]
        assert set(saved["weighted"]) == expected_levels
        check = saved["primary_check"]
        cell = saved["weighted"]["8192"]["0.99"]
        assert check["raw_99_at_8192"] == cell["raw"]
        assert check["under_covering"] == (cell["raw_cp_bonferroni"][1] < 0.99)
        assert check["under_covering"] is False and check["c"] is None
        cases[name] = dict(primary_check=check,
                           primary_saved_Bonferroni_interval=cell["raw_cp_bonferroni"],
                           observed_99_coverage_by_n={n: v["0.99"]["raw"]
                                                     for n, v in saved["weighted"].items()},
                           weighted_reference=score["references"][name],
                           all_input_99_confidence_theorem=False)
    provenance_rows = []
    for phase in ("c4", "c4_score"):
        meta = read(classical(output, phase + "/meta.json"))
        assert meta["dirty"] is False and meta["root"] == 2026100141
        bindings = {"research/frontier_classical_20261001/" + k: v
                    for k, v in meta["code_sha256"].items()}
        bindings.update({SPEC: meta["spec_sha256"], LOCK: meta["lock_sha256"]})
        for path, expected in bindings.items():
            blob = subprocess.run(["git", "show", meta["commit"] + ":" + path],
                                  cwd=ROOT, check=True, capture_output=True).stdout
            candidates = {"Git_blob": blob, "Git_LF_to_CRLF": blob.replace(b"\n", b"\r\n")}
            matches = [label for label, data in candidates.items() if sha_bytes(data) == expected]
            assert matches, (phase, path, "recorded bytes do not match recorded commit")
            data = candidates[matches[0]]
            destination = output / "commit_bindings" / phase / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            provenance_rows.append(dict(phase=phase, path=path, commit=meta["commit"],
                                        representation=matches[0], sha256=expected))
    current_c2 = classical(output, "c2/c2_timing.json").read_bytes()
    earlier = (
        PROGRAM / "C09_audit_run001/snapshots/results/frontier_classical_20261001"
        / "c2/c2_timing.json"
    )
    assert current_c2 == earlier.read_bytes()
    partial = read(classical(output, "c5/timing/c5_timing.json"))
    expected_blocks = {case + "/" + method for case in ("B4x12", "B8x52")
                       for method in ("oss_bb", "oss")}
    blocks = partial["blocks"]
    assert set(blocks) <= expected_blocks
    timing_rows = {name: value["t_c"] for name, value in blocks.items()}
    create(output / "stage_c_observations.json", dict(
        coverage_arms_completed=True, primary_undercoverage_triggered=False, cases=cases,
        C2_byte_identical_to_original_C09_snapshot=True,
        C5_observed_blocks=sorted(blocks), C5_expected_blocks=sorted(expected_blocks),
        C5_all_blocks_present=set(blocks) == expected_blocks,
        C5_completion_not_inferred_from_file_existence=True, C5_observed_timing_rows=timing_rows,
        C5_running_processes_observed_by_root=[28208, 37464],
        C5_process_observation_is_not_a_future_state_guarantee=True,
        Stage_C_status_markdown_is_at_merge_handoff_and_stale_for_C4=True,
        reference_agreement_resolution_still_exceeds_0_0001=True,
        no_detected_undercoverage_is_not_a_proved_99_percent_success_rate=True,
        widened_interval_is_not_a_conservative_lower_true_price_coverage_bound=True,
        B8_decision_point_coverage_was_not_a_planned_arm=True,
        quantum_native_law_bridge_closed=False, final_comparator_minimum_closed=False,
        quantum_advantage_established=False,
    ))
    create(output / "commit_provenance_reconciliation.json", provenance_rows)
    cpu = time.process_time() - started
    assert cpu < 60
    create(output / "summary.json", dict(
        passed=True, scope="Read-only saved-result and provenance inspection",
        local_only=True, CPU_seconds=cpu, new_pytests_timing_or_price_runs=0,
        coverage_scoring_recomputed=False, complete_physical_or_financial_certificate=False,
        frozen_snapshot_inputs_verified=True, code_spec_lock_bindings_checked=len(provenance_rows),
    ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "inspect"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if args.mode == "prepare":
        prepare(output)
        print("Stage C read-only snapshots frozen")
        return
    output.relative_to(PROGRAM)
    assert not (output / "summary.json").exists()
    try:
        inspect(output)
    except Exception:
        create(output / "failure.json", dict(passed=False, traceback=traceback.format_exc()))
        raise
    finally:
        protocol = read(output / "protocol.json")
        create(output / "manifest.json", dict(
            files={relative(p): sha(p) for p in sorted(output.rglob("*"))
                   if p.is_file() and p.name != "manifest.json"},
            frozen_inputs=protocol["frozen_inputs"], manifest_self_hash_excluded=True,
        ))
    print("Stage C saved-result inspection passed")


if __name__ == "__main__":
    main()
