"""Snapshot the scoped final handoff without modifying completed experiments."""

from .checks import archive_path

from .checks import require

import argparse
import json
import re
import shutil
import xml.etree.ElementTree as ET

from .storage import ROOT, finish_run, sha256, start_run, write_json


def checked_test_report(source):
    suites = list(ET.parse(source).getroot().iter("testsuite"))
    require(bool(suites), "test report contains no suites")
    totals = {
        key: sum(int(s.attrib[key]) for s in suites) for key in ("tests", "errors", "failures")
    }
    require(
        totals["tests"] > 0 and totals["errors"] == totals["failures"] == 0,
        "test report has failures, errors or no tests",
    )
    return {key: str(value) for key, value in totals.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/journal_sprint/week12_handoff_v1")
    args = parser.parse_args()
    path = start_run(args.output, {"purpose": "final scoped source/docs/test snapshot"})
    documents = list((ROOT / "docs/journal_sprint").glob("*.md"))
    documents += list((ROOT / "docs").glob("JOURNAL_REENGINEERING*.md"))
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    files = documents + sources + [ROOT / "README.md", ROOT / "pyproject.toml"]
    tests = {}
    for name in ("tests_week12_closeout.xml", "tests_closeout_sprint.xml"):
        source = ROOT / "results/journal_sprint" / name
        tests[name] = checked_test_report(source)
        files.append(source)
    links = []
    for document in documents:
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            destination = document.parent / target.split("#")[0]
            require(destination.exists(), (document, target))
            links.append({"document": str(document.relative_to(ROOT)), "target": target})
    for source in files:
        destination = path / "snapshot" / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    provenance = {}
    for name in ("week12_closeout_v1", "price_intervals_v2c", "pricing_gate_v2b"):
        folder = ROOT / "results/journal_sprint" / name
        manifest = folder / "complete.json"
        content = json.loads(manifest.read_text())
        require(
            all(
                sha256(archive_path(folder, file)) == value
                for file, value in content["sha256"].items()
            )
        )
        provenance[name] = sha256(manifest)
    write_json(
        path / "index.json",
        {
            "files_copied": len(files),
            "local_links_checked": len(links),
            "tests": tests,
            "linked_run_manifests": provenance,
            "scientific_status": "technical feasibility complete; human agreement outstanding",
            "note": (
                "Supplementary snapshot, not a standalone runnable repository. "
                "Links are checked against the originating workspace, not the snapshot. "
                "No claim of independent human review, hardware validation or journal readiness"
            ),
        },
    )
    finish_run(path)
    print(f"Handoff archived: {path}; {len(files)} files, {len(links)} local links checked")


if __name__ == "__main__":
    main()
