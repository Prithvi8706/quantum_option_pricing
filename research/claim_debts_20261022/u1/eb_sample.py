"""U1 sample: iid raw-payoff Monte Carlo for the continuous-GBM B8x52 knock-out price, for a one-sided
empirical-Bernstein upper confidence bound (Maurer & Pontil 2009, Thm 4).

The payoff is simulated from the contract definition (common + idiosyncratic Brownian increments), not
from the Stage C factor or kernels:
    log S_i(t_j) = log 100 + (r - sigma^2/2) t_j + sigma (sqrt(rho) W_0(t_j) + sqrt(1-rho) W_i(t_j)),
    B_j = mean_i S_i(t_j), A = mean_{i,j} S_i(t_j), Y = e^{-rT} (A - 100)^+ 1{max_j B_j < 140}.
Y lies in [0, 40 e^{-rT}] because on survival A <= max_j B_j < 140.

Run (worktree root; Stage C env WITHOUT -I -S, numpy needed):
  ../../../.context/frontier_t0_env/Scripts/python.exe -B research/claim_debts_20261022/u1/eb_sample.py RUN
Writes results/claim_debts_20261022/u1/RUN/eb_sample.json (exclusive create).
"""
import hashlib
import json
import math
import os
import sys
import time

sys.path.insert(0, os.getcwd())
import numpy as np  # noqa: E402

from research.frontier_classical_20261001.c2_timing import machine_state  # noqa: E402

RUN = sys.argv[1]
OUT = os.path.join("results", "claim_debts_20261022", "u1", RUN)
NA, NT = 8, 52
S0, K, H, SIG, RHO, R, T = 100.0, 100.0, 140.0, 0.3, 0.4, 0.03, 1.0
N_TOTAL = 2 ** 23  # fixed in advance (no pilot, no stopping rule)
CHUNK = 2 ** 15
SEED = [2026102231, 8, 52]


def chunk_payoffs(rng, m):
    dt = T / NT
    t = dt * np.arange(1, NT + 1)
    w0 = np.cumsum(rng.standard_normal((m, NT)), axis=1) * math.sqrt(dt)
    wi = np.cumsum(rng.standard_normal((m, NA, NT)), axis=2) * math.sqrt(dt)
    x = math.log(S0) + (R - 0.5 * SIG * SIG) * t + SIG * (math.sqrt(RHO) * w0[:, None, :] + math.sqrt(1 - RHO) * wi)
    s = np.exp(x)
    b = s.mean(axis=1)  # (m, NT) date baskets
    alive = (b < H).all(axis=1)
    a = b.mean(axis=1)
    return math.exp(-R * T) * np.maximum(a - K, 0.0) * alive


def main():
    os.makedirs(OUT, exist_ok=False)
    m0 = machine_state()
    rng = np.random.default_rng(SEED)
    t0, c0 = time.perf_counter(), time.process_time()
    n, s1, s2, lo, hi = 0, [], [], math.inf, -math.inf
    while n < N_TOTAL:
        y = chunk_payoffs(rng, min(CHUNK, N_TOTAL - n))
        s1.append(math.fsum(y.tolist()))
        s2.append(math.fsum((y * y).tolist()))
        lo, hi = min(lo, float(y.min())), max(hi, float(y.max()))
        n += y.size
    S1, S2 = math.fsum(s1), math.fsum(s2)
    wall, cpu = time.perf_counter() - t0, time.process_time() - c0
    m1 = machine_state()
    rec = dict(
        meta=dict(script="research/claim_debts_20261022/u1/eb_sample.py", python=sys.version, numpy=np.__version__,
                  script_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
                  rng="numpy PCG64 default_rng(%s), standard_normal" % SEED, n_fixed_in_advance=N_TOTAL,
                  chunk=CHUNK, contract=dict(na=NA, nt=NT, spot=S0, strike=K, barrier=H, sigma=SIG, rho=RHO,
                                             rate=R, maturity=T, barrier_rule="alive iff max_j B_j < 140"),
                  label="meas (iid pseudo-random sample; iid-ness of the PRNG stream is assm)"),
        machine=[m0, m1], wall_s=wall, cpu_s=cpu,
        n=n, sum=S1, sum_sq=S2, mean=S1 / n, var_unbiased=(S2 - S1 * S1 / n) / (n - 1), min=lo, max=hi,
        range_upper=40.0 * math.exp(-R * T))
    with open(os.path.join(OUT, "eb_sample.json"), "x", encoding="utf-8") as f:
        json.dump(rec, f, indent=1)
    print(json.dumps({k: rec[k] for k in ("n", "mean", "var_unbiased", "min", "max", "wall_s", "cpu_s")}))


if __name__ == "__main__":
    main()
