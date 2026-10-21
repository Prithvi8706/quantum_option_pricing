"""Static-only peer receipt author; no experiment or source imports."""
from pathlib import Path
import ast, hashlib, json
root=Path(__file__).resolve().parents[4]
names=[
 'research/independent_110_20261004/E14/deterministic_schedule_audit_v2.py',
 'docs/independent_110_20261004/E14/PROOF_AND_LIMITS_v2.txt',
 'results/independent_110_20261004/E14/run002/protocol.json',
 'research/independent_110_20261004/scoped_audit_runtime_v2.py',
]
pins={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in names}
protocol=json.loads((root/names[2]).read_text())
for p,v in protocol['input_pins'].items():
 assert hashlib.sha256((root/p).read_bytes()).hexdigest()==v['sha256'],p
for p in (names[0],names[3]):ast.parse((root/p).read_text())
receipt={
 'disposition':'STATIC_REVIEW_PASS_FOR_ONE_FROZEN_ARITHMETIC_RUN',
 'reviewed_sha256':pins,'protocol_input_pins_all_match':True,
 'source_imports':0,'scientific_invocations':0,'prospective_review':True,
 'findings':[
  'Corrected base bound 17/8 follows E[g(R)^2] <= 2*g(p)^2 + 2*E[(R-p)^2], using g(p)<=1/4 and RMSE at base <=1.',
  'Positive levels retain 6*2^-n without an unsupported bounded-output cap.',
  'Rare-positive exact control has mean-square error 1 and base second moment 21/16, above 1 and below 17/8; it properly rejects the removed generic cap.',
  'Three-error cutoff factor-four and explicit Delta0 convention remain selected-text diagnostics; neither proves universal theorem invalidity.',
  'Runtime validates pinned inputs before and after the one invocation, retains failure, and scopes 30 CPU/60 wall/4 MiB output to this arithmetic audit.',
  'The prepared protocol pins the original static hold, revised source, proof and new helper; no source adoption or finance paths are authorized by this review.'
 ],
 'remaining_obligations':['Finite QAMC controller and decoder','Preparation/inverse and median costs','Finite constants and financial theorem transfer','Executable compiled implementation'],
 'entire_limitation_solved':False,'new_fixture_credit':0,'quantum_advantage':False,
}
out=Path(__file__).with_name('STATIC_REVIEW_v2.json')
assert not out.exists()
out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'receipt':str(out.relative_to(root)).replace('\\','/'),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'disposition':receipt['disposition']}))
