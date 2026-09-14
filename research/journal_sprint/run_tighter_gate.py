"""V2B paired deterministic comparison on the unchanged V2A discovery matrix."""

import argparse
from dataclasses import asdict
import json
import shutil

from .checks import archive_path
from .storage import ROOT, finish_run, sha256, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/pricing_gate_v2b")
    args = parser.parse_args()
    baseline = ROOT / "results/journal_sprint/pricing_gate_v2a_retry1"
    manifest = json.loads((baseline / "complete.json").read_text())
    for relative, expected in manifest["sha256"].items():
        if sha256(archive_path(baseline, relative)) != expected:
            raise ValueError(f"Baseline integrity failure: {relative}")
    inputs = json.loads((baseline / "rows.json").read_text())
    lookup = {(r["contract"], r["n"], r["scale"]): r for r in inputs}
    path = start_run(
        args.output,
        {
            "protocol": "PROTOCOL_V2B",
            "contracts": C6,
            "n": [3, 4, 5, 6],
            "scale": [0.125, 0.25, 0.5],
            "baseline_rows_sha256": sha256(baseline / "rows.json"),
        },
    )
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += [ROOT / "docs/journal_sprint/PROTOCOL_V2B.md"]
    sources += [ROOT / "research/paper_a" / name for name in ("benchmark.py", "references.py")]
    for source in sources:
        destination = path / "source_snapshot" / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    rows = []
    for cid in C6:
        contract = by_id(cid)
        for n in (3, 4, 5, 6):
            for scale in (0.125, 0.25, 0.5):
                b, details = tighter_bounds_for(contract, n, scale)
                # Decisions are made before consulting archived target diagnostics.
                budgets = {
                    "one_dollar": b.probability_budget(1.0),
                    "one_percent_spot": b.probability_budget(0.01 * contract.S0),
                }
                old = lookup[cid, n, scale]
                diagnostic = old["diagnostic"]
                passed = (
                    abs(diagnostic["signed_errors"][1]) <= b.grid + 1e-9
                    and abs(diagnostic["encoded"] - diagnostic["black_scholes"]) <= b.total + 1e-9
                    and b.total <= old["total_bound"] + 1e-9
                )
                for field in ("support", "encoding", "sensitivity", "offset"):
                    passed = passed and abs(getattr(b, field) - old["bounds"][field]) <= 1e-12
                rows.append(
                    {
                        "contract": cid,
                        "n": n,
                        "scale": scale,
                        "bounds": asdict(b),
                        "details": details,
                        "total_bound": b.total,
                        "old_total_bound": old["total_bound"],
                        "probability_budget": budgets,
                        "old_probability_budget": old["probability_budget"],
                        "diagnostic": diagnostic,
                        "checks_pass": bool(passed),
                    }
                )
    write_json(path / "rows.json", rows)
    summary = {
        "configurations": len(rows),
        "all_checks_pass": all(r["checks_pass"] for r in rows),
        "contracts": {},
    }
    for cid in C6:
        group = [row for row in rows if row["contract"] == cid]
        best = min(group, key=lambda row: row["total_bound"])
        summary["contracts"][cid] = {
            "one_dollar_feasible": sum(r["probability_budget"]["one_dollar"] > 0 for r in group),
            "one_percent_spot_feasible": sum(
                r["probability_budget"]["one_percent_spot"] > 0 for r in group
            ),
            "smallest_bound": best["total_bound"],
            "n": best["n"],
            "scale": best["scale"],
            "old_total_bound_at_best": best["old_total_bound"],
            "grid_bound_at_best": best["bounds"]["grid"],
        }
    write_json(path / "summary.json", summary)
    finish_run(path)
    print(json.dumps(summary, indent=2))
    if not summary["all_checks_pass"]:
        raise SystemExit("V2B check failed; all outputs retained")


if __name__ == "__main__":
    main()
