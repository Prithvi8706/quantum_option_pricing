from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[3];out=root/'results/independent_110_20261004/H09/run001'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((out/'manifest.json').read_text())
for name,expected in m['files'].items():assert sha(out/name)==expected,name
for name,expected in m['input_pins'].items():assert sha(root/name)==expected,name
assert not (out/'FAILED_UNSEALED.json').exists()
receipt={'passed':True,'fresh_owned_hashes':len(m['files']),'fresh_input_hashes':len(m['input_pins']),
 'manifest_sha256':sha(out/'manifest.json'),'scientific_reruns':0,'physical_integration':False}
dest=out/'HANDOFF_INTEGRITY.json';assert not dest.exists();dest.write_text(json.dumps(receipt,indent=2)+'\n')
text='''H09 bounded initial step completed. Two original72/F40 H17 B4/B8 demand/error rows reconciled. Seven exact capacity boundaries, eight negative allocation/interface controls and one synthetic positive guard passed. Both actual unresolved allocation records were rejected. This does not certify a source allocation or claim storage savings.

The single exact Bravyi2308.07915v1 [[144,12,12]] candidate includes144 data and144 check qubits, unused slots and required connectivity. The capacity-only expression288*ceil(m/12) excludes active arithmetic, factories and interfaces. Original logical totals and private peaks do not reveal measured live storage; original physical caps, conversion/movement bill, topology, idle/feedback exposure and full source-compatible failure remain null. Integration is closed.

Artifacts: research/independent_110_20261004/H09/memory_allocation_audit_v1.py; docs/independent_110_20261004/H09/MEMORY_INTERFACE_AND_LIMITS.txt; results/independent_110_20261004/H09/run001/ with frozen protocol, allocation_records, capacity_only_rows, negative_controls, summary, manifest and fresh HANDOFF_INTEGRITY. One30CPU/60wall/4MiB invocation; all10 input and6 owned hashes freshly matched. No new finance paths, timing, replay, fixture credit, source adoption or quantum advantage.

Retained read failure: PREFLIGHT_PRIMARY_run001.json records the initial default-encoding roadmap read error before any scientific check. No scientific failure or retry occurred. Broader H09 requires original liveness and disjoint allocation, compatible finite storage/active/factory resources, measured conversion schedule, topology, decoder and complete failure/latency/cap accounting. Entire limitation remains open.
'''
for name in ('HANDOFF.md','STATUS.md'):
 p=Path(__file__).with_name(name);assert not p.exists();p.write_text(text,encoding='utf-8')
print(json.dumps(receipt))
