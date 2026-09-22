"""Bounded exploratory GBM screen; not a confidence certificate or holdout.

Run from repository root: python -m research.advantage_investigation_20260922.classical_screen
Uses existing source unchanged; records every declared case/method/sample size.
"""

import os

for _key in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ[_key] = "1"

import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy
from scipy.integrate import quad
from scipy.special import ndtr
from scipy.stats import t

from research.journal_sprint.asian_basket import Basket, estimate, fit_control, setup


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/advantage_investigation_20260922/classical_screen.json"
CASES = [
    ("D1", Basket(1, 2, 95, sigma=.2, correlation=.3)),
    ("D2", Basket(2, 2, 105, sigma=.25, correlation=.4)),
    ("B4x12", Basket(4, 12, 100, sigma=.3, correlation=.4)),
    ("B8x52", Basket(8, 52, 100, sigma=.3, correlation=.4)),
]


def d1_reference():
    """One-dimensional conditioning at first date; quadrature error is empirical."""
    discount = math.exp(-.03)
    dt = .5
    sigma = .2

    def integrand(z):
        first = 100 * math.exp((.03 - sigma**2 / 2) * dt + sigma * math.sqrt(dt) * z)
        strike2 = 190 - first
        mean2 = first * math.exp(.03 * dt)
        if strike2 <= 0:
            payoff = (mean2 - strike2) / 2
        else:
            d2 = (math.log(first / strike2) + (.03 - sigma**2 / 2) * dt)
            d2 /= sigma * math.sqrt(dt)
            payoff = (mean2 * ndtr(d2 + sigma * math.sqrt(dt)) - strike2 * ndtr(d2)) / 2
        return discount * payoff * math.exp(-z*z/2) / math.sqrt(2*math.pi)

    begin = time.perf_counter()
    value, err = quad(integrand, -12, 12, epsabs=1e-10, epsrel=1e-12)
    return dict(price=value, scipy_error_estimate=err, seconds=time.perf_counter()-begin,
                range=[-12, 12], rigorous=False,
                note="Normal tails and floating arithmetic not interval-certified")


def main():
    if OUT.exists():
        raise FileExistsError("Preserve prior evidence; choose a new output version")
    begin_all = time.perf_counter()
    rows = []
    for ci, (name, contract) in enumerate(CASES):
        begin = time.perf_counter()
        model = setup(contract)
        setup_seconds = time.perf_counter() - begin
        methods = ["mc_cv", "rqmc_cv"]
        if name in ("D1", "D2"):
            methods.append("conditional_cv")
        for mi, method in enumerate(methods):
            pilot_seed = 922600 + 100 * ci + mi
            begin = time.perf_counter()
            beta, root = fit_control(contract, model, np.random.default_rng(pilot_seed),
                                     conditional=method == "conditional_cv", count=1024)
            pilot_seconds = time.perf_counter() - begin
            for power in (8, 10, 12):
                seeds = [923000 + ci*10000 + mi*1000 + power*32 + i for i in range(16)]
                begin = time.perf_counter()
                samples = [estimate(contract, model, power, seed, method, beta) for seed in seeds]
                seconds = time.perf_counter() - begin
                values = np.array([x[0] for x in samples])
                row = dict(case=name, dimension=contract.assets*contract.dates,
                           contract=contract.__dict__, method=method, power=power,
                           pilot_seed=pilot_seed, beta=beta, seeds=seeds,
                           replicate_prices=values.tolist(), price=float(values.mean()),
                           empirical_95_halfwidth=float(t.ppf(.975, 15)*values.std(ddof=1)/4),
                           setup_seconds=setup_seconds, pilot_seconds=pilot_seconds,
                           evaluation_seconds=seconds,
                           total_seconds=setup_seconds+pilot_seconds+seconds,
                           paths_including_pilot=16*2**power+1024,
                           max_root_residual=max([root]+[x[1] for x in samples]))
                rows.append(row)
                print(name, method, power, row["price"], row["empirical_95_halfwidth"],
                      row["total_seconds"], flush=True)
    archive = json.loads((ROOT / "results/journal_sprint/common_compilation_20260922_v2/results.json").read_text())
    result = dict(scope="exploratory continuous-Gaussian discretely monitored GBM precision screen",
                  statistical_warning="Student t intervals across 16 replicates are empirical; no rigorous coverage claim",
                  selection_warning="All cases are development; no independent confirmation",
                  timing_warning="Single process/thread CPU; imports/interpreter startup excluded; no GPU comparison",
                  environment=dict(python=sys.version, numpy=np.__version__, scipy=scipy.__version__,
                                   platform=platform.platform(), processor=platform.processor()),
                  d1_reference=d1_reference(), rows=rows, total_wall_seconds=time.perf_counter()-begin_all,
                  source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in [Path(__file__), ROOT / "research/journal_sprint/asian_basket.py"]},
                  quantum_archive_type=type(archive).__name__)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf8")


if __name__ == "__main__":
    main()
