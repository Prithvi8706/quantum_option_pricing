"""Dormant external-cap564 stock component transfer for original B4x12.

The fixed prospective certificate uses each own saved M4608 kernel allowance,
raw log squared-L2 allowance and lower-tail component in
3*(saved A_squared + 564_squared*saved Blog_raw + saved Tlower).
The cap564 proof removes the upper-clip discrepancy without changing the saved
kernel certificate. The virtual cap is a mathematical postprocessor; no new
native cap circuit, complete payoff/price, G2 or advantage result is claimed.
ROOT must separately authorize actual SOURCE publication and an exact-current
independent SOURCE peer/release before any SCI. This draft evaluates no guard.
"""
# Authoring gate is True; current independent SOURCE peer and ROOT closed READY remain required. Future own SCI/result pins are None.
# The future SCI will check the fixed clip/cap guard under unchanged budgets.
# Verified matrix receipt is a byte-only premise with the explicit typed factual projection.

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

SOURCE=ROOT/'research/limitation_program_20261001/experiment_e11_b4x12_external_cap564_stock_components_v1.py'

PLAN=ROOT/'.context/E11_B4X12_EXTERNAL_CAP564_STOCK_COMPONENT_REUSE_INPUT_ADAPTER_run001.json'

MD=ROOT/'.context/E11_B4X12_EXTERNAL_CAP564_STOCK_COMPONENT_REUSE_PREFLIGHT_run001.md'

READY=ROOT/'.context/E11_B4X12_EXTERNAL_CAP564_STOCK_COMPONENT_REUSE_ROOT_READY_run001.json'

OUTPUT=ROOT/'results/limitation_program_20261001/E11_B4x12_external_cap564_stock_components_run001'

LEDGER=['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'external_cap564_original_stock_component_witness.json', 'five_metadata_controls.json', 'primary_twelve_date_cap564_stock_component_matrix.json', 'independent_twelve_date_cap564_stock_component_matrix.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']

CPU, ADMISSION, WALL = (180, 150, 600)

_STARTED = None

_OWNS_OUTPUT = False

_OUTPUT_ID = None

CURRENT_EXTERNAL_CAP564_AUTHORING_AND_PROOF_BOUND = True
FUTURE_CURRENT_READY_TERMINAL_MANIFEST_ROOT_RESULT_PINS = None

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
    require(CURRENT_EXTERNAL_CAP564_AUTHORING_AND_PROOF_BOUND is True, 'Disabled draft until ROOT full scientific/header read and current SOURCE release')
    fixed={'case':'B4x12','W':72,'F':40,'contractual_dates_one_based':list(range(1,13)),'assets_zero_based':[0,1,2,3],'profiles':['primary90','independent130'],'own_profile_rows':24,'original_stock_sites':48,'profile_site_instantiations':96,'external_cap_dollars':[564,1],'barrier_dollars':[140,1],'band_half_width_dollars':[1,1],'parent_kernel_M_fixed':4608,'component_names':['kernel_allowance_squared','raw_log_t_squared_L2_upper','new_lower_tail'],'formula':'3*(savedA_squared+564^2*savedBlog_raw+savedTlower)','units':'dollars_squared','reference':'min(original native stock,564) versus min(original unclipped ideal continuous stock,564) under the same original product60-uniform coupling','virtual_postprocessors_not_emitted_native_circuit':True,'old_assembled_stock_bound_decomposed':False,'new_alpha_times564_claimed':False,'old_upper_tail_subtracted':False,'stock_native_or_error_independence_assumed':False,'adaptive_cap_grid_or_profile_selection':False,'full_price_or_G2_or_advantage_scope':False}
    require(ready['external_cap564_stock_component_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']) and exact(plan['interface'],fixed), 'Current fixed cap564/three-stage component interface')
    root_key=plan['verified_matrix_ROOT'];facts=plan['verified_matrix_ROOT_metadata_facts']
    require(type(inputs[root_key]) is bytes and plan['selected_input_modes'][root_key]=='plain_text_only' and plan['matrix_ROOT_factual_projection_exact_against_expected_bytes'] is True, 'Verified matrix ROOT opaque bytes; exact typed facts checked in all current3 reviews')
    require(facts['passed'] is facts['completed'] is True and facts['blockers']==[] and type(facts['ROOT_observed_terminal_exit_code']) is int and facts['ROOT_observed_terminal_exit_code']==0 and facts['SOURCE_SHA256']==plan['verified_matrix_SOURCE_SHA256'] and facts['manifest_SHA256']==plan['selected_expected_SHA256'][plan['verified_matrix_manifest']] and exact([facts['completed_own_numeric_rows'],facts['original_distinct_stock_sites'],facts['completed_own_profile_site_instantiations']],[24,48,96]) and facts['fixed_M']==4608 and facts['profiles_remain_separate'] is True, 'Exact completed parent24 rows/48 stocks/96 own source instantiations')
    mf=inputs[plan['verified_matrix_manifest']];witness=inputs[plan['verified_matrix_witness']];original=inputs[plan['verified_matrix_PLAN']]
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['inclusive_files']==13 and set(mf['files'])==set(plan['verified_matrix_exact13_ledger'])-{'manifest.json'} and mf['files'][Path(plan['verified_matrix_witness']).name]==plan['selected_expected_SHA256'][plan['verified_matrix_witness']], 'Exact verified parent13 and source-witness ownership')
    require(witness['schema']=='e11-B4x12-all48-clamp-Gaussian-source-witness-v1' and witness['passed'] is True and witness['fixed_M']==4608 and witness['native_errors_stock_or_digital_pair_independence_assumed'] is witness['old_provider_native_guard_series_or_recipe_replayed'] is False and exact(witness['selected_source_mappings'],original['fixed_all48_source_mappings']) and exact(witness['native_and_continuous_use_same_signed_clip_interval'],[-12193974156573,9145480617430]), 'Saved original full signed clamp/kernel/source law, no old recipe replay')
    law=witness['continuous_product_law_witness']
    require(exact(law,original['continuous_product_law_witness']) and law['ideal_only'] is True and law['digital_or_error_independence'] is False and law['polar_jacobian']=='exp(-(z0^2+z1^2)/2)/(2pi)=phi(z0)*phi(z1)', 'Full original product60/polar joint ideal law; no native/error independence')
    prospective=inputs[plan['historical_assessment']]
    require(prospective['schema']=='e11-B4x12-external-cap564-stock-component-reuse-prospective-assessment-v1' and prospective['scientific_evaluation_performed'] is prospective['SOURCE_READY_SCI_or_result_authorized'] is False and exact(prospective['fixed_contract']['external_cap_dollars'],[564,1]) and prospective['symbolic_kernel_raw_lower_tail_reuse']['fixed_expression']=='3*(saved_kernel_allowance_squared + 564^2*saved_raw_log_t_squared_L2_upper + saved_new_lower_tail)', 'Frozen prospective cap proof is ancestry, not permission')
    native=inputs[plan['runtime_manifest']];target=inputs[plan['target']]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs'])==2842 and exact([target['width'],target['fraction_bits']],[72,40]), 'Original full72/Q40 runtime and target')
    require(type(inputs[plan['original_ir_path']]) is bytes and plan['selected_input_modes'][plan['original_ir_path']]=='plaintext_AST_only' and native['frozen_inputs'][plan['original_ir_path']]==plan['selected_expected_SHA256'][plan['original_ir_path']], 'Original signed cmul-floor/strict-LT/SELECT semantic citation only')
    nodes={v:node for node in target['nodes'] for v in node['out']};sites=original['fixed_all48_source_mappings']
    require(len(sites)==48 and [(s['contractual_date_one_based'],s['asset_zero_based']) for s in sites]==[(d,a) for d in range(1,13) for a in range(4)], 'All original48 stock source mappings')
    for date in range(12):
        basket=5576+4*date
        require(exact(nodes[basket],{'op':'cmul','args':[basket-1],'params':{'c':274877906944},'out':[basket]}), 'Original quarter-floor basket, not general exact divisibility')
    require(exact(nodes[5643],{'op':'const','args':[],'params':{'value':153931627888640},'out':[5643]}) and exact(nodes[5644],{'op':'lt','args':[5642,5643],'params':{},'out':[5644]}) and exact(nodes[5697],{'op':'select','args':[5644,5696,13],'params':{},'out':[5697]}) and exact(nodes[13],{'op':'const','args':[],'params':{'value':0},'out':[13]}), 'Original strict140 and knocked-out zero payoff boundary')
    own={}
    require(set(plan['profiles'])=={'primary90','independent130'}, 'Two own physical component authorities only')
    for profile,roles in plan['profiles'].items():
        record=inputs[roles['verified_matrix_record']];old_roles=original['profiles'][profile];envelope=inputs[roles['original_kernel_envelope']]
        require(mf['files'][Path(roles['verified_matrix_record']).name]==plan['selected_expected_SHA256'][roles['verified_matrix_record']] and record['schema']=='e11-B4x12-all48-original-stock-clamp-squared-L2-limb-matrix-v1' and record['profile']==profile and record['units']=='dollars_squared' and record['fixed_M']==4608 and record['source_site_count']==48 and record['own_numeric_row_count']==12 and record['own_profile_site_instantiations']==48 and record['native_clip_inactive_assumed'] is record['native_values_errors_or_stock_independence_assumed'] is record['candidate_or_whole_financial_price_or_G2_or_quantum_advantage'] is False, 'Own physically sealed parent stages, not reconstructed old final B')
        require(native['frozen_inputs'][roles['original_kernel_envelope']]==plan['selected_expected_SHA256'][roles['original_kernel_envelope']] and old_roles['stock_envelope_record']==roles['original_kernel_envelope'], 'Original own kernel archive expected pin')
        case=envelope['cases']['B4x12'] if profile=='primary90' else envelope['B4x12'];bindings=case['actual_sites'] if profile=='primary90' else case['all_actual_stock_bindings']
        commitment=hashlib.sha256(json.dumps({k:case[k] for k in ('alpha_upper','beta_upper')},sort_keys=True,separators=(',',':')).encode()).hexdigest()
        require(len(bindings)==48 and commitment==old_roles['fixed_generic_alpha_beta_commitment']==roles['generic_alpha_beta_commitment'], 'Own saved full-domain alpha/beta unchanged; no alpha564 calculation')
        ordered=[next(row for row in bindings if row['stock']==site['stock']) for site in sites]
        require(exact(ordered,old_roles['fixed_all48_kernel_bindings']) and exact(ordered,witness['whole48_original_degree12_kernel_bindings'][profile]), 'All48 original full-support pointwise kernel contracts retained')
        if profile=='primary90':require(case['whole_clipped_integer_domain_covered'] is case['all_positive_stock_stored72_product144_shift_guards_passed'] is case['final_negative_shift_floor_charged_once'] is True and case['retained_classes']==30 and [case['lower_clamp_raw'],case['upper_clamp_raw']]==[-12193974156573,9145480617430], 'Original signed72/144 positivity/negative shift-floor guarantees')
        else:require(case['original_degree12_Estrin_no_AS_certificate_transfer'] is True and case['class_count']==30 and case['clamp_raw_bounds']==[-12193974156573,9145480617430], 'Independent original full signed kernel domain')
        rows=[]
        require(len(record['date_rows'])==len(roles['own_component_pointers'])==12, 'All12 own stage rows before arithmetic')
        for date,row in enumerate(record['date_rows']):
            current=[site for site in sites if site['date_zero_based']==date];pointer=roles['own_component_pointers'][date]
            require(row['profile']==profile and row['contractual_date_one_based']==date+1 and row['source_stocks']==pointer['source_stocks']==[s['stock'] for s in current] and row['source_raw_logs']==pointer['source_raw_logs']==[s['raw_log'] for s in current] and row['grouped_raw_equals_expanded'] is row['stock_grouped_equals_expanded'] is True, 'Each own date source/mean-variance/full-kernel stage scope')
            for field,key in [('kernel_squared_JSON_pointer','kernel_allowance_squared'),('raw_log_squared_JSON_pointer','raw_log_t_squared_L2_upper'),('lower_tail_JSON_pointer','new_lower_tail')]:require(pointer[field]=='/date_rows/%d/components/%s'%(date,key), 'Exactly named own already saved component pointer')
            rows.append({'date_zero_based':date,'source_stocks':row['source_stocks'],'source_raw_logs':row['source_raw_logs'],'physical_parent_record_path':roles['verified_matrix_record'],'component_pointers':pointer,'kernel_allowance_squared':row['components']['kernel_allowance_squared'],'raw_log_t_squared_L2_upper':row['components']['raw_log_t_squared_L2_upper'],'new_lower_tail':row['components']['new_lower_tail']})
        own[profile]=rows
    result={'schema':'e11-B4x12-external-cap564-stock-component-source-witness-v1','passed':True,'accepted_interface':fixed,'accepted_joint_law_witness':law,'all48_original_source_mappings':sites,'both_own_physical_matrix_records_consumed_once':True,'named_three_stages_not_assembled_old_B':True,'saved_kernel_M4608_unchanged_by_min_contraction':True,'signed_clip_raw_bounds':[-12193974156573,9145480617430],'fixed_new_guard_symbolic':'8*Q<=signed_clip_high_raw','fixed_guard_elementary_implication':'exp(1)>=8/3; exp(8)>=(8/3)^8>564','virtual_native_and_continuous_cap_preserve_original_strict140_payoff':True,'ideal_closed139_to141_band_unchanged_at_cap564':True,'native_closed_band_equivalence_claimed':False,'uncapped_ideal_shared_Gaussian_factorization_only':True,'global_capped_exponential_Lipschitz564':True,'upper_clamp_discrepancy_zero_after_fixed_guard':True,'saved_unconditional_lower_tail_retained':True,'no_old_upper_tail_subtraction_or_alpha564':True,'no_new_emitted_cap_circuit_or_resource_savings':True,'full_price_G2_candidate_physical_or_advantage_excluded':True}
    return result,own



def compose(profile, plan, own):
    require(profile in ('primary90','independent130') and exact(plan['interface']['external_cap_dollars'],[564,1]) and plan['interface']['adaptive_cap_grid_or_profile_selection'] is False, 'One fixed cap564 three-stage expression only, no grid/fallback')
    Q=1099511627776;clip_high=9145480617430
    require(type(plan['signed_clip_raw_bounds'][1]) is int and plan['signed_clip_raw_bounds']==[-12193974156573,clip_high], 'Original signed upper clamp before sole fixed new guard')
    guard=8*Q<=clip_high
    require(guard, 'Fixed cap564 upper-clamp guard failed; no cap widening or retry')
    cap=Fraction(564);cap_squared=times(cap,cap);three=Fraction(3)
    rows=[];certificates=own[profile]
    require(len(certificates)==12 and [c['date_zero_based'] for c in certificates]==list(range(12)), 'All12 own dates before numerical work')
    for saved in certificates:
        kernel=limb_ratio(saved['kernel_allowance_squared']);raw=limb_ratio(saved['raw_log_t_squared_L2_upper']);lower=limb_ratio(saved['new_lower_tail'])
        transported=times(cap_squared,raw);stages=[kernel,transported,lower];ordered=stages if profile=='primary90' else list(reversed(stages))
        subtotal=Fraction(0);expanded=Fraction(0)
        for stage in ordered:subtotal=plus(subtotal,stage);expanded=plus(expanded,times(three,stage))
        bound=times(three,subtotal)
        require(bound==expanded, 'Own fixed three-stage grouped/distributed identity; no old assembled B reconstruction')
        components={'saved_kernel_allowance_squared':saved['kernel_allowance_squared'],'saved_raw_log_t_squared_L2_upper':saved['raw_log_t_squared_L2_upper'],'saved_new_lower_tail':saved['new_lower_tail'],'external_cap':pair(cap),'external_cap_squared':pair(cap_squared),'transported_capped_raw_log_squared_L2':pair(transported),'three_stage_subtotal':pair(subtotal),'capped_stock_squared_L2_upper':pair(bound),'independent_distributed_expression':pair(expanded)}
        rows.append({'schema':'e11-B4x12-original-date-external-cap564-stock-squared-L2-limb-row-v1','profile':profile,'units':'dollars_squared','contractual_date_one_based':saved['date_zero_based']+1,'source_stocks':saved['source_stocks'],'source_raw_logs':saved['source_raw_logs'],'physical_parent_record_path':saved['physical_parent_record_path'],'own_component_pointers':saved['component_pointers'],'components':components,'per_stock_instantiations':[{'asset_zero_based':asset,'source_stock':stock,'source_raw_log':log,'bound':pair(bound),'same_profile_same_mean_variance_and_full_kernel':True} for asset,(stock,log) in enumerate(zip(saved['source_stocks'],saved['source_raw_logs']))],'new_fixed_guard_8Q_le_signed_clip_high':guard,'three_stage_grouped_equals_distributed':True,'old_kernel_M4608_reused_unchanged':True,'lower_tail_reused_unchanged':True,'upper_tail_omitted_by_new_pointwise_cap_proof':True,'old_final_B_or_upper_tail_reconstructed_subtracted':False,'new_alpha564_or_old_recipe_called':False})
    return {'schema':'e11-B4x12-external-cap564-original-stock-component-limb-matrix-v1','profile':profile,'units':'dollars_squared','external_cap_dollars_fixed':[564,1],'contractual_dates_one_based':list(range(1,13)),'own_numeric_row_count':12,'original_stock_sites':48,'own_profile_site_instantiations':48,'date_rows':rows,'chosen_formula':'3*(savedA_squared+564^2*savedBlog_raw+savedTlower)','parent_kernel_M_fixed':4608,'old_assembled_stock_B_decomposed':False,'old_upper_tail_subtracted':False,'new_alpha564_estimate_claimed':False,'stock_native_or_error_independence_assumed':False,'adaptive_cap_grid_profile_or_improvement_adoption':False,'virtual_postprocessor_not_emitted_cap_circuit':True,'payoff_equivalence_symbolic_only_not_whole_payoff_error_certificate':True,'full_price_G2_candidate_physical_resource_or_advantage_results':None}



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
    require(CURRENT_EXTERNAL_CAP564_AUTHORING_AND_PROOF_BOUND is True, 'Disabled cap564 draft needs ROOT fullread and current release')
    try:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ready-sha256',required=True);args=parser.parse_args()
        base=Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True)==ROOT and Path(__file__).resolve(strict=True)==SOURCE,'Exact isolated default4300')
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256],'Separate original base argv0/venv and exact current absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(),'Pinned isolated paths/no ZIP/no site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'Unused own output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','external_cap564_stock_component_execution_authorized','external_cap564_stock_component_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-external-cap564-stock-component-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['external_cap564_stock_component_execution_authorized'] is True,'Own current fixed external-cap564 component release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['external_cap564_stock_component_transfer_witness_accepted'] is True and review['factual_projection_exact_against_verified_matrix_ROOT'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        files['external_cap564_original_stock_component_witness.json']=save('external_cap564_original_stock_component_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_twelve_date_cap564_stock_component_matrix.json']=save('primary_twelve_date_cap564_stock_component_matrix.json',primary)
        files['independent_twelve_date_cap564_stock_component_matrix.json']=save('independent_twelve_date_cap564_stock_component_matrix.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'no_minimum_or_cross_profile_selection':True,'one_fixed_cap564_three_stage_expression':True,'all24_own_rows_and96_site_instantiations':True,'both_own_grouped_expanded_identities':True,'only_three_own_saved_component_operands_consumed':True,'saved_lower_tail_retained_and_upper_tail_omitted_by_new_pointwise_cap_proof':True,'saved_M4608_kernel_unchanged_fixed_cap564_at_all_dates':True,'no_native_error_or_stock_independence':True,'old_final_B_upper_tail_and_new_alpha564_not_numeric_operands':True,'output_rationals_all_canonical_limbs':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'completed_own_numeric_rows':24,'completed_own_profile_site_instantiations':96,'original_distinct_stock_sites':48,'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'old_native_kernel_raw_log_tail_moment_exp_or_provider_recipe_called':False,'new_fixed_cap564_guard_and_three_saved_stage_expression_only':True,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','all48_original_virtual_cap564_stock_component_sites_only':True,'emitted_cap_circuit_resources_whole_payoff_price_G2_or_advantage_results':None}
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
