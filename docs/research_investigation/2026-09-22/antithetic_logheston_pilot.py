"""Exploratory antithetic multilevel correction diagnostic, not a price certificate.

All contractual averages have exactly twelve equally spaced monitoring dates.
Fine and antithetic paths swap the same Gaussian vector pair within each coarse
step. No Levy-area samples, variance clipping, or true-price reference is used.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import math
import platform
import time

import numpy as np
from scipy.stats import t

PARAMETERS = dict(kappa=2.0, theta=0.09, v0=0.09, xi=0.3, rate=0.03,
                  S0=100.0, K=100.0, T=1.0, monitoring_dates=12,
                  equity_correlation=0.3, equity_variance_correlation=-0.5)
MASTER_SEED = 20260922
REPLICATES = 8
PATHS = 2048
LEVELS = list(range(1, 6))


def advance(logs, variance, equity_increment, variance_increment, dt, spec):
    root = np.sqrt(variance)
    new_logs = (logs + (spec['rate'] - 0.5*variance)*dt
                + root*equity_increment
                + spec['xi']/4*(equity_increment*variance_increment
                                - spec['equity_variance_correlation']*dt))
    new_variance = (variance + spec['kappa']*spec['theta']*dt
                    + spec['xi']*root*variance_increment
                    + 0.25*spec['xi']**2*(variance_increment**2-dt)) / (1+spec['kappa']*dt)
    return new_logs, new_variance


def gaussian_pair(rng, paths, assets, dt, spec):
    independent = rng.standard_normal((2, paths, 1+2*assets))
    equity = (math.sqrt(spec['equity_correlation'])*independent[..., :1]
              + math.sqrt(1-spec['equity_correlation'])*independent[..., 1:assets+1])
    variance = (spec['equity_variance_correlation']*equity
                + math.sqrt(1-spec['equity_variance_correlation']**2)*independent[..., assets+1:])
    return math.sqrt(dt)*equity, math.sqrt(dt)*variance


def coupled_payoffs(assets, level, paths, seed_words, spec):
    start = time.perf_counter()
    rng = np.random.default_rng(np.random.SeedSequence(seed_words))
    intervals_per_date = 2**(level-1)
    coarse_steps = spec['monitoring_dates']*intervals_per_date
    dt = spec['T']/(2*coarse_steps)
    shape = (paths, assets)
    logs = [np.full(shape, math.log(spec['S0'])) for _ in range(3)]
    variances = [np.full(shape, spec['v0']) for _ in range(3)]
    sums = [np.zeros(paths) for _ in range(3)]
    minimum_variance = spec['v0']
    random_seconds = 0.0
    path_seconds = 0.0
    for step in range(coarse_steps):
        tick = time.perf_counter()
        dw_s, dw_v = gaussian_pair(rng, paths, assets, dt, spec)
        random_seconds += time.perf_counter()-tick
        tick = time.perf_counter()
        for order in (0, 1):
            logs[0], variances[0] = advance(logs[0], variances[0], dw_s[order], dw_v[order], dt, spec)
            logs[1], variances[1] = advance(logs[1], variances[1], dw_s[1-order], dw_v[1-order], dt, spec)
        logs[2], variances[2] = advance(logs[2], variances[2], dw_s.sum(axis=0), dw_v.sum(axis=0), 2*dt, spec)
        minimum_variance = min(minimum_variance, *(float(v.min()) for v in variances))
        if (step+1) % intervals_per_date == 0:
            for index in range(3):
                sums[index] += np.exp(logs[index]).mean(axis=1)
        path_seconds += time.perf_counter()-tick
    payoffs = [math.exp(-spec['rate']*spec['T'])*np.maximum(x/spec['monitoring_dates']-spec['K'], 0) for x in sums]
    assert minimum_variance > 0
    assert all(np.isfinite(p).all() for p in payoffs)
    return payoffs, dict(seconds=time.perf_counter()-start, random_seconds=random_seconds,
                         path_and_monitoring_seconds=path_seconds,
                         minimum_variance=minimum_variance, coarse_steps=coarse_steps,
                         fine_steps=2*coarse_steps, gaussian_scalar_draws=coarse_steps*2*paths*(1+2*assets))


def correlation_matrix(assets, spec):
    equity = np.full((assets, assets), spec['equity_correlation'])
    np.fill_diagonal(equity, 1)
    rho = spec['equity_variance_correlation']
    return np.block([[equity, rho*equity],
                     [rho*equity, rho*rho*equity+(1-rho*rho)*np.eye(assets)]])


def constant_volatility_check():
    spec = dict(PARAMETERS, xi=0.0)
    values, timing = coupled_payoffs(4, 2, 128, [MASTER_SEED, 0], spec)
    errors = [float(np.max(np.abs(values[i]-values[2]))) for i in (0, 1)]
    assert max(errors) < 1e-10
    return dict(description='xi=0,v0=theta: fine, swapped-fine and coarse agree at contractual dates',
                maximum_pathwise_payoff_discrepancies=errors)


def run():
    tick = time.perf_counter()
    sanity = constant_volatility_check()
    raw = []
    summaries = []
    for assets in (1, 4):
        corr = correlation_matrix(assets, PARAMETERS)
        assert np.linalg.eigvalsh(corr).min() > 0
        for level in LEVELS:
            for replicate in range(REPLICATES):
                words = [MASTER_SEED, assets, level, replicate]
                (fine, swapped, coarse), timing = coupled_payoffs(assets, level, PATHS, words, PARAMETERS)
                differences = dict(plain=fine-coarse,
                                   antithetic=0.5*(fine+swapped)-coarse,
                                   swap_difference=fine-swapped)
                row = dict(assets=assets, level=level, replicate=replicate, paths=PATHS,
                           seed_words=words, **timing,
                           fine_mean=float(fine.mean()), swapped_mean=float(swapped.mean()),
                           coarse_mean=float(coarse.mean()))
                for name, vals in differences.items():
                    row[name] = dict(mean=float(vals.mean()), variance=float(vals.var(ddof=1)),
                                     sum=float(vals.sum()), sum_squares=float(np.dot(vals, vals)),
                                     max_absolute=float(np.abs(vals).max()))
                raw.append(row)
            level_rows = [x for x in raw if x['assets']==assets and x['level']==level]
            summary = dict(assets=assets, level=level, paths=PATHS*REPLICATES,
                           fine_steps=level_rows[0]['fine_steps'],
                           total_seconds=sum(x['seconds'] for x in level_rows),
                           min_variance_state=min(x['minimum_variance'] for x in level_rows))
            for name in ('plain', 'antithetic', 'swap_difference'):
                total = sum(x[name]['sum'] for x in level_rows)
                squares = sum(x[name]['sum_squares'] for x in level_rows)
                count = PATHS*REPLICATES
                replicate_means = np.array([x[name]['mean'] for x in level_rows])
                summary[name] = dict(mean=total/count, variance=(squares-total**2/count)/(count-1),
                                     empirical_95pct_mean_radius=float(t.ppf(.975, REPLICATES-1)*replicate_means.std(ddof=1)/math.sqrt(REPLICATES)),
                                     replicate_means=replicate_means.tolist())
            summary['variance_reduction_plain_over_antithetic'] = summary['plain']['variance']/summary['antithetic']['variance']
            summaries.append(summary)
            print(json.dumps(summary), flush=True)
    slopes = []
    for assets in (1, 4):
        for first in (1, 2, 3):
            selected_levels = list(range(first, 6))
            for kind in ('plain', 'antithetic'):
                selected = [x for x in summaries if x['assets']==assets and x['level'] in selected_levels]
                beta = -float(np.polyfit(selected_levels, np.log2([x[kind]['variance'] for x in selected]), 1)[0])
                replicate_betas = []
                for rep in range(REPLICATES):
                    selected_raw = [x for x in raw if x['assets']==assets and x['replicate']==rep and x['level'] in selected_levels]
                    replicate_betas.append(-float(np.polyfit(selected_levels, np.log2([x[kind]['variance'] for x in selected_raw]), 1)[0]))
                slopes.append(dict(assets=assets, correction=kind, fitted_levels=selected_levels,
                                   empirical_beta=beta, replicate_beta_values=replicate_betas,
                                   descriptive_95pct_t_radius=float(t.ppf(.975, REPLICATES-1)*np.std(replicate_betas, ddof=1)/math.sqrt(REPLICATES))))
    source = Path(__file__)
    result = dict(status='exploratory executed diagnostic; no theorem, price certificate, true-price reference, or quantum timing',
                  parameters=PARAMETERS, master_seed=MASTER_SEED, replicates=REPLICATES, paths_per_replicate=PATHS,
                  correlation_matrices={str(a):correlation_matrix(a, PARAMETERS).tolist() for a in (1, 4)},
                  environment=dict(python=platform.python_version(), numpy=np.__version__, platform=platform.platform()),
                  source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  constant_volatility_check=sanity, rows=raw, summaries=summaries, variance_decay_fits=slopes,
                  total_seconds=time.perf_counter()-tick,
                  limitations=['No continuous-model reference or certified bias.',
                               'Student intervals and slope intervals are descriptive, not finite-sample guarantees.',
                               'All cases are development data, not held-out confirmation.',
                               'CPU diagnostic prices three coupled paths; it is not quantum-oracle timing.',
                               'Induced off-diagonal variance correlation=.075, cross equity-variance correlation=-.15.',
                               'Positivity follows for these parameters; this is not a proof for arbitrary Heston parameters.'])
    source.with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(output=str(source.with_suffix('.json')), elapsed_seconds=result['total_seconds'], variance_decay_fits=slopes)), flush=True)


if __name__ == '__main__':
    run()
