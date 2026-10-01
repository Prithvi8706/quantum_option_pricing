"""Items C7 (missing arms) and C8 (24 generated out-of-sample cases), ANALYSIS_SPEC_STAGE_C.md.

  python -m research.frontier_classical_20261001.c7_c8_cases rates  --item c7|c8 --out <dir>
  python -m research.frontier_classical_20261001.c7_c8_cases timing --item c7|c8 --out <dir>
  python -m research.frontier_classical_20261001.c7_c8_cases oracle --item c7|c8 --out <dir>
`rates` (non-timing slot): sigma_Q and 32-scramble rate runs (C7: preint and rqmc to 2^19,
2^18 for 16x52 if truncated; C8: preint to 2^17). `timing` (exclusive slot): warm all-16
repeats (C7: 3 to 2^19; C8: 1 to 2^17). `oracle`: favourable leaf-table score (a) and the
compiled clean dependency-only and scheduled depths (b), budget 2 CPU-hours per case.
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import json
import multiprocessing as mp
import subprocess
import time
from pathlib import Path

import numpy as np

from research.frontier_classical_20261001 import c2_timing
from research.frontier_classical_20261001.fit import summarize
from research.frontier_classical_20261001.kernels import ESTIMANDS
from research.frontier_classical_20261001.sigma_q import sigma_q
from research.frontier_classical_20261001.timing import wait_workers, warm_up

ROOTS = {"c7": 2026100171, "c8": 2026100181}
SCRAMBLES, WORKERS = 32, 16
C7_CASES = (sc.Case(2, 16, 52), sc.Case(3, 4, 12, barrier=120.0), sc.Case(4, 4, 12, barrier=160.0),
            sc.Case(5, 8, 52, barrier=120.0), sc.Case(6, 8, 52, barrier=160.0),
            sc.Case(7, 16, 52, barrier=120.0), sc.Case(8, 16, 52, barrier=160.0))
STRATA = ((4, 12), (4, 52), (8, 12), (8, 52), (16, 12), (16, 52))


def c8_cases():
    """DECISION.md section 6 generator, pinned by ANALYSIS_SPEC_STAGE_C.md item C8."""
    cases = []
    for s, (na, nt) in enumerate(STRATA):
        for j in range(4):
            rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence([2026092301, s, j])))
            h_ratio = rng.uniform(1.15, 1.6)
            sigma = rng.uniform(0.15, 0.45)
            rho = rng.uniform(0.1, 0.7)
            cases.append(sc.Case(100 + 4 * s + j, na, nt, spot=100.0,
                                 strike=100.0 * (0.9, 1.0, 1.1)[(s + j) % 3],
                                 barrier=100.0 * h_ratio, sigma=sigma, rho=rho, rate=0.03,
                                 maturity=float(1 + j % 2)))
    return cases


def cases_for(item):
    return C7_CASES if item == "c7" else tuple(c8_cases())


def m_top_rule(item, out_dir):
    """C7: 2^19, or 2^18 for all 16x52 cases if 8 x (first 16x52 H=140 scramble's time to
    2^16) > 10 min, decided once before any fit. C8: 2^17."""
    if item == "c8":
        return {}, 17
    t0 = time.perf_counter()
    sc.run_scramble((C7_CASES[0], "canonical", (ROOTS["c7"], 2, 0, 0, 0), 16))
    probe = time.perf_counter() - t0
    m16 = 18 if 8 * probe > 600 else 19
    (out_dir / "truncation.json").write_text(json.dumps(dict(probe_seconds_to_2_16=probe,
                                                             m_top_16x52=m16)))
    return {16: m16}, 19


def rates(item, out_dir):
    overrides, m_default = m_top_rule(item, out_dir)
    result = {}
    with mp.Pool(WORKERS) as pool:
        sigmas = dict(zip((c.case_index for c in cases_for(item)),
                          pool.map(sigma_q, cases_for(item), chunksize=1)))
        for case in cases_for(item):
            m_top = overrides.get(case.na, m_default)
            t0 = time.time()
            tasks = [(case, "canonical", (ROOTS[item], case.case_index, 0, 0, s), m_top)
                     for s in range(SCRAMBLES)]
            rows = pool.map(sc.run_scramble, tasks, chunksize=1)
            arr = np.stack([r["prefix"] for r in rows])
            np.save(out_dir / f"case{case.case_index}.npy", arr)
            ms = rows[0]["ms"]
            keep = ("knockout_pre", "knockout") if item == "c7" else ("knockout_pre",)
            result[str(case.case_index)] = dict(
                case=case.__dict__, m_top=m_top, sigma=sigmas[case.case_index],
                summary={e: summarize(ms, arr[:, ESTIMANDS.index(e), :], case.case_index)
                         for e in keep},
                seconds=time.time() - t0)
            (out_dir / f"{item}_rates.json").write_text(json.dumps(result, indent=1))
            print(item, case.case_index, round(result[str(case.case_index)]["summary"]
                                               ["knockout_pre"]["fits"]["primary"]["r"], 3),
                  flush=True)


def timing(item, out_dir, rates_path):
    rates_summary = json.loads(Path(rates_path).read_text())
    repeats = range(3) if item == "c7" else range(1)
    log, result = [], {}
    for case in cases_for(item):
        entry = rates_summary[str(case.case_index)]
        n_top = 2 ** (19 if item == "c7" else 17)
        block = dict(machine=c2_timing.wait_idle(log))
        with mp.Pool(WORKERS, initializer=warm_up) as pool:
            wait_workers(pool, WORKERS)
            block["warm"] = [c2_timing.all16(pool, f"{item}-{case.case_index}-w{r}", case, "preint",
                                             r, n_top) for r in repeats]
        block["fits"] = dict(all16=c2_timing.fit_ab(c2_timing.medians(block["warm"], "all16")),
                             per_scramble=c2_timing.fit_ab(c2_timing.medians(
                                 block["warm"], "per_scramble_median")))
        a, b = block["fits"]["all16"]
        n = entry["summary"]["knockout_pre"]["n_eps"]["0.001"]["point"]
        block["t_c_0.001"] = dict(n_eps=n, all16_model=a + b * n,
                                  per_scramble_model=sum(x * y for x, y in zip(
                                      block["fits"]["per_scramble"], (1, n))))
        result[str(case.case_index)] = block
        (out_dir / f"{item}_timing.json").write_text(json.dumps(
            dict(machine_log=log, blocks=result), indent=1, default=str))


def oracle(item, out_dir):
    from research.frontier_classical_20261001.oracle import compiled_depths, favourable_score
    result = {}
    for case in cases_for(item):
        fav = favourable_score(case)
        row = dict(favourable_clean_call_t_depth=fav["clean_call_t_depth"],
                   favourable_forward=fav["forward_critical_t_depth"])
        try:
            row["compiled"] = compiled_depths(case, out_dir / f"case{case.case_index}")
        except Exception as exc:                      # reported as not done, never retried
            row["compiled"] = dict(error=repr(exc))
        result[str(case.case_index)] = row
        (out_dir / f"{item}_oracle.json").write_text(json.dumps(result, indent=1))
        print(item, case.case_index, row["favourable_clean_call_t_depth"],
              row["compiled"].get("clean_dependency_t_depth"), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=("rates", "timing", "oracle"))
    ap.add_argument("--item", choices=("c7", "c8"), required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rates")
    args = ap.parse_args()
    out_dir = Path(args.out) / args.item / args.phase
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    (out_dir / "commit.txt").write_text(subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=sc.ROOT, capture_output=True, text=True).stdout)
    if args.phase == "rates":
        rates(args.item, out_dir)
    elif args.phase == "timing":
        timing(args.item, out_dir, args.rates)
    else:
        oracle(args.item, out_dir)


if __name__ == "__main__":
    main()
