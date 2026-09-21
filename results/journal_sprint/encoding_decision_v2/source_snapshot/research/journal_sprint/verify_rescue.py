"""Archive integrity, pure-target checks, and deterministic inference replay."""

import argparse
from dataclasses import asdict, replace
import json
import math
from pathlib import Path

from .checks import archive_names, archive_path, require
from .run_rescue import acquisition, summarize
from .storage import ROOT, sha256, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc
from research.paper_a.references import black_scholes_call, grid_points, grid_probabilities, p_grid


def verify(folder):
    folder = Path(folder)
    manifest = json.loads((folder / "complete.json").read_text())["sha256"]
    require(
        archive_names(manifest)
        == {
            p.relative_to(folder).as_posix()
            for p in folder.rglob("*")
            if p.is_file() and p != folder / "complete.json"
        },
        "archive inventory mismatch",
    )
    for name, digest in manifest.items():
        require(sha256(archive_path(folder, name)) == digest, "archive hash mismatch")
    config = json.loads((folder / "planned.json").read_text())["config"]
    require(
        config["protocol"] == "PROTOCOL_RESCUE_V1" and config["replicates"] == 30, "wrong protocol"
    )
    needed = {
        "research/journal_sprint/" + n
        for n in (
            "run_rescue.py",
            "exact_payoff.py",
            "anytime_readout.py",
            "calibrated_readout.py",
            "intervals.py",
            "tighter_grid.py",
        )
    }
    needed.add("docs/journal_sprint/PROTOCOL_RESCUE_V1.md")
    require(needed <= archive_names(config["sources"]), "missing producing source")
    for name, digest in config["sources"].items():
        require(sha256(archive_path(ROOT, name)) == digest, "live source drift")
        require(sha256(archive_path(folder / "source_snapshot", name)) == digest, "snapshot drift")
    rows = [json.loads(line) for line in (folder / "records.jsonl").read_text().splitlines()]
    require(len(rows) == 4320, "record count mismatch")
    cursor = 0
    for name in C6:
        c = by_id(name)
        profiles = json.loads((folder / f"profile_{name}.json").read_text())
        old, _ = tighter_bounds_for(c, 6, 0.125)
        exact = replace(
            old, sensitivity=math.exp(-c.r * c.T) * (old.upper - c.K), offset=0.0, encoding=0.0
        )
        pi = grid_probabilities(c, old.lower, old.upper, 6)
        x = grid_points(old.lower, old.upper, 6)
        for encoding, b in (("linearized", old), ("exact_table", exact)):
            require(profiles[encoding]["bounds"] == asdict(b), "bound mismatch")
            amplitude = (
                a_calc(pi, x, c.K, old.upper, 0.125)
                if encoding == "linearized"
                else p_grid(c, old.lower, old.upper, 6) / exact.sensitivity
            )
            require(abs(profiles[encoding]["amplitude"] - amplitude) < 1e-12, "target mismatch")
            for k in ("0", "1", "2"):
                require(
                    profiles[encoding]["profiles"][k]["amplitude_error"] <= 1e-9, "circuit mismatch"
                )
        for guard in (0.0, 0.003, 0.03):
            for axis in ("shots", "cx"):
                for encoding in ("linearized", "exact_table"):
                    for rep in range(30):
                        expected = acquisition(
                            c,
                            encoding,
                            profiles[encoding],
                            guard,
                            axis,
                            rep,
                            profiles["linearized"]["profiles"]["0"]["gates"]["cx"],
                        )
                        expected = json.loads(json.dumps(expected, allow_nan=False))
                        require(rows[cursor : cursor + 2] == expected, "inference replay mismatch")
                        cursor += 2
    require(
        json.loads((folder / "summary.json").read_text()) == summarize(rows), "summary mismatch"
    )
    classical = json.loads((folder / "classical.json").read_text())
    require([r["contract"] for r in classical] == list(C6), "classical inventory mismatch")
    for row in classical:
        c = by_id(row["contract"])
        b, _ = tighter_bounds_for(c, 6, 0.125)
        require(
            row["terms"] == 64 and abs(row["value"] - p_grid(c, b.lower, b.upper, 6)) < 1e-12,
            "classical target mismatch",
        )
        require(row["continuous_error"] <= row["bound"], "classical bound violation")
        require(abs(row["bound"] - (b.support + b.grid)) < 1e-12, "classical bound mismatch")
        truth = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
        require(
            abs(row["continuous_error"] - abs(row["value"] - truth)) < 1e-12,
            "classical error mismatch",
        )
    return dict(
        verified=True,
        replayed_rows=cursor,
        files_checked=len(manifest),
        scope=(
            "target arithmetic, archive integrity and inference replay; "
            "not hardware or external peer review"
        ),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    result = verify(args.source)
    write_json(args.report, result)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
