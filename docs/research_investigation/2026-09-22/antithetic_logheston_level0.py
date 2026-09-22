"""Independent level-zero and memory supplement to the exploratory pilot.

Does not overwrite the original pilot output. Memory includes Python/scipy and
uses Windows peak working set where available. No quantum-resource inference.
"""
from pathlib import Path
import hashlib
import json
import math
import time

import numpy as np
import psutil
from scipy.stats import t

from antithetic_logheston_pilot import (
    PARAMETERS, MASTER_SEED, REPLICATES, PATHS, advance, coupled_payoffs)


def peak_memory_bytes():
    info = psutil.Process().memory_info()
    return int(getattr(info, 'peak_wset', info.rss))


def level_zero(assets, seed_words):
    start = time.perf_counter()
    rng = np.random.default_rng(np.random.SeedSequence(seed_words))
    p = PARAMETERS
    dt = p['T']/p['monitoring_dates']
    logs = np.full((PATHS, assets), math.log(p['S0']))
    variance = np.full((PATHS, assets), p['v0'])
    accumulated = np.zeros(PATHS)
    min_v = p['v0']
    random_seconds = 0.
    path_seconds = 0.
    for _ in range(p['monitoring_dates']):
        tick = time.perf_counter()
        z = rng.standard_normal((PATHS, 1+2*assets))
        ds = math.sqrt(p['equity_correlation'])*z[:, :1] + math.sqrt(1-p['equity_correlation'])*z[:, 1:assets+1]
        dv = p['equity_variance_correlation']*ds + math.sqrt(1-p['equity_variance_correlation']**2)*z[:, assets+1:]
        ds *= math.sqrt(dt)
        dv *= math.sqrt(dt)
        random_seconds += time.perf_counter()-tick
        tick = time.perf_counter()
        logs, variance = advance(logs, variance, ds, dv, dt, p)
        accumulated += np.exp(logs).mean(axis=1)
        min_v = min(min_v, float(variance.min()))
        path_seconds += time.perf_counter()-tick
    payoff = math.exp(-p['rate']*p['T'])*np.maximum(accumulated/p['monitoring_dates']-p['K'], 0)
    assert min_v > 0 and np.isfinite(payoff).all()
    return dict(assets=assets, level=0, seed_words=seed_words, paths=PATHS,
                mean=float(payoff.mean()), variance=float(payoff.var(ddof=1)),
                sum=float(payoff.sum()), sum_squares=float(np.dot(payoff, payoff)),
                seconds=time.perf_counter()-start, random_seconds=random_seconds,
                path_and_monitoring_seconds=path_seconds,
                minimum_variance=min_v, process_peak_working_set_bytes=peak_memory_bytes())


def run():
    start = time.perf_counter()
    rows = [level_zero(a, [MASTER_SEED, a, 0, rep]) for a in (1, 4) for rep in range(REPLICATES)]
    summaries = []
    for a in (1, 4):
        selected = [x for x in rows if x['assets']==a]
        n = PATHS*REPLICATES
        total = sum(x['sum'] for x in selected)
        squares = sum(x['sum_squares'] for x in selected)
        means = np.array([x['mean'] for x in selected])
        summaries.append(dict(assets=a, level=0, paths=n, mean=total/n,
            variance=(squares-total**2/n)/(n-1),
            empirical_95pct_mean_radius=float(t.ppf(.975, REPLICATES-1)*means.std(ddof=1)/math.sqrt(REPLICATES)),
            seconds=sum(x['seconds'] for x in selected),
            cpu_seconds_per_path=sum(x['seconds'] for x in selected)/n))
    # One previously executed worst-shape batch measures memory; does not
    # regenerate or replace the original ensemble or select new cases.
    payoffs, timing = coupled_payoffs(4, 5, PATHS, [MASTER_SEED, 4, 5, 0], PARAMETERS)
    memory_spot_check = dict(assets=4, level=5, paths=PATHS,
        seed_words=[MASTER_SEED, 4, 5, 0],
        process_peak_working_set_bytes=peak_memory_bytes(),
        process_peak_working_set_GiB=peak_memory_bytes()/2**30,
        antithetic_mean=float((.5*(payoffs[0]+payoffs[1])-payoffs[2]).mean()),
        seconds=timing['seconds'])
    assert memory_spot_check['process_peak_working_set_GiB'] < 16
    source = Path(__file__)
    result = dict(status='Executed independent level-zero and memory supplement; development cases only',
        parameters=PARAMETERS, rows=rows, summaries=summaries,
        memory_spot_check=memory_spot_check,
        memory_measurement='Windows process peak working set where available, otherwise RSS; includes imports. Original ensemble was not instrumented.',
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        imported_pilot_sha256=hashlib.sha256(source.with_name('antithetic_logheston_pilot.py').read_bytes()).hexdigest(),
        total_seconds=time.perf_counter()-start)
    source.with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
