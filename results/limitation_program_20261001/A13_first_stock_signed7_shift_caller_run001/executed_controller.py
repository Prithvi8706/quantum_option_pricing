"""Dormant signed7 shift caller. ROOT READY is required before selected array use.

Only the isolated full72 signed-shift boundary is tested. The old native array,
all-data algebraic proof and exact paid macro are pinned separately. No dirty
provider import, whole polynomial/log caller, financial or hardware claim.
"""
import time
WALL_START = time.perf_counter()
import ast
import ctypes
import ctypes.wintypes
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import sys
import types
__annotations__ = {}
ROOT = Path('C:/Users/prith/quantum_option_pricing')
SOURCE_KEY = 'research/limitation_program_20261001/experiment_a13_first_stock_signed7_shift_caller_v1.py'
SCOPE_KEY = '.context/A13_FIRST_STOCK_SIGNED7_SHIFT_CALLER_INPUT_ADAPTER_run001.json'
MD_KEY = '.context/A13_FIRST_STOCK_SIGNED7_SHIFT_CALLER_PREFLIGHT_run001.md'
READY_KEY = '.context/A13_FIRST_STOCK_SIGNED7_SHIFT_CALLER_ROOT_READY_run001.json'
OUTPUT_KEY = 'results/limitation_program_20261001/A13_first_stock_signed7_shift_caller_run001'
PLAN_KEY = '.context/A13_FIRST_STOCK_SIGNED7_SHIFT_CALLER_PLAN_run001.json'
PLAN_SHA = 'a2e21ba957dd6d1cbd4e94bc0af4ccf64f5290ed3334a5aeafa929d26f92e232'
ARRAY_KEY = 'results/limitation_program_20261001/A07_shift_leaf_run001/16077b59a0122da5ed2f.npy'
ARRAY_SHA = '22bc94f5d8430d818365c3ff7d357ff04adbffa4609ba1e4bae7e4cda244fa17'
DESC_KEY = 'results/limitation_program_20261001/A07_shift_leaf_run001/16077b59a0122da5ed2f.json'
ARITHMETIC_KEY = 'results/limitation_program_20261001/A01_run009/shift_arithmetic_certificate.json'
BOUNDARY_ROOT_KEY = '.context/A13_FIRST_STOCK_SOURCE_BOUNDARY_V2_ACTUAL_RESULT_ROOT_VERIFICATION_run001.json'
BOUNDARY_MF_KEY = 'results/limitation_program_20261001/A13_first_stock_source_boundary_run002/manifest.json'
CASES_KEY = 'results/limitation_program_20261001/A13_first_stock_source_boundary_run002/fixed_logical_caller_cases.json'
MACRO_KEY = 'results/limitation_program_20261001/A13_d4_s4_v14_signed_leaf_min65_run002/paid_CCX_macro.json'
PHASE_KEY = 'results/limitation_program_20261001/A13_d4_s4_v14_signed_leaf_min65_run002/independent_exact_absolute_CCX_phase.json'
WORD = 72
MASK = 4722366482869645213695
CAPS = {'CPU_seconds': 180, 'admission_CPU_seconds': 150, 'inclusive_owned_bytes_max': 134217728, 'inclusive_owned_files_max': 64, 'integer_decimal_digits': 4300, 'physical_write_bytes_max': 65536, 'selected_bytes_max': 67108864, 'selected_paths_max': 256, 'single_selected_file_bytes_max': 67108864, 'source_bytes_max': 8388608, 'wall_seconds': 600, 'process_CPU_seconds': 180, 'resident_set_bytes': 157286400, 'output_bytes_total_maximum': 134217728, 'native_rows_maximum': 1000000, 'allocated_wires_maximum': 32768}
LEDGER = ['executed_controller.py', 'executed_adapter.json', 'executed_preflight.md', 'executed_ROOT_READY.json', 'run_started.json', 'selected_premise_authority.json', 'source_interface_and_universal_contract.json', 'archived_leaf_structural_phase_witness.json', 'fixed_912_caller_cases.json', 'positive_first_controls.json', 'paid_caller_resources.json', 'qualification.json', 'summary.json', 'manifest.json']
INTERFACE = {'argument_copy_CX': 144, 'argument_uncopy_CX': 144, 'asset': 0, 'caller_argument_locals_clean': 144, 'caller_local_arguments_used': True, 'case': 'B4x12', 'count_bits': 7, 'count_scale': 'unscaled integer, not k_Q', 'count_source': 3979, 'count_word': 'full72 sign extension of signed7 count', 'current_declared_count_interval': [-17, 12], 'current_occupied_count_interval': [-16, 11], 'data_candidate_polynomial': 15, 'date': 1, 'fraction_bits': 40, 'original_data_polynomial': 4020, 'output': 'full72 arbitrary dirty XOR', 'output_source': 4021, 'private_leaf_scratch_clean': 591, 'spectators': 'untouched; no overlap with external ports, argument locals or leaf scratch', 'width': 72}
REVIEW_ROUTES = {'author_QA': '.context/A13_FIRST_STOCK_SIGNED7_SHIFT_CALLER_AUTHOR_STATIC_QA_run001.json', 'independent_SOURCE_peer': '.context/A13_FIRST_STOCK_SIGNED7_SHIFT_CALLER_INDEPENDENT_STATIC_PEER_run001.json', 'ROOT_static_review': '.context/A13_FIRST_STOCK_SIGNED7_SHIFT_CALLER_ROOT_STATIC_REVIEW_run001.json'}
READY_KEYS = ['schema', 'ready', 'signed_shift_caller_execution_authorized', 'input_adapter_path', 'input_adapter_SHA256', 'own_source_expected_files', 'output_directory', 'caps', 'definition_AST_SHA256', 'exact14_inclusive_ledger', 'current_review_roles', 'preflight']
CCX_MACRO = (('H', 2), ('CX', 1, 2), ('TD', 2), ('CX', 0, 2), ('T', 2), ('CX', 1, 2), ('TD', 2), ('CX', 0, 2), ('T', 1), ('T', 2), ('H', 2), ('CX', 0, 1), ('T', 0), ('TD', 1), ('CX', 0, 1))
CASE_KEYS = {'source_input_preserved', 'output_raw', 'inverse_restores_dirty', 'k', 'stock_raw', 'id', 'clipped', 'polynomial', 'segment', 'remainder', 'raw_log_signed', 'dirty_raw'}
_OWNS_OUTPUT = False
_OUTPUT_ID = None


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fingerprint(path):
    value = path.stat()
    return tuple(getattr(value, key, 0) for key in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns", "st_mode", "st_file_attributes", "st_reparse_tag"))


def exact_path(path, *, regular=True):
    path = Path(path)
    require(path.is_absolute() and path.resolve(strict=True) == path, "Exact absolute physical path required")
    for part in (path, *path.parents):
        row = part.stat()
        require(not part.is_symlink() and not getattr(row, "st_reparse_tag", 0) and not getattr(row, "st_file_attributes", 0) & 1024, "No input/output reparse or alias")
    if regular:
        require(path.is_file(), "Regular file required")
    return path


def checked_bytes(path, expected, length, budget=None, *, collect=False):
    require(type(expected) is str and len(expected) == 64 and all(c in "0123456789abcdef" for c in expected), "Exact expected SHA required")
    require(type(length) is int and 0 <= length <= 128 << 20, "Declared finite byte length required")
    path = exact_path(path)
    before = fingerprint(path)
    require(before[2] == length, "Exact declared input byte length")
    state, chunks, total = hashlib.sha256(), [], 0
    with path.open("rb") as handle:
        first = os.fstat(handle.fileno())
        while True:
            if budget:
                budget.check()
            chunk = handle.read(min(65536, length - total + 1))
            if not chunk:
                break
            total += len(chunk)
            require(total <= length, "Input did not grow")
            state.update(chunk)
            if collect:
                chunks.append(chunk)
        last = os.fstat(handle.fileno())
    require(total == length and state.hexdigest() == expected and fingerprint(path) == before,
            "Full pinned bytes and exact stable eight-field identity")
    require(all(getattr(first, k) == getattr(last, k) for k in ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")), "Open input identity stable")
    return (b"".join(chunks) if collect else None), before


def read_pinned_json(path, expected, budget=None):
    path = exact_path(path)
    length = path.stat().st_size
    require(length <= 8 << 20, "Small release/scope JSON cap")
    raw, fp = checked_bytes(path, expected, length, budget, collect=True)
    return json.loads(raw), fp


class Budget:
    def __init__(self):
        class Counters(ctypes.Structure):
            _fields_ = [("cb", ctypes.wintypes.DWORD), ("PageFaultCount", ctypes.wintypes.DWORD)] + [(name, ctypes.c_size_t) for name in ("PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage", "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage", "PagefileUsage", "PeakPagefileUsage")]
        self.counters_type = Counters
        self.kernel = ctypes.WinDLL(str(Path(os.environ["SystemRoot"]) / "System32/kernel32.dll"), use_last_error=True)
        self.psapi = ctypes.WinDLL(str(Path(os.environ["SystemRoot"]) / "System32/psapi.dll"), use_last_error=True)
        self.kernel.GetCurrentProcess.restype = ctypes.wintypes.HANDLE
        self.psapi.GetProcessMemoryInfo.argtypes = [ctypes.wintypes.HANDLE, ctypes.c_void_p, ctypes.wintypes.DWORD]
        self.psapi.GetProcessMemoryInfo.restype = ctypes.wintypes.BOOL
        self.admitted = False
        self.max_rss = 0

    def check(self):
        cpu, wall = time.process_time(), time.perf_counter() - WALL_START
        row = self.counters_type()
        row.cb = ctypes.sizeof(row)
        require(self.psapi.GetProcessMemoryInfo(self.kernel.GetCurrentProcess(), ctypes.byref(row), row.cb), "Process RSS metric available")
        self.max_rss = max(self.max_rss, row.WorkingSetSize)
        require(cpu < CAPS["process_CPU_seconds"] and wall < CAPS["wall_seconds"] and row.WorkingSetSize < CAPS["resident_set_bytes"], "Fixed total CPU/wall/RSS caps")
        require(self.admitted or cpu < CAPS["admission_CPU_seconds"], "Fixed admission CPU cap")
        return {"process_CPU_seconds": cpu, "wall_seconds": wall, "maximum_observed_RSS_bytes": self.max_rss}


def runtime_origins(scope):
    for module in tuple(sys.modules.values()):
        path = getattr(module, "__file__", None)
        if path is None:
            spec = getattr(module, "__spec__", None)
            require(spec is None or spec.origin in (None, "built-in", "frozen"), "No undeclared nonfile import origin")
            continue
        path = str(Path(path).resolve(strict=True))
        require(path in scope["expected_files"] or path == str(Path(__file__)), "Every loaded library origin is exactly selected and pinned")
        cached = getattr(module, "__cached__", None)
        if cached and Path(cached).exists():
            require(str(Path(cached).resolve(strict=True)) in scope["expected_files"], "Existing loaded cache is selected and pinned")


class OwnedOutput:
    def __init__(self, directory, budget):
        global _OWNS_OUTPUT, _OUTPUT_ID
        require(_OWNS_OUTPUT is False and _OUTPUT_ID is None, "Unconditional fresh this-run ownership state")
        self.path, self.budget, self.total = directory, budget, 0
        self.files = {}
        self.owned = False
        require(not directory.exists() and not directory.is_symlink(), "Fresh output must be absent")
        exact_path(directory.parent, regular=False)
        directory.mkdir()
        self.owned = True
        _OWNS_OUTPUT = True
        self.identity = self.directory_identity()
        _OUTPUT_ID = self.identity

    def directory_identity(self):
        exact_path(self.path, regular=False)
        row = self.path.stat()
        return row.st_dev, row.st_ino, row.st_ctime_ns, row.st_mode, getattr(row, "st_file_attributes", 0), getattr(row, "st_reparse_tag", 0)

    def guard(self):
        self.budget.check()
        require(self.owned and _OWNS_OUTPUT is True and _OUTPUT_ID == self.identity and self.directory_identity() == self.identity, "This-run exclusive output identity")

    def writer(self, name):
        require(name in LEDGER and name not in self.files, "Unique fixed owned output slot")
        return BoundedWriter(self, name)

    def json(self, name, value):
        with self.writer(name) as writer:
            encoder = json.JSONEncoder(sort_keys=True, separators=(",", ":"), ensure_ascii=True)
            for part in encoder.iterencode(value):
                writer.write(part)
            writer.write("\n")


class BoundedWriter:
    def __init__(self, owner, name):
        owner.guard()
        self.owner, self.name, self.buffer = owner, name, bytearray()
        self.path = owner.path / name
        self.handle = self.path.open("xb")
        self.state, self.bytes = hashlib.sha256(), 0
        self.identity = (os.fstat(self.handle.fileno()).st_dev, os.fstat(self.handle.fileno()).st_ino)

    def write(self, text):
        self.write_bytes(text.encode("utf-8"))

    def write_bytes(self, data):
        require(type(data) is bytes, "Exact serialized output bytes required")
        self.buffer.extend(data)
        while len(self.buffer) >= 65536:
            self.flush(65536)

    def flush(self, size=None):
        if not self.buffer:
            return
        self.owner.guard()
        size = len(self.buffer) if size is None else size
        chunk = bytes(self.buffer[:size])
        require(self.owner.total + size <= CAPS["output_bytes_total_maximum"], "Total serialized output byte cap")
        current = self.path.stat()
        require(not self.path.is_symlink() and not getattr(current, "st_reparse_tag", 0)
                and stat.S_ISREG(current.st_mode) and (current.st_dev, current.st_ino) == self.identity
                and current.st_size == self.bytes, "Exclusive streamed output file identity/length")
        require(self.handle.write(chunk) == size, "Complete physical output write")
        self.handle.flush()
        del self.buffer[:size]
        self.state.update(chunk)
        self.bytes += size
        self.owner.total += size

    def __enter__(self):
        return self

    def __exit__(self, kind, value, traceback):
        if kind is None:
            self.flush()
        self.handle.close()
        if kind is None:
            self.owner.guard()
            self.owner.files[self.name] = {"SHA256": self.state.hexdigest(), "bytes": self.bytes}


def selected_json(scope, key, budget):
    path = str(ROOT / key)
    spec = scope["expected_files"][path]
    require(spec["bytes"] <= 8 << 20, "Explicit small selected JSON role")
    raw, _ = checked_bytes(Path(path), spec["SHA256"], spec["bytes"], budget, collect=True)
    return json.loads(raw)


def stream_trace(rows, qubits, emit, *, outputs=()):
    if type(qubits) is not int or qubits < 1 or not callable(emit):
        raise ValueError("Positive exact allocated width and explicit sink required")
    if type(outputs) not in (list, tuple) or any(type(w) is not int or not 0 <= w < qubits for w in outputs) or len(set(outputs)) != len(outputs):
        raise ValueError("Distinct allocated output wires required")
    t_clock, ct_clock = [0] * qubits, [0] * qubits
    frontier = [f"input:{w}" for w in range(qubits)]
    demand_t, demand_ct = {}, {}
    counts = {"X": 0, "CX": 0, "CCX": 0}
    event_count = row_count = 0
    for row_index, row in enumerate(rows):
        if type(row) not in (list, tuple) or len(row) != 4 or any(type(slot) is not int for slot in row):
            raise ValueError("Exactly four signed integer slots required")
        kind = row[0]
        if kind not in (1, 2, 3):
            raise ValueError("Only native X/CX/CCX opcodes admitted")
        operands = tuple(row[1:1 + kind])
        if len(set(operands)) != kind or any(not 0 <= w < qubits for w in operands) or any(row[1 + kind:]):
            raise ValueError("Distinct allocated wires and canonical zero padding required")
        counts[{1: "X", 2: "CX", 3: "CCX"}[kind]] += 1
        row_count += 1
        expanded = CCX_MACRO if kind == 3 else (("X", 0),) if kind == 1 else (("CX", 0, 1),)
        for local_index, primitive in enumerate(expanded):
            label = primitive[0]
            touched = tuple(operands[i] for i in primitive[1:])
            predecessors = tuple((w, frontier[w]) for w in touched)
            paid = int(label in ("T", "TD"))
            t_layer = max(t_clock[w] for w in touched) + paid
            ct_layer = max(ct_clock[w] for w in touched) + 1
            event_id = f"event:{event_count}"
            emit({"event_id": event_id, "native_row_index": row_index,
                  "macro_event_index": local_index, "label": label,
                  "wires": touched, "wire_predecessors": predecessors,
                  "logical_T_layer": t_layer, "logical_Clifford_T_layer": ct_layer,
                  "T_family_demand": paid})
            event_count += 1
            for w in touched:
                t_clock[w], ct_clock[w], frontier[w] = t_layer, ct_layer, event_id
            if paid:
                demand_t[t_layer] = demand_t.get(t_layer, 0) + 1
                demand_ct[ct_layer] = demand_ct.get(ct_layer, 0) + 1
    return {"final_wire_frontier": tuple(frontier),
            "output_wire_frontier": tuple((w, frontier[w]) for w in outputs),
            "final_T_clocks": tuple(t_clock), "final_Clifford_T_clocks": tuple(ct_clock),
            "T_demand_by_logical_T_layer": tuple(sorted(demand_t.items())),
            "T_demand_by_logical_Clifford_T_layer": tuple(sorted(demand_ct.items())),
            "resources": {"allocated_qubits": qubits, "native_gate_rows": row_count,
                          **counts, "T": sum(demand_t.values()),
                          "Clifford_T_macro_events": event_count,
                          "ASAP_T_depth": max(t_clock),
                          "ASAP_Clifford_T_depth": max(ct_clock)}}


def exact(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(exact(a[k], b[k]) for k in b)
    if type(a) in (list, tuple):
        return len(a) == len(b) and all(exact(x, y) for x, y in zip(a, b))
    return a == b


def equal_code(loaded, compiled):
    pending = [(loaded, compiled)]
    count = 0
    while pending:
        a, b = pending.pop()
        require(type(a) is type(b) is types.CodeType and a == b and a.co_filename == b.co_filename
                and a.co_firstlineno == b.co_firstlineno and a.co_linetable == b.co_linetable,
                "Whole root/nested loaded code equals pinned fresh compilation")
        x = [c for c in a.co_consts if isinstance(c, types.CodeType)]
        y = [c for c in b.co_consts if isinstance(c, types.CodeType)]
        require(len(x) == len(y), "Exact ordered child-code census")
        pending.extend(zip(x, y))
        count += 1
    return count


def code_guard(raw, ready):
    tree = ast.parse(raw, filename=str(ROOT / SOURCE_KEY))
    definitions = {n.name:n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    expected = {name:sha(ast.dump(n, include_attributes=False).encode()) for name,n in definitions.items()}
    require(exact(expected, ready["definition_AST_SHA256"]), "All current function/Class ASTs")
    program = compile(tree, str(ROOT / SOURCE_KEY), "exec", dont_inherit=True, optimize=0)
    codes = {c.co_name:c for c in program.co_consts if isinstance(c, types.CodeType)}
    total = 0
    def check_function(value, node, code):
        require(type(value) is types.FunctionType and value.__globals__ is globals(), "Exact loaded function/global namespace")
        defaults = tuple(ast.literal_eval(n) for n in node.args.defaults) or None
        kw = {n.arg:ast.literal_eval(v) for n,v in zip(node.args.kwonlyargs,node.args.kw_defaults) if v is not None} or None
        require(exact(value.__defaults__, defaults) and exact(value.__kwdefaults__, kw)
                and value.__annotations__ == {} and value.__dict__ == {}, "Whole function defaults/annotations/attributes")
        return equal_code(value.__code__, code)
    for name,node in definitions.items():
        value = globals()[name]
        if isinstance(node, ast.FunctionDef):
            total += check_function(value,node,codes[name])
        else:
            require(type(value) is type and value.__module__ == __name__, "Current Class identity")
            methods = {n.name:n for n in node.body if isinstance(n, ast.FunctionDef)}
            method_codes = {c.co_name:c for c in codes[name].co_consts if isinstance(c, types.CodeType)}
            require(set(vars(value)) == set(methods) | {"__module__","__dict__","__weakref__","__doc__"}, "Exact current Class namespace")
            for method,n in methods.items():
                total += check_function(vars(value)[method],n,method_codes[method])
    aliases = {}
    def literal(node):
        if isinstance(node, ast.Name):
            require(node.id in aliases, "Previously closed initializer alias")
            return aliases[node.id]
        if isinstance(node, ast.Call) and isinstance(node.func,ast.Name) and node.func.id == "Path":
            require(len(node.args) == 1 and not node.keywords, "One literal Path initializer")
            return Path(ast.literal_eval(node.args[0]))
        if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div):
            return literal(node.left) / literal(node.right)
        return ast.literal_eval(node)
    bound = set(definitions)
    for node in tree.body:
        if isinstance(node,ast.Import):
            bound.update(n.asname or n.name.split('.')[0] for n in node.names)
        elif isinstance(node,ast.ImportFrom):
            bound.update(n.asname or n.name for n in node.names)
        elif isinstance(node,ast.Assign):
            require(len(node.targets)==1 and isinstance(node.targets[0],ast.Name), "Only explicit single-name module initializers")
            name = node.targets[0].id
            bound.add(name)
            if name == "WALL_START":
                require(ast.unparse(node.value) == "time.perf_counter()" and type(WALL_START) is float
                        and WALL_START <= time.perf_counter(), "Original this-process clock; no reset")
            elif name in {"_OWNS_OUTPUT","_OUTPUT_ID"}:
                require(ast.literal_eval(node.value) is (False if name=="_OWNS_OUTPUT" else None), "Unconditional this-run ownership initializers")
            else:
                aliases[name] = literal(node.value)
                require(exact(globals()[name],aliases[name]), "Every immutable literal/Path module alias remains exact")
    standard = {"__name__","__doc__","__package__","__loader__","__spec__","__annotations__","__builtins__","__file__","__cached__"}
    require(set(globals()) == bound | standard and __annotations__ == {} and type(__doc__) is str
            and __doc__ == program.co_consts[0], "Whole current module namespace/docstring")
    require(type(_OWNS_OUTPUT) is bool, "Exact tracked this-run ownership type")
    if _OWNS_OUTPUT:
        row=exact_path(ROOT/OUTPUT_KEY,regular=False).stat()
        current=(row.st_dev,row.st_ino,row.st_ctime_ns,row.st_mode,getattr(row,"st_file_attributes",0),getattr(row,"st_reparse_tag",0))
        require(type(_OUTPUT_ID) is tuple and len(_OUTPUT_ID)==6 and _OUTPUT_ID==current, "Tracked owned output exact stable six-field identity")
    else:
        require(_OUTPUT_ID is None, "No precreation output identity or false ownership")
    require(Path is sys.modules["pathlib"].Path and types is sys.modules["types"] and ast is sys.modules["ast"]
            and stat is sys.modules["stat"] and struct is sys.modules["struct"], "Selected import identities")
    require(exact(LEDGER,ready["exact14_inclusive_ledger"]) and sys.get_int_max_str_digits()==4300, "Fixed ledger/default4300")
    return {"passed":True,"definition_count":len(definitions),"paired_loaded_code_objects":total,
            "all_root_nested_defaults_and_module_literals_checked":True,"fresh_source_functions_executed":False}


def hash_inputs(scope, budget):
    found = {}
    require(len(scope["expected_files"]) <= CAPS["selected_paths_max"]
            and sum(v["bytes"] for v in scope["expected_files"].values()) <= CAPS["selected_bytes_max"], "Fixed complete selected scope caps")
    for key,spec in scope["expected_files"].items():
        require(set(spec)=={"SHA256","bytes","original_stat8"} and type(spec["original_stat8"]) is list
                and len(spec["original_stat8"])==8 and all(type(v) is int for v in spec["original_stat8"])
                and spec["bytes"] <= CAPS["single_selected_file_bytes_max"]
                and not Path(key).is_relative_to(ROOT / OUTPUT_KEY), "Only prior selected input identities; output excluded")
        _, found[key] = checked_bytes(Path(key),spec["SHA256"],spec["bytes"],budget)
        require(found[key] == tuple(spec["original_stat8"]), "Original eight-field identity for every selected path")
    for key in scope["absent_cache_paths"]:
        require(not Path(key).exists() and not Path(key).is_symlink(), "All original selected cache absences remain exact")
    return found


def review_admission(ready, own, budget):
    require(set(ready["current_review_roles"]) == {"author_QA","independent_SOURCE_peer","ROOT_static_review"}, "Exact current three reviews")
    rows = {}
    for role,key in REVIEW_ROUTES.items():
        spec = ready["current_review_roles"][role]
        require(set(spec)=={"path","SHA256"} and spec["path"]==key, "Explicit current review route")
        row,fp = read_pinned_json(ROOT/key,spec["SHA256"],budget)
        require(all(row[k] is True for k in ("passed","science_static_passed","lifecycle_static_passed")) and row["blockers"]==[], "Whole dual static approval")
        require(exact(row["author_method_SHA256"],{SOURCE_KEY:own[SOURCE_KEY]["SHA256"],SCOPE_KEY:ready["input_adapter_SHA256"],MD_KEY:ready["preflight"]["SHA256"]})
                and exact(row["complete_definition_AST_SHA256"],ready["definition_AST_SHA256"])
                and exact(row["caps"],CAPS) and exact(row["exact14_inclusive_ledger"],LEDGER), "All current SOURCE/adapter/MD/AST/caps/ledger joins")
        rows[key] = {"expected_SHA256":spec["SHA256"],"original_stat8":list(fp)}
    return rows


def admit_premises(scope, budget):
    plan = selected_json(scope,PLAN_KEY,budget)
    require(plan["schema"] == "a13-first-stock-signed7-shift-caller-prospective-plan-v1"
            and plan["array_role"]["path"]==ARRAY_KEY and plan["array_role"]["expected_SHA256"]==ARRAY_SHA
            and plan["exact14_inclusive_future_ledger"]==LEDGER and plan["fixed_finite_cohort"]["records"]==912
            and exact(plan["interface"],INTERFACE), "Exact immutable accepted plan and caller boundary")
    descriptor = selected_json(scope,DESC_KEY,budget)
    require(descriptor["key"]=="16077b59a0122da5ed2f" and descriptor["op"]=="shift" and descriptor["params"]=={}
            and descriptor["sha256"]==ARRAY_SHA and descriptor["gate_file"]==Path(ARRAY_KEY).name
            and exact(descriptor["args"],[list(range(72)),list(range(72,144))])
            and exact(descriptor["outs"],[list(range(144,216))])
            and descriptor["resources"]["qubits"]==807 and descriptor["spec"]["width"]==72
            and descriptor["spec"]["fraction_bits"]==40 and descriptor["spec"]["count_bits"]==7
            and descriptor["spec"]["count_scale"]=="unscaled integer; fraction_bits does not scale the count"
            and descriptor["spec"]["lowering"]=="signed-count-narrow-barrel-shift-v1"
            and exact(descriptor["input_contract"],{"signed_shift_count_bits":7}), "Actual archived full72 signed7 descriptor")
    old = selected_json(scope,"results/limitation_program_20261001/A01_run009/manifest.json",budget)
    historical = selected_json(scope,"results/limitation_program_20261001/A07_shift_leaf_run001/manifest.json",budget)
    require(old["frozen_inputs"][ARRAY_KEY]==ARRAY_SHA
            and historical["files"][ARRAY_KEY.replace('/','\\')]==ARRAY_SHA
            and historical["files"][DESC_KEY.replace('/','\\')]==scope["expected_files"][str(ROOT/DESC_KEY)]["SHA256"], "Original expected descriptor and array pins; no observed authority")
    proof = selected_json(scope,ARITHMETIC_KEY,budget)
    require(proof["passed"] is proof["all_word_identity"] is True and proof["signed_count_bits"]==7
            and proof["full_native_width"]==72 and proof["admissible_count_interval"]==[-64,63]
            and proof["unsigned_magnitude_interval"]==[0,64] and proof["minimum_count_magnitude"]==64
            and proof["direction"]=="nonnegative count: left modulo2**72; negative count: arithmetic right", "Pinned algebraic all-data signed-shift proof, not finite enumeration")
    boundary = selected_json(scope,BOUNDARY_ROOT_KEY,budget)
    require(boundary["passed"] is True and boundary["ROOT_observed_terminal_exit_code"]==0
            and boundary["manifest_SHA256"]==scope["expected_files"][str(ROOT/BOUNDARY_MF_KEY)]["SHA256"]
            and boundary["saved912_forward_and_inverse_logical_case_scalar_identities_checked"] is True
            and boundary["financial_G2_hardware_or_quantum_advantage"] is False, "Own completed logical first-stock premise only")
    cases = selected_json(scope,CASES_KEY,budget)
    mf = selected_json(scope,BOUNDARY_MF_KEY,budget)
    require(cases["schema"]=="a13-first-stock-fixed-logical-caller-cases-v1" and cases["passed"] is True
            and cases["logical_integer_source_only"] is True and cases["quantum_circuit_phase_or_workspace_simulated"] is False
            and cases["forward_count"]==cases["inverse_count"]==len(cases["cases"])==912
            and mf["files"]["fixed_logical_caller_cases.json"]==scope["expected_files"][str(ROOT/CASES_KEY)]["SHA256"], "Exact saved912 cohort authority and original order")
    macro = selected_json(scope,MACRO_KEY,budget)
    phase = selected_json(scope,PHASE_KEY,budget)
    require(exact(macro["macro"],[list(row) for row in CCX_MACRO])
            and phase["passed"] is phase["absolute_unit_global_phase"] is True
            and phase["relative_phase_or_approximate_CCX_used"] is False, "Separately pinned exact paid15-event7T unit-phase macro")
    return plan,descriptor,proof,cases,boundary,phase


def decode_archive(raw, descriptor):
    require(type(raw) is bytes and raw[:8]==b"\x93NUMPY\x01\x00", "Exact archived NumPy v1 data; no numpy import")
    length = struct.unpack_from("<H",raw,8)[0]
    require(0 < length < 65536 and len(raw)>=10+length, "Finite complete native header")
    header = ast.literal_eval(raw[10:10+length].decode("ascii").strip())
    expected = {"descr":"<i4","fortran_order":False,"shape":(descriptor["resources"]["source_gates"],4)}
    require(exact(header,expected), "Exact typed little-endian four-int native shape")
    body = raw[10+length:]
    require(len(body)==16*descriptor["resources"]["source_gates"] and len(body)//16 <= CAPS["native_rows_maximum"], "Complete array byte/row coverage")
    return list(struct.iter_unpack("<iiii",body))


def make_mapping(descriptor):
    require(descriptor["resources"]["qubits"]==807, "Archived807-wire allocation")
    mapping = list(range(217,361)) + list(range(144,216)) + list(range(361,952))
    contract = {"schema":"signed7-full72-caller-map-v1","count_scale":"unscaled integer","count_bits":7,
        "count_sign_extension_width":72,"caller_args":[list(range(72)),list(range(72,144))],"caller_out":list(range(144,216)),
        "spectators":[216],"local_args":[list(range(217,289)),list(range(289,361))],"private":list(range(361,952)),
        "leaf_wire_map":mapping,"allocated_qubits":952,"copy_CX":144,"uncopy_CX":144,
        "private_entry":"zero","private_exit":"zero","output_copy_count":72,"literal_reverse_complete":True}
    validate_mapping(contract)
    return contract


def validate_mapping(contract):
    require(contract["count_scale"]=="unscaled integer", "SHIFT_CALLER_UNSCALED_COUNT")
    require(type(contract["count_bits"]) is type(contract["count_sign_extension_width"]) is int
            and contract["count_bits"]==7 and contract["count_sign_extension_width"]==72, "SHIFT_CALLER_SIGNED7_EXTENSION")
    require(exact(contract["caller_args"],[list(range(72)),list(range(72,144))])
            and exact(contract["caller_out"],list(range(144,216))) and exact(contract["spectators"],[216])
            and exact(contract["local_args"],[list(range(217,289)),list(range(289,361))])
            and exact(contract["private"],list(range(361,952))) and type(contract["allocated_qubits"]) is int
            and contract["allocated_qubits"]==952, "SHIFT_CALLER_PORT_INJECTION")
    mapping=contract["leaf_wire_map"]
    require(type(mapping) is list and len(mapping)==807 and all(type(v) is int and 0<=v<952 for v in mapping)
            and len(set(mapping))==807 and exact(mapping,list(range(217,361))+list(range(144,216))+list(range(361,952)))
            and not set(mapping)&set(list(range(144))+[216]), "SHIFT_CALLER_PORT_INJECTION")
    require(contract["private_entry"]==contract["private_exit"]=="zero", "SHIFT_CALLER_PRIVATE_CLEAN")
    require(type(contract["output_copy_count"]) is int and contract["output_copy_count"]==72
            and contract["literal_reverse_complete"] is True and type(contract["copy_CX"]) is type(contract["uncopy_CX"]) is int
            and contract["copy_CX"]==contract["uncopy_CX"]==144, "SHIFT_CALLER_COMPLETE_INVERSE")


def structural_witness(rows, descriptor, proof, contract, budget):
    outputs=set(range(144,216))
    copies=[]
    for index,row in enumerate(rows):
        if index%128==0:
            budget.check()
        kind=row[0]
        require(type(row) is tuple and len(row)==4 and all(type(v) is int for v in row) and kind in (1,2,3), "Native X/CX/CCX grammar")
        wires=row[1:1+kind]
        require(len(set(wires))==kind and all(0<=v<807 for v in wires) and not any(row[1+kind:]), "Native allocated distinct operands/canonical padding")
        require(wires[-1]>=144 and not set(wires)&set(range(79,144)), "Original inputs never targets; high65 count bits untouched")
        require(not set(wires[:-1])&outputs, "Dirty output is never a control")
        if wires[-1] in outputs:
            require(kind==2 and wires[0]>=216, "Only clean-work to dirty-output copy")
            copies.append(index)
    midpoint=(len(rows)-72)//2
    require(len(rows)==descriptor["resources"]["source_gates"] and len(rows)%2==0
            and copies==list(range(midpoint,midpoint+72))
            and [rows[i][2] for i in copies]==list(range(144,216))
            and rows[midpoint+72:]==list(reversed(rows[:midpoint])), "Exact complete compute/72copy/literal reverse")
    validate_mapping(contract)
    return {"schema":"signed7-archived-caller-structural-phase-v1","passed":True,"array_SHA256":ARRAY_SHA,
        "source_gates":len(rows),"compute_interval":[0,midpoint],"output_copy_interval":[midpoint,midpoint+72],
        "literal_reverse_interval":[midpoint+72,len(rows)],"no_input_targets_output_controls_or_high_count_selectors":True,
        "all72_dirty_output_copies_and_complete_literal_private_inverse":True,"original_algebraic_all_word_identity_cited":proof["all_word_identity"],
        "native_X_CX_CCX_basis_permutations_have_absolute_phase_one":True,
        "injective_caller_and_clean_private_subspace_extension_by_linearity":True,
        "arbitrary_external_reference_entanglement_preserved_by_disjoint_identity":True,
        "finite912_cohort_is_not_the_universal_proof":True,
        "proof":["The pinned original signed7 all-data magnitude/reversal/barrel identity applies to every full72 data word under the sign-extension promise.",
            "The exact archived compute body, all72 dirty output XOR copies and literal reverse preserve both input words and clear all private work.",
            "The caller's first144 CX copies the two unchanged full72 arguments into clean disjoint locals; the leaf output is the external dirty72 bank.",
            "The final144 reversed argument CXs clear the locals. All native gates have phase+1, so the operator is exact on the clean-workspace promised span and its coherent/reference extension."],
        "whole_polynomial_row_log_clipping_or_financial_caller_compiled":False}


def wrapped_rows(rows, contract):
    validate_mapping(contract)
    prefix=[(2,a,b,0) for caller,local in zip(contract["caller_args"],contract["local_args"]) for a,b in zip(caller,local)]
    mapping=contract["leaf_wire_map"]
    mapped=[tuple([row[0]]+[mapping[w] for w in row[1:1+row[0]]]+[0]*(3-row[0])) for row in rows]
    return prefix+mapped+list(reversed(prefix))


def packed_payloads(cases, contract, start_index):
    require(type(cases) is list and 1<=len(cases)<=64 and type(start_index) is int and start_index>=0, "Finite vector batch with original cohort offset")
    initial=[0]*contract["allocated_qubits"]
    for index,case in enumerate(cases):
        require(set(case)==CASE_KEYS and type(case["id"]) is str and type(case["k"]) is int and -17<=case["k"]<=12,
                "Exact own saved case identity and unscaled declared count")
        require(all(type(case[k]) is int for k in ("polynomial","dirty_raw","stock_raw","output_raw"))
                and all(0<=case[k]<=MASK for k in ("polynomial","dirty_raw","stock_raw","output_raw"))
                and case["output_raw"]==case["dirty_raw"]^case["stock_raw"]
                and case["source_input_preserved"] is case["inverse_restores_dirty"] is True, "Own saved raw output identity and original logical premise")
        values=[case["polynomial"],case["k"]&MASK,case["dirty_raw"]]
        for value,bank in zip(values,contract["caller_args"]+[contract["caller_out"]]):
            for bit,wire in enumerate(bank):
                initial[wire]|=((value>>bit)&1)<<index
        initial[216]|=((start_index+index)&1)<<index
    expected=initial[:]
    for index,case in enumerate(cases):
        for bit,wire in enumerate(contract["caller_out"]):
            expected[wire]=(expected[wire]&~(1<<index))|(((case["output_raw"]>>bit)&1)<<index)
    return initial,expected


def simulate(rows, wires, mask, checkpoint=None):
    require(type(mask) is int and mask>0, "Exact finite vector basis mask")
    for index,(kind,a,b,c) in enumerate(rows):
        if checkpoint and index%128==0:
            checkpoint()
        if kind==1:
            wires[a]^=mask
        elif kind==2:
            wires[b]^=wires[a]
        elif kind==3:
            wires[c]^=wires[a]&wires[b]
        else:
            raise ValueError("Only native exact X/CX/CCX")
    return wires


def current_controls(contract):
    categories={}
    changes=[("SHIFT_CALLER_UNSCALED_COUNT","count_scale","k_Q scaled by2**40"),
        ("SHIFT_CALLER_SIGNED7_EXTENSION","count_sign_extension_width",7),
        ("SHIFT_CALLER_PORT_INJECTION","leaf_wire_map",[0]+contract["leaf_wire_map"][1:]),
        ("SHIFT_CALLER_PRIVATE_CLEAN","private_entry","dirty"),
        ("SHIFT_CALLER_COMPLETE_INVERSE","output_copy_count",71)]
    for tag,key,value in changes:
        validate_mapping(contract)
        bad=json.loads(json.dumps(contract))
        bad[key]=value
        rejected=False
        try:
            validate_mapping(bad)
        except ValueError as error:
            require(str(error)==tag, "Dedicated typed metadata rejection category")
            rejected=True
        require(rejected,"Current signed-shift metadata mutation rejected")
        categories[tag]={"positive_passed_first":True,"mutation_rejected":True,"mutated_field":key,"metadata_only_control":True}
    return {"passed":True,"category_count":5,"categories":categories,"old_controls_or_new_array_mutations_replayed":False,
            "finite_control_credit_is_not_whole_caller_or_financial_credit":True}


def main():
    require(len(sys.argv)==3 and sys.argv[1]=="--root-ready-sha256" and len(sys.argv[2])==64
            and all(c in "0123456789abcdef" for c in sys.argv[2]), "Exact external ROOT READY command")
    require(Path.cwd().resolve()==ROOT and sys.version_info[:3]==(3,12,4) and sys.flags.isolated==sys.flags.no_site==1
            and sys.flags.dont_write_bytecode and sys.flags.optimize==0 and sys.get_int_max_str_digits()==4300,
            "Exact isolated default4300 command; no setter")
    require(sys.orig_argv[1:]==["-I","-S","-B",str(ROOT/SOURCE_KEY),"--root-ready-sha256",sys.argv[2]]
            and "PYTHONINTMAXSTRDIGITS" not in os.environ and "int_max_str_digits" not in sys._xoptions, "Exact command tail/no parser override")
    require((ROOT/READY_KEY).stat().st_size <= 8 << 20,"Finite ROOT READY JSON")
    ready_raw,ready_fp=checked_bytes(ROOT/READY_KEY,sys.argv[2],(ROOT/READY_KEY).stat().st_size,collect=True)
    ready=json.loads(ready_raw)
    require(set(ready)==set(READY_KEYS) and ready["schema"]=="a13-signed7-shift-caller-root-ready-v1"
            and ready["ready"] is ready["signed_shift_caller_execution_authorized"] is True
            and ready["input_adapter_path"]==SCOPE_KEY and ready["output_directory"]==OUTPUT_KEY
            and exact(ready["caps"],CAPS) and exact(ready["exact14_inclusive_ledger"],LEDGER), "Closed one-run ROOT authority")
    own=ready["own_source_expected_files"]
    require(set(own)=={SOURCE_KEY} and set(own[SOURCE_KEY])=={"SHA256","bytes"}
            and own[SOURCE_KEY]["bytes"]<=CAPS["source_bytes_max"], "One entire current SOURCE byte authority")
    raw,own_fp=checked_bytes(ROOT/SOURCE_KEY,own[SOURCE_KEY]["SHA256"],own[SOURCE_KEY]["bytes"],collect=True)
    budget,output=Budget(),None
    try:
        source_guard=code_guard(raw,ready)
        reviews=review_admission(ready,own,budget)
        require((ROOT/SCOPE_KEY).stat().st_size <= 8 << 20,"Finite current adapter JSON")
        scope_raw,scope_fp=checked_bytes(ROOT/SCOPE_KEY,ready["input_adapter_SHA256"],(ROOT/SCOPE_KEY).stat().st_size,budget,collect=True)
        scope=json.loads(scope_raw)
        require(scope["schema"]=="a13-signed7-shift-caller-input-adapter-v1" and scope["PLAN_SHA256"]==PLAN_SHA
                and scope["PLAN_path"]==PLAN_KEY and exact(scope["caps"],CAPS) and exact(scope["output_ledger"],LEDGER)
                and scope["expected_files_canonical_SHA256"]==sha(json.dumps(scope["expected_files"],sort_keys=True,separators=(",",":")).encode()),
                "Complete bounded expected-only selected adapter")
        env=scope["explicit_environment_roles"]
        require(sys.executable==env["venv_launcher"]==str(ROOT/".context/frontier_t0_env/Scripts/python.exe")
                and sys.orig_argv[0]==sys._base_executable==env["base_python"], "Separate pinned Windows venv/base identities")
        require(ready["preflight"]["path"]==MD_KEY and set(ready["preflight"])=={"path","SHA256"}, "Exact current preflight route")
        md,md_fp=checked_bytes(ROOT/MD_KEY,ready["preflight"]["SHA256"],(ROOT/MD_KEY).stat().st_size,budget,collect=True)
        runtime_origins(scope)
        before=hash_inputs(scope,budget)
        plan,descriptor,proof,cases,boundary,phase=admit_premises(scope,budget)
        require(scope["expected_files"][str(ROOT/ARRAY_KEY)]["SHA256"]==ARRAY_SHA
                and ready["preflight"]["SHA256"]==scope["current_preflight_expected_SHA256"], "Exact selected original array/current prose")
        runtime_origins(scope)
        budget.check()
        budget.admitted=True
        # First numerical array consumption occurs only after current three
        # reviews, origin/admission checks and the complete first byte pass.
        spec=scope["expected_files"][str(ROOT/ARRAY_KEY)]
        archive,_=checked_bytes(ROOT/ARRAY_KEY,spec["SHA256"],spec["bytes"],budget,collect=True)
        rows=decode_archive(archive,descriptor)
        contract=make_mapping(descriptor)
        structure=structural_witness(rows,descriptor,proof,contract,budget)
        wrapped=wrapped_rows(rows,contract)
        output=OwnedOutput(ROOT/OUTPUT_KEY,budget)
        for name,data in (("executed_controller.py",raw),("executed_adapter.json",scope_raw),
                          ("executed_preflight.md",md),("executed_ROOT_READY.json",ready_raw)):
            with output.writer(name) as writer:
                writer.write_bytes(data)
        output.json("run_started.json",{"schema":"signed7-shift-caller-run-started-v1","ROOT_READY_SHA256":sys.argv[2],
            "own_source_expected_files":own,"input_adapter_SHA256":ready["input_adapter_SHA256"],"current_review_roles":ready["current_review_roles"],
            "source_guard":source_guard,"current_reviews_bound_before_selected_array":True,"caps":CAPS,"admission_observation":budget.check()})
        output.json("selected_premise_authority.json",{"schema":"signed7-shift-caller-selected-premises-v1","expected_files":scope["expected_files"],
            "first_pass_original_stat8":{k:list(v) for k,v in before.items()},"original_plan_SHA256":PLAN_SHA,
            "ROOT_READY_SHA256":sys.argv[2],"current_review_original_identities":reviews,"no_transitive_financial_union_recertification":True})
        output.json("source_interface_and_universal_contract.json",{"passed":True,"interface":INTERFACE,"caller_mapping":contract,
            "entire_original_count_interval_inside_signed7":True,"arithmetic_proof_SHA256":scope["expected_files"][str(ROOT/ARITHMETIC_KEY)]["SHA256"],
            "unscaled_count3979_candidate_polynomial15_output4021":True,"original_negative_shift_floor_payment_retained":True,
            "compiled_full_polynomial_row_or_clipping_caller":False})
        output.json("archived_leaf_structural_phase_witness.json",structure)
        batches=[]
        for start in range(0,912,64):
            cohort=cases["cases"][start:start+64]
            initial,expected=packed_payloads(cohort,contract,start)
            mask=(1<<len(cohort))-1
            final=simulate(wrapped,initial[:],mask,budget.check)
            require(final==expected,"All952 full caller/local/private/spectator wires match saved forward outputs")
            inverse=simulate(reversed(wrapped),final[:],mask,budget.check)
            require(inverse==initial,"Every allocated wire restored by the full literal inverse")
            batches.append({"start_index":start,"case_count":len(cohort),"case_ids":[c["id"] for c in cohort],"passed":True,
                "all_allocated_wires_checked":contract["allocated_qubits"],"forward_state_SHA256":sha(json.dumps(final,separators=(",",":")).encode()),
                "inverse_state_SHA256":sha(json.dumps(inverse,separators=(",",":")).encode()),"all_inputs_locals_private_spectators_restored":True})
        output.json("fixed_912_caller_cases.json",{"schema":"signed7-shift-caller-fixed912-v1","passed":True,"forward_count":912,"inverse_count":912,
            "original_case_SHA256":scope["expected_files"][str(ROOT/CASES_KEY)]["SHA256"],"cases":cases["cases"],"original_cases_order_and_values_unchanged":True,
            "batch_maximum":64,"batches":batches,"physical_packed_forward_passes":len(batches),"physical_packed_inverse_passes":len(batches),
            "finite_cohort_is_not_universal_proof":True})
        output.json("positive_first_controls.json",current_controls(contract))
        calls=[0]
        def checkpoint(event):
            if calls[0]%128==0:
                budget.check()
            calls[0]+=1
        standalone=stream_trace(rows,807,checkpoint,outputs=descriptor["outs"][0])["resources"]
        archived=descriptor["resources"]
        saved={"allocated_qubits":archived["qubits"],"native_gate_rows":archived["source_gates"],"X":archived["x"],"CX":archived["cx"],
            "CCX":archived["ccx"],"T":archived["t_count"],"Clifford_T_macro_events":archived["x"]+archived["cx"]+15*archived["ccx"],
            "ASAP_T_depth":archived["t_depth"],"ASAP_Clifford_T_depth":archived["clifford_t_depth"]}
        require(exact(standalone,saved),"Exact independently evaluated archived logical resources")
        calls[0]=0
        caller=stream_trace(wrapped,contract["allocated_qubits"],checkpoint,outputs=contract["caller_out"])["resources"]
        require(caller["CX"]==standalone["CX"]+288 and caller["native_gate_rows"]==standalone["native_gate_rows"]+288
                and caller["Clifford_T_macro_events"]==standalone["Clifford_T_macro_events"]+288
                and all(caller[k]==standalone[k] for k in ("X","CCX","T")),"Exactly144 copy plus144 uncopy CX, no free local work")
        resources={"schema":"signed7-shift-caller-paid-logical-resources-v1","passed":True,"standalone_archived_resources":standalone,
            "actual_caller_resources":caller,"argument_copy_CX":144,"argument_uncopy_CX":144,"exact_paid15_event7T_macro":True,
            "paid_macro_absolute_phase_premise_SHA256":scope["expected_files"][str(ROOT/PHASE_KEY)]["SHA256"],
            "native_permutation_phase_and_paid_convention_are_separate_claims":True,"new_whole_financial_compilation_cost":False,
            "physical_ticks_factory_yield_or_delivery":False}
        output.json("paid_caller_resources.json",resources)
        qualification={"actual_archived_signed7_array_evaluated":True,"isolated_compiled_shift_caller_at_stock4021":True,
            "full72_unscaled_signed7_count_dirty_output_and_original_inputs":True,"argument144_copy144_uncopy_and591_private_clean":True,
            "fixed912_forward_and_inverse_and_spectator_restoration":True,"universal_structural_algebraic_native_phase_extension":True,
            "paid_exact15_event7T_macro_has_separately_pinned_absolute_phase":True,"Tdag_Clifford_frame_premise_required":True,
            "full_polynomial_row_to_shift_or_log_reduction_clipping_coherently_integrated":False,"new_financial_L2_or_price_certificate":False,
            "whole_B4x12_G2_hardware_adoption_or_advantage":False,"original_producer_or_dirty_primitives_imported_or_called":False,"fixture_credit":0}
        output.json("qualification.json",qualification)
        after=hash_inputs(scope,budget)
        require(before==after,"Both fresh complete selected byte passes retain all original eight-field identities")
        runtime_origins(scope)
        last_raw,last_own=checked_bytes(ROOT/SOURCE_KEY,own[SOURCE_KEY]["SHA256"],own[SOURCE_KEY]["bytes"],budget,collect=True)
        require(last_own==own_fp and last_raw==raw,"Whole current SOURCE retains original bytes/identity")
        final_guard=code_guard(last_raw,ready)
        require(final_guard==source_guard,"Whole loaded code/literals/defaults stable after numerical work")
        for key,spec in ready["current_review_roles"].items():
            _,fp=read_pinned_json(ROOT/spec["path"],spec["SHA256"],budget)
            require(list(fp)==reviews[spec["path"]]["original_stat8"],"Every current review remains exact")
        _,last_scope=read_pinned_json(ROOT/SCOPE_KEY,ready["input_adapter_SHA256"],budget)
        _,last_ready=read_pinned_json(ROOT/READY_KEY,sys.argv[2],budget)
        _,last_md=checked_bytes(ROOT/MD_KEY,ready["preflight"]["SHA256"],len(md),budget)
        require(last_scope==scope_fp and last_ready==ready_fp and last_md==md_fp,"Adapter/READY/preflight original identities unchanged")
        output.json("summary.json",{"passed":True,"completed":True,"caps":CAPS,"preseal_observation":budget.check(),
            "both_complete_selected_input_hash_passes":True,"selected_expected_roles":len(before),"all_original_stat8_retained":True,
            "forward_case_count":912,"inverse_case_count":912,"positive_first_control_categories":5,
            "actual_caller_resources":caller,"ROOT_READY_SHA256":sys.argv[2],**qualification})
        require(set(output.files)==set(LEDGER)-{"manifest.json"} and {p.name for p in output.path.iterdir()}==set(output.files), "Exact13 preseal physical files")
        for name,spec in output.files.items():
            checked_bytes(output.path/name,spec["SHA256"],spec["bytes"],budget)
        output.json("manifest.json",{"schema":"signed7-shift-caller-manifest-v1","passed":True,"completed":True,"manifest_self_hash_excluded":True,
            "manifest_inclusive_owned_file_count":14,"files":dict(output.files),"owned_nonmanifest_bytes":output.total,
            "ROOT_READY_SHA256":sys.argv[2],"input_adapter_SHA256":ready["input_adapter_SHA256"],"isolated_shift_caller_only":True,
            "whole_financial_hardware_or_advantage":False})
        require({p.name for p in output.path.iterdir()}==set(LEDGER),"Exact14 sealed owned files, no marker")
        output.guard()
        print(json.dumps({"passed":True,"manifest_SHA256":output.files["manifest.json"]["SHA256"],"output_directory":OUTPUT_KEY,
            "actual_caller_resources":caller,"forward_case_count":912,"inverse_case_count":912}))
    except BaseException as error:
        if output is not None and output.owned and output.directory_identity()==output.identity:
            marker=output.path/"FAILED_UNSEALED.json"
            if not marker.exists():
                failure=json.dumps({"passed":False,"completed":False,"error_type":type(error).__name__,"reason":str(error),"zero_result_credit":True}).encode()
                require(len(failure)<=65536,"Bounded owned failure marker")
                with marker.open("xb") as handle:
                    require(handle.write(failure)==len(failure),"Complete preserved failure marker")
        raise


if __name__ == "__main__":
    main()
