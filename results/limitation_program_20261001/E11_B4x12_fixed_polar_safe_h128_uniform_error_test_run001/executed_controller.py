"""Bounded fixed-polar-safe uniform error and all12 h1/128 feasibility test.
The same original60 uniforms, native log/cos/root, all48 degree12 source and
pointwise A4608-squared premises are joined to fixed lambda2^-18 and h1/128.
All12 inequalities must pass before adopting an own conditional payoff mean.
Criterion failure seals a negative feasibility record with mean None; there
is no threshold retry, original-provider replay, accuracy policy or advantage.
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
SOURCE=ROOT/'research/limitation_program_20261001/experiment_e11_b4x12_fixed_polar_safe_h128_uniform_error_test_v1.py'
PLAN=ROOT/'.context/E11_B4X12_FIXED_POLAR_SAFE_H128_UNIFORM_ERROR_TEST_INPUT_ADAPTER_run001.json'
MD=ROOT/'.context/E11_B4X12_FIXED_POLAR_SAFE_H128_UNIFORM_ERROR_TEST_PREFLIGHT_run001.md'
READY=ROOT/'.context/E11_B4X12_FIXED_POLAR_SAFE_H128_UNIFORM_ERROR_TEST_ROOT_READY_run001.json'
OUTPUT=ROOT/'results/limitation_program_20261001/E11_B4x12_fixed_polar_safe_h128_uniform_error_test_run001'
LEDGER=['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'fixed_polar_safe_h128_source_pointwise_witness.json', 'five_metadata_controls.json', 'primary_fixed_polar_safe_h128_uniform_error_feasibility.json', 'independent_fixed_polar_safe_h128_uniform_error_feasibility.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']
CPU, ADMISSION, WALL=(180,150,600)
_STARTED=None
_OWNS_OUTPUT=False
_OUTPUT_ID=None
CURRENT_FIXED_POLAR_SAFE_AUTHORING_AND_PROOF_BOUND=True
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
    require(CURRENT_FIXED_POLAR_SAFE_AUTHORING_AND_PROOF_BOUND is True and ready['fixed_polar_safe_h128_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']), 'Current fixed polar-safe SOURCE and separate READY')
    fixed={'case':'B4x12','W':72,'F':40,'profiles':['primary90','independent130'],'fixed_lambda':[1,262144],'fixed_h_dollars':[1,128],'radial_pair_count':30,'uniform_input_count':60,'original_stock_sites':48,'pointwise_date_rows_per_profile':12,'external_cap_dollars':[564,1],'pointwise_kernel_M':4608,'sqrt_grid_exponent_fixed':128,'ideal_band_leading_factor':[1,1176],'ideal_band_correction':[1,963379197],'source_full_payoff':5697,'fixed_criterion':'all12_saved_pointwise_basket_upper<=1/128','criterion_failure_seals_negative_feasibility_with_payoff_mean_None':True,'same_coupling_no_native_or_error_independence':True,'no_adaptive_lambda_h_fallback_or_accuracy_adoption':True,'candidate_circuit_G2_physical_or_advantage':False}
    require(exact(plan['interface'],fixed), 'Only upfront lambda2^-18/h1/128 pointwise test')
    proof=inputs[plan['prospectus002']];proot=inputs[plan['conditional_ROOT']];peer=inputs[plan['conditional_peer']]
    require(proof['metadata_only'] is True and proof['scientific_evaluation_performed'] is False and proot['schema']=='root-e11-fixed-polar-safe-h128-conditional-proof-review-v1' and proot['passed'] is proot['science_static_passed'] is proot['lifecycle_static_passed'] is True and proot['blockers']==[] and proot['bounded_actual_SOURCE_authoring_permitted'] is True and proot['current_SOURCE_peer_ROOT_READY_SCI_or_result_authorized'] is False and exact(proot['fixed_lambda'],fixed['fixed_lambda']) and exact(proot['fixed_h_dollars'],fixed['fixed_h_dollars']) and proot['failed_fixed_criterion_no_payoff_certificate_adoption_or_adaptive_fallback'] is True and peer['passed'] is peer['science_static_passed'] is peer['lifecycle_static_passed'] is True and peer['blockers']==[], 'Conditional proof ancestry requires actual current SOURCE release')
    inventory=inputs[plan['operand_inventory']]
    require(inventory['schema']=='e11-B4x12-fixed-polar-safe-saved-operand-role-inventory-v1' and inventory['metadata_only'] is True and inventory['scientific_evaluation_performed'] is inventory['new_pointwise_allowances_guards_ratios_sums_or_limb_values_evaluated'] is False and inventory['all24_own_rows_and96_stock_identity_joins_checked'] is inventory['all30_pair_and60_uniform_identity_joins_checked'] is True and exact(inventory['fixed_lambda'],fixed['fixed_lambda']) and exact(inventory['fixed_h'],fixed['fixed_h_dollars']), 'Exact independently prepared saved operand roles, not numeric evidence by themselves')
    facts=plan['verified_matrix_ROOT_metadata_facts'];original=inputs[plan['verified_matrix_PLAN']];mf=inputs[plan['verified_matrix_manifest']];mw=inputs[plan['verified_matrix_witness']]
    require(type(inputs[plan['verified_matrix_ROOT']]) is bytes and plan['matrix_ROOT_factual_projection_exact_against_expected_bytes'] is True and facts['passed'] is facts['completed'] is True and facts['blockers']==[] and type(facts['ROOT_observed_terminal_exit_code']) is int and facts['ROOT_observed_terminal_exit_code']==0 and exact([facts['completed_own_numeric_rows'],facts['original_distinct_stock_sites'],facts['completed_own_profile_site_instantiations']],[24,48,96]) and facts['fixed_M']==4608 and facts['manifest_SHA256']==plan['selected_expected_SHA256'][plan['verified_matrix_manifest']], 'Opaque original ROOT bytes plus exact reviewed facts, no large-integer parser bypass')
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and type(mf['inclusive_files']) is int and mf['inclusive_files']==13 and mf['files'][Path(plan['verified_matrix_witness']).name]==plan['selected_expected_SHA256'][plan['verified_matrix_witness']] and mw['passed'] is True and mw['fixed_M']==4608 and mw['native_errors_stock_or_digital_pair_independence_assumed'] is False and exact(mw['selected_source_mappings'],original['fixed_all48_source_mappings']), 'Saved matrix13/full48 original source authority')
    matrix_ast={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse(inputs[plan['verified_matrix_SOURCE']]).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    require(matrix_ast['compose']==plan['matrix_compose_AST_SHA256'] and plan['matrix_A_squared_semantics']=='A_t=alpha*4608+beta;kernel_squared=fixed_power(A_t,2)' and exact(mw['whole48_original_degree12_kernel_bindings'],{p:original['profiles'][p]['fixed_all48_kernel_bindings'] for p in fixed['profiles']}), 'Exact original pointwise alpha/floor kernel lineage; not generic L2 or alpha564')
    cap=inputs[plan['verified_cap_ROOT']];cmf=inputs[plan['verified_cap_manifest']];cw=inputs[plan['verified_cap_witness']]
    require(cap['passed'] is cap['completed'] is cap['virtual_native_and_continuous_cap_preserve_original_strict140_payoff'] is True and cap['ROOT_observed_terminal_exit_code']==0 and cap['manifest_SHA256']==plan['selected_expected_SHA256'][plan['verified_cap_manifest']] and cmf['passed'] is cmf['completed'] is True and cmf['files'][Path(plan['verified_cap_witness']).name]==plan['selected_expected_SHA256'][plan['verified_cap_witness']] and cw['passed'] is cw['upper_clamp_discrepancy_zero_after_fixed_guard'] is cw['global_capped_exponential_Lipschitz564'] is cw['virtual_native_and_continuous_cap_preserve_original_strict140_payoff'] is cw['ideal_closed139_to141_band_unchanged_at_cap564'] is True and cw['native_closed_band_equivalence_claimed'] is False and exact(cw['all48_original_source_mappings'],mw['selected_source_mappings']) and exact(cw['accepted_joint_law_witness'],mw['continuous_product_law_witness']), 'Completed virtual cap proof; native clipped band is not factored')
    native=inputs[plan['runtime_manifest']];sampler=inputs[plan['sampler']];target=inputs[plan['target']];theorem=inputs[plan['native_theorem']]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs'])==2842 and exact([target['width'],target['fraction_bits']],[72,40]) and sampler['original_target_expected_SHA256']==plan['selected_expected_SHA256'][plan['target']] and sampler['pair_count']==30 and sampler['normal_argument_slots']==60 and sampler['digital_pair_independence'] is False and theorem['original_U_V_uniform_cell_coupling'] is theorem['shifted_second_cosine_exact_three_quarter_circular_grid_slot_same_bound'] is True, 'Original uniform tables, midpoint/three-quarter orientation and full72 runtime scope')
    nodes={v:row for row in target['nodes'] for v in row['out']};pairs=sampler['all_original_joint_pair_scopes'];sites=mw['selected_source_mappings'];financial=sampler['complete_original_saved_source_case']['financial_roles']
    require(len(pairs)==30 and {v for row in pairs for v in row['raw_uniform_values']}==set(target['inputs']) and len(target['inputs'])==60 and len(mw['native_normal_family_witnesses'])==30, 'All30 radial/60 distinct uniform source slots')
    for pair,stored in zip(pairs,mw['native_normal_family_witnesses']):
        radius=pair['radius'];minus=nodes[radius-2];positive=nodes[radius-1]
        require(exact(nodes[radius],{'op':'sqrt','args':[radius-1],'params':{},'out':[radius]}) and minus['op']=='cmul' and exact(minus['params'],{'c':-2199023255552}) and positive['op']=='positive' and positive['args']==[radius-2] and len(minus['args'])==1 and stored['normal_values']==pair['normal_values'] and stored['raw_uniform_values']==pair['raw_uniform_values'], 'Actual exact minus2Q/nonnegative radial source followed by unsigned root')
        for value,cosine in zip(pair['normal_values'],pair['cosines']):require(exact(nodes[value],{'op':'mul','args':[radius,cosine['output']],'params':{},'out':[value]}),'Both original radius-cosine products/floors')
        first,second=pair['cosines'];rotation=nodes[second['input']];addition=nodes[rotation['args'][0]]
        require(rotation['op']=='bits' and exact(rotation['params'],{'shift':0,'width':40,'signed':False}) and addition['op']=='add' and len(addition['args'])==2 and first['input'] in addition['args'] and len(set(addition['args']))==2 and all(nodes[v]['op']=='const' and nodes[v]['params']['value']==824633720832 for v in addition['args'] if v!=first['input']), 'Exact circular three-quarter Q40 shift, same Q32 midpoint orientation')
    for v in target['inputs']:require(nodes[v]['op']=='input' and nodes[v]['params']['bits']==32 and nodes[v]['params']['preparation']=='uniform','Separate original uniform preparations')
    require(len(sites)==48 and [(s['contractual_date_one_based'],s['asset_zero_based']) for s in sites]==[(d,a) for d in range(1,13) for a in range(4)], 'All48 exact original stock/prefix roles')
    for row in original['actual_copied_all48_source_rows']:require(all(exact(nodes[v],row) for v in row['out']),'Pinned complete native prefix/clip/kernel source rows')
    clipwords=[nodes[v]['params']['value'] for v in (3490,3491)];require(all(type(v) is int and 0<=v<1<<72 for v in clipwords),'Typed original raw72 clip words')
    signedclip=[v if v<1<<71 else v-(1<<72) for v in clipwords]
    require(signedclip==[-12193974156573,9145480617430] and signedclip[0]<=-11*1099511627776 and signedclip[1]>=8*1099511627776,'Signed-normalized clip and safe ideal lower/virtual cap upper implications; native clip may be active')
    require(exact(nodes[5692],{'op':'cmul','args':[5691],'params':{'c':22906492245},'out':[5692]}) and exact(nodes[5693],{'op':'const','args':[],'params':{'value':109951162777600},'out':[5693]}) and exact(nodes[5694],{'op':'sub','args':[5692,5693],'params':{},'out':[5694]}) and exact(nodes[5695],{'op':'positive','args':[5694],'params':{},'out':[5695]}) and exact(nodes[5696],{'op':'cmul','args':[5695],'params':{'c':1067016148260},'out':[5696]}) and exact(nodes[5697],{'op':'select','args':[5644,5696,13],'params':{},'out':[5697]}),'Original average/strike/positive/strict-survival output')
    primaryraw=inputs[plan['profiles']['primary90']['raw_prefix']]['cases']['B4x12'];indraw=inputs[plan['profiles']['independent130']['raw_prefix']]['B4x12']
    require(primaryraw['every_stored72_raw_partial_sum_safe'] is primaryraw['every_signed144_scaled_normal_product_safe'] is primaryraw['raw_prefix_proof_before_clips_and_survival'] is indraw['every_stored_partial_sum_and_product_safe'] is indraw['every_original_driver_once'] is True and primaryraw['addition_rounding_paid']==0 and indraw['source_reset_or_AS_endpoint_used'] is False,'Saved full partial72/product144 no-wrap, no guard/provider replay')
    for site in sites:
        d=site['contractual_date_one_based'];a=site['asset_zero_based'];prefix=[r for r in financial['prefix_witnesses'] if r['date']==d-1 and r['asset']==a];guard=[r for r in indraw['actual_raw_prefix_word_guards'] if r['value']==site['raw_log']];primary=[r for r in primaryraw['prefixes'] if r['date']==d-1]
        require(len(prefix)==len(guard)==len(primary)==1 and prefix[0]['stock']==site['stock'] and prefix[0]['original_normal_indices']==site['normal_driver_indices']==[5*j+s for j in range(d) for s in (0,a+1)] and prefix[0]['every_driver_multiplicity']==1 and prefix[0]['constants']==[[-1374389535,d],[5063438167381,1]] and site['initial_multiplicity']==1 and site['drift_multiplicity']==d and site['per_path_coefficient_floors']==len(site['normal_driver_records'])==2*d and site['whole_native_prefix_has_no_clip_select_or_reset'] is True and guard[0]['raw_bounds']==primary[0]['actual_raw_log_bounds'][a]==site['native_raw_interval_saved'],'Each48 actual driver/initial/drift/floor and signed interval identity')
    primarycomponents=inputs[plan['profiles']['primary90']['native_components']];radialguard=primarycomponents['original_native_radicand_domain_guard']
    require(type(radialguard) is dict and radialguard['strict_guard_passed'] is radialguard['original_exact_minus2_and_unsigned_root_storage_guards_required_separately'] is True and radialguard['native_source_clipping_inserted'] is False and exact(radialguard['epsilon_l_exact'],primarycomponents['exact_component_allowances']['epsilon_l']), 'Completed original radicand nonnegativity proof shared by the same native source, not old Holder inversion')
    own={}
    for profile,roles in plan['profiles'].items():
        record=inputs[roles['matrix_record']];nc=inputs[roles['native_components']];raw=inputs[roles['raw_prefix']];discount=inputs[roles['discount']];case=raw['cases']['B4x12'] if profile=='primary90' else raw['B4x12'];dc=discount['cases']['B4x12'] if profile=='primary90' else discount['B4x12'];env=inputs[roles['original_kernel_envelope']];kernel=env['cases']['B4x12'] if profile=='primary90' else env['B4x12']
        require(mf['files'][Path(roles['matrix_record']).name]==plan['selected_expected_SHA256'][roles['matrix_record']] and record['profile']==profile and record['fixed_M']==4608 and len(record['date_rows'])==12 and set(record['own_allowed_literal_operands'])=={'aN','bN','ea','eb','e0','ed','tau'},'Own12 saved kernel-square rows and seven literal operands')
        require(nc['all_low_native_product_floor_charged'] is nc['original_unsigned_isqrt_storage_and_product144_nooverflow_required'] is True and native['files'][Path(roles['native_components']).name]==plan['selected_expected_SHA256'][roles['native_components']] and exact(nc['exact_component_allowances']['delta'],[1,4294967296]) and exact(nc['exact_component_allowances']['tau'],[1,1099511627776]), 'Own uniform table/root/product operands from completed native seal')
        require(native['frozen_inputs'][roles['raw_prefix']]==plan['selected_expected_SHA256'][roles['raw_prefix']] and native['frozen_inputs'][roles['discount']]==plan['selected_expected_SHA256'][roles['discount']] and native['frozen_inputs'][roles['original_kernel_envelope']]==plan['selected_expected_SHA256'][roles['original_kernel_envelope']], 'Own raw/literal/discount/full-support kernel archives retain original expected pins')
        if profile=='primary90':require(kernel['whole_clipped_integer_domain_covered'] is kernel['all_positive_stock_stored72_product144_shift_guards_passed'] is kernel['final_negative_shift_floor_charged_once'] is True and kernel['retained_classes']==30,'Original native stock nonnegativity/full72/144/floor contract for all48, needed by cap identity')
        else:require(kernel['original_degree12_Estrin_no_AS_certificate_transfer'] is True and kernel['class_count']==30,'Independent full-domain original kernel, no candidate or generic-L2 promotion')
        rows=[]
        for date,row in enumerate(record['date_rows']):
            current=sites[4*date:4*date+4];ir=inventory['profiles'][profile]['all12_pointwise_kernel_rows'][date]
            require(row['profile']==profile and row['contractual_date_one_based']==date+1 and row['source_stocks']==ir['source_stocks']==[s['stock'] for s in current] and row['source_raw_logs']==ir['source_raw_logs']==[s['raw_log'] for s in current] and ir['kernel_A_squared']['JSON_pointer']=='/date_rows/%d/components/kernel_allowance_squared'%date and len(row['per_stock_instantiations'])==4,'Each saved pointwise A4608-squared has four complete source instantiations')
            for inst,site in zip(row['per_stock_instantiations'],current):require(inst['asset_zero_based']==site['asset_zero_based'] and inst['source_stock']==site['stock'] and inst['source_raw_log']==site['raw_log'] and inst['same_profile_same_mean_variance_and_case_global_kernel'] is True,'Explicit four saved full-domain pointwise kernel/source instantiations')
            rows.append({'contractual_date_one_based':date+1,'source_stocks':row['source_stocks'],'source_raw_logs':row['source_raw_logs'],'source_basket':5576+4*date,'saved_kernel_A_squared':row['components']['kernel_allowance_squared'],'saved_generic_alpha':row['components']['original_generic_alpha'],'saved_generic_beta':row['components']['original_generic_beta']})
        require(type(dc[roles['discount_U_field']]) is list and len(dc[roles['discount_U_field']])==2 and all(type(v) is list and len(v)==2 and all(type(x) is int for x in v) for v in dc[roles['discount_U_field']]) and type(dc[roles['discount_eta_field']]) is list and len(dc[roles['discount_eta_field']])==2,'Own already archived true exp(-3/100) enclosure and literal discrepancy roles')
        if profile=='primary90':require(dc['actual_discount_literal']==nodes[5696]['params']['c'] and exact(dc['final_discount_floor_upper'],[1,1099511627776]) and dc['positive_part_is_1_Lipschitz_and_same_exact_strike'] is True,'Original shared discount literal and paid Q40 floor; each own enclosure remains separate')
        own[profile]={'rows':rows,'literal_pool':record['own_allowed_literal_operands'],'native_uniform':nc['exact_component_allowances'],'raw_original_pairs':{name:case[field] for name,field in roles['raw_fields'].items()},'discount_U':dc[roles['discount_U_field']][1],'discount_eta':dc[roles['discount_eta_field']]}
    witness={'schema':'e11-B4x12-fixed-polar-safe-h128-pointwise-source-witness-v1','passed':True,'accepted_interface':fixed,'original48_source_mappings':sites,'original30_radial_pairs':pairs,'matrix_A_squared_is_pointwise_alpha4608_plus_beta_squared':True,'native_stock_nonnegativity_full_support_required_by_cap_identity':True,'native_radicand_nonnegative_and_exact_minus2Q_root_source_bound':True,'ideal_only_common94_factorization_not_conditioned_on_safe_event':True,'safe_ideal_log_lower_minus6_above_signed_lower_clip_minus11':True,'native_clip_inactivity_assumed':False,'fixed_criterion_failure_keeps_pointwise_test_sealed_and_payoff_mean_None':True,'no_old_stock_tail_Holder_L2_recipe_or_native_provider_replayed':True,'candidate_pricepolicy_estimator_G2_physical_or_advantage_excluded':True}
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
    require(profile in ('primary90','independent130') and exact(plan['interface']['fixed_lambda'],[1,262144]) and exact(plan['interface']['fixed_h_dollars'],[1,128]), 'Only fixed preselected two-profile test')
    value=own[profile];pool={k:limb_ratio(v) for k,v in value['literal_pool'].items()};uniform=value['native_uniform'];tau=ratio(uniform['tau']);delta=ratio(uniform['delta']);el=ratio(uniform['epsilon_l']);ec=ratio(uniform['cosine_table']);lam=Fraction(1,262144);h=Fraction(1,128)
    for key,pairvalue in value['raw_original_pairs'].items():
        expected=Fraction(pairvalue,1099511627776) if key in ('aN','bN') else ratio(pairvalue)
        require(pool[key]==expected,'Same own raw original literal/pool identity, not pointwise old coordinate fields')
    require(pool['tau']==tau and tau==Fraction(1,1099511627776) and delta==Fraction(1,4294967296) and pool['aN']>=0 and pool['bN']>=0,'Explicit fixed units and nonnegative original loading literals')
    radius=plus(times(Fraction(1024),el),tau)
    native_coordinate=plus(plus(times(plus(Fraction(1),ec),radius),times(Fraction(6),ec)),tau)
    midpoint_radius=times(delta,Fraction(32768));midpoint_angle=times(delta,Fraction(132,7));coordinate=plus(native_coordinate,plus(midpoint_radius,midpoint_angle))
    per_increment=plus(plus(times(plus(pool['aN'],pool['bN']),coordinate),times(Fraction(6),plus(pool['ea'],pool['eb']))),plus(pool['ed'],twice(tau)))
    dates=[];stock_sum=Fraction(0)
    for row in value['rows']:
        d=row['contractual_date_one_based'];log_error=plus(pool['e0'],times(Fraction(d),per_increment));A2=limb_ratio(row['saved_kernel_A_squared']);Aup,sw=outward_fixed_sqrt128(A2)
        stock=plus(Aup,times(Fraction(564),log_error));basket=plus(stock,tau);passed=basket<=h
        stock_sum=plus(stock_sum,times(Fraction(4),stock))
        dates.append({'contractual_date_one_based':d,'source_stocks':row['source_stocks'],'source_raw_logs':row['source_raw_logs'],'source_basket':row['source_basket'],'saved_kernel_A_squared':row['saved_kernel_A_squared'],'saved_generic_alpha':row['saved_generic_alpha'],'saved_generic_beta':row['saved_generic_beta'],'components':{k:pair(v) for k,v in {'fixed_sqrt128_pointwise_kernel_upper':Aup,'uniform_raw_log_prefix_error_upper':log_error,'uniform_four_source_cap_stock_error_upper':stock,'uniform_quarter_floor_basket_error_upper':basket,'fixed_h':h}.items()},'pointwise_kernel_sqrt128_witness':sw,'all_four_original_source_bindings_checked':True,'original_quarter_floor_paid_once':True,'fixed_basket_criterion_passed':passed})
    criterion=all(row['fixed_basket_criterion_passed'] for row in dates)
    U=ratio(value['discount_U']);eta=ratio(value['discount_eta']);bad=times(Fraction(60),lam);band=times(Fraction(1,1176),plus(Fraction(1),Fraction(1,963379197)));prob=min(Fraction(1),plus(bad,band))
    average=plus(times(stock_sum,Fraction(1,48)),times(Fraction(9025),tau));smooth=plus(plus(times(U,average),times(Fraction(40),eta)),tau)
    conditional_mean=plus(smooth,times(Fraction(40),prob)) if criterion else None
    components={'fixed_lambda':lam,'fixed_h':h,'own_uniform_log_error_epsilon_l':el,'own_uniform_cosine_error':ec,'native_radius_pointwise_error_upper':radius,'native_coordinate_pointwise_error_upper':native_coordinate,'midpoint_radius_error_upper':midpoint_radius,'midpoint_angular_error_upper':midpoint_angle,'complete_coordinate_pointwise_error_upper':coordinate,'raw_log_per_increment_error_upper':per_increment,'sum48_pointwise_stock_error_upper':stock_sum,'average_pointwise_error_upper':average,'own_discount_U':U,'own_discount_literal_error_eta':eta,'native_discount_floor_tau':tau,'polar_bad_event_probability_upper':bad,'fixed_ideal_band_probability_upper':band}
    return {'schema':'e11-B4x12-fixed-polar-safe-h128-pointwise-feasibility-limb-profile-v1','profile':profile,'fixed_lambda':[1,262144],'fixed_h_dollars':[1,128],'own_pointwise_date_rows':12,'original_stock_source_instantiations':48,'components':{k:pair(v) for k,v in components.items()},'date_rows':dates,'all12_fixed_basket_criterion_passed':criterion,'outcome':'conditional_payoff_mean_certificate' if criterion else 'negative_fixed_criterion_feasibility','conditional_mismatch_probability_upper':pair(prob) if criterion else None,'conditional_smooth_survival_payoff_error_upper':pair(smooth) if criterion else None,'conditional_full_payoff_mean_bias_upper':pair(conditional_mean) if criterion else None,'all_pointwise_certificates_kept_when_fixed_criterion_fails':True,'full_payoff_mean_certificate_adopted':criterion,'accuracy_policy_adopted':False,'all12_simultaneous_on_same_fixed_safe_event':True,'ideal_band_factorization_conditioned_on_safe_event':False,'P_safe_intersect_band_bounded_by_unconditional_ideal_band':True,'native_errors_or_stocks_independence_assumed':False,'native_clipping_inactive_assumed':False,'adaptive_lambda_h_or_retry_or_cross_profile_selection':False,'old_tail_moment_Holder_native_kernel_or_provider_recipe_replayed':False,'actual_bias_price_lower_bound_estimator_G2_physical_or_advantage':False}

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
    require(CURRENT_FIXED_POLAR_SAFE_AUTHORING_AND_PROOF_BOUND is True, 'Dormant parent pins must be completed before own current ROOT release')
    try:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ready-sha256',required=True);args=parser.parse_args()
        base=Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True)==ROOT and Path(__file__).resolve(strict=True)==SOURCE,'Exact isolated default4300')
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256],'Separate original base argv0/venv and exact current absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(),'Pinned isolated paths/no ZIP/no site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(),'Unused own output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','fixed_polar_safe_h128_execution_authorized','fixed_polar_safe_h128_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-fixed-polar-safe-h128-uniform-error-test-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['fixed_polar_safe_h128_execution_authorized'] is True,'Own current tighter hquarter band saved-chain release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name},'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(plan['caps']==ready['caps']==[180,150,600] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']),'Exact current adapter/RSS/caps/ledger/reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['fixed_polar_safe_h128_transfer_witness_accepted'] is True and review['pointwise_A4608_squared_kernel_lineage_accepted'] is True and review['criterion_failure_is_sealed_negative_feasibility'] is True and review['factual_projection_exact_against_verified_matrix_ROOT'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER,'All3 current full-role reviews before premises/origins/numbers')
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
        files['fixed_polar_safe_h128_source_pointwise_witness.json']=save('fixed_polar_safe_h128_source_pointwise_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_fixed_polar_safe_h128_uniform_error_feasibility.json']=save('primary_fixed_polar_safe_h128_uniform_error_feasibility.json',primary)
        files['independent_fixed_polar_safe_h128_uniform_error_feasibility.json']=save('independent_fixed_polar_safe_h128_uniform_error_feasibility.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed': True, 'profiles_kept_separate': True, 'fixed_lambda_and_h_before_pointwise_numerics': True, 'own24_pointwise_date_rows_and96_source_instantiations': True, 'negative_fixed_criterion_retains_valid_pointwise_test_records': True, 'no_adaptive_lambda_h_fallback_or_cross_profile_selection': True, 'ideal_band_not_conditioned_on_safe_event': True, 'no_old_stock_tail_moment_Holder_native_kernel_or_provider_recipe_replay': True, 'no_price_policy_estimator_G2_physical_or_advantage_adoption': True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected,'Every declared original stat8 retained after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        owned_guard()
        summary={'schema':'e11-fixed-polar-safe-h128-uniform-error-feasibility-reference-summary-v1','passed':True,'completed':True,'completed_fixed_uniform_test':True,'profile_result_files':[{'filename':name,'expected_SHA256':files[name],'bytes':(OUTPUT/name).stat().st_size,'profile':profile,'own_pointwise_date_rows':12,'original_stock_source_instantiations':48} for profile,name in [('primary90','primary_fixed_polar_safe_h128_uniform_error_feasibility.json'),('independent130','independent_fixed_polar_safe_h128_uniform_error_feasibility.json')]],'profile_outcomes':[{'profile':row['profile'],'all12_fixed_basket_criterion_passed':row['all12_fixed_basket_criterion_passed'],'outcome':row['outcome'],'full_payoff_mean_certificate_adopted':row['full_payoff_mean_certificate_adopted']} for row in (primary,independent)],'completed_own_pointwise_date_rows':24,'completed_own_profile_site_instantiations':96,'original_distinct_stock_sites':48,'source_full_payoff':5697,'controls_file':{'filename':'five_metadata_controls.json','expected_SHA256':files['five_metadata_controls.json']},'witness_file':{'filename':'fixed_polar_safe_h128_source_pointwise_witness.json','expected_SHA256':files['fixed_polar_safe_h128_source_pointwise_witness.json']},'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','fixed_criterion_failure_is_negative_feasibility_not_scientific_crash':True,'new_stock_kernel_tail_moment_native_or_provider_recipe_replayed':False,'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'accuracy_policy_estimator_physical_G2_or_advantage_results':None}
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
