"""Record retained failed audit alongside completed producer; metadata only."""
import argparse
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
CPU, WALL = time.process_time(), time.monotonic()
PINS = {}


def capture(path):
    assert time.process_time()-CPU < 60 and time.monotonic()-WALL < 180
    data = (ROOT / path).read_bytes()
    PINS[path] = hashlib.sha256(data).hexdigest()
    return data


def read(path):
    return json.loads(capture(path))


def save(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--failure-capture-manifest-sha256',required=True)
    args = parser.parse_args()
    assert ROOT == Path.cwd().resolve()
    protocol = HERE / 'ROOT_FAILED_NOTIFICATION_PROTOCOL_run001.json'
    save(protocol, {'schema':'a20-failed-outcome-notification-protocol-v1','scientific_execution':False,
        'limits_CPU_wall_seconds':[60,180],
        'acceptance':'Exact retained completed producer and root integrity pins; exact full failed-audit capture pin, owned failure markers and two fresh complete failed-map/inventory checks. No partial audit approval.',
        'stop_rule':'Any mismatch prevents notification; do not retry science, increase caps or convert null fields to zero.'})
    producer = 'results/limitation_program_20261001/A20_continuation_20261004_producer_run004'
    manifest = read(producer + '/manifest.json')
    assert PINS[producer + '/manifest.json'] == 'af0ec4aaecc0a48e296840350017414f4e6f263d9f2a36ef61e98114cc848c31'
    summary = read(producer + '/summary.json')
    assert PINS[producer + '/summary.json'] == manifest['files']['summary.json']
    assert summary['completed'] is True and summary['passed'] is True and summary['budget_censored'] is False
    assert summary['internal_component_checks'] == 2608
    root = 'results/limitation_program_20261001/A20_continuation_20261004_ROOT_producer_integrity_run001'
    root_manifest = read(root + '/manifest.json')
    assert PINS[root + '/manifest.json'] == '56f824653f1bfa2e33a9dce89a37a65032c1c351c5a52b8061eb17001a4bf28b'
    report = read(root + '/verification.json')
    assert PINS[root + '/verification.json'] == root_manifest['files']['verification.json']
    assert report['passed'] is True and report['completed'] is True and report['budget_censored'] is False
    assert report['source_manifest_sha256'] == PINS[producer + '/manifest.json']
    assert len(report['two_uncached_fresh_passes']) == 2 and all(p['sha_mismatches'] == 0 and p['inventory_exact'] is True for p in report['two_uncached_fresh_passes'])
    retained = 'results/limitation_program_20261001/A20_continuation_20261004_audit_failure_capture_run001'
    retained_manifest = read(retained + '/manifest.json')
    assert PINS[retained + '/manifest.json'] == args.failure_capture_manifest_sha256
    assert not (ROOT / retained / 'FAILED_UNSEALED.json').exists()
    retention = read(retained + '/verification.json')
    inventory = read(retained + '/failed_source_owned_inventory.json')
    for name in ('verification.json','failed_source_owned_inventory.json'):
        assert PINS[retained + '/' + name] == retained_manifest['files'][name]
    assert retention['passed'] is True and retention['integrity_only'] is True
    assert retention['original_audit_passed'] is False and retention['original_failed_unsealed_authoritative'] is True
    assert retention['original_hard_budget_state_uncertified'] is True and retention['published_independent_group_files'] == 0
    assert retention['original_budget_censored'] is None and retention['completed_audit_component_checks'] is None
    assert len(retention['two_fresh_union_checks']) == 2 and all(p['mismatches'] == 0 and p['failed_source_inventory_exact'] is True for p in retention['two_fresh_union_checks'])
    failed = 'results/limitation_program_20261001/A20_continuation_20261004_audit_run004'
    assert not (ROOT / failed / 'manifest.json').exists()
    parsed = {}
    for name in ('protocol.json','FAILED_UNSEALED.json','failure.json','RUN_STARTED.json'):
        parsed[name] = read(failed + '/' + name)
        assert PINS[failed + '/' + name] == inventory[name]
    marker = parsed['FAILED_UNSEALED.json']
    error = parsed['failure.json']
    assert marker['authoritative_failure'] is True and marker['hard_budget_state_uncertified'] is True
    assert marker['budget_censored'] is None and error['message'] == 'Fixed A20 process CPU/wall guard'
    for relative in (
        'results/limitation_program_20261001/A20_continuation_20261004_failure_capture_run001/manifest.json',
        'results/limitation_program_20261001/A20_continuation_20261004_template_diagnostic_run001/manifest.json',
        'research/limitation_program_20261001/continuation_20261004/A20/ROOT_STATIC_REJECTION_v5.json',
        'docs/limitation_program_20261001/continuation_20261004/A20/HANDOFF_DRAFT_run001.md',
        'docs/limitation_program_20261001/continuation_20261004/A20/author_final_handoff_run001.py',
    ):
        capture(relative)
    capture(Path(__file__).relative_to(ROOT).as_posix())
    capture(protocol.relative_to(ROOT).as_posix())
    notification = {'schema':'a20-root-handoff-outcome-v1','notified_by_root':True,'outcome':'FAILED',
        'producer_complete':True,'audit_complete':False,'full_fresh_integrity_complete':False,
        'producer_full_fresh_integrity_complete':True,'audit_failed_evidence_retention_complete':True,
        'execution_summary':'The V6 producer completed all2608 fixed component checks and its ROOT integrity passed two8779-path fresh unions with exact inventories and zero mismatches. The separate independent audit preparation passed, then its one scientific run stopped with ValueError: Fixed A20 process CPU/wall guard. No independent result group or complete audit manifest was published. Its FAILED_UNSEALED marker remains authoritative, with hard budget state UNCERTIFIED, budget_censored null and completed independent checks unknown/null. ROOT retained every failed-owned file and originally prepared expectation and checked the full joined failed-source/owned/frozen/external union twice. That capture PASS means byte/inventory retention only. Producer PASS is not independent audit completion. No unchanged retry or increased cap occurred. A20 remains partial; full price-source G2/cost, generalq32 access/law, threshold transform, adoption and advantage remain open/false.',
        'evidence_sha256':dict(PINS),'A20_status':'partial','full_G2':False,'adoption':False,
        'quantum_advantage':False,'new_fixture_or_financial_replay_credit':0}
    out = HERE / 'ROOT_FINAL_OUTCOME_run001.json'
    save(out, notification)
    print(json.dumps({'notification':out.relative_to(ROOT).as_posix(),
                      'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'outcome':'FAILED','scientific_execution':False}))


if __name__ == '__main__':
    main()
