"""Original B4x12 cap564 complete payoff chain with the verified V2 parent.
Fixed h1/4, dyadic256, sqrt128 and all Young coefficients were chosen before
cap results. ROOT accepted all32 body definitions and compact summary method.
Both verified V2 parent pins are bound and SOURCE authoring gate is True.
Distinct current SOURCE peer, ROOT review and closed14 READY remain required
before the sole ROOT SCI. No new numerical result, adoption, G2 or advantage.
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
SOURCE = ROOT/'research/limitation_program_20261001/experiment_e11_b4x12_cap564_full_payoff_chain_fixed_hquarter_dyadic256_sqrt128_v1.py'
PLAN = ROOT/'.context/E11_B4X12_CAP564_FULL_PAYOFF_CHAIN_INPUT_ADAPTER_run001.json'
MD = ROOT/'.context/E11_B4X12_CAP564_FULL_PAYOFF_CHAIN_PREFLIGHT_run001.md'
READY = ROOT/'.context/E11_B4X12_CAP564_FULL_PAYOFF_CHAIN_ROOT_READY_run001.json'
OUTPUT = ROOT/'results/limitation_program_20261001/E11_B4x12_cap564_full_payoff_chain_fixed_hquarter_dyadic256_sqrt128_run001'
LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'cap564_payoff_chain_source_and_common_coupling_witness.json', 'five_metadata_controls.json', 'primary_cap564_payoff_chain_squared_L2_and_mean_bias.json', 'independent_cap564_payoff_chain_squared_L2_and_mean_bias.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']
CPU, ADMISSION, WALL = (180,150,600)
_STARTED = None
_OWNS_OUTPUT = False
_OUTPUT_ID = None
CURRENT_VERIFIED_CAP564_PARENT_BOUND = True
CAP_PARENT_ROOT_EXPECTED_SHA256 = 'db7b34dd8ed2c3e11edab1b24a68512343304987799b36c9528c91515b0c1a6e'
CAP_PARENT_MANIFEST_EXPECTED_SHA256 = 'dc6711e805a2140379a39e5eb9471d6047a2adcf05ee7272792b40486ca16fb2'
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
    require(CURRENT_VERIFIED_CAP564_PARENT_BOUND is True, 'Dormant cap564 payoff-chain draft requires verified parent and separate current release')
    fixed={'case':'B4x12','W':72,'F':40,'external_cap_dollars':[564,1],'profiles':['primary90','independent130'],'contractual_dates_one_based':[1,2,3,4,5,6,7,8,9,10,11,12],'original_stock_sites':48,'own_stock_source_bindings':96,'own_date_basket_rows':24,'own_summary_rows':2,'source_average':5692,'source_strike':5693,'source_positive_part':5695,'source_discount':5696,'source_full_payoff':5697,'source_max':5642,'source_strict_survival_flag':5644,'source_zero':13,'basket_Young_delta':[1,1000000000],'average_Young_delta':[1,100000],'discount_Young_delta':[1,100000],'average_deterministic_error_numerator_over_Q':9025,'native_positive_support_strict_upper_dollars':464,'barrier_dollars':[140,1],'barrier_h_dollars':[1,4],'barrier_Markov_scale':16,'ideal_band_term':[20,559],'outward_dyadic_grid_exponent_fixed':256,'sqrt_grid_exponent_fixed':128,'surviving_payoff_strict_upper_dollars':40,'mismatch_squared_payoff_upper_dollars_squared':1600,'coarse_reporting_unit':[1,1],'same_original_coupling_and_virtual_cap_payoff_identity':True,'old_cap_stock_kernel_tail_discount_barrier_recipes_replayed':False,'adaptive_grid_h_delta_or_cross_profile_minimum':False,'native_stock_date_error_or_digital_pair_independence_assumed':False,'price_policy_candidate_G2_physical_or_advantage':False}
    require(ready['cap564_payoff_chain_transfer_witness_accepted'] is True and exact(plan['interface'],fixed) and exact(ready['interface'],fixed), 'One upfront cap564/hquarter/dyadic256/sqrt128 contract')
    require(type(CAP_PARENT_ROOT_EXPECTED_SHA256) is type(CAP_PARENT_MANIFEST_EXPECTED_SHA256) is str and plan['selected_expected_SHA256'][plan['verified_cap_ROOT']]==CAP_PARENT_ROOT_EXPECTED_SHA256 and plan['selected_expected_SHA256'][plan['verified_cap_manifest']]==CAP_PARENT_MANIFEST_EXPECTED_SHA256, 'Both future cap parent pins filled only after actual ROOT verification')
    root_key=plan['verified_cap_ROOT'];facts=plan['verified_cap_ROOT_metadata_facts'];mf_key=plan['verified_cap_manifest']
    require(type(inputs[root_key]) is bytes and plan['selected_input_modes'][root_key]=='plain_text_only' and plan['cap_ROOT_factual_projection_exact_against_expected_bytes'] is True, 'Parent ROOT is opaque bytes with exact typed facts independently checked by current3')
    require(facts['passed'] is facts['completed'] is True and facts['blockers']==[] and type(facts['ROOT_observed_terminal_exit_code']) is int and facts['ROOT_observed_terminal_exit_code']==0 and facts['SOURCE_SHA256']==plan['verified_cap_SOURCE_SHA256'] and facts['manifest_SHA256']==CAP_PARENT_MANIFEST_EXPECTED_SHA256 and type(facts['completed_own_numeric_rows']) is int and facts['completed_own_numeric_rows']==24 and type(facts['original_distinct_stock_sites']) is int and facts['original_distinct_stock_sites']==48 and type(facts['completed_own_profile_site_instantiations']) is int and facts['completed_own_profile_site_instantiations']==96 and facts['profiles_remain_separate'] is True and facts['financial_price_policy_G2_or_quantum_advantage'] is False and type(facts['fixture_credit']) is int and facts['fixture_credit']==0, 'Only actual completed cap24/48/96 and two own profiles may be used')
    mf=inputs[mf_key];cap_witness=inputs[plan['verified_cap_witness']]
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['budget_censored'] is False and mf['inclusive_files']==13 and set(mf['files'])==set(plan['verified_cap_exact13_ledger'])-{'manifest.json'} and mf['files'][Path(plan['verified_cap_witness']).name]==plan['selected_expected_SHA256'][plan['verified_cap_witness']], 'Exact parent13 ownership and cap source witness')
    require(cap_witness['schema']=='e11-B4x12-external-cap564-stock-component-source-witness-v1' and cap_witness['passed'] is cap_witness['virtual_native_and_continuous_cap_preserve_original_strict140_payoff'] is cap_witness['ideal_closed139_to141_band_unchanged_at_cap564'] is cap_witness['uncapped_ideal_shared_Gaussian_factorization_only'] is cap_witness['no_new_emitted_cap_circuit_or_resource_savings'] is True and cap_witness['native_closed_band_equivalence_claimed'] is False and exact(cap_witness['accepted_interface']['external_cap_dollars'],[564,1]), 'Verified virtual-payoff identity and ideal-only cap band transport; no native factorization')
    bw=inputs[plan['original_barrier_source_witness']];bmf=inputs[plan['original_barrier_source_manifest']]
    require(bmf['passed'] is bmf['completed'] is True and bmf['files'][Path(plan['original_barrier_source_witness']).name]==plan['selected_expected_SHA256'][plan['original_barrier_source_witness']], 'Verified original barrier source witness membership only, not old probability operands')
    require(bw['schema']=='e11-B4x12-barrier-common94-fixed-h1-dyadic256-source-witness-v1' and bw['passed'] is bw['shared_first_common94_once_in_all48'] is bw['ideal_unclipped_common_factor_only'] is bw['dependence_safe_union_and_squared_error_Markov'] is bw['maximum_adds_no_floor'] is bw['basket_floor_already_paid'] is True and bw['native_clipped_stock_factorization_claimed'] is bw['stock_date_native_or_error_independence_assumed'] is False and exact(cap_witness['accepted_joint_law_witness'],bw['accepted_joint_law_witness']) and bw['accepted_joint_law_witness']['ideal_only'] is True and bw['accepted_joint_law_witness']['digital_or_error_independence'] is False, 'Same original product60/polar joint ideal law and common94; no native or error independence')
    require(type(inputs[plan['historical_chain_proof_MD']]) is bytes and plan['selected_input_modes'][plan['historical_chain_proof_MD']]=='plain_text_only' and type(inputs[plan['historical_chain_proof_peer']]) is bytes, 'Upfront fixed hquarter proof and distinct accepted peer are plaintext ancestry only')
    support=inputs[plan['original12_support_witness']];support_mf=inputs[plan['original12_support_manifest']]
    require(support_mf['passed'] is support_mf['completed'] is True and support_mf['files'][Path(plan['original12_support_witness']).name]==plan['selected_expected_SHA256'][plan['original12_support_witness']] and support['schema']=='e11-B4x12-twelve-native-basket-common-coupling-source-witness-v1' and support['passed'] is support['floor_paid_once_not_assumed_exact_divisibility'] is True and exact(support['continuous_product_law_witness'],bw['accepted_joint_law_witness']), 'Original twelve quarter-floor basket source and same law, no old basket numeric recipe')
    native=inputs[plan['runtime_manifest']];target=inputs[plan['target']]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs'])==2842 and exact([target['width'],target['fraction_bits']],[72,40]) and type(inputs[plan['original_ir_path']]) is bytes and native['frozen_inputs'][plan['original_ir_path']]==plan['selected_expected_SHA256'][plan['original_ir_path']], 'Original72/Q40 native authority and plaintext signed/floor/SELECT semantics')
    nodes={value:node for node in target['nodes'] for value in node['out']};mappings=cap_witness['all48_original_source_mappings']
    require(len(mappings)==48 and [(s['contractual_date_one_based'],s['asset_zero_based']) for s in mappings]==[(d,a) for d in range(1,13) for a in range(4)], 'All48 same original stock mappings before virtual postprocessors')
    require(all(exact(nodes[int(k)],v) for k,v in plan['fixed_original_endpoint_rows'].items()) and exact(nodes[5697],{'op':'select','args':[5644,5696,13],'params':{},'out':[5697]}) and exact(nodes[5644],{'op':'lt','args':[5642,5643],'params':{},'out':[5644]}), 'Exact original strict flag/strike/discount/zero/finalSELECT endpoints')
    stocks=[]
    require(len(support['source_results'])==12 and [r['source_basket'] for r in support['source_results']]==bw['source_baskets'], 'Same original twelve source baskets')
    for date,row in enumerate(support['source_results']):
        sites=mappings[4*date:4*date+4]
        require(row['saved_date_zero_based']==date and row['source_stocks']==[s['stock'] for s in sites] and row['exact_three_adds_and_quarter_literal'] is row['sum_stored72_and_product144_safe'] is True and exact(nodes[row['source_basket']],{'op':'cmul','args':[row['full_sum_source']],'params':{'c':274877906944},'out':[row['source_basket']]}), 'Each original four-stock quarter-floor source uses exactly the own cap stock bindings')
        stocks.extend(row['source_stocks'])
    leaves=[];sum_rows=[];stack=[5691]
    while stack:
        budget();value=stack.pop()
        if value in stocks:leaves.append(value)
        else:
            node=nodes[value];require(node['op']=='add' and node['params']=={} and len(node['args'])==2,'Literal original48-stock sum tree, no basket numeric input');sum_rows.append(node);stack.extend(reversed(node['args']))
    require(len(leaves)==len(set(leaves))==len(stocks)==48 and sorted(leaves)==sorted(stocks) and len(sum_rows)==47 and exact(sum_rows,plan['fixed_original48_sum_rows_in_visit_order']), 'All original48 stocks once and exact47 literal sums')
    require(exact(bw['exact_maximum_rows'],plan['fixed_original_maximum_rows']) and len(plan['fixed_original_maximum_rows'])==11 and all(exact(nodes[node['out'][0]],node) for row in plan['fixed_original_maximum_rows'] for node in (row['strict_lt'],row['select'])), 'Exact old eleven maximum joins as source metadata, no old barrier recipe')
    Q=1099511627776;cap_raw=564*Q;four_sum_max=4*cap_raw;full_sum_max=48*cap_raw
    require(48*22906492245==Q-16 and 0<1067016148260<Q and max(cap_raw.bit_length(),four_sum_max.bit_length(),full_sum_max.bit_length())<72 and (full_sum_max*22906492245).bit_length()<144 and (four_sum_max*274877906944).bit_length()<144 and (464*Q*1067016148260).bit_length()<144, 'Bounded virtual native words/products and original multiplier truncation9025/Q; no cap circuit emitted')
    primary_mf=inputs[plan['discount_primary_manifest']];independent_mf=inputs[plan['discount_independent_manifest']];integrity=inputs[plan['discount_old_ROOT_integrity']]
    require(integrity['passed'] is integrity['producer_and_independent_audit_terminal_PASS'] is True and integrity['SHA_mismatches']==0 and integrity['scientific_kernels_executed'] is False, 'Original archived scalar authority ROOT integrity only')
    for manifest,key in [(primary_mf,plan['discount_primary_authority']),(independent_mf,plan['discount_independent_authority'])]:
        require(manifest['passed'] is manifest['completed'] is manifest['archived_selected_receipt_validity_separate'] is True and manifest['budget_censored'] is manifest['original_expected_hashes_waived'] is False and manifest['files'][Path(key).name]==plan['selected_expected_SHA256'][key] and native['frozen_inputs'][key]==plan['selected_expected_SHA256'][key], 'Own saved discount enclosure/error selected archive; no old discount/smooth-payoff recipe')
    own={}
    require(set(plan['profiles'])=={'primary90','independent130'}, 'Two own physical cap matrices only')
    for profile,roles in plan['profiles'].items():
        key=roles['verified_cap_record'];record=inputs[key]
        require(mf['files'][Path(key).name]==plan['selected_expected_SHA256'][key] and record['schema']=='e11-B4x12-external-cap564-original-stock-component-limb-matrix-v1' and record['profile']==profile and record['units']=='dollars_squared' and exact(record['external_cap_dollars_fixed'],[564,1]) and record['own_numeric_row_count']==12 and record['original_stock_sites']==record['own_profile_site_instantiations']==48 and record['old_assembled_stock_B_decomposed'] is record['old_upper_tail_subtracted'] is record['new_alpha564_estimate_claimed'] is record['stock_native_or_error_independence_assumed'] is record['adaptive_cap_grid_profile_or_improvement_adoption'] is False, 'Own sealed12 cap stock records; direct saved Bcap only, no underlying cap/kernel/log/tail recipes')
        dates=[]
        require(len(record['date_rows'])==len(roles['cap_bound_pointers'])==12, 'Exactly twelve direct own saved capped-stock operands')
        for date,row in enumerate(record['date_rows']):
            sites=mappings[4*date:4*date+4];pointer=roles['cap_bound_pointers'][date]
            require(row['profile']==profile and row['contractual_date_one_based']==date+1 and row['source_stocks']==[s['stock'] for s in sites] and row['source_raw_logs']==[s['raw_log'] for s in sites] and row['new_fixed_guard_8Q_le_signed_clip_high'] is row['three_stage_grouped_equals_distributed'] is True and pointer=='/date_rows/%d/components/capped_stock_squared_L2_upper'%date, 'Own same-date cap physical field and original source mapping')
            bound=row['components']['capped_stock_squared_L2_upper'];bindings=row['per_stock_instantiations']
            require(len(bindings)==4 and [v['asset_zero_based'] for v in bindings]==[0,1,2,3] and all(v['source_stock']==site['stock'] and v['source_raw_log']==site['raw_log'] and exact(v['bound'],bound) and v['same_profile_same_mean_variance_and_full_kernel'] is True for v,site in zip(bindings,sites)), 'Four SAME own Bcap bindings justify collapsed sum4/4; no unproved stock independence')
            dates.append({'date_zero_based':date,'source_stocks':row['source_stocks'],'source_raw_logs':row['source_raw_logs'],'source_basket':support['source_results'][date]['source_basket'],'physical_cap_record_path':key,'bound_JSON_pointer':pointer,'capped_stock_bound':bound,'per_stock_bindings':[{k:v[k] for k in ('asset_zero_based','source_stock','source_raw_log','same_profile_same_mean_variance_and_full_kernel')} for v in bindings]})
        authority_path=roles['discount_authority']
        if profile=='primary90':authority=inputs[authority_path]['cases']['B4x12'];interval=authority['exact_discount_enclosure'];eta=authority['discount_literal_error_upper'];interval_pointer='/cases/B4x12/exact_discount_enclosure';eta_pointer='/cases/B4x12/discount_literal_error_upper'
        else:authority=inputs[authority_path]['B4x12'];interval=authority['independent_true_discount_enclosure'];eta=authority['independent_discount_literal_error_upper'];interval_pointer='/B4x12/independent_true_discount_enclosure';eta_pointer='/B4x12/independent_discount_literal_error_upper'
        require(type(interval) is list and len(interval)==2 and roles['discount_interval_JSON_pointer']==interval_pointer and roles['discount_literal_error_JSON_pointer']==eta_pointer, 'Own unconditional scalar discount interval and eta pointers only')
        own[profile]={'dates':dates,'saved_discount_interval':interval,'saved_literal_error_upper':eta,'discount_authority_path':authority_path,'discount_interval_JSON_pointer':interval_pointer,'discount_literal_error_JSON_pointer':eta_pointer}
    witness={'schema':'e11-B4x12-cap564-payoff-chain-common-coupling-source-witness-v1','passed':True,'accepted_interface':fixed,'verified_cap_ROOT_expected_SHA256':CAP_PARENT_ROOT_EXPECTED_SHA256,'verified_cap_manifest_expected_SHA256':CAP_PARENT_MANIFEST_EXPECTED_SHA256,'all48_original_source_mappings':mappings,'original48_sum_rows':sum_rows,'literal_original_endpoint_rows':plan['fixed_original_endpoint_rows'],'literal_original_maximum_rows':plan['fixed_original_maximum_rows'],'accepted_joint_ideal_law_witness':bw['accepted_joint_law_witness'],'both_own_cap_physical_records_decoded_once':True,'only_direct_saved_Bcap_date_components_consumed':True,'four_same_Bcap_bindings_per_date_verified':True,'original_virtual_cap564_preserves_each_native_and_ideal_full_payoff':True,'quarter_floor_paid_once_at_each_date':True,'time_average_has_original48_stock_inputs_not_baskets':True,'native_capped_average_strict_upper_dollars':564,'native_capped_positivepart_strict_upper_dollars':464,'native_coefficient_floor_error_numerator_over_Q':9025,'original_uncapped_continuous_positive_support_assumed_bounded':False,'ideal_closed_quarter_dollar_band_preserved_by_cap564':True,'common94_factorization_used_only_for_uncapped_ideal_maximum':True,'native_factorization_or_stock_date_error_independence_assumed':False,'fixed_band_and_all_Young_deltas_selected_before_cap_numerics':True,'survival_each_own_stock_sum_lt560Q_or560dollars':True,'own_surviving_payoffs_strictly_below40':True,'four_flag_cases_disjoint_no_extra_Young':True,'new_cap_circuit_resources_candidate_G2_estimator_physical_or_advantage':False}
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
    require(profile in ('primary90','independent130') and plan['interface']['outward_dyadic_grid_exponent_fixed']==256 and plan['interface']['sqrt_grid_exponent_fixed']==128 and plan['interface']['barrier_h_dollars']==[1,4] and plan['interface']['adaptive_grid_h_delta_or_cross_profile_minimum'] is False, 'Only upfront cap564 complete-chain recipe and separate own profile')
    saved=own[profile];dates=saved['dates'];require(len(dates)==12 and [r['date_zero_based'] for r in dates]==list(range(12)), 'All twelve direct own cap rows before any new arithmetic')
    cap_bounds=[limb_ratio(row['capped_stock_bound']) for row in dates]
    Q=1099511627776;epsilon=Fraction(1,Q);delta_b=Fraction(1,1000000000);delta_a=Fraction(1,100000);delta_d=Fraction(1,100000)
    factor_b=plus(Fraction(1),delta_b);floor_b=times(plus(Fraction(1),positive_reciprocal(delta_b)),times(epsilon,epsilon))
    baskets=[];rounded_baskets=[];barrier_rounding=[];date_rows=[]
    for date,(row,bound) in enumerate(zip(dates,cap_bounds)):
        basket=plus(times(factor_b,bound),floor_b)
        expanded=plus(plus(bound,times(delta_b,bound)),floor_b)
        require(basket==expanded, 'Own collapsed four-SAME-B Cauchy then fixed Young equals distributed expression; quarter floor paid once')
        rounded,rw=outward_fixed_dyadic(basket,256)
        baskets.append(basket);rounded_baskets.append(rounded);barrier_rounding.append(dict(rw,own_operand_index=date,source_basket=row['source_basket']))
        date_rows.append({'schema':'e11-B4x12-cap564-chain-quarter-basket-limb-row-v1','profile':profile,'contractual_date_one_based':date+1,'source_stocks':row['source_stocks'],'source_raw_logs':row['source_raw_logs'],'source_basket':row['source_basket'],'physical_cap_record_path':row['physical_cap_record_path'],'saved_cap_bound_JSON_pointer':row['bound_JSON_pointer'],'four_same_bound_source_bindings':row['per_stock_bindings'],'components':{'saved_capped_stock_squared_L2_upper':row['capped_stock_bound'],'basket_Young_delta':pair(delta_b),'basket_Young_factor':pair(factor_b),'paid_quarter_floor_term':pair(floor_b),'capped_basket_squared_L2_upper':pair(basket),'independent_distributed_basket_expression':pair(expanded),'outward_dyadic256_basket_allowance':pair(rounded)},'fixed_barrier_rounding_witness':rw,'same_coupling_not_stock_error_independence':True,'quarter_floor_paid_once':True})
    rounded_stocks=[];stock_rounding=[];stock_bindings=[]
    for date,(row,bound) in enumerate(zip(dates,cap_bounds)):
        for binding in row['per_stock_bindings']:
            rounded,rw=outward_fixed_dyadic(bound,256);rounded_stocks.append(rounded);stock_rounding.append(dict(rw,own_operand_index=len(stock_rounding),source_stock=binding['source_stock']))
            stock_bindings.append(dict(binding,contractual_date_one_based=date+1,saved_cap_bound_JSON_pointer=row['bound_JSON_pointer'],physical_cap_record_path=row['physical_cap_record_path']))
    require(len(rounded_stocks)==len(stock_rounding)==len(stock_bindings)==48, 'All48 own capped stock operands individually rounded before first average addition')
    ordered=rounded_stocks if profile=='primary90' else list(reversed(rounded_stocks));sum_stock=Fraction(0)
    for bound in ordered:sum_stock=plus(sum_stock,bound)
    factor_a=plus(Fraction(1),delta_a);average_error=Fraction(9025,Q);average_floor_term=times(plus(Fraction(1),positive_reciprocal(delta_a)),times(average_error,average_error))
    average=plus(times(factor_a,times(Fraction(1,48),sum_stock)),average_floor_term);average_expanded=average_floor_term
    for bound in ordered:average_expanded=plus(average_expanded,times(times(factor_a,Fraction(1,48)),bound))
    require(average==average_expanded, 'Own fixed dyadic average grouped/distributed equality; no original exact aggregate or second grid penalty')
    positive=average
    lower,upper=[ratio(value) for value in saved['saved_discount_interval']];eta=ratio(saved['saved_literal_error_upper']);q=Fraction(1067016148260,Q)
    require(0<lower<=upper<=1 and eta>=0 and abs(q-lower)<=eta and abs(q-upper)<=eta, 'Own saved unconditional discount enclosure/error endpoints, no exp reevaluation')
    coefficient_error=times(Fraction(464),eta);remainder=plus(coefficient_error,epsilon);factor_d=plus(Fraction(1),delta_d);factor_remainder=plus(Fraction(1),positive_reciprocal(delta_d))
    discount_parent_term=times(times(factor_d,times(upper,upper)),positive);discount_remainder_term=times(factor_remainder,times(remainder,remainder));discount=plus(discount_parent_term,discount_remainder_term)
    square_expanded=plus(plus(times(coefficient_error,coefficient_error),twice(times(coefficient_error,epsilon))),times(epsilon,epsilon));discount_expanded=plus(discount_parent_term,times(factor_remainder,square_expanded))
    require(discount==discount_expanded, 'Fixed own discount Young/remainder square distributed equality; native464 support only and one new floor')
    ordered_baskets=rounded_baskets if profile=='primary90' else list(reversed(rounded_baskets));sum_baskets=Fraction(0)
    for bound in ordered_baskets:sum_baskets=plus(sum_baskets,bound)
    band=Fraction(20,559);scaled_markov=times(Fraction(16),sum_baskets);raw_probability=plus(scaled_markov,band);probability=min(Fraction(1),raw_probability);barrier_expanded=band
    for bound in ordered_baskets:barrier_expanded=plus(barrier_expanded,times(Fraction(16),bound))
    require(raw_probability==barrier_expanded and 0<=probability<=1, 'Own hquarter rounded barrier sum/distributed identity and cap1 only; no h/grid optimization')
    mismatch_squared=times(Fraction(1600),probability);full_squared=plus(discount,mismatch_squared);sqrt_upper,sqrt_witness=outward_fixed_sqrt128(discount);mismatch_absolute=times(Fraction(40),probability);mean_bias=plus(sqrt_upper,mismatch_absolute)
    whole,remainder_whole=divmod(mean_bias.numerator,mean_bias.denominator);coarse=whole+(1 if remainder_whole else 0);require(type(coarse) is int and coarse>=0 and coarse.bit_length()<=256, 'Upfront whole-dollar diagnostic within small JSON token frontier')
    components={'basket_Young_delta':pair(delta_b),'average_Young_delta':pair(delta_a),'discount_Young_delta':pair(delta_d),'sum_outward48_stock_allowances':pair(sum_stock),'average_deterministic_error_absolute_upper':pair(average_error),'weighted_average_deterministic_error_squared':pair(average_floor_term),'capped_native48_average_squared_L2_upper':pair(average),'independent_distributed_average_expression':pair(average_expanded),'capped_strike100_positivepart_squared_L2_upper':pair(positive),'true_discount_lower':pair(lower),'true_discount_upper':pair(upper),'stored_discount_literal_exact':pair(q),'stored_discount_literal_abs_error_upper':pair(eta),'new_discount_floor_absolute_upper':pair(epsilon),'native464_coefficient_error_absolute_upper':pair(coefficient_error),'discount_deterministic_remainder_upper':pair(remainder),'weighted_discount_parent_term':pair(discount_parent_term),'weighted_discount_remainder_term':pair(discount_remainder_term),'capped_discount_squared_L2_upper':pair(discount),'independent_distributed_discount_expression':pair(discount_expanded),'sum_outward12_basket_allowances':pair(sum_baskets),'scaled_hquarter_Markov_term':pair(scaled_markov),'fixed_uncapped_ideal_band_term':pair(band),'uncapped_mismatch_probability_upper':pair(raw_probability),'independent_distributed_barrier_expression':pair(barrier_expanded),'capped_mismatch_probability_upper':pair(probability),'mismatch_squared_payoff_term':pair(mismatch_squared),'full_original_payoff_squared_L2_upper':pair(full_squared),'fixed_sqrt128_capped_discount_L2_upper':pair(sqrt_upper),'mismatch_absolute_payoff_term':pair(mismatch_absolute),'full_original_payoff_mean_bias_upper':pair(mean_bias)}
    return {'schema':'e11-B4x12-cap564-full-payoff-chain-dyadic256-sqrt128-limb-profile-v1','profile':profile,'units':{'date_baskets':'dollars_squared','squared_L2':'dollars_squared','mean_bias_upper':'dollars','mismatch':'probability'},'source_full_payoff':5697,'source_strict_survival_flag':5644,'source_average':5692,'source_discount':5696,'date_rows':date_rows,'components':components,'own_date_basket_row_count':12,'own_summary_row_count':1,'own_numeric_row_count':13,'own_stock_source_binding_count':48,'source_stock_rounding_bindings':stock_bindings,'outward48_stock_rounding_witnesses':stock_rounding,'outward48_stock_operands':[pair(v) for v in rounded_stocks],'outward12_basket_rounding_witnesses':barrier_rounding,'fixed_sqrt128_operand_witness':sqrt_witness,'coarse_mean_bias_reporting_diagnostic':{'unit':'whole_dollars','fixed_reporting_unit':[1,1],'ceiling_of_certified_mean_bias_upper':coarse,'certified_upper_allowance_only':True,'actual_measured_bias_or_price':False,'accuracy_threshold_policy_or_adoption':False,'exact_canonical_mean_bound_remains_authority':True},'external_cap_dollars_fixed':[564,1],'barrier_h_dollars_fixed_before_cap_numerics':[1,4],'outward_grid_exponent_fixed':256,'sqrt_grid_exponent_fixed':128,'basket_quarter_floor_paid_once':True,'average9025_coefficient_truncation_and_floor_paid':True,'positivepart_global_one_Lipschitz_same_bound':True,'discount464_native_coefficient_charge_and_floor_paid':True,'outward_rounding_before48_stock_and12_basket_additions':True,'second_grid_gap_added':False,'old_cap_stock_kernel_tail_discount_barrier_recipe_replayed':False,'same_coupling_disjoint_events_without_new_Young_or_independence':True,'virtual_cap_payoff_identity_transports_back_to_original_payoff':True,'native_factorization_or_unconditional_original_continuous_bounded_support_assumed':False,'adaptive_h_grid_deltas_cross_profile_minimum_or_adoption':False,'mean_bias_upper_is_not_actual_bias_lower_bound':True,'financial_allowance_policy_G2_candidate_estimator_physical_or_advantage':False,'two_profile_combined_scope_not26_completed_limitation_items':True}


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
    require(CURRENT_VERIFIED_CAP564_PARENT_BOUND is True, 'Dormant parent pins must be completed before own current ROOT release')
    try:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ready-sha256',required=True);args=parser.parse_args()
        base=Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True)==ROOT and Path(__file__).resolve(strict=True)==SOURCE,'Exact isolated default4300')
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256],'Separate original base argv0/venv and exact current absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(),'Pinned isolated paths/no ZIP/no site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'Unused own output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','cap564_payoff_chain_execution_authorized','cap564_payoff_chain_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-cap564-payoff-chain-fixed-hquarter-dyadic256-sqrt128-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['cap564_payoff_chain_execution_authorized'] is True,'Own current cap564 full payoff-chain release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['cap564_payoff_chain_transfer_witness_accepted'] is True and review['fixed_sqrt128_outward_recipe_accepted'] is True and review['fixed_dyadic256_outward_recipe_accepted'] is True and review['factual_projection_exact_against_verified_cap_ROOT'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        files['cap564_payoff_chain_source_and_common_coupling_witness.json']=save('cap564_payoff_chain_source_and_common_coupling_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_cap564_payoff_chain_squared_L2_and_mean_bias.json']=save('primary_cap564_payoff_chain_squared_L2_and_mean_bias.json',primary)
        files['independent_cap564_payoff_chain_squared_L2_and_mean_bias.json']=save('independent_cap564_payoff_chain_squared_L2_and_mean_bias.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'both_own_cap_stock_matrices_consumed_directly_before_new_chain_stages':True,'quarter_floor_average9025_positive_contraction_discount464_barrier_hquarter_all_paid':True,'fixed_dyadic256_before48_and12_additions':True,'only_two_own_physical_cap_records_read_once':True,'no_minimum_or_cross_profile_selection':True,'fixed_sqrt128_selected_before_SCI':True,'disjoint_events_no_new_Young_factor':True,'bounds_only_on_each_own_survival_event':True,'no_independence_assumption':True,'no_old_numeric_recipe_replayed':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'schema':'e11-cap564-full-payoff-chain-reference-summary-v1','passed':True,'completed':True,'profile_result_files':[{'filename':'primary_cap564_payoff_chain_squared_L2_and_mean_bias.json','expected_SHA256':files['primary_cap564_payoff_chain_squared_L2_and_mean_bias.json'],'profile':'primary90','own_date_basket_rows':12,'own_summary_rows':1,'own_numeric_rows':13,'own_stock_source_bindings':48},{'filename':'independent_cap564_payoff_chain_squared_L2_and_mean_bias.json','expected_SHA256':files['independent_cap564_payoff_chain_squared_L2_and_mean_bias.json'],'profile':'independent130','own_date_basket_rows':12,'own_summary_rows':1,'own_numeric_rows':13,'own_stock_source_bindings':48}],'completed_own_numeric_rows':26,'completed_own_date_basket_rows':24,'completed_own_summary_rows':2,'original_stock_source_sites':48,'own_stock_source_bindings':96,'original_distinct_full_payoff_sites':1,'source_full_payoff':5697,'controls_file':{'filename':'five_metadata_controls.json','expected_SHA256':files['five_metadata_controls.json']},'witness_file':{'filename':'cap564_payoff_chain_source_and_common_coupling_witness.json','expected_SHA256':files['cap564_payoff_chain_source_and_common_coupling_witness.json']},'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','new_chain_uses_only_own_saved_cap_stock_and_discount_scalar_authorities':True,'fixed_hquarter_dyadic256_sqrt128_complete_chain_route':True,'old_cap_stock_tail_moment_kernel_discount_barrier_or_provider_recipe_replayed':False,'mean_bias_upper_is_not_actual_bias_lower_bound':True,'financial_allowance_pricepolicy_G2_candidate_estimator_or_advantage_results':None}
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

if __name__=='__main__':
    main()
