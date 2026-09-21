"""Week-11 timing pilot only; stage B/C acquisition remains gated separately."""

import argparse
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time

import numpy as np
import psutil

from .asian_basket import Basket
from .run_encoding_decision import verify_inventory
from .run_shortlist import assert_numeric_equal, without_timing
from .storage import ROOT, finish_run, sha256, start_run, write_json
from .w11_baselines import deployment, pilot_schedule


PROTOCOL = ROOT / "docs/journal_sprint/PROTOCOL_W11_BASELINES_V1.md"


def append_event(output, event):
    with (output / "events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, allow_nan=False) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def telemetry():
    memory = psutil.Process().memory_info()
    return dict(rss_bytes=memory.rss,
                peak_working_set_bytes=getattr(memory, "peak_wset", None),
                system_cpu_percent=psutil.cpu_percent(interval=None),
                available_memory_bytes=psutil.virtual_memory().available)


def inventory_environment():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        np.show_config()
    return dict(platform=platform.platform(), processor=platform.processor(),
                logical_cpu_count=os.cpu_count(), psutil_version=psutil.__version__,
                blas_config=buffer.getvalue(),
                total_memory_bytes=psutil.virtual_memory().total,
                external_contention="uncontrolled; sampled system utilization recorded",
                git_status=subprocess.run(["git", "status", "--short"], cwd=ROOT,
                                          capture_output=True, text=True, check=True).stdout,
                tracked_dirty_patch=subprocess.run(["git", "diff", "HEAD", "--binary"],
                                                   cwd=ROOT, capture_output=True, text=True,
                                                   check=True).stdout)


def run(output, cap_seconds=1200., acquire=deployment):
    if not 0 < cap_seconds <= 1200:
        raise ValueError("cap must be positive and <=1200 seconds")
    thread_names = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
    if any(os.environ.get(name) != "1" for name in thread_names):
        raise ValueError("set all numerical-library thread variables to 1 before launching")
    sources = sorted((ROOT / "research/journal_sprint").rglob("*.py")) + [PROTOCOL]
    hashes = {str(p.relative_to(ROOT)): sha256(p) for p in sources}
    schedule = pilot_schedule()
    output = start_run(output, dict(stage="pilot", quantum_results=False,
                                   cap_seconds=cap_seconds, replay_sources=hashes))
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
        # Initialize psutil's sampling interval before the first real unit.
        telemetry()
        before = time.perf_counter()
        completed = 0
        for spec in schedule:
            if time.perf_counter() - before >= cap_seconds:
                break
            attempt = spec["attempt"]
            append_event(output, dict(attempt=attempt, status="started", **telemetry()))
            unit_start = time.perf_counter()
            result = acquire(Basket(spec["assets"], spec["dates"], spec["strike"]), spec)
            row = dict(spec=spec, result=result, telemetry=telemetry(),
                       unit_wall_seconds=time.perf_counter() - unit_start)
            write_json(output / f"row_{attempt:03d}.json", row)
            append_event(output, dict(attempt=attempt, status="completed"))
            completed += 1
            attempt = None
            if completed % 16 == 0:
                print(f"completed {completed}/{len(schedule)} including warmups", flush=True)
        summary = dict(status="complete" if completed == len(schedule) else "time_cap_partial",
                       planned=len(schedule), completed=completed,
                       pilot_rows=max(0, completed-4), warmup_rows=min(completed, 4),
                       acquisition_wall_seconds=time.perf_counter() - before)
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


def audit_events(output):
    """Recover the durable attempt state, including raw-written/event-missing crashes."""
    schedule = json.loads((output / "schedule.json").read_text())
    states = {}
    event_path = output / "events.jsonl"
    if event_path.exists():
        lines = event_path.read_text().splitlines()
        for i, line in enumerate(lines):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                if i != len(lines)-1:
                    raise
                return dict(status="torn_final_event", states=states)
            attempt = event["attempt"]
            if attempt is not None:
                states[str(attempt)] = event["status"]
    out = {}
    for spec in schedule:
        key = str(spec["attempt"])
        state = states.get(key, "not_started")
        raw = (output / f"row_{spec['attempt']:03d}.json").exists()
        if raw and state != "completed":
            state = "raw_present_needs_reconciliation"
        elif not raw and state == "completed":
            state = "completed_event_missing_raw"
        out[key] = state
    return dict(status="audited", states=out)


def verify(output):
    files = verify_inventory(output)
    plan = json.loads((output / "planned.json").read_text())
    for relative, digest in plan["config"]["replay_sources"].items():
        if (sha256(ROOT / relative) != digest
                or sha256(output / "source_snapshot" / relative) != digest):
            raise ValueError("source differs from frozen replay source")
    schedule = json.loads((output / "schedule.json").read_text())
    assert_numeric_equal(schedule, pilot_schedule())
    summary = json.loads((output / "summary.json").read_text())
    paths = sorted(output.glob("row_*.json"))
    if len(paths) != summary["completed"]:
        raise ValueError("row denominator mismatch")
    states = audit_events(output)
    for index, path in enumerate(paths):
        saved = json.loads(path.read_text())
        spec = schedule[index]
        assert_numeric_equal(saved["spec"], spec)
        if states["states"].get(str(index)) != "completed":
            raise ValueError("unreconciled attempt")
        result = deployment(Basket(spec["assets"], spec["dates"], spec["strike"]), spec)
        assert_numeric_equal(without_timing(result), without_timing(saved["result"]))
    return dict(verified=True, files=files, replayed_rows=len(paths),
                pilot_rows=summary["pilot_rows"], acquisition_status=summary["status"],
                timings_reproduced=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    if args.audit:
        result = audit_events(args.output)
    elif args.verify:
        result = verify(args.output)
    else:
        result = run(args.output)
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
