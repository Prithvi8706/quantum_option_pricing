'Dormant remaining first-date stocks and paid-floor basket; own ROOT release required.'

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

SOURCE = ROOT / 'research/limitation_program_20261001/experiment_e11_first_date_remaining_stocks_and_basket_v1.py'

PLAN = ROOT / '.context/E11_FIRST_DATE_REMAINING_STOCKS_AND_BASKET_INPUT_ADAPTER_run001.json'

MD = ROOT / '.context/E11_FIRST_DATE_REMAINING_STOCKS_AND_BASKET_PREFLIGHT_run001.md'

READY = ROOT / '.context/E11_FIRST_DATE_REMAINING_STOCKS_AND_BASKET_ROOT_READY_run001.json'

OUTPUT = ROOT / 'results/limitation_program_20261001/E11_first_date_remaining_stocks_and_basket_run001'

LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'source_four_stock_basket_witness.json', 'five_metadata_controls.json', 'primary_stock4813.json', 'primary_stock5209.json', 'primary_sum5575.json', 'primary_basket5576.json', 'independent_stock4813.json', 'independent_stock5209.json', 'independent_sum5575.json', 'independent_basket5576.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']

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

def budget(admission=False):
    require(_STARTED is not None and time.process_time() <= CPU and time.monotonic() - _STARTED <= WALL and (not admission or time.process_time() <= ADMISSION), 'Unchanged180/150/600 hard budgets')

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
    require(LEDGER == ready['exact19_inclusive_ledger'] and sys.get_int_max_str_digits() == 4300, 'Current ledger and decoder remain fixed')
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


def interface_witness(plan,ready,inputs):
    require(ready['source_branch_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']),'Current accepted source branches before bound transfer')
    original=inputs[plan['symbolic_PLAN_path']]
    require(original['schema']=='e11-first-date-remaining-two-stocks-and-basket-prospective-plan-v1' and exact(original['fixed_scope'],plan['scope_values']) and original['profiles']['primary90']['new4813_bound'] is original['profiles']['independent130']['new5576_basket_average_bound'] is None,'Pinned unexecuted planning scope, no inherited new result')
    require(exact(plan['selected_expected_SHA256'],{**original['selected_expected_SHA256'],plan['symbolic_PLAN_path']:plan['symbolic_PLAN_expected_SHA256']}) and original['preregistered_basket_error_proof']['chosen_once_unevaluated_formula']=='B_basket = 2*( (B4021+B4417+B4813+B5209)/4 + 1/Q^2 )' and original['preregistered_basket_error_proof']['independence_required'] is False,'Exact selected bytes and one preregistered basket expression')
    require(plan['interface']['source_normal_branches']=={'241':'shifted_three_quarter_cosine','326':'first_cosine'} and plan['interface']['quarter_floor_squared_allowance']==[1,1208925819614629174706176] and plan['interface']['native_error_or_stock_independence_assumed'] is False,'Shifted branch and paid quarter floor are mandatory')
    theorem=inputs[plan['native_theorem']]
    require(theorem['shifted_second_cosine_exact_three_quarter_circular_grid_slot_same_bound'] is True and theorem['original_U_V_uniform_cell_coupling'] is True and theorem['scope']['digital_pair_independence'] is False and theorem['scope']['source_law']=='original_B4_B8_Q32_shared_U_V_BoxMuller_F40_W72','Unchanged verified shifted-coordinate arithmetic/coupling theorem')
    old_composition=inputs[plan['coordinate_composition_plan']]
    require(exact(old_composition['interface'],original['retained_native_coordinate_interface']) and old_composition['interface']['middle_coordinates']==['sqrt(-2*ln(U_M))*cos(2*pi*V_M)','sqrt(-2*ln(U_M))*cos(2*pi*((V_M+3/4) mod 1))'] and old_composition['interface']['native_quantizer']=={'F':40,'Q':32,'W':72,'clipped':False},'Both identical midpoint orientations, unclipped coordinate premise')
    coord_root=inputs[plan['coordinate_ROOT_verification']]
    require(coord_root['passed'] is True and coord_root['native_or_radial_SOURCE_called'] is coord_root['new_native_arithmetic_or_downstream_financial_recertification'] is False,'Completed coordinate premise, no new native proof')
    target=inputs[plan['target']]
    require(target['fraction_bits']==40 and target['width']==72,'Exact original native word geometry')
    nodes={v:row for row in target['nodes'] for v in row['out']}
    binding=inputs[plan['native_sampler_binding']]
    require(binding['original_target_expected_SHA256']==plan['selected_expected_SHA256'][plan['target']] and binding['digital_pair_independence'] is False and [p['normal_values'] for p in binding['all_original_joint_pair_scopes'][:3]]==[[94,125],[210,241],[326,357]],'Original pair branches from declared target')
    rows=original['source_normal_marginal_witnesses']
    require([(r['old_normal'],r['new_normal']) for r in rows]==[(125,241),(94,326)],'Same shifted branch and same first-cosine branch, never first-to-shifted')
    pairs=binding['all_original_joint_pair_scopes']
    require([r['original_raw_uniform_boundaries'] for r in rows]==[pairs[0]['raw_uniform_values'],pairs[0]['raw_uniform_values']] and [r['new_raw_uniform_boundaries'] for r in rows]==[pairs[1]['raw_uniform_values'],pairs[2]['raw_uniform_values']],'Exact original pair boundaries for each same branch')
    for row in rows:
        old=source_signature(nodes,row['old_normal'],dict(zip(row['original_raw_uniform_boundaries'],('U_word','V_word'))))
        new=source_signature(nodes,row['new_normal'],dict(zip(row['new_raw_uniform_boundaries'],('U_word','V_word'))))
        require(exact(old,row['old_literal_scope']) and exact(new,row['new_literal_scope']) and old['canonical_ordered_except_add_mul_DAG_SHA256']==new['canonical_ordered_except_add_mul_DAG_SHA256'],'Every original normal literal/midpoint/angle/lookup/output row and exact commutation witness')
    stock_envelope=inputs[plan['stock_envelope']]['B4x12']
    firstdate=sorted([r for r in stock_envelope['all_actual_stock_bindings'] if r['date']==0],key=lambda r:r['asset'])
    require([(r['raw_log'],r['clipped'],r['stock']) for r in firstdate]==[(3542,3579,4021),(3660,3697,4417),(3778,3815,4813),(3896,3933,5209)],'Actual first-date raw/clip/stock routes, not later date')
    require([(r['new_stock'],r['raw_log'],r['clipped_log']) for r in original['source_stock_clip_exp_witnesses']]==[(4813,3778,3815),(5209,3896,3933)],'Exact new two stock boundaries')
    for row in original['source_stock_clip_exp_witnesses']:
        fresh=[source_signature(nodes,4021,{3579:'same_clipped_F40_log'}),source_signature(nodes,row['new_stock'],{row['clipped_log']:'same_clipped_F40_log'}),source_signature(nodes,3579,{3542:'same_raw_F40_log'}),source_signature(nodes,row['clipped_log'],{row['raw_log']:'same_raw_F40_log'})]
        require(all(exact(a,row[k]) for a,k in zip(fresh,('old_exp_scope','new_exp_scope','old_clip_scope','new_clip_scope'))) and fresh[0]['canonical_ordered_except_add_mul_DAG_SHA256']==fresh[1]['canonical_ordered_except_add_mul_DAG_SHA256'] and fresh[2]['canonical_ordered_except_add_mul_DAG_SHA256']==fresh[3]['canonical_ordered_except_add_mul_DAG_SHA256'],'Full new clipping/degree12/native exponential graph equality, not just template labels')
        actual=firstdate[row['asset_zero_based']]
        require(exact({k:actual[k] for k in row['saved_binding']},row['saved_binding']),'Exact saved stock binding')
    primary=inputs[plan['primary_raw_ranges']]['cases']['B4x12'];independent=inputs[plan['independent_raw_ranges']]['B4x12']
    require(primary['every_stored72_raw_partial_sum_safe'] is primary['every_signed144_scaled_normal_product_safe'] is True and independent['every_stored_partial_sum_and_product_safe'] is independent['additive_rounding_zero_only_after_no_wrap'] is True,'Original every partial/signed product no-wrap, no new range evaluator')
    values={3492,3742,3743,3744,3778,3860,3861,3862,3896}
    selected=[r for r in independent['actual_raw_prefix_word_guards'] if r['value'] in values]
    require({r['value'] for r in selected}==values and exact(selected,original['own_saved_all_partial_no_wrap_witness']['selected_independent_rows']) and all(exact(nodes[v],r) for r in original['remaining_first_date_log_rows'] for v in r['out']),'Literal common/idio/drift/initial source rows and all-partial range premises')
    require(primary['actual_common_literal']==independent['actual_common_raw']==60222732077 and primary['actual_idio_literal']==independent['actual_idio_raw']==73757482253 and primary['actual_drift_literal']==independent['actual_drift_raw']==-1374389535 and primary['actual_initial_literal']==independent['actual_initial_raw']==5063438167381,'Unchanged five-term log coefficients/constants and same mean/variance before projection')
    require(exact(original['original_product_uniform_model'],plan['original_product_uniform_model']) and plan['original_product_uniform_model']['whole_native_joint_law_transfer'] is False and plan['original_product_uniform_model']['arbitrary_correlated_or_changed_preparation_covered'] is False,'Same original six-uniform ideal model, no native/error/stock independence claim')
    for source_key,expected in original['selected_source_definition_witnesses'].items():
        tree=ast.parse(inputs[source_key]);actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in expected}
        require(actual=={name:row['AST_SHA256'] for name,row in expected.items()},'Original builder/normal branches/IR floor semantics plaintext only')
    basket=[nodes[v] for v in (5573,5574,5575,5576)]
    require(exact(basket,original['basket_source_rows']) and basket==[{'op':'add','args':[4021,4417],'params':{},'out':[5573]},{'op':'add','args':[4813,5209],'params':{},'out':[5574]},{'op':'add','args':[5573,5574],'params':{},'out':[5575]},{'op':'cmul','args':[5575],'params':{'c':274877906944},'out':[5576]}],'Exact balanced4-stock adds and quarter-scaling row')
    bounds=stock_envelope['native_stock_raw_bounds']
    require(bounds==[16777216,4503599627354112] and all(type(v) is int for v in bounds) and bounds[0]>=0 and bounds[1].bit_length()==52 and original['basket_integer_representation_proof']['exact_divisibility_by4_proved'] is False,'All positive stocks below2^52, sumbelow2^54/productbelow2^92/no72wrap; floor not waived')
    root_stock=inputs[plan['current_stock_ROOT_verification']];mf=inputs[plan['current_stock_manifest']]
    require(root_stock['passed'] is True and type(root_stock['ROOT_observed_terminal_exit_code']) is int and root_stock['ROOT_observed_terminal_exit_code']==0 and root_stock['fixture_credit']==0 and root_stock['manifest_SHA256']==plan['selected_expected_SHA256'][plan['current_stock_manifest']] and root_stock['stock_log_projection_transfer_witness_accepted'] is True and root_stock['financial_price_policy_G2_or_quantum_advantage'] is root_stock['new_native_downstream_G2_recertification'] is False and mf['passed'] is mf['completed'] is True and mf['budget_censored'] is False,'Completed stock certificate before own transfer; no inherited grant')
    require(exact(root_stock['accepted_interface'],inputs[plan['current_stock_adapter']]['interface']),'Original stock projection/guard/tail operands stay pinned')
    for profile,roles in plan['profiles'].items():
        record=inputs[roles['completed_stock_record']]
        require(record['profile']==profile and next(r for r in root_stock['profile_results'] if r['profile']==profile)==record and mf['files'][Path(roles['completed_stock_record']).name]==plan['selected_expected_SHA256'][roles['completed_stock_record']] and record['only_B_and_B_log_replaced'] is record['new_log_not_greater_than_old_saved_B_log'] is record['no_extra100_factor'] is True and record['native_pair_or_error_or_stock_independence_assumed'] is record['old_guard_tail_moment_series_or_native_provider_called'] is False,'Exact ROOT verified own stock record with retained A/M/both tails, no other profile')
        require(exact(record['new4021_stock_dollars_squared_L2'],record['new4417_source_scoped_stock_dollars_squared_L2']),'Original two own marginal stock allowances equal before new source transfer')
    return {'schema':'e11-first-date-four-stock-source-witness-v1','accepted_interface':plan['interface'],'source_normal_branches':plan['interface']['source_normal_branches'],'first_date_source_routes':plan['scope_values'],'same_shifted125_to241_and_first94_to326_literal_witnesses':True,'full_clip_and_exp_boundaries_joined':True,'common_continuous_Gaussian_model_before_unchanged_projection':True,'own_profile_A_M_both_tails_and_old_guards_retained':True,'three_native_adds_exact_after_full4_no_wrap':True,'complete_quarter_product_below2p92_fits_signed144':True,'final_quarter_floor_at_most1_over_Q_paid':True,'exact_divisibility_or_native_joint_law_assumed':False,'old_range_provider_guard_moment_tail_series_or_native_called':False}



def compose(profile,plan,inputs):
    own=inputs[plan['profiles'][profile]['completed_stock_record']]
    first=limb_ratio(own['new4021_stock_dollars_squared_L2']);second=limb_ratio(own['new4417_source_scoped_stock_dollars_squared_L2'])
    require(first==second,'Only ROOT verified same-profile equal marginal stock allowances')
    common={'profile':profile,'units':'dollars_squared_error','original_first_date_only':True,'native_error_or_stock_independence_assumed':False,'old_guard_tail_moment_series_or_native_provider_called':False,'financial_price_G2_or_quantum_advantage':False}
    third={'schema':'e11-first-date-stock-source-transfer-limb-bound-v1','exact_stock_value':4813,'exact_raw_log_value':3778,'exact_native_normal':241,'native_branch':'shifted_three_quarter_cosine','dollars_squared_stock_error_upper':pair(first),'copied_from_own_verified4021_after_exact_source_witness':True,'A_M_both_tail_premises_unchanged':True,'new_bound_arithmetic_performed':False,**common}
    fourth={'schema':'e11-first-date-stock-source-transfer-limb-bound-v1','exact_stock_value':5209,'exact_raw_log_value':3896,'exact_native_normal':326,'native_branch':'first_cosine','dollars_squared_stock_error_upper':pair(first),'copied_from_own_verified4021_after_exact_source_witness':True,'A_M_both_tail_premises_unchanged':True,'new_bound_arithmetic_performed':False,**common}
    bounds=[first,second,first,first]
    total=Fraction(0)
    for value in (bounds if profile=='primary90' else list(reversed(bounds))):total=plus(total,value)
    full=times(Fraction(4),total) if profile=='primary90' else twice(twice(total))
    floor_squared=Fraction(1,1208925819614629174706176)
    if profile=='primary90':basket=twice(plus(times(total,Fraction(1,4)),floor_squared))
    else:basket=plus(times(total,Fraction(1,2)),twice(floor_squared))
    require(basket==plus(times(full,Fraction(1,8)),twice(floor_squared)),'One selected basket expression equals full-sum transport plus paid floor, no adaptive candidate')
    stock_values=[4021,4417,4813,5209]
    sum_record={'schema':'e11-first-date-four-stock-full-sum-limb-bound-v1','exact_sum_value':5575,'stock_values':stock_values,'stock_allowances':[pair(v) for v in bounds],'dollars_squared_sum_error_upper':pair(full),'pointwise_Cauchy_terms':4,'native_add_rounding_after_no_wrap':0,**common}
    basket_record={'schema':'e11-first-date-four-stock-basket-limb-bound-v1','exact_basket_value':5576,'exact_sum_value':5575,'stock_values':stock_values,'dollars_squared_basket_error_upper':pair(basket),'quarter_floor_squared_allowance':pair(floor_squared),'chosen_formula':'2*((B4021+B4417+B4813+B5209)/4+1/Q^2)','Q':1099511627776,'before_floor_Cauchy_terms':4,'final_floor_squared_triangle_terms':2,'exact_divisibility_by4_assumed':False,'same_profile_fixed_formula_identity_checked':True,**common}
    return {'stock4813':third,'stock5209':fourth,'sum5575':sum_record,'basket5576':basket_record}



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
        keys={'schema','ready','root_and_independent_static_reviews_passed','first_date_stock_basket_transfer_authorized','source_branch_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact19_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-first-date-stock-basket-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['first_date_stock_basket_transfer_authorized'] is True,'Own new current release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['default_decimal_digits']==4300 and plan['exact19_inclusive_ledger']==ready['exact19_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors,'All3 current reviews before premises/origins/numbers')
        code_guard(source_raw,ready)
        caches=['research/limitation_program_20261001/__pycache__/'+SOURCE.stem+'.cpython-312'+s+'.pyc' for s in ('','.opt-1','.opt-2')]
        require(ready['existing_current_cache_SHA256']=={} and ready['absent_current_cache_paths']==sorted(caches) and all(not (ROOT/k).exists() and not (ROOT/k).is_symlink() for k in caches),'Exact unused current3 cache partition')
        inputs={}
        for key,pin in plan['selected_expected_SHA256'].items():
            data=read_bytes(ROOT/key,pin,records);mode=plan['selected_input_modes'][key]
            require(mode in ('ordinary_json','plaintext_AST_only'),'No old huge ROOT decimal recipe parsing or unknown decode roles')
            inputs[key]=decode(data) if mode=='ordinary_json' else data
        native=inputs[plan['runtime_manifest']];origins=loaded_origins(native,records)
        witness=interface_witness(plan,ready,inputs);controls=controls_record(plan)
        code_guard(source_raw,ready);budget(admission=True)
        OUTPUT.mkdir(exist_ok=False);_OUTPUT_ID=[stat8(OUTPUT)[i] for i in (0,1,4,5,6,7)];_OWNS_OUTPUT=True
        files={}
        for name,data in [('executed_controller.py',source_raw),('executed_adapter.json',plan_raw),('executed_preflight.md',md_raw),('executed_ROOT_READY.json',read_bytes(READY,args.ready_sha256,records))]:files[name]=save(name,raw=data)
        files['run_started.json']=save('run_started.json',{'created_UTC_ns':time.time_ns(),'PID':os.getpid(),'caps':[CPU,ADMISSION,WALL],'default4300_no_setter':True})
        files['source_four_stock_basket_witness.json']=save('source_four_stock_basket_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,inputs);independent=compose('independent130',plan,inputs)
        for prefix,bundle in [('primary',primary),('independent',independent)]:
            for key in ('stock4813','stock5209','sum5575','basket5576'):
                name=prefix+'_'+key+'.json';files[name]=save(name,bundle[key])
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'no_minimum_or_cross_profile_selection':True,'two_copied_stock_allowances_from_own_verified4021_only':True,'fixed_basket_formula_and_paid_quarter_floor':True,'output_rationals_all_canonical_limbs':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[{'profile':'primary90','records':primary},{'profile':'independent130','records':independent}],'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'native_range_guard_tail_moment_series_or_provider_called':False,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','first_date_only':True,'final_quarter_floor_paid':True}
        files['summary.json']=save('summary.json',summary)
        require(set(files)==set(LEDGER)-{'manifest.json'} and {p.name for p in OUTPUT.iterdir()}==set(files),'Exact preseal18/no failure')
        manifest={'passed':True,'completed':True,'budget_censored':False,'files':files,'manifest_self_hash_excluded':True,'inclusive_files':19,'author_method_SHA256':authors,'ROOT_READY_expected_SHA256':args.ready_sha256,'selected_expected_SHA256':plan['selected_expected_SHA256'],'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0}
        seal=save('manifest.json',manifest);require({p.name for p in OUTPUT.iterdir()}==set(LEDGER),'Exact sealed19/no failure');budget()
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
