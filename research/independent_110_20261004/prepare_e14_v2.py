"""Prospective E14 moment-bound correction; v1 inputs remain immutable/unexecuted."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'research/independent_110_20261004';D=ROOT/'docs/independent_110_20261004/E14'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not (ROOT/'results/independent_110_20261004/E14/run001/ATTEMPT.json').exists()
hold={'status':'STATIC_REJECTED_BEFORE_ARITHMETIC','reason':'RMSE-only generic inner outputs need not be bounded; proposed Delta0<=1 and min(1,6*2^-n) moments unjustified without clipping.',
      'author_sha256':sha(R/'E14/deterministic_schedule_audit_v1.py'),
      'protocol_sha256':sha(ROOT/'results/independent_110_20261004/E14/run001/protocol.json'),
      'proof_sha256':sha(D/'PROOF_AND_LIMITS.txt'),'scientific_runs':0,'originals_preserved':True}
(D/'STATIC_HOLD_run001.json').write_text(json.dumps(hold,indent=2)+'\n')
new_runtime=R/'scoped_audit_runtime_v2.py';assert not new_runtime.exists()
runtime=(R/'scoped_audit_runtime_v1.py').read_text(encoding='utf-8')
runtime=runtime.replace("PROOF_AND_LIMITS.txt'","PROOF_AND_LIMITS_v2.txt'")
runtime=runtime.replace("/{item}/run001'","/{item}/run002'")
new_runtime.write_text(runtime,encoding='utf-8')
author=R/'E14/deterministic_schedule_audit_v2.py';assert not author.exists()
source=(R/'E14/deterministic_schedule_audit_v1.py').read_text(encoding='utf-8')
source=source.replace('from scoped_audit_runtime_v1 import','from scoped_audit_runtime_v2 import')
source=source.replace(" 'docs/limitation_audit_20261001/implementation_plan/roadmap.json']", " 'docs/limitation_audit_20261001/implementation_plan/roadmap.json',\n 'docs/independent_110_20261004/E14/STATIC_HOLD_run001.json']")
source=source.replace("pair(Q(1) if n==0 else min(Q(1),6*Q(1,2**n)))", "pair(Q(17,8) if n==0 else 6*Q(1,2**n))")
source=source.replace("    rows=[];checks=1", "    # RMSE-only outputs may exceed unit support; this exact control rejects the old cap.\n    mse=Q(1,4)*Q(2)**2\n    base_second=Q(1,4)*g(Q(3,4)+2)**2+Q(3,4)*g(Q(3,4))**2\n    assert mse==1 and 1<base_second<=Q(17,8)\n    rows=[];checks=3")
author.write_text(source,encoding='utf-8')
proof=(D/'PROOF_AND_LIMITS.txt').read_text(encoding='utf-8')
proof=proof.replace('bounded signed difference\nmoment', 'generic RMSE-promised signed difference\nmoment')
proof += '\nV2 prospective correction: RMSE-only inner estimators have no bounded-output\nguarantee. For Delta0, (g(R1))^2 <=2*(g(p))^2+2*|R1-p|^2\nin expectation, giving17/8 uniformly over the two toy outer states. Positive\nlevels use6*2^-n without a unit-support cap. An exact rare-positive-output\ncontrol has inner MSE1 but base second moment21/16>1; it rejects the old\ncap before any arithmetic run. No clipping or bounded generic QAMC output\ncontroller is silently assumed. Original v1 source/proof/protocol are retained\nas a rejected static preparation with zero scientific invocation.\n'
(D/'PROOF_AND_LIMITS_v2.txt').write_text(proof,encoding='utf-8')
print(json.dumps({'v2_authored':True,'v1_scientific_invocations':0,'author_sha256':sha(author)}))
