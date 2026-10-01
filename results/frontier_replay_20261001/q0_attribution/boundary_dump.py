"""Q0 attribution diagnostic: dump P3 intermediates for 8x52 scramble 0, first chunk."""
import sys
from pathlib import Path
import numpy as np
import scipy
from scipy.special import ndtri
from scipy.stats import qmc
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "research" / "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402
tag = sys.argv[1]
na, nt, s = 8, 52, 0
dim = na * nt
if len(sys.argv) > 2:                      # force the numpy 1.26.4 eigendecomposition
    e = np.load(HERE / "eigh_8x52_numpy1.26.4.npz")
    np.linalg.eigh = lambda m: (e["vals"].copy(), e["vecs"].copy())
L, mu = p3.setup(na, nt)
v = np.ascontiguousarray(L[:, 0])
sampler = qmc.Sobol(dim, scramble=True, seed=np.random.default_rng([p3.ROOT_SEED, dim, s]))
u = sampler.random(p3.CHUNK)
z = ndtri(np.clip(u, 1e-15, 1 - 1e-15))
x = z @ L.T + mu
y = p3.estimand(x, np.ascontiguousarray(z[:, 0]), v, na, nt, np.exp(-p3.RATE * p3.T))
np.savez(HERE / f"dump_{tag}.npz", L=L, u=u, z=z, x=x, y=y)
print(tag, "numpy", np.__version__, "scipy", scipy.__version__, "blas",
      np.show_config.__module__, "y mean %.12f" % y.mean())
