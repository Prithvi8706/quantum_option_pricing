"""Item C4: coverage of the 16-scramble preint interval (ANALYSIS_SPEC_STAGE_C.md).

Phase `raw` archives raw estimates: per development case, R = 1000 replications of 16 fresh
scrambles to 2^13 (nested prefixes give 2^10..2^13), keys [2026100141, case_index, 4, rep, s];
for 4x12 also replications 1000..1999 to 2^17. Phase `score` computes coverage from those
estimates and the item C3 references (Ref A, Ref B) by the spec's rules.
  python -m research.frontier_classical_20261001.c4_coverage raw --out <dir>
  python -m research.frontier_classical_20261001.c4_coverage score --res <results dir> --out <dir>
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import json
import math
import multiprocessing as mp
import time
from pathlib import Path

import numpy as np
from scipy.special import ndtri
from scipy.stats import beta, qmc
from scipy.stats import t as student_t

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.kernels import knockout_preint
from research.frontier_classical_20261001.provenance import meta as provenance_meta
from research.frontier_classical_20261001.provenance import require_clean

ROOT_C4 = 2026100141
R, SCRAMBLES, WORKERS = 1000, 16, 16
LEVELS = (10, 11, 12, 13)
DEV = (sc.Case(0, 4, 12), sc.Case(1, 8, 52))
_L = {}


def preint_scramble(task):
    """Prefix means of the preint knock-out estimand at 2^m for m in `levels`."""
    case, rep, s, levels = task
    if case not in _L:
        _L[case] = canonical_factor(case.na, case.nt, case.sigma, case.rho, case.maturity)[0]
    L, mu = _L[case], sc.drift(case)
    sampler = qmc.Sobol(case.dim, scramble=True,
                        seed=np.random.default_rng([ROOT_C4, case.case_index, 4, rep, s]))
    disc = math.exp(-case.rate * case.maturity)
    n_top = 2 ** max(levels)
    total, count, out = 0.0, 0, {}
    while count < n_top:
        size = min(sc.CHUNK, n_top - count)
        z = ndtri(np.clip(sampler.random(size), 1e-15, 1 - 1e-15))
        y = knockout_preint(z @ L.T + mu, np.ascontiguousarray(z[:, 0]),
                            np.ascontiguousarray(L[:, 0]), case.na, case.nt, disc,
                            case.strike, case.barrier)
        cs = np.cumsum(y)
        for m in levels:
            if count < 2 ** m <= count + size:
                out[m] = (total + cs[2 ** m - count - 1]) / 2 ** m
        total += cs[-1]
        count += size
    return [out[m] for m in levels]


def run_arm(pool, case, reps, levels):
    tasks = [(case, rep, s, levels) for rep in reps for s in range(SCRAMBLES)]
    rows = pool.map(preint_scramble, tasks, chunksize=SCRAMBLES)
    return np.array(rows).reshape(len(reps), SCRAMBLES, len(levels))


def score(estimates, levels, reference, ref_hw99, alpha_cells=18):
    """Raw and widened coverage of nominal 99% and 95% t-intervals, Clopper-Pearson 95%
    intervals, and the Bonferroni-level under-coverage check of the primary cell."""
    def cp(k, n, level=0.95):
        a = 1 - level
        lo = beta.ppf(a / 2, k, n - k + 1) if k > 0 else 0.0
        hi = beta.ppf(1 - a / 2, k + 1, n - k) if k < n else 1.0
        return [float(lo), float(hi)]
    out = {}
    means = estimates.mean(1)
    s = estimates.std(1, ddof=1)
    for j, m in enumerate(levels):
        cell = {}
        for nominal in (0.99, 0.95):
            t = float(student_t.ppf(1 - (1 - nominal) / 2, SCRAMBLES - 1))
            hw = t * s[:, j] / math.sqrt(SCRAMBLES)
            raw = np.abs(means[:, j] - reference) <= hw
            widened = np.abs(means[:, j] - reference) <= hw + ref_hw99
            k = int(raw.sum())
            cell[str(nominal)] = dict(
                raw=k / len(raw), raw_cp95=cp(k, len(raw)),
                widened=float(widened.mean()),
                reference_limited=bool(ref_hw99 > 0.25 * float(np.median(
                    float(student_t.ppf(0.975, SCRAMBLES - 1)) * s[:, j] / math.sqrt(SCRAMBLES)))),
                raw_cp_bonferroni=cp(k, len(raw), 1 - 0.05 / alpha_cells))
        q = np.abs(means[:, j] - reference) / (s[:, j] / math.sqrt(SCRAMBLES))
        cell["c_empirical_99"] = float(np.quantile(q, 0.99))
        out[str(2 ** m)] = cell
    return out


def references(res):
    """Item C3 primary agreement test and the item C4 reference (spec item C3)."""
    a = json.loads((res / "c3_refa" / "ref_a.json").read_text())["cases"]
    out = {}
    for name in ("B4x12", "B8x52"):
        b = json.loads((res / "c3_refb" / name / "ref_b.json").read_text())
        ra, rb = a[name], b
        diff = abs(ra["price"] - rb["price"])
        passed = diff <= ra["hw99"] + rb["hw99"]
        w_a, w_b = ra["se"] ** -2, rb["se"] ** -2
        ref = (w_a * ra["price"] + w_b * rb["price"]) / (w_a + w_b)
        out[name] = dict(ref_a=ra["price"], ref_a_hw99=ra["hw99"], ref_b=rb["price"],
                         ref_b_hw99=rb["hw99"], abs_diff=diff, agreement_passed=passed,
                         resolution=ra["hw99"] + rb["hw99"],
                         reference=ref if passed else None,
                         reference_hw99=2.576 * (w_a + w_b) ** -0.5 if passed else None)
    return out


def score_phase(res, out_dir):
    refs = references(res)
    raw = res / "c4"
    result = dict(references=refs, cases={})
    arms = [("B4x12", "B4x12_levels10to13.npy", LEVELS),
            ("B8x52", "B8x52_levels10to13.npy", LEVELS),
            ("B4x12", "B4x12_level17.npy", (17,))]
    for name, f, levels in arms:
        est = np.load(raw / f)
        r = refs[name]
        if r["agreement_passed"]:
            targets = {"weighted": (r["reference"], r["reference_hw99"])}
        else:
            targets = {"ref_a": (r["ref_a"], r["ref_a_hw99"]),
                       "ref_b": (r["ref_b"], r["ref_b_hw99"])}
        for label, (ref, hw) in targets.items():
            cells = result["cases"].setdefault(name, {}).setdefault(label, {})
            cells.update(score(est, levels, ref, hw))
    for name, by_ref in result["cases"].items():
        # Primary check: raw 99% coverage at n = 2^13; the reference with lower coverage decides.
        label = min(by_ref, key=lambda k: by_ref[k]["8192"]["0.99"]["raw"])
        cell = by_ref[label]["8192"]
        under = cell["0.99"]["raw_cp_bonferroni"][1] < 0.99
        by_ref["primary_check"] = dict(reference=label, raw_99_at_8192=cell["0.99"]["raw"],
                                       under_covering=bool(under),
                                       c=cell["c_empirical_99"] if under else None)
    (out_dir / "c4_coverage.json").write_text(json.dumps(result, indent=1))
    for name, v in result["cases"].items():
        print(name, v["primary_check"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", choices=("raw", "score"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--res")
    args = ap.parse_args()
    if args.phase == "score" and not args.res:
        ap.error("the score phase needs --res <results dir>")
    require_clean()
    out_dir = Path(args.out)
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    (out_dir / "meta.json").write_text(json.dumps(provenance_meta(phase=args.phase, root=ROOT_C4),
                                                  indent=1))
    if args.phase == "score":
        score_phase(Path(args.res), out_dir)
        return
    meta = dict(replications=R, scrambles=SCRAMBLES, levels=LEVELS, seconds={})
    with mp.Pool(WORKERS) as pool:
        for case in DEV:
            name = f"B{case.na}x{case.nt}"
            t0 = time.time()
            np.save(out_dir / f"{name}_levels10to13.npy", run_arm(pool, case, range(R), LEVELS))
            meta["seconds"][name] = time.time() - t0
            (out_dir / "c4_raw.json").write_text(json.dumps(meta, indent=1))
        t0 = time.time()
        np.save(out_dir / "B4x12_level17.npy", run_arm(pool, DEV[0], range(R, 2 * R), (17,)))
        meta["seconds"]["B4x12_2^17"] = time.time() - t0
    (out_dir / "c4_raw.json").write_text(json.dumps(meta, indent=1))
    print("wrote", out_dir)


if __name__ == "__main__":
    main()
