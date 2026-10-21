'Dormant conditional d4_s4 first-stock L2; own alpha/beta and signed same-profile comparison.'

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

SOURCE = ROOT / 'research/limitation_program_20261001/experiment_e11_d4_s4_candidate_first_stock_squared_l2_v1.py'

PLAN = ROOT / '.context/E11_D4_S4_CANDIDATE_FIRST_STOCK_SQUARED_L2_INPUT_ADAPTER_run001.json'

MD = ROOT / '.context/E11_D4_S4_CANDIDATE_FIRST_STOCK_SQUARED_L2_PREFLIGHT_run001.md'

READY = ROOT / '.context/E11_D4_S4_CANDIDATE_FIRST_STOCK_SQUARED_L2_ROOT_READY_run001.json'

OUTPUT = ROOT / 'results/limitation_program_20261001/E11_d4_s4_candidate_first_stock_squared_L2_run001'

LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'candidate_projection_and_transfer_witness.json', 'five_metadata_controls.json', 'primary_candidate_first_stock.json', 'independent_candidate_first_stock.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']

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
    require(ready['candidate_first_stock_projection_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']), 'Current candidate projection/source authority before numbers')
    accepted=inputs[plan['accepted_PLAN_path']]
    require(accepted['schema']=='e11-d4-s4-candidate-first-stock-squared-L2-prospective-plan-v1' and accepted['scientific_evaluation_performed'] is accepted['SOURCE_authoring_or_READY_or_SCI_authorized_by_this_plan'] is False, 'Historical accepted PLAN is scope evidence, never current permission')
    require(exact(accepted['selected_expected_SHA256'],plan['accepted_original18_expected_SHA256']) and exact(accepted['scope'],plan['source_scope']) and exact(accepted['profiles'],plan['accepted_profile_roles']), 'Exact accepted original18 and both profile roles')
    require(exact(accepted['projection_proof'],plan['projection_proof']) and exact(accepted['native_projection'],plan['native_projection']) and exact(accepted['candidate_deterministic_envelope'],plan['candidate_deterministic_envelope']), 'Whole accepted source-scoped projection and own candidate envelope')
    a13=inputs[plan['A13_ROOT_verification']]
    require(a13['passed'] is a13['conditional_accuracy_premise_join_accepted'] is a13['saved120_cells_and112_occupied8_empty_checked'] is a13['saved912_forward_and_inverse_logical_case_scalar_identities_checked'] is True, 'Completed conditional allcase A13 accuracy source join, not finite-case-only evidence')
    require(type(a13['ROOT_observed_terminal_exit_code']) is int and a13['ROOT_observed_terminal_exit_code']==0 and a13['manifest_SHA256']==plan['selected_expected_SHA256'][plan['A13_manifest']] and a13['new_financial_L2_bound'] is None and a13['financial_G2_hardware_or_quantum_advantage'] is False, 'A13 completed limited boundary, no inherited financial adoption')
    witness=inputs[plan['A13_witness']]
    require(exact(a13['saved_source_and_conditional_envelope_witness'],witness), 'Exact saved ROOT witness identity')
    s=witness['source'];e=witness['conditional_accuracy']
    require(s['passed'] is e['passed'] is True and s['case']=='B4x12' and s['asset']==0 and s['date']==1 and s['raw_log']==3542 and s['clipped']==3579 and s['exponent']==3979 and s['remainder']==3982 and s['stock']==4021 and s['new_tested_polynomial']==15, 'One exact first-stock candidate source')
    require(e['relative_alpha']==plan['interface']['candidate_alpha']==[1,16777216] and e['final_negative_shift_beta']==plan['interface']['candidate_beta']==[1,1099511627776] and e['old_degree12_alpha_used'] is s['old_degree12_alpha_used'] is False and e['compiled_signed_shift_phase_remains_open'] is True and s['realized_signed_shift_circuit_and_phase_proved'] is False, 'Candidate own alpha/beta; realized phase remains open')
    transfer=inputs[plan['original_native_improved_stock_ROOT']]
    require(transfer['passed'] is transfer['stock_log_projection_transfer_witness_accepted'] is True and type(transfer['ROOT_observed_terminal_exit_code']) is int and transfer['ROOT_observed_terminal_exit_code']==0 and transfer['manifest_SHA256']==plan['selected_expected_SHA256'][plan['improved_stock_manifest']] and transfer['financial_price_policy_G2_or_quantum_advantage'] is False, 'Completed same-profile original-native comparison and unchanged log certificate')
    for manifest_key in plan['selected_owner_manifests']:
        manifest=inputs[manifest_key]
        require(manifest['passed'] is manifest['completed'] is True, 'Completed selected owner only')
        for key,pin in plan['selected_expected_SHA256'].items():
            if Path(key).parent==Path(manifest_key).parent and key!=manifest_key:
                require(manifest['files'][Path(key).name]==pin, 'Selected owned role joins exact sealed SHA')
    for source_key,names in plan['original_source_definition_AST_SHA256'].items():
        tree=ast.parse(inputs[source_key]);actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names}
        require(actual==names, 'Original proof SOURCE plaintext AST only; never import or invoke')
    support=inputs[plan['native_support_record']]['cases']['B4x12']['prefixes'][0]['actual_raw_log_bounds'][0]
    require(support==plan['native_projection']['original_all_input_raw_interval']==[4155861047200,5968266508490], 'Original native all-input first-site support')
    oldw=inputs[plan['old_stock_source_witness']]
    require(oldw['native_clamp_inactive_unconditionally_at_this_site_only'] is True and oldw['continuous_L_unbounded_both_tails_still_required'] is True and exact(oldw['original_raw_log_contract'],accepted['accepted_ideal_model']['native_log_source_scope']), 'Unchanged upstream source/coupling and both unbounded continuous tails')
    oldadapter=inputs[plan['old_transfer_adapter']]
    require(exact(oldadapter['projection_theorem'],accepted['historical_projection_theorem']), 'Historical projection theorem is proof evidence; old amplitude is not current numerical authority')
    for profile,roles in plan['profiles'].items():
        sub=inputs[roles['verified_improved_log_record']];components=inputs[roles['old_projection_components_record']]
        require(sub['profile']==profile and any(exact(sub,row) for row in transfer['profile_results']) and sub['no_extra100_factor'] is True and sub['native_pair_or_error_or_stock_independence_assumed'] is False, 'Exact verified own-profile log and original-native stock comparison')
        require(components['all_three_own_profile_guards_before_reciprocals'] is components['both_unconditional_continuous_tails_paid'] is components['fixed_M256_moment32'] is True and components['native_source_clipping_inserted'] is components['digital_pair_independence'] is False, 'Saved guards/tails kept as evidence, not replayed')
        c=components['exact_rational_components'];allowed=roles['allowed_original_component_fields']
        require(exact({key:c[key] for key in allowed},plan['saved_allowed_projection_fields'][profile]) and c['M']==[256,1] and c['v']==[3,400], 'Only allowlisted original support/projection/tail fields; old A/alpha/B_log/beta excluded')
    return {'accepted_interface':plan['interface'],'conditional_candidate_envelope_accepted':True,'one_stock4021_dollars_squared_only':True,'projection_proof':plan['projection_proof'],'both_original_saved_unconditional_Gaussian_tails_reused':True,'old_degree12_alpha_A_B_log_beta_read_as_candidate_numeric_premises':False,'native_sampler_guard_moment_tail_series_or_caller_reexecuted':False,'finite_cases_are_only_supplements':True,'compiled_signed_shift_phase_and_cleanup_remain_open':True,'no_native_pair_error_or_stock_independence':True,'M_is_native_exp_cap_and_projection_Lipschitz_not_candidate_stock_cap':True}



def compose(profile,plan,inputs):
    roles=plan['profiles'][profile]
    sub=inputs[roles['verified_improved_log_record']]
    c=inputs[roles['old_projection_components_record']]['exact_rational_components']
    M,lower,upper=(ratio(c[key]) for key in ('M','lower_tail','upper_tail'))
    alpha=ratio(plan['interface']['candidate_alpha']);beta=ratio(plan['interface']['candidate_beta'])
    improved_log=limb_ratio(sub[roles['B_log_field'][0]])
    original_native_stock=limb_ratio(sub[roles['original_native_improved_stock_comparison_field'][0]])
    amplitude=plus(times(alpha,M),beta)
    amplitude_squared=times(amplitude,amplitude)
    propagated_log=times(times(M,M),improved_log)
    tails=plus(lower,upper)
    if profile=='primary90':
        candidate=times(Fraction(3),plus(plus(amplitude_squared,propagated_log),tails))
        alternate=plus(plus(times(Fraction(3),upper),times(lower,Fraction(3))),plus(times(amplitude_squared,Fraction(3)),times(Fraction(3),propagated_log)))
    else:
        candidate=plus(plus(times(upper,Fraction(3)),times(Fraction(3),lower)),plus(times(propagated_log,Fraction(3)),times(Fraction(3),amplitude_squared)))
        alternate=times(Fraction(3),plus(plus(amplitude_squared,propagated_log),tails))
    require(candidate==alternate, 'Saved-term grouped/expanded exact rational identity')
    require(max(candidate.numerator.bit_length()+original_native_stock.denominator.bit_length(),original_native_stock.numerator.bit_length()+candidate.denominator.bit_length(),candidate.denominator.bit_length()+original_native_stock.denominator.bit_length())<=524288, 'Signed comparison temporary bit frontier')
    difference=candidate-original_native_stock
    require(max(difference.numerator.bit_length(),difference.denominator.bit_length())<=131072, 'Signed comparison reduced bit frontier')
    return {'schema':'candidate-d4-s4-first-stock-squared-L2-limb-bound-v1','profile':profile,'units':'dollars_squared','stock4021_candidate_squared_L2_upper':pair(candidate),'same_profile_original_native_improved_stock_squared_L2_upper':pair(original_native_stock),'candidate_minus_original_native_signed_difference':signed_pair(difference),'candidate_bound_valid_in_scoped_conditional_model':True,'candidate_bound_not_greater_than_original':difference<=0,'comparison_status':'strictly_smaller' if difference<0 else 'equal' if difference==0 else 'larger_valid_scoped_bound','valid_candidate_certificate_does_not_require_improvement':True,'candidate_amplitude':pair(amplitude),'candidate_alpha':pair(alpha),'candidate_beta':pair(beta),'verified_unchanged_raw3542_log_squared_L2':pair(improved_log),'unchanged_projection_tail_terms':{'M':pair(M),'lower_tail':pair(lower),'upper_tail':pair(upper)},'grouped_equals_expanded':True,'old_degree12_alpha_A_B_log_beta_used':False,'guard_moment_tail_series_native_sampler_or_caller_replayed':False,'no_extra100_factor':True,'native_pair_error_or_stock_independence_assumed':False,'financial_G2_price_tolerance_adoption_or_quantum_advantage':False}



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
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256],'Separate base argv0 and launcher/current absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(),'Pinned isolated paths/no ZIP/no site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'Unused output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','candidate_first_stock_L2_execution_authorized','candidate_first_stock_projection_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-d4-s4-candidate-first-stock-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['candidate_first_stock_L2_execution_authorized'] is True,'Own current release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors,'All three current reviews before premises/origins/numbers')
        code_guard(source_raw,ready)
        caches=['research/limitation_program_20261001/__pycache__/'+SOURCE.stem+'.cpython-312'+s+'.pyc' for s in ('','.opt-1','.opt-2')]
        require(ready['existing_current_cache_SHA256']=={} and ready['absent_current_cache_paths']==sorted(caches) and all(not (ROOT/k).exists() and not (ROOT/k).is_symlink() for k in caches),'Exact unused current cache partition')
        inputs={}
        for key,pin in plan['selected_expected_SHA256'].items():
            raw=read_bytes(ROOT/key,pin,records)
            mode=plan['selected_input_modes'][key];require(mode in ('ordinary_json','opaque_bytes','plaintext_AST_only'),'Closed input decode roles')
            inputs[key]=decode(raw) if mode=='ordinary_json' else raw
        native=inputs[plan['runtime_manifest']];origins=loaded_origins(native,records)
        witness=interface_witness(plan,ready,inputs);controls=controls_record(plan)
        code_guard(source_raw,ready);budget(admission=True)
        OUTPUT.mkdir(exist_ok=False);_OUTPUT_ID=[stat8(OUTPUT)[i] for i in (0,1,4,5,6,7)];_OWNS_OUTPUT=True
        files={}
        for name,raw in [('executed_controller.py',source_raw),('executed_adapter.json',plan_raw),('executed_preflight.md',md_raw),('executed_ROOT_READY.json',read_bytes(READY,args.ready_sha256,records))]:files[name]=save(name,raw=raw)
        files['run_started.json']=save('run_started.json',{'created_UTC_ns':time.time_ns(),'PID':os.getpid(),'caps':[CPU,ADMISSION,WALL],'default4300_no_setter':True})
        files['candidate_projection_and_transfer_witness.json']=save('candidate_projection_and_transfer_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,inputs);independent=compose('independent130',plan,inputs)
        files['primary_candidate_first_stock.json']=save('primary_candidate_first_stock.json',primary);files['independent_candidate_first_stock.json']=save('independent_candidate_first_stock.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'no_minimum_or_cross_profile_selection':True,'valid_candidate_bound_accepted_even_if_larger':True,'output_rationals_all_canonical_limbs':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'guard_tail_moment_series_native_sampler_or_caller_called':False,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical32bit-rational-limbs-and-signed-comparison-v1','candidate_alpha':[1,16777216],'candidate_beta':[1,1099511627776],'candidate4021_only':True,'compiled_signed_shift_phase_and_cleanup_open':True,'financial_tolerance_adoption':False}
        files['summary.json']=save('summary.json',summary)
        require(set(files)==set(LEDGER)-{'manifest.json'} and {p.name for p in OUTPUT.iterdir()}==set(files),'Exact preseal12/no failure marker')
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

if __name__ == "__main__":
    main()
