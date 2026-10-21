"""Read-only Stage C snapshot and source/estimand/timing ledger.

Prepare selects bounded existing receipts and copies their bytes before any
numerical outcomes are read. Run interprets only those copies. Existing jobs,
source files, incomplete checkpoints and historical outputs are never changed.
No pricing, sampler, compilation, benchmark or bootstrap job is executed.
"""

from __future__ import annotations

# Receipt descriptions keep their prose.
# ruff: noqa: E501

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import sys
import traceback

import numpy as np
from scipy.stats import t as student_t

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
CLASSICAL = ROOT / "results/frontier_classical_20261001"
RESEARCH = ROOT / "research/frontier_classical_20261001"
SPEC = ROOT / "manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md"
SELECTED = (
    "c1",
    "c2",
    "c3_refa",
    "c3_refb",
    "c4",
    "c5",
    "c7/rates",
    "decision_interim",
    "decision_interim_v2",
    "q4",
    "q4_d2",
    "sigma_dev",
)
MAX_FILE_BYTES = 64 << 20
MAX_TOTAL_BYTES = 256 << 20
MAX_FILES = 500
EPS = (0.1, 0.03, 0.01, 0.001)
METHODS = {"rqmc": "knockout", "preint": "knockout_pre"}


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(Path(path).read_bytes())


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def close(actual, expected, label, rel=2e-11, absolute=2e-12):
    assert math.isfinite(actual) and math.isfinite(expected)
    assert math.isclose(actual, expected, rel_tol=rel, abs_tol=absolute), (label, actual, expected)


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM)
    assert not output.exists()
    # Directory and extension selection is fixed before any JSON/array parsing.
    inputs = [
        Path(__file__).resolve(),
        SPEC,
        ROOT / "research/frontier_replay_20261001/t0_requirements.lock",
        ROOT / "results/frontier_replay_20261001/t0_environment.json",
        ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py",
    ]
    inputs.extend(sorted(RESEARCH.glob("*.py")))
    for selected in SELECTED:
        directory = CLASSICAL / selected
        if directory.exists():
            inputs.extend(
                path
                for path in sorted(directory.rglob("*"))
                if path.is_file()
                and path.suffix.lower() in (".json", ".npy", ".txt", ".log")
                and "oracle" not in path.parts
                and "leaves_f40" not in path.parts
            )
    for receipt in (
        "C06_pair_run001",
        "C06_pair_audit_run001",
        "C07_bound_date1_run001",
        "E02_financial_run002",
    ):
        inputs.extend(PROGRAM / receipt / file for file in ("summary.json", "manifest.json"))
    inputs.extend(
        PROGRAM / "A10_coefficient_run001" / case / "min-depth/target.json"
        for case in ("B4x12", "B8x52")
    )
    inputs = sorted(set(inputs))
    assert len(inputs) <= MAX_FILES
    assert all(path.is_file() and path.stat().st_size <= MAX_FILE_BYTES for path in inputs)
    assert sum(path.stat().st_size for path in inputs) <= MAX_TOTAL_BYTES
    output.mkdir()
    snapshots = output / "snapshots"
    records, total = [], 0
    for path in inputs:
        before = path.stat()
        data = path.read_bytes()
        after = path.stat()
        assert len(data) <= MAX_FILE_BYTES
        target = snapshots / relative(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
        digest = sha_bytes(data)
        assert sha(target) == digest
        total += len(data)
        records.append(
            dict(
                original=relative(path),
                snapshot=relative(target),
                sha256=digest,
                bytes=len(data),
                original_mtime_ns_at_capture=after.st_mtime_ns,
                stable_during_capture=before.st_size == after.st_size == len(data)
                and before.st_mtime_ns == after.st_mtime_ns,
                potentially_live_original=path.is_relative_to(CLASSICAL),
            )
        )
    assert total <= MAX_TOTAL_BYTES
    process = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^python(w)?\\.exe$' } | Select-Object ProcessId, ExecutablePath, CommandLine | ConvertTo-Json -Depth 3",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    (output / "python_process_inventory.txt").write_text(process.stdout, encoding="utf-8")
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_numerical_outcomes_inspected=True,
            bounded_existing_directories=list(SELECTED),
            max_files=MAX_FILES,
            max_single_file_bytes=MAX_FILE_BYTES,
            max_total_bytes=MAX_TOTAL_BYTES,
            captured_file_count=len(records),
            captured_bytes=total,
            files=records,
            interpreter_sha256=sha(sys.executable),
            python=sys.version,
            numpy=np.__version__,
            method_families=[
                "continuous-model PCA ndtri RQMC",
                "continuous-model first-direction preintegration",
                "continuous-model time-ordered/bridge OSS",
                "continuous-model one-factor iid reference",
            ],
            primary_task="One original discounted monitored knock-out price per B4/B8 case with its declared accuracy/confidence",
            arithmetic_checks=[
                "actual20confirmation wall medians,320scramble pooled halfwidth,roundednrun,scale andprimary",
                "warm/per-scramble/load-balanced timing fit arithmetic",
                "canonical primary rate,n_target andrawprefix mean/sd",
                "referenceA64scramble arrays andreferenceB16worker aggregates",
                "referenceagreement andcoveragecompletionstatus",
                "originaltargetinputlaw andopen commonfinancialbridge",
                "receiptcode/specprovenance pluslocalhistoricalgitobject reads",
            ],
            no_new_financial_executions=True,
            no_existing_process_mutations=True,
            interpret_only_immutable_snapshots=True,
            original_live_files_may_change=True,
            no_new_bootstrap_or_coverage_scoring=True,
            full_G2_required_for_continuous_law_comparison=True,
            exact_finite_law_comparator_not_assumed_present=True,
            no_push=True,
            failures_preserved=True,
        ),
    )
    print(
        "C09 bounded existing Stage C inventory frozen before numerical inspection",
        len(records),
        "files",
        total,
        "bytes",
        flush=True,
    )


class Snapshot:
    def __init__(self, output):
        self.output = Path(output).resolve()
        self.protocol = read(self.output / "protocol.json")
        self.by_name = {r["original"]: r for r in self.protocol["files"]}
        assert len(self.by_name) == len(self.protocol["files"])
        self.parse_errors = []
        for record in self.by_name.values():
            assert sha(ROOT / record["snapshot"]) == record["sha256"]

    def path(self, path):
        record = self.by_name.get(relative(path))
        return ROOT / record["snapshot"] if record else None

    def text(self, path):
        captured = self.path(path)
        assert captured is not None
        return captured.read_text(encoding="utf-8")

    def json(self, path):
        captured = self.path(path)
        if captured is None:
            return None
        try:
            return read(captured)
        except (UnicodeError, json.JSONDecodeError) as error:
            self.parse_errors.append(
                dict(
                    original=relative(path),
                    failure_type=type(error).__name__,
                    message=str(error),
                    incomplete_live_snapshot_possible=True,
                )
            )
            return None

    def array(self, path):
        captured = self.path(path)
        if captured is None:
            return None
        try:
            result = np.load(captured, allow_pickle=False)
        except (ValueError, OSError) as error:
            self.parse_errors.append(
                dict(
                    original=relative(path),
                    failure_type=type(error).__name__,
                    message=str(error),
                    incomplete_live_snapshot_possible=True,
                )
            )
            return None
        assert np.issubdtype(result.dtype, np.number) and np.isfinite(result).all()
        return result


def source_and_law(snap):
    timing, c2, scrambles, kernels, oss, refb = (
        snap.text(RESEARCH / name)
        for name in (
            "timing.py",
            "c2_timing.py",
            "scrambles.py",
            "kernels.py",
            "oss.py",
            "c3_refb.py",
        )
    )
    assert "ndtri(np.clip(u, 1e-15, 1 - 1e-15))" in timing
    assert "z @ L.T + mu" in timing and "canonical_factor" in timing
    assert "_factor(run_id, case, method)" in timing and "time.perf_counter()" in timing
    assert "knockout_preint" in timing and "knockout_plain" in timing
    assert "oss_paths" in timing and "oss_bb_paths" in timing
    assert "scale = max(1.0, (hw16 / (SHARE * eps)) ** (1 / r))" in c2
    assert "primary=wall * scale" in c2 and 'convention="measured confirmation"' in c2
    assert "wall=end - submit" in c2 and "n_run = 2 ** math.ceil(math.log2(n))" in c2
    assert """sampler = qmc.Sobol(case.dim, scramble=True""" in timing
    assert "def dim(self):\n        return self.na * self.nt" in scrambles
    assert "if basket / na >= barrier:" in refb and "rng.standard_normal" in refb
    assert "math.exp(-case.rate * case.maturity)" in timing and "disc *" in kernels
    assert "def ndtri" in oss and "prob" in oss
    assert "NUMBA_CACHE_DIR" in c2 and "warm_up" in c2 and "wait_workers" in c2
    tree = ast.parse(scrambles)
    case = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Case")
    values = {
        n.target.id: ast.literal_eval(n.value)
        for n in case.body
        if isinstance(n, ast.AnnAssign) and n.value is not None
    }
    assert values == dict(
        spot=100.0, strike=100.0, barrier=140.0, sigma=0.3, rho=0.4, rate=0.03, maturity=1.0
    )
    quantum = {}
    for case_name in ("B4x12", "B8x52"):
        target_path = PROGRAM / "A10_coefficient_run001" / case_name / "min-depth/target.json"
        target = snap.json(target_path)
        assert target["width"] == 72 and target["fraction_bits"] == 40
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        assert all(
            node["params"]["bits"] == 32 and node["params"]["preparation"] == "uniform"
            for node in inputs
        )
        count = 60 if case_name == "B4x12" else 468
        assert len(inputs) == count
        quantum[case_name] = dict(
            target_sha256=snap.by_name[relative(target_path)]["sha256"],
            random_uniform32_words=count,
            shared_Box_Muller_pairs=count // 2,
            fraction_bits=40,
            native_width=72,
            original_named_output=target["outputs"],
        )
    c06 = snap.json(PROGRAM / "C06_pair_audit_run001/summary.json")
    assert c06["passed"] and not c06["full_G2_closed"] and not c06["complete_price_certified"]
    return dict(
        passed=True,
        source_model_parameters=values,
        classical_contract="discounted positive Asian arithmetic average minus100,zeroifanymonitored equal-weight basket>=140",
        classical_dimension=dict(B4x12=48, B8x52=416),
        classical_law="Float64 scrambledSobol->clipped inverse-normal->fullrank covariance PCA, or survival-conditioned OSS; iid reference usesPCG64 standard normals withonefactor exactdate stepping. These are numerical constructions for theoriginal continuousGBM estimand.",
        classical_numeric_endpoint_clip=[1e-15, 1 - 1e-15],
        classical_numeric_inverse_normal_root_roundoff_bias_dollars=None,
        classical_hard_payoff_and_preintegrated_estimands_differ_pointwise_but_target_same_continuous_expectation=True,
        actual_time_includes_uniform_generation_inverse_normal_GEMM_and_payoff=True,
        actual_factor_built_per_worker_inside_timed_run=True,
        warm_start_excludes_worker_creation_initial_cache_and_compilation=True,
        fresh_cached_and_cold_start_sensitivities_exist_in_code=True,
        noPCA_rank_dropped=True,
        quantum_law="Independentuniform32 words,exactf40midpoints,jointsharedinputBoxMuller,native table arithmetic,clipped logpath,native exp/strictbarrier/alreadydiscounted72bitY",
        quantum_cases=quantum,
        identical_actual_finite_sampler_or_arithmetic=False,
        full_common_continuous_price_bridge_certified=False,
        exact_finite_law_classical_comparator_executed_in_this_audit=False,
        full_G2_open=True,
        financial_accuracy_and_G4_closed=False,
    )


def provenance(snap, name, data):
    meta = data.get("meta", data)
    commit = meta.get("commit")
    hashes = meta.get("code_sha256", {})
    records = []
    for file, digest in hashes.items():
        path = RESEARCH / file
        current = snap.by_name.get(relative(path))
        record = dict(
            module=file,
            recorded_sha256=digest,
            current_snapshot_byte_match=current is not None and current["sha256"] == digest,
            recorded_commit_byte_match=None,
            recorded_commit_line_ending_normalization_match=None,
        )
        if (
            isinstance(commit, str)
            and re.fullmatch(r"[0-9a-fA-F]{40}", commit)
            and path.is_relative_to(RESEARCH)
            and path.suffix == ".py"
        ):
            result = subprocess.run(
                ["git", "show", commit + ":" + relative(path)],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
            if result.returncode == 0:
                raw = result.stdout
                record["recorded_commit_byte_match"] = sha_bytes(raw) == digest
                record["recorded_commit_line_ending_normalization_match"] = (
                    sha_bytes(raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")) == digest
                )
                stored = snap.output / "historical_git_objects" / commit / file
                if not stored.exists():
                    stored.parent.mkdir(parents=True, exist_ok=True)
                    with stored.open("xb") as handle:
                        handle.write(raw)
                record["historical_git_object_snapshot"] = relative(stored)
        records.append(record)
    source_match = bool(records) and all(
        row["current_snapshot_byte_match"]
        or row["recorded_commit_byte_match"]
        or row["recorded_commit_line_ending_normalization_match"]
        for row in records
    )
    spec_hash = meta.get("spec_sha256")
    return dict(
        receipt=name,
        recorded_commit=commit,
        recorded_dirty=meta.get("dirty"),
        recorded_spec_sha256=spec_hash,
        current_spec_snapshot_byte_match=spec_hash == snap.by_name[relative(SPEC)]["sha256"]
        if spec_hash
        else None,
        recorded_lock_sha256=meta.get("lock_sha256"),
        code_hashes_recorded=len(records),
        all_recorded_code_hashes_bound_to_available_local_bytes=source_match,
        code_hash_checks=records,
        absence_of_fullcode_spec_environment_binding_is_a_limitation=not hashes or not spec_hash,
        recorded_machine={
            k: meta[k]
            for k in ("cpu", "workers", "lb_workers", "power_plan", "affinity", "python", "numpy")
            if k in meta
        },
    )


def timing_ledger(snap, c1, c2):
    if c1 is None or c2 is None:
        return dict(status="missing timing or rate receipt", rows=[], complete=False)
    t995 = float(student_t.ppf(0.995, 15))
    close(c2["meta"]["t995_15"], t995, "t99515")
    rows, blocks = [], []
    for key, block in c2["blocks"].items():
        case, method = key.split("/")
        assert method in METHODS
        estimate = c1["cases"][case]["summary"]["canonical"][METHODS[method]]
        fit = estimate["fits"]["primary"]
        rate, amplitude = fit["r"], fit["A"]
        assert rate > 0 and amplitude > 0
        start_states = {}
        for label, values in (
            ("warm", block.get("warm", [])),
            ("load_balanced", block.get("load_balanced", [])),
        ):
            start_states[label] = dict(
                repeats=len(values),
                actual_wall_seconds=[v["wall"] for v in values],
                actual_points_per_scramble=[v["n_top"] for v in values],
            )
        for label in ("fresh", "cold"):
            value = block.get(label)
            start_states[label] = (
                dict(actual_wall_seconds=value["wall"], actual_points_per_scramble=value["n_top"])
                if value
                else None
            )
        all16_marks = sorted(int(n) for n in block["warm"][0]["all16"])
        warm_medians = {
            n: statistics.median(run["all16"][str(n)] for run in block["warm"]) for n in all16_marks
        }
        for label, field, source in (
            ("all16", "all16", block["warm"]),
            ("per_scramble", "per_scramble_median", block["warm"]),
            ("load_balanced", "all16", block["load_balanced"]),
        ):
            marks = sorted(int(n) for n in source[0][field] if int(n) >= 1 << 13)
            walls = [statistics.median(run[field][str(n)] for run in source) for n in marks]
            slope, intercept = np.polyfit(np.asarray(marks, dtype=float), walls, 1)
            close(block["fits"][label][0], float(intercept), key + " " + label + " intercept")
            close(block["fits"][label][1], float(slope), key + " " + label + " slope")
        for epsilon in EPS:
            label = str(epsilon)
            target = (t995 * amplitude / (4 * 0.45 * epsilon)) ** (1 / rate)
            close(estimate["n_eps"][label]["point"], target, key + " n_target")
            saved = block["t_c"][label]
            close(saved["n_eps"], target, key + " n_eps")
            model = block["fits"]["all16"][0] + block["fits"]["all16"][1] * target
            close(saved["model_all16_unrounded"], model, key + " model")
            confirmation = block["confirmation"].get(label)
            row = dict(
                case=case,
                method=method,
                epsilon_dollars=epsilon,
                statistical_share_dollars=0.45 * epsilon,
                n_target_fitted_per_scramble=target,
                n_target_is_not_an_executed_count=True,
                canonical_primary_rate=rate,
                rate_ci95=estimate["r_ci95"],
                fitted_count_extrapolation_flag=estimate["n_eps"][label]["flag"],
                model_all16_unrounded_seconds=model,
                recorded_primary_t_c_seconds=saved["primary"],
                recorded_primary_convention=saved["convention"],
                measured_median_wall_seconds=None,
                actual_n_run_per_scramble=None,
                confirmation_replications=0,
                confirmation_scrambles_per_replication=16,
                pooled_hw16_dollars=None,
                scale=None,
                scale_is_a_modelled_count_time_adjustment=False,
                fresh_cached_sensitivity_seconds=saved.get("fresh_cached"),
                successful_same_law_price_timing_certified=False,
                independent_reference_and_coverage_required=True,
            )
            if confirmation:
                runs = confirmation["runs"]
                assert len(runs) == 20 and all(len(run["scramble_means"]) == 16 for run in runs)
                n_run = confirmation["n_run"]
                assert n_run == 1 << math.ceil(math.log2(target))
                assert all(run["n_top"] == n_run for run in runs)
                means = [mean for run in runs for mean in run["scramble_means"]]
                pooled = t995 * statistics.stdev(means) / 4
                wall = statistics.median(run["wall"] for run in runs)
                scale = max(1.0, (pooled / (0.45 * epsilon)) ** (1 / rate))
                fraction = sum(run["hw99"] <= 0.45 * epsilon for run in runs) / 20
                for run in runs:
                    close(
                        run["mean"],
                        statistics.mean(run["scramble_means"]),
                        key + " confirmation mean",
                    )
                    close(
                        run["hw99"],
                        t995 * statistics.stdev(run["scramble_means"]) / 4,
                        key + " confirmation hw",
                    )
                for saved_key, value in (
                    ("median_wall", wall),
                    ("pooled_hw16", pooled),
                    ("scale", scale),
                    ("fraction_hw_ok", fraction),
                    ("primary", wall * scale),
                ):
                    close(saved[saved_key], value, key + " " + label + " " + saved_key)
                assert saved["n_run"] == n_run
                row.update(
                    measured_median_wall_seconds=wall,
                    actual_n_run_per_scramble=n_run,
                    confirmation_replications=20,
                    pooled_hw16_dollars=pooled,
                    scale=scale,
                    scale_is_a_modelled_count_time_adjustment=scale > 1,
                    scaled_derived_t_c_seconds=wall * scale,
                    unscaled_pooled_interval_meets_statistical_share=pooled <= 0.45 * epsilon,
                    fraction_of_actual_replications_meeting_statistical_share=fraction,
                    actual_price_estimates=[run["mean"] for run in runs],
                    actual_replication_halfwidths=[run["hw99"] for run in runs],
                    interpretation="Measured20confirmation walltimes atn_run; primaryt_cincludes a fitted extrapolation ifscale>1. No new run atscaledcount wasexecuted.",
                )
            elif target < 1 << 13:
                mark = min(n for n in all16_marks if n >= max(target, 1 << 6))
                assert saved["mark"] == mark
                close(saved["primary"], warm_medians[mark], key + " smallmark")
                row.update(
                    actual_n_run_per_scramble=mark,
                    measured_median_wall_seconds=warm_medians[mark],
                    interpretation="Measured warm elapsedprefix mark; no20-replication accuracy confirmation at thisepsilon.",
                )
            else:
                close(saved["primary"], model, key + " modelled primary")
                row["interpretation"] = (
                    "Modelled all16 time at fittedn_target; no accuracy-target execution recorded."
                )
            rows.append(row)
        blocks.append(
            dict(
                case=case,
                method=method,
                start_state_runs=start_states,
                machine_at_block_start=block.get("machine"),
                source_root=block.get("root"),
                actual_timing_fit_reconciled=True,
            )
        )
    return dict(
        complete=len(c2["blocks"]) == 4,
        arithmetic_reconciled=True,
        rows=rows,
        blocks=blocks,
        primary_scaled_t_c_is_not_independently_timed_success=True,
        standalone_classical_reference_coverage_status_checked_separately=True,
    )


def rate_ledger(snap, c1):
    if c1 is None:
        return dict(complete=False, cases=[])
    cases = []
    for case, data in c1["cases"].items():
        array = snap.array(CLASSICAL / "c1" / (case + "_canonical.npy"))
        assert array is not None and array.shape == (32, 6, len(data["ms"]))
        for column, estimand in ((2, "knockout"), (5, "knockout_pre")):
            value = data["summary"]["canonical"][estimand]
            close(value["price"], float(array[:, column, -1].mean()), case + " price")
            close(
                value["std_error"],
                float(array[:, column, -1].std(ddof=1) / math.sqrt(32)),
                case + " SE",
            )
            deviation = array[:, column, :].std(0, ddof=1)
            assert np.allclose(value["sd_one_scramble"], deviation, rtol=2e-11, atol=2e-12)
            selected = [j for j, m in enumerate(data["ms"]) if 10 <= m <= max(data["ms"])]
            slope, intercept = np.polyfit(
                np.asarray(data["ms"])[selected] * math.log(2), np.log(deviation[selected]), 1
            )
            close(value["fits"]["primary"]["r"], float(-slope), case + " rate")
            close(value["fits"]["primary"]["A"], float(np.exp(intercept)), case + " amplitude")
            cases.append(
                dict(
                    case=case,
                    estimand=estimand,
                    canonical_raw_prefixes_reconciled=True,
                    scrambles=32,
                    prefix_powers=data["ms"],
                    price=value["price"],
                    standard_error=value["std_error"],
                    primary_rate=value["fits"]["primary"]["r"],
                    primary_rate_ci95_recorded=value["r_ci95"],
                    rate_claim_label=value["c2_label"],
                    bootstrap_draws_not_reexecuted=True,
                    recorded_factor_sha256=data["factor_sha256"]["canonical"],
                    covariance_factor_not_rebuilt_in_audit=True,
                )
            )
    return dict(complete=len(c1["cases"]) == 2, port_check=c1["port_check"], cases=cases)


def references_ledger(snap):
    refa = snap.json(CLASSICAL / "c3_refa/ref_a.json")
    rows = []
    for case in ("B4x12", "B8x52"):
        a = refa.get("cases", {}).get(case) if refa else None
        b = snap.json(CLASSICAL / "c3_refb" / case / "ref_b.json")
        row = dict(
            case=case,
            ref_A_complete=a is not None,
            ref_B_complete=b is not None,
            primary_reference_agreement=None,
            reference_resolution_dollars=None,
            reference_resolves_1e4_dollars=None,
        )
        if a:
            array = snap.array(CLASSICAL / "c3_refa" / (case + "_oss_prefix.npy"))
            assert array is not None and array.shape == (64, len(a["ms"]))
            assert a["ms"][-1] == 22 and refa["scrambles"] == 64 and refa["m_top"] == 22
            mean, se = float(array[:, -1].mean()), float(array[:, -1].std(ddof=1) / 8)
            close(a["price"], mean, case + " RefA mean")
            close(a["se"], se, case + " RefA SE")
            close(a["hw99"], float(student_t.ppf(0.995, 63)) * se, case + " RefA halfwidth")
            row["ref_A"] = dict(
                price=a["price"],
                se=a["se"],
                hw99=a["hw99"],
                total_scrambles=64,
                actual_points_per_scramble=1 << 22,
                recorded_wall_seconds=a["seconds"],
                algorithm="timeordered canonicalassetPCA OSS RQMC",
                raw_prefixes_reconciled=True,
                complete_spec_code_environment_hash_binding_present=False,
            )
        if b:
            workers = b["workers"]
            assert len(workers) == 16 and sorted(w["worker"] for w in workers) == list(range(16))
            n = sum(w["n"] for w in workers)
            mean = math.fsum(w["sum"] for w in workers) / n
            variance = (math.fsum(w["sumsq"] for w in workers) - n * mean**2) / (n - 1)
            se = math.sqrt(variance / n)
            assert n == b["paths"] and b["budget_seconds"] == 21600
            for key, expected in (
                ("price", mean),
                ("sd", math.sqrt(variance)),
                ("se", se),
                ("hw99", 2.5758293035489004 * se),
            ):
                close(b[key], expected, case + " RefB " + key)
            checkpoints_match = []
            for worker in workers:
                checkpoint = snap.json(
                    CLASSICAL / "c3_refb" / case / ("worker%d.json" % worker["worker"])
                )
                checkpoints_match.append(checkpoint == worker)
            row["ref_B"] = dict(
                price=b["price"],
                se=b["se"],
                hw99=b["hw99"],
                actual_paths=n,
                recorded_wall_seconds=b["wall_seconds"],
                fixed_machine_budget_seconds=b["budget_seconds"],
                workers=16,
                worker_aggregates_reconciled=True,
                captured_worker_checkpoints_match_final=all(checkpoints_match),
                algorithm="PCG64 iidnormal onefactor exactdate float64plain monitored payoff",
                complete_spec_code_environment_hash_binding_present=False,
            )
        if a and b:
            gap, resolution = abs(a["price"] - b["price"]), a["hw99"] + b["hw99"]
            agreement = gap <= resolution
            row.update(
                primary_reference_agreement=agreement,
                absolute_reference_gap_dollars=gap,
                reference_resolution_dollars=resolution,
                reference_resolves_1e4_dollars=resolution <= 0.0001,
            )
            if agreement:
                wa, wb = a["se"] ** -2, b["se"] ** -2
                row["combined_reference"] = dict(
                    price=(wa * a["price"] + wb * b["price"]) / (wa + wb),
                    hw99=2.576 / math.sqrt(wa + wb),
                    inversevariance_reference_arithmetic=True,
                )
        rows.append(row)
    return dict(
        cases=rows,
        complete=all(row["ref_A_complete"] and row["ref_B_complete"] for row in rows),
        references_same_continuous_financial_model_not_current_exact_BM_finite_law=True,
        primary_agreement_does_not_close_common_quantum_law_bridge=True,
    )


def coverage_ledger(snap):
    expected = [
        ("B4x12_levels10to13.npy", (1000, 16, 4)),
        ("B8x52_levels10to13.npy", (1000, 16, 4)),
        ("B4x12_level17.npy", (1000, 16, 1)),
    ]
    arms = []
    for name, shape in expected:
        array = snap.array(CLASSICAL / "c4" / name)
        arms.append(
            dict(
                artifact=name,
                exists_at_freeze=array is not None,
                expected_shape=list(shape),
                captured_shape=list(array.shape) if array is not None else None,
                complete_shape=array is not None and array.shape == shape,
                actual_financial_samples_replayed_in_audit=0,
            )
        )
    raw = snap.json(CLASSICAL / "c4/c4_raw.json")
    scores = []
    for name, record in snap.by_name.items():
        if Path(name).name == "c4_coverage.json":
            scores.append(dict(original=name, score=snap.json(ROOT / name)))
    return dict(
        raw_arms=arms,
        all_declared_raw_arms_present=all(a["complete_shape"] for a in arms),
        raw_metadata=raw,
        scored_coverage_receipts=scores,
        completed_scored_coverage_available=bool(scores),
        B8_decisionpoint_coverage_not_required_and_still_assumed_by_originalspec=True,
        bootstrap_or_coverage_scoring_executed_in_audit=False,
        nominal99_interval_is_not_automatically_rigorous_fullprice_confidence=True,
    )


def decisions_and_other_receipts(snap, timing):
    by_case = {
        case: [r for r in timing["rows"] if r["case"] == case and r["epsilon_dollars"] == 0.001]
        for case in ("B4x12", "B8x52")
    }
    decisions = []
    for directory in ("decision_interim", "decision_interim_v2"):
        data = snap.json(CLASSICAL / directory / "decision_interim.json")
        if not data:
            continue
        rows = []
        for case, value in data["cases"].items():
            actual = {r["method"]: r for r in by_case[case]}
            comparator = value["comparator"]
            rows.append(
                dict(
                    case=case,
                    comparator=comparator,
                    recorded_candidates_seconds=value["candidates_s"],
                    pending_comparators=value["pending_candidates"],
                    recorded_primary_seconds=value["rows"]["primary"]["t_c_s"],
                    current_C2_primary_matches=case in by_case
                    and comparator in actual
                    and math.isclose(
                        value["rows"]["primary"]["t_c_s"],
                        actual[comparator]["recorded_primary_t_c_seconds"],
                        rel_tol=2e-11,
                        abs_tol=2e-12,
                    ),
                    recorded_stop=value["stop"],
                    stop_is_historical_source_cost_model_not_current_complete_quantum_runtime=True,
                    same_law_complete_financial_confidence_supported=False,
                )
            )
        decisions.append(dict(receipt=directory, status=data["status"], rows=rows))
    other = []
    for directory, name in (
        ("c5/rates", "c5_rates.json"),
        ("c7/rates", "c7_rates.json"),
        ("q4", "q4.json"),
        ("q4_d2", "q4_deviation_d2.json"),
        ("sigma_dev", "sigma_dev.json"),
    ):
        data = snap.json(CLASSICAL / directory / name)
        if data is not None:
            other.append(
                dict(
                    receipt=directory + "/" + name,
                    captured_top_level_keys=list(data),
                    pricing_reexecuted=False,
                    interpretation="Existingevidence retained; a rate,payoff comparison orvariancepilot alone isnota fullcontinuouslaw/accuracy/runtime certificate",
                    recorded_meta=data.get("meta"),
                )
            )
    return dict(
        interim_decisions=decisions,
        additional_existing_receipts=other,
        GPU_and_plainMC_timing_anchors_not_implicitly_filled=True,
        current_quantum_physical_time=None,
        current_fullcontinuous_price_bias=None,
    )


def run(output):
    snap = Snapshot(output)
    assert not (snap.output / "summary.json").exists()
    assert sha(Path(__file__).resolve()) == snap.by_name[relative(Path(__file__).resolve())]["sha256"]
    assert sha(sys.executable) == snap.protocol["interpreter_sha256"]
    c1, c2 = snap.json(CLASSICAL / "c1/c1_summary.json"), snap.json(CLASSICAL / "c2/c2_timing.json")
    law = source_and_law(snap)
    save(snap.output / "source_estimand_law_ledger.json", law)
    rates = rate_ledger(snap, c1)
    save(snap.output / "canonical_rate_prefix_audit.json", rates)
    timing = timing_ledger(snap, c1, c2)
    save(snap.output / "measured_and_modelled_timing_ledger.json", timing)
    refs = references_ledger(snap)
    save(snap.output / "independent_reference_status.json", refs)
    coverage = coverage_ledger(snap)
    save(snap.output / "coverage_completion_status.json", coverage)
    other = decisions_and_other_receipts(snap, timing)
    save(snap.output / "historical_decision_and_other_status.json", other)
    provenance_rows = []
    for path, data in (
        (CLASSICAL / "c1/c1_summary.json", c1),
        (CLASSICAL / "c2/c2_timing.json", c2),
        (CLASSICAL / "c3_refa/ref_a.json", snap.json(CLASSICAL / "c3_refa/ref_a.json")),
        (CLASSICAL / "c4/meta.json", snap.json(CLASSICAL / "c4/meta.json")),
    ):
        if data is not None:
            provenance_rows.append(provenance(snap, relative(path), data))
    for case in ("B4x12", "B8x52"):
        path = CLASSICAL / "c3_refb" / case / "ref_b.json"
        data = snap.json(path)
        if data is not None:
            provenance_rows.append(provenance(snap, relative(path), data))
    save(snap.output / "recorded_source_provenance_audit.json", provenance_rows)
    drift = []
    for record in snap.protocol["files"]:
        path = ROOT / record["original"]
        current = sha(path) if path.exists() else None
        if current != record["sha256"]:
            drift.append(
                dict(
                    original=record["original"],
                    captured_sha256=record["sha256"],
                    current_sha256=current,
                    original_live_receipt=record["potentially_live_original"],
                    interpreted_captured_bytes_only=True,
                )
            )
        assert sha(ROOT / record["snapshot"]) == record["sha256"]
    save(snap.output / "live_original_change_report.json", drift)
    rows = timing["rows"]
    summary = dict(
        passed=True,
        local_only=True,
        bounded_receipt_inventory_audited=True,
        captured_files=snap.protocol["captured_file_count"],
        timing_rows_reconciled=len(rows),
        confirmation_rows=sum(r["confirmation_replications"] > 0 for r in rows),
        scaled_confirmation_rows=sum(r["scale_is_a_modelled_count_time_adjustment"] for r in rows),
        entirely_modelled_rows=sum(r["measured_median_wall_seconds"] is None for r in rows),
        actual_reference_status=refs,
        coverage_complete_and_scored=coverage["all_declared_raw_arms_present"]
        and coverage["completed_scored_coverage_available"],
        numerical_parse_errors=snap.parse_errors,
        original_live_file_changes_during_audit=len(drift),
        existing_jobs_untouched=True,
        no_classical_job_executed=True,
        no_bootstrap_or_new_coverage_scoring=True,
        no_financial_gate_replays=True,
        source_target_laws_identical=False,
        full_common_continuous_price_bridge_certified=False,
        exact_finite_law_classical_comparator_timed=False,
        scaled_t_c_credited_as_timed_success=False,
        C09_complete=False,
        G4_closed=False,
        complete_runtime_quantum_advantage_claim=False,
        immediate_blockers=[
            "Fullpath continuous/digital price bridge remainsopen, or a separately qualified exactfinite comparator isneeded",
            "Scaledconfirmation/model times arederivedfields; successful accuracy-target execution remainsseparate",
            "Coverage/refprecision mustqualify the classical confidence at thechosenoriginalaccuracy",
            "Stage C comparator minimum andhardware sensitivities mustretain pending/existing methods honestly",
            "Complete physical quantum runtime remainsunknown",
        ],
        candidate_timing_rows=[
            {
                k: r[k]
                for k in (
                    "case",
                    "method",
                    "epsilon_dollars",
                    "n_target_fitted_per_scramble",
                    "actual_n_run_per_scramble",
                    "measured_median_wall_seconds",
                    "pooled_hw16_dollars",
                    "scale",
                    "recorded_primary_t_c_seconds",
                    "recorded_primary_convention",
                    "scale_is_a_modelled_count_time_adjustment",
                )
            }
            for r in rows
        ],
    )
    save(snap.output / "summary.json", summary)
    finish_manifest(snap.output)
    print(
        "C09 source/estimand/timing inventory PASS; completeclassicalcomparison remainsOPEN",
        flush=True,
    )
    print(
        "timing rows",
        len(rows),
        "scaled confirmations",
        summary["scaled_confirmation_rows"],
        "modelled rows",
        summary["entirely_modelled_rows"],
        "coveragecomplete",
        summary["coverage_complete_and_scored"],
        flush=True,
    )


def finish_manifest(output):
    save(
        output / "manifest.json",
        dict(
            files={relative(path): sha(path) for path in output.rglob("*") if path.is_file()},
            snapshot_inputs_immutable=True,
            originals_may_be_live_and_were_never_written=True,
            manifest_self_hash_excluded=True,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.phase == "prepare":
        prepare(args.output)
    else:
        try:
            run(args.output)
        except Exception as failure:
            output = args.output.resolve()
            (output / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    local_only=True,
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    existing_jobs_untouched=True,
                    no_classical_job_executed=True,
                    no_financial_gate_replays=True,
                    scaled_t_c_credited_as_timed_success=False,
                    C09_complete=False,
                    G4_closed=False,
                ),
            )
            finish_manifest(output)
            raise
