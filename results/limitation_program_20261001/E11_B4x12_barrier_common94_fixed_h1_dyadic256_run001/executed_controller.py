"""Dormant original strict barrier mismatch; fixed h1 and outward dyadic256 only."""
# Completed basket ROOT22308d supplies two separate own12-row records and the original joint coupling.
# Accepted barrier prospectus b428fed0/917a3ea1; independent proof-only peer901df6f3 is ancestry, not SCI permission.
# Upfront h1/grid256: sum12 rounded own basket bounds +20/139; cap at1 only. No extra rounding gap/Young/adaptive selection.
# Current SOURCE gateFalse; future current ROOT/READY/terminal/manifest/results remain None. No SCI authorization.

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
SOURCE = ROOT/'research/limitation_program_20261001/experiment_e11_b4x12_barrier_common94_fixed_h1_dyadic256_v1.py'
PLAN = ROOT/'.context/E11_B4X12_BARRIER_COMMON94_FIXED_H1_DYADIC256_INPUT_ADAPTER_run001.json'
MD = ROOT/'.context/E11_B4X12_BARRIER_COMMON94_FIXED_H1_DYADIC256_PREFLIGHT_run001.md'
READY = ROOT/'.context/E11_B4X12_BARRIER_COMMON94_FIXED_H1_DYADIC256_ROOT_READY_run001.json'
OUTPUT = ROOT/'results/limitation_program_20261001/E11_B4x12_barrier_common94_fixed_h1_dyadic256_run001'
LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'original12_maximum_common94_and_fixed_band_witness.json', 'five_metadata_controls.json', 'primary_barrier_fixed_h1_dyadic256_mismatch_probability.json', 'independent_barrier_fixed_h1_dyadic256_mismatch_probability.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']
CPU, ADMISSION, WALL = (180,150,600)
_STARTED = None
_OWNS_OUTPUT = False
_OUTPUT_ID = None
CURRENT_BARRIER_AUTHORING_AND_PROOF_BOUND = True


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
    require(CURRENT_BARRIER_AUTHORING_AND_PROOF_BOUND is True, 'Dormant until ROOT accepts exact current SOURCE and closed release')
    fixed={'case':'B4x12','W':72,'F':40,'source_max':5642,'source_barrier_literal':5643,'source_strict_survival_flag':5644,'H_dollars':[140,1],'h_dollars':[1,1],'shared_first_ideal_normal_source':94,'shared_ideal_scalar_index':0,'ideal_common_loading_squared':[3,1000],'grid_exponent_fixed':256,'outward_rounding_before_addition':True,'profiles':['primary90','independent130'],'own_profile_rows':2,'own_basket_inputs_each_profile':12,'quantity':'survival_indicator_mismatch_probability','units':'probability','stock_date_native_or_error_independence_assumed':False,'ideal_joint_independence_only':True,'adaptive_h_grid_or_cross_profile_selection':False,'financial_price_discount_payoff_or_G2_scope':False}
    require(ready['barrier_common94_fixed_h1_dyadic256_transfer_witness_accepted'] is True and exact(ready['interface'],plan['interface']) and exact(plan['interface'],fixed), 'One fixed original barrier indicator contract')
    root_key=plan['verified_basket_ROOT'];root_bytes=inputs[root_key];facts=plan['verified_basket_ROOT_metadata_facts']
    require(type(root_bytes) is bytes and plan['selected_input_modes'][root_key]=='plain_text_only' and plan['basket_ROOT_factual_projection_exact_against_expected_bytes'] is True, 'Completed basket ROOT opaque bytes; exact typed facts checked in current3 reviews')
    require(facts['passed'] is facts['completed'] is True and facts['blockers']==[] and type(facts['ROOT_observed_terminal_exit_code']) is int and facts['ROOT_observed_terminal_exit_code']==0 and facts['manifest_SHA256']==plan['selected_expected_SHA256'][plan['verified_basket_manifest']] and facts['SOURCE_SHA256']==plan['verified_basket_SOURCE_SHA256'] and exact([facts['completed_own_numeric_rows'],facts['original_distinct_basket_sites'],facts['own_four_stock_certificate_joins']],[24,12,96]), 'Completed own12 baskets in each profile, no permission inherited')
    mf=inputs[plan['verified_basket_manifest']];bw=inputs[plan['verified_basket_witness']]
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['inclusive_files']==13 and set(mf['files'])==set(plan['verified_basket_exact13_ledger'])-{'manifest.json'} and mf['files'][Path(plan['verified_basket_witness']).name]==plan['selected_expected_SHA256'][plan['verified_basket_witness']], 'Exact completed parent owner and witness member')
    require(bw['schema']=='e11-B4x12-twelve-native-basket-common-coupling-source-witness-v1' and bw['passed'] is bw['floor_paid_once_not_assumed_exact_divisibility'] is bw['no_independence_adaptive_minimum_or_adoption'] is True and exact(bw['accepted_interface'],facts['accepted_interface']) and exact(bw['source_results'],plan['original12_basket_source_joins']), 'Saved original basket source/no-wrap/floor joins, no basket recipe replay')
    require(exact([bw['signed_word_bits'],bw['whole_product_bits'],bw['original_full48_native_positive_stock_bound']],[72,144,4503599627354112]), 'Bounded native positive inputs to literal maximum')
    prospective=inputs[plan['historical_prospectus']]
    require(prospective['schema']=='e11-b4x12-barrier-common94-fixed-h1-prospective-plan-v1' and prospective['metadata_only'] is True and prospective['scientific_evaluation_performed'] is prospective['SOURCE_READY_SCI_or_result_authorized'] is False and exact(prospective['all48_shared_first_common94_source_joins'],plan['all48_shared_first_common94_source_joins']) and exact(prospective['exact11_original_maximum_LT_SELECT_joins'],plan['exact11_original_maximum_LT_SELECT_joins']), 'Frozen symbolic proof only, fresh route fixed in current packet')
    sw=inputs[plan['verified_stock_source_witness']];mp=inputs[plan['verified_stock_source_plan']];sampler=inputs[plan['native_sampler_binding']]
    law=bw['continuous_product_law_witness']
    require(exact(law,sw['continuous_product_law_witness']) and exact(law,mp['continuous_product_law_witness']) and exact(law,plan['accepted_joint_law_witness']) and law['ideal_only'] is True and law['digital_or_error_independence'] is False and law['polar_jacobian']=='exp(-(z0^2+z1^2)/2)/(2pi)=phi(z0)*phi(z1)', 'Full joint reference law, not scalar marginals or native error independence')
    require(exact(mp['ideal_law_constants']['a_squared'],[3,1000]) and sw['passed'] is True and exact(mp['fixed_all48_source_mappings'],sw['selected_source_mappings']), 'Saved positive ideal loading and all48 source mapping')
    native=inputs[plan['runtime_manifest']];target=inputs[plan['target']]
    require(native['passed'] is native['completed'] is True and len(native['external_runtime_inputs'])==2842 and exact([target['width'],target['fraction_bits']],[72,40]), 'Original full72 target and fixed runtime citation')
    for key in plan['source_semantics_citations']:
        require(type(inputs[key]) is bytes and plan['selected_input_modes'][key]=='plaintext_AST_only' and native['frozen_inputs'][key]==plan['selected_expected_SHA256'][key], 'Expected plaintext source/model citations never imported or called')
    pairs=sampler['all_original_joint_pair_scopes']
    require(len(pairs)==30 and pairs[0]['normal_values']==[94,125] and len({v for pair in pairs for v in pair['raw_uniform_values']})==60 and len({v for pair in pairs for v in pair['normal_values']})==60 and {v for pair in pairs for v in pair['raw_uniform_values']}==set(target['inputs']), 'Thirty disjoint pairs cover original60 inputs; ideal94 independent of partner125')
    nodes={v:n for n in target['nodes'] for v in n['out']};joins=plan['all48_shared_first_common94_source_joins'];sites=mp['fixed_all48_source_mappings']
    require(len(sites)==len(joins)==48 and len({s['stock'] for s in sites})==48, 'All original12x4 stocks, not a subset')
    for site,join in zip(sites,joins):
        drivers=site['normal_driver_records'];shared=[r for r in drivers if r['normal']==94]
        require(len(shared)==1 and exact(shared[0],{'cmul_floor_node':3492,'coefficient_raw':60222732077,'driver_role':'common','innovation_date_zero_based':0,'normal':94,'orientation':'cosine','pair':0,'scalar_index':0}) and site['whole_native_prefix_has_no_clip_select_or_reset'] is True, 'Shared first common94 once, no prefix reset or clipping')
        counts={};stack=[site['raw_log']]
        while stack:
            budget();node=nodes[stack.pop()]
            if node['op']=='add':stack.extend(node['args'])
            elif node['op']=='cmul':counts[node['out'][0]]=counts.get(node['out'][0],0)+1
            else:require(node['op']=='const', 'Original raw prefix is only additions, fixed coefficients and constants')
        require(counts=={r['cmul_floor_node']:1 for r in drivers} and counts[3492]==1 and all(exact(nodes[r['cmul_floor_node']],{'op':'cmul','args':[r['normal']],'params':{'c':r['coefficient_raw']},'out':[r['cmul_floor_node']]}) for r in drivers), 'Every declared raw innovation once, literal native coefficient is not exact ideal a')
        expected={'date_zero_based':site['date_zero_based'],'asset_zero_based':site['asset_zero_based'],'source_raw_log':site['raw_log'],'source_stock':site['stock'],'shared_first_common_normal':94,'shared_native_cmul':3492,'native_coefficient_raw':60222732077,'actual_additive_prefix_multiplicity':1,'ideal_positive_loading_symbol':'a','ideal_loading_squared':[3,1000]}
        require(exact(join,expected), 'Each exact original common-factor source join')
    basket_ids=[row['source_basket'] for row in bw['source_results']]
    require(exact(basket_ids,facts['accepted_interface']['source_baskets']) and exact(basket_ids,plan['native_maximum_leaf_order']) and len(basket_ids)==12, 'All12 original dates included once')
    maxima=plan['exact11_original_maximum_LT_SELECT_joins'];maximum_ids=[]
    require(len(maxima)==11, 'Exact11 max operations')
    for join in maxima:
        row=join['select'];lt=join['strict_lt'];flag,right,left=row['args']
        require(exact(nodes[row['out'][0]],row) and row['op']=='select' and row['params']=={} and exact(lt,{'op':'lt','args':[left,right],'params':{},'out':[flag]}) and exact(nodes[flag],lt), 'Literal strict LT/SELECT is max; equal values remain equal')
        maximum_ids.append(row['out'][0])
    leaves=[];stack=[5642]
    while stack:
        value=stack.pop()
        if value in basket_ids:leaves.append(value)
        else:
            require(value in maximum_ids, 'Maximum uses only declared tree or baskets');node=nodes[value];stack.extend([node['args'][1],node['args'][2]])
    require(exact(leaves,basket_ids) and exact(nodes[5643],{'op':'const','args':[],'params':{'value':153931627888640},'out':[5643]}) and exact(nodes[5644],{'op':'lt','args':[5642,5643],'params':{},'out':[5644]}), 'Original maximum all12 once and strict140Q barrier, equality retained as mismatch risk')
    own={}
    require(set(plan['profiles'])=={'primary90','independent130'}, 'Exactly two own profile records')
    for profile,role in plan['profiles'].items():
        record=inputs[role['verified_basket_record']]
        require(mf['files'][Path(role['verified_basket_record']).name]==plan['selected_expected_SHA256'][role['verified_basket_record']] and record['schema']=='e11-B4x12-twelve-native-basket-squared-L2-limb-matrix-v1' and record['profile']==profile and record['units']=='dollars_squared' and record['own_numeric_row_count']==12 and exact(record['source_baskets'],basket_ids) and len(record['date_rows'])==12 and record['same_original_continuous_four_stock_average_reference'] is True and record['stock_error_independence_assumed'] is record['old_stock_raw_tail_kernel_native_or_provider_recipe_replayed'] is record['adaptive_minimum_fallback_or_improvement_adoption'] is False, 'Own physically saved basket allowances, not other profile minimum')
        certificates=[]
        for date,row in enumerate(record['date_rows']):
            source=bw['source_results'][date]
            require(row['schema']=='e11-B4x12-original-date-native-basket-squared-L2-limb-row-v1' and row['profile']==profile and row['units']=='dollars_squared' and row['contractual_date_one_based']==date+1 and row['source_basket']==basket_ids[date] and exact(row['source_stocks'],source['source_stocks']) and row['grouped_equals_distributed'] is row['floor_error_paid_without_exact_divisibility'] is True and row['stock_error_independence_assumed'] is row['adaptive_or_improvement_adoption'] is False and exact(row['components']['basket_squared_L2_upper'],row['components']['independent_distributed_expression']), 'Each own source/date and already paid basket floor')
            pointer={'date_zero_based':date,'source_basket':basket_ids[date],'bound_JSON_pointer':'/date_rows/%d/components/basket_squared_L2_upper'%date}
            require(exact(role['own_Bj_pointers'][date],pointer), 'Exact own saved field pointer before reconstruction')
            certificates.append(dict(pointer,basket_allowance=row['components']['basket_squared_L2_upper']))
        own[profile]=certificates
    witness={'schema':'e11-B4x12-barrier-common94-fixed-h1-dyadic256-source-witness-v1','passed':True,'accepted_interface':fixed,'shared_first_common94_once_in_all48':True,'accepted_joint_law_witness':law,'ideal_unclipped_common_factor_only':True,'log_ideal_maximum_equals_aZ94_plus_independent_rest':True,'native_clipped_stock_factorization_claimed':False,'conditional_log_max_density_upper_symbolic':'1/(a*sqrt(2*pi))','fixed_band_rational':[20,139],'closed_band_includes_equalities':True,'exact_maximum_rows':maxima,'source_baskets':basket_ids,'source_max':5642,'source_strict_survival_flag':5644,'maximum_adds_no_floor':True,'basket_floor_already_paid':True,'dependence_safe_union_and_squared_error_Markov':True,'stock_date_native_or_error_independence_assumed':False,'grid_exponent_fixed':256,'h_dollars_fixed':[1,1],'outward_rounding_before12_additions':True,'rounding_gap_already_paid_in_operands':True,'no_second_gap_or_extra_Young_factor':True,'ideal_loading_literal_not_native_coefficient_square':True,'money_payoff_discount_price_G2_or_advantage_excluded':True}
    return witness,own


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

def compose(profile, plan, own):
    require(profile in ('primary90','independent130') and exact(plan['interface']['h_dollars'],[1,1]) and plan['interface']['grid_exponent_fixed']==256 and plan['interface']['adaptive_h_grid_or_cross_profile_selection'] is False, 'One upfront h1/grid256 route; no fallback')
    certificates=own[profile]
    require(len(certificates)==12 and [c['date_zero_based'] for c in certificates]==list(range(12)), 'All12 own dates before any arithmetic')
    original=[limb_ratio(c['basket_allowance']) for c in certificates];rounded=[];rounding=[]
    for index,value in enumerate(original):
        upper,witness=outward_fixed_dyadic(value,256);rounded.append(upper);rounding.append(dict(witness,own_operand_index=index,source_basket=certificates[index]['source_basket']))
    ordered=rounded if profile=='primary90' else list(reversed(rounded))
    total=Fraction(0)
    for value in ordered:total=plus(total,value)
    band=Fraction(20,139);raw=plus(total,band)
    expanded=band
    for value in ordered:expanded=plus(expanded,value)
    require(raw==expanded and ((139<<256)%raw.denominator)==0, 'Fixed outward union/Markov sum plus band; denominator divides139*2^256')
    capped=raw if raw<=1 else Fraction(1)
    strength={'raw_probability_upper_lt_one':raw<1,'probability_cap_active':raw>1,'no_threshold_or_accuracy_adoption':True}
    components={'original_twelve_basket_allowances':[pair(v) for v in original],'outward_fixed_dyadic256_basket_allowances':[pair(v) for v in rounded],'sum_rounded_basket_allowances':pair(total),'fixed_band_upper':pair(band),'uncapped_mismatch_probability_upper':pair(raw),'independent_distributed_expression':pair(expanded),'capped_mismatch_probability_upper':pair(capped)}
    return {'schema':'e11-B4x12-barrier-common94-fixed-h1-dyadic256-probability-limb-row-v1','profile':profile,'units':'probability','source_max':5642,'source_strict_survival_flag':5644,'components':components,'own_Bj_source_bindings':[{k:c[k] for k in ('date_zero_based','source_basket','bound_JSON_pointer')} for c in certificates],'fixed_outward_rounding_operand_witnesses':rounding,'own_basket_allowance_count':12,'own_numeric_row_count':1,'H_dollars_fixed':[140,1],'h_dollars_fixed':[1,1],'grid_exponent_fixed':256,'chosen_formula':'min(1,sum12 ceil(2^256*B_j)/2^256 + 20/139)','uncapped_grouped_equals_distributed':True,'probability_cap_at_one_only':True,'strength_diagnostic':strength,'outward_rounding_before_all12_additions':True,'rounding_gap_already_paid_in_outward_operands':True,'second_rounding_gap_or_extra_Young_factor_added':False,'old_exact_aggregate_reconstructed_or_required':False,'numerator_or_CPU_feasibility_certified_by_denominator_proof':False,'stock_date_native_or_error_independence_assumed':False,'adaptive_h_grid_or_cross_profile_minimum':False,'native_stock_factorization_claimed':False,'stock_basket_tail_moment_kernel_or_provider_recipe_replayed':False,'money_payoff_discount_price_G2_or_advantage_claimed':False}


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
    require(CURRENT_BARRIER_AUTHORING_AND_PROOF_BOUND is True, 'Disabled draft, no current proof/release permission')
    try:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ready-sha256',required=True);args=parser.parse_args()
        base=Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True)==ROOT and Path(__file__).resolve(strict=True)==SOURCE, 'Exact isolated default4300')
        require(Path(sys.executable).resolve(strict=True)==ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True)==base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True)==base/'python.exe' and sys.orig_argv[1:]==['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256], 'Separate base argv0/venv and exact absolute command')
        require(sys.path==[str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(), 'Pinned isolated paths/no ZIP/site')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(), 'Unused output namespace')
        records={};ready=decode(read_bytes(READY,args.ready_sha256,records))
        keys={'schema','ready','root_and_independent_static_reviews_passed','barrier_common94_fixed_h1_dyadic256_execution_authorized','barrier_common94_fixed_h1_dyadic256_transfer_witness_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready)==keys and ready['schema']=='root-e11-barrier-common94-fixed-h1-dyadic256-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['barrier_common94_fixed_h1_dyadic256_execution_authorized'] is True, 'Own closed14 ROOT barrier release only')
        authors=ready['author_method_SHA256'];require(set(authors)=={SOURCE.name,PLAN.name,MD.name}, 'Current author trio')
        source_raw=read_bytes(SOURCE,authors[SOURCE.name],records);plan_raw=read_bytes(PLAN,authors[PLAN.name],records);md_raw=read_bytes(MD,authors[MD.name],records);plan=decode(plan_raw)
        require(exact(plan['caps'],[180,150,600]) and ready['caps']==plan['caps'] and plan['resident_set_bytes']==157286400 and plan['default_decimal_digits']==4300 and plan['exact13_inclusive_ledger']==ready['exact13_inclusive_ledger']==LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256'])==set(plan['current_review_paths']), 'Fixed adapter/caps/RSS/13ledger/current3')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review=decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers']==[] and review['author_method_SHA256']==authors and review['complete_definition_AST_SHA256']==ready['definition_AST_SHA256'] and review['selected_expected_SHA256']==plan['selected_expected_SHA256'] and exact(review['accepted_interface'],plan['interface']) and review['barrier_common94_fixed_h1_dyadic256_transfer_witness_accepted'] is True and review['factual_projection_exact_against_verified_basket_ROOT'] is True and review['caps']==plan['caps'] and review['exact13_inclusive_ledger']==LEDGER, 'All3 current source/science/projection reviews before premises and arithmetic')
        code_guard(source_raw,ready)
        caches=['research/limitation_program_20261001/__pycache__/'+SOURCE.stem+'.cpython-312'+s+'.pyc' for s in ('','.opt-1','.opt-2')]
        require(ready['existing_current_cache_SHA256']=={} and ready['absent_current_cache_paths']==sorted(caches) and all(not (ROOT/k).exists() and not (ROOT/k).is_symlink() for k in caches), 'Exact absent current3 caches')
        inputs={}
        for key,pin in plan['selected_expected_SHA256'].items():
            data=read_bytes(ROOT/key,pin,records);mode=plan['selected_input_modes'][key]
            require(mode in ('ordinary_json','plaintext_AST_only','plain_text_only') and stat8(ROOT/key)==plan['selected_original_8_field_fingerprints'][key], 'Closed selected parsing role and original stat8, no arrays')
            inputs[key]=decode(data) if mode=='ordinary_json' else data
        origins=loaded_origins(inputs[plan['runtime_manifest']],records)
        witness,own=interface_witness(plan,ready,inputs);controls=controls_record(plan)
        code_guard(source_raw,ready);budget(admission=True)
        OUTPUT.mkdir(exist_ok=False);_OUTPUT_ID=[stat8(OUTPUT)[i] for i in (0,1,4,5,6,7)];_OWNS_OUTPUT=True
        files={}
        for name,data in [('executed_controller.py',source_raw),('executed_adapter.json',plan_raw),('executed_preflight.md',md_raw),('executed_ROOT_READY.json',read_bytes(READY,args.ready_sha256,records))]:files[name]=save(name,raw=data)
        files['run_started.json']=save('run_started.json',{'created_UTC_ns':time.time_ns(),'PID':os.getpid(),'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'default4300_no_setter':True,'current3_bound_before_premises_origins_numbers_output':True})
        files['original12_maximum_common94_and_fixed_band_witness.json']=save('original12_maximum_common94_and_fixed_band_witness.json',witness)
        files['five_metadata_controls.json']=save('five_metadata_controls.json',controls)
        primary=compose('primary90',plan,own);independent=compose('independent130',plan,own)
        files['primary_barrier_fixed_h1_dyadic256_mismatch_probability.json']=save('primary_barrier_fixed_h1_dyadic256_mismatch_probability.json',primary)
        files['independent_barrier_fixed_h1_dyadic256_mismatch_probability.json']=save('independent_barrier_fixed_h1_dyadic256_mismatch_probability.json',independent)
        files['same_profile_reconciliation.json']=save('same_profile_reconciliation.json',{'passed':True,'profiles_kept_separate':True,'both_own12_basket_allowances_only':True,'no_cross_profile_minimum':True,'h1_grid256_fixed_before_arithmetic':True,'rounding_before_addition_no_second_gap':True,'probability_cap_at_one_only':True,'no_independence_or_extra_Young_factor':True,'no_old_recipe_replayed':True})
        for key,row in tuple(records.items()):read_bytes(Path(key),row['expected_SHA256'],records)
        for key,expected in plan['selected_original_8_field_fingerprints'].items():require(stat8(ROOT/key)==expected, 'Every original stat8 after uncached byte pass')
        code_guard(source_raw,ready)
        files['selected_premise_authority.json']=save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'selected_input_modes':plan['selected_input_modes'],'selected_original_8_field_fingerprints':plan['selected_original_8_field_fingerprints'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary={'passed':True,'completed':True,'profile_results':[primary,independent],'completed_own_numeric_rows':2,'original_strict_barrier_flag':5644,'original_distinct_barrier_sites':1,'controls':controls,'witness':witness,'caps':[CPU,ADMISSION,WALL],'resident_set_bytes':157286400,'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'preseal_current_or_peak_RSS_bytes':rss_bytes(),'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0,'default4300_without_setter_or_parser_bypass_science':True,'new_rational_output_encoding':'canonical-nonnegative-rational-base2p32-v1','fixed_h1_dyadic256_route':True,'old_exact_aggregate_reconstructed_or_required':False,'stock_basket_native_tail_moment_kernel_or_provider_recipe_replayed':False,'money_payoff_discount_price_G2_candidate_results':None}
        files['summary.json']=save('summary.json',summary)
        require(set(files)==set(LEDGER)-{'manifest.json'} and {p.name for p in OUTPUT.iterdir()}==set(files), 'Exact preseal12/no failure')
        manifest={'passed':True,'completed':True,'budget_censored':False,'files':files,'manifest_self_hash_excluded':True,'inclusive_files':13,'author_method_SHA256':authors,'ROOT_READY_expected_SHA256':args.ready_sha256,'selected_expected_SHA256':plan['selected_expected_SHA256'],'financial_price_policy_G2_or_quantum_advantage':False,'fixture_credit':0}
        seal=save('manifest.json',manifest);require({p.name for p in OUTPUT.iterdir()}==set(LEDGER), 'Exact sealed13/no failure');budget()
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
