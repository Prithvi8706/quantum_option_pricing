"""Read-only completed C5/C7 snapshots, provenance and fitted-time inspection.

No Stage C module is imported, no model is fitted and no price or timing job is
run. Prepare and inspect both refuse live supervisors/timing worker descendants.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from math import isfinite
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
CLASSICAL = ROOT / "results/frontier_classical_20261001"
PRIOR = PROGRAM / "C09_stagec_update_run001"
RESEARCH = ROOT / "research/limitation_program_20261001"
SPEC = "manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md"
LOCK = "research/frontier_replay_20261001/t0_requirements.lock"
PRIOR_HELPER = RESEARCH / "snapshot_stage_c_update.py"
CODE = ("snapshot_stage_c_timings.py", "stage_c_timing_update_preflight.json")
CPU_LIMIT = 30
WALL_LIMIT = 120
C5_KEYS = tuple(case + "/" + method for case in ("B4x12", "B8x52") for method in ("oss_bb", "oss"))
C7_KEYS = tuple(str(index) for index in range(2, 9))
EPS_KEYS = ("0.1", "0.03", "0.01", "0.001")
TIMING_FILES = (
    "c5/timing/c5_timing.json",
    "c5/timing/meta.json",
    "c5/rates/c5_rates.json",
    "c5/rates/commit.txt",
    *("c5/rates/" + key.replace("/", "_") + ".npy" for key in C5_KEYS),
    "c7/timing/c7_timing.json",
    "c7/timing/meta.json",
    "c7/rates/c7_rates.json",
    "c7/rates/meta.json",
    "c7/rates/truncation.json",
    *("c7/rates/case" + key + ".npy" for key in C7_KEYS),
)
UNCHANGED = (
    "c4/c4_raw.json",
    "c4/meta.json",
    "c4/B4x12_levels10to13.npy",
    "c4/B8x52_levels10to13.npy",
    "c4/B4x12_level17.npy",
    "c4_score/c4_coverage.json",
    "c4_score/meta.json",
    "c3_refa/ref_a.json",
    "c3_refb/B4x12/ref_b.json",
    "c3_refb/B8x52/ref_b.json",
    "c2/c2_timing.json",
)
C5_RATE_SOURCES = (
    "c5_smoothers.py",
    "c2_timing.py",
    "fit.py",
    "oss.py",
    "basis.py",
    "scrambles.py",
    "kernels.py",
    "timing.py",
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(Path(path).read_bytes())


def receipt_files(output):
    return {
        relative(path): sha(path)
        for path in sorted(output.rglob("*"))
        if path.is_file() and path.name != "manifest.json"
    }


def relative(path):
    return Path(path).resolve().relative_to(ROOT.resolve()).as_posix()


def create(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def bind(frozen, path, expected):
    """Normalize aliases and preserve every legitimate earlier expectation."""
    path = Path(str(path).replace("\\", "/"))
    actual = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    name = relative(actual)
    require(
        isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
        "Explicit frozen SHA256 required",
    )
    require(
        name not in frozen or frozen[name] == expected,
        "Existing frozen byte expectation conflicts: " + name,
    )
    frozen[name] = expected


def verify(frozen):
    for name, expected in frozen.items():
        path = (ROOT / name.replace("\\", "/")).resolve()
        path.relative_to(ROOT.resolve())
        require(sha(path) == expected, "Frozen completed timing input changed: " + name)


def budget(cpu, wall):
    if time.process_time() - cpu > CPU_LIMIT or time.monotonic() - wall > WALL_LIMIT:
        raise TimeoutError("Fixed snapshot inspection30CPU/120wall limit")


def process_clearance():
    """Observe command lines/parent chains; never terminate or wait on jobs."""
    require(os.name == "nt", "Windows process observation required for this local machine")
    command = (
        "Get-CimInstance Win32_Process | "
        "Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    )
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    rows = json.loads(result.stdout)
    if isinstance(rows, dict):
        rows = [rows]
    require(isinstance(rows, list) and rows, "Complete process observation required")
    roots, workers = set(), set()
    for row in rows:
        name = str(row["Name"]).lower()
        line = str(row.get("CommandLine") or "").lower().replace("\\", "/")
        pid = int(row["ProcessId"])
        if pid == os.getpid():
            continue
        supervisor = name in {"bash.exe", "sh.exe", "cmd.exe", "wsl.exe"} and re.search(
            r"stage_c_day[^\s\"']*\.sh", line
        )
        timing = (
            "python" in name
            and "research.frontier_classical_20261001." in line
            and ("c5_smoothers" in line or "c7_c8_cases" in line or "c2_timing" in line)
            and ("timing" in line or "c2_timing" in line)
        )
        if supervisor or timing:
            roots.add(pid)
        if "python" in name and any(
            marker in line
            for marker in ("spawn_main", "--multiprocessing-fork", "resource_tracker")
        ):
            # Spawn workers can use a system interpreter and carry only
            # parent_pid/pipe handles, with no workspace path in their argv.
            # Refuse all visible Python spawn workers rather than miss a
            # tracked timing child or resource tracker after its root ends.
            workers.add(pid)
    descendants = set(roots)
    while True:
        more = {int(row["ProcessId"]) for row in rows if int(row["ParentProcessId"]) in descendants}
        if more.issubset(descendants):
            break
        descendants.update(more)
    relevant = [row for row in rows if int(row["ProcessId"]) in descendants | workers]
    require(
        not relevant,
        "Live Stage C supervisor, exclusive timing root or worker descendant: "
        + json.dumps(relevant, sort_keys=True),
    )
    return {
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "live_stage_c_supervisors_or_timing_descendants": [],
        "live_multiprocessing_spawn_or_resource_tracker_workers": [],
        "worker_admission_requires_every_visible_spawn_worker_and_resource_tracker_terminal": True,
        "clearance_is_observation_not_a_future_process_guarantee": True,
    }


def completion_shape(c5, c7):
    """Check only completed runner schema; no fitted result is interpreted."""
    require(set(c5["blocks"]) == set(C5_KEYS), "All four complete C5 blocks required")
    require(set(c7["blocks"]) == set(C7_KEYS), "All seven complete C7 final blocks required")
    for key in C5_KEYS:
        block = c5["blocks"][key]
        require(
            block["root"] == 2026100151
            and len(block["warm"]) == 5
            and len(block["load_balanced"]) == 5
            and set(block["t_c"]) == set(EPS_KEYS)
            and all(field in block for field in ("fresh", "cold", "confirmation", "fits")),
            "C5 final block has all warm/fresh/cold/load-balanced/derived records",
        )
    for key in C7_KEYS:
        block = c7["blocks"][key]
        require(
            len(block["warm"]) == 3
            and set(block["fits"]) == {"all16", "per_scramble"}
            and "t_c_0.001" in block,
            "Each C7 final block requires three saved warm runs",
        )
    return {"C5_complete_blocks": 4, "C7_complete_blocks": 7, "C7_warm_runs_per_block": 3}


def prior_inputs():
    require(
        read(PRIOR / "summary.json").get("passed") is True,
        "Completed immutable C4/prior snapshot premise",
    )
    receipt = read(PRIOR / "manifest.json")
    frozen = {}
    for field in ("files", "frozen_inputs"):
        for path, expected in receipt[field].items():
            bind(frozen, path, expected)
    bind(frozen, PRIOR / "manifest.json", sha(PRIOR / "manifest.json"))
    require(
        frozen.get(relative(PRIOR_HELPER)) == sha(PRIOR_HELPER),
        "Original proven commit-materialization inspector is byte-identical",
    )
    verify(frozen)
    return frozen


def snapshot(output, source, frozen, observations):
    data = source.read_bytes()
    destination = output / "snapshots" / relative(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    require(sha(destination) == sha_bytes(data), "Snapshot byte equality")
    bind(frozen, destination, sha_bytes(data))
    # These completed runner outputs are now immutable inputs too.
    bind(frozen, source, sha_bytes(data))
    observations.append(
        {
            "live_path": relative(source),
            "snapshot": relative(destination),
            "observed_sha256": sha_bytes(data),
        }
    )


def materialize(output, metadata, phase, cache):
    """The prior inspector's exact Git-blob/LF→CRLF hash admission, without waiver."""
    require(
        metadata["dirty"] is False and re.fullmatch(r"[0-9a-f]{40}", metadata["commit"]),
        "Recorded clean full local commit required",
    )
    bindings = {}
    for name, expected in metadata["code_sha256"].items():
        require(
            Path(name).name == name and name.endswith(".py"), "Recorded Stage C module basename"
        )
        bindings["research/frontier_classical_20261001/" + name] = expected
    bindings.update({SPEC: metadata["spec_sha256"], LOCK: metadata["lock_sha256"]})
    rows = []
    for path, expected in bindings.items():
        key = metadata["commit"], path
        if key not in cache:
            cache[key] = subprocess.run(
                ["git", "show", metadata["commit"] + ":" + path],
                cwd=ROOT,
                check=True,
                capture_output=True,
                timeout=15,
            ).stdout
        blob = cache[key]
        candidates = {"Git_blob": blob, "Git_LF_to_CRLF": blob.replace(b"\n", b"\r\n")}
        matches = [label for label, data in candidates.items() if sha_bytes(data) == expected]
        require(
            matches,
            "Recorded source bytes differ from recorded local commit: " + phase + "/" + path,
        )
        destination = output / "commit_bindings" / phase / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(candidates[matches[0]])
        rows.append(
            {
                "phase": phase,
                "path": path,
                "commit": metadata["commit"],
                "representation": matches[0],
                "sha256": expected,
                "recorded_per_file_digest_verified": True,
            }
        )
    return rows


def prepare(output):
    cpu, wall = time.process_time(), time.monotonic()
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    require(not output.exists(), "Fresh completed-timing snapshot receipt required")
    clearance = process_clearance()
    shape = completion_shape(
        read(CLASSICAL / "c5/timing/c5_timing.json"), read(CLASSICAL / "c7/timing/c7_timing.json")
    )
    frozen = prior_inputs()
    for name in UNCHANGED:
        live = CLASSICAL / name
        previous = PRIOR / "snapshots/results/frontier_classical_20261001" / name
        require(
            live.read_bytes() == previous.read_bytes(),
            "Original C4/score/reference/C2 bytes changed: " + name,
        )
    for name in CODE:
        bind(frozen, RESEARCH / name, sha(RESEARCH / name))
    bind(frozen, Path(sys.executable), sha(Path(sys.executable)))
    budget(cpu, wall)
    output.mkdir()
    try:
        prepare_snapshots(output, frozen, cpu, wall, clearance, shape)
    except Exception as exc:
        create(
            output / "preparation_failure.json",
            {
                "failure_type": type(exc).__name__,
                "failure": traceback.format_exc(),
                "partial_files_preserved": True,
                "frozen_bytes_expected_at_failure": frozen,
                "fixed_receipt_terminal_no_retry": True,
            },
        )
        create(
            output / "summary.json",
            {
                "passed": False,
                "preparation_failed": True,
                "budget_censored": isinstance(exc, (TimeoutError, subprocess.TimeoutExpired))
                or time.process_time() - cpu > CPU_LIMIT
                or time.monotonic() - wall > WALL_LIMIT,
                "fixed_receipt_terminal_no_retry": True,
                "partial_files_preserved": True,
                "new_tests_prices_paths_or_timing_runs": 0,
                "CPU_seconds": time.process_time() - cpu,
                "wall_seconds": time.monotonic() - wall,
            },
        )
        create(
            output / "manifest.json",
            {
                "files": {
                    relative(path): sha(path)
                    for path in sorted(output.rglob("*"))
                    if path.is_file() and path.name != "manifest.json"
                },
                "frozen_inputs": frozen,
                "manifest_self_hash_excluded": True,
                "terminal_partial_preparation": True,
            },
        )
        raise


def prepare_snapshots(output, frozen, cpu, wall, clearance, shape):
    """Preserve every mutation if preparation fails after the fresh mkdir."""
    observations = []
    for name in TIMING_FILES + UNCHANGED:
        snapshot(output, CLASSICAL / name, frozen, observations)
        budget(cpu, wall)
    for name in CODE:
        path = RESEARCH / name
        bind(frozen, path, sha(path))
        shutil.copy2(path, output / name)
    bind(frozen, Path(sys.executable), sha(Path(sys.executable)))
    provenance, cache = [], {}
    for phase, path, seed in (
        ("C5_timing", "c5/timing/meta.json", 2026100151),
        ("C7_timing", "c7/timing/meta.json", 2026100171),
        ("C7_rates", "c7/rates/meta.json", 2026100171),
    ):
        metadata = read(output / "snapshots" / relative(CLASSICAL / path))
        require(metadata["root"] == seed, "Recorded timing/rates seed root")
        require(
            metadata["phase"] == ("rates" if phase == "C7_rates" else "timing"), "Recorded phase"
        )
        provenance.extend(materialize(output, metadata, phase, cache))
        budget(cpu, wall)
    rate_commit = (
        (output / "snapshots" / relative(CLASSICAL / "c5/rates/commit.txt")).read_text().strip()
    )
    require(re.fullmatch(r"[0-9a-f]{40}", rate_commit), "C5 rates original local commit marker")
    marker_sources = []
    for name in C5_RATE_SOURCES:
        path = "research/frontier_classical_20261001/" + name
        blob = subprocess.run(
            ["git", "show", rate_commit + ":" + path],
            cwd=ROOT,
            check=True,
            capture_output=True,
            timeout=15,
        ).stdout
        destination = output / "commit_bindings/C5_rates_commit_marker" / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(blob)
        marker_sources.append(
            {
                "commit": rate_commit,
                "path": path,
                "Git_blob_sha256": sha_bytes(blob),
                "recorded_per_file_rate_digest_available": False,
                "provenance_scope": (
                    "Recorded commit marker and materialized code; "
                    "not an independent per-file rates-time digest"
                ),
            }
        )
        budget(cpu, wall)
    for path in (output / "commit_bindings").rglob("*"):
        if path.is_file():
            bind(frozen, path, sha(path))
    create(
        output / "recorded_commit_materialization.json",
        {
            "hash_bound_metadata_rows": provenance,
            "C5_rates_commit_marker_rows": marker_sources,
            "broad_hash_equivalence_waiver_used": False,
        },
    )
    bind(
        frozen,
        output / "recorded_commit_materialization.json",
        sha(output / "recorded_commit_materialization.json"),
    )
    final_clearance = process_clearance()
    verify(frozen)
    budget(cpu, wall)
    create(
        output / "protocol.json",
        {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "local_only": True,
            "before_interpreting_completed_timing_or_fitted_rate_values": True,
            "requires_every_Stage_C_supervisor_timing_root_and_pool_descendant_terminal": True,
            "process_clearance_before_and_after_snapshot": [clearance, final_clearance],
            "completed_runner_schema": shape,
            "prior_immutable_C4_reference_provenance_receipt": relative(PRIOR),
            "original_C4_score_reference_C2_byte_equality_required": True,
            "fixed_snapshot_files": list(TIMING_FILES),
            "observations": observations,
            "C5_0p001_and_all_C7_times_label": (
                "Fitted rate/sample-size and warm-time models; no 20-run confirmation"
            ),
            "C5_0p01_report": (
                "Twenty measured run walls/median and saved scale-adjusted primary separately; "
                "no true-price coverage theorem"
            ),
            "new_tests_prices_paths_or_timing_runs": 0,
            "new_rate_fits_or_coverage_scores": 0,
            "old_one_block_snapshot_changed": False,
            "true_price99_delivery_G4_final_minimum_or_advantage_claim": False,
            "process_CPU_limit_seconds_each_phase": CPU_LIMIT,
            "wall_limit_seconds_each_phase": WALL_LIMIT,
            "prepare_process_CPU_seconds": time.process_time() - cpu,
            "prepare_wall_seconds": time.monotonic() - wall,
            "preexisting_Stage_C_jobs_or_supervisor_scripts_edited_or_restarted": False,
            "frozen_inputs": frozen,
            "python": sys.version,
            "executable": sys.executable,
        },
    )
    print(
        "Completed C5/C7 snapshot inputs/provenance frozen after terminal-process admission",
        flush=True,
    )


def finite(value):
    require(type(value) in (int, float) and isfinite(value), "Finite saved numeric field required")
    return value


def completed_run(run, n_top):
    require(
        run["n_top"] == n_top
        and len(run["scramble_means"]) == 16
        and finite(run["wall"]) > 0
        and finite(run["hw99"]) >= 0,
        "Complete saved16-scramble measured record",
    )
    require(
        all(isfinite(value) for value in run["scramble_means"]) and isfinite(run["mean"]),
        "Finite saved scramble means",
    )
    require(
        set(run["all16"]) == set(run["per_scramble_median"]) and str(n_top) in run["all16"],
        "Complete time-mark arrays",
    )
    require(
        all(finite(value) >= 0 for value in run["all16"].values())
        and all(finite(value) >= 0 for value in run["per_scramble_median"].values()),
        "Saved elapsed timing marks nonnegative",
    )


def inspect(output):
    cpu, wall = time.process_time(), time.monotonic()
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    require(
        not (output / "summary.json").exists(), "Completed timing inspection is already terminal"
    )
    protocol = read(output / "protocol.json")
    files = None
    try:
        clearance = process_clearance()
        verify(protocol["frozen_inputs"])
        saved_root = output / "snapshots/results/frontier_classical_20261001"
        c5, c7 = [
            read(saved_root / name)
            for name in ("c5/timing/c5_timing.json", "c7/timing/c7_timing.json")
        ]
        shape = completion_shape(c5, c7)
        rates5, rates7 = [
            read(saved_root / name) for name in ("c5/rates/c5_rates.json", "c7/rates/c7_rates.json")
        ]
        require(
            set(rates5) == set(C5_KEYS) and set(rates7) == set(C7_KEYS),
            "Complete matching saved rate arms",
        )
        c5_rows, c7_rows = [], []
        for key in C5_KEYS:
            budget(cpu, wall)
            block = c5["blocks"][key]
            require(
                all(state["idle"] is True for state in (block["machine"],)),
                "C5 recorded idle-machine admission",
            )
            for run in block["warm"] + [block["fresh"], block["cold"]]:
                completed_run(run, 1 << 19)
            for run in block["load_balanced"]:
                require(
                    run["n_top"] == 1 << 19
                    and finite(run["wall"]) > 0
                    and finite(run["mean"]) >= 0
                    and str(1 << 19) in run["all16"]
                    and all(finite(value) >= 0 for value in run["all16"].values()),
                    "Complete saved load-balanced timing record",
                )
            require(
                "0.001" not in block["confirmation"]
                and block["t_c"]["0.001"]["convention"] == "modelled all-16",
                "C5.001 is fitted, not confirmed",
            )
            fitted = block["t_c"]["0.001"]
            rate = rates5[key]["summary"]["n_eps"]["0.001"]
            require(
                fitted["n_eps"] == rate["point"], "C5 fitted sample size binds exact saved rates"
            )
            a, b = map(finite, block["fits"]["all16"])
            require(
                fitted["model_all16_unrounded"] == a + b * fitted["n_eps"]
                and fitted["primary"] == fitted["model_all16_unrounded"],
                "C5 saved model time algebra",
            )
            for kind, field in (
                ("per_scramble", "model_per_scramble_median"),
                ("load_balanced", "model_load_balanced"),
            ):
                a, b = map(finite, block["fits"][kind])
                require(fitted[field] == a + b * fitted["n_eps"], "C5 saved secondary model")
            confirmation = block["confirmation"].get("0.01")
            require(
                confirmation is not None
                and len(confirmation["runs"]) == 20
                and block["t_c"]["0.01"]["convention"] == "measured confirmation",
                "C5.01 saved20-run confirmations",
            )
            for run in confirmation["runs"]:
                completed_run(run, confirmation["n_run"])
            measured = block["t_c"]["0.01"]
            rate01 = rates5[key]["summary"]["n_eps"]["0.01"]
            walls = sorted(finite(run["wall"]) for run in confirmation["runs"])
            measured_median = (walls[9] + walls[10]) / 2
            require(
                measured["n_eps"] == rate01["point"]
                and measured["n_run"] == confirmation["n_run"]
                and measured["median_wall"] == measured_median
                and finite(measured["scale"]) >= 1
                and measured["primary"] == measured_median * measured["scale"],
                "Saved measured median and derived scale-adjusted primary stay distinct",
            )
            c5_rows.append(
                {
                    "arm": key,
                    "epsilon0p001_saved_t_c": fitted,
                    "epsilon0p001_rate_n_eps": rate,
                    "epsilon0p001_is_fitted_not20_confirmed": True,
                    "epsilon0p01_measured_confirmation": block["t_c"]["0.01"],
                    "epsilon0p01_repetitions": 20,
                    "epsilon0p01_n_run": confirmation["n_run"],
                    "epsilon0p01_measured_median_wall_seconds": measured_median,
                    "epsilon0p01_rate_n_target": rate01,
                    "epsilon0p01_n_eps_target": measured["n_eps"],
                    "epsilon0p01_saved_scale": measured["scale"],
                    "epsilon0p01_derived_primary_seconds": measured["primary"],
                    "epsilon0p01_primary_is_median_wall_times_scale": True,
                    "epsilon0p01_primary_is_not_a_separate_elapsed_measurement": True,
                    "measured_confirmation_is_not_true_price99_coverage_proof": True,
                }
            )
        for key in C7_KEYS:
            budget(cpu, wall)
            block = c7["blocks"][key]
            require(block["machine"]["idle"] is True, "C7 recorded idle-machine admission")
            for run in block["warm"]:
                completed_run(run, 1 << 19)
            fitted = block["t_c_0.001"]
            rate = rates7[key]["summary"]["knockout_pre"]["n_eps"]["0.001"]
            require(
                fitted["n_eps"] == rate["point"] and "confirmation" not in block,
                "C7 fitted point/no confirmation branch",
            )
            a, b = map(finite, block["fits"]["all16"])
            require(fitted["all16_model"] == a + b * fitted["n_eps"], "C7 saved model algebra")
            a, b = map(finite, block["fits"]["per_scramble"])
            require(
                fitted["per_scramble_model"] == a + b * fitted["n_eps"],
                "C7 saved per-scramble model algebra",
            )
            c7_rows.append(
                {
                    "case_index": int(key),
                    "case_parameters": rates7[key]["case"],
                    "warm_repetitions": 3,
                    "epsilon0p001_saved_t_c": fitted,
                    "epsilon0p001_rate_n_eps": rate,
                    "epsilon0p001_is_fitted_not20_confirmed": True,
                    "warm_timings_are_not_accuracy_delivery_confirmations": True,
                }
            )
        for name in UNCHANGED:
            require(
                (CLASSICAL / name).read_bytes()
                == (saved_root / name).read_bytes()
                == (PRIOR / "snapshots/results/frontier_classical_20261001" / name).read_bytes(),
                "Original C4/reference/score/C2 remain byte-identical: " + name,
            )
        prior_score = read(saved_root / "c4_score/c4_coverage.json")
        create(
            output / "stage_c_timing_observations.json",
            {
                **shape,
                "C5": c5_rows,
                "C7": c7_rows,
                "original_C4_primary_checks_unchanged": {
                    case: prior_score["cases"][case]["primary_check"] for case in ("B4x12", "B8x52")
                },
                "original_score_reference_C2_byte_identical_to_prior_receipt": True,
                "all_epsilon0p001_times_fitted_not20_confirmed": True,
                "true_price99_delivery_G4_final_comparator_minimum_or_advantage_established": False,
            },
        )
        final_clearance = process_clearance()
        verify(protocol["frozen_inputs"])
        provenance = read(output / "recorded_commit_materialization.json")
        files = receipt_files(output)
        budget(cpu, wall)
        create(
            output / "summary.json",
            {
                "passed": True,
                "local_only": True,
                "scope": "Read-only completed C5/C7 timing/provenance observations",
                **shape,
                "terminal_process_observations": [clearance, final_clearance],
                "hash_bound_recorded_code_spec_lock_bindings": len(
                    provenance["hash_bound_metadata_rows"]
                ),
                "C5_rates_source_provenance_has_commit_marker_not_recorded_per_file_digests": True,
                "old_C09_one_block_snapshot_byte_identical_and_immutable": True,
                "original_C4_score_references_and_C2_unchanged": True,
                "all_epsilon0p001_C5_C7_times_are_fitted_not20_run_confirmed": True,
                "C5_epsilon0p01_measured_confirmation_records_reported": True,
                "C5_epsilon0p01_elapsed_median_and_scale_adjusted_primary_kept_distinct": True,
                "new_tests_prices_paths_timing_runs_rate_fits_or_coverage_scores": 0,
                "true_price99_delivery_G4_final_minimum_or_quantum_advantage_proved": False,
                "CPU_seconds": time.process_time() - cpu,
                "wall_seconds": time.monotonic() - wall,
            },
        )
    except Exception as exc:
        create(
            output / "summary.json",
            {
                "passed": False,
                "budget_censored": isinstance(exc, TimeoutError),
                "failure": traceback.format_exc(),
                "new_tests_prices_paths_or_timing_runs": 0,
            },
        )
        raise
    finally:
        if files is None:
            files = receipt_files(output)
        else:
            files[relative(output / "summary.json")] = sha(output / "summary.json")
        create(
            output / "manifest.json",
            {
                "files": files,
                "frozen_inputs": protocol["frozen_inputs"],
                "manifest_self_hash_excluded": True,
            },
        )
    print("Completed C5/C7 snapshots inspected; fitted times remain conditional models", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "inspect"))
    parser.add_argument("--output", type=Path, default=PROGRAM / "C09_stagec_timing_update_run001")
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else inspect)(args.output)
