"""Static prepared-packet hold; no scientific imports or array reads."""
from pathlib import Path
import ast,hashlib,json
root=Path(__file__).resolve().parents[3];out=root/'results/independent_110_20261004/F30/run001'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((out/'protocol.json').read_text())
for row in p['corpus']:assert sha(root/row['path'])==row['sha256'],row['path']
source=root/'research/independent_110_20261004/F30/rank_screen_v1.py'
ast.parse(source.read_text());assert not (out/'ATTEMPT.json').exists()
receipt={'item':'F30','disposition':'STATIC_HOLD_ENVIRONMENT_MISMATCH_BEFORE_DIAGNOSTIC',
 'protocol_sha256':sha(out/'protocol.json'),'input_sha256':{r['path']:r['sha256'] for r in p['corpus']},
 'prepared_numpy_version':p['numpy'],'proof_named_numpy_version':'2.0.2',
 'no_payoff_or_fit_invocation_marker':True,'scientific_invocations_by_reviewer':0,'audited_source_imports':0,
 'core_scientific_static_review':'PASS_SCOPED_DIAGNOSTIC_MATH',
 'findings':['Original plain D1 PCA Asian integrand preserved, without transform or preintegration change.',
  'Unnormalized truncated Gaussian training grid and separate conditioned validation law are explicit.',
  'Weighted rank2/4/8 SVD/Cauchy and contraction operation counts are finite-grid diagnostics; no continuum or loader-cost theorem is transferred.',
  'Negative fits and training/setup obligations remain; no validation rank selection or timing claim.',
  'Prepared version1.26.4 conflicts with prospectively named2.0.2; author independently detected and retained this preparation before any science.'],
 'next':'Preserve v1 source/proof/corpus/protocol; fresh prospective release with verified explicit interpreter and unchanged scientific rank/corpus/cap scope.',
 'quantum_advantage':False,'new_fixture_credit':0,'run001_approved':False}
dest=Path(__file__).with_name('STATIC_REVIEW_REJECTION_run001.json');assert not dest.exists();dest.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'receipt':dest.relative_to(root).as_posix(),'sha256':sha(dest)}))
