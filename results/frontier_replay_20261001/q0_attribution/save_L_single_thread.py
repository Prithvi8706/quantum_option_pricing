"""Q0 attribution diagnostic: save P3's 8x52 factor L exactly as P3 workers build it
(BLAS/LAPACK threads pinned to 1 before numpy is imported). Run with the numpy 1.26.4 interpreter."""
import os
for _k in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS", "NUMBA_NUM_THREADS"):
    os.environ[_k] = "1"
import hashlib, sys  # noqa: E402
from pathlib import Path  # noqa: E402
import numpy as np  # noqa: E402
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "research" / "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402
L, _ = p3.setup(8, 52)
np.save(HERE / "L_8x52_numpy1.26.4_single_thread.npy", L)
print("saved", hashlib.sha256(L.tobytes()).hexdigest()[:10], np.__version__)
