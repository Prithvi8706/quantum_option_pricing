"""Assemble local reconciliation metadata from already sealed component evidence."""
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/limitation_program_20261001/continuation_20261004/handoff_run001'
CPU, WALL = time.process_time(), time.monotonic()
INPUTS = {}


def capture(relative):
    assert time.process_time() - CPU < 60 and time.monotonic() - WALL < 180
    path = ROOT / relative
    blob = path.read_bytes()
    INPUTS[relative] = hashlib.sha256(blob).hexdigest()
    return blob


def read(relative):
    return json.loads(capture(relative))


def write(name, value):
    with (OUT / name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def root_packet(name, component_manifest_sha256):
    prefix = 'results/limitation_program_20261001/' + name
    assert not any((ROOT / prefix / f).exists() for f in
                   ('FAILED_UNSEALED.json','FAILED.json','failure.json','run_failure.json','prepare_failure.json'))
    manifest = read(prefix + '/manifest.json')
    verification = read(prefix + '/verification.json')
    assert INPUTS[prefix + '/verification.json'] == manifest['files']['verification.json']
    assert verification['passed'] is True and verification['budget_censored'] is False
    assert verification['completed'] is True
    assert verification['source_manifest_sha256'] == component_manifest_sha256
    assert len(verification['two_uncached_fresh_passes']) == 2
    assert all(r['sha_mismatches'] == 0 and r['inventory_exact'] is True
               for r in verification['two_uncached_fresh_passes'])
    return {'path':prefix, 'manifest_sha256':INPUTS[prefix + '/manifest.json'],
            'passes':verification['two_uncached_fresh_passes'],
            'scope':'Byte/inventory integrity only; no independent runtime-completeness or financial theorem.'}


def completed_packet(name):
    prefix = 'results/limitation_program_20261001/' + name
    assert not any((ROOT / prefix / f).exists() for f in
                   ('FAILED_UNSEALED.json','failure.json','run_failure.json','prepare_failure.json'))
    manifest = read(prefix + '/manifest.json')
    summary = read(prefix + '/summary.json')
    assert INPUTS[prefix + '/summary.json'] == manifest['files']['summary.json']
    assert summary['completed'] is True and summary['passed'] is True and summary['budget_censored'] is False
    assert summary['full_G2'] is False and summary['quantum_advantage'] is False
    return {'path':prefix, 'manifest_sha256':INPUTS[prefix + '/manifest.json'], 'summary':summary}


def main():
    assert ROOT == Path.cwd().resolve() and not OUT.exists()
    OUT.mkdir(parents=True)
    write('protocol.json', {
        'schema':'local-main-chat-reconciliation-protocol-v1', 'scientific_execution':False,
        'limits_CPU_wall_seconds':[60,180],
        'acceptance':'Read already sealed fixed component summaries and root two-pass reports, preserve broad partial/zero credit, hash every selected handoff input; do not rerun science.',
        'stop_rule':'Any inconsistency fails metadata assembly; no promotion or alteration of existing packets.',
        'controller_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    })
    try:
        a13 = read('docs/limitation_program_20261001/continuation_20261004/A13/handoff.json')
        e12 = read('docs/limitation_program_20261001/continuation_20261004/E12/HANDOFF.json')
        review = read('docs/limitation_program_20261001/continuation_20261004/E12/CROSS_ITEM_HANDOFF_REVIEW_run001.json')
        live_note = read('docs/limitation_program_20261001/continuation_20261004/E12/CROSS_ITEM_LIVE_DOCUMENT_NOTE_run001.json')
        assert review['passed'] is True and not review['substantive_mismatches']
        assert live_note['passed'] is True
        assert live_note['original_review_sha256'] == INPUTS[live_note['original_review_path']]
        document = live_note['updated_document']
        live_document = capture(document['path'])
        assert len(live_document) == document['current_bytes']
        assert INPUTS[document['path']] == document['current_sha256']
        assert hashlib.sha256(live_document[:document['old_cross_review_bytes']]).hexdigest() == document['old_cross_review_sha256']
        for key, expected in live_note['unchanged_selected_completed_packet_metadata_and_A14_handoff'].items():
            assert len(capture(key)) == expected['bytes'] and INPUTS[key] == expected['sha256']
        assert a13['QA_counts']['corpora'] == 4681 and a13['QA_counts']['predicate_comparisons'] == 56172
        assert e12['broad_item_completed'] is False and e12['finance_acquisitions'] == 0
        a13prefix = 'results/limitation_program_20261001/A13_continuation_20261004_membership_QA_run001'
        e12prefix = 'results/limitation_program_20261001/E12_continuation_20261004_screen_run001'
        read(a13prefix + '/manifest.json')
        read(e12prefix + '/manifest.json')
        assert INPUTS[a13prefix + '/manifest.json'] == a13['QA_manifest_SHA256']
        assert INPUTS[e12prefix + '/manifest.json'] == e12['component_manifest']['sha256']
        a14producer = completed_packet('A14_continuation_20261004_stage_k_producer_run002')
        a14audit = completed_packet('A14_continuation_20261004_stage_k_audit_run002')
        a20producer = completed_packet('A20_continuation_20261004_producer_run004')
        a20audit = completed_packet('A20_continuation_20261004_audit_run004')
        assert a14audit['summary']['source_manifest_SHA256'] == a14producer['manifest_sha256']
        assert a20audit['summary']['source_manifest_sha256'] == a20producer['manifest_sha256']
        assert a20producer['summary']['internal_component_checks'] == 2608
        assert a20audit['summary']['internal_component_checks'] == 2608
        a20handoff = read('docs/limitation_program_20261001/continuation_20261004/A20/HANDOFF_AUTHOR_RECEIPT_run001.json')
        assert a20handoff['root_reported_outcome'] == 'PASS' and a20handoff['A20_status'] == 'partial'
        assert all(a20handoff[key] is False for key in ('full_G2','adoption','quantum_advantage'))
        for packet in (a20producer, a20audit):
            assert a20handoff['evidence_sha256'][packet['path'] + '/manifest.json'] == packet['manifest_sha256']
        records = {
            'A13':{'status':'partial','completed_scope':'Fixed-snapshot exact metadata membership component and finite QA',
                   'checks':a13['QA_counts'], 'root_integrity':root_packet('A13_continuation_20261004_ROOT_integrity_run001', a13['QA_manifest_SHA256']),
                   'remaining':'Auditor integration, complete audit feasibility, all20 proof/budget closure and any measured improvement.'},
            'A14':{'status':'partial','completed_scope':'Signed52x38 F44 multiplier and signed72 ties-even rounder primitives',
                   'producer':a14producer, 'audit':a14audit, 'fixed_diagnostics':88,
                   'root_producer_integrity':root_packet('A14_continuation_20261004_ROOT_producer_integrity_run001', a14producer['manifest_sha256']),
                   'root_audit_integrity':root_packet('A14_continuation_20261004_ROOT_audit_integrity_run001', a14audit['manifest_sha256']),
                   'remaining':'All448 true coefficient enclosures, cosine uniform bound, caller ranges, full new source and financial/cost certification.'},
            'A20':{'status':'partial','completed_scope':'Restricted native comparator-phase/QROM component with separate independent construction/checker',
                   'producer':a20producer, 'audit':a20audit, 'internal_component_checks_each':2608,
                   'root_producer_integrity':root_packet('A20_continuation_20261004_ROOT_producer_integrity_run001', a20producer['manifest_sha256']),
                   'root_audit_integrity':root_packet('A20_continuation_20261004_ROOT_audit_integrity_run001', a20audit['manifest_sha256']),
                   'semantic_sharing_implies_ordered_source_cost_equivalence':False,
                   'prior_failed_V4_remains_FAILED_UNSEALED':True, 'V5_remains_static_rejected':True,
                   'remaining':'General full72/q32 access/law, table scaling, tiny threshold gap, paid phase-clean threshold transform, full price-source G2/bias/cost and physical delivery.'},
            'E12':{'status':'partial','completed_scope':'Conservative iid dyadic empirical-Bernstein component; fixed finance rule rejected before acquisition',
                   'toy_attempts':384,'toy_target_failures_retained':128,'finite_oracle_families':7,
                   'finance_floor_dollars_squared':e12['finance_all_20_look_minimum_lower_floor_dollars_squared'],
                   'finance_target_dollars_squared':e12['finance_target_dollars_squared'], 'finance_acquisitions':0,
                   'root_integrity':root_packet('E12_continuation_20261004_ROOT_integrity_run001', e12['component_manifest']['sha256']),
                   'remaining':'Sharper preregistered sequence or larger-moment/complete-latency tradeoff, finance sampling law and complete runtime/acquisition certification.'},
        }
        reservation = read('.context/parallel_110_chat_reservation_20261004.json')
        assert reservation['main_chat_reserved_items'] == ['A13','A14','A20','E12']
        assert reservation['separate_chat_suggested_items_in_order'] == ['F31','F03','F32']
        result = {'schema':'main-chat-continuation-handoff-v1','local_metadata_complete':True,
                  'items':records,'secondary_items_reserved':['F31','F03','F32'],
                  'shared_progress_STATUS_README_manuscript_edited':False,
                  'global_new_pytest_financial_fixture_gate_replay_financial_replay_credit':0,
                  'full_G2':False,'adoption':False,'quantum_advantage':False,
                  'matched_performance_measured':False,'physical_runtime':None,
                  'cross_item_review_scope':'Point-in-time handoff/evidence review; additive note retains later A14 live STATUS append without changing completed packets.',
                  'handoff_directory':'docs/limitation_program_20261001/continuation_20261004',
                  'metadata_assembly_CPU_seconds':time.process_time()-CPU,
                  'metadata_assembly_wall_seconds':time.monotonic()-WALL}
        write('handoff.json',result)
        owned = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}
        write('manifest.json',{'schema':'local-handoff-integrity-manifest-v1','files':owned,
                              'frozen_inputs':INPUTS,'self_hash_excluded':True,'metadata_only':True,
                              'scientific_execution':False,'new_test_credit':0})
        print(json.dumps({'passed':True,'output':OUT.relative_to(ROOT).as_posix(),
                          'items_broad_status':'all partial','scientific_execution':False}))
    except BaseException as exc:
        write('FAILED_UNSEALED.json',{'passed':False,'metadata_only':True,'error':repr(exc)})
        raise


if __name__ == '__main__':
    main()
