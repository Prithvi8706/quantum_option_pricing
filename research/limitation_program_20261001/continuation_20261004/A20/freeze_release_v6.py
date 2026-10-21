"""Root-only static freeze: never import or execute scientific author modules."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RESEARCH = ROOT / 'research/limitation_program_20261001'
START_CPU, START_WALL = time.process_time(), time.monotonic()


def guard():
    assert time.process_time() - START_CPU < 120
    assert time.monotonic() - START_WALL < 300


def digest(path):
    guard()
    before = path.stat()
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(1024 * 1024):
            guard()
            h.update(block)
    after = path.stat()
    assert (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns)
    return h.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    guard()
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def join(mapping, key, expected):
    assert key not in mapping or mapping[key] == expected, key
    mapping[key] = expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--role', choices=('producer', 'audit'), required=True)
    parser.add_argument('--independent-review', required=True)
    parser.add_argument('--independent-review-sha256', required=True)
    parser.add_argument('--author-pins', required=True)
    parser.add_argument('--producer-manifest-sha256')
    args = parser.parse_args()
    assert ROOT == Path.cwd().resolve()
    author_record = ROOT / args.author_pins
    authors = read(author_record)['author_sha256']
    expected_names = (
        'arithmetic_free_basket_signal_continuation_v6.py',
        'a20_signal_receipt_continuation_v6.py',
        'experiment_arithmetic_free_basket_signal_continuation_v6.py',
        'audit_arithmetic_free_basket_signal_continuation_v6.py',
        'A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_V6.md',
        'a20_comparator_phase_continuation_preflight_v6.json',
    )
    assert set(authors) == {(RESEARCH / n).relative_to(ROOT).as_posix() for n in expected_names}
    for key, expected in authors.items():
        assert digest(ROOT / key) == expected, key
    trees = {}
    for name in expected_names[:4]:
        data = (RESEARCH / name).read_text(encoding='utf-8')
        tree = ast.parse(data, filename=name)
        compile(tree, name, 'exec')
        trees[name] = tree
    receipt_tree = trees[expected_names[1]]
    declared = [ast.literal_eval(n.value) for n in receipt_tree.body
                if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'AUTHOR_NAMES' for t in n.targets)]
    assert declared == [expected_names]
    support = 'E03_support_audit_run002/B4x12_audit.json'
    for name in expected_names[2:4]:
        constants = [n.value for n in ast.walk(trees[name]) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        assert support in constants
        assert not any('E03_support_audit_run003' in c or 'E03_support_audit_run004' in c for c in constants)
    policy = read(RESEARCH / expected_names[-1])
    assert policy['total_internal_checks'] == 2608
    assert policy['pricing_word_width'] == 72 and policy['pricing_fractional_bits'] == 40
    assert policy['budgets_each_prepare_run'] == {'creation_wall_seconds':600, 'hard_process_CPU_seconds':180, 'work_admission_CPU_seconds':150}
    old_ready = read(HERE / 'PRODUCER_ROOT_READY_run002.json')
    selected = old_ready['selected_prerequisite_sha256']
    owners = old_ready['selected_owner_manifest_sha256']
    old_prospectus = read(RESEARCH / 'a20_arithmetic_free_loading_prospectus.json')
    assert selected == old_prospectus['selected_original_expected_sha256'] | policy['additional_selected_expected_sha256']
    membership = set()
    for key, expected in owners.items():
        owner = ROOT / key
        assert digest(owner) == expected
        packet = read(owner)
        legacy = key.endswith('/A10_coefficient_run001/manifest.json')
        if legacy:
            assert 'files' not in packet
            packet = {'files':packet}
        for field in ('files', 'frozen_inputs'):
            for raw, wanted in packet.get(field, {}).items():
                if field == 'frozen_inputs':
                    canonical = raw
                else:
                    normalized = raw.replace('\\', '/') if legacy else raw
                    base = owner.parent.relative_to(ROOT).as_posix()
                    canonical = normalized if normalized.startswith(base + '/') else base + '/' + normalized
                    assert (ROOT / canonical).resolve().is_relative_to(owner.parent.resolve())
                if canonical in selected:
                    assert selected[canonical] == wanted == digest(ROOT / canonical)
                    membership.add((canonical, wanted))
    assert all((k,v) in membership for k,v in selected.items() if not k.endswith('/manifest.json'))
    prior = dict(policy['prior_attempt_sha256'])
    external = dict(policy['prior_attempt_external_runtime_sha256'])
    additional = [
        author_record,
        ROOT / args.independent_review,
        HERE / 'ROOT_STATIC_REJECTION_v5.json',
        HERE / 'ROOT_FREEZE_PROTOCOL_v6.json',
        Path(__file__),
        ROOT / 'docs/limitation_program_20261001/continuation_20261004/A13/A20_V5_ORDERED_COST_BOUNDARY_SUPPLEMENT.md',
        ROOT / 'docs/limitation_program_20261001/continuation_20261004/A14/A20_COMMUTATIVITY_REVIEW_v5.md',
        ROOT / 'docs/limitation_program_20261001/continuation_20261004/A20_V6_OPERATIONAL_ERRATUM.md',
    ]
    assert digest(ROOT / args.independent_review) == args.independent_review_sha256
    independent = read(ROOT / args.independent_review)
    assert independent['static_pass'] is True
    assert independent['scientific_execution'] is False
    assert independent['author_sha256'] == authors
    for path in additional:
        join(prior, path.relative_to(ROOT).as_posix(), digest(path))
    for key, expected in prior.items():
        assert (ROOT / key).relative_to(ROOT).as_posix() == key
        assert digest(ROOT / key) == expected, key
    for key, expected in external.items():
        path = Path(key)
        assert path.is_absolute() and str(path) == key and not path.is_relative_to(ROOT)
        assert digest(path) == expected, key
    interpreter = ROOT / '.context/frontier_t0_env/Scripts/python.exe'
    import sys
    base = Path(sys._base_executable).resolve()
    assert digest(interpreter) == old_ready['interpreter_sha256']
    assert digest(base) == old_ready['base_interpreter_sha256']
    review_path = HERE / 'ROOT_STATIC_REVIEW_v6.json'
    review = {
        'schema':'root-a20-static-review-v6', 'science_executed':False,
        'static_pass':True, 'author_sha256':authors,
        'independent_review_sha256':args.independent_review_sha256,
        'actual_receipt_AUTHOR_NAMES_verified':True,
        'historical_support_routes_preserved':True,
        'complete_prior_ROOT_count':len(prior), 'complete_prior_external_count':len(external),
        'native_precision_counts_budgets_unchanged':True,
        'semantic_sharing_only_no_ordered_backend_cost_equivalence':True,
        'full_G2':False, 'adoption':False, 'quantum_advantage':False,
        'scope':'Restricted paid exact comparator-phase/QROM component; no threshold or complete price source.',
    }
    if args.role == 'producer':
        assert args.producer_manifest_sha256 is None
        save(review_path, review)
    else:
        assert read(review_path) == review
        producer = ROOT / policy['producer_receipt']
        assert digest(producer / 'manifest.json') == args.producer_manifest_sha256
        assert not any((producer / name).exists() for name in ('FAILED_UNSEALED.json','failure.json','run_failure.json','prepare_failure.json'))
        summary = read(producer / 'summary.json')
        assert summary['completed'] is True and summary['passed'] is True and summary['budget_censored'] is False
    join(prior, review_path.relative_to(ROOT).as_posix(), digest(review_path))
    ready = {
        'schema':policy['required_external_ROOT_READY_schema'], 'ready':True, 'role':args.role,
        'budget':[180,150,600], 'science_executed_during_authoring':False,
        'output':policy['producer_receipt'] if args.role == 'producer' else policy['audit_receipt'],
        'interpreter_sha256':old_ready['interpreter_sha256'],
        'base_interpreter_sha256':old_ready['base_interpreter_sha256'],
        'author_sha256':authors, 'selected_prerequisite_sha256':selected,
        'selected_owner_manifest_sha256':owners, 'prior_attempt_sha256':prior,
        'prior_attempt_external_runtime_sha256':external,
        'root_static_review_sha256':digest(review_path), 'new_test_credit':0,
    }
    assert set(policy['required_ROOT_READY_fields']) <= set(ready)
    if args.role == 'audit':
        ready['producer_manifest_sha256'] = args.producer_manifest_sha256
    ready_path = HERE / ('PRODUCER_ROOT_READY_run004.json' if args.role == 'producer' else 'AUDIT_ROOT_READY_run004.json')
    save(ready_path, ready)
    print(json.dumps({'READY':ready_path.relative_to(ROOT).as_posix(), 'sha256':digest(ready_path), 'prior_ROOT':len(prior), 'prior_external':len(external), 'science_executed':False}))


if __name__ == '__main__':
    main()
