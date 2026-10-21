"""Dormant original5696 discount transfer after positive-part; parent and ROOT release required."""
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
SOURCE = ROOT/'research/limitation_program_20261001/experiment_e11_b4x12_discount_after_positivepart_v1.py'
PLAN = ROOT/'.context/E11_B4X12_DISCOUNTED_POSITIVE_PART_INPUT_ADAPTER_run001.json'
MD = ROOT/'.context/E11_B4X12_DISCOUNTED_POSITIVE_PART_PREFLIGHT_run001.md'
READY = ROOT/'.context/E11_B4X12_DISCOUNTED_POSITIVE_PART_ROOT_READY_run001.json'
OUTPUT = ROOT/'results/limitation_program_20261001/E11_B4x12_discount_after_positivepart_run001'
LEDGER = ['executed_controller.py','executed_adapter.json','executed_preflight.md','executed_ROOT_READY.json','run_started.json','selected_premise_authority.json','discount_after_positivepart_common_coupling_witness.json','five_metadata_controls.json','primary_discount_after_positivepart_squared_L2.json','independent_discount_after_positivepart_squared_L2.json','same_profile_reconciliation.json','summary.json','manifest.json']
CPU, ADMISSION, WALL = (180,150,600)
_STARTED = None
_OWNS_OUTPUT = False
_OUTPUT_ID = None
CURRENT_POSITIVEPART_PARENT_SAVED_VERIFICATION_BOUND = True
POSITIVEPART_PARENT_ROOT_EXPECTED_SHA256 = '008d69089c0d07bf716840a4630f3baa8e56ddfc1a5825a9af5d9125334ec037'
POSITIVEPART_PARENT_MANIFEST_EXPECTED_SHA256 = '55f1fed0b8bf40e8d0a8dd4ba89257d6600c383926f86ac1870bd4d3250fab8b'


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
    require(CURRENT_POSITIVEPART_PARENT_SAVED_VERIFICATION_BOUND is True and type(POSITIVEPART_PARENT_ROOT_EXPECTED_SHA256) is str and type(POSITIVEPART_PARENT_MANIFEST_EXPECTED_SHA256) is str, 'Completed own positive-part certificate must be externally bound before transfer')
    fixed={'case':'B4x12','W':72,'F':40,'source_positive_part':5695,'source_discount':5696,'discount_literal':1067016148260,'native_positive_support_dollars_half_open':[0,3996],'delta':[1,100000],'profiles':['primary90','independent130'],'own_profile_rows':2,'units':'dollars_squared','reference':'exp(-3/100) times positive part of continuous arithmetic average of the original48 stocks minus100 dollars','single_new_cmul_floor_paid':True,'coefficient_error_paid_against_native_positive_part':True,'fixed_pathwise_Young_not_error_independence':True,'own_profile_discount_authorities_kept_separate':True,'continuous_positive_support_assumed':False,'barrier_or_fullprice_included':False}
    require(ready['discount_after_positivepart_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']) and exact(plan['interface'],fixed), 'Current exact original5696 discount and fixed own Young witness')
    require(set(plan['profiles'])=={'primary90','independent130'} and plan['selected_expected_SHA256'][plan['verified_positivepart_ROOT']]==POSITIVEPART_PARENT_ROOT_EXPECTED_SHA256 and plan['selected_expected_SHA256'][plan['verified_positivepart_manifest']]==POSITIVEPART_PARENT_MANIFEST_EXPECTED_SHA256, 'Original completed positive-part authority; no discovered promotion')
    root_bytes=inputs[plan['verified_positivepart_ROOT']]
    require(type(root_bytes) is bytes and plan['selected_input_modes'][plan['verified_positivepart_ROOT']]=='plain_text_only' and plan['positivepart_ROOT_factual_projection_exact_against_expected_bytes'] is True, 'Parent ROOT pinned opaque bytes; exact typed projection checked in all current3 reviews')
    facts=plan['verified_positivepart_ROOT_metadata_facts']
    require(type(facts) is dict and facts['passed'] is facts['completed'] is True and facts['blockers']==[] and type(facts['ROOT_observed_terminal_exit_code']) is int and facts['ROOT_observed_terminal_exit_code']==0 and facts['SOURCE_SHA256']==plan['verified_positivepart_SOURCE_SHA256'] and facts['manifest_SHA256']==POSITIVEPART_PARENT_MANIFEST_EXPECTED_SHA256, 'Completed parent ROOT factual projection, never inherited permission')
    require(facts['completed_own_numeric_rows']==2 and facts['original_distinct_strike_positivepart_sites']==1, 'One original strike100/positive-part site and two own saved allowances')
    mf=inputs[plan['verified_positivepart_manifest']]
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['inclusive_files']==13 and set(mf['files'])==set(plan['verified_positivepart_exact13_ledger'])-{'manifest.json'}, 'Exact completed13-file positive-part parent owner')
    parent_witness=inputs[plan['verified_positivepart_witness']]
    require(mf['files'][Path(plan['verified_positivepart_witness']).name]==plan['selected_expected_SHA256'][plan['verified_positivepart_witness']] and parent_witness['schema']=='e11-B4x12-strike100-positive-part-common-coupling-witness-v1' and parent_witness['passed'] is True and parent_witness['source_average']==5692, 'Saved original positive-part common-coupling witness')
    require(exact(parent_witness['native_positive_dollars_half_open'],[0,3996]) and parent_witness['signed72_subtraction_no_wrap'] is parent_witness['same_Q40_no_additional_floor_or_rounding'] is parent_witness['positivepart_global_one_Lipschitz'] is parent_witness['same_coupling_no_independence'] is parent_witness['both_own_parent_allowances_copied_unchanged'] is parent_witness['ideal_average_has_no_bounded_support_assumption'] is parent_witness['discount5696_barrier5697_price_G2_candidate_and_advantage_excluded'] is True, 'Verified native positive support/common coupling and parent boundary; no continuous support assumption')
    native=inputs[plan['runtime_manifest']]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs'])==2842 and native['frozen_inputs'][plan['original_ir_path']]==plan['selected_expected_SHA256'][plan['original_ir_path']], 'Original signed-word semantic source expected pin')
    require(type(inputs[plan['original_ir_path']]) is bytes and plan['selected_input_modes'][plan['original_ir_path']]=='plaintext_AST_only', 'Original evaluator is an unexecuted source citation')
    target=inputs[plan['target']]
    require(type(target['width']) is type(target['fraction_bits']) is int and target['width']==72 and target['fraction_bits']==40, 'Original full72/Q40 target')
    nodes={v:n for n in target['nodes'] for v in n['out']}
    required={5695:{'op':'positive','args':[5694],'params':{},'out':[5695]},5696:{'op':'cmul','args':[5695],'params':{'c':1067016148260},'out':[5696]}}
    require(all(exact(nodes[k],row) for k,row in required.items()) and exact(nodes[13],{'op':'const','args':[],'params':{'value':0},'out':[13]}) and exact(nodes[5697],{'op':'select','args':[5644,5696,13],'params':{},'out':[5697]}), 'Actual original discount endpoint and later zero/barrier boundary')
    require(0<1067016148260<1099511627776 and 3996<4096, 'Native raw positive<2^52 and coefficient<2^40 keep product<2^92 within signed144 and shifted output within signed72')
    old_integrity=inputs[plan['discount_old_ROOT_integrity']]
    require(native['frozen_inputs'][plan['discount_old_ROOT_integrity']]==plan['selected_expected_SHA256'][plan['discount_old_ROOT_integrity']] and old_integrity['passed'] is old_integrity['producer_and_independent_audit_terminal_PASS'] is True and old_integrity['SHA_mismatches']==0 and old_integrity['scientific_kernels_executed'] is False, 'Old selected archived discount authorities ROOT verified; not a new whole-origin walk')
    for role in ('discount_primary_manifest','discount_independent_manifest','discount_primary_authority','discount_independent_authority'):
        key=plan[role]
        require(native['frozen_inputs'][key]==plan['selected_expected_SHA256'][key], 'Original saved scalar discount authority pin; no exp producer replay')
    primary_mf=inputs[plan['discount_primary_manifest']]; independent_mf=inputs[plan['discount_independent_manifest']]
    for old_mf in (primary_mf,independent_mf):
        require(old_mf['passed'] is old_mf['completed'] is True and old_mf['budget_censored'] is old_mf['original_expected_hashes_waived'] is False and old_mf['archived_selected_receipt_validity_separate'] is True, 'Sealed unwaived selected discount premise; historical LIVE integrity remains separate')
    require(primary_mf['files'][Path(plan['discount_primary_authority']).name]==plan['selected_expected_SHA256'][plan['discount_primary_authority']] and independent_mf['files'][Path(plan['discount_independent_authority']).name]==plan['selected_expected_SHA256'][plan['discount_independent_authority']], 'Own old manifest membership for both small saved scalar facts')
    primary_authority=inputs[plan['discount_primary_authority']]
    require(primary_authority['schema']=='original-BM-smooth-payoff-envelopes-v1' and primary_authority['interval_digits']==90 and primary_authority['cases']['B4x12']['actual_discount_literal']==1067016148260, 'Exact original unconditional primary90 discount facts only; no barrier40 allowance transfer')
    own={}
    for profile,role in plan['profiles'].items():
        record=inputs[role['verified_positivepart_record']]
        require(mf['files'][Path(role['verified_positivepart_record']).name]==plan['selected_expected_SHA256'][role['verified_positivepart_record']] and record['schema']=='e11-B4x12-strike100-positive-part-squared-L2-limb-row-v1' and record['profile']==profile and record['units']=='dollars_squared' and record['source_average']==5692 and record['source_strike']==5693 and record['source_subtraction']==5694 and record['source_positive_part']==5695, 'Own physically saved positive-part record')
        require(record['own_numeric_row_count']==1 and record['same_profile_parent_bound_copied_exactly'] is record['same_coupling_pointwise_contraction_not_error_independence'] is True and record['new_rational_recipe_or_rounding_Young_tail_moment_kernel_provider'] is record['discount_barrier_price_G2_candidate_or_advantage'] is False, 'Saved own positive-part bound, with later discount excluded')
        require(exact(record['components']['positive_part_squared_L2_upper'],record['components']['parent_time_average_squared_L2_upper']), 'Parent contraction allowance copied; no numeric average recipe')
        if profile=='primary90':
            authority=primary_authority['cases']['B4x12']; authority_path=plan['discount_primary_authority']
            interval=authority['exact_discount_enclosure']; eta=authority['discount_literal_error_upper']
            interval_pointer='/cases/B4x12/exact_discount_enclosure'; eta_pointer='/cases/B4x12/discount_literal_error_upper'
        else:
            authority=inputs[plan['discount_independent_authority']]['B4x12']; authority_path=plan['discount_independent_authority']
            interval=authority['independent_true_discount_enclosure']; eta=authority['independent_discount_literal_error_upper']
            interval_pointer='/B4x12/independent_true_discount_enclosure'; eta_pointer='/B4x12/independent_discount_literal_error_upper'
        require(type(interval) is list and len(interval)==2 and role['discount_authority']==authority_path and role['discount_interval_JSON_pointer']==interval_pointer and role['discount_literal_error_JSON_pointer']==eta_pointer, 'Closed own discount authority mapping; no cross-profile choice')
        own[profile]={'saved_parent_record_path':role['verified_positivepart_record'],'saved_parent_bound_JSON_pointer':'/components/positive_part_squared_L2_upper','bound':record['components']['positive_part_squared_L2_upper'],'discount_authority_path':authority_path,'discount_interval_JSON_pointer':interval_pointer,'discount_literal_error_JSON_pointer':eta_pointer,'saved_discount_interval':interval,'saved_literal_abs_error_upper':eta}
    witness={'schema':'e11-B4x12-discount-after-positivepart-common-coupling-witness-v1','passed':True,'accepted_interface':fixed,'source_rows':required,'source_positive_part':5695,'source_discount':5696,'native_positive_dollars_half_open':[0,3996],'fixed_delta':[1,100000],'coefficient_literal':1067016148260,'signed72_output_and_signed144_product_no_wrap':True,'one_new_cmul_Q40_floor_paid':True,'true_discount_same_exp_minus3_over100':True,'coefficient_error_charged_only_to_bounded_native_positive_part':True,'continuous_positive_part_has_no_bounded_support_assumption':True,'same_coupling_pathwise_fixed_Young_no_independence':True,'both_own_discount_and_positivepart_authorities_kept_separate':True,'old_barrier40_or_smooth_payoff_allowance_not_reused':True,'full_endpoint_safety_trees_or_exp_producers_not_selected_or_replayed':True,'barrier5697_price_G2_candidate_and_advantage_excluded':True,'verified_parent_ROOT_expected_SHA256':POSITIVEPART_PARENT_ROOT_EXPECTED_SHA256,'verified_parent_manifest_expected_SHA256':POSITIVEPART_PARENT_MANIFEST_EXPECTED_SHA256}
    return witness,own


def compose(profile, plan, own):
    require(profile in ('primary90','independent130') and exact(plan['interface']['delta'],[1,100000]) and plan['interface']['source_discount']==5696 and plan['interface']['single_new_cmul_floor_paid'] is True, 'Fixed own original5696 discount transfer only')
    saved=own[profile]
    parent_bound=limb_ratio(saved['bound'])
    lower,upper=[ratio(value) for value in saved['saved_discount_interval']]
    eta=ratio(saved['saved_literal_abs_error_upper'])
    require(0<lower<=upper<=1 and eta>=0, 'Own saved true-discount enclosure and nonnegative literal error')
    q=Fraction(1067016148260,1099511627776)
    require(abs(q-lower)<=eta and abs(q-upper)<=eta, 'Own saved eta contains the actual coefficient endpoint errors; no exponential reevaluation')
    delta=Fraction(1,100000); epsilon=Fraction(1,1099511627776)
    factor_parent=plus(Fraction(1),delta); factor_remainder=plus(Fraction(1),positive_reciprocal(delta))
    upper_square=times(upper,upper)
    coefficient_remainder=times(Fraction(3996),eta)
    deterministic_remainder=plus(coefficient_remainder,epsilon)
    parent_weight=times(factor_parent,upper_square)
    parent_term=times(parent_weight,parent_bound)
    remainder_square=times(deterministic_remainder,deterministic_remainder)
    remainder_term=times(factor_remainder,remainder_square)
    grouped=plus(parent_term,remainder_term)
    distributed_remainder=plus(plus(times(coefficient_remainder,coefficient_remainder),twice(times(coefficient_remainder,epsilon))),times(epsilon,epsilon))
    distributed=plus(parent_term,times(factor_remainder,distributed_remainder))
    require(grouped==distributed, 'Own grouped fixed-Young allowance equals independently distributed square expression')
    components={'parent_positive_part_squared_L2_upper':saved['bound'],'true_discount_lower':pair(lower),'true_discount_upper':pair(upper),'stored_discount_literal_exact':pair(q),'stored_discount_literal_abs_error_upper':pair(eta),'new_cmul_floor_upper':pair(epsilon),'fixed_delta':pair(delta),'parent_Young_factor':pair(factor_parent),'remainder_Young_factor':pair(factor_remainder),'discount_upper_squared':pair(upper_square),'native_coefficient_remainder_upper':pair(coefficient_remainder),'deterministic_remainder_upper':pair(deterministic_remainder),'weighted_parent_error_squared_upper':pair(parent_term),'weighted_remainder_squared_upper':pair(remainder_term),'discount_squared_L2_upper':pair(grouped),'independent_distributed_expression':pair(distributed)}
    return {'schema':'e11-B4x12-discount-after-positivepart-squared-L2-limb-row-v1','profile':profile,'units':'dollars_squared','source_positive_part':5695,'source_discount':5696,'discount_literal':1067016148260,'native_positive_upper_exclusive_dollars':3996,'saved_parent_record_path':saved['saved_parent_record_path'],'saved_parent_bound_JSON_pointer':saved['saved_parent_bound_JSON_pointer'],'discount_authority_path':saved['discount_authority_path'],'discount_interval_JSON_pointer':saved['discount_interval_JSON_pointer'],'discount_literal_error_JSON_pointer':saved['discount_literal_error_JSON_pointer'],'components':components,'own_numeric_row_count':1,'fixed_delta_chosen_before_SCI':[1,100000],'grouped_equals_distributed':True,'own_parent_and_discount_authorities_kept_separate':True,'same_coupling_fixed_Young_not_error_independence':True,'single_new_cmul_floor_paid':True,'coefficient_error_charged_to_native3996_not_continuous_support':True,'old_stock_average_positivepart_exp_tail_moment_kernel_or_provider_recipe_replayed':False,'old_barrier40_or_smooth_payoff_allowance_reused':False,'barrier_price_G2_candidate_or_advantage':False}


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
    require(CURRENT_POSITIVEPART_PARENT_SAVED_VERIFICATION_BOUND is True, 'Dormant parent pins must be completed before own current ROOT release')
    try:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ready-sha256',required=True);args=parser.parse_args()
        base=Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True)==ROOT and Path(__file__).resolve(strict=True)==SOURCE,'Exact isolated default4300')
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256],'Separate original base argv0/venv and exact current absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(),'Pinned isolated paths/no ZIP/no site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'Unused own output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','discount_after_positivepart_execution_authorized','discount_after_positivepart_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-discount-after-positivepart-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['discount_after_positivepart_execution_authorized'] is True,'Own current original5696 discount release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['discount_after_positivepart_transfer_witness_accepted'] is True and review['factual_projection_exact_against_verified_positivepart_ROOT'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
        code_guard(source_raw,ready)
        caches=['research/limitation_program_20261001/__pycache__/'+SOURCE.stem+'.cpython-312'+s+'.pyc' for s in ('','.opt-1','.opt-2')]
        require(ready['existing_current_cache_SHA256']=={} and ready['absent_current_cache_paths']==sorted(caches) and all(not (ROOT/k).exists() and not (ROOT/k).is_symlink() for k in caches),'Exact unused current3 cache partition')
        inputs={}
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
        files['discount_after_positivepart_common_coupling_witness.json']=save('discount_after_positivepart_common_coupling_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_discount_after_positivepart_squared_L2.json']=save('primary_discount_after_positivepart_squared_L2.json',primary)
        files['independent_discount_after_positivepart_squared_L2.json']=save('independent_discount_after_positivepart_squared_L2.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'both_own_parent_allowances_consumed_same_profile':True,'no_minimum_or_cross_profile_selection':True,'fixed_pathwise_Young_bound':True,'single_new_cmul_floor_paid':True,'fixed_delta_before_SCI':[1,100000],'no_independence_assumption':True,'no_old_numeric_recipe_replayed':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'completed_own_numeric_rows':2,'original_distinct_discount_sites':1,'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','own_positivepart_and_discount_authorities_consumed_same_profile':True,'old_tail_moment_kernel_stock_average_positivepart_or_exp_recipe_replayed':False,'barrier_price_G2_candidate_results':None}
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
