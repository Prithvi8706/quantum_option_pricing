"""Bounded boundary-tail and disconnected-set diagnostic; not certification."""

import argparse
import json
import os
import shutil
import time

import mpmath as mp

from . import numerical_reference as nr
from .calibrated_readout import invert_calibrated
from .storage import ROOT, start_run, finish_run, sha256, write_json


def cases(extension=False):
    rows = []
    schedules = ([1], [2], [1, 2], [0, 1, 2])
    for ds in schedules:
        for n in (128, 30000, 100000):
            for guard in ("0", ".01"):
                for counts in (
                    [0] * len(ds),
                    [n] * len(ds),
                    [0 if j % 2 == 0 else n for j in range(len(ds))],
                ):
                    rows.append(dict(depths=ds, shots=n, guard=guard, counts=counts))
    for ds in schedules:
        for count in (64, 127):
            rows.append(dict(depths=ds, shots=128, guard="0", counts=[count] * len(ds)))
    if extension:
        for n in (8, 16, 32):
            rows.append(dict(depths=[1, 2], shots=n, guard="0", counts=[n // 2] * 2))
    return [dict(case_id=f"w10_{i:03}", **r) for i, r in enumerate(rows)]


def interval(k, n, alpha):
    if not isinstance(n, int) or n < 1 or not 0 <= k <= n or not 0 < alpha < 1:
        raise ValueError("invalid interval")
    if k == 0:
        return mp.mpf(0), -mp.expm1(mp.log(alpha / 2) / n)
    if k == n:
        return mp.exp(mp.log(alpha / 2) / n), mp.mpf(1)
    if n > 128:
        raise ValueError("large interior counts outside declared scope")
    return nr.cp(k, n, alpha)


def reference(row, precision):
    with mp.workdps(precision):
        alpha = mp.mpf(".025")
        upper = interval(0, 64, alpha / 2)[1] + mp.mpf(row["guard"])
        result = [(mp.mpf(0), mp.mpf(1))]
        for count, depth in zip(row["counts"], row["depths"]):
            lo, hi = interval(count, row["shots"], alpha / len(row["depths"]))
            branch = nr.preimage(
                max(0, (lo - upper) / (1 - upper)), min(1, hi / (1 - upper)), depth
            )
            result = nr.union([(max(a, c), min(b, d)) for a, b in result for c, d in branch])
        return result


def compare(row):
    production, _ = invert_calibrated(
        row["counts"],
        [row["shots"]] * len(row["depths"]),
        row["depths"],
        [0, 0],
        [64, 64],
        transfer_bounds=(float(row["guard"]),) * 2,
    )
    a, b = reference(row, 80), reference(row, 100)
    with mp.workdps(100):
        stable = len(a) == len(b) and all(
            abs(x - y) < mp.mpf("1e-40") for pair, other in zip(a, b) for x, y in zip(pair, other)
        )
        enclosed = all(
            any(mp.mpf(c) <= lo and hi <= mp.mpf(d) for c, d in production.components)
            for lo, hi in b
        )
        return dict(
            **row,
            stable=stable,
            encloses=enclosed,
            production=production.components,
            reference=[[mp.nstr(x, 70), mp.nstr(y, 70)] for x, y in b],
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--extension", action="store_true")
    args = parser.parse_args()
    sources = [
        ROOT / "research/journal_sprint" / name
        for name in (
            "week10_stress.py",
            "numerical_reference.py",
            "calibrated_readout.py",
            "intervals.py",
            "storage.py",
        )
    ]
    sources.append(ROOT / "docs/journal_sprint/PROTOCOL_W10_STRESS.md")
    sources.append(ROOT / "docs/journal_sprint/PROTOCOL_W10_EXTENSION.md")
    output = start_run(
        args.output,
        dict(
            protocol="PROTOCOL_W10_STRESS",
            extension=args.extension,
            mpmath=mp.__version__,
            sources={str(p.relative_to(ROOT)): sha256(p) for p in sources},
        ),
    )
    rows = []
    tick = time.monotonic()
    try:
        for p in sources:
            target = output / "source_snapshot" / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            if sha256(p) != sha256(target):
                raise ValueError("snapshot drift")
        write_json(output / "cases.json", cases(args.extension))
        with (output / "records.jsonl").open("x", encoding="utf-8") as stream:
            for row in cases(args.extension):
                if time.monotonic() - tick > 900:
                    raise RuntimeError("elapsed limit")
                result = compare(row)
                rows.append(result)
                stream.write(json.dumps(result, allow_nan=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
        summary = dict(
            cases=len(rows),
            failed=sum(not r["encloses"] for r in rows),
            unstable=sum(not r["stable"] for r in rows),
            disconnected=sum(len(r["reference"]) > 1 for r in rows),
            disconnected_intersections=sum(
                r["depths"] == [1, 2] and len(r["reference"]) > 1 for r in rows
            ),
            empty=sum(not r["reference"] for r in rows),
            elapsed=time.monotonic() - tick,
        )
        write_json(output / "summary.json", summary)
        if summary["failed"] or summary["unstable"] or not summary["disconnected_intersections"]:
            raise ValueError("numerical or required topology gate failed")
        finish_run(output)
        print(json.dumps(summary))
    except Exception as exc:
        write_json(output / "failure.json", dict(completed=len(rows), error=str(exc)))
        raise


if __name__ == "__main__":
    main()
