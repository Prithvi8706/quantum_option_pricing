'Dormant fixed-Young first-date basket endpoint; own ROOT release required.'

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

SOURCE = ROOT / 'research/limitation_program_20261001/experiment_e11_first_date_basket_fixed_young_v1.py'

PLAN = ROOT / '.context/E11_FIRST_DATE_BASKET_FIXED_YOUNG_INPUT_ADAPTER_run001.json'

MD = ROOT / '.context/E11_FIRST_DATE_BASKET_FIXED_YOUNG_PREFLIGHT_run001.md'

READY = ROOT / '.context/E11_FIRST_DATE_BASKET_FIXED_YOUNG_ROOT_READY_run001.json'

OUTPUT = ROOT / 'results/limitation_program_20261001/E11_first_date_basket_fixed_young_run001'

LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'fixed_young_source_interface_witness.json', 'five_metadata_controls.json', 'primary_fixed_young.json', 'independent_fixed_young.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']

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

def interface_witness(plan,ready,inputs):
    symbolic=inputs[plan['symbolic_PLAN_path']]
    require(symbolic['fixed_choice_before_any_new_numeric_test']['delta_exact']==[1,1000000000] and symbolic['fixed_choice_before_any_new_numeric_test']['adapt_delta_from_profile_or_result'] is False and symbolic['pointwise_and_expectation_proof']['independence_or_favorable_error_sign_used'] is False,'Fixed prospective Young weight and no adaptive selection')
    require(exact(plan['interface'],ready['interface']) and ready['fixed_young_floor_transport_witness_accepted'] is True,'Own reviewed endpoint interface')
    certificate=inputs[plan['parent_ROOT_verification']];mf=inputs[plan['parent_manifest']];witness=inputs[plan['parent_source_witness']]
    require(certificate['schema']=='root-e11-first-date-stocks-basket-saved-verification-v1' and certificate['passed'] is True and type(certificate['ROOT_observed_terminal_exit_code']) is int and certificate['ROOT_observed_terminal_exit_code']==0 and certificate['fixture_credit']==0 and certificate['manifest_SHA256']==plan['selected_expected_SHA256'][plan['parent_manifest']],'Verified nineteen-file parent, not a terminal or manifest alone')
    require(certificate['source_branch_transfer_witness_accepted'] is certificate['first_date_only'] is certificate['final_quarter_floor_paid'] is True and certificate['financial_price_policy_G2_or_quantum_advantage'] is certificate['new_native_downstream_G2_recertification'] is False and exact(certificate['accepted_interface'],plan['parent_interface']),'Exact verified parent first-date scope and paid floor')
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['budget_censored'] is False and mf['inclusive_files']==19,'Original parent seal')
    require(witness['schema']=='e11-first-date-four-stock-source-witness-v1' and exact(witness['accepted_interface'],plan['parent_interface']) and witness['same_shifted125_to241_and_first94_to326_literal_witnesses'] is witness['full_clip_and_exp_boundaries_joined'] is witness['common_continuous_Gaussian_model_before_unchanged_projection'] is witness['own_profile_A_M_both_tails_and_old_guards_retained'] is witness['three_native_adds_exact_after_full4_no_wrap'] is witness['complete_quarter_product_below2p92_fits_signed144'] is witness['final_quarter_floor_at_most1_over_Q_paid'] is True and witness['exact_divisibility_or_native_joint_law_assumed'] is witness['old_range_provider_guard_moment_tail_series_or_native_called'] is False,'Verified same-middle/no-wrap/floor witness; no original SOURCE graph replay')
    require(mf['files'][Path(plan['parent_source_witness']).name]==plan['selected_expected_SHA256'][plan['parent_source_witness']],'Parent witness manifest membership')
    for profile,roles in plan['profiles'].items():
        recorded=next(row['records'] for row in certificate['profile_results'] if row['profile']==profile)
        for key,kind in ((roles['parent_sum'],'sum5575'),(roles['parent_basket'],'basket5576')):
            record=inputs[key]
            require(exact(record,recorded[kind]) and mf['files'][Path(key).name]==plan['selected_expected_SHA256'][key] and record['profile']==profile and record['units']=='dollars_squared_error' and record['original_first_date_only'] is True and record['native_error_or_stock_independence_assumed'] is record['old_guard_tail_moment_series_or_native_provider_called'] is record['financial_price_G2_or_quantum_advantage'] is False,'Exact verified own-profile bound premises')
        total=inputs[roles['parent_sum']];basket=inputs[roles['parent_basket']]
        require(total['schema']=='e11-first-date-four-stock-full-sum-limb-bound-v1' and total['exact_sum_value']==5575 and total['stock_values']==[4021,4417,4813,5209] and type(total['stock_allowances']) is list and len(total['stock_allowances'])==4 and total['pointwise_Cauchy_terms']==4 and total['native_add_rounding_after_no_wrap']==0,'Same four-term average middle variable')
        require(basket['schema']=='e11-first-date-four-stock-basket-limb-bound-v1' and basket['exact_basket_value']==5576 and basket['exact_sum_value']==5575 and basket['stock_values']==[4021,4417,4813,5209] and basket['Q']==1099511627776 and basket['chosen_formula']=='2*((B4021+B4417+B4813+B5209)/4+1/Q^2)' and basket['before_floor_Cauchy_terms']==4 and basket['final_floor_squared_triangle_terms']==2 and basket['exact_divisibility_by4_assumed'] is False and basket['same_profile_fixed_formula_identity_checked'] is True,'Parent fixed formula and quarter floor remain paid')
        require(exact(basket['quarter_floor_squared_allowance'],{'schema':'canonical-nonnegative-rational-base2p32-v1','numerator_sign':'positive','numerator_limbs':[1],'denominator_limbs':[0,0,65536]}),'Literal canonical1/Q^2, not a new floor guard')
    return {'schema':'e11-first-date-basket-fixed-young-interface-witness-v1','accepted_interface':plan['interface'],'parent_verified_result_expected_SHA256':plan['selected_expected_SHA256'][plan['parent_ROOT_verification']],'same_average_middle_variable_and_paid_quarter_floor':True,'parent_own_stock_A_M_tails_guards_native_and_source_witnesses_reused_without_replay':True,'fixed_delta_before_numeric_test':[1,1000000000],'no_independence_or_adaptive_selection':True,'original_PROVIDER_guard_tail_series_or_native_called':False}


def compose(profile,plan,inputs):
    total_record=inputs[plan['profiles'][profile]['parent_sum']];parent=inputs[plan['profiles'][profile]['parent_basket']]
    bounds=[limb_ratio(row) for row in total_record['stock_allowances']]
    total=Fraction(0)
    for bound in (bounds if profile=='primary90' else list(reversed(bounds))):total=plus(total,bound)
    A=times(total,Fraction(1,4));F=limb_ratio(parent['quarter_floor_squared_allowance']);old=limb_ratio(parent['dollars_squared_basket_error_upper'])
    require(old==twice(plus(A,F)),'Exact verified parent factor2 identity')
    delta=ratio([1,1000000000]);scaled_A=times(delta,A)
    condition=scaled_A>=F
    if profile=='primary90':new=plus(times(plus(Fraction(1),delta),A),times(Fraction(1000000001),F))
    else:new=plus(plus(A,times(delta,A)),plus(F,times(Fraction(1000000000),F)))
    difference=plus(old,-new)
    factored=times(plus(Fraction(1),-delta),plus(A,-times(Fraction(1000000000),F)))
    require(difference==factored and condition==(new<=old) and (scaled_A==F)==(new==old) and (scaled_A>F)==(new<old),'Fixed Young difference and nonincrease/equality/strict equivalence')
    return {'schema':'e11-first-date-basket-fixed-young-limb-bound-v1','profile':profile,'units':'dollars_squared_error','stock_values':[4021,4417,4813,5209],'exact_sum_value':5575,'exact_basket_value':5576,'delta_exact':[1,1000000000],'stock_allowances':[pair(v) for v in bounds],'average_before_floor_squared_allowance':pair(A),'quarter_floor_squared_allowance':pair(F),'parent_factor2_basket_allowance':pair(old),'fixed_young_basket_allowance':pair(new),'old_minus_new_signed_difference':signed_pair(difference),'delta_times_average_allowance':pair(scaled_A),'preregistered_nonincrease_criterion_passed':bool(condition),'nonincrease':bool(new<=old),'equal':bool(new==old),'strict':bool(new<old),'candidate_adopted_as_nonincreasing':bool(condition),'strict_improvement_adopted':bool(condition and new<old),'failed_criterion_changes_delta_or_selects_alternative':False,'failed_criterion_retains_parent_certificate_without_improvement_adoption':not bool(condition),'exact_difference_identity_checked':True,'final_quarter_floor_paid':True,'first_date_only':True,'native_error_or_stock_independence_assumed':False,'original_bound_guard_tail_moment_series_or_native_recipe_called':False,'financial_price_policy_G2_or_quantum_advantage':False}


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
        keys={'schema','ready','root_and_independent_static_reviews_passed','fixed_young_endpoint_execution_authorized','fixed_young_floor_transport_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-first-date-basket-fixed-young-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['fixed_young_endpoint_execution_authorized'] is True,'Own current endpoint release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors,'All3 current reviews before premises/origins/numbers')
        code_guard(source_raw,ready)
        caches=['research/limitation_program_20261001/__pycache__/'+SOURCE.stem+'.cpython-312'+s+'.pyc' for s in ('','.opt-1','.opt-2')]
        require(ready['existing_current_cache_SHA256']=={} and ready['absent_current_cache_paths']==sorted(caches) and all(not (ROOT/k).exists() and not (ROOT/k).is_symlink() for k in caches),'Exact unused current3 cache partition')
        inputs={}
        for key,pin in plan['selected_expected_SHA256'].items():inputs[key]=decode(read_bytes(ROOT/key,pin,records))
        origins=loaded_origins(inputs[plan['runtime_manifest']],records)
        witness=interface_witness(plan,ready,inputs);controls=controls_record(plan)
        code_guard(source_raw,ready);budget(admission=True)
        OUTPUT.mkdir(exist_ok=False);_OUTPUT_ID=[stat8(OUTPUT)[i] for i in (0,1,4,5,6,7)];_OWNS_OUTPUT=True
        files={}
        for name,data in [('executed_controller.py',source_raw),('executed_adapter.json',plan_raw),('executed_preflight.md',md_raw),('executed_ROOT_READY.json',read_bytes(READY,args.ready_sha256,records))]:files[name]=save(name,raw=data)
        files['run_started.json']=save('run_started.json',{'created_UTC_ns':time.time_ns(),'PID':os.getpid(),'caps':[CPU,ADMISSION,WALL],'default4300_no_setter':True})
        files['fixed_young_source_interface_witness.json']=save('fixed_young_source_interface_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,inputs);independent=compose('independent130',plan,inputs)
        files['primary_fixed_young.json']=save('primary_fixed_young.json',primary);files['independent_fixed_young.json']=save('independent_fixed_young.json',independent)
        reconciliation={'passed':True,'profiles_kept_separate':True,'no_minimum_or_adaptive_delta_selection':True,'same_fixed_delta_and_expression_for_both_profiles':[1,1000000000],'both_preregistered_difference_and_criterion_identities_checked':True,'failed_criterion_has_no_improvement_adoption':True,'all_outputs_canonical_limbs_including_signed_difference':True}
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',reconciliation)
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'controls':controls,'witness':witness,'reconciliation':reconciliation,'caps':[CPU,ADMISSION,WALL],'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'both_profiles_preregistered_nonincrease_criterion_passed':all(v['preregistered_nonincrease_criterion_passed'] for v in (primary,independent)),'failed_criterion_changes_delta_or_selects_alternative':False,'original_bound_guard_tail_moment_series_or_native_recipe_called':False,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'first_date_only':True,'final_quarter_floor_paid':True}
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

def signed_pair(value):
    require(type(value) is Fraction and max(value.numerator.bit_length(),value.denominator.bit_length())<=131072,'Signed difference reduced bit frontier')
    result=pair(value if value>=0 else -value)
    result['schema']='canonical-signed-rational-base2p32-v1'
    result['numerator_sign']='zero' if value==0 else 'positive' if value>0 else 'negative'
    require(limbs_integer(result['numerator_limbs'])==abs(value.numerator) and limbs_integer(result['denominator_limbs'])==value.denominator,'Complete signed magnitude limb roundtrip')
    return result


if __name__ == '__main__':
    main()
