"""Independent invariant checks for wave scheduling and modular range analysis."""

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_priority_completion.range_audit import Audit
from research.controlled_source_completion.ir import Graph, evaluate


ROOT = Path("results/controlled_priority_completion")


def exhaustive_ranges():
    graph = Graph(2, 3)
    a, b = graph.input("a", 5), graph.input("b", 5)
    ids = [a, b, graph.const_int(-16), graph.const_int(15), graph.const_int(0)]
    for x in (a, b):
        ids.extend((graph.pos(x), graph.neg(x), graph.sqrt(x), graph.node("msb", (x,))))
        ids.append(graph.select(graph.lt(x, graph.const_int(0)), graph.neg(x), x))
        for signed in (False, True):
            for width in (1, 3, 5):
                for shift in (-7, -2, 0, 2, 7):
                    ids.append(graph.bits(x, shift, width=width, signed=signed))
    graph.tables["test"] = [[0, -16], [15, 1], [-2, 7], [9, -9]]
    lookup = graph.node("lookup", (a,), dict(table="test", bits=2), nout=2)
    ids.extend(lookup)
    rng = random.Random(2026092803)
    for j in range(120):
        x, y = rng.choice(ids), rng.choice(ids)
        if j % 11 == 0:
            out = graph.add(x, y)
        elif j % 11 == 1:
            out = graph.sub(x, y)
        elif j % 11 == 2:
            out = graph.mul(x, y)
        elif j % 11 == 3:
            out = graph.mul(x, x)
        elif j % 11 == 4:
            out = graph.node("cmul", (x,), dict(c=rng.randrange(-20, 21)))
        elif j % 11 == 5:
            out = graph.lt(x, y)
        elif j % 11 == 6:
            out = graph.div(x, y)
        elif j % 11 == 7:
            out = graph.shift(x, y)
        elif j % 11 == 8:
            out = graph.minimum(x, y)
        elif j % 11 == 9:
            out = graph.maximum(x, y)
        else:
            out = graph.select(x, x, y)
        ids.append(out)
    graph.outputs = {"last": ids[-1]}
    data = graph.as_dict()
    audit = Audit(data).run()
    checked = 0
    for a in range(32):
        for b in range(32):
            _, trace = evaluate(data, dict(a=a, b=b), trace=True)
            for ident, raw in enumerate(trace):
                signed = raw if raw < 16 else raw - 32
                lo, hi = audit.bounds[ident]
                assert lo <= signed <= hi, (a, b, ident, signed, (lo, hi))
                checked += 1
    return dict(
        width=5,
        fraction_bits=2,
        inputs=1024,
        nodes=len(graph.nodes),
        enclosed_values=checked,
        scope=(
            "Exhaustive finite primitive graph, including signed wrap and shifts; "
            "supplements proof review of financial structural witnesses."
        ),
    )


def audit_schedule(path):
    schedule = json.loads(path.read_text())
    source_file = Path(schedule["source_manifest"])
    assert hashlib.sha256(source_file.read_bytes()).hexdigest() == schedule["source_sha256"]
    source = json.loads(source_file.read_text())
    metadata = entries(source)
    w = source["word_width"]
    prefix = (source["values"] + len(source["outputs"])) * w
    ready = {out for node in source["inputs"] for out in node["out"]}
    seen = set()
    max_scratch = 0
    total_T_depth, total_depth = 0, 0
    for group in schedule["groups"]:
        cursor = prefix
        occupied = set()
        rounds = defaultdict(set)
        occurrences = Counter()
        outputs = set()
        td, depth = 0, 0
        for index in group["call_indices"]:
            assert index not in seen
            seen.add(index)
            call = source["forward_calls"][index]
            assert set(call["args"]) <= ready
            assert not set(call["out"]) & (ready | outputs)
            outputs.update(call["out"])
            arity, nout = len(call["args"]), len(call["out"])
            resources = metadata[call["leaf"]]["resources"]
            mapping = []
            for wire in range(resources["qubits"]):
                if arity * w <= wire < (arity + nout) * w:
                    mapping.append(call["out"][(wire - arity * w) // w] * w + wire % w)
                else:
                    mapping.append(cursor + wire - (nout * w if wire >= (arity + nout) * w else 0))
            wire_set = set(mapping)
            assert len(wire_set) == len(mapping)
            assert not wire_set & occupied
            occupied.update(wire_set)
            for j, value in enumerate(call["args"]):
                occurrence = occurrences[value]
                occurrences[value] += 1
                wires = set(range(value * w, (value + 1) * w))
                wires.update(range(cursor + j * w, cursor + (j + 1) * w))
                assert len(wires) == 2 * w
                assert not rounds[occurrence] & wires
                rounds[occurrence].update(wires)
            cursor += resources["qubits"] - nout * w
            td = max(td, resources["t_depth"])
            depth = max(depth, resources["clifford_t_depth"])
        ready |= outputs
        copies = max(occurrences.values(), default=0)
        assert copies == group["copy_rounds"]
        assert cursor - prefix == group["private_scratch_qubits"]
        assert td == group["t_depth"]
        assert depth + 2 * copies == group["clifford_t_depth"]
        total_T_depth += td
        total_depth += depth + 2 * copies
        max_scratch = max(max_scratch, cursor - prefix)
    assert seen == set(range(len(source["forward_calls"])))
    result = schedule["resources"]
    assert result["logical_qubits"] == prefix + max_scratch
    assert result["t_depth"] == 2 * total_T_depth
    assert result["clifford_t_depth"] == (
        2 * total_depth + max(Counter(source["outputs"].values()).values(), default=0)
    )
    for field in ("t_count", "ccx", "clifford_cx", "clifford_h", "x", "source_gates"):
        assert result[field] == source["resources"][field]
    return dict(
        artifact=path.as_posix(),
        calls=len(seen),
        groups=len(schedule["groups"]),
        all_private_workspaces_disjoint=True,
        shared_control_copy_rounds_explicitly_colored=True,
        counts_depth_and_space_reconciled=True,
    )


def main():
    ranges = exhaustive_ranges()
    schedules = []
    for folder in (ROOT / "parallel_v1", ROOT / "range_parallel_v1"):
        if not folder.exists():
            continue
        for path in folder.rglob("*.json"):
            data = json.loads(path.read_text())
            if (
                isinstance(data, dict)
                and data.get("format") == "clean-xor-parallel-wave-schedule-v1"
            ):
                schedules.append(audit_schedule(path))
    result = dict(
        reviewer=(
            "independent estimator agent reviewing compiler/range components authored by others"
        ),
        generic_range_check=ranges,
        schedules=schedules,
        joint_arithmetic_review=dict(
            status="passed for the stated joint same-digital-policy finite-path expectation",
            source_sha256=hashlib.sha256(
                Path("research/controlled_priority_completion/range_joint_arithmetic.py").read_bytes()
            ).hexdigest(),
            artifact_sha256=hashlib.sha256(
                (ROOT / "range_joint_arithmetic.json").read_bytes()
            ).hexdigest(),
            hardened_premises=[
                "exact raw exponential input, exponent and reduced-argument domains",
                "expected absolute digital normal below two",
                "source stock, forward multiplier and digital baseline caps",
            ],
            excluded_claims=[
                "old real-policy baseline equivalence",
                "regret or baseline mean confidence",
                "tight second-moment transfer",
                "end-to-end advantage",
            ],
        ),
        status=(
            "passed; does not review the reviewer's own estimator or establish "
            "financial approximation accuracy"
        ),
    )
    (ROOT / "review_compiler.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(range_values=ranges["enclosed_values"], schedules=len(schedules))))


if __name__ == "__main__":
    main()
