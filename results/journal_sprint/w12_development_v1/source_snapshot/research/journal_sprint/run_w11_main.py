"""Prospective reference/main classical stages, separately gated and archived."""

import argparse
import json
from pathlib import Path
import os
import shutil
import time

import numpy as np
from scipy.stats import t

from .asian_basket import Basket
from .run_encoding_decision import verify_inventory
from .run_shortlist import assert_numeric_equal, without_timing
from .run_w11_baselines import (
    PROTOCOL, append_event, inventory_environment, telemetry,
)
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from .w11_baselines import METHODS, NAMESPACE, deployment


AMENDMENT = ROOT / "docs/journal_sprint/PROTOCOL_W11_MAIN_V1.md"


def schedule_for(stage):
    if stage not in ("reference", "main"):
        raise ValueError("unknown stage")
    rows = []
    if stage == "main":
        rows = [dict(assets=2, dates=12, strike=100., power=8, rep=0,
                     method=m, phase="main_warmup") for m in METHODS]
    for assets in (2, 4):
        for dates in (12, 52):
            for strike in (90., 100., 110.):
                for power in ((15,) if stage == "reference" else (10, 12, 14)):
                    for rep in range(32 if stage == "reference" else 16):
                        methods = ("rqmc_cv",) if stage == "reference" else tuple(
                            METHODS[int(i)] for i in rng_for(
                                NAMESPACE, "main_order", assets, dates, strike, power, rep
                            ).permutation(4)
                        )
                        for method in methods:
                            rows.append(dict(assets=assets, dates=dates, strike=strike,
                                             power=power, rep=rep, method=method, phase=stage))
    return [dict(row, attempt=i) for i, row in enumerate(rows)]


def contract_key(spec):
    return f"{spec['assets']}/{spec['dates']}/{spec['strike']:g}"


def reference_summary(rows):
    groups = {}
    for row in rows:
        groups.setdefault(contract_key(row["spec"]), []).append(row["result"]["value"])
    return {key: dict(count=len(values), mean=float(np.mean(values)),
                      se=float(np.std(values, ddof=1)/np.sqrt(len(values)))
                      if len(values) > 1 else None)
            for key, values in groups.items()}


def reference_gate(path):
    verify_inventory(path)
    plan = json.loads((path / "planned.json").read_text())
    if plan["config"]["stage"] != "reference":
        raise ValueError("reference archive required")
    saved_schedule = json.loads((path / "schedule.json").read_text())
    assert_numeric_equal(saved_schedule, schedule_for("reference"))
    rows = [json.loads(p.read_text()) for p in sorted(path.glob("row_*.json"))]
    if len(rows) != len(saved_schedule):
        raise ValueError("reference stage incomplete")
    for row, spec in zip(rows, saved_schedule):
        assert_numeric_equal(row["spec"], spec)
    refs = reference_summary(rows)
    if len(refs) != 12 or any(r["count"] != 32 or not 0 <= r["se"] <= .001
                              for r in refs.values()):
        raise ValueError("reference precision diagnostic gate failed")
    return refs


def main_summary(rows, refs):
    groups = {}
    for row in rows:
        spec = row["spec"]
        if spec["phase"] != "main":
            continue
        key = (contract_key(spec), spec["power"], spec["method"])
        groups.setdefault(key, []).append(row["result"])
    out = []
    for (key, power, method), values in sorted(groups.items()):
        a = np.array([v["value"] for v in values])
        n = len(a)
        costs = [v["standalone_seconds"] for v in values]
        out.append(dict(contract=key, power=power, method=method, repetitions=n,
                        mean=float(a.mean()), reference=refs[key]["mean"],
                        reference_se=refs[key]["se"],
                        rmse_to_reference=float(np.sqrt(np.mean((a-refs[key]["mean"])**2))),
                        between_deployment_sd=float(a.std(ddof=1)) if n > 1 else None,
                        approximate_mean_t_halfwidth=float(t.ppf(.975, n-1)*a.std(ddof=1)/n**.5)
                        if n > 1 else None,
                        mean_standalone_seconds=float(np.mean(costs)),
                        aggregate_mean_cost_seconds=float(np.sum(costs)),
                        aggregate_evaluation_count=sum(v["evaluation_count"] for v in values),
                        aggregate_training_count=sum(v["training_count"] for v in values),
                        **{f"mean_{field}": float(np.mean([v[field] for v in values])) for field in
                           ("setup_seconds", "training_seconds", "evaluation_seconds",
                            "amortized_10_seconds", "amortized_100_seconds")}))
    return out


def run(output, stage, reference=None):
    # This gate is read-only and precedes output creation/main observations.
    refs = reference_gate(reference) if stage == "main" else None
    schedule = schedule_for(stage)
    if any(os.environ.get(k) != "1" for k in
           ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")):
        raise ValueError("single-thread environment required")
    sources = sorted((ROOT / "research/journal_sprint").rglob("*.py")) + [PROTOCOL, AMENDMENT]
    hashes = {str(p.relative_to(ROOT)): sha256(p) for p in sources}
    cap = 900 if stage == "reference" else 1500
    output = start_run(output, dict(stage=stage, replay_sources=hashes, cap_seconds=cap,
                                   reference_archive=str(reference) if reference else None,
                                   reference_manifest_sha256=sha256(reference / "complete.json")
                                   if reference else None, quantum_results=False))
    attempt = None
    try:
        for source in sources:
            target = output / "source_snapshot" / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if sha256(target) != hashes[str(source.relative_to(ROOT))]:
                raise ValueError("source changed during snapshot")
        write_json(output / "environment.json", inventory_environment())
        write_json(output / "schedule.json", schedule)
        if refs is not None:
            write_json(output / "reference_values.json", refs)
        telemetry()
        rows = []
        before = time.perf_counter()
        for spec in schedule:
            if time.perf_counter() - before >= cap:
                break
            attempt = spec["attempt"]
            append_event(output, dict(attempt=attempt, status="started", **telemetry()))
            unit_start = time.perf_counter()
            result = deployment(Basket(spec["assets"], spec["dates"], spec["strike"]), spec)
            row = dict(spec=spec, result=result, telemetry=telemetry(),
                       unit_wall_seconds=time.perf_counter()-unit_start)
            write_json(output / f"row_{attempt:04d}.json", row)
            append_event(output, dict(attempt=attempt, status="completed"))
            rows.append(row)
            attempt = None
            if len(rows) % 32 == 0:
                print(f"{stage}: {len(rows)}/{len(schedule)}", flush=True)
        acquisition_seconds = time.perf_counter()-before
        before = time.perf_counter()
        analysis = reference_summary(rows) if stage == "reference" else main_summary(rows, refs)
        analysis_seconds = time.perf_counter()-before
        write_json(output / "analysis.json", analysis)
        summary = dict(stage=stage, completed=len(rows), planned=len(schedule),
                       status="complete" if len(rows) == len(schedule) else "time_cap_partial",
                       acquisition_wall_seconds=acquisition_seconds,
                       analysis_seconds=analysis_seconds)
        write_json(output / "summary.json", summary)
        finish_run(output)
        return summary
    except BaseException as error:
        append_event(output, dict(attempt=attempt, status="failed",
                                  error_type=type(error).__name__, error=str(error)))
        write_json(output / "failure.json", dict(
            attempt=attempt, error_type=type(error).__name__, error=str(error)
        ))
        raise


def verify(output):
    files = verify_inventory(output)
    config = json.loads((output / "planned.json").read_text())["config"]
    for relative, digest in config["replay_sources"].items():
        if (sha256(ROOT / relative) != digest
                or sha256(output / "source_snapshot" / relative) != digest):
            raise ValueError("source differs from frozen replay source")
    schedule = json.loads((output / "schedule.json").read_text())
    assert_numeric_equal(schedule, schedule_for(config["stage"]))
    # Four-digit stage filenames differ from the pilot; reconcile directly.
    events = [json.loads(line) for line in (output / "events.jsonl").read_text().splitlines()]
    rows = []
    for index, path in enumerate(sorted(output.glob("row_*.json"))):
        saved = json.loads(path.read_text())
        spec = schedule[index]
        assert_numeric_equal(saved["spec"], spec)
        statuses = [e["status"] for e in events if e["attempt"] == index]
        if statuses != ["started", "completed"]:
            raise ValueError("unreconciled attempt events")
        result = deployment(Basket(spec["assets"], spec["dates"], spec["strike"]), spec)
        assert_numeric_equal(without_timing(result), without_timing(saved["result"]))
        rows.append(saved)
        if len(rows) % 128 == 0:
            print(f"replayed {len(rows)}/{len(schedule)}", flush=True)
    summary = json.loads((output / "summary.json").read_text())
    if summary["completed"] != len(rows):
        raise ValueError("denominator mismatch")
    if config["stage"] == "reference":
        analysis = reference_summary(rows)
    else:
        refpath = Path(config["reference_archive"])
        if sha256(refpath / "complete.json") != config["reference_manifest_sha256"]:
            raise ValueError("reference manifest changed")
        refs = reference_gate(refpath)
        assert_numeric_equal(refs, json.loads((output / "reference_values.json").read_text()))
        analysis = main_summary(rows, refs)
    assert_numeric_equal(analysis, json.loads((output / "analysis.json").read_text()))
    return dict(verified=True, files=files, replayed_rows=len(rows),
                acquisition_status=summary["status"], timings_reproduced=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--stage", choices=("reference", "main"))
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        result = verify(args.output)
    else:
        if args.stage is None or (args.stage == "main" and args.reference is None):
            parser.error("stage required; main also requires --reference")
        result = run(args.output, args.stage, args.reference)
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
