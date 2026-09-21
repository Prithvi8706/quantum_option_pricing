"""Compare production against independent 80-digit inverse on declared finite cases."""

import argparse
import json
import os
import shutil
import time

import mpmath as mp

from .calibrated_readout import invert_calibrated
from .numerical_reference import PRECISION, STEPS, case_table, reference
from .storage import ROOT, finish_run, sha256, start_run, write_json


def compare(case):
    production, _ = invert_calibrated(
        case["counts"],
        [128] * len(case["depths"]),
        case["depths"],
        case["calibration_errors"],
        [64, 64],
        transfer_bounds=(float(case["guard"]),) * 2,
    )
    expected = reference(case)
    with mp.workdps(PRECISION):
        missing = []
        slack = []
        for lo, hi in expected:
            containing = [
                (mp.mpf(a), mp.mpf(b))
                for a, b in production.components
                if mp.mpf(a) <= lo and hi <= mp.mpf(b)
            ]
            if not containing:
                missing.append([mp.nstr(lo, 70), mp.nstr(hi, 70)])
            else:
                slack.extend([float(lo - containing[0][0]), float(containing[0][1] - hi)])
        return dict(
            **case,
            production_components=production.components,
            reference_components=[[mp.nstr(a, 70), mp.nstr(b, 70)] for a, b in expected],
            missing_components=missing,
            encloses=not missing,
            max_endpoint_slack=max(slack, default=0.0),
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week9_numerical_v1")
    args = parser.parse_args()
    if shutil.disk_usage(ROOT).free < 1_000_000_000:
        raise RuntimeError("need 1 GB free disk")
    sources = sorted((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += [ROOT / "docs/journal_sprint/PROTOCOL_W9_NUMERICAL.md"]
    config = dict(
        protocol="PROTOCOL_W9_NUMERICAL",
        precision=PRECISION,
        bisections=STEPS,
        mpmath=mp.__version__,
        case_count=312,
        dependency_sha256={str(p.relative_to(ROOT)): sha256(p) for p in sources},
    )
    output = start_run(args.output, config)
    tick, rows = time.perf_counter(), []
    try:
        for p in sources:
            target = output / "source_snapshot" / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            if sha256(target) != config["dependency_sha256"][str(p.relative_to(ROOT))]:
                raise ValueError("source drift")
        cases = case_table()
        write_json(output / "cases.json", cases)
        with (output / "records.jsonl").open("x", encoding="utf-8") as stream:

            def limits():
                if time.perf_counter() - tick > 900 or stream.tell() > 100_000_000:
                    raise RuntimeError("numerical diagnostic limit")

            for case in cases:
                limits()
                row = compare(case)
                rows.append(row)
                stream.write(json.dumps(row, allow_nan=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
                limits()
        summary = dict(
            cases=len(rows),
            failed=sum(not r["encloses"] for r in rows),
            empty_reference=sum(not r["reference_components"] for r in rows),
            full_reference=sum(r["reference_components"] == [["0.0", "1.0"]] for r in rows),
            multicomponent_reference=sum(len(r["reference_components"]) > 1 for r in rows),
            max_endpoint_slack=max(r["max_endpoint_slack"] for r in rows),
            elapsed_seconds=time.perf_counter() - tick,
            scope="finite high-precision diagnostic; not certification or coverage",
        )
        write_json(output / "summary.json", summary)
        if summary["failed"]:
            raise AssertionError("reference components not enclosed; preserve and investigate")
        finish_run(output)
        print(json.dumps(summary))
    except Exception as error:
        write_json(output / "failure.json", dict(completed_cases=len(rows), error=str(error)))
        raise


if __name__ == "__main__":
    main()
