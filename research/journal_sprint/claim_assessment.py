"""Exact secondary checks of frozen W2 evidence; no new pricing acquisition."""

import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def atan_bounds(inverse, terms):
    """Alternating-series rational enclosure for atan(1/inverse)."""
    if type(inverse) is not int or inverse < 2 or type(terms) is not int or terms < 1:
        raise ValueError("positive term count and inverse >= 2 required")
    partial = sum((F((-1) ** k, (2*k+1)*inverse**(2*k+1))
                   for k in range(terms)), F(0))
    following = partial + F((-1)**terms, (2*terms+1)*inverse**(2*terms+1))
    return min(partial, following), max(partial, following)


def pi_bounds():
    a, b = atan_bounds(5, 48), atan_bounds(239, 12)
    return 16*a[0]-4*b[1], 16*a[1]-4*b[0]


PI_LOWER, PI_UPPER = pi_bounds()
REPETITIONS = 17
CALL_CAP = 10_000_000
TOLERANCES = ("0.5", "1", "2")
ALLOWANCES = ("0", "0.01", "0.025", "0.05", "0.1", "0.2")


def universal_radius(coefficients, strike):
    """Norm on the whole independent probability cube, not actual basket support."""
    coefficients = tuple(map(F, coefficients))
    strike = F(strike)
    if not coefficients or any(c < 0 for c in coefficients) or strike < 0:
        raise ValueError("nonempty nonnegative coefficients and strike required")
    total = sum(coefficients, F(0))
    return max(strike, abs(total-strike))


def proxy_optimum(g, beta, a, remaining):
    g, beta, a, remaining = map(F, (g, beta, a, remaining))
    if min(g, beta, a, remaining) <= 0:
        raise ValueError("positive proxy parameters required")
    return 2*a/remaining, 4*g*beta*a/remaining**2


def schedule(beta, deterministic, tolerance="1", extra="0", cap=CALL_CAP):
    beta, deterministic, tolerance, extra = map(F, (beta, deterministic, tolerance, extra))
    if beta <= 0 or deterministic < 0 or tolerance <= 0 or extra < 0:
        raise ValueError("invalid price-budget inputs")
    if type(cap) is not int or cap < 1:
        raise ValueError("positive integer cap required")
    remaining = tolerance-deterministic-extra
    if remaining <= 0:
        return {"status": "deterministic_budget_exhausted", "M": None, "a_calls": None}
    m_size = 2
    while 2*beta*(PI_UPPER/m_size+PI_UPPER**2/m_size**2) > remaining:
        m_size *= 2
        if m_size > 2**40:
            return {"status": "precision_cap", "M": None, "a_calls": None}
    calls = REPETITIONS*(2*m_size-1)
    bound = 2*beta*(PI_UPPER/m_size+PI_UPPER**2/m_size**2)
    return {"status": "ideal_plan" if calls <= cap else "query_cap", "M": m_size,
            "a_calls": calls, "phase_qubits": m_size.bit_length()-1,
            "repetitions": REPETITIONS, "statistical_upper_rational": str(bound),
            "fixed_schedule_margin_rational": str(remaining-bound)}


def projected_cost(resources, m_size, repetitions=REPETITIONS):
    if type(m_size) is not int or m_size < 2 or m_size & (m_size-1):
        raise ValueError("M must be a power of two >= 2")
    if type(repetitions) is not int or repetitions <= 0:
        raise ValueError("positive repetition count required")
    names = ("a_cx_projection", "controlled_a_cx_projection", "zero_reflection_cx_projection")
    if any(type(resources[n]) is not int or resources[n] < 0 for n in names):
        raise ValueError("nonnegative integer composition costs required")
    a_cost, controlled, zero = (resources[n] for n in names)
    bits = m_size.bit_length()-1
    # Initial A, both directions per Grover iterate, reflections, full IQFT.
    return repetitions*(a_cost+(m_size-1)*(2*controlled+zero+1)
                        +bits*(bits-1)+3*(bits//2))


def evaluate(row, tolerance, extra):
    result = schedule(row["budget"]["beta"], row["budget"]["deterministic_upper"],
                      tolerance, extra)
    return {"case": row["case"]["id"], "mode": row["mode"],
            "degree": row["budget"]["degree"], "tolerance": tolerance, "extra": extra,
            "schedule": result, "projected_cx": projected_cost(row["resources"], result["M"])
            if result["status"] == "ideal_plan" else None}


def compare(rows):
    best = {}
    for mode in ("original", "reflection"):
        eligible = [r for r in rows if r["mode"] == mode and r["projected_cx"] is not None]
        best[mode] = min(eligible, key=lambda r: (r["projected_cx"], r["degree"])) if eligible else None
    left, right = best["original"], best["reflection"]
    if left is None and right is None:
        outcome = "neither_feasible"
    elif left is None or right is None:
        outcome = "reflection_only" if left is None else "original_only"
    elif left["projected_cx"] == right["projected_cx"]:
        outcome = "tie"
    else:
        outcome = "reflection_lower_projection" if right["projected_cx"] < left["projected_cx"] else "original_lower_projection"
    return {"best": best, "outcome": outcome,
            "original_over_reflection_rational": str(F(left["projected_cx"], right["projected_cx"]))
            if left is not None and right is not None else None}


def analyze(production, authoritative, tiny):
    rows = production["rows"]
    expected = {(c, m, n) for c in ("D1", "D2", "E1", "E2")
                for m in ("original", "reflection") for n in (16, 32, 64, 128)}
    keys = [(r["case"]["id"], r["mode"], r["budget"]["degree"]) for r in rows]
    if len(keys) != 32 or set(keys) != expected:
        raise ValueError("frozen grid missing, duplicated or changed")
    for row in rows:
        if row["budget"]["physical_execution_error"] is not None or row["budget"]["confirmation_admitted"]:
            raise ValueError("unexpected physical promotion")
        independent = evaluate(row, "1", "0")
        old = row["budget"]["schedule"]
        if any(independent["schedule"][k] != old[k] for k in ("status", "M", "a_calls")):
            raise ValueError("schedule discrepancy")
        if old["status"] == "ideal_plan":
            corrected = row["resources"]["total_cx_projection"]+old["repetitions"]*3*(old["phase_qubits"]//2)
            if independent["projected_cx"] != corrected:
                raise ValueError("cost discrepancy")
    cells = []
    counts = {}
    for tolerance in TOLERANCES:
        for extra in ALLOWANCES:
            for case in ("D1", "D2", "E1", "E2"):
                alternatives = [evaluate(r, tolerance, extra) for r in rows if r["case"]["id"] == case]
                comparison = compare(alternatives)
                cells.append({"case": case, "tolerance": tolerance, "extra": extra,
                              **comparison, "all_plans": alternatives})
                counts[comparison["outcome"]] = counts.get(comparison["outcome"], 0)+1
                if tolerance == "1" and extra == "0":
                    old = next(c for c in authoritative["comparisons"] if c["case"]["id"] == case)
                    for mode in ("original", "reflection"):
                        first, second = comparison["best"][mode], old["alternatives"][mode]
                        if (first is None) != (second is None):
                            raise ValueError("feasibility discrepancy")
                        if first and (first["degree"], first["projected_cx"]) != (second["degree"], second["projected_cx"]):
                            raise ValueError("selected-plan discrepancy")
    tiny_costs = {r["mode"]: r["ae_cost"]["cx"] for r in tiny}
    return {"baseline_rows_checked": 32, "plan_evaluations": 576, "cells": cells,
            "outcome_counts": counts, "tiny_fixed_schedule_cx": tiny_costs,
            "candidate_status": "standby", "confirmation_admitted": False,
            "quantum_over_classical_advantage_established": False,
            "scope": "retrospective logical composition sensitivity; extra allowance is hypothetical price bias"}


def main():
    from .storage import ROOT, start_run, finish_run, write_json, sha256
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    base = ROOT/"results/journal_sprint"
    inputs = {"production": base/"minimal_pivot_week2_production_v1/results.json",
              "authoritative": base/"minimal_pivot_week2_analysis_v2.json",
              "tiny": base/"minimal_pivot_week2_tiny_v2/results.json"}
    hashes = {key: sha256(path) for key, path in inputs.items()}
    protocol = ROOT/"docs/journal_sprint/CLAIM_ASSESSMENT_PROTOCOL_20260917.md"
    start_run(args.output, {"tolerances": TOLERANCES, "extra_allowances": ALLOWANCES,
                           "repetitions": REPETITIONS, "cap": CALL_CAP,
                           "protocol_sha256": sha256(protocol), "posthoc": True})
    data = {key: json.loads(path.read_text(encoding="utf-8")) for key, path in inputs.items()}
    result = analyze(**data)
    if hashes != {key: sha256(path) for key, path in inputs.items()}:
        raise ValueError("input mutated during analysis")
    write_json(args.output/"inputs.json", {"sha256": hashes, "paths": {
        key: path.relative_to(ROOT).as_posix() for key, path in inputs.items()}})
    write_json(args.output/"results.json", result)
    finish_run(args.output)
    print(json.dumps({"baseline_rows_checked": 32, "plan_evaluations": 576,
                      "case_comparisons": len(result["cells"]), "outcomes": result["outcome_counts"]}))


if __name__ == "__main__":
    main()
