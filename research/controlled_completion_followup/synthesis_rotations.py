"""Synthesize the archived phase envelope; verify with independent interval matrices.

Run as a module. Generation needs pygridsynth==1.1.0; --verify-only needs mpmath.
The exact target is reconstructed from integer rationals, never binary64 angles.
"""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.metadata
import json
from pathlib import Path
import random
import time

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results/controlled_source_completion/cost_v3_phase64"
OUTPUT = ROOT / "results/controlled_completion_followup/synthesis_rotations.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def targets_and_usage():
    rows = json.loads((SOURCE / "ledger.json").read_text())
    targets = {}
    uses = []
    for row in rows:
        tag = "%s_f%d_%s" % (row["model"], row["f"], row["mode"])
        circuit = json.loads((SOURCE / (tag + "_circuit.json")).read_text())
        usage = Counter()
        for phase in circuit["phase_bits"]:
            numerator, denominator = phase["angle_exact_radians"]
            value = abs(Fraction(numerator, 2 * denominator))
            key = "radian_%d_%d" % (value.numerator, value.denominator)
            targets[key] = dict(
                kind="radian", numerator=value.numerator, denominator=value.denominator
            )
            usage[key] += 3 * row["ledger"]["controlled_U_calls"]
        for stage in circuit["qpe_stages"]:
            b = stage["qpe_bits"]
            for gap in range(2, b):
                key = "pi_1_%d" % (2 ** (gap + 1))
                targets[key] = dict(kind="pi", numerator=1, denominator=2 ** (gap + 1))
                usage[key] += 3 * (b - gap) * stage["repetitions"]
        assert sum(usage.values()) == row["ledger"]["unsynthesized_single_qubit_phase_gates"]
        uses.append(dict(tag=tag, usage=dict(usage)))
    return rows, targets, uses


def target_angle(spec, ctx):
    value = ctx.mpf(spec["numerator"]) / spec["denominator"]
    return value * ctx.pi if spec["kind"] == "pi" else value


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def interval_error_squared(spec, gates, dps=120):
    """Directed interval Frobenius norm squared, hence an operator-norm bound.

    The gate string is a matrix product written left to right, so gates execute
    right to left. Global W=exp(i*pi/4)I is included in this certificate.
    """
    iv = mp.iv
    iv.dps = dps
    one, zero = iv.mpc(1), iv.mpc(0)
    rt = iv.sqrt(2)
    omega = iv.mpc(1 / rt, 1 / rt)
    table = {
        "H": [[one / rt, one / rt], [one / rt, -one / rt]],
        "T": [[one, zero], [zero, omega]],
        "S": [[one, zero], [zero, iv.mpc(0, 1)]],
        "X": [[zero, one], [one, zero]],
        "W": [[omega, zero], [zero, omega]],
    }
    result = [[one, zero], [zero, one]]
    for gate in gates:
        if gate not in table:
            raise ValueError("Unknown synthesis token: " + gate)
        result = multiply(result, table[gate])
    angle = target_angle(spec, iv)
    target = [[iv.exp(iv.mpc(0, -angle / 2)), zero], [zero, iv.exp(iv.mpc(0, angle / 2))]]
    squared = iv.mpf(0)
    for i in range(2):
        for j in range(2):
            delta = result[i][j] - target[i][j]
            squared += delta.real**2 + delta.imag**2
    # _mpi_ endpoint is an exact binary rational (sign, mantissa, exponent, bits).
    sign, mantissa, exponent, _ = squared._mpi_[1]
    return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent


def upward_decimal(value, digits=90):
    scale = 10**digits
    integer = -((-value.numerator * scale) // value.denominator)
    return "%d.%0*d" % (integer // scale, digits, integer % scale)


def verify(payload):
    rows, specs, uses = targets_and_usage()
    assert payload["source_ledger_sha256"] == sha(SOURCE / "ledger.json")
    assert payload["usage"] == uses
    assert set(payload["rotations"]) == set(specs)
    epsilon = Fraction(
        1, 4000 * max(r["ledger"]["unsynthesized_single_qubit_phase_gates"] for r in rows)
    )
    for key, spec in specs.items():
        record = payload["rotations"][key]
        assert record["target"] == spec
        squared = interval_error_squared(spec, record["matrix_product_gates"])
        assert squared <= epsilon**2, (key, float(squared), float(epsilon**2))
        assert squared <= Fraction(record["frobenius_error_squared_upper"])
        assert record["t_count"] == record["matrix_product_gates"].count("T")
        assert record["clifford_count"] == sum(
            record["matrix_product_gates"].count(g) for g in "HSX"
        )
    return len(specs)


def main(verify_only=False):
    if verify_only:
        print(
            "Verified %d exact-target interval certificates"
            % verify(json.loads(OUTPUT.read_text()))
        )
        return
    import pygridsynth
    import pygridsynth.ring as ring

    # pygridsynth 1.1.0 uses int.bit_count (Python >=3.10). This equivalent
    # valuation function supports the project's Python 3.9 without editing it.
    ring.ntz = lambda n: 0 if n == 0 else (n & -n).bit_length() - 1
    mp.mp.dps = 120
    rows, specs, uses = targets_and_usage()
    max_rotations = max(r["ledger"]["unsynthesized_single_qubit_phase_gates"] for r in rows)
    eps = mp.mpf(1) / (4000 * max_rotations)
    payload = dict(
        format="verified-rotation-library-v1",
        source_ledger_sha256=sha(SOURCE / "ledger.json"),
        generator="pygridsynth",
        generator_version=importlib.metadata.version("pygridsynth"),
        mpmath_version=mp.__version__,
        generation_decimal_precision=120,
        verification_decimal_precision=120,
        common_operator_epsilon_exact=[1, 4000 * max_rotations],
        requested_generator_epsilon=str(eps / 16),
        usage=uses,
        rotations={},
        semantics=(
            "matrix_product_gates multiply left to right; execute reversed. W is "
            "global exp(i*pi/4). Negative targets use conjugate-transpose of the "
            "complete product; T/S become Tdg/Sdg at identical resource counts. "
            "Remove W physically and track its global phase. "
            "P(theta)=exp(i*theta/2)Rz(theta). The three-phase CP decomposition "
            "thus changes only overall global phase, including at zero control."
        ),
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    random.seed(999)
    base = pygridsynth.gridsynth_gates(mp.mpf(1) / 2, eps / 16)
    payload["conditioning_base_gates"] = base
    for index, (key, spec) in enumerate(specs.items()):
        angle = target_angle(spec, mp.mp)
        random.seed(index)
        before = time.perf_counter()
        # Identity is accepted only through the same interval certificate.
        if interval_error_squared(spec, "") <= Fraction(1, 4000 * max_rotations) ** 2:
            gates = ""
        else:
            # Avoid the pathological near-Clifford thin-grid region in this
            # package version. X A X approximates Rz(-1/2) when A approximates
            # Rz(1/2); compose it with the separately synthesized shifted target.
            gates = pygridsynth.gridsynth_gates(angle + mp.mpf(1) / 2, eps / 16) + "X" + base + "X"
        squared = interval_error_squared(spec, gates)
        assert squared <= Fraction(1, 4000 * max_rotations) ** 2
        record = dict(
            target=spec,
            matrix_product_gates=gates,
            t_count=gates.count("T"),
            clifford_count=sum(gates.count(g) for g in "HSX"),
            global_w_count=gates.count("W"),
            frobenius_error_squared_upper=upward_decimal(squared),
            seed=index,
            generation_seconds=time.perf_counter() - before,
        )
        payload["rotations"][key] = record
        OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
        print(index + 1, len(specs), key, "T=" + str(record["t_count"]), flush=True)
    payload["generation_seconds"] = time.perf_counter() - start
    payload["verified_rotations"] = verify(payload)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    main(parser.parse_args().verify_only)
