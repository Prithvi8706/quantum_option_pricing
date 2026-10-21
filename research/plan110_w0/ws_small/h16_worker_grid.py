"""H16 classical worker-scaling grid (plan110 W0, WS-small). AUTHORED, NOT RUN by WS-small.

Times the best classical knock-out method of Stage C item C2 (`preint`) at worker counts
1, 2, 4, 8, 16 for B4x12 and B8x52, with the item C2 measured-confirmation accuracy rule
(manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md, item C2):

  - n(eps) = item C1 primary point estimate (canonical factor, `knockout_pre`);
    n_run = 2^ceil(log2 n(eps)); n is never re-chosen;
  - one replication = the 16-scramble estimator to n_run, timed with C2's all-16
    convention (`c2_timing.all16`: submission until all 16 prefix means exist, per-run
    factor build, Sobol construction, dispatch and reduction included);
  - pooled check: per-scramble sd over all replications, hw16 = t_{.995,15}*sd/4;
    T_C = median wall * max(1, (hw16 / (0.45 eps))^(1/r)).

Only the pool size differs from C2. Scrambles are PAIRED across worker counts (same seed
keys for every W), so the achieved accuracy is identical for every W and only time changes;
the runner checks that the scramble means agree across W. Seed root ROOT_H16 is new
(spec deviation D6: no item reuses another item's scrambles); key
[ROOT_H16, case_index, 3, 100*eps_index + replication, scramble].

Machine-state gate: C2's `wait_idle` (30 s CPU average < 10 % and no other busy python
process) before the run and before every (case, W) pool; `NotIdleError` refuses the run.
Also refuses when not on AC power (spec: primary timings on AC power).

Run from the repository root with the Stage C T0 interpreter (C2's c2_timing.json meta:
python 3.12.4, numpy 2.0.2; that is .context/frontier_t0_env, which carries numpy 2.0.2,
scipy 1.13.1, numba 0.60.0):

  PY=.context/frontier_t0_env/Scripts/python.exe
  $PY -B -m research.plan110_w0.ws_small.h16_worker_grid --dry-run
  $PY -B -m research.plan110_w0.ws_small.h16_worker_grid --run run001

Writes only results/plan110_w0/ws_small/h16_grid/<run>/ (exclusive create; one checkpoint
file per (case, eps, workers) row).
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

import research.frontier_classical_20261001.c2_timing as c2
from research.frontier_classical_20261001.fit import EPS, SHARE, T995_15
from research.frontier_classical_20261001.timing import warm_up, wait_workers

ROOT = sc.ROOT
OUT_PARENT = ROOT / "results/plan110_w0/ws_small/h16_grid"
C1_SUMMARY = ROOT / "results/frontier_classical_20261001/c1/c1_summary.json"
C2_TIMING = ROOT / "results/frontier_classical_20261001/c2/c2_timing.json"
C2_C1_SHA = "5d91aecc5ae26140be4e8c6a86ce304ac97870470f04bedce11a3ad55a2b9123"  # c2 meta
ROOT_H16 = 2026101116
METHOD, C1_KEY = "preint", "knockout_pre"  # C2's best knock-out method
WORKER_GRID = (16, 8, 4, 2, 1)  # 16 first: reproduces the C2 condition early
REPS = {0.03: 20, 0.01: 20, 0.001: 5}  # C2 used 20; 5 at $0.001 keeps the grid < 2 h
PURPOSE = 3  # confirmation
IDLE_CHECK_S = 40  # one machine_state() call: 30 s counter + 5 s process sample + startup
POOL_OVERHEAD_S = 15  # pool start, warm_up initializer, barrier, untimed warm call
MAX_HOURS = 2.0


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def plan_rows(c1, c2_blocks, eps_list):
    """Every (case, eps, W) row with its n_run, r and an UPPER runtime estimate.

    Estimate: C2's measured W=16 median confirmation wall (or C2's T_C where C2 ran no
    confirmation) times ceil(16/W), i.e. per-scramble time assumed not to fall when fewer
    workers share the CPU (it usually does fall on this hybrid CPU, so this over-estimates).
    """
    rows = []
    for case in c2.DEV:
        name = f"B{case.na}x{case.nt}"
        est = c1["cases"][name]["summary"]["canonical"][C1_KEY]
        tc = c2_blocks[f"{name}/{METHOD}"]["t_c"]
        for eps in eps_list:
            n = est["n_eps"][str(eps)]["point"]
            n_run = 2 ** math.ceil(math.log2(n))
            wall16 = tc[str(eps)].get("median_wall", tc[str(eps)]["primary"])
            for w in WORKER_GRID:
                rows.append(dict(case=name, case_index=case.case_index, eps=eps,
                                 eps_index=EPS.index(eps), workers=w, n_eps=n, n_run=n_run,
                                 r=est["fits"]["primary"]["r"], reps=REPS[eps],
                                 c2_wall16=wall16, c2_primary=tc[str(eps)]["primary"],
                                 c2_convention=tc[str(eps)]["convention"],
                                 est_s=wall16 * math.ceil(16 / w) * REPS[eps]))
    return rows


def estimate_total(rows):
    pools = {(r["case"], r["workers"]) for r in rows}
    timed = sum(r["est_s"] for r in rows)
    overhead = (len(pools) + 1) * IDLE_CHECK_S + len(pools) * POOL_OVERHEAD_S
    return timed, overhead


def score(row, runs):
    """C2's measured-confirmation rule (c2_timing.t_c), applied to this row's runs."""
    means = np.concatenate([run["scramble_means"] for run in runs])
    hw16 = T995_15 * float(np.std(means, ddof=1)) / math.sqrt(c2.SCRAMBLES)
    wall = float(np.median([run["wall"] for run in runs]))
    scale = max(1.0, (hw16 / (SHARE * row["eps"])) ** (1 / row["r"]))
    return dict(t_c=wall * scale, median_wall=wall, pooled_hw16=hw16, scale=scale,
                walls=[run["wall"] for run in runs],
                wall_range=[min(run["wall"] for run in runs), max(run["wall"] for run in runs)],
                fraction_hw_ok=float(np.mean([run["hw99"] <= SHARE * row["eps"] for run in runs])),
                mean=float(np.mean(means)))


def write_new(path, obj):
    with open(path, "x", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, default=str)


def append_line(path, obj):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, default=str) + "\n")


def gate(log, max_wait_s, label):
    """C2's idle gate, plus the AC-power requirement. Raises c2.NotIdleError on refusal."""
    state = c2.wait_idle(log, max_wait_s=max_wait_s, label=label)
    if str(state.get("battery_status")).strip() not in ("2", ""):
        raise c2.NotIdleError(f"not on AC power before {label}: {state}")
    return state


def run_pool(case, w, rows, out, log, max_wait_s):
    """One pool of w warm workers; times every eps row of this (case, w)."""
    name = f"B{case.na}x{case.nt}"
    state = gate(log, max_wait_s, f"{name} W={w}")
    append_line(out / "machine_log.jsonl", state)
    results = []
    with mp.Pool(w, initializer=warm_up) as pool:
        wait_workers(pool, w)
        c2.all16(pool, f"h16-{case.case_index}-w{w}-warm", case, METHOD, 0, 2 ** 12,
                 purpose=1, root=ROOT_H16)  # untimed, discarded: loads factor/Sobol paths
        for row in rows:
            runs = [c2.all16(pool, f"h16-{case.case_index}-e{row['eps_index']}-w{w}-r{k}",
                             case, METHOD, 100 * row["eps_index"] + k, row["n_run"],
                             purpose=PURPOSE, root=ROOT_H16)
                    for k in range(row["reps"])]
            res = dict(row, machine_state=state, runs=runs, **score(row, runs))
            write_new(out / "rows" / f"{name}_eps{row['eps']}_w{w}.json", res)
            append_line(out / "rows.jsonl", {k: v for k, v in res.items() if k != "runs"})
            print(f"{name} eps={row['eps']} W={w}: T_C={res['t_c']:.4f}s "
                  f"(median wall {res['median_wall']:.4f}s, hw16 {res['pooled_hw16']:.2e})",
                  flush=True)
            results.append(res)
    return results


def summarize(results):
    by = {}
    for res in results:
        by.setdefault(f"{res['case']}/{res['eps']}", {})[res["workers"]] = res
    out = {}
    for key, rows in by.items():
        t = {w: rows[w]["t_c"] for w in sorted(rows)}
        means = {w: [run["scramble_means"] for run in rows[w]["runs"]] for w in rows}
        ref = means[max(means)]
        out[key] = dict(
            t_c_by_workers=t,
            speedup_vs_1=({w: t[1] / t[w] for w in t} if 1 in t else None),
            t1_over_16t16=(t[1] / (16 * t[16]) if 1 in t and 16 in t else None),
            c2_primary_w16=rows[max(rows)]["c2_primary"],
            paired_scramble_means_identical=all(m == ref for m in means.values()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", help="run name; output results/plan110_w0/ws_small/h16_grid/<run>/")
    ap.add_argument("--eps", type=float, nargs="+", default=[0.01, 0.001],
                    choices=[0.03, 0.01, 0.001])
    ap.add_argument("--max-wait", type=int, default=1800,
                    help="seconds to wait for an idle machine before refusing")
    ap.add_argument("--dry-run", action="store_true",
                    help="validate imports and inputs, print the plan; no timing, no writes")
    args = ap.parse_args()
    eps_list = sorted(set(args.eps), reverse=True)

    c1 = json.loads(C1_SUMMARY.read_text())
    c2_rec = json.loads(C2_TIMING.read_text())
    if sha(C1_SUMMARY) != C2_C1_SHA or c2_rec["meta"]["c1_summary_sha256"] != C2_C1_SHA:
        raise SystemExit("C1 summary does not match the one item C2 used")
    rows = plan_rows(c1, c2_rec["blocks"], eps_list)
    timed, overhead = estimate_total(rows)
    total_h = (timed + overhead) / 3600
    print(f"H16 grid: method={METHOD}, workers={WORKER_GRID}, eps={eps_list}, root={ROOT_H16}")
    for r in rows:
        print(f"  {r['case']} eps={r['eps']} W={r['workers']:>2} n_eps={r['n_eps']:.0f} "
              f"n_run=2^{int(math.log2(r['n_run']))} reps={r['reps']} "
              f"C2 W=16 wall={r['c2_wall16']:.3f}s est<= {r['est_s']:.0f}s")
    print(f"ESTIMATED TOTAL RUNTIME (upper): {total_h:.2f} h = timed {timed / 60:.1f} min "
          f"+ idle checks/pools {overhead / 60:.1f} min (+ waits for idleness, if any)")
    if total_h > MAX_HOURS:
        raise SystemExit(f"estimated runtime {total_h:.2f} h exceeds {MAX_HOURS} h; drop eps 0.03")
    provenance = dict(
        python=sys.version, executable=sys.executable, numpy=np.__version__,
        c2_meta_python=c2_rec["meta"]["python"], c2_meta_numpy=c2_rec["meta"]["numpy"],
        spec_sha256=sha(ROOT / c2.SPEC), c1_summary_sha256=sha(C1_SUMMARY),
        c2_timing_sha256=sha(C2_TIMING),
        code_sha256={p.name: sha(p) for p in
                     [*sorted(Path(c2.__file__).parent.glob("*.py")), Path(__file__)]},
        root=ROOT_H16, method=METHOD, worker_grid=WORKER_GRID, reps=REPS, eps=eps_list,
        scrambles=c2.SCRAMBLES, t995_15=T995_15, share=SHARE, purpose=PURPOSE,
        estimate_hours=total_h)
    if sys.version.split()[0] != c2_rec["meta"]["python"].split()[0] \
            or np.__version__ != c2_rec["meta"]["numpy"]:
        raise SystemExit(f"interpreter {sys.version.split()[0]}/numpy {np.__version__} differs "
                         f"from item C2's {c2_rec['meta']['python'].split()[0]}/"
                         f"{c2_rec['meta']['numpy']}; use .context/frontier_t0_env")
    if args.dry_run:
        # Self-check: score() applied to C2's recorded confirmation runs reproduces C2's T_C.
        for r in rows:
            conf = c2_rec["blocks"][f"{r['case']}/{METHOD}"]["confirmation"].get(str(r["eps"]))
            if conf and r["workers"] == 16:
                got = score(r, conf["runs"])["t_c"]
                if abs(got - r["c2_primary"]) > 1e-12 * r["c2_primary"]:
                    raise SystemExit(f"score() does not reproduce C2 T_C: {got} vs "
                                     f"{r['c2_primary']}")
                print(f"  self-check {r['case']} eps={r['eps']}: score(C2 runs)={got:.4f}s "
                      f"== C2 primary {r['c2_primary']:.4f}s")
        print("dry run OK: imports, C1/C2 inputs and interpreter validated; nothing timed or "
              "written")
        print(json.dumps({k: v for k, v in provenance.items() if k != "code_sha256"}, indent=1,
                         default=str))
        return
    if not args.run:
        raise SystemExit("--run is required unless --dry-run")

    out = OUT_PARENT / args.run
    out.mkdir(parents=True, exist_ok=False)
    (out / "rows").mkdir()
    provenance.update(
        cpu=c2.powershell("(Get-CimInstance Win32_Processor).Name"),
        power_plan=subprocess.run(["powercfg", "/getactivescheme"], capture_output=True,
                                  text=True).stdout.strip(), affinity="none set",
        started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    write_new(out / "meta.json", provenance)
    log, results = [], []
    try:
        state = gate(log, args.max_wait, "start")
        append_line(out / "machine_log.jsonl", state)
        for case in c2.DEV:
            name = f"B{case.na}x{case.nt}"
            for w in WORKER_GRID:
                mine = [r for r in rows if r["case"] == name and r["workers"] == w]
                results += run_pool(case, w, mine, out, log, args.max_wait)
    except c2.NotIdleError as err:
        write_new(out / "refused.json", dict(reason=str(err), machine_log=log,
                                             rows_completed=len(results)))
        print("REFUSED:", err, flush=True)
        sys.exit(3)
    write_new(out / "summary.json", dict(meta=provenance, machine_log=log,
                                         summary=summarize(results)))
    print("wrote", out)


if __name__ == "__main__":
    main()
