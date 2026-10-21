'Dormant date2 raw3543 grouped fixed Young bound and own saved comparison; ROOT release required.'

import argparse

import ast

import ctypes

from ctypes import wintypes

from fractions import Fraction

from importlib.util import cache_from_source

import hashlib

import json

import marshal

from math import gcd

import os

from pathlib import Path

import sys

import time

import types

import _pylong

ROOT = Path('C:/Users/prith/quantum_option_pricing')

SOURCE = ROOT / 'research/limitation_program_20261001/experiment_e11_second_date_grouped_fixed_young_raw_log_squared_l2_v1.py'

PLAN = ROOT / '.context/E11_SECOND_DATE_GROUPED_FIXED_YOUNG_SQUARED_L2_INPUT_ADAPTER_run001.json'

MD = ROOT / '.context/E11_SECOND_DATE_GROUPED_FIXED_YOUNG_SQUARED_L2_PREFLIGHT_run001.md'

READY = ROOT / '.context/E11_SECOND_DATE_GROUPED_FIXED_YOUNG_SQUARED_L2_ROOT_READY_run001.json'

OUTPUT = ROOT / 'results/limitation_program_20261001/E11_second_date_grouped_fixed_Young_raw_log_squared_L2_run001'

LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'source_prefix_and_grouped_norm_witness.json', 'five_metadata_controls.json', 'primary_grouped_raw_log_squared_L2.json', 'independent_grouped_raw_log_squared_L2.json', 'same_profile_comparison.json', 'summary.json', 'manifest.json']

CPU, ADMISSION, WALL = (180, 150, 600)

_STARTED = None

_OWNS_OUTPUT = False

_OUTPUT_ID = None

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def exact(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(exact(a[k], b[k]) for k in b)
    if type(a) is list:
        return len(a) == len(b) and all(exact(x, y) for x, y in zip(a, b))
    return a == b

def process_started():
    require(os.name == 'nt' and ctypes.sizeof(ctypes.c_void_p) == 8, 'Pinned Win64')
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    stamps = [wintypes.FILETIME() for _ in range(4)]
    require(kernel.GetProcessTimes(kernel.GetCurrentProcess(), *[ctypes.byref(stamp) for stamp in stamps]), 'Actual process creation clock')
    ticks = stamps[0].dwHighDateTime << 32 | stamps[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, 'Actual UTC creation precedes observation')
    return time.monotonic() - age_ns / 1000000000

def rss_bytes():
    require(os.name == 'nt' and ctypes.sizeof(ctypes.c_void_p) == 8, 'Pinned Win64 memory counter API')
    class Counters(ctypes.Structure):
        _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [(name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize', 'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage', 'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]
    kernel = ctypes.WinDLL(str(Path(os.environ['SystemRoot']) / 'System32/kernel32.dll'), use_last_error=True)
    psapi = ctypes.WinDLL(str(Path(os.environ['SystemRoot']) / 'System32/psapi.dll'), use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD]
    psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
    row = Counters(); row.cb = ctypes.sizeof(row)
    require(psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(row), row.cb), 'Actual current and peak resident set available')
    return max(row.WorkingSetSize, row.PeakWorkingSetSize)


def budget(admission=False):
    require(_STARTED is not None and time.process_time() <= CPU and time.monotonic() - _STARTED <= WALL and (not admission or time.process_time() <= ADMISSION), 'Unchanged180/150/600 hard budgets')
    require(rss_bytes() <= 157286400, 'Fixed current and peak RSS150MiB')

def stat8(path):
    s = path.stat()
    return [getattr(s, key, None) for key in ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns', 'st_mode', 'st_file_attributes', 'st_reparse_tag')]

def read_bytes(path, expected, records):
    budget()
    require(type(expected) is str and len(expected) == 64 and all(c in '0123456789abcdef' for c in expected), 'External original expected SHA')
    require(path.resolve(strict=True) == path and path.is_file() and not path.is_symlink() and not path.is_relative_to(OUTPUT), 'Canonical selected input; OUTPUT excluded')
    before = stat8(path)
    require(not before[-1] and 0 <= before[2] <= 64 << 20 and len(records) < 256 and sum(row['bytes'] for row in records.values()) + (0 if str(path) in records else before[2]) <= 64 << 20, 'Finite selected-byte scope')
    with path.open('rb') as stream:
        raw = stream.read(before[2] + 1)
    require(len(raw) == before[2] and stat8(path) == before and hashlib.sha256(raw).hexdigest() == expected, 'Selected original expected bytes and all8 stable')
    row = {'expected_SHA256': expected, 'bytes': len(raw), 'fingerprint': before}
    require(str(path) not in records or records[str(path)] == row, 'Equal original expected role overlaps')
    records[str(path)] = row
    budget()
    return raw

def decode(raw):
    require(sys.get_int_max_str_digits() == 4300, 'Default4300; no decimal setter')
    return json.loads(raw)

def code_guard(raw, ready):
    tree = ast.parse(raw)
    actual = {n.name: hashlib.sha256(ast.dump(n, include_attributes=False).encode('utf-8')).hexdigest() for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    require(actual == ready['definition_AST_SHA256'], 'Complete current function/Class source ASTs')
    compiled = compile(tree, str(SOURCE), 'exec', dont_inherit=True, optimize=0)
    codes = {c.co_name: c for c in compiled.co_consts if isinstance(c, types.CodeType)}
    for name in actual:
        require(type(globals()[name]) is types.FunctionType, 'Exact loaded function type')
        pending_codes = [(globals()[name].__code__, codes[name])]
        while pending_codes:
            loaded_code, source_code = pending_codes.pop()
            require(loaded_code == source_code and loaded_code.co_filename == source_code.co_filename and loaded_code.co_firstlineno == source_code.co_firstlineno and loaded_code.co_linetable == source_code.co_linetable, 'Every whole root and nested code object and filename firstline linetable equals freshly compiled SOURCE')
            loaded_children = [value for value in loaded_code.co_consts if isinstance(value, types.CodeType)]
            source_children = [value for value in source_code.co_consts if isinstance(value, types.CodeType)]
            require(len(loaded_children) == len(source_children), 'Exact ordered nested code constant census')
            pending_codes.extend(zip(loaded_children, source_children))
    aliases = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id not in {'_STARTED', '_OWNS_OUTPUT', '_OUTPUT_ID'}:
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                expr = node.value
                if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name) and expr.func.id == 'Path' and len(expr.args) == 1:
                    value = Path(ast.literal_eval(expr.args[0]))
                elif isinstance(expr, ast.BinOp) and isinstance(expr.op, ast.Div) and isinstance(expr.left, ast.Name) and expr.left.id in aliases:
                    value = aliases[expr.left.id] / ast.literal_eval(expr.right)
                else:
                    raise AssertionError('Every immutable module initializer has a closed literal or Path role')
            aliases[node.targets[0].id] = value
            require(exact(globals()[node.targets[0].id], value), 'Immutable loaded literal globals remain exact')
        elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Tuple):
            require(exact(tuple(globals()[item.id] for item in node.targets[0].elts), ast.literal_eval(node.value)), 'All immutable packed module constants retain exact values')
    require(LEDGER == ready['exact13_inclusive_ledger'] and sys.get_int_max_str_digits() == 4300, 'Current ledger and decoder remain fixed')
    require(type(_STARTED) is float and type(_OWNS_OUTPUT) is bool, "Exact tracked process/output state types")
    if _OWNS_OUTPUT:
        require(type(_OUTPUT_ID) is list and len(_OUTPUT_ID)==6, "Owned output state shape")
        owned_guard()
    else:
        require(_OUTPUT_ID is None, "No pre-admission output identity")
    require(Fraction is sys.modules["fractions"].Fraction and gcd is sys.modules["math"].gcd and Path is sys.modules["pathlib"].Path, "Imported constructor identities")


def loaded_origins(native_manifest, records):
    external = native_manifest['external_runtime_inputs']
    frozen = native_manifest['frozen_inputs']
    require(len(external) == 2842 and not any(name.split('.')[0] in {'numpy', 'scipy', 'mpmath', 'sympy', 'numba', 'pytest', 'pandas', 'gmpy2', 'research'} for name in sys.modules), 'Original expected runtime citation only; no scientific imports')
    origins = {}
    for name, module in tuple(sys.modules.items()):
        for attribute in ('__file__', '__cached__'):
            value = getattr(module, attribute, None)
            if not value:
                continue
            path = Path(os.path.abspath(value))
            if path == SOURCE:
                continue
            if not path.exists():
                source_name = getattr(module, '__file__', None)
                require(attribute == '__cached__' and source_name is not None and str(source_name).endswith('.py') and path.resolve(strict=False) == path and not path.is_symlink() and path == Path(cache_from_source(str(source_name), optimization='')), 'Only exact immediate absent cache for a known Python source')
                continue
            key = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
            mapping = frozen if path.is_relative_to(ROOT) else external
            require(key in mapping, 'Loaded origin must have an original expected pin; no observed promotion')
            read_bytes(path, mapping[key], records)
            origins[str(path)] = mapping[key]
    source = Path(_pylong.__file__)
    require(str(source) in external, 'Original serializer expectation')
    read_bytes(source, external[str(source)], records)
    read_bytes(ROOT / '.context/frontier_t0_env/pyvenv.cfg', frozen['.context/frontier_t0_env/pyvenv.cfg'], records)
    read_bytes(Path(sys.executable), frozen['.context/frontier_t0_env/Scripts/python.exe'], records)
    base_executable = Path(sys._base_executable)
    require(str(base_executable) in external and Path(sys.orig_argv[0]) == base_executable, 'Redirected original argv0 is the original pinned base executable')
    read_bytes(base_executable, external[str(base_executable)], records)
    return origins

def scope_validator(value, positive, controls):
    for row in controls:
        key = row['field']
        if key not in value or not exact(value[key], positive[key]):
            raise ValueError(row['tag'])
    if not exact(value, positive):
        raise ValueError('COMPOSITION_INTERFACE')

def controls_record(plan):
    positive = plan['interface']
    scope_validator(positive, positive, plan['controls'])
    rows = []
    for specification in plan['controls']:
        bad = dict(positive)
        bad[specification['field']] = specification['bad']
        try:
            scope_validator(bad, positive, plan['controls'])
        except ValueError as error:
            require(type(error) is ValueError and str(error) == specification['tag'], 'Dedicated artificial metadata rejection')
            rows.append({'field': specification['field'], 'mutation': specification['bad'], 'dedicated_tag': str(error), 'rejected': True})
        else:
            raise AssertionError('Fixed artificial control not rejected')
    require(len(rows) == 5, 'Five preregistered metadata controls')
    return {'passed': True, 'positive_first': True, 'artificial_metadata_only': True, 'controls': rows}

def ratio(pair):
    require(type(pair) is list and len(pair)==2 and all(type(v) is int and v.bit_length()<=131072 for v in pair) and pair[0]>=0 and pair[1]>0 and gcd(*pair)==1, 'Nonnegative canonical ordinary-input ratio')
    return Fraction(*pair)


def plus(a,b):
    budget()
    require(max(a.numerator.bit_length()+b.denominator.bit_length(),b.numerator.bit_length()+a.denominator.bit_length(),a.denominator.bit_length()+b.denominator.bit_length())<=524288,'Addition temporary bit frontier')
    value=a+b
    require(max(value.numerator.bit_length(),value.denominator.bit_length())<=131072,'Reduced addition bit frontier')
    return value


def twice(a):
    return times(Fraction(2),a)


def pair(value):
    require(type(value) is Fraction and value.numerator>=0 and max(value.numerator.bit_length(),value.denominator.bit_length())<=131072,'Nonnegative output rational bit frontier')
    result={'schema':'canonical-nonnegative-rational-base2p32-v1','numerator_sign':'zero' if value.numerator==0 else 'positive','numerator_limbs':integer_limbs(value.numerator),'denominator_limbs':integer_limbs(value.denominator)}
    require(limb_ratio(result)==value,'Canonical limb output roundtrip')
    return result


def source_signature(nodes, output, boundary):
    memo = {}; used = set()
    def visit(value):
        budget()
        if value in boundary:return 'boundary:' + boundary[value]
        if value in memo:return memo[value]
        node = nodes[value]; used.add(value)
        args = [visit(v) for v in node['args']]
        if node['op'] in ('add','mul'):args.sort()
        row = {'op':node['op'],'params':node['params'],'output_slot':node['out'].index(value),'output_count':len(node['out']),'arguments':args}
        result = hashlib.sha256(json.dumps(row,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        memo[value]=result
        return result
    pin=visit(output)
    return {'canonical_ordered_except_add_mul_DAG_SHA256':pin,'literal_value_count_excluding_declared_boundaries':len(used),'literal_rows':[nodes[v] for v in sorted(used)]}


def signed_pair(value):
    require(type(value) is Fraction and value.denominator>0 and max(abs(value.numerator).bit_length(),value.denominator.bit_length())<=131072 and gcd(abs(value.numerator),value.denominator)==1, 'Canonical reduced signed rational within the unchanged bit cap')
    return {'schema':'canonical-signed-rational-base2p32-v1','numerator_sign':'zero' if value.numerator==0 else 'positive' if value.numerator>0 else 'negative','numerator_limbs':integer_limbs(abs(value.numerator)),'denominator_limbs':integer_limbs(value.denominator)}

def interface_witness(plan, ready, inputs):
    require(ready['date2_grouped_young_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']), 'Current own grouped Young release before any numerical assembly')
    symbolic=inputs[plan['symbolic_PLAN_path']]
    require(symbolic['schema']=='e11-date2-grouped-fixed-young-prospective-plan-v1' and symbolic['scientific_evaluation_performed'] is symbolic['SOURCE_authoring_READY_or_SCI_authorized_by_PLAN'] is False and all(exact(plan[k],symbolic[k]) for k in ('interface','profiles','source_scope_proof','selected_expected_SHA256','selected_input_modes','fixed_expression','parent_complete13_owned_expected_SHA256')), 'One fixed planned route and exact expected operands, not an inherited execution grant')
    assessment=inputs[plan['accepted_assessment_path']];acceptance=inputs[plan['ROOT_assessment_review_path']]
    require(assessment['schema']=='e11-date2-raw3543-grouped-fixed-young-feasibility-assessment-v1' and assessment['assessment_metadata_checks_passed'] is True and assessment['scientific_evaluation_performed'] is assessment['SOURCE_or_recipe_guard_control_model_array_called'] is False and assessment['fixed_delta_exact_pair']==[1,100000] and assessment['delta_selected_before_future_SCI'] is assessment['no_delta_optimization_or_profile_minimum_or_adaptive_formula'] is True, 'Original preregistered grouped proof and fixed delta')
    require(acceptance['schema']=='root-e11-date2-grouped-young-assessment-acceptance-v1' and acceptance['passed'] is acceptance['science_static_passed'] is acceptance['lifecycle_static_passed'] is acceptance['metadata_only'] is True and acceptance['blockers']==[] and acceptance['scientific_evaluation_performed'] is acceptance['new_numeric_bounds_comparisons_or_ratio_decode_performed'] is acceptance['READY_or_SCI_or_numeric_adoption_authorized'] is False and acceptance['source_authoring_within_existing_user_authorization'] is acceptance['independent_current_SOURCE_review_still_required'] is True and acceptance['assessment_path']==plan['accepted_assessment_path'] and acceptance['assessment_expected_SHA256']==plan['selected_expected_SHA256'][plan['accepted_assessment_path']] and acceptance['proof_MD_expected_SHA256']==plan['selected_expected_SHA256'][plan['assessment_proof_MD_path']], 'Pinned ROOT symbolic acceptance; current READY alone licenses SCI')
    require(exact(plan['interface']['source_scope'],assessment['scope']) and exact(plan['fixed_expression'],assessment['fixed_expression']) and all(plan['selected_expected_SHA256'][k]==v for k,v in assessment['prospective_selected30_expected_SHA256'].items()) and exact(plan['parent_complete13_owned_expected_SHA256'],assessment['parent_complete13_owned_expected_SHA256']), 'All30 original/parent roles and full13 owner inherited by fixed expected pin')
    require(exact(plan['interface']['fixed_young'],{'delta_exact_pair':[1,100000],'profiles':['primary90','independent130'],'one_delta_for_both_profiles':True}) and plan['interface']['coordinate_quantity']=='own_per_coordinate_squared_L2_not_pair_sum' and exact(plan['interface']['multiplicities'],{'initial':1,'drift':2,'signed_cmul_floors':4,'aN_drivers':[94,357],'bN_drivers':[125,442]}) and exact(plan['interface']['proof_qualification'],{'native_error_or_previous_log_innovation_independence_assumed':False,'adaptive_minimum_formula_or_profile_choice':False,'stock_projection_tails_or_price_certificate':False}), 'Per-coordinate quantity, grouping, paid deterministic multiplicities and no independence/minimum')
    parent_root=inputs[plan['parent_ROOT_verification']];parent_mf=inputs[plan['parent_manifest']];parent_adapter=inputs[plan['parent_executed_adapter']];parent_ready=inputs[plan['parent_executed_READY']]
    require(parent_root['passed'] is parent_root['completed'] is parent_root['date2_raw_log_transfer_witness_accepted'] is parent_root['date2_asset0_raw3543_only'] is True and type(parent_root['ROOT_observed_terminal_exit_code']) is int and parent_root['ROOT_observed_terminal_exit_code']==0 and parent_root['manifest_SHA256']==plan['selected_expected_SHA256'][plan['parent_manifest']] and parent_root['stock_projection_tails_candidate_or_price_results'] is None and parent_root['native_error_or_previous_log_innovation_independence_assumed'] is False, 'Verified parent raw3543 certificate, no stock or independence promotion')
    require(parent_mf['passed'] is parent_mf['completed'] is True and parent_mf['budget_censored'] is False and type(parent_mf['inclusive_files']) is int and parent_mf['inclusive_files']==13 and set(parent_mf['files'])==set(plan['parent_ledger'])-{'manifest.json'}, 'Complete sealed parent13 not a partial result')
    expected_owned={plan['parent_output']+'/manifest.json':plan['selected_expected_SHA256'][plan['parent_manifest']]}
    expected_owned.update({plan['parent_output']+'/'+name:pin for name,pin in parent_mf['files'].items()})
    require(exact(expected_owned,plan['parent_complete13_owned_expected_SHA256']) and all(plan['selected_expected_SHA256'][k]==pin for k,pin in expected_owned.items()) and parent_mf['selected_expected_SHA256']==parent_adapter['selected_expected_SHA256']==assessment['original16_expected_SHA256'], 'Every full parent owner pin and original16 expectation retained, with no observed promotion')
    require(parent_ready['ready'] is parent_ready['root_and_independent_static_reviews_passed'] is parent_ready['date2_raw_log_execution_authorized'] is parent_ready['date2_raw_log_transfer_witness_accepted'] is True and parent_ready['author_method_SHA256']==parent_root['author_method_SHA256'] and parent_ready['definition_AST_SHA256']==parent_root['complete_definition_AST_SHA256'] and parent_ready['static_review_expected_SHA256'][plan['parent_SOURCE_peer_path']]==parent_root['independent_source_peer_expected_SHA256'] and parent_ready['static_review_expected_SHA256'][plan['parent_ROOT_source_review_path']]==parent_root['ROOT_source_review_expected_SHA256'], 'Historical parent execution authority is certified data, never current permission')
    parent_witness=inputs[plan['parent_source_witness']]
    require(exact(parent_root['saved_source_prefix_and_coordinate_witness'],parent_witness) and parent_witness['passed'] is parent_witness['all_original_signed144_and_stored72_no_wrap'] is parent_witness['initial_once_drift_twice_four_distinct_driver_slots_once'] is parent_witness['four_coefficient_product_floors_paid'] is parent_witness['same_own_per_coordinate_C_prime'] is parent_witness['nine_term_pointwise_Cauchy_no_error_independence'] is True and parent_witness['provider_native_guard_series_moment_tail_or_source_function_replayed'] is False and exact(parent_witness['prefix'],plan['source_scope_proof']['saved_prefix_witness']), 'Saved fully verified source/marginal/no-wrap witness; no DAG/provider/raw9 recipe replay')
    require(exact(parent_adapter['source_scope_proof'],plan['source_scope_proof']) and parent_root['accepted_interface']==parent_adapter['interface'] and parent_root['SOURCE_SHA256']==assessment['immutable_provenance_expected_SHA256'][plan['parent_SOURCE_path']], 'Original whole source witness and parent source commitment remain unchanged')
    target=inputs[plan['target']];nodes={v:row for row in target['nodes'] for v in row['out']}
    require(type(target['width']) is type(target['fraction_bits']) is int and target['width']==72 and target['fraction_bits']==40 and all(all(exact(nodes[v],row) for v in row['out']) for row in plan['source_scope_proof']['literal_log_rows']), 'Exact stored72 raw prefix/coefficient/drift/initial literal metadata')
    primary=inputs[plan['primary_raw_ranges']]['cases']['B4x12'];independent=inputs[plan['independent_raw_ranges']]['B4x12']
    require(primary['every_stored72_raw_partial_sum_safe'] is primary['every_signed144_scaled_normal_product_safe'] is independent['every_stored_partial_sum_and_product_safe'] is independent['additive_rounding_zero_only_after_no_wrap'] is True and primary['actual_common_literal']==independent['actual_common_raw']==60222732077 and primary['actual_idio_literal']==independent['actual_idio_raw']==73757482253, 'Original nonnegative coefficient literals and all saved no-wrap flags')
    saved72=[r for r in independent['actual_raw_prefix_word_guards'] if r['value'] in {3492,3493,3494,3495,3496,3497,3498,3499,3500,3541,3542,3543}]
    saved144=[r for r in primary['native_full144_product_inventory'] if r['value'] in {3492,3493,3497,3498}]
    require(exact(saved72,plan['source_scope_proof']['saved_independent_signed72_rows']) and exact(saved144,plan['source_scope_proof']['saved_primary_signed144_rows']), 'Every saved signed144 coefficient product and stored72 partial, without guard replay')
    binding=inputs[plan['native_sampler_binding']];theorem=inputs[plan['native_theorem']]
    require(binding['original_target_expected_SHA256']==plan['selected_expected_SHA256'][plan['target']] and binding['digital_pair_independence'] is False and [binding['all_original_joint_pair_scopes'][i]['normal_values'] for i in (0,2,3)]==[[94,125],[326,357],[442,473]] and theorem['original_U_V_uniform_cell_coupling'] is theorem['shifted_second_cosine_exact_three_quarter_circular_grid_slot_same_bound'] is True and theorem['scope']['digital_pair_independence'] is False and theorem['scope']['source_law']=='original_B4_B8_Q32_shared_U_V_BoxMuller_F40_W72', 'Four same own-coordinate marginal orientations on original continuous coupling; native pair stays shared')
    coordinate_root=inputs[plan['coordinate_ROOT_verification']];coordinate_mf=inputs[plan['coordinate_manifest']]
    require(coordinate_root['passed'] is coordinate_root['both_saved_profile_identities_and_same_middle_witness_checked'] is True and coordinate_root['ROOT_external_terminal_exit_code']==0 and coordinate_root['manifest_SHA256']==plan['selected_expected_SHA256'][plan['coordinate_manifest']] and coordinate_root['native_or_radial_SOURCE_called'] is coordinate_root['new_native_arithmetic_or_downstream_financial_recertification'] is False and coordinate_mf['passed'] is coordinate_mf['completed'] is True, 'Completed own per-coordinate C-prime premise, no native recertification')
    for profile,roles in plan['profiles'].items():
        literal=inputs[roles['literal_record']];coordinate=inputs[roles['coordinate_record']];old=inputs[roles['old_nine_term_record']]
        require(roles['allowed_fields']==['aN','bN','ea','eb','e0','ed','tau'] and 'profile' not in literal and {k:literal['exact_rational_components'][k] for k in roles['allowed_fields']}==roles['exact_fixed_allowed_values'] and hashlib.sha256(json.dumps(roles['exact_fixed_allowed_values'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==roles['exact_allowed_values_canonical_JSON_SHA256'], 'Own external path/pin/seven-field operand commitment, no invented literal-record profile')
        require(coordinate['profile']==profile and coordinate['units']=='dimensionless_Gaussian_coordinate_squared' and coordinate['grouped_equals_expanded'] is True and any(exact(coordinate,r) for r in coordinate_root['profile_compositions']) and coordinate_mf['files'][Path(roles['coordinate_record']).name]==plan['selected_expected_SHA256'][roles['coordinate_record']], 'Own completed per-coordinate result exact ROOT/MF member')
        require(old['profile']==profile and old['units']=='squared_error_of_log_price' and old['source_raw_log']==3543 and old['asset_zero_based']==0 and old['contractual_date_one_based']==2 and old['grouped_equals_expanded'] is True and old['native_error_or_previous_log_innovation_independence_assumed'] is False and old['stock_squared_L2_upper'] is None and any(exact(old,r) for r in parent_root['profile_results']) and parent_mf['files'][Path(roles['old_nine_term_record']).name]==plan['selected_expected_SHA256'][roles['old_nine_term_record']], 'Own saved old9 comparison only, never delta selection or formula replay')
    return {'schema':'e11-date2-raw3543-grouped-young-source-norm-witness-v1','passed':True,'accepted_interface':plan['interface'],'saved_parent_source_and_coordinate_witness':parent_witness,'parent_ROOT_expected_SHA256':plan['selected_expected_SHA256'][plan['parent_ROOT_verification']],'parent_manifest_expected_SHA256':plan['selected_expected_SHA256'][plan['parent_manifest']],'full_parent13_owned_expected_SHA256':expected_owned,'original_shared_pair_and_four_marginal_mappings_retained':True,'all_original_signed144_and_stored72_no_wrap_retained':True,'continuous_ideal_coordinate_unit_L2_theorem':'Independent continuous U,V within each pair give integral(-2logU)=2 and integral cos^2(2piV+phi)=1/2, so E Zi^2=1 for either branch; no cross-coordinate/native-error independence needed.','U_error':'aN*(E94+E357)+bN*(E125+E442)','V_error':'(aN-a)*(Z94+Z357)+(bN-b)*(Z125+Z442)+eta','kappa2':'e0+2*ed+4*tau','U_squared_L2_upper':'4*(aN+bN)^2*C_prime','V_squared_L2_upper':'(2*ea+2*eb+kappa2)^2','fixed_delta_exact_pair':[1,100000],'Young_hilbert_space_proof':'Nonnegative squared norm of sqrt(delta)*U-V/sqrt(delta) yields (1+delta)||U||^2+(1+1/delta)||V||^2.','numerical_square_root_required':False,'native_error_covariance_or_previous_log_innovation_independence_assumed':False,'old9_source_DAG_guard_provider_or_recipe_reexecuted':False,'validity_separate_from_comparison_or_adoption':True,'stock_projection_tails_candidate_financial_price_G2_or_quantum_advantage':False}



def compose(profile, plan, inputs):
    roles=plan['profiles'][profile];literal=inputs[roles['literal_record']]['exact_rational_components'];old_record=inputs[roles['old_nine_term_record']]
    require(profile in ('primary90','independent130') and plan['fixed_delta_exact_pair']==[1,100000] and plan['factor_native_exact_pair']==[100001,100000] and plan['factor_literal_exact_pair']==[100001,1], 'Only the one preregistered Young delta and its exact fixed factors')
    values={k:ratio(literal[k]) for k in ('aN','bN','ea','eb','e0','ed','tau')};C=ratio(inputs[roles['coordinate_record']]['composed_original_native_coordinate_squared_L2_upper'])
    require(exact(pair(C),old_record['C_prime']) and exact({k:pair(v) for k,v in values.items()},old_record['allowed_literal_operands']), 'Current operands equal parent saved canonical copies, not recomputed old9')
    a,b,ea,eb,e0,ed,tau=(values[k] for k in ('aN','bN','ea','eb','e0','ed','tau'))
    kappa=plus(e0,plus(twice(ed),times(Fraction(4),tau)));require(exact(pair(kappa),old_record['kappa2']), 'One initial error, two drifts, four paid floors in new grouped recipe')
    native_sum=plus(a,b);literal_sum=plus(plus(twice(ea),twice(eb)),kappa)
    U_squared=times(Fraction(4),times(times(native_sum,native_sum),C));V_squared=times(literal_sum,literal_sum)
    factor_native=ratio(plan['factor_native_exact_pair']);factor_literal=ratio(plan['factor_literal_exact_pair'])
    weighted_U=times(factor_native,U_squared);weighted_V=times(factor_literal,V_squared);grouped=plus(weighted_U,weighted_V)
    native_terms=[times(Fraction(4),times(times(a,a),C)),times(Fraction(8),times(times(a,b),C)),times(Fraction(4),times(times(b,b),C))]
    literal_terms=[times(Fraction(4),times(ea,ea)),times(Fraction(4),times(eb,eb)),times(kappa,kappa),times(Fraction(8),times(ea,eb)),times(Fraction(4),times(ea,kappa)),times(Fraction(4),times(eb,kappa))]
    expanded_terms=[times(factor_native,v) for v in native_terms]+[times(factor_literal,v) for v in literal_terms]
    expanded=Fraction(0)
    for value in (expanded_terms if profile=='primary90' else list(reversed(expanded_terms))):expanded=plus(expanded,value)
    require(grouped==expanded, 'One fixed grouped expression equals its own expanded identity; no alternative bound choice')
    old=limb_ratio(old_record['raw_log_squared_L2_upper']);difference=plus(grouped,-old)
    return {'schema':'e11-date2-raw3543-grouped-fixed-young-limb-bound-v1','profile':profile,'units':'squared_error_of_log_price','source_raw_log':3543,'asset_zero_based':0,'contractual_date_one_based':2,'fixed_delta_exact_pair':[1,100000],'C_prime':pair(C),'allowed_literal_operands':{k:pair(v) for k,v in values.items()},'kappa2':pair(kappa),'native_group_sum':pair(native_sum),'literal_group_sum':pair(literal_sum),'U_squared_L2_upper':pair(U_squared),'V_squared_L2_upper':pair(V_squared),'factor_native':pair(factor_native),'factor_literal':pair(factor_literal),'weighted_native_term':pair(weighted_U),'weighted_literal_term':pair(weighted_V),'grouped_raw_log_squared_L2_upper':pair(grouped),'own_saved_old_nine_term_bound':old_record['raw_log_squared_L2_upper'],'signed_new_minus_old':signed_pair(difference),'comparison':{'nonincreasing':difference<=0,'strictly_smaller':difference<0,'equal':difference==0,'valid_bound_regardless_of_comparison_sign':True,'adoption':False},'grouped_equals_expanded':True,'chosen_formula':'(1+delta)*4*(aN+bN)^2*C_prime+(1+1/delta)*(2*ea+2*eb+kappa2)^2','numerical_sqrt_delta_optimization_adaptive_formula_or_profile_minimum':False,'native_error_covariance_or_previous_log_innovation_independence_assumed':False,'initial_once_drift_twice_four_signed_cmul_floors_paid':True,'own_parent_old9_formula_or_source_DAG_guard_provider_reexecuted':False,'stock_projection_tails_candidate_financial_price_G2_or_quantum_advantage':False}



def owned_guard():
    require(_OWNS_OUTPUT is True and OUTPUT.resolve(strict=True) == OUTPUT and OUTPUT.is_dir() and not OUTPUT.is_symlink() and [stat8(OUTPUT)[i] for i in (0, 1, 4, 5, 6, 7)] == _OUTPUT_ID, 'This-run exclusive output identity')

def save(name,value=None,raw=None):
    owned_guard()
    require(name in LEDGER and not (OUTPUT/name).exists() and not (OUTPUT/name).is_symlink(),'Exclusive registered output')
    if raw is None:
        pending=[value];count=0
        while pending:
            budget();item=pending.pop();count+=1
            require(count<=134217728,'Bounded serialization traversal')
            require(type(item) in (dict,list,tuple,str,int,float,bool,type(None)),'No raw Fraction or unknown serialization object')
            if type(item) is int:require(item.bit_length()<=256,'All emitted JSON integer tokens small; bound limbs are32bit')
            if type(item) is dict:pending.extend(item.values())
            elif type(item) in (list,tuple):pending.extend(item)
        raw=(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    require(len(raw)<=128<<20 and len(list(OUTPUT.iterdir()))<64 and sum(p.stat().st_size for p in OUTPUT.iterdir())+len(raw)<=128<<20,'Owned inclusive file and byte caps')
    h=hashlib.sha256(raw)
    with (OUTPUT/name).open('xb') as stream:
        for start in range(0,len(raw),65536):
            budget();owned_guard();part=raw[start:start+65536]
            require(stream.write(part)==len(part),'Bounded physical write');owned_guard()
    require((OUTPUT/name).stat().st_size==len(raw),'Exact saved bytes')
    return h.hexdigest()


def failure(error):
    if not _OWNS_OUTPUT:
        return
    try:
        owned_guard()
        path = OUTPUT / 'FAILED_UNSEALED.json'
        if not path.exists() and not path.is_symlink():
            with path.open('xb') as stream:
                stream.write((json.dumps({'passed': False, 'completed': False, 'error': type(error).__name__, 'message': str(error)[:1000], 'no_result_credit': True}) + '\n').encode('utf-8'))
    except BaseException:
        pass

def same_profile_comparison(primary, independent):
    require(primary['profile']=='primary90' and independent['profile']=='independent130' and primary['fixed_delta_exact_pair']==independent['fixed_delta_exact_pair']==[1,100000] and primary['grouped_equals_expanded'] is independent['grouped_equals_expanded'] is True, 'Separate required profiles, same fixed delta and own expression identity')
    for record in (primary,independent):
        flags=record['comparison']
        require(set(flags)=={'nonincreasing','strictly_smaller','equal','valid_bound_regardless_of_comparison_sign','adoption'} and all(type(v) is bool for v in flags.values()) and flags['valid_bound_regardless_of_comparison_sign'] is True and flags['adoption'] is False, 'Validity stays separate from every recorded comparison sign and adoption')
    return {'schema':'e11-date2-grouped-young-same-profile-comparison-v1','passed':True,'profiles_kept_separate':True,'fixed_delta_exact_pair':[1,100000],'no_minimum_or_cross_profile_formula_selection':True,'validity_separate_from_improvement':True,'numeric_adoption':False,'profile_comparisons':[{'profile':r['profile'],'own_saved_old_nine_term_bound':r['own_saved_old_nine_term_bound'],'grouped_raw_log_squared_L2_upper':r['grouped_raw_log_squared_L2_upper'],'signed_new_minus_old':r['signed_new_minus_old'],'comparison':r['comparison']} for r in (primary,independent)],'no_old9_recipe_or_source_provider_replay':True,'stock_projection_tails_candidate_or_price_result':None}

def main():
    global _STARTED,_OWNS_OUTPUT,_OUTPUT_ID
    _STARTED=process_started()
    try:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ready-sha256',required=True);args=parser.parse_args()
        base=Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True)==ROOT and Path(__file__).resolve(strict=True)==SOURCE,'Exact isolated default4300')
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256],'Separate original base argv0/venv and exact current absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(),'Pinned isolated paths/no ZIP/no site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'Unused own output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','date2_grouped_young_execution_authorized','date2_grouped_young_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-date2-grouped-fixed-young-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['date2_grouped_young_execution_authorized'] is True,'Own current grouped fixed Young release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['date2_grouped_young_transfer_witness_accepted'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
        code_guard(source_raw,ready)
        caches=['research/limitation_program_20261001/__pycache__/'+SOURCE.stem+'.cpython-312'+s+'.pyc' for s in ('','.opt-1','.opt-2')]
        require(ready['existing_current_cache_SHA256']=={} and ready['absent_current_cache_paths']==sorted(caches) and all(not (ROOT/k).exists() and not (ROOT/k).is_symlink() for k in caches),'Exact unused current3 cache partition')
        inputs={plan['symbolic_PLAN_path']:decode(read_bytes(ROOT/plan['symbolic_PLAN_path'],plan['symbolic_PLAN_expected_SHA256'],records))}
        for key,pin in plan['selected_expected_SHA256'].items():
            data=read_bytes(ROOT/key,pin,records);mode=plan['selected_input_modes'][key]
            require(mode in ('ordinary_json','plaintext_AST_only','plain_text_only'),'No arrays or unknown parsing authority')
            require(stat8(ROOT/key)==plan['selected_original_8_field_fingerprints'][key],'Every originally declared complete8-field identity before decoding')
            inputs[key]=decode(data) if mode=='ordinary_json' else data
        native=inputs[plan['runtime_manifest']];origins=loaded_origins(native,records)
        witness=interface_witness(plan,ready,inputs);controls=controls_record(plan)
        code_guard(source_raw,ready);budget(admission=True)
        OUTPUT.mkdir(exist_ok=False);_OUTPUT_ID=[stat8(OUTPUT)[i] for i in (0,1,4,5,6,7)];_OWNS_OUTPUT=True
        files={}
        for name,data in [('executed_controller.py',source_raw),('executed_adapter.json',plan_raw),('executed_preflight.md',md_raw),('executed_ROOT_READY.json',read_bytes(READY,args.ready_sha256,records))]:files[name]=save(name,raw=data)
        files['run_started.json']=save('run_started.json',{'created_UTC_ns':time.time_ns(),'PID':os.getpid(),'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'default4300_no_setter':True,'current3_bound_before_premises_origins_numbers_output':True})
        files['source_prefix_and_grouped_norm_witness.json']=save('source_prefix_and_grouped_norm_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,inputs);independent=compose('independent130',plan,inputs)
        files['primary_grouped_raw_log_squared_L2.json']=save('primary_grouped_raw_log_squared_L2.json',primary)
        files['independent_grouped_raw_log_squared_L2.json']=save('independent_grouped_raw_log_squared_L2.json',independent)
        comparison=same_profile_comparison(primary,independent);files['same_profile_comparison.json']=save('same_profile_comparison.json',comparison)
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'native_range_guard_tail_moment_series_or_provider_called':False,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','date2_asset0_raw3543_only':True,'fixed_delta_exact_pair':[1,100000],'same_profile_comparison':comparison,'validity_separate_from_improvement_and_no_adoption':True,'old9_recipe_or_source_DAG_provider_called':False,'stock_projection_tails_candidate_or_price_results':None}
        files['summary.json']=save('summary.json',summary)
        require(set(files)==set(LEDGER)-{'manifest.json'} and {p.name for p in OUTPUT.iterdir()}==set(files),'Exact preseal12/no failure')
        manifest={'passed':True,'completed':True,'budget_censored':False,'files':files,'manifest_self_hash_excluded':True,'inclusive_files':13,'author_method_SHA256':authors,'ROOT_READY_expected_SHA256':args.ready_sha256,'selected_expected_SHA256':plan['selected_expected_SHA256'],'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0}
        seal=save('manifest.json',manifest);require({p.name for p in OUTPUT.iterdir()}==set(LEDGER),'Exact sealed13/no failure');budget()
        print(json.dumps({'passed':True,'manifest_SHA256':seal,'fixture_credit':0,'financial_price_policy_G2_or_quantum_advantage':False}),flush=True)
    except BaseException as error:
        failure(error);raise




def times(a,b):
    budget()
    require(max(a.numerator.bit_length()+b.numerator.bit_length(),a.denominator.bit_length()+b.denominator.bit_length())<=524288,'Multiplication temporary bit frontier')
    value=a*b
    require(max(value.numerator.bit_length(),value.denominator.bit_length())<=131072,'Reduced multiplication bit frontier')
    return value

def integer_limbs(value):
    require(type(value) is int and value>=0 and value.bit_length()<=131072,'Nonnegative integer encoding frontier')
    if value==0:return [0]
    result=[]
    while value:
        result.append(value & 4294967295);value >>= 32
    return result

def limbs_integer(values):
    require(type(values) is list and 1<=len(values)<=4096 and all(type(v) is int and 0<=v<=4294967295 for v in values),'Exact bounded32bit limb list, no bool')
    require(len(values)==1 or values[-1]>0,'No leading high zero limb')
    require(32*(len(values)-1)+values[-1].bit_length()<=131072,'Bit frontier before any reconstruction shifts')
    result=0
    for value in reversed(values):result=(result<<32)|value
    return result

def limb_ratio(record):
    require(type(record) is dict and set(record)=={'schema','numerator_sign','numerator_limbs','denominator_limbs'} and record['schema']=='canonical-nonnegative-rational-base2p32-v1','Closed rational limb schema')
    n,d=limbs_integer(record['numerator_limbs']),limbs_integer(record['denominator_limbs'])
    require(d>0 and record['numerator_sign']==('zero' if n==0 else 'positive') and gcd(n,d)==1,'Positive denominator/reduced rational/exact nonnegative sign')
    require(n!=0 or record['denominator_limbs']==[1],'Canonical zero is exactly0/1')
    return Fraction(n,d)


if __name__ == "__main__":
    main()
