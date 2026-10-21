"""Independent full-operator bridge audit, with no SDK or audited helper imports."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import isfinite, isqrt
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research/limitation_program_20261001"
PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "A04_mps_u_bridge_run001"
RECEIPT = PROGRAM / "A04_mps_u_bridge_audit_run001"
INTERPRETER = ROOT / ".context/controlled_closeout_repro/Scripts/python.exe"
PREFLIGHT = RESEARCH / "mps_local_u_bridge_preflight.json"
DPS, ROOT_BITS, CPU, ADMISSION, WALL = 160, 256, 120, 90, 300
ALLOWANCE = Fraction(1, 74880000000)
MATRIX_HASH = "4f91a35a9d13366d3e02b79d23271f581dc30514a946155598950a3632415066"


class BudgetCensoredError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def budget(started, admission=False):
    cpu, wall = time.process_time() - started[0], time.monotonic() - started[1]
    if cpu > (ADMISSION if admission else CPU) or wall > WALL:
        raise BudgetCensoredError("Independent fixed120CPU/admission90/wall300 audit")
    return cpu, wall


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def sha(path, started=None):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while True:
            if started is not None:
                budget(started)
            block = stream.read(1 << 20)
            if not block:
                break
            result.update(block)
            if started is not None:
                budget(started)
    return result.hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT.resolve()).as_posix()


def bind(frozen, path, expected):
    resolved = (ROOT / str(path).replace("\\", "/")).resolve()
    resolved.relative_to(ROOT.resolve())
    key = relative(resolved)
    require(
        type(expected) is str
        and len(expected) == 64
        and all(c in "0123456789abcdef" for c in expected),
        "Canonical prior SHA",
    )
    require(key not in frozen or frozen[key] == expected, "Canonical expectation conflict: " + key)
    frozen[key] = expected


def verify(frozen, started=None):
    for key, expected in frozen.items():
        if started is not None:
            budget(started)
        require(sha(ROOT / key, started) == expected, "Independent frozen input mismatch: " + key)


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def rational(value):
    require(
        type(value) is list
        and len(value) == 2
        and all(type(x) is int for x in value)
        and value[1] > 0,
        "Typed rational literal",
    )
    result = Fraction(*value)
    require(pair(result) == value, "Canonical exact rational")
    return result


def binary64(value):
    result = rational(value)
    try:
        floating = float(result)
    except OverflowError as error:
        raise AssertionError("Finite saved binary64") from error
    require(isfinite(floating) and Fraction.from_float(floating) == result, "Exact saved binary64")
    return result


def fingerprint(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


def recover(sdk):
    require(
        sdk["schema"] == "one-local-SDK-U-CX-v1"
        and type(sdk["local_qubits"]) is int
        and sdk["local_qubits"] == 3
        and type(sdk["global_wires"]) is list
        and all(type(wire) is int for wire in sdk["global_wires"])
        and sdk["global_wires"] == [10, 11, 8]
        and type(sdk["sdk_calls"]) is int
        and sdk["sdk_calls"] == 1,
        "Sole original SDK call, dimension and wire map",
    )
    require(type(sdk["operations"]) is list and len(sdk["operations"]) <= 1024, "SDK row cap")
    phase = binary64(sdk["sdk_global_phase_exact"])
    phases, expected = [], []
    for index, row in enumerate(sdk["operations"]):
        require(set(row) == {"op", "wires", "params_exact"}, "SDK exact row fields")
        name, wires, parameters = row["op"], row["wires"], row["params_exact"]
        require(name in ("u", "cx"), "Independent u/cx gate inventory")
        require(
            type(wires) is list
            and len(wires) == (1 if name == "u" else 2)
            and all(type(w) is int and 0 <= w < 3 for w in wires)
            and len(set(wires)) == len(wires),
            "Independent local wire arity",
        )
        require(
            type(parameters) is list and len(parameters) == (3 if name == "u" else 0),
            "Independent exact parameter arity",
        )
        if name == "cx":
            expected.append(dict(op="cx", wires=wires[:], source_sdk_row=index))
        else:
            theta, phi, lam = [binary64(x) for x in parameters]
            paid = (phi + lam) / 2
            phase += paid
            phases.append(dict(source_sdk_row=index, phase_exact=pair(paid)))
            expected.extend(
                dict(
                    op=name,
                    wires=wires[:],
                    angle_exact=pair(angle),
                    source_sdk_row=index,
                    source_parameter=role,
                )
                for name, angle, role in (
                    ("rz", lam, "lambda"),
                    ("ry", theta, "theta"),
                    ("rz", phi, "phi"),
                )
            )
    expected.append(dict(op="phase", wires=[], angle_exact=pair(phase)))
    require(len(expected) <= 4096, "Independent paid native slot cap")
    return dict(
        schema="one-local-phase-paid-native-v1",
        local_qubits=3,
        global_wires=[10, 11, 8],
        operations=expected,
        sdk_global_phase_exact=sdk["sdk_global_phase_exact"],
        per_U_phases=phases,
        aggregate_phase_exact=pair(phase),
        phase_slots=1,
        controlled_phase_implementation_and_cost=None,
        full_Gaussian_preparation_or_cost=False,
    )


def inverted(rows):
    result = deepcopy(rows[::-1])
    for gate in result:
        if gate["op"] != "cx":
            gate["angle_exact"] = pair(-rational(gate["angle_exact"]))
    return result


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def multiply(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def expand(rows, started, sdk=False, phase=None):
    """Embed each gate by basis indices and sparsely multiply all eight columns."""
    import mpmath as mp

    mp.iv.dps = DPS
    iv = mp.iv
    zero, one = iv.mpf(0), iv.mpf(1)
    origin = (zero, zero)
    matrix = [[(one if row == column else zero, zero) for column in range(8)] for row in range(8)]

    def interval(q):
        return iv.mpf(q.numerator) / iv.mpf(q.denominator)

    def unit_phase(q):
        angle = interval(q)
        return iv.cos(angle), iv.sin(angle)

    for item in rows:
        budget(started)
        op, wires = item["op"], item["wires"]
        supports = [[] for _ in range(8)]
        if op == "cx":
            c, t = wires
            for column in range(8):
                row = column ^ (1 << t) if (column >> c) & 1 else column
                supports[row].append((column, (one, zero)))
        elif op == "phase":
            diagonal = unit_phase(rational(item["angle_exact"]))
            supports = [[(index, diagonal)] for index in range(8)]
        else:
            if sdk:
                require(op == "u", "Original SDK operator alphabet")
                theta, phi, lam = [binary64(q) for q in item["params_exact"]]
                a = interval(theta / 2)
                c, s = iv.cos(a), iv.sin(a)
                small = [
                    [(c, zero), multiply((-s, zero), unit_phase(lam))],
                    [
                        multiply((s, zero), unit_phase(phi)),
                        multiply((c, zero), unit_phase(phi + lam)),
                    ],
                ]
            else:
                a = interval(rational(item["angle_exact"]) / 2)
                c, s = iv.cos(a), iv.sin(a)
                require(op in ("ry", "rz"), "Native local rotation alphabet")
                small = (
                    [[(c, zero), (-s, zero)], [(s, zero), (c, zero)]]
                    if op == "ry"
                    else [[(c, -s), origin], [origin, (c, s)]]
                )
            wire = wires[0]
            for row in range(8):
                for bit in range(2):
                    column = (row & ~(1 << wire)) | (bit << wire)
                    supports[row].append((column, small[(row >> wire) & 1][bit]))
        fresh = [[origin for _ in range(8)] for _ in range(8)]
        for row, support in enumerate(supports):
            for column, coefficient in support:
                for output in range(8):
                    fresh[row][output] = add(
                        fresh[row][output], multiply(coefficient, matrix[column][output])
                    )
        matrix = fresh
    if phase is not None:
        z = unit_phase(phase)
        matrix = [[multiply(z, coefficient) for coefficient in row] for row in matrix]
    return matrix


def endpoint(value):
    sign, integer, exponent, bits = value
    require(sign in (0, 1) and integer >= 0 and bits >= 0, "Finite outward interval")
    return Fraction((-1 if sign else 1) * int(integer)) * Fraction(2) ** int(exponent)


def root_upper(squared):
    scaled = squared.numerator << (2 * ROOT_BITS)
    q, remainder = divmod(scaled, squared.denominator)
    root = isqrt(q)
    root += int(root * root != q or remainder != 0)
    result = Fraction(root, 1 << ROOT_BITS)
    require(result * result >= squared, "Independent outward binary root")
    return result


def bound(actual, target, exact_target=False):
    import mpmath as mp

    mp.iv.dps = DPS
    total = mp.iv.mpf(0)
    entries = []
    for row in range(8):
        for column in range(8):
            b = target[row][column]
            if exact_target:
                b = tuple(mp.iv.mpf(x.numerator) / mp.iv.mpf(x.denominator) for x in b)
            a = actual[row][column]
            re, im = a[0] - b[0], a[1] - b[1]
            squared = re * re + im * im
            total += squared
            entries.append(
                dict(
                    lower_exact=pair(max(Fraction(0), endpoint(squared._mpi_[0]))),
                    upper_exact=pair(max(Fraction(0), endpoint(squared._mpi_[1]))),
                )
            )
    upper = max(Fraction(0), endpoint(total._mpi_[1]))
    return dict(
        entries=64,
        entry_squared_enclosures=entries,
        squared_Frobenius_upper_exact=pair(upper),
        operator_error_upper_exact=pair(root_upper(upper)),
        decimal_digits=DPS,
        outward_root_bits=ROOT_BITS,
        phase_optimized=False,
    )


def target_matrix(value):
    require(
        set(value) == {"shape", "binary64_complex_rationals"} and value["shape"] == [8, 8],
        "Original exact full8x8 target",
    )
    rows = value["binary64_complex_rationals"]
    require(type(rows) is list and len(rows) == 64, "All64 target entries")
    entries = []
    for entry in rows:
        require(type(entry) is list and len(entry) == 2, "Original exact complex literal")
        entries.append(tuple(rational(q) for q in entry))
    return [entries[8 * i : 8 * (i + 1)] for i in range(8)]


def seal(output, record, started):
    budget(started)
    encoded = (json.dumps(record, indent=2, allow_nan=False) + "\n").encode()
    budget(started)
    with (output / "manifest.json").open("xb") as stream:
        for offset in range(0, len(encoded), 1 << 20):
            budget(started)
            stream.write(encoded[offset : offset + (1 << 20)])
            budget(started)


def preserve(output, frozen, failure, phase, started):
    if not output.exists():
        return
    try:
        budget(started)
        retain_failure(output, frozen, failure, phase, started)
    except BaseException as sealing_failure:
        marker = output / "failed_unsealed.json"
        if not marker.exists():
            save(
                marker,
                dict(
                    passed=False,
                    receipt_unsealed=True,
                    local_only=True,
                    hard_terminal_budget_exhausted=isinstance(sealing_failure, BudgetCensoredError),
                    budget_censored=isinstance(sealing_failure, BudgetCensoredError)
                    or isinstance(failure, (BudgetCensoredError, TimeoutError)),
                    phase=phase,
                    failure_type=type(failure).__name__,
                    message=str(failure)[:1024],
                    sealing_failure_type=type(sealing_failure).__name__,
                    SDK_calls=0,
                    new_test_credit=0,
                    fixed_receipt_terminal_no_retry=True,
                    no_further_hashing_or_verification=True,
                ),
            )


def retain_failure(output, frozen, failure, phase, started):
    budget(started)
    save(
        output / (phase + "_failure.json"),
        dict(
            type=type(failure).__name__,
            message=str(failure),
            traceback=traceback.format_exc(),
            files_preserved=True,
            fixed_receipt_terminal_no_retry=True,
        ),
    )
    terminal = output / (
        "completion_outcome.json" if (output / "summary.json").exists() else "summary.json"
    )
    save(
        terminal,
        dict(
            passed=False,
            budget_censored=isinstance(failure, (BudgetCensoredError, TimeoutError)),
            local_only=True,
            new_test_credit=0,
            SDK_calls=0,
            fixed_receipt_terminal_no_retry=True,
            full_Gaussian_loader_certified=False,
            native_financial_cost=None,
            Clifford_T_cost=None,
        ),
    )
    if not (output / "manifest.json").exists():
        files = {relative(p): sha(p, started) for p in sorted(output.rglob("*")) if p.is_file()}
        error = None
        try:
            verify(frozen, started)
        except BudgetCensoredError:
            raise
        except BaseException as check:
            error = str(check)
        seal(
            output,
            dict(
                files=files,
                frozen_inputs=frozen,
                manifest_self_hash_excluded=True,
                terminal_record=relative(terminal),
                failure_inputs_verified=error is None,
                verification_error=error,
            ),
            started,
        )
    else:
        raise AssertionError("Failed audit cannot replace an existing or partial manifest")


def prepare(output):
    output = Path(output).resolve()
    require(
        output == RECEIPT.resolve() and not output.exists(), "Fresh exclusive independent audit"
    )
    frozen, started = {}, (time.process_time(), time.monotonic())
    try:
        require(
            Path(sys.executable).resolve() == INTERPRETER.resolve(), "Pinned original interpreter"
        )
        summary = read(SOURCE / "summary.json")
        require(
            not (SOURCE / "failed_unsealed.json").exists()
            and not (SOURCE / "completion_outcome.json").exists()
            and not (SOURCE / "run_failure.json").exists()
            and not (SOURCE / "prepare_failure.json").exists(),
            "No failed or unsealed source",
        )
        require(
            summary["passed"] is True
            and not summary["budget_censored"]
            and summary["actual_SDK_calls"] == 1
            and summary["tests_completed"] == 6,
            "Completed uncensored sole bridge source and six fixtures",
        )
        manifest = SOURCE / "manifest.json"
        record = read(manifest)
        for field in ("files", "frozen_inputs"):
            for path, expected in record[field].items():
                bind(frozen, path, expected)
        bind(frozen, manifest, sha(manifest, started))
        for path in (Path(__file__).resolve(), PREFLIGHT):
            require(
                relative(path) in frozen and frozen[relative(path)] == sha(path, started),
                "Auditor and preflight were frozen before the sole SDK call",
            )
        verify(frozen, started)
        budget(started, admission=True)
        output.mkdir()
        for path in (Path(__file__).resolve(), PREFLIGHT):
            shutil.copy2(path, output / path.name)
            require(
                sha(output / path.name, started) == frozen[relative(path)],
                "Copied independent source",
            )
            bind(frozen, output / path.name, frozen[relative(path)])
        verify(frozen, started)
        save(
            output / "protocol.json",
            dict(
                schema="independent-one-local-U-bridge-audit-v1",
                created_utc=datetime.now(timezone.utc).isoformat(),
                local_only=True,
                frozen_before_operator_evaluation=True,
                frozen_inputs=frozen,
                source_receipt=relative(SOURCE),
                decimal_digits=DPS,
                outward_root_bits=ROOT_BITS,
                local_allowance_exact=pair(ALLOWANCE),
                process_CPU_seconds=CPU,
                admission_CPU_seconds=ADMISSION,
                wall_seconds=WALL,
                fixed_matrices=1,
                entries=64,
                SDK_calls=0,
                audited_helper_imports=0,
                new_test_credit=0,
                requires_root_exclusive_timing_clearance=True,
                no_precision_site_basis_method_retry=True,
            ),
        )
        verify(frozen, started)
        budget(started)
    except BaseException as failure:
        preserve(output, frozen, failure, "prepare", started)
        raise


def run(output):
    output = Path(output).resolve()
    require(
        output == RECEIPT.resolve()
        and not (output / "summary.json").exists()
        and not (output / "operator_audit.json").exists(),
        "Prepared audit cannot retry",
    )
    protocol = read(output / "protocol.json")
    frozen, started = protocol["frozen_inputs"], (time.process_time(), time.monotonic())
    try:
        verify(frozen, started)
        sdk, native, saved_inverse, target, saved = [
            read(SOURCE / name)
            for name in (
                "sdk_operations.json",
                "native_operations.json",
                "native_inverse.json",
                "saved_matrix.json",
                "operator_certificate.json",
            )
        ]
        require(
            fingerprint(native) == fingerprint(recover(sdk)),
            "Independent phase-paid literal bridge identity",
        )
        require(
            fingerprint(saved_inverse)
            == fingerprint(dict(operations=inverted(native["operations"]))),
            "Literal inverse phase/gates",
        )
        require(fingerprint(target) == MATRIX_HASH, "Fixed matrix fingerprint")
        archived = read(PROGRAM / "A04_mps_run001/bond4/structure_plan.json")["transitions"][1]
        require(
            target == archived["completed_local_matrix"] and archived["local_wires"] == [10, 11, 8],
            "Exact full saved bond4 site1 matrix and wires",
        )
        xml = list(ET.parse(SOURCE / "tests.xml").getroot().iter("testcase"))
        require(
            len(xml) == len({(x.attrib.get("classname"), x.attrib["name"]) for x in xml}) == 6
            and not any(
                x.find(tag) is not None for x in xml for tag in ("failure", "error", "skipped")
            ),
            "Six actual distinct fixtures, no new credit",
        )
        budget(started, admission=True)
        operator = expand(native["operations"], started)
        sdk_operator = expand(
            sdk["operations"], started, True, binary64(sdk["sdk_global_phase_exact"])
        )
        restored = expand(native["operations"] + saved_inverse["operations"], started)
        identity = [[(Fraction(i == j), Fraction(0)) for j in range(8)] for i in range(8)]
        comparisons = dict(
            native_to_saved_full_operator=bound(operator, target_matrix(target), True),
            SDK_to_saved_full_operator=bound(sdk_operator, target_matrix(target), True),
            native_to_original_SDK_full_operator=bound(operator, sdk_operator),
            native_literal_inverse_full_operator=bound(restored, identity, True),
        )
        for key, independent in comparisons.items():
            original = saved[key]
            independent_norm = rational(independent["operator_error_upper_exact"])
            original_norm = rational(original["operator_error_upper_exact"])
            require(
                original["entries"] == 64
                and original["phase_optimized"] is False
                and original["full_operator"] is True
                and original["decimal_digits"] == DPS
                and original["outward_root_bits"] == ROOT_BITS,
                "Complete outward original certificate",
            )
            require(
                original_norm >= independent_norm
                and original_norm <= ALLOWANCE
                and original_norm * original_norm
                >= rational(original["squared_Frobenius_upper_exact"]),
                "Saved full bound dominates independent operator bound within fixed allowance",
            )
            require(
                len(original["squared_entry_upper_exact"]) == 64
                and all(
                    rational(upper) >= rational(entry["lower_exact"])
                    for upper, entry in zip(
                        original["squared_entry_upper_exact"],
                        independent["entry_squared_enclosures"],
                    )
                ),
                "All64 saved squared residual entries independently compatible",
            )
        require(
            saved["passed"] is True
            and saved["local_error_allowance_exact"] == pair(ALLOWANCE)
            and saved["paid_scalar_phase_exact"] == native["aggregate_phase_exact"]
            and saved["global_phase_is_not_discarded"] is True,
            "Full paid phase certificate",
        )
        save(
            output / "operator_audit.json",
            dict(
                comparisons=comparisons,
                full_phase_correct_64_entry_audit_passed=True,
                SDK_calls=0,
                helper_imports=0,
                native_slots_including_phase=len(native["operations"]),
                new_test_credit=0,
            ),
        )
        verify(frozen, started)
        save(
            output / "summary.json",
            dict(
                passed=True,
                local_only=True,
                budget_censored=False,
                SDK_calls=0,
                new_test_credit=0,
                source_fixtures_reconciled_without_recredit=6,
                independent_full_phase_correct_local_operator_audit_passed=True,
                independent_literal_inverse_audit_passed=True,
                fixed_receipt_terminal_no_retry=True,
                full_Gaussian_loader_certified=False,
                q10_financial_law_repaired=False,
                native_financial_cost=None,
                Clifford_T_cost=None,
                controlled_phase_cost=None,
                quantum_advantage_established=False,
            ),
        )
        files = {relative(p): sha(p, started) for p in sorted(output.rglob("*")) if p.is_file()}
        verify(frozen, started)
        cpu, wall = budget(started)
        seal(
            output,
            dict(
                files=files,
                frozen_inputs=frozen,
                manifest_self_hash_excluded=True,
                all_inputs_and_bulk_hashes_verified_before_terminal=True,
                process_CPU_seconds_before_terminal=cpu,
                wall_seconds_before_terminal=wall,
            ),
            started,
        )
    except BaseException as failure:
        preserve(output, frozen, failure, "run", started)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "run"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    (prepare if args.phase == "prepare" else run)(args.output)


if __name__ == "__main__":
    main()
