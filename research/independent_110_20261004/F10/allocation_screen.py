"""One frozen metadata/accounting screen; never imports archived finance code."""
import argparse
import csv
import hashlib
import io
import itertools
import json
import math
import sys
import time
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOC = ROOT / 'docs/independent_110_20261004/F10'
OUT = ROOT / 'results/independent_110_20261004/F10/allocation_run001'
ARCH = ROOT / 'results/antithetic_feasibility'
PINS = [
    'docs/independent_110_20261004/F10/PROTOCOL.json',
    'docs/independent_110_20261004/F10/ALLOCATION_PROOF.md',
    'docs/independent_110_20261004/F10/PREPARATION_NOTES.json',
    'research/independent_110_20261004/F10/allocation_screen.py',
    'docs/independent_110_20261004/F10/primary_sources/Montanaro_1504_06987v3.pdf',
    'docs/antithetic_feasibility/PROTOCOL.md',
    'docs/antithetic_feasibility/RESULTS.md',
    'research/antithetic_feasibility/cost_model.py',
    'research/antithetic_feasibility/estimator.py',
    'research/antithetic_feasibility/classical.py',
    'research/antithetic_feasibility/multilevel.py',
    'research/antithetic_feasibility/hybrid_classical.py',
    'results/antithetic_feasibility/classical_prices_v1/summaries.json',
    'results/antithetic_feasibility/classical_corrections_v1/summaries.json',
    'results/antithetic_feasibility/complete_cost_screen_v1/oracle_plans.json',
    'results/antithetic_feasibility/complete_cost_screen_v1/costs.json',
    'results/antithetic_feasibility/compiled_blocks_v1/blocks.json',
    'results/antithetic_feasibility/compiled_blocks_v1/loaders.json',
    'results/antithetic_feasibility/hybrid_classical_v1/summaries.json',
    'results/antithetic_feasibility/hybrid_classical_v1/frozen_plans.json',
    'docs/independent_110_20261004/inventory_run001/WORK_LIST.txt',
    '.context/frontier_t0_env/Scripts/python.exe',
]
DELTA = F(1,1500)
SLOTS = 64
NMAX = 1 << 60
NULLS = {k: None for k in [
    'population_moment_certificate', 'centered_support_certificate',
    'continuous_bias_dollars', 'finite_input_bridge_dollars',
    'arithmetic_overflow_and_center_dollars', 'cap_dollars',
    'source_and_rotation_error_dollars', 'output_normalization_error_dollars',
    'source_and_inverse_complete_gate_cost', 'quantum_setup_seconds',
    'preprocessing_calibration_compilation_seconds', 'quantum_readout_decode_seconds',
    'classical_setup_complete_seconds', 'physical_execution_seconds',
    'physical_failure_bound', 'remaining_failure_bound', 'complete_price_seconds',
    'fastest_eligible_classical_total_seconds', 'mixed_unit_speedup'
]}


def q(x):
    if x is None or isinstance(x, bool):
        raise ValueError('missing/non-numeric input remains unresolved')
    return F(x)


def ceil(x):
    return -(-x.numerator // x.denominator)


def sqrt_up(x):
    if x < 0:
        raise ValueError('negative square root')
    scale = 1 << 64
    z = math.isqrt(x.numerator * scale * scale // x.denominator)
    if F(z*z, scale*scale) < x:
        z += 1
    return F(z, scale)


def load(path):
    return json.loads(path.read_text(encoding='utf-8'), parse_float=str)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(x):
    return (json.dumps(x, indent=2, sort_keys=True) + '\n').encode('utf-8')


def freeze():
    dest = DOC / 'FREEZE.json'
    assert not dest.exists(), 'freeze cannot be overwritten'
    paths = [ROOT / s for s in PINS] + [Path(sys._base_executable).resolve()]
    unique = list(dict.fromkeys(paths))
    assert len(unique) <= 32
    rows = [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': digest(p)} for p in unique]
    assert sum(r['bytes'] for r in rows) <= 8388608
    obj = {'item': 'F10', 'phase': 'prospective, no accounting run',
           'protocol_sha256': digest(DOC/'PROTOCOL.json'), 'inputs': rows,
           'input_scope': 'selected source/archives and launcher/base binaries only; no complete runtime closure',
           'output': str(OUT)}
    dest.write_bytes(dump(obj))
    print(json.dumps({'freeze_sha256': digest(dest), 'inputs': len(rows),
                      'bytes': sum(r['bytes'] for r in rows)}))


class Guard:
    def __init__(self):
        self.cpu = time.process_time()
        self.wall = time.monotonic()

    def elapsed(self):
        return {'cpu_seconds': time.process_time()-self.cpu,
                'wall_seconds': time.monotonic()-self.wall}

    def check(self):
        e = self.elapsed()
        if e['cpu_seconds'] > 120 or e['wall_seconds'] > 300:
            raise RuntimeError('fixed administrative CPU/wall cap')


def checked_sample(v, e):
    if v is None or e <= 0 or v <= 0:
        raise ValueError('positive assumed moment and error required')
    n = ceil(v / (DELTA*e*e))
    if n > NMAX:
        return None
    assert n >= 1 and v/(n*e*e) <= DELTA
    assert n == 1 or v/((n-1)*e*e) > DELTA
    return n


def make_dp(values, rates, h, slots, guard):
    table = {(0,b): (F(0), (0,)*len(values)) for b in range(slots+1)}
    options = [[None]+[checked_sample(v,k*h) for k in range(1,slots+1)] for v in values]
    comparisons = 0
    for mask in range(1, 1 << len(values)):
        j = (mask & -mask).bit_length()-1
        rest = mask ^ (1 << j)
        for b in range(slots+1):
            best = None
            for k in range(1,b+1):
                guard.check()
                previous = table[(rest,b-k)]
                n = options[j][k]
                if previous is None or n is None:
                    continue
                arr = list(previous[1]); arr[j] = k
                candidate = (previous[0]+rates[j]*n, tuple(arr))
                comparisons += 1
                if best is None or candidate < best:
                    best = candidate
            table[(mask,b)] = best
    return table, options, comparisons


TAIL_CACHE = {}


def majority(r):
    if r < 1 or r % 2 != 1:
        raise ValueError('odd positive repetitions required')
    if r not in TAIL_CACHE:
        p = F(23,121)
        TAIL_CACHE[r] = sum((F(math.comb(r,k))*p**k*(1-p)**(r-k)
                             for k in range(r//2+1,r+1)), F(0))
    return TAIL_CACHE[r]


def native(plan, schedule, v):
    bins = schedule['bins']; assert bins and len(bins)%2 == 0
    common_m = bins[0]['M']; hi0 = q(bins[0]['upper'])
    geometry_pass = hi0*hi0 >= v and hi0*hi0 <= 4*v
    previous = F(0)
    for i in range(0,len(bins),2):
        a,b = bins[i:i+2]
        assert a['sign'] == -1 and b['sign'] == 1
        assert q(a['lower']) == previous
        assert q(a['upper']) == q(b['upper']) and q(a['lower']) == q(b['lower'])
        assert q(a['upper']) > previous
        assert i == 0 or q(a['upper']) == 2*previous
        previous = q(a['upper'])
    assert previous == q(schedule['cutoff'])
    counts = dict(source_forward=0, source_inverse=0, reflection_zero=0,
                  reflection_good=0, qft_controlled_phases=0, qpe_readout_bits=0,
                  independent_qae_shots=0)
    failure = F(0)
    for b in bins:
        M,r,m = b['M'],b['repetitions'],b['qpe_qubits']
        assert type(M) is int and M > 0 and M & (M-1) == 0
        assert M == common_m and M == 1 << m
        assert b['calls_A'] == r*(2*M-1)
        assert b['grover_iterates'] == r*(M-1)
        assert b['qft_controlled_rotations'] == r*m*(m-1)//2
        counts['source_forward'] += r*M
        counts['source_inverse'] += r*(M-1)
        counts['reflection_zero'] += r*(M-1)
        counts['reflection_good'] += r*(M-1)
        counts['qft_controlled_phases'] += r*m*(m-1)//2
        counts['qpe_readout_bits'] += r*m
        counts['independent_qae_shots'] += r
        failure += majority(r)
    ca = counts['source_forward']+counts['source_inverse']
    g = counts['reflection_zero']
    assert ca == schedule['calls_A'] and g == schedule['grover_iterates']
    assert counts['qft_controlled_phases'] == schedule['qft_controlled_rotations']
    pi = F(22,7)
    tail = F(0) if q(schedule['cutoff']) >= 1024 else v/q(schedule['cutoff'])
    error = (tail+4*pi*sqrt_up(len(bins)*v)/common_m+pi*pi*sum(q(b['upper']) for b in bins)/(common_m**2)) if geometry_pass else None
    counts.update(t_count_excluding_rotation_synthesis=ca*plan['f_t_count']+g*plan['reflection_t_count'],
                  t_depth_serial_blocks_excluding_rotations=ca*plan['f_t_depth_serial']+g*plan['reflection_t_depth_serial'],
                  loader_u=ca*plan['loader_u'], loader_cx=ca*plan['loader_cx'],
                  arbitrary_rotation_upper_count=ca*plan['loader_arbitrary_rotation_upper_count']+3*counts['qft_controlled_phases'],
                  gaussian_preparations=ca*plan['gaussian_preparations'])
    return {'native': counts, 'conditional_error_upper': str(error) if error is not None else None,
            'conditional_tail_upper': str(tail), 'conditional_failure_upper': str(failure),
            'conditional_bin_geometry_pass': geometry_pass,
            'conditional_failure_pass': failure <= DELTA,
            'peak_logical_qubits_stored_history': plan['logical_qubits_stored_history'],
            'max_single_qpe_t_depth_serial_blocks': max((2*b['M']-1)*plan['f_t_depth_serial']+(b['M']-1)*plan['reflection_t_depth_serial'] for b in bins),
            'bins': len(bins), 'conditional_support_only': True,
            'emitted_monolithic_financial_source': False, 'complete_fields': NULLS}


def controls(guard):
    v = [F(1),F(2),F(3)]; rates = [F(1),F(2),F(1)]
    table,_,_ = make_dp(v,rates,F(1),5,guard)
    checks = 0
    for mask in range(8):
        for budget in range(6):
            best = None
            for slots in itertools.product(range(6),repeat=3):
                if sum(slots)>budget or any((s>0)!=bool(mask & (1<<j)) for j,s in enumerate(slots)):
                    continue
                cost = sum((rates[j]*checked_sample(v[j],F(s)) for j,s in enumerate(slots) if s),F(0))
                candidate = (cost,slots)
                if best is None or candidate < best: best = candidate
            assert table[(mask,budget)] == best
            checks += 1
    rejects = 0
    for action in [lambda:q(None),lambda:q(False),lambda:checked_sample(F(0),F(1)),
                   lambda:checked_sample(F(1),F(0)),lambda:majority(2),lambda:sqrt_up(F(-1))]:
        try: action()
        except ValueError: rejects += 1
        else: raise AssertionError('invalid control silently accepted')
    assert checked_sample(F(1),F(1,1<<64)) is None
    assert table[(7,2)] is None
    assert ceil(F(64,1)) == 64 and ceil(F(64)+F(1,1<<64)) == 65
    for x in [F(0),F(1),F(2),F(1,1<<160),F(10001,10000)]:
        z = sqrt_up(x); assert z*z>=x
        assert z == 0 or (z-F(1,1<<64))**2 < x
    return {'tiny_grid_bruteforce_states':checks,'invalid_input_rejections':rejects,
            'sample_cap_rejection':True,'insufficient_slots_rejection':True,
            'ceiling_boundaries':2,'sqrt_enclosure_boundaries':5,
            'global_fixture_credit':0}


def run(expected):
    guard = Guard()
    OUT.mkdir(parents=True,exist_ok=False)
    marker = OUT/'FAILED_UNSEALED.json'
    marker.write_bytes(dump({'item':'F10','status':'FAILED_UNSEALED','completed_checks':None,
                             'reason':'pending complete accounting and sealing'}))
    owned = {}
    def write(name,obj):
        guard.check()
        data = dump(obj) if not isinstance(obj,bytes) else obj
        total = sum((OUT/n).stat().st_size for n in owned)
        if len(owned)+1 > 10 or total+len(data)+65536+16384 > 8388608:
            raise RuntimeError('fixed output budget')
        p=OUT/name
        with p.open('xb') as stream: stream.write(data)
        owned[name]={'bytes':len(data),'sha256':digest(p)}
        guard.check()
    try:
        frozen = DOC/'FREEZE.json'
        assert digest(frozen)==expected
        pins = load(frozen)['inputs']
        assert len(pins)<=32 and sum(p['bytes'] for p in pins)<=8388608
        for p in pins:
            guard.check(); path=Path(p['path'])
            assert path.stat().st_size==p['bytes'] and digest(path)==p['sha256']
        assert load(DOC/'PROTOCOL.json')['allocation']['error_slots']==SLOTS
        if guard.elapsed()['cpu_seconds']>90: raise RuntimeError('fixed run admission guard')
        base=load(ARCH/'classical_prices_v1/summaries.json')
        corr=load(ARCH/'classical_corrections_v1/summaries.json')
        plans=load(ARCH/'complete_cost_screen_v1/oracle_plans.json')
        costs=load(ARCH/'complete_cost_screen_v1/costs.json')
        blocks=load(ARCH/'compiled_blocks_v1/blocks.json')
        loaders=load(ARCH/'compiled_blocks_v1/loaders.json')
        loader=next(x for x in loaders if x['qubits']==10)
        assert len(plans)==24 and len(costs)==12
        assert {(r['case'],r['fraction_bits'],q(r['epsilon'])) for r in costs}==set(itertools.product(['A1','A4'],[24,32],[F(1,10),F(3,100),F(1,100)]))
        inputs=[]; vals={}; rates={}; fits={}; pilots={}
        for case in ['A1','A4']:
            vals[case]=[]; rates[case]=[]
            for level in range(6):
                selected=[r for r in (base if level==0 else corr) if r['case']==case and r['level']==level and r['method']=='mc' and r['conditional'] is False and r['power']==(12 if level==0 else 10)]
                assert len(selected)==1; r=selected[0]; pilots[(case,level)]=r
                pilotmoment=4*(q(r['sample_variance'])+(q(r['mean'])**2 if level else 0))
                moments=[q(c['schedules'][level]['second_moment']) for c in costs if c['case']==case]
                working=max([pilotmoment]+moments); v=working+max(F(1),working)*F(1,1<<40)
                rate=(q(r['seconds'])-q(r['fit_seconds']))/(r['replicates']*(1<<r['power']))
                assert v>0 and rate>0
                vals[case].append(v); rates[case].append(rate)
                if level==0: fits[case]=q(r['fit_seconds'])
                inputs.append({'case':case,'level':level,'signed_correction':level>0,
                               'center':r['mean'] if level==0 else '0',
                               'pilot_mean':r['mean'],'pilot_sample_variance':r['sample_variance'],
                               'assumed_moment_upper':str(v),'population_moment_certificate':None,
                               'historical_iid_warm_seconds_per_path':str(rate),
                               'cost_model':'assumed linear extrapolation; not new measured/matched timing',
                               'pilot_power':r['power'],'pilot_replicates':r['replicates']})
        planmap={}
        for p in plans:
            guard.check(); key=(p['case'],p['fraction_bits'],p['level'])
            assert key not in planmap; planmap[key]=p
            for typ in ['t_count','t_depth_serial']:
                assert p['f_'+typ]==sum(e['multiplicity']*e[typ+'_each'] for e in p['entries'])
            w=p['fraction_bits']+16
            assert p['reflection_t_count']==14*(p['input_qubits']+w+1)
            assert p['reflection_t_depth_serial']==8*(p['input_qubits']+w+1)
            assert p['input_qubits']==10*p['gaussian_preparations']
            assert p['gaussian_preparations']==(2*(1 if p['case']=='A1' else 4)+1)*12*(1<<p['level'])
            assert p['loader_u']==p['gaussian_preparations']*loader['counts']['u']
            assert p['loader_cx']==p['gaussian_preparations']*loader['counts']['cx']
            assert p['loader_arbitrary_rotation_upper_count']==p['gaussian_preparations']*loader['arbitrary_rotation_upper_count']
            sqrtblock=next(b for b in blocks if b['fraction_bits']==p['fraction_bits'] and b['block']=='sqrt')
            assert p['sqrt_only_serial_depth_one_path']==12*(1<<p['level'])*sqrtblock['t_depth']
        ledgers=[]; bycost={}
        for c in costs:
            case,f,eps=c['case'],c['fraction_bits'],q(c['epsilon']); current=[]
            assert len(c['schedules'])==6
            for level,s in enumerate(c['schedules']):
                guard.check()
                assert q(s['center'])==(q(pilots[(case,0)]['mean']) if level==0 else 0)
                assert q(s['delta'])<=DELTA
                l=native(planmap[(case,f,level)],s,vals[case][level])
                l.update(case=case,fraction_bits=f,epsilon=str(eps),level=level)
                current.append(l); ledgers.append(l)
            for archkey,nativekey in [('source_invocations',None),('t_count_excluding_rotation_synthesis','t_count_excluding_rotation_synthesis'),('t_depth_serial_blocks_excluding_rotations','t_depth_serial_blocks_excluding_rotations'),('arbitrary_rotation_upper_count','arbitrary_rotation_upper_count')]:
                result=sum(l['native'][nativekey] if nativekey else l['native']['source_forward']+l['native']['source_inverse'] for l in current)
                assert result==c[archkey]
            assert max(l['max_single_qpe_t_depth_serial_blocks'] for l in current)==c['max_single_qpe_t_depth_serial_blocks']
            assert max(l['peak_logical_qubits_stored_history'] for l in current)==c['peak_logical_qubits_stored_history']
            bycost[(case,f,eps)]=current
        write('level_inputs.json',inputs)
        write('native_ledgers.json',ledgers)
        qa=controls(guard); rows=[]; comparisons=0
        for case in ['A1','A4']:
            for eps in [F(1,10),F(3,100),F(1,100)]:
                h=F(9,20)*eps/SLOTS
                table,options,ncomp=make_dp(vals[case],rates[case],h,SLOTS,guard)
                comparisons+=ncomp
                for f in [24,32]:
                    ls=bycost[(case,f,eps)]
                    for mask in range(64):
                        guard.check(); qs=[l for i,l in enumerate(ls) if mask & (1<<i)]
                        geometry_failures=[l['level'] for l in qs if not l['conditional_bin_geometry_pass']]
                        qslots=sum(ceil(q(l['conditional_error_upper'])/h) for l in qs) if not geometry_failures else None
                        cmask=63^mask
                        best=table.get((cmask,SLOTS-qslots)) if qslots is not None and qslots<=SLOTS else None
                        failures=[l['level'] for l in qs if not l['conditional_failure_pass']]
                        reason=('REJECT_QUANTUM_BIN_GEOMETRY' if geometry_failures else
                                'REJECT_QUANTUM_FAILURE_CAP' if failures else
                                'REJECT_FIXED_ERROR_GRID' if qslots>SLOTS else
                                'REJECT_CLASSICAL_SLOT_OR_SAMPLE_CAP' if best is None else
                                'CONDITIONAL_STATISTICAL_MODEL_ONLY')
                        allocation=list(best[1]) if best is not None else None
                        ns=[options[i][allocation[i]] if allocation[i] else None for i in range(6)] if allocation is not None else None
                        if allocation is not None:
                            assert qslots+sum(allocation)<=SLOTS
                            assert all(bool(k)==bool(cmask&(1<<i)) for i,k in enumerate(allocation))
                            assert best[0]==sum((rates[case][i]*n for i,n in enumerate(ns) if n is not None),F(0))
                        nv={k:sum(l['native'][k] for l in qs) for k in ls[0]['native']}
                        row={'case':case,'epsilon':str(eps),'fraction_bits':f,'quantum_mask':mask,
                             'classical_mask':cmask,'decision':reason,'quantum_failure_rejected_levels':failures,
                             'quantum_geometry_rejected_levels':geometry_failures,
                             'quantum_error_slots':qslots,'classical_error_slots':allocation,
                             'classical_iid_path_counts':ns,
                             'conditional_classical_sample_seconds_model':str(best[0]) if best is not None else None,
                             'historical_base_fit_seconds_anchor':str(fits[case]),
                             'conditional_classical_sample_plus_fit_seconds_model':str(best[0]+fits[case]) if best is not None else None,
                             'quantum_native':nv,'complete_fields':NULLS,
                             'joint_statistical_failure_cap':str(6*DELTA),
                             'joint_financial_99percent_eligible':False,'comparison_complete':False,
                             'analytic_coarse_mean':None,'full_limitation_complete':False}
                        if mask==0: assert all(v==0 for v in nv.values())
                        if mask==63 and allocation is not None: assert ns==[None]*6 and best[0]==0
                        rows.append(row)
        assert len(rows)==768 and len({(r['case'],r['epsilon'],r['fraction_bits'],r['quantum_mask']) for r in rows})==768
        write('hybrid_allocations.json',rows)
        text=io.StringIO(newline=''); writer=csv.writer(text)
        writer.writerow(['case','epsilon','fraction_bits','quantum_mask','decision','q_error_slots','c_error_slots','c_paths','conditional_c_sample_plus_fit_seconds','source_forward','source_inverse','native_t_count','native_serial_t_depth','physical_seconds','complete_seconds','eligible_99percent'])
        for r in rows:
            n=r['quantum_native']; writer.writerow([r['case'],r['epsilon'],r['fraction_bits'],r['quantum_mask'],r['decision'],r['quantum_error_slots'],r['classical_error_slots'],r['classical_iid_path_counts'],r['conditional_classical_sample_plus_fit_seconds_model'],n['source_forward'],n['source_inverse'],n['t_count_excluding_rotation_synthesis'],n['t_depth_serial_blocks_excluding_rotations'],'unresolved','unresolved','false'])
        write('hybrid_allocations.csv',text.getvalue().encode('utf-8'))
        floors=[]; hybrids=load(ARCH/'hybrid_classical_v1/summaries.json')
        frozenplans=load(ARCH/'hybrid_classical_v1/frozen_plans.json')
        assert len(hybrids)==len(frozenplans)==6
        for r in hybrids:
            guard.check()
            fp=[p for p in frozenplans if p['case']==r['case'] and q(p['epsilon'])==q(r['epsilon'])]
            assert len(fp)==1 and fp[0]['powers']==r['powers']
            total=q(r['seconds']); basecost=q(r['level_seconds'][0]); fit=q(r['fit_seconds'])
            assert len(r['level_seconds'])==len(r['level_means'])==6
            remaining=basecost+fit
            assert remaining>0 and remaining>total/10
            floors.append({'case':r['case'],'epsilon':str(q(r['epsilon'])),
                           'archived_total_warm_seconds':str(total),'base_only_warm_seconds':str(basecost),
                           'fit_warm_seconds':str(fit),'fixed_free_correction_remaining_warm_seconds':str(remaining),
                           'legacy_tenfold_budget_seconds':str(total/10),
                           'fixed_allocation_max_speedup_with_free_corrections':str(total/remaining),
                           'tenfold_rejected_under_legacy_fixed_cost_assumptions':True,
                           'financial_eligibility':False,'retuned_or_all_hybrid_no_go':False,
                           'broader_base_question':'F11'})
        write('fixed_base_floors.json',floors)
        qa.update(assignments=768,plans=24,schedules=72,whole_quantum_joins=12,
                  legacy_floor_rejections=6,conditional_dp_comparisons=comparisons)
        write('checks.json',qa)
        counts={s:sum(r['decision']==s for r in rows) for s in sorted({r['decision'] for r in rows})}
        summary={'item':'F10','status':'COMPLETE_BOUNDED_INITIAL_SCOPE','accounting':'PASS',
                 'assignment_counts':counts,'checks':qa,
                 'conditional_quantum_failure_pass_schedules':sum(l['conditional_failure_pass'] for l in ledgers),
                 'best_complete_hybrid':None,'compile_winner':False,'retain_archived_classical_and_antithetic_menu':True,
                 'legacy_fixed_hybrid_stop_rule_closed':True,'broader_base_question':'F11',
                 'analytic_coarse_mean_built':False,'complete_fields':NULLS,
                 'full_limitation_complete':False,'advantage':False,'global_fixture_credit':0,
                 'new_finance_acquisitions':0,'new_performance_measurements':0,
                 'administrative_elapsed':guard.elapsed()}
        write('summary.json',summary)
        for p in pins:
            guard.check(); path=Path(p['path'])
            assert path.stat().st_size==p['bytes'] and digest(path)==p['sha256']
        for name,info in owned.items():
            guard.check(); assert digest(OUT/name)==info['sha256']
        assert {p.name for p in OUT.iterdir()}==set(owned)|{marker.name}
        guard.check()
        mf={'item':'F10','status':'COMPLETE_UNCENSORED','freeze_sha256':expected,
            'owned':owned,'input_pins':pins,'administrative_elapsed':guard.elapsed(),
            'complete_runtime_closure':False,'financial_eligibility':False}
        data=dump(mf); assert len(data)<=49152
        assert sum((OUT/n).stat().st_size for n in owned)+len(data)+16384<=8388608
        with (OUT/'manifest.json').open('xb') as stream: stream.write(data)
        guard.check(); mfsha=digest(OUT/'manifest.json'); guard.check()
        marker.unlink()
        print(json.dumps({'status':'PASS','manifest_sha256':mfsha,'counts':counts,
                          'administrative_elapsed':guard.elapsed()}))
    except BaseException as error:
        data=dump({'item':'F10','status':'FAILED_UNSEALED','completed_checks':None,
                   'error_type':type(error).__name__,'error':str(error)[:4000],
                   'administrative_elapsed':guard.elapsed(),'financial_eligibility':False})
        assert len(data)<16384
        marker.write_bytes(data)
        raise


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['freeze','run'])
    parser.add_argument('--freeze-sha256')
    args=parser.parse_args()
    if args.mode=='freeze': freeze()
    else:
        if not args.freeze_sha256: parser.error('run requires exact prospective freeze SHA')
        run(args.freeze_sha256)
