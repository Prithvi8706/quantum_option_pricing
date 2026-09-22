"""Separate fixed-work Hoeffding diagnostic; see adjacent protocol."""
import json
import time
from pathlib import Path
from heston_discrete_pilot import np, simulate, N, DISCOUNT

def main():
    bound = 200*DISCOUNT
    epsilon,delta=.25,.05
    required=int(np.ceil(bound**2*np.log(2/delta)/(2*epsilon**2)))
    rng=np.random.default_rng(22094026)
    done=0
    total=0.
    cap_exceedances=0
    max_payoff=0.
    started=time.perf_counter()
    while done<required and time.perf_counter()-started<120:
        batch=min(8192,required-done)
        signs=2*rng.integers(0,2,size=(batch,2*N),dtype=np.int8)-1
        payoffs,_,diagnostic=simulate(np.concatenate([signs,-signs],axis=0))
        total+=float(payoffs.sum())
        done+=batch
        cap_exceedances+=diagnostic['cap_exceedances']
        max_payoff=max(max_payoff,diagnostic['max_payoff'])
    elapsed=time.perf_counter()-started
    result={'contract':'capped discounted weak Euler Asian; not continuous or uncapped','seed':22094026,'required_pairs':required,'completed_pairs':done,'price':total/done,'epsilon':epsilon,'delta':delta,'hoeffding_radius':float(bound*np.sqrt(np.log(2/delta)/(2*done))),'range_bound':float(bound),'completed':done==required,'seconds':elapsed,'cap_exceedances':cap_exceedances,'max_raw_payoff_observed':max_payoff,'negative_variance_events':0,'assumptions':['ideal iid sign generation represented by PCG64','floating-point payoff error negligible; not certified','cap200 is contractual; no tail-price claim','same SDE step and monitoring convention as Wang-Kan; no fixed-point equivalence assertion']}
    Path(__file__).with_name('heston_hoeffding_pilot_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
