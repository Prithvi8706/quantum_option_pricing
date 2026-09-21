"""Independent, bounded, standard-library inspection of frozen resource evidence.

Question fixed before this check: do the archived component counts, schedules,
two CX ledgers, selected ratios and claimed inventories support the closeout?
Menu: the existing 148 primary layout rows, 18 residual rows and two selected
reflection references. Fixed-route sensitivity holds those selected circuits
fixed and adds common dollar allowances {0,.025,.05,.1,.15,.2}; it is neither
physical-error estimation nor a newly optimized menu. No acquisitions, circuit
emission, simulation or fitting.
Pass criterion: exact integer ledger/hash equality and rational schedule checks.
Run from any directory; optionally pass a NEW output JSON filename.
"""

import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "results/journal_sprint"
PI_UP = F("3.141592653589793238462643383279502884197169399375105820974944592307816406286209")
PI_LO = PI_UP - F(1, 10**78)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def native(counts):
    return {"cx": counts["cx"] + 6 * counts["ccx"], "u": counts["x"] + 9 * counts["ccx"]}


def check_archive(name):
    path = BASE / name
    manifest = read(path / "complete.json")["sha256"]
    for name, digest in manifest.items():
        require(sha(path / name) == digest, "archive hash " + name)
    actual = {p.relative_to(path).as_posix() for p in path.rglob("*") if p.is_file()}
    require(actual == set(manifest) | {"complete.json"}, "complete file inventory")
    planned = read(path / "planned.json")
    entries = 0
    for names in (planned["source_sha256"], planned["input_sha256"]):
        for name, digest in names.items():
            require(sha(ROOT / name) == digest, "live source/input hash " + name)
            entries += 1
    # This is a new independent commit binding check, not the original verifier.
    checked = 0
    normalized = 0
    for name in planned["source_sha256"]:
        blob = subprocess.check_output(["git", "show", planned["git_head"] + ":" + name], cwd=ROOT)
        disk = (ROOT / name).read_bytes()
        strict = name.startswith("research/stronger_arithmetic/") or name in (
            "docs/release/STRONGER_ARITHMETIC_PROTOCOL_20260921.md",
            "docs/release/SIGNED_RESIDUAL_PROTOCOL_20260921.md",
        )
        if strict:
            require(blob == disk, "strict source commit bytes " + name)
        else:
            require(blob.replace(b"\r\n", b"\n") == disk.replace(b"\r\n", b"\n"), "source commit text " + name)
            normalized += blob != disk
        checked += 1
    return {"files_hashed": len(manifest), "source_and_input_entries_hashed": entries,
            "source_commit_files_checked": checked, "newline_normalized_files": normalized,
            "acquisition_head": planned["git_head"], "tracked_tree_dirty_at_acquisition": planned["tracked_tree_dirty"]}


def check_row(row, reflection=False):
    r, b = row["resources"], row["budget"]
    s = b["schedule"]
    require(row.get("status", "ideal_plan") == "ideal_plan", "row feasibility")
    m, reps, bits = s["M"], s["repetitions"], s["phase_qubits"]
    require(reps == 17 and m == 1 << bits and s["a_calls"] == reps * (2*m-1), "AE count")
    require(s["a_calls"] <= 10_000_000, "query cap")
    a, controlled, z = (r[k] for k in ("a_cx_projection", "controlled_a_cx_projection", "zero_reflection_cx_projection"))
    iqft = bits * (bits-1) + 3 * (bits//2)
    require(r["total_cx_projection"] == reps*(a+(m-1)*(2*controlled+z+1)+iqft), "conservative ledger")
    require(r["control_cancelled_total_cx_projection"] == reps*(a+(m-1)*(2*a+z+1)+iqft), "cancelled ledger")
    if not reflection:
        require(controlled == 6*a + 2*r["a_u_projection"], "controlled oracle")
        require(r["total_qubits"] == 2*r["a_qubits"]-2+bits, "allocated width")
        require(z == 6*r["a_qubits"]-6, "zero reflection component formula")
    slope = 2*F(b["beta"]) if reflection else F(b["sensitivity_upper"])
    deterministic = F(b["deterministic_upper"])
    # Different pi enclosure and formula implementation from frozen schedule.
    require(deterministic+slope*(PI_UP/m+PI_UP**2/m**2) <= 1, "one-dollar bound")
    require(deterministic+slope*(PI_LO/(m//2)+PI_LO**2/(m//2)**2) > 1, "minimal dyadic M")
    return {"deterministic_upper": float(deterministic), "slope_upper": float(slope), "M": m,
            "a_calls": s["a_calls"], "a_cx": a, "conservative_cx": r["total_cx_projection"],
            "control_cancelled_cx": r["control_cancelled_total_cx_projection"], "total_qubits": r["total_qubits"],
            "one_dollar_remaining_margin": float(1-deterministic-slope*(PI_UP/m+PI_UP**2/m**2))}


def main():
    report = {"scope": "read-only independent archival arithmetic and provenance check; no new acquisition or gate emission",
              "date": "2026-09-21", "archives": {}}
    for name in ("stronger_arithmetic_v1", "signed_residual_arithmetic_v1"):
        report["archives"][name] = check_archive(name)
    primary = read(BASE / "stronger_arithmetic_v1/results.json")
    residual = read(BASE / "signed_residual_arithmetic_v1/results.json")
    require(len(primary["rows"]) == 148 and len(residual["rows"]) == 18, "declared menu cardinality")
    loader = read(BASE / "stronger_arithmetic_v1/loader.json")["resources"]
    record_by_spec, groups = {}, defaultdict(list)
    for path in sorted((BASE / "stronger_arithmetic_v1").glob("D?_??.json")):
        rec = read(path)
        key = (rec["case"], json.dumps(rec["spec"], sort_keys=True))
        require(key not in record_by_spec, "unique primary spec")
        record_by_spec[key] = rec
        plan = rec["plan"]
        coefficients = list(plan["exp_budget"]["coefficients"])
        while coefficients and not coefficients[-1]:
            coefficients.pop()
        # Circuit-defining parameters, not nominal degree or error certificate.
        identity = json.dumps({"case": rec["case"], "f": plan["fraction_bits"], "w": plan["width"],
                               "s": plan.get("reductions", 0), "coefficients": coefficients,
                               "affine_rows": plan["affine_rows"], "spot": plan.get("spot", 1)}, sort_keys=True)
        groups[identity].append(path.name)
        require(rec["components"]["retained"]["total"] == rec["components"]["reused"]["total"], "scratch reuse gate identity")
    for row in primary["rows"]:
        check_row(row)
        rec = record_by_spec[(row["case"], json.dumps(row["spec"], sort_keys=True))]
        comp = rec["components"][row["layout"]]
        calculated = native(comp["total"])
        dimension = len(rec["plan"]["affine_rows"])
        require(row["resources"]["a_cx_projection"] == calculated["cx"] + dimension*loader["cx"], "primary full A CX")
        require(row["resources"]["a_u_projection"] == calculated["u"] + dimension*loader["u"] + rec["plan"]["selector_bits"]+1, "primary full A U")
    residual_groups = defaultdict(list)
    for path in sorted((BASE / "signed_residual_arithmetic_v1").glob("D?_??.json")):
        rec = read(path)
        check_row(rec)
        comp, cert = rec["components"], rec["certificate"]
        parent = record_by_spec[(rec["case"], json.dumps(rec["spec"], sort_keys=True))]
        source = parent["components"]["reused"]
        require(cert["parent_plan"] == parent["plan"], "residual parent plan")
        for gate in ("x", "cx", "ccx"):
            expected = 2*source["conversion_forward"][gate]+2*source["aggregation"][gate]+comp["complete_postoracle"][gate]
            require(comp["total"][gate] == expected, "all inherited inverses/oracle counted")
        calculated = native(comp["total"])
        require(rec["resources"]["a_cx_projection"] == calculated["cx"]+cert["dimension"]*loader["cx"], "residual full A CX")
        require(rec["resources"]["a_u_projection"] == calculated["u"]+cert["dimension"]*loader["u"]+cert["selector_bits"]+1, "residual full A U")
        require(comp["qubits"] == sum(comp["wire_layout"].values()), "residual width components")
        coefficients = list(parent["plan"]["exp_budget"]["coefficients"])
        while coefficients and not coefficients[-1]:
            coefficients.pop()
        fingerprint = json.dumps({"case": rec["case"], "spec": {k:v for k,v in rec["spec"].items() if k != "degree"},
                                  "coefficients": coefficients,
                                  "oracle": comp["total"]}, sort_keys=True)
        residual_groups[fingerprint].append(path.name)
    report["primary_rows_checked"] = 148
    report["residual_rows_checked"] = 18
    report["cx_ledgers_checked"] = 332
    report["primary_distinct_circuit_parameter_groups"] = len(groups)
    report["primary_duplicate_groups"] = [v for v in groups.values() if len(v)>1]
    report["residual_distinct_circuit_parameter_groups"] = len(residual_groups)
    report["residual_duplicate_groups"] = [v for v in residual_groups.values() if len(v)>1]
    report["selected"] = {}
    for case in ("D1", "D2"):
        raw = min((r for r in primary["rows"] if r["case"] == case), key=lambda r:r["resources"]["control_cancelled_total_cx_projection"])
        res = min((r for r in residual["rows"] if r["case"] == case), key=lambda r:r["resources"]["control_cancelled_total_cx_projection"])
        parent = next(r for r in primary["rows"] if r["case"] == case and r["spec"] == res["spec"] and r["layout"] == "reused")
        reflection = next(r for r in primary["summary"] if r["case"] == case)["reflection_reference"]
        data = {"raw_best": check_row(raw), "raw_matched_parent": check_row(parent), "residual": check_row(res), "reflection": check_row(reflection, True)}
        data["ratios"] = {"reflection_over_residual_cx": float(F(data["reflection"]["control_cancelled_cx"], data["residual"]["control_cancelled_cx"])),
                          "reflection_over_residual_conservative": float(F(data["reflection"]["conservative_cx"], data["residual"]["conservative_cx"])),
                          "residual_over_reflection_width": float(F(data["residual"]["total_qubits"], data["reflection"]["total_qubits"])),
                          "parent_over_residual_cx": float(F(data["raw_matched_parent"]["control_cancelled_cx"], data["residual"]["control_cancelled_cx"])),
                          "residual_over_parent_a_cx": float(F(data["residual"]["a_cx"], data["raw_matched_parent"]["a_cx"]))}
        report["selected"][case] = data
    report["fixed_route_extra_dollar_allowance_sensitivity"] = []
    for case in ("D1", "D2"):
        for extra in ("0", ".025", ".05", ".1", ".15", ".2"):
            item = {"case": case, "extra_deterministic_dollars": extra,
                    "scope": "fixed selected circuits; no route/menu reoptimization or measured physical error"}
            for name in ("reflection", "residual"):
                row = (next(r for r in primary["summary"] if r["case"] == case)["reflection_reference"] if name == "reflection"
                       else min((r for r in residual["rows"] if r["case"] == case), key=lambda r:r["resources"]["control_cancelled_total_cx_projection"]))
                b, r = row["budget"], row["resources"]
                slope = 2*F(b["beta"]) if name == "reflection" else F(b["sensitivity_upper"])
                remaining = 1-F(b["deterministic_upper"])-F(extra)
                require(remaining>0, "positive fixed sensitivity budget")
                m = 2
                while slope*(PI_UP/m+PI_UP**2/m**2)>remaining:
                    m *= 2
                bits = m.bit_length()-1
                cx = 17*(r["a_cx_projection"]+(m-1)*(2*r["a_cx_projection"]+r["zero_reflection_cx_projection"]+1)
                         +bits*(bits-1)+3*(bits//2))
                item[name] = {"M": m, "control_cancelled_cx": cx}
            item["reflection_over_residual_cx"] = float(F(item["reflection"]["control_cancelled_cx"],item["residual"]["control_cancelled_cx"]))
            report["fixed_route_extra_dollar_allowance_sensitivity"].append(item)
    report["reflections_checked"] = 2
    report["confidence_bound"] = {"repetitions": 17, "assumed_independent_single_run_success_lower": .8,
                                  "hoeffding_failure_upper": math.exp(-2*17*.3**2)}
    receipts = {}
    for name in ("stronger_arithmetic_full_tests_20260921.xml", "stronger_arithmetic_pinned_tests_20260921.xml"):
        root = ET.parse(BASE / name).getroot()
        cases = root.findall(".//testcase")
        require(cases and not root.findall(".//failure") and not root.findall(".//error") and not root.findall(".//skipped"), "passing test receipt")
        receipts[name] = {"actual_testcase_elements": len(cases), "sha256": sha(BASE/name), "scope": "historical receipt; not rerun"}
    report["test_receipts"] = receipts
    report["classical_existing_development"] = [{k:r[k] for k in ("case", "method", "power", "price", "approximate_95_halfwidth", "paths_with_pilot", "rigorous_coverage_certificate")}
        for r in read(BASE / "minimal_pivot_week2_classical_v1/results.json") if r["case"] in ("D1", "D2") and r["power"] == 12]
    report["passed"] = True
    report["checker_sha256"] = sha(Path(__file__))
    payload = json.dumps(report, indent=2)+"\n"
    if len(sys.argv) == 2:
        with Path(sys.argv[1]).open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
    else:
        print(payload)


if __name__ == "__main__":
    main()
