"""Prospectively frozen finite metadata equivalence check, without scientific work."""

import argparse
import ast
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUTPUT = ROOT / "results/limitation_program_20261001/A13_continuation_20261004_membership_QA_run001"
ORIGINAL = ROOT / "research/limitation_program_20261001/audit_exp_frontier_recovery_v5.py"
ORIGINAL_SHA = "c34f7096f783a61caa586c4e3f30067304da3d457626b367fd609ffebc2b2593"
PROFILE_MANIFEST = ROOT / "results/limitation_program_20261001/A13_metadata_validation_profile_run001/manifest.json"
PROFILE_SHA = "44ab18466e03906e05f6b370aaf7a6791ccfeda811ea7d32870b4a05e66a195f"
SCHEMA = "a13-membership-index-finite-qa-preflight-v1"
STARTED_WALL = time.monotonic()
STARTED_CPU = time.process_time()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def budget(*, work=False):
    cpu, wall = time.process_time() - STARTED_CPU, time.monotonic() - STARTED_WALL
    require(cpu < (15 if work else 25) and wall < (65 if work else 90), "Fixed finite QA budget")
    return {"process_CPU_seconds": cpu, "wall_seconds": wall}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    budget()
    (OUTPUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def exact_legacy_predicate():
    require(sha(ORIGINAL) == ORIGINAL_SHA, "Original V5 bytes before isolated predicate extraction")
    tree = ast.parse(ORIGINAL.read_text(encoding="utf-8"))
    selected = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "selected_inputs"]
    require(len(selected) == 1, "One original selected_inputs definition")
    calls = [
        node for node in ast.walk(selected[0])
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "any"
    ]
    require(len(calls) == 1, "One original existential membership predicate")
    expression = ast.Expression(body=calls[0])
    require(
        {node.id for node in ast.walk(expression) if isinstance(node, ast.Name)}
        == {"any", "row", "actual", "ROOT", "expected", "records"},
        "Exact isolated predicate variable set",
    )
    code = compile(expression, str(ORIGINAL), "eval")
    digest = hashlib.sha256(ast.dump(expression, include_attributes=False).encode("utf-8")).hexdigest()

    def original(records, path, expected):
        namespace = {"any": any, "records": records, "actual": ROOT / path, "ROOT": ROOT, "expected": expected}
        namespace["__builtins__"] = {}
        return eval(code, namespace)

    return original, digest


def corpus():
    first, second = "a" * 64, "b" * 64
    atoms = [
        ("research/membership/p", first),
        ("research/membership/p", second),
        ("research/membership/q", first),
        ("research/Membership/p", first),
        ("research/membership/p/extra", first),
        ("research\\membership\\p", first),
        ("results/archive/executed_p", first),
        ("C:/external/membership/p", first),
    ]
    queries = [
        ("research/membership/p", first), ("research/membership/p", second),
        ("research/membership/q", first), ("research/membership/q", second),
        ("research/Membership/p", first), ("research/membership/p/extra", first),
        ("research/membership/missing", first), ("results/archive/executed_p", first),
        ("results/archive/p", first), ("research/membership/p", "A" * 64),
        ("research/membership/p", "c" * 64), ("research/membership/", first),
    ]
    return atoms, queries


def fixed_checks(module, original):
    atoms, queries = corpus()
    counts = {"corpora": 0, "predicate_comparisons": 0, "full_record_retention_checks": 0,
              "witness_position_checks": 0, "invalid_input_rejections": 0, "snapshot_guards": 0}
    for length in range(5):
        for sequence in itertools.product(range(len(atoms)), repeat=length):
            budget(work=True)
            records = [
                {"owner_manifest": "synthetic_owner_" + str(number % 2),
                 "source_map": ("files", "frozen_inputs", "external_runtime_inputs")[number % 3],
                 "original_key": "synthetic_original_" + str(number),
                 "verified_input_path": atoms[atom][0], "original_expected_sha256": atoms[atom][1],
                 "expected_hash_waived": False, "archived_equal_SHA_route": bool(number % 2)}
                for number, atom in enumerate(sequence)
            ]
            indexed = module.build_verified_membership_index(records)
            require([dict(row) for row in indexed.records] == records, "Full rows and duplicate order retained")
            counts["full_record_retention_checks"] += 1
            for path, expected in queries:
                budget(work=True)
                # Structural oracle enumerates every matching original position; no index/grouping.
                witnesses = tuple(
                    position for position in range(len(records))
                    if records[position]["verified_input_path"] == path
                    and records[position]["original_expected_sha256"] == expected
                )
                require(indexed.witnesses(path, expected) == witnesses, "All exact duplicate witness positions")
                require(indexed.contains(path, expected) == original(records, path, expected) == bool(witnesses),
                        "Indexed/original/independent finite predicate equality")
                counts["witness_position_checks"] += 1
                counts["predicate_comparisons"] += 1
            counts["corpora"] += 1
    for records in ([{}], [{"verified_input_path": 1, "original_expected_sha256": "a"}],
                    [{"verified_input_path": "p", "original_expected_sha256": None}], [None]):
        try:
            module.build_verified_membership_index(records)
        except ValueError:
            counts["invalid_input_rejections"] += 1
        else:
            raise ValueError("Malformed metadata record unexpectedly accepted")
    original_row = {"verified_input_path": "p", "original_expected_sha256": "a", "other_metadata": "retained"}
    indexed = module.build_verified_membership_index([original_row, dict(original_row)])
    original_row["verified_input_path"] = "changed"
    require(indexed.witnesses("p", "a") == (0, 1) and indexed.records[0]["verified_input_path"] == "p",
            "Invocation snapshot unaffected by original-row mutation")
    counts["snapshot_guards"] += 1
    for mutation in (lambda: indexed.records[0].__setitem__("verified_input_path", "changed"),
                     lambda: indexed.positions.__setitem__(("p", "a"), ())):
        try:
            mutation()
        except (TypeError, AttributeError):
            counts["snapshot_guards"] += 1
        else:
            raise ValueError("Read-only snapshot unexpectedly mutable")
    require(counts == {"corpora": 4681, "predicate_comparisons": 56172, "full_record_retention_checks": 4681,
                       "witness_position_checks": 56172, "invalid_input_rejections": 4, "snapshot_guards": 3},
            "Exact preregistered finite counts")
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", type=Path, required=True)
    arguments = parser.parse_args()
    freeze = json.loads(arguments.freeze.read_text(encoding="utf-8"))
    require(freeze["schema"] == "a13-membership-index-finite-qa-frozen-v1" and freeze["static_review_passed"] is True,
            "Prospective static reviewer freeze")
    expectations = freeze["expected_files"]
    expected_set = {
        (HERE / name).relative_to(ROOT).as_posix() for name in (
            "verified_membership_index_v1.py", "membership_index_finite_qa_v1.py",
            "MEMBERSHIP_INDEX_FINITE_QA_PREFLIGHT.md", "membership_index_finite_qa_preflight.json")
    } | {ORIGINAL.relative_to(ROOT).as_posix(), PROFILE_MANIFEST.relative_to(ROOT).as_posix()}
    require(set(expectations) == expected_set, "Exact six prospective pins, no expectation additions")
    for key, expected in expectations.items():
        budget()
        require(sha(ROOT / key) == expected, "Fresh actual prospective byte admission: " + key)
    require(expectations[ORIGINAL.relative_to(ROOT).as_posix()] == ORIGINAL_SHA
            and expectations[PROFILE_MANIFEST.relative_to(ROOT).as_posix()] == PROFILE_SHA, "Exact historical pin constants")
    policy = json.loads((HERE / "membership_index_finite_qa_preflight.json").read_text(encoding="utf-8"))
    require(policy["schema"] == SCHEMA and policy["limits_CPU_wall"] == [25, 90]
            and policy["selected_work_CPU_wall"] == [15, 65]
            and policy["counts"] == [4681, 56172, 4, 3], "Exact policy and frozen counts")
    require(time.process_time() - STARTED_CPU < 20, "Fixed20CPU admission cutoff")
    require(not OUTPUT.exists(), "Fresh finite-QA output directory")
    OUTPUT.mkdir()
    write("FAILED_UNSEALED.json", {"failed": True, "authoritative_until_terminal_manifest": True,
                                   "scope": "finite_metadata_equivalence_only", "scientific_execution": False})
    try:
        write("run_started.json", {"expected_files": expectations, "freeze_SHA256": sha(arguments.freeze),
                                   "interpreter": sys.executable, "version": sys.version,
                                   "runtime_scope": "launcher_information_only_no_complete_runtime_provenance_claim"})
        for key in expected_set:
            if key.startswith(HERE.relative_to(ROOT).as_posix() + "/"):
                (OUTPUT / Path(key).name).write_bytes((ROOT / key).read_bytes())
        specification = importlib.util.spec_from_file_location("a13_verified_membership_finite_candidate", HERE / "verified_membership_index_v1.py")
        module = importlib.util.module_from_spec(specification)
        sys.modules[specification.name] = module
        specification.loader.exec_module(module)
        original, ast_digest = exact_legacy_predicate()
        counts = fixed_checks(module, original)
        require(not any(name.startswith("research.limitation_program_20261001.audit_") for name in sys.modules)
                and "mpmath" not in sys.modules, "No historical/scientific module import")
        for key, expected in expectations.items():
            require(sha(ROOT / key) == expected, "Fresh terminal prospective bytes: " + key)
        summary = {"schema": "a13-membership-index-finite-qa-summary-v1", "passed": True,
                   "completed": True, "budget_censored": False, "counts": counts,
                   "isolated_original_predicate_AST_SHA256": ast_digest,
                   "general_equivalence_scope": "fixed_complete_typed_metadata_record_snapshot",
                   "all20_approval": False, "original_audit005_remains_FAILED_UNSEALED": True,
                   "scientific_execution": False, "mathematical_row_approval": False,
                   "new_fixture_credit": 0, "new_gate_replays": 0, "new_price_samples": 0,
                   "adoption": False, "quantum_advantage_established": False,
                   "operational_speedup_or_complete_budget_fit_claim": False, "budget": budget()}
        write("summary.json", summary)
        write("completion_outcome.json", summary)
        owned = {path.name: sha(path) for path in OUTPUT.iterdir() if path.name != "FAILED_UNSEALED.json"}
        manifest = {"schema": "a13-membership-index-finite-qa-manifest-v1", "files": owned,
                    "frozen_inputs": expectations, "external_runtime_inputs": {},
                    "runtime_scope": "no_complete_runtime_provenance_claim", "manifest_self_hash_excluded": True,
                    "passed": True, "scientific_execution": False, "new_fixture_credit": 0,
                    "all20_approval": False, "budget": budget()}
        require(len(owned) <= 12 and sum(path.stat().st_size for path in OUTPUT.iterdir()) < 2**20, "Fixed12files/1MiB retained cap")
        write("manifest.json", manifest)
        (OUTPUT / "FAILED_UNSEALED.json").unlink()
        print(json.dumps({"passed": True, "counts": counts, "manifest_SHA256": sha(OUTPUT / "manifest.json"),
                          "budget": budget(), "receipt": OUTPUT.relative_to(ROOT).as_posix()}))
    except BaseException as error:
        failure = {"failed": True, "passed": False, "authoritative": True, "error_type": type(error).__name__,
                   "error": str(error), "traceback": traceback.format_exc(), "scientific_execution": False,
                   "all20_approval": False, "new_fixture_credit": 0}
        (OUTPUT / "FAILED_UNSEALED.json").write_text(json.dumps(failure, indent=2) + "\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
