"""Three frozen dollar splits for one original source; never changes shared budgets."""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import hashlib
import json
import math
import time

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/independent_110_20261004/C05/run001'
DOC=ROOT/'docs/independent_110_20261004/C05'
AUTHOR=Path(__file__).resolve()
CORPUS=[ROOT/p for p in [
    'docs/limitation_audit_20261001/implementation_plan/roadmap.json',
    'results/limitation_program_20261001/E07_original_BM_G2_composition_audit_run001/B4x12_G2_composed_ledger.json',
    'results/limitation_program_20261001/E07_original_BM_G2_composition_audit_run001/manifest.json',
    'results/limitation_program_20261001/E07_schedule_run001/schedule.json',
    'results/limitation_program_20261001/E02_financial_run002/B4x12/estimator_ledger.json',
]]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pair(q): return [q.numerator,q.denominator]
def dump(p,v): p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')

def prepare():
    assert not OUT.exists()
    OUT.mkdir(parents=True)
    dump(OUT/'protocol.json',{'author_sha256':sha(AUTHOR),'corpus':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in CORPUS},
        'case':'Original B4x12 q32 Box-Muller/native72F40, fixed already discounted payoff and source.',
        'grid_statistical_dollar_fractions':[[7,20],[9,20],[11,20]],
        'epsilon_exact':[1,100],'ideal_failure_allowance':[3,1000],
        'qpe_bits_search':[1,20],'odd_repetitions_search':[1,31],
        'acceptance':['All3rows have known certified source bias plus statistical bound<=one cent.',
                      'Minimal integer rounds satisfy archived uniform AE bound and exact majority failure<=3/1000.',
                      'Only strict paid logical-call reduction can survive as a candidate; absent physical bounds prohibit a full99% claim.'],
        'assumptions':'Archived source-specific G2 bias certificate and rational pi/single-shot probability enclosures are fixed accepted inputs; no new source certificate is proved.',
        'budgets':{'cpu_seconds':30,'wall_seconds':60,'output_bytes':4*1024*1024},
        'stop':'Exactly3allocations, one fixed source. Retain original split if no strict improvement; no retiming, source substitution or confidence revision.',
        'new_finance_draws':0,'new_global_fixture_credit':0})
    print('C05 one-source three-allocation grid frozen.')

def run():
    cpu=time.process_time(); wall=time.monotonic()
    p=json.loads((OUT/'protocol.json').read_text())
    assert not (OUT/'RUN_STARTED.json').exists() and sha(AUTHOR)==p['author_sha256']
    for path,wanted in p['corpus'].items(): assert sha(ROOT/path)==wanted
    dump(OUT/'RUN_STARTED.json',{'allocations':3,'finance_draws':0})
    ledger=json.loads(CORPUS[1].read_text()); schedule=json.loads(CORPUS[3].read_text()); invocation=json.loads(CORPUS[4].read_text())
    assert ledger['source_specific_mathematical_G2_bias_complete'] is True
    bias_terms=[t for t in ledger['dollar_terms'] if t['name']!='statistical_digital_mean']
    assert all(t['bound'] is not None for t in bias_terms)
    bias=sum(Q(*t['bound']) for t in bias_terms)
    stat=next(t for t in ledger['dollar_terms'] if t['name']=='statistical_digital_mean')
    assert Q(*stat['bound'])==Q(9,2000)==Q(*schedule['statistical_error_dollars_exact'])
    span=schedule['normalization_span_dollars']; pi_hi=Q(*schedule['pi_enclosure_exact'][1])
    elementary=Q(*schedule['elementary_failure_upper_exact']); epsilon=Q(1,100); alpha=Q(3,1000)
    majority=[]
    for r in range(1,32,2):
        failure=sum(Q(math.comb(r,j))*elementary**j*(1-elementary)**(r-j) for j in range(r//2+1,r+1))
        majority.append((r,failure))
    r,fail=next((r,f) for r,f in majority if f<=alpha)
    assert r==schedule['repetitions'] and fail==Q(*schedule['ideal_failure_upper_exact'])
    baseline=schedule['controlled_grover_calls']; readout=Q(*invocation['classical_readout_error_allowance'])
    rows=[]
    for fraction_pair in p['grid_statistical_dollar_fractions']:
        allowance=epsilon*Q(*fraction_pair)
        bits=next(k for k in range(1,21) if span*(pi_hi/(1<<k)+pi_hi*pi_hi/(1<<(2*k)))+readout<=allowance)
        actual=span*(pi_hi/(1<<bits)+pi_hi*pi_hi/(1<<(2*bits)))+readout
        assert bias+allowance<=epsilon and actual<=allowance and fail<=alpha
        calls=r*((1<<bits)-1)
        rows.append({'statistical_fraction':fraction_pair,'statistical_allowance':pair(allowance),
            'known_source_bias':pair(bias),'bias_plus_statistical_allowance':pair(bias+allowance),
            'actual_ideal_error_plus_readout_upper':pair(actual),'qpe_bits':bits,'odd_repetitions':r,
            'controlled_grover_calls':calls,'source_forward_calls':calls,'source_inverse_calls':calls,
            'fresh_preparations':r,'ideal_failure_upper':pair(fail),'math_dollar_row_feasible':True,
            'physical_failure_upper':None,'full_joint99_certificate':False,
            'emitted_changed_IQFT_recipe':False,'strict_call_improvement':calls<baseline})
    # Preserve all missing execution failures. They are never filled with zero.
    unknown=[t['name'] for t in ledger['failure_terms'] if t['bound'] is None]
    assert 'physical_execution' in unknown
    assert any(Q(*t['allowance']) for t in ledger['failure_terms'] if t['bound'] is None)
    summary={'passed':True,'completed':True,'scope':'C05 three mathematical error-allocation rows for one frozen original source.',
        'decision':'RETAIN_ORIGINAL_045_SPLIT_NO_STRICT_CALL_IMPROVEMENT',
        'feasible_mathematical_rows':3,'baseline_controlled_grover_calls':baseline,
        'row_call_counts':[r['controlled_grover_calls'] for r in rows],
        'any_strict_call_improvement':any(r['strict_call_improvement'] for r in rows),
        'missing_execution_failures':unknown,'active_budgets_changed':False,
        'full_joint99_certificate':False,'source_adoption':False,'quantum_advantage':False,
        'new_finance_draws':0,'new_global_fixture_credit':0}
    assert not summary['any_strict_call_improvement']
    dump(OUT/'allocation_rows.json',rows); dump(OUT/'summary.json',summary)
    DOC.mkdir(parents=True,exist_ok=True)
    report=DOC/'RESULTS.txt'; assert not report.exists()
    report.write_text('C05: fixed original B4x12 allocation screen\n\n'
        'Three preregistered statistical fractions0.35/0.45/0.55 passed the mathematical dollar and ideal-estimator constraints using the accepted source bias. All require16QPEbits,15fresh shots and983025controlled iterates. Their source-forward and source-inverse calls are each983025. No strict call improvement was found; retain the original0.45split.\n\n'
        'Finite bound: span*(pi_hi/M+pi_hi^2/M^2)+certified readout error. Uniform per-shot failure and an exact binomial majority tail determine odd repetitions. The source bias is charged once and is not rerun or recertified.\n\n'
        'The physical-execution failure remainsNULL. These are feasible mathematical rows under accepted archived source/schedule inputs, not three complete99%delivery certificates or emitted alternateIQFTs. No source, estimator, shared confidence or budget was changed; no new matched timing or advantage.\n')
    for path,wanted in p['corpus'].items(): assert sha(ROOT/path)==wanted
    assert time.process_time()-cpu<=30 and time.monotonic()-wall<=60
    files=[x for x in OUT.iterdir() if x.is_file()]+[report]
    assert sum(x.stat().st_size for x in files)+32768<=4*1024*1024
    dump(OUT/'manifest.json',{'files':{str(x.relative_to(ROOT)).replace('\\','/'):{'sha256':sha(x),'bytes':x.stat().st_size} for x in files},'author_sha256':sha(AUTHOR),'input_pins':p['corpus']})
    print(json.dumps(summary))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['prepare','run']);args=ap.parse_args()
    if args.mode=='prepare':prepare()
    else:
        try:run()
        except BaseException as exc:
            if OUT.exists():dump(OUT/'FAILED_UNSEALED.json',{'passed':False,'completed':False,'message':str(exc)[:2048],'failure_overrides_partial_summary':True})
            raise
