"""Independent text/AST review receipt; imports no A13 or A14 scientific module."""

import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PINS = {
    "verified_membership_index_v1.py": "32a6757a5af72f271d2a5b0f7eb61ab0f5d1e45ed11b85e7d18b87e0f34e3d4c",
    "membership_index_finite_qa_v1.py": "7aa19074645fb712587fd447e0000783afb1fd93900b71aae120eeb4409f2f12",
    "MEMBERSHIP_INDEX_FINITE_QA_PREFLIGHT.md": "8db966d25976bfafecf93d92984278c11ac5e826c306037753f9d61a4cb4315e",
    "membership_index_finite_qa_preflight.json": "d86621a4032765231a1c391669d6eb508c403bf6fac172a941f61349539cd3e1",
}


def main():
    folder = ROOT / "research/limitation_program_20261001/continuation_20261004/A13"
    for name, pin in PINS.items():
        data = (folder / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != pin:
            raise ValueError("Reviewed A13 author bytes changed: " + name)
        if name.endswith(".py"):
            tree = ast.parse(data.decode("utf-8"))
            compile(tree, str(folder / name), "exec")
    receipt = {
        "schema": "a13-membership-finite-qa-independent-static-review-v1",
        "reviewed_UTC": datetime.now(timezone.utc).isoformat(),
        "reviewer_agent": "/root/a14_continuation",
        "reviewed_exact_files": {
            (folder / name).relative_to(ROOT).as_posix(): pin for name, pin in PINS.items()
        },
        "static_review_passed": True,
        "code_import_or_scientific_execution": False,
        "findings": [
            "Exact tuple-key grouping records each original position; append induction proves equivalence to existential membership on fixed complete string-typed snapshots.",
            "No normalization, casefolding, canonicalization, deduplication of full rows or expected-hash replacement; duplicates and same-path multiple hashes retained.",
            "Legacy isolated any-expression comes from fixed V5 SHA, with exact variable-set guard; historical module/scientific definitions are not imported or executed.",
            "Eight fixed atoms at lengths0..4 give4681 ordered corpora; twelve queries yield56172 equality/position comparisons, including empty corpus, duplicates, case/hash/prefix/archive mismatches.",
            "Four malformed-record guards and three top-level snapshot guards have fixed acceptance; recursive metadata immutability is not claimed and existing primitive-field assumption is explicit.",
            "Six selected files are prospectively frozen and freshly checked at admission/terminal; sealed profile full maps and complete runtime provenance are expressly outside scope.",
            "Fixed25CPU/20admission/90wall starts at controller load; selected15CPU/65wall is conservative because it includes admission. One fresh output and authoritative failure marker retain failed partials.",
            "All20 approval, scientific adoption, measured speedup, complete budget feasibility and fixture/replay credit remain false.",
        ],
        "material_objections": [],
        "remaining_obligations": [
            "Parent ROOT six-file freeze before finite QA execution.",
            "Actual complete finite QA and terminal integrity within fixed caps.",
            "Separate integration/full-metadata profile and remaining mathematics budget assessment before any all20 release.",
        ],
        "all20_approval": False, "new_fixture_credit": 0,
    }
    with (HERE / "A13_INDEPENDENT_STATIC_REVIEW_run001.json").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"static_review_passed": True, "reviewed_files": len(PINS), "scientific_execution": False}))


if __name__ == "__main__":
    main()
