"""Fast read-only release consistency overlay, not full circuit reconstruction."""
import argparse
import json
from pathlib import Path
import subprocess

from .budgets import verify_budget
from .claims import verify_claims
from .environment import compare_environment
from .finite import verify_finite
from .gates import scientific_status
from .hashes import digest, verify_hashes
from .inputs import input_entries, verify_inputs
from .inventory import verify_archive
from .json_io import read
from .ledger import verify_ledger
from .licenses import license_inventory
from .links import verify_links
from .paths import within
from .pins import pins
from .receipts import junit
from .replay import compare_replay
from .schedules import verify_schedule
from .sources import verify_sources
from .targets import verify_targets


ROOT = Path(__file__).resolve().parents[2]


def build_report(root=ROOT):
    scope = read(root/'docs/release/scope.json')
    if scope['schema'] != 'release_scope_v1' or len(scope['archives']) != 4:
        raise ValueError('unexpected release scope')
    if set(scope['manifest_sha256']) != {a+'/complete.json' for a in scope['archives']}:
        raise ValueError('manifest pins do not cover scope')
    verify_hashes(root, scope['manifest_sha256'])
    paths = [within(root, a) for a in scope['archives']]
    archives = []
    for path in paths:
        files = verify_archive(path)
        planned = read(path/'planned.json')
        matched = path.name.startswith('matched_arithmetic')
        stem = 'MATCHED_ARITHMETIC' if matched else 'CLAIM_ASSESSMENT'
        protocol = 'docs/journal_sprint/'+stem+'_PROTOCOL_20260917.md'
        required = ['research/journal_sprint/storage.py',
                    'research/journal_sprint/'+('run_matched_arithmetic' if matched else 'claim_assessment')+'.py']
        sources = verify_sources(root, planned, protocol, required)
        inputs = read(path/'inputs.json')
        # Pinned complete -> planned/input hashes anchor this exact inventory.
        count = verify_inputs(root, inputs, input_entries(inputs))
        archives.append({'path': path.relative_to(root).as_posix(), 'artifacts': files,
                         'inputs': count, **sources})
    if scope['replay_pairs'] != [[0, 1], [2, 3]]:
        raise ValueError('incomplete replay-pair menu')
    replays = [compare_replay(paths[a], paths[b]) for a, b in scope['replay_pairs']]
    results = read(paths[2]/'results.json')
    target = verify_targets(results)
    for case in results['comparisons']:
        for row in case['alternatives']:
            verify_budget(row)
            verify_schedule(row)
            verify_ledger(row)
    documents = ['README.md', 'checklist_17.9.26.md'] + [
        p.relative_to(root).as_posix() for p in sorted((root/'docs/release').glob('*.md'))]
    report = {'schema': 'release_audit_v1', 'artifact_checks_passed': True,
              'archives': archives, 'replays': replays, 'matched_target': target,
              'finite_diagnostics': verify_finite(read(paths[2]/'finite.json')),
              'claims': verify_claims(root, read(root/'docs/release/claims.json')),
              'scientific_status': scientific_status(scope['scientific_gates']),
              'environment': compare_environment(pins(within(root, scope['requirements']).read_text(encoding='utf-8'))),
              'licenses': license_inventory(root, scope['licenses']),
              'test_receipts': [{'path': name, **junit(within(root, name))} for name in scope['receipts']],
              'links': verify_links(root, documents),
              'scope_sha256': digest(root/'docs/release/scope.json'),
              'claim_register_sha256': digest(root/'docs/release/claims.json'),
              'auditor_sha256': {p.relative_to(root).as_posix(): digest(p)
                                 for p in sorted((root/'research/release_checks').glob('*.py'))},
              'full_circuit_reconstruction_performed': False}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--require-environment', action='store_true')
    args = parser.parse_args()
    result = build_report()
    result['git_head'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    text = json.dumps(result, indent=2, allow_nan=False)+'\n'
    if args.output:
        with args.output.open('x', encoding='utf-8') as stream:
            stream.write(text)
    else:
        print(text, end='')
    if args.require_environment and not result['environment']['matches']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
