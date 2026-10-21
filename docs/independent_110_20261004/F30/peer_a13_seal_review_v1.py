"""Independent static recovery review and deterministic expected raw-byte inventory."""
from pathlib import Path
import ast,hashlib,json
root=Path(__file__).resolve().parents[3]
new=root/'results/independent_110_20261004/F30/seal_recovery_run001'
old=root/'results/independent_110_20261004/F30/run002'
sha=lambda b:hashlib.sha256(b).hexdigest()
encode=lambda d:(json.dumps(d,indent=2,sort_keys=True)+'\n').encode('utf-8')
p=json.loads((new/'protocol.json').read_bytes())
for r in p['corpus']:
 raw=(root/r['path']).read_bytes();assert sha(raw)==r['sha256'] and len(raw)==r['bytes'],r['path']
assert {f.name for f in new.iterdir()}=={'protocol.json'}
author=root/'research/independent_110_20261004/F30/seal_recovery_v1.py'
tree=ast.parse(author.read_text())
names=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='OLD_NAMES' for t in n.targets))
assert {f.name for f in old.iterdir()}==set(names) and len(names)==9
failure=json.loads((root/'docs/independent_110_20261004/F30/SEAL_FAILURE_run002.json').read_bytes())
m=json.loads((old/'manifest.json').read_bytes());bad=[]
assert len(m['files'])==8
for r in m['files']:
 raw=(old/r['path']).read_bytes()
 if len(raw)!=r['bytes'] or sha(raw)!=r['sha256']:
  bad.append({'path':r['path'],'recorded_bytes':r['bytes'],'actual_bytes':len(raw),'recorded_sha256':r['sha256'],'actual_sha256':sha(raw)})
assert bad==failure['mismatches'] and len(bad)==1 and bad[0]['path']=='SUCCESS.json'
assert bad[0]['recorded_bytes']==121 and bad[0]['actual_bytes']==125
lf=(old/'SUCCESS.json').read_bytes().replace(b'\r\n',b'\n')
assert len(lf)==121 and sha(lf)==bad[0]['recorded_sha256']
external=[]
for name in names:
 path='results/independent_110_20261004/F30/run002/'+name;raw=(root/path).read_bytes()
 external.append({'path':path,'bytes':len(raw),'sha256':sha(raw)})
expected_contents={
 'protocol.json':(new/'protocol.json').read_bytes(),
 'ATTEMPT.json':encode({'kind':'metadata_only','scientific_invocations':0}),
 'summary.json':encode({'status':'PASS_METADATA_ONLY_EXACT_BYTE_RECOVERY','external_artifacts':external,
  'original_manifest_valid':False,'retained_mismatches':bad,'scientific_invocations':0,'scientific_reruns':0,'new_scientific_credit':False,'full_F30_acceptance':False}),
 'SUCCESS.json':encode({'status':'PASS_METADATA_ONLY_EXACT_BYTE_RECOVERY','scientific_invocations':0,'full_F30_acceptance':False})}
# Use the actual platform's Path ordering, as prescribed by the frozen writer.
ordered=sorted(new/name for name in expected_contents)
expected={'files':[{'path:f.name,'bytes':len(expected_contents[f.name]),'sha256':sha(expected_contents[f.name])} for f in ordered],
 'external_artifacts':external,'provenance':'Original failed LF-planned seal retained; actual bytes recovered without science execution','scientific_invocations':0}
dest=Path(__file__).with_name('SEAL_RECOVERY_EXPECTED_MANIFEST_run001.json');assert not dest.exists();dest.write_bytes(encode(expected))
receipt={'item':'F30','disposition':'STATIC_REVIEW_PASS_FOR_ONE_FROZEN_METADATA_RECOVERY',
 'source_sha256':sha(author.read_bytes()),'protocol_sha256':sha((new/'protocol.json').read_bytes()),
 'nineteen_frozen_input_pins_match':True,'old_manifest_rows':8,'matching_old_manifest_rows':7,'original_owned_files':9,
 'retained_original_mismatch':bad,'LF_normalization_exactly_matches_original_expectation':True,
 'expected_corrected_manifest':dest.relative_to(root).as_posix(),'expected_corrected_manifest_sha256':sha(dest.read_bytes()),
 'original_actual_output_inventory':external,'recovery_not_executed_at_review':True,
 'findings':['Canonical UTF8 write_bytes avoids newline translation; hashes come from actual raw owned/external bytes.',
  'Frozen membership and sole declared SUCCESS mismatch are checked; old failed manifest remains explicit and included externally.',
  'All original scientific inputs remain bound; no experiment, project or NumPy import and no payoff/fit/SVD call occurs.',
  'Failure and CPU/wall/output caps remain separate metadata scope. Recovery cannot certify mathematics, full price error or quantum loading.'],
 'scientific_reruns':0,'new_scientific_credit':False,'full_F30_acceptance':False,
 'budgets':p['budgets']}
review=Path(__file__).with_name('SEAL_STATIC_REVIEW_run001.json');assert not review.exists();review.write_bytes(encode(receipt))
print(json.dumps({'review':review.relative_to(root).as_posix(),'review_sha256':sha(review.read_bytes()),'expected_manifest_sha256':sha(dest.read_bytes())}))
