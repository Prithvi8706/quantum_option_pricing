"""Item C1: port check, then RQMC rates with whole-scramble bootstrap (ANALYSIS_SPEC_STAGE_C.md).

Run from a clean detached worktree of a committed revision (spec section 0):
  python -m research.frontier_classical_20261001.c1_rates --out <absolute results dir>
"""

import research.frontier_classical_20261001.scrambles as sc  # noqa: I001  (pins threads first)

import argparse
import hashlib
import json
import multiprocessing as mp
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from research.frontier_classical_20261001.fit import summarize
from research.frontier_classical_20261001.kernels import ESTIMANDS

sys.path.insert(0, str(sc.ROOT / "research" / "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402

WORKERS = 16
SCRAMBLES = 32
ROOT_C1 = 2026100111
DEV = (sc.Case(0, 4, 12), sc.Case(1, 8, 52))
BASES = ("canonical", "archived", "eigh", ("rotation", 1), ("rotation", 2), ("rotation", 3),
         ("rotation", 4))
T0_EIGH_8X52 = "f980fbabce8234cbf92aa888b02f15004ea53a55e6f456de41980be56b2ebbbf"
SPEC = "manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def basis_name(basis):
    return basis if isinstance(basis, str) else f"rotation{basis[1]}"


def port_check(pool):
    """P3b preint knock-out with P3's seeds and factor vs P3 run in the same environment,
    and vs the Q0-replayed prices. Reported, never re-run under other settings."""
    q0 = json.loads((sc.ROOT / "results/frontier_replay_20261001/q0_provenance_replay.json")
                    .read_text())
    archive = sc.ROOT / "results/advantage_frontier_20260923/barrier_fast_classical.json"
    replayed = {"B4x12": json.loads(archive.read_text())["results"][0]["price"]}
    for m in q0["files"]["barrier_fast_classical.json"]["exact_mismatches"]:
        if m["path"] == "/results[1]/price":
            replayed["B8x52"] = m["replayed"]
    out = {}
    for case in DEV:
        name = f"B{case.na}x{case.nt}"
        L = sc.factor(case, "eigh")
        new = pool.map(sc.run_scramble, [(case, "eigh", (p3.ROOT_SEED, case.dim, s), 17)
                                         for s in range(SCRAMBLES)])
        old = pool.map(p3.scramble_run, [(case.na, case.nt, s) for s in range(SCRAMBLES)])
        rel = max(abs(n["prefix"][5, n["ms"].index(m)] - o["prefix"][m]) / abs(o["prefix"][m])
                  for n, o in zip(new, old) for m in range(8, 18))
        price = float(np.array([n["prefix"][5, -1] for n in new]).mean())
        out[name] = dict(factor_sha256=hashlib.sha256(L.tobytes()).hexdigest(),
                         max_rel_diff_per_scramble_prefix=float(rel), price=price,
                         q0_replayed_price=replayed[name],
                         price_rel_diff=abs(price - replayed[name]) / replayed[name])
    hash_ok = out["B8x52"]["factor_sha256"] == T0_EIGH_8X52
    out["passed"] = hash_ok and all(out[c]["max_rel_diff_per_scramble_prefix"] <= 1e-12
                                    and out[c]["price_rel_diff"] <= 1e-12
                                    for c in ("B4x12", "B8x52"))
    out["failure_kind"] = None if out["passed"] else ("setup" if not hash_ok else "port")
    return out


def rates(pool, out_dir):
    results = {}
    for case in DEV:
        name = f"B{case.na}x{case.nt}"
        arrays, factor_hashes, seconds = {}, {}, {}
        for basis in BASES:
            key, t0 = basis_name(basis), time.perf_counter()
            tasks = [(case, basis, (ROOT_C1, case.case_index, 0, 0, s), 19)
                     for s in range(SCRAMBLES)]           # shared scrambles: paired design
            rows = pool.map(sc.run_scramble, tasks)
            arrays[key] = np.stack([r["prefix"] for r in rows])  # (32, 6, M)
            factor_hashes[key] = hashlib.sha256(sc.factor(case, basis).tobytes()).hexdigest()
            seconds[key] = time.perf_counter() - t0
            np.save(out_dir / f"{name}_{key}.npy", arrays[key])
            print(f"{name} {key} {seconds[key]:.0f} s", flush=True)
        ms = rows[0]["ms"]
        summary = {}
        for key, arr in arrays.items():
            canon = arrays["canonical"]
            summary[key] = {est: summarize(ms, arr[:, j, :], case.case_index,
                                           None if key == "canonical" else canon[:, j, :])
                            for j, est in enumerate(ESTIMANDS)}
        results[name] = dict(ms=ms, factor_sha256=factor_hashes, seconds=seconds, summary=summary)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out_dir = Path(ap.parse_args().out)
    if out_dir.exists():
        raise SystemExit(f"refusing to overwrite {out_dir}")
    out_dir.mkdir(parents=True)
    meta = dict(
        commit=subprocess.run(["git", "rev-parse", "HEAD"], cwd=sc.ROOT, capture_output=True,
                              text=True).stdout.strip(),
        dirty=bool(subprocess.run(["git", "status", "--porcelain"], cwd=sc.ROOT,
                                  capture_output=True, text=True).stdout.strip()),
        spec_sha256=sha(sc.ROOT / SPEC),
        lock_sha256=sha(sc.ROOT / "research/frontier_replay_20261001/t0_requirements.lock"),
        code_sha256={p.name: sha(p) for p in sorted(Path(__file__).parent.glob("*.py"))},
        python=sys.version, numpy=np.__version__, workers=WORKERS, scrambles=SCRAMBLES,
        root=ROOT_C1, bases=[basis_name(b) for b in BASES])
    with mp.Pool(WORKERS) as pool:
        check = port_check(pool)
        (out_dir / "port_check.json").write_text(json.dumps(dict(meta=meta, **check), indent=1))
        print("port check passed:", check["passed"], flush=True)
        if not check["passed"]:
            raise SystemExit("port check failed; item C1 is blocked and reported (spec C1)")
        result = rates(pool, out_dir)
    (out_dir / "c1_summary.json").write_text(json.dumps(dict(meta=meta, port_check=check,
                                                             cases=result), indent=1))
    print("wrote", out_dir)


if __name__ == "__main__":
    main()
