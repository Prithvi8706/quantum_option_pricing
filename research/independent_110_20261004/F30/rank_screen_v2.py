"""Frozen D1 two-core TT fit diagnostics; no timing or quantum implementation."""
import argparse
import ast
import hashlib
import json
import math
import sys
from pathlib import Path
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
OWN='research/independent_110_20261004/F30'
OUT=ROOT/'results/independent_110_20261004/F30/run002'
DATA=ROOT/(OWN+'/corpus_run002')
INPUTS=['research/release_checks/targets.py','research/journal_sprint/asian_basket.py',
        OWN+'/primary_sources/Sakurai_Takahashi_Miyamoto_2405_00701v1.html',OWN+'/rank_screen_v2.py',
        'docs/independent_110_20261004/F30/ASSUMPTIONS_run002.txt',OWN+'/corpus_run002/fixed_data.npz']
CAPS=dict(cpu_seconds=10,wall_seconds=30,input_bytes=4*1024**2,output_bytes=2*1024**2,output_files=16,
          integrand_evaluations=1601,validation_normal_pairs=2048)
D1=dict(id='D1',split='development',assets=1,dates=2,sigma=.2,strike=95.,correlation=.3)

def sha(x):return hashlib.sha256(x).hexdigest()
def write(name,data):
    p=OUT/name
    if p.exists():raise ValueError('Refuse overwrite')
    p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')

def check_environment():
    expected=ROOT/'.context/frontier_t0_env/Scripts/python.exe'
    if np.__version__!='2.0.2' or sys.version_info[:3]!=(3,12,4) or Path(sys.executable).resolve()!=expected.resolve():raise ValueError('Use frozen explicit project launcher')

def prepare():
    check_environment()
    if OUT.exists() or DATA.exists():raise ValueError('Fresh data/output required')
    OUT.mkdir(parents=True);DATA.mkdir(parents=True)
    try:
        # Metadata/data creation only: no payoff evaluations or model fitting.
        z,w=np.polynomial.legendre.leggauss(33);z*=4;w*=4
        w*=np.exp(-z*z/2)/math.sqrt(2*math.pi)
        rng=np.random.default_rng(2026100430);blocks=[];draws=0
        while sum(len(b) for b in blocks)<512 and draws<2048:
            raw=rng.normal(size=(512,2));draws+=512
            blocks.append(raw[(np.abs(raw)<=4).all(axis=1)])
        accepted=np.vstack(blocks)
        if len(accepted)<512:raise ValueError('Prospective validation draw budget exceeded')
        validation=accepted[:512]
        if np.any(np.isin(validation[:,0],z)&np.isin(validation[:,1],z)):raise ValueError('Training-validation collision')
        np.savez(DATA/'fixed_data.npz',nodes=z,weights=w,validation_normals=validation)
        corpus=[dict(path=p,bytes=(ROOT/p).stat().st_size,sha256=sha((ROOT/p).read_bytes())) for p in INPUTS]
        size=sum(r['bytes'] for r in corpus)
        if size>CAPS['input_bytes']:raise ValueError('Input cap')
        write('protocol.json',dict(corpus=corpus,corpus_bytes=size,budgets=CAPS,contract=D1,
            ranks=[2,4,8],training_shape=[33,33],training_targets=1089,validation_targets=512,
            validation_seed=2026100430,validation_raw_pairs_drawn=draws,validation_distribution='Gaussian conditioned on [-4,4]^2',
            training_quadrature='unnormalized truncated Gaussian Gauss-Legendre',n_svd=1,
            interpolation='linear per core, constant endpoint extrapolation',numpy=np.__version__,
            python=sys.version.split()[0],executable=str(Path(sys.executable).resolve()),
            preflight_lineage='run001 retained without payoff/SVD: default launcher mismatch',
            no_F03_transform=True,training_payoffs_already_evaluated=0,
            acceptance='Finite rank/contraction diagnostics only, no integral or price certificate',
            stop='Exactly3 ranks then close uncertified quantum loader; no timing/adoption'))
        print(json.dumps(dict(prepared=True,files=len(corpus),bytes=size,protocol_sha256=sha((OUT/'protocol.json').read_bytes()))))
    except BaseException as exc:
        if not (OUT/'PREPARE_FAILED.json').exists():write('PREPARE_FAILED.json',dict(status='FAILED_PRESERVED',error=str(exc)))
        raise

def bind_contract():
    tree=ast.parse((ROOT/'research/release_checks/targets.py').read_text())
    n=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='CASES' for a in n.targets))
    data={kw.arg:ast.literal_eval(kw.value) for kw in n.value.elts[0].keywords}
    if data!=D1:raise ValueError('D1 changed')
    tree=ast.parse((ROOT/'research/journal_sprint/asian_basket.py').read_text())
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Basket')
    defaults={n.target.id:ast.literal_eval(n.value) for n in cls.body if isinstance(n,ast.AnnAssign) and n.value is not None}
    if any(defaults[k]!=v for k,v in {'spot':100.,'rate':.03,'maturity':1.}.items()):raise ValueError('D1 defaults changed')

def existing_PCA_map():
    times=np.linspace(.5,1.,2)
    asset_cov=(1-.3)*np.eye(1)+.3
    cov=.2**2*np.kron(asset_cov,np.minimum.outer(times,times))
    vals,vecs=np.linalg.eigh(cov);order=np.argsort(vals)[::-1]
    factor=vecs[:,order]*np.sqrt(np.maximum(vals[order],0))
    for j in range(factor.shape[1]):
        if factor[np.argmax(np.abs(factor[:,j])),j]<0:factor[:,j]*=-1
    means=math.log(100)+(.03-.2**2/2)*times
    if not np.allclose(factor@factor.T,cov,rtol=0,atol=1e-14):raise ValueError('PCA reconstruction diagnostic failed')
    return means,factor,cov

def run():
    check_environment()
    if (OUT/'ATTEMPT.json').exists():raise ValueError('One invocation only')
    p=json.loads((OUT/'protocol.json').read_text());cpu=time.process_time();wall=time.monotonic();evaluations=0
    write('ATTEMPT.json',dict(status='STARTED',kind='fixed_three_rank_development_fit'))
    def guard():
        if time.process_time()-cpu>CAPS['cpu_seconds'] or time.monotonic()-wall>CAPS['wall_seconds']:raise ValueError('Budget cap')
        if evaluations>CAPS['integrand_evaluations']:raise ValueError('Evaluation cap')
    try:
        if p['python']!=sys.version.split()[0] or p['executable']!=str(Path(sys.executable).resolve()):raise ValueError('Prepared launcher changed')
        if p['budgets']!=CAPS or p['ranks']!=[2,4,8] or np.__version__!=p['numpy'] or p['contract']!=D1:raise ValueError('Protocol changed')
        if [r['path'] for r in p['corpus']]!=INPUTS or p['corpus_bytes']!=sum(r['bytes'] for r in p['corpus']) or p['corpus_bytes']>CAPS['input_bytes']:raise ValueError('Frozen corpus membership changed')
        if p['training_shape']!=[33,33] or p['training_targets']!=1089 or p['validation_targets']!=512 or p['n_svd']!=1 or p['validation_seed']!=2026100430:raise ValueError('Prescribed fit changed')
        if not 512<=p['validation_raw_pairs_drawn']<=CAPS['validation_normal_pairs'] or p['validation_raw_pairs_drawn']%512:raise ValueError('Validation draw accounting changed')
        for r in p['corpus']:
            raw=(ROOT/r['path']).read_bytes()
            if len(raw)!=r['bytes'] or sha(raw)!=r['sha256']:raise ValueError('Frozen input changed')
        bind_contract();means,factor,cov=existing_PCA_map()
        with np.load(DATA/'fixed_data.npz',allow_pickle=False) as fixed:
            z=fixed['nodes'].copy();w=fixed['weights'].copy();validation=fixed['validation_normals'].copy()
        if z.shape!=(33,) or w.shape!=(33,) or validation.shape!=(512,2) or not np.all(w>0):raise ValueError('Frozen data shapes changed')
        def target(normals):
            nonlocal evaluations
            evaluations+=len(normals);guard()
            logs=means+normals@factor.T
            return math.exp(-.03)*np.maximum(np.exp(logs).mean(axis=1)-95,0)
        xx,yy=np.meshgrid(z,z,indexing='ij');train=np.column_stack([xx.ravel(),yy.ravel()])
        F=target(train).reshape(33,33);valid_y=target(validation)
        sqrtw=np.sqrt(w);G=sqrtw[:,None]*F*sqrtw[None,:]
        U,S,Vt=np.linalg.svd(G,full_matrices=False);guard()
        reference=float(w@F@w);rows=[];weighted_mass=float(w.sum()**2)
        for rank in (2,4,8):
            root_s=np.sqrt(S[:rank])
            A=U[:,:rank]*root_s[None,:]/sqrtw[:,None]
            B=root_s[:,None]*Vt[:rank,:]/sqrtw[None,:]
            approx=A@B
            # Predetermine constant-endpoint/linear-core interpolation, no tuning.
            Aa=np.column_stack([np.interp(validation[:,0],z,A[:,j]) for j in range(rank)])
            Bb=np.column_stack([np.interp(validation[:,1],z,B[j]) for j in range(rank)])
            pred=np.sum(Aa*Bb,axis=1);err=pred-valid_y
            contraction=float((w@A)@(B@w));matrix_sum=float(w@approx@w)
            if not abs(contraction-matrix_sum)<1e-10:raise ValueError('Direct contraction consistency failed')
            residual=float(np.linalg.norm(sqrtw[:,None]*(F-approx)*sqrtw[None,:]))
            discarded=float(np.linalg.norm(S[rank:]))
            if not abs(residual-discarded)<1e-10:raise ValueError('Weighted SVD residual diagnostic failed')
            if abs(contraction-reference)>math.sqrt(weighted_mass)*residual+1e-10:raise ValueError('Finite weighted-grid Cauchy diagnostic failed')
            np.savez(OUT/f'rank_{rank}_cores.npz',A=A,B=B,training_approximation=approx,validation_predictions=pred)
            rows.append(dict(rank=rank,core_parameters=2*33*rank,
                unique_training_targets_shared=1089,unique_validation_targets_shared=512,
                weighted_training_residual_diagnostic=residual,discarded_singular_norm_diagnostic=discarded,
                validation_RMSE_diagnostic=float(np.sqrt(np.mean(err**2))),validation_max_abs_diagnostic=float(np.max(np.abs(err))),
                negative_training_fit_count=int((approx<0).sum()),negative_validation_fit_count=int((pred<0).sum()),
                classical_direct_contraction_diagnostic=contraction,truncated_grid_integral_change_diagnostic=abs(contraction-reference),
                finite_weighted_grid_Cauchy_diagnostic=math.sqrt(weighted_mass)*residual,
                contraction_multiplications=(2*33+1)*rank,contraction_additions=(2*(33-1)+1)*rank-1,
                continuum_integral_price_error_certificate=None,numerical_enclosure=None,
                coherent_loader=None,loader_inverse=None,loading_rotation_synthesis=None,
                loader_normalization_certificate=None,loading_estimation_total_cost=None,
                loading_vs_uncompressed_improvement_percent=None,quantum20percent_threshold_passed=False,
                matched_classical_contraction_seconds=None,matched_quantum_loading_seconds=None,
                full_F30_acceptance=False))
            guard()
        if evaluations!=1601:raise ValueError('Unique training/validation accounting failed')
        np.savez(OUT/'training_and_validation.npz',training_values=F,validation_values=valid_y,
                 means=means,factor=factor,covariance=cov,singular_values=S)
        summary=dict(status='PASS_THREE_RANK_D1_DIAGNOSTICS_ONLY_QUANTUM_LOADING_CLOSED_UNCERTIFIED',
            contract=D1,rows=rows,unique_integrand_evaluations=evaluations,n_SVD=1,
            fixed_validation_seed=p['validation_seed'],training_weighted_mass_diagnostic=weighted_mass,
            full_training_grid_integral_diagnostic=reference,
            continuum_integral_certificate=None,Gaussian_tail_price_certificate=None,
            interpolation_certificate=None,no_rank_selected_on_validation=True,
            negative_fits_retained=True,barrier_rank_claim=False,high_dimensional_rank_claim=False,
            new_F03_transforms=0,quantum_loaders_compiled=0,new_physical_costs_adopted=0,
            full_F30_acceptance=False,matched_timings=0,advantage_claimed=False)
        for r in p['corpus']:
            raw=(ROOT/r['path']).read_bytes()
            if len(raw)!=r['bytes'] or sha(raw)!=r['sha256']:raise ValueError('Frozen input changed during check')
        write('summary.json',summary);guard()
        files=[f for f in OUT.iterdir() if f.is_file()]
        success=dict(status=summary['status'],full_F30_acceptance=False)
        success_raw=(json.dumps(success,indent=2,sort_keys=True)+'\n').encode('utf-8')
        entries=[dict(path=f.name,bytes=f.stat().st_size,sha256=sha(f.read_bytes())) for f in files]
        entries.append(dict(path='SUCCESS.json',bytes=len(success_raw),sha256=sha(success_raw)))
        manifest=dict(files=sorted(entries,key=lambda r:r['path']))
        manifest_raw=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode('utf-8')
        if len(files)+2>CAPS['output_files'] or sum(f.stat().st_size for f in files)+len(success_raw)+len(manifest_raw)>CAPS['output_bytes']:raise ValueError('Output cap')
        write('SUCCESS.json',success)
        write('manifest.json',manifest)
        print(json.dumps(dict(status=summary['status'],evaluations=evaluations,
            validation_RMSE=[r['validation_RMSE_diagnostic'] for r in rows],summary_sha256=sha((OUT/'summary.json').read_bytes()))))
    except BaseException as exc:
        if not (OUT/'FAILED.json').exists():write('FAILED.json',dict(status='FAILED_PRESERVED',error=str(exc)))
        raise

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['prepare','run']);args=a.parse_args()
    prepare() if args.mode=='prepare' else run()
