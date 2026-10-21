"""Outward rational covariance omission screen; no source imports or samples."""
import time
CPU_START = time.process_time()
import argparse
import functools
import hashlib
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

WALL_START = time.monotonic()
ROOT = Path(__file__).resolve().parents[3]
DOC = ROOT / "docs/independent_110_20261004/F23"
OUT = ROOT / "results/independent_110_20261004/F23/screen_run001"
FREEZE = DOC / "FREEZE.json"
SCALE = 1 << 120
CASE_RANKS = ((4,12,(24,36,47)), (8,52,(208,312,415)))
PATHS = [
    "docs/independent_110_20261004/F23/PROTOCOL.json",
    "docs/independent_110_20261004/F23/OMITTED_MODE_PROOF.md",
    "research/independent_110_20261004/F23/screen_covariance_compression.py",
    "docs/independent_110_20261004/inventory_run001/WORK_LIST.txt",
    "docs/limitation_audit_20261001/implementation_plan/roadmap.json",
    "docs/limitation_audit_20261001/implementation_plan/FORMULATIONS.md",
    "research/frontier_classical_20261001/basis.py",
    "manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md",
    "research/independent_110_20261004/F16/primary_sources/Sigman_2007_BM_GBM_I.pdf",
    "results/limitation_program_20261001/G0_run003/B4x12_task.json",
    "results/limitation_program_20261001/G0_run003/B8x52_task.json",
    "results/limitation_program_20261001/G0_run003/B4x12_error_ledger.json",
    "results/limitation_program_20261001/G0_run003/B8x52_error_ledger.json",
    "results/independent_110_20261004/E01/audit_run001/access_cards.json",
    "results/independent_110_20261004/E01/audit_run001/manifest.json",
]


def guard(admission=False):
    if time.process_time()-CPU_START > (60 if admission else 90) or time.monotonic()-WALL_START > 180:
        raise RuntimeError("Fixed F23 administrative CPU/wall budget exhausted")


def sha(path):
    guard()
    value=hashlib.sha256(path.read_bytes()).hexdigest()
    guard()
    return value


def read(path):
    guard()
    value=json.loads(path.read_text(encoding="utf-8-sig"))
    guard()
    return value


def down(v):
    v=Q(v)
    return Q((v.numerator*SCALE)//v.denominator,SCALE)


def up(v):
    return -down(-Q(v))


class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi=down(lo),up(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,o):
        o=o if isinstance(o,I) else I(o)
        return I(self.lo+o.lo,self.hi+o.hi)
    def __sub__(self,o):
        o=o if isinstance(o,I) else I(o)
        return I(self.lo-o.hi,self.hi-o.lo)
    def __mul__(self,o):
        o=o if isinstance(o,I) else I(o)
        v=[a*b for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return I(min(v),max(v))
    def __truediv__(self,o):
        o=o if isinstance(o,I) else I(o)
        assert o.lo>0 or o.hi<0
        return self*I(1/o.hi,1/o.lo)
    def square(self):
        return I(0 if self.lo<=0<=self.hi else min(self.lo*self.lo,self.hi*self.hi),max(self.lo*self.lo,self.hi*self.hi))
    def sqrt(self):
        assert self.lo>=0
        def root(v):
            k=math.isqrt((v.numerator*SCALE*SCALE)//v.denominator)
            return k
        a,b=root(self.lo),root(self.hi)
        return I(Q(a,SCALE),Q(b if Q(b,SCALE)**2==self.hi else b+1,SCALE))
    def pair(self):
        return {"lower_exact":[self.lo.numerator,self.lo.denominator],"upper_exact":[self.hi.numerator,self.hi.denominator]}


def atan_inverse(n,terms):
    partial=sum((Q((-1)**k,(2*k+1)*n**(2*k+1)) for k in range(terms)),Q(0))
    next_term=Q((-1)**terms,(2*terms+1)*n**(2*terms+1))
    return I(min(partial,partial+next_term),max(partial,partial+next_term))


def pi_interval():
    return atan_inverse(5,60)*16-atan_inverse(239,20)*4


@functools.lru_cache(maxsize=2048)
def sin_ratio(r):
    guard()
    r=r%2
    sign=1
    if r>1:
        sign=-1
        r-=1
    if r>Q(1,2):
        r=1-r
    if r==0:
        return I(0)
    x=PI*I(r)
    x2=x.square()
    term,total=x,x
    for k in range(1,32):
        term=(term*x2)/I((2*k)*(2*k+1))
        total=total-term if k%2 else total+term
    rem=Q(2**65,math.factorial(65))
    result=I(max(0,total.lo-rem),min(1,total.hi+rem))
    return result*sign


def exp_positive(x):
    assert 0<=x<=1
    xi,term,total=I(x),I(1),I(1)
    for k in range(1,33):
        term=(term*xi)/I(k)
        total=total+term
    tail=Q(x)**33/math.factorial(33)/(1-Q(x)/34)
    return I(total.lo,total.hi+tail)


def log_band(eta):
    z=Q(eta,140)
    assert 0<z<1
    term,total=I(z),I(0)
    for k in range(32):
        total=total+term/I(2*k+1)
        term=term*I(z*z)
    tail=2*z**65/(65*(1-z*z))
    return I((total*2).lo,(total*2).hi+tail)


def asset_square(asset,mode,na):
    if mode==0:
        return Q(1,na)
    if asset<mode:
        return Q(1,mode*(mode+1))
    if asset==mode:
        return Q(mode,mode+1)
    return Q(0)


def midpoint(v):
    return (v.lo+v.hi)/2


def case_screen(na,nt,ranks):
    global PI
    sigma2,rho=Q(9,100),Q(2,5)
    dt=Q(1,nt)
    asset_lam=[sigma2*(1+(na-1)*rho)]+[sigma2*(1-rho)]*(na-1)
    time_lam=[I(dt)/(sin_ratio(Q(2*k-1,2*(2*nt+1))).square()*4) for k in range(1,nt+1)]
    time_square=[[sin_ratio(Q((2*k-1)*j,2*nt+1)).square()*Q(4,2*nt+1) for k in range(1,nt+1)] for j in range(1,nt+1)]
    for asset in range(na):
        assert sum(asset_lam[a]*asset_square(asset,a,na) for a in range(na))==sigma2
    for j in range(nt):
        full=sum_intervals(time_lam[k]*time_square[j][k] for k in range(nt))
        assert full.lo<=Q(j+1,nt)<=full.hi
    modes=[(a,k,I(asset_lam[a])*time_lam[k]) for a in range(na) for k in range(nt)]
    modes.sort(key=lambda item:(-midpoint(item[2]),item[0],item[1]))
    for left,right in zip(modes,modes[1:]):
        same_exact=left[1]==right[1] and asset_lam[left[0]]==asset_lam[right[0]]
        if same_exact:
            assert (left[0],left[1])<(right[0],right[1])
        elif left[2].lo<right[2].hi:
            raise RuntimeError("UNRESOLVED exact covariance eigenvalue ordering")
    discount=I(1)/exp_positive(Q(3,100))
    rows=[]
    for rank in ranks:
        guard()
        assert 0<rank<na*nt
        omitted=modes[rank:]
        residual=[]
        deltas=[]
        for j in range(nt):
            residual_j=[sum_intervals(lam*asset_square(asset,a,na)*time_square[j][k] for a,k,lam in omitted) for asset in range(na)]
            residual.append(residual_j)
            delta=sum_intervals((v*2/PI).sqrt() for v in residual_j)/I(na)*100*exp_positive(Q(3*(j+1),100*nt))
            deltas.append(delta)
        diagonal_trace=sum_intervals(v for row in residual for v in row)
        omitted_trace=sum_intervals(lam for _,_,lam in omitted)
        assert max(diagonal_trace.lo,omitted_trace.lo)<=min(diagonal_trace.hi,omitted_trace.hi)
        call=discount*sum_intervals(deltas)/I(nt)
        date_total=sum_intervals(deltas)
        support=discount*40
        bands=[]
        for eta in (1,5,10):
            band_union=sum_intervals(log_band(eta)/(PI*2*sigma2*rho*Q(j+1,nt)).sqrt() for j in range(nt))
            switch=date_total/I(eta)+band_union
            switch_upper=min(Q(1),switch.hi)
            combined=discount*(sum_intervals(deltas)/I(nt)+I(40)*I(switch_upper))
            upper=min(support.hi,combined.hi)
            bands.append({"eta_dollars":eta,"original_band_union_upper_exact":[band_union.hi.numerator,band_union.hi.denominator],
                          "Markov_perturbation_upper_exact":[(date_total/I(eta)).hi.numerator,(date_total/I(eta)).hi.denominator],
                          "switch_probability_upper_exact":[switch_upper.numerator,switch_upper.denominator],
                          "knockout_dollar_upper_exact":[upper.numerator,upper.denominator]})
        best=min(Q(*b["knockout_dollar_upper_exact"]) for b in bands)
        rows.append({"case":f"B{na}x{nt}","rank":rank,"full_rank":na*nt,"contractual_dates_retained":nt,
                     "continuous_covariance_approximation":True,"original_drift_retained":True,
                     "omitted_trace":omitted_trace.pair(),"variance_residuals":[[v.pair() for v in row] for row in residual],
                     "call_coupling_dollar_upper_exact":[call.hi.numerator,call.hi.denominator],
                     "barrier_bound_cases":bands,"knockout_dollar_upper_exact":[best.numerator,best.denominator],
                     "isolated_allowance_exact":[1,1000],"bias_screen_pass":best<=Q(1,1000),
                     "changed_finite_law_bridge":None,"implemented_compressed_preparation":False,
                     "charged_quantum_ledger":None,"matched_classical_timing":None,
                     "advance_to_compilation":False,"decision":"BOUND_METHOD_DOES_NOT_CERTIFY_ALLOWANCE" if best>Q(1,1000) else "BIAS_BOUND_ONLY_PREPARATION_UNBUILT"})
    # Full rank is an identity, not an additional candidate rank.
    full_rank_omitted=modes[na*nt:]
    assert not full_rank_omitted
    full_zero=[sum_intervals(lam*asset_square(asset,a,na)*time_square[j][k]
                              for a,k,lam in full_rank_omitted)
               for j in range(nt) for asset in range(na)]
    assert all(v.lo==v.hi==0 for v in full_zero)
    assert sum_intervals((v*2/PI).sqrt() for v in full_zero).lo==0
    assert sum_intervals((v*2/PI).sqrt() for v in full_zero).hi==0
    return rows,{"marginal_time_variance_checks":nt,"asset_variance_identities":na,"rank_trace_checks":len(ranks),
                 "spectral_adjacent_checks":len(modes)-1,"full_rank_zero_identity":1,"fixed_barrier_cases":3*len(ranks)}


def sum_intervals(items):
    total=I(0)
    for value in items:
        total=total+value
    return total


def write(path,value,emergency=False):
    payload=(json.dumps(value,indent=2,sort_keys=True)+"\n").encode()
    if emergency:
        assert len(payload)<=16384
    else:
        guard()
        files=[p for p in OUT.iterdir() if p.is_file()]
        assert len(files)+1<=16 and sum(p.stat().st_size for p in files)+len(payload)+16384<=4194304
    with path.open("xb") as handle:
        handle.write(payload)
    if not emergency:
        guard()


def verify(freeze):
    assert set(freeze["inputs"])==set(PATHS)
    for name,pin in freeze["inputs"].items():
        assert (ROOT/name).stat().st_size==pin["bytes"] and sha(ROOT/name)==pin["sha256"],name
    for name,pin in freeze["selected_runtime"].items():
        assert sha(Path(name))==pin["sha256"]


def freeze():
    assert not FREEZE.exists() and not OUT.exists()
    assert len(PATHS)==len(set(PATHS))<=24
    pins={}
    for name in PATHS:
        path=ROOT/name
        assert path.stat().st_size<=2097152
        pins[name]={"sha256":sha(path),"bytes":path.stat().st_size}
    assert sum(p["bytes"] for p in pins.values())<=8388608
    runtime={str(p):{"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted(set([Path(sys.executable),Path(sys.base_prefix)/"python.exe"]),key=str)}
    with FREEZE.open("x",encoding="utf-8") as handle:
        json.dump({"schema":"f23-prospective-corpus-freeze-v1","inputs":pins,"selected_runtime":runtime,"science_started":False},handle,indent=2,sort_keys=True)
        handle.write("\n")
    print(json.dumps({"freeze_sha256":sha(FREEZE),"inputs":len(pins),"bytes":sum(p["bytes"] for p in pins.values())}))


def run(expected):
    global PI
    assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
    if OUT.exists():
        raise RuntimeError("Fresh F23 receipt required; no retries")
    OUT.mkdir(parents=True)
    marker=OUT/"FAILED_UNSEALED.json"
    write(marker,{"passed":False,"completed":False,"decision":"UNSEALED_FROM_START"},emergency=True)
    try:
        assert sha(FREEZE)==expected
        frozen=read(FREEZE)
        verify(frozen)
        guard(admission=True)
        write(OUT/"protocol.json",read(DOC/"PROTOCOL.json"))
        write(OUT/"run_started.json",{"freeze_sha256":expected,"source_imports":0,"financial_draws":0})
        PI=pi_interval()
        assert Q(3)<PI.lo<PI.hi<Q(22,7)
        rows,diagnostics=[],{}
        for na,nt,ranks in CASE_RANKS:
            task=read(ROOT/f"results/limitation_program_20261001/G0_run003/B{na}x{nt}_task.json")
            assert task["assets"]==na and task["dates"]==nt and task["annual_volatility_each_asset"]==.3 and task["equicorrelation"]==.4 and task["maturity_years"]==1
            current,counts=case_screen(na,nt,ranks)
            rows+=current
            diagnostics[f"B{na}x{nt}"]=counts
        assert len(rows)==6
        write(OUT/"rank_bounds.json",rows)
        write(OUT/"checks.json",{"passed":True,"pi_enclosure":PI.pair(),"dyadic_precision":120,"counts":diagnostics,
              "scope":"Population bound derived in proof; finite mapping/interval checks only, no simulations or gate replay"})
        write(OUT/"certificate.json",{"passed":True,"completed":True,"budget_censored":False,"F23_bounded_rank_screen_complete":True,
              "rank_rows":6,"any_bias_screen_pass":any(r["bias_screen_pass"] for r in rows),"any_implemented_preparation":False,
              "decision":"RETAIN_FULL_RANK_NO_ELIGIBLE_COMPRESSED_SOURCE","actual_bias_lower_bound":None,
              "changed_finite_law_certified":False,"financial_delivery_certified":False,"matched_timing":False,
              "new_global_fixture_credit":0,"new_gate_replay_credit":0,"new_samples":0,"source_adoption":False,"quantum_advantage":False})
        write(OUT/"comparison.json",{"scope":"Isolated compression allowance versus proved continuous-coupling upper certificate; not actual price error or runtime",
              "ranks":[{"case":r["case"],"rank":r["rank"],"dollar_upper_exact":r["knockout_dollar_upper_exact"],"pass":r["bias_screen_pass"]} for r in rows],
              "other_new_source_errors":None,"compressed_quantum_cost":None,"compressed_classical_cost":None,"source_adoption":False})
        verify(frozen)
        files={str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in OUT.iterdir() if p.is_file() and p!=marker}
        write(OUT/"manifest.json",{"passed":True,"completed":True,"budget_censored":False,"files":files,"frozen_inputs":frozen["inputs"],
              "selected_runtime":frozen["selected_runtime"],"freeze_sha256":expected,"runtime_scope":"Selected launcher/base interpreter only",
              "manifest_self_hash_excluded":True,"failure_marker_authoritative":True,"quantum_advantage":False,"new_global_fixture_credit":0})
        assert set(p.name for p in OUT.iterdir())=={"FAILED_UNSEALED.json","protocol.json","run_started.json","rank_bounds.json","checks.json","certificate.json","comparison.json","manifest.json"}
        guard()
        marker.unlink()
        print(json.dumps({"passed":True,"bias_pass_rows":sum(r["bias_screen_pass"] for r in rows),"manifest_sha256":sha(OUT/"manifest.json")}))
    except BaseException as exc:
        payload=(json.dumps({"passed":False,"completed":False,"decision":"FAILED_UNSEALED","type":type(exc).__name__,"message":str(exc)[:2048],
                             "budget_censored":"budget" in str(exc).lower(),"failure_marker_overrides_partial_PASS":True,"new_global_fixture_credit":0},indent=2)+"\n").encode()
        assert len(payload)<=16384
        marker.write_bytes(payload)
        raise


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=("freeze","run"))
    parser.add_argument("--freeze-sha256")
    args=parser.parse_args()
    if args.mode=="freeze":
        freeze()
    else:
        if not args.freeze_sha256:
            parser.error("run requires --freeze-sha256")
        run(args.freeze_sha256)
