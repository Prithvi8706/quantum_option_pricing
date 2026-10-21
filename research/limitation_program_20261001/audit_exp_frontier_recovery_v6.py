"""Independent130 A13 exploratory exponential frontier, AUTHOR ONLY.

No producer/helper imports, coefficient fitting, proof, source walk or numerical
operation has executed during authoring. All20 fixed choices share one future
300/270/900 process budget. NULL G2 allocation excludes feasibility/adoption.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from fractions import Fraction
import gzip
import hashlib
from importlib import metadata
from importlib.util import cache_from_source
import json
from math import comb, factorial, lcm
import os
from pathlib import Path, PureWindowsPath
import re
import site
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "A13_recovery_run001"
OUTPUT = PROGRAM / "A13_recovery_audit_run006"
MATERIAL = PROGRAM / "A13_run002"
CAPTURE = PROGRAM / "A13_terminal_failure_capture_run002"
AUTHOR = RESEARCH / "audit_exp_frontier_recovery_v6.py"
PRODUCER_AUTHOR = RESEARCH / "experiment_exp_frontier_recovery.py"
METHOD = RESEARCH / "a13_exp_frontier_preflight.json"
METHOD_DOC = RESEARCH / "A13_EXP_FRONTIER_PREFLIGHT.md"
IMPLEMENTATION = RESEARCH / "a13_exp_frontier_recovery_audit_implementation_preflight_v6.json"
IMPLEMENTATION_DOC = RESEARCH / "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V6.md"
RECOVERY_METHOD = RESEARCH / "a13_exp_frontier_recovery_preflight.json"
RECOVERY_METHOD_DOC = RESEARCH / "A13_EXP_FRONTIER_RECOVERY_PREFLIGHT.md"
LAUNCHER = ROOT / ".context/frontier_t0_env/Scripts/python.exe"
METHOD_SHA = "6c0e97f33e1277c070e6e84883b6631a880997becd214772bb9ef287e1c7ba85"
METHOD_DOC_SHA = "f5b4404650c1ee9bd3a8ef2557d67e1340dda0fc059d94126e19fcfc046d7f7b"
CPU, ADMISSION, WALL, DIGITS = 300, 270, 900, 130
Q, N, W = 1 << 40, 1 << 32, 72
EPS = Fraction(1, Q)
GRID = tuple((d, s) for d in (4, 6, 8, 10, 12) for s in (1, 2, 4, 8))
EXPONENTS = tuple(range(-17, 13))
CASES = {"B4x12": (4, 12, 30), "B8x52": (8, 52, 234)}
BASELINE = {"B4x12": (520720662, 555774, 550141), "B8x52": (4267435214, 663704, 4460479)}
RESOURCE_FIELDS = (
    "source_gates",
    "x",
    "cx",
    "ccx",
    "t_count",
    "t_depth",
    "clifford_t_depth",
    "clifford_cx",
    "clifford_h",
)
PATH_CACHE, ACTUAL_HASH_CACHE, OBSERVED_HASHES = {}, {}, {}
BASE_TREES, BASE_FILES = (), ()
BASE_PREFIX = BASE_SITE_LEXICAL = BASE_SITE = None
MAX_RUNTIME_FILES, MAX_RUNTIME_BYTES = 24000, 2 * 1024**3
SHA_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
A07_SHA = "7380a91d89d4d7657533290406712139dee98913eef4ba60cb71e1de7e0e1f7e"
PRIOR_AUTHOR_SHA256 = {
    "experiment_exp_frontier.py": (
        "0fff55c681f3ecf0dca8cd8e50f4f20be1b276e6c7481a651ede5cd90661a78e"
    ),
    "audit_exp_frontier.py": "3385268148620aa1618452bdd14d678eed9c457f327d0c59fcbb04cabebae93a",
    "A13_EXP_FRONTIER_IMPLEMENTATION_PREFLIGHT.md": (
        "5aa7ace3c45c3c0734e933624b321d7b575de3d38ba206b73a27b92db41649e3"
    ),
    "a13_exp_frontier_implementation_preflight.json": (
        "08658b0283b293337c5e9965f37aff1643e21873fec99a9962fc2b9c392cee59"
    ),
}
PRIOR_FAILED = PROGRAM / "A13_run001"
PRIOR_FAILED_SHA = "d77077cfb2d67ee2973a02b236ea6e6b2336962f35fed6ce4aeb48ef8bb65aa8"
PRIOR_REVIEW = PROGRAM / "A13_exp_frontier_root_review_run001"
PRIOR_REVIEW_SHA = "744e04e887ef94a218004845a8655014389cc2f4cf5d4d41153c352d7db4ebce"
PRIOR_V2_SHA256 = {
    "experiment_exp_frontier_v2.py": (
        "2c3d0f17c0c6b3789071ef85c31c1f8e69957fe71768bde0877b134196a3575a"
    ),
    "audit_exp_frontier_v2.py": "df66aa45c223837e820a0cf720cd112db42aacdbf87817f58139b1ce57a404f5",
    "A13_EXP_FRONTIER_IMPLEMENTATION_PREFLIGHT_V2.md": (
        "b3e5d7443ed753ecbf577a305a61ef946a18689f00629be12bbd16f20716a038"
    ),
    "a13_exp_frontier_implementation_preflight_v2.json": (
        "de40e3d7ba0def85f4b7d1b1e7bd9d06005524517feb52eca5dcaff587f41c0f"
    ),
}
PRIOR_V2_REVIEW = PROGRAM / "A13_exp_frontier_root_review_run002"
PRIOR_V2_REVIEW_SHA = "6834a90acb76a5489f3fac66ce874adf81357692ba2bade7cd709455846626e3"
ORIGINAL_RECOVERY_AUTHOR_SHA256 = {
    "experiment_exp_frontier_recovery.py": (
        "9a83c9ed87df61415af94b1ee15840c97714f48c90bebcf2c1d0b1367d79b8d9"
    ),
    "audit_exp_frontier_recovery.py": (
        "e10184be6b451dff12f01e74aa67786c116a089ac814e42df542e63d0449e6ed"
    ),
    "A13_EXP_FRONTIER_RECOVERY_PREFLIGHT.md": (
        "2d86febd3e35963e051113da6490b5e8ed352b7be10c79e6d8187cdf8950b747"
    ),
    "a13_exp_frontier_recovery_preflight.json": (
        "c36d9c97266144a73373c1dd55922585a2271206d0a5cc1ddf0f42ddaa9ce291"
    ),
    "A13_EXP_FRONTIER_RECOVERY_IMPLEMENTATION_PREFLIGHT.md": (
        "b44deaeca4d2a39fdb88e484bc85c3575d45aea8a805aaf953b049bb3bddc2a3"
    ),
    "a13_exp_frontier_recovery_implementation_preflight.json": (
        "926b787958e8a482fb707d209b6f4284ecc389b2fabfd648a3e37873e3871986"
    ),
}
PRIOR_RECOVERY_AUDIT = PROGRAM / "A13_recovery_audit_run001"
PRIOR_RECOVERY_AUDIT_SHA = "2770a360c67ba6ee5c1df720679a6376679f5efcaba91052683af698cfb66c72"
PRIOR_RECOVERY_REVIEW = PROGRAM / "A13_recovery_root_review_run001"
PRIOR_RECOVERY_REVIEW_SHA = "2aac4a58ed85fc672a9a83fb9cae555534287a3998edf42ea28a57cf66cd77b6"
ORIGINAL_RECOVERY_SOURCE_SHA = "e3c23aaa0697727952a7c979503424146c0224e8b2c8c32cff652974ab557dc9"
PRIOR_RECOVERY_AUDIT_V2_AUTHOR_SHA256 = {
    "audit_exp_frontier_recovery_v2.py": (
        "411930cf13eaf4a61b7f5d9e3e34870644fa2960a7d8d18afef90e26672a31af"
    ),
    "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V2.md": (
        "8731ab0d15e12a590aa0c9ebdabf7bb696ceb780630d281ebea2f86b0a2fec44"
    ),
    "a13_exp_frontier_recovery_audit_implementation_preflight_v2.json": (
        "a559e03871cc5295401843fc011bca581fc6bd4e9e23aa23785032eef6cc5aea"
    ),
}
PRIOR_RECOVERY_AUDIT_V2 = PROGRAM / "A13_recovery_audit_run002"
PRIOR_RECOVERY_AUDIT_V2_SHA = "ba3b0715f9ee994c157e7422e12919b808916105f6ab1a1b8350017b7ceb9dcd"
PRIOR_RECOVERY_V2_REVIEW = PROGRAM / "A13_recovery_root_review_run002"
PRIOR_RECOVERY_V2_REVIEW_SHA = "47a49e01e1395d21a3d08873ebfee9b17906bd0f48184c89e0614f5b075fefb2"
PRIOR_RECOVERY_AUDIT_V3_AUTHOR_SHA256 = {
    "audit_exp_frontier_recovery_v3.py": (
        "f094a5bd4738735bfae4775b6149fc354a9a15bad7e28850811aa1f0f27d7a3c"
    ),
    "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V3.md": (
        "66df965afd04126ebdd3bf742676fbe12c5944626bd03201cc9e0a92e29e10ff"
    ),
    "a13_exp_frontier_recovery_audit_implementation_preflight_v3.json": (
        "479cd7b015ba530abcd1b73099cfdca1e9ebed976c316a8ebe6943dc9da99cd1"
    ),
}
PRIOR_RECOVERY_AUDIT_V3 = PROGRAM / "A13_recovery_audit_run003"
PRIOR_RECOVERY_AUDIT_V3_SHA = "753ffde46904f2b4995efbdcb42b89161386e9267108179f9b0cc9dfe9a14551"
PRIOR_RECOVERY_V3_REVIEW = PROGRAM / "A13_recovery_root_review_run003"
PRIOR_RECOVERY_V3_REVIEW_SHA = "0108b046dcf9ebf55a85926d68f8e7d02036e039f9966d654e1773df61de96a6"
DP_METHOD = RESEARCH / "a13_exp_frontier_recovery_dp_optimization_preflight_v4.json"
DP_METHOD_DOC = RESEARCH / "A13_EXP_FRONTIER_RECOVERY_DP_OPTIMIZATION_PREFLIGHT_V4.md"
PRIOR_RECOVERY_AUDIT_V4_AUTHOR_SHA256 = {
    "audit_exp_frontier_recovery_v4.py": (
        "61c05812abd7c7c042ab654a025e14b96afcfff00afd5398e72ea334307d07ba"
    ),
    "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V4.md": (
        "75b962da0239f371f34bc4c675243fba29b504038a68975a6b347fa0596af3f5"
    ),
    "a13_exp_frontier_recovery_audit_implementation_preflight_v4.json": (
        "8b1bf237dd2739fdbfe59c5af4cd2bf776dc29ce198d02dcf8c900bedae1e1ea"
    ),
}
PRIOR_RECOVERY_AUDIT_V4 = PROGRAM / "A13_recovery_audit_run004"
PRIOR_RECOVERY_AUDIT_V4_SHA = "334aa0386e0321b7fb9690a52378a8c94234b5c0488fa50464d89d076ca20471"
PRIOR_RECOVERY_V4_REVIEW = PROGRAM / "A13_recovery_root_review_run004"
PRIOR_RECOVERY_V4_REVIEW_SHA = "c427b46bf39133fddbccc2d9022d14d8756545885f7a4279e788a3fbc04dec1a"
BERNSTEIN_KERNEL = RESEARCH / "bernstein_integer_kernel_v5.py"
BERNSTEIN_AUTHOR_SHA256 = {
    "bernstein_integer_kernel_v5.py": (
        "695c10c095c17a0827d5e180195021828b1613e77cb22f6ead42783b7fa70048"
    ),
    "verify_a13_bernstein_equivalence_v5.py": (
        "005b266056e791f06001f073858028096ff49f415f89cdc2f79b7de62ecca3ad"
    ),
    "A13_BERNSTEIN_EQUIVALENCE_PREFLIGHT_V5.md": (
        "e7ff698ea67c3ea28776c7da92078871426e3faa2ad6de210d272792ad1cd4a3"
    ),
    "a13_bernstein_equivalence_preflight_v5.json": (
        "165426876e38662577fb1e1f1f816f664188245b46ec85bdf8c508e958c5880b"
    ),
}
BERNSTEIN_QA = PROGRAM / "A13_Bernstein_equivalence_check_run001"
BERNSTEIN_QA_SHA = "574876915ac0418ab80d44f7763d98f4051b56a40f54d9e29717a8fff131401e"
BERNSTEIN_QA_READY = ROOT / ".context/A13_Bernstein_equivalence_ROOT_READY_run001.json"
BERNSTEIN_QA_READY_SHA = "a58efdc98f3a4c9c41b708c1afa009636fc335ca5f49f5b57d88b5a0afdaa4fd"
PRIOR_PROFILE = PROGRAM / "A13_recovery_profile_d10_s4_run001"
PRIOR_PROFILE_SHA = "e099b1547056d12eb81e920bcaaf71bb1a33bc2bc5223643cd60cb8881190983"
INTEGER_BERNSTEIN = None

V6_READY = ROOT / ".context/A13_RECOVERY_AUDIT_V6_ROOT_READY_run001.json"
V5_FAILED = PROGRAM / "A13_recovery_audit_run005"
V5_FAILED_PROTOCOL_SHA = "bc7dc2f880c31fdbc40543923d3b3d7e1faca27a154af9d8c03d6d72f8169bcb"
V5_FAILURE_CAPTURE = PROGRAM / "A13_recovery_audit_terminal_failure_capture_run005"
V5_FAILURE_CAPTURE_SHA = "e6eef6653d70e0b5d61ea52162617cf551088c165b1ac1f1e2eb8d21f1c51a6b"
V5_STATIC_REVIEW = PROGRAM / "A13_recovery_root_review_run005"
V5_STATIC_REVIEW_SHA = "0f39476d4e25793f7ee029d4df979d329e77a589623055e2bb307be890c2a9e4"
V2_METADATA_PROFILE = PROGRAM / "A13_metadata_validation_profile_run002"
V2_METADATA_PROFILE_SHA = "288909d936a2a1e15098abbfb47cf96027b940d5050bbbf1bd5cc85b8abe275d"
V2_METADATA_READY = ROOT / ".context/A13_METADATA_PROFILE_ROOT_READY_run002.json"
V2_METADATA_READY_SHA = "641a2a6b3abcbe24c5c3374a35cc3fd973b773a4a4313a5e4d3bc2940c83d168"
V5_AUTHOR_SHA256 = {
    "audit_exp_frontier_recovery_v5.py": (
        "c34f7096f783a61caa586c4e3f30067304da3d457626b367fd609ffebc2b2593"
    ),
    "A13_EXP_FRONTIER_RECOVERY_AUDIT_IMPLEMENTATION_PREFLIGHT_V5.md": (
        "06ddca7b99dba0d44c5dcc7de7f27d5c26ea82691cf8bdccfe91a2d969ceae18"
    ),
    "a13_exp_frontier_recovery_audit_implementation_preflight_v5.json": (
        "c8d592ab4e6beb52b59bc4c3275ab9a33e7e898c94ef56a8a733be821f6d6693"
    ),
}
V2_METADATA_AUTHOR_SHA256 = {
    "profile_a13_metadata_validation_v2.py": (
        "f033e7e551bad139e56fa9c350c3ce17f7a34bda85e156f4c091e1c366e51402"
    ),
    "A13_METADATA_VALIDATION_PROFILE_PREFLIGHT_V2.md": (
        "f07512a9714e611fdac659b4c3d83be4d6aa98daa92d4fabc1e0def9a43565b2"
    ),
    "a13_metadata_validation_profile_preflight_v2.json": (
        "8e612119a7af4eff12107b4d4a44b26891180b8406d4f59f901ada354cc74b84"
    ),
}
V6_METADATA_EXPECTED = {
    V5_FAILURE_CAPTURE.relative_to(ROOT).as_posix(): V5_FAILURE_CAPTURE_SHA,
    V5_STATIC_REVIEW.relative_to(ROOT).as_posix(): V5_STATIC_REVIEW_SHA,
    V2_METADATA_PROFILE.relative_to(ROOT).as_posix(): V2_METADATA_PROFILE_SHA,
}
_V6_PRIOR_INVENTORIES, _V6_ABSENT_CODE_CACHES = {}, set()


MAX_REFERENCES = 100000
_LEXICAL_PARTS_CACHE = {}


def lexical_parts(path):
    """Immutable Windows syntax only; never a physical-resolution cache."""
    require(isinstance(path, (Path, PureWindowsPath)), "Only Windows path objects")
    key = str(path)
    if key not in _LEXICAL_PARTS_CACHE:
        require(len(_LEXICAL_PARTS_CACHE) < MAX_REFERENCES, "Bounded lexical syntax cache")
        _LEXICAL_PARTS_CACHE[key] = (
            path.anchor.lower(),
            tuple(part.lower() for part in path.parts),
        )
    return _LEXICAL_PARTS_CACHE[key]


def lexically_under(path, parent):
    """Exact Path.is_relative_to syntax predicate; aliases still resolve separately."""
    if (path.drive and not path.root) or (parent.drive and not parent.root):
        return path.is_relative_to(parent)
    anchor, parts = lexical_parts(path)
    root_anchor, root_parts = lexical_parts(parent)
    return (
        anchor == root_anchor
        and len(parts) >= len(root_parts)
        and parts[: len(root_parts)] == root_parts
    )


class BudgetCensoredError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(started, *, admission=False):
    cpu, wall = time.process_time(), time.monotonic() - started
    if cpu >= (ADMISSION if admission else CPU) or wall >= WALL:
        raise BudgetCensoredError("Fixed independent A13 CPU/wall censor")
    return cpu, wall


def start_clock():
    require(os.name == "nt" and ctypes.sizeof(ctypes.c_void_p) == 8, "Pinned Win64 runtime")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.argtypes = []
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    kernel.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    kernel.GetProcessTimes.restype = wintypes.BOOL
    fields = [wintypes.FILETIME() for _ in range(4)]
    require(
        kernel.GetProcessTimes(kernel.GetCurrentProcess(), *(ctypes.byref(v) for v in fields)),
        "Actual creation time unavailable",
    )
    ticks = (fields[0].dwHighDateTime << 32) | fields[0].dwLowDateTime
    age_ns = time.time_ns() - (ticks - 116444736000000000) * 100
    require(age_ns >= 0, "Actual creation precedes clock observation")
    return time.monotonic() - age_ns / 1000000000


def encode(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def rational(value):
    require(
        type(value) is list
        and len(value) == 2
        and all(type(v) is int for v in value)
        and value[1] > 0,
        "Typed canonical exact rational",
    )
    result = Fraction(*value)
    require(encode(result) == value, "Reduced rational representation")
    return result


def same(left, right, message):
    require(
        json.dumps(left, sort_keys=True, separators=(",", ":"), allow_nan=False)
        == json.dumps(right, sort_keys=True, separators=(",", ":"), allow_nan=False),
        message,
    )


def unsigned_word(value):
    require(type(value) is int and 0 <= value < 1 << W, "Canonical unsigned72 CONST word")
    return value - (1 << W) if value >= 1 << (W - 1) else value


def signed_coefficient(value):
    require(type(value) is int and -(1 << 71) <= value < 1 << 71, "Canonical signed72 coefficient")
    return value


def nearest_fraction(value):
    value = Fraction(value)
    low, remainder = divmod(value.numerator, value.denominator)
    twice = 2 * remainder
    return low + int(twice > value.denominator or (twice == value.denominator and low % 2))


class GraphAudit:
    """Own backward traversal on actual SSA; never constructs or evaluates it."""

    def __init__(self, target, started):
        self.target, self.started, self.nodes, self.ancestor_cache = target, started, {}, {}
        require((target["width"], target["fraction_bits"]) == (72, 40), "Native W72/F40")
        arities = {
            "input": 0,
            "const": 0,
            "add": 2,
            "sub": 2,
            "mul": 2,
            "cmul": 1,
            "lt": 2,
            "select": 3,
            "positive": 1,
            "msb": 1,
            "bits": 1,
            "shift": 2,
            "sqrt": 1,
            "lookup": 1,
        }
        next_value = 0
        for row in target["nodes"]:
            check(started)
            op, args, out, params = (row[k] for k in ("op", "args", "out", "params"))
            require(
                op in arities and type(args) is list and len(args) == arities[op], "Typed arity"
            )
            require(type(out) is list and type(params) is dict and out, "Typed node shape")
            require(all(type(v) is int and v in self.nodes for v in args), "Topological dependency")
            require(
                out == list(range(next_value, next_value + len(out))),
                "Exact contiguous output slots",
            )
            require(all(type(v) is int for v in out), "Typed SSA identities")
            next_value += len(out)
            require(op == "lookup" or len(out) == 1, "Single output native primitive")
            if op == "const":
                require(set(params) == {"value"}, "Exact constant fields")
                unsigned_word(params["value"])
            elif op == "cmul":
                require(set(params) == {"c"}, "Exact coefficient fields")
                signed_coefficient(params["c"])
            elif op == "bits":
                require(
                    set(params) == {"shift", "width", "signed"}
                    and type(params["shift"]) is int
                    and type(params["width"]) is int
                    and 1 <= params["width"] <= 72
                    and type(params["signed"]) is bool,
                    "Exact bit-extraction fields",
                )
            elif op == "lookup":
                require(
                    set(params) == {"table", "bits"} and type(params["bits"]) is int,
                    "Exact lookup fields",
                )
                table = target["tables"][params["table"]]
                require(
                    len(table) == 1 << params["bits"]
                    and all(len(entry) == len(out) for entry in table),
                    "Complete table shape",
                )
                for entry in table:
                    for coefficient in entry:
                        signed_coefficient(coefficient)
            elif op == "input":
                require(set(params) == {"name", "bits", "preparation"}, "Exact input fields")
            else:
                require(params == {}, "No undeclared arithmetic parameters")
            for value in out:
                self.nodes[value] = row

    def node(self, value, kind=None, params=None):
        check(self.started)
        require(type(value) is int and value in self.nodes, "Actual SSA identity")
        row = self.nodes[value]
        require(kind is None or row["op"] == kind, "Expected native operation")
        if params is not None:
            same(row["params"], params, "Exact native operation parameters")
        return row

    def constant(self, value, expected=None):
        result = unsigned_word(self.node(value, "const")["params"]["value"])
        require(expected is None or result == expected, "Actual decoded constant")
        return result

    def ancestors(self, value):
        if value not in self.ancestor_cache:
            pending, values = [value], set()
            while pending:
                check(self.started)
                current = pending.pop()
                if current not in values:
                    values.add(current)
                    pending.extend(self.node(current)["args"])
            self.ancestor_cache[value] = values
        return self.ancestor_cache[value]

    def clamp(self, value, low=None, high=None):
        topflag, middle, upper = self.node(value, "select")["args"]
        require(self.node(topflag, "lt")["args"] == [middle, upper], "Exact upper clamp")
        bottomflag, lower, original = self.node(middle, "select")["args"]
        require(self.node(bottomflag, "lt")["args"] == [original, lower], "Exact lower clamp")
        require(self.constant(lower, low) < self.constant(upper, high), "Ordered clamp literals")
        return original

    def midpoint(self, value, input_value):
        args = self.node(value, "add")["args"]
        shifted = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifted) == 1, "One midpoint conversion")
        require(
            self.node(shifted[0], "bits", {"shift": -8, "width": 72, "signed": False})["args"]
            == [input_value],
            "Exact q32 to f40 conversion",
        )
        self.constant(next(v for v in args if v != shifted[0]), 128)

    def interpolation(self, result, table_name, input_value):
        bins, degree, lower, bits = (32, 8, Q, 5) if table_name == "log" else (64, 7, 0, 6)
        candidates = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(result)
            if self.node(v)["op"] == "lookup" and self.node(v)["params"]["table"] == table_name
        }
        require(len(candidates) == 1, "One table supplies every Horner coefficient")
        coefficients = next(iter(candidates))
        require(len(coefficients) == degree + 1, "All actual polynomial coefficients")
        address = self.node(coefficients[0], "lookup", {"table": table_name, "bits": bits})["args"][
            0
        ]
        bounded = self.node(address, "bits", {"shift": 40 - bits, "width": bits, "signed": False})[
            "args"
        ][0]
        if lower:
            bounded, literal = self.node(bounded, "sub")["args"]
            self.constant(literal, lower)
        require(
            self.clamp(bounded, lower, lower + Q - 1) == input_value, "Interpolation input binding"
        )
        current, local = result, None
        for coefficient in coefficients[:-1]:
            args = self.node(current, "add")["args"]
            require(coefficient in args, "Horner coefficient order")
            factors = self.node(next(v for v in args if v != coefficient), "mul")["args"]
            if local is None:
                possible = [v for v in factors if self.node(v)["op"] == "sub"]
                require(len(possible) == 1, "One local variable in Horner")
                local = possible[0]
            require(local in factors, "Every Horner product uses same local variable")
            current = next(v for v in factors if v != local)
        require(current == coefficients[-1], "Horner terminal coefficient")
        actual, center = self.node(local, "sub")["args"]
        require(actual == bounded, "Local variable uses bounded argument")
        args = self.node(center, "add")["args"]
        shifted = [v for v in args if self.node(v)["op"] == "bits"]
        require(len(shifted) == 1, "Exact local center shift")
        require(
            self.node(shifted[0], "bits", {"shift": bits - 40, "width": 72, "signed": False})[
                "args"
            ]
            == [address],
            "Local center derives from same address",
        )
        self.constant(next(v for v in args if v != shifted[0]), lower + Q // (2 * bins))
        return dict(
            output=result,
            input=input_value,
            address=address,
            local=local,
            lookup_outputs=list(coefficients),
            floors=degree,
        )

    def joint_pair(self, first, second, input_u, input_v, ln2):
        products = [self.node(v, "mul")["args"] for v in (first, second)]
        shared = set(products[0]) & set(products[1])
        require(len(shared) == 1, "Actual pair shares one radius")
        radius = next(iter(shared))
        positive = self.node(radius, "sqrt")["args"][0]
        product = self.node(positive, "positive")["args"][0]
        logarithm = self.node(product, "cmul", {"c": -2 * Q})["args"][0]
        addends = self.node(logarithm, "add")["args"]
        exponent_terms = [v for v in addends if self.node(v)["op"] == "cmul"]
        require(len(exponent_terms) == 1, "Unique integer exponent literal product")
        term = exponent_terms[0]
        scaled = self.node(term, "cmul", {"c": ln2})["args"][0]
        exponent = self.node(scaled, "bits", {"shift": -40, "width": 72, "signed": False})["args"][
            0
        ]
        top, f = self.node(exponent, "sub")["args"]
        self.constant(f, 40)
        safe = self.node(top, "msb")["args"][0]
        flag, tiny, midpoint_u = self.node(safe, "select")["args"]
        self.constant(tiny, 1)
        require(self.node(flag, "lt")["args"] == [midpoint_u, tiny], "Actual positive-input guard")
        self.midpoint(midpoint_u, input_u)
        polynomial = next(v for v in addends if v != term)
        lookups = {
            tuple(self.node(v)["out"])
            for v in self.ancestors(polynomial)
            if self.node(v)["op"] == "lookup"
        }
        require(len(lookups) == 1, "Unique original log lookup")
        address = self.node(next(iter(lookups))[0])["args"][0]
        shifted = self.node(address)["args"][0]
        bounded = self.node(shifted, "sub")["args"][0]
        mantissa = self.clamp(bounded, Q, 2 * Q - 1)
        u, negated = self.node(mantissa, "shift")["args"]
        require(u == safe, "Same positive midpoint is normalized")
        zero, same_exponent = self.node(negated, "sub")["args"]
        self.constant(zero, 0)
        require(same_exponent == exponent, "Exact normalization exponent")
        log_scope = self.interpolation(polynomial, "log", mantissa)
        cosines = [next(v for v in args if v != radius) for args in products]
        turns = []
        for cosine in cosines:
            lookups = {
                tuple(self.node(v)["out"])
                for v in self.ancestors(cosine)
                if self.node(v)["op"] == "lookup"
            }
            require(len(lookups) == 1, "Unique original cosine lookup")
            address = self.node(next(iter(lookups))[0])["args"][0]
            bounded = self.node(address)["args"][0]
            turns.append(self.clamp(bounded, 0, Q - 1))
        midpoint_v, wrapped = turns
        self.midpoint(midpoint_v, input_v)
        total = self.node(wrapped, "bits", {"shift": 0, "width": 40, "signed": False})["args"][0]
        args = self.node(total, "add")["args"]
        require(midpoint_v in args, "Both angles derive from same midpoint")
        self.constant(next(v for v in args if v != midpoint_v), 3 * Q // 4)
        scopes = [self.interpolation(v, "cos", a) for v, a in zip(cosines, turns, strict=True)]
        dependencies = {
            v
            for root in (first, second)
            for v in self.ancestors(root)
            if self.node(v)["op"] == "input"
        }
        require(dependencies == {input_u, input_v}, "Exactly two independent pair input words")
        return dict(
            normal_values=[first, second],
            raw_uniform_values=[input_u, input_v],
            radius=radius,
            log=log_scope,
            cosines=scopes,
            original_shared_pair_preserved=True,
        )

    def sum_terms(self, value, stops):
        pending, result = [value], Counter()
        while pending:
            check(self.started)
            current = pending.pop()
            if current in stops:
                result[current] += 1
            else:
                pending.extend(self.node(current, "add")["args"])
        return result


def initialize(started):
    """Independent admission of the actual local interpreter; stdlib only."""
    global BASE_PREFIX, BASE_TREES, BASE_FILES, BASE_SITE_LEXICAL, BASE_SITE
    PATH_CACHE.clear()
    ACTUAL_HASH_CACHE.clear()
    OBSERVED_HASHES.clear()
    require(sys.dont_write_bytecode is True, "Interpreter startup -B is mandatory")
    require(
        Path.cwd().resolve() == ROOT and Path(__file__).resolve() == AUTHOR,
        "Exact auditor module and working directory",
    )
    require(Path(sys.executable).resolve() == LAUNCHER, "Pinned isolated launcher")
    require(
        Path(sys.prefix).resolve() == ROOT / ".context/frontier_t0_env",
        "Exact isolated interpreter prefix",
    )
    require(site.ENABLE_USER_SITE is False, "User site must be disabled")
    for name in ("PYTHONPATH", "PYTHONHOME", "SAGE_ROOT", "MPMATH_SAGE"):
        require(not os.environ.get(name), "Unexpected runtime override: " + name)
    os.environ["MPMATH_NOGMPY"] = os.environ["MPMATH_NOSAGE"] = "1"
    BASE_PREFIX = Path(sys.base_prefix).resolve(strict=True)
    BASE_SITE_LEXICAL = BASE_PREFIX / "Lib/site-packages"
    BASE_SITE = BASE_SITE_LEXICAL.resolve()
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve(strict=True)
    require(base.parent == BASE_PREFIX, "Actual adjacent base interpreter")
    BASE_TREES = tuple(
        (BASE_PREFIX / name).resolve(strict=True)
        for name in ("Lib", "DLLs")
        if (BASE_PREFIX / name).is_dir()
    )
    BASE_FILES = tuple(
        path.resolve(strict=True) for path in BASE_PREFIX.iterdir() if path.is_file()
    )
    require(base in BASE_FILES, "Actual base executable is captured")
    forbidden_imports()
    check(started)


def forbidden_imports():
    banned = ("numpy", "scipy", "numba", "llvmlite", "qiskit", "gmpy", "gmpy2", "sage")
    for name in sys.modules:
        require(
            not any(name == prefix or name.startswith(prefix + ".") for prefix in banned),
            "Forbidden numerical or SDK import: " + name,
        )
        if name.startswith("research."):
            require(
                name
                in (
                    "research.limitation_program_20261001",
                    "research.limitation_program_20261001.audit_exp_frontier_recovery_v6",
                ),
                "Auditor must not import producer or other research helpers",
            )


def permitted(path):
    if BASE_SITE is not None and lexically_under(path, BASE_SITE):
        return False
    return (
        lexically_under(path, ROOT)
        or path == BASE_PREFIX
        or path in BASE_FILES
        or any(lexically_under(path, root) for root in BASE_TREES)
    )


def canonical_path(path, started, *, fresh=False):
    check(started)
    value = Path(path)
    require(not value.drive or value.is_absolute(), "Ambiguous drive-relative path forbidden")
    require(
        BASE_SITE_LEXICAL is None or not lexically_under(value.absolute(), BASE_SITE_LEXICAL),
        "Unreachable base site-packages lexical paths forbidden",
    )
    lexical = str(value.absolute())
    if not fresh and lexical in PATH_CACHE:
        check(started)
        return PATH_CACHE[lexical]
    actual = value.resolve(strict=True)
    require(permitted(actual), "Outside ROOT or exact observed base-runtime scopes")
    require(
        lexical not in PATH_CACHE or PATH_CACHE[lexical] == actual,
        "Previously confined lexical path redirected",
    )
    PATH_CACHE[lexical] = actual
    PATH_CACHE.setdefault(str(actual), actual)
    check(started)
    return actual


def fingerprint(path):
    data = path.stat()
    return (
        data.st_dev,
        data.st_ino,
        data.st_size,
        data.st_mtime_ns,
        data.st_ctime_ns,
        getattr(data, "st_file_attributes", None),
        getattr(data, "st_reparse_tag", None),
    )


def actual_digest(path, started, *, fresh=False):
    check(started)
    require(permitted(path), "Pre-read confinement of actual hash path")
    identity, key = fingerprint(path), str(path)
    require(path.is_file(), "Actual regular byte input")
    if not fresh and key in ACTUAL_HASH_CACHE and ACTUAL_HASH_CACHE[key][0] == identity:
        check(started)
        return ACTUAL_HASH_CACHE[key][1]
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            check(started)
            state.update(block)
            check(started)
    require(fingerprint(path) == identity, "Actual bytes changed during SHA observation")
    result = state.hexdigest()
    require(
        key not in OBSERVED_HASHES or OBSERVED_HASHES[key] == result,
        "First independently observed actual SHA changed",
    )
    OBSERVED_HASHES.setdefault(key, result)
    ACTUAL_HASH_CACHE[key] = (identity, result)
    check(started)
    return result


def sha(path, started, *, fresh=False):
    return actual_digest(canonical_path(path, started, fresh=fresh), started, fresh=fresh)


def root_key(path, started):
    actual = canonical_path(path, started)
    require(lexically_under(actual, ROOT), "ROOT-relative field confinement")
    return actual.relative_to(ROOT).as_posix()


def bind(frozen, external, path, expected, started):
    check(started)
    require(type(expected) is str and SHA_PATTERN.fullmatch(expected), "Canonical SHA256")
    actual = canonical_path(path, started)
    mapping = frozen if lexically_under(actual, ROOT) else external
    key = actual.relative_to(ROOT).as_posix() if lexically_under(actual, ROOT) else str(actual)
    require(key not in mapping or mapping[key] == expected, "Conflicting expected SHA binding")
    require(actual_digest(actual, started) == expected, "Actual byte SHA differs: " + key)
    mapping[key] = expected
    check(started)
    return actual


def read_bytes(path, started):
    actual = canonical_path(path, started)
    identity = fingerprint(actual)
    require(
        actual.is_file() and identity[2] <= 128 * 1024**2, "Bounded regular source/artifact input"
    )
    chunks, state, total = [], hashlib.sha256(), 0
    with actual.open("rb") as stream:
        while block := stream.read(1 << 20):
            check(started)
            total += len(block)
            require(total <= identity[2], "Text input grew while reading")
            state.update(block)
            check(started)
            chunks.append(block)
    require(
        total == identity[2] and fingerprint(actual) == identity,
        "Exact text bytes stable during read",
    )
    data = b"".join(chunks)
    observed = state.hexdigest()
    check(started)
    key = str(actual)
    require(
        key not in OBSERVED_HASHES or OBSERVED_HASHES[key] == observed,
        "JSON/source read contradicts original actual SHA",
    )
    OBSERVED_HASHES.setdefault(key, observed)
    ACTUAL_HASH_CACHE[key] = (identity, observed)
    return data


def read_json(path, started):
    value = json.loads(read_bytes(path, started))
    check(started)
    return value


def write_json(path, value, started):
    check(started)
    data = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    check(started)
    require(len(data) <= 128 * 1024**2, "Bounded JSON output")
    with Path(path).open("xb") as stream:
        for offset in range(0, len(data), 1 << 20):
            check(started)
            stream.write(data[offset : offset + (1 << 20)])
            check(started)


def write_compressed_proof(path, value, started):
    """One canonical gzip JSON member; compression is charged bookkeeping."""
    check(started)
    state, uncompressed = hashlib.sha256(), 0
    encoder = json.JSONEncoder(sort_keys=True, separators=(",", ":"), allow_nan=False)
    with path.open("xb") as target:
        with gzip.GzipFile(
            filename="", mode="wb", compresslevel=1, fileobj=target, mtime=0
        ) as stream:
            pending = bytearray()
            for fragment in encoder.iterencode(value):
                check(started)
                encoded = fragment.encode("utf-8")
                check(started)
                pending.extend(encoded)
                check(started)
                while len(pending) >= 65536:
                    check(started)
                    block = bytes(pending[:65536])
                    del pending[:65536]
                    uncompressed += len(block)
                    require(
                        uncompressed <= 128 * 1024**2, "Finite uncompressed single proof artifact"
                    )
                    state.update(block)
                    check(started)
                    stream.write(block)
                    check(started)
            check(started)
            pending.extend(b"\n")
            block = bytes(pending)
            uncompressed += len(block)
            require(uncompressed <= 128 * 1024**2, "Finite uncompressed single proof artifact")
            state.update(block)
            check(started)
            stream.write(block)
            check(started)
        check(started)
    check(started)
    return dict(
        artifact_encoding="canonical-gzip-json-v1",
        compression_level=1,
        gzip_mtime=0,
        gzip_filename="",
        compact_sorted_JSON=True,
        uncompressed_bytes=uncompressed,
        uncompressed_JSON_SHA256=state.hexdigest(),
        compressed_bytes=path.stat().st_size,
        compressed_SHA256=sha(path, started),
    )


def verify_maps(frozen, external, started):
    for mapping, parent in ((frozen, ROOT), (external, None)):
        for key, expected in mapping.items():
            check(started)
            path = parent / key if parent is not None else Path(key)
            require(sha(path, started) == expected, "Immutable map byte mismatch: " + key)


def final_fresh(frozen, external, started):
    """Fresh confinement for all aliases and fresh full bytes for every actual path."""
    v6_terminal_metadata_inventory(started)
    for lexical, expected_path in tuple(PATH_CACHE.items()):
        check(started)
        require(
            canonical_path(lexical, started, fresh=True) == expected_path,
            "Final independent lexical alias mismatch",
        )
    expected = {}
    for mapping, parent in ((frozen, ROOT), (external, None)):
        for key, value in mapping.items():
            check(started)
            actual = canonical_path(parent / key if parent is not None else key, started)
            require(actual not in expected or expected[actual] == value, "Equal-SHA final merge")
            expected[actual] = value
    observed = {Path(key): value for key, value in OBSERVED_HASHES.items()}
    union = set(expected) | set(observed)
    for path in sorted(union):
        check(started)
        actual = canonical_path(path, started, fresh=True)
        value = actual_digest(actual, started, fresh=True)
        require(path not in expected or expected[path] == value, "Final expected SHA differs")
        require(path not in observed or observed[path] == value, "Final observed SHA differs")
    v6_terminal_metadata_inventory(started)
    return len(union)


def original_owner_entries(path, data, started):
    """Independently normalize exact historical map conventions, without LIVE waiver."""
    if "files" in data:
        require(
            data.get("manifest_self_hash_excluded") is True,
            "Original nested owner self-hash convention",
        )
        mappings = [(field, data.get(field, {})) for field in ("files", "frozen_inputs")]
    else:
        require(
            path == PROGRAM / "A10_coefficient_run001/manifest.json",
            "Only pinned historical A10 flat map is recognized",
        )
        mappings = [("flat_owned_files", data)]
    result = []
    for field, mapping in mappings:
        require(type(mapping) is dict, "Recognized original expected byte map")
        for literal, expected in mapping.items():
            check(started)
            require(
                type(literal) is str and type(expected) is str and SHA_PATTERN.fullmatch(expected),
                "Typed original map record",
            )
            normalized = literal.replace("\\", "/")
            route = (
                ROOT / normalized
                if normalized.startswith(
                    ("results/", "research/", "docs/", "manuscript/", ".context/")
                )
                else path.parent / normalized
            )
            # Membership is structural; no claim that every original current source remains LIVE.
            actual = route.resolve()
            require(lexically_under(actual, ROOT), "Original membership confined to ROOT")
            result.append((field, actual, literal, expected))
            check(started)
    return result


def independent_origins(pins, owners, frozen, external, started, *, selected):
    inventories = []
    for key, expected in owners.items():
        path = bind(frozen, external, ROOT / key, expected, started)
        inventories.append((key, original_owner_entries(path, read_json(path, started), started)))
    records = []
    for key, expected in pins.items():
        check(started)
        actual = bind(frozen, external, ROOT / key, expected, started)
        if selected and key.endswith("/manifest.json"):
            continue
        matches = []
        for owner, inventory in inventories:
            for field, candidate, original, value in inventory:
                check(started)
                if candidate == actual and value == expected:
                    matches.append(
                        dict(
                            owner_manifest=owner,
                            source_map=field,
                            original_key=original,
                            expected_sha256=value,
                        )
                    )
        require(matches, "Original equal-SHA owner membership required: " + key)
        row = dict(
            path=key, sha256=expected, original_memberships=matches, expected_hash_waived=False
        )
        if selected:
            row["archived_route"] = False
        records.append(row)
    return records


def reject_unreachable_origin(path, started):
    """Deny excluded lexical/physical origins even when their files disappeared."""
    check(started)
    candidate = Path(path)
    require(not candidate.drive or candidate.is_absolute(), "Ambiguous runtime origin drive")
    require(
        BASE_SITE_LEXICAL is None or not lexically_under(candidate.absolute(), BASE_SITE_LEXICAL),
        "Unreachable base site-packages lexical origin forbidden",
    )
    actual = candidate.resolve(strict=False)
    require(
        BASE_SITE is None or not lexically_under(actual, BASE_SITE),
        "Unreachable base site-packages physical origin forbidden",
    )
    check(started)


def runtime_candidates(root, started):
    """Prune the unreachable base site directory before traversing its entries."""
    root = canonical_path(root, started)
    if root.is_file():
        yield root
        return
    require(root.is_dir(), "Finite actual runtime directory")
    for current, directory_names, filenames in os.walk(root, topdown=True, followlinks=False):
        check(started)
        directory = canonical_path(current, started)
        require(
            directory == root or lexically_under(directory, root),
            "Runtime walk directory confinement",
        )
        retained = []
        for name in directory_names:
            check(started)
            candidate = directory / name
            if candidate.absolute() == BASE_SITE_LEXICAL:
                continue
            actual = canonical_path(candidate, started)
            require(lexically_under(actual, root), "Runtime directory alias escape")
            require(
                not candidate.is_symlink() and not candidate.is_junction(),
                "Untraversed runtime directory links forbidden",
            )
            retained.append(name)
        directory_names[:] = retained
        for name in filenames:
            check(started)
            candidate = directory / name
            if candidate.is_file():
                actual = canonical_path(candidate, started)
                require(lexically_under(actual, root), "Runtime file alias escape")
                yield actual


def bootstrap_runtime_paths(site_root, started):
    """Exact actual hook roots and preexisting loaded venv files, without package expansion."""
    paths = set()
    for candidate in site_root.iterdir():
        check(started)
        hook_name = candidate.name.split(".", 1)[0]
        customize_names = ("sitecustomize", "usercustomize")
        hook_file = candidate.is_file() and (
            candidate.suffix.lower() == ".pth"
            or hook_name in customize_names
            and candidate.suffix.lower() in (".py", ".pyc", ".pyd")
        )
        hook_package = candidate.is_dir() and candidate.name in customize_names
        if not (hook_file or hook_package):
            continue
        reject_unreachable_origin(candidate, started)
        require(lexically_under(candidate.absolute(), site_root), "Lexical isolated startup hook")
        actual = canonical_path(candidate, started)
        require(lexically_under(actual, site_root), "Physical isolated startup hook")
        require(actual.is_file() or actual.is_dir(), "Actual startup hook file or package")
        paths.add(actual)
        if candidate.suffix == ".py":
            cached = Path(cache_from_source(str(candidate)))
            reject_unreachable_origin(cached, started)
            if cached.is_file():
                require(
                    lexically_under(cached.absolute(), site_root),
                    "Lexical startup cache confinement",
                )
                cache_actual = canonical_path(cached, started)
                require(
                    lexically_under(cache_actual, site_root), "Physical startup cache confinement"
                )
                paths.add(cache_actual)
    for module in tuple(sys.modules.values()):
        check(started)
        if module is None:
            continue
        for origin in (getattr(module, "__file__", None), getattr(module, "__cached__", None)):
            if not origin:
                continue
            reject_unreachable_origin(origin, started)
            lexical = Path(origin).absolute()
            if Path(origin).is_file():
                actual = canonical_path(origin, started)
                if lexically_under(lexical, site_root):
                    require(
                        lexically_under(actual, site_root),
                        "Loaded venv bootstrap alias confinement",
                    )
                if lexically_under(actual, site_root) and not lexically_under(
                    actual, site_root / "mpmath"
                ):
                    paths.add(actual)
    return sorted(paths)


def venv_adjacent_runtime(prefix, started):
    """Exact admitted prefix entries; capture adjacent files, caches and real packages."""
    paths, membership = set(), []
    for candidate in sorted(prefix.iterdir()):
        check(started)
        actual = canonical_path(candidate, started)
        require(
            actual == candidate.absolute() and actual.parent == prefix,
            "Adjacent actual venv entry is direct and has no redirected alias",
        )
        if candidate.is_file():
            kind = "file"
            require(actual.parent == prefix, "Actual adjacent venv regular file")
            paths.add(actual)
        else:
            require(candidate.is_dir(), "Actual adjacent venv file or directory")
            kind = "directory"
            importable_package = any(
                (candidate / name).is_file() for name in ("__init__.py", "__init__.pyc")
            )
            if candidate.name == "__pycache__" or importable_package:
                require(candidate.name not in ("Lib", "Scripts"), "No ambiguous venv package root")
                paths.add(actual)
        membership.append([candidate.name, kind])
    return sorted(paths), sorted(membership)


def runtime_inventory(frozen, external, started):
    prefix = canonical_path(sys.prefix, started)
    config = prefix / "pyvenv.cfg"
    require(
        "include-system-site-packages = false" in read_bytes(config, started).decode().lower(),
        "Isolated actual venv config",
    )
    site_root = canonical_path(prefix / "Lib/site-packages", started)
    distribution = metadata.distribution("mpmath")
    require(
        distribution.version == "1.3.0" and distribution.files,
        "Fixed installed mpmath RECORD inventory",
    )
    metadata_roots = set()
    for member in distribution.files:
        check(started)
        path = canonical_path(distribution.locate_file(member), started)
        for parent in (path, *path.parents):
            if parent.name.endswith(".dist-info"):
                metadata_roots.add(parent)
                break
    require(len(metadata_roots) == 1, "Exactly one actual mpmath metadata root")
    metadata_root = metadata_roots.pop()
    require(metadata_root.parent == site_root, "Distribution metadata confined to pinned site")
    roots = [
        config,
        prefix / "Scripts",
        site_root / "mpmath",
        metadata_root,
        *BASE_TREES,
        *BASE_FILES,
    ]
    bootstrap_paths = bootstrap_runtime_paths(site_root, started)
    roots.extend(bootstrap_paths)
    adjacent_paths, adjacent_membership = venv_adjacent_runtime(prefix, started)
    roots.extend(adjacent_paths)
    for path in (ROOT / "research/__init__.py", RESEARCH / "__init__.py"):
        if path.is_file():
            roots.append(path)
    for path in (ROOT / "research/__init__.py", RESEARCH / "__init__.py", AUTHOR, PRODUCER_AUTHOR):
        cached = Path(cache_from_source(str(path)))
        if cached.is_file():
            roots.append(cached)
    paths, total = set(), 0
    actual_roots = []
    for route in roots:
        root = canonical_path(route, started)
        actual_roots.append(str(root))
        for candidate in runtime_candidates(root, started):
            check(started)
            if not candidate.is_file():
                continue
            path = canonical_path(candidate, started)
            require(path == root or lexically_under(path, root), "Actual runtime tree confinement")
            if path in paths:
                continue
            total += path.stat().st_size
            paths.add(path)
            require(
                len(paths) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
                "Fixed entire runtime inventory cap",
            )
            bind(frozen, external, path, sha(path, started), started)
    absent = []
    allowed_roots = {ROOT, prefix, site_root, BASE_PREFIX, *BASE_TREES}
    for entry in sys.path:
        check(started)
        path = Path(entry or ROOT)
        reject_unreachable_origin(path, started)
        if path.exists():
            require(
                canonical_path(path, started) in allowed_roots
                or canonical_path(path, started) in BASE_FILES,
                "Unexpected actual module search path",
            )
        else:
            actual = path.resolve()
            require(
                actual
                == BASE_PREFIX
                / ("python" + str(sys.version_info.major) + str(sys.version_info.minor) + ".zip"),
                "Only standard absent interpreter zip",
            )
            absent.append(str(actual))
    return dict(
        python_version=sys.version,
        executable=str(canonical_path(sys.executable, started)),
        base_executable=str(canonical_path(sys._base_executable, started)),
        base_prefix=str(BASE_PREFIX),
        venv_prefix=str(prefix),
        mpmath_version="1.3.0",
        backend="python",
        MPMATH_NOGMPY="1",
        MPMATH_NOSAGE="1",
        startup_bytecode_disabled=True,
        user_site_disabled=True,
        runtime_inventory=dict(
            roots=actual_roots,
            actual_file_paths=sorted(str(p) for p in paths),
            files=len(paths),
            bytes=total,
        ),
        sys_path=list(sys.path),
        external_runtime_trees=[str(p) for p in BASE_TREES],
        external_adjacent_files=[str(p) for p in BASE_FILES],
        absent_standard_runtime_paths=absent,
        excluded_base_site_packages=str(BASE_SITE),
        excluded_base_site_packages_lexical=str(BASE_SITE_LEXICAL),
        base_site_packages_import_rejected=True,
        bootstrap_hook_and_loaded_venv_paths=[str(path) for path in bootstrap_paths],
        standard_Lib_excludes_only_unreachable_base_site_packages=True,
        other_installed_venv_packages_not_blanket_admitted=True,
        exact_sys_prefix_search_path_admitted=True,
        venv_adjacent_runtime_paths=[str(path) for path in adjacent_paths],
        venv_root_directory_membership=adjacent_membership,
    )


def verify_runtime(record, frozen, external, started):
    check(started)
    require(
        record["python_version"] == sys.version
        and record["executable"] == str(canonical_path(sys.executable, started))
        and record["base_executable"] == str(canonical_path(sys._base_executable, started))
        and record["base_prefix"] == str(BASE_PREFIX)
        and record["venv_prefix"] == str(canonical_path(sys.prefix, started))
        and record["mpmath_version"] == metadata.version("mpmath") == "1.3.0",
        "Actual interpreter and dependency version provenance",
    )
    same(record["sys_path"], list(sys.path), "Exact interpreter search path snapshot")
    same(
        record["external_runtime_trees"],
        [str(p) for p in BASE_TREES],
        "Exact observed base tree scopes",
    )
    same(
        record["external_adjacent_files"],
        [str(p) for p in BASE_FILES],
        "Exact observed adjacent runtime files",
    )
    require(
        record["backend"] == "python"
        and record["startup_bytecode_disabled"] is True
        and record["user_site_disabled"] is True
        and sys.dont_write_bytecode is True
        and site.ENABLE_USER_SITE is False
        and os.environ.get("MPMATH_NOGMPY") == os.environ.get("MPMATH_NOSAGE") == "1",
        "Exact isolated pure Python import policy",
    )
    require(
        record["excluded_base_site_packages"] == str(BASE_SITE)
        and record["excluded_base_site_packages_lexical"] == str(BASE_SITE_LEXICAL)
        and record["base_site_packages_import_rejected"] is True,
        "Exact unreachable base site-packages exclusion and import rejection",
    )
    require(
        record["standard_Lib_excludes_only_unreachable_base_site_packages"] is True
        and record["other_installed_venv_packages_not_blanket_admitted"] is True,
        "Full remaining runtime and selected venv package policy",
    )
    site_root = canonical_path(Path(sys.prefix) / "Lib/site-packages", started)
    prefix = canonical_path(sys.prefix, started)
    require(
        record["exact_sys_prefix_search_path_admitted"] is True,
        "Only exact isolated venv-prefix search root additionally admitted",
    )
    adjacent_paths, adjacent_membership = venv_adjacent_runtime(prefix, started)
    same(
        [str(path) for path in adjacent_paths],
        record["venv_adjacent_runtime_paths"],
        "Exact adjacent venv runtime roots",
    )
    same(
        adjacent_membership,
        record["venv_root_directory_membership"],
        "Exact finite venv-root directory membership",
    )
    same(
        [str(path) for path in bootstrap_runtime_paths(site_root, started)],
        record["bootstrap_hook_and_loaded_venv_paths"],
        "Actual complete startup hook membership",
    )
    allowed_sys_roots = {ROOT, prefix, site_root, BASE_PREFIX, *BASE_TREES}
    for entry in sys.path:
        check(started)
        candidate = Path(entry or ROOT)
        reject_unreachable_origin(candidate, started)
        if candidate.exists():
            actual = canonical_path(candidate, started)
            require(
                actual in allowed_sys_roots or actual in BASE_FILES,
                "Unexpected current sys.path root",
            )
    paths = set()
    for route in record["runtime_inventory"]["roots"]:
        root = canonical_path(route, started)
        for candidate in runtime_candidates(root, started):
            check(started)
            if candidate.is_file():
                path = canonical_path(candidate, started)
                require(
                    path == root or lexically_under(path, root),
                    "Fresh runtime membership confinement",
                )
                paths.add(path)
    same(
        sorted(str(p) for p in paths),
        record["runtime_inventory"]["actual_file_paths"],
        "Complete existing source/cache/metadata/runtime file membership",
    )
    total = 0
    for path in paths:
        check(started)
        total += path.stat().st_size
        require(
            len(paths) <= MAX_RUNTIME_FILES and total <= MAX_RUNTIME_BYTES,
            "Actual complete runtime cap",
        )
        key = path.relative_to(ROOT).as_posix() if lexically_under(path, ROOT) else str(path)
        mapping = frozen if lexically_under(path, ROOT) else external
        require(
            key in mapping and sha(path, started) == mapping[key],
            "Entire runtime byte origin is frozen",
        )
    require(
        record["runtime_inventory"]["files"] == len(paths)
        and record["runtime_inventory"]["bytes"] == total,
        "Exact recorded runtime count and bytes",
    )
    for path in record["absent_standard_runtime_paths"]:
        check(started)
        require(not Path(path).exists(), "Recorded absent interpreter zip appeared")
    forbidden_imports()


def loaded_origins(frozen, external, started):
    forbidden_imports()
    result = []
    for name, module in tuple(sys.modules.items()):
        check(started)
        if module is None:
            continue
        for kind, origin in (
            ("source", getattr(module, "__file__", None)),
            ("cache", getattr(module, "__cached__", None)),
        ):
            if origin:
                reject_unreachable_origin(origin, started)
            if origin and Path(origin).is_file():
                path = canonical_path(origin, started)
                key = (
                    path.relative_to(ROOT).as_posix() if lexically_under(path, ROOT) else str(path)
                )
                mapping = frozen if lexically_under(path, ROOT) else external
                require(
                    key in mapping and sha(path, started) == mapping[key],
                    "Actual loaded module source/existing cache not frozen: " + name,
                )
                result.append(dict(module=name, kind=kind, path=key, sha256=mapping[key]))
    return result


def map_inputs(record, frozen, external, started):
    for field, is_external in (("frozen_inputs", False), ("external_runtime_inputs", True)):
        mapping = record[field]
        require(type(mapping) is dict, "Complete recognized source/protocol byte map")
        for key, expected in mapping.items():
            check(started)
            require(type(key) is str, "Typed input map path")
            route = Path(key) if is_external else ROOT / key
            require(
                route.is_absolute() if is_external else not Path(key).is_absolute(),
                "Exact external-absolute / ROOT-relative map convention",
            )
            actual = bind(frozen, external, route, expected, started)
            canonical = str(actual) if is_external else actual.relative_to(ROOT).as_posix()
            require(
                canonical == key and (not is_external or not lexically_under(actual, ROOT)),
                "Canonical source-map path; no aliases or ROOT path in external map",
            )


def elapsed(started):
    return dict(process_CPU_seconds=time.process_time(), wall_seconds=time.monotonic() - started)


def copy_exact(source, destination, frozen, external, started):
    source = canonical_path(source, started)
    expected, identity = sha(source, started), fingerprint(source)
    with source.open("rb") as incoming, Path(destination).open("xb") as outgoing:
        while block := incoming.read(1 << 20):
            check(started)
            outgoing.write(block)
            check(started)
    require(fingerprint(source) == identity, "Copy source remains immutable")
    bind(frozen, external, destination, expected, started)


def owned_artifacts(output, started):
    result, total = {}, 0
    for candidate in output.rglob("*"):
        check(started)
        if candidate.is_file():
            path = canonical_path(candidate, started)
            require(
                lexically_under(path, output) and path.name != "manifest.json",
                "Owned output confinement and no manifest reuse",
            )
            key = path.relative_to(output).as_posix()
            require(key not in result, "No aliased owned output")
            total += path.stat().st_size
            require(
                len(result) < 63 and total <= 128 * 1024**2,
                "Finite owned artifact caps reserving final manifest",
            )
            result[key] = sha(path, started)
    return result


def outward(mp, value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoints(value):
    result = [
        Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent
        for sign, mantissa, exponent, _ in value._mpi_
    ]
    require(len(result) == 2 and result[0] <= result[1], "Finite outward interval endpoints")
    return tuple(result)


def interval_record(value):
    return [encode(endpoint) for endpoint in endpoints(value)]


def enclosures_contain(declared, actual, message):
    lo, hi = [rational(value) for value in declared]
    first, last = [rational(value) for value in actual]
    require(lo <= first <= last <= hi, message)


def word_range(pair):
    require(
        len(pair) == 2
        and all(type(value) is int for value in pair)
        and -(1 << 71) <= pair[0] <= pair[1] < 1 << 71,
        "Stored signed72 no-wrap proof",
    )
    return tuple(pair)


def integer_product(first, second, *, square=False):
    values = [a * b for a in first for b in second]
    lower = 0 if square and first[0] <= 0 <= first[1] else min(values)
    result = (lower, max(values))
    require(-(1 << 143) <= result[0] <= result[1] < 1 << 143, "Whole signed144 product proof")
    return result


def typed_source_domain(started):
    """Walk original typed source; canonical signatures never reorder actual operations."""
    reports, common = {}, None
    for case, (assets, dates, pairs) in CASES.items():
        check(started, admission=True)
        receipt = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
        target, native = (
            read_json(receipt / "target.json", started),
            read_json(receipt / "source.json", started),
        )
        support = read_json(PROGRAM / "E03_support_run001" / (case + "_certificate.json"), started)
        audit = read_json(PROGRAM / "E03_support_audit_run002" / (case + "_audit.json"), started)
        graph = GraphAudit(target, started)
        require(
            native["word_width"] == W and native["fraction_bits"] == 40,
            "Unchanged full72 f40 native ABI",
        )
        inputs = [node for node in target["nodes"] if node["op"] == "input"]
        require(
            len(inputs) == 2 * pairs == dates * (assets + 1), "All original independent q32 words"
        )
        same(native["inputs"], inputs, "Exact original source input inventory")
        same(native["outputs"], target["outputs"], "Exact original financial outputs")
        noninputs = [node for node in target["nodes"] if node["op"] != "input"]
        require(
            len(noninputs) == len(native["forward_calls"]), "Every original native call retained"
        )
        for node, call in zip(noninputs, native["forward_calls"], strict=True):
            check(started)
            same(
                [node["args"], node["out"]],
                [call["args"], call["out"]],
                "Exact source call mapping",
            )
            require(
                call["argument_copy_cx"] == 2 * W * len(node["args"]),
                "All original full-word argument copies",
            )
        require(
            support["complete_builder_equality"] is True
            and support["all_original_uniform_word_patterns"] is True
            and audit["passed"] is True
            and audit["actual_stock_templates_checked"] == assets * dates
            and audit["finite_samples_used"] is False,
            "Original universal support and actual-source audit",
        )
        same(support["target_output"], target["outputs"], "Original support source identity")
        stocks, templates = support["stock_ids"], []
        require(
            len(stocks) == assets * dates and len(set(stocks)) == len(stocks),
            "Every distinct original stock site",
        )
        for stock in stocks:
            check(started)
            polynomial, exponent = graph.node(stock, "shift")["args"]
            scaled = graph.node(exponent, "bits", {"shift": 40, "width": 72, "signed": True})[
                "args"
            ][0]
            reducer = graph.node(scaled, "cmul")
            clipped, inverse = reducer["args"][0], signed_coefficient(reducer["params"]["c"])
            raw_log = graph.clamp(clipped)
            upper = graph.node(clipped, "select")
            lower_id = graph.node(upper["args"][1], "select")["args"][1]
            lo, hi = graph.constant(lower_id), graph.constant(upper["args"][2])
            require(
                lo < hi and inverse > 0, "Actual signed clamp and positive reduction coefficient"
            )
            closure, pending = set(), [stock]
            while pending:
                check(started)
                value = pending.pop()
                if value == clipped or value in closure:
                    continue
                node = graph.node(value)
                require(
                    node["op"] in ("const", "add", "sub", "mul", "cmul", "bits", "shift")
                    and len(node["out"]) == 1,
                    "Original stock-only arithmetic template",
                )
                closure.add(value)
                pending.extend(node["args"])
            reductions = [
                value
                for value in closure
                if graph.node(value)["op"] == "sub" and graph.node(value)["args"][0] == clipped
            ]
            require(len(reductions) == 1, "One exact stock reduction remainder")
            remainder = reductions[0]
            logarithm = graph.node(graph.node(remainder)["args"][1], "cmul")
            ln2 = signed_coefficient(logarithm["params"]["c"])
            same(
                graph.node(logarithm["args"][0], "bits")["params"],
                {"shift": -40, "width": 72, "signed": False},
                "Exact full72 exponent scaling",
            )
            require(
                graph.node(logarithm["args"][0])["args"] == [exponent] and ln2 > 0,
                "Same native floor exponent used for shift and remainder",
            )
            signatures = {clipped: ["clipped-native-word"]}
            for value in sorted(closure):
                check(started)
                node = graph.node(value)
                children = [signatures[arg] for arg in node["args"]]
                if node["op"] in ("add", "mul"):
                    children.sort(key=lambda child: json.dumps(child, sort_keys=True))
                signatures[value] = [node["op"], node["params"], children]
            signature = hashlib.sha256(
                json.dumps(signatures[stock], sort_keys=True).encode()
            ).hexdigest()
            require(
                signature == audit["actual_stock_template_signature"],
                "Exact E03 canonical original stock identity",
            )
            require(
                [lo, hi] == support["clipped_log_integer_bounds"]
                and inverse == support["literal_inverse_ln2"]
                and ln2 == support["literal_ln2"],
                "Every actual original reduction and signed clamp literal",
            )
            template = dict(
                stock=stock,
                polynomial=polynomial,
                exponent=exponent,
                clipped=clipped,
                raw_log=raw_log,
                remainder=remainder,
                lower_raw=lo,
                upper_raw=hi,
                inverse_ln2_raw=inverse,
                ln2_raw=ln2,
                actual_stock_signature=signature,
                original_native_stock_node_ids=sorted(closure),
            )
            templates.append(template)
        reference = templates[0]
        parameters = tuple(
            reference[k] for k in ("lower_raw", "upper_raw", "inverse_ln2_raw", "ln2_raw")
        )
        require(
            all(
                tuple(row[k] for k in ("lower_raw", "upper_raw", "inverse_ln2_raw", "ln2_raw"))
                == parameters
                for row in templates
            ),
            "Common original remainder domain at all stock sites",
        )
        if common is None:
            common = parameters
        require(parameters == common, "One common whole domain across both original contracts")
        lo, hi, inverse, ln2 = parameters
        occupied, cells, next_raw = [], [], lo
        for k in EXPONENTS:
            check(started)
            first = max(lo, -((-k * Q**2) // inverse))
            last = min(hi, -((-(k + 1) * Q**2) // inverse) - 1)
            empty = first > last
            row = dict(k=k, empty=empty, clipped_raw_interval=[first, last])
            if not empty:
                require(
                    first == next_raw and first * inverse // Q**2 == last * inverse // Q**2 == k,
                    "Whole actual integer class cover, no gaps or overlaps",
                )
                next_raw = last + 1
                remainder_bounds = word_range((first - k * ln2, last - k * ln2))
                row["remainder_raw_interval"] = list(remainder_bounds)
                occupied.append(row)
            cells.append(row)
        require(
            next_raw == hi + 1 and len(cells) == 30, "Full clipped domain inside fixed30 classes"
        )
        hull = [
            min(row["remainder_raw_interval"][0] for row in occupied),
            max(row["remainder_raw_interval"][1] for row in occupied),
        ]
        reports[case] = dict(
            actual_stock_sites=templates,
            original_cells=cells,
            whole_integer_remainder_hull=hull,
            original_native_settings=list(parameters),
            original_literal_exp_coefficients=support["literal_exp_coefficients"],
            original_baseline_T_depth_qubits=list(BASELINE[case]),
        )
    same(
        reports["B4x12"]["whole_integer_remainder_hull"],
        reports["B8x52"]["whole_integer_remainder_hull"],
        "Both original sources share the complete certified remainder hull",
    )
    return dict(schema="independent-A13-original-source-domain-v1", cases=reports)


def exact_segments(hull, count):
    require(type(count) is int and count in (1, 2, 4, 8), "Fixed segment inventory")
    lo, hi = hull
    require(
        type(lo) is int and type(hi) is int and lo <= hi and hi - lo + 1 >= count,
        "Finite nonempty raw-word domain",
    )
    width = hi - lo + 1
    rows, next_raw = [], lo
    for index in range(count):
        first = lo + index * width // count
        last = lo + (index + 1) * width // count - 1
        center = nearest_fraction(Fraction(first + last, 2))
        require(
            first == next_raw and first <= center <= last,
            "Complete native partition and exact internal center",
        )
        next_raw = last + 1
        rows.append(
            dict(
                index=index,
                first_raw=first,
                last_raw=last,
                center_raw=center,
                local_interval=[
                    encode(Fraction(first - center, Q)),
                    encode(Fraction(last - center, Q)),
                ],
            )
        )
    require(next_raw == hi + 1, "Every raw integer selected once, including ties")
    return rows


def interval_scaled(pair, scale):
    a, b = (value * scale for value in pair)
    return (min(a, b), max(a, b))


def exact_bernstein(coefficients, left, right, degree, started):
    """Original ABI; identical rational vector through the pinned integer kernel."""
    check(started)
    require(callable(INTEGER_BERNSTEIN), "Fully admitted exact arithmetic kernel")
    return INTEGER_BERNSTEIN(coefficients, left, right, degree, lambda: check(started))


def load_integer_bernstein(frozen, external, started):
    """Compile only the already admitted exact function; run no transform here."""
    global INTEGER_BERNSTEIN
    require(INTEGER_BERNSTEIN is None, "No kernel replacement or repeated loading")
    expected = BERNSTEIN_AUTHOR_SHA256[BERNSTEIN_KERNEL.name]
    bind(frozen, external, BERNSTEIN_KERNEL, expected, started)
    data = read_bytes(BERNSTEIN_KERNEL, started)
    require(hashlib.sha256(data).hexdigest() == expected, "Exact kernel bytes before AST compile")
    check(started)
    tree = ast.parse(data, filename=str(BERNSTEIN_KERNEL))
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "integer_bernstein"
    ]
    require(len(matches) == 1, "One reviewed exact integer function")
    function = matches[0]
    require(
        not function.decorator_list
        and not function.args.defaults
        and not function.args.kw_defaults
        and function.returns is None
        and all(argument.annotation is None for argument in function.args.args)
        and len(function.args.args) == 5
        and function.args.vararg is None
        and function.args.kwarg is None
        and not function.args.kwonlyargs
        and not function.args.posonlyargs
        and not any(
            isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef))
            for node in ast.walk(function)
        ),
        "Only five-argument definition; no imports or definition-time evaluation",
    )
    require(
        hashlib.sha256(ast.dump(function, include_attributes=False).encode()).hexdigest()
        == "c6676e11751660894db8b2a03e6752d7e5f16b7805dc34adafe338d5f1039bac",
        "Actual finite-QA function AST identity",
    )
    isolated = ast.Module(body=[function], type_ignores=[])
    ast.fix_missing_locations(isolated)
    environment = {
        "__builtins__": {
            "len": len,
            "range": range,
            "sum": sum,
            "min": min,
            "max": max,
            "tuple": tuple,
            "ValueError": ValueError,
        },
        "Fraction": Fraction,
        "comb": comb,
        "lcm": lcm,
    }
    code = compile(isolated, str(BERNSTEIN_KERNEL), "exec")
    check(started)
    exec(code, environment)
    check(started)
    INTEGER_BERNSTEIN = environment["integer_bernstein"]


def dyadic_outward(pair, bits):
    require(type(bits) is int and bits in (384, 544), "Fixed outward serialization grid")
    scale = 1 << bits
    lower, upper = (Fraction(value) * scale for value in pair)
    require(lower <= upper, "Ordered enclosure before outward serialization")
    return (
        Fraction(lower.numerator // lower.denominator, scale),
        Fraction(-((-upper.numerator) // upper.denominator), scale),
    )


def bernstein_witness(mp, coefficients, segment, terms, started):
    """Independent interval power-to-Bernstein proof on the full CLOSED interval."""
    require(
        terms in (80, 112) and len(coefficients) <= 13, "Prospectively fixed proof and degree caps"
    )
    a, b = [rational(value) for value in segment["local_interval"]]
    center = Fraction(segment["center_raw"], Q)
    require(a <= 0 <= b and a < b, "Exact center inside nondegenerate closed segment")
    ecoefficient = endpoints(mp.iv.exp(outward(mp, center)))
    degree = terms - 1
    polynomial = exact_bernstein(coefficients, a, b, degree, started)
    taylor = exact_bernstein(
        [Fraction(1, factorial(k)) for k in range(terms)], a, b, degree, started
    )
    bernstein = []
    for implemented, witness in zip(polynomial, taylor, strict=True):
        check(started)
        scaled = interval_scaled(ecoefficient, witness)
        pair = (implemented - scaled[1], implemented - scaled[0])
        # Unsnap80 to check every primary384-bit enclosure. Own112 uses a fixed
        # outward544-bit serialization grid, and pays its widening in its bound.
        bernstein.append(dyadic_outward(pair, 544) if terms == 112 else pair)
    hull = (min(pair[0] for pair in bernstein), max(pair[1] for pair in bernstein))
    h = max(abs(a), abs(b))
    upper_domain = Fraction(segment["last_raw"], Q)
    tail = endpoints(
        mp.iv.exp(outward(mp, upper_domain)) * outward(mp, h**terms / factorial(terms))
    )[1]
    error = max(abs(hull[0]), abs(hull[1])) + tail
    return dict(
        Taylor_terms=terms,
        interval_digits=DIGITS,
        exact_exp_center_enclosure=[encode(value) for value in ecoefficient],
        closed_local_interval=segment["local_interval"],
        Bernstein_coefficients=[[encode(value) for value in pair] for pair in bernstein],
        Bernstein_hull=[encode(value) for value in hull],
        Taylor_tail_upper=encode(tail),
        uniform_absolute_error_upper=encode(error),
        finite_grid_or_Remez_convergence_used_as_proof=False,
    )


def estrin_ir(degree, started):
    require(degree in (4, 6, 8, 10, 12), "Exactly one declared degree")
    nodes = [dict(id=0, op="input", args=[])]
    nodes.extend(dict(id=j + 1, op="coefficient", args=[], degree=j) for j in range(degree + 1))
    terms, power, level = list(range(1, degree + 2)), 0, 0
    while len(terms) > 1:
        check(started)
        next_terms = []
        for j in range(0, len(terms), 2):
            if j + 1 == len(terms):
                next_terms.append(terms[j])
                continue
            product = len(nodes)
            nodes.append(dict(id=product, op="mul", args=[power, terms[j + 1]], level=level))
            result = len(nodes)
            nodes.append(dict(id=result, op="add", args=[terms[j], product], level=level))
            next_terms.append(result)
        if len(next_terms) > 1:
            squared = len(nodes)
            nodes.append(dict(id=squared, op="mul", args=[power, power], level=level))
            power = squared
        terms, level = next_terms, level + 1
    return dict(
        degree=degree,
        nodes=nodes,
        polynomial_output=terms[0],
        unpaired_term_carried=True,
        zero_padding=False,
        unused_candidate_power_emitted=False,
    )


def polynomial_sum(first, second):
    result = dict(first)
    for degree, value in second.items():
        result[degree] = result.get(degree, Fraction(0)) + value
    return {degree: value for degree, value in result.items() if value != 0}


def polynomial_product(first, second):
    result = {}
    for a, x in first.items():
        for b, y in second.items():
            result[a + b] = result.get(a + b, Fraction(0)) + x * y
    return {degree: value for degree, value in result.items() if value != 0}


def native_estrin_certificate(ir, words, local_raw, started):
    """No execution/replay: whole-interval range and floor-error induction over the fixed IR."""
    require(
        len(words) == ir["degree"] + 1 and all(type(word) is int for word in words),
        "All actual selected coefficient words in ascending degree",
    )
    local = word_range(local_raw)
    radius = Fraction(max(abs(value) for value in local), Q)
    ranges, polynomials, errors, rows, products = {}, {}, {}, [], []
    for node in ir["nodes"]:
        check(started)
        value, op = node["id"], node["op"]
        if op == "input":
            bounds, polynomial, error = local, {1: Fraction(1)}, Fraction(0)
        elif op == "coefficient":
            word = signed_coefficient(words[node["degree"]])
            bounds, polynomial, error = (word, word), {0: Fraction(word, Q)}, Fraction(0)
        else:
            left, right = node["args"]
            first, second = polynomials[left], polynomials[right]
            if op == "add":
                bounds = (ranges[left][0] + ranges[right][0], ranges[left][1] + ranges[right][1])
                polynomial = polynomial_sum(first, second)
                error = errors[left] + errors[right]
            else:
                require(op == "mul", "No implicit operation or free floor in candidate IR")
                product = integer_product(ranges[left], ranges[right], square=left == right)
                bounds = (product[0] // Q, product[1] // Q)
                products.append(dict(value=value, product_raw_bounds=list(product)))
                polynomial = polynomial_product(first, second)
                ma = sum((abs(c) * radius**d for d, c in first.items()), Fraction(0))
                mb = sum((abs(c) * radius**d for d, c in second.items()), Fraction(0))
                error = ma * errors[right] + mb * errors[left] + errors[left] * errors[right] + EPS
                require(
                    (ma + errors[left]) * (mb + errors[right]) * Q**2 < 1 << 143,
                    "Candidate ideal/native error-induction product also signed144 safe",
                )
        ranges[value] = word_range(bounds)
        magnitude = sum((abs(c) * radius**d for d, c in polynomial.items()), Fraction(0)) + error
        require(magnitude * Q < 1 << 71, "Candidate whole stored-word error induction no-wrap")
        polynomials[value], errors[value] = polynomial, error
        rows.append(
            dict(
                value=value,
                op=op,
                raw_bounds=list(bounds),
                magnitude_upper=encode(magnitude),
                native_floor_error_upper=encode(error),
            )
        )
    output = ir["polynomial_output"]
    same(
        [encode(polynomials[output].get(j, Fraction(0))) for j in range(ir["degree"] + 1)],
        [encode(Fraction(word, Q)) for word in words],
        "Fixed IR evaluates exactly the selected quantized polynomial",
    )
    return dict(
        native_intermediate_ranges=rows,
        signed144_products=products,
        native_floor_error_upper=encode(errors[output]),
        native_polynomial_raw_bounds=list(ranges[output]),
        all_native72_product144_guards_passed=True,
        every_actual_multiplication_floor_paid=True,
    )


def class_segment_intersections(
    mp, domain, segments, words, quantized_errors, degree, started, authorized_ln2_error=None
):
    """All fixed30 classes times every segment, including empty native intersections."""
    ir = estrin_ir(degree, started)
    lo, hi, inverse, ln2_word = domain["original_native_settings"]
    actual_ln2 = Fraction(ln2_word, Q)
    true_ln2 = endpoints(mp.iv.log(outward(mp, 2)))
    ln_error = max(abs(actual_ln2 - value) for value in true_ln2)
    if authorized_ln2_error is not None:
        require(
            authorized_ln2_error >= ln_error,
            "Primary reduction literal envelope independently valid",
        )
        ln_error = authorized_ln2_error
    rows, stock_error = [], Fraction(0)
    for cell in domain["original_cells"]:
        for segment in segments:
            check(started)
            k, index = cell["k"], segment["index"]
            first, last = cell["clipped_raw_interval"]
            if not cell["empty"]:
                first = max(first, segment["first_raw"] + k * ln2_word)
                last = min(last, segment["last_raw"] + k * ln2_word)
            empty = cell["empty"] or first > last
            row = dict(k=k, segment=index, empty=empty, clipped_log_raw_bounds=[first, last])
            if not empty:
                require(
                    lo <= first <= last <= hi
                    and first * inverse // Q**2 == last * inverse // Q**2 == k,
                    "Exact whole original reduction-class intersection",
                )
                remainder = word_range((first - k * ln2_word, last - k * ln2_word))
                local = word_range(
                    (remainder[0] - segment["center_raw"], remainder[1] - segment["center_raw"])
                )
                require(
                    segment["first_raw"] <= remainder[0] <= remainder[1] <= segment["last_raw"],
                    "Actual integer selector ties and exact center subtraction",
                )
                native = native_estrin_certificate(ir, words[index], local, started)
                minimum, maximum = native["native_polynomial_raw_bounds"]
                require(
                    minimum > 0, "Every candidate stock polynomial is positive on its actual cell"
                )
                require(-72 < k < 72, "Same original full-word shift exponent")
                shifted = word_range(
                    (minimum << k, maximum << k) if k >= 0 else (minimum >> -k, maximum >> -k)
                )
                floor = rational(native["native_floor_error_upper"])
                approximation = quantized_errors[index]
                r_max = Fraction(remainder[1], Q)
                scale = Fraction(2) ** k
                reduction = endpoints(
                    outward(mp, scale)
                    * mp.iv.exp(outward(mp, r_max))
                    * (mp.iv.exp(outward(mp, abs(k) * ln_error)) - 1)
                )[1]
                final_floor = EPS if k < 0 else Fraction(0)
                absolute = scale * (approximation + floor) + reduction + final_floor
                require(absolute >= 0, "Complete nonnegative candidate absolute stock envelope")
                stock_error = max(stock_error, absolute)
                row.update(
                    remainder_raw_bounds=list(remainder),
                    local_raw_bounds=list(local),
                    native_floor_error_upper=encode(floor),
                    native_intermediate_ranges=native["native_intermediate_ranges"],
                    signed144_products=native["signed144_products"],
                    native_polynomial_raw_bounds=native["native_polynomial_raw_bounds"],
                    ln2_literal_error_upper=encode(ln_error),
                    reduction_stock_error_upper=encode(reduction),
                    negative_shift_floor_upper=encode(final_floor),
                    absolute_stock_error_upper=encode(absolute),
                    stock_raw_bounds=list(shifted),
                    all_native72_product144_and_shift_guards_passed=True,
                )
            rows.append(row)
    require(len(rows) == 30 * len(segments), "Every empty and nonempty class/segment row retained")
    for cell in domain["original_cells"]:
        if cell["empty"]:
            continue
        covered = sorted(
            row["clipped_log_raw_bounds"]
            for row in rows
            if row["k"] == cell["k"] and not row["empty"]
        )
        require(
            covered
            and covered[0][0] == cell["clipped_raw_interval"][0]
            and covered[-1][1] == cell["clipped_raw_interval"][1]
            and all(first[1] + 1 == second[0] for first, second in zip(covered, covered[1:])),
            "Candidate selector covers each original integer class without gap or overlap",
        )
    return dict(
        classes_segments=rows,
        absolute_stock_error_upper=encode(stock_error),
        exact_candidate_IR=ir,
        all_fixed_classes_and_segments_retained=True,
        original_G2_allocation_or_safety_not_transferred=True,
    )


def canonical_digest(value, started):
    check(started)
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    check(started)
    state = hashlib.sha256()
    for offset in range(0, len(data), 1 << 20):
        check(started)
        state.update(data[offset : offset + (1 << 20)])
        check(started)
    return state.hexdigest()


def finite_binary(value):
    point = rational(value)
    denominator = point.denominator
    require(denominator & (denominator - 1) == 0, "Exact serialized finite binary fitting value")
    return point


def alternating_selection(residuals, length, started):
    """Exact dyadic integer threshold feasibility, then prefix sum/lex states."""
    check(started)
    require(type(length) is int and 1 <= length <= 14, "Fixed finite selection length")
    require(2 <= len(residuals) <= 67, "Unchanged finite fitting candidate cap")
    dyadics, exponent = [], 0
    for index, value in enumerate(residuals):
        check(started)
        value = Fraction(value)
        denominator = value.denominator
        require(
            denominator & (denominator - 1) == 0,
            "Independently validated residual remains exact finite dyadic",
        )
        local_exponent = denominator.bit_length() - 1
        exponent = max(exponent, local_exponent)
        dyadics.append((index, value.numerator, local_exponent))
        check(started)
    denominator = 1 << exponent
    check(started)
    points = []
    for index, numerator, local_exponent in dyadics:
        check(started)
        weight = numerator << (exponent - local_exponent)
        if weight:
            points.append((index, abs(weight), 1 if weight > 0 else -1))
        check(started)
    thresholds = sorted({height for _, height, _ in points})
    check(started)
    require(thresholds, "Alternating nonzero candidate residuals")

    def possible(threshold):
        last, runs = None, 0
        for _, height, sign in points:
            check(started)
            if height >= threshold and sign != last:
                runs += 1
                last = sign
        return runs >= length

    require(possible(thresholds[0]), "Declared alternating subset exists")
    low, high = 0, len(thresholds)
    while low + 1 < high:
        check(started)
        middle = (low + high) // 2
        if possible(thresholds[middle]):
            low = middle
        else:
            high = middle
    threshold = thresholds[low]
    states = [[None] * (length + 1), [None] * (length + 1)]
    for index, height, sign in points:
        check(started)
        if height < threshold:
            continue
        ending = 1 if sign > 0 else 0
        for size in range(length, 1, -1):
            check(started)
            previous = states[1 - ending][size - 1]
            if previous is None:
                continue
            total, indices = previous[0] + height, previous[1] + (index,)
            old = states[ending][size]
            if old is None or total > old[0] or total == old[0] and indices < old[1]:
                states[ending][size] = (total, indices)
            check(started)
        first = (height, (index,))
        old = states[ending][1]
        if old is None or first[0] > old[0] or first[0] == old[0] and first[1] < old[1]:
            states[ending][1] = first
        check(started)
    candidates = [state[length] for state in states if state[length] is not None]
    require(candidates, "Threshold-constrained alternating optimum")
    total, indices = min(candidates, key=lambda value: (-value[0], value[1]))
    require(
        min(
            abs(numerator << (exponent - local_exponent))
            for index, numerator, local_exponent in dyadics
            if index in indices
        )
        == threshold,
        "Exact bottleneck attained",
    )
    check(started)
    result = Fraction(threshold, denominator), Fraction(total, denominator), list(indices)
    check(started)
    return result


def audit_fit_segment(declared, degree, segment, started):
    expected = dict(
        segment=segment["index"],
        raw_bounds=[segment["first_raw"], segment["last_raw"]],
        center_raw=segment["center_raw"],
        local_interval=segment["local_interval"],
    )
    for key, value in expected.items():
        same(declared[key], value, "Exact preregistered native segment: " + key)
    require(
        declared["degree"] == degree
        and declared["coefficients_from_round32_solve"] is True
        and declared["extra33rd_solve"] is False
        and declared["root_search_fitting_evidence_only"] is True
        and declared["global_minimax_optimality_claim"] is False,
        "Fixed fitting claim scope",
    )
    rounds = declared["exchange_rounds"]
    require(type(rounds) is list and len(rounds) == 32, "Exactly32 finite solve/exchange rounds")
    left, right = (rational(value) for value in segment["local_interval"])
    previous = None
    for index, row in enumerate(rounds):
        check(started, admission=True)
        require(row["round"] == index + 1, "Exact round order")
        solve = [finite_binary(value) for value in row["solve_nodes"]]
        require(
            len(solve) == degree + 2
            and all(a < b for a, b in zip(solve, solve[1:]))
            and left <= solve[0] <= solve[-1] <= right,
            "Distinct in-domain solve nodes",
        )
        if previous is not None:
            same(row["solve_nodes"], previous, "No hidden fitting solve or exchange")
        solved = [finite_binary(value) for value in row["solved_coefficients"]]
        require(len(solved) == degree + 1, "Each solve has exactly the declared coefficient count")
        finite_binary(row["solved_alternating_error"])
        extrema = [finite_binary(value) for value in row["candidate_extrema"]]
        heights = [finite_binary(value) for value in row["candidate_residuals"]]
        require(
            len(extrema) == len(heights)
            and 2 <= len(extrema) <= 67
            and extrema[0] == left
            and extrema[-1] == right
            and all(a < b for a, b in zip(extrema, extrema[1:])),
            "Endpoints and deduplicated candidate locations",
        )
        seen_cells = set()
        for bracket in row["candidate_stationary_brackets"]:
            check(started)
            cell = bracket["grid_cell"]
            require(
                type(cell) is int and 0 <= cell < 64 and cell not in seen_cells,
                "Each frozen64 bracket at most once",
            )
            seen_cells.add(cell)
            a, b = (finite_binary(value) for value in bracket["final_bracket"])
            cell_left = left + (right - left) * cell / 64
            cell_right = left + (right - left) * (cell + 1) / 64
            require(
                cell_left <= a <= b <= cell_right and b - a <= (cell_right - cell_left) / (1 << 24),
                "Exactly24 bisection bound, including exact root collapse",
            )
            require(
                (a + b) / 2 in extrema, "Every retained bracket midpoint is a fitting candidate"
            )
        threshold, total, indices = alternating_selection(heights, degree + 2, started)
        same(row["selected_next_node_indices"], indices, "Exact bottleneck, sum and lex exchange")
        same(
            row["exact_exchange_bottleneck"],
            encode(threshold),
            "Exact serialized bottleneck threshold",
        )
        require(
            row["exact_two_pass_bottleneck_then_sum_lex"] is True,
            "Declared finite exchange algorithm",
        )
        following = [row["candidate_extrema"][value] for value in indices]
        same(row["selected_next_nodes"], following, "Selected node positions and index ordering")
        previous = following
    coefficients = [finite_binary(value) for value in declared["coefficients_before_quantization"]]
    same(
        declared["coefficients_before_quantization"],
        rounds[-1]["solved_coefficients"],
        "Round32 coefficients, no33rd solve",
    )
    words = [signed_coefficient(nearest_fraction(value * Q)) for value in coefficients]
    same(declared["coefficient_raw"], words, "Exactly one signedf40 nearest/ties-even conversion")
    return (
        coefficients,
        words,
        dict(
            rounds_structurally_checked=32,
            selected_exchange_objectives_exact=True,
            fitting_numeric_solve_or_root_search_reexecuted=False,
            fitting_diagnostics_used_as_uniform_proof=False,
        ),
    )


def audit_segment_certificate(mp, declared, coefficients, words, segment, started):
    for key, expected in (
        ("segment", segment["index"]),
        ("raw_bounds", [segment["first_raw"], segment["last_raw"]]),
        ("center_raw", segment["center_raw"]),
        ("local_interval", segment["local_interval"]),
        ("Taylor_terms", 80),
        ("Bernstein_degree", 79),
        ("Bernstein_coefficients_count", 80),
        ("Bernstein_outward_binary_grid_bits", 384),
    ):
        same(declared[key], expected, "Frozen primary uniform proof setting: " + key)
    require(
        declared["mesh_or_exchange_convergence_used_as_uniform_proof"] is False,
        "Full interval proof is independent of fitting mesh",
    )
    own80, own112, authorized = {}, {}, {}
    for name, actual in (
        ("fit", coefficients),
        ("quantized", [Fraction(word, Q) for word in words]),
    ):
        check(started, admission=True)
        proof = bernstein_witness(mp, actual, segment, 80, started)
        enclosures_contain(
            declared["exp_center_enclosure"],
            proof["exact_exp_center_enclosure"],
            "Fresh130 exponential center inclusion",
        )
        saved = declared[name + "_Bernstein_coefficient_enclosures"]
        require(
            type(saved) is list and len(saved) == 80,
            "All actual80 primary coefficient enclosures retained",
        )
        maximum = Fraction(0)
        for old, fresh in zip(saved, proof["Bernstein_coefficients"], strict=True):
            check(started)
            enclosures_contain(
                old, fresh, "Every primary Bernstein coefficient independently enclosed"
            )
            lo, hi = (rational(value) for value in old)
            require(
                lo * (1 << 384) == int(lo * (1 << 384)) and hi * (1 << 384) == int(hi * (1 << 384)),
                "Fixed outward384-bit grid evidence",
            )
            maximum = max(maximum, abs(lo), abs(hi))
        require(
            declared[name + "_Bernstein_SHA256"] == canonical_digest(saved, started),
            "Digest names actual saved coefficient list",
        )
        tail = rational(declared["Taylor_tail_upper"])
        require(
            tail >= rational(proof["Taylor_tail_upper"]) >= 0,
            "Whole closed interval analytic Taylor tail",
        )
        claimed = rational(declared[name + "_uniform_error_upper"])
        require(
            claimed == maximum + tail, "Saved outward conversion and analytic tail are both paid"
        )
        authorized[name] = claimed
        # Do not compare a degree79 hull to degree111: distinct valid witnesses
        # can produce different conservative hull bounds.
        own80[name] = dict(
            Taylor_terms=80,
            interval_digits=DIGITS,
            every_saved_primary_coefficient_contains_independent130=True,
            verified_primary_uniform_error_upper=encode(claimed),
            independent_analytic_tail_upper=proof["Taylor_tail_upper"],
        )
        own112[name] = bernstein_witness(mp, actual, segment, 112, started)
        own112[name]["Bernstein_outward_binary_grid_bits"] = 544
    return authorized, dict(
        primary80_authorizations=own80,
        independent112_certificates=own112,
        independent112_compared_as_primary80_replacement=False,
    )


def implementation_policy(started):
    policy = read_json(IMPLEMENTATION, started)
    require(
        policy["schema"] == "a13-exp-frontier-recovery-audit-only-implementation-preflight-v6",
        "Exact implementation release",
    )
    same(policy["CPU_admission_wall_seconds"], [CPU, ADMISSION, WALL], "Same all20 row budget")
    same(policy["owned_caps_files_bytes"], [64, 128 * 1024**2], "Unchanged owned artifact caps")
    same(policy["fixed_grid"], [list(value) for value in GRID], "No extra/adaptive architecture")
    require(
        policy["primary_digits"] == 90
        and policy["independent_digits"] == DIGITS
        and policy["threads"] == 1
        and policy["new_fixture_credit"] == 0,
        "Fixed independent precision and zero credit",
    )
    require(
        policy["candidate_G2_absolute_stock_error_allocation"] is None
        and policy["candidate_G2_barrier_band_allocation"] is None
        and policy["gate_emission_authorized"] is False,
        "Allocation-free exploratory screen only",
    )
    same(
        policy["original_method_document_SHA256"],
        {METHOD.name: METHOD_SHA, METHOD_DOC.name: METHOD_DOC_SHA},
        "Held method bytes",
    )
    require(policy["A07_manifest_SHA256"] == A07_SHA, "Actual frozen A07 interface owner")
    same(
        policy["original_recovery_author_SHA256"],
        ORIGINAL_RECOVERY_AUTHOR_SHA256,
        "All six executed recovery author and paper bytes remain immutable",
    )
    same(
        policy["original_recovery_source_author_sha256"],
        {
            name: ORIGINAL_RECOVERY_AUTHOR_SHA256[name]
            for name in (PRODUCER_AUTHOR.name, "audit_exp_frontier_recovery.py")
        },
        "Actual successful metadata source author pair remains separate from this new audit",
    )
    require(
        policy["source_manifest_SHA256"] == ORIGINAL_RECOVERY_SOURCE_SHA
        and policy["prior_recovery_audit_failed_manifest_SHA256"] == PRIOR_RECOVERY_AUDIT_SHA
        and policy["prior_recovery_root_review_manifest_SHA256"] == PRIOR_RECOVERY_REVIEW_SHA,
        "Actual metadata-only source and failed independent audit/review pins",
    )
    same(
        policy["prior_recovery_audit_v2_author_SHA256"],
        PRIOR_RECOVERY_AUDIT_V2_AUTHOR_SHA256,
        "All three executed audit-only v2 author bytes remain immutable",
    )
    require(
        type(PRIOR_RECOVERY_AUDIT_V2_SHA) is str
        and SHA_PATTERN.fullmatch(PRIOR_RECOVERY_AUDIT_V2_SHA)
        and policy["prior_recovery_audit_v2_failed_manifest_SHA256"] == PRIOR_RECOVERY_AUDIT_V2_SHA
        and policy["prior_recovery_audit_v2_root_review_manifest_SHA256"]
        == PRIOR_RECOVERY_V2_REVIEW_SHA,
        "Actual prior serialization-only failure and static release pins",
    )
    same(
        policy["prior_recovery_audit_v3_author_SHA256"],
        PRIOR_RECOVERY_AUDIT_V3_AUTHOR_SHA256,
        "All three executed audit-only v3 author bytes remain immutable",
    )
    require(
        policy["prior_recovery_audit_v3_failed_manifest_SHA256"] == PRIOR_RECOVERY_AUDIT_V3_SHA
        and policy["prior_recovery_audit_v3_root_review_manifest_SHA256"]
        == PRIOR_RECOVERY_V3_REVIEW_SHA,
        "Actual prior all20 budget censor and static review pins",
    )
    same(
        policy["prior_recovery_audit_v4_author_SHA256"],
        PRIOR_RECOVERY_AUDIT_V4_AUTHOR_SHA256,
        "Immutable executed V4 source and companions",
    )
    same(
        policy["Bernstein_author_SHA256"],
        BERNSTEIN_AUTHOR_SHA256,
        "Actual pinned arithmetic kernel and complete finite-QA author quartet",
    )
    require(
        policy["prior_recovery_audit_v4_failed_manifest_SHA256"] == PRIOR_RECOVERY_AUDIT_V4_SHA
        and policy["prior_recovery_audit_v4_root_review_manifest_SHA256"]
        == PRIOR_RECOVERY_V4_REVIEW_SHA
        and policy["actual_profile_manifest_SHA256"] == PRIOR_PROFILE_SHA
        and policy["Bernstein_finite_QA_manifest_SHA256"] == BERNSTEIN_QA_SHA
        and policy["Bernstein_finite_QA_ROOT_READY_SHA256"] == BERNSTEIN_QA_READY_SHA
        and policy["previous_failed_audit_v4_credit"] == 0
        and policy["kernel_AST_only_no_module_import"] is True,
        "Actual failed V4/profile/finite-QA guards; no prospective or partial PASS",
    )
    dp_pins = policy["exact_DP_optimization_method_document_SHA256"]
    require(
        type(dp_pins) is dict and set(dp_pins) == {DP_METHOD.name, DP_METHOD_DOC.name},
        "Exact separately frozen dyadic DP optimization prospectus",
    )
    for name, expected in dp_pins.items():
        check(started)
        require(
            type(expected) is str and SHA_PATTERN.fullmatch(expected),
            "Null optimization prospectus pin blocks prepare",
        )
        require(sha(RESEARCH / name, started) == expected, "Exact optimization prospectus SHA")
    dp_method = read_json(DP_METHOD, started)
    require(
        dp_method["schema"] == "a13-exp-frontier-recovery-exact-dp-optimization-prospectus-v4"
        and dp_method["source_manifest_SHA256"] == ORIGINAL_RECOVERY_SOURCE_SHA
        and dp_method["preserved_failed_audit003"]["manifest_SHA256"] == PRIOR_RECOVERY_AUDIT_V3_SHA
        and dp_method["candidate_G2_established"] is False
        and dp_method["gate_emission_authorized"] is False
        and dp_method["adoption"] is False
        and dp_method["new_test_credit"] == 0,
        "Exact operational method cannot promote failed rows or candidate G2",
    )
    same(dp_method["CPU_admission_wall_seconds"], [CPU, ADMISSION, WALL], "Unchanged DP clocks")
    same(dp_method["fixed_grid"], [list(value) for value in GRID], "Unchanged DP inventory")
    same(
        policy["prior_A13_v2_author_SHA256"],
        PRIOR_V2_SHA256,
        "Original unsealed v2 quartet unchanged",
    )
    require(
        policy["prior_A13_v2_root_review_manifest_SHA256"] == PRIOR_V2_REVIEW_SHA,
        "Original v2 static review manifest pin",
    )
    require(
        policy["capture_manifest_SHA256"]
        == "20126972220fc8ae35aae71e789e96b4dde6b755b9c692c97b4e89dfdb9285c3",
        "Actual root integrity-only failure capture pin",
    )
    recovery_pins = policy["method_document_SHA256"]
    same(
        recovery_pins,
        policy["original_recovery_method_document_SHA256"],
        "No change to the held recovery method",
    )
    same(
        recovery_pins,
        {
            name: ORIGINAL_RECOVERY_AUTHOR_SHA256[name]
            for name in (RECOVERY_METHOD.name, RECOVERY_METHOD_DOC.name)
        },
        "Exact original held recovery method bytes",
    )
    require(
        type(recovery_pins) is dict
        and set(recovery_pins) == {RECOVERY_METHOD.name, RECOVERY_METHOD_DOC.name},
        "Exact newly frozen recovery paper",
    )
    for name, expected in recovery_pins.items():
        require(sha(RESEARCH / name, started) == expected, "Recovery method byte pin")
    same(policy["prior_A13_author_SHA256"], PRIOR_AUTHOR_SHA256, "Original quartet unchanged")
    require(
        policy["prior_A13_failed_receipt_manifest_SHA256"] == PRIOR_FAILED_SHA
        and policy["prior_A13_root_review_manifest_SHA256"] == PRIOR_REVIEW_SHA
        and policy["previous_failed_A13_credit"] == 0,
        "Exact failed original and static review, zero credit",
    )
    same(
        [policy["recovery_source_receipt"], policy["recovery_audit_receipt"]],
        [SOURCE.relative_to(ROOT).as_posix(), OUTPUT.relative_to(ROOT).as_posix()],
        "Fresh operational v6 receipt routes",
    )
    author = policy["author_sha256"]
    require(
        type(author) is dict and set(author) == {AUTHOR.name},
        "Only the newly reviewed independent audit executable",
    )
    for name, expected in author.items():
        check(started)
        require(
            type(expected) is str and SHA_PATTERN.fullmatch(expected),
            "Null source pin blocks prepare",
        )
        require(sha(RESEARCH / name, started) == expected, "Exact author source SHA")
    return policy


def no_failure(receipt):
    require(
        not any(
            (receipt / name).exists()
            for name in (
                "FAILED_UNSEALED.json",
                "failure.json",
                "run_failure.json",
                "prepare_failure.json",
            )
        ),
        "No failed, unsealed or partial prerequisite",
    )


def prior_a13_provenance(policy, frozen, external, started):
    """Strict active original maps; failure remains zero-credit evidence only."""
    same(policy["prior_A13_author_SHA256"], PRIOR_AUTHOR_SHA256, "Exact original author quartet")
    require(not (PROGRAM / "A13_audit_run001").exists(), "Original audit was never executed")
    for name, expected in PRIOR_AUTHOR_SHA256.items():
        check(started)
        bind(frozen, external, RESEARCH / name, expected, started)
    records = []
    for receipt, expected_manifest, expected_counts in (
        (PRIOR_FAILED, PRIOR_FAILED_SHA, [13, 832, 2842]),
        (PRIOR_REVIEW, PRIOR_REVIEW_SHA, [1, 6, 0]),
    ):
        check(started)
        path = bind(frozen, external, receipt / "manifest.json", expected_manifest, started)
        records.append(
            dict(
                owner_manifest=path.relative_to(ROOT).as_posix(),
                source_map="manifest",
                original_key=path.relative_to(ROOT).as_posix(),
                verified_input_path=path.relative_to(ROOT).as_posix(),
                original_expected_sha256=expected_manifest,
                expected_hash_waived=False,
            )
        )
        manifest = read_json(path, started)
        require(manifest["manifest_self_hash_excluded"] is True, "Original self-hash exclusion")
        mappings = [
            (field, manifest.get(field, {}))
            for field in ("files", "frozen_inputs", "external_runtime_inputs")
        ]
        require(all(type(mapping) is dict for _, mapping in mappings), "Complete original maps")
        same([len(mapping) for _, mapping in mappings], expected_counts, "All original references")
        owned = set()
        for field, mapping in mappings:
            for key, expected in mapping.items():
                check(started)
                require(type(key) is str, "Typed original key spelling")
                if field == "external_runtime_inputs":
                    require(Path(key).is_absolute(), "Explicit original external runtime")
                    candidate = Path(key)
                else:
                    require(
                        not Path(key).is_absolute() and "\\" not in key,
                        "Original canonical relative ROOT/owned key",
                    )
                    candidate = (
                        ROOT / key
                        if key.startswith("results/") or field == "frozen_inputs"
                        else receipt / key
                    )
                actual = bind(frozen, external, candidate, expected, started)
                if field == "files":
                    require(
                        lexically_under(actual, receipt) and actual != path and actual not in owned,
                        "No escaped, duplicate or aliased original owned entry",
                    )
                    owned.add(actual)
                    canonical = (
                        actual.relative_to(ROOT).as_posix()
                        if key.startswith("results/")
                        else actual.relative_to(receipt).as_posix()
                    )
                    require(key == canonical, "Exact original own key")
                elif field == "frozen_inputs":
                    require(
                        lexically_under(actual, ROOT)
                        and actual.relative_to(ROOT).as_posix() == key,
                        "Strict original active ROOT binding without archive or waiver",
                    )
                else:
                    require(
                        not lexically_under(actual, ROOT) and str(actual) == key,
                        "Exact original external binding",
                    )
                records.append(
                    dict(
                        owner_manifest=path.relative_to(ROOT).as_posix(),
                        source_map=field,
                        original_key=key,
                        verified_input_path=actual.relative_to(ROOT).as_posix()
                        if lexically_under(actual, ROOT)
                        else str(actual),
                        original_expected_sha256=expected,
                        expected_hash_waived=False,
                    )
                )
                check(started)
        actual_owned, total = set(), 0
        for candidate in receipt.rglob("*"):
            check(started)
            if not candidate.is_file():
                continue
            actual = canonical_path(candidate, started)
            require(
                lexically_under(actual, receipt) and actual not in actual_owned,
                "Original directory noalias confinement",
            )
            actual_owned.add(actual)
            total += actual.stat().st_size
            require(len(actual_owned) <= 25000 and total <= 8 * 1024**3, "Original membership cap")
        require(actual_owned == owned | {path}, "Complete exact original owned inventory")
        if receipt == PRIOR_FAILED:
            require(
                manifest["schema"] == "a13-exp-frontier-terminal-manifest-v1"
                and manifest["completed"] is False
                and manifest["passed"] is False
                and manifest["budget_censored"] is False,
                "Actual sealed original failure, not numerical or resource result",
            )
            outcome = read_json(receipt / "completion_outcome.json", started)
            failure = read_json(receipt / "failure.json", started)
            require(
                outcome["completed"] is False
                and outcome["passed"] is False
                and outcome["failed"] is True
                and outcome["budget_censored"] is False
                and outcome["phase"] == "run"
                and outcome["new_test_credit"] == 0
                and outcome["full_G2"] is False
                and outcome["cost_transfer"] is False
                and outcome["adoption"] is False
                and failure["all_fixture_credit"] == 0
                and failure["error_type"] == "MathematicalGuardError"
                and "signed_range(bounds)" in failure["traceback"],
                "Preserve exact tuple-representation failure and zero credit",
            )
            same(
                outcome["limits_CPU_admission_wall"],
                [CPU, ADMISSION, WALL],
                "Original fixed limits",
            )
            for observation in (outcome["budget"], manifest["terminal_budget_observation"]):
                require(
                    0 <= observation["process_CPU_seconds"] < CPU
                    and 0 <= observation["wall_seconds"] < WALL,
                    "Original failure sealed within unchanged hard limits",
                )
            for name in (
                "summary.json",
                "source_domain_binding.json",
                "fixed_inventory.json",
                "original_baseline_certificate.json",
                "coefficient_fit_diagnostics.json",
                "exponential_approximation_certificate.json",
                "function_frontier.json",
            ):
                require(not (receipt / name).exists(), "No fabricated original scientific result")
            no_unsealed = ("FAILED_UNSEALED.json", "failed_unsealed.json")
            require(
                not any((receipt / name).exists() for name in no_unsealed),
                "Original sealed failure only",
            )
            for name, expected in PRIOR_AUTHOR_SHA256.items():
                require(
                    manifest["files"]["executed_code/" + name] == expected,
                    "Exact old executed quartet",
                )
        else:
            no_failure(receipt)
            review = read_json(receipt / "summary.json", started)
            require(
                review["schema"] == "root-a13-exp-frontier-static-release-v1"
                and review["passed"] is True
                and review["root_static_review"] is True
                and review["independent_text_peer_review"] is True
                and review["new_scientific_execution_during_review"] is False
                and review["new_fixture_credit"] == 0
                and review["candidate_G2_allocations"] is None
                and review["realized_cost_or_emission_authorized"] is False,
                "Static original review has no scientific credit",
            )
            same(
                review["limits_CPU_admission_wall"],
                [CPU, ADMISSION, WALL],
                "Original static limit record",
            )
        check(started)
    return dict(
        prior_A13_author_SHA256=PRIOR_AUTHOR_SHA256,
        prior_A13_failed_receipt_manifest_SHA256=PRIOR_FAILED_SHA,
        prior_A13_root_review_manifest_SHA256=PRIOR_REVIEW_SHA,
        previous_failed_A13_credit=0,
        original_audit_run001_absent=True,
        failed_source_domain_binding_or_fit_bound_resource_result_claim=False,
        records=records,
    )


def freeze_owner(path, expected_manifest, frozen, external, started):
    """Full old receipt maps and actual owned membership, without replay or LIVE waiver."""
    path = bind(frozen, external, path, expected_manifest, started)
    receipt = path.parent
    no_failure(receipt)
    data = read_json(path, started)
    flat = path == PROGRAM / "A10_coefficient_run001/manifest.json" and "files" not in data
    if flat:
        mappings = [("flat_owned_files", data)]
    else:
        require(
            data.get("manifest_self_hash_excluded") is True, "Exact self-hash exclusion convention"
        )
        mappings = [
            (field, data.get(field, {}))
            for field in ("files", "frozen_inputs", "external_runtime_inputs")
        ]
    owned, owned_expected, records = set(), {}, []
    for field, mapping in mappings:
        require(
            type(mapping) is dict and (mapping or field != "files"), "Complete typed receipt map"
        )
        for original, expected in mapping.items():
            check(started)
            require(type(original) is str, "Typed original map path")
            key = original.replace("\\", "/")
            if field == "external_runtime_inputs":
                require(Path(original).is_absolute(), "Explicit actual external path")
                route = Path(original)
            else:
                require(not Path(original).is_absolute(), "ROOT or receipt relative original path")
                route = (
                    ROOT / key
                    if key.startswith(
                        ("results/", "research/", "docs/", "manuscript/", ".context/")
                    )
                    else receipt / key
                )
            archived = False
            if field == "frozen_inputs":
                original_actual = route.resolve(strict=False)
                require(
                    lexically_under(original_actual, ROOT)
                    and original_actual.relative_to(ROOT).as_posix() == key,
                    "Canonical historical ROOT dependency origin",
                )
                if original_actual.is_file() and sha(original_actual, started) == expected:
                    actual = bind(frozen, external, original_actual, expected, started)
                else:
                    matches = [
                        candidate
                        for candidate, value in owned_expected.items()
                        if value == expected
                        and candidate.name
                        in (original_actual.name, "executed_" + original_actual.name)
                    ]
                    require(
                        matches, "Exact owner-owned equal-SHA archive required; no expected waiver"
                    )
                    actual = bind(frozen, external, sorted(matches)[0], expected, started)
                    archived = True
            else:
                actual = bind(frozen, external, route, expected, started)
            if field in ("files", "flat_owned_files"):
                require(
                    lexically_under(actual, receipt) and actual != path and actual not in owned,
                    "No escaped, duplicate, self-hashed or aliased owned artifact",
                )
                owned.add(actual)
                owned_expected[actual] = expected
                canonical = (
                    actual.relative_to(ROOT).as_posix()
                    if key.startswith("results/")
                    else actual.relative_to(receipt).as_posix()
                )
                require(canonical == key, "Exact historical slash-normalized own key")
            elif field == "frozen_inputs":
                require(
                    lexically_under(actual, ROOT),
                    "Current or exact owner-owned archived dependency route",
                )
            else:
                require(
                    not lexically_under(actual, ROOT) and str(actual) == original,
                    "Separate canonical external runtime key",
                )
            records.append(
                dict(
                    owner_manifest=path.relative_to(ROOT).as_posix(),
                    source_map=field,
                    original_key=original,
                    verified_input_path=(
                        actual.relative_to(ROOT).as_posix()
                        if lexically_under(actual, ROOT)
                        else str(actual)
                    ),
                    original_expected_sha256=expected,
                    expected_hash_waived=False,
                )
            )
            records[-1]["archived_equal_SHA_route"] = archived
    actual_owned, byte_count = set(), 0
    for candidate in receipt.rglob("*"):
        check(started)
        if candidate.is_file():
            actual = canonical_path(candidate, started)
            require(
                lexically_under(actual, receipt) and actual not in actual_owned,
                "Actual owned inventory cannot alias or escape",
            )
            actual_owned.add(actual)
            byte_count += actual.stat().st_size
            require(
                len(actual_owned) <= 25000 and byte_count <= 8 * 1024**3,
                "Finite receipt byte/membership cap",
            )
    require(actual_owned == owned | {path}, "Complete exact original owned membership")
    if (receipt / "summary.json").is_file():
        summary = read_json(receipt / "summary.json", started)
        require(
            summary.get("passed") is True and not summary.get("budget_censored", False),
            "Actual successful original scoped prerequisite",
        )
    no_failure(receipt)
    return records


def selected_inputs(policy, frozen, external, started):
    bind(frozen, external, METHOD, METHOD_SHA, started)
    bind(frozen, external, METHOD_DOC, METHOD_DOC_SHA, started)
    method = read_json(METHOD, started)
    require(method["schema"] == "a13-exp-frontier-author-preflight-v1", "Exact held A13 method")
    pins = method["selected_existing_manifest_expected_pins"]
    owners = {key: expected for key, expected in pins.items() if key.endswith("/manifest.json")}
    owners["results/limitation_program_20261001/A07_run003/manifest.json"] = A07_SHA
    records = []
    for key, expected in owners.items():
        check(started)
        records.extend(freeze_owner(ROOT / key, expected, frozen, external, started))
    for key, expected in pins.items():
        check(started)
        actual = bind(frozen, external, ROOT / key, expected, started)
        if not key.endswith("/manifest.json"):
            actual_key = actual.relative_to(ROOT).as_posix()
            require(
                any(
                    row["verified_input_path"] == actual_key
                    and row["original_expected_sha256"] == expected
                    for row in records
                ),
                "Exact original equal-SHA selected membership",
            )
    for name, expected in method["A07_domain_interface"][
        "selected_existing_bounds_expected_pins"
    ].items():
        bind(frozen, external, PROGRAM / "A07_run003" / name, expected, started)
    for path in (
        AUTHOR,
        PRODUCER_AUTHOR,
        IMPLEMENTATION,
        IMPLEMENTATION_DOC,
        RECOVERY_METHOD,
        RECOVERY_METHOD_DOC,
    ):
        bind(frozen, external, path, sha(path, started), started)
    return method, records


def prior_recovery_audit_provenance(policy, frozen, external, started):
    """Bind the real prior sealed audit failure and static release without result credit."""
    records = []
    for name, expected in ORIGINAL_RECOVERY_AUTHOR_SHA256.items():
        check(started)
        bind(frozen, external, RESEARCH / name, expected, started)
    for receipt, pin, counts in (
        (PRIOR_RECOVERY_AUDIT, PRIOR_RECOVERY_AUDIT_SHA, (19, 931, 2842)),
        (PRIOR_RECOVERY_REVIEW, PRIOR_RECOVERY_REVIEW_SHA, (1, 17, 0)),
    ):
        path = bind(frozen, external, receipt / "manifest.json", pin, started)
        manifest = read_json(path, started)
        require(
            manifest.get("manifest_self_hash_excluded") is True,
            "Prior terminal self-hash exclusion",
        )
        require(
            tuple(
                len(manifest.get(field, {}))
                for field in ("files", "frozen_inputs", "external_runtime_inputs")
            )
            == counts,
            "Complete real prior recovery maps",
        )
        owned = set()
        for field in ("files", "frozen_inputs", "external_runtime_inputs"):
            mapping = manifest.get(field, {})
            require(type(mapping) is dict, "Prior recognized map type")
            for key, expected in mapping.items():
                check(started)
                require(
                    type(key) is str and type(expected) is str and SHA_PATTERN.fullmatch(expected),
                    "Typed prior exact SHA reference",
                )
                if field == "external_runtime_inputs":
                    candidate = Path(key)
                    require(candidate.is_absolute(), "Prior exact absolute external runtime path")
                else:
                    require(
                        not Path(key).is_absolute()
                        and not Path(key).drive
                        and "\\" not in key
                        and ".." not in key.split("/"),
                        "Prior canonical ROOT or receipt-relative key",
                    )
                    candidate = (
                        ROOT / key
                        if field == "frozen_inputs" or key.startswith("results/")
                        else receipt / key
                    )
                actual = bind(frozen, external, candidate, expected, started)
                if field == "files":
                    require(
                        lexically_under(actual, receipt) and actual != path and actual not in owned,
                        "Prior exact own confinement",
                    )
                    owned.add(actual)
                    canonical = (
                        actual.relative_to(ROOT).as_posix()
                        if key.startswith("results/")
                        else actual.relative_to(receipt).as_posix()
                    )
                    require(canonical == key, "Prior exact own spelling")
                elif field == "frozen_inputs":
                    require(
                        lexically_under(actual, ROOT)
                        and actual.relative_to(ROOT).as_posix() == key,
                        "Prior direct active ROOT expectation",
                    )
                else:
                    require(
                        not lexically_under(actual, ROOT) and str(actual) == key,
                        "Prior direct exact external expectation",
                    )
                records.append(
                    dict(
                        owner_manifest=path.relative_to(ROOT).as_posix(),
                        source_map=field,
                        original_key=key,
                        verified_input_path=actual.relative_to(ROOT).as_posix()
                        if lexically_under(actual, ROOT)
                        else str(actual),
                        original_expected_sha256=expected,
                        expected_hash_waived=False,
                    )
                )
                check(started)
        found = set()
        for candidate in receipt.rglob("*"):
            check(started)
            if candidate.is_file():
                actual = canonical_path(candidate, started)
                require(
                    lexically_under(actual, receipt) and actual not in found,
                    "Prior actual own noalias membership",
                )
                found.add(actual)
        require(found == owned | {path}, "Prior exact complete owned inventory")
        records.append(
            dict(
                owner_manifest=path.relative_to(ROOT).as_posix(),
                source_map="manifest",
                original_key=path.relative_to(ROOT).as_posix(),
                verified_input_path=path.relative_to(ROOT).as_posix(),
                original_expected_sha256=pin,
                expected_hash_waived=False,
            )
        )
    manifest = read_json(PRIOR_RECOVERY_AUDIT / "manifest.json", started)
    outcome = read_json(PRIOR_RECOVERY_AUDIT / "completion_outcome.json", started)
    failure = read_json(PRIOR_RECOVERY_AUDIT / "failure.json", started)
    require(
        manifest["schema"] == "a13-exp-frontier-recovery-independent-audit-manifest-v1"
        and manifest["completed"] is False
        and manifest["passed"] is False
        and manifest["budget_censored"] is False,
        "Original sealed uncensored metadata-access audit failure only",
    )
    require(
        outcome["completed"] is False
        and outcome["passed"] is False
        and outcome["failed"] is True
        and outcome["budget_censored"] is False
        and outcome["new_test_credit"] == 0
        and outcome["full_G2"] is False
        and outcome["adoption"] is False
        and outcome["cost_transfer"] is False
        and failure["error_type"] == "KeyError"
        and failure["error"] == "'spec'"
        and failure["new_test_credit"] == 0
        and 'entry["spec"]["width"]' in failure["traceback"],
        "Preserve exact original optional-spec failure with zero scientific credit",
    )
    require(
        not (PRIOR_RECOVERY_AUDIT / "summary.json").exists()
        and not (PRIOR_RECOVERY_AUDIT / "fixed_inventory_authorization.json").exists()
        and not (PRIOR_RECOVERY_AUDIT / "FAILED_UNSEALED.json").exists(),
        "No prior scientific PASS or unsealed substitute",
    )
    same(outcome["limits_CPU_admission_wall"], [CPU, ADMISSION, WALL], "Original identical limits")
    for observation in (outcome["budget"], manifest["terminal_budget_observation"]):
        require(
            0 <= observation["process_CPU_seconds"] < CPU
            and 0 <= observation["wall_seconds"] < WALL,
            "Original uncensored failure terminal budget",
        )
    review = read_json(PRIOR_RECOVERY_REVIEW / "summary.json", started)
    require(
        review["schema"] == "root-a13-exp-frontier-recovery-static-READY-v1"
        and review["passed"] is True
        and review["ready"] is True
        and review["root_and_independent_TEXT_static_reviews"] is True
        and review["source_metadata_integrity_only"] is True
        and review["candidate_material_untrusted_until_independent130_all20_validation"] is True
        and review["refit_authorized"] is False
        and review["new_fixture_credit"] == 0,
        "Prior root READY is static only and never validates failed scientific material",
    )
    return dict(
        records=records,
        previous_failed_recovery_audit_credit=0,
        original_recovery_source_manifest_SHA256=ORIGINAL_RECOVERY_SOURCE_SHA,
        original_recovery_audit_failed_manifest_SHA256=PRIOR_RECOVERY_AUDIT_SHA,
    )


def prior_recovery_audit_v2_provenance(policy, frozen, external, started):
    """Bind every actual v2 failure/release byte without promoting partial mathematics."""
    records = []
    for name, expected in PRIOR_RECOVERY_AUDIT_V2_AUTHOR_SHA256.items():
        check(started)
        bind(frozen, external, RESEARCH / name, expected, started)
    for receipt, pin, counts in (
        (PRIOR_RECOVERY_AUDIT_V2, PRIOR_RECOVERY_AUDIT_V2_SHA, (20, 957, 2842)),
        (PRIOR_RECOVERY_V2_REVIEW, PRIOR_RECOVERY_V2_REVIEW_SHA, (1, 23, 0)),
    ):
        path = bind(frozen, external, receipt / "manifest.json", pin, started)
        manifest = read_json(path, started)
        require(
            manifest.get("manifest_self_hash_excluded") is True,
            "Prior v2 terminal self-hash exclusion",
        )
        require(
            tuple(
                len(manifest.get(field, {}))
                for field in ("files", "frozen_inputs", "external_runtime_inputs")
            )
            == counts,
            "Complete actual prior audit-only v2 maps",
        )
        owned = set()
        for field in ("files", "frozen_inputs", "external_runtime_inputs"):
            mapping = manifest.get(field, {})
            require(type(mapping) is dict, "Prior v2 recognized map type")
            for key, expected in mapping.items():
                check(started)
                require(
                    type(key) is str and type(expected) is str and SHA_PATTERN.fullmatch(expected),
                    "Typed prior v2 exact SHA reference",
                )
                if field == "external_runtime_inputs":
                    candidate = Path(key)
                    require(candidate.is_absolute(), "Prior v2 exact absolute external path")
                else:
                    require(
                        not Path(key).is_absolute()
                        and not Path(key).drive
                        and "\\" not in key
                        and ".." not in key.split("/"),
                        "Prior v2 canonical ROOT or receipt-relative key",
                    )
                    candidate = (
                        ROOT / key
                        if field == "frozen_inputs" or key.startswith("results/")
                        else receipt / key
                    )
                actual = bind(frozen, external, candidate, expected, started)
                if field == "files":
                    require(
                        lexically_under(actual, receipt) and actual != path and actual not in owned,
                        "Prior v2 exact own confinement",
                    )
                    owned.add(actual)
                    canonical = (
                        actual.relative_to(ROOT).as_posix()
                        if key.startswith("results/")
                        else actual.relative_to(receipt).as_posix()
                    )
                    require(canonical == key, "Prior v2 exact own spelling")
                elif field == "frozen_inputs":
                    require(
                        lexically_under(actual, ROOT)
                        and actual.relative_to(ROOT).as_posix() == key,
                        "Prior v2 direct active ROOT expectation",
                    )
                else:
                    require(
                        not lexically_under(actual, ROOT) and str(actual) == key,
                        "Prior v2 direct exact external expectation",
                    )
                records.append(
                    dict(
                        owner_manifest=path.relative_to(ROOT).as_posix(),
                        source_map=field,
                        original_key=key,
                        verified_input_path=actual.relative_to(ROOT).as_posix()
                        if lexically_under(actual, ROOT)
                        else str(actual),
                        original_expected_sha256=expected,
                        expected_hash_waived=False,
                    )
                )
                check(started)
        found = set()
        for candidate in receipt.rglob("*"):
            check(started)
            if candidate.is_file():
                actual = canonical_path(candidate, started)
                require(
                    lexically_under(actual, receipt) and actual not in found,
                    "Prior v2 actual own noalias membership",
                )
                found.add(actual)
        require(found == owned | {path}, "Prior v2 exact complete owned inventory")
        records.append(
            dict(
                owner_manifest=path.relative_to(ROOT).as_posix(),
                source_map="manifest",
                original_key=path.relative_to(ROOT).as_posix(),
                verified_input_path=path.relative_to(ROOT).as_posix(),
                original_expected_sha256=pin,
                expected_hash_waived=False,
            )
        )
    manifest = read_json(PRIOR_RECOVERY_AUDIT_V2 / "manifest.json", started)
    outcome = read_json(PRIOR_RECOVERY_AUDIT_V2 / "completion_outcome.json", started)
    failure = read_json(PRIOR_RECOVERY_AUDIT_V2 / "failure.json", started)
    require(
        manifest["schema"] == "a13-exp-frontier-recovery-independent-audit-manifest-v1"
        and manifest["completed"] is False
        and manifest["passed"] is False
        and manifest["budget_censored"] is False,
        "Actual sealed uncensored v2 resource-schema failure only",
    )
    require(
        outcome["completed"] is False
        and outcome["passed"] is False
        and outcome["failed"] is True
        and outcome["budget_censored"] is False
        and outcome["new_test_credit"] == 0
        and outcome["full_G2"] is False
        and outcome["adoption"] is False
        and outcome["cost_transfer"] is False
        and failure["error_type"] == "ValueError"
        and failure["error"]
        == "Every selector/table/copy/bank/cleanup and whole-source resource term"
        and failure["new_test_credit"] == 0
        and "audit_rows" in failure["traceback"],
        "Preserve exact v2 resource-key failure with zero scientific credit",
    )
    require(
        not (PRIOR_RECOVERY_AUDIT_V2 / "summary.json").exists()
        and not (PRIOR_RECOVERY_AUDIT_V2 / "fixed_inventory_authorization.json").exists()
        and not (PRIOR_RECOVERY_AUDIT_V2 / "FAILED_UNSEALED.json").exists(),
        "No prior v2 mathematical PASS or unsealed substitute",
    )
    same(outcome["limits_CPU_admission_wall"], [CPU, ADMISSION, WALL], "Same v2 fixed limits")
    for observation in (outcome["budget"], manifest["terminal_budget_observation"]):
        require(
            0 <= observation["process_CPU_seconds"] < CPU
            and 0 <= observation["wall_seconds"] < WALL,
            "Actual uncensored v2 terminal budget",
        )
    review = read_json(PRIOR_RECOVERY_V2_REVIEW / "summary.json", started)
    require(
        review["schema"] == "root-a13-exp-frontier-recovery-audit-only-static-READY-v2"
        and review["passed"] is True
        and review["ready"] is True
        and review["root_and_two_independent_TEXT_static_reviews"] is True
        and review["actual_new_trio_pins_PASS"] is True
        and review["original_source_metadata_only"] is True
        and review["original_source_reexecuted"] is False
        and review["all20_independent130_required"] is True
        and review["refit_authorized"] is False
        and review["new_fixture_credit"] == 0,
        "Prior v2 root READY is static only and never approves failed mathematics",
    )
    return dict(
        records=records,
        previous_failed_recovery_audit_v2_credit=0,
        original_recovery_source_manifest_SHA256=ORIGINAL_RECOVERY_SOURCE_SHA,
        prior_recovery_audit_v2_failed_manifest_SHA256=PRIOR_RECOVERY_AUDIT_V2_SHA,
        cost_formula_or_value_expression_changed=False,
        canonical_resource_key_serialization_only=True,
    )


def prior_recovery_audit_v3_provenance(policy, frozen, external, started):
    """Bind the complete censored V3 packet; its fourteen rows confer no approval."""
    records = []
    for name, expected in PRIOR_RECOVERY_AUDIT_V3_AUTHOR_SHA256.items():
        check(started)
        bind(frozen, external, RESEARCH / name, expected, started)
    for receipt, pin, counts in (
        (PRIOR_RECOVERY_AUDIT_V3, PRIOR_RECOVERY_AUDIT_V3_SHA, (35, 984, 2842)),
        (PRIOR_RECOVERY_V3_REVIEW, PRIOR_RECOVERY_V3_REVIEW_SHA, (1, 28, 0)),
    ):
        path = bind(frozen, external, receipt / "manifest.json", pin, started)
        manifest = read_json(path, started)
        require(
            manifest.get("manifest_self_hash_excluded") is True,
            "Prior V3 terminal self-hash exclusion",
        )
        require(
            tuple(
                len(manifest.get(field, {}))
                for field in ("files", "frozen_inputs", "external_runtime_inputs")
            )
            == counts,
            "Complete actual prior V3 failed audit and static-review maps",
        )
        owned = set()
        for field in ("files", "frozen_inputs", "external_runtime_inputs"):
            mapping = manifest.get(field, {})
            require(type(mapping) is dict, "Prior V3 recognized map type")
            for key, expected in mapping.items():
                check(started)
                require(
                    type(key) is str and type(expected) is str and SHA_PATTERN.fullmatch(expected),
                    "Typed prior V3 exact SHA reference",
                )
                if field == "external_runtime_inputs":
                    candidate = Path(key)
                    require(candidate.is_absolute(), "Prior V3 exact absolute external path")
                else:
                    require(
                        not Path(key).is_absolute()
                        and not Path(key).drive
                        and "\\" not in key
                        and ".." not in key.split("/"),
                        "Prior V3 canonical ROOT or receipt-relative key",
                    )
                    candidate = (
                        ROOT / key
                        if field == "frozen_inputs" or key.startswith("results/")
                        else receipt / key
                    )
                actual = bind(frozen, external, candidate, expected, started)
                if field == "files":
                    require(
                        lexically_under(actual, receipt) and actual != path and actual not in owned,
                        "Prior V3 exact own confinement",
                    )
                    owned.add(actual)
                    spelling = (
                        actual.relative_to(ROOT).as_posix()
                        if key.startswith("results/")
                        else actual.relative_to(receipt).as_posix()
                    )
                    require(spelling == key, "Prior V3 exact own spelling")
                elif field == "frozen_inputs":
                    require(
                        lexically_under(actual, ROOT)
                        and actual.relative_to(ROOT).as_posix() == key,
                        "Prior V3 direct active ROOT expectation",
                    )
                else:
                    require(
                        not lexically_under(actual, ROOT) and str(actual) == key,
                        "Prior V3 direct exact external expectation",
                    )
                records.append(
                    dict(
                        owner_manifest=path.relative_to(ROOT).as_posix(),
                        source_map=field,
                        original_key=key,
                        verified_input_path=actual.relative_to(ROOT).as_posix()
                        if lexically_under(actual, ROOT)
                        else str(actual),
                        original_expected_sha256=expected,
                        expected_hash_waived=False,
                    )
                )
                check(started)
        found = set()
        for candidate in receipt.rglob("*"):
            check(started)
            if candidate.is_file():
                actual = canonical_path(candidate, started)
                require(
                    lexically_under(actual, receipt) and actual not in found,
                    "Prior V3 actual own noalias membership",
                )
                found.add(actual)
        require(found == owned | {path}, "Prior V3 exact complete owned inventory")
        if receipt == PRIOR_RECOVERY_AUDIT_V3:
            same(
                sorted(
                    actual.relative_to(receipt).as_posix()
                    for actual in owned
                    if lexically_under(actual, receipt / "rows")
                ),
                sorted(f"rows/d{degree}_s{count}.json.gz" for degree, count in GRID[:14]),
                "Exactly fourteen censored proof rows retained as failure provenance only",
            )
        records.append(
            dict(
                owner_manifest=path.relative_to(ROOT).as_posix(),
                source_map="manifest",
                original_key=path.relative_to(ROOT).as_posix(),
                verified_input_path=path.relative_to(ROOT).as_posix(),
                original_expected_sha256=pin,
                expected_hash_waived=False,
            )
        )
    manifest = read_json(PRIOR_RECOVERY_AUDIT_V3 / "manifest.json", started)
    outcome = read_json(PRIOR_RECOVERY_AUDIT_V3 / "completion_outcome.json", started)
    failure = read_json(PRIOR_RECOVERY_AUDIT_V3 / "failure.json", started)
    require(
        manifest["schema"] == "a13-exp-frontier-recovery-independent-audit-manifest-v1"
        and manifest["completed"] is False
        and manifest["passed"] is False
        and manifest["budget_censored"] is True,
        "Actual sealed budget-censored V3 attempt remains failed",
    )
    require(
        outcome["completed"] is False
        and outcome["passed"] is False
        and outcome["failed"] is True
        and outcome["budget_censored"] is True
        and outcome["new_test_credit"] == 0
        and outcome["full_G2"] is False
        and outcome["adoption"] is False
        and outcome["cost_transfer"] is False
        and failure["error_type"] == "BudgetCensoredError"
        and failure["error"] == "Fixed independent A13 CPU/wall censor"
        and failure["new_test_credit"] == 0
        and "audit_fit_segment" in failure["traceback"],
        "Preserve exact V3 admission censor with zero scientific credit",
    )
    require(
        not any(
            (PRIOR_RECOVERY_AUDIT_V3 / name).exists()
            for name in (
                "summary.json",
                "fixed_inventory_authorization.json",
                "FAILED_UNSEALED.json",
            )
        ),
        "No prior V3 all20 PASS, index or unsealed substitute",
    )
    same(outcome["limits_CPU_admission_wall"], [CPU, ADMISSION, WALL], "Same V3 fixed limits")
    require(
        ADMISSION <= failure["budget"]["process_CPU_seconds"] < CPU
        and 0 <= failure["budget"]["wall_seconds"] < WALL,
        "Actual V3 work-admission CPU refusal below the unchanged hard limit",
    )
    for observation in (outcome["budget"], manifest["terminal_budget_observation"]):
        require(
            failure["budget"]["process_CPU_seconds"] <= observation["process_CPU_seconds"] < CPU
            and failure["budget"]["wall_seconds"] <= observation["wall_seconds"] < WALL,
            "Actual failed V3 terminal retention below the hard limits",
        )
    review = read_json(PRIOR_RECOVERY_V3_REVIEW / "summary.json", started)
    require(
        review["schema"] == "root-a13-exp-frontier-recovery-audit-only-static-READY-v3"
        and review["passed"] is True
        and review["ready"] is True
        and review["root_and_two_independent_TEXT_static_reviews"] is True
        and review["actual_new_trio_pins_PASS"] is True
        and review["original_source_metadata_only"] is True
        and review["original_source_reexecuted"] is False
        and review["all20_independent130_required"] is True
        and review["refit_authorized"] is False
        and review["new_fixture_credit"] == 0,
        "Prior V3 READY is static and never approves failed mathematics",
    )
    return dict(
        records=records,
        previous_failed_recovery_audit_v3_credit=0,
        original_recovery_source_manifest_SHA256=ORIGINAL_RECOVERY_SOURCE_SHA,
        prior_recovery_audit_v3_failed_manifest_SHA256=PRIOR_RECOVERY_AUDIT_V3_SHA,
        preserved_censored_gzip_rows=14,
        preserved_partial_rows_reused_as_authorizations=False,
        fresh_all20_authorizations_required=True,
        new_scientific_budget_raised=False,
    )


def bernstein_v5_prerequisites(policy, frozen, external, started):
    """Verify full failed V4, static review, profile and actual finite-QA maps."""
    records = []
    for pins in (PRIOR_RECOVERY_AUDIT_V4_AUTHOR_SHA256, BERNSTEIN_AUTHOR_SHA256):
        for name, expected in pins.items():
            check(started)
            bind(frozen, external, RESEARCH / name, expected, started)
    packets = (
        (PRIOR_RECOVERY_AUDIT_V4, PRIOR_RECOVERY_AUDIT_V4_SHA, (38, 1030, 2842)),
        (PRIOR_RECOVERY_V4_REVIEW, PRIOR_RECOVERY_V4_REVIEW_SHA, (1, 37, 0)),
        (PRIOR_PROFILE, PRIOR_PROFILE_SHA, (11, 1064, 2842)),
        (BERNSTEIN_QA, BERNSTEIN_QA_SHA, (2, 6, 0)),
    )
    manifests = {}
    for receipt, pin, counts in packets:
        path = bind(frozen, external, receipt / "manifest.json", pin, started)
        manifest = read_json(path, started)
        require(manifest.get("manifest_self_hash_excluded") is True, "V5 prior self-hash exclusion")
        require(
            tuple(
                len(manifest.get(field, {}))
                for field in ("files", "frozen_inputs", "external_runtime_inputs")
            )
            == counts,
            "Complete original V5 prerequisite maps, without truncation",
        )
        owned = set()
        for field in ("files", "frozen_inputs", "external_runtime_inputs"):
            mapping = manifest.get(field, {})
            require(type(mapping) is dict, "Typed complete prerequisite map")
            for key, expected in mapping.items():
                check(started)
                require(
                    type(key) is str and type(expected) is str and SHA_PATTERN.fullmatch(expected),
                    "Typed immutable prior expected SHA",
                )
                if field == "external_runtime_inputs":
                    candidate = Path(key)
                    require(candidate.is_absolute(), "Exact prior absolute external path")
                else:
                    require(
                        not Path(key).is_absolute()
                        and not Path(key).drive
                        and "\\" not in key
                        and ".." not in key.split("/"),
                        "Canonical prior ROOT/receipt spelling",
                    )
                    candidate = (
                        ROOT / key
                        if field == "frozen_inputs" or key.startswith("results/")
                        else receipt / key
                    )
                actual = bind(frozen, external, candidate, expected, started)
                if field == "files":
                    require(
                        lexically_under(actual, receipt) and actual != path and actual not in owned,
                        "Exact prior owned confinement and uniqueness",
                    )
                    owned.add(actual)
                    spelling = (
                        actual.relative_to(ROOT).as_posix()
                        if key.startswith("results/")
                        else actual.relative_to(receipt).as_posix()
                    )
                    require(spelling == key, "Exact canonical own spelling")
                elif field == "frozen_inputs":
                    require(
                        lexically_under(actual, ROOT)
                        and actual.relative_to(ROOT).as_posix() == key,
                        "Direct prior canonical ROOT expectation",
                    )
                else:
                    require(
                        not lexically_under(actual, ROOT) and str(actual) == key,
                        "Direct prior exact external expectation",
                    )
                records.append(
                    dict(
                        owner_manifest=path.relative_to(ROOT).as_posix(),
                        source_map=field,
                        original_key=key,
                        original_expected_sha256=expected,
                        verified_input_path=actual.relative_to(ROOT).as_posix()
                        if lexically_under(actual, ROOT)
                        else str(actual),
                        expected_hash_waived=False,
                    )
                )
                check(started)
        found = set()
        for candidate in receipt.rglob("*"):
            check(started)
            if candidate.is_file():
                actual = canonical_path(candidate, started)
                require(
                    lexically_under(actual, receipt) and actual not in found,
                    "No own aliases or escaping members",
                )
                found.add(actual)
        require(found == owned | {path}, "Complete exact prerequisite owned inventory")
        records.append(
            dict(
                owner_manifest=path.relative_to(ROOT).as_posix(),
                source_map="manifest",
                original_key=path.relative_to(ROOT).as_posix(),
                verified_input_path=path.relative_to(ROOT).as_posix(),
                original_expected_sha256=pin,
                expected_hash_waived=False,
            )
        )
        manifests[receipt] = manifest
    failed = manifests[PRIOR_RECOVERY_AUDIT_V4]
    outcome = read_json(PRIOR_RECOVERY_AUDIT_V4 / "completion_outcome.json", started)
    failure = read_json(PRIOR_RECOVERY_AUDIT_V4 / "failure.json", started)
    require(
        failed["schema"] == "a13-exp-frontier-recovery-independent-audit-manifest-v1"
        and failed["completed"] is False
        and failed["passed"] is False
        and failed["budget_censored"] is True
        and outcome["completed"] is False
        and outcome["passed"] is False
        and outcome["failed"] is True
        and outcome["budget_censored"] is True
        and outcome["new_test_credit"] == 0
        and outcome["full_G2"] is False
        and outcome["adoption"] is False
        and outcome["cost_transfer"] is False
        and failure["error_type"] == "BudgetCensoredError"
        and failure["error"] == "Fixed independent A13 CPU/wall censor"
        and failure["new_test_credit"] == 0,
        "Sealed censored V4 stays authoritative failed with zero credit",
    )
    same(
        outcome["limits_CPU_admission_wall"],
        [CPU, ADMISSION, WALL],
        "Unchanged V4 scientific limits",
    )
    require(
        ADMISSION <= failure["budget"]["process_CPU_seconds"] < CPU
        and 0 <= failure["budget"]["wall_seconds"] < WALL,
        "Actual V4 admission refusal below hard cap",
    )
    for observation in (outcome["budget"], failed["terminal_budget_observation"]):
        require(
            failure["budget"]["process_CPU_seconds"] <= observation["process_CPU_seconds"] < CPU
            and failure["budget"]["wall_seconds"] <= observation["wall_seconds"] < WALL,
            "Censored V4 terminal retained under original hard cap",
        )
    require(
        not any(
            (PRIOR_RECOVERY_AUDIT_V4 / name).exists()
            for name in (
                "summary.json",
                "fixed_inventory_authorization.json",
                "FAILED_UNSEALED.json",
            )
        ),
        "No V4 all20 PASS or substitute partial authority",
    )
    same(
        sorted(
            path.relative_to(PRIOR_RECOVERY_AUDIT_V4).as_posix()
            for path in PRIOR_RECOVERY_AUDIT_V4.rglob("*.json.gz")
        ),
        sorted(f"rows/d{degree}_s{count}.json.gz" for degree, count in GRID[:14]),
        "Exactly fourteen failed V4 gzip rows, never authorizations",
    )
    review = read_json(PRIOR_RECOVERY_V4_REVIEW / "summary.json", started)
    require(
        review["schema"] == "root-a13-exp-frontier-recovery-audit-only-static-READY-v4"
        and review["passed"] is True
        and review["ready"] is True
        and review["actual_new_release_pins_PASS"] is True
        and review["actual_finite16_equivalence_check_PASS"] is True
        and review["all20_fresh_independent130_required"] is True
        and review["partial_proof_authorization_reused"] is False
        and review["new_fixture_credit"] == 0,
        "Old V4 release is static only",
    )
    no_failure(PRIOR_PROFILE)
    profile = read_json(PRIOR_PROFILE / "summary.json", started)
    profile_outcome = read_json(PRIOR_PROFILE / "completion_outcome.json", started)
    require(
        manifests[PRIOR_PROFILE]["completed"] is True
        and manifests[PRIOR_PROFILE]["passed"] is True
        and manifests[PRIOR_PROFILE]["budget_censored"] is False
        and profile["schema"] == "a13-fixed-architecture-profile-summary-v1"
        and profile["completed"] is True
        and profile["passed"] is True
        and profile["fixed_call_returned"] is True
        and profile["diagnostic_not_independent_scientific_audit"] is True
        and profile["all20_approval"] is False
        and profile["row_approval"] is False
        and profile["new_test_credit"] == 0
        and profile_outcome["completed"] is True
        and profile_outcome["passed"] is True
        and profile_outcome["budget_censored"] is False
        and profile_outcome["prior_failed004_remains_failed"] is True,
        "Actual profile is diagnostic-only, not row approval",
    )
    same(
        profile["fixed_architecture"],
        dict(degree=10, segments=4, row_id="d10_s4"),
        "Original fixed profiled row",
    )
    no_failure(BERNSTEIN_QA)
    qa = read_json(BERNSTEIN_QA / "summary.json", started)
    require(
        manifests[BERNSTEIN_QA]["schema"] == "a13-bernstein-exact-equivalence-manifest-v5"
        and manifests[BERNSTEIN_QA]["completed"] is True
        and manifests[BERNSTEIN_QA]["passed"] is True
        and qa["schema"] == "a13-bernstein-exact-equivalence-summary-v5"
        and qa["completed"] is True
        and qa["passed"] is True
        and qa["budget_censored"] is False
        and qa["fixed_small_oracle_cases"] == 20
        and qa["oracle_sample_points"] == 75
        and qa["oracle_Gaussian_cell_updates"] == 1395
        and qa["complete_exact_coordinates_compared"] == 267
        and qa["empty_degree_minus1_compatibility_passed"] is True
        and qa["matching_rejected_input_cases"] == 3
        and qa["all_small_cases_equal_independent_interpolation_oracle"] is True
        and qa["complete_Taylor_comparisons_are_reference_equivalence_only"] is True
        and qa["auditor_and_kernel_modules_imported"] is False
        and qa["all20_scientific_screen_approved"] is False
        and qa["candidate_G2_established"] is False
        and qa["adoption"] is False
        and qa["new_test_credit"] == qa["new_gate_replays"] == qa["new_price_samples"] == 0
        and qa["new_function_AST_sha256"]
        == "c6676e11751660894db8b2a03e6752d7e5f16b7805dc34adafe338d5f1039bac",
        "Actual full finite-QA PASS; no mathematical screen or timing promotion",
    )
    same(qa["complete_Taylor_degrees"], [79, 111], "Both complete Taylor comparisons")
    same(qa["limits_CPU_work_wall_seconds"], [180, 150, 600], "Fixed QA process limits")
    require(
        0 <= qa["actual_process_CPU_seconds"] < 180
        and 0 <= qa["actual_creation_wall_seconds"] < 600,
        "Actual uncensored QA observation",
    )
    expected_qa_inputs = {
        f"research/limitation_program_20261001/{name}": expected
        for name, expected in BERNSTEIN_AUTHOR_SHA256.items()
    }
    expected_qa_inputs[
        f"research/limitation_program_20261001/{'audit_exp_frontier_recovery_v4.py'}"
    ] = PRIOR_RECOVERY_AUDIT_V4_AUTHOR_SHA256["audit_exp_frontier_recovery_v4.py"]
    expected_qa_inputs[LAUNCHER.relative_to(ROOT).as_posix()] = (
        "41123879d2e991377997acadf5f0cf8f34fa10d86362eded8c69b6041e2893b5"
    )
    same(
        manifests[BERNSTEIN_QA]["frozen_inputs"],
        expected_qa_inputs,
        "Actual complete six QA expected-source bindings",
    )
    ready_path = bind(frozen, external, BERNSTEIN_QA_READY, BERNSTEIN_QA_READY_SHA, started)
    ready = read_json(ready_path, started)
    require(
        ready["schema"] == "ROOT-a13-Bernstein-exact-QA-ready-v5"
        and ready["passed_static_review"] is True
        and ready["fixed_checks"] == 26
        and ready["exact_coordinates"] == 267
        and ready["scientific_candidate_approval"] is False
        and ready["new_test_credit"] == 0,
        "Exact actual finite-QA root static release bytes",
    )
    same(ready["frozen_inputs"], expected_qa_inputs, "READY full source and interpreter pins")
    same(ready["limits_CPU_work_wall_seconds"], [180, 150, 600], "READY fixed QA clocks")
    require(
        ready["fresh_receipt"] == BERNSTEIN_QA.relative_to(ROOT).as_posix(),
        "Exact QA release route",
    )
    return dict(
        records=records,
        prior_failed_recovery_audit_v4_credit=0,
        prior_recovery_audit_v4_failed_manifest_SHA256=PRIOR_RECOVERY_AUDIT_V4_SHA,
        actual_profile_manifest_SHA256=PRIOR_PROFILE_SHA,
        Bernstein_finite_QA_manifest_SHA256=BERNSTEIN_QA_SHA,
        Bernstein_finite_QA_ROOT_READY_SHA256=BERNSTEIN_QA_READY_SHA,
        kernel_source_SHA256=BERNSTEIN_AUTHOR_SHA256[BERNSTEIN_KERNEL.name],
        kernel_loaded_via_AST_only=True,
        old_partial_authorizations_reused=False,
        finite_QA_does_not_approve_all20_or_candidate=True,
    )


def v6_owned_inventory(directory, started):
    """Strict complete inventory; no index or member filtering."""
    found, total = set(), 0
    for candidate in directory.rglob("*"):
        check(started)
        if candidate.is_file():
            actual = canonical_path(candidate, started)
            require(
                lexically_under(actual, directory) and actual not in found,
                "No V6 prerequisite alias or owned escape",
            )
            found.add(actual)
            total += actual.stat().st_size
            require(
                len(found) <= 25000 and total <= 8 * 1024**3,
                "Original finite metadata inventory bounds",
            )
    return found


def v6_metadata_packet(receipt, pin, counts, frozen, external, started):
    path = bind(frozen, external, receipt / "manifest.json", pin, started)
    no_failure(receipt)
    document = read_json(path, started)
    require(
        document.get("manifest_self_hash_excluded") is True
        and document.get("passed") is True
        and document.get("new_test_credit") == 0,
        "Only actual scoped metadata success prerequisites",
    )
    require(
        tuple(
            len(document.get(field, {}))
            for field in ("files", "frozen_inputs", "external_runtime_inputs")
        )
        == counts,
        "Complete V6 metadata prerequisite maps",
    )
    owned, records = {path}, []
    for field in ("files", "frozen_inputs", "external_runtime_inputs"):
        mapping = document.get(field, {})
        require(type(mapping) is dict and (mapping or field != "files"), "Typed complete maps")
        for key, expected in mapping.items():
            check(started)
            require(
                type(key) is str and type(expected) is str and SHA_PATTERN.fullmatch(expected),
                "Exact original metadata key and expected SHA",
            )
            if field == "external_runtime_inputs":
                require(Path(key).is_absolute(), "Exact absolute external runtime key")
                route = Path(key)
            else:
                require(
                    not Path(key).is_absolute()
                    and not Path(key).drive
                    and "\\" not in key
                    and ".." not in key.split("/"),
                    "Canonical original slash-relative spelling",
                )
                route = (
                    ROOT / key
                    if field == "frozen_inputs" or key.startswith("results/")
                    else receipt / key
                )
            actual = bind(frozen, external, route, expected, started)
            if field == "files":
                require(
                    lexically_under(actual, receipt) and actual not in owned,
                    "Exact original owned membership",
                )
                owned.add(actual)
                spelling = actual.relative_to(
                    ROOT if key.startswith("results/") else receipt
                ).as_posix()
                require(spelling == key, "Exact owned spelling without archive substitution")
            elif field == "frozen_inputs":
                require(
                    lexically_under(actual, ROOT) and actual.relative_to(ROOT).as_posix() == key,
                    "Exact direct original ROOT dependency",
                )
            else:
                require(
                    not lexically_under(actual, ROOT) and str(actual) == key,
                    "Exact direct external expectation",
                )
            records.append(
                dict(
                    owner_manifest=path.relative_to(ROOT).as_posix(),
                    source_map=field,
                    original_key=key,
                    verified_input_path=root_key(actual, started)
                    if lexically_under(actual, ROOT)
                    else str(actual),
                    original_expected_sha256=expected,
                    expected_hash_waived=False,
                )
            )
    require(v6_owned_inventory(receipt, started) == owned, "Complete exact metadata inventory")
    _V6_PRIOR_INVENTORIES[receipt] = owned
    return document, records


def v6_metadata_prerequisites(policy, frozen, external, started):
    """No failed witness is read, decompressed, compiled or promoted."""
    same(
        policy["V6_metadata_prerequisite_manifest_SHA256"],
        V6_METADATA_EXPECTED,
        "Externally fixed actual capture, profile and static review",
    )
    documents, records = {}, []
    for receipt, pin, counts in (
        (V5_FAILURE_CAPTURE, V5_FAILURE_CAPTURE_SHA, (7, 1146, 2842)),
        (V5_STATIC_REVIEW, V5_STATIC_REVIEW_SHA, (1, 49, 0)),
        (V2_METADATA_PROFILE, V2_METADATA_PROFILE_SHA, (10, 1157, 2842)),
    ):
        document, entries = v6_metadata_packet(receipt, pin, counts, frozen, external, started)
        documents[receipt], records = document, records + entries
    for pins in (V5_AUTHOR_SHA256, V2_METADATA_AUTHOR_SHA256):
        for name, expected in pins.items():
            bind(frozen, external, RESEARCH / name, expected, started)
    capture = documents[V5_FAILURE_CAPTURE]
    profile = documents[V2_METADATA_PROFILE]
    require(
        capture["schema"] == "a13-audit005-unsealed-failure-metadata-capture-manifest-v1"
        and capture["completed"] is True
        and capture["budget_censored"] is False
        and capture["diagnostic_integrity"] is True
        and capture["scientific_execution"] is False
        and capture["original_attempt_failed"] is True
        and capture["original_attempt_sealed"] is False,
        "Original V5 failure capture stays metadata only",
    )
    require(
        profile["schema"] == "a13-selected-metadata-validation-profile-manifest-v2"
        and profile["completed"] is True
        and profile["budget_censored"] is False
        and profile["scientific_execution"] is False
        and profile["mathematical_result_or_row_approval"] is False
        and profile["all20_approval"] is False
        and profile["cost_transfer"] is False,
        "Actual V2 profile does not approve full scientific audit",
    )
    parity = read_json(V2_METADATA_PROFILE / "lexical_predicate_equivalence.json", started)
    require(
        parity["exact_cases"] == 425
        and len(parity["records"]) == 425
        and all(row["matches"] is True for row in parity["records"])
        and parity["syntax_only_not_physical_alias_check"] is True
        and parity["new_fixture_credit"] == 0,
        "Exact passed425 lexical syntax QA",
    )
    ready_path = bind(frozen, external, V2_METADATA_READY, V2_METADATA_READY_SHA, started)
    ready = read_json(ready_path, started)
    same(
        ready["expected_author_files"],
        {
            (RESEARCH / name).relative_to(ROOT).as_posix(): pin
            for name, pin in V2_METADATA_AUTHOR_SHA256.items()
        },
        "Actual frozen V2 profile trio",
    )
    require(
        ready["schema"] == "root-a13-selected-metadata-profile-READY-v2"
        and ready["static_review_passed"] is True
        and ready["lexical_parity_cases"] == 425
        and ready["science_or_partial_result_approval"] is False,
        "Original metadata-only ROOT release remains scoped",
    )
    summary = read_json(V5_FAILURE_CAPTURE / "summary.json", started)
    members = read_json(V5_FAILURE_CAPTURE / "untrusted_failed_material_index.json", started)
    require(type(members) is dict and len(members) == 50, "All50 original failed-owned bytes")
    found, total = set(), 0
    for key, row in members.items():
        check(started)
        actual = bind(frozen, external, ROOT / key, row["SHA256"], started)
        require(
            lexically_under(actual, V5_FAILED)
            and actual.relative_to(ROOT).as_posix() == key
            and actual not in found
            and row["scientific_claims_trusted"] is False
            and actual.stat().st_size == row["bytes"],
            "Opaque exact captured failed-owned byte",
        )
        found.add(actual)
        total += row["bytes"]
    require(
        v6_owned_inventory(V5_FAILED, started) == found and total == 25959363,
        "Complete original failed50 inventory unchanged",
    )
    _V6_PRIOR_INVENTORIES[V5_FAILED] = found
    rows = {
        path.relative_to(V5_FAILED).as_posix()
        for path in found
        if path.parent == V5_FAILED / "rows"
    }
    require(
        rows == {f"rows/d{d}_s{s}.json.gz" for d, s in GRID[:18]}, "Only18 opaque partial witnesses"
    )
    require(
        not any(
            (V5_FAILED / name).exists()
            for name in (
                "summary.json",
                "fixed_inventory_authorization.json",
                "completion_outcome.json",
                "manifest.json",
            )
        ),
        "Original V5 never gains a terminal scientific receipt",
    )
    marker = read_json(V5_FAILED / "FAILED_UNSEALED.json", started)
    failure = read_json(V5_FAILED / "failure.json", started)
    same(marker, summary["original_marker"], "Original authoritative failed marker unchanged")
    same(failure, summary["original_failure_metadata"], "Original recorded censor unchanged")
    require(
        marker["failed"] is True
        and marker["passed"] is False
        and marker["budget_censored"] is None
        and marker["hard_budget_state_uncertified"] is True
        and failure["error_type"] == "BudgetCensoredError"
        and summary["partial_rows_unapproved"] is True,
        "No unsealed V5 failure or18 partial row promotion",
    )
    protocol_path = bind(
        frozen, external, V5_FAILED / "protocol.json", V5_FAILED_PROTOCOL_SHA, started
    )
    protocol = read_json(protocol_path, started)
    require(
        protocol["operational_recovery_audit_version"] == 5
        and protocol["CPU_admission_wall_seconds"] == [CPU, ADMISSION, WALL]
        and protocol["independent_digits"] == DIGITS
        and protocol["primary_digits"] == 90
        and [len(protocol["frozen_inputs"]), len(protocol["external_runtime_inputs"])]
        == [1099, 2842],
        "Original complete prepared science maps and budgets retained",
    )
    for field in ("frozen_inputs", "external_runtime_inputs"):
        for key, expected in protocol[field].items():
            check(started)
            require(
                capture[field].get(key) == expected, "Every old prepared expectation still strict"
            )
    map_inputs(protocol, frozen, external, started)
    return dict(
        manifest_SHA256=V6_METADATA_EXPECTED,
        original_failed_owned_count=50,
        original_failed_owned_bytes=total,
        original_partial_rows_unapproved=18,
        metadata_profile_does_not_approve_all20=True,
        lexical_parity_cases=425,
        records=records,
        new_fixture_credit=0,
        new_gate_replays=0,
        membership_index_introduced=False,
        expected_hashes_waived=False,
    )


def v6_root_release(expected, frozen, external, started):
    path = bind(frozen, external, V6_READY, expected, started)
    ready = read_json(path, started)
    require(
        ready["schema"] == "root-a13-recovery-audit-READY-v6"
        and ready["ready"] is True
        and ready["root_and_independent_static_reviews_passed"] is True
        and ready["output"] == OUTPUT.relative_to(ROOT).as_posix()
        and ready["CPU_admission_wall_seconds"] == [CPU, ADMISSION, WALL]
        and ready["new_fixture_credit"] == 0
        and ready["gate_emission_authorized"] is False,
        "Separate externally issued V6 review and release required",
    )
    pins = ready["author_method_SHA256"]
    require(
        type(pins) is dict
        and set(pins) == {AUTHOR.name, IMPLEMENTATION.name, IMPLEMENTATION_DOC.name},
        "Exactly new V6 author and method trio",
    )
    for name, pin in pins.items():
        bind(frozen, external, RESEARCH / name, pin, started)
    same(
        ready["V6_metadata_prerequisite_manifest_SHA256"],
        V6_METADATA_EXPECTED,
        "ROOT releases only the fixed scope-limited prerequisite set",
    )
    cache = Path(cache_from_source(str(AUTHOR)))
    key = cache.relative_to(ROOT).as_posix()
    present = {key} if cache.exists() else set()
    require(
        set(ready["existing_new_code_cache_SHA256"]) == present
        and ready["absent_new_code_cache_paths"] == sorted({key} - present),
        "Exact external new-code cache presence/absence",
    )
    if present:
        bind(frozen, external, cache, ready["existing_new_code_cache_SHA256"][key], started)
    else:
        require(not cache.is_symlink(), "No absent cache dangling alias")
        _V6_ABSENT_CODE_CACHES.add(cache)
    return expected


def v6_terminal_metadata_inventory(started):
    for directory, members in _V6_PRIOR_INVENTORIES.items():
        check(started)
        require(
            v6_owned_inventory(directory, started) == members,
            "All complete V6 metadata and opaque failed inventories unchanged",
        )
        if directory != V5_FAILED:
            no_failure(directory)
    require(
        not any(path.exists() or path.is_symlink() for path in _V6_ABSENT_CODE_CACHES),
        "Externally declared absent V6 cache remains absent",
    )


def source_packet(policy, frozen, external, started):
    """Admit metadata integrity only; old mathematical material remains untrusted."""
    prior = prior_a13_provenance(policy, frozen, external, started)
    prior_recovery = prior_recovery_audit_provenance(policy, frozen, external, started)
    prior_recovery_v2 = prior_recovery_audit_v2_provenance(policy, frozen, external, started)
    prior_recovery_v3 = prior_recovery_audit_v3_provenance(policy, frozen, external, started)
    bernstein_v5 = bernstein_v5_prerequisites(policy, frozen, external, started)
    metadata_v6 = v6_metadata_prerequisites(policy, frozen, external, started)
    for name, expected in policy["exact_DP_optimization_method_document_SHA256"].items():
        check(started)
        bind(frozen, external, RESEARCH / name, expected, started)
    method, origins = selected_inputs(policy, frozen, external, started)
    capture_path = CAPTURE / "manifest.json"
    capture_pin = policy["capture_manifest_SHA256"]
    freeze_owner(capture_path, capture_pin, frozen, external, started)
    capture = read_json(capture_path, started)
    require(len(capture["files"]) == 3, "Exactly three integrity-only capture outputs")
    diagnostic = read_json(CAPTURE / "summary.json", started)
    require(
        diagnostic["schema"] == "failed-a13-metadata-capture-v1"
        and diagnostic["passed"] is True
        and diagnostic["diagnostic_integrity"] is True
        and diagnostic["original_attempt_failed"] is True
        and diagnostic["original_partial_success_invalid"] is True
        and diagnostic["new_fixture_credit"] == diagnostic["new_gate_replays"] == 0
        and diagnostic["mathematical_result_or_candidate_adoption_claim"] is False
        and diagnostic["scientific_import_or_evaluation_executed"] is False,
        "Root capture certifies only byte integrity, not original science",
    )
    require(not (MATERIAL / "manifest.json").exists(), "Original terminal manifest never existed")
    marker = read_json(MATERIAL / "FAILED_UNSEALED.json", started)
    same(marker, diagnostic["original_failure_marker"], "Original authoritative failure unchanged")
    require(
        marker["failed"] is True
        and marker["completed"] is False
        and marker["passed"] is False
        and marker["partial_summary_or_manifest_is_not_terminal_success"] is True
        and marker["new_test_credit"] == 0,
        "No promotion of any original partial success",
    )
    require(not (PROGRAM / "A13_audit_run002").exists(), "Old independent audit never executed")
    index = read_json(CAPTURE / "frozen_reference_index.json", started)
    require(type(index) is dict and len(index) == 42, "All42 original material files")
    total, members = 0, set()
    for key, expected in index.items():
        check(started)
        actual = bind(frozen, external, ROOT / key, expected, started)
        require(
            lexically_under(actual, MATERIAL) and actual.relative_to(ROOT).as_posix() == key,
            "Exact original material ROOT path",
        )
        require(
            capture["frozen_inputs"][key] == expected and actual not in members,
            "Every original file is an exact captured reference",
        )
        members.add(actual)
        total += actual.stat().st_size
    found = set()
    for item in MATERIAL.rglob("*"):
        check(started)
        if item.is_file():
            actual = canonical_path(item, started)
            require(
                lexically_under(actual, MATERIAL) and actual not in found,
                "Material noalias confinement",
            )
            found.add(actual)
    require(
        found == members
        and total == diagnostic["original_owned_bytes"]
        and diagnostic["original_owned_files"] == 42,
        "Original complete owned inventory unchanged",
    )
    for name, expected in PRIOR_V2_SHA256.items():
        bind(frozen, external, RESEARCH / name, expected, started)
        require(
            index[(MATERIAL / "executed_code" / name).relative_to(ROOT).as_posix()] == expected,
            "All frozen v2 author originals and executed copies",
        )
    original_protocol = read_json(MATERIAL / "protocol.json", started)
    require(
        original_protocol["schema"] == "a13-exp-frontier-protocol-v1"
        and original_protocol["operational_A13_version"] == 2,
        "Exact original v2 prepared protocol",
    )
    same(
        original_protocol["author_sha256"],
        {
            name: PRIOR_V2_SHA256[name]
            for name in ("experiment_exp_frontier_v2.py", "audit_exp_frontier_v2.py")
        },
        "Original actual scientific executable pair",
    )
    same(
        original_protocol["method_document_SHA256"],
        {METHOD.name: METHOD_SHA, METHOD_DOC.name: METHOD_DOC_SHA},
        "Original held mathematical method",
    )
    same(
        original_protocol["CPU_admission_wall_seconds"],
        [CPU, ADMISSION, WALL],
        "Original process budget",
    )
    same(original_protocol["fixed_grid"], [list(value) for value in GRID], "Original all20 grid")
    require(
        original_protocol["primary_digits"] == 90
        and original_protocol["independent_digits"] == DIGITS
        and original_protocol["threads"] == 1
        and original_protocol["new_fixture_credit"] == 0,
        "Original scientific precision and zero fixture credit",
    )
    for field, count in (("frozen_inputs", 848), ("external_runtime_inputs", 2842)):
        original_map = original_protocol[field]
        require(
            type(original_map) is dict and len(original_map) == count,
            "Complete actual original prepared input map",
        )
        for key, expected in original_map.items():
            check(started)
            require(
                capture[field].get(key) == expected,
                "Every original expected hash preserved in capture",
            )
            bind(
                frozen,
                external,
                ROOT / key if field == "frozen_inputs" else Path(key),
                expected,
                started,
            )
    freeze_owner(PRIOR_V2_REVIEW / "manifest.json", PRIOR_V2_REVIEW_SHA, frozen, external, started)
    review_manifest = read_json(PRIOR_V2_REVIEW / "manifest.json", started)
    require(
        len(review_manifest["files"]) == 1
        and len(review_manifest["frozen_inputs"]) == 12
        and not review_manifest.get("external_runtime_inputs", {}),
        "Full original v2 root review maps",
    )
    review = read_json(PRIOR_V2_REVIEW / "summary.json", started)
    require(
        review["schema"] == "root-a13-exp-frontier-static-release-v2"
        and review["passed"] is True
        and review["root_static_review"] is True
        and review["independent_text_peer_review"] is True
        and review["new_scientific_execution_during_review"] is False
        and review["new_fixture_credit"] == 0,
        "Original review is static release only, never science credit",
    )
    no_failure(SOURCE)
    manifest_path = SOURCE / "manifest.json"
    manifest_sha = sha(manifest_path, started)
    require(
        manifest_sha == policy["source_manifest_SHA256"],
        "Exact already successful metadata-only source manifest",
    )
    freeze_owner(manifest_path, manifest_sha, frozen, external, started)
    manifest, outcome, summary, protocol = (
        read_json(SOURCE / name, started)
        for name in ("manifest.json", "completion_outcome.json", "summary.json", "protocol.json")
    )
    require(
        manifest["schema"] == "a13-exp-frontier-recovery-terminal-manifest-v1",
        "Fresh thin metadata packet terminal schema",
    )
    require(
        tuple(
            len(manifest.get(field, {}))
            for field in ("files", "frozen_inputs", "external_runtime_inputs")
        )
        == (16, 909, 2842),
        "Complete original metadata source maps remain exact",
    )
    for value in (manifest, outcome, summary):
        require(
            value["completed"] is True
            and value["passed"] is True
            and value["budget_censored"] is False
            and not value.get("failed", False),
            "Actual uncensored metadata-only completion",
        )
    require(
        summary["schema"] == "a13-exp-frontier-recovery-summary-v1"
        and summary["metadata_integrity"] is True
        and summary["candidate_material_untrusted"] is True
        and summary["independent130_validation_required"] is True
        and summary["scientific_screen_complete"] is False
        and summary["recovered_mathematical_pass_claim"] is False
        and summary["new_test_credit"] == 0
        and summary["full_G2"] is False
        and summary["adoption"] is False
        and summary["cost_transfer"] is False,
        "Metadata PASS never certifies mathematical candidates",
    )
    require(
        protocol["schema"] == "a13-exp-frontier-recovery-protocol-v1"
        and protocol["original_material_receipt"] == MATERIAL.relative_to(ROOT).as_posix()
        and protocol["capture_manifest_SHA256"] == capture_pin,
        "Exact thin recovery provenance protocol",
    )
    same(
        protocol["author_sha256"],
        policy["original_recovery_source_author_sha256"],
        "Original successful metadata source pair is never overwritten by new audit pin",
    )
    same(
        protocol["original_author_sha256"],
        {
            name: PRIOR_V2_SHA256[name]
            for name in ("experiment_exp_frontier_v2.py", "audit_exp_frontier_v2.py")
        },
        "Original material executables unchanged",
    )
    for key in (
        "CPU_admission_wall_seconds",
        "method_document_SHA256",
        "original_method_document_SHA256",
    ):
        same(protocol[key], policy[key], "Prepared recovery contract unchanged")
    same(protocol["fixed_grid"], [list(value) for value in GRID], "All20 fixed choices, no refit")
    inventory = read_json(SOURCE / "material_inventory.json", started)
    require(
        inventory["schema"] == "a13-exp-frontier-untrusted-material-inventory-v1"
        and inventory["material_receipt"] == MATERIAL.relative_to(ROOT).as_posix()
        and inventory["capture_manifest_SHA256"] == capture_pin
        and inventory["original_terminal_failure_authoritative"] is True
        and inventory["original_manifest_absent"] is True
        and inventory["exact_file_count"] == 42
        and inventory["original_file_bytes"] == total
        and inventory["scientific_claims_trusted"] is False
        and inventory["audit_required_all20"] is True,
        "Complete untrusted scientific material inventory",
    )
    require(
        set(inventory["files"]) == {path.relative_to(MATERIAL).as_posix() for path in members},
        "Every original material file referenced exactly once",
    )
    for name, row in inventory["files"].items():
        check(started)
        actual = canonical_path(MATERIAL / name, started)
        key = actual.relative_to(ROOT).as_posix()
        require(
            row["ROOT_relative_path"] == key
            and row["sha256"] == index[key]
            and row["bytes"] == actual.stat().st_size,
            "Exact material reference route/hash/bytes",
        )
    for observation in (
        outcome["budget"],
        manifest["terminal_budget_observation"],
        summary["budget"],
    ):
        require(
            0 <= observation["process_CPU_seconds"] < CPU
            and 0 <= observation["wall_seconds"] < WALL,
            "Thin packet fixed hard limits",
        )
    for name, expected in policy["original_recovery_source_author_sha256"].items():
        require(
            sha(SOURCE / "executed_code" / name, started) == expected,
            "Actual thin executed author copy",
        )
    no_failure(SOURCE)
    return (
        method,
        origins,
        dict(
            manifest_sha256=manifest_sha,
            manifest=manifest,
            outcome=outcome,
            summary=summary,
            protocol=protocol,
            prior_A13_provenance=prior,
            capture_manifest_sha256=capture_pin,
            material_index=index,
            prior_recovery_audit_provenance=prior_recovery,
            prior_recovery_audit_v2_provenance=prior_recovery_v2,
            prior_recovery_audit_v3_provenance=prior_recovery_v3,
            Bernstein_v5_prerequisites=bernstein_v5,
            V6_metadata_prerequisites=metadata_v6,
        ),
    )


def saved_library(source, started):
    route = source["library_workspace_relative"].replace("\\", "/")
    require(".." not in route.split("/"), "No saved library traversal")
    marker = route.lower().find("/results/")
    actual = canonical_path(ROOT / (route[marker + 1 :] if marker >= 0 else route), started)
    require(lexically_under(actual, PROGRAM), "Exact ROOT-owned saved native library")
    return actual


def original_native_metadata(frozen, started):
    cases = {}
    for case in CASES:
        check(started, admission=True)
        route = PROGRAM / "A10_coefficient_run001" / case / "min-depth"
        target, source, schedule = (
            read_json(route / name, started)
            for name in ("target.json", "source.json", "schedule_capped.json")
        )
        require(
            source["word_width"] == W and source["fraction_bits"] == 40, "Full source native ABI"
        )
        require(
            source["exact_clifford_t"] is True and source["arbitrary_rotations"] == 0,
            "Source exact7T applicable macro premise",
        )
        same(
            [schedule["resources"][key] for key in ("t_count", "t_depth", "logical_qubits")],
            list(BASELINE[case]),
            "Original accepted capped resource row",
        )
        require(schedule["qubit_cap"] == BASELINE[case][2], "Same original whole-function cap")
        for name, value in (("target", target), ("source", source)):
            check(started)
            digest = hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()
            require(
                schedule[name + "_fingerprint"] == digest,
                "Actual baseline source/target fingerprint",
            )
        library, leaves = saved_library(source, started), {}
        for key in source["library_keys"]:
            check(started)
            descriptor = library / (key + ".json")
            require(
                root_key(descriptor, started) in frozen,
                "Each actual native descriptor frozen before kernel",
            )
            entry = read_json(descriptor, started)
            require(
                entry["key"] == key
                and entry["resources"]["t_count"] == 7 * entry["resources"]["ccx"],
                "Exact original leaf identity and paid7T count",
            )
            gate = canonical_path(library / entry["gate_file"], started)
            require(
                gate.parent == library
                and root_key(gate, started) in frozen
                and sha(gate, started) == entry["sha256"],
                "Full frozen actual gate bytes without scanning",
            )
            leaves[key] = entry
        actual_nodes = [node for node in target["nodes"] if node["op"] != "input"]
        require(
            len(actual_nodes) == len(source["forward_calls"]),
            "Complete actual forward call catalog",
        )
        for node, call in zip(actual_nodes, source["forward_calls"], strict=True):
            check(started)
            entry = leaves[call["leaf"]]
            same(
                [entry["op"], entry["params"]],
                [node["op"], node["params"]],
                "Same actual leaf parameters",
            )
            same(
                [call["args"], call["out"]],
                [node["args"], node["out"]],
                "Native call operand addresses",
            )
            require(
                call["argument_copy_cx"] == 2 * W * len(node["args"]),
                "Every full72 argument copy in and out",
            )
        interface = read_json(PROGRAM / "A07_run003" / (case + "_bounds.json"), started)
        require(
            interface["target_sha256"] == sha(route / "target.json", started),
            "A07 exact source domain interface",
        )
        for node in target["nodes"]:
            check(started)
            if node["op"] == "input":
                require(node["params"]["bits"] == 32, "Original fullq32 inputs")
                same(
                    interface["intervals"][str(node["out"][0])],
                    [0, N - 1],
                    "Universal A07 input domain",
                )
        cases[case] = dict(
            target=target,
            source=source,
            schedule=schedule,
            leaves=leaves,
            library=library,
            A07=interface,
        )
    return cases


def reconcile_domain(declared, independent, metadata_cases, started):
    require(
        declared["schema"] == "a13-source-domain-binding-v1"
        and declared["fixed30_classes_retained"] is True
        and declared["generic_zero_to_ln2_domain_assumed"] is False
        and declared["source_or_gate_array_executed"] is False,
        "Original source/domain scope",
    )
    require(set(declared["cases"]) == set(CASES), "Both original source contracts")
    hull = independent["cases"]["B4x12"]["whole_integer_remainder_hull"]
    same(declared["common_remainder_raw_hull"], hull, "Fresh complete actual remainder hull")
    for case, (_, _, pairs) in CASES.items():
        check(started)
        own, primary, actual = (
            independent["cases"][case],
            declared["cases"][case],
            metadata_cases[case],
        )
        lo, hi, inverse, logarithm = own["original_native_settings"]
        require(
            declared["inverse_ln2_word"] == inverse and declared["ln2_word"] == logarithm,
            "Same actual signed reduction coefficients",
        )
        same(primary["clipped_log_raw_bounds"], [lo, hi], "Actual signed original clamp domain")
        require(
            primary["actual_stock_sites"] == len(own["actual_stock_sites"])
            and primary["original_joint_pairs"] == pairs,
            "All original stock/pair sites",
        )
        same(
            primary["original_13_coefficients_raw"],
            own["original_literal_exp_coefficients"],
            "Original coefficient baseline only",
        )
        same(
            primary["baseline_capped_resources"],
            actual["schedule"]["resources"],
            "Unchanged actual capped row",
        )
        same(
            primary["baseline_serial_resources"],
            actual["source"]["resources"],
            "Unchanged complete source serial row",
        )
        expected_sites = []
        for stock_site in own["actual_stock_sites"]:
            check(started)
            expected_sites.append(
                dict(
                    stock=stock_site["stock"],
                    clipped=stock_site["clipped"],
                    raw_log=stock_site["raw_log"],
                    polynomial=stock_site["polynomial"],
                    exponent=stock_site["exponent"],
                    remainder=stock_site["remainder"],
                    low=stock_site["lower_raw"],
                    high=stock_site["upper_raw"],
                    inverse_ln2=stock_site["inverse_ln2_raw"],
                    ln2=stock_site["ln2_raw"],
                    values=stock_site["original_native_stock_node_ids"],
                    actual_original_support_signature=stock_site["actual_stock_signature"],
                )
            )
            bound = word_range(actual["A07"]["intervals"][str(stock_site["clipped"])])
            require(
                lo <= bound[0] <= bound[1] <= hi,
                "A07 original clipped domain, no candidate safety transfer",
            )
        same(
            primary["stock_sites"],
            expected_sites,
            "Every original template and exact commutative signature",
        )
        require(
            primary["original_support_signature"]
            == expected_sites[0]["actual_original_support_signature"],
            "Exact E03 signature witness",
        )
        cells = []
        for row in own["original_cells"]:
            check(started)
            item = dict(
                k=row["k"], empty=row["empty"], clipped_log_raw_bounds=row["clipped_raw_interval"]
            )
            if not row["empty"]:
                item["remainder_raw_bounds"] = row["remainder_raw_interval"]
            cells.append(item)
        same(
            primary["reduction_cells"],
            cells,
            "All fixed30 empty and occupied cells independently recovered",
        )
    return dict(
        original_domain_authorized=True,
        original_E03_support_transferred_to_changed_polynomial=False,
        actual_source_calls_or_gate_arrays_executed=False,
        all_original_templates_checked=464,
    )


def primary_plan(ir):
    nodes = []
    for node in ir["nodes"]:
        item = dict(
            value=node["id"], op="local" if node["op"] == "input" else node["op"], args=node["args"]
        )
        if "degree" in node:
            item["degree"] = node["degree"]
        nodes.append(item)
    return dict(
        nodes=nodes,
        output=ir["polynomial_output"],
        odd_term_carried_without_zero_pad=True,
        unused_candidate_power_emitted=False,
    )


def audit_architecture(mp, declared, fit_rows, degree, count, domain, started):
    require(
        declared["degree"] == degree and declared["segments"] == count,
        "Exact fixed architecture identity",
    )
    require(
        declared["no_G2_allocation_or_feasibility_claim"] is True
        and declared["realized_candidate_gate_or_ABI_proof"] is False,
        "Exploratory proof, not emission/adoption",
    )
    partitions = exact_segments(domain["cases"]["B4x12"]["whole_integer_remainder_hull"], count)
    require(
        len(fit_rows) == len(declared["segments_certificate"]) == count,
        "Each declared segment retained",
    )
    words, errors, uniform, diagnostics = [], [], [], []
    for fit, certificate, segment in zip(
        fit_rows, declared["segments_certificate"], partitions, strict=True
    ):
        coefficients, quantized, evidence = audit_fit_segment(fit, degree, segment, started)
        authorized, proofs = audit_segment_certificate(
            mp, certificate, coefficients, quantized, segment, started
        )
        words.append(quantized)
        errors.append(authorized["quantized"])
        uniform.append(dict(segment=segment["index"], **proofs))
        diagnostics.append(dict(segment=segment["index"], **evidence))
    same(
        declared["native_evaluation_plan"],
        primary_plan(estrin_ir(degree, started)),
        "Exact frozen Estrin operation list",
    )
    require(
        set(declared["cases"]) == set(CASES), "Both complete original class/segment inventories"
    )
    own_cases = {}
    for case in CASES:
        check(started, admission=True)
        primary = declared["cases"][case]
        rows = primary["intersections"]
        require(
            len(rows) == 30 * count
            and [(row["k"], row["segment"]) for row in rows]
            == [(k, segment) for k in EXPONENTS for segment in range(count)],
            "Complete fixed row ordering",
        )
        ln_errors = {rational(row["ln2_literal_error_upper"]) for row in rows if not row["empty"]}
        require(len(ln_errors) == 1, "One actual original ln2 literal error envelope")
        own = class_segment_intersections(
            mp, domain["cases"][case], partitions, words, errors, degree, started, ln_errors.pop()
        )
        maximum, maximum_alpha = Fraction(0), Fraction(0)
        for primary_row, fresh in zip(rows, own["classes_segments"], strict=True):
            check(started)
            require(primary_row["empty"] is fresh["empty"], "Exact native empty-cell decision")
            if fresh["empty"]:
                same(
                    primary_row,
                    {key: fresh[key] for key in ("k", "segment", "empty")},
                    "Empty row retained without fictitious bounds",
                )
                continue
            for key in (
                "clipped_log_raw_bounds",
                "remainder_raw_bounds",
                "local_raw_bounds",
                "signed144_products",
                "native_polynomial_raw_bounds",
                "stock_raw_bounds",
            ):
                same(primary_row[key], fresh[key], "Every actual native range/product: " + key)
            expected_ranges = []
            for node in fresh["native_intermediate_ranges"]:
                item = {
                    key: node[key]
                    for key in ("value", "op", "raw_bounds", "native_floor_error_upper")
                }
                if item["op"] == "input":
                    item["op"] = "local"
                expected_ranges.append(item)
            same(
                primary_row["native_intermediate_ranges"],
                expected_ranges,
                "Whole actual stored-word/floor induction",
            )
            for key in (
                "native_floor_error_upper",
                "negative_shift_floor_upper",
                "ln2_literal_error_upper",
            ):
                same(primary_row[key], fresh[key], "Exact charged native term: " + key)
            reduction = rational(primary_row["reduction_stock_error_upper"])
            require(
                reduction >= rational(fresh["reduction_stock_error_upper"]) >= 0,
                "Fresh130 authorizes primary original range-reduction stock error",
            )
            segment = primary_row["segment"]
            final = Fraction(2) ** primary_row["k"] * (
                errors[segment] + rational(primary_row["native_floor_error_upper"])
            )
            final += reduction + rational(primary_row["negative_shift_floor_upper"])
            same(
                primary_row["absolute_stock_error_upper"],
                encode(final),
                "Quantized approximation and every native floor/reduction/shift paid once",
            )
            relative = endpoints(
                mp.iv.exp(
                    outward(
                        mp, abs(primary_row["k"]) * rational(primary_row["ln2_literal_error_upper"])
                    )
                )
                * (
                    1
                    + outward(
                        mp, errors[segment] + rational(primary_row["native_floor_error_upper"])
                    )
                    * mp.iv.exp(outward(mp, Fraction(-primary_row["remainder_raw_bounds"][0], Q)))
                )
                - 1
            )[1]
            claimed_alpha = rational(primary_row["relative_stock_alpha_upper"])
            require(
                claimed_alpha >= relative >= 0,
                "Fresh130 closed-cell relative envelope, no allocation transfer",
            )
            same(
                primary_row["additive_stock_beta_upper"],
                primary_row["negative_shift_floor_upper"],
                "Shift beta kept separate from relative alpha",
            )
            require(
                primary_row["all_native72_product144_and_shift_guards_passed"] is True,
                "Fresh changed native safety required",
            )
            maximum = max(maximum, final)
            maximum_alpha = max(maximum_alpha, claimed_alpha)
        same(
            primary["maximum_absolute_stock_error_upper"],
            encode(maximum),
            "Full original domain maximum, not sampled cells",
        )
        same(
            primary["maximum_relative_stock_alpha_upper"],
            encode(maximum_alpha),
            "Relative alpha maximum over every occupied cell",
        )
        same(
            primary["additive_stock_beta_upper"], encode(EPS), "One original negative-shift epsilon"
        )
        own_cases[case] = dict(
            verified_primary_maximum_absolute_stock_error_upper=encode(maximum),
            verified_primary_maximum_relative_stock_alpha_upper=encode(maximum_alpha),
            independent_class_segment_ranges=own["classes_segments"],
            changed_polynomial_safety_independently_recomputed=True,
        )
    return dict(
        degree=degree,
        segments=count,
        independent_fit_structure=diagnostics,
        uniform_segment_proofs=uniform,
        cases=own_cases,
        no_G2_allocation_or_feasibility_claim=True,
        new_gate_emission_or_replays=0,
    )


def independent_units(entries, compiled_source, started):
    require(
        compiled_source["format"] == "hierarchical-clean-xor-source-v1"
        and compiled_source["word_width"] == W
        and compiled_source["fraction_bits"] == 40,
        "Actual frozen compiled source establishes legacy native word format",
    )
    units = {}
    for operation in ("add", "sub", "mul", "lt"):
        valid = []
        for key in sorted(entries):
            check(started)
            entry = entries[key]
            if entry["op"] != operation or entry["params"] != {}:
                continue
            if "spec" in entry:
                spec = entry["spec"]
                require(type(spec) is dict, "Actual optional native descriptor metadata type")
            else:
                require(
                    operation in ("add", "sub", "lt"), "MUL requires its actual explicit f40 spec"
                )
                spec = {}
            contracts = [entry.get("input_contract"), spec.get("input_contract")]
            if any(value and value != {"signed_operand_bits": [W, W]} for value in contracts):
                continue
            active = spec.get("active_operand_bits")
            if active is not None and active != [W, W]:
                continue
            require(
                len(entry["args"]) == 2
                and all(len(value) == W for value in entry["args"])
                and len(entry["outs"]) == 1
                and len(entry["outs"][0]) == W,
                "Actual generic full72 primitive port contract",
            )
            if "spec" in entry:
                require(
                    spec["width"] == W and spec["fraction_bits"] == 40,
                    "Every present original primitive precision field remains exact",
                )
            if operation == "mul":
                require(
                    spec["product_width"] == W + 40,
                    "Actual full72/f40 multiplier product window112 remains explicit",
                )
            counts = entry["resources"]
            require(
                all(type(counts[field]) is int and counts[field] >= 0 for field in RESOURCE_FIELDS)
                and counts["t_count"] == 7 * counts["ccx"]
                and type(counts["qubits"]) is int
                and counts["qubits"] >= 2 * W + len(entry["outs"][0]),
                "Actual exact7T primitive counts and complete private scratch",
            )
            valid.append((key, counts))
        require(valid, "Source-owned unspecialized dynamic primitive required")
        units[operation] = dict(
            resource_upper={
                field: max(counts[field] for _, counts in valid) for field in RESOURCE_FIELDS
            },
            qubits_upper=max(counts["qubits"] for _, counts in valid),
            actual_leaf_keys=[key for key, _ in valid],
            componentwise_max_is_conservative=True,
        )
    return units


def independent_removal(target, source, sites, started):
    nodes = {node["out"][0]: node for node in target["nodes"]}
    endpoints = {site["polynomial"] for site in sites}
    boundaries = {site["remainder"] for site in sites}
    closure, pending = set(), list(endpoints)
    while pending:
        check(started)
        value = pending.pop()
        if value in boundaries or value in closure:
            continue
        node = nodes[value]
        require(
            node["op"] in ("const", "add", "mul") and len(node["out"]) == 1,
            "Actual original active polynomial closure",
        )
        closure.add(value)
        pending.extend(node["args"])
    replaceable_consumers = {site["stock"] for site in sites}
    retained = set()
    for value, node in nodes.items():
        check(started)
        if value not in closure and value not in replaceable_consumers:
            retained.update(argument for argument in node["args"] if argument in closure)
    changed = True
    while changed:
        check(started)
        changed = False
        for value in tuple(retained):
            for argument in nodes[value]["args"]:
                if argument in closure and argument not in retained:
                    retained.add(argument)
                    changed = True
    removable = closure - retained
    indices = [
        index for index, call in enumerate(source["forward_calls"]) if call["out"][0] in removable
    ]
    require(len(indices) == len(removable), "One actual removable forward call per SSA value")
    return dict(
        active_polynomial_value_ids=sorted(closure),
        retained_shared_or_dead_ancestor_value_ids=sorted(retained),
        removed_value_ids=sorted(removable),
        removed_forward_call_indices=indices,
        eager_unused_values_outside_closure_retained=True,
    )


def independent_resources(degree, count, fit_rows, primary_domain, metadata_cases, started):
    operation_count = Counter(node["op"] for node in estrin_ir(degree, started)["nodes"])
    cases = {}
    for case in CASES:
        check(started, admission=True)
        actual, original = metadata_cases[case], primary_domain["cases"][case]
        source, leaves = actual["source"], actual["leaves"]
        units = independent_units(leaves, source, started)
        table = [[row["center_raw"], *row["coefficient_raw"]] for row in fit_rows]
        require(
            len(table) == count and all(len(row) == degree + 2 for row in table),
            "Every actual center/coefficient table word",
        )
        encoded_table = [[signed_coefficient(word) % (1 << W) for word in row] for row in table]
        address_bits = count.bit_length() - 1
        require(
            count == 1 << address_bits and 0 <= address_bits <= 3,
            "Fixed power-of-two address inventory",
        )
        data_toggles = sum(word.bit_count() for row in encoded_table for word in row)
        zero_address_bits = sum(address_bits - index.bit_count() for index in range(count))
        equality_ccx = count * (0, 0, 2, 6)[address_bits]
        equality_cx = 2 * count if address_bits == 1 else 0
        qrom_cx = data_toggles if address_bits else 0
        qrom_x = data_toggles if not address_bits else 0
        thresholds = [row["raw_bounds"][0] for row in fit_rows[1:]]
        address_changes = sum((index ^ (index - 1)).bit_count() for index in range(1, count))
        calls = dict(add=operation_count["add"], mul=operation_count["mul"], sub=1, lt=count - 1)
        primitive = {
            field: sum(
                calls[operation] * units[operation]["resource_upper"][field] for operation in calls
            )
            for field in RESOURCE_FIELDS
        }
        copies = sum(calls.values()) * 4 * W
        extra_x = (
            2 * zero_address_bits
            + qrom_x
            + sum((word % (1 << W)).bit_count() for word in thresholds)
            + count
            - 1
        )
        extra_cx = equality_cx + qrom_cx + address_changes + copies
        additions = dict(
            source_gates=extra_x + extra_cx + equality_ccx,
            x=extra_x,
            cx=extra_cx,
            ccx=equality_ccx,
            t_count=7 * equality_ccx,
            t_depth=7 * equality_ccx,
            clifford_t_depth=extra_x + extra_cx + 15 * equality_ccx,
            clifford_cx=extra_cx + 6 * equality_ccx,
            clifford_h=2 * equality_ccx,
        )
        forward = {field: primitive[field] + additions[field] for field in RESOURCE_FIELDS}
        clean = {field: 2 * value for field, value in forward.items()}
        for field in ("cx", "source_gates", "clifford_cx", "clifford_t_depth"):
            clean[field] += 3 * W
        plan_count = len(estrin_ir(degree, started)["nodes"])
        words = plan_count + 2 + 2 * (count - 1) + int(address_bits > 0) + degree + 2
        scratches = [unit["qubits_upper"] - 3 * W for operation, unit in units.items()]
        private = max(*scratches, 2 * max(0, address_bits - 2))
        removal = independent_removal(actual["target"], source, original["stock_sites"], started)
        removed_indices = set(removal["removed_forward_call_indices"])
        removed, removed_copies, kept_depth = dict.fromkeys(RESOURCE_FIELDS, 0), 0, 0
        for index, call in enumerate(source["forward_calls"]):
            check(started)
            leaf = leaves[call["leaf"]]["resources"]
            if index in removed_indices:
                for field in RESOURCE_FIELDS:
                    removed[field] += leaf[field]
                removed_copies += 2 * W * len(call["args"])
            else:
                kept_depth += leaf["t_depth"]
        sites = original["actual_stock_sites"]
        whole = {
            field: source["resources"][field] - 2 * removed[field] + 2 * sites * clean[field]
            for field in RESOURCE_FIELDS
        }
        for field in ("cx", "source_gates", "clifford_cx"):
            whole[field] -= 2 * removed_copies
        whole["t_depth"] = 2 * kept_depth + 2 * sites * clean["t_depth"]
        require(
            all(value >= 0 for value in whole.values()) and whole["t_count"] == 7 * whole["ccx"],
            "Complete nonnegative exact7T symbolic source estimate",
        )
        qubits = source["resources"]["logical_qubits"] + sites * W * words
        qubits += max(0, private - source["resources"]["max_reused_scratch_qubits"])
        cap = original["baseline_capped_resources"]["logical_qubits"]
        cases[case] = dict(
            primitive_units=units,
            coefficient_QROM_rows_raw=table,
            coefficient_QROM_rows_unsigned72=encoded_table,
            primitive_forward_calls=calls,
            threshold_raw=thresholds,
            selector=dict(
                address_bits=address_bits,
                threshold_count=count - 1,
                address_toggle_CX=address_changes,
                equality_compute_uncompute_CCX=equality_ccx,
                equality_CX=equality_cx,
                address_inversion_X=2 * zero_address_bits,
                table_data_controlled_CX=qrom_cx,
                table_constant_X=qrom_x,
            ),
            full72_argument_copy_CX_per_forward=copies,
            dirty_output_XOR_CX=W,
            outer_function_argument_copy_CX_per_clean_invocation=2 * W,
            function_forward_resource_estimate=forward,
            function_clean_resource_estimate=clean,
            function_full72_SSA_words=words,
            function_private_scratch_qubits=private,
            full72_bank_inventory=dict(
                candidate_IR_values=plan_count,
                raw_remainder_bank=1,
                outer_argument_copy_bank=1,
                threshold_constant_banks=count - 1,
                threshold_predicate_banks=count - 1,
                selector_address_banks=int(address_bits > 0),
                QROM_center_and_coefficient_banks=degree + 2,
                external_input_output_banks=2,
            ),
            function_logical_qubit_upper=W * (words + 2) + private,
            original_polynomial_removal=removal,
            original_removed_leaf_forward_resources=removed,
            original_removed_argument_copy_CX=removed_copies,
            whole_source_resource_estimate=whole,
            whole_source_logical_qubit_upper=qubits,
            original_capped_source_resources=original["baseline_capped_resources"],
            original_serial_source_resources=original["baseline_serial_resources"],
            original_logical_qubit_cap=cap,
            estimated_qubit_upper_within_cap=qubits <= cap,
            estimated_serial_depth_not_realized_capped_schedule=True,
            whole_candidate_clean_invocations=2 * sites,
            global_forward_and_inverse_each_use_clean_candidate=True,
            exact7T_phase_paid=True,
            relative_phase_substitution=False,
            dynamic_selected_coefficient_constant_multiplier_discount=False,
            all_costs_are_estimates_until_emitted_ABI_and_capped_schedule_proofs=True,
        )
    return dict(
        schema="a13-symbolic-resource-estimate-v1",
        degree=degree,
        segments=count,
        cases=cases,
        arbitrary_phase_clean_XOR_ABI_still_requires_emitted_proof=True,
        old_dead_paths_preserved=True,
        full_financial_cost_not_divided_by_coordinates=True,
        resource_adoption_or_realized_improvement_claim=False,
    )


def original_polynomial_model(graph, site, radius, started):
    cache, records = {}, []

    def visit(value):
        check(started)
        if value == site["remainder"]:
            return {1: Fraction(1)}, Fraction(0)
        if value in cache:
            return cache[value]
        node = graph.node(value)
        if node["op"] == "const":
            polynomial, error = {0: Fraction(graph.constant(value), Q)}, Fraction(0)
        else:
            require(
                node["op"] in ("add", "mul") and node["params"] == {},
                "Original active Estrin polynomial",
            )
            a, ea = visit(node["args"][0])
            b, eb = visit(node["args"][1])
            if node["op"] == "add":
                polynomial, error = polynomial_sum(a, b), ea + eb
            else:
                ma = sum(
                    (abs(coefficient) * radius**degree for degree, coefficient in a.items()),
                    Fraction(0),
                )
                mb = sum(
                    (abs(coefficient) * radius**degree for degree, coefficient in b.items()),
                    Fraction(0),
                )
                polynomial = polynomial_product(a, b)
                error = ma * eb + mb * ea + ea * eb + EPS
                require(
                    (ma + ea) * (mb + eb) * Q**2 < 1 << 143, "Original error-induction product safe"
                )
        magnitude = (
            sum(
                (abs(coefficient) * radius**degree for degree, coefficient in polynomial.items()),
                Fraction(0),
            )
            + error
        )
        require(magnitude * Q < 1 << 71, "Original stored-word error induction safe")
        cache[value] = (polynomial, error)
        records.append(
            dict(
                value=value,
                op=node["op"],
                magnitude_upper=encode(magnitude),
                native_floor_error_upper=encode(error),
            )
        )
        return polynomial, error

    polynomial, error = visit(site["polynomial"])
    require(
        set(polynomial) == set(range(13)),
        "Original degree12 literal polynomial, not fitted candidate",
    )
    return polynomial, error, records


def original_integer_stock(graph, site, left, right, exponent, started):
    ranges, products = {site["clipped"]: word_range((left, right))}, []
    for value in site["original_native_stock_node_ids"]:
        check(started)
        node = graph.node(value)
        operands = [ranges[argument] for argument in node["args"]]
        operation, parameters = node["op"], node["params"]
        if operation == "const":
            raw = graph.constant(value)
            result = (raw, raw)
        elif operation in ("cmul", "mul"):
            second = (
                (signed_coefficient(parameters["c"]),) * 2 if operation == "cmul" else operands[1]
            )
            product = integer_product(
                operands[0],
                second,
                square=operation == "mul" and node["args"][0] == node["args"][1],
            )
            products.append(dict(value=value, product_raw_bounds=list(product)))
            result = (product[0] // Q, product[1] // Q)
        elif operation == "add":
            result = (operands[0][0] + operands[1][0], operands[0][1] + operands[1][1])
        elif operation == "sub":
            result = (operands[0][0] - operands[1][1], operands[0][1] - operands[1][0])
        elif operation == "bits":
            require(parameters["width"] == W, "Original full72 exponent conversion")
            shift = parameters["shift"]
            if shift >= 0:
                require(parameters["signed"] is True, "Signed native arithmetic extraction")
                result = (operands[0][0] >> shift, operands[0][1] >> shift)
            else:
                require(parameters["signed"] is False, "Native modular integer-exponent scaling")
                result = (operands[0][0] << -shift, operands[0][1] << -shift)
        else:
            require(
                operation == "shift"
                and operands[1] == (exponent, exponent)
                and -W < exponent < W
                and operands[0][0] > 0,
                "Original positive stock shift",
            )
            result = tuple(
                word << exponent if exponent >= 0 else word >> -exponent for word in operands[0]
            )
        ranges[value] = word_range(result)
    require(
        ranges[site["exponent"]] == (exponent, exponent)
        and ranges[site["remainder"]]
        == (left - exponent * site["ln2_raw"], right - exponent * site["ln2_raw"])
        and ranges[site["stock"]][0] > 0,
        "Original exact exponent/remainder/positive output",
    )
    return ranges, products


def audit_baseline(mp, declared, domain, metadata_cases, started):
    require(
        declared["schema"] == "a13-original-Estrin-baseline-certificate-v1"
        and declared["degree"] == 12
        and declared["segments"] == 1
        and declared["original_source_polynomial_not_new_fit"] is True
        and declared["original_eager_dead_paths_retained_in_source_cost"] is True
        and declared["no_G2_allocation_or_feasibility_claim"] is True,
        "Separate unchanged original baseline",
    )
    cases = {}
    for case in CASES:
        check(started, admission=True)
        original, primary = domain["cases"][case], declared["cases"][case]
        graph = GraphAudit(metadata_cases[case]["target"], started)
        site = original["actual_stock_sites"][0]
        words = original["original_literal_exp_coefficients"]
        coefficients = [Fraction(signed_coefficient(word), Q) for word in words]
        lo, hi = original["whole_integer_remainder_hull"]
        require(lo <= 0 <= hi, "Original variable-centered baseline witness")
        segment = dict(
            index=0,
            first_raw=lo,
            last_raw=hi,
            center_raw=0,
            local_interval=[encode(Fraction(lo, Q)), encode(Fraction(hi, Q))],
        )
        authorized, uniform = audit_segment_certificate(
            mp, primary["segment_certificate"], coefficients, words, segment, started
        )
        _, _, _, logarithm = original["original_native_settings"]
        true_logarithm = endpoints(mp.iv.log(outward(mp, 2)))
        ln_error = max(abs(Fraction(logarithm, Q) - endpoint) for endpoint in true_logarithm)
        maximum, alpha_max, witnesses = Fraction(0), Fraction(0), []
        require(len(primary["intersections"]) == 30, "Every original baseline class retained")
        for row, cell in zip(primary["intersections"], original["original_cells"], strict=True):
            check(started)
            require(
                row["k"] == cell["k"] and row["empty"] is cell["empty"],
                "Original baseline class identity",
            )
            if cell["empty"]:
                same(
                    row,
                    dict(k=cell["k"], empty=True),
                    "Original empty class contains no invented bound",
                )
                continue
            left, right = cell["clipped_raw_interval"]
            ranges, products = original_integer_stock(graph, site, left, right, cell["k"], started)
            rlo, rhi = cell["remainder_raw_interval"]
            actual_polynomial, floor, steps = original_polynomial_model(
                graph, site, Fraction(max(abs(rlo), abs(rhi)), Q), started
            )
            same(
                [encode(actual_polynomial[degree]) for degree in range(13)],
                [encode(value) for value in coefficients],
                "Actual original coefficient polynomial",
            )
            same(
                row["original_native_intermediate_raw_bounds"],
                {str(value): list(bounds) for value, bounds in ranges.items()},
                "Every original class stored-word guard",
            )
            same(row["original_signed144_products"], products, "Every original class product guard")
            same(
                row["actual_Estrin_floor_induction"],
                steps,
                "Every original floor and magnitude induction",
            )
            same(row["native_floor_error_upper"], encode(floor), "Original actual tree floor error")
            same(row["remainder_raw_bounds"], [rlo, rhi], "Original closed remainder class")
            same(
                row["additive_stock_beta_upper"],
                encode(EPS if cell["k"] < 0 else Fraction(0)),
                "Original shift beta separate",
            )
            total_poly = authorized["quantized"] + floor
            # The primary does not expose its ln2 endpoint error in baseline
            # rows. Authorize its final conservative relative/absolute claims
            # independently at130, using the actual literal and primary Epoly.
            k = cell["k"]
            relative = endpoints(
                mp.iv.exp(outward(mp, abs(k) * ln_error))
                * (1 + outward(mp, total_poly) * mp.iv.exp(outward(mp, Fraction(-rlo, Q))))
                - 1
            )[1]
            reduction = endpoints(
                outward(mp, Fraction(2) ** k)
                * mp.iv.exp(outward(mp, Fraction(rhi, Q)))
                * (mp.iv.exp(outward(mp, abs(k) * ln_error)) - 1)
            )[1]
            absolute = Fraction(2) ** k * total_poly + reduction + (EPS if k < 0 else Fraction(0))
            alpha = rational(row["relative_stock_alpha_upper"])
            error = rational(row["absolute_stock_error_upper"])
            require(
                alpha >= relative >= 0 and error >= absolute >= 0,
                "Original baseline fresh130 uniform error authorization",
            )
            maximum, alpha_max = max(maximum, error), max(alpha_max, alpha)
            witnesses.append(
                dict(
                    k=k,
                    verified_primary_absolute_stock_error_upper=encode(error),
                    verified_primary_relative_stock_alpha_upper=encode(alpha),
                )
            )
        same(
            primary["maximum_absolute_stock_error_upper"],
            encode(maximum),
            "Original maximum absolute error",
        )
        same(
            primary["maximum_relative_stock_alpha_upper"],
            encode(alpha_max),
            "Original maximum relative error",
        )
        same(primary["additive_stock_beta_upper"], encode(EPS), "Original full-domain shift beta")
        cases[case] = dict(
            uniform_proofs=uniform,
            class_authorizations=witnesses,
            verified_primary_absolute_stock_error_upper=encode(maximum),
            original_source_not_replaced_by_new_degree12_fit=True,
        )
    return dict(schema="independent130-a13-original-baseline-v1", cases=cases)


def seal(output, frozen, external, started, outcome):
    require(
        not (output / "manifest.json").exists() and not (output / "FAILED_UNSEALED.json").exists(),
        "Exclusive independent terminal, never partial reseal",
    )
    count = final_fresh(frozen, external, started)
    outcome = dict(
        outcome,
        verification_unique_paths=count,
        budget=elapsed(started),
        limits_CPU_admission_wall=[CPU, ADMISSION, WALL],
        new_test_credit=0,
        full_G2=False,
        adoption=False,
        cost_transfer=False,
        gate_emission_authorized=False,
    )
    write_json(output / "completion_outcome.json", outcome, started)
    files = owned_artifacts(output, started)
    manifest = dict(
        schema="a13-exp-frontier-recovery-independent-audit-manifest-v1",
        files=files,
        frozen_inputs=frozen,
        external_runtime_inputs=external,
        manifest_self_hash_excluded=True,
        terminal_outcome_file="completion_outcome.json",
        completed=outcome["completed"],
        passed=outcome["passed"],
        budget_censored=outcome["budget_censored"],
        terminal_budget_observation=elapsed(started),
        verification_and_output_hashing_before_terminal=True,
        original_expected_hashes_waived=False,
        historical_global_LIVE_integrity=dict(
            passed=False, mismatch_references=36, distinct_paths=9, expected_hashes_waived=False
        ),
    )
    manifest["manifest_inclusive_owned_count"] = len(files) + 1
    manifest["manifest_inclusive_retention_checked"] = True
    require(len(files) + 1 <= 64, "Owned64 cap includes the final manifest")
    owned_bytes = 0
    for key in files:
        check(started)
        owned_bytes += (output / key).stat().st_size
    manifest_bytes = 1
    for fragment in json.JSONEncoder(sort_keys=True, indent=2, allow_nan=False).iterencode(
        manifest
    ):
        check(started)
        manifest_bytes += len(fragment.encode())
        require(
            owned_bytes + manifest_bytes <= 128 * 1024**2,
            "Owned128MiB cap includes exact final manifest UTF8 bytes",
        )
    write_json(output / "manifest.json", manifest, started)
    found = v6_owned_inventory(output, started)
    require(
        found == {output / key for key in files} | {output / "manifest.json"}
        and len(found) == len(files) + 1 <= 64,
        "Exact final manifest-inclusive successful or failed inventory",
    )
    require(
        (output / "manifest.json").stat().st_size == manifest_bytes
        and sum(path.stat().st_size for path in found)
        == owned_bytes + manifest_bytes
        <= 128 * 1024**2,
        "Exact final aggregate retained bytes",
    )
    check(started)


def retain_failure(output, frozen, external, started, error, phase):
    if not output.exists():
        return
    try:
        require(
            not (output / "manifest.json").exists()
            and not (output / "completion_outcome.json").exists(),
            "A partial success terminal must remain failed-unsealed",
        )
        check(started)
        write_json(
            output / "failure.json",
            dict(
                failed=True,
                phase=phase,
                error_type=type(error).__name__,
                error=str(error),
                traceback=traceback.format_exc(),
                new_test_credit=0,
                budget=elapsed(started),
            ),
            started,
        )
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=False,
                passed=False,
                failed=True,
                rejection=False,
                budget_censored=isinstance(error, BudgetCensoredError),
                phase=phase,
                failure_file="failure.json",
            ),
        )
    except BaseException:
        # Constant evidence only after hard-clock exhaustion. This marker takes
        # precedence over every partial summary, outcome or manifest.
        try:
            with (output / "FAILED_UNSEALED.json").open("xb") as stream:
                stream.write(
                    b'{"failed":true,"completed":false,"passed":false,"budget_censored":null,"hard_budget_state_uncertified":true,"new_test_credit":0,"partial_success_invalid":true,"requires_fresh_version_and_receipt":true}\n'
                )
        except FileExistsError:
            pass


def audit_protocol(protocol, policy, method, source, started):
    check(started)
    require(
        protocol["schema"] == "a13-exp-frontier-recovery-independent-audit-protocol-v1"
        and protocol["source"] == SOURCE.relative_to(ROOT).as_posix()
        and protocol["output"] == OUTPUT.relative_to(ROOT).as_posix(),
        "Exact independently prepared source/route",
    )
    same(
        protocol["CPU_admission_wall_seconds"],
        [CPU, ADMISSION, WALL],
        "Unchanged independent whole-screen clocks",
    )
    same(protocol["fixed_grid"], [list(value) for value in GRID], "All20 fixed choices")
    same(
        protocol["author_sha256"], policy["author_sha256"], "Immutable reviewed pair of executables"
    )
    require(
        protocol["operational_recovery_audit_version"] == 6,
        "Exact audit-only new operational release",
    )
    same(
        protocol["V6_metadata_prerequisite_manifest_SHA256"],
        V6_METADATA_EXPECTED,
        "Immutable exact V6 metadata prerequisites",
    )
    for key in (
        "original_recovery_source_author_sha256",
        "original_recovery_author_SHA256",
        "source_manifest_SHA256",
        "prior_recovery_audit_failed_manifest_SHA256",
        "prior_recovery_root_review_manifest_SHA256",
        "prior_recovery_audit_v2_author_SHA256",
        "prior_recovery_audit_v2_failed_manifest_SHA256",
        "prior_recovery_audit_v2_root_review_manifest_SHA256",
        "prior_recovery_audit_v3_author_SHA256",
        "prior_recovery_audit_v3_failed_manifest_SHA256",
        "prior_recovery_audit_v3_root_review_manifest_SHA256",
        "exact_DP_optimization_method_document_SHA256",
        "prior_recovery_audit_v4_author_SHA256",
        "prior_recovery_audit_v4_failed_manifest_SHA256",
        "prior_recovery_audit_v4_root_review_manifest_SHA256",
        "actual_profile_manifest_SHA256",
        "Bernstein_author_SHA256",
        "Bernstein_finite_QA_manifest_SHA256",
        "Bernstein_finite_QA_ROOT_READY_SHA256",
    ):
        same(
            protocol[key],
            policy[key],
            "Original successful metadata source and failed audit remain separately pinned",
        )
    require(
        protocol["operational_A13_version"] == 2 and protocol["previous_failed_A13_credit"] == 0,
        "Fixed operational v2 and zero original failure credit",
    )
    for name in (
        "prior_A13_author_SHA256",
        "prior_A13_failed_receipt_manifest_SHA256",
        "prior_A13_root_review_manifest_SHA256",
    ):
        same(protocol[name], policy[name], "Immutable prior failure protocol pin")
    same(
        protocol["method_document_SHA256"],
        policy["method_document_SHA256"],
        "Immutable held method",
    )
    same(
        protocol["original_method_document_SHA256"],
        policy["original_method_document_SHA256"],
        "Unchanged original scientific method",
    )
    require(
        protocol["capture_manifest_SHA256"] == policy["capture_manifest_SHA256"]
        and protocol["original_material_receipt"] == MATERIAL.relative_to(ROOT).as_posix()
        and protocol["metadata_source_not_mathematical_PASS"] is True,
        "Strict recovery provenance without original success promotion",
    )
    same(
        protocol["proof_retention"],
        dict(
            format="canonical-gzip-json-v1",
            level=1,
            mtime=0,
            filename="",
            encoded_chunk_bytes=65536,
            duplicate_aggregate_proofs=False,
        ),
        "Fixed retention-only encoding",
    )
    same(
        protocol["selected_source_SHA256"],
        method["selected_existing_manifest_expected_pins"],
        "No selected source expectation override",
    )
    require(
        protocol["A07_manifest_SHA256"] == A07_SHA
        and protocol["source_manifest_sha256"] == source["manifest_sha256"],
        "Exact preparation prerequisite packets",
    )
    require(
        protocol["primary_digits"] == 90
        and protocol["independent_digits"] == DIGITS
        and protocol["threads"] == 1
        and protocol["new_fixture_credit"] == 0
        and protocol["startup_B_required"] is True
        and protocol["pure_Python_mpmath_backend_required"] is True,
        "Same fixed runtime, precision and credit",
    )
    require(
        protocol["candidate_G2_absolute_stock_error_allocation"] is None
        and protocol["candidate_G2_barrier_band_allocation"] is None
        and protocol["gate_emission_authorized"] is False
        and protocol["no_fit_bound_source_walk_gate_or_sample_executed_in_prepare"] is True,
        "Exploratory byte-only preparation, no science claim",
    )


def prepare(output, ready_sha256):
    started = start_clock()
    frozen, external, created = {}, {}, False
    try:
        initialize(started)
        require(output == OUTPUT and not output.exists(), "Exclusive fresh independent receipt")
        require("mpmath" not in sys.modules, "Preparation imports no scientific engine")
        v6_root_release(ready_sha256, frozen, external, started)
        policy = implementation_policy(started)
        method, origins, source = source_packet(policy, frozen, external, started)
        prior = source["prior_A13_provenance"]
        interpreter = runtime_inventory(frozen, external, started)
        verify_runtime(interpreter, frozen, external, started)
        loaded_origins(frozen, external, started)
        verify_maps(frozen, external, started)
        check(started, admission=True)
        output.mkdir()
        created = True
        (output / "executed_code").mkdir()
        (output / "rows").mkdir()
        for path in (
            AUTHOR,
            PRODUCER_AUTHOR,
            IMPLEMENTATION,
            IMPLEMENTATION_DOC,
            RECOVERY_METHOD,
            RECOVERY_METHOD_DOC,
            METHOD,
            METHOD_DOC,
            DP_METHOD,
            DP_METHOD_DOC,
            *(RESEARCH / name for name in PRIOR_RECOVERY_AUDIT_V4_AUTHOR_SHA256),
            *(RESEARCH / name for name in BERNSTEIN_AUTHOR_SHA256),
            *(RESEARCH / name for name in V5_AUTHOR_SHA256),
            *(RESEARCH / name for name in V2_METADATA_AUTHOR_SHA256),
            V6_READY,
            V2_METADATA_READY,
        ):
            copy_exact(path, output / "executed_code" / path.name, frozen, external, started)
        write_json(output / "selected_source_origins.json", origins, started)
        write_json(output / "prior_A13_provenance.json", prior, started)
        write_json(
            output / "prior_recovery_audit_provenance.json",
            source["prior_recovery_audit_provenance"],
            started,
        )
        write_json(
            output / "prior_recovery_audit_v2_provenance.json",
            source["prior_recovery_audit_v2_provenance"],
            started,
        )
        write_json(
            output / "prior_recovery_audit_v3_provenance.json",
            source["prior_recovery_audit_v3_provenance"],
            started,
        )
        write_json(output / "interpreter.json", interpreter, started)
        write_json(
            output / "Bernstein_v5_prerequisites.json",
            source["Bernstein_v5_prerequisites"],
            started,
        )
        write_json(
            output / "V6_metadata_prerequisites.json", source["V6_metadata_prerequisites"], started
        )
        verified = final_fresh(frozen, external, started)
        check(started, admission=True)
        protocol = dict(
            schema="a13-exp-frontier-recovery-independent-audit-protocol-v1",
            operational_A13_version=2,
            operational_recovery_audit_version=6,
            V6_ROOT_READY_SHA256=ready_sha256,
            V6_metadata_prerequisite_manifest_SHA256=V6_METADATA_EXPECTED,
            previous_failed_A13_credit=0,
            original_recovery_source_author_sha256=policy["original_recovery_source_author_sha256"],
            original_recovery_author_SHA256=policy["original_recovery_author_SHA256"],
            source_manifest_SHA256=policy["source_manifest_SHA256"],
            prior_recovery_audit_failed_manifest_SHA256=policy[
                "prior_recovery_audit_failed_manifest_SHA256"
            ],
            prior_recovery_root_review_manifest_SHA256=policy[
                "prior_recovery_root_review_manifest_SHA256"
            ],
            prior_recovery_audit_v2_author_SHA256=policy["prior_recovery_audit_v2_author_SHA256"],
            prior_recovery_audit_v2_failed_manifest_SHA256=policy[
                "prior_recovery_audit_v2_failed_manifest_SHA256"
            ],
            prior_recovery_audit_v2_root_review_manifest_SHA256=policy[
                "prior_recovery_audit_v2_root_review_manifest_SHA256"
            ],
            prior_recovery_audit_v3_author_SHA256=policy["prior_recovery_audit_v3_author_SHA256"],
            prior_recovery_audit_v3_failed_manifest_SHA256=policy[
                "prior_recovery_audit_v3_failed_manifest_SHA256"
            ],
            prior_recovery_audit_v3_root_review_manifest_SHA256=policy[
                "prior_recovery_audit_v3_root_review_manifest_SHA256"
            ],
            exact_DP_optimization_method_document_SHA256=policy[
                "exact_DP_optimization_method_document_SHA256"
            ],
            prior_recovery_audit_v4_author_SHA256=policy["prior_recovery_audit_v4_author_SHA256"],
            prior_recovery_audit_v4_failed_manifest_SHA256=policy[
                "prior_recovery_audit_v4_failed_manifest_SHA256"
            ],
            prior_recovery_audit_v4_root_review_manifest_SHA256=policy[
                "prior_recovery_audit_v4_root_review_manifest_SHA256"
            ],
            actual_profile_manifest_SHA256=policy["actual_profile_manifest_SHA256"],
            Bernstein_author_SHA256=policy["Bernstein_author_SHA256"],
            Bernstein_finite_QA_manifest_SHA256=policy["Bernstein_finite_QA_manifest_SHA256"],
            Bernstein_finite_QA_ROOT_READY_SHA256=policy["Bernstein_finite_QA_ROOT_READY_SHA256"],
            prior_A13_author_SHA256=policy["prior_A13_author_SHA256"],
            prior_A13_failed_receipt_manifest_SHA256=policy[
                "prior_A13_failed_receipt_manifest_SHA256"
            ],
            prior_A13_root_review_manifest_SHA256=policy["prior_A13_root_review_manifest_SHA256"],
            output=output.relative_to(ROOT).as_posix(),
            source=SOURCE.relative_to(ROOT).as_posix(),
            source_manifest_sha256=source["manifest_sha256"],
            prepared_UTC=datetime.now(timezone.utc).isoformat(),
            independent_auditor_module="research.limitation_program_20261001.audit_exp_frontier_recovery_v6",
            author_sha256=policy["author_sha256"],
            method_document_SHA256=policy["method_document_SHA256"],
            original_method_document_SHA256=policy["original_method_document_SHA256"],
            original_material_receipt=MATERIAL.relative_to(ROOT).as_posix(),
            capture_manifest_SHA256=policy["capture_manifest_SHA256"],
            metadata_source_not_mathematical_PASS=True,
            proof_retention=dict(
                format="canonical-gzip-json-v1",
                level=1,
                mtime=0,
                filename="",
                encoded_chunk_bytes=65536,
                duplicate_aggregate_proofs=False,
            ),
            selected_source_SHA256=method["selected_existing_manifest_expected_pins"],
            A07_manifest_SHA256=A07_SHA,
            CPU_admission_wall_seconds=[CPU, ADMISSION, WALL],
            primary_digits=90,
            independent_digits=DIGITS,
            threads=1,
            new_fixture_credit=0,
            startup_B_required=True,
            pure_Python_mpmath_backend_required=True,
            fixed_grid=[list(value) for value in GRID],
            candidate_G2_absolute_stock_error_allocation=None,
            candidate_G2_barrier_band_allocation=None,
            gate_emission_authorized=False,
            interpreter=interpreter,
            frozen_inputs=frozen,
            external_runtime_inputs=external,
            final_fresh_preparation_verified_paths=verified,
            preparation_budget=elapsed(started),
            all_process_CPU_and_creation_wall_charged=True,
            scientific_producer_or_helper_imports=False,
            no_fit_bound_source_walk_gate_or_sample_executed_in_prepare=True,
        )
        write_json(output / "protocol.json", protocol, started)
        write_json(
            output / "PREPARED_RECEIPT.json",
            dict(
                prepared=True,
                terminal=False,
                protocol_sha256=sha(output / "protocol.json", started),
                preparation_budget=elapsed(started),
                no_numeric_result_claim=True,
            ),
            started,
        )
        check(started)
        return protocol
    except BaseException as error:
        if created:
            retain_failure(output, frozen, external, started, error, "prepare")
        raise


def audit_rows(mp, domain, primary_domain, metadata_cases, started, output):
    inventory = read_json(MATERIAL / "fixed_inventory.json", started)
    expected_rows = [dict(degree=d, segments=s, row_id=f"d{d}_s{s}") for d, s in GRID]
    require(
        inventory["schema"] == "a13-fixed-inventory-v1"
        and inventory["no_adaptive_degrees_segments_or_precision"] is True,
        "Exact fixed inventory scope",
    )
    same(inventory["rows"], expected_rows, "All20 identities and their preregistered ordering")
    same(
        inventory["separate_original_baseline"],
        dict(degree=12, segments=1, new_degree12_fit_is_not_original_baseline=True),
        "Original baseline and fresh degree12 fit remain separate",
    )
    fits = read_json(MATERIAL / "coefficient_fit_diagnostics.json", started)
    certificates = read_json(MATERIAL / "exponential_approximation_certificate.json", started)
    frontier = read_json(MATERIAL / "function_frontier.json", started)
    require(
        fits["schema"] == "a13-fit-diagnostics-v1"
        and fits["round32_solve_is_final"] is True
        and fits["no_extra33rd_solve"] is True
        and fits["no_optimality_claim"] is True,
        "Actual finite fitting diagnostic scope",
    )
    require(
        certificates["schema"] == "a13-approximation-certificate-v1"
        and certificates["all_uniform_bounds_are_Bernstein_not_mesh"] is True
        and certificates["relative_alpha_and_negative_shift_beta_separate"] is True
        and certificates["original_baseline_file"] == "original_baseline_certificate.json",
        "Whole interval error proof ledger",
    )
    require(
        frontier["schema"] == "a13-function-frontier-v1"
        and frontier["all_costs_symbolic_estimates"] is True
        and frontier["candidate_G2_absolute_stock_error_allocation"] is None
        and frontier["candidate_G2_barrier_band_allocation"] is None
        and frontier["feasible_candidates_not_selected"] is True
        and frontier["gate_emission_authorized"] is False,
        "Allocation-free symbolic cost screen",
    )
    same(
        frontier["original_capped_baseline_resources"],
        {
            case: value["baseline_capped_resources"]
            for case, value in primary_domain["cases"].items()
        },
        "Unchanged baseline capped rows beside unexecuted candidate estimates",
    )
    require(
        len(fits["rows"]) == 20 and len(frontier["fixed_row_statuses"]) == 20,
        "Every successful or rejected row retained",
    )
    fit_by_id = {row["row_id"]: row for row in fits["rows"]}
    cert_by_id = {row["row_id"]: row for row in certificates["rows"]}
    cost_by_id = {row["row_id"]: row for row in frontier["rows"]}
    require(
        len(fit_by_id) == len(fits["rows"])
        and len(cert_by_id) == len(certificates["rows"])
        and len(cost_by_id) == len(frontier["rows"]),
        "No duplicate diagnostic or proof architecture",
    )
    success, statuses, rows = set(), [], []
    for identity, fit in zip(expected_rows, fits["rows"], strict=True):
        check(started, admission=True)
        degree, count, row_id = identity["degree"], identity["segments"], identity["row_id"]
        for key, value in identity.items():
            same(fit[key], value, "Exact fitting row identity")
        actual = read_json(MATERIAL / "rows" / (row_id + ".json"), started)
        for key, value in identity.items():
            same(actual[key], value, "Exact row artifact identity")
        status = fit["status"]
        require(
            actual["status"] == status
            and status
            in ("CERTIFIED_ESTIMATE", "FIT_FAILED", "CERTIFICATE_REJECTED", "RESOURCE_REJECTED"),
            "Exact retained fixed-row outcome",
        )
        status_row = dict(**identity, status=status)
        statuses.append(status_row)
        partitions = exact_segments(domain["cases"]["B4x12"]["whole_integer_remainder_hull"], count)
        if status == "CERTIFIED_ESTIMATE":
            success.add(row_id)
            same(
                actual["fit"]["segment_fits"],
                fit["segment_fits"],
                "Actual completed segment fitting payload",
            )
            certificate, cost = cert_by_id[row_id], cost_by_id[row_id]
            for payload in (certificate, cost):
                for key, value in status_row.items():
                    same(payload[key], value, "Success aggregate row identity")
            same(
                actual["certificate"],
                certificate["certificate"],
                "Actual certificate and aggregate",
            )
            same(
                actual["resource_estimate"],
                cost["resource_estimate"],
                "Actual resource and aggregate",
            )
            proof = audit_architecture(
                mp, actual["certificate"], fit["segment_fits"], degree, count, domain, started
            )
            independent_cost = independent_resources(
                degree, count, fit["segment_fits"], primary_domain, metadata_cases, started
            )
            same(
                actual["resource_estimate"],
                independent_cost,
                "Every selector/table/copy/bank/cleanup and whole-source resource term",
            )
            result = dict(
                **status_row,
                independently_authorized_error_certificate=proof,
                independently_reconstructed_resource_estimate=independent_cost,
            )
        else:
            require(
                row_id not in cert_by_id and row_id not in cost_by_id,
                "Rejected row has no certificate or resource credit",
            )
            expected_stage = {
                "FIT_FAILED": "fit",
                "CERTIFICATE_REJECTED": "certificate",
                "RESOURCE_REJECTED": "resource",
            }[status]
            require(
                actual["failed_stage"] == expected_stage
                and actual["no_uniform_certificate_claim"] is True
                and actual["no_resource_improvement_claim"] is True
                and actual["no_alternate_fitter_retry_or_new_choice"] is True,
                "Retained rejected row without mathematical or resource claim",
            )
            require(
                type(actual["error_type"]) is str
                and actual["error_type"]
                and type(actual["error"]) is str
                and actual["error"],
                "Actual rejected premise diagnostic",
            )
            same(
                actual["retained_completed_segment_fits"],
                fit["segment_fits"],
                "Every completed pre-rejection segment fit retained",
            )
            for key in ("error_type", "error"):
                same(actual[key], fit[key], "Exact row diagnostic reconciliation")
            require(
                len(fit["segment_fits"]) <= count
                and (status == "FIT_FAILED" or len(fit["segment_fits"]) == count),
                "Only a fitting failure may leave incomplete segment fits",
            )
            evidence = []
            for segment_fit, segment in zip(fit["segment_fits"], partitions):
                _, _, checked = audit_fit_segment(segment_fit, degree, segment, started)
                evidence.append(checked)
            result = dict(
                **status_row,
                rejected_primary_premise_preserved=True,
                no_certificate_resource_or_feasibility_claim=True,
                independent_completed_fit_structure=evidence,
                numeric_fit_or_rejected_premise_reexecuted=False,
                error_type=actual["error_type"],
                error=actual["error"],
            )
        name = "rows/" + row_id + ".json.gz"
        encoding = write_compressed_proof(output / name, result, started)
        rows.append(dict(**status_row, actual_row_file=name, **encoding))
    require(
        set(cert_by_id) == set(cost_by_id) == success,
        "Only and all certified rows have proof/cost aggregates",
    )
    same(frontier["fixed_row_statuses"], statuses, "All fixed outcome statuses reconcile")
    return statuses, rows


def run(output, ready_sha256, protocol_sha256):
    started = start_clock()
    frozen, external, admitted = {}, {}, False
    try:
        initialize(started)
        require(output == OUTPUT and output.is_dir(), "Exact actual prepared independent screen")
        require(
            not any(
                (output / name).exists()
                for name in (
                    "manifest.json",
                    "completion_outcome.json",
                    "FAILED_UNSEALED.json",
                    "failure.json",
                    "run_started.json",
                )
            ),
            "No failed preparation, repeated run or partial terminal",
        )
        admitted = True
        v6_root_release(ready_sha256, frozen, external, started)
        bind(frozen, external, output / "protocol.json", protocol_sha256, started)
        protocol = read_json(output / "protocol.json", started)
        require(
            protocol["V6_ROOT_READY_SHA256"] == ready_sha256,
            "Run uses the exact originally frozen V6 ROOT release",
        )
        prepared = read_json(output / "PREPARED_RECEIPT.json", started)
        require(
            prepared["prepared"] is True
            and prepared["terminal"] is False
            and prepared["protocol_sha256"] == sha(output / "protocol.json", started),
            "Immutable actual preparation",
        )
        map_inputs(protocol, frozen, external, started)
        for name in (
            "protocol.json",
            "PREPARED_RECEIPT.json",
            "selected_source_origins.json",
            "prior_A13_provenance.json",
            "prior_recovery_audit_provenance.json",
            "prior_recovery_audit_v2_provenance.json",
            "prior_recovery_audit_v3_provenance.json",
            "interpreter.json",
            "Bernstein_v5_prerequisites.json",
            "V6_metadata_prerequisites.json",
        ):
            bind(frozen, external, output / name, sha(output / name, started), started)
        policy = implementation_policy(started)
        method, origins, source = source_packet(policy, frozen, external, started)
        same(
            read_json(output / "prior_A13_provenance.json", started),
            source["prior_A13_provenance"],
            "Full original failure maps immutable after prepare",
        )
        same(
            read_json(output / "prior_recovery_audit_provenance.json", started),
            source["prior_recovery_audit_provenance"],
            "Complete original recovery audit failure map remains immutable",
        )
        same(
            read_json(output / "prior_recovery_audit_v2_provenance.json", started),
            source["prior_recovery_audit_v2_provenance"],
            "Complete failed v2 audit and static release maps remain immutable",
        )
        same(
            read_json(output / "prior_recovery_audit_v3_provenance.json", started),
            source["prior_recovery_audit_v3_provenance"],
            "Complete censored V3 maps and fourteen failure-only rows remain immutable",
        )
        audit_protocol(protocol, policy, method, source, started)
        same(
            read_json(output / "Bernstein_v5_prerequisites.json", started),
            source["Bernstein_v5_prerequisites"],
            "Full V5 actual prerequisites immutable after preparation",
        )
        same(
            read_json(output / "V6_metadata_prerequisites.json", started),
            source["V6_metadata_prerequisites"],
            "Complete exact V6 metadata remains immutable",
        )
        same(
            origins,
            read_json(output / "selected_source_origins.json", started),
            "Every original input origin remains strict",
        )
        interpreter = read_json(output / "interpreter.json", started)
        same(interpreter, protocol["interpreter"], "Unchanged actual prepared runtime record")
        verify_runtime(interpreter, frozen, external, started)
        loaded_origins(frozen, external, started)
        verify_maps(frozen, external, started)
        check(started, admission=True)
        write_json(
            output / "run_started.json",
            dict(
                UTC=datetime.now(timezone.utc).isoformat(),
                process_id=os.getpid(),
                limits=[CPU, ADMISSION, WALL],
            ),
            started,
        )
        require(
            "mpmath" not in sys.modules, "Lazy numerical engine only after complete byte admission"
        )
        import mpmath as mp

        require(
            mp.__version__ == "1.3.0" and sys.modules["mpmath.libmp.backend"].BACKEND == "python",
            "Actual pure-Python fixed backend",
        )
        mp.mp.dps = mp.iv.dps = DIGITS
        loaded_origins(frozen, external, started)
        check(started, admission=True)
        load_integer_bernstein(frozen, external, started)
        check(started, admission=True)
        domain = typed_source_domain(started)
        metadata_cases = original_native_metadata(frozen, started)
        primary_domain = read_json(MATERIAL / "source_domain_binding.json", started)
        domain_authorization = reconcile_domain(primary_domain, domain, metadata_cases, started)
        write_json(output / "independent_source_domain_binding.json", domain, started)
        write_json(output / "source_domain_authorization.json", domain_authorization, started)
        baseline = audit_baseline(
            mp,
            read_json(MATERIAL / "original_baseline_certificate.json", started),
            domain,
            metadata_cases,
            started,
        )
        write_json(output / "independent_original_baseline_certificate.json", baseline, started)
        statuses, row_evidence = audit_rows(
            mp, domain, primary_domain, metadata_cases, started, output
        )
        certified = sum(row["status"] == "CERTIFIED_ESTIMATE" for row in statuses)
        # The failed material's partial summary and completion are never scientific
        # premises. This fresh audit establishes every row result independently.
        verify_runtime(interpreter, frozen, external, started)
        write_json(
            output / "loaded_module_origins.json",
            loaded_origins(frozen, external, started),
            started,
        )
        write_json(
            output / "fixed_inventory_authorization.json",
            dict(
                fixed_row_statuses=statuses,
                independent_row_artifacts=row_evidence,
                original_baseline_retained_separately=True,
                all20_rows_and_rejections_retained=True,
            ),
            started,
        )
        summary = dict(
            schema="a13-exp-frontier-recovery-independent-audit-summary-v1",
            operational_recovery_audit_version=6,
            V6_ROOT_READY_SHA256=ready_sha256,
            V6_metadata_prerequisite_manifest_SHA256=V6_METADATA_EXPECTED,
            prior_failed_recovery_audit_v5_credit=0,
            partial_v5_rows_promoted=False,
            lexical_syntax_only_optimization=True,
            membership_index_introduced=False,
            prior_failed_recovery_audit_credit=0,
            prior_failed_recovery_audit_v2_credit=0,
            prior_failed_recovery_audit_v3_credit=0,
            prior_failed_recovery_audit_v4_credit=0,
            exact_integer_Bernstein_kernel=True,
            Bernstein_kernel_source_SHA256=BERNSTEIN_AUTHOR_SHA256[BERNSTEIN_KERNEL.name],
            Bernstein_finite_QA_manifest_SHA256=BERNSTEIN_QA_SHA,
            actual_profile_manifest_SHA256=PRIOR_PROFILE_SHA,
            Bernstein_function_ABI_or_rational_result_changed=False,
            exact_dyadic_integer_two_pass_prefix_selection=True,
            selection_objective_or_declared_transcript_changed=False,
            old_censored_proof_rows_promoted_or_reused=False,
            completed=True,
            passed=True,
            independent_audit_passed=True,
            metadata_source_passed=True,
            failed_original_source_mathematical_PASS=False,
            all_untrusted_claimed_rows_independently_recertified=True,
            original_failure_remains_authoritative_zero_credit=True,
            capture_manifest_sha256=source["capture_manifest_sha256"],
            rejection=False,
            budget_censored=False,
            scientific_screen_complete=True,
            fixed_architecture_rows=20,
            certified_estimate_rows=certified,
            retained_rejected_rows=20 - certified,
            all20_uniformly_certified=certified == 20,
            fixed_row_statuses=statuses,
            source_manifest_sha256=source["manifest_sha256"],
            every_claimed_primary80_uniform_bound_authorized_by_independent130=True,
            independent112_uniform_witnesses_retained_separately=True,
            exact_finite_fitting_transcript_and_single_tie_even_quantization_checked=True,
            all_claimed_native_intermediate72_product144_and_shift_guards_independently_recomputed=True,
            all_claimed_selector_QROM_argument_output_copies_banks_and_cleanup_costs_independently_reconstructed=True,
            global_financial_forward_and_inverse_clean_function_invocations_paid=True,
            symbolic_resources_not_actual_source_or_capped_schedule=True,
            candidate_G2_absolute_stock_error_allocation=None,
            candidate_G2_barrier_band_allocation=None,
            gate_emission_authorized=False,
            full_G2=False,
            adoption=False,
            cost_transfer=False,
            feasible_architecture_or_realized_cost_improvement_claim=False,
            new_test_credit=0,
            new_gate_replays=0,
            new_price_samples=0,
            scientific_producer_or_helper_imports=False,
            source_expected_hashes_waived=False,
            budget=elapsed(started),
        )
        write_json(output / "summary.json", summary, started)
        seal(
            output,
            frozen,
            external,
            started,
            dict(
                completed=True,
                passed=True,
                independent_audit_passed=True,
                metadata_source_passed=True,
                rejection=False,
                budget_censored=False,
                scientific_screen_complete=True,
                phase="run",
                summary_file="summary.json",
            ),
        )
        return summary
    except BaseException as error:
        if admitted:
            retain_failure(output, frozen, external, started, error, "run")
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "run"))
    parser.add_argument("--output", required=True)
    parser.add_argument("--ready-sha256", required=True)
    parser.add_argument("--protocol-sha256")
    arguments = parser.parse_args()
    output = (ROOT / arguments.output).resolve()
    require(output == OUTPUT, "Only the fresh exact independent A13 receipt")
    require(SHA_PATTERN.fullmatch(arguments.ready_sha256), "Externally frozen READY SHA")
    if arguments.operation == "prepare":
        require(
            arguments.protocol_sha256 is None, "Prepare has no yet-created protocol expectation"
        )
        result = prepare(output, arguments.ready_sha256)
    else:
        require(
            type(arguments.protocol_sha256) is str
            and SHA_PATTERN.fullmatch(arguments.protocol_sha256),
            "ROOT must externally freeze the prepared protocol before scientific run",
        )
        result = run(output, arguments.ready_sha256, arguments.protocol_sha256)
    print(
        json.dumps(
            dict(
                operation=arguments.operation,
                output=output.relative_to(ROOT).as_posix(),
                prepared=arguments.operation == "prepare",
                passed=result.get("passed"),
                new_test_credit=0,
            )
        )
    )


if __name__ == "__main__":
    main()
