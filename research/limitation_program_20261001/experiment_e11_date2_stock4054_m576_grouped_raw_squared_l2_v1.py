'Dormant original date2 stock4054 M576 with verified grouped raw and saved-tail reuse; ROOT release required.'

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

SOURCE=ROOT/'research/limitation_program_20261001/experiment_e11_date2_stock4054_m576_grouped_raw_squared_l2_v1.py'

PLAN=ROOT/'.context/E11_DATE2_STOCK4054_FIXED_M576_GROUPED_RAW_SQUARED_L2_INPUT_ADAPTER_run001.json'

MD=ROOT/'.context/E11_DATE2_STOCK4054_FIXED_M576_GROUPED_RAW_SQUARED_L2_PREFLIGHT_run001.md'

READY=ROOT/'.context/E11_DATE2_STOCK4054_FIXED_M576_GROUPED_RAW_SQUARED_L2_ROOT_READY_run001.json'

OUTPUT=ROOT/'results/limitation_program_20261001/E11_date2_stock4054_M576_grouped_raw_squared_L2_run001'

LEDGER=['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'source_projection_and_saved_tail_witness.json', 'five_metadata_controls.json', 'primary_stock4054_M576_squared_L2.json', 'independent_stock4054_M576_squared_L2.json', 'same_profile_comparison.json', 'summary.json', 'manifest.json']

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

def signed_pair(value):
    require(type(value) is Fraction and value.denominator>0 and max(abs(value.numerator).bit_length(),value.denominator.bit_length())<=131072 and gcd(abs(value.numerator),value.denominator)==1, 'Canonical reduced signed rational within the unchanged bit cap')
    return {'schema':'canonical-signed-rational-base2p32-v1','numerator_sign':'zero' if value.numerator==0 else 'positive' if value.numerator>0 else 'negative','numerator_limbs':integer_limbs(abs(value.numerator)),'denominator_limbs':integer_limbs(value.denominator)}

def interface_witness(plan, ready, inputs):
    require(ready['date2_stock4054_M576_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']), 'Current fixedM576 stock4054 release before numerical assembly')
    symbolic=inputs[plan['symbolic_PLAN_path']]
    require(symbolic['schema']=='e11-date2-stock4054-M576-grouped-prospective-plan-v1' and symbolic['metadata_only'] is True and symbolic['scientific_evaluation_performed'] is symbolic['SOURCE_READY_or_SCI_authorized_by_PLAN'] is False and all(exact(plan[k],symbolic[k]) for k in ('interface','profiles','source_scope_proof','ideal_law_constants','selected_expected_SHA256','selected_input_modes','parent_stock_full13_expected_SHA256','grouped_raw_full13_expected_SHA256')), 'One fixed prospective route and exact expected operands')
    assessment=inputs[plan['accepted_assessment_path']];acceptance=inputs[plan['ROOT_assessment_review_path']]
    require(assessment['schema']=='e11-date2-stock4054-fixed-M576-grouped-raw-feasibility-assessment-v1' and assessment['assessment_metadata_checks_passed'] is True and assessment['scientific_evaluation_performed'] is assessment['SOURCE_or_guard_control_bound_moment_tail_kernel_or_provider_called'] is False and assessment['fixed_M_new']==576 and assessment['M_selected_before_future_SCI_guard_or_results'] is True and assessment['new_SOURCE_READY_or_SCI_authorized_by_assessment'] is False, 'Pinned prospective M576 choice before endpoint guard or outcomes')
    require(acceptance['schema']=='root-e11-date2-stock4054-fixed-M576-groupedraw-assessment-acceptance-v1' and acceptance['passed'] is acceptance['science_static_passed'] is acceptance['lifecycle_static_passed'] is acceptance['metadata_only'] is acceptance['source_authoring_within_existing_user_authorization'] is acceptance['independent_exact_current_SOURCE_review_still_required'] is acceptance['one_future_independently_ROOT_verified_groupedraw_run002_required'] is True and acceptance['blockers']==[] and acceptance['scientific_evaluation_performed'] is acceptance['new_guards_bounds_comparisons_or_ratio_decode_performed'] is acceptance['READY_or_SCI_or_numeric_adoption_authorized'] is False and acceptance['assessment_expected_SHA256']==plan['selected_expected_SHA256'][plan['accepted_assessment_path']] and acceptance['proof_MD_expected_SHA256']==plan['selected_expected_SHA256'][plan['assessment_proof_MD_path']], 'Pinned ROOT assessment acceptance; current READY alone licenses SCI')
    expected_scope={'case':'B4x12','asset_zero_based':0,'contractual_date_one_based':2,'saved_date_zero_based':1,'raw_log':3543,'clipped_log':3583,'remainder':4026,'polynomial':4053,'count':4023,'stock':4054,'F':40,'W':72}
    require(exact(plan['interface']['source_scope'],expected_scope) and exact(assessment['scope'],expected_scope) and exact(plan['source_scope_proof'],assessment['source_scope_proof_unchanged']) and exact(plan['ideal_law_constants'],assessment['ideal_law_constants_unchanged']), 'Exact original date2 asset0 degree12 stock4054 and immutable law/source operands')
    require(exact(plan['interface']['fixed_parameters'],{'M':576,'parent_M':1024,'moment_order':32,'grouped_delta_exact_pair':[1,100000],'failed_guard_retuning_or_M_fallback':False}) and exact(plan['interface']['grouped_profile_and_source_match'],{'raw_log':3543,'drivers':[94,125,357,442],'same_own_C_prime_and_seven_literals':True}) and exact(plan['interface']['tail_reuse'],{'lower_scale_exact_pair':[576,1024],'lower_scale_squared':True,'upper_saved_identical':True,'both_unconditional_continuous_tails_paid':True}) and exact(plan['interface']['qualification'],{'extra_spot_multiplier':1,'native_error_or_stock_independence_assumed':False,'candidate_or_date1_kernel_operand_used':False,'adaptive_M_formula_profile_minimum_or_numeric_adoption':False}), 'Fixed parameters, two unconditional tails and excluded alternatives')
    require(exact(assessment['analytic_log_lower_certificate'],plan['analytic_log_lower_certificate']) and exact(plan['analytic_log_lower_certificate'],{'identity':'ln((1+x)/(1-x))=2*integral_0^x 1/(1-t^2) dt','integrand_lower':'1/(1-t^2)>=1+t^2; remainder t^4/(1-t^2)>=0 for0<=t<1','ln2_lower_exact_pair':[56,81],'ln2_x_exact_pair':[1,3],'ln3_lower_exact_pair':[13,12],'ln3_x_exact_pair':[1,2],'ln576_lower_exact_pair':[341,54],'lower_combination':'6*(56/81)+2*(13/12)=341/54','no_transcendental_numeric_evaluation':True}), 'Analytic fixed rational ln576 lower certificate, no new logarithm evaluation')
    parent_root=inputs[plan['parent_stock_ROOT']];parent_mf=inputs[plan['parent_stock_manifest']];parent_adapter=inputs[plan['parent_stock_adapter']];parent_ready=inputs[plan['parent_stock_READY']];parent_witness=inputs[plan['parent_stock_witness']]
    require(parent_root['passed'] is parent_root['completed'] is parent_root['date2_stock4054_projection_transfer_witness_accepted'] is parent_root['date2_asset0_original_native_stock4054_only'] is parent_root['both_unconditional_continuous_tails_paid'] is True and type(parent_root['ROOT_observed_terminal_exit_code']) is int and parent_root['ROOT_observed_terminal_exit_code']==0 and parent_root['fixed_M2']==1024 and parent_root['fixed_moment_order']==32 and parent_root['native_error_or_previous_log_innovation_or_stock_independence_assumed'] is False and parent_root['candidate_or_whole_financial_price_results'] is None, 'Completed own original M1024 stock certificate with both unconditional tails')
    require(parent_root['manifest_SHA256']==plan['selected_expected_SHA256'][plan['parent_stock_manifest']] and parent_root['SOURCE_SHA256']==plan['selected_expected_SHA256'][plan['parent_stock_SOURCE']] and parent_mf['passed'] is parent_mf['completed'] is True and parent_mf['budget_censored'] is False and type(parent_mf['inclusive_files']) is int and parent_mf['inclusive_files']==13 and set(parent_mf['files'])==set(parent_adapter['exact13_inclusive_ledger'])-{'manifest.json'}, 'Sealed parent stock13/source, not a partial result')
    parent_owned={plan['parent_stock_output']+'/manifest.json':plan['selected_expected_SHA256'][plan['parent_stock_manifest']]};parent_owned.update({plan['parent_stock_output']+'/'+name:pin for name,pin in parent_mf['files'].items()})
    require(exact(parent_owned,plan['parent_stock_full13_expected_SHA256']) and exact(parent_owned,assessment['parent_complete13_owned_expected_SHA256']) and all(plan['selected_expected_SHA256'][key]==pin for key,pin in parent_owned.items()) and parent_ready['ready'] is parent_ready['date2_stock4054_execution_authorized'] is parent_ready['date2_stock4054_projection_transfer_witness_accepted'] is True and parent_ready['author_method_SHA256']==parent_root['author_method_SHA256'] and parent_ready['definition_AST_SHA256']==parent_root['complete_definition_AST_SHA256'], 'All parent stock ownership pins and verified review/READY metadata remain data, not current permission')
    require(exact(parent_root['saved_source_projection_and_continuous_law_witness'],parent_witness) and parent_witness['passed'] is parent_witness['native_clip_inactive_after_signed_containment'] is parent_witness['ideal_continuous_Gaussian_law_from_original_product_uniform_BoxMuller'] is parent_witness['both_unconditional_continuous_tails_required'] is parent_witness['original_signed144_stored72_and_floor_guards_retained'] is True and parent_witness['new_M_fixed']==1024 and parent_witness['native_values_errors_previous_log_or_stock_independence_assumed'] is parent_witness['candidate_site2_alpha_or120_cell_financial_application_used'] is parent_witness['date1_M256_B_kappa_A_tail_numbers_or_alpha_adapter_used'] is False, 'Saved original complete degree12 source/clip/law/floor witness, no source DAG/provider replay')
    require(exact(parent_adapter['source_scope_proof'],plan['source_scope_proof']) and exact(parent_adapter['ideal_law_constants'],plan['ideal_law_constants']) and exact(parent_witness['selected_scope'],expected_scope) and exact(parent_witness['native_raw_interval'],[3248283927019,6873094849599]) and exact(parent_witness['signed_clip_constants'],[-12193974156573,9145480617430]) and parent_witness['ideal_mean']=='ln100+2*d' and parent_witness['ideal_variance']=='2*(a^2+b^2)', 'Original signed72 clip endpoints, source interval and own continuous Gaussian law stay unchanged')
    grouped_root=inputs[plan['grouped_raw_ROOT']];grouped_mf=inputs[plan['grouped_raw_manifest']];grouped_adapter=inputs[plan['grouped_raw_adapter']];grouped_ready=inputs[plan['grouped_raw_READY']];grouped_witness=inputs[plan['grouped_raw_witness']]
    require(grouped_root['passed'] is grouped_root['completed'] is grouped_root['date2_grouped_young_transfer_witness_accepted'] is grouped_root['date2_asset0_raw3543_only'] is True and type(grouped_root['ROOT_observed_terminal_exit_code']) is int and grouped_root['ROOT_observed_terminal_exit_code']==0 and grouped_root['fixed_delta_exact_pair']==[1,100000] and grouped_root['numeric_adoption'] is grouped_root['native_error_or_previous_log_innovation_independence_assumed'] is False and grouped_root['stock_projection_tails_candidate_or_price_results'] is None, 'Separately verified grouped run002 raw3543 prerequisite, not an anticipated result')
    require(grouped_root['SOURCE_SHA256']==plan['selected_expected_SHA256'][plan['grouped_raw_SOURCE']] and grouped_root['manifest_SHA256']==plan['selected_expected_SHA256'][plan['grouped_raw_manifest']] and grouped_mf['passed'] is grouped_mf['completed'] is True and grouped_mf['budget_censored'] is False and grouped_mf['inclusive_files']==13 and set(grouped_mf['files'])==set(grouped_adapter['exact13_inclusive_ledger'])-{'manifest.json'}, 'Verified grouped SOURCE and complete sealed owner13')
    grouped_owned={plan['grouped_raw_output']+'/manifest.json':plan['selected_expected_SHA256'][plan['grouped_raw_manifest']]};grouped_owned.update({plan['grouped_raw_output']+'/'+name:pin for name,pin in grouped_mf['files'].items()})
    require(exact(grouped_owned,plan['grouped_raw_full13_expected_SHA256']) and all(plan['selected_expected_SHA256'][key]==pin for key,pin in grouped_owned.items()) and grouped_ready['ready'] is grouped_ready['date2_grouped_young_execution_authorized'] is grouped_ready['date2_grouped_young_transfer_witness_accepted'] is True and grouped_ready['author_method_SHA256']==grouped_root['author_method_SHA256'] and grouped_ready['definition_AST_SHA256']==grouped_root['complete_definition_AST_SHA256'] and exact(grouped_root['saved_source_prefix_and_grouped_norm_witness'],grouped_witness), 'Every grouped owner and saved source/norm witness joined by expected authority')
    require(grouped_witness['passed'] is grouped_witness['original_shared_pair_and_four_marginal_mappings_retained'] is grouped_witness['all_original_signed144_and_stored72_no_wrap_retained'] is True and grouped_witness['fixed_delta_exact_pair']==[1,100000] and grouped_witness['native_error_covariance_or_previous_log_innovation_independence_assumed'] is grouped_witness['old9_source_DAG_guard_provider_or_recipe_reexecuted'] is False and exact(grouped_adapter['source_scope_proof']['saved_prefix_witness'],plan['source_scope_proof']['saved_prefix_witness']), 'Same original four drivers/floors/native coupling and no raw9 or source recipe replay')
    expected_parent_components={'M2','native_interval_lower','native_interval_upper','mu2_lower','mu2_upper','variance2','own_original_e0','site4054_original_generic_alpha','site4054_original_generic_beta','A2','new_lower_distance','new_upper_tilted_distance','tilt_x2','tilt_mass_upper','C16','central_moment32','new_lower_tail','new_upper_tail','verified_raw3543_squared_L2','native_exponential_allowance_squared','transported_raw_log_squared_L2','stock4054_squared_L2_upper'}
    expected_parent_guards={'M_b_le_20_over3':True,'lower_distance_strict_positive':True,'upper_tilted_distance_strict_positive':True,'tilt_x_in_zero_to_one':True,'all_guards_before_reciprocals':True}
    own={}
    for profile,roles in plan['profiles'].items():
        require(profile in ('primary90','independent130') and roles['profile']==profile, 'Own original90/130 profiles remain separate')
        old=inputs[roles['parent_stock_record']];grouped=inputs[roles['grouped_raw_record']];requirements=assessment['profiles'][profile]['groupedraw_matching_requirements']
        require(old['schema']=='e11-date2-original-native-stock4054-squared-L2-limb-bound-v1' and old['profile']==profile and old['units']=='dollars_squared' and old['source_raw_log']==3543 and old['source_stock']==4054 and old['asset_zero_based']==0 and old['contractual_date_one_based']==2 and old['fixed_M2']==1024 and old['fixed_moment_order']==32 and old['grouped_equals_expanded'] is old['both_unconditional_continuous_tails_paid'] is old['site4054_case_global_original_degree12_envelope_instantiated'] is True and old['native_values_errors_previous_log_or_stock_independence_assumed'] is old['date1_M_B_kappa_A_tails_or_alpha_adapter_used'] is old['candidate_D4S4_site2_alpha_or_financial_bound_used'] is False and old['extra_spot_multiplier']==1 and exact(old['original_ideal_law_constants'],plan['ideal_law_constants']) and set(old['components'])==expected_parent_components and exact(old['new_guard_results'],expected_parent_guards), 'Typed complete original own stock components and certified positivity/moment/tail premises')
        require(any(exact(old,row) for row in parent_root['profile_results']) and parent_mf['files'][Path(roles['parent_stock_record']).name]==plan['selected_expected_SHA256'][roles['parent_stock_record']] and plan['selected_expected_SHA256'][roles['parent_stock_record']]==assessment['profiles'][profile]['parent_stock_record']['expected_SHA256'], 'Own old stock result is a completed ROOT/MF member, never a substituted baseline')
        require(grouped['schema']=='e11-date2-raw3543-grouped-fixed-young-limb-bound-v1' and grouped['profile']==profile and grouped['units']=='squared_error_of_log_price' and grouped['source_raw_log']==3543 and grouped['asset_zero_based']==0 and grouped['contractual_date_one_based']==2 and grouped['fixed_delta_exact_pair']==[1,100000] and grouped['grouped_equals_expanded'] is grouped['initial_once_drift_twice_four_signed_cmul_floors_paid'] is True and grouped['native_error_covariance_or_previous_log_innovation_independence_assumed'] is False and any(exact(grouped,row) for row in grouped_root['profile_results']) and grouped_mf['files'][Path(roles['grouped_raw_record']).name]==plan['selected_expected_SHA256'][roles['grouped_raw_record']], 'Own completed grouped record selected regardless of its comparison sign')
        require(hashlib.sha256(json.dumps(grouped['C_prime'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==requirements['own_C_prime_limbs_canonical_JSON_SHA256'] and hashlib.sha256(json.dumps(grouped['allowed_literal_operands'],sort_keys=True,separators=(',',':')).encode()).hexdigest()==requirements['allowed_literal_limbs_canonical_JSON_SHA256'] and set(grouped['allowed_literal_operands'])=={'aN','bN','ea','eb','e0','ed','tau'} and exact(grouped['allowed_literal_operands']['e0'],old['components']['own_original_e0']), 'Same own Cprime/seven original literals/initial allowance by canonical saved commitments, not old raw comparison min')
        require(parent_witness['site4054_original_global_kernel_bindings'][profile]['alpha_beta_commitment']==assessment['profiles'][profile]['original_generic_alpha_beta_expected_commitment'], 'Own original generic degree12 alpha/beta commitment, no candidate or date1 adapter')
        own[profile]={'old_stock_record':old,'grouped_raw_record':grouped}
    return {'schema':'e11-date2-stock4054-M576-saved-tail-source-witness-v1','passed':True,'accepted_interface':plan['interface'],'selected_scope':expected_scope,'saved_parent_source_projection_and_continuous_law_witness':parent_witness,'parent_stock_ROOT_expected_SHA256':plan['selected_expected_SHA256'][plan['parent_stock_ROOT']],'parent_stock_manifest_expected_SHA256':plan['selected_expected_SHA256'][plan['parent_stock_manifest']],'grouped_raw_ROOT_expected_SHA256':plan['selected_expected_SHA256'][plan['grouped_raw_ROOT']],'grouped_raw_manifest_expected_SHA256':plan['selected_expected_SHA256'][plan['grouped_raw_manifest']],'full_parent_stock13_owned_expected_SHA256':parent_owned,'full_grouped_raw13_owned_expected_SHA256':grouped_owned,'fixed_M_new':576,'fixed_M_parent':1024,'fixed_moment_order_reused':32,'analytic_ln576_lower_certificate':plan['analytic_log_lower_certificate'],'M_guard_before_usage':'54*6873094849599<=341*1099511627776; then b<=341/54<=ln576','projection_transport':'P(X_N)=X_N; |X_N-P(X)|<=|X_N-X|; exp Lipschitz<=576 on unchanged [a,b]','lower_tail_reuse':'own certified Tlo_old*(576/1024)^2','upper_tail_reuse':'own certified Tup_old exactly, unconditional exponential-tilt tail retained','pointwise_stock_transport':'3*(A_new^2+576^2*Bchosen+Tlo_new+Tup_old)','both_unconditional_continuous_tails_paid':True,'native_error_or_stock_independence_assumed':False,'old_source_DAG_native_kernel_moment_reciprocal_power_or_tail_provider_reexecuted':False,'fixed_grouped_prerequisite_selected_without_fallback_or_minimum':True,'comparison_separate_from_validity_or_adoption':True,'candidate_whole_price_G2_circuit_or_quantum_advantage':False},own



def compose(profile, plan, own):
    require(profile in ('primary90','independent130') and plan['interface']['fixed_parameters']['M']==576 and plan['interface']['fixed_parameters']['parent_M']==1024 and plan['interface']['fixed_parameters']['moment_order']==32, 'Only fixed original own M576 stock4054 route')
    old=own[profile]['old_stock_record'];grouped=own[profile]['grouped_raw_record'];parent=old['components'];Q=plan['ideal_law_constants']['Q']
    upper=plan['source_scope_proof']['native_raw_interval'][1]
    require(type(upper) is type(Q) is int and upper==6873094849599 and Q==1099511627776 and max(abs(upper).bit_length()+6,Q.bit_length()+9)<=524288, 'Exact bounded native endpoint operands before integer guard')
    M_guard=54*upper<=341*Q
    require(M_guard, 'Fixed M576 native endpoint guard; fail without tuning, fallback or candidate selection')
    M=Fraction(576);Mparent=limb_ratio(parent['M2']);require(Mparent==1024, 'Certified parent M1024 tail scaling denominator')
    alpha=limb_ratio(parent['site4054_original_generic_alpha']);beta=limb_ratio(parent['site4054_original_generic_beta']);old_bound=limb_ratio(parent['stock4054_squared_L2_upper'])
    lower_old=limb_ratio(parent['new_lower_tail']);upper_old=limb_ratio(parent['new_upper_tail']);Bchosen=limb_ratio(grouped['grouped_raw_log_squared_L2_upper'])
    Anew=plus(times(alpha,M),beta);A_squared=times(Anew,Anew);M_squared=times(M,M);transport=times(M_squared,Bchosen)
    scale=Fraction(576,1024);scale_squared=times(scale,scale);lower_new=times(lower_old,scale_squared);upper_new=upper_old
    stages=[A_squared,transport,lower_new,upper_new];subtotal=Fraction(0);expanded=Fraction(0)
    for value in (stages if profile=='primary90' else list(reversed(stages))):
        subtotal=plus(subtotal,value);expanded=plus(expanded,times(Fraction(3),value))
    bound=times(Fraction(3),subtotal);require(bound==expanded, 'One fixed factor3 stock bound, own grouped/expanded identity; no old formula reconstruction')
    difference=plus(bound,-old_bound)
    components={'M_new':M,'M_parent':Mparent,'alpha':alpha,'beta':beta,'A_new':Anew,'A_new_squared':A_squared,'verified_grouped_raw_squared_L2':Bchosen,'M_new_squared':M_squared,'transported_raw_squared_L2':transport,'saved_lower_tail_parent':lower_old,'lower_tail_scale_squared':scale_squared,'lower_tail_new':lower_new,'saved_upper_tail_parent':upper_old,'upper_tail_new':upper_new,'old_stock_bound':old_bound,'new_stock_bound':bound}
    return {'schema':'e11-date2-stock4054-fixed-M576-groupedraw-limb-bound-v1','profile':profile,'units':'dollars_squared','source_raw_log':3543,'source_stock':4054,'asset_zero_based':0,'contractual_date_one_based':2,'fixed_M_new':576,'fixed_M_parent':1024,'fixed_moment_order_reused':32,'fixed_grouped_delta_exact_pair':[1,100000],'original_ideal_law_constants':plan['ideal_law_constants'],'components':{k:pair(v) for k,v in components.items()},'certified_original_law_and_tail_components':parent,'reused_parent_guard_results':old['new_guard_results'],'C_prime':grouped['C_prime'],'allowed_literal_operands':grouped['allowed_literal_operands'],'kappa2':grouped['kappa2'],'new_guard_results':{'native_b_le_341_over54':M_guard,'M_guard_before_M576_usage':True,'failed_guard_retuning_or_fallback':False},'chosen_formula':'3*(A_new^2+576^2*Bchosen+Tlo_old*(576/1024)^2+Tup_old)','grouped_equals_expanded':True,'signed_new_minus_own_old_stock':signed_pair(difference),'comparison':{'nonincreasing':difference<=0,'strictly_smaller':difference<0,'equal':difference==0,'valid_bound_regardless_of_comparison_sign':True,'adoption':False},'both_unconditional_continuous_tails_paid':True,'upper_tail_reused_identically':True,'old_moments_reciprocals_powers_or_tail_providers_recomputed':False,'original_degree12_site4054_generic_envelope_retained':True,'native_error_or_stock_independence_assumed':False,'adaptive_M_formula_profile_minimum_or_fallback':False,'extra_spot_multiplier':1,'candidate_date1_endpoint_or_whole_price_G2_quantum_advantage':False}



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
    require(primary['profile']=='primary90' and independent['profile']=='independent130' and primary['fixed_M_new']==independent['fixed_M_new']==576 and primary['fixed_grouped_delta_exact_pair']==independent['fixed_grouped_delta_exact_pair']==[1,100000] and primary['grouped_equals_expanded'] is independent['grouped_equals_expanded'] is True, 'Separate own profiles and one prescribed M/grouped route')
    for record in (primary,independent):
        flags=record['comparison']
        require(set(flags)=={'nonincreasing','strictly_smaller','equal','valid_bound_regardless_of_comparison_sign','adoption'} and all(type(v) is bool for v in flags.values()) and flags['valid_bound_regardless_of_comparison_sign'] is True and flags['adoption'] is False, 'Validity, comparison sign and adoption remain separate')
    return {'schema':'e11-date2-stock4054-M576-own-comparison-v1','passed':True,'profiles_kept_separate':True,'fixed_M_new':576,'fixed_grouped_delta_exact_pair':[1,100000],'comparison_combines_M_and_raw_bound_changes_not_individual_savings':True,'no_minimum_fallback_or_cross_profile_selection':True,'validity_separate_from_improvement':True,'numeric_adoption':False,'profile_comparisons':[{'profile':r['profile'],'old_stock_bound':r['components']['old_stock_bound'],'new_stock_bound':r['components']['new_stock_bound'],'signed_new_minus_own_old_stock':r['signed_new_minus_own_old_stock'],'comparison':r['comparison']} for r in (primary,independent)],'old_native_kernel_moment_reciprocal_power_or_tail_provider_called':False,'candidate_or_whole_financial_price_result':None}

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
        keys={'schema','ready','root_and_independent_static_reviews_passed','date2_stock4054_M576_execution_authorized','date2_stock4054_M576_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-date2-stock4054-M576-grouped-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['date2_stock4054_M576_execution_authorized'] is True,'Own current fixedM576 date2 stock4054 release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['date2_stock4054_M576_transfer_witness_accepted'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        files['source_projection_and_saved_tail_witness.json']=save('source_projection_and_saved_tail_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_stock4054_M576_squared_L2.json']=save('primary_stock4054_M576_squared_L2.json',primary)
        files['independent_stock4054_M576_squared_L2.json']=save('independent_stock4054_M576_squared_L2.json',independent)
        comparison=same_profile_comparison(primary,independent);files['same_profile_comparison.json']=save('same_profile_comparison.json',comparison)
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'original_native_range_guard_tail_moment_series_or_provider_called':False,'new_M_guard_and_saved_tail_transport_assembled':True,'old_moments_reciprocals_powers_or_tail_providers_recomputed':False,'fixed_M_new':576,'fixed_M_parent':1024,'fixed_grouped_delta_exact_pair':[1,100000],'same_profile_comparison':comparison,'validity_separate_from_improvement_and_no_adoption':True,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','date2_asset0_original_native_stock4054_only':True,'candidate_or_whole_financial_price_results':None}
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
