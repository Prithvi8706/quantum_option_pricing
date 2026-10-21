"""Root metadata verifier with explicitly pinned postseal administrative overlays."""
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
    checks=[];receipts=[];extras={}
    for extra in a.extra:
        name,wanted=extra.rsplit('=',1);extras[ROOT/name]=wanted
    try:
        for definition in a.receipt:
            fields=definition.split('=');assert len(fields)==3,'Explicit expected manifest hash required'
            item,relative,mf_expected=fields;run=BASE/relative;mf=run/'manifest.json'
            assert run.is_relative_to(BASE) and mf.exists() and not any('fail' in p.name.lower() for p in run.iterdir())
            assert sha(mf)==mf_expected,'Manifest handoff SHA mismatch'
            m=json.loads(mf.read_text(encoding='utf-8'));filetable=m['files']
            entries=filetable.items() if isinstance(filetable,dict) else [(s['path'],s) for s in filetable]
            expected={resolve(name,run):spec for name,spec in entries}
            declared={str(p.relative_to(run)).replace('\\','/') for p in expected if p.is_relative_to(run)}
            overlays={str(p.relative_to(run)).replace('\\','/') for p in extras if p.is_relative_to(run) and p.name!='manifest.json'}
            observed={str(p.relative_to(run)).replace('\\','/') for p in run.rglob('*') if p.is_file() and p.name!='manifest.json'}
            assert declared|overlays==observed,(item,(declared|overlays)^observed)
            for key in ('input_pins','frozen_inputs','selected_runtime','frozen_corpus_sha256','corpus_sha256'):
                table=m.get(key,{})
                if isinstance(table,list):table={r['path']:r for r in table}
                expected.update({resolve(name,run):spec for name,spec in table.items()})
            for p in run.glob('*protocol.json'):
                corpus=json.loads(p.read_text(encoding='utf-8')).get('corpus',[])
                if isinstance(corpus,list):expected.update({ROOT/s['path']:s for s in corpus})
            if 'freeze_sha256' in m:expected[ROOT/f'docs/independent_110_20261004/{item}/FREEZE.json']=m['freeze_sha256']
            for path,spec in expected.items():
                wanted=spec if isinstance(spec,str) else spec['sha256'];size=path.stat().st_size;actual=sha(path)
                ok=actual==wanted and (isinstance(spec,str) or 'bytes' not in spec or size==spec['bytes'])
                try:label=str(path.relative_to(ROOT)).replace('\\','/')
                except ValueError:label=str(path)
                checks.append({'item':item,'path':label,'expected':wanted,'observed':actual,'bytes':size,'passed':ok})
            receipts.append({'item':item,'manifest':str(mf.relative_to(ROOT)).replace('\\','/'),'expected_sha256':mf_expected,
               'observed_sha256':sha(mf),'scientific_inventory_plus_explicit_overlays_exact':True,'postseal_administrative_overlays':sorted(overlays-declared)})
        for p,wanted in extras.items():
            actual=sha(p);checks.append({'item':'pinned_administrative_overlay_or_review','path':str(p.relative_to(ROOT)).replace('\\','/'),'expected':wanted,'observed':actual,'passed':actual==wanted})
        result={'passed':all(c['passed'] for c in checks),'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'fresh_hash_checks':len(checks),'mismatches':sum(not c['passed'] for c in checks),'receipts':receipts,'checks':checks,
          'metadata_only':True,'new_scientific_runs':0,'new_global_fixture_credit':0,
          'scope':'Explicit handoff manifest pins, selected input/artifact hashes and scientific inventory plus separately hash-pinned postseal administrative overlays. No scientific replication or complete-runtime proof.'}
        (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
        assert result['passed'],'Artifact/input mismatch'
        (out/'manifest.json').write_text(json.dumps({'author_sha256':sha(Path(__file__)),'verification_sha256':sha(out/'verification.json')},indent=2)+'\n')
        print(json.dumps({k:result[k] for k in ('passed','fresh_hash_checks','mismatches')}))
    except BaseException as e:
        (out/'FAILED.json').write_text(json.dumps({'passed':False,'scope':'metadata_only','error':str(e),'scientific_receipts_changed':False},indent=2)+'\n');raise
if __name__=='__main__':main()
