"""Local status only; shared progress remains read-only and scope explicit."""
from pathlib import Path
import csv
import json
import hashlib
import datetime

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/independent_110_20261004'
CSV=ROOT/'docs/independent_110_20261004/inventory_run001/INDEPENDENT_FIRST_STEPS.csv'
COMPLETED={
 'C05':('C05/run001','Three mathematical allocation rows; retain original split; no full delivery.'),
 'C12':('C12/audit_run002','Existing evidence-family/shared-module audit; no new independent backend.'),
 'E08':('E08/run004','20candidate fixed-geometry logical-call screen under archived promises; no physical or financial adoption.'),
 'E17':('E17/audit_run001','One moment/relevance audit; corrected additive citation overlay; uncapped Heston/weights unresolved.'),
 'F08':('F08/run001','Finite tilted identity/rounding and normalization first screen; broader prep/cost obligation unresolved.'),
 'F13':('F13/run001','One S4 theorem plus one transform audit; rejected transfer, not a universal antithetic no-go.'),
 'F16':('F16/run001','Ideal GBM future-factor reuse audit; finite-law and confidence bridges unresolved.'),
 'F18':('F18/run001','One contract/theorem/error-norm/access map; practical theorem transfer closed on missing interfaces.'),
 'C15':('C15/run002','169 versioned claim rows; numerical hardware/compiled-time transfers remain unverified.'),
 'E01':('E01/audit_run001','Original-source Sobol access audit; finite input-law equivalence and coherent cost remain unresolved.'),
 'E15':('E15/run002','Two reversible coherent inner toys and measured-record rejection; no financial inner estimator.'),
 'F15':('F15/run001','Nominal continuous A1 upper-state tail proof; cutoff bound below standalone allowance; loader and transition implementation unresolved.'),
 'F23':('F23/screen_run001','Six covariance ranks and eighteen band certificates; no certified bias-screen pass, retain full rank.'),
 'F11':('F11/run001','Two existing A4 control expectation/conditioning proofs; training-inclusive matched performance and retuning held.'),
 'F12':('F12/run001','S4 positivity and one boundary-adapted coupling preflight at four levels; full payoff bias and matched variance/cost remain unresolved.'),
 'F14':('F14/run001','Original A1 endpoint and negative-leverage primitive inventory; conditional integral inverse certificate missing, transition pilot stopped.'),
 'F17':('F17/run001','Three fixed-policy boundary widths and exact regret-envelope checks; population certification unavailable, localization closed.'),
 'E20':('E20/run001','Necessary original-source parallel-lane accounting: assumed bare P2 memory exceeds cap; finite QSP and physical performance unresolved.'),
 'E09':('E09/controller_run001','Exact finite support fallback/readout controller checked; unknown-variance reduction constants, emitted gates and finance costs remain unresolved.'),
 'E14':('E14/run002','Three-error deterministic D1 schedule/convention audit with corrected unclipped moment bounds; finite coherent QAMC and same-contract cost comparison remain unresolved.'),
 'H07':('H07/run001','Logical protected-adder gate-set and cleanup/inverse audit; actual cat noise, correction and duration interfaces remain unresolved.'),
 'H09':('H09/run001','One finite memory candidate and capacity audit; both original source allocations reject missing liveness/cap/conversion; no savings.'),
 'E16':('E16/scalar_run001','Six conditional scalar moment/cap/weighted finite-law rows; loading/arithmetic/synthesis and complete quantile constants remain unresolved.'),
 'F24':('F24/run001','Original D1 two-date backward formulation and two prescribed grids; finite stability passes, global price bias and quantum delivery remain unresolved.'),
 'F25':('F25/run001','Original D1 forward normalization/overlap proof and two conditional readout ledgers; mass, state/control error, continuous price bias and full costs remain unresolved.'),
 'H11':('H11/run001','One finite addressable-CCZ parameter bill and original leaf ideal gate interface; stabilizers/Clifford/noisy-CCZ implementations remain unresolved.'),
 'H12':('H12/run001','Versioned constant-overhead construction and finite-width audit; actual constants/code lengths and full compatible estimator compilation remain unresolved.'),
 'H13':('H13/run001','Original multiplier/chain component-block registries and ideal idle accounting; oriented topology/factory/reaction/full physical schedule remains unresolved.'),
 'E25':('E25/amplitude_run001','One finite adaptive amplitude design and continuous ideal-law likelihood coverage wrapper; all18 truths remain uncertified at cap, noise/full-cost/adoption unresolved.'),
 'F10':('F10/allocation_run001','All768 archived-menu conditional hybrid assignments with exact native/DP accounting; six legacy fixed free-correction floors rejecttenfold; population/full-cost/99percent delivery remain unresolved.'),
 'F30':('F30/seal_recovery_run001','One original D1 three-rank diagnostic; failed original seal preserved and actual outputs bound by independently verified metadata-only recovery. Validation, loading, original-price certification and complete costs remain unresolved.'),
}
STOPPED={'H03':('H03/run001/failure_manifest.json','Sole reaction-map invocation hit the frozen CPU cap; partial artifacts retained, no completed-map or physical credit.')}
ACTIVE=set()
rows=[]
for row in csv.DictReader(CSV.open(newline='',encoding='utf-8-sig')):
    item=row['item']
    status='active' if item in ACTIVE else 'queued'
    receipt=None;scope=row['independent_scope_or_hold_reason']
    if item in COMPLETED:
        rel,scope=COMPLETED[item];run=BASE/rel
        assert (run/'manifest.json').exists() and not any('fail' in p.name.lower() for p in run.iterdir())
        status='completed_scoped';receipt=str((run/'manifest.json').relative_to(ROOT)).replace('\\','/')
    if item in STOPPED:
        relative,scope=STOPPED[item];path=BASE/relative
        assert path.exists() and (path.parent/'FAILED.json').exists() and not (path.parent/'SUCCESS.json').exists()
        status='failed_stopped';receipt=str(path.relative_to(ROOT)).replace('\\','/')
    rows.append({'item':item,'title':row['title'],'execution_status':status,'scope':scope,'receipt_manifest':receipt,
                 'entire_limitation_declared_solved':False,'quantum_advantage':False,'new_global_fixture_credit':0})
assert len(rows)==32 and len({r['item'] for r in rows})==32
counts={s:sum(r['execution_status']==s for r in rows) for s in ['completed_scoped','failed_stopped','active','queued']}
live=json.loads((ROOT/'results/limitation_program_20261001/progress.json').read_text())
result={'schema':'local-independent-checklist-progress-v1','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'checklist_csv_sha256':hashlib.sha256(CSV.read_bytes()).hexdigest(),'counts':counts,'entries':rows,
 'protected_elsewhere':['A13','A14','A20','E12','F31','F03','F32'],
 'live_shared_active_items_read_only':live.get('active_items'),
 'shared_progress_written':False,'global_fixture_credit_added':0,'financial_contract_changed':False,
 'completed_means':'Named bounded audit/screen only; each handoff preserves broader unresolved obligations.',
 'holds':'Prerequisite, timing, semantic overlap and new-contract holds remain as inventory_run001.'}
(BASE/'checklist_progress.json').write_text(json.dumps(result,indent=2)+'\n')
status_lines=['# Independent implementation-plan checklist','',
 'This chat follows [the dated work list](inventory_run001/WORK_LIST.txt). A13, A14, A20, E12, F31, F03 and F32 remain reserved elsewhere. Shared files and progress are read-only. All results below are isolated local handoffs.','',
 f"Current bounded-step counts: {counts['completed_scoped']} completed, {counts['failed_stopped']} failed and stopped, {counts['active']} active, {counts['queued']} queued. Completion here applies only to the stated audit or screen, not the entire limitation.",'',
 '| Item | Local status | Exact scope |','| --- | --- | --- |']
for row in rows:
    scope=row['scope'].replace('|','/')
    if row['receipt_manifest']:
        receipt='../../'+row['receipt_manifest']
        label='[Failed; stopped]('+receipt+')' if row['execution_status']=='failed_stopped' else '[Bounded step complete]('+receipt+')'
    else:label=row['execution_status'].capitalize()
    status_lines.append(f"| {row['item']} | {label} | {scope} |")
status_lines += ['', 'No financial contract or shared error allocation changed. No concurrent matched timing, new global fixture credit, whole-limitation completion or quantum advantage is claimed. Prerequisite, timing, overlap and new-contract holds in the inventory remain in force.', '',
 'Root metadata verification receipts: '+', '.join(f'[run{i:03d}](../../results/independent_110_20261004/handoff_integrity_run{i:03d}/verification.json)' for i in [1,2,3,4,5,7,8])+'. These checks verify artifact integrity; they do not repeat scientific experiments. The failed [run006](../../results/independent_110_20261004/handoff_integrity_run006/FAILED.json) inventory attempt is retained; run007 explicitly pins postseal administrative overlays without changing science receipts. Run008 binds the final E25, F10 and F30 receipts. F30 retains its invalid original seal and uses a separately reviewed metadata recovery to bind the unchanged scientific outputs.', '',
 'Static and failed attempts are retained in their original directories. The original chat will reconcile these handoffs into shared progress.']
(ROOT/'docs/independent_110_20261004/STATUS.md').write_text('\n'.join(status_lines)+'\n',encoding='utf-8')
print(json.dumps({'items':len(rows),'counts':counts,'shared_progress_written':False}))
