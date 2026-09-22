"""Bounded Heston discrete target diagnostic; protocol is in adjacent markdown."""
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import json
import platform
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import qmc, t

N = 256
H = 1.0 / N
DISCOUNT = np.exp(-.03)
SAMPLES = 4096
REPLICATES = 16

def simulate(signs):
    count = signs.shape[0]
    v = np.full(count, .1)
    log_return = np.zeros(count)
    asset_sum = np.zeros(count)
    log_sum = np.zeros(count)
    negative_variance = 0
    for step in range(N):
        negative_variance += int(np.count_nonzero(v < 0))
        if negative_variance:
            raise ValueError('Negative variance violates unchanged weak scheme')
        root_vh = np.sqrt(v * H)
        log_return += (.03 - .5 * v) * H + root_vh * (-.1 * signs[:, 2*step] + np.sqrt(.99)*signs[:, 2*step+1])
        v += 2 * (.12 - v) * H + .3 * root_vh * signs[:, 2*step]
        asset_sum += 100 * np.exp(log_return)
        log_sum += log_return
    raw = np.maximum(asset_sum / N - 90, 0)
    capped = np.minimum(raw, 200) * DISCOUNT
    control = log_sum / N
    return (capped[:count//2]+capped[count//2:])/2, (control[:count//2]+control[count//2:])/2, {'cap_exceedances':int(np.count_nonzero(raw > 200)), 'max_payoff':float(raw.max()), 'negative_variance':negative_variance, 'raw_price':float(raw.mean()*DISCOUNT)}

def draw(method, seed):
    if method == 'mc':
        signs = 2 * np.random.default_rng(seed).integers(0,2,size=(SAMPLES,2*N),dtype=np.int8) - 1
    else:
        signs = (2*(qmc.Sobol(2*N, scramble=True, seed=seed).random_base2(12) >= .5).astype(np.int8)-1)
    return np.concatenate([signs, -signs], axis=0)

def summary(values):
    values=np.asarray(values)
    se=float(values.std(ddof=1)/np.sqrt(len(values)))
    return {'price':float(values.mean()),'replicate_se':se,'halfwidth90_empirical_t':float(t.ppf(.95,len(values)-1)*se),'halfwidth95_empirical_t':float(t.ppf(.975,len(values)-1)*se),'replicate_prices':values.tolist()}

def main():
    m_v, m_r, m_c = .1, 0., 0.
    for _ in range(N):
        m_r += (.03 - .5*m_v)*H
        m_c += m_r / N
        m_v += 2*(.12-m_v)*H
    started=time.perf_counter()
    train_y,train_c,train_diagnostic=simulate(draw('mc',22091026))
    beta=float(np.cov(train_y,train_c,ddof=1)[0,1]/np.var(train_c,ddof=1))
    train_time=time.perf_counter()-started
    results={'contract':'discounted capped weak Euler N256 Asian; empirical uncertainty only','environment':{'platform':platform.platform(),'processor':platform.processor(),'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'thread_limits':{k:os.environ[k] for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']}},'training':{'seconds':train_time,'beta':beta,'control_exact_discrete_mean':m_c,'diagnostic':train_diagnostic},'methods':{}}
    for method,seed_base in [('mc',22092026),('sobol',22093026)]:
        raw,controlled,diagnostics=[],[],[]
        started=time.perf_counter()
        for replicate in range(REPLICATES):
            y,c,d=simulate(draw(method,seed_base+replicate))
            raw.append(float(y.mean()))
            controlled.append(float((y-beta*(c-m_c)).mean()))
            diagnostics.append(d)
        elapsed=time.perf_counter()-started
        results['methods'][method]={'raw':summary(raw),'controlled':summary(controlled),'run_seconds':elapsed,'controlled_total_seconds_with_training':elapsed+train_time,'replicates':REPLICATES,'base_points_per_replicate':SAMPLES,'paths_per_replicate':2*SAMPLES,'seed_base':seed_base,'diagnostics':diagnostics}
    results['published_circuit_sensitivity']={'T_count':2.4e11,'T_depth':1.2e11,'logical_qubits':22000,'discounted_dollar_error_excluding_model_bias':float(DISCOUNT*200*.0013),'scenarios':[{'effective_T_layer_seconds':latency,'runtime_lower_bound_seconds':1.2e11*latency,'classical_seconds_required_for_10x_quantum_win':10*1.2e11*latency} for latency in [1e-7,1e-6,1e-5]]}
    destination=Path(__file__).with_name('heston_discrete_pilot_results.json')
    destination.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))

if __name__ == '__main__':
    main()
