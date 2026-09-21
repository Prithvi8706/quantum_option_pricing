"""Week-5 fixed-design comparison with distinct calibration/validation streams."""

import argparse
from collections import defaultdict
from dataclasses import asdict
import json
import os
import shutil
import time

import numpy as np

from .calibrated_readout import invert_calibrated
from .fixed_costs import fixed_allocation, schedule_cost
from .intervals import price_decision, response
from .storage import ROOT, finish_run, rng_for, sha256, start_run, write_json
from .tighter_grid import tighter_bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc
from research.paper_a.references import black_scholes_call, grid_points, grid_probabilities

DESIGNS = ("direct", "A_matched", "CX_capped")
BUDGETS = (73728, 294912)
CONDITIONS = ("stationary", "constant_transfer")
COST_FIELDS = (
    "pricing_shots",
    "pricing_A_equivalents",
    "pricing_Grover_queries",
    "pricing_logical_cx",
    "pricing_logical_u",
    "max_circuit_depth",
    "max_qubits",
    "calibration_shots",
    "total_shots",
)


def checked_inputs():
    base = ROOT / "results/journal_sprint"
    manifests = {}
    profiles = defaultdict(dict)
    for name in ("week3_resources_v1", "week5_resources_v1", "week5_fixed_costs_v1"):
        folder = base / name
        manifest = json.loads((folder / "complete.json").read_text())
        for relative, expected in manifest["sha256"].items():
            if sha256(folder / relative) != expected:
                raise ValueError(f"corrupt input {name}/{relative}")
        manifests[name] = sha256(folder / "complete.json")
        if name != "week5_fixed_costs_v1":
            for row in json.loads((folder / "summary.json").read_text())["rows"]:
                if row["n"] == 6 and row["scale"] == 0.125:
                    if row["k"] in profiles[row["contract"]]:
                        raise ValueError("duplicate circuit profile")
                    profiles[row["contract"]][row["k"]] = row
    ledger_path = base / "week5_fixed_costs_v1"
    planned = json.loads((ledger_path / "planned.json").read_text())["config"]
    for name in ("week3_resources_v1", "week5_resources_v1"):
        if planned["source_manifests"][name]["manifest_sha256"] != manifests[name]:
            raise ValueError("ledger source lineage mismatch")
    ledger = json.loads((ledger_path / "ledger.json").read_text())
    return ledger, profiles, manifests


def designs_for(cid, budget, ledger, profiles):
    selected = [
        r
        for r in ledger
        if r["contract"] == cid
        and r["n"] == 6
        and r["scale"] == 0.125
        and r["reference_A_budget"] == budget
    ]
    if len(selected) != 2 or {r["axis"] for r in selected} != {"A_equivalents", "logical_cx"}:
        raise ValueError("missing or duplicate ledger axes")
    if set(profiles) != {0, 1, 2}:
        raise ValueError("incomplete compiled profiles")
    result = {}
    for row in selected:
        direct, multi = fixed_allocation(profiles, budget, row["axis"])
        if direct != row["direct_shots"] or multi != row["multi_shots"]:
            raise ValueError("ledger allocation mismatch")
        for side, depths, shots in (("direct", [0], direct), ("multi", [0, 1, 2], multi)):
            cost = schedule_cost(profiles, depths, shots)
            if cost != row[side]:
                raise ValueError("ledger cost mismatch")
            name = (
                "direct"
                if side == "direct"
                else "A_matched"
                if row["axis"] == "A_equivalents"
                else "CX_capped"
            )
            value = {"depths": depths, "shots": shots, "cost": cost}
            if name in result and result[name] != value:
                raise ValueError("inconsistent shared direct design")
            result[name] = value
    return result


def summarize_cell(rows):
    executed = sum(r["status"] != "pre_refusal" for r in rows)
    declarations = sum(r["status"] == "precision_met" for r in rows)
    false = sum(r.get("false_declaration", False) for r in rows)
    radii = [r["radius"] for r in rows if r.get("radius") is not None]
    return {
        "attempts": len(rows),
        "executed": executed,
        "declared": declarations,
        "incompatible": sum(r["status"] == "incompatible" for r in rows),
        "unresolved": sum(r["status"] == "unresolved" for r in rows),
        "amplitude_contained": sum(r.get("amplitude_contains", False) for r in rows),
        "price_contained": sum(r.get("price_contains", False) for r in rows),
        "false_declarations": false,
        "false_per_attempt": false / len(rows),
        "false_per_executed": false / executed if executed else None,
        "false_given_declaration": false / declarations if declarations else None,
        "median_radius_nonempty": float(np.median(radii)) if radii else None,
        "acquisition_totals": {
            k: sum(r["cost"][k] for r in rows) for k in COST_FIELDS if not k.startswith("max_")
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week5_fixed_discovery_v1")
    args = parser.parse_args()
    ledger, profiles, manifests = checked_inputs()
    path = start_run(
        args.output,
        {
            "protocol": "PROTOCOL_W5_FIXED_DISCOVERY",
            "input_manifests": manifests,
            "contracts": list(C6),
            "budgets": BUDGETS,
            "designs": DESIGNS,
            "conditions": CONDITIONS,
            "repetitions": 100,
            "n": 6,
            "scale": 0.125,
            "tolerance": 1.0,
            "calibration_shots_per_state": 4096,
            "alpha_calibration": 0.025,
            "alpha_validation": 0.025,
            "transfer_bounds": [0.03, 0.03],
        },
    )
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += list((ROOT / "research/paper_a").glob("*.py"))
    sources.append(ROOT / "docs/journal_sprint/PROTOCOL_W5_FIXED_DISCOVERY.md")
    for source in sources:
        target = path / "source_snapshot" / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    attempts = 0
    prepared = {}
    groups = defaultdict(list)
    try:
        for cid in C6:
            tick = time.perf_counter()
            bound, _ = tighter_bounds_for(by_id(cid), 6, 0.125)
            refused = bool(bound.total >= 1)
            prepared[cid] = {
                "bounds": {k: float(v) for k, v in asdict(bound).items()},
                "bound_total": float(bound.total),
                "refused": refused,
                "designs": {}
                if refused
                else {str(b): designs_for(cid, b, ledger, profiles[cid]) for b in BUDGETS},
                "setup_seconds": time.perf_counter() - tick,
            }
        write_json(path / "decisions.json", prepared)
        truths = {}
        for cid in C6:
            if prepared[cid]["refused"]:
                continue
            c = by_id(cid)
            b = prepared[cid]["bounds"]
            a = a_calc(
                grid_probabilities(c, b["lower"], b["upper"], 6),
                grid_points(b["lower"], b["upper"], 6),
                c.K,
                b["upper"],
                0.125,
            )
            price = float(black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T))
            if (
                abs(b["offset"] + b["sensitivity"] * a - price)
                > prepared[cid]["bound_total"] + 1e-9
            ):
                raise ValueError("diagnostic representation-bound check failed")
            truths[cid] = {"amplitude": a, "price": price}
        write_json(path / "diagnostic_truths.json", truths)
        with (path / "records.jsonl").open("x", encoding="utf-8") as stream:
            for cid in C6:
                prepared_contract = prepared[cid]
                for budget in BUDGETS:
                    for condition in CONDITIONS:
                        f, g = (0.02, 0.07) if condition == "stationary" else (0.05, 0.04)
                        for design in DESIGNS:
                            for rep in range(100):
                                key = ("week5_fixed", cid, budget, condition, design, rep)
                                row = {
                                    "contract": cid,
                                    "budget": budget,
                                    "condition": condition,
                                    "design": design,
                                    "rep": rep,
                                    "seed_key": key,
                                }
                                if prepared_contract["refused"]:
                                    row.update(
                                        status="pre_refusal", cost={k: 0 for k in COST_FIELDS}
                                    )
                                else:
                                    fixed = prepared_contract["designs"][str(budget)][design]
                                    depths, shots = fixed["depths"], fixed["shots"]
                                    truth = truths[cid]
                                    errors = rng_for(*key, "calibration").binomial(
                                        4096, [0.02, 0.07]
                                    )
                                    q = f + (1 - f - g) * response(truth["amplitude"], depths)
                                    counts = rng_for(*key, "validation").binomial(shots, q)
                                    confidence, calibration = invert_calibrated(
                                        counts,
                                        shots,
                                        depths,
                                        errors,
                                        [4096] * 2,
                                        transfer_bounds=(0.03, 0.03),
                                    )
                                    b = prepared_contract["bounds"]
                                    decision = price_decision(
                                        confidence,
                                        b["sensitivity"],
                                        b["offset"],
                                        prepared_contract["bound_total"],
                                        1.0,
                                    )
                                    interval = decision["interval"]
                                    row.update(
                                        **decision,
                                        counts=counts.tolist(),
                                        calibration_errors=errors.tolist(),
                                        calibration=calibration,
                                        depths=depths,
                                        shots=shots,
                                        cost=fixed["cost"],
                                        components=confidence.components,
                                        amplitude_contains=confidence.contains(truth["amplitude"]),
                                        price_contains=bool(
                                            interval is not None
                                            and interval[0] <= truth["price"] <= interval[1]
                                        ),
                                        false_declaration=bool(
                                            decision["status"] == "precision_met"
                                            and abs(sum(interval) / 2 - truth["price"]) > 1
                                        ),
                                    )
                                stream.write(json.dumps(row, allow_nan=False) + "\n")
                                attempts += 1
                                groups[(cid, budget, condition, design)].append(row)
                        stream.flush()
                        os.fsync(stream.fileno())
                print(cid, "completed", flush=True)
        cells = [
            {
                "contract": cid,
                "budget": budget,
                "condition": condition,
                "design": design,
                **summarize_cell(rows),
            }
            for (cid, budget, condition, design), rows in sorted(groups.items())
        ]
        write_json(path / "summary.json", {"attempts": attempts, "cells": cells})
        finish_run(path)
    except Exception as error:
        write_json(path / "failure.json", {"completed_attempts": attempts, "error": str(error)})
        raise


if __name__ == "__main__":
    main()
