"""Fresh selected handoff integrity, with authoritative failed-attempt handling."""
from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/independent_110_20261004'
OUT=BASE/'handoff_integrity_run004'
SPECS={
 'F15':('F15/run001','manifest.json','F15/negative_leverage_tail_v1.py'),
 'F23':('F23/screen_run001','manifest.json',None),
 'H03':('H03/run001','failure_manifest.json',None),
 'F11':('F11/run001','manifest.json','F11/coarse_control_audit_v1.py'),
 'F12':('F12/run001','manifest.json','F12/boundary_coupling_audit_v1.py'),
 'F14':('F14/run001','manifest.json','F14/exact_transition_inventory_v1.py'),
 'F17':('F17/run001','manifest.json','F17/boundary_band_audit_v1.py'),
}
EXTRA={
 'docs/independent_110_20261004/F15/peer_a13_run001/STATIC_REVIEW.json':'100fad253b6340e154dd5a00e0e6091d6c0158c7ea68896dafd5466d663e42a6',
 'docs/independent_110_20261004/F23/HANDOFF.md':'bdac7f9f38561d8d0c0383fb0f9655a3f2fa332270195060914e7cd9a36e6d5c',
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(name,run):
    p=Path(name)
    return p if p.is_absolute() else ROOT/p if p.parts[0] in ('docs','research','results','manuscript','.context') else run/p
def main():
    assert not OUT.exists();OUT.mkdir(parents=True)
    checks=[];receipts=[]
    for item,(relative,mfname,author) in SPECS.items():
        run=BASE/relative;mf=run/mfname;manifest=json.loads(mf.read_text(encoding='utf-8'))
        failed=item=='H03'
        assert (run/'FAILED.json').exists() if failed else not any('fail' in p.name.lower() for p in run.iterdir())
        if failed:assert not (run/'SUCCESS.json').exists() and not (run/'summary.json').exists()
        files=manifest['files'];entries=files.items() if isinstance(files,dict) else [(s['path'],s) for s in files]
        expected={resolve(name,run):spec for name,spec in entries}
        declared={str(p.relative_to(run)).replace('\\','/') for p in expected if p.is_relative_to(run)}
        observed={str(p.relative_to(run)).replace('\\','/') for p in run.rglob('*') if p.is_file() and p.name!=mfname}
        assert declared==observed,(item,declared^observed)
        for key in ('input_pins','frozen_inputs'):
            expected.update({resolve(name,run):spec for name,spec in manifest.get(key,{}).items()})
        if author:expected[ROOT/'research/independent_110_20261004'/author]=manifest['author_sha256']
        if item=='F23':expected[ROOT/'docs/independent_110_20261004/F23/FREEZE.json']=manifest['freeze_sha256']
        if item=='H03':
            protocol=json.loads((run/'protocol.json').read_text())
            expected.update({ROOT/v['path']:v for v in protocol['corpus']})
        for p,spec in expected.items():
            wanted=spec if isinstance(spec,str) else spec['sha256'];size=p.stat().st_size
            ok=sha(p)==wanted and (isinstance(spec,str) or 'bytes' not in spec or size==spec['bytes'])
            checks.append({'item':item,'path':str(p.relative_to(ROOT)).replace('\\','/'),'expected':wanted,'observed':sha(p),'bytes':size,'passed':ok})
        receipts.append({'item':item,'manifest':str(mf.relative_to(ROOT)).replace('\\','/'),'sha256':sha(mf),
            'inventory_exact':True,'failed_attempt_preserved':failed,'scientific_success_asserted':False if failed else 'Only original bounded scope'})
    for name,wanted in EXTRA.items():
        p=ROOT/name;checks.append({'item':'peer_or_handoff','path':name,'expected':wanted,'observed':sha(p),'passed':sha(p)==wanted})
    result={'passed':all(c['passed'] for c in checks),'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'fresh_hash_checks':len(checks),'mismatches':sum(not c['passed'] for c in checks),'receipts':receipts,'checks':checks,
       'metadata_only':True,'new_scientific_runs':0,'new_global_fixture_credit':0,
       'scope':'Selected fresh hashes and exact receipt inventories; failed H03 remains failed, not reclassified by metadata integrity.'}
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'manifest.json').write_text(json.dumps({'author_sha256':sha(Path(__file__)),'verification_sha256':sha(OUT/'verification.json')},indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','fresh_hash_checks','mismatches')}));assert result['passed']
if __name__=='__main__':main()
