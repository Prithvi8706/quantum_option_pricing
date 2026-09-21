"""Reconstruct week-6 discovery and calculate descriptive contrasts."""

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
import json
from pathlib import Path
import shutil

from .run_fixed_discovery import DESIGNS, checked_inputs, designs_for, summarize_cell
from .run_transfer_grid import CALIBRATIONS, SHIFTS, cells, trial
from .storage import ROOT, finish_run, sha256, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc
from research.paper_a.references import black_scholes_call, grid_points, grid_probabilities


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_config(config, manifests):
    expected = dict(
        protocol="PROTOCOL_W6_TRANSFER_GRID",
        contracts=list(C6),
        calibration_sizes=list(CALIBRATIONS),
        shifts=[list(s) for s in SHIFTS],
        designs=list(DESIGNS),
        repetitions=100,
        budget=294912,
        n=6,
        scale=0.125,
        tolerance=1.0,
        alpha_calibration=0.025,
        alpha_validation=0.025,
        transfer_bounds=[0.03, 0.03],
        calibration_rates=[0.02, 0.07],
        max_seconds=900,
        max_record_bytes=250_000_000,
        input_manifests=manifests,
    )
    require(
        {k: v for k, v in config.items() if k != "dependency_sha256"} == expected,
        "declared configuration mismatch",
    )


def contrasts(rows):
    index = {(r["contract"], r["calibration_n"], r["position"], r["design"]): r for r in rows}
    require(len(index) == len(rows) == 324 and set(index) == set(cells()), "cell matrix")

    def rate(r):
        return r["declared"] / r["executed"] if r["executed"] else None

    def delta(a, b):
        return None if a is None or b is None else a - b

    calibration, design, ranges = [], [], []
    for cid in C6:
        for p in range(9):
            for name in DESIGNS:
                low, high = [index[cid, n, p, name] for n in CALIBRATIONS]
                calibration.append(
                    dict(
                        contract=cid,
                        position=p,
                        design=name,
                        delivery_difference=delta(rate(high), rate(low)),
                        added_calibration_shots_per_acquisition=24576,
                        added_acquired_shots=high["acquisition_totals"]["calibration_shots"]
                        - low["acquisition_totals"]["calibration_shots"],
                    )
                )
            for n in CALIBRATIONS:
                for name in DESIGNS[1:]:
                    design.append(
                        dict(
                            contract=cid,
                            position=p,
                            calibration_n=n,
                            design=name,
                            delivery_difference=delta(
                                rate(index[cid, n, p, name]), rate(index[cid, n, p, "direct"])
                            ),
                        )
                    )
        for n in CALIBRATIONS:
            for name in DESIGNS:
                group = [index[cid, n, p, name] for p in range(9)]
                rates = [rate(r) for r in group if rate(r) is not None]
                ranges.append(
                    dict(
                        contract=cid,
                        calibration_n=n,
                        design=name,
                        delivery_min=min(rates) if rates else None,
                        delivery_max=max(rates) if rates else None,
                        declared=sum(r["declared"] for r in group),
                        executed=sum(r["executed"] for r in group),
                        attempts=sum(r["attempts"] for r in group),
                    )
                )
    return dict(calibration_contrasts=calibration, design_contrasts=design, rate_ranges=ranges)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=Path("results/journal_sprint/week6_transfer_grid_v1")
    )
    parser.add_argument("--output", default="results/journal_sprint/week6_closeout_v1")
    args = parser.parse_args()
    source = args.source
    manifest = json.loads((source / "complete.json").read_text())
    for name, digest in manifest["sha256"].items():
        require(sha256(source / name) == digest, f"archive hash: {name}")
    config = json.loads((source / "planned.json").read_text())["config"]
    ledger, profiles, manifests = checked_inputs()
    validate_config(config, manifests)
    snapshots = {
        str(p.relative_to(source / "source_snapshot"))
        for p in (source / "source_snapshot").rglob("*")
        if p.is_file()
    }
    require(snapshots == set(config["dependency_sha256"]), "snapshot inventory")
    required = {
        "research/journal_sprint/run_transfer_grid.py",
        "research/journal_sprint/run_fixed_discovery.py",
        "docs/journal_sprint/PROTOCOL_W6_TRANSFER_GRID.md",
    }
    require(required <= {Path(p).as_posix() for p in snapshots}, "required source inventory")
    for name, digest in config["dependency_sha256"].items():
        require(sha256(source / "source_snapshot" / name) == digest, f"planned snapshot: {name}")
        require(sha256(ROOT / name) == digest, f"live source drift: {name}")
    prepared, truths = {}, {}
    for cid in C6:
        b, _ = tighter_bounds_for(by_id(cid), 6, 0.125)
        prepared[cid] = dict(
            bounds=asdict(b),
            bound_total=b.total,
            refused=b.total >= 1,
            designs={} if b.total >= 1 else designs_for(cid, 294912, ledger, profiles[cid]),
        )
    require(
        prepared == json.loads((source / "decisions.json").read_text()),
        "bound/design reconstruction",
    )
    for cid, p in prepared.items():
        if p["refused"]:
            continue
        c, b = by_id(cid), p["bounds"]
        a = a_calc(
            grid_probabilities(c, b["lower"], b["upper"], 6),
            grid_points(b["lower"], b["upper"], 6),
            c.K,
            b["upper"],
            0.125,
        )
        truths[cid] = dict(
            amplitude=a, price=float(black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T))
        )
    require(truths == json.loads((source / "diagnostic_truths.json").read_text()), "truths")
    groups, seen, totals = defaultdict(list), set(), Counter()
    with (source / "records.jsonl").open() as stream:
        for line in stream:
            row = json.loads(line)
            key = tuple(row[k] for k in ("contract", "calibration_n", "position", "design", "rep"))
            require(key not in seen, "duplicate identity")
            seen.add(key)
            cid, n, p, design, rep = key
            replay = trial(cid, n, p, design, rep, prepared[cid], truths.get(cid))
            require(row == json.loads(json.dumps(replay)), f"trial reconstruction: {key}")
            groups[key[:-1]].append(row)
            totals[row["status"]] += 1
            totals["price_contained"] += int(row.get("price_contains", False))
            totals["false_declarations"] += int(row.get("false_declaration", False))
            for field, value in row["cost"].items():
                if not field.startswith("max_"):
                    totals[field] += value
    require(seen == {(*cell, r) for cell in cells() for r in range(100)}, "full identity matrix")
    summary = json.loads((source / "summary.json").read_text())
    require(summary["attempts"] == 32400, "attempts")
    for row in summary["cells"]:
        key = tuple(row[k] for k in ("contract", "calibration_n", "position", "design"))
        recomputed = summarize_cell(groups[key])
        require(recomputed == {k: row[k] for k in recomputed}, "summary reconstruction")
    comparisons = contrasts(summary["cells"])
    output = start_run(args.output, dict(source_manifest_sha256=sha256(source / "complete.json")))
    shutil.copy2(__file__, output / "closeout_transfer_grid.py")
    write_json(
        output / "verification.json",
        dict(
            attempts=len(seen),
            cells=len(groups),
            archive_hashes=len(manifest["sha256"]),
            dependency_hashes=len(snapshots),
            totals=dict(totals),
            scope="exact replay using producing trial/numerical helpers; not independent proof",
        ),
    )
    write_json(output / "contrasts.json", comparisons)
    finish_run(output)
    print(json.dumps(dict(totals)))


if __name__ == "__main__":
    main()
