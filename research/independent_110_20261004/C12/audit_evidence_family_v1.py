"""Bounded C12 inventory audit: AST/JSON/byte checks, no arithmetic backend replay."""
import time
STARTED = time.monotonic()
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "results/independent_110_20261004/C12/audit_run001"
DOC = ROOT / "docs/independent_110_20261004/C12"
FAILURE = OUT / "FAILED_UNSEALED.json"
DATA = HERE / "evidence_family_data_v1.json"
MAX_INPUT = 16 * 2**20
MAX_FILE = 4 * 2**20
MAX_OUTPUT = 8 * 2**20

CORPUS = [
    "docs/independent_110_20261004/inventory_run001/WORK_LIST.txt",
    "docs/limitation_audit_20261001/implementation_plan/roadmap.json",
    "docs/limitation_audit_20261001/implementation_plan/CONTRACT.md",
    "docs/limitation_audit_20261001/CONTRACT_AND_EVIDENCE.md",
    "manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md",
    "manuscript/advantage-frontier-2026-09-23/STAGE_A_RESULTS.md",
    "docs/research_investigation/2026-09-23/ERRATA.md",
    "docs/research_investigation/2026-09-23/H1_FALSIFIER_RESULTS.md",
    "docs/antithetic_feasibility/RESULTS.md", "docs/compound_feasibility/RESULTS.md",
    "docs/controlled_residual_feasibility/RESULTS.md",
    "docs/controlled_source_completion/RESULTS.md", "docs/controlled_priority_completion/RESULTS.md",
    "research/antithetic_feasibility/compile_blocks.py", "research/antithetic_feasibility/reversible.py",
    "research/antithetic_feasibility/estimator.py", "research/compound_feasibility/compile.py",
    "research/compound_feasibility/reversible.py", "research/compound_feasibility/model.py",
    "research/controlled_residual_feasibility/cost.py", "research/controlled_residual_feasibility/bounds.py",
    "research/controlled_source_completion/run.py", "research/controlled_source_completion/finance.py",
    "research/controlled_source_completion/compiler.py", "research/controlled_source_completion/ir.py",
    "research/controlled_source_completion/primitives.py", "research/controlled_source_completion/exact_lookup.py",
    "research/controlled_source_completion/carry_save_multiplier.py",
    "research/controlled_source_completion/constant_multiplier.py",
    "research/controlled_priority_completion/ranged_run.py", "research/controlled_priority_completion/ranged_multiplier.py",
    "research/advantage_frontier_20260923/barrier_oracle_depth.py",
    "research/journal_sprint/reversible_fixed_point.py", "research/stronger_arithmetic/circuits.py",
    "research/controlled_completion_followup/truncated_multiplier.py",
    "research/controlled_completion_followup/test_truncated_multiplier.py",
    "research/limitation_audit_20261001/experiment_lookup.py", "research/limitation_audit_20261001/test_lookup.py",
    "research/limitation_audit_20261001/experiment_multiplier.py", "research/limitation_audit_20261001/test_carry_save_multiplier.py",
    "research/limitation_audit_20261001/experiment_constant_multiplier.py", "research/limitation_audit_20261001/test_constant_multiplier.py",
    "research/limitation_audit_20261001/experiment_mcx_cleanup.py",
    "results/limitation_audit_20261001/lookup_v2/protocol.json", "results/limitation_audit_20261001/lookup_v2/summary.json",
    "results/limitation_audit_20261001/multiplier_v2/protocol.json", "results/limitation_audit_20261001/multiplier_v2/summary.json",
    "results/limitation_audit_20261001/constant_multiplier_v1/protocol.json",
    "results/limitation_audit_20261001/constant_multiplier_v1/summary.json",
    "results/limitation_audit_20261001/constant_multiplier_v1/verification.json",
    "results/limitation_audit_20261001/constant_multiplier_v1/executed_experiment_constant_multiplier.py",
    "results/limitation_audit_20261001/mcx_cleanup_v1/result.json", "results/limitation_audit_20261001/mcx_cleanup_v1/mcx5.qasm",
    "research/independent_110_20261004/C12/peer_run001/selected_evidence.json",
    "docs/independent_110_20261004/C12/peer_run001/ARITHMETIC_EVIDENCE_STATIC_REVIEW.md",
]
for branch in ("lookup_v2", "multiplier_v2", "constant_multiplier_v1"):
    for case in ("B4x12", "B8x52"):
        middle = "/signed-digit-carry-save" if branch == "constant_multiplier_v1" else ""
        CORPUS.append(f"results/limitation_audit_20261001/{branch}/{case}{middle}/target.json")
CORPUS += [DATA.relative_to(ROOT).as_posix(), Path(__file__).resolve().relative_to(ROOT).as_posix()]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def guard():
    require(time.process_time() < 30 and time.monotonic() - STARTED < 90,
            "Frozen30processCPU/90script-wall metadata cap")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    guard()
    require(path.resolve(strict=True) == path and not path.is_symlink(), "Canonical non-link input")
    before = path.stat()
    require(before.st_size <= MAX_FILE, "Frozen4MiB individual metadata cap")
    value = path.read_bytes()
    after = path.stat()
    require((before.st_size, before.st_mtime_ns, before.st_ino) ==
            (after.st_size, after.st_mtime_ns, after.st_ino), "Stable read bytes")
    return value


def load(path):
    return json.loads(read(path).decode("utf-8"))


def write(path, data):
    guard()
    encoded = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(len(encoded) <= MAX_OUTPUT, "Frozen output cap")
    with path.open("xb") as stream:
        stream.write(encoded)


def prepare():
    require(not OUT.exists(), "Fresh C12 receipt required")
    require(len(CORPUS) == len(set(CORPUS)) and len(CORPUS) <= 80, "Fixed unique corpus")
    pins = {}
    for key in CORPUS:
        data = read(ROOT / key)
        pins[key] = {"sha256": digest(data), "bytes": len(data)}
    require(sum(v["bytes"] for v in pins.values()) <= MAX_INPUT, "Frozen16MiB corpus cap")
    OUT.mkdir(parents=True)
    write(OUT / "protocol.json", {
        "schema": "c12-preregistered-evidence-inventory-v1", "corpus_sha256": pins,
        "corpus_count": len(pins), "scope": "Six original constructions, three contract families, current reference topology and four existing arithmetic records.",
        "assumptions": [
            "Original documents/erratum identify the historical construction-to-contract families; parameter cases are not independent constructions.",
            "Frozen current AST imports identify shared reference modules, not proof that current live sources reproduce every historical run.",
            "Archived same-target fingerprints and recorded correctness/cost fields are reusable evidence metadata; no gate, pytest or backend is rerun.",
            "No complete archive LIVE/hash closure, continuous-price certificate, independent end-to-end backend or physical performance is inferred.",
        ],
        "acceptance": [
            "Exactly six unique constructions map to exactly three named families with multiplicities1,4,1 and independent_replication=false.",
            "Every entry module and attachment is source-bound; AST and explicit archived-cost links demonstrate common toolchain ancestry while unknown imports remain listed.",
            "Three whole-source arithmetic replacement stages bind the identical original72/f40 target bytes for each B4x12/B8x52 case; recorded replay outputs and cleanup fields are consistent.",
            "All four existing records have separate correctness/cost locators and explicit target/assumption/independence limits; measuredMCX fragment is not a pricing backend.",
            "Eight fixed negative inventory controls reject duplicate/missing families, false independence/credit, missing evidence, mixed targets or improper cross-family cost transfer.",
            "Every frozen input SHA rechecked after accounting; exact output inventory and own hashes retained. Unknowns remain unresolved.",
        ],
        "budgets": {"process_CPU_seconds": 30, "script_wall_seconds": 90, "maximum_corpus_files": 80,
                    "input_bytes": MAX_INPUT, "individual_metadata_bytes": MAX_FILE,
                    "new_owned_files": 16, "new_owned_bytes": MAX_OUTPUT},
        "stopping_rule": "One fixed inventory and its eight negative controls. No new backend, scientific replay, candidate, target, source adoption or timing benchmark. Retain any actual failure; no changed-source retry.",
        "runtime_scope": "Pinned script/corpus and observed interpreter only; no complete interpreter/runtime closure claim.",
        "new_fixture_credit": 0, "new_backend_created": False, "quantum_advantage": False,
    })
    print(json.dumps({"prepared": True, "protocol_sha256": digest(read(OUT / "protocol.json")),
                      "corpus_files": len(pins), "input_bytes": sum(v["bytes"] for v in pins.values()),
                      "checks_executed": False}))


def validate_family_map(data, corpus):
    contracts = data["contract_families"]
    require(len(contracts) == 3 and len({x["id"] for x in contracts}) == 3, "Exactly three contract families")
    ids = {x["id"] for x in contracts}
    rows = data["constructions"]
    require(len(rows) == 6 and {r["id"] for r in rows} == {f"S{i}" for i in range(1, 7)}, "Exactly six unique constructions")
    require(all(r["contract_family"] in ids and r["independent_replication"] is False for r in rows),
            "Valid correlated construction labels")
    require({k: sum(r["contract_family"] == k for r in rows) for k in ids} ==
            {"HestonAsian": 1, "GBMCompoundAsian": 4, "GBMKnockoutAsian": 1}, "Historical1/4/1 multiplicities")
    require(all(r["evidence"] in corpus for r in rows), "Source-bound family evidence")
    replacements = data["existing_replacements"]
    require(len(replacements) == 4 and len({r["id"] for r in replacements}) == 4, "Four unique existing component records")
    for record in replacements:
        require(record["same_target_claim"] is True and record["new_credit"] == 0,
                "Same target recorded, historical credit not duplicated")
        require(all(record[k] in corpus for k in ("source", "correctness_source", "cost_receipt", "correctness_receipt")),
                "Explicit existing correctness and cost evidence")
        application = data["replacement_applicability"][record["id"]]
        require(application["cost_transfer_to_other_constructions"] is False, "No cross-family cost transfer")
        expected = ["B4x12", "B8x52"] if record["id"] != "R_mcx" else []
        require(application["demonstrated_full_source_targets"] == expected, "Exact demonstrated target scope")
    require(data["new_fixture_credit"] == 0 and data["new_backend_created"] is False
            and data["source_adoption"] is False and data["quantum_advantage"] is False,
            "Bounded accounting scope")


def import_graph(corpus):
    modules = {key[:-3].replace("/", "."): key for key in corpus if key.endswith(".py") and key.startswith("research/")}
    graph = {module: set() for module in modules}
    edges, unresolved = [], []
    for module, key in modules.items():
        tree = ast.parse(read(ROOT / key).decode("utf-8"))
        for node in ast.walk(tree):
            destinations = []
            if isinstance(node, ast.ImportFrom):
                if node.level:
                    prefix = module.split(".")[:-node.level]
                    destination = ".".join(prefix + ([node.module] if node.module else []))
                else:
                    destination = node.module or ""
                destinations.append(destination)
            elif isinstance(node, ast.Import):
                destinations.extend(v.name for v in node.names)
            for destination in destinations:
                if destination in modules:
                    graph[module].add(destination)
                    edges.append({"from": module, "to": destination, "kind": "AST_import", "source": key, "line": node.lineno})
                else:
                    unresolved.append({"from": module, "import": destination, "line": node.lineno,
                                       "status": "EXTERNAL_OR_OUTSIDE_FROZEN_CORPUS"})
    return graph, edges, unresolved


def reach(graph, start):
    seen, todo = set(), [start]
    while todo:
        guard()
        module = todo.pop()
        if module not in seen:
            seen.add(module)
            todo.extend(graph.get(module, ()))
    return seen


def audit_existing_records(corpus):
    base = ROOT / "results/limitation_audit_20261001"
    lookup = load(base / "lookup_v2/summary.json")
    multiply = load(base / "multiplier_v2/summary.json")
    ln2 = load(base / "constant_multiplier_v1/summary.json")
    verification = load(base / "constant_multiplier_v1/verification.json")
    mcx = load(base / "mcx_cleanup_v1/result.json")
    require(all(d["passed"] is True for d in (lookup, multiply, ln2, mcx)), "Existing recorded component PASS fields")
    require(verification["artifact_checks_passed"] is True, "Separate guarded constant artifact record")
    target_identity, replay_count, comparisons = [], 0, 0
    for case in ("B4x12", "B8x52"):
        fingerprints = []
        for branch in ("lookup_v2", "multiplier_v2", "constant_multiplier_v1"):
            middle = "/signed-digit-carry-save" if branch == "constant_multiplier_v1" else ""
            path = base / f"{branch}/{case}{middle}/target.json"
            raw = read(path)
            target = json.loads(raw)
            require(target["width"] == 72 and target["fraction_bits"] == 40, "Original numerical widths")
            fingerprints.append(digest(raw))
        row_l = next(r for r in lookup["cases"] if r["case"] == case)
        row_m = next(r for r in multiply["cases"] if r["case"] == case)
        row_c = next(r for r in ln2["cases"] if r["case"] == case)
        recorded = [row_l["target_sha256"], row_m["source_target_sha256"], row_c["original_target_sha256"]]
        require(len(set(fingerprints + recorded)) == 1, "Same exact target bytes through all three replacement stages")
        target_identity.append({"case": case, "target_sha256": fingerprints[0], "three_stages": 3,
                                "original_width": 72, "original_fraction_bits": 40})
        require(row_m["candidate"]["logical_qubits"] <= row_m["qubit_cap"], "Recorded capped multiplier schedule")
        for replays in (row_l["replays"], row_m["gate_replay"], row_c["replays"]):
            require(type(replays) is list and replays, "Recorded nonempty source replay inventory")
            for replay in replays:
                guard()
                require(replay["actual"]["all_input_and_workspace_bits_restored"] is True,
                        "Recorded complete replay cleanup")
                expected, actual = replay["expected"], replay["actual"]["values"]
                require(json.dumps(expected, sort_keys=True) == json.dumps(actual, sort_keys=True),
                        "Type-exact recorded target/output equality")
                replay_count += 1
                comparisons += len(expected)
    log = next(v for v in lookup["leaves"] if v["name"] == "log")
    require(all(v["every_address_and_inverse_passed"] is True for v in lookup["leaves"]), "Recorded lookup address/inverse checks")
    require(log["baseline"]["qubits"] == log["candidate"]["qubits"], "Lookup example equal workspace")
    require(mcx["full_kraus_columns"] == 128 and mcx["branches"] == 8
            and mcx["max_forward_branch_error"] < 1e-12 and mcx["max_inverse_branch_error"] < 1e-12
            and mcx["negative_control_fidelity_without_corrections"] < .99,
            "Recorded MCX full-branch numerical diagnostic and correction negative control")
    return {"same_target_identity": target_identity, "archived_replay_records_checked": replay_count,
            "recorded_output_values_compared": comparisons,
            "lookup_log_example": {"baseline": log["baseline"], "candidate": log["candidate"]},
            "MCX_fragment_record": mcx,
            "costs_are_historical_logical_component_records": True,
            "new_replays_or_global_fixture_credit": 0,
            "historical_complete_manifest_or_gate_bytes_revalidated": False}


def negative_controls(data, corpus):
    changes = [
        ("duplicate_construction", lambda d: d["constructions"][1].update(id="S1")),
        ("extra_contract_family", lambda d: d["contract_families"].append({"id": "fourth"})),
        ("six_independent_replications", lambda d: d["constructions"][0].update(independent_replication=True)),
        ("unbound_family_evidence", lambda d: d["constructions"][0].update(evidence="missing.md")),
        ("missing_component_cost", lambda d: d["existing_replacements"][0].update(cost_receipt=None)),
        ("duplicated_historical_credit", lambda d: d["existing_replacements"][0].update(new_credit=1)),
        ("mixed_demonstrated_targets", lambda d: d["replacement_applicability"]["R_multiply"].update(demonstrated_full_source_targets=["C4"])),
        ("unproved_cross_family_cost_transfer", lambda d: d["replacement_applicability"]["R_ln2"].update(cost_transfer_to_other_constructions=True)),
    ]
    records = []
    for name, change in changes:
        mutated = copy.deepcopy(data)
        change(mutated)
        try:
            validate_family_map(mutated, corpus)
        except ValueError as error:
            records.append({"name": name, "rejected": True, "reason": str(error)})
        else:
            raise ValueError("Negative inventory control escaped: " + name)
    return records


def run(expected_protocol):
    require(not (OUT / "RUN_STARTED.json").exists() and not (OUT / "manifest.json").exists()
            and not FAILURE.exists(), "One frozen invocation, no retry")
    raw = read(OUT / "protocol.json")
    require(digest(raw) == expected_protocol, "Actual frozen protocol bytes")
    protocol = json.loads(raw)
    require(protocol["schema"] == "c12-preregistered-evidence-inventory-v1"
            and set(protocol["corpus_sha256"]) == set(CORPUS), "Exact prospectively frozen corpus")
    write(OUT / "RUN_STARTED.json", {"protocol_sha256": expected_protocol, "scientific_backend_executed": False})
    write(FAILURE, {"provisional": True, "passed": False, "authoritative_if_retained": True})
    try:
        for key, pin in protocol["corpus_sha256"].items():
            require(digest(read(ROOT / key)) == pin["sha256"], "Fresh initial frozen SHA: " + key)
        data = load(DATA)
        validate_family_map(data, protocol["corpus_sha256"])
        graph, edges, unresolved = import_graph(protocol["corpus_sha256"])
        for record in data["artifact_dependencies"]:
            key = record["from_module"].replace(".", "/") + ".py"
            text = read(ROOT / key).decode("utf-8")
            require(all(fragment in text for fragment in record["source_fragments"]), "Bound actual archived cost dependency")
            graph[record["from_module"]].add(record["to_module"])
            edges.append({"from": record["from_module"], "to": record["to_module"],
                          "kind": "archived_cost_dependency", "source": key,
                          "source_fragments": record["source_fragments"]})
        maps = []
        for row in data["constructions"]:
            require(row["entry_module"] in graph, "Bound construction entry module")
            ancestry = reach(graph, row["entry_module"])
            require("research.journal_sprint.reversible_fixed_point" in ancestry, "Bound shared core ancestry")
            maps.append({"id": row["id"], "contract_family": row["contract_family"],
                         "mapped_reference_modules": sorted(ancestry),
                         "scope": "Current reference AST plus explicitly bound historical cost links; no old-code provenance replacement"})
        counts = {m: sum(m in row["mapped_reference_modules"] for row in maps) for m in graph}
        accounting = audit_existing_records(protocol["corpus_sha256"])
        controls = negative_controls(data, protocol["corpus_sha256"])
        write(OUT / "evidence_families.json", data)
        write(OUT / "shared_module_graph.json", {"edges": edges, "construction_ancestry": maps,
                                                "shared_module_construction_counts": counts,
                                                "external_or_unmapped_imports": unresolved})
        write(OUT / "existing_evidence_accounting.json", accounting)
        write(OUT / "negative_inventory_controls.json", controls)
        after_checks = []
        for key, pin in protocol["corpus_sha256"].items():
            require(digest(read(ROOT / key)) == pin["sha256"], "Fresh final frozen SHA: " + key)
            after_checks.append(key)
        summary = {"schema": "c12-bounded-evidence-inventory-summary-v1", "passed": True, "completed": True,
                   "construction_count": 6, "contract_family_count": 3,
                   "family_multiplicities": {"HestonAsian": 1, "GBMCompoundAsian": 4, "GBMKnockoutAsian": 1},
                   "existing_component_records": 4, "same_target_source_case_chains": 2,
                   "frozen_corpus_files": len(after_checks), "AST_source_files": sum(key.endswith(".py") for key in CORPUS),
                   "negative_inventory_controls": len(controls), "frozen_SHA_initial_and_final_mismatches": 0,
                   "budget_observation": {"process_CPU_seconds": time.process_time(), "script_wall_seconds": time.monotonic() - STARTED},
                   "new_fixture_credit": 0, "new_backend_created": False, "new_gate_or_finance_replays": 0,
                   "source_adoption": False, "quantum_advantage": False,
                   "exact_completion_scope": "C12 bounded existing-evidence map and inventory accounting, not independent replication or a full pricing backend.",
                   "missing_independent_backends": data["missing_independent_backends"],
                   "remaining_limits": ["Same-target component evidence reuses recorded receipts; no correctness backend or old gate suite rerun.",
                                        "No full historical manifest/runtime closure validation.",
                                        "Current reference topology does not prove current sources generated every historical artifact.",
                                        "No construction-independent impossibility, physical performance or financial-delivery claim."]}
        write(OUT / "summary.json", summary)
        write(OUT / "completion_outcome.json", summary)
        owned = [p for p in OUT.iterdir() if p.is_file() and p != FAILURE]
        require(len(owned) + 1 <= 16 and sum(p.stat().st_size for p in owned) < MAX_OUTPUT, "Complete retained evidence cap")
        manifest = {"schema": "c12-bounded-evidence-inventory-manifest-v1", "files": {p.name: digest(read(p)) for p in owned},
                    "frozen_corpus_sha256": protocol["corpus_sha256"], "passed": True, "completed": True,
                    "manifest_self_hash_excluded": True, "runtime_scope": protocol["runtime_scope"],
                    "interpreter": os.path.abspath(os.sys.executable), "new_fixture_credit": 0}
        write(OUT / "manifest.json", manifest)
        require({p.name for p in OUT.iterdir()} == set(manifest["files"]) | {"manifest.json", "FAILED_UNSEALED.json"}, "Exact own inventory")
        for name, expected in manifest["files"].items():
            require(digest(read(OUT / name)) == expected, "Fresh owned file SHA")
        guard()
        FAILURE.unlink()
        print(json.dumps({"passed": True, "receipt": OUT.relative_to(ROOT).as_posix(),
                          "manifest_sha256": digest(read(OUT / "manifest.json")),
                          "new_fixture_credit": 0, "quantum_advantage": False}))
    except BaseException as error:
        FAILURE.write_text(json.dumps({"passed": False, "authoritative": True, "error_type": type(error).__name__,
                                       "error": str(error), "new_fixture_credit": 0, "quantum_advantage": False}, indent=2) + "\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument("--protocol-sha256")
    args = parser.parse_args()
    if args.mode == "prepare":
        require(args.protocol_sha256 is None, "No future pin in preparation")
        prepare()
    else:
        require(args.protocol_sha256 is not None, "Actual protocol SHA required")
        run(args.protocol_sha256)
