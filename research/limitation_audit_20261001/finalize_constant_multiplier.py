"""Verify saved constant-multiplier evidence and record a fresh local snapshot."""

import ast
from collections import Counter
from datetime import datetime, timezone
from functools import cache
import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform

from research.controlled_priority_completion.parallel_source import entries
from research.controlled_source_completion.compiler import resolve_library
from research.controlled_source_completion.constant_multiplier import has_zero_low_proof


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "results/limitation_audit_20261001"
OUT = AUDIT / "constant_multiplier_v1"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


@cache
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_new(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, indent=2, allow_nan=False) + "\n")


def check_schedule(source, schedule):
    leaves = entries(source)
    calls = source["forward_calls"]
    w = source["word_width"]
    seen, levels = set(), {v: 0 for n in source["inputs"] for v in n["out"]}
    for index, call in enumerate(calls):
        level = 1 + max((levels[v] for v in call["args"]), default=0)
        for value in call["out"]:
            assert value not in levels
            levels[value] = level
    for group in schedule["groups"]:
        batch = [calls[i] for i in group["call_indices"]]
        assert len(batch) == len(set(group["call_indices"]))
        assert not seen.intersection(group["call_indices"])
        seen.update(group["call_indices"])
        rs = [leaves[c["leaf"]]["resources"] for c in batch]
        scratch = sum(r["qubits"] - len(c["out"]) * w for c, r in zip(batch, rs))
        assert scratch == group["private_scratch_qubits"]
        assert all(levels[v] == group["wave"] for c in batch for v in c["out"])
        copies = max(Counter(v for c in batch for v in c["args"]).values(), default=0)
        assert group["copy_rounds"] == copies
        assert group["t_depth"] == max(r["t_depth"] for r in rs)
        assert group["clifford_t_depth"] == max(r["clifford_t_depth"] for r in rs) + 2 * copies
    assert seen == set(range(len(calls)))
    assert [g["wave"] for g in schedule["groups"]] == sorted(g["wave"] for g in schedule["groups"])
    retained = (source["values"] + len(source["outputs"])) * w
    actual = retained + max(g["private_scratch_qubits"] for g in schedule["groups"])
    assert actual == schedule["resources"]["logical_qubits"] <= schedule["qubit_cap"]
    assert schedule["resources"]["t_depth"] == 2 * sum(g["t_depth"] for g in schedule["groups"])
    output_copy = max(Counter(source["outputs"].values()).values(), default=0)
    assert schedule["resources"]["clifford_t_depth"] == output_copy + 2 * sum(
        g["clifford_t_depth"] for g in schedule["groups"]
    )
    assert schedule["resources"]["t_count"] == 2 * sum(
        leaves[c["leaf"]]["resources"]["t_count"] for c in calls
    )
    return leaves


def check_case(case, source_root):
    name = case["case"]
    original = source_root / name
    target = read(original / "target.json")
    old = read(original / "source.json")
    old_library = resolve_library(old)
    baseline = read(original / "schedule_capped.json")
    assert case == read(OUT / name / "comparison.json")
    assert case["baseline"] == baseline["resources"]
    for kind in ("target", "source"):
        assert case["original_" + kind + "_sha256"] == digest(original / (kind + ".json"))
    nodes = [n for n in target["nodes"] if n["op"] != "input"]
    producers = {v: n for n in target["nodes"] for v in n["out"]}
    fixed_diagnostics = []
    reused = set()
    for trial in case["all_candidates"]:
        path = OUT / name / trial["strategy"]
        source = read(path / "source.json")
        library = resolve_library(source)
        schedule = read(path / "schedule_capped.json")
        assert digest(path / "target.json") == digest(original / "target.json")
        assert schedule["resources"] == trial["candidate"]
        assert (
            schedule["qubit_cap"] == trial["qubit_cap"] == baseline["resources"]["logical_qubits"]
        )
        for field in ("word_width", "fraction_bits", "values", "inputs", "outputs"):
            assert source[field] == old[field]
        leaves = check_schedule(source, schedule)
        assert len(source["forward_calls"]) == len(old["forward_calls"]) == len(nodes)
        changes = 0
        for node, before, after in zip(nodes, old["forward_calls"], source["forward_calls"]):
            assert {k: v for k, v in before.items() if k != "leaf"} == {
                k: v for k, v in after.items() if k != "leaf"
            }
            if before["leaf"] == after["leaf"]:
                entry = leaves[after["leaf"]]
                for file in (after["leaf"] + ".json", entry["gate_file"]):
                    assert digest(old_library / file) == digest(library / file)
                reused.add(after["leaf"])
            else:
                assert node["params"].get("c") == 762123384786
                assert has_zero_low_proof(node, producers, 40)
                entry = leaves[after["leaf"]]
                assert entry["input_contract"] == {"zero_low_bits": 40}
                assert entry["spec"]["strategy"] == trial["strategy"]
                assert digest(library / entry["gate_file"]) == entry["sha256"]
                changes += 1
        assert changes == trial["proved_calls"] == len(read(path / "input_proofs.json"))
        fixed_scratch = max(
            sum(
                leaves[source["forward_calls"][i]["leaf"]]["resources"]["qubits"]
                - len(source["forward_calls"][i]["out"]) * source["word_width"]
                for i in group["call_indices"]
            )
            for group in baseline["groups"]
        )
        fixed_qubits = (source["values"] + len(source["outputs"])) * source[
            "word_width"
        ] + fixed_scratch
        fixed_diagnostics.append(
            dict(
                strategy=trial["strategy"],
                logical_qubits=fixed_qubits,
                within_cap=fixed_qubits <= trial["qubit_cap"],
                scope="Fixed old batches: arithmetic-only diagnostic, not the accepted schedule",
            )
        )
    selected = min(
        case["all_candidates"],
        key=lambda c: (
            c["repacked_t_depth"],
            c["candidate"]["t_count"],
            c["candidate"]["logical_qubits"],
        ),
    )
    assert selected == case["best"]
    assert selected["repacked_t_depth"] < case["baseline"]["t_depth"]
    assert len(case["replays"]) == (3 if name == "B4x12" else 1)
    for replay in case["replays"]:
        assert replay["passed"] and replay["actual"]["all_input_and_workspace_bits_restored"]
        assert replay["actual"]["values"] == replay["expected"]
        assert replay["negative_operands"] > 0
    archived = read(original / "comparison.json")["archived_baseline"]
    return dict(
        case=name,
        reused_leaf_keys=len(reused),
        changed_calls=selected["proved_calls"],
        accepted_t_depth=selected["repacked_t_depth"],
        further_depth_reduction=1 - selected["repacked_t_depth"] / case["baseline"]["t_depth"],
        depth_gain_vs_stage_a=archived["t_depth"] / selected["repacked_t_depth"],
        t_count_reduction_vs_stage_a=1 - selected["candidate"]["t_count"] / archived["t_count"],
        full_replays=len(case["replays"]),
        fixed_batch_diagnostics=fixed_diagnostics,
    )


def run():
    summary, protocol = read(OUT / "summary.json"), read(OUT / "protocol.json")
    assert summary["passed"]
    source_root = ROOT / protocol["source_root"].replace("\\", "/")
    producer = ROOT / "research/limitation_audit_20261001/experiment_constant_multiplier.py"
    executed = OUT / "executed_experiment_constant_multiplier.py"
    assert digest(executed) == protocol["producer_sha256"]
    assert ast.dump(ast.parse(executed.read_text())) == ast.dump(ast.parse(producer.read_text()))
    cases = [check_case(case, source_root) for case in summary["cases"]]
    previous_manifest = AUDIT / "execution_manifest_v1.json"
    historical = read(previous_manifest)
    changed = [name for name, sha in historical["files"].items() if digest(ROOT / name) != sha]
    assert changed == ["docs/limitation_audit_20261001/README.md"]
    tests = [
        "research/limitation_audit_20261001/test_constant_multiplier.py",
        "research/limitation_audit_20261001/test_carry_save_multiplier.py",
        "research/limitation_audit_20261001/test_budget_schedule.py",
        "research/controlled_source_completion/test_completion.py",
        "research/controlled_priority_completion/test_parallel_source.py",
    ]
    save_new(
        OUT / "verification.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            artifact_checks_passed=True,
            cases=cases,
            executed_producer_sha256=digest(executed),
            maintained_producer_sha256=digest(producer),
            producer_asts_identical=True,
            tests=dict(
                command=".context/frontier_t0_env/Scripts/python.exe -m pytest "
                + " ".join(tests)
                + " -q",
                observed_passes=61,
                new_tests=16,
                observed_warnings=3,
                observed_seconds=42.20,
                warning_kind="Pre-existing Qiskit QFT PendingDeprecationWarning",
                evidence="Observed terminal run; this finalizer checks artifacts, "
                "not test execution",
            ),
            ruff="The four new Python files passed ruff check",
            python_version=platform.python_version(),
            packages={
                name: metadata.version(name)
                for name in ("numpy", "numba", "scipy", "qiskit", "pytest")
            },
            historical_manifest_sha256=digest(previous_manifest),
            changed_since_historical_snapshot=changed,
            scope="Exact arithmetic-source improvement. Full-source input replays are sampled. "
            "No physical timing, continuous-price certification or quantum advantage established.",
        ),
    )
    paths = [p for p in OUT.rglob("*") if p.is_file()]
    paths += [
        producer,
        Path(__file__),
        ROOT / tests[0],
        ROOT / "research/controlled_source_completion/constant_multiplier.py",
        ROOT / "docs/limitation_audit_20261001/CONSTANT_MULTIPLIER_RESULT.md",
        ROOT / "docs/limitation_audit_20261001/README.md",
        previous_manifest,
    ]
    hashes = {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(set(paths))}
    save_new(
        OUT / "manifest.json",
        dict(
            format="sha256-constant-multiplier-snapshot-v1",
            files=hashes,
            note="Previous manifests remain historical snapshots. This snapshot records the "
            "updated README and the constant-multiplier implementation, report and evidence.",
        ),
    )
    print(
        "Verified eight capped candidates and four saved full-source replays; hashed",
        len(hashes),
        "files",
    )
    print(json.dumps(cases, indent=2))


if __name__ == "__main__":
    run()
