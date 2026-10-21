"""Fixed two-closure metadata diagnostic; no builder imports or financial calls."""

import argparse
import hashlib
import json
from pathlib import Path
import time
import traceback

ROOT = Path(__file__).resolve().parents[4]
AUTHOR = Path(__file__).resolve()
POLICY = AUTHOR.with_name("A20_TWO_CLOSURE_DIAGNOSTIC_PROTOCOL_run001.json")
OUTPUT = ROOT / "results/limitation_program_20261001/A20_continuation_20261004_template_diagnostic_run001"
STARTED = time.monotonic()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check():
    require(time.process_time() < 30 and time.monotonic() - STARTED < 90, "Fixed30CPU/90wall diagnostic cap")


def digest(path):
    check()
    before = path.stat()
    require(before.st_size <= 64 * 1024**2, "Fixed64MiB input file cap")
    data = path.read_bytes()
    after = path.stat()
    require((before.st_size, before.st_mtime_ns, before.st_ctime_ns)
            == (after.st_size, after.st_mtime_ns, after.st_ctime_ns), "Stable read-only diagnostic input")
    check()
    return data, hashlib.sha256(data).hexdigest()


def write(name, value):
    check()
    data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
    require(sum(path.stat().st_size for path in OUTPUT.iterdir()) + len(data) <= 1048576,
            "Fixed1MiB retained evidence cap before mutation")
    require(len(list(OUTPUT.iterdir())) < 12, "Fixed12file retained evidence cap")
    with (OUTPUT / name).open("xb") as stream:
        stream.write(data)
    check()


def extract_closure(occurrence, clips, index):
    boundary, output = occurrence["clipped_log"], occurrence["stock"]
    chosen = [clip for clip in clips if clip["out"] == boundary]
    require(len(chosen) == 1, "One exact source clamp for fixed selected boundary")
    clamp = {}
    for label in ("low", "high"):
        node = index[chosen[0][label]]
        word = node["params"]["value"]
        require(node["op"] == "const" and type(word) is int and 0 <= word < 1 << 72,
                "Canonical source clamp CONST72")
        clamp[label] = {"source_SSA": chosen[0][label], "raw_word72": word,
                        "signed_word72": word - (1 << 72) if word >= 1 << 71 else word}
    order, completed, active = [], set(), set()

    def descend(value):
        check()
        if value == boundary or value in completed:
            return
        require(value not in active and value in index, "Acyclic closed source dependency")
        active.add(value)
        require(len(active) <= 64, "Fixed64-node dependency depth")
        node = index[value]
        require(node["op"] in {"const", "add", "sub", "mul", "cmul", "bits", "shift"}
                and node["out"] == [value], "Exact single-output scalar closure operation")
        for argument in node["args"]:
            descend(argument)
        active.remove(value)
        completed.add(value)
        order.append(node)
        require(len(order) <= 64, "Fixed64-node independent closure cap")

    descend(output)
    identifiers = {boundary: 0}
    normalized, correspondence = [], []
    for position, node in enumerate(order, 1):
        check()
        require(all(argument in identifiers for argument in node["args"]), "Postorder arguments available")
        identifiers[node["out"][0]] = position
        normalized.append({"op": node["op"], "args": [identifiers[v] for v in node["args"]],
                           "params": node["params"], "out": position})
        correspondence.append({"normalized_output": position, "original_output_SSA": node["out"][0]})
    return {"asset": occurrence["asset"], "date": occurrence["date"], "boundary_SSA": boundary,
            "stock_output_SSA": output, "normalized_output": identifiers[output],
            "clamps": clamp, "normalized_nodes": normalized, "SSA_correspondence": correspondence}


def diagnose(target, census):
    require((target["width"], target["fraction_bits"]) == (72, 40), "Unchanged source72/F40")
    index = {}
    for node in target["nodes"]:
        check()
        for output in node["out"]:
            require(output not in index, "Unique source SSA producer")
            index[output] = node
    closures = []
    for asset in (0, 1):
        selected = [row for row in census["builder_label_proof"]["exponentials"]
                    if row["date"] == 0 and row["asset"] == asset]
        require(len(selected) == 1, "Exactly frozen asset/date occurrence")
        closures.append(extract_closure(selected[0], census["builder_label_proof"]["clips"], index))
    first, second = closures
    differences = []
    for position in range(max(len(first["normalized_nodes"]), len(second["normalized_nodes"]))):
        left = first["normalized_nodes"][position] if position < len(first["normalized_nodes"]) else None
        right = second["normalized_nodes"][position] if position < len(second["normalized_nodes"]) else None
        if left != right:
            fields = [field for field in ("op", "args", "params", "out")
                      if left is None or right is None or left[field] != right[field]]
            difference = {"position_zero_based": position, "different_fields": fields,
                          "asset0": left, "asset1": right}
            if left is not None and right is not None and fields == ["params"]:
                parameters = set(left["params"]) | set(right["params"])
                difference["different_parameter_keys"] = sorted(key for key in parameters
                    if left["params"].get(key) != right["params"].get(key))
            differences.append(difference)
    clamp_equal = all(first["clamps"][key]["signed_word72"] == second["clamps"][key]["signed_word72"]
                      for key in ("low", "high"))
    same = not differences and clamp_equal
    interpretation = []
    for difference in differences:
        left, right = difference["asset0"], difference["asset1"]
        if left and right and left["op"] == right["op"] == "cmul" and left["args"] == right["args"]:
            constants = []
            for node in (left, right):
                coefficient = node["params"].get("c")
                require(type(coefficient) is int, "Typed exact source CMUL coefficient")
                constants.append({"signed_literal_c": coefficient, "fixed_point_denominator": 1 << 40})
            interpretation.append({"normalized_output": left["out"], "operation": "cmul",
                                   "asset_coefficients": constants,
                                   "local_semantics": "Native fixed-point constant multiplication: retain distinct coefficient and floor/cleanup duties; no scalar point evaluated"})
    return {"closures": closures, "node_differences": differences,
            "clamp_signed_literals_equal": clamp_equal, "exact_shared_template_premise": same,
            "local_operation_interpretations": interpretation,
            "disposition": "SHARED_TABLE_PREMISE_REJECTED" if not same else "STRUCTURAL_EQUALITY_ONLY",
            "missing_operation_cost_scope": "Any asset-dependent CMUL, distinct table or loader/control work must be explicitly included with preparation/inverse/storage; no replacement or cost number supplied here",
            "no_mathematical_equivalence_or_inequivalence_proof_claim": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author-sha256", required=True)
    parser.add_argument("--protocol-sha256", required=True)
    arguments = parser.parse_args()
    author_bytes, author_sha = digest(AUTHOR)
    policy_bytes, policy_sha = digest(POLICY)
    require(author_sha == arguments.author_sha256 and policy_sha == arguments.protocol_sha256,
            "Actual prospective diagnostic author/protocol pins")
    policy = json.loads(policy_bytes)
    require(policy["schema"] == "a20-fixed-independent-two-stock-closure-diagnostic-v1"
            and policy["selection"]["assets"] == [0, 1] and policy["selection"]["date"] == 0,
            "Exact prospective two-closure policy")
    require(not OUTPUT.exists(), "One fresh diagnostic output, no retries")
    OUTPUT.mkdir()
    (OUTPUT / "FAILED_UNSEALED.json").write_text('{"passed":false,"authoritative":true}\n', encoding="utf-8")
    try:
        (OUTPUT / "executed_diagnostic.py").write_bytes(author_bytes)
        (OUTPUT / "protocol.json").write_bytes(policy_bytes)
        inputs = {}
        for key, expected in policy["input_expected_SHA256"].items():
            data, actual = digest(ROOT / key)
            require(actual == expected, "Exact original diagnostic JSON input SHA")
            inputs[key] = json.loads(data)
        target = inputs["results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json"]
        census = inputs["results/limitation_program_20261001/E22_census_run002/B4x12_predicate_census.json"]
        result = diagnose(target, census)
        for key, expected in policy["input_expected_SHA256"].items():
            require(digest(ROOT / key)[1] == expected, "Fresh terminal original diagnostic JSON SHA")
        require(digest(AUTHOR)[1] == author_sha and digest(POLICY)[1] == policy_sha, "Unchanged diagnostic author/protocol")
        result.update(schema="a20-fixed-two-stock-closure-diagnostic-summary-v1", passed=True,
                      scientific_component_approval=False, producer_retry=False, gates_fits_price_calls=0,
                      new_fixture_credit=0, finance_draws=0, adoption=False, quantum_advantage=False,
                      V4_failed_unsealed_retained=True,
                      budget={"process_CPU_seconds": time.process_time(), "controller_wall_seconds": time.monotonic()-STARTED})
        write("summary.json", result)
        write("completion_outcome.json", {"passed": True, "diagnostic_only": True, "disposition": result["disposition"],
                                          "scientific_component_approval": False, "new_fixture_credit": 0})
        owned = {path.name: digest(path)[1] for path in OUTPUT.iterdir() if path.name != "FAILED_UNSEALED.json"}
        write("manifest.json", {"schema": "a20-two-closure-diagnostic-manifest-v1", "passed": True,
              "files": owned, "frozen_inputs": {**policy["input_expected_SHA256"],
                 AUTHOR.relative_to(ROOT).as_posix(): author_sha, POLICY.relative_to(ROOT).as_posix(): policy_sha},
              "manifest_self_hash_excluded": True, "scientific_component_approval": False, "new_fixture_credit": 0,
              "runtime_scope": "No complete runtime or historical input-map validity claim"})
        check()
        (OUTPUT / "FAILED_UNSEALED.json").unlink()
        print(json.dumps({"passed": True, "disposition": result["disposition"], "differences": result["node_differences"],
                          "clamps_equal": result["clamp_signed_literals_equal"], "budget": result["budget"],
                          "manifest_SHA256": digest(OUTPUT / "manifest.json")[1]}))
    except BaseException as error:
        (OUTPUT / "FAILED_UNSEALED.json").write_text(json.dumps({"passed": False, "authoritative": True,
            "error": repr(error), "traceback": traceback.format_exc(), "partial_results_unapproved": True}) + "\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
