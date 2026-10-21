"""Root's static freeze of the operational release; no scientific imports."""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
RESEARCH = ROOT / 'research/limitation_program_20261001'
HERE = Path(__file__).resolve().parent
AUTHORS = (
    'arithmetic_free_basket_signal_v2.py',
    'a20_signal_receipt_continuation_v3.py',
    'experiment_arithmetic_free_basket_signal_continuation_v3.py',
    'audit_arithmetic_free_basket_signal_continuation_v3.py',
    'A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_V3.md',
    'a20_comparator_phase_continuation_preflight_v3.json',
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(obj, stream, sort_keys=True, indent=2)
        stream.write('\n')


def main():
    assert ROOT == Path.cwd().resolve()
    old = json.loads((RESEARCH / 'a20_arithmetic_free_loading_prospectus.json').read_text())
    policy = json.loads((RESEARCH / AUTHORS[-1]).read_text())
    selected = old['selected_original_expected_sha256'] | policy['additional_selected_expected_sha256']
    assert all(sha(ROOT / key) == value for key, value in selected.items())
    owners, membership = {}, set()
    rows = []
    for owner in ('A10_coefficient_run001', 'G0_run003', 'E03_support_audit_run002', 'E22_census_run002', 'A17_quantile_divider_run001'):
        path = ROOT / 'results/limitation_program_20261001' / owner / 'manifest.json'
        owners[path.relative_to(ROOT).as_posix()] = sha(path)
        packet = json.loads(path.read_text())
        legacy = 'files' not in packet
        if legacy:
            assert owner == 'A10_coefficient_run001'
            assert sha(path) == old['selected_original_expected_sha256'][path.relative_to(ROOT).as_posix()]
            packet = {'files': packet}
        for field in ('files', 'frozen_inputs'):
            for name, expected in packet.get(field, {}).items():
                if field == 'files':
                    lexical = ROOT / name if name.startswith(path.parent.relative_to(ROOT).as_posix() + '/') else path.parent / name
                    actual = lexical.resolve(strict=False)
                    key = actual.relative_to(ROOT).as_posix()
                    if key not in selected:
                        continue
                    assert actual.is_relative_to(path.parent)
                    permitted = name.replace('\\', '/') if legacy else name
                    assert permitted in (key, actual.relative_to(path.parent).as_posix())
                else:
                    if name not in selected:
                        continue
                    key = name
                    actual = ROOT / key
                assert expected == selected[key] == sha(actual)
                membership.add((key, expected))
                rows.append({'owner': path.relative_to(ROOT).as_posix(), 'original_key': name, 'canonical_key': key, 'sha256': expected})
    assert all((k, v) in membership for k, v in selected.items() if not k.endswith('/manifest.json'))
    authors = {(RESEARCH / name).relative_to(ROOT).as_posix(): sha(RESEARCH / name) for name in AUTHORS}
    comparisons = {}
    for stem in ('experiment_arithmetic_free_basket_signal', 'audit_arithmetic_free_basket_signal'):
        old_data = (RESEARCH / (stem + '_v2.py')).read_text()
        new_data = (RESEARCH / (stem + '_continuation_v3.py')).read_text()
        a, b = ast.parse(old_data), ast.parse(new_data)
        compile(b, stem + '_continuation_v3.py', 'exec')
        defs = lambda tree: {n.name: ast.dump(n, include_attributes=False) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        aa, bb = defs(a), defs(b)
        assert aa.keys() == bb.keys()
        changed = [k for k in aa if aa[k] != bb[k]]
        assert set(changed) <= {'main', 'run_independent_audit'}
        comparisons[stem] = {'changed_definitions': changed, 'unchanged_definitions': len(aa)-len(changed)}
    review = {
        'schema': 'root-A20-continuation-static-review-v3',
        'science_executed': False,
        'root_static_review_passed': True,
        'scope': 'Paid restricted exact comparator-phase recipe, no full pricing-source or threshold transform.',
        'reviewed': [
            'H-reference exact counting (2F-M)/M and coherent selector pair (F1+F2-M)/M.',
            'Absolute phase Z(c)CZ(c,p), literal comparator/QROM/address inverse and private zero workspace.',
            'Native signed72/F40 evaluation, floor basket ties and half-lattice signal gap.',
            'Full gate, control, QROM, copy, H, inverse and7T costs; no physical runtime or full-source superiority.',
            'Fixed2608 component inventory; sparse tiny operator/native phase test scope and no53bit statevector.',
            'Pinned actual legacy owner separators only; exact canonical selected membership and fresh byte admission.',
        ],
        'author_sha256': authors,
        'selected_prerequisite_sha256': selected,
        'selected_owner_manifest_sha256': owners,
        'selected_membership_records': rows,
        'AST_comparisons': comparisons,
        'budget': [180,150,600],
        'new_test_credit': 0, 'adoption': False, 'full_G2': False, 'quantum_advantage': False,
    }
    write_new(HERE / 'ROOT_STATIC_REVIEW_v3.json', review)
    print(json.dumps({'review_sha256':sha(HERE/'ROOT_STATIC_REVIEW_v3.json'), 'author_sha256':authors, 'all_selected_prerequisites_match':True},indent=2))


if __name__ == '__main__':
    main()
