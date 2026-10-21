"""Assemble final bounded-checklist handoff from sealed receipts; metadata only."""
from pathlib import Path
import datetime
import hashlib
import json

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/independent_110_20261004'
OUT=BASE/'handoff_run001'
DOC=ROOT/'docs/independent_110_20261004/HANDOFF.txt'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    assert not OUT.exists() and not DOC.exists(),'Fresh handoff only'
    progress=json.loads((BASE/'checklist_progress.json').read_text())
    assert progress['counts']=={'completed_scoped':31,'failed_stopped':1,'active':0,'queued':0}
    verification_paths=[BASE/f'handoff_integrity_run{i:03d}/verification.json' for i in [1,2,3,4,5,7,8]]
    checks=[json.loads(p.read_text()) for p in verification_paths]
    assert all(v['passed'] and v.get('mismatches',0)==0 for v in checks)
    verified_manifests={}
    for verification in checks:
        for receipt in verification['receipts']:
            wanted=receipt.get('expected_sha256',receipt.get('sha256',receipt.get('manifest_sha256')))
            assert wanted and sha(ROOT/receipt['manifest'])==wanted,'Final manifest no longer matches root verification'
            verified_manifests[receipt['item']]=receipt['manifest']
    assert set(verified_manifests)=={row['item'] for row in progress['entries']},'Every checklist receipt must have root verification'
    receipt_rows=[]
    for row in progress['entries']:
        p=ROOT/row['receipt_manifest'];assert p.exists()
        assert row['receipt_manifest']==verified_manifests[row['item']], 'Checklist receipt must be the verified manifest'
        receipt_rows.append({**row,'receipt_sha256':sha(p)})
    assert {r['item'] for r in receipt_rows}==set(r['item'] for r in progress['entries'])
    protected=set(progress['protected_elsewhere'])
    assert not protected.intersection(r['item'] for r in receipt_rows)
    owned_roots=[BASE,ROOT/'research/independent_110_20261004',ROOT/'docs/independent_110_20261004']
    retained=[str(p.relative_to(ROOT)).replace('\\','/') for owned in owned_roots for p in owned.rglob('*')
              if p.is_file() and any(tag in p.name.lower() for tag in ['fail','hold','reject'])]
    OUT.mkdir()
    packet={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'counts':progress['counts'],'entries':receipt_rows,'retained_failure_or_hold_artifacts':sorted(retained),
      'all32_receipt_manifests_bound_to_root_verification':True,
      'retained_marker_inventory_scope':'Named fail/hold/reject markers under all three owned namespaces; not an exhaustive lineage of every rejected finite row, control or static review.',
      'root_integrity_receipts':[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),
         'scope':'Artifact/input hash and inventory verification; not an independent scientific replication.'} for p in verification_paths],
      'protected_elsewhere':sorted(protected),'shared_progress_written':False,'global_fixture_credit_added':0,
      'all_110_limitations_completed':False,'whole_limitation_completion_claimed':False,
      'financial_contract_changed':False,'concurrent_matched_timings_claimed':False,'quantum_advantage_claimed':False,
      'completion_scope':'Each of the 32 named independent initial steps reached its fixed stopping rule. 31 scoped audits/screens have verified artifact bindings; H03 stopped at the prospective CPU cap with failure preserved. F30 uses a metadata-only recovery binding its unchanged scientific outputs, with the invalid original seal retained. Broader obligations stay in individual proofs and handoffs.'}
    (OUT/'summary.json').write_text(json.dumps(packet,indent=2)+'\n',encoding='utf-8')
    lines=['Independent implementation-plan checklist handoff,2026-10-04','',
      'All 32 selected independent initial steps reached their bounded stopping rules: 31 scoped audits/screens with verified artifact bindings and one retained failed/stopped H03 invocation. This is not completion of 32 entire limitations or of the 110-item plan. Shared source, progress, STATUS, README and manuscript were not edited by this work. A13, A14, A20, E12, F31, F03 and F32 remain reserved elsewhere.','',
      'Artifacts: docs/independent_110_20261004/STATUS.md contains the complete item table and exact scope links. results/independent_110_20261004/handoff_run001/summary.json binds all32 manifest paths and hashes, retained failures/holds, and root integrity receipts. Sources are under research/independent_110_20261004; proofs, primary-source provenance, static reviews and individual handoffs are under docs/independent_110_20261004 and the corresponding research item directories.','',
      'Checks: prospective corpus/assumptions/acceptance/budget/stopping packets; item-specific exact algebra, outward enclosures, metadata reconciliation, finite-control and prescribed development diagnostics. Root integrity runs001-005,007-008 verify hashes and receipt inventories; they do not repeat experiments or add independent fixture credit. Run006 retained a metadata inventory failure because postseal administrative overlays were not listed in scientific manifests; fresh007 verifies these overlays using explicit expected hashes without changing scientific receipts. No combined independent-test count is asserted. H03 hit its frozen CPU cap; partial output and failure authority remain preserved, with no completed-map credit or cap-raising retry.','',
      'F30 provenance: one scientific rank-screen invocation was completed. Its original seal failed because SUCCESS.json was hashed as LF bytes but written with CRLF bytes. The invalid manifest and every original output remain preserved. A fresh, independently reviewed metadata-only recovery binds the actual bytes and matches a manifest hash predicted before recovery execution. The corrected HANDOFF_RECOVERY_run001.md explicitly withdraws the original handoff sentence that incorrectly claimed seal verification. No scientific work was rerun or credited by recovery.','',
      'Concrete findings: original allocation changes and covariance truncations did not produce an eligible certified improvement. The nominal negative-leverage A1 upper-tail certificate passes its standalone allowance but does not complete finite loading or transitions. Scalar capped/weighted bounds and logical coherent/toy/gate-interface checks pass their stated conditions; state loading, arithmetic, confidence constants and complete physical delivery remain unpaid where missing. D1 PDE/tensor diagnostics retain global truncation/event/floating bias obligations. Hardware construction/code/gadget component bills retain finite implementation, topology, noise, factories, idles, reaction, controller and readout obligations. None is a demonstrated quantum-advantage result.','',
      'Exact item completion scopes:']
    for row in receipt_rows:
        lines.append(f"{row['item']}: {row['execution_status']}. {row['scope']} Receipt: {row['receipt_manifest']} SHA256{row['receipt_sha256']}.")
    lines+=['','Reconciliation obligations: the original chat must independently decide which scoped findings merit changes to shared progress. Prerequisite, timing, semantic-overlap and new-contract holds from inventory_run001 remain. No existing test was credited again and no whole limitation was declared solved after one component. Continued work requires the unresolved certificates/interfaces identified in each individual proof, subject to their explicit stopping rules.']
    DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    files=[OUT/'summary.json',DOC,BASE/'checklist_progress.json',ROOT/'docs/independent_110_20261004/STATUS.md']
    (OUT/'manifest.json').write_text(json.dumps({'files':{str(p.relative_to(ROOT)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files},
       'author_sha256':sha(Path(__file__))},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'counts':progress['counts'],'manifest_sha256':sha(OUT/'manifest.json'),'shared_progress_written':False}))

if __name__=='__main__':main()
