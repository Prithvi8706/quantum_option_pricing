"""Reconcile completed components and retained failed audit; metadata only."""
import hashlib
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[3]
CONTROLLER = Path(__file__).with_name('assemble_handoff.py')
spec = importlib.util.spec_from_file_location('_local_handoff_metadata', CONTROLLER)
meta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meta)  # This author module defines metadata helpers only.


def main():
    assert ROOT == Path.cwd().resolve() and not meta.OUT.exists()
    meta.OUT.mkdir(parents=True)
    meta.write('protocol.json', {
        'schema':'local-partial-reconciliation-protocol-v1','scientific_execution':False,
        'limits_CPU_wall_seconds':[60,180],
        'acceptance':'Bind completed A13/A14/E12 evidence and A20 producer to full root integrity; bind failed A20 audit to complete metadata-only failure retention. No independent audit PASS, no unknown-to-zero substitution.',
        'stop_rule':'Any evidence inconsistency fails metadata assembly; preserve old sources, failures and expectations.',
        'controller_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    })
    try:
        meta.capture(Path(__file__).relative_to(ROOT).as_posix())
        meta.capture(CONTROLLER.relative_to(ROOT).as_posix())
        a13 = meta.read('docs/limitation_program_20261001/continuation_20261004/A13/handoff.json')
        e12 = meta.read('docs/limitation_program_20261001/continuation_20261004/E12/HANDOFF.json')
        review_path = 'docs/limitation_program_20261001/continuation_20261004/E12/CROSS_ITEM_HANDOFF_REVIEW_run001.json'
        review = meta.read(review_path)
        note = meta.read('docs/limitation_program_20261001/continuation_20261004/E12/CROSS_ITEM_LIVE_DOCUMENT_NOTE_run001.json')
        assert review['passed'] is True and not review['substantive_mismatches']
        assert note['passed'] is True and note['original_review_sha256'] == meta.INPUTS[review_path]
        doc = note['updated_document']
        current = meta.capture(doc['path'])
        assert len(current) == doc['current_bytes'] and meta.INPUTS[doc['path']] == doc['current_sha256']
        assert hashlib.sha256(current[:doc['old_cross_review_bytes']]).hexdigest() == doc['old_cross_review_sha256']
        for path, expected in note['unchanged_selected_completed_packet_metadata_and_A14_handoff'].items():
            assert len(meta.capture(path)) == expected['bytes'] and meta.INPUTS[path] == expected['sha256']
        assert a13['QA_counts']['corpora'] == 4681 and a13['QA_counts']['predicate_comparisons'] == 56172
        assert e12['broad_item_completed'] is False and e12['finance_acquisitions'] == 0
        a14producer = meta.completed_packet('A14_continuation_20261004_stage_k_producer_run002')
        a14audit = meta.completed_packet('A14_continuation_20261004_stage_k_audit_run002')
        assert a14audit['summary']['source_manifest_SHA256'] == a14producer['manifest_sha256']
        a20producer = meta.completed_packet('A20_continuation_20261004_producer_run004')
        assert a20producer['summary']['internal_component_checks'] == 2608
        a20doc = meta.read('docs/limitation_program_20261001/continuation_20261004/A20/HANDOFF_AUTHOR_RECEIPT_run001.json')
        assert a20doc['root_reported_outcome'] == 'FAILED' and a20doc['A20_status'] == 'partial'
        assert all(a20doc[k] is False for k in ('full_G2','adoption','quantum_advantage'))
        assert a20doc['evidence_sha256'][a20producer['path'] + '/manifest.json'] == a20producer['manifest_sha256']
        capture_prefix = 'results/limitation_program_20261001/A20_continuation_20261004_audit_failure_capture_run001'
        failed_capture = meta.read(capture_prefix + '/manifest.json')
        retained = meta.read(capture_prefix + '/verification.json')
        assert meta.INPUTS[capture_prefix + '/verification.json'] == failed_capture['files']['verification.json']
        assert not (ROOT / capture_prefix / 'FAILED_UNSEALED.json').exists()
        assert retained['passed'] is True and retained['integrity_only'] is True
        assert retained['original_audit_passed'] is False and retained['original_failed_unsealed_authoritative'] is True
        assert retained['original_budget_censored'] is None and retained['completed_audit_component_checks'] is None
        assert len(retained['two_fresh_union_checks']) == 2 and all(r['mismatches'] == 0 and r['failed_source_inventory_exact'] is True for r in retained['two_fresh_union_checks'])
        assert a20doc['evidence_sha256'][capture_prefix + '/manifest.json'] == meta.INPUTS[capture_prefix + '/manifest.json']
        source = 'results/limitation_program_20261001/A20_continuation_20261004_audit_run004'
        marker = meta.read(source + '/FAILED_UNSEALED.json')
        error = meta.read(source + '/failure.json')
        assert meta.INPUTS[source + '/FAILED_UNSEALED.json'] == a20doc['evidence_sha256'][source + '/FAILED_UNSEALED.json']
        assert meta.INPUTS[source + '/failure.json'] == a20doc['evidence_sha256'][source + '/failure.json']
        assert marker['authoritative_failure'] is True and marker['hard_budget_state_uncertified'] is True
        assert marker['budget_censored'] is None and not (ROOT / source / 'manifest.json').exists()
        assert error['message'] == 'Fixed A20 process CPU/wall guard'
        for path, expected in ((a13['QA_receipt'] + '/manifest.json', a13['QA_manifest_SHA256']),
                               (e12['component_manifest']['path'],e12['component_manifest']['sha256'])):
            meta.read(path)
            assert meta.INPUTS[path] == expected
        items = {
            'A13':{'status':'partial','completed_scope':'Fixed-snapshot metadata membership predicate component and finite QA',
                   'checks':a13['QA_counts'],'root_integrity':meta.root_packet('A13_continuation_20261004_ROOT_integrity_run001',a13['QA_manifest_SHA256']),
                   'remaining':'Auditor integration, full audit feasibility and all20 proof/budget closure; no measured improvement.'},
            'A14':{'status':'partial','completed_scope':'Signed52x38 F44 multiplier and signed72 ties-even rounder primitives',
                   'producer':a14producer,'audit':a14audit,'fixed_diagnostics':88,
                   'root_producer_integrity':meta.root_packet('A14_continuation_20261004_ROOT_producer_integrity_run001',a14producer['manifest_sha256']),
                   'root_audit_integrity':meta.root_packet('A14_continuation_20261004_ROOT_audit_integrity_run001',a14audit['manifest_sha256']),
                   'remaining':'448coefficients, cosine uniform bound, caller ranges, full source and financial/cost certification.'},
            'A20':{'status':'partial','completed_scope':'Restricted comparator-phase/QROM producer and full producer packet integrity; complete retention of failed independent attempt',
                   'producer':a20producer,'producer_internal_component_checks':2608,
                   'root_producer_integrity':meta.root_packet('A20_continuation_20261004_ROOT_producer_integrity_run001',a20producer['manifest_sha256']),
                   'audit':{'path':source,'outcome':'FAILED_UNSEALED','budget_censored':None,
                            'hard_budget_state_uncertified':True,'completed_component_checks':None,'error':error},
                   'audit_failure_retention':{'path':capture_prefix,'manifest_sha256':meta.INPUTS[capture_prefix + '/manifest.json'],
                                             'two_fresh_union_checks':retained['two_fresh_union_checks']},
                   'component_fully_audited':False,'ordered_source_cost_equivalence':False,
                   'remaining':'Cold complete independent audit under unchanged caps; general full72/q32 law/access, table scaling, threshold gap/transform, full price-source G2/bias/cost and physical delivery.'},
            'E12':{'status':'partial','completed_scope':'Conservative iid dyadic empirical-Bernstein component; fixed finance rule rejected before acquisition',
                   'toy_attempts':384,'toy_target_failures_retained':128,'finite_oracle_families':7,
                   'finance_floor_dollars_squared':e12['finance_all_20_look_minimum_lower_floor_dollars_squared'],
                   'finance_target_dollars_squared':e12['finance_target_dollars_squared'],'finance_acquisitions':0,
                   'root_integrity':meta.root_packet('E12_continuation_20261004_ROOT_integrity_run001',e12['component_manifest']['sha256']),
                   'remaining':'Sharper preregistered sequence or larger-moment/complete-latency tradeoff, finance law and full acquisition/runtime certification.'},
        }
        reservation = meta.read('.context/parallel_110_chat_reservation_20261004.json')
        assert reservation['main_chat_reserved_items'] == ['A13','A14','A20','E12']
        assert reservation['separate_chat_suggested_items_in_order'] == ['F31','F03','F32']
        result = {'schema':'main-chat-partial-continuation-handoff-v1','local_metadata_complete':True,
                  'items':items,'secondary_items_reserved':['F31','F03','F32'],
                  'this_continuation_edited_shared_progress_STATUS_README_manuscript':False,
                  'this_continuation_new_global_fixture_or_financial_replay_credit':0,
                  'full_G2':False,'adoption':False,'quantum_advantage':False,
                  'matched_performance_measured':False,'physical_runtime':None,
                  'handoff_directory':'docs/limitation_program_20261001/continuation_20261004',
                  'metadata_assembly_CPU_wall_seconds':[time.process_time()-meta.CPU,time.monotonic()-meta.WALL]}
        meta.write('handoff.json',result)
        owned = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in meta.OUT.iterdir() if p.is_file()}
        meta.write('manifest.json',{'files':owned,'frozen_inputs':meta.INPUTS,'self_hash_excluded':True,
                                  'metadata_only':True,'scientific_execution':False,'new_test_credit':0})
        print(json.dumps({'passed':True,'output':meta.OUT.relative_to(ROOT).as_posix(),
                          'items_broad_status':'all partial','A20_audit_failed':True,'scientific_execution':False}))
    except BaseException as exc:
        meta.write('FAILED_UNSEALED.json',{'passed':False,'metadata_only':True,'error':repr(exc)})
        raise


if __name__ == '__main__':
    main()
