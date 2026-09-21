"""Snapshot the scoped final handoff without modifying completed experiments."""

import argparse
import json
import re
import shutil
import xml.etree.ElementTree as ET

from .storage import ROOT, finish_run, sha256, start_run, write_json


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
        suite = ET.parse(source).getroot().find("testsuite")
        tests[name] = dict(suite.attrib)
        assert suite.attrib["errors"] == suite.attrib["failures"] == "0"
        files.append(source)
    links = []
    for document in documents:
        for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#"):
                continue
            destination = document.parent / target.split("#")[0]
            assert destination.exists(), (document, target)
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
        assert all(sha256(folder / file) == value for file, value in content["sha256"].items())
        provenance[name] = sha256(manifest)
    write_json(path / "index.json", {
        "files_copied": len(files), "local_links_checked": len(links),
        "tests": tests, "linked_run_manifests": provenance,
        "scientific_status": "technical feasibility complete; human agreement outstanding",
        "note": "No claim of independent human review, hardware validation or journal readiness",
    })
    finish_run(path)
    print(f"Handoff archived: {path}; {len(files)} files, {len(links)} local links checked")


if __name__ == "__main__":
    main()
