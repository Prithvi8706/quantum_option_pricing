"""Independent arithmetic/hash reconstruction; imports no project producer."""

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[4]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def pair(profile):
    assert profile["serial_depth_upper"] == profile["u"] + profile["cx"]
    return profile["u"], profile["cx"]


def pi_upper():
    # Machin identity; alternating rational arctan series upper endpoints.
    def arctan_bounds(q):
        total = sum(
            (Fraction((-1) ** j, (2 * j + 1) * q ** (2 * j + 1)) for j in range(100)), Fraction(0)
        )
        return total, total + Fraction(1, 201 * q**201)

    low5, high5 = arctan_bounds(5)
    low239, high239 = arctan_bounds(239)
    return 16 * high5 - 4 * low239


def check(archive):
    completion, planned = read(archive / "complete.json"), read(archive / "planned.json")
    assert completion["status"] == "complete"
    hashes = 0
    for name, expected in completion["sha256"].items():
        assert sha(archive / name) == expected, name
        hashes += 1
    for name, expected in completion["input_sha256"].items():
        assert sha(ROOT / name) == expected, name
        hashes += 1
    for name, expected in planned["source_sha256"].items():
        assert sha(ROOT / name) == expected, name
        blob = subprocess.check_output(
            ["git", "show", planned["source_commit"] + ":" + name], cwd=ROOT
        )
        assert blob.replace(b"\r\n", b"\n") == (ROOT / name).read_bytes().replace(b"\r\n", b"\n")
        hashes += 1
    result = read(archive / "results.json")
    assert len(result["rows"]) == 6
    assert {(r["case"], r["route"]) for r in result["rows"]} == {
        (c, r) for c in ("D1", "D2") for r in ("reflection", "raw_parent", "residual")
    }
    output = []
    for row in result["rows"]:
        assert row == read(archive / (row["case"] + "_" + row["route"] + ".json"))
        u, cx = pair(row["a"])
        parts = row["components"]
        lu, lcx = pair(parts["loader"])
        copies = parts["loader_copies"]
        if row["route"] == "reflection":
            su, scx = pair(parts["signal"])
            assert pair(parts["controlled_signal"]) == (5 * su + 9 * scx + 1, 2 * su + 6 * scx)
            ru, rcx = pair(parts["controlled_walk_reflection"])
            count = parts["signal_copies"]
            projectors = [pair(p) for p in parts["controlled_projectors"]]
            assert len(projectors) == count + 1
            assert (u, cx) == (
                copies * lu
                + count * (5 * su + 9 * scx + 1 + ru)
                + sum(p[0] for p in projectors)
                + 2,
                copies * lcx + count * (2 * su + 6 * scx + rcx) + sum(p[1] for p in projectors),
            )
        else:
            emitted = parts["emitted"]
            arithmetic = (emitted["x"] + 9 * emitted["ccx"], emitted["cx"] + 6 * emitted["ccx"])
            assert pair(parts["arithmetic"]) == arithmetic
            assert (u, cx) == (
                arithmetic[0] + copies * lu + parts["selector_h"] + 1,
                arithmetic[1] + copies * lcx,
            )
        assert row["a"] == row["a_inverse"]
        assert pair(row["controlled_a"]) == (5 * u + 9 * cx + 1, 2 * u + 6 * cx)
        assert row["controlled_a"] == row["controlled_a_inverse"]
        zu, zcx = pair(row["controlled_zero"])
        schedule = row["schedule"]
        size, repetitions = schedule["M"], schedule["repetitions"]
        bits = size.bit_length() - 1
        assert size == 2**bits and bits == schedule["phase_qubits"]
        assert repetitions == 17 and schedule["a_calls"] == 17 * (2 * size - 1)
        assert schedule["a_calls"] <= 10_000_000
        assert row["total_allocated_qubits"] == 2 * row["a_qubits"] - 2 + bits
        pairs = bits * (bits - 1) // 2
        for name, (au, acx) in (
            ("control_cancelled", (u, cx)),
            ("controlled", (5 * u + 9 * cx + 1, 2 * u + 6 * cx)),
        ):
            expected = (
                17 * (u + bits + (size - 1) * (2 * au + zu + 3) + bits + 3 * pairs),
                17 * (cx + (size - 1) * (2 * acx + zcx + 1) + 2 * pairs + 3 * (bits // 2)),
            )
            assert pair(row["totals"][name]) == expected
        old, delta = row["historical_resources"], row["reconciliation"]
        assert delta["a_cx_change"] == cx - old["a_cx_projection"]
        assert (
            delta["controlled_total_cx_change"]
            == row["totals"]["controlled"]["cx"] - old["total_cx_projection"]
        )
        assert (
            delta["cancelled_total_cx_change"]
            == row["totals"]["control_cancelled"]["cx"]
            - old["control_cancelled_total_cx_projection"]
        )
        budget, bridge = row["budget"], row["label_bridge"]
        slope = (
            Fraction(budget["sensitivity_upper"])
            if "sensitivity_upper" in budget
            else 2 * Fraction(budget["beta"])
        )
        extra = slope * Fraction(bridge["label_error_upper_rational"])
        assert extra == Fraction(bridge["extra_price_bound_rational"])
        p = pi_upper()
        margin = (
            1
            - Fraction(budget["deterministic_upper"])
            - extra
            - slope * (p / size + p * p / (size * size))
        )
        assert margin > 0 and Fraction(bridge["remaining_price_margin_rational"]) > 0
        output.append(
            dict(
                case=row["case"],
                route=row["route"],
                M=size,
                independently_certified_remaining_margin=float(margin),
                control_cancelled_CX=row["totals"]["control_cancelled"]["cx"],
                allocated_qubits=row["total_allocated_qubits"],
            )
        )
    for comparison in result["comparisons"]:
        chosen = {r["route"]: r for r in result["rows"] if r["case"] == comparison["case"]}
        for ledger, values in comparison["ledgers"].items():
            costs = {k: r["totals"][ledger]["cx"] for k, r in chosen.items()}
            assert values["winner"] == min(costs, key=costs.get)
            assert Fraction(values["reflection_over_residual"]) == Fraction(
                costs["reflection"], costs["residual"]
            )
    assert completion["cpu_seconds"] < planned["cpu_limit_seconds"]
    assert completion["peak_rss_bytes"] < planned["memory_limit_bytes"]
    return dict(
        passed=True,
        checked_hash_bindings=hashes,
        source_commit=planned["source_commit"],
        reviewed_git_head=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        rows=output,
        complete_ledgers=12,
        source_sha256=sha(Path(__file__)),
        scope=(
            "Independent receipt arithmetic, hashes and rational feasibility; "
            "no production reemission or native execution certificate"
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    receipt = check(args.archive)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
