"""Independent metadata-only V6 freeze review. Never import scientific modules."""
import ast
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RESEARCH = ROOT / 'research/limitation_program_20261001'
START_CPU, START_WALL = time.process_time(), time.monotonic()


def guard():
    assert time.process_time()-START_CPU < 30
    assert time.monotonic()-START_WALL < 90


def sha(path):
    guard()
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def read(path):
    guard()
    return json.loads(path.read_text(encoding='utf-8'))


def parsed(path):
    guard()
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    compile(tree, str(path), 'exec')
    return tree


def spelling(value, mapping):
    for old, new in mapping.items():
        value = value.replace(old, new)
    return value


class ReleaseNames(ast.NodeTransformer):
    def __init__(self, mapping):
        self.mapping = mapping

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            node.value = spelling(node.value, self.mapping)
        return node

    def visit_ImportFrom(self, node):
        if node.module:
            node.module = spelling(node.module, self.mapping)
        return self.generic_visit(node)

    def visit_alias(self, node):
        node.name = spelling(node.name, self.mapping)
        return node


def dump(node):
    return ast.dump(node, include_attributes=False)


def definitions(tree):
    return {node.name: node for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}


def assign(tree, name):
    values = [ast.literal_eval(node.value) for node in tree.body
              if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)]
    assert len(values) == 1, name
    return values[0]


def main():
    author_record = RESEARCH/'continuation_20261004/A13/A20_V6_AUTHOR_PINS_run001.json'
    authors = read(author_record)['author_sha256']
    names = ('arithmetic_free_basket_signal_continuation_v6.py', 'a20_signal_receipt_continuation_v6.py',
             'experiment_arithmetic_free_basket_signal_continuation_v6.py', 'audit_arithmetic_free_basket_signal_continuation_v6.py',
             'A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_V6.md', 'a20_comparator_phase_continuation_preflight_v6.json')
    assert set(authors) == {(RESEARCH/n).relative_to(ROOT).as_posix() for n in names}
    assert all(sha(ROOT/k) == expected for k,expected in authors.items())
    trees = {n:parsed(RESEARCH/n) for n in names[:4]}
    assert assign(trees[names[1]], 'AUTHOR_NAMES') == names
    mappings = {n.replace('_v6', '_v5'):n for n in names}
    mappings.update({n.replace('_V6', '_V5'):n for n in names if '_V6' in n})
    mappings.update({
        'a20_comparator_phase_continuation_preflight_v4.json':names[-1],
        'A20-comparator-phase-static-READY-v5':'A20-comparator-phase-static-READY-v6',
        'A20_continuation_20261004_producer_run003':'A20_continuation_20261004_producer_run004',
        'A20_continuation_20261004_audit_run003':'A20_continuation_20261004_audit_run004',
        'E03_support_audit_run003/B4x12_audit.json':'E03_support_audit_run002/B4x12_audit.json'})
    mappings.update({n[:-3].replace('_v6','_v5'):n[:-3] for n in names[:4]})
    comparisons = {}
    for new in names[:4]:
        old = new.replace('_v6','_v5')
        previous = parsed(RESEARCH/old)
        transformed = ReleaseNames(mappings).visit(copy.deepcopy(previous))
        assert dump(transformed) == dump(trees[new]), new
        old_strings = Counter(n.value for n in ast.walk(previous) if isinstance(n,ast.Constant) and isinstance(n.value,str))
        new_strings = Counter(n.value for n in ast.walk(trees[new]) if isinstance(n,ast.Constant) and isinstance(n.value,str))
        expected = Counter()
        for value,count in old_strings.items(): expected[spelling(value,mappings)] += count
        assert expected == new_strings, new
        comparisons[new] = {'whole_AST_equal_under_precise_release_mapping':True,
                            'all_string_constants_equal_under_precise_mapping':True,
                            'string_constant_occurrences':sum(new_strings.values()),
                            'previous_SHA256':sha(RESEARCH/old)}
    routes = read(HERE/'A20_V6_ROUTE_STATIC_REVIEW_run001.json')
    assert routes['passed'] is True and routes['scientific_execution'] is False
    for key,value in routes['path_diff'].items():
        assert value['SHA256'] == authors[(RESEARCH/key).relative_to(ROOT).as_posix()]
    # Check every retained scientific function against the held V4/base release.
    changes = {}
    for new in (names[0],names[3]):
        old = 'arithmetic_free_basket_signal_v2.py' if new == names[0] else new.replace('_v6','_v4')
        old_tree = parsed(RESEARCH/old)
        old_defs,new_defs = definitions(old_tree),definitions(trees[new])
        old_map = {n.replace('_v6','_v4'):n for n in names}
        old_map.update({n[:-3].replace('_v6','_v4'):n[:-3] for n in names[:4]})
        old_map['arithmetic_free_basket_signal_v2.py'] = names[0]
        old_map['A20_continuation_20261004_producer_run002']='A20_continuation_20261004_producer_run004'
        old_map['A20_continuation_20261004_audit_run002']='A20_continuation_20261004_audit_run004'
        changed = sorted(n for n in old_defs if dump(ReleaseNames(old_map).visit(copy.deepcopy(old_defs[n]))) != dump(new_defs[n]))
        added = sorted(set(new_defs)-set(old_defs))
        assert not set(old_defs)-set(new_defs)
        expected_changed = ['stock_templates'] if new == names[0] else ['independent_component','independently_bind_stock']
        expected_added = ['stock_template_sharing_signature'] if new == names[0] else ['independent_stock_sharing_signature']
        assert changed == expected_changed and added == expected_added, (new,changed,added)
        changes[new] = {'held_original':old,'held_SHA256':sha(RESEARCH/old),
                        'changed_only_reviewed_sharing_guards_or_typed_binding':changed,
                        'added_only_separate_semantic_signature':added,
                        'all_other_definition_ASTs_unchanged':len(old_defs)-len(changed)}
    policy=read(RESEARCH/names[-1]); previous_policy=read(RESEARCH/'a20_comparator_phase_continuation_preflight_v5.json')
    assert policy['total_internal_checks'] == 2608 and sum(policy['internal_check_families'].values()) == 2608
    assert (policy['pricing_word_width'],policy['pricing_fractional_bits']) == (72,40)
    assert policy['budgets_each_prepare_run'] == {'creation_wall_seconds':600,'hard_process_CPU_seconds':180,'work_admission_CPU_seconds':150}
    invariant_keys=('internal_check_families','limits','native_scalar_knots','native_interface_cases','restricted_pair_truth_rows','offline_scalar_evaluations','additional_selected_expected_sha256','original_immutable_prospectus','pricing_word_width','pricing_fractional_bits','budgets_each_prepare_run','MQ','new_test_credit','new_financial_replay_credit','new_gate_replay_credit','full_G2','adoption','quantum_advantage','physical_runtime','complete_financial_bias_allocation')
    assert all(policy[k] == previous_policy[k] for k in invariant_keys)
    assert all(policy['prior_attempt_sha256'].get(k) == v for k,v in previous_policy['prior_attempt_sha256'].items())
    assert policy['prior_attempt_external_runtime_sha256'] == previous_policy['prior_attempt_external_runtime_sha256']
    assert policy['producer_receipt'].endswith('A20_continuation_20261004_producer_run004')
    assert policy['audit_receipt'].endswith('A20_continuation_20261004_audit_run004')
    required=('author_sha256','base_interpreter_sha256','budget','interpreter_sha256','output','prior_attempt_external_runtime_sha256','prior_attempt_sha256','ready','role','schema','science_executed_during_authoring','selected_owner_manifest_sha256','selected_prerequisite_sha256')
    assert sorted(policy['required_ROOT_READY_fields']) == sorted(required)
    admission_keys = {n.slice.value for n in ast.walk(trees[names[1]])
                      if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Attribute)
                      and n.value.attr=='ready' and isinstance(n.slice,ast.Constant) and isinstance(n.slice.value,str)}
    assert set(required) <= admission_keys
    audit_keys={n.slice.value for n in ast.walk(trees[names[3]]) if isinstance(n,ast.Subscript)
                and isinstance(n.value,ast.Attribute) and n.value.attr=='ready'
                and isinstance(n.slice,ast.Constant) and isinstance(n.slice.value,str)}
    assert 'producer_manifest_sha256' in audit_keys
    support='E03_support_audit_run002/B4x12_audit.json'
    for n in names[2:4]:
        strings=[x.value for x in ast.walk(trees[n]) if isinstance(x,ast.Constant) and isinstance(x.value,str)]
        assert support in strings and not any('E03_support_audit_run003' in s or 'E03_support_audit_run004' in s for s in strings)
    bound_paths = [HERE/'A20_V6_STATIC_REVIEW_PREFLIGHT.json',Path(__file__),author_record,
        HERE/'A20_V6_ROUTE_STATIC_REVIEW_run001.json',HERE/'A20_V5_ROUTE_STATIC_REVIEW_run001.json',
        HERE/'A20_MUL_METADATA_REVIEW_v5b.json',HERE/'A20_METADATA_REVIEW_v5_failure.json',
        ROOT/'docs/limitation_program_20261001/continuation_20261004/A14/A20_COMMUTATIVITY_REVIEW_v5.md',
        ROOT/'docs/limitation_program_20261001/continuation_20261004/A13/A20_V5_ORDERED_COST_BOUNDARY_SUPPLEMENT.md',
        ROOT/'docs/limitation_program_20261001/continuation_20261004/A20_V6_OPERATIONAL_ERRATUM.md']
    evidence={p.relative_to(ROOT).as_posix():sha(p) for p in bound_paths}
    assert evidence[bound_paths[-3].relative_to(ROOT).as_posix()] == 'cc141ffe56e5666f1b8a303e3171653feda577922b237cfb23493aa241c88b57'
    assert evidence[bound_paths[-2].relative_to(ROOT).as_posix()] == 'c7a326a02752306d6a61ae821351298ef083070cd6d73fbc2540848fadd6596c'
    erratum=bound_paths[-1].read_text(encoding='utf-8')
    assert 'run004' in erratum and 'run003' in erratum
    record={'schema':'a20-independent-v6-prospective-static-review-v1','static_pass':True,
        'scientific_execution':False,'author_sha256':authors,'evidence_sha256':evidence,
        'whole_AST_and_all_string_comparisons':comparisons,'held_original_definition_comparisons':changes,
        'actual_AUTHOR_NAMES_exact_six':True,'historical_support_restored_to_run002':True,
        'required_common_READY_fields_verified_against_actual_admission':list(required),
        'audit_additional_READY_field':'producer_manifest_sha256','operative_output_routes':'Only A20 own producer/audit run004',
        'fixed_internal_checks':2608,'native_width_fraction_bits':[72,40],'CPU_admission_wall_limits':[180,150,600],
        'prior_ROOT_map_count':len(policy['prior_attempt_sha256']),'prior_external_map_count':len(policy['prior_attempt_external_runtime_sha256']),
        'prior_maps_checked':'Metadata exact preservation; root issuer independently hashes complete live expected maps',
        'semantic_sharing_scope':'Only scalar-map equality of the two fixed normalized native72/F40 closures; original ordered arrays/hashes/evaluation and costs retained',
        'ordered_backend_depths':{'outputs11_18_22':[1076,1012],'outputs31_35':[1009,913]},
        'full_source_cost_equivalence':False,'Stage_C':False,'component_PASS':False,'full_G2':False,'adoption':False,'new_test_credit':0,'quantum_advantage':False,
        'frozen_V6_MD_stale_run003_sentence':'Operative run004 is resolved by separately bound erratum; no frozen author byte edited',
        'remaining':'Root exact complete byte freeze/READY; actual one bounded producer; separately admitted independent audit; root terminal integrity; no complete price source or physical performance claim',
        'review_CPU_seconds':time.process_time()-START_CPU,'review_wall_seconds':time.monotonic()-START_WALL}
    guard()
    output=HERE/'A20_V6_INDEPENDENT_STATIC_REVIEW_run001.json'
    with output.open('x',encoding='utf-8') as stream:
        json.dump(record,stream,indent=2,sort_keys=True);stream.write('\n')
    print(json.dumps({'static_pass':True,'output':output.relative_to(ROOT).as_posix(),'SHA256':sha(output),'six_author_count':len(authors),'science':False}))


if __name__ == '__main__':
    main()
