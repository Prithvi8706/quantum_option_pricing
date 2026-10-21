'Dormant original date5 four-stock clamp squared-L2, fixedM4608 and both continuous tails; ROOT release required.'

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

SOURCE=ROOT/'research/limitation_program_20261001/experiment_e11_date5_four_stock_fixed_m4608_clipped_squared_l2_v1.py'

PLAN=ROOT/'.context/E11_DATE5_FOUR_STOCK_FIXED_M4608_CLIPPED_SQUARED_L2_INPUT_ADAPTER_run001.json'

MD=ROOT/'.context/E11_DATE5_FOUR_STOCK_FIXED_M4608_CLIPPED_SQUARED_L2_PREFLIGHT_run001.md'

READY=ROOT/'.context/E11_DATE5_FOUR_STOCK_FIXED_M4608_CLIPPED_SQUARED_L2_ROOT_READY_run001.json'

OUTPUT=ROOT/'results/limitation_program_20261001/E11_date5_four_stock_fixed_M4608_clipped_squared_L2_run001'

LEDGER=['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'source_projection_and_continuous_law_witness.json', 'five_metadata_controls.json', 'primary_date5_four_stock_squared_L2.json', 'independent_date5_four_stock_squared_L2.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']

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


def signed_ratio(value):
    require(type(value) is list and len(value)==2 and all(type(v) is int and abs(v).bit_length()<=131072 for v in value) and value[1]>0 and gcd(abs(value[0]),value[1])==1, 'Exact canonical signed original rational pair')
    return Fraction(*value)


def positive_reciprocal(value):
    budget()
    require(type(value) is Fraction and value.numerator>0 and max(value.numerator.bit_length(),value.denominator.bit_length())<=131072, 'Strict positive reduced guard before reciprocal')
    return Fraction(value.denominator,value.numerator)


def fixed_power(value, exponent):
    require(type(value) is Fraction and type(exponent) is int and exponent in (2,16,32), 'Only the prescribed finite powers')
    result=Fraction(1)
    for _ in range(exponent):result=times(result,value)
    return result

def interface_witness(plan, ready, inputs):
    require(ready['date5_four_stock_clamp_transfer_witness_accepted'] is True and exact(ready['interface'], plan['interface']), 'Current original date5 four-stock witness before numerical assembly')
    fixed = {'case':'B4x12','contractual_date_one_based':5,'saved_date_zero_based':4,'assets_zero_based':[0,1,2,3],'stocks':[4153,4549,4945,5341],'raw_logs':[3564,3682,3800,3918],'W':72,'F':40,'profiles':['primary90','independent130'],'M_fixed':4608,'moment_fixed':32,'delta_fixed':[1,100000],'kernel':'original_degree12_full_clipped_domain','projection':'same_signed_clip_interval_on_native_and_continuous_logs','native_error_or_stock_independence_assumed':False}
    require(exact(plan['interface'], fixed), 'One upfront fixed M4608/date5 original-kernel route; no adaptive choice')
    original = inputs[plan['symbolic_PLAN_path']]
    require(original['schema'] == 'e11-date5-four-stock-fixed-M4608-clamp-pilot-plan-v1' and original['scientific_evaluation_performed'] is original['SOURCE_authoring_READY_or_SCI_authorized_by_PLAN'] is False and all(exact(plan[key], original[key]) for key in ('interface','profiles','ideal_law_constants','fixed_expression','selected_expected_SHA256','selected_input_modes','fixed_date5_source_mappings','actual_copied_date5_source_rows','continuous_product_law_witness')), 'Exactly preregistered future operands/law/source roles, not an execution grant')
    assessment = inputs[plan['all48_assessment_path']]
    require(assessment['schema'] == 'e11-B4x12-all48-original-stock-certificate-readonly-feasibility-v1' and assessment['assessment_metadata_checks_passed'] is True and assessment['scientific_evaluation_performed'] is assessment['new_SOURCE_READY_SCI_or_grant_authorized_by_assessment'] is False and assessment['original_actual_target_has_no_prefix_reset'] is True, 'Read-only full48 original mapping, not an execution authority or all48 result')
    acceptance = inputs[plan['accepted_all48_assessment_ROOT_path']]
    require(acceptance['schema'] == 'e11-B4x12-date5-four-stock-pilot-root-authoring-acceptance-v1' and acceptance['passed'] is acceptance['metadata_only'] is acceptance['SOURCE_authoring_authorized'] is True and acceptance['scientific_evaluation_performed'] is acceptance['READY_or_SCI_authorized'] is acceptance['adaptive_M_moment_delta_minimum_or_fallback_authorized'] is False, 'Exact ROOT authoring-only acceptance; current READY grants SCI separately')
    require(acceptance['selected_contractual_date'] == 5 and acceptance['selected_assets'] == [0,1,2,3] and acceptance['selected_stock_ids'] == [4153,4549,4945,5341] and acceptance['selected_fixed_M'] == 4608 and acceptance['selected_fixed_delta'] == [1,100000] and acceptance['selected_fixed_moment'] == 32 and acceptance['selected_lower_exponential_square_cap'] == [1,1073741824] and acceptance['frozen_assessment_M8192_prototype_retained_and_not_adopted'] is True, 'M4608 selected analytically before SCI, preserving the unexecuted8192 assessment unchanged')
    require(acceptance['assessment_expected_SHA256'] == plan['selected_expected_SHA256'][plan['all48_assessment_path']] and acceptance['proof_MD_expected_SHA256'] == plan['selected_expected_SHA256'][plan['all48_proof_MD_path']], 'Exact accepted assessment and whole symbolic proof')
    require(plan['all48_assessment_expected_SHA256'] == plan['selected_expected_SHA256'][plan['all48_assessment_path']] and plan['accepted_all48_assessment_ROOT_expected_SHA256'] == plan['selected_expected_SHA256'][plan['accepted_all48_assessment_ROOT_path']], 'Prior external expected authority, never an observed result pin')
    target = inputs[plan['target']]
    require(type(target['width']) is type(target['fraction_bits']) is int and target['width'] == 72 and target['fraction_bits'] == 40, 'Original full72 F40 target')
    nodes = {value:row for row in target['nodes'] for value in row['out']}
    sampler = inputs[plan['native_sampler_binding']]
    theorem = inputs[plan['native_theorem']]
    native = inputs[plan['runtime_manifest']]
    require(sampler['original_target_expected_SHA256'] == plan['selected_expected_SHA256'][plan['target']] and sampler['pair_count'] == 30 and sampler['normal_argument_slots'] == 60 and sampler['digital_pair_independence'] is False and native['passed'] is native['completed'] is True and len(native['external_runtime_inputs']) == 2842, 'Original saved target/marginal/runtime scope, no native runtime union or digital independence')
    require(theorem['original_U_V_uniform_cell_coupling'] is theorem['shifted_second_cosine_exact_three_quarter_circular_grid_slot_same_bound'] is theorem['two_coordinate_Euclidean_squared_bound_by_sum_not_independence'] is True and theorem['scope']['digital_pair_independence'] is False, 'Same native/continuous midpoint interface; no error independence')
    pairs = sampler['all_original_joint_pair_scopes']
    require(len(pairs) == 30 and len({value for row in pairs for value in row['raw_uniform_values']}) == 60 and {value for row in pairs for value in row['raw_uniform_values']} == set(target['inputs']), 'Thirty disjoint original pairs cover all sixty distinct uniform registers')
    for value in target['inputs']:
        require(nodes[value]['op'] == 'input' and nodes[value]['params']['bits'] == 32 and nodes[value]['params']['preparation'] == 'uniform', 'Original separate uniform-register preparation roles')
    scalar = inputs[plan['scalar_continuous_authority']]
    require(scalar['scope']['source_variables'] == 'Independent U,V uniform onopen(0,1); deterministicfloorcellmidpoints underthesamecoupling', 'Exact original within-pair continuous uniform coupling')
    require(exact(plan['continuous_product_law_witness'], {'continuous_variables':'product of sixty independent uniform(0,1) variables coupled by original Q32 floor-cell midpoints','original_preparation':'sixty separate uniform input registers; tensor uniform preparation','pair_orientation':'R*cos(2piV), R*cos(2pi(V+3/4))=R*sin(2piV)','polar_jacobian':'exp(-(z0^2+z1^2)/2)/(2pi)=phi(z0)*phi(z1)','cross_pair_law':'product over thirty disjoint raw-U/raw-V pairs','unused_partner':'retained in original joint coupling','ideal_only':True,'digital_or_error_independence':False}), 'Explicit full product-law and polar density witness, not marginal-to-joint promotion')
    def literal_form(value, stops, memo):
        if value in stops:return {'boundary':stops[value]}
        if value in memo:return memo[value]
        row = nodes[value]
        arguments = [literal_form(argument, stops, memo) for argument in row['args']]
        if row['op'] in ('add','mul'):arguments.sort(key=lambda item:json.dumps(item,sort_keys=True,separators=(',',':'),ensure_ascii=True))
        result = {'op':row['op'],'params':row['params'],'args':arguments,'output_index':row['out'].index(value)}
        memo[value] = result
        return result
    family_results = []
    for index,row in enumerate(pairs):
        stops = dict(zip(row['raw_uniform_values'], ['raw_U','raw_V']))
        signatures = [hashlib.sha256(json.dumps(literal_form(value, stops, {}),sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest() for value in row['normal_values']]
        expected = assessment['all30_native_marginal_literal_family_witnesses'][index]
        require(expected['pair'] == index and row['normal_values'] == expected['normal_values'] and row['raw_uniform_values'] == expected['raw_uniform_values'] and signatures == expected['whole_normal_family_SHA256'] == assessment['all30_native_marginal_literal_family_witnesses'][0]['whole_normal_family_SHA256'], 'Whole actual native normal literal kernels within each cosine/shifted-sine family; same-middle Cprime transfer only')
        family_results.append({'pair':index,'normal_values':row['normal_values'],'raw_uniform_values':row['raw_uniform_values'],'whole_normal_family_SHA256':signatures})
    primary_raw = inputs[plan['primary_raw_ranges']]['cases']['B4x12']
    independent_raw = inputs[plan['independent_raw_ranges']]['B4x12']
    require(primary_raw['every_stored72_raw_partial_sum_safe'] is primary_raw['every_signed144_scaled_normal_product_safe'] is primary_raw['raw_prefix_proof_before_clips_and_survival'] is independent_raw['every_stored_partial_sum_and_product_safe'] is independent_raw['every_original_driver_once'] is True and primary_raw['addition_rounding_paid'] == 0 and independent_raw['source_reset_or_AS_endpoint_used'] is False, 'Original whole prefix/no-wrap/floor facts; no old guard or provider replay')
    financial = sampler['complete_original_saved_source_case']['financial_roles']
    require(exact(plan['ideal_law_constants'], {'d':[-1,800],'a_squared':[3,1000],'b_squared':[9,2000],'Q':1099511627776,'native_initial_literal_raw':5063438167381,'mean_expression':'ln100+5*d','variance_expression':'5*(a^2+b^2)'}) and financial['actual_common_literal'] == 60222732077 and financial['actual_idio_literal'] == 73757482253 and financial['actual_drift_literal'] == -1374389535 and financial['actual_initial_literal'] == 5063438167381 and financial['native_literal_coefficients_equal_ideal_claimed'] is False, 'New date5 Gaussian law versus distinct original native literals')
    selected = [row for row in assessment['all48_exact_source_driver_floor_and_stock_mappings'] if row['contractual_date_one_based'] == 5]
    require(len(selected) == 4 and [row['stock'] for row in selected] == fixed['stocks'] and [row['raw_log'] for row in selected] == fixed['raw_logs'] and exact(selected, plan['fixed_date5_source_mappings']), 'Exactly four original date5 source instantiations from the full48 assessment')
    for row in plan['actual_copied_date5_source_rows']:
        require(all(exact(nodes[value], row) for value in row['out']), 'All actual prefix/clip/stock literals and branches, before numbers')
    primary_prefix = [row for row in primary_raw['prefixes'] if row['date'] == 4]
    require(len(primary_prefix) == 1 and primary_prefix[0]['actual_raw_log_sites'] == fixed['raw_logs'] and primary_prefix[0]['original_driver_count_per_stock'] == 10, 'Exact original primary date5 ten-driver prefix roles')
    for asset,site in enumerate(selected):
        prefix = [row for row in financial['prefix_witnesses'] if row['date'] == 4 and row['asset'] == asset]
        independent_guard = [row for row in independent_raw['actual_raw_prefix_word_guards'] if row['value'] == site['raw_log']]
        require(len(prefix) == len(independent_guard) == 1 and prefix[0]['stock'] == site['stock'] and prefix[0]['original_normal_indices'] == site['normal_driver_indices'] and prefix[0]['every_driver_multiplicity'] == 1 and prefix[0]['constants'] == [[-1374389535,5],[5063438167381,1]] and independent_guard[0]['raw_bounds'] == primary_prefix[0]['actual_raw_log_bounds'][asset] == site['native_raw_interval_saved'], 'Each own initial/drift/drivers and stored native interval; no all-input inference from first-pair marginals')
    lower_word,upper_word = (nodes[value]['params']['value'] for value in (3490,3491))
    require(type(lower_word) is type(upper_word) is int and 0 <= lower_word < 1<<72 and 0 <= upper_word < 1<<72, 'Exact original unsigned raw72 clip constants')
    signed_clip = [word if word < 1<<71 else word-(1<<72) for word in (lower_word,upper_word)]
    require(signed_clip == plan['signed_clip_raw_bounds'] == [-12193974156573,9145480617430], 'Normalize both original clip constants before signed endpoint equality')
    grouped_root = inputs[plan['verified_grouped_ROOT']]
    grouped_manifest = inputs[plan['verified_grouped_manifest']]
    require(grouped_root['passed'] is grouped_root['completed'] is grouped_root['date2_grouped_young_transfer_witness_accepted'] is True and grouped_root['ROOT_observed_terminal_exit_code'] == 0 and grouped_root['manifest_SHA256'] == plan['selected_expected_SHA256'][plan['verified_grouped_manifest']] and grouped_manifest['passed'] is grouped_manifest['completed'] is True and grouped_manifest['inclusive_files'] == 13, 'Completed saved own Cprime/literal premises, not an inherited date5 bound')
    own = {}
    kernel_bindings = {}
    for profile,roles in plan['profiles'].items():
        pool = inputs[roles['verified_grouped_record']]
        require(pool['profile'] == profile and pool['source_raw_log'] == 3543 and pool['native_error_covariance_or_previous_log_innovation_independence_assumed'] is False and set(pool['allowed_literal_operands']) == {'aN','bN','ea','eb','e0','ed','tau'} and pool in grouped_root['profile_results'] and grouped_manifest['files'][Path(roles['verified_grouped_record']).name] == plan['selected_expected_SHA256'][roles['verified_grouped_record']], 'Exact own saved Cprime/seven operands only; old date2 B/kappa/tails not numeric inputs')
        require(exact(pool['C_prime'], roles['fixed_C_prime']) and exact(pool['allowed_literal_operands'], roles['fixed_literal_pool']), 'Every own-profile reduced input is preregistered and immutable')
        ledger = inputs[roles['ln2_ledger']]
        endpoint = ledger['endpoints'][2]
        require(endpoint['argument_exact'] == [2,1] and endpoint['id'] == 2 and endpoint['fixed_terms'] == endpoint['terms_executed'] == roles['fixed_ln2_terms'] and endpoint['precision_passed'] is True and exact(endpoint['window_exact'][1], roles['fixed_ln2_upper']) and native['frozen_inputs'][roles['ln2_ledger']] == plan['selected_expected_SHA256'][roles['ln2_ledger']], 'Own original certified Ln2 upper endpoint, no log series or profile transplant')
        envelope = inputs[roles['stock_envelope_record']]
        case = envelope['cases']['B4x12'] if profile == 'primary90' else envelope['B4x12']
        bindings = case['actual_sites'] if profile == 'primary90' else case['all_actual_stock_bindings']
        require(len(bindings) == 48 and native['frozen_inputs'][roles['stock_envelope_record']] == plan['selected_expected_SHA256'][roles['stock_envelope_record']] and hashlib.sha256(json.dumps({key:case[key] for key in ('alpha_upper','beta_upper')},sort_keys=True,separators=(',',':')).encode()).hexdigest() == roles['fixed_generic_alpha_beta_commitment'], 'Original complete48 generic kernel and own unchanged alpha/beta')
        current_sites = [next(row for row in bindings if row['stock'] == value) for value in fixed['stocks']]
        require(exact(current_sites, roles['fixed_date5_kernel_bindings']) and all(row['actual_original_support_signature'] == assessment['case_global_kernel']['all48_same_full_support_signature'] for row in current_sites), 'Whole original degree12 support at each of the four exact date5 sites')
        if profile == 'primary90':
            require(case['whole_clipped_integer_domain_covered'] is case['all_positive_stock_stored72_product144_shift_guards_passed'] is case['final_negative_shift_floor_charged_once'] is True and case['retained_classes'] == 30 and [case['lower_clamp_raw'],case['upper_clamp_raw']] == signed_clip, 'Full original72/144/class support and paid signed final floor')
        else:
            require(case['original_degree12_Estrin_no_AS_certificate_transfer'] is True and case['class_count'] == 30 and case['clamp_raw_bounds'] == signed_clip and case['inverse_ln2_raw'] == 1586259972792 and case['ln2_raw'] == 762123384786, 'Independent original whole-domain kernel, no candidate certificate')
        own[profile] = {'C_prime':pool['C_prime'],'literal_pool':pool['allowed_literal_operands'],'alpha':case['alpha_upper'],'beta':case['beta_upper'],'ln2_upper':endpoint['window_exact'][1]}
        kernel_bindings[profile] = current_sites
    witness = {'schema':'e11-date5-four-stock-clamp-Gaussian-source-witness-v1','passed':True,'accepted_interface':fixed,'selected_source_mappings':selected,'native_normal_family_witnesses':family_results,'continuous_product_law_witness':plan['continuous_product_law_witness'],'ideal_mean':'ln100+5*d','ideal_variance':'5*(a^2+b^2)','ten_driver_slots_initial_once_drift_five_floors_ten':True,'native_and_continuous_use_same_signed_clip_interval':signed_clip,'native_clipping_inactive_assumed':False,'clamp_contraction_and_M_exponential_Lipschitz':True,'whole48_original_degree12_kernel_bindings_selected_date5':kernel_bindings,'fixed_M':4608,'M_log_lower_certificate':{'factorization':[9,2],'ln2_lower':[56,81],'ln3_lower':[13,12],'ln_M_lower':[151,18],'native_clip_upper_guard':'18*clip_high<=151*Q'},'fixed_delta':[1,100000],'moment32':True,'lower_tail_exp2_cap':[1,1073741824],'both_new_unconditional_clip_threshold_continuous_tails_required':True,'native_errors_stock_or_digital_pair_independence_assumed':False,'date1_date2_or_candidate_stock_B_A_M_tail_number_consumed':False,'old_provider_native_guard_series_or_recipe_replayed':False,'all48_new_numerical_results_or_whole_financial_completion':False}
    return witness,own



def compose(profile, plan, own):
    require(profile in ('primary90','independent130') and plan['interface']['M_fixed'] == 4608 and plan['interface']['contractual_date_one_based'] == 5, 'Only the upfront fixed M4608/date5 profile')
    constants = plan['ideal_law_constants']
    values = own[profile]
    Q = constants['Q']
    clip_low,clip_high = plan['signed_clip_raw_bounds']
    require(type(clip_low) is type(clip_high) is type(Q) is int and Q == 1099511627776 and max(abs(clip_high).bit_length()+5,Q.bit_length()+8) <= 524288, 'Bounded exact integer M comparison before constructing or using M')
    M_guard = 18*clip_high <= 151*Q
    require(M_guard, 'Fixed analytic ln4608 lower guard; no fallback M')
    M = Fraction(4608)
    delta = Fraction(1,100000)
    t = Fraction(5)
    one = Fraction(1)
    C_prime = limb_ratio(values['C_prime'])
    pool = {key:limb_ratio(value) for key,value in values['literal_pool'].items()}
    require(set(pool) == {'aN','bN','ea','eb','e0','ed','tau'}, 'Own fixed seven-field literal pool')
    alpha,beta,ln2_upper = (ratio(values[key]) for key in ('alpha','beta','ln2_upper'))
    d = signed_ratio(constants['d'])
    a_squared,b_squared = ratio(constants['a_squared']),ratio(constants['b_squared'])
    native_initial = Fraction(constants['native_initial_literal_raw'],Q)
    clip_a,clip_b = Fraction(clip_low,Q),Fraction(clip_high,Q)
    require(max(abs(clip_a.numerator).bit_length()+ln2_upper.denominator.bit_length(),ln2_upper.numerator.bit_length()+clip_a.denominator.bit_length()+4) <= 524288, 'Bounded signed crossproducts before lower exponential guard')
    lower_exp_guard = clip_a.numerator*ln2_upper.denominator <= -15*ln2_upper.numerator*clip_a.denominator
    require(lower_exp_guard and ln2_upper.numerator > 0, 'Own Ln2 upper certifies exp(2*clip_a)<=2^-30 before any tail')
    kappa5 = plus(pool['e0'],plus(times(t,pool['ed']),times(Fraction(10),pool['tau'])))
    if profile == 'primary90':
        native_sum = times(t,plus(pool['aN'],pool['bN']))
        literal_sum = plus(times(t,plus(pool['ea'],pool['eb'])),kappa5)
    else:
        native_sum = plus(times(t,pool['aN']),times(t,pool['bN']))
        literal_sum = plus(plus(times(t,pool['ea']),times(t,pool['eb'])),kappa5)
    U_squared = times(fixed_power(native_sum,2),C_prime)
    V_squared = fixed_power(literal_sum,2)
    native_factor,literal_factor = plus(one,delta),plus(one,positive_reciprocal(delta))
    raw_native_term,raw_literal_term = times(native_factor,U_squared),times(literal_factor,V_squared)
    B_log5 = plus(raw_native_term,raw_literal_term) if profile == 'primary90' else plus(raw_literal_term,raw_native_term)
    raw_expanded = plus(times(native_factor,times(times(t,t),times(fixed_power(plus(pool['aN'],pool['bN']),2),C_prime))),times(literal_factor,fixed_power(plus(plus(times(t,pool['ea']),times(t,pool['eb'])),kappa5),2)))
    require(B_log5 == raw_expanded, 'Fixed ten-term dependence-safe grouped Young identity; no old raw recipe or adaptive minimum')
    mean_center = plus(native_initial,times(t,d))
    mu_lower,mu_upper = plus(mean_center,-pool['e0']),plus(mean_center,pool['e0'])
    variance5 = times(t,plus(a_squared,b_squared))
    lower_distance = plus(mu_lower,-clip_a)
    upper_distance = plus(plus(clip_b,-mu_upper),-twice(variance5))
    tilt_x5 = plus(times(twice(t),d),twice(variance5))
    require(lower_distance.numerator > 0 and upper_distance.numerator > 0 and variance5.numerator > 0 and tilt_x5.numerator >= 0 and tilt_x5.numerator < tilt_x5.denominator, 'Own date5 lower/tilted-upper/variance/x5 positivity before reciprocal or moment tails')
    tilt_mass = times(Fraction(10000),positive_reciprocal(plus(one,-tilt_x5)))
    C16 = one
    factors = plan['C16_factors']
    require(factors == list(range(1,32,2)), 'Exactly the fixed Gaussian moment32 product')
    for factor in (factors if profile == 'primary90' else list(reversed(factors))):C16 = times(C16,Fraction(factor))
    moment32 = times(C16,fixed_power(variance5,16))
    inverse_lower,inverse_upper = positive_reciprocal(lower_distance),positive_reciprocal(upper_distance)
    lower_exp2_cap = Fraction(1,1073741824)
    lower_tail = times(times(lower_exp2_cap,moment32),fixed_power(inverse_lower,32))
    upper_tail = times(times(tilt_mass,moment32),fixed_power(inverse_upper,32))
    A5 = plus(times(alpha,M),beta)
    kernel_squared = fixed_power(A5,2)
    transported_raw = times(fixed_power(M,2),B_log5)
    stages = [kernel_squared,transported_raw,lower_tail,upper_tail]
    ordered = stages if profile == 'primary90' else list(reversed(stages))
    subtotal,expanded = Fraction(0),Fraction(0)
    for stage in ordered:
        subtotal = plus(subtotal,stage)
        expanded = plus(expanded,times(Fraction(3),stage))
    stock_bound = times(Fraction(3),subtotal)
    require(stock_bound == expanded, 'One fixed three-term clamp-transport bound with both disjoint tails, own assembly identity')
    components = {'M5':M,'fixed_delta':delta,'C_prime':C_prime,'kappa5':kappa5,'native_group_sum':native_sum,'literal_group_sum':literal_sum,'U_squared_L2_upper':U_squared,'V_squared_L2_upper':V_squared,'factor_native':native_factor,'factor_literal':literal_factor,'weighted_native_term':raw_native_term,'weighted_literal_term':raw_literal_term,'raw_log5_squared_L2_upper':B_log5,'signed_clip_lower':clip_a,'signed_clip_upper':clip_b,'mean5_center_native_literal_plus_ideal_drift':mean_center,'mu5_lower':mu_lower,'mu5_upper':mu_upper,'variance5':variance5,'own_original_e0':pool['e0'],'original_generic_alpha':alpha,'original_generic_beta':beta,'A5':A5,'lower_distance':lower_distance,'upper_tilted_distance':upper_distance,'tilt_x5':tilt_x5,'tilt_mass_upper':tilt_mass,'C16':C16,'central_moment32':moment32,'lower_exp2_cap':lower_exp2_cap,'new_lower_tail':lower_tail,'new_upper_tail':upper_tail,'kernel_allowance_squared':kernel_squared,'transported_raw_log_squared_L2':transported_raw,'four_stock_common_own_profile_squared_L2_upper':stock_bound}
    signed_fields = {'signed_clip_lower','signed_clip_upper','mean5_center_native_literal_plus_ideal_drift','mu5_lower','mu5_upper'}
    encoded = {key:({'schema':'canonical-signed-rational-base2p32-v1','numerator_sign':'negative' if value.numerator < 0 else 'zero' if value.numerator == 0 else 'positive','absolute_value':pair(abs(value))} if key in signed_fields else pair(value)) for key,value in components.items()}
    return {'schema':'e11-date5-four-original-stock-clamp-squared-L2-limb-bound-v1','profile':profile,'units':'dollars_squared','contractual_date_one_based':5,'assets_zero_based':[0,1,2,3],'source_stocks':[4153,4549,4945,5341],'source_raw_logs':[3564,3682,3800,3918],'own_allowed_literal_operands':values['literal_pool'],'original_ideal_law_constants':constants,'components':encoded,'per_stock_instantiations':[{'asset_zero_based':site['asset_zero_based'],'source_stock':site['stock'],'source_raw_log':site['raw_log'],'source_clipped_log':site['clipped_log'],'bound':pair(stock_bound),'same_profile_same_mean_variance_and_case_global_kernel':True} for site in plan['fixed_date5_source_mappings']],'new_guard_results':{'fixed_M_log_lower_guard_18cliphi_le_151Q':M_guard,'own_Ln2_upper_lower_exp_guard':lower_exp_guard,'lower_distance_strict_positive':True,'upper_tilted_distance_strict_positive':True,'tilt_x5_in_zero_to_one':True,'all_tail_guards_before_reciprocals':True},'fixed_M':4608,'fixed_delta':[1,100000],'fixed_moment_order':32,'grouped_raw_equals_expanded':True,'stock_grouped_equals_expanded':True,'chosen_formula':'3*((alpha*4608+beta)^2+4608^2*B_log5+Tlower5+Tupper5)','both_new_unconditional_continuous_clip_threshold_tails_paid':True,'native_clip_inactive_assumed':False,'native_values_errors_or_stock_independence_assumed':False,'old_date1_date2_M_B_A_kappa_or_tail_numbers_used':False,'all48_certified':False,'candidate_or_whole_financial_price_or_G2_or_quantum_advantage':False,'adaptive_M_delta_moment_profile_minimum_or_bound_adoption':False,'old_provider_guard_series_kernel_or_native_SOURCE_replayed':False}



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
        keys={'schema','ready','root_and_independent_static_reviews_passed','date5_four_stock_execution_authorized','date5_four_stock_clamp_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-date5-four-stock-clamp-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['date5_four_stock_execution_authorized'] is True,'Own current original date5 four-stock release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['date5_four_stock_clamp_transfer_witness_accepted'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        witness,own=interface_witness(plan,ready,inputs);controls=controls_record(plan)
        code_guard(source_raw,ready);budget(admission=True)
        OUTPUT.mkdir(exist_ok=False);_OUTPUT_ID=[stat8(OUTPUT)[i] for i in (0,1,4,5,6,7)];_OWNS_OUTPUT=True
        files={}
        for name,data in [('executed_controller.py',source_raw),('executed_adapter.json',plan_raw),('executed_preflight.md',md_raw),('executed_ROOT_READY.json',read_bytes(READY,args.ready_sha256,records))]:files[name]=save(name,raw=data)
        files['run_started.json']=save('run_started.json',{'created_UTC_ns':time.time_ns(),'PID':os.getpid(),'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'default4300_no_setter':True,'current3_bound_before_premises_origins_numbers_output':True})
        files['source_projection_and_continuous_law_witness.json']=save('source_projection_and_continuous_law_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_date5_four_stock_squared_L2.json']=save('primary_date5_four_stock_squared_L2.json',primary)
        files['independent_date5_four_stock_squared_L2.json']=save('independent_date5_four_stock_squared_L2.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'no_minimum_or_cross_profile_selection':True,'one_prescribed_date5_four_stock_expression':True,'both_own_grouped_expanded_identities':True,'only_own_verified_Cprime_literal_and_original_global_kernel_operands_consumed':True,'both_new_continuous_tails_paid':True,'fixed_M4608_and_moment32':True,'no_native_error_or_stock_independence':True,'old_date1_date2_B_A_M_and_tail_numbers_not_numeric_operands':True,'output_rationals_all_canonical_limbs':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'original_native_range_guard_tail_moment_series_or_provider_called':False,'new_projection_guard_and_both_continuous_tails_assembled':True,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','date5_four_original_native_stocks_only':True,'candidate_or_whole_financial_price_results':None}
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
