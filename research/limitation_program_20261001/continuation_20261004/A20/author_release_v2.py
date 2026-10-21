"""Create a fresh operational A20 release; never import scientific modules."""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
RESEARCH = ROOT / 'research/limitation_program_20261001'
NAMES = {
    'a20_signal_receipt_v2.py': 'a20_signal_receipt_continuation_v3.py',
    'experiment_arithmetic_free_basket_signal_v2.py': 'experiment_arithmetic_free_basket_signal_continuation_v3.py',
    'audit_arithmetic_free_basket_signal_v2.py': 'audit_arithmetic_free_basket_signal_continuation_v3.py',
    'A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V2.md': 'A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_V3.md',
    'a20_comparator_phase_implementation_preflight_v2.json': 'a20_comparator_phase_continuation_preflight_v3.json',
}


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)


def main():
    assert ROOT == Path.cwd().resolve()
    record = {'science_executed': False, 'old_files_edited': False, 'changes': {}}
    for old, new in NAMES.items():
        source = (RESEARCH / old).read_bytes()
        text = source.decode('utf-8-sig')
        for before, after in NAMES.items():
            text = text.replace(before, after)
            if before.endswith('.py'):
                text = text.replace(before[:-3], after[:-3])
        text = text.replace('A20_signal_semantics_audit_run001', 'A20_continuation_20261004_audit_run001')
        text = text.replace('A20_signal_semantics_run001', 'A20_continuation_20261004_producer_run001')
        text = text.replace('A20-comparator-phase-static-READY-v2', 'A20-comparator-phase-static-READY-v3')
        if old == 'a20_signal_receipt_v2.py':
            before = '            if "files" not in packet:\n'
            assert text.count(before) == 1
            text = text.replace(before, '            legacy_flat_owner = "files" not in packet\n' + before)
            before = '''                        require(
                            name
                            in (
                                actual.relative_to(ROOT).as_posix(),
                                actual.relative_to(path.parent).as_posix(),
                            ),
                            "Exact selected owned member spelling",
                        )'''
            assert text.count(before) == 1
            after = '''                        permitted_name = name.replace("\\\\", "/") if legacy_flat_owner else name
                        require(
                            permitted_name
                            in (
                                actual.relative_to(ROOT).as_posix(),
                                actual.relative_to(path.parent).as_posix(),
                            ),
                            "Exact selected owned member spelling; pinned legacy separator only",
                        )'''
            text = text.replace(before, after)
        elif old.endswith('.json'):
            obj = json.loads(text)
            obj['schema'] = 'A20-comparator-phase-continuation-preflight-v3'
            obj['operational_changes_only'] = [
                'Fresh controller module/output routes and six release author pins.',
                'Only the exact pinned legacy A10 flat manifest admits its Windows separators; canonical containment and actual expected SHA remain mandatory.',
            ]
            obj['scientific_builder_unchanged'] = 'arithmetic_free_basket_signal_v2.py'
            obj['scientific_counts_precision_budgets_unchanged'] = True
            obj['old_V2_unexecuted_no_failure_promoted'] = True
            text = json.dumps(obj, sort_keys=True, indent=2) + '\n'
        elif old.endswith('.md'):
            text = ('# Continuation V3 operational release\n\n'
                    'V2 remains immutable and unexecuted. Static inspection found its authentic, pinned A10 flat manifest contains Windows path separators that its spelling guard rejected. V3 normalizes only those exact pinned legacy names for comparison, retaining confinement, canonical selected keys and actual equal-SHA membership. Fresh operational modules and output routes avoid reuse. The scientific builder, independent mathematical kernels, 2,608 internal checks, all counts, precision, gates, error boundaries, CPU/wall/evidence limits and zero program credit are unchanged.\n\n' + text)
        data = text.encode('utf-8')
        if new.endswith('.py'):
            compile(ast.parse(text), str(RESEARCH / new), 'exec')
        write_new(RESEARCH / new, data)
        record['changes'][new] = {'original': old, 'original_sha256': hashlib.sha256(source).hexdigest(), 'new_sha256': hashlib.sha256(data).hexdigest()}
    write_new(Path(__file__).parent / 'release_authoring.json', (json.dumps(record, sort_keys=True, indent=2) + '\n').encode())
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()
