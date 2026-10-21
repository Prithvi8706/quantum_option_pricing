"""Read-only post-recovery integrity against the independent prospective expected seal."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[3]
out=root/'results/independent_110_20261004/F30/seal_recovery_run001'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=json.loads(Path(__file__).with_name('SEAL_STATIC_REVIEW_run001.json').read_text())
expected=root/prior['expected_corrected_manifest']
assert sha(expected)==prior['expected_corrected_manifest_sha256']
assert (out/'manifest.json').read_bytes()==expected.read_bytes()
m=json.loads(expected.read_bytes())
assert {p.name for p in out.iterdir()}=={r['path'] for r in m['files']}|{'manifest.json'}
for r in m['files']:
 p=out/r['path'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
for r in m['external_artifacts']:
 p=root/r['path'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
protocol=json.loads((out/'protocol.json').read_bytes())
for r in protocol['corpus']:
 p=root/r['path'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
assert not (out/'FAILED.json').exists()
record={'item':'F30','disposition':'POST_RECOVERY_INTEGRITY_PASS_METADATA_ONLY',
 'actual_recovery_manifest_sha256':sha(out/'manifest.json'),
 'matches_independently_predicted_manifest_exact_bytes':True,
 'fresh_frozen_input_pins':19,'fresh_owned_manifest_entries':4,'fresh_external_original_outputs':9,
 'actual_recovery_owned_files':5,'actual_recovery_owned_bytes':sum(p.stat().st_size for p in out.iterdir()),
 'old_manifest_still_invalid':True,'original_sole_SUCCESS_mismatch_preserved':prior['retained_original_mismatch'],
 'scientific_reruns':0,'new_scientific_credit':False,'full_F30_acceptance':False,
 'scope':'Completed one original diagnostic; original scientific seal failed; fresh metadata recovery exact-byte seal verified. No original artifacts edited and no quantum or continuum certificate acquired.'}
dest=Path(__file__).with_name('SEAL_POSTRUN_REVIEW_run001.json');assert not dest.exists();dest.write_bytes((json.dumps(record,indent=2,sort_keys=True)+'\n').encode())
print(json.dumps({'review':dest.relative_to(root).as_posix(),'sha256':sha(dest),'actual_manifest_sha256':sha(out/'manifest.json')}))
