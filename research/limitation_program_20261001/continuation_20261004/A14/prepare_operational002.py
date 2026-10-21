"""Preserve pre-mkdir admission failure and author a distinct operational release."""

import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[4]
OLD = Path(__file__).resolve().parent
NEW = OLD / "run002"
CAPTURE = ROOT / "results/limitation_program_20261001/A14_continuation_20261004_stage_k_admission_failure_run001"
MODULE = "research.limitation_program_20261001.continuation_20261004.A14"
PREFIX = "A14_continuation_20261004_stage_k"
START = time.monotonic()


def check():
    if time.process_time() >= 25 or time.monotonic() - START >= 90:
        raise ValueError("Fixed authoring/capture25CPU90wall")


def sha(path):
    check()
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, text):
    check()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def save(path, value):
    write(path, json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n")


def defs(text):
    return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(text).body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))}


def main():
    if NEW.exists() or CAPTURE.exists():
        raise ValueError("Exclusive fresh capture/release002")
    names = ("experiment_taylor_f44_stage_k.py", "taylor_f44_stage_k_source.py",
             "a14_taylor_f44_stage_k_implementation_preflight.json",
             "A14_TAYLOR_F44_STAGE_K_IMPLEMENTATION_PREFLIGHT.md",
             "authoring_freeze.json", "PRODUCER_ROOT_READY_run001.json", "producer_launch_run001.log")
    pins = {(OLD / name).relative_to(ROOT).as_posix(): sha(OLD / name) for name in names}
    if pins[(OLD / names[5]).relative_to(ROOT).as_posix()] != "3cdc703bcda036ab59bc84923873adf8acf01119356caeb1b7355c97839ee2f2":
        raise ValueError("Root-issued failed READY remains exact")
    log_text = (OLD / names[6]).read_text(encoding="utf-16")
    if "KeyError: 'limits_CPU_admission_wall'" not in log_text:
        raise ValueError("Exact failed admission witness")
    if (ROOT / f"results/limitation_program_20261001/{PREFIX}_producer_run001").exists():
        raise ValueError("Original output remains absent")
    old_ready = json.loads((OLD / names[5]).read_text(encoding="utf-8"))
    if "limits_CPU_admission_wall" in old_ready or old_ready["limits"] != [180,150,600]:
        raise ValueError("Exact observed failed field-map mismatch")
    CAPTURE.mkdir()
    for name in names:
        (CAPTURE / ("retained_" + name)).write_bytes((OLD / name).read_bytes())
    summary = {
        "schema": "a14-scoped-stage-k-admission-failure-preservation-v1",
        "preservation_passed": True, "original_attempt_passed": False,
        "original_attempt_failed": True, "original_output_absent": True,
        "failure_stage": "READY field admission before mkdir or builder import",
        "error": "KeyError: 'limits_CPU_admission_wall'",
        "scientific_execution": False, "gate_generation": False,
        "fixed88_diagnostics_executed": 0, "new_test_credit": 0,
        "complete_historical_owner_maps_or_runtime_rehashed": False,
        "scope": "Selected original source/READY/log bytes only; no global provenance claim",
        "frozen_inputs": pins, "created_UTC": datetime.now(timezone.utc).isoformat(),
        "budget_capture25CPU90wall": {"CPU": time.process_time(), "wall": time.monotonic()-START},
    }
    for key, pin in pins.items():
        if sha(ROOT / key) != pin:
            raise ValueError("Failure evidence changed while preserving")
    save(CAPTURE / "summary.json", summary)
    files = {p.name: sha(p) for p in CAPTURE.iterdir()}
    save(CAPTURE / "manifest.json", {
        "schema": "a14-scoped-stage-k-admission-failure-capture-manifest-v1",
        "files": files, "frozen_inputs": pins, "external_runtime_inputs": {},
        "manifest_self_hash_excluded": True, "preservation_passed": True,
        "original_attempt_passed": False, "scientific_execution": False, "new_test_credit": 0,
        "runtime_scope": "selected bytes only, no complete runtime provenance",
    })
    failure_pins = dict(pins)
    failure_pins[(CAPTURE / "manifest.json").relative_to(ROOT).as_posix()] = sha(CAPTURE / "manifest.json")
    for name, pin in files.items():
        failure_pins[(CAPTURE / name).relative_to(ROOT).as_posix()] = pin
    NEW.mkdir()
    compare = {}
    for name in ("experiment_taylor_f44_stage_k.py", "audit_taylor_f44_stage_k.py"):
        old = (OLD / name).read_text(encoding="utf-8")
        text = old.replace("parents[4]", "parents[5]")
        text = text.replace(MODULE + ".experiment_taylor_f44_stage_k", MODULE + ".run002.experiment_taylor_f44_stage_k")
        text = text.replace(MODULE + ".audit_taylor_f44_stage_k", MODULE + ".run002.audit_taylor_f44_stage_k")
        text = text.replace(MODULE + ".taylor_f44_stage_k_source", MODULE + ".run002.taylor_f44_stage_k_source")
        text = text.replace('"' + MODULE + '"', '"' + MODULE + '", "' + MODULE + '.run002"')
        text = text.replace(PREFIX + "_producer_run001", PREFIX + "_producer_run002")
        text = text.replace(PREFIX + "_audit_run001", PREFIX + "_audit_run002")
        text = text.replace("PRODUCER_ROOT_READY_run001.json", "PRODUCER_ROOT_READY_run002.json")
        text = text.replace("AUDIT_ROOT_READY_run001.json", "AUDIT_ROOT_READY_run002.json")
        text = text.replace("_STARTED = None", "_STARTED = None\nFAILURE_HISTORY = " + repr(failure_pins))
        anchor = '    ready = read(bind(READY, expected_ready))\n'
        if text.count(anchor) != 1:
            raise ValueError("Exactly one new admission entry")
        text = text.replace(anchor, anchor + '    for key, pin in FAILURE_HISTORY.items():\n        bind(ROOT / key, pin)\n', 1)
        a,b = defs(old),defs(text)
        changed = sorted(key for key in a if a[key]!=b[key])
        if a.keys() != b.keys() or changed != ["admission", "loaded_origins"]:
            raise ValueError("Operational002 exact AST boundary: " + repr(changed))
        compile(text, str(NEW / name), "exec")
        write(NEW / name, text)
        compare[name] = {"old_SHA256": sha(OLD / name), "new_SHA256": sha(NEW / name),
                         "retained_definitions": len(a)-len(changed), "changed_definitions": changed}
    (NEW / "taylor_f44_stage_k_source.py").write_bytes((OLD / "taylor_f44_stage_k_source.py").read_bytes())
    docname = "A14_TAYLOR_F44_STAGE_K_IMPLEMENTATION_PREFLIGHT.md"
    doc = (OLD / docname).read_text(encoding="utf-8")
    doc = doc.replace(MODULE + ".experiment_taylor_f44_stage_k", MODULE + ".run002.experiment_taylor_f44_stage_k")
    doc = doc.replace(PREFIX + "_producer_run001", PREFIX + "_producer_run002")
    doc = doc.replace("PRODUCER_ROOT_READY_run001.json", "run002/PRODUCER_ROOT_READY_run002.json")
    doc += """

## Distinct operational release002

The first scoped invocation001 failed before mkdir/builder import at the ROOT
release's missing `limits_CPU_admission_wall` key; its supplied key was `limits`.
Original source/READY/UTF16 launch log and selected-byte metadata capture remain
immutable. This is a separate newly reviewed release002, not a rerun001, failure
promotion or budget change. All88 diagnostics remain unexecuted before this release.
Both controllers bind all selected failed-attempt and preservation packet bytes
before work; complete prior source/audit expected maps stay unchanged. Namespace
root/route and this exact provenance admission are the sole operational changes;
builder bytes and every structural/arithmetic/replay/resource function remain fixed.
All new author/ROOT release files reside under A14/run002, and producer/auditor
outputs use fresh A14_continuation_20261004_stage_k_{producer,audit}_run002 names.
Admission must use `limits_CPU_admission_wall`, not `limits`; exact root required
field examples are in ROOT_READY_REQUIRED_FIELDS.json. ROOT must review and issue
the new SHA-bound release before the single invocation; original001 stays failed.
Every original mathematical/financial/adoption/Stage C/credit boundary is unchanged.
"""
    write(NEW / docname, doc)
    policy = json.loads((OLD / "a14_taylor_f44_stage_k_implementation_preflight.json").read_text(encoding="utf-8"))
    policy["author_SHA256"] = {n:sha(NEW/n) for n in ("experiment_taylor_f44_stage_k.py","taylor_f44_stage_k_source.py")}
    policy["method_document_SHA256"] = sha(NEW/docname)
    policy["fresh_receipt"] = "results/limitation_program_20261001/" + PREFIX + "_producer_run002"
    policy["external_ROOT_READY"] = (NEW / "PRODUCER_ROOT_READY_run002.json").relative_to(ROOT).as_posix()
    policy["CLI"][3] = MODULE + ".run002.experiment_taylor_f44_stage_k"
    policy["future_independent_checker_source_SHA256"] = sha(NEW/"audit_taylor_f44_stage_k.py")
    policy["failed_attempt001_expected_inputs"] = failure_pins
    save(NEW/"a14_taylor_f44_stage_k_implementation_preflight.json",policy)
    producer_names = ("experiment_taylor_f44_stage_k.py","taylor_f44_stage_k_source.py",
                      "a14_taylor_f44_stage_k_implementation_preflight.json",docname)
    producer_pins = {n:sha(NEW/n) for n in producer_names}
    audit_docname = "A14_TAYLOR_F44_STAGE_K_AUDIT_PREFLIGHT.md"
    audit_doc = (OLD/audit_docname).read_text(encoding="utf-8")
    audit_doc = audit_doc.replace(MODULE + ".audit_taylor_f44_stage_k", MODULE + ".run002.audit_taylor_f44_stage_k")
    audit_doc = audit_doc.replace(PREFIX + "_audit_run001", PREFIX + "_audit_run002")
    audit_doc = audit_doc.replace("AUDIT_ROOT_READY_run001.json", "AUDIT_ROOT_READY_run002.json")
    audit_doc += "\nDistinct operational002 route and immutable admission-failure provenance match the producer method; all mathematical functions and88 corpus remain unchanged.\n"
    write(NEW/audit_docname,audit_doc)
    audit_policy = json.loads((OLD/"a14_taylor_f44_stage_k_audit_preflight.json").read_text(encoding="utf-8"))
    audit_policy["author_SHA256"] = {"audit_taylor_f44_stage_k.py":sha(NEW/"audit_taylor_f44_stage_k.py")}
    audit_policy["method_document_SHA256"] = sha(NEW/audit_docname)
    audit_policy["producer_author_method_SHA256"] = producer_pins
    audit_policy["fresh_receipt"] = "results/limitation_program_20261001/" + PREFIX + "_audit_run002"
    audit_policy["ROOT_READY_path"] = (NEW/"AUDIT_ROOT_READY_run002.json").relative_to(ROOT).as_posix()
    save(NEW/"a14_taylor_f44_stage_k_audit_preflight.json",audit_policy)
    audit_pins = {n:sha(NEW/n) for n in ("audit_taylor_f44_stage_k.py","a14_taylor_f44_stage_k_audit_preflight.json",audit_docname)}
    fields = {
        "schema": "root-a14-taylor-f44-stage-k-READY-v1", "ready": True,
        "root_and_independent_static_reviews_passed": True,
        "limits_CPU_admission_wall": [180,150,600],
        "output": policy["fresh_receipt"],
        "argv_prefix": ["-B","-m",MODULE+".run002.experiment_taylor_f44_stage_k","--ready-sha256"],
        "author_method_SHA256": producer_pins, "existing_new_code_cache_SHA256": {},
        "required_existing_packet_manifest_SHA256": policy["required_existing_packet_manifest_SHA256"],
    }
    # This is an unissued example file, never the active READY route.
    save(NEW/"ROOT_READY_REQUIRED_FIELDS.json",fields)
    freeze = {"schema":"a14-scoped-stage-k-operational002-author-freeze-v1",
              "producer_author_method_SHA256":producer_pins,"audit_author_method_SHA256":audit_pins,
              "definition_comparisons":compare,"failed_history_expected_SHA256":failure_pins,
              "builder_byte_identical":sha(NEW/"taylor_f44_stage_k_source.py")==sha(OLD/"taylor_f44_stage_k_source.py"),
              "ROOT_READY":False,"scientific_execution":False,"diagnostic_counts":[16,40,32,88],
              "failure_capture_manifest_SHA256":sha(CAPTURE/"manifest.json"),"new_test_credit":0}
    save(NEW/"authoring_freeze.json",freeze)
    check()
    print(json.dumps(freeze,sort_keys=True))


if __name__ == "__main__":
    main()
