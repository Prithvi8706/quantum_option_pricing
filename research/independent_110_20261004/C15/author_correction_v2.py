"""Author a fresh metadata-only release; preserve failed V1 preparation bytes."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
old=HERE/'citation_audit_v1.py'
raw=old.read_bytes()
failed=ROOT/'results/independent_110_20261004/C15/run001'
failed.mkdir(parents=True)
failure={'schema':'c15-preparation-failure-v1','passed':False,'failure_stage':'Before output mkdir/protocol/accounting or primary retrieval',
    'command':'.context/frontier_t0_env/Scripts/python.exe -B research/independent_110_20261004/C15/citation_audit_v1.py prepare',
    'exit_code':1,'error_type':'ValueError','error':'16MiB local metadata cap','source_sha256':hashlib.sha256(raw).hexdigest(),
    'scientific_checks_executed':0,'protocol_created':False,'source_preserved':True,'budget_increase':False,
    'disposition':'Fresh V2 citation-only metadata corpus omits detailed H17 reports and retains selected summary/provenance/manifest.'}
with (failed/'PREPARATION_FAILED.json').open('x') as f:json.dump(failure,f,indent=2);f.write('\n')
text=raw.decode().replace("C15/run001'","C15/run002'").replace('c15-fixed-next-reference-audit-v1','c15-fixed-next-reference-audit-v2')
for case in ('B4x12','B8x52'):
    text=text.replace("    'results/limitation_program_20261001/H17_demand_run002/"+case+"/hardware_demand.json',\n",'')
text=text.replace("    Path(__file__).resolve().relative_to(ROOT).as_posix(),", "    'research/independent_110_20261004/C15/citation_audit_v1.py',\n    'results/independent_110_20261004/C15/run001/PREPARATION_FAILED.json',\n    Path(__file__).resolve().relative_to(ROOT).as_posix(),")
text=text.replace("'Check selected H17 count metadata and all unresolved physical fields without reexecuting hardware or arithmetic.'", "'Check selected H17 summary/provenance byte membership and unresolved physical fields; detailed report/count closure is not refreshed.'")
text=text.replace("        h17=[]", "        archived_manifest=json.loads((ROOT/'results/limitation_program_20261001/H17_demand_run002/manifest.json').read_bytes())\n        for member in ('summary.json','hardware_provenance.json'):\n            key='results/limitation_program_20261001/H17_demand_run002/'+member\n            require(sha((ROOT/key).read_bytes())==archived_manifest['files'][key], 'Selected archived H17 member SHA')\n        h17=[]")
text=text.replace("            report=json.loads((ROOT/('results/limitation_program_20261001/H17_demand_run002/'+record['case']+'/hardware_demand.json')).read_bytes())\n",'')
text=text.replace("            require(report['case']==record['case'],'Exact report case binding')\n            require(report['logical_qubits']==record['logical_qubits'] and report['consumed_T_states']==record['consumed_T_states']\n                and report['primitive_elementary_gate_count']==record['primitive_elementary_gate_count']\n                and report['native_CCX_positions_before_exact_seven_T_expansion']==record['native_CCX_positions'], 'Selected H17 report/summary exact counts')", "            require(all(type(record[k]) is int and record[k]>0 for k in ('logical_qubits','consumed_T_states','primitive_elementary_gate_count','native_CCX_positions')), 'Recorded integer demand fields; no rederivation')")
ast.parse(text);compile(text,'citation_audit_v2.py','exec')
new=HERE/'citation_audit_v2.py'
with new.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
record={'old_source_sha256':hashlib.sha256(raw).hexdigest(),'new_source_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),
    'changes':['Fresh run002/schemaV2','Remove two large detailed H17 demand reports from frozen citation corpus','Attach selected archived summary/provenance SHA memberships only','Retain original failed source and failure record in corpus'],
    'all_budgets_unchanged':True,'scientific_checks_executed':0,'author_static_compile_passed':True}
with (HERE/'V2_AUTHORING.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(record))
