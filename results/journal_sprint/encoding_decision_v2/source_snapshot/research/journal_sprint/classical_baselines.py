"""Costed classical discovery baselines with independent pilot streams."""

from .checks import require

import argparse
import math
import shutil
import time

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm, qmc, t

from .storage import ROOT, finish_run, rng_for, start_run, write_json
from research.paper_a.benchmark import C6, by_id
from research.paper_a.references import black_scholes_call


def brownian_pca(d, maturity):
    dates = np.arange(1, d + 1) * maturity / d
    covariance = np.minimum.outer(dates, dates)
    values, vectors = np.linalg.eigh(covariance)
    return dates, vectors[:, ::-1] * np.sqrt(np.maximum(values[::-1], 0))


def geometric_price(S0, K, rate, sigma, maturity, d):
    dates = np.arange(1, d + 1) * maturity / d
    mu = math.log(S0) + (rate - sigma**2 / 2) * dates.mean()
    variance = sigma**2 * np.minimum.outer(dates, dates).mean()
    vol = math.sqrt(variance)
    d2 = (mu - math.log(K)) / vol
    return math.exp(-rate * maturity) * (
        math.exp(mu + variance / 2) * norm.cdf(d2 + vol) - K * norm.cdf(d2)
    )


def payoffs(z, spec, dates, factor):
    logs = (
        math.log(spec["S0"])
        + (spec["rate"] - spec["sigma"] ** 2 / 2) * dates
        + spec["sigma"] * (z @ factor.T)
    )
    stock = np.exp(logs)
    discount = math.exp(-spec["rate"] * spec["maturity"])
    if spec["kind"] == "european":
        return discount * np.maximum(stock[:, -1] - spec["K"], 0), discount * stock[:, -1]
    return (
        discount * np.maximum(stock.mean(axis=1) - spec["K"], 0),
        discount * np.maximum(np.exp(logs.mean(axis=1)) - spec["K"], 0),
    )


def estimate(spec, method, paths, key, pilot_paths=1024):
    if method not in {"mc", "cv_mc", "rqmc"}:
        raise ValueError("unknown classical method")
    if spec["kind"] not in {"european", "asian"}:
        raise ValueError("unknown option kind")
    if isinstance(paths, bool) or not isinstance(paths, int) or paths < 2:
        raise ValueError("paths must be an integer >= 2")
    tick = time.perf_counter()
    dates, factor = brownian_pca(spec["d"], spec["maturity"])
    control_mean = (
        spec["S0"]
        if spec["kind"] == "european"
        else geometric_price(
            spec["S0"], spec["K"], spec["rate"], spec["sigma"], spec["maturity"], spec["d"]
        )
    )
    use_control = method == "cv_mc" or (method == "rqmc" and spec["kind"] == "asian")
    if use_control and (
        isinstance(pilot_paths, bool) or not isinstance(pilot_paths, int) or pilot_paths < 2
    ):
        raise ValueError("control pilot requires at least two paths")
    coefficient = 0.0
    if use_control:
        z = rng_for(*key, "pilot").standard_normal((pilot_paths, spec["d"]))
        y, x = payoffs(z, spec, dates, factor)
        variance = float(np.var(x, ddof=1))
        coefficient = float(np.cov(x, y, ddof=1)[0, 1] / variance) if variance > 0 else 0.0
    else:
        pilot_paths = 0
    seeds = []
    if method == "rqmc":
        if paths < 64 or paths % 32 or (paths // 32) & (paths // 32 - 1):
            raise ValueError("RQMC requires 32 power-of-two sized scrambles")
        estimates = []
        for scramble in range(32):
            seed = int(rng_for(*key, "scramble", scramble).integers(0, 2**32))
            seeds.append(seed)
            uniforms = qmc.Sobol(d=spec["d"], scramble=True, seed=seed).random_base2(
                int(math.log2(paths // 32))
            )
            z = norm.ppf(np.clip(uniforms, np.finfo(float).eps, 1 - np.finfo(float).eps))
            y, x = payoffs(z, spec, dates, factor)
            estimates.append(float(np.mean(y - coefficient * (x - control_mean))))
        samples = np.array(estimates)
    else:
        z = rng_for(*key, "evaluation").standard_normal((paths, spec["d"]))
        y, x = payoffs(z, spec, dates, factor)
        samples = y - coefficient * (x - control_mean)
        estimates = None
    price = float(samples.mean())
    se = float(samples.std(ddof=1) / math.sqrt(len(samples)))
    return {
        "price": price,
        "se": se,
        "radius": float(t.ppf(0.975, len(samples) - 1) * se),
        "df": len(samples) - 1,
        "sample_sum": float(samples.sum()),
        "sample_sum_squares": float(np.dot(samples, samples)),
        "coefficient": coefficient,
        "control_mean": control_mean,
        "scramble_means": estimates,
        "scramble_seeds": seeds,
        "paths": paths,
        "pilot_paths": pilot_paths,
        "total_paths": paths + pilot_paths,
        "normal_variates": (paths + pilot_paths) * spec["d"],
        "seconds": time.perf_counter() - tick,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week3_classical_v1")
    args = parser.parse_args(argv)
    path = start_run(
        args.output,
        {"protocol": "PROTOCOL_W3_CLASSICAL", "paths": [4096, 16384], "repetitions": 10},
    )
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += [
        ROOT / "docs/journal_sprint/PROTOCOL_W3_CLASSICAL.md",
        ROOT / "research/paper_a/benchmark.py",
        ROOT / "research/paper_a/references.py",
    ]
    for source in sources:
        target = path / "source_snapshot" / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    specs = []
    for cid in C6:
        c = by_id(cid)
        specs.append(
            {
                "id": cid,
                "kind": "european",
                "d": 1,
                "S0": c.S0,
                "K": c.K,
                "rate": c.r,
                "sigma": c.sigma,
                "maturity": c.T,
            }
        )
    for d in (8, 32):
        specs.append(
            {
                "id": f"ASIAN{d}",
                "kind": "asian",
                "d": d,
                "S0": 100.0,
                "K": 100.0,
                "rate": 0.05,
                "sigma": 0.2,
                "maturity": 1.0,
            }
        )
    write_json(path / "specs.json", specs)
    rows = []
    references = {}
    for spec in specs:
        cid = spec["id"]
        if spec["kind"] == "european":
            S0, K, r, sigma, T = (spec[k] for k in ("S0", "K", "rate", "sigma", "maturity"))
            bs = black_scholes_call(S0, K, r, sigma, T)
            cutoff = (math.log(K / S0) - (r - sigma**2 / 2) * T) / (sigma * math.sqrt(T))

            # Integrate the smooth positive-payoff branch in log space; avoid exp overflow.
            def integrand(z):
                return (
                    math.exp(-r * T)
                    * (
                        S0 * math.exp((r - sigma**2 / 2) * T + sigma * math.sqrt(T) * z - z * z / 2)
                        - K * math.exp(-z * z / 2)
                    )
                    / math.sqrt(2 * math.pi)
                )

            value, error = quad(integrand, cutoff, np.inf, epsabs=1e-10, epsrel=1e-10)
            require(abs(bs - value) < 1e-8)
            references[cid] = {
                "price": bs,
                "quadrature": value,
                "quad_error_estimate": error,
                "se": 0.0,
                "exact_model_reference": True,
            }
        else:
            reference = estimate(spec, "rqmc", 32 * 16384, ("week3", cid, "reference"), 4096)
            references[cid] = {**reference, "exact_model_reference": False}
        write_json(path / f"reference_{cid}.json", references[cid])
        for method in ("mc", "cv_mc", "rqmc"):
            for paths in (4096, 16384):
                for rep in range(10):
                    key = ("week3_classical", cid, method, paths, rep)
                    result = estimate(spec, method, paths, key)
                    row = {
                        "contract": cid,
                        "method": method,
                        "rep": rep,
                        "seed_key": key,
                        **result,
                        "reference_deviation": result["price"] - references[cid]["price"],
                    }
                    write_json(path / f"{cid}_{method}_{paths}_{rep}.json", row)
                    rows.append(row)
        print(cid, "completed", flush=True)
    write_json(path / "rows.json", rows)
    finish_run(path)


if __name__ == "__main__":
    main()
