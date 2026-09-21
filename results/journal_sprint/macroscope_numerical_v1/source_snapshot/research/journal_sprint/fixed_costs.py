"""Audited logical cost ledgers for fixed schedules; excludes hardware routing."""

import argparse
import json
import shutil
from pathlib import Path

from .storage import ROOT, finish_run, sha256, start_run, write_json


def schedule_cost(profiles, depths, shots, calibration_shots=8192):
    if not depths or len(depths) != len(shots):
        raise ValueError("nonempty depths and shots must match")
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in depths):
        raise ValueError("nonnegative integer depths required")
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 1 for x in shots):
        raise ValueError("positive integer shot counts required")
    if (
        isinstance(calibration_shots, bool)
        or not isinstance(calibration_shots, int)
        or calibration_shots < 0
    ):
        raise ValueError("nonnegative integer calibration shots required")
    if any(k not in profiles for k in depths):
        raise ValueError("missing compiled depth profile")
    return {
        "pricing_shots": sum(shots),
        "pricing_A_equivalents": sum((2 * k + 1) * s for k, s in zip(depths, shots)),
        "pricing_Grover_queries": sum(k * s for k, s in zip(depths, shots)),
        "pricing_logical_cx": sum(
            profiles[k]["gates"].get("cx", 0) * s for k, s in zip(depths, shots)
        ),
        "pricing_logical_u": sum(
            profiles[k]["gates"].get("u", 0) * s for k, s in zip(depths, shots)
        ),
        "max_circuit_depth": max(profiles[k]["depth"] for k in depths),
        "max_qubits": max(profiles[k]["total_qubits"] for k in depths),
        "calibration_shots": calibration_shots,
        "total_shots": sum(shots) + calibration_shots,
    }


def fixed_allocation(profiles, budget, axis):
    if isinstance(budget, bool) or not isinstance(budget, int) or budget < 9:
        raise ValueError("integer reference A budget >=9 required")
    if axis == "A_equivalents":
        return [budget], [budget // 9] * 3
    if axis == "logical_cx":
        cap = budget * profiles[0]["gates"]["cx"]
        cost_per_ladder = sum(profiles[k]["gates"]["cx"] for k in (0, 1, 2))
        per_depth = cap // cost_per_ladder
        if per_depth < 1:
            raise ValueError("CX cap cannot fund one ladder")
        return [budget], [per_depth] * 3
    raise ValueError("unknown cost axis")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week5_fixed_costs_v1")
    args = parser.parse_args()
    rows = []
    verified = {}
    for name in ("week3_resources_v1", "week5_resources_v1"):
        folder = ROOT / "results/journal_sprint" / name
        manifest = json.loads((folder / "complete.json").read_text())
        for relative, expected in manifest["sha256"].items():
            if sha256(folder / relative) != expected:
                raise ValueError(f"hash mismatch: {name}/{relative}")
        verified[name] = {
            "files": len(manifest["sha256"]),
            "manifest_sha256": sha256(folder / "complete.json"),
        }
        rows += json.loads((folder / "summary.json").read_text())["rows"]
    groups = {}
    for row in rows:
        key = (row["contract"], row["n"], row["scale"])
        group = groups.setdefault(key, {})
        if row["k"] in group:
            raise ValueError("duplicate profile")
        group[row["k"]] = row
    if len(groups) != 10 or any(set(group) != {0, 1, 2} for group in groups.values()):
        raise ValueError("incomplete profile matrix")
    ledger = []
    for (cid, n, scale), profiles in sorted(groups.items()):
        for budget in (73728, 294912):
            for axis in ("A_equivalents", "logical_cx"):
                direct, multi = fixed_allocation(profiles, budget, axis)
                direct_cost = schedule_cost(profiles, [0], direct)
                multi_cost = schedule_cost(profiles, [0, 1, 2], multi)
                field = "pricing_" + axis
                if multi_cost[field] > direct_cost[field]:
                    raise ValueError("multidepth allocation exceeds cap")
                ledger.append(
                    {
                        "contract": cid,
                        "n": n,
                        "scale": scale,
                        "axis": axis,
                        "reference_A_budget": budget,
                        "direct_shots": direct,
                        "multi_shots": multi,
                        "direct": direct_cost,
                        "multi": multi_cost,
                        "unused_multidepth_budget": direct_cost[field] - multi_cost[field],
                    }
                )
    path = start_run(
        args.output,
        {
            "source_manifests": verified,
            "reference_A_budgets": [73728, 294912],
            "calibration_shots_per_state": 4096,
        },
    )
    write_json(path / "ledger.json", ledger)
    shutil.copy2(__file__, path / "fixed_costs.py")
    write_json(
        path / "scope.json",
        {
            "source_file_sha256": sha256(Path(__file__)),
            "note": "Logical pricing gates only; no routing/reset/measurement or hardware time. "
            "Calibration counted in shots, not included in pricing gate totals.",
        },
    )
    finish_run(path)
    print(f"Verified {len(rows)} profiles; recorded {len(ledger)} fixed-cost comparisons")


if __name__ == "__main__":
    main()
