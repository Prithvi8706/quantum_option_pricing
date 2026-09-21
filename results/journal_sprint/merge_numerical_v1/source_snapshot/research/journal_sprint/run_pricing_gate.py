"""V2A deterministic feasibility; exact target prices used only for diagnostics."""

import argparse
from dataclasses import asdict
import shutil

from .pricing_bounds import bounds_for
from .storage import ROOT, finish_run, start_run, write_json
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc, to_price
from research.paper_a.references import (
    black_scholes_call,
    grid_points,
    grid_probabilities,
    p_grid,
    support_audit,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/pricing_gate_v2a")
    args = parser.parse_args()
    path = start_run(
        args.output,
        {
            "protocol": "PROTOCOL_V2A",
            "contracts": C6,
            "n": [3, 4, 5, 6],
            "scale": [0.125, 0.25, 0.5],
            "q_total": 1e-5,
            "dollar_targets": ["1", ".01*S0"],
        },
    )
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += [ROOT / "docs/journal_sprint/PROTOCOL_V2A.md"]
    sources += [
        ROOT / "research/paper_a" / name
        for name in ("benchmark.py", "references.py", "payoff.py", "european/circuits.py")
    ]
    for source in sources:
        destination = path / "source_snapshot" / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    rows = []
    for cid in C6:
        c = by_id(cid)
        for n in (3, 4, 5, 6):
            for scale in (0.125, 0.25, 0.5):
                b = bounds_for(c, n, scale)
                # Feasibility only consults bounds, never the diagnostic values below.
                decisions = {
                    "one_dollar": b.probability_budget(1.0),
                    "one_percent_spot": b.probability_budget(0.01 * c.S0),
                }
                support = support_audit(c, 1e-5)
                bs = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
                grid = p_grid(c, b.lower, b.upper, n)
                a = a_calc(
                    grid_probabilities(c, b.lower, b.upper, n),
                    grid_points(b.lower, b.upper, n),
                    c.K,
                    b.upper,
                    scale,
                )
                encoded = to_price(a, c.K, b.upper, scale, c.r, c.T)
                errors = [support.P_support - bs, grid - support.P_support, encoded - grid]
                passed = all(
                    abs(e) <= bound + 1e-9
                    for e, bound in zip(errors, (b.support, b.grid, b.encoding))
                )
                passed = passed and abs(sum(errors) - (encoded - bs)) <= 1e-9
                rows.append(
                    {
                        "contract": cid,
                        "n": n,
                        "scale": scale,
                        "bounds": asdict(b),
                        "total_bound": b.total,
                        "probability_budget": decisions,
                        "diagnostic": {
                            "black_scholes": bs,
                            "support": support.P_support,
                            "grid": grid,
                            "encoded": encoded,
                            "probability": a,
                            "signed_errors": errors,
                        },
                        "bound_checks_pass": bool(passed),
                    }
                )
    write_json(path / "rows.json", rows)
    summary = {
        "configurations": len(rows),
        "all_bound_checks_pass": all(row["bound_checks_pass"] for row in rows),
        "contracts": {},
    }
    for cid in C6:
        group = [row for row in rows if row["contract"] == cid]
        best = min(group, key=lambda row: row["total_bound"])
        summary["contracts"][cid] = {
            "one_dollar_feasible": sum(
                row["probability_budget"]["one_dollar"] > 0 for row in group
            ),
            "one_percent_spot_feasible": sum(
                row["probability_budget"]["one_percent_spot"] > 0 for row in group
            ),
            "smallest_bound": best["total_bound"],
            "n": best["n"],
            "scale": best["scale"],
            "bound_components": {
                key: best["bounds"][key] for key in ("support", "grid", "encoding")
            },
        }
    write_json(path / "summary.json", summary)
    finish_run(path)
    print(summary)
    if not summary["all_bound_checks_pass"]:
        raise SystemExit("Bound validation failed; outputs retained")


if __name__ == "__main__":
    main()
