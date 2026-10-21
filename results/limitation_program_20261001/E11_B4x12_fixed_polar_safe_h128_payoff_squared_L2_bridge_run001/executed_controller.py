"""Bounded fixed-polar-safe h1/128 payoff squared-L2 bridge over saved #42 fields.
The same coupling, lambda2^-18, h1/128, M4608 and sqrt128 are inherited unchanged.
Per own profile, gated on both saved all12 booleans: C_J=40(U+eta)+tau and the
G-restricted disjoint LP bound L2SQ=E_s^2+(C_J^2-E_s^2)p, with BASE, L1 and an
outward sqrt128 RMS, under exact rational checks R1-R7. An inherited False or any
failed check seals a negative bridge feasibility record with L2SQ/BASE/L1/RMS None;
no retuning, cross-profile minimum, moment transfer, accuracy policy or advantage.
SOURCE authoring is bound; fresh current SOURCE peer, ROOT review and closed
READY are still mandatory. Current SCI/terminal/manifest/result pins are None.
"""
import argparse
import ast
import ctypes
from ctypes import wintypes
from fractions import Fraction
from importlib.util import cache_from_source
import hashlib
import json
import marshal
from math import gcd, isqrt
import os
from pathlib import Path
import sys
import time
import types
import _pylong
ROOT=Path('C:/Users/prith/quantum_option_pricing')
SOURCE=ROOT/'research/limitation_program_20261001/experiment_e11_b4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_v1.py'
PLAN=ROOT/'.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_INPUT_ADAPTER_run001.json'
MD=ROOT/'.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_PREFLIGHT_run001.md'
READY=ROOT/'.context/E11_B4X12_FIXED_POLAR_SAFE_H128_PAYOFF_L2_ROOT_READY_run001.json'
OUTPUT=ROOT/'results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_payoff_squared_L2_bridge_run001'
LEDGER=['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'fixed_polar_safe_h128_payoff_L2_source_premise_witness.json', 'five_metadata_controls.json', 'primary_fixed_polar_safe_h128_payoff_squared_L2_bridge.json', 'independent_fixed_polar_safe_h128_payoff_squared_L2_bridge.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']
CPU, ADMISSION, WALL=(180,150,600)
_STARTED=None
_OWNS_OUTPUT=False
_OUTPUT_ID=None
CURRENT_FIXED_POLAR_SAFE_PAYOFF_L2_AUTHORING_AND_PROOF_BOUND=True
FUTURE_CURRENT_SCI_OR_RESULT_PINS=None
SQRT_GRID_EXPONENT_FIXED=128


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
    require(CURRENT_FIXED_POLAR_SAFE_PAYOFF_L2_AUTHORING_AND_PROOF_BOUND is True and ready['fixed_polar_safe_h128_payoff_L2_transfer_witness_accepted'] is True and exact(ready['interface'], plan['interface']), 'Current fixed polar-safe payoff-L2 SOURCE and separate READY')
    fixed = {'case': 'B4x12', 'W': 72, 'F': 40, 'profiles': ['primary90', 'independent130'],
             'fixed_lambda': [1, 262144], 'fixed_h_dollars': [1, 128], 'pointwise_kernel_M': 4608, 'radial_pair_count': 30,
             'sqrt_grid_exponent_fixed': 128, 'ideal_band_leading_factor': [1, 1176], 'ideal_band_correction': [1, 963379197],
             'source_full_payoff': 5697, 'native_survival_selector': 5644, 'native_zero_branch': 13,
             'inherited42_conditioning': ['all12_fixed_basket_criterion_passed', 'all12_simultaneous_on_same_fixed_safe_event'],
             'payoff_jump_constant_C_J': '40*(U+eta)+tau',
             'bad_or_mismatch_probability_upper': 'min(1,60*lambda+B_band)',
             'G_restricted_disjoint_LP_combination': 'E_s^2+(C_J^2-E_s^2)*p',
             'payoff_squared_L2_baseline': 'E_s^2+1600*p',
             'payoff_L1_secondary': 'E_s*(1-p)+C_J*p',
             'payoff_RMS': 'outward_fixed_sqrt128(L2SQ)',
             'rational_checks': ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7'],
             'criterion_or_check_failure_seals_negative_with_L2SQ_BASE_L1_RMS_None': True,
             'same_coupling_no_native_or_error_independence': True,
             'no_adaptive_lambda_h_retuning_fallback_or_cross_profile_minimum': True,
             'moment_transfer_estimator_saving_accuracy_policy_G2_physical_or_advantage': False}
    require(exact(plan['interface'], fixed), 'Only the upfront inherited lambda2^-18/h1/128 payoff-L2 bridge')
    pins = plan['selected_expected_SHA256']
    LIMB = {'schema', 'numerator_sign', 'numerator_limbs', 'denominator_limbs'}
    LP_BAD = '2*E_s^2+2*C_J^2*p (Young (a+b)^2 split)'
    # Reviewed #43 prospectus, proof memo, operand-role inventory, independent peer and ROOT conditional review.
    pros = inputs[plan['prospectus43']]; pmd = inputs[plan['prospectus43_MD']]; inv = inputs[plan['inventory43']]; imd = inputs[plan['inventory43_MD']]; peer = inputs[plan['peer43']]; root = inputs[plan['ROOT43']]
    bridge = pros['new_payoff_L2_bridge']; route = pros['upfront_fixed_route']; neg = pros['negative_branch']; pc = pros['proposed_five_metadata_controls']
    require(pros['schema'] == 'e11-B4x12-fixed-polar-safe-h128-payoff-squared-L2-bridge-v1' and pros['scope'] == 43 and pros['metadata_only'] is True
            and pros['scientific_evaluation_performed'] is False and pros['separate_ROOT_and_independent_full_proof_review_required_before_SOURCE_authoring'] is True
            and pros['user_authorized_scope43_after_stop42'] is True and pros['USER_REQUESTED_STOP_CHECKPOINT'] is True and pros['beyond44_SCI_authorized'] is False
            and type(pmd) is bytes and type(imd) is bytes and pros['proof_MD_expected_SHA256'] == pins[plan['prospectus43_MD']]
            and exact(route['lambda'], [1, 262144]) and exact(route['h'], [1, 128]) and route['pointwise_kernel_M'] == 4608 and route['sqrt_grid_exponent'] == 128
            and route['cross_profile_minimum'] is False and exact(route['conditional_on_saved'], {'/all12_fixed_basket_criterion_passed': True, '/all12_simultaneous_on_same_fixed_safe_event': True})
            and bridge['L2SQ_adopted'] == fixed['G_restricted_disjoint_LP_combination'] and bridge['BASE_cross_check'] == fixed['payoff_squared_L2_baseline']
            and bridge['L1_secondary'] == fixed['payoff_L1_secondary'] and bridge['C_J'].startswith(fixed['payoff_jump_constant_C_J'] + ',')
            and bridge['new_Young_factor_or_any_independence_assumed'] is False and bridge['unconditional_smooth_positivepart_support_assumed_40'] is False
            and neg['outcome'] == 'negative_fixed_bridge_feasibility' and neg['positive_outcome'] == 'conditional_payoff_squared_L2_certificate' and neg['fallback_or_retuning'] is False
            and exact(pros['exact13_inclusive_ledger'], LEDGER) and len(pros['rational_checks']) == 7 and [r[:2] for r in pros['rational_checks']] == fixed['rational_checks']
            and all(k in pins and pins[k] == v for k, v in pros['expected_premise_pins'].items()), 'Reviewed #43 prospectus exactly as preregistered')
    require(pc['positive_first'] is True and pc['artificial_metadata_only'] is True and len(plan['controls']) == len(pc['controls']) == 5
            and [c['tag'] for c in plan['controls']] == ['JUMP_CONSTANT', 'PROBABILITY', 'LP_FORM', 'FAILED_CRITERION', 'INDEPENDENCE']
            and all(c['field'] == r['field'] and c['tag'] == r['dedicated_tag'] and r['expected_rejected'] is True and c['field'] in fixed
                    and exact(c['bad'], LP_BAD if r['dedicated_tag'] == 'LP_FORM' else r['mutation']) for c, r in zip(plan['controls'], pc['controls'])),
            'Five dedicated controls, one exact bad value each; LP_FORM fixed to the single Young (a+b)^2 split value')
    require(inv['schema'] == 'e11-B4x12-fixed-polar-safe-h128-payoff-squared-L2-saved-operand-role-inventory-v1' and inv['metadata_only'] is True
            and inv['scientific_evaluation_performed'] is False and inv['limb_decoding_or_rational_assembly_performed'] is False and inv['new_values_evaluated'] is False
            and exact(inv['fixed_lambda'], [1, 262144]) and exact(inv['fixed_h'], [1, 128]) and inv['memo_expected_SHA256'] == pins[plan['inventory43_MD']]
            and inv['prospectus_expected_commitments']['json']['expected_SHA256'] == pins[plan['prospectus43']]
            and inv['ROOT42_expected_commitment']['expected_SHA256'] == pins[plan['ROOT42_result']] and inv['manifest42_expected_commitment']['expected_SHA256'] == pins[plan['manifest42']]
            and inv['summary42_expected_commitment']['expected_SHA256'] == pins[plan['summary42']] and inv['reconciliation42_expected_commitment']['expected_SHA256'] == pins[plan['reconciliation42']]
            and inv['executed_controller42']['expected_SHA256'] == pins[plan['controller42']] and inv['executed_controller42']['input_mode'] == 'plaintext_AST_only',
            'Exact independently prepared saved operand roles; not numeric evidence by themselves')
    require(peer['schema'] == 'e11-B4x12-fixed-polar-safe-h128-payoff-squared-L2-independent-conditional-symbolic-proof-peer-v1' and peer['scope'] == 43
            and peer['passed'] is peer['science_static_passed'] is peer['lifecycle_static_passed'] is True and peer['blockers'] == [] and peer['independent_peer'] is True
            and peer['fixed_polar_safe_h128_payoff_squared_L2_bridge_conditional_proof_accepted'] is True and peer['P9_accepted'] is True and peer['P10_accepted'] is True
            and peer['P9_event_split_L2_L1_statement_with_C_J_40_U_plus_eta_plus_tau_and_LP_combination_accepted'] is True
            and peer['P10_explicit_L2_use_of_run002_pointwise_bound_on_G_accepted'] is True and peer['LP_combination_accepted'] is True and peer['each_partition_step_accepted'] is True
            and peer['five_metadata_controls_judgment']['accepted'] is True and peer['saved_limbs_decoded'] is False
            and peer['SOURCE_READY_SCI_execution_or_result_adoption_authorized_by_this_peer'] is False
            and peer['reviewed_prospectus_JSON_SHA256'] == pins[plan['prospectus43']] and peer['reviewed_proof_MD_SHA256'] == pins[plan['prospectus43_MD']]
            and peer['reviewed_inventory_JSON_SHA256'] == pins[plan['inventory43']], 'Independent #43 peer explicitly accepted P9, P10, each partition step and the LP combination')
    reviewed = root['reviewed_expected_SHA256']
    require(root['schema'] == 'root-e11-fixed-polar-safe-h128-payoff-L2-conditional-proof-review-v1' and root['scope'] == 43
            and root['passed'] is root['science_static_passed'] is root['lifecycle_static_passed'] is True and root['blockers'] == []
            and root['bounded_actual_SOURCE_authoring_permitted'] is True and root['current_SOURCE_peer_ROOT_READY_SCI_or_result_authorized'] is False
            and root['nonauthor_proof_review_claimed'] is False and root['SOURCE_must_gate_on_inherited_booleans_before_decoding_conditional_fields'] is True
            and root['ROOT_confirmed_target_json_a7a68273_selected_by_42_adapter_0caab3ae'] is True and root['pointwise_E_s_only_on_G_mandatory'] is True
            and root['rational_checks_R1_R7_required'] is True and root['negative_branch_seals_13_with_None_no_fallback'] is True
            and root['no_independence_or_conditioning_on_E'] is True and root['no_retuning_grid_or_cross_profile_minimum'] is True
            and root['safe_band_subset'] == 'P(E intersect ideal_band)<=P(ideal_band)' and exact(root['fixed_lambda'], [1, 262144]) and exact(root['fixed_h_dollars'], [1, 128])
            and root['user_authorized_scope43_after_stop42'] is True and root['beyond44_SCI_authorized'] is False
            and root['separate_nonauthor_conditional_peer_expected_SHA256'] == pins[plan['peer43']]
            and all(reviewed[plan[k]] == pins[plan[k]] for k in ('prospectus43', 'prospectus43_MD', 'inventory43', 'inventory43_MD', 'peer43', 'ROOT42_result', 'target'))
            and reviewed[plan['profiles']['independent130']['discount']] == pins[plan['profiles']['independent130']['discount']],
            'ROOT #43 conditional proof review grants bounded SOURCE authoring only')
    # Inherited #42 premises P1-P4 (structural feasibility, h128 mean bridge, its peer and ROOT review).
    r1 = inputs[plan['prospectus001']]; r2 = inputs[plan['prospectus002']]; md1 = inputs[plan['prospectus001_MD']]; md2 = inputs[plan['prospectus002_MD']]; p42 = inputs[plan['peer42']]; c42 = inputs[plan['ROOT42_conditional']]
    require(type(md1) is bytes and type(md2) is bytes and r1['schema'] == 'e11-B4x12-fixed-polar-safe-source-specific-uniform-feasibility-v1' and r1['metadata_only'] is True
            and r1['proof_MD_expected_SHA256'] == pins[plan['prospectus001_MD']] and r2['schema'] == 'e11-B4x12-fixed-polar-safe-h128-source-specific-uniform-mean-bridge-v1'
            and r2['metadata_only'] is True and r2['proof_MD_expected_SHA256'] == pins[plan['prospectus002_MD']]
            and r2['safe_band_subset_inequality'].startswith('P(E intersect ideal_band)<=P(ideal_band)')
            and b'\n## Fixed ideal band\n' in md2 and b'\n## Smooth mean transport only on simultaneous survival\n' in md2
            and p42['schema'] == 'e11-B4x12-fixed-polar-safe-h128-independent-conditional-symbolic-proof-peer-v1' and p42['passed'] is p42['science_static_passed'] is p42['lifecycle_static_passed'] is True
            and p42['blockers'] == [] and p42['independent_peer'] is True and p42['fixed_polar_safe_h128_uniform_mean_bridge_conditional_proof_accepted'] is True
            and p42['reviewed_proof_MD_SHA256'] == pins[plan['prospectus002_MD']] and p42['reviewed_prospective_assessment_SHA256'] == pins[plan['prospectus002']]
            and c42['schema'] == 'root-e11-fixed-polar-safe-h128-conditional-proof-review-v1' and c42['passed'] is True and c42['blockers'] == []
            and c42['safe_band_subset'] == 'P(E intersect ideal_band)<=P(ideal_band)' and c42['separate_nonauthor_conditional_peer_expected_SHA256'] == pins[plan['peer42']],
            'Inherited #42 safe event, band, pointwise smooth transport on simultaneous survival and safe-band subset premises')
    # Sealed #42 outputs, the #42 adapter chain and ROOT saved verification.
    mf = inputs[plan['manifest42']]; sm = inputs[plan['summary42']]; rc = inputs[plan['reconciliation42']]; rv = inputs[plan['ROOT42_result']]; a42 = inputs[plan['adapter42']]; native = inputs[plan['runtime_manifest']]
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['budget_censored'] is False and mf['inclusive_files'] == 13 and mf['fixture_credit'] == 0
            and mf['files']['summary.json'] == pins[plan['summary42']] and mf['files']['same_profile_reconciliation.json'] == pins[plan['reconciliation42']]
            and mf['files']['executed_controller.py'] == pins[plan['controller42']] and mf['files']['executed_adapter.json'] == pins[plan['adapter42']]
            and all(mf['files'][Path(r['profile_file']).name] == pins[r['profile_file']] for r in plan['profiles'].values()), 'Sealed #42 thirteen-file manifest pins every inherited output')
    require(rv['schema'] == 'root-e11-B4x12-fixed-polar-safe-h128-uniform-error-test-saved-verification-v1' and rv['passed'] is rv['completed'] is True and rv['blockers'] == []
            and rv['ROOT_observed_terminal_exit_code'] == 0 and rv['manifest_SHA256'] == pins[plan['manifest42']] and rv['SOURCE_SHA256'] == pins[plan['controller42']]
            and rv['ROOT_READY_expected_SHA256'] == mf['ROOT_READY_expected_SHA256'] and rv['inclusive_owned_files'] == 13
            and rv['full_numeric_profile_records_embedded_in_ROOT_receipt'] is False and rv['fixture_credit'] == 0
            and rv['failed_criterion_conditional_mean_probability_smooth_fields_None_checked'] is True
            and exact(rv['profile_result_files'], sm['profile_result_files']) and exact(rv['profile_outcomes'], sm['profile_outcomes']), 'ROOT saved verification of #42 is typed authority, not re-run')
    require(sm['schema'] == 'e11-fixed-polar-safe-h128-uniform-error-feasibility-reference-summary-v1' and sm['passed'] is sm['completed'] is True and sm['source_full_payoff'] == 5697
            and sm['new_rational_output_encoding'] == 'canonical-nonnegative-rational-base2p32-v1' and [r['profile'] for r in sm['profile_outcomes']] == fixed['profiles']
            and [r['profile'] for r in sm['profile_result_files']] == fixed['profiles']
            and all(r['filename'] == Path(plan['profiles'][r['profile']]['profile_file']).name and r['expected_SHA256'] == pins[plan['profiles'][r['profile']]['profile_file']] for r in sm['profile_result_files'])
            and rc['passed'] is rc['profiles_kept_separate'] is rc['ideal_band_not_conditioned_on_safe_event'] is rc['no_adaptive_lambda_h_fallback_or_cross_profile_selection'] is True,
            'Saved #42 summary and same-profile reconciliation')
    chain = [plan['target'], plan['ir_semantics'], plan['audit_code']] + [r['discount'] for r in plan['profiles'].values()]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs']) == 2842 and all(native['frozen_inputs'][k] == pins[k] for k in chain)
            and a42['schema'] == 'e11-B4x12-fixed-polar-safe-h128-uniform-error-test-input-adapter-v1' and a42['target'] == plan['target'] and a42['runtime_manifest'] == plan['runtime_manifest']
            and a42['selected_expected_SHA256'][plan['target']] == pins[plan['target']] == mf['selected_expected_SHA256'][plan['target']]
            and a42['selected_expected_SHA256'][plan['runtime_manifest']] == pins[plan['runtime_manifest']]
            and all(a42['profiles'][p]['discount'] == r['discount'] and a42['profiles'][p]['discount_U_field'] == r['discount_U_field'] and a42['profiles'][p]['discount_eta_field'] == r['discount_eta_field']
                    and a42['selected_expected_SHA256'][r['discount']] == pins[r['discount']] == mf['selected_expected_SHA256'][r['discount']] for p, r in plan['profiles'].items()),
            'Target, IR semantics, A02 audit code and both own discount archives keep their own original pins through the #42 adapter chain')
    # Executed #42 controller as plaintext authority (lines 274, 291, 305, 314; shared native graph, primary90 run).
    ctl = inputs[plan['controller42']]; lines = ctl.decode('utf-8').split('\n')
    require(type(ctl) is bytes and set(plan['controller42_pinned_line_SHA256']) == {'274', '291', '305', '314'}
            and exact(plan['controller42_pinned_line_SHA256'], {n: r['line_text_SHA256'] for n, r in inv['executed_controller42']['pinned_lines'].items()})
            and all(hashlib.sha256(lines[int(n) - 1].encode('utf-8')).hexdigest() == s for n, s in plan['controller42_pinned_line_SHA256'].items())
            and "exact(nodes[5697],{'op':'select','args':[5644,5696,13],'params':{},'out':[5697]})" in lines[290]
            and "if profile=='primary90':require(kernel['whole_clipped_integer_domain_covered']" in lines[304]
            and "if profile=='primary90':require(dc['actual_discount_literal']==nodes[5696]['params']['c']" in lines[313]
            and len([n for n in ast.parse(ctl).body if isinstance(n, ast.FunctionDef)]) == 31, 'Executed #42 controller lines 274/291/305/314 as saved authority')
    # Native graph bound directly in target.json (not by controller line 291 alone).
    target = inputs[plan['target']]; nodes = {v: row for row in target['nodes'] for v in row['out']}
    baskets = [5576 + 4 * i for i in range(12)]; tests = [5621 + 2 * i for i in range(11)]; picks = [5622 + 2 * i for i in range(11)]
    require(exact([target['width'], target['fraction_bits']], [72, 40]) and exact(target['outputs'], {'Y': 5697})
            and exact(nodes[13], {'op': 'const', 'args': [], 'params': {'value': 0}, 'out': [13]})
            and exact(nodes[5643], {'op': 'const', 'args': [], 'params': {'value': 153931627888640}, 'out': [5643]})
            and exact(nodes[5644], {'op': 'lt', 'args': [5642, 5643], 'params': {}, 'out': [5644]})
            and exact(nodes[5692], {'op': 'cmul', 'args': [5691], 'params': {'c': 22906492245}, 'out': [5692]})
            and exact(nodes[5693], {'op': 'const', 'args': [], 'params': {'value': 109951162777600}, 'out': [5693]})
            and exact(nodes[5694], {'op': 'sub', 'args': [5692, 5693], 'params': {}, 'out': [5694]})
            and exact(nodes[5695], {'op': 'positive', 'args': [5694], 'params': {}, 'out': [5695]})
            and exact(nodes[5696], {'op': 'cmul', 'args': [5695], 'params': {'c': 1067016148260}, 'out': [5696]})
            and exact(nodes[5697], {'op': 'select', 'args': [5644, 5696, 13], 'params': {}, 'out': [5697]}), 'Zero branch 13, strict-140Q survival 5644 and payoff chain 5692-5697 in target.json')
    stocks = {}
    for b in baskets:
        total = nodes[b - 1]; left = nodes[b - 3]; right = nodes[b - 2]
        require(exact(nodes[b], {'op': 'cmul', 'args': [b - 1], 'params': {'c': 274877906944}, 'out': [b]}) and total['op'] == left['op'] == right['op'] == 'add'
                and sorted(total['args']) == [b - 3, b - 2] and len(left['args']) == len(right['args']) == 2, 'Each of twelve baskets is floor(sum4*2^38/Q), a quarter of four stocks')
        stocks[b] = sorted(left['args'] + right['args'])
    for t, s in zip(tests, picks):
        first, second = nodes[t]['args']
        require(exact(nodes[t], {'op': 'lt', 'args': [first, second], 'params': {}, 'out': [t]}) and exact(nodes[s], {'op': 'select', 'args': [t, second, first], 'params': {}, 'out': [s]})
                and first < t and second < t, 'Each tree node is max(a,b)=select(lt(a,b),b,a)')
    require(picks[-1] == 5642 and sorted(v for t in tests for v in nodes[t]['args']) == sorted(baskets + picks[:-1]), 'Binary max tree over exactly the twelve baskets, rooted at 5642')
    all48 = sorted(v for b in baskets for v in stocks[b]); pending = [5691]; leaves = []
    while pending:
        v = pending.pop()
        if 5645 <= v <= 5691:
            require(nodes[v]['op'] == 'add' and len(nodes[v]['args']) == 2, 'Whole-stock sum tree uses additions only')
            pending.extend(nodes[v]['args'])
        else:
            leaves.append(v)
    require(len(set(all48)) == 48 and sorted(leaves) == all48, 'Average node 5692 sums exactly the same 48 basket stocks once each')
    irl = inputs[plan['ir_semantics']].decode('utf-8').split('\n'); aud = inputs[plan['audit_code']].decode('utf-8').split('\n')
    require(type(inputs[plan['ir_semantics']]) is bytes and type(inputs[plan['audit_code']]) is bytes
            and "def maximum(self,a,b):return self.select(self.lt(a,b),b,a)" in irl[49] and "elif op=='const':result=[p['value']]" in irl[108]
            and "elif op=='cmul':result=[(v[0]*p['c'])>>f]" in irl[112] and "elif op=='lt':result=[int(v[0]<v[1])]" in irl[113]
            and "elif op=='select':result=[raw[1] if raw[0]&1 else raw[2]]" in irl[114] and "elif op=='positive':result=[max(v[0],0)]" in irl[115],
            'IR semantics: select returns arg1 iff flag&1, else the zero branch; strict lt; floor cmul')
    require('Q, N, W = 1 << 40, 1 << 32, 72' in aud[49] and 'c_average, c_discount = support["actual_average_literal"], support["actual_discount_literal"]' in aud[3061]
            and 'and declared["actual_discount_literal"] == c_discount,' in aud[3064] and 'true_discount = endpoints(mp.iv.exp(outward(mp, Fraction(-3, 100))))' in aud[3073]
            and 'discount_error = max(abs(Fraction(c_discount, Q) - v) for v in true_discount)' in aud[3079]
            and 'independent_true_discount_enclosure=[encode(v) for v in true_discount],' in aud[3143] and 'independent_discount_literal_error_upper=encode(discount_error),' in aud[3144],
            'A02 audit joins the independent130 enclosure and eta to the declared primary support literal by an endpoint maximum')
    literal = Fraction(nodes[5696]['params']['c'], 1 << 40)
    # Own profiles: provenance and shape only; the inherited booleans gate every conditional-field access.
    OPS = {'E_s': '/conditional_smooth_survival_payoff_error_upper', 'p': '/conditional_mismatch_probability_upper', 'saved_mean': '/conditional_full_payoff_mean_bias_upper',
           'U': '/components/own_discount_U', 'eta': '/components/own_discount_literal_error_eta', 'tau': '/components/native_discount_floor_tau',
           'avg': '/components/average_pointwise_error_upper', 'polar_bad': '/components/polar_bad_event_probability_upper', 'B_band': '/components/fixed_ideal_band_probability_upper'}
    COND = {'E_s': 'conditional_smooth_survival_payoff_error_upper', 'p': 'conditional_mismatch_probability_upper', 'mean': 'conditional_full_payoff_mean_bias_upper'}
    SIX = ['own_discount_U', 'own_discount_literal_error_eta', 'native_discount_floor_tau', 'average_pointwise_error_upper', 'polar_bad_event_probability_upper', 'fixed_ideal_band_probability_upper', 'fixed_lambda', 'fixed_h']
    own = {}; discounts = {}
    for profile, roles in plan['profiles'].items():
        rec = inputs[roles['profile_file']]; row = inv['profiles'][profile]; ops = row['certificate_operands']; archive = inputs[roles['discount']]
        dc = archive['cases']['B4x12'] if profile == 'primary90' else archive['B4x12']
        require(row['profile_file'] == roles['profile_file'] and row['profile_file_expected_SHA256'] == pins[roles['profile_file']]
                and all(ops[k]['JSON_pointer'] == v and ops[k]['path'] == roles['profile_file'] for k, v in OPS.items()), 'Inventory operand pointers are the own saved #42 fields')
        require(rec['schema'] == 'e11-B4x12-fixed-polar-safe-h128-pointwise-feasibility-limb-profile-v1' and rec['profile'] == profile
                and exact(rec['fixed_lambda'], [1, 262144]) and exact(rec['fixed_h_dollars'], [1, 128]) and rec['own_pointwise_date_rows'] == 12 and len(rec['date_rows']) == 12
                and type(rec['all12_fixed_basket_criterion_passed']) is bool and type(rec['all12_simultaneous_on_same_fixed_safe_event']) is bool
                and rec['all12_fixed_basket_criterion_passed'] == all(r['fixed_basket_criterion_passed'] is True for r in rec['date_rows'])
                and rec['ideal_band_factorization_conditioned_on_safe_event'] is False and rec['P_safe_intersect_band_bounded_by_unconditional_ideal_band'] is True
                and rec['native_errors_or_stocks_independence_assumed'] is False and rec['native_clipping_inactive_assumed'] is False
                and rec['adaptive_lambda_h_or_retry_or_cross_profile_selection'] is False
                and all(type(rec['components'][k]) is dict and set(rec['components'][k]) == LIMB for k in SIX), 'Own saved #42 profile record shape and typed flags')
        require([r['source_basket'] for r in rec['date_rows']] == baskets and all(sorted(r['source_stocks']) == stocks[r['source_basket']] for r in rec['date_rows'])
                and exact(rec['components']['fixed_lambda'], pair(Fraction(1, 262144))) and exact(rec['components']['fixed_h'], pair(Fraction(1, 128)))
                and exact(rec['components']['native_discount_floor_tau'], pair(Fraction(1, 1 << 40))), 'Own twelve saved date rows join the target baskets; fixed lambda, h and Q40 floor')
        out = [r for r in sm['profile_outcomes'] if r['profile'] == profile]
        require(len(out) == 1 and out[0]['all12_fixed_basket_criterion_passed'] is rec['all12_fixed_basket_criterion_passed'] and out[0]['outcome'] == rec['outcome']
                and out[0]['full_payoff_mean_certificate_adopted'] is rec['full_payoff_mean_certificate_adopted'], 'Summary and own profile outcomes agree')
        enclosure = dc[roles['discount_U_field']]; eta_pair = dc[roles['discount_eta_field']]
        require(type(enclosure) is list and len(enclosure) == 2 and exact(pair(ratio(enclosure[1])), rec['components']['own_discount_U'])
                and exact(pair(ratio(eta_pair)), rec['components']['own_discount_literal_error_eta']), 'Own saved U and eta are the own archived enclosure upper and literal error')
        lower = ratio(enclosure[0]); upper = ratio(enclosure[1]); eta = ratio(eta_pair)
        require(lower <= upper and eta == max(abs(plus(literal, -lower)), abs(plus(literal, -upper))), 'Own eta is the endpoint maximum of |D_lit-L|,|D_lit-U|, hence eta>=|D_lit-d| for d in [L,U]')
        if profile == 'primary90':
            require(dc['actual_discount_literal'] == nodes[5696]['params']['c'] and dc['positive_part_is_1_Lipschitz_and_same_exact_strike'] is True, 'Primary archive literal is target node 5696')
        discounts[profile] = {'archive_path': roles['discount'], 'archive_expected_SHA256': pins[roles['discount']], 'enclosure_field': roles['discount_U_field'], 'eta_field': roles['discount_eta_field'],
                              'D_lit_Q40_word': nodes[5696]['params']['c'], 'literal_join': 'target node 5696 and controller42 line 314' if profile == 'primary90' else 'target node 5696 and A02 audit lines 3062-3080/3144-3145',
                              'saved42_U_equals_archived_enclosure_upper': True, 'saved42_eta_equals_archived_eta': True, 'archived_eta_equals_endpoint_maximum_against_D_lit': True,
                              'eta_ge_abs_D_lit_minus_d_since_d_in_own_outward_enclosure': True}
        inherited = rec['all12_fixed_basket_criterion_passed'] is True and rec['all12_simultaneous_on_same_fixed_safe_event'] is True
        cond = None
        if inherited:
            cond = {k: rec[v] for k, v in COND.items()}
            require(all(type(v) is dict and set(v) == LIMB for v in cond.values()), 'Saved conditional fields present only after both inherited booleans')
        elif rec['all12_fixed_basket_criterion_passed'] is False:
            require(all(rec[v] is None for v in COND.values()), 'Saved #42 None branch shape exact')
        own[profile] = {'inherited_criterion': rec['all12_fixed_basket_criterion_passed'], 'inherited_simultaneous': rec['all12_simultaneous_on_same_fixed_safe_event'],
                        'conditional': cond, 'components': {k: rec['components'][k] for k in SIX},
                        'profile_file': {'filename': Path(roles['profile_file']).name, 'expected_SHA256': pins[roles['profile_file']]}}
    witness = {'schema': 'e11-B4x12-fixed-polar-safe-h128-payoff-L2-source-premise-witness-v1', 'passed': True, 'accepted_interface': fixed,
               'inherited42_SOURCE_SHA256': pins[plan['controller42']], 'inherited42_manifest_SHA256': pins[plan['manifest42']], 'inherited42_ROOT_receipt_SHA256': pins[plan['ROOT42_result']],
               'inherited42_adapter_SHA256': pins[plan['adapter42']], 'inherited42_profile_files': {p: own[p]['profile_file'] for p in own}, 'inherited42_profile_outcomes': sm['profile_outcomes'],
               'inherited42_operand_JSON_pointers': OPS, 'controller42_pinned_line_SHA256': plan['controller42_pinned_line_SHA256'],
               'target_expected_SHA256': pins[plan['target']], 'ir_semantics_expected_SHA256': pins[plan['ir_semantics']], 'A02_audit_code_expected_SHA256': pins[plan['audit_code']],
               'target_native_graph': {'zero_branch_node13_const': 0, 'barrier_node5643_const_140Q': 153931627888640, 'survival_node5644': 'lt(5642,5643)',
                                       'basket_nodes': baskets, 'basket_cmul_c_2p38': 274877906944, 'max_tree_lt_nodes': tests, 'max_tree_select_nodes': picks,
                                       'basket_stock_nodes': [stocks[b] for b in baskets], 'sum48_tree_root': 5691, 'average_node5692_c': 22906492245,
                                       'strike_node5693_const_100Q': 109951162777600, 'discount_node5696_c': 1067016148260, 'payoff_node5697': 'select(5644,5696,13)'},
               'own_discount_archive_bindings': discounts,
               'native_payoff_5697_select_5644_5696_13_bound_in_target': True, 'twelve_basket_max_tree_bound_in_target': True,
               'partition_G_Z_M_Ec_disjoint_exhaustive': True, 'P9_event_split_C_J_LP_accepted': True, 'P10_G_restricted_pointwise_E_s_accepted': True,
               'P11_continuous_B4_second_moment_missing_no_transfer': True, 'safe_band_subset_unconditional': True,
               'shared_native_graph_lines_305_314_apply_to_both_profiles': True, 'native_stock_nonnegativity_line305_used_on_G_and_B': True,
               'conditional_fields_decoded_only_after_both_inherited_booleans_true': True, 'LP_FORM_single_exact_bad_value': LP_BAD,
               'unselected_smooth_positive_part_bounded_by_40_assumed': False, 'native_error_safe_event_or_band_independence_assumed': False,
               'candidate_pricepolicy_estimator_G2_physical_or_advantage_excluded': True}
    return witness, own

def outward_fixed_sqrt128(value):
    budget()
    require(type(value) is Fraction and value>=0 and max(value.numerator.bit_length(),value.denominator.bit_length())<=131072 and type(SQRT_GRID_EXPONENT_FIXED) is int and SQRT_GRID_EXPONENT_FIXED==128, 'Only the upfront sqrt128 grid and inherited reduced frontier')
    require(type(isqrt) is types.BuiltinFunctionType and isqrt is sys.modules['math'].isqrt, 'Exact imported standard integer-sqrt identity')
    n,d=value.numerator,value.denominator
    require(n.bit_length()+256<=524288, 'Temporary bound before sqrt-grid numerator shift')
    shifted=n<<256;quotient=shifted//d;k=isqrt(quotient)
    require(2*(k+1).bit_length()+d.bit_length()<=524288, 'Square-times-denominator frontier before all order products')
    square_product=k*k*d;next_square_product=(k+1)*(k+1)*d
    require(square_product<=shifted<next_square_product, 'Exact floor sqrt of shifted rational without floating square root')
    ceiling=k+(1 if square_product<shifted else 0)
    require(ceiling*ceiling*d>=shifted and (ceiling==0 or (ceiling-1)*(ceiling-1)*d<shifted), 'Exact outward ceiling/order and strict sqrt-grid gap including zero')
    upper=Fraction(ceiling,1<<128)
    require(max(upper.numerator.bit_length(),upper.denominator.bit_length())<=131072, 'Canonical output frontier unchanged, no cap widening')
    return upper,{'schema':'e11-fixed-sqrt128-outward-operand-witness-v1','grid_exponent':128,'input_was_zero':n==0,'shifted_rational_square_was_exact':square_product==shifted,'outward_order_and_strict_sqrt_grid_gap_passed':True,'temporary_bit_frontier_unchanged':524288,'reduced_bit_frontier_unchanged':131072,'adaptive_grid_or_float_square_root_used':False}

def compose(profile, plan, own):
    require(profile in ('primary90', 'independent130') and exact(plan['interface']['fixed_lambda'], [1, 262144]) and exact(plan['interface']['fixed_h_dollars'], [1, 128])
            and plan['interface']['payoff_jump_constant_C_J'] == '40*(U+eta)+tau' and plan['interface']['G_restricted_disjoint_LP_combination'] == 'E_s^2+(C_J^2-E_s^2)*p',
            'Only the fixed preselected per-profile payoff-L2 bridge')
    value = own[profile]; c = {k: limb_ratio(v) for k, v in value['components'].items()}
    lam = Fraction(1, 262144); h = Fraction(1, 128); tau = c['native_discount_floor_tau']
    require(c['fixed_lambda'] == lam and c['fixed_h'] == h and tau == Fraction(1, 1099511627776), 'Saved fixed units unchanged')
    U = c['own_discount_U']; eta = c['own_discount_literal_error_eta']; avg = c['average_pointwise_error_upper']
    bad = c['polar_bad_event_probability_upper']; band = c['fixed_ideal_band_probability_upper']
    C_J = plus(times(Fraction(40), plus(U, eta)), tau)
    inherited = value['inherited_criterion'] is True and value['inherited_simultaneous'] is True
    checks = {k: None for k in ('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7')}
    E_s = p = mean = L2SQ = BASE = L1 = RMS = rms_witness = None
    if inherited:
        E_s = limb_ratio(value['conditional']['E_s']); p = limb_ratio(value['conditional']['p']); mean = limb_ratio(value['conditional']['mean'])
        checks['R1'] = E_s == plus(plus(times(U, avg), times(Fraction(40), eta)), tau)
        checks['R2'] = bad == times(Fraction(60), lam) and band == times(Fraction(1, 1176), plus(Fraction(1), Fraction(1, 963379197))) and p == min(Fraction(1), plus(bad, band))
        checks['R3'] = mean == plus(E_s, times(Fraction(40), p))
        checks['R4'] = E_s <= C_J <= Fraction(40)
        if all(checks[k] is True for k in ('R1', 'R2', 'R3', 'R4')):
            q = plus(Fraction(1), -p)
            ES2 = times(E_s, E_s); CJ2 = times(C_J, C_J)
            l2 = plus(times(ES2, q), times(CJ2, p))
            base = plus(ES2, times(Fraction(1600), p))
            l1 = plus(times(E_s, q), times(C_J, p))
            checks['R5'] = l2 <= base; checks['R6'] = l2 <= CJ2; checks['R7'] = l1 <= mean
    passed = inherited and all(v is True for v in checks.values())
    if passed:
        L2SQ = l2; BASE = base; L1 = l1; RMS, rms_witness = outward_fixed_sqrt128(L2SQ)
    components = {'fixed_lambda': lam, 'fixed_h': h, 'own_discount_U': U, 'own_discount_literal_error_eta': eta, 'native_discount_floor_tau': tau,
                  'average_pointwise_error_upper': avg, 'polar_bad_event_probability_upper': bad, 'fixed_ideal_band_probability_upper': band, 'payoff_jump_constant_C_J': C_J}
    return {'schema': 'e11-B4x12-fixed-polar-safe-h128-payoff-squared-L2-bridge-limb-profile-v1', 'profile': profile,
            'fixed_lambda': [1, 262144], 'fixed_h_dollars': [1, 128], 'inherited42_profile_file': value['profile_file'],
            'inherited42_all12_fixed_basket_criterion_passed': value['inherited_criterion'], 'inherited42_all12_simultaneous_on_same_fixed_safe_event': value['inherited_simultaneous'],
            'conditional_fields_decoded_only_after_both_inherited_booleans_true': True,
            'components': {k: pair(v) for k, v in components.items()},
            'inherited42_conditional_smooth_survival_payoff_error_upper': pair(E_s) if E_s is not None else None,
            'inherited42_conditional_mismatch_probability_upper': pair(p) if p is not None else None,
            'inherited42_conditional_full_payoff_mean_bias_upper': pair(mean) if mean is not None else None,
            'formulas': {'C_J': '40*(U+eta)+tau', 'L2SQ': 'E_s^2*(1-p)+C_J^2*p == E_s^2+(C_J^2-E_s^2)*p', 'BASE': 'E_s^2+1600*p', 'L1': 'E_s*(1-p)+C_J*p', 'RMS': 'outward_fixed_sqrt128(L2SQ)'},
            'rational_checks': checks, 'R5_R7_None_unless_R1_R4_all_true': True, 'all_rational_checks_passed': passed,
            'outcome': 'conditional_payoff_squared_L2_certificate' if passed else 'negative_fixed_bridge_feasibility',
            'payoff_squared_L2_upper_L2SQ': pair(L2SQ) if passed else None, 'payoff_squared_L2_baseline_BASE': pair(BASE) if passed else None,
            'payoff_L1_upper': pair(L1) if passed else None, 'payoff_RMS_sqrt128_upper': pair(RMS) if passed else None, 'payoff_RMS_sqrt128_witness': rms_witness,
            'payoff_squared_L2_certificate_adopted': passed, 'LP_relaxation_exact_maximum_not_sharpest_bound': True, 'G_restricted_pointwise_E_s_only': True,
            'unselected_smooth_positive_part_bounded_by_40_assumed': False, 'Young_or_a_plus_b_squared_split_used': False,
            'native_errors_safe_event_or_band_independence_assumed': False, 'cross_profile_minimum_or_selection': False, 'adaptive_lambda_h_retuning_or_fallback': False,
            'moment_or_variance_transfer_claimed': False, 'estimator_saving_claimed': False, 'accuracy_policy_adopted': False,
            'actual_bias_price_policy_G2_physical_or_advantage': False}

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
    require(CURRENT_FIXED_POLAR_SAFE_PAYOFF_L2_AUTHORING_AND_PROOF_BOUND is True, 'Dormant parent pins must be completed before own current ROOT release')
    try:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ready-sha256',required=True);args=parser.parse_args()
        base=Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True)==ROOT and Path(__file__).resolve(strict=True)==SOURCE,'Exact isolated default4300')
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256],'Separate original base argv0/venv and exact current absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(),'Pinned isolated paths/no ZIP/no site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'Unused own output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','fixed_polar_safe_h128_payoff_L2_execution_authorized','fixed_polar_safe_h128_payoff_L2_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-fixed-polar-safe-h128-payoff-L2-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['fixed_polar_safe_h128_payoff_L2_execution_authorized'] is True,'Own current payoff-L2 bridge release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['fixed_polar_safe_h128_payoff_L2_transfer_witness_accepted'] is True and review['event_split_LP_payoff_L2_bridge_P9_P10_accepted'] is True and review['criterion_or_check_failure_is_sealed_negative_bridge_feasibility'] is True and review['saved42_typed_projection_exact_against_ROOT42_receipt'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        files['fixed_polar_safe_h128_payoff_L2_source_premise_witness.json']=save('fixed_polar_safe_h128_payoff_L2_source_premise_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_fixed_polar_safe_h128_payoff_squared_L2_bridge.json']=save('primary_fixed_polar_safe_h128_payoff_squared_L2_bridge.json',primary)
        files['independent_fixed_polar_safe_h128_payoff_squared_L2_bridge.json']=save('independent_fixed_polar_safe_h128_payoff_squared_L2_bridge.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed': True, 'profiles_kept_separate': True, 'fixed_lambda_h_inherited_unchanged': True, 'no_cross_profile_minimum_or_selection': True, 'negative_branch_keeps_sealed_records_with_L2SQ_BASE_L1_RMS_None': True, 'G_restricted_disjoint_LP_combination_only': True, 'ideal_band_not_conditioned_on_safe_event': True, 'no_moment_transfer_estimator_saving_or_accuracy_policy': True, 'no_price_policy_estimator_G2_physical_or_advantage_adoption': True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        owned_guard()
        summary={'schema':'e11-fixed-polar-safe-h128-payoff-squared-L2-bridge-reference-summary-v1','passed':True,'completed':True,'completed_fixed_payoff_L2_bridge':True,'profile_result_files':[{'filename':name,'expected_SHA256':files[name],'bytes':(OUTPUT/name).stat().st_size,'profile':profile} for profile,name in [('primary90','primary_fixed_polar_safe_h128_payoff_squared_L2_bridge.json'),('independent130','independent_fixed_polar_safe_h128_payoff_squared_L2_bridge.json')]],'profile_outcomes':[{'profile':row['profile'],'inherited42_all12_fixed_basket_criterion_passed':row['inherited42_all12_fixed_basket_criterion_passed'],'inherited42_all12_simultaneous_on_same_fixed_safe_event':row['inherited42_all12_simultaneous_on_same_fixed_safe_event'],'all_rational_checks_passed':row['all_rational_checks_passed'],'outcome':row['outcome'],'payoff_squared_L2_certificate_adopted':row['payoff_squared_L2_certificate_adopted']} for row in (primary,independent)],'source_full_payoff':5697,'inherited42_manifest_SHA256':plan['selected_expected_SHA256'][plan['manifest42']],'inherited42_ROOT_receipt_SHA256':plan['selected_expected_SHA256'][plan['ROOT42_result']],'controls_file':{'filename':'five_metadata_controls.json','expected_SHA256':files['five_metadata_controls.json']},'witness_file':{'filename':'fixed_polar_safe_h128_payoff_L2_source_premise_witness.json','expected_SHA256':files['fixed_polar_safe_h128_payoff_L2_source_premise_witness.json']},'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','negative_bridge_branch_is_feasibility_not_scientific_crash':True,'moment_transfer_or_estimator_saving_claimed':False,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'accuracy_policy_estimator_physical_G2_or_advantage_results':None}
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

if __name__=='__main__':
    main()
