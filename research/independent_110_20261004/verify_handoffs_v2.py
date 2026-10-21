"""Fresh root verification of scoped local handoffs; zero scientific reruns."""
from pathlib import Path
import hashlib
import json
import datetime

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/independent_110_20261004/handoff_integrity_run002'
SPECS={
 'F16':('F16/run001','F16/factor_reuse_audit_v1.py'),
 'F08':('F08/run001','F08/single_predicate_screen_v1.py'),
 'F13':('F13/run001','F13/non_lipschitz_transfer_audit_v1.py'),
 'E17':('E17/audit_run001',None),
 'E08':('E08/run004','E08/confidence_allocation_screen_v4.py'),
 'C12':('C12/audit_run002',None),
 'F18':('F18/run001','F18/nested_theorem_map_v1.py'),
 'C05':('C05/run001','C05/allocation_grid_v1.py'),
}
EXTRA={
 'docs/independent_110_20261004/E17/MOMENT_PROOF_v2.md':'8427a39204ff66474dde1f4fc2dc010b714548f506cc9b37a177707fcd9f0ca6',
 'docs/independent_110_20261004/E17/CITATION_ERRATUM_run001.json':'7db187f5445b37dbf97739441871037c3141bf7ed07804fc8f78bdb6f32a80df',
 'docs/independent_110_20261004/E17/HANDOFF.md':'5f15e6a776bdcdb3ff22ef848d4962d4b34c3617f097b6e6207eae9390a5802c',
 'docs/independent_110_20261004/C12/peer_run001/F18_PROOF_STATIC_REVIEW_run001.json':'aa5fd5db5a6ed61b6356e9f2b72aabcba19a8e052790ddd7aa96e6f61c7d270d',
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
        for key in ['files','input_pins','frozen_inputs','selected_runtime','frozen_corpus_sha256']:
            for name,spec in manifest.get(key,{}).items():
                file=Path(name)
                if not file.is_absolute():file=(run/file) if key=='files' and len(file.parts)==1 else ROOT/file
                expected[file]=spec
        if author:expected[ROOT/'research/independent_110_20261004'/author]=manifest['author_sha256']
        if item=='E17':expected[ROOT/'docs/independent_110_20261004/E17/FREEZE.json']=manifest['prospective_freeze_sha256']
        declared=set()
        for name in manifest['files']:
            path=Path(name)
            if not path.is_absolute():path=(run/path) if len(path.parts)==1 else ROOT/path
            if path.parent==run:declared.add(path.name)
        observed={p.name for p in run.iterdir() if p.is_file() and p.name!='manifest.json'}
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
