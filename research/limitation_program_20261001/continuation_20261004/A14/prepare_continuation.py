"""Author scoped F44 Stage K sources; no imports or primitive execution."""

import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ORIGINAL = ROOT / "research/limitation_program_20261001"
LOCAL = Path(__file__).resolve().parent
DOCS = ROOT / "docs/limitation_program_20261001/continuation_20261004/A14"
MODULE = "research.limitation_program_20261001.continuation_20261004.A14"
PREFIX = "A14_continuation_20261004_stage_k"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def save(path, value):
    write(path, json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n")


def definitions(text):
    return {
        node.name: ast.dump(node, include_attributes=False)
        for node in ast.parse(text).body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    }


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"Exact author replacement count: {old!r}")
    return text.replace(old, new, 1)


def main():
    original_files = (
        "taylor_f44_stage_k_source.py", "experiment_taylor_f44_stage_k.py",
        "audit_taylor_f44_stage_k.py", "a14_taylor_f44_stage_k_implementation_preflight.json",
        "A14_TAYLOR_F44_STAGE_K_IMPLEMENTATION_PREFLIGHT.md",
        "a14_taylor_f44_prospectus_v1.json", "A14_TAYLOR_F44_PROSPECTUS_V1.md",
    )
    old_pins = {name: digest(ORIGINAL / name) for name in original_files}
    reports = {}
    for name in original_files[:3]:
        path = ORIGINAL / name
        old = path.read_text(encoding="utf-8")
        text = old
        if name != "taylor_f44_stage_k_source.py":
            text = replace_once(text, "ROOT = Path(__file__).resolve().parents[2]",
                                "ROOT = Path(__file__).resolve().parents[4]")
            text = replace_once(text, 'RESEARCH = ROOT / "research/limitation_program_20261001"',
                                'RESEARCH = Path(__file__).resolve().parent\nORIGINAL_RESEARCH = ROOT / "research/limitation_program_20261001"')
            text = replace_once(text, 'PROSPECTUS = RESEARCH / "a14_taylor_f44_prospectus_v1.json"',
                                'PROSPECTUS = ORIGINAL_RESEARCH / "a14_taylor_f44_prospectus_v1.json"')
            text = replace_once(text, 'PROSPECTUS_DOC = RESEARCH / "A14_TAYLOR_F44_PROSPECTUS_V1.md"',
                                'PROSPECTUS_DOC = ORIGINAL_RESEARCH / "A14_TAYLOR_F44_PROSPECTUS_V1.md"')
            if name == "experiment_taylor_f44_stage_k.py":
                text = replace_once(text, 'OUTPUT = PROGRAM / "A14_taylor_f44_stage_K_run001"',
                                    f'OUTPUT = PROGRAM / "{PREFIX}_producer_run001"')
                text = replace_once(text, 'READY = ROOT / ".context/A14_TAYLOR_F44_STAGE_K_ROOT_READY_run001.json"',
                                    'READY = RESEARCH / "PRODUCER_ROOT_READY_run001.json"')
                text = text.replace("research.limitation_program_20261001.taylor_f44_stage_k_source",
                                    MODULE + ".taylor_f44_stage_k_source")
                text = text.replace("research.limitation_program_20261001.experiment_taylor_f44_stage_k",
                                    MODULE + ".experiment_taylor_f44_stage_k")
                text = replace_once(text,
                    '{__name__, "research.limitation_program_20261001", BUILDER_MODULE}',
                    '{__name__, "research.limitation_program_20261001",\n'
                    '                                "research.limitation_program_20261001.continuation_20261004",\n'
                    f'                                "{MODULE}", BUILDER_MODULE}}')
                text = replace_once(text, "len(owned) < MAX_OWN_FILES and total <= MAX_OWN_BYTES",
                                    "len(owned) < MAX_OWN_FILES - 1 and total <= MAX_OWN_BYTES")
                allowed = {"loaded_origins", "admission", "main"}
            else:
                text = replace_once(text, 'SOURCE = PROGRAM / "A14_taylor_f44_stage_K_run001"',
                                    f'SOURCE = PROGRAM / "{PREFIX}_producer_run001"')
                text = replace_once(text, 'OUTPUT = PROGRAM / "A14_taylor_f44_stage_K_audit_run001"',
                                    f'OUTPUT = PROGRAM / "{PREFIX}_audit_run001"')
                text = replace_once(text, 'READY = ROOT / ".context/A14_TAYLOR_F44_STAGE_K_AUDIT_ROOT_READY_run001.json"',
                                    'READY = RESEARCH / "AUDIT_ROOT_READY_run001.json"')
                text = replace_once(text, 'SOURCE_READY = ROOT / ".context/A14_TAYLOR_F44_STAGE_K_ROOT_READY_run001.json"',
                                    'SOURCE_READY = RESEARCH / "PRODUCER_ROOT_READY_run001.json"')
                text = text.replace("research.limitation_program_20261001.audit_taylor_f44_stage_k",
                                    MODULE + ".audit_taylor_f44_stage_k")
                text = replace_once(text, '{__name__, "research.limitation_program_20261001"}',
                    '{__name__, "research.limitation_program_20261001",\n'
                    '                     "research.limitation_program_20261001.continuation_20261004",\n'
                    f'                     "{MODULE}"}}')
                allowed = {"loaded_origins", "admission"}
            old_defs, new_defs = definitions(old), definitions(text)
            changed = {key for key in old_defs if old_defs[key] != new_defs[key]}
            if old_defs.keys() != new_defs.keys() or changed != allowed:
                raise ValueError(f"Operational-only AST change guard: {changed}, expected {allowed}")
        else:
            allowed = set()
            changed = set()
        ast.parse(text)
        compile(text, str(LOCAL / name), "exec")
        write(LOCAL / name, text)
        if name == "taylor_f44_stage_k_source.py":
            # Preserve the entire held realization byte-for-byte, including newline convention.
            (LOCAL / name).write_bytes(path.read_bytes())
        reports[name] = {
            "base_SHA256": old_pins[name], "scoped_SHA256": digest(LOCAL / name),
            "retained_definition_count": len(definitions(old)) - len(changed),
            "changed_definitions": sorted(changed),
            "all_arithmetic_replay_structure_and_resource_definitions_AST_identical": True,
        }

    method = (ORIGINAL / original_files[4]).read_text(encoding="utf-8")
    method = method.replace('`A14_taylor_f44_stage_K_run001`', f'`{PREFIX}_producer_run001`')
    method = method.replace('.context/A14_TAYLOR_F44_STAGE_K_ROOT_READY_run001.json',
        'research/limitation_program_20261001/continuation_20261004/A14/PRODUCER_ROOT_READY_run001.json')
    method = method.replace('research.limitation_program_20261001.experiment_taylor_f44_stage_k',
        MODULE + '.experiment_taylor_f44_stage_k')
    method += """

## Scoped continuation release, 4 October 2026

All new sources and ROOT releases are in
`research/limitation_program_20261001/continuation_20261004/A14/`; all handoffs are
in the matching docs namespace. Old author files, completed receipts, maps and
expected SHA values are read-only. The builder is an exact held-byte copy.
The controller changes only routing, namespace import admission and the owned
file-count guard to reserve one file for the self-excluded manifest. The saved
AST comparison binds all arithmetic, structural, fixed-corpus, phase and resource
functions without change. READY is `PRODUCER_ROOT_READY_run001.json` in the
scoped research directory; the original .context READY is neither created nor used.

The exact CLI is pinned Python with `-B -m
research.limitation_program_20261001.continuation_20261004.A14.experiment_taylor_f44_stage_k
--ready-sha256 ROOT_ISSUED_EXPECTED_SHA256`. ROOT reviews and freezes the actual
four scoped author/method files before issuance. The corpus stays exactly
16 multiplier,40 signed-rounder,32 actual Boolean-prefix diagnostics (88 total).
Acceptance is complete actual-array structure, whole-wire forward/inverse replay,
native absolute phase proof and paid primitive resources within180CPU/150admission/
600wall,1000000rows,64owned files/128MiB, including full prior input maps/current
runtime/two fresh uncached unions. Failure is retained as failure; no retry, new
variant, budget increase or partial-credit promotion. Launch stdout/stderr is
retained outside the scientifically owned receipt in this research namespace.

The independently authored checker has separate source and release. Its actual
sealed PASS plus separate ROOT fresh integrity remain required before any Stage C
release. Stage C is false in every Stage K artifact. All448 F44 literals, cosine
uniform envelope, eager caller ranges, total-map gates, source binding, complete
costs, financialG2, estimator99percent delivery and physical advantage remain open.
"""
    write(LOCAL / original_files[4], method)
    policy = json.loads((ORIGINAL / original_files[3]).read_text(encoding="utf-8"))
    policy["status"] = "SCOPED_AUTHOR_FROZEN_PENDING_PARENT_ROOT_STATIC_REVIEW"
    policy["author_SHA256"] = {name: digest(LOCAL / name) for name in original_files[:2]}
    policy["method_document_SHA256"] = digest(LOCAL / original_files[4])
    policy["fresh_receipt"] = f"results/limitation_program_20261001/{PREFIX}_producer_run001"
    policy["external_ROOT_READY"] = (LOCAL / "PRODUCER_ROOT_READY_run001.json").relative_to(ROOT).as_posix()
    policy["CLI"][3] = MODULE + ".experiment_taylor_f44_stage_k"
    policy["future_independent_checker_source_SHA256"] = digest(LOCAL / "audit_taylor_f44_stage_k.py")
    policy["old_author_and_receipts_read_only"] = True
    save(LOCAL / original_files[3], policy)
    producer_pins = {name: digest(LOCAL / name) for name in (*original_files[:2], original_files[3], original_files[4])}
    auditor_doc = """# Independent F44 Stage K checker, scoped continuation

Author-only, frozen pending parent ROOT review and actual producer PASS. No
builder/producer imports. The checker consumes actual raw binary rows with its
own dense allocator/structural recurrence and integer-mask whole-state interpreter.
It independently applies the same fixed16+40+32 corpus, all56 leaf cases in both
directions plus forward/literal reverse and all32 emitted-prefix reversals.
It checks every allocated wire, full52x38 signed product116/f44 copy window and
negative Euclidean ties-even rounding, then recounts every native row and actual
7T macro chronology. Absolute phase is checked on all8 exact cyclotomic operator
columns using rational coordinates in Q[zeta]/(zeta^4+1), including global phase1.
Those8 matrix columns are phase-proof checks, not additional credited fixtures.

Assumptions: inputs obey the ordered signed52/signed38 sign-extension contract;
rounding accepts every signed72 word; private banks enter zero; dirty outputs
are arbitrary72 words; X/CX and the independently matrix-checked macro implement
absolute gates. No universal full72 multiplication claim or reduced-width proxy.

Acceptance: actual producer sealed PASS, no failure marker, actual source clocks
under180CPU/150admission/600creation-wall, all complete source/prior manifests and
inventories, current pinned runtime, exactly two fresh uncached input unions,
complete binary-size/SHA/row/port/structural proof, all88 diagnostics and costs
matching the producer. Same caps64owned files/128MiB,1000000total native rows,
24000runtime files/2GiB and100000references/8GiB unique input/24GiB hash work.
One fresh audit output: A14_continuation_20261004_stage_k_audit_run001. The exact
CLI is pinned Python -B -m
research.limitation_program_20261001.continuation_20261004.A14.audit_taylor_f44_stage_k
--ready-sha256 ROOT_ISSUED_EXPECTED_SHA256 --source-manifest-sha256 ACTUAL_PASSED_SOURCE_SHA256.
Parent ROOT issues AUDIT_ROOT_READY_run001.json only after actual source PASS,
freezing actual source manifest/counts, producer ROOT release and all four
producer/three auditor files. No observed input replaces an expected old SHA.
Failure is authoritative, retained and invalidates all partial reports; no retry,
budget extension, repair or partial-credit promotion. Exact launch logs stay
outside the scientifically owned receipt in this scoped research namespace.

This author-only release retains all independent checker mathematical functions
AST-identical to its held draft; only namespace/routing admission changes.
There is no cosine coefficient creation, candidate approval, financial certificate,
source adoption, Stage C release, timing measurement or quantum advantage.
Fixture, price-sample and credited replay increments are zero. A separate ROOT
fresh integrity audit remains required; broad A14 remains partial.
"""
    audit_doc_name = "A14_TAYLOR_F44_STAGE_K_AUDIT_PREFLIGHT.md"
    write(LOCAL / audit_doc_name, auditor_doc)
    audit_policy = {
        "schema": "a14-taylor-f44-stage-k-audit-preflight-v1",
        "status": "AUTHOR_FROZEN_PENDING_PARENT_ROOT_REVIEW_AND_ACTUAL_SOURCE_PASS",
        "author_SHA256": {"audit_taylor_f44_stage_k.py": digest(LOCAL / "audit_taylor_f44_stage_k.py")},
        "method_document_SHA256": digest(LOCAL / audit_doc_name),
        "producer_author_method_SHA256": producer_pins,
        "limits_CPU_admission_wall": [180,150,600],
        "owned_caps_files_bytes": [64,134217728],
        "fixed_diagnostic_counts": [16,40,32,88],
        "fresh_receipt": f"results/limitation_program_20261001/{PREFIX}_audit_run001",
        "ROOT_READY_path": (LOCAL / "AUDIT_ROOT_READY_run001.json").relative_to(ROOT).as_posix(),
        "Stage_C_release_authorized": False, "full_G2": False, "adoption": False,
        "new_test_credit": 0, "quantum_advantage": False,
    }
    save(LOCAL / "a14_taylor_f44_stage_k_audit_preflight.json", audit_policy)
    freeze = {
        "schema": "a14-continuation-scoped-stage-k-authoring-freeze-v1",
        "created_UTC": datetime.now(timezone.utc).isoformat(),
        "original_selected_SHA256": old_pins, "definition_comparisons": reports,
        "producer_author_method_SHA256": producer_pins,
        "audit_author_method_SHA256": {name: digest(LOCAL / name) for name in (
            "audit_taylor_f44_stage_k.py", "a14_taylor_f44_stage_k_audit_preflight.json", audit_doc_name)},
        "ROOT_READY": False, "scientific_execution": False, "gate_generation": False,
        "diagnostics": [16,40,32,88], "new_test_credit": 0,
    }
    if any(digest(ORIGINAL / name) != value for name, value in old_pins.items()):
        raise ValueError("Original author bytes changed during scoped authoring")
    save(LOCAL / "authoring_freeze.json", freeze)
    write(DOCS / "STATUS.md", """# A14 continuation, 4 October 2026

Scoped Stage K producer and independent checker authored and AST-checked.
All held builder bytes and arithmetic/structural/replay/resource definitions
remain unchanged. The producer cap now reserves the manifest file; routes and
parent namespace admission use only the assigned continuation namespaces.

Corpus16+40+32=88, assumptions, acceptance, fixed180CPU/150admission/600wall and
failure stopping rule are frozen in the implementation/audit preflights before
any scientific execution. Parent ROOT static review/releases are pending.
No gate generation, diagnostic execution, coefficients or scientific acceptance
yet. Previous CORDIC/F40 Taylor rejections and failures remain immutable.

Broad A14 remains partial. Remaining: actual Stage K producer, separate binary
checker, ROOT fresh integrity; then separately authorized448F44 literals/cosine
screen with whole-input eager promises, total-map gates, exact source binding,
paid source/inverse/capped schedule and financialG2. Stage C/candidate selection/
source adoption/quantum advantage are false; zero new fixture/replay credit.
""")
    print(json.dumps(freeze, sort_keys=True))


if __name__ == "__main__":
    main()
