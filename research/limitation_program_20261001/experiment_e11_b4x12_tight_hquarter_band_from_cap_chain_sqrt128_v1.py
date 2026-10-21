"""Current tighter-quarter-band continuation of the saved-verified cap564 chain.
The source consumes only each own parent's twelve already rounded basket operands
and saved discount allowance. It substitutes the fixed ideal analytic band
(4/147)*(1+1/940797), retains cap1/disjoint1600/40/sqrt128, and replays no child recipe.
The five parent paths/hashes/identities are bound to verified39; current numerical
results remain unbound. SOURCE authoring is authorized; fresh current SOURCE peer,
ROOT review and closed READY remain mandatory before the sole future ROOT SCI.
No numerical, performance, adoption, price-policy, candidate G2 or advantage claim.
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
SOURCE=ROOT/'research/limitation_program_20261001/experiment_e11_b4x12_tight_hquarter_band_from_cap_chain_sqrt128_v1.py'
PLAN=ROOT/'.context/E11_B4X12_TIGHT_HQUARTER_BAND_FROM_CAP_CHAIN_INPUT_ADAPTER_run001.json'
MD=ROOT/'.context/E11_B4X12_TIGHT_HQUARTER_BAND_FROM_CAP_CHAIN_PREFLIGHT_run001.md'
READY=ROOT/'.context/E11_B4X12_TIGHT_HQUARTER_BAND_FROM_CAP_CHAIN_ROOT_READY_run001.json'
OUTPUT=ROOT/'results/limitation_program_20261001/E11_B4x12_tight_hquarter_band_from_cap_chain_sqrt128_run001'
LEDGER=['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'tight_hquarter_band_saved_chain_and_original_payoff_witness.json', 'five_metadata_controls.json', 'primary_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json', 'independent_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']
CPU, ADMISSION, WALL=(180,150,600)
_STARTED=None
_OWNS_OUTPUT=False
_OUTPUT_ID=None
CURRENT_VERIFIED_CHAIN_PARENT_BOUND=True
CHAIN_PARENT_ROOT_EXPECTED_SHA256='ea307dd11687b7b0dcab7984695d26e1a75ff48969b2e567e0b2e17d3e400e54'
CHAIN_PARENT_MANIFEST_EXPECTED_SHA256='020bb7792734a7df8b6cb587319f3b8ef75c731ae3882c9ac77ffef851f00cc7'
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
    require(CURRENT_VERIFIED_CHAIN_PARENT_BOUND is True, 'Disabled until completed own chain parent, independent current SOURCE peer and ROOT release')
    fixed={'case':'B4x12','W':72,'F':40,'profiles':['primary90','independent130'],'source_full_payoff':5697,'source_strict_survival_flag':5644,'source_max':5642,'source_discount':5696,'source_zero':13,'external_cap_dollars':[564,1],'barrier_h_dollars':[1,4],'barrier_Markov_scale':16,'ideal_band_leading_factor':[4,147],'ideal_band_correction':[1,940797],'saved_basket_grid_exponent':256,'sqrt_grid_exponent_fixed':128,'own_profile_rows':2,'saved_basket_operands_per_profile':12,'saved_discount_operands_per_profile':1,'mismatch_squared_payoff_upper_dollars_squared':[1600,1],'surviving_payoff_upper_dollars':[40,1],'coarse_reporting_unit_dollars':[1,1],'new_rounding_or_stock_average_discount_recipe':False,'ideal_common94_factorization_only':True,'same_original_coupling_disjoint_events_not_independence':True,'adaptive_h_grid_delta_or_cross_profile_minimum':False,'price_policy_G2_candidate_physical_or_advantage':False}
    require(exact(plan['interface'],fixed) and exact(ready['interface'],fixed) and ready['tight_hquarter_band_transfer_witness_accepted'] is True, 'Only fixed saved-parent/hquarter/new-band/sqrt128 contract')
    require(type(CHAIN_PARENT_ROOT_EXPECTED_SHA256) is type(CHAIN_PARENT_MANIFEST_EXPECTED_SHA256) is str and plan['selected_expected_SHA256'][plan['verified_chain_ROOT']]==CHAIN_PARENT_ROOT_EXPECTED_SHA256 and plan['selected_expected_SHA256'][plan['verified_chain_manifest']]==CHAIN_PARENT_MANIFEST_EXPECTED_SHA256 and plan['future_parent_bindings_pending'] is False, 'Five completed future parent roles genuinely bound before any numerical operand')
    root_key=plan['verified_chain_ROOT'];facts=plan['verified_chain_ROOT_metadata_facts'];mf=inputs[plan['verified_chain_manifest']];pw=inputs[plan['verified_chain_witness']]
    require(type(inputs[root_key]) is bytes and plan['selected_input_modes'][root_key]=='plain_text_only' and plan['chain_ROOT_factual_projection_exact_against_expected_bytes'] is True and type(facts) is dict, 'Current independently reviewed exact parent opaque ROOT projection')
    require(facts['passed'] is facts['completed'] is True and facts['blockers']==[] and type(facts['ROOT_observed_terminal_exit_code']) is int and facts['ROOT_observed_terminal_exit_code']==0 and facts['SOURCE_SHA256']==plan['verified_chain_SOURCE_SHA256'] and facts['manifest_SHA256']==CHAIN_PARENT_MANIFEST_EXPECTED_SHA256 and exact([facts['completed_own_numeric_rows'],facts['completed_own_date_basket_rows'],facts['completed_own_summary_rows'],facts['original_stock_source_sites'],facts['own_stock_source_bindings']],[26,24,2,48,96]) and facts['financial_price_policy_G2_or_quantum_advantage'] is False and type(facts['fixture_credit']) is int and facts['fixture_credit']==0 and facts['dyadic256_sqrt128_and_reporting_checked_by_saved_order_and_predecessor_only'] is True, 'Completed saved chain26 rows are finite own operands, not26 limitation completions or adoption')
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['budget_censored'] is False and type(mf['inclusive_files']) is int and mf['inclusive_files']==13 and set(mf['files'])==set(plan['verified_chain_exact13_ledger'])-{'manifest.json'} and mf['files'][Path(plan['verified_chain_witness']).name]==plan['selected_expected_SHA256'][plan['verified_chain_witness']], 'Exact completed parent13 seal/witness ownership')
    require(pw['schema']=='e11-B4x12-cap564-payoff-chain-common-coupling-source-witness-v1' and pw['passed'] is pw['original_virtual_cap564_preserves_each_native_and_ideal_full_payoff'] is pw['ideal_closed_quarter_dollar_band_preserved_by_cap564'] is pw['common94_factorization_used_only_for_uncapped_ideal_maximum'] is pw['own_surviving_payoffs_strictly_below40'] is pw['four_flag_cases_disjoint_no_extra_Young'] is True and pw['native_factorization_or_stock_date_error_independence_assumed'] is pw['original_uncapped_continuous_positive_support_assumed_bounded'] is pw['new_cap_circuit_resources_candidate_G2_estimator_physical_or_advantage'] is False, 'Parent virtual cap/payoff identity and survival-only40/disjoint witness; no native band or independence')
    bw=inputs[plan['original_barrier_source_witness']];bmf=inputs[plan['original_barrier_source_manifest']]
    require(bmf['passed'] is bmf['completed'] is True and bmf['files'][Path(plan['original_barrier_source_witness']).name]==plan['selected_expected_SHA256'][plan['original_barrier_source_witness']] and bw['schema']=='e11-B4x12-barrier-common94-fixed-h1-dyadic256-source-witness-v1' and bw['passed'] is bw['shared_first_common94_once_in_all48'] is bw['ideal_unclipped_common_factor_only'] is True and bw['native_clipped_stock_factorization_claimed'] is bw['stock_date_native_or_error_independence_assumed'] is False and exact(pw['accepted_joint_ideal_law_witness'],bw['accepted_joint_law_witness']), 'Existing original all48 common94 ideal source law only, no old probability reuse')
    lemma=inputs[plan['tighter_band_lemma_JSON']];review=inputs[plan['tighter_band_ROOT_conditional_review']]
    require(lemma['schema']=='e11-B4x12-common94-fixed-hquarter-improved-ideal-closed-band-prospective-lemma-v1' and lemma['metadata_only'] is True and lemma['scientific_evaluation_performed'] is lemma['SOURCE_READY_SCI_or_result_authorized'] is False and exact(lemma['fixed_contract']['h_dollars'],[1,4]) and exact(lemma['fixed_contract']['H_dollars'],[140,1]) and exact(lemma['fixed_contract']['ideal_loading_squared'],[3,1000]) and lemma['fixed_contract']['ideal_shared_normal_source']==94 and lemma['fixed_contract']['native_or_error_independence'] is False and lemma['proof_MD_expected_SHA256']==plan['selected_expected_SHA256'][plan['tighter_band_lemma_MD']], 'Exact fixed quarter-dollar ideal density lemma and MD byte binding, no permission inheritance')
    expression={'operation':'product','factors':[[4,147],{'operation':'sum','terms':[[1,1],[1,940797]]}]}
    require(exact(lemma['elementary_constant_proof']['new_fixed_band_expression'],expression) and exact(lemma['elementary_constant_proof']['conditional_log_density_upper'],[160,21]) and lemma['ideal_closed_band_equivalence_only']['factorization_used_only_for_uncapped_ideal_maximum'] is True and lemma['ideal_closed_band_equivalence_only']['native_closed_band_equivalence_claimed'] is False and lemma['ideal_closed_band_equivalence_only']['interval_for_fixed_contract']=='[140-1/4,140+1/4]', 'Upfront analytic tighter-band expression and ideal-only closed endpoints; no series/density evaluation')
    require(review['schema']=='root-e11-common94-fixed-hquarter-improved-ideal-band-conditional-proof-review-v1' and review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is review['nonauthor_review'] is True and review['blockers']==[] and review['SOURCE_READY_or_SCI_authorized'] is False and review['reviewed_JSON_SHA256']==plan['selected_expected_SHA256'][plan['tighter_band_lemma_JSON']] and review['reviewed_MD_SHA256']==plan['selected_expected_SHA256'][plan['tighter_band_lemma_MD']] and review['fixed_band_expression']=='(4/147)*(1+1/940797)', 'Separate ROOT conditional proof review licenses only the exact ideal band, not this SCI')
    require(type(inputs[plan['tighter_band_lemma_MD']]) is bytes and plan['selected_input_modes'][plan['tighter_band_lemma_MD']]=='plain_text_only', 'Original tighter-band proof MD bytes retained')
    native=inputs[plan['runtime_manifest']];target=inputs[plan['target']]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs'])==2842 and exact([target['width'],target['fraction_bits']],[72,40]), 'Original signed72/Q40 target and expected runtime authority only')
    nodes={value:node for node in target['nodes'] for value in node['out']}
    require(all(exact(nodes[int(k)],v) for k,v in pw['literal_original_endpoint_rows'].items()) and exact(nodes[5697],{'op':'select','args':[5644,5696,13],'params':{},'out':[5697]}) and exact(nodes[5644],{'op':'lt','args':[5642,5643],'params':{},'out':[5644]}) and exact(pw['literal_original_maximum_rows'],bw['exact_maximum_rows']) and len(pw['literal_original_maximum_rows'])==11, 'Original strict140/fullpayoff/max endpoints stay fixed source citations')
    mappings=pw['all48_original_source_mappings'];require(type(mappings) is list and len(mappings)==48 and [(r['contractual_date_one_based'],r['asset_zero_based']) for r in mappings]==[(d,a) for d in range(1,13) for a in range(4)], 'Same original48 source bindings for all future direct basket operands')
    own={};require(set(plan['profiles'])=={'primary90','independent130'}, 'Exactly two own physical saved chain records')
    for profile,roles in plan['profiles'].items():
        key=roles['verified_chain_record'];record=inputs[key]
        require(mf['files'][Path(key).name]==plan['selected_expected_SHA256'][key] and record['schema']=='e11-B4x12-cap564-full-payoff-chain-dyadic256-sqrt128-limb-profile-v1' and record['profile']==profile and exact([record['own_date_basket_row_count'],record['own_summary_row_count'],record['own_numeric_row_count'],record['own_stock_source_binding_count']],[12,1,13,48]) and exact(record['external_cap_dollars_fixed'],[564,1]) and exact(record['barrier_h_dollars_fixed_before_cap_numerics'],[1,4]) and record['outward_grid_exponent_fixed']==256 and record['virtual_cap_payoff_identity_transports_back_to_original_payoff'] is record['outward_rounding_before48_stock_and12_basket_additions'] is True and record['second_grid_gap_added'] is record['old_cap_stock_kernel_tail_discount_barrier_recipe_replayed'] is record['native_factorization_or_unconditional_original_continuous_bounded_support_assumed'] is record['adaptive_h_grid_deltas_cross_profile_minimum_or_adoption'] is record['financial_allowance_policy_G2_candidate_estimator_physical_or_advantage'] is False, 'Own saved chain source/scope/rounded operands; no full old chain or adaptive recipe')
        require(type(record['date_rows']) is type(record['outward12_basket_rounding_witnesses']) is type(roles['basket_operand_pointers']) is list and len(record['date_rows'])==len(record['outward12_basket_rounding_witnesses'])==len(roles['basket_operand_pointers'])==12 and roles['discount_operand_pointer']=='/components/capped_discount_squared_L2_upper', 'Only twelve saved outward basket and one direct own discount pointers')
        baskets=[];bindings=[]
        for date,(row,pointer,rw) in enumerate(zip(record['date_rows'],roles['basket_operand_pointers'],record['outward12_basket_rounding_witnesses'])):
            sites=mappings[4*date:4*date+4]
            require(pointer=='/date_rows/%d/components/outward_dyadic256_basket_allowance'%date and row['profile']==profile and type(row['contractual_date_one_based']) is int and row['contractual_date_one_based']==date+1 and exact(row['source_stocks'],[r['stock'] for r in sites]) and exact(row['source_raw_logs'],[r['raw_log'] for r in sites]) and row['quarter_floor_paid_once'] is row['same_coupling_not_stock_error_independence'] is True and row['source_basket']==bw['source_baskets'][date], 'Each saved outward operand retains original date/stock/rawlog/basket/paid-floor binding')
            base=row['fixed_barrier_rounding_witness']
            require(base['schema']=='e11-fixed-dyadic256-outward-rounding-operand-witness-v1' and type(base['grid_exponent']) is int and base['grid_exponent']==256 and type(base['division_had_nonzero_remainder']) is bool and base['outward_order_and_strict_grid_gap_passed'] is True and base['old_exact_aggregate_required'] is False and exact(rw,dict(base,own_operand_index=date,source_basket=row['source_basket'])), 'Only already saved and independently verified parent dyadic witnesses; no new rounding')
            baskets.append(row['components']['outward_dyadic256_basket_allowance']);bindings.append({'contractual_date_one_based':date+1,'source_basket':row['source_basket'],'source_stocks':row['source_stocks'],'source_raw_logs':row['source_raw_logs'],'saved_operand_pointer':pointer,'saved_rounding_witness':base})
        own[profile]={'parent_record_path':key,'saved_baskets':baskets,'basket_bindings':bindings,'saved_discount':record['components']['capped_discount_squared_L2_upper'],'discount_operand_pointer':roles['discount_operand_pointer']}
    witness={'schema':'e11-B4x12-tight-hquarter-band-saved-chain-common-coupling-witness-v1','passed':True,'accepted_interface':fixed,'verified_chain_ROOT_expected_SHA256':CHAIN_PARENT_ROOT_EXPECTED_SHA256,'verified_chain_manifest_expected_SHA256':CHAIN_PARENT_MANIFEST_EXPECTED_SHA256,'literal_original_endpoint_rows':pw['literal_original_endpoint_rows'],'accepted_joint_ideal_law_witness':pw['accepted_joint_ideal_law_witness'],'original48_source_mappings':mappings,'both_own_saved_chain_records_decoded_once':True,'only_saved_outward12_baskets_and_own_discount_consumed':True,'no_new_stock_rounding_average_positive_discount_cap_or_kernel_recipe':True,'ideal_tighter_band_lemma_expected_SHA256':plan['selected_expected_SHA256'][plan['tighter_band_lemma_JSON']],'ideal_tighter_band_ROOT_conditional_review_expected_SHA256':plan['selected_expected_SHA256'][plan['tighter_band_ROOT_conditional_review']],'fixed_ideal_band_expression':'(4/147)*(1+1/940797)','ideal_closed_hquarter_band_transport_and_uncapped_common94_only':True,'native_band_factorization_or_error_independence':False,'original_virtual_cap_payoff_identity_preserved':True,'own_survival40_and_disjoint1600_40_transport_preserved':True,'current_SOURCE_peer_and_ROOT_READY_separate_from_conditional_proof':True,'old_child_probability_or_full_payoff_allowance_consumed':False,'candidate_pricepolicy_G2_physical_or_advantage_excluded':True}
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
    require(profile in ('primary90','independent130') and exact(plan['interface']['barrier_h_dollars'],[1,4]) and exact(plan['interface']['ideal_band_leading_factor'],[4,147]) and exact(plan['interface']['ideal_band_correction'],[1,940797]) and plan['interface']['adaptive_h_grid_delta_or_cross_profile_minimum'] is False, 'Only fixed conditional band recipe and own profile')
    saved=own[profile];require(len(saved['saved_baskets'])==len(saved['basket_bindings'])==12, 'Twelve existing same-profile outward basket operands')
    baskets=[limb_ratio(value) for value in saved['saved_baskets']]
    require(all((1<<256)%value.denominator==0 for value in baskets), 'Saved dyadic denominator shape before first addition; no new rounding')
    discount=limb_ratio(saved['saved_discount']);total=Fraction(0)
    ordered=baskets if profile=='primary90' else list(reversed(baskets))
    for value in ordered:total=plus(total,value)
    leading=Fraction(4,147);correction=Fraction(1,940797);band=times(leading,plus(Fraction(1),correction));markov=times(Fraction(16),total);raw=plus(markov,band);probability=min(Fraction(1),raw);expanded=band
    for value in ordered:expanded=plus(expanded,times(Fraction(16),value))
    require(raw==expanded and 0<=probability<=1, 'Independent distributed new fixed band/Markov identity and cap1 only')
    mismatch_squared=times(Fraction(1600),probability);full_squared=plus(discount,mismatch_squared);sqrt_upper,sqrt_witness=outward_fixed_sqrt128(discount);mismatch_absolute=times(Fraction(40),probability);mean=plus(sqrt_upper,mismatch_absolute)
    whole,remainder=divmod(mean.numerator,mean.denominator);coarse=whole+(1 if remainder else 0);require(type(coarse) is int and coarse>=0 and coarse.bit_length()<=256, 'Fixed whole-dollar reporting ceiling is small allowance diagnostic, not actual bias')
    components={'saved_capped_discount_squared_L2_upper':saved['saved_discount'],'sum_saved_outward12_basket_allowances':pair(total),'fixed_ideal_band_leading_factor':pair(leading),'fixed_ideal_band_correction':pair(correction),'fixed_ideal_band_probability_upper':pair(band),'scaled_saved_basket_Markov_term':pair(markov),'uncapped_mismatch_probability_upper':pair(raw),'independent_distributed_barrier_expression':pair(expanded),'capped_mismatch_probability_upper':pair(probability),'mismatch_squared_payoff_term':pair(mismatch_squared),'full_original_payoff_squared_L2_upper':pair(full_squared),'fixed_sqrt128_capped_discount_L2_upper':pair(sqrt_upper),'mismatch_absolute_payoff_term':pair(mismatch_absolute),'full_original_payoff_mean_bias_upper':pair(mean)}
    return {'schema':'e11-B4x12-tight-hquarter-band-saved-chain-sqrt128-limb-row-v1','profile':profile,'units':{'mismatch':'probability','squared_L2':'dollars_squared','mean_bias_upper':'dollars'},'source_full_payoff':5697,'source_strict_survival_flag':5644,'source_discount':5696,'own_numeric_row_count':1,'physical_chain_record_path':saved['parent_record_path'],'saved_basket_operand_count':12,'saved_discount_operand_count':1,'saved_basket_bindings':saved['basket_bindings'],'saved_outward_basket_operands':saved['saved_baskets'],'saved_discount_operand_pointer':saved['discount_operand_pointer'],'components':components,'fixed_sqrt128_operand_witness':sqrt_witness,'fixed_band_dollars_h':[1,4],'fixed_band_expression':'(4/147)*(1+1/940797)','fixed_sqrt_grid_exponent':128,'raw_probability_upper_less_than_one':raw<1,'probability_cap_active':raw>1,'diagnostic_threshold_is_not_accuracy_adoption':True,'coarse_mean_bias_reporting_diagnostic':{'unit':'whole_dollars','fixed_reporting_unit':[1,1],'ceiling_of_certified_mean_bias_upper':coarse,'certified_upper_allowance_only':True,'actual_measured_bias_or_price':False,'accuracy_threshold_policy_or_adoption':False,'exact_canonical_mean_bound_remains_authority':True},'saved_operands_only_no_new_dyadic_rounding_or_child_chain_recipe':True,'no_new_Young_gap_or_adaptive_cross_profile_minimum':True,'same_coupling_disjoint_event_not_error_independence':True,'virtual_cap_payoff_identity_transports_to_original_payoff':True,'unconditional_continuous_payoff_bounded_support_assumed':False,'native_band_factorization_claimed':False,'mean_bias_upper_is_not_actual_bias_lower_bound':True,'price_policy_G2_candidate_physical_or_advantage':False}

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
    require(CURRENT_VERIFIED_CHAIN_PARENT_BOUND is True, 'Dormant parent pins must be completed before own current ROOT release')
    try:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ready-sha256',required=True);args=parser.parse_args()
        base=Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True)==ROOT and Path(__file__).resolve(strict=True)==SOURCE,'Exact isolated default4300')
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256],'Separate original base argv0/venv and exact current absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(),'Pinned isolated paths/no ZIP/no site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'Unused own output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','tight_hquarter_band_execution_authorized','tight_hquarter_band_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-tight-hquarter-band-from-cap-chain-sqrt128-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['tight_hquarter_band_execution_authorized'] is True,'Own current tighter hquarter band saved-chain release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['tight_hquarter_band_transfer_witness_accepted'] is True and review['fixed_sqrt128_outward_recipe_accepted'] is True and review['saved_outward_basket_operands_only'] is True and review['factual_projection_exact_against_verified_chain_ROOT'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        files['tight_hquarter_band_saved_chain_and_original_payoff_witness.json']=save('tight_hquarter_band_saved_chain_and_original_payoff_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json']=save('primary_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json',primary)
        files['independent_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json']=save('independent_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'two_own_saved_chain_profiles_consumed_once':True,'only_already_rounded12_baskets_and_own_discount_are_numeric_inputs':True,'one_fixed_hquarter_tighter_ideal_band':True,'no_new_stock_rounding_or_child_chain_recipe':True,'no_minimum_or_cross_profile_selection':True,'fixed_sqrt128_selected_before_SCI':True,'disjoint_events_no_new_Young_factor':True,'bounds_only_on_each_own_survival_event':True,'no_independence_assumption':True,'no_old_numeric_recipe_replayed':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        owned_guard()
        summary={'schema':'e11-tight-hquarter-band-saved-chain-reference-summary-v1','passed':True,'completed':True,'profile_result_files':[{'filename':'primary_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json','expected_SHA256':files['primary_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json'],'bytes':(OUTPUT/'primary_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json').stat().st_size,'profile':'primary90','own_numeric_rows':1,'saved_basket_operand_count':12,'saved_discount_operand_count':1},{'filename':'independent_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json','expected_SHA256':files['independent_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json'],'bytes':(OUTPUT/'independent_tight_hquarter_band_original_payoff_squared_L2_and_mean_bias.json').stat().st_size,'profile':'independent130','own_numeric_rows':1,'saved_basket_operand_count':12,'saved_discount_operand_count':1}],'completed_own_numeric_rows':2,'original_distinct_full_payoff_sites':1,'source_full_payoff':5697,'controls_file':{'filename':'five_metadata_controls.json','expected_SHA256':files['five_metadata_controls.json']},'witness_file':{'filename':'tight_hquarter_band_saved_chain_and_original_payoff_witness.json','expected_SHA256':files['tight_hquarter_band_saved_chain_and_original_payoff_witness.json']},'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','only_verified_saved_baskets_and_discount_operands':True,'fixed_tighter_hquarter_band_sqrt128_route':True,'old_chain_cap_stock_tail_moment_kernel_discount_barrier_or_provider_recipe_replayed':False,'mean_bias_upper_is_not_actual_bias_lower_bound':True,'financial_allowance_pricepolicy_G2_candidate_estimator_or_advantage_results':None}
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
