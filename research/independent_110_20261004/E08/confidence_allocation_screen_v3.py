"""Exact fixed-geometry confidence allocation screen. No sampling or source changes."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import time
import traceback
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/independent_110_20261004/E08/run003"
DOC = ROOT / "docs/independent_110_20261004/E08"
SAVED = ROOT / "results/controlled_priority_completion/estimator_hadamard.json"
AUTHOR = Path(__file__).resolve()
ALPHA = Q(3, 1000)
MAX_R = 128
CORPUS = [SAVED,
    ROOT / "research/controlled_priority_completion/estimator_hadamard.py",
    ROOT / "docs/controlled_priority_completion/ESTIMATOR_REDESIGN.md",
    ROOT / "docs/limitation_audit_20261001/implementation_plan/roadmap.json"]


START_CPU = None
START_WALL = None


def guard(admission=False):
    if START_CPU is not None:
        if time.process_time() - START_CPU > (90 if admission else 120) or time.monotonic() - START_WALL > 300:
            raise ValueError("Fixed E08 CPU/wall guard")


def sha(path):
    guard()
    value = hashlib.sha256(path.read_bytes()).hexdigest()
    guard()
    return value


def pair(x):
    return [x.numerator, x.denominator]


def dump(path, value):
    guard()
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    guard()


def prepare():
    if OUT.exists():
        raise ValueError("Fresh E08 output required.")
    rows = json.loads(SAVED.read_text())
    OUT.mkdir(parents=True)
    dump(OUT / "protocol.json", {
        "schema": "e08-fixed-geometry-allocation-preregistration-v1",
        "corpus": {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p) for p in CORPUS},
        "author_sha256": sha(AUTHOR), "row_count": len(rows),
        "stage_counts": [len(r["allocation"]["stages"]) for r in rows],
        "alpha_exact": pair(ALPHA), "max_repetitions": MAX_R,
        "allocations": ["uniform", "ceil-dyadic40 sqrt(T)", "T", "T^2", "best prior plus three deterministic greedy slack rounds"],
        "local_rule": "Each round visits stages descending T then index; lower repetitions by one only if exact sum of max(small,large) tails stays <=3/1000. At most three rounds.",
        "frozen_inputs": "Source family, continuous/support mode, moment, normalizer, interval geometry, chain T and certified stage probability bounds are unchanged. This screen assumes archived probability promises, and does not recertify their population financial bridge.",
        "acceptance": ["Recompute all saved binomial tails/calls exactly, including saved threshold.", "Five candidates per row; feasible schedules have exact summed tail <=3/1000 and unchanged geometry/probability promises; fixed-cap resource rejections are retained.", "Any promoted candidate must strictly beat saved calls; nonimproving selections are retained as negative diagnostics only. No comparison to superseded billion-call schedule.", "No source/law/geometry/synthesis/physical or financial-delivery claim; no shared ledger change."],
        "budgets": {"cpu_seconds": 120, "admission_cpu_seconds": 90, "wall_seconds": 300, "output_bytes": 16 * 1024 * 1024},
        "stopping_rule": "Four declared allocations and one local candidate with at most three rounds, all four saved rows. No adaptive observed data or further sweep.",
        "finance_draws": 0, "new_global_fixture_credit": 0,
    })
    print("E08 fixed four-row/five-allocation protocol frozen.")


@lru_cache(maxsize=40000)
def exact_best(r, a, b):
    """Every threshold is checked; no monotonicity in repetitions is assumed."""
    d = math.lcm(a.denominator, b.denominator)
    pa, pb = a.numerator * (d // a.denominator), b.numerator * (d // b.denominator)
    qa, qb = d - pa, d - pb
    assert 0 < pb < pa < d
    weights_a, weights_b = [qa ** r], [qb ** r]
    for j in range(r):
        guard()
        na = weights_a[-1] * (r - j) * pa
        nb = weights_b[-1] * (r - j) * pb
        da, db = (j + 1) * qa, (j + 1) * qb
        assert na % da == 0 and nb % db == 0
        weights_a.append(na // da)
        weights_b.append(nb // db)
    den = d ** r
    assert sum(weights_a) == den and sum(weights_b) == den
    lower, upper = 0, den
    best = None
    for k in range(r + 2):
        guard()
        candidate = (max(lower, upper), k, lower, upper)
        if best is None or candidate[:2] < best[:2]:
            best = candidate
        if k <= r:
            lower += weights_a[k]
            upper -= weights_b[k]
    return Q(best[0], den), best[1], Q(best[2], den), Q(best[3], den)


def exact_given(r, k, p, lower):
    n, d = p.numerator, p.denominator
    indices = range(0, k) if lower else range(k, r + 1)
    return Q(sum(math.comb(r, j) * n ** j * (d - n) ** (r - j) for j in indices), d ** r)


def parameters(stage):
    return Q(*stage["p_plus_small_lower_exact"]), Q(*stage["p_plus_large_upper_exact"])


def minimum_stage(stage, delta):
    a, b = parameters(stage)
    for r in range(1, MAX_R + 1):
        guard()
        fail, k, fs, fl = exact_best(r, a, b)
        if fail <= delta:
            return {"stage": stage["stage"], "T": stage["T"], "repetitions": r, "threshold": k,
                    "failure_allocation_exact": pair(delta), "max_failure_exact": pair(fail),
                    "small_failure_exact": pair(fs), "large_failure_exact": pair(fl),
                    "controlled_U_calls": stage["T"] * r}
    raise ValueError("Frozen E08 repetition cap exhausted.")


def total(rows):
    return sum(Q(*s["max_failure_exact"]) for s in rows)


def weight(T, exponent):
    if exponent == 0:
        return Q(1)
    if exponent == 1:
        return Q(T)
    if exponent == 2:
        return Q(T * T)
    scale = 1 << 40
    integer = math.isqrt(T * scale * scale)
    if integer * integer != T * scale * scale:
        integer += 1
    assert (integer - 1) ** 2 < T * scale * scale <= integer ** 2
    return Q(integer, scale)


def run():
    global START_CPU, START_WALL
    t_cpu, t_wall = time.process_time(), time.monotonic()
    START_CPU, START_WALL = t_cpu, t_wall
    protocol = json.loads((OUT / "protocol.json").read_text())
    if (OUT / "RUN_STARTED.json").exists():
        raise ValueError("E08 one-attempt rule.")
    assert sha(AUTHOR) == protocol["author_sha256"]
    for path, expected in protocol["corpus"].items():
        assert sha(ROOT / path) == expected
    guard(admission=True)
    dump(OUT / "RUN_STARTED.json", {"finance_draws": 0, "frozen_rows": protocol["row_count"]})
    saved = json.loads(SAVED.read_text())
    results = []
    for index, row in enumerate(saved):
        stages = row["allocation"]["stages"]
        assert len(stages) == protocol["stage_counts"][index]
        assert [s["stage"] for s in stages] == list(range(len(stages)))
        baseline_tails = []
        for stage in stages:
            guard()
            a, b = parameters(stage)
            r, k = stage["repetitions"], stage["small_if_plus_count_at_least"]
            fs, fl = exact_given(r, k, a, True), exact_given(r, k, b, False)
            assert max(fs, fl) <= Q(*stage["failure_allocation_exact"])
            baseline_tails.append(max(fs, fl))
            assert stage["T"] * r == stage["controlled_U_calls"]
        baseline_calls = sum(s["T"] * s["repetitions"] for s in stages)
        assert baseline_calls == row["allocation"]["controlled_U_calls"]
        assert sum(baseline_tails) <= ALPHA
        candidates = []
        for exponent in [0, 0.5, 1, 2]:
            guard()
            weights = [weight(s["T"], exponent) for s in stages]
            denominator = sum(weights)
            allocation = [ALPHA * w / denominator for w in weights]
            assert sum(allocation) == ALPHA
            try:
                schedule = [minimum_stage(s, delta) for s, delta in zip(stages, allocation)]
            except ValueError as exc:
                candidates.append({"name": f"power_{exponent}", "resource_rejected": True,
                                   "reason": str(exc), "max_repetitions": MAX_R,
                                   "controlled_U_calls": None, "stages": None})
                continue
            assert total(schedule) <= ALPHA
            candidates.append({"name": f"power_{exponent}", "resource_rejected": False, "stages": schedule,
                               "controlled_U_calls": sum(s["controlled_U_calls"] for s in schedule),
                               "max_failure_sum_exact": pair(total(schedule))})
        best = min((x for x in candidates if not x.get("resource_rejected", False)), key=lambda x: (x["controlled_U_calls"], x["name"]))
        local = [dict(s) for s in best["stages"]]
        changes = []
        order = sorted(range(len(stages)), key=lambda j: (-stages[j]["T"], j))
        failure_total = total(local)
        for round_index in range(3):
            for j in order:
                guard()
                r = local[j]["repetitions"]
                if r <= 1:
                    continue
                fail, k, fs, fl = exact_best(r - 1, *parameters(stages[j]))
                revised = failure_total - Q(*local[j]["max_failure_exact"]) + fail
                if revised <= ALPHA:
                    local[j].update(repetitions=r - 1, threshold=k, max_failure_exact=pair(fail),
                                    small_failure_exact=pair(fs), large_failure_exact=pair(fl),
                                    controlled_U_calls=stages[j]["T"] * (r - 1))
                    local[j]["failure_allocation_exact"] = pair(fail)
                    changes.append({"round": round_index + 1, "stage": j, "calls_saved": stages[j]["T"]})
                    failure_total = revised
        assert total(local) == failure_total <= ALPHA
        for local_stage in local:
            local_stage["failure_allocation_exact"] = local_stage["max_failure_exact"]
        assert sum(Q(*s["failure_allocation_exact"]) for s in local) <= ALPHA
        candidates.append({"name": "three_round_local", "started_from": best["name"], "changes": changes,
                           "stages": local, "controlled_U_calls": sum(s["controlled_U_calls"] for s in local),
                           "max_failure_sum_exact": pair(failure_total)})
        assert len(candidates) == 5
        selected = min((x for x in candidates if not x.get("resource_rejected", False)), key=lambda x: (x["controlled_U_calls"], x["name"]))
        results.append({"saved_row_index": index, "model": row["model"], "mode": row["mode"],
                        "baseline_controlled_U_calls": baseline_calls,
                        "baseline_exact_max_failure_sum": pair(sum(baseline_tails)),
                        "baseline_nominal_allocation_sum": pair(sum(Q(*s["failure_allocation_exact"]) for s in stages)),
                        "candidate_schedules": candidates, "selected": selected["name"],
                        "selected_controlled_U_calls": selected["controlled_U_calls"],
                        "saving_exact": pair(Q(baseline_calls - selected["controlled_U_calls"], baseline_calls)),
                        "strict_logical_call_improvement": selected["controlled_U_calls"] < baseline_calls,
                        "selection_decision": "eligible_logical_call_improvement" if selected["controlled_U_calls"] < baseline_calls else "rejected_no_strict_improvement",
                        "full_financial_or_physical_transfer": False})
        assert time.process_time() - t_cpu <= protocol["budgets"]["cpu_seconds"]
        assert time.monotonic() - t_wall <= protocol["budgets"]["wall_seconds"]
    dump(OUT / "schedules.json", results)
    for path, expected in protocol["corpus"].items():
        assert sha(ROOT / path) == expected
    summary = {"passed": True, "completed": True, "scope": "E08 finite five-allocation screen of four fixed archived residual estimator rows.",
               "rows": [{k: r[k] for k in ["model", "mode", "baseline_controlled_U_calls", "selected_controlled_U_calls", "selected", "saving_exact", "strict_logical_call_improvement"]} for r in results],
               "candidate_count": 20, "resource_rejected_candidates": sum(bool(c.get("resource_rejected")) for r in results for c in r["candidate_schedules"]), "unchanged_geometry_and_probability_promises": True,
               "exact_failure_budget": pair(ALPHA), "finance_draws": 0, "new_global_fixture_credit": 0,
               "shared_ledger_replaced": False, "source_adoption": False, "financial_delivery_certified": False,
               "quantum_advantage": False,
               "limitations": ["The continuous-moment rows remain conditional on their original moment/source bridge; E12 is untouched.", "These are C4/H8 residual-family schedules; no call counts transfer to original B4/B8 knock-out sources.", "Exact binomial union bounds assume the archived stage probability promises and conditional shot model.", "No physical runtime, synthesis improvement, matched performance or full price delivery is certified."]}
    dump(OUT / "summary.json", summary)
    DOC.mkdir(parents=True, exist_ok=True)
    report = DOC / "RESULTS_run003.txt"
    if report.exists():
        raise ValueError("Fresh E08 report required.")
    lines = [summary["scope"], "", "The fixed source/stage promises were retained. Exact rational binomial tails cover every stage by a union bound <=3/1000."]
    for r in results:
        saving = Q(*r["saving_exact"])
        lines.append(f"{r['model']} {r['mode']}: {r['baseline_controlled_U_calls']} -> {r['selected_controlled_U_calls']} controlled U calls; {float(saving)*100:.6f}% saving; selected {r['selected']}.")
    lines += ["", "Saved nominal allocations encode the binary64 representation of0.003. Their tiny excess over3/1000 is not treated as proof of failure: the actual exact saved tail sums are independently checked below3/1000. New allocations use exact3/1000.",
              "", "Every candidate repetition search checked all smaller integer r through the frozen cap and every threshold; no monotonicity in r or favorable observed data was assumed.",
              "", "A logical call improvement is a scoped estimator component. Existing geometry, probabilities and source assumptions were read, not re-proved. Current shared ledgers and source families were not changed."] + summary["limitations"]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    files = list(OUT.iterdir()) + [report]
    assert sum(p.stat().st_size for p in files if p.is_file()) <= protocol["budgets"]["output_bytes"]
    dump(OUT / "manifest.json", {"files": {str(p.relative_to(ROOT)).replace('\\', '/'): {"sha256": sha(p), "bytes": p.stat().st_size} for p in sorted(files) if p.is_file()}, "author_sha256": protocol["author_sha256"], "input_pins": protocol["corpus"]})
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "run"])
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare()
    else:
        try:
            run()
        except BaseException as exc:
            if OUT.exists():
                failed = {"passed": False, "completed": False, "decision": "FAILED_UNSEALED",
                          "error_type": type(exc).__name__, "message": str(exc)[:2048],
                          "budget_censored": "Fixed E08 CPU/wall guard" in str(exc),
                          "failure_marker_overrides_any_partial_pass": True,
                          "new_global_fixture_credit": 0, "source_adoption": False}
                # Bounded retention deliberately bypasses a spent scientific guard.
                payload = (json.dumps(failed, indent=2, sort_keys=True) + "\n").encode("utf-8")
                if len(payload) > 16384:
                    raise RuntimeError("Bounded E08 failure-retention cap") from exc
                (OUT / "FAILED_UNSEALED.json").write_bytes(payload)
            traceback.print_exc()
            raise SystemExit(1)
