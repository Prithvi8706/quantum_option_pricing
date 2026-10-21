'Dormant date2 original native stock4054 squared-L2 with own projection and both continuous tails; ROOT release required.'

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

SOURCE = ROOT / 'research/limitation_program_20261001/experiment_e11_second_date_first_stock_squared_l2_v1.py'

PLAN = ROOT / '.context/E11_SECOND_DATE_FIRST_STOCK_SQUARED_L2_INPUT_ADAPTER_run001.json'

MD = ROOT / '.context/E11_SECOND_DATE_FIRST_STOCK_SQUARED_L2_PREFLIGHT_run001.md'

READY = ROOT / '.context/E11_SECOND_DATE_FIRST_STOCK_SQUARED_L2_ROOT_READY_run001.json'

OUTPUT = ROOT / 'results/limitation_program_20261001/E11_second_date_first_stock_squared_L2_run001'

LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'source_projection_and_continuous_law_witness.json', 'five_metadata_controls.json', 'primary_stock4054_squared_L2.json', 'independent_stock4054_squared_L2.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']

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
    require(ready['date2_stock4054_projection_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']), 'Current date2 stock4054 witness before any numerical assembly')
    original=inputs[plan['symbolic_PLAN_path']]
    require(original['schema']=='e11-date2-stock4054-projection-tail-prospective-plan-v1' and original['scientific_evaluation_performed'] is original['SOURCE_authoring_READY_or_SCI_authorized_by_PLAN'] is False and all(exact(plan[k],original[k]) for k in ('interface','profiles','source_scope_proof','fixed_expression','selected_expected_SHA256','selected_input_modes')), 'Exactly the fixed prospective operands, proof and route; not an inherited execution grant')
    expected_scope={'case':'B4x12','asset_zero_based':0,'contractual_date_one_based':2,'saved_date_zero_based':1,'raw_log':3543,'clipped_log':3583,'count':4023,'remainder':4026,'polynomial':4053,'stock':4054,'W':72,'F':40}
    require(exact(plan['interface']['source_scope'],expected_scope) and plan['interface']['profiles']==['primary90','independent130'] and plan['interface']['M_fixed']==1024 and plan['interface']['kernel']=='original_degree12_full_clipped_domain' and exact(plan['interface']['tail_model'],{'both_unconditional_continuous_tails':True,'original_continuous_ideal_product_uniform_law':True,'native_error_or_stock_independence_assumed':False}), 'Only original native stock4054 with fixedM1024 and both continuous tails')
    feasibility=inputs[plan['accepted_assessment_path']]
    require(feasibility['schema']=='e11-date2-stock4054-projection-tail-feasibility-assessment-v1' and feasibility['assessment_metadata_checks_passed'] is True and feasibility['scientific_evaluation_performed'] is feasibility['new_SOURCE_READY_SCI_or_grant_authorized'] is False and feasibility['selected_fixed_route']['M2_fixed']==1024 and feasibility['selected_fixed_route']['new_bounds_guards_ratios_kernels_moments_tails_transcendentals_evaluated'] is False and feasibility['qualification']['candidate_site2_source_cells_phase_and_financial_L2_remain_separate'] is True, 'Accepted metadata feasibility fixes the route and excludes candidate finance')
    require(all(plan['selected_expected_SHA256'][k]==pin for k,pin in feasibility['selected_expected_SHA256'].items()) and exact(feasibility['scope'],plan['accepted_assessment_scope']), 'Every prior expected role and accepted scoped witness remains pinned')
    assessment=inputs[plan['original_interface_assessment_path']]
    require(assessment['assessment_metadata_checks_passed'] is True and assessment['SOURCE_or_model_functions_called'] is assessment['arrays_opened_hashed_or_decoded'] is assessment['scientific_evaluation_performed'] is False and exact(assessment['source_ids'],plan['source_scope_proof']['source_ids']), 'Original date2 source-ID metadata only')
    target=inputs[plan['target']];nodes={v:row for row in target['nodes'] for v in row['out']}
    require(type(target['width']) is type(target['fraction_bits']) is int and target['width']==72 and target['fraction_bits']==40, 'Exact original full72/F40')
    for group in ('prefix_log_and_innovation','clip_and_reduction','old_exp_all_literal_rows'):
        for row in plan['source_scope_proof']['actual_copied_source_rows'][group]:require(all(exact(nodes[v],row) for v in row['out']), 'Every actual original prefix/clip/reduction/degree12 source row')
    low_word,high_word=(nodes[v]['params']['value'] for v in (3490,3491))
    require(type(low_word) is type(high_word) is int and 0<=low_word<(1<<72) and 0<=high_word<(1<<72), 'Clip constants are exact unsigned raw72 words')
    signed_low=low_word if low_word<(1<<71) else low_word-(1<<72)
    signed_high=high_word if high_word<(1<<71) else high_word-(1<<72)
    require([signed_low,signed_high]==plan['source_scope_proof']['clip_signed_raw_bounds'], 'Normalize raw72 clip words before signed endpoint equality')
    primary=inputs[plan['primary_raw_ranges']]['cases']['B4x12'];independent=inputs[plan['independent_raw_ranges']]['B4x12']
    selected=[row for row in primary['prefixes'] if row['date']==1]
    independent_rows=[row for row in independent['actual_raw_prefix_word_guards'] if row['value']==3543]
    require(len(selected)==len(independent_rows)==1 and selected[0]['actual_raw_log_sites'][0]==3543 and selected[0]['actual_raw_log_bounds'][0]==independent_rows[0]['raw_bounds']==plan['source_scope_proof']['native_raw_interval'], 'Own new native raw3543 interval in both original complete records')
    native_low,native_high=plan['source_scope_proof']['native_raw_interval']
    require(type(native_low) is type(native_high) is int and signed_low<native_low<=native_high<signed_high and primary['every_stored72_raw_partial_sum_safe'] is primary['every_signed144_scaled_normal_product_safe'] is independent['every_stored_partial_sum_and_product_safe'] is independent['additive_rounding_zero_only_after_no_wrap'] is True, 'Clip inactive at this site after explicit signed containment and original72/144 safety')
    binding=inputs[plan['native_sampler_binding']];theorem=inputs[plan['native_theorem']]
    require(binding['original_target_expected_SHA256']==plan['selected_expected_SHA256'][plan['target']] and binding['digital_pair_independence'] is False and [binding['all_original_joint_pair_scopes'][i]['normal_values'] for i in (0,2,3)]==[[94,125],[326,357],[442,473]], 'Exact ideal coordinates Z0/Z1/Z5/Z6 with native pair sharing retained')
    prefix=[row for row in binding['complete_original_saved_source_case']['financial_roles']['prefix_witnesses'] if row['asset']==0 and row['date']==1]
    require(len(prefix)==1 and exact(prefix[0],plan['source_scope_proof']['saved_prefix_witness']) and prefix[0]['original_normal_indices']==[0,1,5,6] and prefix[0]['every_driver_multiplicity']==1 and prefix[0]['constants']==[[-1374389535,2],[5063438167381,1]], 'Initial once, ideal drift twice and four driver marginals once')
    require(theorem['original_U_V_uniform_cell_coupling'] is theorem['shifted_second_cosine_exact_three_quarter_circular_grid_slot_same_bound'] is True and theorem['scope']['digital_pair_independence'] is False and theorem['scope']['source_law']=='original_B4_B8_Q32_shared_U_V_BoxMuller_F40_W72', 'Only the original ideal product-uniform coupling and Gaussian marginal orientations')
    require(exact(plan['ideal_law_constants'],{'d':[-1,800],'a_squared':[3,1000],'b_squared':[9,2000],'Q':1099511627776,'native_initial_literal_raw':5063438167381,'mean_expression':'ln100+2*d','variance_expression':'2*(a^2+b^2)'}) and exact(feasibility['ideal_law_proof']['ideal_coordinates'],[0,1,5,6]), 'New ideal mean/variance from four continuous normal coordinates, no native error independence')
    financial=binding['complete_original_saved_source_case']['financial_roles']
    require(financial['actual_common_literal']==60222732077 and financial['actual_idio_literal']==73757482253 and financial['actual_drift_literal']==-1374389535 and financial['actual_initial_literal']==5063438167381 and financial['native_literal_coefficients_equal_ideal_claimed'] is False and primary['exact_drift']==[-1,800], 'Actual native literals versus distinct original ideal parameters')
    pair_incidence=[]
    for pair_row in financial['actual_pair_roles']:
        rows=[row for row in pair_row['stock_prefix_incidence'] if row['asset']==0 and row['date']==1]
        require(len(rows)==1, 'Complete original selected-stock incidence in each source pair')
        if any(rows[0]['active']):pair_incidence.append({'pair':pair_row['pair'],'active':rows[0]['active'],'ideal_squared_norm':rows[0]['ideal_squared_norm']})
    require(exact(pair_incidence,[{'pair':0,'active':[True,True],'ideal_squared_norm':[3,400]},{'pair':2,'active':[False,True],'ideal_squared_norm':[3,1000]},{'pair':3,'active':[True,False],'ideal_squared_norm':[9,2000]}]) and [binding['all_original_joint_pair_scopes'][i]['raw_uniform_values'] for i in (0,2,3)]==[[0,1],[242,243],[358,359]], 'All and only the three independent continuous input pairs and their exact ideal variance incidences')
    raw_root=inputs[plan['raw_log_ROOT_verification']];raw_mf=inputs[plan['raw_log_manifest']];raw_witness=inputs[plan['raw_log_source_witness']]
    require(raw_root['passed'] is raw_root['completed'] is raw_root['date2_raw_log_transfer_witness_accepted'] is raw_root['date2_asset0_raw3543_only'] is True and type(raw_root['ROOT_observed_terminal_exit_code']) is int and raw_root['ROOT_observed_terminal_exit_code']==0 and raw_root['manifest_SHA256']==plan['selected_expected_SHA256'][plan['raw_log_manifest']] and raw_root['stock_projection_tails_candidate_or_price_results'] is None and raw_mf['passed'] is raw_mf['completed'] is True and raw_mf['inclusive_files']==13, 'Completed own raw3543 ROOT saved certificate, not a site1 log or stock bound')
    require(exact(raw_root['saved_source_prefix_and_coordinate_witness'],raw_witness) and raw_witness['all_original_signed144_and_stored72_no_wrap'] is raw_witness['initial_once_drift_twice_four_distinct_driver_slots_once'] is raw_witness['four_coefficient_product_floors_paid'] is True and exact(raw_witness['prefix'],prefix[0]), 'Verified raw witness fixes prefix/floors without reassembling raw log')
    native=inputs[plan['runtime_manifest']]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs'])==2842, 'Pinned original expected runtime authority, not a transitive union replay')
    envelopes={};own_inputs={}
    for profile,roles in plan['profiles'].items():
        raw=inputs[roles['raw_log_record']]
        require(raw['profile']==profile and raw['units']=='squared_error_of_log_price' and raw['source_raw_log']==3543 and raw['asset_zero_based']==0 and raw['contractual_date_one_based']==2 and raw['grouped_equals_expanded'] is True and raw['native_error_or_previous_log_innovation_independence_assumed'] is False and raw['stock_squared_L2_upper'] is None and any(exact(raw,row) for row in raw_root['profile_results']) and raw_mf['files'][Path(roles['raw_log_record']).name]==plan['selected_expected_SHA256'][roles['raw_log_record']], 'Exact own new raw L2, ROOT membership and manifest role; no numeric replay')
        e0_case=primary if profile=='primary90' else independent
        require(roles['e0_field'] in e0_case and exact(e0_case[roles['e0_field']],roles['fixed_original_e0']) and raw['allowed_literal_operands']['e0']['schema']=='canonical-nonnegative-rational-base2p32-v1', 'Own unchanged initial-literal allowance, not old B/kappa/A')
        envelope_doc=inputs[roles['stock_envelope_record']];case=envelope_doc['cases']['B4x12'] if profile=='primary90' else envelope_doc['B4x12']
        entries=case['actual_sites'] if profile=='primary90' else case['all_actual_stock_bindings'];sites=[row for row in entries if row['stock']==4054]
        require(len(entries)==48 and len(sites)==1 and exact(sites[0],roles['fixed_site4054_binding']) and sites[0]['raw_log']==3543 and sites[0]['clipped']==3583 and sites[0]['polynomial']==4053 and sites[0]['remainder']==4026 and sites[0]['actual_original_support_signature']==plan['source_scope_proof']['original_full_clipped_support_signature'], 'New site4054 instantiation from the complete original case-global48 envelope')
        require(native['frozen_inputs'][roles['stock_envelope_record']]==plan['selected_expected_SHA256'][roles['stock_envelope_record']] and native['frozen_inputs'][roles['raw_range_record']]==plan['selected_expected_SHA256'][roles['raw_range_record']], 'All reused generic metadata has original immutable native-manifest expected authority')
        require(hashlib.sha256(json.dumps({k:case[k] for k in ('alpha_upper','beta_upper')},sort_keys=True,separators=(',',':')).encode()).hexdigest()==roles['fixed_generic_alpha_beta_commitment'], 'Own original case-global alpha/beta exact unchanged operand commitment, not a date1 adapter')
        if profile=='primary90':
            require(case['whole_clipped_integer_domain_covered'] is case['all_positive_stock_stored72_product144_shift_guards_passed'] is case['final_negative_shift_floor_charged_once'] is True and case['retained_classes']==30 and [case['lower_clamp_raw'],case['upper_clamp_raw']]==[signed_low,signed_high] and sites[0]['exponent']==4023, 'Original complete degree12 domain, all30 classes/72/144 and paid negative shift floor')
        else:
            require(case['original_degree12_Estrin_no_AS_certificate_transfer'] is True and case['class_count']==30 and case['clamp_raw_bounds']==[signed_low,signed_high] and case['inverse_ln2_raw']==1586259972792 and case['ln2_raw']==762123384786 and sites[0]['k']==4023, 'Independent original degree12 support/constants and actual site4054 scalar count')
        envelopes[profile]={'stock':4054,'raw_log':3543,'clipped_log':3583,'case_global_original_sites':48,'exponent_classes':30,'site_binding':sites[0],'alpha_beta_commitment':roles['fixed_generic_alpha_beta_commitment'],'date1_stock_alpha_A_endpoint_proof_consumed':False}
        own_inputs[profile]={'raw_log_record':raw,'e0':e0_case[roles['e0_field']],'alpha':case['alpha_upper'],'beta':case['beta_upper']}
    kernel_results=[]
    for declaration in plan['source_scope_proof']['clip_and_exp_literal_kernel_witnesses']:
        old=source_signature(nodes,declaration['old_output'],{int(k):v for k,v in declaration['old_boundaries'].items()})
        new=source_signature(nodes,declaration['new_output'],{int(k):v for k,v in declaration['new_boundaries'].items()})
        require(old['canonical_ordered_except_add_mul_DAG_SHA256']==new['canonical_ordered_except_add_mul_DAG_SHA256']==declaration['canonical_ordered_except_add_mul_DAG_SHA256'] and old['literal_value_count_excluding_declared_boundaries']==new['literal_value_count_excluding_declared_boundaries']==declaration['literal_value_count_excluding_boundaries'], 'Whole actual clip and original degree12 kernel literal identity; only add/mul commutations')
        kernel_results.append({'role':declaration['role'],'old_output':declaration['old_output'],'new_output':declaration['new_output'],'old_literal_scope':old,'new_literal_scope':new})
    witness={'schema':'e11-date2-stock4054-source-projection-continuous-law-witness-v1','passed':True,'accepted_interface':plan['interface'],'selected_scope':expected_scope,'signed_clip_constants':[signed_low,signed_high],'native_raw_interval':plan['source_scope_proof']['native_raw_interval'],'native_clip_inactive_after_signed_containment':True,'source_prefix':prefix[0],'ideal_log':'ln100+2*d+a*(Z0+Z5)+b*(Z1+Z6)','ideal_mean':'ln100+2*d','ideal_variance':'2*(a^2+b^2)','original_pair_variance_incidence':pair_incidence,'ideal_continuous_Gaussian_law_from_original_product_uniform_BoxMuller':True,'native_values_errors_previous_log_or_stock_independence_assumed':False,'site4054_original_global_kernel_bindings':envelopes,'literal_kernel_results':kernel_results,'new_M_fixed':1024,'M_guard_theorem':'ln2>=2/3 so b2<=20/3 implies exp(b2)<=2^10','moment32_theorem':'centered continuous Gaussian moment32=(31)!!*v2^16','tilt_theorem':'E exp(2L2)1{L2>b2}=exp(2mu2+2v2)*P(N(mu2+2v2,v2)>b2)','tilt_mass_theorem':'exp(2mu2+2v2)=10000*exp(x2)<=10000/(1-x2), x2=4d+4(a^2+b^2), 0<=x2<1','both_unconditional_continuous_tails_required':True,'original_signed144_stored72_and_floor_guards_retained':True,'date1_M256_B_kappa_A_tail_numbers_or_alpha_adapter_used':False,'candidate_site2_alpha_or120_cell_financial_application_used':False,'source_or_native_range_guard_series_moment_tail_provider_replayed':False,'whole_financial_price_G2_or_quantum_advantage':False}
    return witness,own_inputs



def compose(profile, plan, own):
    require(profile in ('primary90','independent130') and plan['interface']['M_fixed']==1024, 'Own fixed prescribed stock4054 profile')
    values=own[profile];constants=plan['ideal_law_constants'];Q=constants['Q']
    B_log=limb_ratio(values['raw_log_record']['raw_log_squared_L2_upper']);e0=ratio(values['e0']);alpha=ratio(values['alpha']);beta=ratio(values['beta'])
    d=signed_ratio(constants['d']);a_squared=ratio(constants['a_squared']);b_squared=ratio(constants['b_squared'])
    M=Fraction(1024);native_a=Fraction(plan['source_scope_proof']['native_raw_interval'][0],Q);native_b=Fraction(plan['source_scope_proof']['native_raw_interval'][1],Q)
    mu_native=Fraction(constants['native_initial_literal_raw'],Q);twice_d=twice(d)
    mu_lower=plus(plus(mu_native,-e0),twice_d);mu_upper=plus(plus(mu_native,e0),twice_d)
    v1=plus(a_squared,b_squared);v2=twice(v1)
    require(v2==plus(plus(Fraction(3,400),a_squared),b_squared), 'New variance equals the three original selected-pair ideal squared norms')
    lower_distance=plus(mu_lower,-native_a);upper_distance=plus(plus(native_b,-mu_upper),-twice(v2))
    x2=plus(times(Fraction(4),d),times(Fraction(4),v1))
    require(max(native_b.numerator.bit_length()+2,native_b.denominator.bit_length()+5)<=524288, 'M guard exact comparison crossproducts bounded before evaluation')
    M_guard=native_b.numerator*3<=native_b.denominator*20
    require(M_guard and lower_distance.numerator>0 and upper_distance.numerator>0 and x2.numerator>=0 and x2.numerator<x2.denominator and mu_lower.numerator>0 and v2.numerator>0, 'All new M/lower/tilted-upper/x2 guards before every reciprocal or tail')
    tilt_denominator=plus(Fraction(1),-x2);Ktilt=times(Fraction(10000),positive_reciprocal(tilt_denominator))
    A=plus(times(alpha,M),beta)
    C16=Fraction(1);factors=plan['C16_factors']
    require(factors==list(range(1,32,2)), 'Exact fixed continuous Gaussian moment32 factors')
    for factor in (factors if profile=='primary90' else list(reversed(factors))):C16=times(C16,Fraction(factor))
    moment32=times(C16,fixed_power(v2,16))
    inverse_lower=positive_reciprocal(lower_distance);inverse_upper=positive_reciprocal(upper_distance)
    lower_tail=times(times(fixed_power(M,2),moment32),fixed_power(inverse_lower,32))
    upper_tail=times(times(Ktilt,moment32),fixed_power(inverse_upper,32))
    native_exponential_squared=fixed_power(A,2);transported_raw=times(fixed_power(M,2),B_log)
    stages=[native_exponential_squared,transported_raw,lower_tail,upper_tail]
    subtotal=Fraction(0)
    for value in (stages if profile=='primary90' else list(reversed(stages))):subtotal=plus(subtotal,value)
    bound=times(Fraction(3),subtotal)
    expanded=Fraction(0)
    for value in (stages if profile=='primary90' else list(reversed(stages))):expanded=plus(expanded,times(Fraction(3),value))
    require(bound==expanded, 'One fixed stock formula and own grouped/expanded identity; no route selection')
    components={'M2':M,'native_interval_lower':native_a,'native_interval_upper':native_b,'mu2_lower':mu_lower,'mu2_upper':mu_upper,'variance2':v2,'own_original_e0':e0,'site4054_original_generic_alpha':alpha,'site4054_original_generic_beta':beta,'A2':A,'new_lower_distance':lower_distance,'new_upper_tilted_distance':upper_distance,'tilt_x2':x2,'tilt_mass_upper':Ktilt,'C16':C16,'central_moment32':moment32,'new_lower_tail':lower_tail,'new_upper_tail':upper_tail,'verified_raw3543_squared_L2':B_log,'native_exponential_allowance_squared':native_exponential_squared,'transported_raw_log_squared_L2':transported_raw,'stock4054_squared_L2_upper':bound}
    return {'schema':'e11-date2-original-native-stock4054-squared-L2-limb-bound-v1','profile':profile,'units':'dollars_squared','source_raw_log':3543,'source_stock':4054,'asset_zero_based':0,'contractual_date_one_based':2,'original_ideal_law_constants':constants,'components':{k:pair(v) for k,v in components.items()},'new_guard_results':{'M_b_le_20_over3':M_guard,'lower_distance_strict_positive':True,'upper_tilted_distance_strict_positive':True,'tilt_x_in_zero_to_one':True,'all_guards_before_reciprocals':True},'grouped_equals_expanded':True,'chosen_formula':'3*(A2^2+M2^2*B_log2+Tlower2+Tupper2)','fixed_M2':1024,'fixed_moment_order':32,'both_unconditional_continuous_tails_paid':True,'native_values_errors_previous_log_or_stock_independence_assumed':False,'site4054_case_global_original_degree12_envelope_instantiated':True,'date1_M_B_kappa_A_tails_or_alpha_adapter_used':False,'candidate_D4S4_site2_alpha_or_financial_bound_used':False,'adaptive_M_moment_tail_route_or_cross_profile_selection':False,'extra_spot_multiplier':1,'original_native_guard_range_series_moment_tail_or_provider_reexecuted':False,'full_path_barrier_discount_payoff_financial_price_G2_or_quantum_advantage':False}



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
        keys={'schema','ready','root_and_independent_static_reviews_passed','date2_stock4054_execution_authorized','date2_stock4054_projection_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-date2-first-stock-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['date2_stock4054_execution_authorized'] is True,'Own current original date2 stock4054 release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['date2_stock4054_projection_transfer_witness_accepted'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        files['primary_stock4054_squared_L2.json']=save('primary_stock4054_squared_L2.json',primary)
        files['independent_stock4054_squared_L2.json']=save('independent_stock4054_squared_L2.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'no_minimum_or_cross_profile_selection':True,'one_prescribed_stock4054_expression':True,'both_own_grouped_expanded_identities':True,'only_own_verified_raw3543_and_original_e0_generic_kernel_operands_consumed':True,'both_new_continuous_tails_paid':True,'fixed_M1024_and_moment32':True,'no_native_error_or_stock_independence':True,'date1_M_B_kappa_A_tails_or_alpha_adapter_not_numeric_operands':True,'output_rationals_all_canonical_limbs':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'original_native_range_guard_tail_moment_series_or_provider_called':False,'new_projection_guard_and_both_continuous_tails_assembled':True,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','date2_asset0_original_native_stock4054_only':True,'candidate_or_whole_financial_price_results':None}
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
