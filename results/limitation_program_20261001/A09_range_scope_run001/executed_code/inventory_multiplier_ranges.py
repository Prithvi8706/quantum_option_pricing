"""Prospective actual-SSA multiplier range inventory; no circuit or gain claim."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform
import shutil
import sys
import time

from research.limitation_program_20261001.interval_bounds import bound_graph
from research.limitation_program_20261001.prove_log_exponent import SSAContext

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
BASELINE = PROGRAM / "A11_nonrestoring_run001"
AUDIT = PROGRAM / "A01_run011"
CASES = ("B4x12", "B8x52")
CANDIDATE_BITS = (24, 40, 72)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def signed_bits(low, high, width):
    """Minimum signed width containing the entire inclusive integer interval."""
    if (
        type(width) is not int or width < 1
        or type(low) is not int or type(high) is not int
        or not -(1 << (width - 1)) <= low <= high < 1 << (width - 1)
    ):
        raise ValueError("ordered integer interval within signed native width required")
    for bits in range(1, width + 1):
        if signed_guard(low, high, bits):
            return bits
    raise AssertionError("full signed native width must contain the interval")


def signed_guard(low, high, bits):
    return -(1 << (bits - 1)) <= low <= high < 1 << (bits - 1)


def retained_plane_terms(a_bits, b_bits, product_bits):
    """Diagnostic pair count only; no emitted gate/resource reduction credit."""
    return sum(min(b_bits, max(0, product_bits - bit)) for bit in range(a_bits))


def check_small_intervals():
    """Enumerated signed decode oracle, independent of endpoint classification."""
    checked = 0
    for width in range(1, 7):
        sign = 1 << (width - 1)
        for low in range(-sign, sign):
            for high in range(low, sign):
                oracle = None
                for bits in range(1, width + 1):
                    modulus, bit_sign = 1 << bits, 1 << (bits - 1)
                    preserved = True
                    for value in range(low, high + 1):
                        encoded = value & (modulus - 1)
                        decoded = encoded - modulus if encoded & bit_sign else encoded
                        preserved &= decoded == value
                    if preserved and oracle is None:
                        oracle = bits
                assert signed_bits(low, high, width) == oracle
                checked += 1
    boundaries = 0
    for exponent in range(71):
        # A positive unsigned bit at2**m requires m+2 SIGNED bits.
        assert signed_bits(1 << exponent, 1 << exponent, 72) == exponent + 2
        assert signed_bits(-(1 << exponent), -(1 << exponent), 72) == exponent + 1
        boundaries += 2
    assert signed_bits(0, 0, 72) == 1
    for width in range(1, 7):
        for fraction in range(width + 1):
            for a_bits in range(1, width + 1):
                for b_bits in range(1, width + 1):
                    explicit = sum(i + j < width + fraction
                                   for i in range(a_bits) for j in range(b_bits))
                    assert retained_plane_terms(a_bits, b_bits, width + fraction) == explicit
    return {"enumerated_integer_intervals": checked,
            "signed_positive_negative_power_boundaries": boundaries,
            "pytest_cases_claimed": 0}


def library_path(source):
    raw = source.get("library_workspace_relative", source.get("library"))
    if not isinstance(raw, str) or not raw:
        raise ValueError("actual source library location required")
    path = Path(raw)
    path = path if path.is_absolute() else ROOT / path
    path = path.resolve()
    path.relative_to(ROOT.resolve())
    if not path.is_dir():
        raise ValueError("actual source library does not exist locally")
    return path


def archive_inputs():
    """Read and hash actual immutable source inputs before any range analysis."""
    frozen, data = {}, {}
    for case in CASES:
        paths = {name: BASELINE / case / name
                 for name in ("target.json", "source.json", "schedule_capped.json")}
        target, source, schedule = (read(paths[name]) for name in paths)
        for path in paths.values():
            frozen[relative(path)] = digest(path)
        archive = library_path(source)
        keys = source["library_keys"]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate source library key")
        entries = {}
        for key in keys:
            if (not isinstance(key, str) or len(key) != 20
                    or any(c not in "0123456789abcdef" for c in key)):
                raise ValueError("canonical actual leaf key required")
            path = archive / (key + ".json")
            entry = read(path)
            if entry.get("key") != key or entry.get("gate_file") != key + ".npy":
                raise ValueError("actual leaf key/file binding mismatch")
            binary = archive / entry["gate_file"]
            gate_sha = digest(binary)
            if entry.get("sha256") != gate_sha:
                raise ValueError("actual leaf gate bytes differ from declared SHA")
            frozen[relative(path)], frozen[relative(binary)] = digest(path), gate_sha
            entries[key] = {"entry": entry, "metadata_sha256": digest(path),
                            "gate_sha256": gate_sha}
        data[case] = target, source, schedule, entries
    return frozen, data


def validate_bindings(target, source, schedule, entries):
    context = SSAContext(target)
    width = context.target["width"]
    if (width, target["fraction_bits"]) != (72, 40):
        raise ValueError("inventory is bound to native72/f40 accepted source")
    if (source["word_width"], source["fraction_bits"]) != (width, target["fraction_bits"]):
        raise ValueError("target/source precision mismatch")
    if source["inputs"] != [n for n in target["nodes"] if n["op"] == "input"]:
        raise ValueError("target/source declared input-law mismatch")
    if source["outputs"] != target["outputs"] or source["values"] != len(context.producers):
        raise ValueError("target/source output or SSA allocation mismatch")
    if (schedule["source_fingerprint"] != fingerprint(source)
            or schedule["target_fingerprint"] != fingerprint(target)):
        raise ValueError("actual schedule is not bound to this source/target")
    noninputs = [(i, n) for i, n in enumerate(target["nodes"]) if n["op"] != "input"]
    calls = source["forward_calls"]
    if len(noninputs) != len(calls):
        raise ValueError("target/source forward-call count mismatch")
    if set(source["library_keys"]) != {call["leaf"] for call in calls}:
        raise ValueError("source library keys differ from actual invocation keys")
    for (_, node), call in zip(noninputs, calls, strict=True):
        if (node["args"], node["out"]) != (call["args"], call["out"]):
            raise ValueError("target/source actual invocation binding mismatch")
        entry = entries[call["leaf"]]["entry"]
        if (entry["op"], entry["params"]) != (node["op"], node["params"]):
            raise ValueError("actual leaf operation/params differ from target")
        if len(entry["args"]) != len(node["args"]) or len(entry["outs"]) != len(node["out"]):
            raise ValueError("actual leaf native register arity mismatch")
        if node["op"] == "mul":
            expected = [list(range(width)), list(range(width, 2 * width))]
            if (entry["args"] != expected
                    or entry["outs"] != [list(range(2 * width, 3 * width))]
                    or node["params"] != {}):
                raise ValueError("generic multiply must retain its native two-argument interface")
    return noninputs, context.locations


def inventory_case(case, target, source, schedule, entries):
    noninputs, locations = validate_bindings(target, source, schedule, entries)
    bounds, rules = bound_graph(target)
    width, product_bits = target["width"], target["width"] + target["fraction_bits"]
    sites = []
    for call_index, ((node_index, node), call) in enumerate(
        zip(noninputs, source["forward_calls"], strict=True)
    ):
        if node["op"] != "mul":
            continue
        operands = []
        for value in node["args"]:
            low, high = bounds[value]
            minimum = signed_bits(low, high, width)
            operands.append({
                "ssa_value": value, "inclusive_signed_interval": [low, high],
                "minimum_signed_bits": minimum, "interval_rule": rules[value],
                "producer_node_index": locations[value],
                "proved_candidate_signed_bits": [b for b in CANDIDATE_BITS
                                                 if signed_guard(low, high, b)],
                "full_word_fallback": (low, high) == (-(1 << 71), (1 << 71) - 1),
            })
        a_bits, b_bits = (operand["minimum_signed_bits"] for operand in operands)
        variants = []
        for candidate_a in CANDIDATE_BITS:
            for candidate_b in CANDIDATE_BITS:
                a_proved = candidate_a in operands[0]["proved_candidate_signed_bits"]
                b_proved = candidate_b in operands[1]["proved_candidate_signed_bits"]
                variants.append({"signed_a_bits": candidate_a, "signed_b_bits": candidate_b,
                                 "a_guard_proved": a_proved, "b_guard_proved": b_proved,
                                 "both_guards_proved": a_proved and b_proved})
        info = entries[call["leaf"]]
        sites.append({
            "case": case, "node_index": node_index, "forward_call_index": call_index,
            "arguments": node["args"], "outputs": node["out"], "operands": operands,
            "same_ssa_arguments": node["args"][0] == node["args"][1],
            "current_leaf_key": call["leaf"],
            "current_leaf_metadata_sha256": info["metadata_sha256"],
            "current_leaf_gate_sha256": info["gate_sha256"],
            "current_leaf_lowering": info["entry"].get("spec", {}).get("lowering"),
            "current_leaf_input_contract": info["entry"].get("input_contract", {}),
            "candidate_signed_width_pairs": variants,
            "diagnostic_partial_planes": {
                "minimum_signed_raw_pair_terms": a_bits * b_bits,
                "minimum_signed_retained_pair_terms": retained_plane_terms(
                    a_bits, b_bits, product_bits),
                "native_full_raw_pair_terms": width * width,
                "native_full_retained_pair_terms": retained_plane_terms(width, width, product_bits),
                "no_resource_credit": True,
            },
        })
    pair_counts = Counter(
        f"{s['operands'][0]['minimum_signed_bits']}x{s['operands'][1]['minimum_signed_bits']}"
        for s in sites
    )
    summary = {
        "case": case, "multiply_calls": len(sites),
        "same_ssa_calls": sum(s["same_ssa_arguments"] for s in sites),
        "distinct_ssa_calls": sum(not s["same_ssa_arguments"] for s in sites),
        "minimum_signed_width_pair_inventory": dict(sorted(pair_counts.items())),
        "both_minimum_widths24_or_less": sum(all(o["minimum_signed_bits"] <= 24
                                               for o in s["operands"]) for s in sites),
        "both_minimum_widths40_or_less": sum(all(o["minimum_signed_bits"] <= 40
                                               for o in s["operands"]) for s in sites),
        "at_least_one_operand40_or_less": sum(any(o["minimum_signed_bits"] <= 40
                                                for o in s["operands"]) for s in sites),
        "full_word_fallback_operand_count": sum(o["full_word_fallback"]
                                                for s in sites for o in s["operands"]),
        "candidate_pair_proved_call_counts": {
            f"{a}x{b}": sum(v["both_guards_proved"] for s in sites
                             for v in s["candidate_signed_width_pairs"]
                             if (v["signed_a_bits"], v["signed_b_bits"]) == (a, b))
            for a in CANDIDATE_BITS for b in CANDIDATE_BITS
        },
    }
    assert summary["candidate_pair_proved_call_counts"]["72x72"] == len(sites)
    return sites, summary


def run(output, audit_root=AUDIT):
    output = output.resolve()
    output.relative_to(PROGRAM.resolve())
    audit_root = audit_root.resolve()
    audit_root.relative_to(PROGRAM.resolve())
    baseline_summary = read(BASELINE / "summary.json")
    audit_summary = read(audit_root / "summary.json")
    if not baseline_summary.get("passed") or baseline_summary.get("accepted") is not True:
        raise ValueError("expected non-restoring baseline has not been accepted")
    if (audit_summary.get("passed") is not True or audit_summary.get("accepted") is not True
            or audit_summary.get("source_root") != relative(BASELINE)):
        raise ValueError("passing independent audit must attest the exact accepted source")
    progress = read(PROGRAM / "progress.json")
    if (progress.get("accepted_baseline") != relative(BASELINE)
            or progress.get("local_only") is not True):
        raise ValueError("progress accepted baseline does not match this local inventory")
    output.mkdir(exist_ok=False)
    frozen, archives = archive_inputs()
    dependencies = [Path(__file__).resolve(),
                    ROOT / "research/limitation_program_20261001/interval_bounds.py",
                    ROOT / "research/limitation_program_20261001/prove_log_exponent.py"]
    snapshot = output / "executed_code"
    snapshot.mkdir()
    for path in dependencies:
        frozen[relative(path)] = digest(path)
        shutil.copy2(path, snapshot / path.name)
    for receipt in (BASELINE, audit_root):
        for name in ("manifest.json", "summary.json", "verification.json"):
            path = receipt / name
            frozen[relative(path)] = digest(path)
        if read(receipt / "verification.json").get("passed") is not True:
            raise ValueError("accepted source and independent audit verification must pass")
    save(output / "accepted_progress_snapshot.json", progress)
    interpreter = Path(sys.executable).resolve()
    protocol = {
        "created_utc": datetime.now(timezone.utc).isoformat(), "before_analysis": True,
        "local_only": True, "baseline": relative(BASELINE),
        "independent_audit": relative(audit_root),
        "family": "actual genericmul same-SSA inclusive signed interval inventory",
        "candidate_operand_bits": list(CANDIDATE_BITS), "native_word_bits": 72,
        "fraction_bits": 40, "product_modulus_bits": 112,
        "purpose": "Establish independent actual-operand signed-width guards before circuit work",
        "guard": "Each whole operand interval fits signed n bits; native high bits sign extend",
        "scope": "Exact digital-domain intervals; full72 fallback for unproved narrower guards",
        "diagnostics": "nA*nB/retained partial-plane counts only; no saving estimate or credit",
        "exclusions": "No emitted multiplier, savings, adoption, new pytest count or G2-G5 closure",
        "frozen_inputs": frozen,
        "progress_snapshot_sha256": digest(output / "accepted_progress_snapshot.json"),
        "environment": {"python": platform.python_version(), "executable": str(interpreter),
                        "executable_sha256": digest(interpreter),
                        **{name: metadata.version(name) for name in ("numpy", "numba", "pytest")}},
    }
    save(output / "protocol.json", protocol)
    started = time.perf_counter()
    try:
        checks, cases = check_small_intervals(), []
        for case in CASES:
            sites, case_summary = inventory_case(case, *archives[case])
            save(output / (case + "_multiplier_sites.json"), sites)
            cases.append(case_summary)
        assert all(digest(ROOT / path) == sha for path, sha in frozen.items())
        assert digest(interpreter) == protocol["environment"]["executable_sha256"]
        summary = {
            "passed": True, "baseline": relative(BASELINE),
            "independent_audit": relative(audit_root),
            "cases": cases, "classification_checks": checks,
            "source_actual_bindings_validated": True,
            "all_declared_digital_inputs_covered_by_intervals": True,
            "realized_savings": False, "financial_function_changed": False,
            "new_leaf_emitted": False, "source_adoption": False, "G2_G5": "unresolved",
            "diagnostic_limit": "Planes omit sign corrections/extension, low carries, CSA/final "
                                "adder, native copies and cleanup; no saving is claimed",
            "next": "Choose one proved signed-width multiplier; preserve native72 args/output, "
                    "floor low carries, sign extension, arbitrary output XOR and cleanup",
            "elapsed_seconds": time.perf_counter() - started,
        }
        save(output / "summary.json", summary)
        save(output / "verification.json", {
            "passed": True, "frozen_inputs_unchanged": True,
            "actual_SSA_source_schedule_bindings": True,
            "independent_interval_decode_oracle": checks,
            "producer_sha256": digest(Path(__file__)), "new_pytest_cases": 0,
            "new_financial_replays": 0, "resource_credit": False,
        })
        print(json.dumps({"passed": True, "cases": cases}), flush=True)
    except Exception as error:
        save(output / "failure.json", {
            "passed": False, "type": type(error).__name__, "error": str(error),
        })
        raise
    finally:
        files = {relative(path): digest(path) for path in sorted(output.rglob("*"))
                 if path.is_file() and path.name != "manifest.json"}
        save(output / "manifest.json", {"files": files, "frozen_inputs": frozen,
                                       "manifest_self_hash_excluded": True})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--audit-root", default=AUDIT, type=Path)
    args = parser.parse_args()
    run(args.output, args.audit_root)
