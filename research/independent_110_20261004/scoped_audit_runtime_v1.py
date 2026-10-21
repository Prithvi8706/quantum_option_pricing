"""Immutable runtime for isolated, bounded proof/interface audits; no finance imports."""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import ast
import hashlib
import json
import time

ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pair(q):return [q.numerator,q.denominator]
def dump(p,v):p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def model_rows(relative):
    tree=ast.parse((ROOT/relative).read_text(encoding='utf-8'))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Model')
    base={n.target.id:ast.literal_eval(n.value) for n in cls.body if isinstance(n,ast.AnnAssign)}
    rows=[]
    node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MODELS' for t in n.targets))
    names=list(base)
    for call in node.value.elts:
        row=dict(base)
        for name,value in zip(names,call.args):row[name]=ast.literal_eval(value)
        row.update({k.arg:ast.literal_eval(k.value) for k in call.keywords})
        rows.append({k:Q(str(v)) if isinstance(v,(int,float)) else v for k,v in row.items()})
    return rows

def launch(author,item,inputs,criteria,limits,check):
    author=Path(author).resolve();proof=ROOT/f'docs/independent_110_20261004/{item}/PROOF_AND_LIMITS.txt'
    out=ROOT/f'results/independent_110_20261004/{item}/run001'
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['prepare','run']);args=ap.parse_args()
    files=[author,Path(__file__).resolve(),proof]+[ROOT/p for p in inputs]
    if args.mode=='prepare':
        assert not out.exists() and all(p.is_file() for p in files)
        pins={str(p.relative_to(ROOT)).replace('\\','/'): {'sha256':sha(p),'bytes':p.stat().st_size} for p in files}
        assert sum(v['bytes'] for v in pins.values())<=32*1024*1024
        out.mkdir(parents=True)
        dump(out/'protocol.json',{'item':item,'input_pins':pins,'acceptance':criteria,'fixed_scope_and_stop':limits,
             'budgets':{'cpu_seconds':30,'wall_seconds':60,'output_bytes':4*1024*1024,'new_finance_paths':0,'matched_timing_runs':0},
             'global_fixture_credit':0,'source_adoption':False,'financial_contract_changed':False})
        print(json.dumps({'item':item,'prepared':True,'protocol_sha256':sha(out/'protocol.json')}));return
    assert (out/'protocol.json').exists() and not (out/'ATTEMPT.json').exists()
    cpu=time.process_time();wall=time.monotonic();protocol=json.loads((out/'protocol.json').read_text(encoding='utf-8'))
    def bind():
        for p,v in protocol['input_pins'].items():assert sha(ROOT/p)==v['sha256'] and (ROOT/p).stat().st_size==v['bytes'],p
    try:
        bind();dump(out/'ATTEMPT.json',{'one_fixed_invocation':True,'financial_paths':0})
        findings=check()
        assert time.process_time()-cpu<=30 and time.monotonic()-wall<=60
        bind()
        summary={'item':item,'audit_passed':True,'bounded_step_completed':True,'entire_limitation_solved':False,
          'financial_G2_completed':False,'source_adoption':False,'quantum_advantage':False,'new_global_fixture_credit':0,
          'scientific_scope':'Prospectively frozen proof/interface audit; numerical diagnostics are not financial acquisition or a derivative proof.',
          'findings':findings}
        dump(out/'summary.json',summary)
        inventory=[p for p in out.iterdir() if p.is_file()]
        assert sum(p.stat().st_size for p in inventory)+32768<=4*1024*1024
        dump(out/'manifest.json',{'files':{str(p.relative_to(ROOT)).replace('\\','/'):{'sha256':sha(p),'bytes':p.stat().st_size} for p in inventory},
             'input_pins':protocol['input_pins'],'author_sha256':sha(author),'proof_sha256':sha(proof)})
        print(json.dumps({'item':item,'audit_passed':True,'finding':findings.get('decision'),'checks':findings.get('checks')}))
    except BaseException as exc:
        dump(out/'FAILED_UNSEALED.json',{'audit_passed':False,'bounded_step_completed':False,'error':str(exc)[:2000],
             'failure_overrides_any_partial_summary':True})
        raise
