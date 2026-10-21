"""Bounded exact E01 access-accounting audit; never imports a financial source."""
import time
CPU_START = time.process_time()
import argparse
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

WALL_START = time.monotonic()
ROOT = Path(__file__).resolve().parents[3]
DOC = ROOT / "docs/independent_110_20261004/E01"
OUT = ROOT / "results/independent_110_20261004/E01/audit_run001"
FREEZE = DOC / "FREEZE.json"
CASES = ("B4x12", "B8x52")
PATHS = [
    "docs/independent_110_20261004/inventory_run001/WORK_LIST.txt",
    "docs/limitation_audit_20261001/implementation_plan/roadmap.json",
    "docs/limitation_audit_20261001/ESTIMATION_AND_CERTIFICATION.md",
    "docs/limitation_audit_20261001/FORMULATIONS_AND_CLASSICAL_COMPARATORS.md",
    "docs/limitation_audit_20261001/implementation_plan/FORMULATIONS.md",
    "manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md",
    "docs/independent_110_20261004/E01/PROTOCOL.json",
    "docs/independent_110_20261004/E01/ACCESS_MODEL_CARDS.md",
    "docs/independent_110_20261004/E01/primary_sources/Recchia_2609_03625v1.pdf",
    "research/independent_110_20261004/E01/audit_access_model.py",
    "research/frontier_classical_20261001/basis.py",
    "research/frontier_classical_20261001/scrambles.py",
    "results/limitation_program_20261001/E02_IQFT_run001/manifest.json",
    "results/limitation_program_20261001/E02_financial_run002/manifest.json",
    "results/limitation_program_20261001/E07_original_BM_G2_composition_run001/source_interface_matching.json",
    "results/limitation_program_20261001/E07_original_BM_G2_composition_audit_run001/summary.json",
    "results/limitation_program_20261001/E07_original_BM_G2_root_verification_run001/summary.json",
]
for case in CASES:
    PATHS += [
        f"results/limitation_program_20261001/G0_run003/{case}_task.json",
        f"results/limitation_program_20261001/E02_IQFT_run001/{case}/synthesized_estimator_ledger.json",
        f"results/limitation_program_20261001/E02_financial_run002/{case}/estimator_ledger.json",
    ]
    PATHS += [f"results/limitation_program_20261001/A10_coefficient_run001/{case}/min-depth/{name}.json" for name in ("target", "source", "schedule_capped")]


def guard(admission=False):
    if time.process_time() - CPU_START > (45 if admission else 60) or time.monotonic() - WALL_START > 120:
        raise RuntimeError("Fixed E01 administrative CPU/wall budget exhausted")


def digest(path):
    guard()
    value = hashlib.sha256(path.read_bytes()).hexdigest()
    guard()
    return value


def read(path):
    guard()
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    guard()
    return value


def fresh_write(path, value, emergency=False):
    payload = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    if not emergency:
        guard()
        files = [p for p in OUT.iterdir() if p.is_file()]
        if len(files) + 1 > 16 or sum(p.stat().st_size for p in files) + len(payload) + 16384 > 2097152:
            raise RuntimeError("Fixed E01 owned-output reserve exhausted")
    elif len(payload) > 16384:
        raise RuntimeError("Fixed E01 emergency marker reserve exhausted")
    with path.open("xb") as handle:
        handle.write(payload)
    if not emergency:
        guard()


def make_freeze():
    if FREEZE.exists() or OUT.exists():
        raise RuntimeError("Fresh E01 freeze and receipt required")
    assert len(PATHS) == len(set(PATHS)) <= 40
    pins = {}
    for name in PATHS:
        path = ROOT / name
        assert path.stat().st_size <= 8388608
        pins[name] = {"sha256": digest(path), "bytes": path.stat().st_size}
    assert sum(p["bytes"] for p in pins.values()) <= 33554432
    selected_runtime = {}
    for path in sorted(set([Path(sys.executable), Path(sys.base_prefix) / "python.exe"]), key=str):
        selected_runtime[str(path)] = {"sha256": digest(path), "bytes": path.stat().st_size}
    value = {"schema": "e01-prospective-selected-corpus-freeze-v1", "inputs": pins,
             "selected_runtime": selected_runtime, "runtime_scope": "Selected launcher/base interpreter only; not full runtime provenance",
             "science_started": False, "finance_draws": 0, "source_imports": 0}
    with FREEZE.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps({"freeze_sha256": digest(FREEZE), "input_files": len(pins), "input_bytes": sum(p["bytes"] for p in pins.values())}))


def verify_inputs(freeze):
    assert set(freeze["inputs"]) == set(PATHS)
    for name, pin in freeze["inputs"].items():
        assert (ROOT / name).stat().st_size == pin["bytes"]
        assert digest(ROOT / name) == pin["sha256"], name
    for name, pin in freeze["selected_runtime"].items():
        assert digest(Path(name)) == pin["sha256"], name


def admissible(card):
    return (card["same_law_or_bias_certified"] and card["emitted_reduction"]
            and card["complete_compatible_source_manifest"] and card["cost"] is not None
            and card["baseline"] is not None and card["cost"] < card["baseline"])


def checks(freeze):
    iqft_owner = read(ROOT / "results/limitation_program_20261001/E02_IQFT_run001/manifest.json")
    financial_owner = read(ROOT / "results/limitation_program_20261001/E02_financial_run002/manifest.json")
    bridge = read(ROOT / "results/limitation_program_20261001/E07_original_BM_G2_composition_run001/source_interface_matching.json")
    g2_audit = read(ROOT / "results/limitation_program_20261001/E07_original_BM_G2_composition_audit_run001/summary.json")
    g2_root = read(ROOT / "results/limitation_program_20261001/E07_original_BM_G2_root_verification_run001/summary.json")
    assert g2_audit["passed"] and g2_audit["source_specific_mathematical_G2_bias_complete"]
    assert g2_root["passed"] and g2_root["SHA_mismatches"] == 0
    results, counters = [], {"baseline_rows": 0, "source_hash_joins": 0, "exact_normalization_cases": 0,
                             "rank_capacity_cases": 0, "binary_law_counterchecks": 0, "admission_cases": 0}
    for case in CASES:
        guard()
        task = read(ROOT / f"results/limitation_program_20261001/G0_run003/{case}_task.json")
        iqft_name = f"results/limitation_program_20261001/E02_IQFT_run001/{case}/synthesized_estimator_ledger.json"
        financial_name = f"results/limitation_program_20261001/E02_financial_run002/{case}/estimator_ledger.json"
        ledger, prior = read(ROOT / iqft_name), read(ROOT / financial_name)
        assert iqft_owner["files"][iqft_name] == freeze["inputs"][iqft_name]["sha256"]
        assert financial_owner["files"][financial_name] == freeze["inputs"][financial_name]["sha256"]
        assert ledger["original_source_estimator_ledger_sha256"] == freeze["inputs"][financial_name]["sha256"]
        for filename, expected in ledger["binding"]["hashes"].items():
            name = f"results/limitation_program_20261001/A10_coefficient_run001/{case}/min-depth/{filename}"
            assert expected == freeze["inputs"][name]["sha256"] == bridge[case]["source_hashes"][filename]
            counters["source_hash_joins"] += 1
        src, binding = task["digital_source"], ledger["binding"]
        target = read(ROOT / f"results/limitation_program_20261001/A10_coefficient_run001/{case}/min-depth/target.json")
        assert target["width"] == src["word_width"] and target["fraction_bits"] == src["fraction_bits"]
        assert target["outputs"] == src["output"]
        target_inputs = [n for n in target["nodes"] if n["op"] == "input"]
        assert len(target_inputs) == src["normal_count"] and all(n["params"]["bits"] == 32 and n["params"]["preparation"] == "uniform" for n in target_inputs)
        D, q32, selector = src["normal_count"], src["uniform_bits_each"], binding["selector_bits"]
        assert (D, q32, src["word_width"], src["fraction_bits"], selector) == ((60 if case == "B4x12" else 468), 32, 72, 40, 46)
        assert task["barrier_dollars"] == 140 and task["strike_dollars"] == 100
        assert task["output_contract"]["per_price_success_probability_at_least"] == .99
        assert ledger["statistical_error_dollars_exact"] == [9, 2000]
        assert ledger["normalization_span_dollars"] == 64 and ledger["price_output_already_discounted"] and not ledger["second_discount_applied"]
        assert bridge[case]["selector_normalization_exact"] == "64/2**46=1/2**40"
        assert Q(64, 2**46) == Q(1, 2**40)
        for raw in (0, 1, binding["payoff_raw_bounds"][1], 2**46 - 1):
            assert 64 * Q(raw, 2**46) == Q(raw, 2**40)
            counters["exact_normalization_cases"] += 1
        shots, chain = ledger["serial_shots"], ledger["longest_single_shot_grover_chain"]
        calls = shots * chain
        assert shots == ledger["fresh_preparations"] == 15 and chain == 2**16 - 1
        for key in ("financial_forwards", "financial_literal_inverses", "selector_forwards", "selector_literal_inverses", "controlled_predicate_CZ", "controlled_signed_reflections"):
            assert ledger[key] == prior[key] == calls
        assert ledger["source_graph_directions"] == 2 * calls
        assert ledger["uniform_preparation_H"] == shots * (D * q32 + selector)
        assert ledger["source_iterate_resources"]["original_uniform_bits"] == D * q32
        assert ledger["full_T_count"] == calls * ledger["source_iterate_resources"]["t_count"] + ledger["iqft_exact_CS_T_count"] + ledger["synthesized_single_qubit_T_count"]
        assert ledger["measured_QPE_bits"] == ledger["qpe_preparation_H"] == shots * 16
        counters["baseline_rows"] += 1
        diagnostic = []
        for label_bits in (16, 32):
            assert label_bits < D * q32
            diagnostic.append({"label_bits": label_bits, "maximum_rank": label_bits, "independent_product_bits": D*q32,
                               "maximum_support_fraction_exact": {"numerator": 1, "denominator_base": 2, "denominator_exponent": D*q32-label_bits},
                               "law_equal_by_full_rank": False, "price_bias_lower_bound": None,
                               "generic_loader_CNOT_upper": D*q32*label_bits, "actual_loader_CNOT": None})
            counters["rank_capacity_cases"] += 1
        results.append({"case": case, "source_hashes": ledger["binding"]["hashes"], "output": src["output"],
                        "original_input_bits": D*q32, "normalization_span_dollars": 64, "native_fraction_bits": 40,
                        "fresh_shots": shots, "financial_forwards": calls, "financial_inverses": calls,
                        "selector_forwards": calls, "selector_inverses": calls, "source_graph_directions": 2*calls,
                        "controlled_reflections": calls, "uniform_preparation_H": ledger["uniform_preparation_H"],
                        "baseline_full_logical_T_count": ledger["full_T_count"], "baseline_physical_runtime": None,
                        "candidate": "coherent_Sobol_coordinate_interface", "loader_CNOT": None,
                        "loader_and_inverse_total_coefficient": shots+2*calls, "candidate_complete_logical_T_count": None,
                        "candidate_preprocessing_cost": None, "candidate_same_law_or_bias_certificate": None,
                        "candidate_emitted_reduction": False, "candidate_complete_source_manifest": None,
                        "candidate_price_output_normalization": "If native graph and selector remain unchanged, dollar output is still 64p; changed input law requires separate bias/equivalence proof",
                        "candidate_reflection_workspace": None, "diagnostics": diagnostic,
                        "existing_original_source_specific_G2_evidence": "Archived auditor/root PASS, exact source only; not re-proved or transferred here",
                        "confidence_readout": {"statistics_dollars_exact": [9,2000], "archived_ideal_failure_bound": ledger["ideal_failure_upper_exact"],
                                               "readout_error_exact": ledger["classical_readout_error_allowance"], "physical_failure": None},
                        "decision": "REJECTED_BEFORE_COMPILATION_FOR_MISSING_EXACT_REDUCTION"})
    # A two-bit common label and two identity coordinate maps have uniform marginals but a different joint law.
    net = [(i, i) for i in range(4)]
    product = [(i, j) for i in range(4) for j in range(4)]
    assert {x for x, _ in net} == {0, 1, 2, 3} and {y for _, y in net} == {0, 1, 2, 3}
    assert Q(sum(x == y for x, y in net), len(net)) == 1
    assert Q(sum(x == y for x, y in product), len(product)) == Q(1, 4)
    assert sum(0 for _ in net) == sum(0 for _ in product) == 0  # different law does not prove price bias
    counters["binary_law_counterchecks"] = 3
    base = {"same_law_or_bias_certified": True, "emitted_reduction": True, "complete_compatible_source_manifest": True,
            "cost": 9, "baseline": 10}
    assert admissible(base)
    counters["admission_cases"] += 1
    for change in ({"same_law_or_bias_certified": False}, {"emitted_reduction": False},
                   {"complete_compatible_source_manifest": False}, {"cost": None}, {"cost": 10}, {"cost": 11}, {"baseline": None}):
        assert not admissible(dict(base, **change))
        counters["admission_cases"] += 1
    return results, counters


def run(expected):
    if not sys.flags.isolated or not sys.flags.no_site or not sys.dont_write_bytecode:
        raise RuntimeError("Require isolated -I -S -B standard-library execution")
    if OUT.exists():
        raise RuntimeError("Fresh E01 receipt required; no retries")
    OUT.mkdir(parents=True)
    marker = OUT / "FAILED_UNSEALED.json"
    fresh_write(marker, {"decision": "UNSEALED_FROM_START", "passed": False, "completed": False}, emergency=True)
    try:
        assert digest(FREEZE) == expected
        freeze = read(FREEZE)
        verify_inputs(freeze)
        guard(admission=True)
        fresh_write(OUT / "protocol.json", read(DOC / "PROTOCOL.json"))
        fresh_write(OUT / "run_started.json", {"freeze_sha256": expected, "finance_draws": 0, "source_imports": 0})
        rows, counters = checks(freeze)
        fresh_write(OUT / "access_cards.json", rows)
        fresh_write(OUT / "checks.json", {"passed": True, "counts": counters, "total": sum(counters.values()),
                                          "scope": "Exact selected metadata/accounting and finite algebra; not source replays or financial sampling"})
        fresh_write(OUT / "certificate.json", {"passed": True, "completed": True, "budget_censored": False,
                    "E01_bounded_access_model_audit_complete": True, "transformations_screened": 1,
                    "cards": len(rows), "candidate_decision": "REJECTED_BEFORE_COMPILATION_FOR_MISSING_EXACT_REDUCTION",
                    "generic_baseline_retained": True, "universal_structured_integration_no_go": False,
                    "same_current_source_specific_G2_adoption": "Archived evidence only; no changed-source transfer",
                    "future_obligations": ["F05 separately scoped exact coordinate matrices/clean reversible emission", "Exact-law or charged native/continuous bias proof", "Compatible reflection and complete logical estimator ledger", "Strict matched logical work improvement before compilation"],
                    "new_global_fixture_credit": 0, "new_gate_replay_credit": 0, "source_adoption": False,
                    "new_samples": 0, "timing_comparison": False, "financial_delivery_certified": False, "quantum_advantage": False})
        fresh_write(OUT / "comparison.json", {"scope": "Original compatible logical estimator versus unbuilt Sobol interface",
                    "baseline_T_counts": {r["case"]: r["baseline_full_logical_T_count"] for r in rows},
                    "candidate_T_counts": {r["case"]: None for r in rows}, "strict_improvement_demonstrated": False,
                    "complete_runtime_seconds": None, "performance_comparison": False})
        verify_inputs(freeze)
        owned = {str(p.relative_to(ROOT)).replace('\\','/'): digest(p) for p in OUT.iterdir() if p.is_file() and p != marker}
        fresh_write(OUT / "manifest.json", {"passed": True, "completed": True, "budget_censored": False,
                    "files": owned, "frozen_inputs": freeze["inputs"], "selected_runtime": freeze["selected_runtime"],
                    "freeze_sha256": expected, "runtime_scope": "Selected launcher/base interpreter only",
                    "manifest_self_hash_excluded": True, "failure_marker_authoritative": True,
                    "new_global_fixture_credit": 0, "quantum_advantage": False})
        assert set(p.name for p in OUT.iterdir()) == {"FAILED_UNSEALED.json", "protocol.json", "run_started.json", "access_cards.json", "checks.json", "certificate.json", "comparison.json", "manifest.json"}
        guard()
        marker.unlink()
        print(json.dumps({"passed": True, "checks": counters, "manifest_sha256": digest(OUT/"manifest.json")}))
    except BaseException as exc:
        failure = {"decision": "FAILED_UNSEALED", "passed": False, "completed": False, "error_type": type(exc).__name__,
                   "message": str(exc)[:2048], "budget_censored": "budget" in str(exc).lower(),
                   "failure_precedence": "Overrides all partial PASS files", "new_global_fixture_credit": 0, "quantum_advantage": False}
        payload = (json.dumps(failure, indent=2, sort_keys=True)+"\n").encode()
        assert len(payload) <= 16384
        marker.write_bytes(payload)  # spent-guard-safe retention; restores marker if final hashing fails
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("freeze", "run"))
    parser.add_argument("--freeze-sha256")
    args = parser.parse_args()
    if args.mode == "freeze":
        make_freeze()
    else:
        if not args.freeze_sha256:
            parser.error("run requires --freeze-sha256")
        run(args.freeze_sha256)
