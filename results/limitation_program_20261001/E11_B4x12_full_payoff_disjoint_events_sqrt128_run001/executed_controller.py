"""DISABLED original5697 full-payoff disjoint-event transfer with upfront outward sqrt128.
ROOT proof/body review, both verified children and exact current SOURCE release remain required.
No SCI authorization, current numerical outcomes or financial policy/G2/advantage credit.
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

ROOT = Path('C:/Users/prith/quantum_option_pricing')
SOURCE = ROOT/'research/limitation_program_20261001/experiment_e11_b4x12_full_payoff_disjoint_events_sqrt128_v1.py'
PLAN = ROOT/'.context/E11_B4X12_FULL_PAYOFF_DISJOINT_EVENTS_SQRT128_INPUT_ADAPTER_run001.json'
MD = ROOT/'.context/E11_B4X12_FULL_PAYOFF_DISJOINT_EVENTS_SQRT128_PREFLIGHT_run001.md'
READY = ROOT/'.context/E11_B4X12_FULL_PAYOFF_DISJOINT_EVENTS_SQRT128_ROOT_READY_run001.json'
OUTPUT = ROOT/'results/limitation_program_20261001/E11_B4x12_full_payoff_disjoint_events_sqrt128_run001'
LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'original_full_payoff_disjoint_event_source_witness.json', 'five_metadata_controls.json', 'primary_full_payoff_squared_L2_and_mean_bias.json', 'independent_full_payoff_squared_L2_and_mean_bias.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']
CPU, ADMISSION, WALL = (180,150,600)
_STARTED = None
_OWNS_OUTPUT = False
_OUTPUT_ID = None
# Upfront new numeric recipe: S128(x)=ceil(sqrt(x)*2^128)/2^128.
# Both verified child pins remain unbound in this readable disabled DRAFT.
CURRENT_VERIFIED_DISCOUNT_AND_BARRIER_PARENTS_BOUND = True
DISCOUNT_PARENT_ROOT_EXPECTED_SHA256 = '19ffeaa7e0d71e39381f0f8a5372a2cfd1a4de04c07471af2ccfbc0cef364b27'
DISCOUNT_PARENT_MANIFEST_EXPECTED_SHA256 = '855e6e3fbafce6312716b587b40d8c7771629b333b4a08f89da3ec1d591f449e'
BARRIER_PARENT_ROOT_EXPECTED_SHA256 = 'ad14334d3ef89c73d22e6cc76381f01f779b55e7a1157b4e6ab934f51c4c626d'
BARRIER_PARENT_MANIFEST_EXPECTED_SHA256 = '86a5a096ddaa908d79844fa32935db03e4825307fe31fa850d3f36ccac06f9cb'
SQRT_GRID_EXPONENT_FIXED = 128


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
    require(CURRENT_VERIFIED_DISCOUNT_AND_BARRIER_PARENTS_BOUND is True, 'Disabled until exact both saved-verified child authorities and current release are bound')
    fixed={'case': 'B4x12', 'W': 72, 'F': 40, 'source_full_payoff': 5697, 'source_strict_survival_flag': 5644, 'source_discount': 5696, 'source_zero': 13, 'surviving_payoff_upper_dollars': [40, 1], 'mismatch_squared_payoff_upper_dollars_squared': [1600, 1], 'sqrt_grid_exponent_fixed': 128, 'profiles': ['primary90', 'independent130'], 'own_profile_rows': 2, 'quantity': 'original_full_payoff_squared_L2_and_mean_bias_upper', 'units': {'squared_L2': 'dollars_squared', 'mean_bias_upper': 'dollars'}, 'same_coupling_disjoint_event_not_independence': True, 'unconditional_continuous_payoff_bounded_support_assumed': False, 'adaptive_sqrt_grid_cross_profile_minimum_or_extra_Young': False, 'price_policy_G2_candidate_or_quantum_advantage': False}
    require(ready['full_payoff_disjoint_event_transfer_witness_accepted'] is True and exact(plan['interface'],fixed) and exact(ready['interface'],fixed), 'One fixed original5697 disjoint-event/sqrt128 contract')
    expected_parents={'discount':(DISCOUNT_PARENT_ROOT_EXPECTED_SHA256,DISCOUNT_PARENT_MANIFEST_EXPECTED_SHA256),'barrier':(BARRIER_PARENT_ROOT_EXPECTED_SHA256,BARRIER_PARENT_MANIFEST_EXPECTED_SHA256)}
    child_witness={};child_mf={}
    for child,(root_pin,mf_pin) in expected_parents.items():
        roles=plan['verified_children'][child];root_key=roles['ROOT'];mf_key=roles['manifest'];facts=roles['ROOT_metadata_facts']
        require(type(root_pin) is type(mf_pin) is str and plan['selected_expected_SHA256'][root_key]==root_pin and plan['selected_expected_SHA256'][mf_key]==mf_pin and type(inputs[root_key]) is bytes and plan['selected_input_modes'][root_key]=='plain_text_only' and roles['ROOT_factual_projection_exact_against_expected_bytes'] is True, 'Externally pinned complete child ROOT/MF with typed facts, never inherited release')
        require(facts['passed'] is facts['completed'] is True and facts['blockers']==[] and type(facts['ROOT_observed_terminal_exit_code']) is int and facts['ROOT_observed_terminal_exit_code']==0 and facts['manifest_SHA256']==mf_pin and facts['SOURCE_SHA256']==roles['SOURCE_SHA256'] and type(facts['completed_own_numeric_rows']) is int and facts['completed_own_numeric_rows']==2 and facts['financial_price_policy_G2_or_quantum_advantage'] is False and type(facts['fixture_credit']) is int and facts['fixture_credit']==0, 'Two completed own physical child rows only')
        mf=inputs[mf_key];wk=roles['witness']
        require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['budget_censored'] is False and type(mf['inclusive_files']) is int and mf['inclusive_files']==13 and set(mf['files'])==set(roles['exact13_inclusive_ledger'])-{'manifest.json'} and mf['files'][Path(wk).name]==plan['selected_expected_SHA256'][wk], 'Exact sealed child13 and its expected witness membership')
        child_mf[child]=mf;child_witness[child]=inputs[wk]
    dw=child_witness['discount'];bw=child_witness['barrier']
    require(dw['schema']=='e11-B4x12-discount-after-positivepart-common-coupling-witness-v1' and dw['passed'] is dw['one_new_cmul_Q40_floor_paid'] is dw['true_discount_same_exp_minus3_over100'] is dw['coefficient_error_charged_only_to_bounded_native_positive_part'] is dw['continuous_positive_part_has_no_bounded_support_assumption'] is dw['same_coupling_pathwise_fixed_Young_no_independence'] is True and dw['source_discount']==5696 and dw['source_positive_part']==5695, 'Verified original discounted positive-part same coupling, no continuous unconditional support')
    require(bw['schema']=='e11-B4x12-barrier-common94-fixed-h1-dyadic256-source-witness-v1' and bw['passed'] is bw['shared_first_common94_once_in_all48'] is bw['ideal_unclipped_common_factor_only'] is bw['dependence_safe_union_and_squared_error_Markov'] is bw['maximum_adds_no_floor'] is bw['basket_floor_already_paid'] is True and bw['native_clipped_stock_factorization_claimed'] is bw['stock_date_native_or_error_independence_assumed'] is False and bw['source_max']==5642 and bw['source_strict_survival_flag']==5644 and bw['accepted_joint_law_witness']['ideal_only'] is True and bw['accepted_joint_law_witness']['digital_or_error_independence'] is False, 'Verified same-reference strict indicator mismatch, not native factorization')
    original_proof=inputs[plan['historical_prospectus']]
    require(original_proof['schema']=='e11-b4x12-full-payoff-disjoint-events-prospective-plan-v1' and original_proof['metadata_only'] is True and original_proof['scientific_evaluation_performed'] is original_proof['SOURCE_or_SCI_or_saved_utility_authorized'] is False and original_proof['numeric_recipe_selected'] is None and original_proof['disjoint_event_identity_requires_no_Young_factor'] is original_proof['native_or_ideal_payoff_bound_only_on_its_own_survival_event'] is True, 'Conditional pointwise proof kept distinct from newly upfront sqrt128 recipe')
    basket_mf=inputs[plan['original12_support_manifest']];support=inputs[plan['original12_support_witness']]
    require(basket_mf['passed'] is basket_mf['completed'] is True and basket_mf['files'][Path(plan['original12_support_witness']).name]==plan['selected_expected_SHA256'][plan['original12_support_witness']] and support['schema']=='e11-B4x12-twelve-native-basket-common-coupling-source-witness-v1' and support['passed'] is support['floor_paid_once_not_assumed_exact_divisibility'] is support['no_independence_adaptive_minimum_or_adoption'] is True and exact([support['signed_word_bits'],support['whole_product_bits'],support['original_full48_native_positive_stock_bound']],[72,144,4503599627354112]) and exact(support['continuous_product_law_witness'],bw['accepted_joint_law_witness']), 'Small saved original12/48 nonnegative native support/floor/no-wrap witness, no old numeric recipe')
    target=inputs[plan['target']];native=inputs[plan['runtime_manifest']]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs'])==2842 and exact([target['width'],target['fraction_bits']],[72,40]), 'Original full72/Q40 target and pinned runtime citation')
    nodes={value:node for node in target['nodes'] for value in node['out']};rows=original_proof['literal_original_endpoint_rows']
    require(all(exact(nodes[int(key)],row) for key,row in rows.items()) and exact(nodes[5697],{'op':'select','args':[5644,5696,13],'params':{},'out':[5697]}), 'Exact original zero/flag/discount/fullpayoff endpoint, no candidate substitution')
    stock_ids=[]
    require(len(support['source_results'])==12 and [row['source_basket'] for row in support['source_results']]==bw['source_baskets'], 'All twelve original baskets in the same barrier witness')
    for date,row in enumerate(support['source_results']):
        require(type(row['saved_date_zero_based']) is int and row['saved_date_zero_based']==date and row['exact_three_adds_and_quarter_literal'] is row['sum_stored72_and_product144_safe'] is True and exact(nodes[row['source_basket']],{'op':'cmul','args':[row['full_sum_source']],'params':{'c':274877906944},'out':[row['source_basket']]}), 'Exact nonnegative four-stock quarter floor before maximum')
        leaves=[];stack=[row['full_sum_source']]
        while stack:
            budget();value=stack.pop()
            if value in row['source_stocks']:leaves.append(value)
            else:
                node=nodes[value];require(node['op']=='add' and node['params']=={} and len(node['args'])==2, 'Literal three-add native basket source tree');stack.extend(reversed(node['args']))
        require(exact(leaves,row['source_stocks']) and len(leaves)==4 and len(set(leaves))==4, 'All four same-date native stocks once');stock_ids.extend(leaves)
    leaves=[];stack=[5691]
    while stack:
        budget();value=stack.pop()
        if value in stock_ids:leaves.append(value)
        else:
            node=nodes[value];require(node['op']=='add' and node['params']=={} and len(node['args'])==2, 'Literal original48-stock sum source tree');stack.extend(reversed(node['args']))
    require(len(stock_ids)==len(set(stock_ids))==len(leaves)==48 and sorted(leaves)==sorted(stock_ids) and 48*22906492245==1099511627776-16 and 0<1067016148260<1099511627776, 'Each original stock exactly once, average48c<Q and native discount<Q; all no-wrap support inherited')
    own={}
    require(set(plan['profiles'])=={'primary90','independent130'}, 'Two own profiles, no cross-profile minimum')
    for profile,roles in plan['profiles'].items():
        discount_key=roles['verified_discount_record'];barrier_key=roles['verified_barrier_record'];dr=inputs[discount_key];br=inputs[barrier_key]
        require(child_mf['discount']['files'][Path(discount_key).name]==plan['selected_expected_SHA256'][discount_key] and child_mf['barrier']['files'][Path(barrier_key).name]==plan['selected_expected_SHA256'][barrier_key], 'Two own physical saved child rows read once')
        require(dr['schema']=='e11-B4x12-discount-after-positivepart-squared-L2-limb-row-v1' and dr['profile']==profile and dr['units']=='dollars_squared' and dr['source_discount']==5696 and dr['own_numeric_row_count']==1 and dr['grouped_equals_distributed'] is dr['own_parent_and_discount_authorities_kept_separate'] is dr['same_coupling_fixed_Young_not_error_independence'] is True and exact(dr['components']['discount_squared_L2_upper'],dr['components']['independent_distributed_expression']), 'Own completed unconditional discount bound, no rerun')
        require(br['schema']=='e11-B4x12-barrier-common94-fixed-h1-dyadic256-probability-limb-row-v1' and br['profile']==profile and br['units']=='probability' and br['source_strict_survival_flag']==5644 and br['own_numeric_row_count']==1 and br['probability_cap_at_one_only'] is br['outward_rounding_before_all12_additions'] is True and br['stock_date_native_or_error_independence_assumed'] is br['adaptive_h_grid_or_cross_profile_minimum'] is False, 'Own completed capped mismatch bound; same original flag')
        require(roles['discount_bound_JSON_pointer']=='/components/discount_squared_L2_upper' and roles['barrier_bound_JSON_pointer']=='/components/capped_mismatch_probability_upper', 'Upfront own physical field pointers')
        own[profile]={'discount_bound':dr['components']['discount_squared_L2_upper'],'mismatch_probability_bound':br['components']['capped_mismatch_probability_upper'],'discount_record_path':discount_key,'barrier_record_path':barrier_key}
    witness={'schema':'e11-B4x12-full-payoff-disjoint-events-sqrt128-common-coupling-witness-v1','passed':True,'accepted_interface':fixed,'literal_original_endpoint_rows':rows,'original_stock_ids_once':stock_ids,'original12_basket_source_results':support['source_results'],'accepted_joint_law_witness':bw['accepted_joint_law_witness'],'native_survival_quarter_floor_implies_each_four_stock_sum_lt560Q':True,'native_survival48_stock_sum_lt6720Q':True,'average48c_equals_Q_minus16':True,'native_and_continuous_surviving_average_lt140_dollars':True,'native_and_continuous_surviving_discounted_positivepart_lt40_dollars':True,'boundedness_only_on_each_own_survival_event':True,'unconditional_continuous_positivepart_bounded_support_assumed':False,'four_indicator_events_disjoint':True,'both_survive_uses_unconditional_discount_squared_L2_bound':True,'mismatch_pays1600_squared_and40_absolute':True,'no_new_Young_or_independence_factor':True,'fixed_sqrt_grid_exponent':128,'sqrt_recipe_selected_separately_from_original_unchosen_prospectus':True,'original_strict140_equality_knocks_out':True,'candidate_pricepolicy_G2_estimator_or_advantage_excluded':True}
    return witness,own


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
    require(profile in ('primary90','independent130') and plan['interface']['sqrt_grid_exponent_fixed']==128 and plan['interface']['adaptive_sqrt_grid_cross_profile_minimum_or_extra_Young'] is False, 'One upfront own-profile disjoint-event/sqrt128 route')
    saved=own[profile];discount=limb_ratio(saved['discount_bound']);probability=limb_ratio(saved['mismatch_probability_bound'])
    require(discount>=0 and 0<=probability<=1, 'Own nonnegative verified discount and capped indicator mismatch')
    mismatch_squared=times(Fraction(1600),probability);full_squared=plus(discount,mismatch_squared)
    sqrt_upper,sqrt_witness=outward_fixed_sqrt128(discount)
    mismatch_absolute=times(Fraction(40),probability);mean_bias=plus(sqrt_upper,mismatch_absolute)
    report_quotient,report_remainder=divmod(mean_bias.numerator,mean_bias.denominator)
    report_whole_dollars=report_quotient+(1 if report_remainder else 0)
    require(type(report_whole_dollars) is int and report_whole_dollars>=0 and report_whole_dollars.bit_length()<=256, 'Upfront whole-dollar reporting integer within unchanged JSON token frontier')
    reporting={'unit':'whole_dollars','fixed_reporting_unit':[1,1],'ceiling_of_certified_mean_bias_upper':report_whole_dollars,'certified_upper_allowance_only':True,'actual_measured_bias_or_price':False,'accuracy_threshold_policy_or_adoption':False,'exact_canonical_mean_bound_remains_authority':True}
    components={'parent_discount_squared_L2_upper':saved['discount_bound'],'parent_capped_mismatch_probability_upper':saved['mismatch_probability_bound'],'mismatch_squared_payoff_term':pair(mismatch_squared),'full_payoff_squared_L2_upper':pair(full_squared),'fixed_sqrt128_discount_L2_upper':pair(sqrt_upper),'mismatch_absolute_payoff_term':pair(mismatch_absolute),'full_payoff_mean_bias_upper':pair(mean_bias)}
    return {'schema':'e11-B4x12-full-payoff-disjoint-events-sqrt128-limb-row-v1','profile':profile,'units':{'squared_L2':'dollars_squared','mean_bias_upper':'dollars'},'source_full_payoff':5697,'source_strict_survival_flag':5644,'source_discount':5696,'source_zero':13,'saved_discount_record_path':saved['discount_record_path'],'saved_discount_bound_JSON_pointer':'/components/discount_squared_L2_upper','saved_barrier_record_path':saved['barrier_record_path'],'saved_barrier_bound_JSON_pointer':'/components/capped_mismatch_probability_upper','components':components,'fixed_sqrt128_operand_witness':sqrt_witness,'coarse_mean_bias_reporting_diagnostic':reporting,'own_numeric_row_count':1,'squared_formula':'B_discount+1600*P_mismatch','mean_bias_formula':'S128(B_discount)+40*P_mismatch','sqrt_grid_exponent_fixed':128,'sqrt_grid_strict_gap_upper_symbolic':'2^-128','same_coupling_disjoint_event_not_independence':True,'boundedness_only_on_each_own_survival_event':True,'unconditional_continuous_payoff_support_assumed':False,'extra_Young_rounding_gap_or_cross_profile_minimum_added':False,'old_discount_barrier_stock_tail_moment_kernel_provider_recipe_replayed':False,'mean_bias_upper_is_not_actual_bias_lower_bound':True,'financial_allowance_pricepolicy_G2_candidate_estimator_or_advantage':False}


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
    require(CURRENT_VERIFIED_DISCOUNT_AND_BARRIER_PARENTS_BOUND is True, 'Dormant parent pins must be completed before own current ROOT release')
    try:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ready-sha256',required=True);args=parser.parse_args()
        base=Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True)==ROOT and Path(__file__).resolve(strict=True)==SOURCE,'Exact isolated default4300')
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256],'Separate original base argv0/venv and exact current absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(),'Pinned isolated paths/no ZIP/no site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'Unused own output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','full_payoff_disjoint_event_execution_authorized','full_payoff_disjoint_event_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-full-payoff-disjoint-events-sqrt128-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['full_payoff_disjoint_event_execution_authorized'] is True,'Own current original5696 discount release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['full_payoff_disjoint_event_transfer_witness_accepted'] is True and review['fixed_sqrt128_outward_recipe_accepted'] is True and review['factual_projection_exact_against_verified_child_ROOTs'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        files['original_full_payoff_disjoint_event_source_witness.json']=save('original_full_payoff_disjoint_event_source_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_full_payoff_squared_L2_and_mean_bias.json']=save('primary_full_payoff_squared_L2_and_mean_bias.json',primary)
        files['independent_full_payoff_squared_L2_and_mean_bias.json']=save('independent_full_payoff_squared_L2_and_mean_bias.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'both_own_discount_and_barrier_allowances_consumed_same_profile':True,'no_minimum_or_cross_profile_selection':True,'fixed_sqrt128_selected_before_SCI':True,'disjoint_events_no_new_Young_factor':True,'bounds_only_on_each_own_survival_event':True,'no_independence_assumption':True,'no_old_numeric_recipe_replayed':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'completed_own_numeric_rows':2,'original_distinct_full_payoff_sites':1,'source_full_payoff':5697,'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','own_discount_and_barrier_authorities_consumed_same_profile':True,'fixed_sqrt128_disjoint_event_route':True,'old_child_stock_tail_moment_kernel_or_provider_recipe_replayed':False,'mean_bias_upper_is_not_actual_bias_lower_bound':True,'financial_allowance_pricepolicy_G2_candidate_estimator_or_advantage_results':None}
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
