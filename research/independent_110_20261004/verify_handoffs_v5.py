"""Root metadata verifier for new receipts; no scientific replay or shared writes."""
from pathlib import Path
import hashlib,json,datetime,argparse
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'results/independent_110_20261004'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(name,run):
    p=Path(name)
    return p if p.is_absolute() else ROOT/p if p.parts[0] in ('docs','research','results','manuscript','.context') else run/p
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--receipt',action='append',required=True);ap.add_argument('--extra',action='append',default=[]);a=ap.parse_args()
    out=BASE/a.out;assert out.parent==BASE and not out.exists();out.mkdir()
    checks=[];receipts=[]
    for definition in a.receipt:
        item,relative=definition.split('=',1);run=BASE/relative;mf=run/'manifest.json'
        assert run.is_relative_to(BASE) and mf.exists() and not any('fail' in p.name.lower() for p in run.iterdir())
        m=json.loads(mf.read_text(encoding='utf-8'));filetable=m['files']
        entries=filetable.items() if isinstance(filetable,dict) else [(s['path'],s) for s in filetable]
        expected={resolve(name,run):spec for name,spec in entries}
        declared={str(p.relative_to(run)).replace('\\','/') for p in expected if p.is_relative_to(run)}
        observed={str(p.relative_to(run)).replace('\\','/') for p in run.rglob('*') if p.is_file() and p.name!='manifest.json'}
        assert declared==observed,(item,declared^observed)
        for key in ('input_pins','frozen_inputs','selected_runtime','frozen_corpus_sha256','corpus_sha256'):
            table=m.get(key,{})
            if isinstance(table,list):table={r['path']:r for r in table}
            expected.update({resolve(name,run):spec for name,spec in table.items()})
        for p in run.glob('*protocol.json'):
            protocol=json.loads(p.read_text(encoding='utf-8'))
            corpus=protocol.get('corpus',[])
            if isinstance(corpus,list):expected.update({ROOT/s['path']:s for s in corpus})
        freeze_path=ROOT/f'docs/independent_110_20261004/{item}/FREEZE.json'
        if 'freeze_sha256' in m:expected[freeze_path]=m['freeze_sha256']
        for path,spec in expected.items():
            wanted=spec if isinstance(spec,str) else spec['sha256'];size=path.stat().st_size
            actual=sha(path);ok=actual==wanted and (isinstance(spec,str) or 'bytes' not in spec or size==spec['bytes'])
            try:label=str(path.relative_to(ROOT)).replace('\\','/')
            except ValueError:label=str(path)
            checks.append({'item':item,'path':label,'expected':wanted,'observed':actual,'bytes':size,'passed':ok})
        receipts.append({'item':item,'manifest':str(mf.relative_to(ROOT)).replace('\\','/'),'sha256':sha(mf),'inventory_exact':True})
    for extra in a.extra:
        name,wanted=extra.rsplit('=',1);p=ROOT/name
        checks.append({'item':'peer_or_handoff','path':name,'expected':wanted,'observed':sha(p),'passed':sha(p)==wanted})
    result={'passed':all(c['passed'] for c in checks),'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'fresh_hash_checks':len(checks),'mismatches':sum(not c['passed'] for c in checks),'receipts':receipts,'checks':checks,
       'metadata_only':True,'new_scientific_runs':0,'new_global_fixture_credit':0,
       'scope':'Fresh selected input and owned-artifact hashes with exact receipt inventories. This does not re-prove scientific statements or close complete runtime dependencies.'}
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'author_sha256':sha(Path(__file__)),'verification_sha256':sha(out/'verification.json')},indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','fresh_hash_checks','mismatches')}));assert result['passed']
if __name__=='__main__':main()
