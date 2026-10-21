"""Assemble and validate the local plan without running scientific experiments."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs/limitation_audit_20261001"
PLAN = DOCS / "implementation_plan"
SOURCE = ROOT / "manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md"
PARTS = ("arithmetic", "estimation", "formulations", "hardware", "contract")
COUNTS = {"A": 20, "E": 25, "F": 32, "H": 18, "C": 15}
GATES = {
    "G0": "Fixed task and provenance",
    "G1": "Exact arithmetic and source validity",
    "G2": "Complete financial dollar-error certificate",
    "G3": "Explicit estimator and 99% confidence schedule",
    "G4": "Matched timed classical comparator",
    "G5": "Compatible physical cost and full tenfold inequality",
}
DRAFT_REFRESH = False
REQUIRED = {
    "id",
    "title",
    "status",
    "source_sections",
    "existing_evidence",
    "depends_on",
    "next_action",
    "alternatives",
    "acceptance",
    "stop_rule",
    "on_pass",
    "on_fail",
    "artifacts",
    "priority",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path, text):
    mode = "x"
    if DRAFT_REFRESH:
        assert path.parent == PLAN
        assert path.name in (
            "roadmap.json",
            "COVERAGE.md",
            "CHECKLIST.md",
            "VALIDATION.json",
            "manifest.json",
        )
        mode = "w"
    with path.open(mode, encoding="utf-8") as stream:
        stream.write(text)


def json_new(path, data):
    write_new(path, json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def load_entries():
    result = []
    for part in PARTS:
        raw = read(PLAN / (part + ".json"))
        result.extend(raw if isinstance(raw, list) else raw["entries"])
    expected = {f"{letter}{i:02d}" for letter, count in COUNTS.items() for i in range(1, count + 1)}
    assert len(result) == len(expected) == 110
    assert {e["id"] for e in result} == expected
    assert len({e["id"] for e in result}) == len(result)
    for entry in result:
        assert REQUIRED <= entry.keys(), entry["id"]
        assert entry["status"] in ("complete", "partial", "ready", "conditional", "audit")
        assert type(entry["priority"]) is int and 1 <= entry["priority"] <= 5
        for field in ("title", "next_action", "stop_rule", "on_pass", "on_fail"):
            assert isinstance(entry[field], str) and entry[field].strip()
        for field in (
            "source_sections",
            "existing_evidence",
            "alternatives",
            "acceptance",
            "artifacts",
        ):
            assert isinstance(entry[field], list) and entry[field]
            assert all(isinstance(v, str) and v.strip() for v in entry[field])
        assert isinstance(entry["depends_on"], list)
        assert set(entry["depends_on"]) <= expected | GATES.keys(), entry["id"]
        assert entry["id"] not in entry["depends_on"]
        for path in entry["existing_evidence"]:
            assert (ROOT / path).exists(), (entry["id"], path)
        assert all(p.startswith("results/limitation_program_20261001/") for p in entry["artifacts"])
    return result


def dependencies_cycle(entries):
    graph = {e["id"]: [d for d in e["depends_on"] if not d.startswith("G")] for e in entries}
    visited, active = set(), []

    def visit(node):
        if node in active:
            raise AssertionError(
                "Split this prerequisite cycle into interface handoffs: "
                + " -> ".join(active + [node])
            )
        if node in visited:
            return
        active.append(node)
        for other in graph[node]:
            visit(other)
        active.pop()
        visited.add(node)

    for node in graph:
        visit(node)


def original_units():
    units, lines, start, context, kind = [], [], 0, [], "paragraph"

    def flush():
        if lines:
            units.append(
                dict(
                    start_line=start,
                    end_line=start + len(lines) - 1,
                    context=" / ".join(context),
                    kind=kind,
                    text=" ".join(s.strip() for s in lines),
                )
            )
            lines.clear()

    for number, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), 1):
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush()
            level, title = len(heading[1]), heading[2]
            context = context[: level - 1] + [title]
            units.append(
                dict(
                    start_line=number,
                    end_line=number,
                    context=" / ".join(context),
                    kind="heading",
                    text=title,
                )
            )
        elif not line.strip() or re.fullmatch(r"\s*-{3,}\s*", line):
            flush()
        elif line.startswith("|"):
            flush()
            if not re.fullmatch(r"[| :\-]+", line):
                units.append(
                    dict(
                        start_line=number,
                        end_line=number,
                        context=" / ".join(context),
                        kind="table row",
                        text=line,
                    )
                )
        elif re.match(r"^(?:[-*]\s|\d+\.\s)", line):
            flush()
            start, kind = number, "bullet"
            lines.append(line)
        else:
            if not lines:
                start, kind = number, "paragraph"
            lines.append(line)
    flush()
    return units


def map_unit(unit):
    c, t = unit["context"], unit["text"].lower()
    if "10. Primary references" in c:
        return ["C15"]
    if "9. Evidence map" in c:
        return ["C12", "C15"]
    if "8. What this project" in c:
        return ["C04", "C08", "C12", "C13", "C15"]
    if "Failure 1:" in c:
        if "coupling" in t:
            return ["F10", "F20"]
        if "base level" in t or "74%" in t:
            return ["F11", "F20"]
        if "feller" in t or "variance rate" in t:
            return ["F12", "F13", "F15"]
        return ["A11", "A12", "E02", "F10", "F14", "F15", "H17"]
    if "Failure 2:" in c:
        if "removed the nesting" in t or "bracket" in t:
            return ["F16", "F17"]
        return ["E14", "E15", "F16", "F18", "F19", "C11"]
    if "Failure 3:" in c:
        if "certif" in t:
            return ["E09", "E10", "E11", "E12", "C03"]
        return ["E03", "F08", "F20", "A13", "C13"]
    if "Failure 4:" in c:
        return ["A01", "A02", "A06", "A09", "A13", "A16", "E02", "E07", "C11"]
    if "Failure 5:" in c:
        if "magic-state" in t or "factories" in t:
            return ["H05", "H06", "H18"]
        if "memory" in t or "qubit" in t:
            return ["A18", "A19", "H09", "H15"]
        return ["A06", "A07", "A09", "A18", "E08", "H17", "C13"]
    if "Failure 6:" in c:
        if "fixed-point" in t or "misclass" in t:
            return ["C06", "C07"]
        if "corners" in t or "variance the plain" in t:
            return ["E02", "E03", "F02", "C04", "C13", "C14"]
        if "strict" in t or "extrapolat" in t or "orders of magnitude" in t:
            return ["F01", "F31", "C02", "C08", "C14"]
        return ["A01", "A02", "A13", "F01", "F06", "F07", "C08", "C09", "C11", "H17"]
    if "Root cause A:" in c:
        if "nested" in t or "compound" in t:
            return ["E14", "E15", "F16", "F18", "F19"]
        if "heavy-tailed" in t:
            return ["E16", "E17", "F08", "F09"]
        if "quantum-walk" in t:
            return ["F32"]
        if "discontinuous" in t:
            return ["F01", "F03", "F06", "F07", "C08"]
        return ["E01", "F03", "F04", "F31", "C14"]
    if "Root cause B:" in c:
        if "qldpc" in t or "bivariate" in t:
            return ["H09", "H10", "H11", "H12", "C15"]
        if "decod" in t or "feedback" in t:
            return ["H01", "H02", "H03", "H04", "H18"]
        if "non-clifford" in t or "transversal" in t or "cultivation" in t:
            return ["H04", "H05", "H06", "H07", "H08", "H11"]
        return ["H01", "H03", "H12", "H13", "H14", "H17", "H18", "C15"]
    if "Root cause C:" in c:
        if "signal processing" in t or "arithmetic-free" in t:
            return ["A20", "E22", "E23", "C13"]
        return ["A06", "A07", "A08", "A09", "A10", "A13", "A14", "A16", "A18", "C13"]
    if "Root cause D:" in c:
        return ["F01", "F06", "F07", "F16", "F20", "F24", "F30", "C10", "C14"]
    if "Root cause E:" in c:
        return ["A18", "E20", "E21", "H15", "H16", "H17"]
    if "Root cause F:" in c:
        return ["E07", "E08", "E09", "E10", "E12", "E21", "E25", "C03", "C09", "H18"]
    if "6. Ideas not yet" in c:
        rows = [
            ("more assets", ["A05", "F23"]),
            ("discontinuous", ["F06", "F07", "C07"]),
            ("stochastic or rough", ["F12", "F14", "F15", "F21", "F22", "F26"]),
            ("better compilation", ["A06", "A09", "A18", "C13"]),
            ("variance reduction", ["E03", "E09", "F20"]),
            ("many strikes", ["E18", "E19", "F27", "F28", "F29"]),
            ("pde", ["F24", "F25", "F26"]),
            ("quasi-monte", ["F05"]),
            ("hardware", ["H01", "H05", "H09", "H17", "C15"]),
        ]
        return next((ids for key, ids in rows if key in t), ["C10", "C13", "C15"])
    if "7. The requirements" in c:
        if "classical cost" in t or "cubic" in t:
            return ["F31", "C14", "C15"]
        if "estimator constant" in t:
            return ["E02", "E07", "E08", "E24", "E25"]
        if "accuracy of" in t:
            return ["C02", "C08", "C14"]
        if "logical t-layer" in t:
            return ["H01", "H03", "H17", "H18"]
        if "oracle depth" in t:
            return ["A01", "A09", "A13", "A18", "C13"]
        return ["E02", "H17", "C04", "C11", "C14", "C15"]
    if "2.1 What the quantum" in c:
        return ["E01", "E02", "E03", "E07", "E09", "F02", "C05"]
    if "2.2 What each quantum" in c:
        return ["E02", "F02", "H17", "C04", "C14"]
    if "2.3 Against strong" in c:
        return ["F01", "F02", "F03", "F06", "C08", "C10"]
    if "2.4 The same law" in c:
        return ["E02", "H03", "H17", "C04", "C14"]
    if "2.5 Historical" in c:
        return ["E02", "F02", "H17", "C04", "C09", "C15"]
    if "3. Anatomy" in c:
        if "prepare randomness" in t:
            return ["A01", "A02", "A03", "A04", "A05"]
        if "perform coherent arithmetic" in t:
            return ["A06", "A07", "A08", "A09", "A10"]
        if "transcendental" in t or "exponential" in t:
            return ["A13", "A14"]
        if "uncompute everything" in t:
            return ["A16", "A18", "A19", "E06"]
        if "controllable" in t:
            return ["A17", "E05"]
        if "square root" in t:
            return ["A11"]
        if "divide" in t:
            return ["A12"]
        if "multiply" in t:
            return ["A09", "A10"]
        if "add / subtract" in t:
            return ["A08"]
        if "|" in t or "logical operation" in t or "classical counterpart" in t or "3.7 days" in t:
            return ["H01", "H02", "H03", "H05", "H06", "H16", "H17", "C15"]
        return ["A01", "A09", "A13", "A18", "H17", "C11", "C13"]
    if "1. The question" in c:
        if "confidence" in t or "99%" in t:
            return ["C01", "C02", "C03", "E07", "E21"]
        if "classical comparator" in t or any(
            s in t
            for s in (
                "control variates",
                "conditioning",
                "multilevel",
                "multicore",
                "randomized quasi",
            )
        ):
            return ["F01", "F06", "F10", "F20", "H16", "C10"]
        return ["C01", "C02", "C04", "C11", "C15"]
    return ["C11", "C12", "C15"]


def coverage(entries):
    ids = {e["id"] for e in entries}
    units = original_units()
    covered_lines = set()
    for unit in units:
        unit["entries"] = map_unit(unit)
        assert unit["entries"] and set(unit["entries"]) <= ids
        covered_lines.update(range(unit["start_line"], unit["end_line"] + 1))
    substantive_lines = {
        i
        for i, line in enumerate(SOURCE.read_text(encoding="utf-8").splitlines(), 1)
        if line.strip()
        and not re.fullmatch(r"\s*-{3,}\s*", line)
        and not re.fullmatch(r"[| :\-]+", line)
    }
    assert substantive_lines <= covered_lines, sorted(substantive_lines - covered_lines)
    return units


def check_links():
    files = [DOCS / "IMPLEMENTATION_PLAN.md"] + list(PLAN.glob("*.md"))
    checked = 0
    for file in files:
        for dest in re.findall(r"\]\(([^)]+)\)", file.read_text(encoding="utf-8")):
            if re.match(r"(?:https?://|#|app:)", dest):
                continue
            path = dest.split("#", 1)[0]
            assert (file.parent / path).exists(), (file.name, path)
            checked += 1
    return checked


def run(check_only=False):
    entries = load_entries()
    dependencies_cycle(entries)
    units = coverage(entries)
    if check_only:
        roadmap = read(PLAN / "roadmap.json")
        assert roadmap["entries"] == entries
        assert roadmap["coverage"] == units
        assert roadmap["source_sha256"] == sha(SOURCE)
        for path, expected in read(PLAN / "manifest.json")["files"].items():
            assert sha(ROOT / path) == expected, path
        print(
            "Verified 110 work items,",
            len(units),
            "original source units and",
            check_links(),
            "local links",
        )
        return
    json_new(
        PLAN / "roadmap.json",
        dict(
            schema="local-limitation-implementation-plan-v1",
            created_utc=datetime.now(timezone.utc).isoformat(),
            source=str(SOURCE.relative_to(ROOT)),
            source_sha256=sha(SOURCE),
            gates=GATES,
            dependency_semantics="An entry dependency is a required input interface, "
            "not completion of every branch of that investigation.",
            execution_policy="Local experiments only. Follow the master plan and per-entry "
            "decision rules; no pushes, uploads, publication or cloud hardware.",
            execution_status="Plan authored; future task execution is recorded separately "
            "in progress.json, never inferred from this plan.",
            entries=entries,
            coverage=units,
        ),
    )
    lines = [
        "# Coverage of every point in WHY NO ADVANTAGE",
        "",
        "The source is frozen by SHA-256 `"
        + sha(SOURCE)
        + "`. Every substantive source line belongs to a mapped paragraph, heading, bullet "
        "or table row. Formatting separators are excluded. Context and historical "
        "descriptions are covered too; they are not counted as independent limitations. "
        "The item mapping is an implementation assignment, not a claim that the point "
        "has been solved.",
        "",
        "| Original lines | Source point | Implementation items |",
        "|---|---|---|",
    ]
    for unit in units:
        text = unit["text"].replace("|", "\\|").replace("`", "")
        text = text[:190] + ("…" if len(text) > 190 else "")
        location = f"{unit['start_line']}–{unit['end_line']}"
        link = "../../../manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md"
        lines.append(f"| [{location}]({link}) | {text} | {', '.join(unit['entries'])} |")
    write_new(PLAN / "COVERAGE.md", "\n".join(lines) + "\n")
    lines = [
        "# Execution checklist for the limitation plan",
        "",
        "Checked items below are completed components from existing evidence, not a claim "
        "that all quantum advantage barriers are solved. Other rows are unexecuted planned "
        "scopes. During execution, track individual candidate outcomes and substeps in the "
        "separate program progress.json; a rejected/conditional branch must have a receipt "
        "before it is closed.",
        "",
    ]
    for family in COUNTS:
        lines += ["## " + family + " work items", ""]
        for e in entries:
            if e["id"].startswith(family):
                mark = "x" if e["status"] == "complete" else " "
                lines.append(
                    f"- [{mark}] {e['id']} {e['title']} — {e['status']}; priority {e['priority']}"
                )
        lines.append("")
    write_new(PLAN / "CHECKLIST.md", "\n".join(lines))
    links = check_links()
    json_new(
        PLAN / "VALIDATION.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            work_items=len(entries),
            family_counts=COUNTS,
            status_counts=dict(Counter(e["status"] for e in entries)),
            source_units=len(units),
            all_substantive_source_lines_mapped=True,
            dependencies_valid=True,
            entry_dependency_graph_acyclic=True,
            existing_evidence_paths_valid=True,
            local_links_checked=links,
            scope="Document/schema/provenance checks only; no planned scientific "
            "experiment was executed by this assembler.",
        ),
    )
    paths = [p for p in PLAN.rglob("*") if p.is_file() and p != PLAN / "manifest.json"]
    paths += [DOCS / "IMPLEMENTATION_PLAN.md", DOCS / "README.md", Path(__file__), SOURCE]
    json_new(
        PLAN / "manifest.json",
        dict(
            files={p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(set(paths))},
            note="New planning snapshot. Earlier experiment manifests remain historical; "
            "this snapshot covers the updated audit README.",
        ),
    )
    print("Assembled 110 work items and", len(units), "mapped original source units;")
    print("Validated evidence paths, dependency DAG and", links, "local links.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Read-only validation of the saved snapshot"
    )
    parser.add_argument(
        "--refresh-draft",
        action="store_true",
        help="Regenerate only this draft plan's derived files",
    )
    args = parser.parse_args()
    DRAFT_REFRESH = args.refresh_draft
    run(args.check)
