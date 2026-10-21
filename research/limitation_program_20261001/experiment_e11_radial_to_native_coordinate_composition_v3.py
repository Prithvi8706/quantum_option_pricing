"""Dormant selected-premise radial-to-native squared-L2 composition; own ROOT READY required."""
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
SOURCE = ROOT / 'research/limitation_program_20261001/experiment_e11_radial_to_native_coordinate_composition_v3.py'
PLAN = ROOT / '.context/E11_RADIAL_TO_NATIVE_COORDINATE_COMPOSITION_PLAN_run003.json'
MD = ROOT / '.context/E11_RADIAL_TO_NATIVE_COORDINATE_COMPOSITION_PLAN_run003.md'
READY = ROOT / '.context/E11_RADIAL_TO_NATIVE_COORDINATE_COMPOSITION_ROOT_READY_run003.json'
OUTPUT = ROOT / 'results/limitation_program_20261001/E11_radial_to_native_coordinate_composition_run003'
LEDGER = ['executed_controller.py', 'executed_plan.json', 'executed_plan.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'same_middle_variable_interface_witness.json', 'five_metadata_controls.json', 'primary_composition.json', 'independent_composition.json', 'same_profile_reconciliation.json', 'summary.json', 'manifest.json']
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
    require(type(pair) is list and len(pair) == 2 and all(type(n) is int and n.bit_length() <= 131072 for n in pair) and pair[1] > 0 and gcd(pair[0], pair[1]) == 1, 'Bounded canonical saved ratio before arithmetic')
    return Fraction(*pair)

def plus(a, b):
    require(max(a.numerator.bit_length() + b.denominator.bit_length(), b.numerator.bit_length() + a.denominator.bit_length(), a.denominator.bit_length() + b.denominator.bit_length()) <= 524288, 'Rational temporary bounds before addition')
    value = a + b
    require(max(value.numerator.bit_length(), value.denominator.bit_length()) <= 131072, 'Reduced rational result bound')
    return value

def twice(a):
    require(a.numerator.bit_length() + 2 <= 524288, 'Temporary bound before fixed factor2')
    value = 2 * a
    require(max(value.numerator.bit_length(), value.denominator.bit_length()) <= 131072, 'Reduced fixed factor2 result')
    return value

def pair(value):
    return [value.numerator, value.denominator]

def interface_witness(plan, ready, inputs):
    require(ready['same_middle_variable_interface_witness_accepted'] is True and exact(ready['interface'], plan['interface']), 'Own independently reviewed identical-middle-variable acceptance')
    theorem = inputs[plan['native_theorem']]
    require(theorem['scope']['source_law'] == plan['interface']['source_law'] and theorem['scope']['units'] == plan['interface']['units'] and theorem['scope']['quantity'] == plan['interface']['quantity'] and theorem['scope']['digital_pair_independence'] is False and theorem['original_U_V_uniform_cell_coupling'] is theorem['shifted_second_cosine_exact_three_quarter_circular_grid_slot_same_bound'] is theorem['two_coordinate_Euclidean_squared_bound_by_sum_not_independence'] is True and theorem['coordinate_total_squared_bound'] == '2*(midpoint_squared+native_arithmetic_squared)', 'Exact old native triangle/coupling/rotation theorem')
    qualification = inputs[plan['radial_qualification']]
    require(qualification['radial_and_ideal_midpoint_bounds_only'] is True and qualification['new_native_or_downstream_certificate'] is False and qualification['digital_pair_independence'] is False and qualification['native_arrays_generated_or_replayed'] is False, 'V4 is a new ideal premise only')
    primary_components = inputs[plan['profiles']['primary90']['native_components']]
    guard = primary_components['original_native_radicand_domain_guard']
    require(guard['strict_guard_passed'] is True and guard['guard_comparisons_executed'] == 1 and guard['native_source_clipping_inserted'] is False, 'Reuse sole old certified domain guard; never repeat it')
    for profile, roles in plan['profiles'].items():
        old = inputs[roles['native_bound']]
        new = inputs[roles['radial_bound']]
        components = inputs[roles['native_components']]
        require(old['units'] == plan['interface']['units'] and old['norm_squared_not_norm_twice'] is True and new['profile'] == profile and new['native_coordinate_recertified'] is False and components['all_low_native_product_floor_charged'] is True and components['original_unsigned_isqrt_storage_and_product144_nooverflow_required'] is True and components['root_Holder_and_native_floor_charged'] is True, 'Exact own profile roles and unchanged native arithmetic prerequisites')
        adapter = inputs[plan['radial_adapters']]['own_profiles'][profile]['roles']
        comparison = inputs[roles['radial_comparison']]
        require(adapter['old_coordinate_path'] == roles['native_bound'] and adapter['old_coordinate_expected_SHA256'] == plan['selected_expected_SHA256'][roles['native_bound']] and adapter['old_arithmetic_field'] == roles['arithmetic_field'] and adapter['old_ideal_midpoint_field'] == roles['ideal_field'] and comparison['profile'] == profile and comparison['new_ideal_midpoint_upper'] == new[roles['ideal_field']] and comparison['old_same_profile_ideal_midpoint_upper'] == old[roles['ideal_field']] and comparison['original_native_arithmetic_allowance_unchanged'] == old[roles['arithmetic_field']] and comparison['new_upper_not_greater_than_old_upper'] is True and comparison['new_native_or_financial_certificate'] is False, 'Full V4 own-profile adapter/comparison joins to the same original native record')
    return {'accepted_same_middle_variable': plan['interface'], 'pointwise_triangle': '|Z-N_M|^2 <= 2|Z-H_M|^2 + 2|H_M-N_M|^2', 'expectation_requires_no_error_independence': True, 'native_arithmetic_proof_and_guard_reexecuted': False}

def compose(profile, plan, inputs):
    roles = plan['profiles'][profile]
    old, radial = inputs[roles['native_bound']], inputs[roles['radial_bound']]
    arithmetic = ratio(old[roles['arithmetic_field']])
    old_ideal, old_total = ratio(old[roles['ideal_field']]), ratio(old[roles['old_total_field']])
    new_ideal = ratio(radial[roles['ideal_field']])
    require(arithmetic >= 0 and new_ideal >= 0 and old_total == twice(plus(old_ideal, arithmetic)), 'Verified old decomposition and nonnegative saved premises')
    require(new_ideal <= old_ideal, 'Own verified ideal improvement, no mixed profiles')
    if profile == 'primary90':
        grouped = twice(plus(new_ideal, arithmetic))
        expanded = plus(twice(new_ideal), twice(arithmetic))
    else:
        expanded = plus(twice(new_ideal), twice(arithmetic))
        grouped = twice(plus(new_ideal, arithmetic))
    require(grouped == expanded and grouped <= old_total, 'Two arithmetic orders of same own premises, unchanged old comparator')
    chosen = grouped if profile == 'primary90' else expanded
    return {'profile': profile, 'recipe': 'sum_then_double' if profile == 'primary90' else 'double_then_sum', 'unchanged_native_arithmetic_upper': pair(arithmetic), 'new_ideal_midpoint_upper': pair(new_ideal), 'old_ideal_midpoint_upper': pair(old_ideal), 'composed_original_native_coordinate_squared_L2_upper': pair(chosen), 'old_original_native_coordinate_squared_L2_upper': pair(old_total), 'same_profile_composed_upper_not_greater': True, 'grouped_equals_expanded': True, 'units': plan['interface']['units'], 'native_sampler_or_arithmetic_proof_reexecuted': False}

def owned_guard():
    require(_OWNS_OUTPUT is True and OUTPUT.resolve(strict=True) == OUTPUT and OUTPUT.is_dir() and not OUTPUT.is_symlink() and [stat8(OUTPUT)[i] for i in (0, 1, 4, 5, 6, 7)] == _OUTPUT_ID, 'This-run exclusive output identity')

def save(name, value=None, raw=None):
    owned_guard()
    require(name in LEDGER and not (OUTPUT / name).exists() and not (OUTPUT / name).is_symlink(), 'Exclusive registered output')
    if raw is None:
        pending = [value]
        count = 0
        while pending:
            budget()
            item = pending.pop()
            count += 1
            require(count <= 134217728 and (type(item) is not int or item.bit_length() <= 65536), 'Finite default4300 serialization values')
            if type(item) is dict:
                pending.extend(item.values())
            elif type(item) in (list, tuple):
                pending.extend(item)
        raw = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    require(len(raw) <= 128 << 20 and len(list(OUTPUT.iterdir())) < 64 and sum(p.stat().st_size for p in OUTPUT.iterdir()) + len(raw) <= 128 << 20, 'Inclusive original file/byte caps')
    with (OUTPUT / name).open('xb') as stream:
        for start in range(0, len(raw), 65536):
            budget()
            owned_guard()
            part = raw[start:start + 65536]
            require(stream.write(part) == len(part), 'Bounded whole physical write')
            owned_guard()
    require((OUTPUT / name).stat().st_size == len(raw), 'Exact saved bytes')
    return hashlib.sha256(raw).hexdigest()

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
    global _STARTED, _OWNS_OUTPUT, _OUTPUT_ID
    _STARTED = process_started()
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--ready-sha256', required=True)
        args = parser.parse_args()
        require(sys.version_info[:3] == (3, 12, 4) and sys.flags.isolated == sys.flags.no_site == 1 and sys.dont_write_bytecode and sys.flags.optimize == 0 and sys.get_int_max_str_digits() == 4300 and 'PYTHONINTMAXSTRDIGITS' not in os.environ and 'PYTHONOPTIMIZE' not in os.environ and 'int_max_str_digits' not in sys._xoptions and Path.cwd().resolve(strict=True) == ROOT and Path(__file__).resolve(strict=True) == SOURCE and Path(sys.executable).resolve(strict=True) == ROOT / '.context/frontier_t0_env/Scripts/python.exe' and Path(sys.base_prefix).resolve(strict=True) == Path('C:/Users/prith/AppData/Local/Programs/Python/Python312') and sys.orig_argv[1:] == ['-I', '-S', '-B', str(SOURCE), '--ready-sha256', args.ready_sha256], 'Exact isolated absolute invocation/default4300')
        require(not OUTPUT.exists() and not OUTPUT.is_symlink(), 'No retry of an existing output')
        base = Path('C:/Users/prith/AppData/Local/Programs/Python/Python312')
        require(Path(sys._base_executable).resolve(strict=True) == base / 'python.exe' and Path(sys.orig_argv[0]).resolve(strict=True) == base / 'python.exe', 'Original Windows base executable/argv0 identity is separate from the virtual-environment launcher')
        require(sys.path == [str(base / 'python312.zip'), str(base / 'DLLs'), str(base / 'Lib'), str(base)] and 'site' not in sys.modules and not (base / 'python312.zip').exists() and not (base / 'python312.zip').is_symlink(), 'Original isolated path/absentZIP, no site import')
        records = {}
        ready = decode(read_bytes(READY, args.ready_sha256, records))
        required = {'schema', 'ready', 'root_and_independent_static_reviews_passed', 'verified_premise_composition_authorized', 'same_middle_variable_interface_witness_accepted', 'interface', 'author_method_SHA256', 'static_review_expected_SHA256', 'selected_expected_SHA256', 'caps', 'exact13_inclusive_ledger', 'definition_AST_SHA256', 'absent_current_cache_paths', 'existing_current_cache_SHA256'}
        require(set(ready) == required and ready['schema'] == 'root-e11-radial-to-native-composition-ready-v1' and ready['ready'] is ready['root_and_independent_static_reviews_passed'] is ready['verified_premise_composition_authorized'] is True, 'Own separate ROOT release; no old grant inherited')
        authors = ready['author_method_SHA256']
        require(set(authors) == {SOURCE.name, PLAN.name, MD.name}, 'Exact own three author products')
        source_raw = read_bytes(SOURCE, authors[SOURCE.name], records)
        plan_raw = read_bytes(PLAN, authors[PLAN.name], records)
        md_raw = read_bytes(MD, authors[MD.name], records)
        plan = decode(plan_raw)
        require(plan['caps'] == ready['caps'] == [180, 150, 600] and plan['default_decimal_digits'] == 4300 and plan['exact13_inclusive_ledger'] == ready['exact13_inclusive_ledger'] == LEDGER and exact(plan['selected_expected_SHA256'], ready['selected_expected_SHA256']) and set(ready['static_review_expected_SHA256']) == set(plan['current_review_paths']), 'Closed selected premise map/caps/current reviews/ledger')
        for key, expected in ready['static_review_expected_SHA256'].items():
            review = decode(read_bytes(ROOT / key, expected, records))
            require(review['passed'] is review['science_static_passed'] is review['lifecycle_static_passed'] is True and review['blockers'] == [] and review['author_method_SHA256'] == authors, 'Full independent and ROOT actual source reviews before premises')
        code_guard(source_raw, ready)
        cache = ['research/limitation_program_20261001/__pycache__/' + SOURCE.stem + '.cpython-312' + ending + '.pyc' for ending in ('', '.opt-1', '.opt-2')]
        require(ready['existing_current_cache_SHA256'] == {} and ready['absent_current_cache_paths'] == sorted(cache) and all(not (ROOT / key).exists() and not (ROOT / key).is_symlink() for key in cache), 'Exact own unused cache namespace; no late origin promotion')
        raw_inputs = {key: read_bytes(ROOT / key, expected, records) for key, expected in plan['selected_expected_SHA256'].items()}
        inputs = {key: decode(raw) for key, raw in raw_inputs.items() if key.endswith('.json')}
        native, radial = inputs[plan['old_native_manifest']], inputs[plan['radial_manifest']]
        nr, rr = inputs[plan['old_native_ROOT_verification']], inputs[plan['radial_ROOT_verification']]
        require(nr['passed'] is rr['passed'] is True and nr['manifest_SHA256'] == plan['selected_expected_SHA256'][plan['old_native_manifest']] and rr['manifest_SHA256'] == plan['selected_expected_SHA256'][plan['radial_manifest']] and nr['two_assembled_bounds_one_saved_domain_guard_identity_check_four_controls_checked'] is True and rr['ROOT_external_terminal_exit_code'] == 0 and nr['financial_path_policy_G2_cost_adoption_or_advantage_transfer'] is rr['native_or_downstream_recertification'] is False and nr['fixture_credit'] == rr['fixture_credit'] == 0, 'Both selected bound premises have completed ROOT saved verification')
        require(native['passed'] is native['completed'] is radial['passed'] is radial['completed'] is True and native['budget_censored'] is radial['budget_censored'] is False and native['manifest_inclusive_owned_file_count'] == 47 and radial['manifest_inclusive_owned_file_count'] == 29, 'Old verified packets, never new scientific owner validation')
        require(nr['primary_coordinate_squared_L2_upper_exact'] == inputs[plan['profiles']['primary90']['native_bound']]['continuous_to_original_native_coordinate_squared_L2_upper'] and nr['independent_coordinate_squared_L2_upper_exact'] == inputs[plan['profiles']['independent130']['native_bound']]['continuous_to_original_native_coordinate_squared_L2_upper'], 'Native ROOT verification exact own bound record fields')
        for key, expected in plan['selected_expected_SHA256'].items():
            if key.startswith(str(Path(plan['old_native_manifest']).parent).replace('\\', '/') + '/') and key != plan['old_native_manifest']:
                require(native['files'][Path(key).name] == expected, 'Selected native record belongs to original sealed manifest')
            if key.startswith(str(Path(plan['radial_manifest']).parent).replace('\\', '/') + '/') and key != plan['radial_manifest']:
                require(radial['files'][Path(key).name] == expected, 'Selected radial record belongs to original sealed manifest')
        old_tree = ast.parse(raw_inputs[next(key for key in raw_inputs if key.endswith('/executed_experiment_e11_native_coordinate_squared_l2_v1.py'))])
        old_proof = {n.name: hashlib.sha256(ast.dump(n, include_attributes=False).encode('utf-8')).hexdigest() for n in old_tree.body if isinstance(n, ast.FunctionDef) and n.name in plan['native_SOURCE_proof_definition_AST_SHA256']}
        require(old_proof == plan['native_SOURCE_proof_definition_AST_SHA256'], 'Exactly retained arithmetic/triangle theorem plaintext, never call old code')
        origins = loaded_origins(native, records)
        witness = interface_witness(plan, ready, inputs)
        controls = controls_record(plan)
        code_guard(source_raw, ready)
        budget(admission=True)
        OUTPUT.mkdir(exist_ok=False)
        _OUTPUT_ID = [stat8(OUTPUT)[i] for i in (0, 1, 4, 5, 6, 7)]
        _OWNS_OUTPUT = True
        files = {}
        for name, raw in [('executed_controller.py', source_raw), ('executed_plan.json', plan_raw), ('executed_plan.md', md_raw), ('executed_ROOT_READY.json', read_bytes(READY, args.ready_sha256, records))]:
            files[name] = save(name, raw=raw)
        files['run_started.json'] = save('run_started.json', {'created_UTC_ns': time.time_ns(), 'PID': os.getpid(), 'caps': [CPU, ADMISSION, WALL], 'selected_verified_premise_transform_only': True})
        files['same_middle_variable_interface_witness.json'] = save('same_middle_variable_interface_witness.json', witness)
        files['five_metadata_controls.json'] = save('five_metadata_controls.json', controls)
        primary = compose('primary90', plan, inputs)
        independent = compose('independent130', plan, inputs)
        files['primary_composition.json'] = save('primary_composition.json', primary)
        files['independent_composition.json'] = save('independent_composition.json', independent)
        files['same_profile_reconciliation.json'] = save('same_profile_reconciliation.json', {'passed': True, 'primary90_grouped_equals_expanded': primary['grouped_equals_expanded'], 'independent130_grouped_equals_expanded': independent['grouped_equals_expanded'], 'profiles_not_required_equal_or_nested': True, 'no_cross_profile_arithmetic': True})
        for key, row in tuple(records.items()):
            read_bytes(Path(key), row['expected_SHA256'], records)
        code_guard(source_raw, ready)
        files['selected_premise_authority.json'] = save('selected_premise_authority.json', {'expected_selected_premises': plan['selected_expected_SHA256'], 'full_selected_before_after_byte_reads_only': records, 'loaded_original_expected_origins': origins, 'transitive_runtime_or_native_SCI_union_rehashed': False, 'native_arrays_replayed': False})
        summary = {'passed': True, 'completed': True, 'profile_compositions': [primary, independent], 'controls': controls, 'same_middle_variable_witness': witness, 'caps': [CPU, ADMISSION, WALL], 'preseal_CPU_wall_seconds': [time.process_time(), time.monotonic() - _STARTED], 'budget_censored': False, 'native_arithmetic_proof_or_sampler_reexecuted': False, 'new_series': False, 'financial_transfer': False, 'digital_pair_independence': False, 'quantum_advantage': False, 'fixture_credit': 0}
        files['summary.json'] = save('summary.json', summary)
        require(set(files) == set(LEDGER) - {'manifest.json'} and not (OUTPUT / 'FAILED_UNSEALED.json').exists() and {p.name for p in OUTPUT.iterdir()} == set(files), 'Exact twelve preseal outputs and no failure')
        manifest = {'passed': True, 'completed': True, 'budget_censored': False, 'files': files, 'manifest_self_hash_excluded': True, 'inclusive_files': 13, 'selected_expected_SHA256': plan['selected_expected_SHA256'], 'author_method_SHA256': authors, 'ROOT_READY_expected_SHA256': args.ready_sha256, 'scope': 'Verified saved-premise native-coordinate upper composition only', 'financial_transfer': False, 'quantum_advantage': False, 'fixture_credit': 0}
        manifest_sha = save('manifest.json', manifest)
        require({p.name for p in OUTPUT.iterdir()} == set(LEDGER) and sum(p.stat().st_size for p in OUTPUT.iterdir()) <= 128 << 20 and not (OUTPUT / 'FAILED_UNSEALED.json').exists(), 'Complete13 inclusive output; external terminal0 still required')
        budget()
        print(json.dumps({'passed': True, 'manifest_SHA256': manifest_sha, 'financial_transfer': False, 'quantum_advantage': False, 'fixture_credit': 0}), flush=True)
    except BaseException as error:
        failure(error)
        raise

if __name__ == '__main__':
    main()
