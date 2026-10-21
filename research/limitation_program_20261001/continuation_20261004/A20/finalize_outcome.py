"""Local metadata notification; admits existing completed evidence without science."""
import argparse
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
START = time.monotonic()
CPU = time.process_time()
PINS = {}


def capture(relative):
    assert time.process_time() - CPU < 60 and time.monotonic() - START < 180
    data = (ROOT / relative).read_bytes()
    PINS[relative] = hashlib.sha256(data).hexdigest()
    return data


def read(relative):
    return json.loads(capture(relative))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--producer-manifest-sha256', required=True)
    parser.add_argument('--audit-manifest-sha256', required=True)
    args = parser.parse_args()
    assert ROOT == Path.cwd().resolve()
    protocol = {
        'schema':'a20-final-outcome-notification-protocol-v1', 'scientific_execution':False,
        'limits_CPU_wall_seconds':[60,180],
        'acceptance':'Externally supplied actual producer/audit manifest pins, matching complete uncensored summaries and root two-pass integrity source bindings; all broad promotion flags remain false.',
        'stop_rule':'Any mismatch rejects PASS notification. Retain all original component/failure/static-review bytes.',
    }
    with (HERE / 'ROOT_OUTCOME_NOTIFICATION_PROTOCOL_run001.json').open('x', encoding='utf-8') as stream:
        json.dump(protocol, stream, indent=2, sort_keys=True)
        stream.write('\n')
    for role, expected in (('producer',args.producer_manifest_sha256), ('audit',args.audit_manifest_sha256)):
        prefix = 'results/limitation_program_20261001/A20_continuation_20261004_' + role + '_run004'
        assert not any((ROOT / prefix / f).exists() for f in ('FAILED_UNSEALED.json','failure.json','run_failure.json','prepare_failure.json'))
        manifest = read(prefix + '/manifest.json')
        assert PINS[prefix + '/manifest.json'] == expected
        summary = read(prefix + '/summary.json')
        assert PINS[prefix + '/summary.json'] == manifest['files']['summary.json']
        assert all(summary[k] is True for k in ('completed','passed','component_semantics_verified'))
        assert summary['budget_censored'] is False and summary['internal_component_checks'] == 2608
        assert summary['offline_native_scalar_evaluations'] == 8
        assert summary['restricted_pair_truth_rows'] == 64 and summary['interface_boundary_cases'] == 10
        assert all(summary[k] == 0 for k in ('new_test_credit','new_gate_replay_credit','new_financial_replay_credit'))
        assert summary['general_full72_or_q32_oracle'] is False and summary['threshold_QSP_transform'] is False
        assert all(summary[k] is False for k in ('full_G2','adoption','quantum_advantage'))
        assert summary['physical_runtime'] is None
        if role == 'audit':
            assert summary['source_manifest_sha256'] == args.producer_manifest_sha256
        root_prefix = 'results/limitation_program_20261001/A20_continuation_20261004_ROOT_' + role + '_integrity_run001'
        assert not (ROOT / root_prefix / 'FAILED_UNSEALED.json').exists()
        root_manifest = read(root_prefix + '/manifest.json')
        report = read(root_prefix + '/verification.json')
        assert PINS[root_prefix + '/verification.json'] == root_manifest['files']['verification.json']
        assert report['passed'] is True and report['completed'] is True and report['budget_censored'] is False
        assert report['source_manifest_sha256'] == expected
        assert len(report['two_uncached_fresh_passes']) == 2
        assert all(r['sha_mismatches'] == 0 and r['inventory_exact'] is True for r in report['two_uncached_fresh_passes'])
        ledger_name = 'resource_ledger.json' if role == 'producer' else 'independent_resource_ledger.json'
        read(prefix + '/' + ledger_name)
        assert PINS[prefix + '/' + ledger_name] == manifest['files'][ledger_name]
    for relative in (
        'results/limitation_program_20261001/A20_continuation_20261004_failure_capture_run001/manifest.json',
        'results/limitation_program_20261001/A20_continuation_20261004_template_diagnostic_run001/manifest.json',
        'research/limitation_program_20261001/continuation_20261004/A20/ROOT_STATIC_REJECTION_v5.json',
        'research/limitation_program_20261001/continuation_20261004/A20/PRODUCER_ROOT_READY_run004.json',
        'research/limitation_program_20261001/continuation_20261004/A20/AUDIT_ROOT_READY_run004.json',
        'docs/limitation_program_20261001/continuation_20261004/A20/HANDOFF_DRAFT_run001.md',
        'docs/limitation_program_20261001/continuation_20261004/A20/author_final_handoff_run001.py',
    ):
        capture(relative)
    capture(Path(__file__).relative_to(ROOT).as_posix())
    capture((HERE / 'ROOT_OUTCOME_NOTIFICATION_PROTOCOL_run001.json').relative_to(ROOT).as_posix())
    notification = {
        'schema':'a20-root-handoff-outcome-v1','notified_by_root':True,'outcome':'PASS',
        'producer_complete':True,'audit_complete':True,'full_fresh_integrity_complete':True,
        'execution_summary':'The distinct V6 producer and separately authored/admitted auditor each completed the unchanged 2608 fixed internal component checks, eight scalar evaluations, 64 table-pair truth rows and ten interface boundary cases. Each sealed outcome is uncensored. ROOT independently checked each entire owned/frozen/external expected union and exact inventory twice with zero mismatches. Completion covers only this restricted native comparator-phase/QROM component. Original V4 remains FAILED_UNSEALED and V5 remains static rejected; ordered source costs are preserved. No general q32 law, threshold transform, full price-source cost, financial G2, adoption or quantum advantage is certified. Process clocks are administrative guard observations during concurrent work.',
        'evidence_sha256':dict(PINS),'A20_status':'partial','full_G2':False,
        'adoption':False,'quantum_advantage':False,'new_fixture_or_financial_replay_credit':0,
    }
    path = HERE / 'ROOT_FINAL_OUTCOME_run001.json'
    with path.open('x', encoding='utf-8') as stream:
        json.dump(notification, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'notification':path.relative_to(ROOT).as_posix(),
                      'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'scientific_execution':False}))


if __name__ == '__main__':
    main()
