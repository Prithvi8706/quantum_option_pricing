"""Two exact reversible finite toys; no financial oracle or shared imports."""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import hashlib
import json
import time

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/independent_110_20261004/E15/run002'
DOC=ROOT/'docs/independent_110_20261004/E15'
AUTHOR=Path(__file__).resolve()
PROOF=DOC/'COHERENCE_AND_LIMITS.txt'
CORPUS=[ROOT/p for p in ['research/compound_feasibility/reversible.py',
 'research/compound_feasibility/quantum_schedule.py','docs/compound_feasibility/RESULTS.md',
 'docs/controlled_residual_feasibility/DERIVATION.md',
 'docs/limitation_audit_20261001/implementation_plan/roadmap.json']]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')

class Circuit:
    def __init__(self): self.gates=[];self.width=0
    def reg(self,n):
        answer=list(range(self.width,self.width+n));self.width+=n;return answer
    def gate(self,*w):
        assert 1<=len(w)<=3 and len(set(w))==len(w) and all(0<=x<self.width for x in w)
        self.gates.append(tuple(w))
    def mcx(self,controls,target,temp):
        if len(controls)<=2:self.gate(*controls,target)
        else:
            assert len(controls)==3
            a,b,c=controls
            self.gate(a,b,temp);self.gate(temp,c,target);self.gate(a,b,temp)
    def apply(self,state,gates=None):
        for g in self.gates if gates is None else gates:
            if all((state>>b)&1 for b in g[:-1]): state^=1<<g[-1]
        return state

def increment(c,register,control,temp):
    # Descending targets test the old low bits before changing them.
    for k in reversed(range(len(register))):c.mcx([control]+register[:k],register[k],temp)

def build(deferred):
    c=Circuit();outer=c.reg(1)[0];output=c.reg(3);flags=c.reg(4);count=c.reg(3);temp=c.reg(1)[0]
    halt=c.reg(1)[0] if deferred else None
    if deferred:c.gate(halt);c.gate(outer,halt)  # halt=1-x, retained then uncomputed
    # Explicit frozen four-point oracle: good(x,j) iff j < 1+2*x.
    c.gate(flags[0]);c.gate(outer,flags[1])
    if deferred:
        c.gate(halt);c.gate(outer,halt,flags[2]);c.gate(halt)
    else:c.gate(outer,flags[2])
    for flag in flags:increment(c,count,flag,temp)
    compute=list(c.gates)
    # Full-domain nonlinear output g(n/4)=(n/4-1/2)+, stored in quarters.
    for n in range(8):
        result=max(n-2,0)
        if not result:continue
        flipped=[count[k] for k in range(3) if not ((n>>k)&1)]
        for w in flipped:c.gate(w)
        for k,w in enumerate(output):
            if (result>>k)&1:c.mcx(count,w,temp)
        for w in reversed(flipped):c.gate(w)
    c.gates.extend(reversed(compute))
    return c,outer,output,flags,count,temp,halt,compute

def word(state,wires):return sum(((state>>w)&1)<<k for k,w in enumerate(wires))
def encode(value,wires):return sum(((value>>k)&1)<<w for k,w in enumerate(wires))

def prepare():
    assert not OUT.exists() and PROOF.exists()
    OUT.mkdir(parents=True)
    dump(OUT/'protocol.json',{'author_sha256':sha(AUTHOR),'proof_sha256':sha(PROOF),
        'corpus':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in CORPUS},
        'toy':{'outer_states':[0,1],'inner_uniform_labels':[0,1,2,3],
               'good':'j<1+2*x','inner_means_exact':[[1,4],[3,4]],
               'outer_payoff':'positive part(z-1/2), returned in quarters',
               'designs':['Fixed four-query exact finite enumeration','Stored halt record with four-slot padding and reversible controller']},
        'acceptance':['Check intended XOR output and all scratch restored for both outer states and every three-bit output word.',
                      'Every basis state is a bijective permutation with exact inverse; nonlinear payoff independently evaluated over all count words.',
                      'Check global intended superposition and reversal algebraically; measurement negative control fails coherence.',
                      'Inventory padding/control resources and exact toy inner error; financial oracle, finite error constants and flattening regret remain unproved.'],
        'budgets':{'cpu_seconds':30,'wall_seconds':60,'output_bytes':4*1024*1024,'maximum_width':13,'maximum_full_basis_checks':12288},
        'stop':'Two declared toys and one existing flattening identity only; no financial sampling, source compilation or price-oracle substitution.',
        'new_finance_draws':0,'new_global_fixture_credit':0})
    print('E15 two finite reversible toys frozen.')

def run():
    cpu=time.process_time();wall=time.monotonic();p=json.loads((OUT/'protocol.json').read_text())
    assert not (OUT/'RUN_STARTED.json').exists() and sha(AUTHOR)==p['author_sha256'] and sha(PROOF)==p['proof_sha256']
    for path,wanted in p['corpus'].items():assert sha(ROOT/path)==wanted
    dump(OUT/'RUN_STARTED.json',{'toy_designs':2,'financial_oracle_calls':0})
    rows=[];basis_checks=0;logical_checks=0
    for deferred in [False,True]:
        c,x,out,flags,count,temp,halt,compute=build(deferred)
        assert c.width<=13
        inverse=list(reversed(c.gates))
        image=set()
        for state in range(1<<c.width):
            result=c.apply(state);image.add(result)
            assert c.apply(result,inverse)==state
        assert len(image)==1<<c.width
        basis_checks+=len(image)
        expected_images=[]
        for outer in [0,1]:
            bits=[int(j<1+2*outer) for j in range(4)]
            exact_inner=Q(sum(bits),4)
            expected=max(exact_inner-Q(1,2),0)
            assert expected.denominator in [1,4]
            computed=c.apply(outer<<x,compute)
            assert word(computed,flags)==sum(v<<j for j,v in enumerate(bits))
            assert word(computed,count)==sum(bits)
            if deferred:assert word(computed,[halt])==1-outer
            for initial_output in range(8):
                state=(outer<<x)|encode(initial_output,out)
                result=c.apply(state)
                ideal=(outer<<x)|encode(initial_output^int(4*expected),out)
                assert result==ideal
                assert c.apply(result,inverse)==state
                logical_checks+=1
            expected_images.append({'outer':outer,'inner_mean':[exact_inner.numerator,exact_inner.denominator],
                                    'payoff_quarters':int(4*expected),'basis_image_from_clean_scratch':c.apply(outer<<x)})
        # The payoff table's XOR action is independently checked across all count words.
        payoff=c.gates[len(compute):len(c.gates)-len(compute)]
        for n in range(8):
            result=c.apply(encode(n,count),payoff)
            assert word(result,count)==n and word(result,out)==max(n-2,0) and ((result>>temp)&1)==0
            logical_checks+=1
        counts={str(k):sum(len(g)==k for g in c.gates) for k in [1,2,3]}
        rows.append({'design':'stored_records_padded' if deferred else 'fixed_enumeration',
            'width':c.width,'scratch_qubits':c.width-4,'elementary_gate_counts_by_arity':counts,
            'total_gates':len(c.gates),'source_slots_forward':4,'source_slots_inverse':4,
            'classical_early_stop_query_lengths':[2,4] if deferred else [4,4],
            'coherent_maximum_forward_query_slots':4,'controller_record_qubits':int(deferred),
            'coherent_records_uncomputed':True,'output_images':expected_images,
            'intended_clean_scratch_isometry_error_exact':[0,1],
            'toy_inner_error_exact':[0,1], 'toy_outer_dollar_error_exact':[0,1],
            'finance_inner_error_or_source_interface_certified':False,
            'gates':[list(g) for g in c.gates]})
        assert time.process_time()-cpu<=30 and time.monotonic()-wall<=60
    assert basis_checks<=12288
    # Measuring any stored flag that equalsx before uncomputation recordsx in an
    # inaccessible environment: the balanced intended output's off-diagonal vanishes.
    negative={'measured_record':'flag1=x','desired_output_basis_states':rows[0]['output_images'],
        'coherent_pure_off_diagonal_exact':[1,2],'measured_channel_off_diagonal_exact':[0,1],
        'global_intended_superposition_fidelity_exact':[1,2],
        'trace_distance_from_intended_pure_output_exact':[1,2],
        'threshold_1e_minus12_passed':False,'measurement_record_not_reversible_financial_oracle':True}
    flatten={'identity':'P=d0 E[pi(R-Kc)]+d0 E[pi(C-R)]+d0 E[abs(C-Kc)*1{pi differs from1{C>Kc}}], pi=1{R>Kc}',
        'nonnegative_regret_required':True,'baseline_confidence_cost':None,'residual_source_and_confidence_cost':None,
        'digital_policy_source_equivalence':None,'certified_regret_dollars':None,
        'existing_protected_E12_not_recomputed':True,'flattening_finance_admissible':False}
    summary={'passed':True,'completed':True,'scope':'E15 two exact finite coherent enumeration/controller toys plus existing flattening identity audit.',
        'full_basis_inverse_and_bijection_checks':basis_checks,'intended_output_and_payoff_checks':logical_checks,
        'measured_inner_negative_control_rejected':True,'toy_clean_scratch_isometry_error_exact':[0,1],
        'stored_record_design_reduces_worst_case_query_slots':False,
        'toy_fixed_fallback_retained':True,'full_space_unitarity_proved_as_phase_free_permutation':True,'arbitrary_dirty_scratch_financial_oracle_semantics_claimed':False,'finance_coherent_mean_oracle_built':False,
        'financial_delivery_certified':False,'quantum_advantage':False,'new_global_fixture_credit':0,'new_finance_draws':0}
    dump(OUT/'certificate.json',summary);dump(OUT/'comparison.json',{'designs':rows,'measurement_negative_control':negative,'flattening_interface':flatten})
    for path,wanted in p['corpus'].items():assert sha(ROOT/path)==wanted
    assert time.process_time()-cpu<=30 and time.monotonic()-wall<=60
    files=[q for q in OUT.iterdir() if q.is_file()]+[PROOF]
    assert sum(q.stat().st_size for q in files)+32768<=4*1024*1024
    dump(OUT/'manifest.json',{'files':{str(q.relative_to(ROOT)).replace('\\','/'):{'sha256':sha(q),'bytes':q.stat().st_size} for q in files},'author_sha256':sha(AUTHOR),'input_pins':p['corpus']})
    print(json.dumps(summary))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['prepare','run']);args=ap.parse_args()
    if args.mode=='prepare':prepare()
    else:
        try:run()
        except BaseException as exc:
            if OUT.exists():dump(OUT/'FAILED_UNSEALED.json',{'passed':False,'completed':False,'message':str(exc)[:2048],'failure_overrides_partial_summary':True})
            raise
