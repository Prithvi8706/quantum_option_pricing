"""Q0 attribution diagnostic 2 (separately labelled; does not replace Q0).

Diagnostic 1 injected numpy 1.26.4's eigh output but not its argsort tie order, and did not
reproduce the archive. This one injects the full 8x52 PCA factor L built by P3's setup under
numpy 1.26.4 (dump_conda_1264.npz) into the unchanged P3 run in the T0 environment. If the
output equals the archive exactly, the Q0 mismatch is attributed entirely to the factor L.
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "research" / "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402

L_1264 = np.load(HERE / "dump_conda_1264.npz")["L"]
_setup = p3.setup


def setup_with_1264_factor(na, nt):
    L, mu = _setup(na, nt)
    return (np.ascontiguousarray(L_1264), mu) if (na, nt) == (8, 52) else (L, mu)


p3.setup = setup_with_1264_factor     # module top level, so spawned workers are patched too
p3.OUT = str(HERE / "barrier_fast_classical_L1264.json")

if __name__ == "__main__":
    p3.main()
    a = json.loads((ROOT / "results/advantage_frontier_20260923/barrier_fast_classical.json").read_text())
    b = json.loads(Path(p3.OUT).read_text())
    keys = ["price", "std_error", "rate_r", "fit_constant", "rqmc_std_one_scramble", "n"]
    same = {f"B{ra['assets']}x{ra['dates']}": {k: ra[k] == rb[k] for k in keys}
            for ra, rb in zip(a["results"], b["results"])}
    result = dict(purpose=__doc__, numpy=np.__version__, exact_non_timing_equal=same,
                  all_equal=all(all(v.values()) for v in same.values()))
    (HERE / "attribution_result_L.json").write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(same), "ALL EQUAL:", result["all_equal"])
