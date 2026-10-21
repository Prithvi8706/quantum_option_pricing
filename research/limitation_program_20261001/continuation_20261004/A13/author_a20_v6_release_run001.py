"""Metadata-only authoring: no scientific source imports or execution."""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "research/limitation_program_20261001"
OWN = Path(__file__).parent


def pin(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, content):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(content)


def save(path, value):
    write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


old_record = json.loads((OWN / "A20_V5_AUTHOR_PINS_run001.json").read_text())
for key, expected in old_record["author_sha256"].items():
    assert pin(ROOT / key) == expected, ("immutable V5 pin", key)

names = [
    "arithmetic_free_basket_signal_continuation_v6.py",
    "a20_signal_receipt_continuation_v6.py",
    "experiment_arithmetic_free_basket_signal_continuation_v6.py",
    "audit_arithmetic_free_basket_signal_continuation_v6.py",
    "A20_COMPARATOR_PHASE_CONTINUATION_PREFLIGHT_V6.md",
    "a20_comparator_phase_continuation_preflight_v6.json",
]
assert not any((BASE / name).exists() for name in names)
for role in ("producer", "audit"):
    assert not (ROOT / f"results/limitation_program_20261001/A20_continuation_20261004_{role}_run004").exists()

# The selective release-name mapping never changes an arbitrary run003 path.
replacements = {
    name.replace("_v6", "_v5").replace("_V6", "_V5"): name
    for name in names
}
replacements.update({
    "a20_comparator_phase_continuation_preflight_v4.json": names[-1],
    "A20-comparator-phase-static-READY-v5": "A20-comparator-phase-static-READY-v6",
    "A20_continuation_20261004_producer_run003": "A20_continuation_20261004_producer_run004",
    "A20_continuation_20261004_audit_run003": "A20_continuation_20261004_audit_run004",
    "E03_support_audit_run003/B4x12_audit.json": "E03_support_audit_run002/B4x12_audit.json",
})
for stem in (
    "arithmetic_free_basket_signal", "a20_signal_receipt",
    "experiment_arithmetic_free_basket_signal", "audit_arithmetic_free_basket_signal",
):
    replacements[f"{stem}_continuation_v5"] = f"{stem}_continuation_v6"


def replace_release(text):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


code = {}
string_diffs = []
definition_diffs = []
for name in names[:4]:
    old_name = name.replace("_v6", "_v5")
    old_text = (BASE / old_name).read_text()
    new_text = replace_release(old_text)
    old_ast, new_ast = ast.parse(old_text), ast.parse(new_text)
    compile(new_ast, str(BASE / name), "exec")  # compile only, no execution or pycache
    old_strings = [n for n in ast.walk(old_ast) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    new_strings = [n for n in ast.walk(new_ast) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    assert len(old_strings) == len(new_strings)
    for old, new in zip(old_strings, new_strings):
        assert replace_release(old.value) == new.value
        if old.value != new.value:
            string_diffs.append({"file": name, "line": new.lineno, "old": old.value, "new": new.value})
    # Preserve every node, statement, numeric literal, import and string except
    # precisely the above selective names/routes. This includes top-level paths.
    assert ast.dump(ast.parse(replace_release(old_text)), include_attributes=False) == ast.dump(new_ast, include_attributes=False)
    for n in ast.walk(new_ast):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            assert "E03_support_audit_run003" not in n.value
            assert "a20_comparator_phase_continuation_preflight_v4.json" not in n.value
            assert "_continuation_v5" not in n.value
    def definitions(tree):
        return {n.name: ast.dump(n, include_attributes=False) for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    before, after = definitions(old_ast), definitions(new_ast)
    definition_diffs.append({
        "file": name,
        "changed": sorted(k for k in before.keys() & after.keys() if before[k] != after[k]),
        "added": sorted(after.keys() - before.keys()),
        "removed": sorted(before.keys() - after.keys()),
        "unchanged": sum(before[k] == after[k] for k in before.keys() & after.keys()),
    })
    code[name] = new_text

receipt_ast = ast.parse(code[names[1]])
actual_authors = next(ast.literal_eval(n.value) for n in receipt_ast.body
                      if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "AUTHOR_NAMES" for t in n.targets))
assert actual_authors == tuple(names)
ready_keys = sorted({n.slice.value for n in ast.walk(receipt_ast)
    if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Attribute)
    and n.value.attr == "ready" and isinstance(n.slice, ast.Constant)
    and isinstance(n.slice.value, str)})

# FIRST the prospective V6 MD/JSON; then the four prepared code bytes.
old_preflight = json.loads((BASE / names[-1].replace("_v6", "_v5")).read_text())
preflight = json.loads(json.dumps(old_preflight))
for key in ("schema", "required_external_ROOT_READY_schema", "scientific_builder",
            "producer_module", "auditor_module", "producer_receipt", "audit_receipt"):
    preflight[key] = replace_release(preflight[key]).replace("preflight-v5", "preflight-v6")
preflight["prospective_preflight_authored_before_V6_code"] = True
preflight["V5_disposition"] = "STATIC_REJECTED_BEFORE_READY_OR_SCIENCE"
preflight["V6_operational_corrections"] = [
    "AUTHOR_NAMES binds exactly the six actual V6 source/preflight files.",
    "Producer and auditor E03 support paths restored to original pinned E03_support_audit_run002/B4x12_audit.json.",
    "Only A20 producer/audit output routes advance from run003 to fresh run004.",
    "All source string constants compared under an explicit selective mapping; no global run-number replacement.",
]
preflight["V6_scalar_gate_recipe_resource_semantics_unchanged_from_V5"] = True
preflight["required_ROOT_READY_fields"] = ready_keys
lineage = preflight["prior_attempt_sha256"]
retained = list(old_record["author_sha256"]) + [
    "research/limitation_program_20261001/continuation_20261004/A13/A20_V5_AUTHOR_PINS_run001.json",
    "research/limitation_program_20261001/continuation_20261004/A13/A20_V5_DEFINITION_DIFF_run001.json",
    "research/limitation_program_20261001/continuation_20261004/A20/ROOT_STATIC_REJECTION_v5.json",
    "research/limitation_program_20261001/continuation_20261004/A14/A20_V5_ROUTE_STATIC_REVIEW_run001.json",
    "docs/limitation_program_20261001/continuation_20261004/A13/A20_V5_ORDERED_COST_BOUNDARY_SUPPLEMENT.md",
    "docs/limitation_program_20261001/continuation_20261004/A14/A20_COMMUTATIVITY_REVIEW_v5.md",
    __file__.replace("\\", "/").split("/quantum_option_pricing/", 1)[-1],
]
for key in retained:
    expected = pin(ROOT / key)
    assert key not in lineage or lineage[key] == expected
    lineage[key] = expected
assert all(lineage[k] == v for k, v in old_preflight["prior_attempt_sha256"].items())
assert preflight["prior_attempt_external_runtime_sha256"] == old_preflight["prior_attempt_external_runtime_sha256"]

md = (BASE / names[-2].replace("_V6", "_V5")).read_text()
md = replace_release(md).replace("V5", "V6")
prefix = (
    "# V6 prospective operational correction (written before code)\n\n"
    "V5 was statically rejected before READY, preparation or science. Its six original bytes and pins remain immutable. "
    "This release corrects the actual six AUTHOR_NAMES identities, restores both support references to the original "
    "E03_support_audit_run002/B4x12_audit.json, and advances only A20's own receipts to fresh run004. "
    "Every code string constant and import is checked against an explicit selective release mapping. "
    "No arbitrary run003 path is changed. All V5 scientific functions, recipes, scalar arithmetic and resource definitions remain unchanged.\n\n"
    "The pinned ordered-cost supplement and independent A14 commutativity review retain the distinct original "
    "[72,40]/[40,72] depths1076/1012 and [72,24]/[24,72] depths1009/913. "
    "Canonicalization copies only comparison arguments. Original normalized nodes, hashes, evaluation order and each "
    "source cost contract remain ordered. Shared scalar content does not imply equal T-depth or physical performance.\n\n"
)
write(BASE / names[-2], prefix + md)
save(BASE / names[-1], preflight)
for name in names[:4]:
    write(BASE / name, code[name])

pins = {str((BASE / name).relative_to(ROOT).as_posix()): pin(BASE / name) for name in names}
save(OWN / "A20_V6_AUTHOR_PINS_run001.json", {
    "schema": "a20-v6-six-author-static-pins-v1", "scientific_execution": False,
    "author_sha256": pins, "preflight_authored_before_code": True,
    "original_V5_read_only": True, "V5_static_rejection_retained": True,
    "required_READY_schema": preflight["required_external_ROOT_READY_schema"],
    "required_READY_keys_both_roles": ready_keys,
    "audit_additional_READY_keys": ["producer_manifest_sha256"],
    "prior_ROOT_pins": len(lineage),
    "prior_external_runtime_pins": len(preflight["prior_attempt_external_runtime_sha256"]),
})
save(OWN / "A20_V6_COMPLETE_STRING_AND_DEFINITION_DIFF_run001.json", {
    "schema": "a20-v6-author-complete-static-diff-v1", "science_executed": False,
    "old_six_author_sha256": old_record["author_sha256"], "new_six_author_sha256": pins,
    "selective_mapping": replacements, "all_AST_string_constants_compared": True,
    "changed_string_constants": string_diffs, "definition_changes": definition_diffs,
    "all_nonrelease_code_bytes_preserved_under_exact_mapping": True,
    "builder_bytes_identical_to_V5": pin(BASE / names[0]) == pin(BASE / names[0].replace("_v6", "_v5")),
    "all_old_ROOT_lineage_retained": True, "all_old_external_lineage_retained": True,
    "all_scientific_counts_precision_budgets_unchanged": True,
    "V5_static_rejected_unexecuted": True,
})
for key, expected in old_record["author_sha256"].items():
    assert pin(ROOT / key) == expected
print(json.dumps({"author_sha256": pins, "ready_schema": preflight["required_external_ROOT_READY_schema"],
                  "READY_keys": ready_keys, "audit_extra": ["producer_manifest_sha256"],
                  "prior_ROOT_pins": len(lineage), "prior_external_pins": len(preflight["prior_attempt_external_runtime_sha256"]),
                  "changed_strings": len(string_diffs), "science_executed": False}, indent=2))
