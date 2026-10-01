"""Q0 attribution diagnostic (ANALYSIS_SPEC_STAGE_B.md): separately labelled, does not replace Q0.

Step 1 (numpy 1.26.4 interpreter): save numpy.linalg.eigh(cov) for the P3 covariances.
Step 2 (T0 interpreter, numpy 2.0.2): rerun the unchanged P3 with eigh replaced by the
saved numpy 1.26.4 decomposition, writing to this directory. If the output equals the
archive exactly, the Q0 mismatch is attributed entirely to the eigenbasis.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "research" / "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402

SHAPES = ((4, 12), (8, 52))


def cov(na, nt):
    t = p3.T * np.arange(1, nt + 1) / nt
    a = p3.SIGMA**2 * (p3.CORR * np.ones((na, na)) + (1 - p3.CORR) * np.eye(na))
    return np.kron(a, np.minimum.outer(t, t))


if sys.argv[1:] == ["save"]:
    for na, nt in SHAPES:
        vals, vecs = np.linalg.eigh(cov(na, nt))
        np.savez(HERE / f"eigh_{na}x{nt}_numpy{np.__version__}.npz", vals=vals, vecs=vecs)
    sys.exit()

saved = {na * nt: np.load(HERE / f"eigh_{na}x{nt}_numpy1.26.4.npz") for na, nt in SHAPES}
_eigh = np.linalg.eigh


def eigh_1264(m):
    s = saved.get(m.shape[0])
    if s is not None and np.array_equal(m, cov(*next(x for x in SHAPES if x[0] * x[1] == m.shape[0]))):
        return s["vals"].copy(), s["vecs"].copy()
    return _eigh(m)


np.linalg.eigh = eigh_1264          # module top level, so spawned workers are patched too
p3.OUT = str(HERE / "barrier_fast_classical_eigh1264.json")

if __name__ == "__main__":
    p3.main()
    a = json.loads((ROOT / "results/advantage_frontier_20260923/barrier_fast_classical.json").read_text())
    b = json.loads(Path(p3.OUT).read_text())
    keys = ["price", "std_error", "rate_r", "fit_constant", "rqmc_std_one_scramble", "n"]
    same = {f"B{ra['assets']}x{ra['dates']}": {k: ra[k] == rb[k] for k in keys}
            for ra, rb in zip(a["results"], b["results"])}
    result = dict(purpose=__doc__, numpy=np.__version__, exact_non_timing_equal=same,
                  all_equal=all(all(v.values()) for v in same.values()))
    (HERE / "attribution_result.json").write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result["exact_non_timing_equal"]), "ALL EQUAL:", result["all_equal"])
