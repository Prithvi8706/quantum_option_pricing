# Dormant separate fixed-dyadic256 native48 time average; independent/ROOT SOURCE reviews and current READY required.
# Verified all48 matrix ROOT SHA256: 86546c0ce6f5376d3187d6b7c8d7290d3b4f453d1de3241ed0cf7f4314f09b9e
# ROOT instruction approved prospectus ca468187/f50b094; no extra authorgrant is required.
# Fixed outward grid256 before addition; same delta1/100000 and error65537/Q, no adaptive selection.
# All future peer/review/READY/terminal/manifest/numerical result pins remain None.
'Dormant separate fixed-dyadic256 native48 stock time average; fixed outward transport and ROOT release required.'

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

SOURCE=ROOT/'research/limitation_program_20261001/experiment_e11_b4x12_native48_fixed_dyadic256_stock_time_average_v1.py'

PLAN=ROOT/'.context/E11_B4X12_NATIVE48_FIXED_DYADIC256_STOCK_TIME_AVERAGE_INPUT_ADAPTER_run001.json'

MD=ROOT/'.context/E11_B4X12_NATIVE48_FIXED_DYADIC256_STOCK_TIME_AVERAGE_PREFLIGHT_run001.md'

READY=ROOT/'.context/E11_B4X12_NATIVE48_FIXED_DYADIC256_STOCK_TIME_AVERAGE_ROOT_READY_run001.json'

OUTPUT=ROOT/'results/limitation_program_20261001/E11_B4x12_native48_fixed_dyadic256_stock_time_average_run001'

LEDGER=['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'original48_sum_multiplier_and_fixed_dyadic256_witness.json', 'five_metadata_controls.json', 'primary48_fixed_dyadic256_time_average_squared_L2.json', 'independent48_fixed_dyadic256_time_average_squared_L2.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']

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
    require(ready['native48_fixed_dyadic256_time_average_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']), 'Current original48 stock time-average witness before numerical assembly')
    fixed={'F': 40, 'W': 72, 'adaptive_minimum_fallback_or_adoption': False, 'assets_zero_based': [0, 1, 2, 3], 'case': 'B4x12', 'contractual_dates_one_based': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'delta_fixed': [1, 100000], 'deterministic_native_error_numerator': 65537, 'multiplier_literal_raw': 22906492245, 'own_profile_rows': 2, 'own_stock_certificate_joins': 96, 'profiles': ['primary90', 'independent130'], 'reference': 'continuous arithmetic average of all48 original stocks on the verified product60-uniform coupling', 'saved_dates_zero_based': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 'source_average': 5692, 'source_stock_count': 48, 'source_sum': 5691, 'stock_error_independence_assumed': False, 'units': 'dollars_squared', 'grid_exponent_fixed': 256, 'outward_rounding_before_addition': True}
    require(exact(plan['interface'],fixed), 'Original sum5691/cmul5692 with fixed multiplier-error and Young contract')
    ancestry={'.context/E11_NATIVE48_TIME_AVERAGE_FIXED_DYADIC_CONTINGENCY_PROSPECTIVE_PLAN_run001.json':'2999ca95c3b083f96d36eb8d098448bb6fa41b031cce3d14504c711c31845f8e','.context/E11_NATIVE48_TIME_AVERAGE_FIXED_DYADIC_CONTINGENCY_PROSPECTIVE_PLAN_run001.md':'06a042fb6407786e5aba42d5c998f77b5fde4338404dbb1338cb057b8cfbe38e','.context/E11_B4X12_NATIVE48_STOCK_TIME_AVERAGE_EXACT_SUM_ROOT_FAILURE_CUSTODY_run001.json':'e228457d8e77a0417083cb462b17a988294264b9286d39372866a54fbd50a1d4'}
    require(exact(plan['dyadic_byte_only_ancestry_expected_SHA256'],ancestry) and all(plan['selected_expected_SHA256'][key]==pin and plan['selected_input_modes'][key]=='plain_text_only' and type(inputs[key]) is bytes for key,pin in ancestry.items()), 'Externally pinned byte-only failure/prospectus ancestry, no partial output or old exact sum promoted')
    require(plan['fixed_dyadic_ceil_rule']=='ceil(2^256*B_i)/2^256 before all48 additions' and plan['fixed_positive_rounding_loss_upper_symbolic']=='(1+1/100000)*2^-256' and plan['numerator_or_CPU_feasibility_certified_by_denominator_proof'] is False, 'One upfront outward grid and honest retained-cap qualification')
    original=inputs[plan['symbolic_PLAN_path']]
    require(original['schema']=='e11-B4x12-native48-fixed-dyadic256-stock-time-average-plan-v1' and original['scientific_evaluation_performed'] is original['SOURCE_authoring_READY_or_SCI_authorized_by_PLAN'] is False and all(exact(plan[k],original[k]) for k in ('interface','profiles','fixed_expression','fixed_sum_source_rows','fixed_sum_leaf_order','fixed_final_multiplier_row','fixed_all48_source_mappings','verified_matrix_ROOT_metadata_facts','selected_expected_SHA256','selected_input_modes','dyadic_byte_only_ancestry_expected_SHA256','fixed_dyadic_ceil_rule','fixed_positive_rounding_loss_upper_symbolic')), 'Prerecorded exact original metadata roles and fixed expression; PLAN is not SCI permission')
    prospectus=inputs[plan['prospective_PLAN_path']]
    require(prospectus['schema']=='e11-B4x12-original48-stock-time-average-prospective-plan-v1' and prospectus['metadata_only'] is True and prospectus['scientific_evaluation_performed'] is prospectus['SOURCE_READY_SCI_or_result_authorized_by_this_plan'] is False and prospectus['new_numerical_results'] is None and exact(prospectus['fixed_contract']['fixed_delta'],fixed['delta_fixed']) and prospectus['fixed_contract']['Q']==1099511627776 and prospectus['fixed_contract']['original_multiplier']==fixed['multiplier_literal_raw'] and prospectus['fixed_contract']['deterministic_error_upper_dollars_symbolic']=='65537/Q', 'Fixed upfront ROOT-read prospectus, not an adaptive numeric choice')
    require(exact(plan['fixed_sum_source_rows'],prospectus['original47_addition_rows']) and exact(plan['fixed_sum_leaf_order'],prospectus['original_sum_tree_leaf_order']) and exact(plan['fixed_final_multiplier_row'],prospectus['original_final_multiplier_row']), 'Complete source sum and multiplier are frozen before numerical assembly')
    root_raw=inputs[plan['verified_matrix_ROOT']]
    require(type(root_raw) is bytes and plan['selected_input_modes'][plan['verified_matrix_ROOT']]=='plain_text_only', 'Verified ROOT physical bytes only; own physical profile records parsed once')
    facts=plan['verified_matrix_ROOT_metadata_facts']
    fact_fixed={'passed':True,'completed':True,'blockers':[],'ROOT_observed_terminal_exit_code':0,'manifest_SHA256':plan['selected_expected_SHA256'][plan['verified_matrix_manifest']],'SOURCE_SHA256':plan['verified_matrix_SOURCE_SHA256'],'all48_stock_matrix_clamp_transfer_witness_accepted':True,'all48_original_native_stock_sites_only':True,'completed_own_numeric_rows':24,'completed_own_profile_site_instantiations':96,'original_distinct_stock_sites':48,'accepted_interface':plan['verified_matrix_accepted_interface']}
    require(exact(facts,fact_fixed) and plan['verified_ROOT_factual_projection_exact_against_expected_original_bytes'] is True, 'Compact factual projection exactly checked against original ROOT bytes by all current3 reviews')
    require(exact(prospectus['required_verified_matrix']['compact_ROOT_factual_projection'],facts) and prospectus['required_verified_matrix']['ROOT_expected_SHA256']==plan['selected_expected_SHA256'][plan['verified_matrix_ROOT']], 'Verified matrix certificate expected authority, not observation promotion')
    mf=inputs[plan['verified_matrix_manifest']]
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['inclusive_files']==13 and set(mf['files'])==set(plan['verified_matrix_exact13_ledger'])-{'manifest.json'}, 'Exact completed original matrix owner scope')
    witness=inputs[plan['verified_matrix_witness']]
    require(mf['files'][Path(plan['verified_matrix_witness']).name]==plan['selected_expected_SHA256'][plan['verified_matrix_witness']] and witness['schema']=='e11-B4x12-all48-clamp-Gaussian-source-witness-v1' and witness['passed'] is witness['all48_initial_once_drift_t_drivers_and_floors_2t'] is witness['all48_source_interfaces_only_before_numeric_rows'] is True and exact(witness['accepted_interface'],facts['accepted_interface']), 'Completed all48 source and same-coupling witness')
    require(exact(witness['selected_source_mappings'],plan['fixed_all48_source_mappings']) and exact(witness['continuous_product_law_witness'],plan['fixed_continuous_product_law_witness']) and witness['continuous_product_law_witness']['ideal_only'] is True and witness['continuous_product_law_witness']['digital_or_error_independence'] is witness['native_errors_stock_or_digital_pair_independence_assumed'] is witness['whole_financial_completion'] is False, 'Common coupling only, no stock/native-error independence or whole financial credit')
    target=inputs[plan['target']];sampler=inputs[plan['native_sampler_binding']]
    require(type(target['width']) is type(target['fraction_bits']) is int and target['width']==72 and target['fraction_bits']==40 and sampler['original_target_expected_SHA256']==plan['selected_expected_SHA256'][plan['target']], 'Original full72/F40 source and external sampler pin')
    nodes={v:n for n in target['nodes'] for v in n['out']}
    sites=plan['fixed_all48_source_mappings']
    require(len(sites)==48 and {(s['date_zero_based'],s['asset_zero_based']) for s in sites}=={(d,a) for d in range(12) for a in range(4)} and len({s['stock'] for s in sites})==48, 'Complete original12x4 stock source coverage')
    prefixes=sampler['complete_original_saved_source_case']['financial_roles']['prefix_witnesses']
    require({(p['date'],p['asset'],p['stock'],p['raw_log']) for p in prefixes}=={(s['date_zero_based'],s['asset_zero_based'],s['stock'],s['raw_log']) for s in sites}, 'All48 exact sampler stock/raw/date/asset identities')
    sum_rows=plan['fixed_sum_source_rows'];leaves=plan['fixed_sum_leaf_order']
    require(len(sum_rows)==47 and [row['out'][0] for row in sum_rows]==list(range(5645,5692)) and len(leaves)==len(set(leaves))==48 and set(leaves)=={s['stock'] for s in sites} and all(v<5576 for v in leaves), '47 stock-only additions, each original stock once; no basket inputs')
    require(all(exact(nodes[row['out'][0]],row) and row['op']=='add' and row['params']=={} and len(row['args'])==2 and len(row['out'])==1 for row in sum_rows), 'Original47 exact unscaled full-sum rows')
    known={s['stock']:[s['stock']] for s in sites}
    for row in sum_rows:
        require(all(v in known for v in row['args']), 'Each addition is dominated by already declared stock or earlier sum')
        joined=known[row['args'][0]]+known[row['args'][1]]
        require(len(joined)==len(set(joined)), 'No duplicate stock in any original positive partial sum')
        known[row['out'][0]]=joined
    require(exact(known[5691],leaves), 'Complete native sum tree leaf order matches original metadata')
    require(exact(plan['fixed_final_multiplier_row'],{'op':'cmul','args':[5691],'out':[5692],'params':{'c':22906492245}}) and exact(nodes[5692],plan['fixed_final_multiplier_row']), 'Exact original native average literal and whole-product source row')
    Q=1099511627776;c=22906492245
    require(Q==48*c+16 and c<1<<35, 'Exact fixed-point multiplier identity Qmod48=16 before its use')
    envelope=inputs[plan['primary_native_stock_envelope']]['cases']['B4x12'];native=inputs[plan['runtime_manifest']]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs'])==2842 and native['frozen_inputs'][plan['primary_native_stock_envelope']]==plan['selected_expected_SHA256'][plan['primary_native_stock_envelope']], 'Original native full48 envelope provenance and runtime citation only')
    require(envelope['all_positive_stock_stored72_product144_shift_guards_passed'] is envelope['whole_clipped_integer_domain_covered'] is True and type(envelope['actual_native_upper_clamp_stock_raw']) is int and envelope['actual_native_upper_clamp_stock_raw']==4503599627354112 and 0<envelope['actual_native_upper_clamp_stock_raw']<1<<52 and len(envelope['actual_sites'])==48, 'Verified bounded NATIVE support, not a pointwise continuous stock premise')
    require(all(s['original_support_signature']==plan['case_global_support_signature'] and next(v for v in envelope['actual_sites'] if v['stock']==s['stock'])['actual_original_support_signature']==plan['case_global_support_signature'] for s in sites), 'Each of48 original native kernel/support source sites joined')
    own={}
    for profile,roles in plan['profiles'].items():
        record=inputs[roles['verified_matrix_record']]
        require(mf['files'][Path(roles['verified_matrix_record']).name]==plan['selected_expected_SHA256'][roles['verified_matrix_record']] and record['schema']=='e11-B4x12-all48-original-stock-clamp-squared-L2-limb-matrix-v1' and record['profile']==profile and record['units']=='dollars_squared' and record['own_numeric_row_count']==12 and record['own_profile_site_instantiations']==record['source_site_count']==48 and record['all48_within_own_profile_completed'] is True and len(record['date_rows'])==12 and record['native_values_errors_or_stock_independence_assumed'] is record['candidate_or_whole_financial_price_or_G2_or_quantum_advantage'] is False, 'One physically saved own profile, exact verified owner membership')
        certificates=[]
        for date,row in enumerate(record['date_rows']):
            date_sites=[s for s in sites if s['date_zero_based']==date]
            require([s['asset_zero_based'] for s in date_sites]==[0,1,2,3] and row['contractual_date_one_based']==date+1 and row['profile']==profile and row['units']=='dollars_squared' and row['source_stocks']==[s['stock'] for s in date_sites] and row['assets_zero_based']==[0,1,2,3] and row['grouped_raw_equals_expanded'] is row['stock_grouped_equals_expanded'] is True and len(row['per_stock_instantiations'])==4, 'All12 own date rows and original4 source assets before scalar assembly')
            for asset,cert in enumerate(row['per_stock_instantiations']):
                site=date_sites[asset];pointer=roles['stock_certificate_pointers'][4*date+asset]
                require(cert['asset_zero_based']==asset and cert['source_stock']==site['stock'] and cert['source_raw_log']==site['raw_log'] and cert['source_clipped_log']==site['clipped_log'] and cert['same_profile_same_mean_variance_and_case_global_kernel'] is True and exact(cert['bound'],row['components']['four_stock_common_own_profile_squared_L2_upper']), 'Every actual saved own stock allowance and exact source binding, no old formula replay')
                require(exact(pointer,{'date_zero_based':date,'asset_zero_based':asset,'source_stock':site['stock'],'own_bound_json_pointer':'/date_rows/%d/per_stock_instantiations/%d/bound'%(date,asset)}), 'Fixed48 certificate pointers, not duplicated numeric profile subtrees')
                certificates.append({'contractual_date_one_based':date+1,'asset_zero_based':asset,'source_stock':site['stock'],'source_raw_log':site['raw_log'],'source_clipped_log':site['clipped_log'],'saved_bound_json_pointer':pointer['own_bound_json_pointer'],'stock_allowance':cert['bound']})
        require(len(certificates)==48 and len(roles['stock_certificate_pointers'])==48, 'Exactly all48 own-profile premises')
        own[profile]=certificates
    witness_out={'schema':'e11-B4x12-native48-fixed-dyadic256-stock-time-average-common-coupling-source-witness-v1','passed':True,'accepted_interface':fixed,'source_sum':5691,'source_average':5692,'source_sum_rows':sum_rows,'source_stock_ids_in_tree_order':leaves,'source_final_multiplier_row':plan['fixed_final_multiplier_row'],'each_original_stock_exactly_once':True,'twelve_baskets_are_not_sum_inputs':True,'continuous_product_law_witness':plan['fixed_continuous_product_law_witness'],'verified_matrix_ROOT_expected_SHA256':plan['selected_expected_SHA256'][plan['verified_matrix_ROOT']],'verified_matrix_manifest_expected_SHA256':plan['selected_expected_SHA256'][plan['verified_matrix_manifest']],'compact_ROOT_factual_projection_exact_checked_by_current3':True,'physical_own_profile_records_read_once':True,'original_full48_native_positive_stock_bound':4503599627354112,'full48_sum_raw_strict_upper_power_of_two':58,'whole_multiplier_product_strict_upper_power_of_two':93,'signed_word_bits':72,'whole_product_bits':144,'Qmod48':16,'multiplier_difference_from_one_over48':'1/(3Q)','coefficient_discrepancy_charged_to_bounded_native_sum_not_continuous_stocks':True,'native_sum_dollars_strict_upper':196608,'multiplier_absolute_error_strict_upper_numerator_over_Q':65536,'final_floor_absolute_error_strict_upper_numerator_over_Q':1,'combined_deterministic_absolute_error_closed_numerator_over_Q':65537,'dependence_safe_average_Cauchy_sum_B_over48':True,'fixed_Young_delta':[1,100000],'grid_exponent_fixed':256,'outward_rounding_before_all48_additions':True,'rounding_precision_loss_strict_upper_symbolic':'(1+1/100000)*2^-256','final_denominator_divides_symbolic':'48*100000*2^256','denominator_upper_bits':279,'numerator_or_CPU_feasibility_certified_by_denominator_proof':False,'original_exact_sum_failure_or_partial_records_used_as_numeric_premises':False,'no_independence_adaptive_minimum_or_adoption':True,'basket_numeric_certificate_required':False,'old_stock_raw_tail_kernel_native_or_provider_recipe_replayed':False,'barrier_strike_positive_discount_payoff_price_G2_or_advantage_claimed':False}
    return witness_out,own



def outward_fixed_dyadic(value, grid_exponent):
    budget()
    require(type(value) is Fraction and value>=0 and max(value.numerator.bit_length(),value.denominator.bit_length())<=131072, 'Canonical nonnegative own saved allowance within original reduced frontier')
    require(type(grid_exponent) is int and grid_exponent==256, 'Only the preregistered fixed dyadic grid256; no fallback or adaptation')
    require(value.numerator.bit_length()+grid_exponent<=524288, 'Ceil shift temporary frontier before shifting')
    shifted=value.numerator<<grid_exponent
    quotient,remainder=divmod(shifted,value.denominator)
    ceiling=quotient+(1 if remainder else 0)
    require(ceiling.bit_length()+value.denominator.bit_length()<=524288, 'Ceil order witness multiplication frontier before multiplication')
    gap_numerator=ceiling*value.denominator-shifted
    require(0<=gap_numerator<value.denominator and (gap_numerator==0)==(remainder==0), 'Exact outward order and strict grid gap, with zero precisely at integral grid operands')
    rounded=Fraction(ceiling,1<<grid_exponent)
    require(rounded>=0 and max(rounded.numerator.bit_length(),rounded.denominator.bit_length())<=131072, 'Rounded reduced frontier unchanged; denominator control is no numerator-cap waiver')
    return rounded,{'schema':'e11-fixed-dyadic256-outward-rounding-operand-witness-v1','grid_exponent':256,'division_had_nonzero_remainder':remainder!=0,'outward_order_and_strict_grid_gap_passed':True,'old_exact_aggregate_required':False}


def compose(profile, plan, own):
    require(profile in ('primary90','independent130') and plan['interface']['delta_fixed']==[1,100000] and plan['interface']['source_sum']==5691 and plan['interface']['source_average']==5692 and plan['interface']['deterministic_native_error_numerator']==65537 and plan['interface']['grid_exponent_fixed']==256 and plan['interface']['outward_rounding_before_addition'] is True, 'Own profile and one upfront fixed-dyadic original time-average route')
    certificates=own[profile]
    require(len(certificates)==48 and [(c['contractual_date_one_based'],c['asset_zero_based']) for c in certificates]==[(d,a) for d in range(1,13) for a in range(4)], 'Complete ordered own48 verified stock premises')
    original_allowances=[limb_ratio(c['stock_allowance']) for c in certificates]
    allowances=[];rounding_witnesses=[]
    for index,value in enumerate(original_allowances):
        rounded,witness=outward_fixed_dyadic(value,plan['interface']['grid_exponent_fixed'])
        allowances.append(rounded);rounding_witnesses.append(dict(witness,own_operand_index=index,source_stock=certificates[index]['source_stock']))
    delta=Fraction(1,100000);Q=1099511627776
    factor_average=plus(Fraction(1),delta)
    factor_error=plus(Fraction(1),positive_reciprocal(delta))
    sum_B=Fraction(0)
    ordered=allowances if profile=='primary90' else list(reversed(allowances))
    for value in ordered:sum_B=plus(sum_B,value)
    A=times(Fraction(1,48),sum_B)
    E=Fraction(65537,Q)
    E_squared=times(E,E)
    weighted_average=times(factor_average,A)
    weighted_error=times(factor_error,E_squared)
    B=plus(weighted_average,weighted_error) if profile=='primary90' else plus(weighted_error,weighted_average)
    expanded=weighted_error
    for value in ordered:expanded=plus(expanded,times(times(factor_average,Fraction(1,48)),value))
    require(B==expanded, 'Own rounded full sum then weight equals independent distributed fixed Young expression')
    components={'fixed_delta':pair(delta),'factor_average':pair(factor_average),'factor_deterministic_error':pair(factor_error),'original_forty_eight_stock_allowances':[pair(v) for v in original_allowances],'outward_fixed_dyadic256_stock_allowances':[pair(v) for v in allowances],'sum_rounded_stock_allowances':pair(sum_B),'rounded_average_before_native_multiplier_squared_L2_upper':pair(A),'deterministic_native_multiplier_and_floor_absolute_error_upper':pair(E),'deterministic_error_squared':pair(E_squared),'weighted_rounded_average_term':pair(weighted_average),'weighted_deterministic_error_term':pair(weighted_error),'fixed_dyadic256_time_average_squared_L2_upper':pair(B),'independent_distributed_expression':pair(expanded)}
    return {'schema':'e11-B4x12-native48-fixed-dyadic256-stock-time-average-squared-L2-limb-row-v1','profile':profile,'units':'dollars_squared','source_sum':5691,'source_average':5692,'source_stock_certificate_bindings':[{k:c[k] for k in ('contractual_date_one_based','asset_zero_based','source_stock','source_raw_log','source_clipped_log','saved_bound_json_pointer')} for c in certificates],'components':components,'fixed_outward_rounding_operand_witnesses':rounding_witnesses,'own_stock_certificate_count':48,'own_numeric_row_count':1,'fixed_delta':[1,100000],'grid_exponent_fixed':256,'chosen_formula':'(1+delta)*(sum48 ceil(2^256*Bi)/2^256/48)+(1+1/delta)*(65537/Q)^2','grouped_equals_distributed':True,'same_original_continuous48_stock_average_reference':True,'native_coefficient_truncation_and_final_floor_both_paid':True,'deterministic_error_charged_to_bounded_native_sum':True,'outward_rounding_before_all48_additions':True,'rounding_precision_loss_strict_upper_symbolic':'(1+1/100000)*2^-256','rounding_penalty_already_paid_in_outward_operands':True,'numerator_or_CPU_feasibility_certified_by_denominator_proof':False,'old_exact_aggregate_reconstructed_or_required':False,'stock_error_independence_assumed':False,'basket_numeric_bounds_required_or_reused':False,'old_stock_raw_tail_kernel_native_or_provider_recipe_replayed':False,'adaptive_minimum_fallback_or_improvement_adoption':False,'barrier_strike_positive_discount_payoff_price_G2_or_advantage_claimed':False}




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
        keys={'schema','ready','root_and_independent_static_reviews_passed','native48_fixed_dyadic256_time_average_execution_authorized','native48_fixed_dyadic256_time_average_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-native48-fixed-dyadic256-stock-time-average-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['native48_fixed_dyadic256_time_average_execution_authorized'] is True,'Own current original48 stock time-average release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['native48_fixed_dyadic256_time_average_transfer_witness_accepted'] is True and review['factual_projection_exact_against_verified_ROOT'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        files['original48_sum_multiplier_and_fixed_dyadic256_witness.json']=save('original48_sum_multiplier_and_fixed_dyadic256_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary48_fixed_dyadic256_time_average_squared_L2.json']=save('primary48_fixed_dyadic256_time_average_squared_L2.json',primary)
        files['independent48_fixed_dyadic256_time_average_squared_L2.json']=save('independent48_fixed_dyadic256_time_average_squared_L2.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'no_minimum_or_cross_profile_selection':True,'one_fixed_delta_and_fixed_dyadic256_time_average_expression':True,'outward_grid256_applied_to_each_own_operand_before_any_sum':True,'original_exact_aggregate_reconstructed_or_required':False,'all2_own_time_average_rows':True,'both_own_grouped_distributed_identities':True,'only_own_verified_all48_stock_allowances_consumed':True,'all_original_full_sum_widths_multiplier_truncation_and_final_floor_paid':True,'no_stock_error_independence':True,'basket_numeric_bounds_required_or_reused':False,'old_stock_raw_tail_kernel_native_or_provider_recipe_replayed':False,'output_rationals_all_canonical_limbs':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'completed_own_numeric_rows':2,'original_distinct_time_average_sites':1,'original_stock_sum_leaf_count':48,'own_stock_certificate_joins':96,'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'old_stock_raw_tail_kernel_native_or_provider_recipe_replayed':False,'all_original_full_sum_widths_multiplier_truncation_and_final_floor_paid':True,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','original48_stock_time_average_site_only':True,'fixed_dyadic256_outward_rounding_before_addition':True,'original_exact_sum_failure_or_partial_records_used_as_numeric_premises':False,'original_exact_aggregate_reconstructed_or_required':False,'rounding_precision_loss_strict_upper_symbolic':'(1+1/100000)*2^-256','basket_numeric_bounds_required_or_reused':False,'adaptive_minimum_fallback_or_improvement_adoption':False,'barrier_strike_positive_discount_payoff_price_or_G2_results':None}
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
