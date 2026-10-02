"""Q0 attribution summary: collects the diagnostic outcomes into attribution_summary.json."""
import os

for _k in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ[_k] = "1"            # as P3 workers do, before numpy is imported

import hashlib  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DUMPS = ROOT / ".context" / "frontier_q0_attribution_dumps"   # 41 MB each; kept untracked
sys.path.insert(0, str(ROOT / "research" / "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402


def h(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


def rate(path):
    r = json.loads(Path(path).read_text())["results"][1]
    return dict(rate_r=r["rate_r"], price=r["price"], std_error=r["std_error"])


vals8 = np.load(HERE / "eigh_8x52_numpy1.26.4.npz")["vals"]
vals4 = np.load(HERE / "eigh_4x12_numpy1.26.4.npz")["vals"]
_, c8 = np.unique(vals8, return_counts=True)
_, c4 = np.unique(vals4, return_counts=True)
order_1264 = np.load(HERE / "order_8x52_numpy1.26.4.npy")
summary = dict(
    exact_tie_groups_in_computed_eigenvalues={"B4x12": int((c4 > 1).sum()), "B8x52": int((c8 > 1).sum())},
    argsort_positions_differing_numpy_1264_vs_202_on_identical_values=int(
        (order_1264 != np.argsort(vals8)[::-1]).sum()),
    factor_L_sha256_8x52={
        "numpy1.26.4_MKL_single_thread_(P3 workers, archive)": h(np.load(HERE / "L_8x52_numpy1.26.4_single_thread.npy")),
        "numpy1.26.4_MKL_multithread_(diagnostic 2a, by mistake)": h(np.load(DUMPS / "dump_conda_1264.npz")["L"]),
        "numpy2.0.2_OpenBLAS_single_thread_(T0 P3 workers, Q0 replay)": h(p3.setup(8, 52)[0]),
        "numpy2.0.2_OpenBLAS_multithread_(boundary dump)": h(np.load(DUMPS / "dump_t0_202.npz")["L"]),
        "numpy2.0.2_argsort_with_numpy1.26.4_multithread_eigh_(diagnostic 1)": h(np.load(DUMPS / "dump_t0_202_eigh1264.npz")["L"]),
    },
    p3_8x52_by_factor={
        "archive (numpy 1.26.4 MKL single-thread L)": rate(ROOT / "results/advantage_frontier_20260923/barrier_fast_classical.json"),
        "Q0 replay (T0 OpenBLAS L)": rate(ROOT / "results/frontier_replay_20261001/q0_attribution/pooled_repeat_t0_a.json"),
        "diagnostic 1 (MKL multithread eigh, numpy 2 argsort)": rate(HERE / "barrier_fast_classical_eigh1264.json"),
        "diagnostic 2a (MKL multithread L)": rate(HERE / "barrier_fast_classical_L1264.json"),
        "diagnostic 2b (MKL single-thread L)": rate(HERE / "barrier_fast_classical_L1264_single_thread.json"),
    },
    pooled_run_repeatable_in_T0=json.loads((HERE / "pooled_repeat_t0_a.json").read_text())["results"]
    == json.loads((HERE / "pooled_repeat_t0_b.json").read_text())["results"] or "non-timing fields compared below",
    inprocess_scrambles_identical_given_same_L=json.loads((HERE / "inproc_conda.json").read_text())
    == json.loads((HERE / "inproc_t0_L1264.json").read_text()),
    diagnostic_2b_reproduces_archive_exactly=json.loads(
        (HERE / "attribution_result_L_single_thread.json").read_text())["all_equal"],
)
a = json.loads((HERE / "pooled_repeat_t0_a.json").read_text())["results"]
b = json.loads((HERE / "pooled_repeat_t0_b.json").read_text())["results"]
keys = ["price", "std_error", "rate_r", "fit_constant", "rqmc_std_one_scramble"]
summary["pooled_run_repeatable_in_T0"] = all(x[k] == y[k] for x, y in zip(a, b) for k in keys)
(HERE / "attribution_summary.json").write_text(json.dumps(summary, indent=1) + "\n")
print(json.dumps(summary, indent=1))
