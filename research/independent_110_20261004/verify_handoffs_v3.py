"""Fresh root verification of scoped local handoffs; zero scientific reruns."""
from pathlib import Path
import hashlib
import json
import datetime

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/independent_110_20261004/handoff_integrity_run003'
SPECS={
 'E01':('E01/audit_run001',None),
 'C15':('C15/run002',None),
 'E15':('E15/run002','E15/coherent_inner_toy_v2.py'),
}
EXTRA={
 'docs/independent_110_20261004/E01/HANDOFF.md':'4057fd08ba366c4c32a2f4471a11c1519464b0542ad67cec1d6882094eec188f',
}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert not OUT.exists()
    OUT.mkdir(parents=True)
    checks=[];receipts=[]
    for item,(relative,author) in SPECS.items():
        run=ROOT/'results/independent_110_20261004'/relative
        manifest=json.loads((run/'manifest.json').read_text())
        assert not any('fail' in p.name.lower() for p in run.iterdir())
        expected={}
        for key in ['files','input_pins','frozen_inputs','selected_runtime','frozen_corpus_sha256','corpus_sha256']:
            for name,spec in manifest.get(key,{}).items():
                file=Path(name)
                if not file.is_absolute():file=(run/file) if key=='files' and file.parts[0] not in ('docs','research','results') else ROOT/file
                expected[file]=spec
        if author:expected[ROOT/'research/independent_110_20261004'/author]=manifest['author_sha256']
        if item=='E01':expected[ROOT/'docs/independent_110_20261004/E01/FREEZE.json']=manifest['freeze_sha256']
        if item=='C15':expected[ROOT/'research/independent_110_20261004/C15/claims_v1.json']=manifest['claim_release_sha256']
        if item=='E17':expected[ROOT/'docs/independent_110_20261004/E17/FREEZE.json']=manifest['prospective_freeze_sha256']
        declared=set()
        for name in manifest['files']:
            path=Path(name)
            if not path.is_absolute():path=(run/path) if path.parts[0] not in ('docs','research','results') else ROOT/path
            if path.is_relative_to(run):declared.add(str(path.relative_to(run)).replace('\\','/'))
        observed={str(p.relative_to(run)).replace('\\','/') for p in run.rglob('*') if p.is_file() and p.name!='manifest.json'}
        assert declared==observed, (item,declared^observed)
        for path,spec in expected.items():
            wanted=spec if isinstance(spec,str) else spec['sha256']
            actual=sha(path);size=path.stat().st_size
            try:label=str(path.relative_to(ROOT)).replace('\\','/')
            except ValueError:label=str(path)
            checks.append({'item':item,'path':label,'expected':wanted,'observed':actual,'bytes':size,
                           'passed':actual==wanted and (isinstance(spec,str) or size==spec['bytes'])})
        receipts.append({'item':item,'manifest':str((run/'manifest.json').relative_to(ROOT)).replace('\\','/'),
                         'sha256':sha(run/'manifest.json'),'inventory_exact':True})
    for name,wanted in EXTRA.items():
        path=ROOT/name
        checks.append({'item':'review_or_citation_overlay','path':name,'expected':wanted,'observed':sha(path),
                       'bytes':path.stat().st_size,'passed':sha(path)==wanted})
    passed=all(c['passed'] for c in checks)
    result={'passed':passed,'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'metadata_only':True,'fresh_hash_checks':len(checks),'mismatches':sum(not c['passed'] for c in checks),
            'receipts':receipts,'checks':checks,'new_scientific_runs':0,'new_global_fixture_credit':0,
            'scope':'Root fresh selected-input/owned-artifact hash and exact receipt inventory verification; does not re-prove primary scientific certificates or close runtime dependencies.'}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'manifest.json').write_text(json.dumps({'author_sha256':sha(Path(__file__)),'verification_sha256':sha(OUT/'verification.json')},indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['passed','fresh_hash_checks','mismatches','new_global_fixture_credit']}))
    assert passed
if __name__=='__main__':main()
