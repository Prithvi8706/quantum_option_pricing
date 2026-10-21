'Dormant one-site A13 logical caller and conditional certificate join; compiled shift phase remains open.'

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

SOURCE = ROOT / 'research/limitation_program_20261001/experiment_a13_first_stock_source_boundary_v2.py'

PLAN = ROOT / '.context/A13_FIRST_STOCK_SOURCE_BOUNDARY_V2_INPUT_ADAPTER_run001.json'

MD = ROOT / '.context/A13_FIRST_STOCK_SOURCE_BOUNDARY_V2_PREFLIGHT_run001.md'

READY = ROOT / '.context/A13_FIRST_STOCK_SOURCE_BOUNDARY_V2_ROOT_READY_run001.json'

OUTPUT = ROOT / 'results/limitation_program_20261001/A13_first_stock_source_boundary_run002'

LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'source_and_premise_witness.json', 'positive_first_controls.json', 'complete_class_and_cell_bridge.json', 'fixed_logical_caller_cases.json', 'qualification.json', 'selected_premise_authority.json', 'summary.json', 'manifest.json']

CPU, ADMISSION, WALL = (180, 150, 600)

_STARTED = None

_OWNS_OUTPUT = False

_OUTPUT_ID = None




GRAPH = ((6, "mul", 0, 2), (7, "add", 1, 6), (8, "mul", 0, 4),
         (9, "add", 3, 8), (10, "mul", 0, 0), (11, "mul", 10, 9),
         (12, "add", 7, 11), (13, "mul", 10, 10),
         (14, "mul", 13, 5), (15, "add", 12, 14))

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

def signed(value, width):
    require(type(value) is int and 0 <= value < 1 << width, "Exact raw word")
    return value - (1 << width) if value >> (width - 1) else value

def native_oracle(raw, table, thresholds, width=72, fraction=40):
    mask = (1 << width) - 1
    r = signed(raw, width)
    segment = sum(r >= threshold for threshold in thresholds)
    row = table[segment]
    values = [(r - row[0]) & mask] + [coefficient & mask for coefficient in row[1:]]
    for value, op, a, b in GRAPH:
        require(value == len(values), "Exact independent sixteen-node order")
        x, y = signed(values[a], width), signed(values[b], width)
        values.append(((x * y >> fraction) if op == "mul" else x + y) & mask)
    return segment, values

def scope_validator(value, expected):
    require(type(value) is dict and set(value) == set(expected), 'CALLER_INTERFACE_KEYS')
    for key in expected:
        require(exact(value[key], expected[key]), 'CALLER_' + key.upper())

def controls_record(plan):
    scope_validator(plan['interface'], plan['interface'])
    rows = []
    for specification in plan['controls']:
        bad = dict(plan['interface'])
        bad[specification['field']] = specification['bad']
        try:
            scope_validator(bad, plan['interface'])
        except AssertionError as error:
            require(str(error) == specification['tag'], 'Exact positive-first caller control predicate')
            rows.append({'field': specification['field'], 'rejected': True, 'tag': str(error), 'positive_validated_first': True})
        else:
            raise AssertionError('Current caller control failed to reject')
    require(len(rows) == 4, 'Exactly four current control categories')
    return {'passed': True, 'categories': 4, 'variants': rows}

def signed_shift(value, exponent):
    require(type(value) is type(exponent) is int and -(1 << 71) <= value < 1 << 71, 'Exact full72 signed shift input')
    result = 0 if exponent >= 72 else (-1 if value < 0 else 0) if exponent <= -72 else value << exponent if exponent >= 0 else value >> -exponent
    return result & ((1 << 72) - 1)

def source_witness(plan, inputs):
    target = inputs[plan['roles']['original_target']]
    binding = inputs[plan['roles']['original_domain_binding']]
    site = binding['cases']['B4x12']['stock_sites'][0]
    require(target['width'] == 72 and target['fraction_bits'] == 40 and exact(site, plan['original_site']), 'Exact B4 first stock source ABI')
    rows = {value: row for row in target['nodes'] for value in row['out']}
    for row in plan['original_boundary_rows']:
        require(all(exact(rows[value], row) for value in row['out']), 'Copied original clip reduction polynomial boundary and shift rows')
    low_raw, high_raw = rows[3490]['params']['value'], rows[3491]['params']['value']
    require(type(low_raw) is type(high_raw) is int and 0 <= low_raw < 1 << 72 and 0 <= high_raw < 1 << 72, 'Exact stored raw72 clip constant types and ranges')
    require(signed(low_raw, 72) == site['low'] and signed(high_raw, 72) == site['high'], 'Original stored clip endpoints decoded as signed72')
    require(binding['fixed30_classes_retained'] is True and binding['generic_zero_to_ln2_domain_assumed'] is False, 'Retain original classes including endpoint discrepancy')
    originals = plan['original_SOURCE_AST_witnesses']
    for key, witness in originals.items():
        path, name = key.split('::')
        module = ast.parse(inputs[path])
        definition = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == name)
        require(hashlib.sha256(ast.dump(definition, include_attributes=False).encode()).hexdigest() == witness['normalized_AST_SHA256'], 'Original source branch copied AST')
    require(rows[4021]['op'] == 'shift' and rows[4021]['args'] == [4020, 3979], 'Only original polynomial argument is replaced')
    return {'passed': True, 'schema': 'a13-first-stock-logical-source-witness-v1', 'case': 'B4x12', 'asset': 0, 'date': 1, 'raw_log': 3542, 'clipped': 3579, 'exponent': 3979, 'remainder': 3982, 'old_polynomial': 4020, 'new_tested_polynomial': 15, 'stock': 4021, 'old_degree12_alpha_used': False, 'original_signed_shift_semantics_retained_as_integer_SOURCE': True, 'realized_signed_shift_circuit_and_phase_proved': False}

def certificate_join(plan, inputs):
    roles = plan['roles']
    tested = inputs[roles['original_full16_ROOT']]
    optimized = inputs[roles['optimized_other5_ROOT']]
    mf = inputs[roles['optimized_other5_manifest']]
    table = inputs[roles['tested_selector_table']]
    phase = inputs[roles['optimized_row_phase']]
    native = inputs[roles['complete_native_induction']]
    selected = inputs[roles['certified_selection']]
    alpha_root = inputs[roles['fixed_alpha_ROOT']]
    audit_root = inputs[roles['all20_independent_ROOT']]
    require(tested['passed'] is tested['completed'] is optimized['passed'] is optimized['completed'] is True, 'Verified original and optimized full16 rows')
    require(type(optimized['externally_observed_exit_code']) is int and optimized['externally_observed_exit_code'] == 0 and optimized['manifest_SHA256'] == plan['selected_expected_SHA256'][roles['optimized_other5_manifest']], 'Completed optimized row ROOT proof')
    require(mf['passed'] is mf['completed'] is mf['manifest_self_hash_excluded'] is True and mf['manifest_inclusive_owned_file_count'] == 13, 'Optimized sealed row')
    require(optimized['qualification']['baseline_previous_candidate_byte_and_resource_identity'] is True and optimized['qualification']['allfive_full_domain_range_inclusions_not_sample_only'] is True and optimized['qualification']['v14_min65_unchanged'] is True and optimized['qualification']['original_degree12_financial_source_or_global_G2_recertified'] is False, 'Use optimized row equivalence, not financial recertification')
    require(mf['files']['selected_table_and_selector.json']['SHA256'] == plan['selected_expected_SHA256'][roles['tested_selector_table']] and mf['files']['absolute_phase_and_domain_composition.json']['SHA256'] == plan['selected_expected_SHA256'][roles['optimized_row_phase']], 'Selected full24 table and row phase member authority')
    require(exact(table, plan['tested_table']), 'Exact tested table threshold equality and regions')
    require(phase['passed'] is phase['all_mapped_native_rows_X_CX_CCX_unit_phase'] is phase['coherent_promised_remainder_span_and_external_reference'] is True and phase['original_complete_native_induction_SHA256'] == plan['selected_expected_SHA256'][roles['complete_native_induction']], 'Only the tested polynomial row has completed phase proof')
    row = next(row for row in selected['rows'] if row['row_id'] == 'd4_s4')
    require(selected['primary_original_claims_authorized_only_by_actual_independent130_all20_audit'] is True and selected['original_failed_material_still_failed'] is True, 'Original failed row is not made a new successful owner')
    require(row['degree'] == 4 and row['segments'] == 4 and row['all_native_metadata_promises_valid'] is row['error_and_native_eligible_for_contract_consideration'] is True and row['rejections'] == [], 'Selected certified candidate')
    require(exact(row['native_plan'], native['fixed_plan']) and exact(row['all_quantized_center_coefficient_words'], plan['tested_coefficient_word_rows']), 'Sixteen floor nodes and full24 words match candidate certificate')
    require(native['exact_integer_native_induction_complete'] is True and native['row_id'] == 'd4_s4' and native['fixed_cell_slots'] == 240 and native['occupied_cell_slots'] == 224, 'Complete original induction, no replay')
    require(alpha_root['passed'] is alpha_root['completed'] is alpha_root['conditional_allocation_release_eligible'] is True and alpha_root['alpha'] == selected['fixed_alpha'] == [1, 16777216] and audit_root['passed'] is audit_root['completed'] is audit_root['current_scoped_all20_certification_integrity_verified'] is True, 'Fixed candidate alpha conditional release and independent all20 authority')
    require(alpha_root['actual_candidate_G2_feasibility'] is False and selected['candidate_feasibility'] is False, 'No candidate financial G2 or adoption credit')
    for cell in row['all_case_cell_decisions']['B4x12']:
        if not cell['empty']:
            expected_beta = [1, 1099511627776] if cell['k'] < 0 else [0, 1]
            require(cell['fits_lower_allowance'] is cell['native_metadata_valid'] is cell['all_native72_product144_and_shift_guards_passed'] is True and cell['additive_stock_beta_upper_retained_separately'] == cell['negative_shift_floor_upper_retained_separately'] == expected_beta, 'Every original occupied cell retains conditional alpha and its exact signed-shift beta branch')
            require(cell['approved_lower_allowance'] == alpha_root['conditional_E_allow_lower'] == selected['approved_primary_E_allow_lower'] and type(cell['reduction_stock_error_upper_retained_separately']) is list and len(cell['reduction_stock_error_upper_retained_separately']) == 2, 'Outward lower allowance authority and original reduction discrepancy retained, not substituted by old degree12 alpha')
    return {'passed': True, 'schema': 'a13-first-stock-conditional-envelope-premise-join-v1', 'row_id': 'd4_s4', 'relative_alpha': [1, 16777216], 'final_negative_shift_beta': [1, 1099511627776], 'conditional_pointwise_formula': '|candidate_native_stock-exp(clipped_native_log)| <= alpha_star*exp(clipped_native_log)+beta, conditional on the pinned independent all20/fixed-alpha/cell premises and the exact caller SOURCE join', 'new_uniform_polynomial_proof_or_exp_series_evaluated': False, 'old_degree12_alpha_used': False, 'new_financial_L2_bound': None, 'candidate_G2_or_financial_adoption': False, 'compiled_signed_shift_phase_remains_open': True}

def candidate_caller(raw_log, plan):
    require(type(raw_log) is int and -(1 << 71) <= raw_log < 1 << 71, 'Full72 raw caller input')
    site = plan['original_site']
    clipped = min(max(raw_log, site['low']), site['high'])
    inverse_product = clipped * site['inverse_ln2']
    require(-(1 << 143) <= inverse_product < 1 << 143, 'Original constant full144 product')
    reduced = inverse_product >> 40
    require(-(1 << 71) <= reduced < 1 << 71, 'Inverse ln2 CMUL no wrap')
    exponent = reduced >> 40
    k_q = exponent << 40
    ln2_product = k_q * site['ln2']
    require(-(1 << 143) <= ln2_product < 1 << 143, 'Original ln2 constant full144 product')
    ln2_scaled = ln2_product >> 40
    remainder = clipped - ln2_scaled
    require(-(1 << 71) <= k_q < 1 << 71 and -(1 << 71) <= ln2_scaled < 1 << 71 and -(1 << 71) <= remainder < 1 << 71, 'Original bits CMUL SUB no wrap')
    segment, values = native_oracle(remainder & ((1 << 72) - 1), plan['tested_table']['rows'], plan['tested_table']['thresholds'])
    polynomial = signed(values[15], 72)
    stock_raw = signed_shift(polynomial, exponent)
    return {'clipped': clipped, 'inverse_ln2_cmul': reduced, 'exponent': exponent, 'k_Q': k_q, 'ln2_cmul': ln2_scaled, 'remainder': remainder, 'segment': segment, 'values': values, 'polynomial': polynomial, 'stock_raw': stock_raw, 'stock_signed': signed(stock_raw, 72)}

def reference_caller(raw_log, plan):
    site = plan['original_site']
    x = min(site['high'], max(site['low'], raw_log))
    exponent = (x * site['inverse_ln2']) // (1 << 80)
    remainder = x - exponent * site['ln2']
    segment = sum(remainder >= threshold for threshold in plan['tested_table']['thresholds'])
    center, a, b, c, d, e = plan['tested_table']['rows'][segment]
    local = remainder - center
    g0 = a + (local * b >> 40)
    g1 = c + (local * d >> 40)
    square = local * local >> 40
    h = square * g1 >> 40
    fourth = square * square >> 40
    tail = fourth * e >> 40
    polynomial = (g0 + h) + tail
    stock = polynomial * (1 << exponent) if exponent >= 0 else polynomial // (1 << -exponent)
    require(0 <= stock < 1 << 71 and -(1 << 71) <= polynomial < 1 << 71, 'Independent caller integer no wrap')
    return {'clipped': x, 'exponent': exponent, 'remainder': remainder, 'segment': segment, 'polynomial': polynomial, 'stock_signed': stock, 'stock_raw': stock}

def universal_source_cells(plan, inputs):
    roles = plan['roles']
    binding = inputs[roles['original_domain_binding']]['cases']['B4x12']
    native = inputs[roles['complete_native_induction']]['all_case_cells']['B4x12']
    selected = next(row for row in inputs[roles['certified_selection']]['rows'] if row['row_id'] == 'd4_s4')['all_case_cell_decisions']['B4x12']
    require(len(binding['reduction_cells']) == 30 and len(native) == len(selected) == 120, 'Thirty classes times four segments, including empty cells')
    require([(c['k'], c['segment'], c['empty']) for c in native] == [(c['k'], c['segment'], c['empty']) for c in selected], 'No cell pruning or reordering')
    classes = {c['k']: c for c in binding['reduction_cells']}
    out, intervals = [], []
    for cell in native:
        budget()
        k, segment = cell['k'], cell['segment']
        source_class = classes[k]
        region = plan['tested_table']['regions'][segment]
        require(cell['empty'] is source_class['empty'], 'This original clipped range occupies all four segments in every nonempty class')
        if cell['empty']:
            out.append({'k': k, 'segment': segment, 'empty': True})
            continue
        lo, hi = cell['clipped_log_raw_bounds']
        rlo, rhi = cell['remainder_raw_bounds']
        require(source_class['clipped_log_raw_bounds'][0] <= lo <= hi <= source_class['clipped_log_raw_bounds'][1], 'Original class containment')
        require(rlo == lo - k * plan['original_site']['ln2'] and rhi == hi - k * plan['original_site']['ln2'] and region[0] <= rlo <= rhi <= region[1], 'Exact class-to-segment shift identity and threshold equality')
        require((lo * plan['original_site']['inverse_ln2']) >> 80 == (hi * plan['original_site']['inverse_ln2']) >> 80 == k, 'Monotone constant reduction gives original integer k throughout interval')
        require(cell['fresh_integer_range_and_original_shift_chain_proved'] is True and len(cell['native_intermediate_ranges']) == 16 and cell['selected_center_coefficient_words'] == plan['tested_table']['rows'][segment], 'Saved complete floor induction and coefficients')
        for row in cell['native_intermediate_ranges']:
            require(-(1 << 71) <= row['raw_bounds'][0] <= row['raw_bounds'][1] < 1 << 71, 'Every stored full72 SSA no wrap')
        for row in cell['signed144_products']:
            require(-(1 << 143) <= row['product_raw_bounds'][0] <= row['product_raw_bounds'][1] < 1 << 143, 'Every stored full144 product no wrap')
        p_lo, p_hi = cell['native_polynomial_raw_bounds']
        shifted = [p_lo << k, p_hi << k] if k >= 0 else [p_lo >> -k, p_hi >> -k]
        require(0 <= shifted[0] <= shifted[1] < 1 << 71 and shifted == cell['stock_raw_bounds'], 'Saved polynomial hull and original signed shift do not wrap')
        require(cell['native_intermediate_ranges'][15]['raw_bounds'] == [p_lo, p_hi], 'Output15 is the entire candidate polynomial')
        intervals.append([lo, hi])
        out.append({'k': k, 'segment': segment, 'empty': False, 'clipped_log_raw_bounds': [lo, hi], 'remainder_raw_bounds': [rlo, rhi], 'polynomial_raw_bounds': [p_lo, p_hi], 'stock_raw_bounds': shifted, 'integer_right_shift_floor_paid_once': k < 0})
    ordered = sorted(intervals)
    require(len(ordered) == 112 and ordered[0][0] == plan['original_site']['low'] and ordered[-1][1] == plan['original_site']['high'] and all(a[1] + 1 == b[0] for a, b in zip(ordered, ordered[1:])), 'Exact complete clipped SOURCE partition with no gaps or overlaps')
    return {'passed': True, 'schema': 'a13-first-stock-complete-logical-caller-cells-v1', 'classes': 30, 'cells': out, 'occupied': 112, 'empty': 8, 'all_allowed_integer_inputs_covered': True, 'all16_saved_native_floor_steps_reused': True, 'positive_zero_negative_original_signed_shift_no_wrap': True, 'negative_shift_floor_beta_paid_once': [1, 1099511627776], 'generic_zero_to_ln2_domain_used': False, 'realized_signed_shift_quantum_phase_proved': False}

def finite_caller_cases(plan, cells):
    mask = (1 << 72) - 1
    alternating = sum(1 << bit for bit in range(0, 72, 2))
    points = []
    for cell in cells['cells']:
        if not cell['empty']:
            lo, hi = cell['clipped_log_raw_bounds']
            points.extend([lo, hi])
    points.extend([plan['original_site']['low'] - 1, plan['original_site']['high'] + 1, -(1 << 71), (1 << 71) - 1])
    require(len(points) == 228, 'Fixed 224 class/segment endpoints plus four full source clip edges')
    records = []
    for index, point in enumerate(points):
        budget()
        actual = candidate_caller(point, plan)
        reference = reference_caller(point, plan)
        require(all(actual[key] == value for key, value in reference.items()), 'Independent exact caller identity')
        for dirty_index, dirty in enumerate((0, mask, alternating, 1 << (index % 72))):
            forward = dirty ^ actual['stock_raw']
            inverse = forward ^ actual['stock_raw']
            require(inverse == dirty and 0 <= forward <= mask, 'Full72 logical dirty XOR and self-inverse, not an emitted quantum shift circuit')
            records.append({'id': f'point{index:03d}_dirty{dirty_index}', 'raw_log_signed': point, 'dirty_raw': dirty, 'clipped': actual['clipped'], 'k': actual['exponent'], 'remainder': actual['remainder'], 'segment': actual['segment'], 'polynomial': actual['polynomial'], 'stock_raw': actual['stock_raw'], 'output_raw': forward, 'inverse_restores_dirty': True, 'source_input_preserved': True})
    require(len(records) == 912, 'Exactly fixed912 logical cases with duplicates retained')
    return {'passed': True, 'schema': 'a13-first-stock-fixed-logical-caller-cases-v1', 'point_count': 228, 'cases': records, 'forward_count': 912, 'inverse_count': 912, 'logical_integer_source_only': True, 'quantum_circuit_phase_or_workspace_simulated': False}

def main():
    global _STARTED, _OWNS_OUTPUT, _OUTPUT_ID
    _STARTED = process_started()
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--ready-sha256', required=True)
        args = parser.parse_args()
        base = Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(sys.version_info[:3] == (3,12,4) and sys.flags.isolated == sys.flags.no_site == 1 and sys.dont_write_bytecode and sys.flags.optimize == 0 and sys.get_int_max_str_digits() == 4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True) == ROOT and Path(__file__).resolve(strict=True) == SOURCE, 'Exact isolated default4300 current SOURCE')
        require(Path(sys.executable).resolve(strict=True) == ROOT/'.context/frontier_t0_env/Scripts/python.exe' and Path(sys._base_executable).resolve(strict=True) == base/'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True) == base/'python.exe' and sys.orig_argv[1:] == ['-I','-S','-B',str(SOURCE),'--ready-sha256',args.ready_sha256], 'Separate Windows launcher/base and current exact command')
        require(sys.path == [str(base/'python312.zip'),str(base/'DLLs'),str(base/'Lib'),str(base)] and 'site' not in sys.modules and not (base/'python312.zip').exists() and not (base/'python312.zip').is_symlink(), 'Pinned isolated path and missing ZIP')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(), 'Fresh output namespace')
        records = {}
        ready = decode(read_bytes(READY,args.ready_sha256,records))
        keys = {'schema','ready','root_and_independent_static_reviews_passed','first_stock_logical_caller_execution_authorized','conditional_accuracy_premise_join_accepted','interface','author_method_SHA256','static_review_expected_SHA256','selected_expected_SHA256','caps','exact13_inclusive_ledger','definition_AST_SHA256','absent_current_cache_paths','existing_current_cache_SHA256'}
        require(set(ready) == keys and ready['schema'] == 'root-a13-first-stock-logical-source-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['first_stock_logical_caller_execution_authorized'] is ready['conditional_accuracy_premise_join_accepted'] is True, 'Own current small SOURCE release only')
        authors = ready['author_method_SHA256']
        require(set(authors) == {SOURCE.name,PLAN.name,MD.name}, 'Own current author trio')
        source_raw = read_bytes(SOURCE,authors[SOURCE.name],records)
        plan_raw = read_bytes(PLAN,authors[PLAN.name],records)
        md_raw = read_bytes(MD,authors[MD.name],records)
        plan = decode(plan_raw)
        require(plan['caps'] == ready['caps'] == [180,150,600] and plan['default_decimal_digits'] == 4300 and plan['exact13_inclusive_ledger'] == ready['exact13_inclusive_ledger'] == LEDGER and exact(plan['selected_expected_SHA256'],ready['selected_expected_SHA256']) and exact(plan['interface'],ready['interface']) and set(ready['static_review_expected_SHA256']) == set(plan['current_review_paths']), 'Current scope caps ledger and direct reviews')
        for key,pin in ready['static_review_expected_SHA256'].items():
            review = decode(read_bytes(ROOT/key,pin,records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers'] == [] and review['author_method_SHA256'] == authors, 'All current3 before premises origins and integer evaluation')
        code_guard(source_raw,ready)
        caches = ['research/limitation_program_20261001/__pycache__/'+SOURCE.stem+'.cpython-312'+s+'.pyc' for s in ('','.opt-1','.opt-2')]
        require(ready['existing_current_cache_SHA256'] == {} and ready['absent_current_cache_paths'] == sorted(caches) and all(not (ROOT/key).exists() and not (ROOT/key).is_symlink() for key in caches), 'All current cache absences')
        inputs = {}
        for key,pin in plan['selected_expected_SHA256'].items():
            raw = read_bytes(ROOT/key,pin,records)
            inputs[key] = raw if key.endswith('.py') else decode(raw)
        origins = loaded_origins(inputs[plan['roles']['runtime_manifest']],records)
        witness = source_witness(plan,inputs)
        certificate = certificate_join(plan,inputs)
        controls = controls_record(plan)
        code_guard(source_raw,ready)
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        _OUTPUT_ID = [stat8(OUTPUT)[i] for i in (0,1,4,5,6,7)]
        _OWNS_OUTPUT = True
        files = {}
        for name,raw in [('executed_controller.py',source_raw),('executed_adapter.json',plan_raw),('executed_preflight.md',md_raw),('executed_ROOT_READY.json',read_bytes(READY,args.ready_sha256,records))]:
            files[name] = save(name,raw=raw)
        files['run_started.json'] = save('run_started.json',{'caps':[CPU,ADMISSION,WALL],'created_UTC_ns':time.time_ns(),'PID':os.getpid(),'default4300_no_setter':True})
        files['source_and_premise_witness.json'] = save('source_and_premise_witness.json',{'source':witness,'conditional_accuracy':certificate})
        files['positive_first_controls.json'] = save('positive_first_controls.json',controls)
        cells = universal_source_cells(plan,inputs)
        cases = finite_caller_cases(plan,cells)
        files['complete_class_and_cell_bridge.json'] = save('complete_class_and_cell_bridge.json',cells)
        files['fixed_logical_caller_cases.json'] = save('fixed_logical_caller_cases.json',cases)
        qualification = {'logical_integer_SOURCE_only':True,'original_degree12_alpha_used':False,'new_exponential_tail_moment_fit_or_uniform_proof_evaluated':False,'old_saved_scientific_provider_or_circuit_array_replayed':False,'compiled_signed_shift_quantum_phase_and_actual_clean_workspace_open':True,'new_financial_L2_bound':None,'candidate_G2_financial_adoption_hardware_or_advantage':False,'fixture_credit':0}
        files['qualification.json'] = save('qualification.json',qualification)
        for key,row in tuple(records.items()):
            read_bytes(Path(key),row['expected_SHA256'],records)
        code_guard(source_raw,ready)
        files['selected_premise_authority.json'] = save('selected_premise_authority.json',{'selected_expected_SHA256':plan['selected_expected_SHA256'],'before_after_selected_and_origin_bytes':records,'loaded_original_expected_origins':origins,'full_transitive_union_or_native_arrays_replayed':False})
        summary = {'passed':True,'completed':True,'source_witness':witness,'conditional_accuracy':certificate,'classes':cells['classes'],'occupied_cells':cells['occupied'],'empty_cells':cells['empty'],'fixed_forward_cases':cases['forward_count'],'fixed_inverse_cases':cases['inverse_count'],'controls':controls,'caps':[CPU,ADMISSION,WALL],'preseal_CPU_wall_seconds':[time.process_time(),time.monotonic()-_STARTED],'qualification':qualification}
        files['summary.json'] = save('summary.json',summary)
        require(set(files) == set(LEDGER)-{'manifest.json'} and {p.name for p in OUTPUT.iterdir()} == set(files), 'Exact preseal12 no failed markers')
        manifest = {'passed':True,'completed':True,'budget_censored':False,'files':files,'manifest_self_hash_excluded':True,'inclusive_files':13,'author_method_SHA256':authors,'ROOT_READY_expected_SHA256':args.ready_sha256,'selected_expected_SHA256':plan['selected_expected_SHA256'],'financial_G2_or_advantage':False,'fixture_credit':0}
        seal = save('manifest.json',manifest)
        require({p.name for p in OUTPUT.iterdir()} == set(LEDGER), 'Exact sealed13')
        budget()
        print(json.dumps({'passed':True,'manifest_SHA256':seal,'fixture_credit':0,'financial_G2_or_advantage':False}),flush=True)
    except BaseException as error:
        failure(error)
        raise

if __name__ == '__main__':
    main()
