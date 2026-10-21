'Dormant date2 asset0 raw-log squared-L2 only; own ROOT release required.'

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

SOURCE = ROOT / 'research/limitation_program_20261001/experiment_e11_second_date_first_raw_log_squared_l2_v1.py'

PLAN = ROOT / '.context/E11_SECOND_DATE_FIRST_RAW_LOG_SQUARED_L2_INPUT_ADAPTER_run001.json'

MD = ROOT / '.context/E11_SECOND_DATE_FIRST_RAW_LOG_SQUARED_L2_PREFLIGHT_run001.md'

READY = ROOT / '.context/E11_SECOND_DATE_FIRST_RAW_LOG_SQUARED_L2_ROOT_READY_run001.json'

OUTPUT = ROOT / 'results/limitation_program_20261001/E11_second_date_first_raw_log_squared_L2_run001'

LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'source_prefix_and_coordinate_witness.json', 'five_metadata_controls.json', 'primary_raw_log_squared_L2.json', 'independent_raw_log_squared_L2.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']

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


def interface_witness(plan, ready, inputs):
    require(ready['date2_raw_log_transfer_witness_accepted'] is True and exact(ready['interface'], plan['interface']), 'Current accepted raw3543 transfer before arithmetic')
    original = inputs[plan['symbolic_PLAN_path']]
    require(original['schema'] == 'e11-second-date-first-raw-log-squared-L2-prospective-plan-v1' and original['scientific_evaluation_performed'] is False and original['SOURCE_authoring_READY_or_SCI_authorized_by_PLAN'] is False, 'Historical prospective plan is not an inherited execution grant')
    require(exact(plan['selected_expected_SHA256'], original['selected_expected_SHA256']) and exact(plan['selected_input_modes'], original['selected_input_modes']) and len(plan['selected_expected_SHA256']) == 16, 'Exactly the accepted16 byte-pinned original roles')
    require(exact(plan['interface'], original['interface']) and exact(plan['profiles'], original['profiles']) and exact(plan['source_scope_proof'], original['source_scope_proof']) and exact(plan['fixed_expression'], original['fixed_expression']), 'Exact own-profile operands/source/prescribed formula')
    require(plan['interface']['source_scope'] == {'case':'B4x12','asset_zero_based':0,'contractual_date_one_based':2,'saved_date_zero_based':1,'raw_log':3543,'previous_raw_log':3542,'innovation':3500,'normal_values':[94,125,357,442],'normal_indices':[0,1,5,6],'W':72,'F':40} and plan['interface']['fixed_Cauchy_terms'] == 9 and plan['interface']['four_signed_cmul_floors_paid'] is True and plan['interface']['error_independence_assumed'] is False, 'Second-date raw log only and pointwise nine-term scope')
    assessment = inputs[plan['accepted_assessment']['path']]
    require(assessment['assessment_metadata_checks_passed'] is True and assessment['SOURCE_or_model_functions_called'] is assessment['arrays_opened_hashed_or_decoded'] is assessment['scientific_evaluation_performed'] is False and exact(assessment['source_ids'], plan['source_scope_proof']['source_ids']), 'Byte-bound assessment supplies exact source IDs, not a numerical result')
    target = inputs[plan['target']]
    require(type(target['width']) is type(target['fraction_bits']) is int and target['width'] == 72 and target['fraction_bits'] == 40, 'Original native full72/F40')
    nodes = {v: row for row in target['nodes'] for v in row['out']}
    for row in plan['source_scope_proof']['literal_log_rows']:
        require(all(exact(nodes[v], row) for v in row['out']), 'Every actual prefix/coefficient/drift/initial source row')
    binding = inputs[plan['native_sampler_binding']]
    require(binding['original_target_expected_SHA256'] == plan['selected_expected_SHA256'][plan['target']] and binding['digital_pair_independence'] is False, 'Original target and shared native pair roles')
    financial = binding['complete_original_saved_source_case']['financial_roles']
    prefix = [r for r in financial['prefix_witnesses'] if r['asset'] == 0 and r['date'] == 1]
    require(len(prefix) == 1 and exact(prefix[0], plan['source_scope_proof']['saved_prefix_witness']), 'Initial once, drift twice, each of four drivers once; no tau-reset model')
    pairs = binding['all_original_joint_pair_scopes']
    require([pairs[i]['normal_values'] for i in (0,2,3)] == [[94,125],[326,357],[442,473]], 'Exact pair0/shared and pair2-shifted/pair3-first cosine orientations')
    theorem = inputs[plan['native_theorem']]
    require(theorem['shifted_second_cosine_exact_three_quarter_circular_grid_slot_same_bound'] is theorem['original_U_V_uniform_cell_coupling'] is True and theorem['scope']['digital_pair_independence'] is False and theorem['scope']['source_law'] == 'original_B4_B8_Q32_shared_U_V_BoxMuller_F40_W72', 'Both marginals inherit the original ideal product-uniform coupling only')
    marginal_results = []
    for row in plan['source_scope_proof']['normal_marginal_witnesses']:
        old = source_signature(nodes, row['old_output'], {int(k):v for k,v in row['old_boundaries'].items()})
        new = source_signature(nodes, row['new_output'], {int(k):v for k,v in row['new_boundaries'].items()})
        require(old['canonical_ordered_except_add_mul_DAG_SHA256'] == new['canonical_ordered_except_add_mul_DAG_SHA256'] == row['canonical_ordered_except_add_mul_DAG_SHA256'] and old['literal_value_count_excluding_declared_boundaries'] == new['literal_value_count_excluding_declared_boundaries'] == row['literal_value_count_excluding_boundaries'], 'Full literal DAG with only add/mul commutations and exact same branch')
        marginal_results.append({'old_output':row['old_output'],'new_output':row['new_output'],'old_literal_scope':old,'new_literal_scope':new})
    primary = inputs[plan['primary_raw_ranges']]['cases']['B4x12']
    independent = inputs[plan['independent_raw_ranges']]['B4x12']
    require(primary['every_stored72_raw_partial_sum_safe'] is primary['every_signed144_scaled_normal_product_safe'] is independent['every_stored_partial_sum_and_product_safe'] is independent['additive_rounding_zero_only_after_no_wrap'] is True, 'Complete original signed144 products and stored72 partial no-wrap')
    require(primary['actual_common_literal'] == independent['actual_common_raw'] == 60222732077 and primary['actual_idio_literal'] == independent['actual_idio_raw'] == 73757482253 and primary['actual_drift_literal'] == independent['actual_drift_raw'] == -1374389535 and primary['actual_initial_literal'] == independent['actual_initial_raw'] == 5063438167381, 'Exact shared source coefficient and initial/drift literals')
    selected72 = [r for r in independent['actual_raw_prefix_word_guards'] if r['value'] in {3492,3493,3494,3495,3496,3497,3498,3499,3500,3541,3542,3543}]
    selected144 = [r for r in primary['native_full144_product_inventory'] if r['value'] in {3492,3493,3497,3498}]
    require(exact(selected72,plan['source_scope_proof']['saved_independent_signed72_rows']) and exact(selected144,plan['source_scope_proof']['saved_primary_signed144_rows']), 'Every required partial and all four coefficient-floor products, not sampled points')
    raw_prefix = [r for r in primary['prefixes'] if r['date'] == 1]
    require(len(raw_prefix) == 1 and raw_prefix[0]['original_driver_count_per_stock'] == 4 and raw_prefix[0]['original_driver_multiplicity'] == 1 and raw_prefix[0]['original_drift_multiplicity'] == 2 and raw_prefix[0]['actual_raw_log_sites'][0] == 3543 and raw_prefix[0]['actual_raw_log_bounds'][0] == [3248283927019,6873094849599], 'Actual date2 prefix support/multiplicity without projection or exponentiation')
    for source_key, expected in plan['source_definition_AST_SHA256'].items():
        tree = ast.parse(inputs[source_key])
        actual = {n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in expected}
        require(actual == expected, 'Pinned prefix builder, Box-Muller marginal and signed floor semantics as plaintext only')
    root = inputs[plan['coordinate_ROOT_verification']]; mf = inputs[plan['coordinate_manifest']]
    require(root['passed'] is True and type(root['ROOT_external_terminal_exit_code']) is int and root['ROOT_external_terminal_exit_code'] == 0 and root['both_saved_profile_identities_and_same_middle_witness_checked'] is True and root['native_or_radial_SOURCE_called'] is root['new_native_arithmetic_or_downstream_financial_recertification'] is False and root['manifest_SHA256'] == plan['selected_expected_SHA256'][plan['coordinate_manifest']] and mf['passed'] is mf['completed'] is True, 'Completed coordinate ROOT certificate precedes own log transfer')
    allowed = ['aN','bN','ea','eb','e0','ed','tau']
    for profile, roles in plan['profiles'].items():
        coordinate = inputs[roles['coordinate_record']]
        require(coordinate['profile'] == profile and exact(next(r for r in root['profile_compositions'] if r['profile'] == profile), coordinate) and mf['files'][Path(roles['coordinate_record']).name] == plan['selected_expected_SHA256'][roles['coordinate_record']], 'Exact own-profile ROOT composition and seal, not another coordinate or pair sum')
        require(coordinate['units'] == 'dimensionless_Gaussian_coordinate_squared' and coordinate['grouped_equals_expanded'] is True and coordinate['native_sampler_or_arithmetic_proof_reexecuted'] is False and roles['C_prime_JSON_pointer'] == ['composed_original_native_coordinate_squared_L2_upper'], 'Only the completed per-coordinate C-prime quantity')
        components = inputs[roles['literal_record']]
        actual = {k:components['exact_rational_components'][k] for k in allowed}
        require(roles['allowed_fields'] == allowed and exact(actual,roles['exact_fixed_allowed_values']) and hashlib.sha256(json.dumps(actual,sort_keys=True,separators=(',',':')).encode()).hexdigest() == roles['exact_allowed_values_canonical_JSON_SHA256'], 'Only the seven accepted literal-error/coefficient fields; old B/kappa are excluded')
        require(components['addition_rounding_zero_after_no_wrap_only'] is components['all_original_signed144_products_and_stored72_partials_required'] is components['original_shared94_125_pair_not_independent'] is components['two_signed_cmul_floor_errors_paid'] is True and 'profile' not in components, 'Own-profile role is externally pinned by its exact literal-record path/SHA and fixed seven-field commitment, not an invented profile field')
    return {'schema':'e11-date2-raw3543-source-and-coordinate-witness-v1','passed':True,'accepted_interface':plan['interface'],'prefix':prefix[0],'marginal_results':marginal_results,'all_original_signed144_and_stored72_no_wrap':True,'initial_once_drift_twice_four_distinct_driver_slots_once':True,'four_coefficient_product_floors_paid':True,'same_own_per_coordinate_C_prime':True,'nine_term_pointwise_Cauchy_no_error_independence':True,'new_stock_projection_tail_candidate_alpha_price_G2_or_phase_certificate':False,'old_B_kappa_M_tail_degree12_alpha_used_as_numeric_operand':False,'provider_native_guard_series_moment_tail_or_source_function_replayed':False}



def compose(profile, plan, inputs):
    roles = plan['profiles'][profile]
    literal = inputs[roles['literal_record']]['exact_rational_components']
    values = {key:ratio(literal[key]) for key in ('aN','bN','ea','eb','e0','ed','tau')}
    C_prime = ratio(inputs[roles['coordinate_record']]['composed_original_native_coordinate_squared_L2_upper'])
    a2,b2 = times(values['aN'],values['aN']),times(values['bN'],values['bN'])
    ea2,eb2 = times(values['ea'],values['ea']),times(values['eb'],values['eb'])
    kappa2 = plus(values['e0'],plus(twice(values['ed']),times(Fraction(4),values['tau'])))
    kappa_squared = times(kappa2,kappa2)
    coordinate_term = twice(times(plus(a2,b2),C_prime))
    literal_term = twice(plus(ea2,eb2))
    grouped = times(Fraction(9),plus(plus(coordinate_term,literal_term),kappa_squared))
    expanded_terms = [times(Fraction(18),times(a2,C_prime)),times(Fraction(18),times(b2,C_prime)),times(Fraction(18),ea2),times(Fraction(18),eb2),times(Fraction(9),kappa_squared)]
    expanded = Fraction(0)
    for value in (expanded_terms if profile == 'primary90' else list(reversed(expanded_terms))):
        expanded = plus(expanded,value)
    require(grouped == expanded, 'One preregistered grouped raw-log bound equals its expanded identity; no minimum choice')
    return {'schema':'e11-date2-first-raw-log-squared-L2-limb-bound-v1','profile':profile,'units':'squared_error_of_log_price','source_raw_log':3543,'asset_zero_based':0,'contractual_date_one_based':2,'source_driver_values':[94,125,357,442],'C_prime':pair(C_prime),'allowed_literal_operands':{k:pair(v) for k,v in values.items()},'kappa2':pair(kappa2),'coordinate_term_before_factor9':pair(coordinate_term),'literal_term_before_factor9':pair(literal_term),'deterministic_term_before_factor9':pair(kappa_squared),'raw_log_squared_L2_upper':pair(grouped),'grouped_equals_expanded':True,'chosen_formula':'9*(2*(aN^2+bN^2)*C_prime+2*(ea^2+eb^2)+(e0+2*ed+4*tau)^2)','pointwise_Cauchy_terms':9,'native_error_or_previous_log_innovation_independence_assumed':False,'four_signed_coefficient_product_floors_paid':True,'addition_rounding_zero_only_after_no_wrap':True,'initial_ln100_once_no_extra100':True,'old_B_kappa_M_tail_degree12_alpha_used_as_numeric_operand':False,'native_guard_range_series_moment_tail_or_provider_reexecuted':False,'stock_squared_L2_upper':None,'candidate_alpha_beta_or_projection_tail_certificate':None,'financial_price_G2_hardware_or_quantum_advantage':False}



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
        keys={'schema','ready','root_and_independent_static_reviews_passed','date2_raw_log_execution_authorized','date2_raw_log_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-date2-first-raw-log-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['date2_raw_log_execution_authorized'] is True,'Own current raw-log release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['date2_raw_log_transfer_witness_accepted'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
        code_guard(source_raw,ready)
        caches=['research/limitation_program_20261001/__pycache__/'+SOURCE.stem+'.cpython-312'+s+'.pyc' for s in ('','.opt-1','.opt-2')]
        require(ready['existing_current_cache_SHA256']=={} and ready['absent_current_cache_paths']==sorted(caches) and all(not (ROOT/k).exists() and not (ROOT/k).is_symlink() for k in caches),'Exact unused current3 cache partition')
        inputs={plan['symbolic_PLAN_path']:decode(read_bytes(ROOT/plan['symbolic_PLAN_path'],plan['symbolic_PLAN_expected_SHA256'],records))}
        for key,pin in plan['selected_expected_SHA256'].items():
            data=read_bytes(ROOT/key,pin,records);mode=plan['selected_input_modes'][key]
            require(mode in ('ordinary_json','plaintext_AST_only'),'No arrays or unknown parsing authority')
            require(stat8(ROOT/key)==plan['selected_original_8_field_fingerprints'][key],'Every originally declared complete8-field identity before decoding')
            inputs[key]=decode(data) if mode=='ordinary_json' else data
        native=inputs[plan['runtime_manifest']];origins=loaded_origins(native,records)
        witness=interface_witness(plan,ready,inputs);controls=controls_record(plan)
        code_guard(source_raw,ready);budget(admission=True)
        OUTPUT.mkdir(exist_ok=False);_OUTPUT_ID=[stat8(OUTPUT)[i] for i in (0,1,4,5,6,7)];_OWNS_OUTPUT=True
        files={}
        for name,data in [('executed_controller.py',source_raw),('executed_adapter.json',plan_raw),('executed_preflight.md',md_raw),('executed_ROOT_READY.json',read_bytes(READY,args.ready_sha256,records))]:files[name]=save(name,raw=data)
        files['run_started.json']=save('run_started.json',{'created_UTC_ns':time.time_ns(),'PID':os.getpid(),'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'default4300_no_setter':True,'current3_bound_before_premises_origins_numbers_output':True})
        files['source_prefix_and_coordinate_witness.json']=save('source_prefix_and_coordinate_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,inputs);independent=compose('independent130',plan,inputs)
        files['primary_raw_log_squared_L2.json']=save('primary_raw_log_squared_L2.json',primary)
        files['independent_raw_log_squared_L2.json']=save('independent_raw_log_squared_L2.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'no_minimum_or_cross_profile_selection':True,'one_prescribed_nine_term_expression':True,'both_own_grouped_expanded_identities':True,'only_C_prime_and_seven_literal_operands_consumed':True,'four_signed_cmul_floors_paid':True,'old_B_kappa_M_tails_alpha_not_numeric_operands':True,'output_rationals_all_canonical_limbs':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'native_range_guard_tail_moment_series_or_provider_called':False,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','date2_asset0_raw3543_only':True,'stock_projection_tails_candidate_or_price_results':None}
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
