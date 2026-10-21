"""One local U/CX bridge with paid phase and full outward operator checks.

Importing this module performs no SDK, numerical or operator work.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from math import isfinite, isqrt
import time

DPS = 160
ROOT_BITS = 256
ALLOWANCE = Fraction(1, 74880000000)
CPU = 120
ADMISSION = 90
WALL = 300
SDK_ROWS = 1024
NATIVE_SLOTS = 4096
MATRIX_HASH = "4f91a35a9d13366d3e02b79d23271f581dc30514a946155598950a3632415066"


class BudgetCensoredError(RuntimeError):
    """A terminal global censor, never an unsupported SDK result."""


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Budget:
    def __init__(self):
        self.cpu = time.process_time()
        self.wall = time.monotonic()

    def check(self, admission=False):
        cpu = time.process_time() - self.cpu
        wall = time.monotonic() - self.wall
        if cpu > (ADMISSION if admission else CPU) or wall > WALL:
            raise BudgetCensoredError("Fixed120CPU/admission90/wall300 budget")
        return cpu, wall


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def exact(value):
    require(type(value) is list and len(value) == 2, "Exact rational pair")
    require(all(type(v) is int for v in value) and value[1] > 0, "Exact integer rational")
    result = Fraction(*value)
    require(pair(result) == value, "Canonical rational pair")
    return result


def fingerprint(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


def binary64_pair(value):
    require(type(value) is float and isfinite(value), "Finite actual binary64 SDK parameter")
    return pair(Fraction.from_float(value))


def sdk_exact(value):
    result = exact(value)
    try:
        floating = float(result)
    except OverflowError as error:
        raise ValueError("Finite exact binary64 SDK parameter") from error
    require(
        isfinite(floating) and Fraction.from_float(floating) == result,
        "Exact finite binary64 SDK parameter",
    )
    return result


def literal_matrix(value):
    require(set(value) == {"shape", "binary64_complex_rationals"}, "Saved matrix literal schema")
    require(value["shape"] == [8, 8], "One fixed saved8x8 matrix")
    entries = value["binary64_complex_rationals"]
    require(type(entries) is list and len(entries) == 64, "All64 saved complex entries")
    result = []
    for entry in entries:
        require(type(entry) is list and len(entry) == 2, "Complex rational entry")
        result.append((exact(entry[0]), exact(entry[1])))
    return [result[j * 8 : (j + 1) * 8] for j in range(8)]


def validate_sdk(record):
    require(record["schema"] == "one-local-SDK-U-CX-v1", "Saved SDK row schema")
    n = record["local_qubits"]
    require(type(n) is int and 1 <= n <= 3, "At most three local wires")
    require(
        type(record["global_wires"]) is list
        and len(record["global_wires"]) == n
        and all(type(v) is int and v >= 0 for v in record["global_wires"])
        and len(set(record["global_wires"])) == n,
        "Distinct exact global wire map",
    )
    require(
        type(record["sdk_calls"]) is int and record["sdk_calls"] == 1, "Exactly one saved SDK call"
    )
    sdk_exact(record["sdk_global_phase_exact"])
    rows = record["operations"]
    require(type(rows) is list and len(rows) <= SDK_ROWS, "Fixed1024 SDK row cap")
    for row in rows:
        require(set(row) == {"op", "wires", "params_exact"}, "Exact SDK operation fields")
        op, wires, params = row["op"], row["wires"], row["params_exact"]
        require(op in ("u", "cx"), "Only actual SDK u/cx rows")
        require(
            type(wires) is list
            and len(wires) == (1 if op == "u" else 2)
            and all(type(w) is int and 0 <= w < n for w in wires)
            and len(set(wires)) == len(wires),
            "Exact local SDK wire arity",
        )
        require(
            type(params) is list and len(params) == (3 if op == "u" else 0),
            "Exact SDK parameter arity",
        )
        for value in params:
            sdk_exact(value)
    return n


def bridge(record):
    n = validate_sdk(record)
    phase = sdk_exact(record["sdk_global_phase_exact"])
    phases, native = [], []
    for index, row in enumerate(record["operations"]):
        if row["op"] == "cx":
            native.append(dict(op="cx", wires=row["wires"][:], source_sdk_row=index))
            continue
        theta, phi, lam = map(sdk_exact, row["params_exact"])
        contribution = (phi + lam) / 2
        phase += contribution
        phases.append(dict(source_sdk_row=index, phase_exact=pair(contribution)))
        for op, angle, role in (("rz", lam, "lambda"), ("ry", theta, "theta"), ("rz", phi, "phi")):
            native.append(
                dict(
                    op=op,
                    wires=row["wires"][:],
                    angle_exact=pair(angle),
                    source_sdk_row=index,
                    source_parameter=role,
                )
            )
    native.append(dict(op="phase", wires=[], angle_exact=pair(phase)))
    require(len(native) <= NATIVE_SLOTS, "Fixed4096 native slots including paid phase")
    return dict(
        schema="one-local-phase-paid-native-v1",
        local_qubits=n,
        global_wires=record["global_wires"][:],
        operations=native,
        sdk_global_phase_exact=record["sdk_global_phase_exact"],
        per_U_phases=phases,
        aggregate_phase_exact=pair(phase),
        phase_slots=1,
        controlled_phase_implementation_and_cost=None,
        full_Gaussian_preparation_or_cost=False,
    )


def inverse(rows):
    result = deepcopy(list(reversed(rows)))
    for row in result:
        if row["op"] != "cx":
            row["angle_exact"] = pair(-exact(row["angle_exact"]))
    return result


def validate_native(rows, n):
    require(type(n) is int and 1 <= n <= 3, "At most three local wires")
    require(type(rows) is list and len(rows) <= 2 * NATIVE_SLOTS, "Native/inverse validation cap")
    for row in rows:
        op, wires = row["op"], row["wires"]
        require(op in ("ry", "rz", "cx", "phase"), "Native paid-phase gate alphabet")
        arity = 2 if op == "cx" else 0 if op == "phase" else 1
        require(
            type(wires) is list
            and len(wires) == arity
            and all(type(w) is int and 0 <= w < n for w in wires)
            and len(set(wires)) == len(wires),
            "Native local wire arity",
        )
        if op != "cx":
            exact(row["angle_exact"])


def interval_tools():
    import mpmath as mp

    mp.iv.dps = DPS
    return mp.iv


def iv_exact(iv, value):
    value = Fraction(value)
    return iv.mpf(value.numerator) / iv.mpf(value.denominator)


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def times(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def interval_operator(rows, n, sdk=False, global_phase=None, check=None):
    """Expand all columns using row-pair updates, including scalar phases."""
    if not sdk:
        validate_native(rows, n)
    iv = interval_tools()
    zero, one = iv.mpf(0), iv.mpf(1)
    dim = 1 << n
    matrix = [[(one if i == j else zero, zero) for j in range(dim)] for i in range(dim)]

    def scalar(angle):
        x = iv_exact(iv, angle)
        return iv.cos(x), iv.sin(x)

    for row in rows:
        if check is not None:
            check()
        op, wires = row["op"], row["wires"]
        if op == "phase":
            z = scalar(exact(row["angle_exact"]))
            matrix = [[times(z, v) for v in r] for r in matrix]
        elif op == "cx":
            control, target = wires
            for i in range(dim):
                if (i >> control) & 1 and not ((i >> target) & 1):
                    j = i ^ (1 << target)
                    matrix[i], matrix[j] = matrix[j], matrix[i]
        else:
            if op == "u":
                theta, phi, lam = map(sdk_exact, row["params_exact"])
                a = iv_exact(iv, theta / 2)
                c, s = iv.cos(a), iv.sin(a)
                u00, u01 = (c, zero), times((-s, zero), scalar(lam))
                u10, u11 = times((s, zero), scalar(phi)), times((c, zero), scalar(phi + lam))
            else:
                a = iv_exact(iv, exact(row["angle_exact"]) / 2)
                c, s = iv.cos(a), iv.sin(a)
                if op == "ry":
                    u00, u01, u10, u11 = (c, zero), (-s, zero), (s, zero), (c, zero)
                else:
                    u00, u01, u10, u11 = (c, -s), (zero, zero), (zero, zero), (c, s)
            wire = wires[0]
            for i in range(dim):
                if (i >> wire) & 1:
                    continue
                j = i ^ (1 << wire)
                low, high = matrix[i], matrix[j]
                matrix[i] = [plus(times(u00, a), times(u01, b)) for a, b in zip(low, high)]
                matrix[j] = [plus(times(u10, a), times(u11, b)) for a, b in zip(low, high)]
    if global_phase is not None:
        z = scalar(global_phase)
        matrix = [[times(z, v) for v in r] for r in matrix]
    return matrix


def endpoint(raw):
    sign, mantissa, exponent, bits = raw
    require(sign in (0, 1) and mantissa >= 0 and bits >= 0, "Finite interval endpoint")
    return Fraction((-1 if sign else 1) * int(mantissa)) * Fraction(2) ** int(exponent)


def upper_sqrt(value):
    value = Fraction(value)
    require(value >= 0, "Nonnegative squared residual")
    scaled = value.numerator << (2 * ROOT_BITS)
    quotient, remainder = divmod(scaled, value.denominator)
    integer = isqrt(quotient)
    if integer * integer < quotient or remainder:
        integer += 1
    result = Fraction(integer, 1 << ROOT_BITS)
    require(result * result >= value, "Outward256bit root")
    return result


def residual(actual, target, target_exact=False):
    iv = interval_tools()
    require(len(actual) == len(target), "Full operator dimension")
    squared = iv.mpf(0)
    entries = []
    for row_a, row_b in zip(actual, target):
        require(len(row_a) == len(row_b) == len(actual), "Full square operator")
        for a, b in zip(row_a, row_b):
            if target_exact:
                b = iv_exact(iv, b[0]), iv_exact(iv, b[1])
            re, im = a[0] - b[0], a[1] - b[1]
            entry = re * re + im * im
            squared += entry
            entries.append(pair(max(Fraction(0), endpoint(entry._mpi_[1]))))
    upper = max(Fraction(0), endpoint(squared._mpi_[1]))
    return dict(
        entries=len(entries),
        squared_entry_upper_exact=entries,
        squared_Frobenius_lower_exact=pair(max(Fraction(0), endpoint(squared._mpi_[0]))),
        squared_Frobenius_upper_exact=pair(upper),
        operator_error_upper_exact=pair(upper_sqrt(upper)),
        decimal_digits=DPS,
        outward_root_bits=ROOT_BITS,
        phase_optimized=False,
        full_operator=True,
    )


def identity(n):
    dim = 1 << n
    return [[(Fraction(i == j), Fraction(0)) for j in range(dim)] for i in range(dim)]


def certify(sdk, native, target, check=None):
    require(
        fingerprint(native) == fingerprint(bridge(sdk)),
        "Exact SDK-to-native mapping and paid phase provenance",
    )
    n = validate_sdk(sdk)
    require(n == 3 and sdk["global_wires"] == [10, 11, 8], "Fixed site1 local wire map")
    actual = interval_operator(native["operations"], n, check=check)
    original = interval_operator(
        sdk["operations"],
        n,
        sdk=True,
        global_phase=sdk_exact(sdk["sdk_global_phase_exact"]),
        check=check,
    )
    restored = interval_operator(
        native["operations"] + inverse(native["operations"]), n, check=check
    )
    result = dict(
        native_to_saved_full_operator=residual(actual, literal_matrix(target), True),
        SDK_to_saved_full_operator=residual(original, literal_matrix(target), True),
        native_to_original_SDK_full_operator=residual(actual, original),
        native_literal_inverse_full_operator=residual(restored, identity(n), True),
    )
    result["passed"] = all(
        exact(row["operator_error_upper_exact"]) <= ALLOWANCE for row in result.values()
    )
    result.update(
        local_error_allowance_exact=pair(ALLOWANCE),
        target_entries=64,
        paid_scalar_phase_exact=native["aggregate_phase_exact"],
        global_phase_is_not_discarded=True,
        full_Gaussian_loader_certified=False,
        native_financial_cost=None,
        Clifford_T_cost=None,
    )
    return result
