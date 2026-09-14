"""Check completed run hashes and preserve the final runnable source package."""

from .checks import require

import json
import shutil
import xml.etree.ElementTree as ET

from .storage import ROOT, finish_run, sha256, start_run, write_json
from .run_comparator import validate_golden


def main():
    base = ROOT / "results/journal_sprint"
    runs = [
        "historical_audit_v1",
        "historical_audit_v2",
        "comparator_v1",
        "prototype_v1",
        "analysis_v1",
    ]
    path = start_run(base / "verification_v1", {"runs": runs})
    verified = {}
    for name in runs:
        manifest = json.loads((base / name / "complete.json").read_text(encoding="utf-8"))
        for relative, expected in manifest["sha256"].items():
            require(sha256(base / name / relative) == expected, (name, relative))
        verified[name] = len(manifest["sha256"])
        if name == "comparator_v1":
            validate_golden(json.loads((base / name / "summary.json").read_text()))
    test_report = base / "tests_final.xml"
    suites = list(ET.parse(test_report).getroot().iter("testsuite"))
    test_summary = {
        key: sum(int(suite.attrib.get(key, 0)) for suite in suites)
        for key in ("tests", "failures", "errors", "skipped")
    }
    require(test_summary["tests"] > 0)
    require(test_summary["failures"] == test_summary["errors"] == 0)
    write_json(
        path / "test_evidence.json",
        {
            "summary": test_summary,
            "sha256": sha256(test_report),
            "path": str(test_report.relative_to(ROOT)),
        },
    )
    shutil.copy2(test_report, path / "tests_final.xml")
    sources = list((ROOT / "research/journal_sprint").rglob("*.py"))
    sources += list((ROOT / "docs/journal_sprint").glob("*.md"))
    sources += [
        ROOT / "pyproject.toml",
        ROOT / "research/journal_sprint/requirements-legacy-circuit.txt",
        ROOT / "research/journal_sprint/vendor/LICENSE-csAE",
        ROOT / "research/journal_sprint/vendor/NOTICE.md",
    ]
    for source in sources:
        destination = path / "source_snapshot" / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    write_json(path / "verified.json", verified)
    finish_run(path)
    print("Verified hashed artifacts:", verified)


if __name__ == "__main__":
    main()
