from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[3];out=root/'results/independent_110_20261004/H11/run001'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((out/'manifest.json').read_text())
for name,expected in m['files'].items():assert sha(out/name)==expected,name
for name,expected in m['input_pins'].items():assert sha(root/name)==expected,name
assert not (out/'FAILED_UNSEALED.json').exists()
receipt={'passed':True,'fresh_owned_hashes':len(m['files']),'fresh_input_hashes':len(m['input_pins']),
 'manifest_sha256':sha(out/'manifest.json'),'scientific_reruns':0,'physical_integration':False}
dest=out/'HANDOFF_INTEGRITY.json';assert not dest.exists();dest.write_text(json.dumps(receipt,indent=2)+'\n')
text='''H11 bounded first step completed: one original72/F40 multiplier leaf's22914 native metadata rows and archived logical resources reconciled; eight CCZ phase states/eight full rational H-CCZ-H columns matched Toffoli. Eight negative admission controls and one omitted-H control rejected. No financial multiplier gate replay or arithmetic fixture credit occurred.

One conditional finite theorem parameter bill for the exact He2502.01864v1 full intrablock construction gives n0=32768,m=10923,k=5791,t=30,q=1073741824 and data-block length3538944000, before extraction/decoder/routing ancillas. The distance lower5133 is conditional on the paper construction, not a noisy device/circuit certificate. All block wires, including gauge-fixed/embedding wires, count. The code is non-LDPC. The logical leaf requires11244 CCZ,22488 target Hadamards and original224 X/11446 CNOT; encoded Clifford interfaces are unresolved.

Artifacts: research/independent_110_20261004/H11/addressable_ccz_audit_v1.py; docs/independent_110_20261004/H11/FINITE_PARAMETERS_AND_LIMITS.txt; results/independent_110_20261004/H11/run001/ with protocol, finite_parameter_and_gate_bill, ideal_identity_checks, negative_controls, summary, manifest and HANDOFF_INTEGRITY. One30CPU/60wall/4MiB run; fresh14 input and6 owned hashes all matched. No source adoption, timing, price samples, new fixture credit or quantum advantage.

Physical integration and numerical timing remain closed: finite instantiated stabilizers/code certificate, compatible Clifford operations, extraction/decoder, physical CCZ coherent channel/error/duration, preparation/idle/controller, topology/movement, full space/cap and H17-compatible complete failure are all unprovided. The factory-produced-CCZ baseline also lacks a compatible finite factory row. This does not solve all H11 or disprove the coding theorem.

Retained primary access failures: two browser screenshot fetches timed out; PRIMARY_RETRIEVAL_run001.json records both. Exact official PDF bytes and full text locators were retained. No screenshot-dependent theorem claim or scientific retry occurred.
'''
for name in ('HANDOFF.md','STATUS.md'):
 p=Path(__file__).with_name(name);assert not p.exists();p.write_text(text,encoding='utf-8')
print(json.dumps(receipt))
