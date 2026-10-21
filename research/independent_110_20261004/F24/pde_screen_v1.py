"""Two frozen D1 development grids; diagnostics, no continuum-bias certificate."""
import argparse
import ast
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
OWN='research/independent_110_20261004/F24'
OUT=ROOT/'results/independent_110_20261004/F24/run001'
INPUTS=['research/release_checks/targets.py','research/journal_sprint/asian_basket.py',
        'research/journal_sprint/run_minimal_pivot_week2.py',
        OWN+'/primary_sources/Miyamoto_Kubo_2109_12896v1.html',OWN+'/pde_screen_v1.py',
        'docs/independent_110_20261004/F24/FORMULATION_run001.txt']
CAPS=dict(cpu_seconds=10,wall_seconds=30,input_bytes=4*1024**2,output_bytes=2*1024**2,output_files=16)
D1=dict(id='D1',split='development',assets=1,dates=2,sigma=.2,strike=95.,correlation=.3)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def write(name,data):
    p=OUT/name
    if p.exists():raise ValueError('Refuse overwrite')
    p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def prepare():
    if OUT.exists():raise ValueError('Fresh output required')
    corpus=[dict(path=p,bytes=(ROOT/p).stat().st_size,sha256=sha((ROOT/p).read_bytes())) for p in INPUTS]
    size=sum(r['bytes'] for r in corpus)
    if size>CAPS['input_bytes']:raise ValueError('Input cap')
    OUT.mkdir(parents=True)
    write('protocol.json',dict(corpus=corpus,corpus_bytes=size,budgets=CAPS,D1=D1,spot=100.,rate=.03,maturity=1.,
        dates_exact=[[1,2],[1,1]],grids=[17,33],log_spot_ratio_domain=[-2,2],sum_average_domain=[0,95],
        total_implicit_steps=64,remaining_ITM_branch_exact=True,numpy=np.__version__,
        new_barrier_numerical_contracts=0,acceptance='Finite diagnostics only; no error/runtimes transferred',
        stop='Two fixed grids then close incomplete quantum transfer',matched_timings=False))
    print(json.dumps(dict(prepared=True,files=len(corpus),bytes=size,protocol_sha256=sha((OUT/'protocol.json').read_bytes()))))

def archived_contract():
    t=ast.parse((ROOT/'research/release_checks/targets.py').read_text())
    # Parse data constructors statically; never import/execute project code.
    assignment=next(n for n in t.body if isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='CASES' for a in n.targets))
    call=assignment.value.elts[0]
    if not isinstance(call,ast.Call) or not isinstance(call.func,ast.Name) or call.func.id!='dict':raise ValueError('D1 declaration shape')
    case={kw.arg:ast.literal_eval(kw.value) for kw in call.keywords}
    if case!=D1:raise ValueError('Original D1 changed')
    b=ast.parse((ROOT/'research/journal_sprint/asian_basket.py').read_text())
    cls=next(n for n in b.body if isinstance(n,ast.ClassDef) and n.name=='Basket')
    defaults={n.target.id:ast.literal_eval(n.value) for n in cls.body if isinstance(n,ast.AnnAssign) and n.value is not None}
    if any(defaults[k]!=v for k,v in {'spot':100.,'rate':.03,'maturity':1.}.items()):raise ValueError('D1 default changed')

def grid(N,guard):
    x=np.linspace(-2,2,N);q=np.linspace(0,95,N);s=100*np.exp(x);h=F(4,N-1);dt=F(1,64)
    r=F(.03);diff=F(.2)**2/2;mu=r-diff
    left=diff/h**2-mu/(2*h);right=diff/h**2+mu/(2*h)
    diagonal=1+dt*(2*diff/h**2+r)
    dominance=diagonal-dt*(left+right)
    if min(left,right)<0 or dominance!=1+dt*r:raise ValueError('M-matrix premises failed')
    n=N-2
    M=np.eye(n)*float(diagonal)+np.diag(np.full(n-1,-float(dt*left)),-1)+np.diag(np.full(n-1,-float(dt*right)),1)
    cond_bound=(1+dt*(r+4*diff/h**2))/(1+dt*r)
    # Initial post-final-fixing payoff for q in [0,K], exact zero.
    V=np.zeros((N,N))
    times=[.5,1.]
    def linear(t,q_values,s_value,remaining):
        return math.exp(-.03*(1-t))*(q_values-95)+s_value/2*sum(math.exp(-.03*(1-times[l])) for l in remaining)
    for j in (1,0):
        date=times[j]
        # Date event BEFORE uses continuation AFTER, so remaining dates are l>j.
        updated=np.empty_like(V)
        for i in range(N):
            shifted=q+s[i]/2
            updated[i]=np.interp(shifted,q,V[i])
            mask=shifted>=95
            updated[i,mask]=linear(date,shifted[mask],s[i],range(j+1,2))
        V=updated
        for step in range(32):
            t=date-(step+1)/64
            # Both finite-X boundary values are assumed approximations.
            upper=linear(t,q,s[-1],range(j,2))
            rhs=V[1:-1].copy()
            rhs[-1]+=float(dt*right)*upper
            V[1:-1]=np.linalg.solve(M,rhs)
            V[0]=0;V[-1]=upper
            V[:,-1]=linear(t,np.array([95.]),s,range(j,2))
            guard()
    if not np.isfinite(V).all() or float(V.min())<-1e-8:raise ValueError('Grid numerical positivity/finite check failed')
    price=float(V[N//2,0]);norm=float(np.linalg.norm(V))
    if not norm>0:raise ValueError('Zero price-vector norm')
    path=OUT/f'grid_{N}.npz'
    if path.exists():raise ValueError('Refuse grid overwrite')
    np.savez(path,x=x,q=q,values=V,implicit_interior_matrix=M)
    return dict(Nx=N,Nq=N,full_grid_values=N*N,interior_matrix_dimension=n,
        sparse_block_generator_nonzeros=N*(3*n-2),maximum_row_sparsity=3,
        event_interpolation_max_neighbors=2,implicit_steps=64,date_updates=2,
        condition2_diagnostic=float(np.linalg.cond(M)),condition_inf_upper_exact=[cond_bound.numerator,cond_bound.denominator],
        inverse_inf_norm_upper_exact=[dominance.denominator,dominance.numerator],
        off_diagonal_rates_exact=[[left.numerator,left.denominator],[right.numerator,right.denominator]],
        price_grid_diagnostic=price,vector_L2_norm_diagnostic=norm,target_amplitude_diagnostic=price/norm,
        target_probability_diagnostic=(price/norm)**2,minimum_grid_value_diagnostic=float(V.min()),
        grid_time_boundary_event_bias_upper=None,numerical_enclosure=None,
        quantum_matrix_access_cost=None,quantum_event_update_cost=None,normalized_solution_state_cost=None,
        scalar_price_extraction_cost=None,eligible_measured_classical_time=None,optimistic_complete_quantum_time=None,
        classical_reference_with_certified_bias=False,original_B4_B8_validated=False)

def run():
    if (OUT/'ATTEMPT.json').exists():raise ValueError('One invocation only')
    p=json.loads((OUT/'protocol.json').read_text());cpu=time.process_time();wall=time.monotonic()
    write('ATTEMPT.json',dict(status='STARTED',kind='fixed_two_grid_development_diagnostics'))
    def guard():
        if time.process_time()-cpu>CAPS['cpu_seconds'] or time.monotonic()-wall>CAPS['wall_seconds']:raise ValueError('Budget cap')
    try:
        if p['budgets']!=CAPS or p['grids']!=[17,33] or p['D1']!=D1 or np.__version__!=p['numpy']:raise ValueError('Frozen protocol changed')
        for rec in p['corpus']:
            raw=(ROOT/rec['path']).read_bytes()
            if len(raw)!=rec['bytes'] or sha(raw)!=rec['sha256']:raise ValueError('Frozen input changed')
        archived_contract()
        # Exact event-order accounting controls; no path samples.
        for a,b in [(F(80),F(90)),(F(190),F(10)),(F(95),F(95))]:
            q=a/2;q+=b/2
            if q!=(a+b)/2:raise ValueError('Discrete average changed')
        controls=dict(no_time0_fixing=True,terminal_after_second_fixing=True,
            continuous_average_drift_rejected=True,continuous_barrier_absorption_rejected=True,
            D1_has_no_barrier=True,coarse_fine_difference_is_not_bias_bound=True)
        rows=[grid(N,guard) for N in (17,33)]
        summary=dict(status='PASS_D1_FORMULATION_AND_TWO_GRID_DIAGNOSTICS_ONLY',contract=D1,
            rows=rows,controls=controls,grid_price_change_diagnostic=abs(rows[0]['price_grid_diagnostic']-rows[1]['price_grid_diagnostic']),
            continuum_price_bias_upper=None,barrier_numerical_workloads=0,barrier_extension_formal_only=True,
            theorem_transfer='Miyamoto/Kubo v1 derivative, matrix-access, norm and event premises unresolved',
            full_F24_acceptance=False,full_source_credit=False,quantum_compilations=0,matched_timings=0,
            price_delivery_or_quantum_advantage_claimed=False)
        write('summary.json',summary);guard();write('SUCCESS.json',dict(status=summary['status'],full_F24_acceptance=False))
        files=[a for a in OUT.iterdir() if a.is_file()]
        manifest=dict(files=[dict(path=a.name,bytes=a.stat().st_size,sha256=sha(a.read_bytes())) for a in sorted(files)])
        if len(files)+1>CAPS['output_files'] or sum(a.stat().st_size for a in files)+len(json.dumps(manifest).encode())>CAPS['output_bytes']:raise ValueError('Output cap')
        write('manifest.json',manifest)
        print(json.dumps(dict(status=summary['status'],prices=[r['price_grid_diagnostic'] for r in rows],summary_sha256=sha((OUT/'summary.json').read_bytes()))))
    except BaseException as exc:
        if not (OUT/'FAILED.json').exists():write('FAILED.json',dict(status='FAILED_PRESERVED',error=str(exc)))
        raise

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','run']);args=a.parse_args()
    prepare() if args.mode=='prepare' else run()
