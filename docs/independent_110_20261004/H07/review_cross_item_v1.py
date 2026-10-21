"""Write read-only static peer reviews; do not import or run audited modules."""
from pathlib import Path
import ast,hashlib,json
root=Path(__file__).resolve().parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
specs={
 'H12':('finite_constants_audit_v1.py',[
  'Integer bit_length lower-product construction matches ceil/floor log identities and increasing factors at lambda_Y>=1.',
  'Width hypothesis is C_F*F(n), not n*F(n); unknown constants and usable length stay null.',
  'Source-only serialized H-CCZ-H depth is a logical upper under existing connectivity and is not full estimator D or physical seconds.',
  'Reporting correction before freeze distinguishes one actual missing-input rejection and one finite C_F witness from eight documentary flags.'
 ]),
 'H13':('active_volume_audit_v1.py',[
  'Ordered component registry binds original native wire IDs to primary four-block CNOT/twelve-block generic Toffoli; complete port topology and routing are not claimed.',
  'Compute-copy-inverse source binding preserves original signed72/F40 and compact source argument-copy obligations; original leaf arithmetic is assumed from existing evidence, not newly replayed.',
  'Known subtotals180712/379024 retain missing factories/frame/preparation/routing and do not become complete active volume.',
  'Ideal all-to-all W*D minus gate arity touches is a specified wire-layer diagnostic, not physical dwell/code cycles.',
  'Isolated reaction depth1 is not chain reaction depth. No temporary-AND or incompatible factory assumption is adopted.',
  'W+3+6 is correctly relabeled a declared conservative serial reservation; simultaneous CCZ/reactive-output liveness is not certified.',
  'Root selected Python3.12.4 launcher supports zip strict. Default Python3.9 is unsuitable and was not authorized for this packet.',
  'Thirteen missing-field inputs actually call the admission guard and reject; real physical inputs remain null.'
 ])}
for item,(author,findings) in specs.items():
 proto=root/f'results/independent_110_20261004/{item}/run001/protocol.json'
 p=json.loads(proto.read_text());pins=p['input_pins']
 for name,v in pins.items():assert sha(root/name)==v['sha256'],name
 source=root/f'research/independent_110_20261004/{item}/{author}'
 ast.parse(source.read_text())
 raw=source.read_text()
 if item=='H12':assert 'documentary_interface_flags_count' in raw and 'executed_missing_input_rejections' in raw
 else:assert 'simultaneous_CCZ_and_reactive_output_liveness_certified' in raw and 'declared_serial_CCZ_and_reactive_output_memory_reservation' in raw
 receipt={'item':item,'disposition':'STATIC_REVIEW_PASS_FOR_ONE_FROZEN_BOUNDED_RUN',
  'reviewed_sha256':{name:v['sha256'] for name,v in pins.items()},'protocol_sha256':sha(proto),
  'fresh_frozen_pins_match':True,'source_imports':0,'scientific_invocations':0,
  'findings':findings,'entire_limitation_solved':False,'physical_architecture_admitted':False,'new_fixture_credit':0,
  'review_scope':'Static source/proof/primary-locator audit only; no executed-result approval or scientific rerun.'}
 if item=='H13':receipt['selected_launcher_sha256']=sha(root/'.context/frontier_t0_env/Scripts/python.exe')
 dest=root/f'docs/independent_110_20261004/{item}/STATIC_REVIEW_run001.json'
 assert not dest.exists();dest.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'item':item,'review':dest.relative_to(root).as_posix(),'sha256':sha(dest)}))
