"""Independent direct-combination audit of sealed E08 allocation arithmetic."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib
import json
import math
import time
import copy

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT/'results/independent_110_20261004/E08/run004'
OUT = ROOT/'results/independent_110_20261004/E08/audit_run001'
ALPHA = Q(3,1000)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def tail(r,k,p,below):
    # Direct binomial coefficients; no producer recurrence or threshold optimizer.
    n,d=p.numerator,p.denominator
    indices=range(k) if below else range(k,r+1)
    return Q(sum(math.comb(r,j)*n**j*(d-n)**(r-j) for j in indices),d**r)

def verify(schedule, original):
    assert len(schedule)==len(original)
    failure=Q(0); calls=0
    for s,o in zip(schedule,original):
        assert s['stage']==o['stage'] and s['T']==o['T']
        r,k=s['repetitions'],s['threshold']
        assert type(r) is int and 1<=r<=128 and type(k) is int and 0<=k<=r+1
        fs=tail(r,k,Q(*o['p_plus_small_lower_exact']),True)
        fl=tail(r,k,Q(*o['p_plus_large_upper_exact']),False)
        assert fs==Q(*s['small_failure_exact']) and fl==Q(*s['large_failure_exact'])
        assert max(fs,fl)==Q(*s['max_failure_exact'])<=Q(*s['failure_allocation_exact'])
        assert s['controlled_U_calls']==r*o['T']
        calls+=r*o['T']; failure+=max(fs,fl)
    assert failure<=ALPHA and sum(Q(*s['failure_allocation_exact']) for s in schedule)<=ALPHA
    return calls, failure

def main():
    cpu=time.process_time(); wall=time.monotonic()
    assert not OUT.exists() and not list(RUN.glob('*FAIL*'))
    mf=json.loads((RUN/'manifest.json').read_text())
    pins={}
    for kind in ('files','input_pins'):
        for rel,spec in mf[kind].items():
            digest=spec if isinstance(spec,str) else spec['sha256']
            assert sha(ROOT/rel)==digest
            pins[rel]=digest
    author=ROOT/'research/independent_110_20261004/E08/confidence_allocation_screen_v4.py'
    assert sha(author)==mf['author_sha256']
    saved=json.loads((ROOT/'results/controlled_priority_completion/estimator_hadamard.json').read_text())
    candidates=json.loads((RUN/'schedules.json').read_text())
    summary=json.loads((RUN/'summary.json').read_text())
    assert summary['passed'] is True and summary['completed'] is True
    checks=[]; stage_checks=0; capped=0
    for row,old in zip(candidates,saved):
        assert row['model']==old['model'] and row['mode']==old['mode']
        stages=old['allocation']['stages']; feasible=[]
        for candidate in row['candidate_schedules']:
            if candidate.get('resource_rejected'):
                assert candidate['stages'] is None and candidate['controlled_U_calls'] is None
                assert candidate['reason']=='Frozen E08 repetition cap exhausted.'
                capped+=1; continue
            calls,failure=verify(candidate['stages'],stages)
            assert calls==candidate['controlled_U_calls'] and failure==Q(*candidate['max_failure_sum_exact'])
            feasible.append((calls,candidate['name']))
            checks.append({'row':row['saved_row_index'],'candidate':candidate['name'],'calls':calls,'stages':len(stages),'passed':True})
            stage_checks+=len(stages)
            assert time.process_time()-cpu<30 and time.monotonic()-wall<60
        chosen=min(feasible)
        assert chosen==(row['selected_controlled_U_calls'],row['selected'])
        assert chosen[0]<row['baseline_controlled_U_calls']
        assert Q(*row['saving_exact'])==Q(row['baseline_controlled_U_calls']-chosen[0],row['baseline_controlled_U_calls'])
    negative=[]
    sample=candidates[0]['candidate_schedules'][0]['stages']
    for name in ['call_count','T_geometry','threshold','allocation']:
        mutated=copy.deepcopy(sample)
        if name=='call_count': mutated[0]['controlled_U_calls']+=1
        elif name=='T_geometry': mutated[0]['T']+=1
        elif name=='threshold': mutated[0]['threshold']=0
        else: mutated[0]['failure_allocation_exact']=[1,1]
        try:
            verify(mutated,saved[0]['allocation']['stages'])
        except AssertionError:
            negative.append({'mutation':name,'rejected':True})
        else:
            raise AssertionError('Negative accounting control accepted: '+name)
    assert len(candidates)==4 and len(checks)+capped==20
    OUT.mkdir(parents=True)
    result={'passed':True,'sealed_manifest_sha256':sha(RUN/'manifest.json'),
        'author_sha256':sha(author),'frozen_inputs_and_owned_hashes':len(pins)+1,
        'feasible_candidates_directly_audited':len(checks),'stage_tail_checks':stage_checks,
        'retained_cap_rejections':capped,'candidate_checks':checks,'negative_controls':negative,
        'budgets':{'cpu_seconds':30,'wall_seconds':60},'new_finance_draws':0,'new_global_fixture_credit':0,
        'scope':'Independent finite arithmetic and hash audit; archived probability/source promises are assumptions, not re-certified.'}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'manifest.json').write_text(json.dumps({'author_sha256':sha(Path(__file__)),
        'verification_sha256':sha(OUT/'verification.json'),'input_pins':pins},indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['passed','feasible_candidates_directly_audited','stage_tail_checks','retained_cap_rejections','frozen_inputs_and_owned_hashes']}))

if __name__=='__main__': main()
