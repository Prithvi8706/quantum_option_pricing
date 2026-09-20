"""Read test receipts per suite; overlapping executions are never added."""

from xml.etree import ElementTree as ET


def junit(path):
    payload = path.read_bytes()
    if b"<!DOCTYPE" in payload.upper() or b"<!ENTITY" in payload.upper():
        raise ValueError("XML declarations/entities are not accepted")
    root = ET.fromstring(payload)
    suites = [root] if root.tag == "testsuite" else list(root.findall(".//testsuite"))
    if not suites:
        raise ValueError("missing test suites")
    rows = []
    for suite in suites:
        cases = list(suite.findall("testcase"))
        # Nested aggregate suites would double-count; require leaf suites only.
        if suite.findall("testsuite"):
            raise ValueError("nested aggregate suites unsupported")
        counts = {
            key: int(suite.attrib.get(key, "0"))
            for key in ("tests", "failures", "errors", "skipped")
        }
        actual = {
            key: sum(c.find(tag) is not None for c in cases)
            for key, tag in [("failures", "failure"), ("errors", "error"), ("skipped", "skipped")]
        }
        if counts["tests"] != len(cases) or any(counts[k] != v for k, v in actual.items()):
            raise ValueError("JUnit counters disagree with test cases")
        rows.append(
            {
                "name": suite.attrib.get("name", ""),
                **counts,
                "passed": counts["tests"] - sum(actual.values()),
            }
        )
    if not any(r["tests"] for r in rows) or any(
        r["failures"] or r["errors"] or r["skipped"] for r in rows
    ):
        raise ValueError("empty, failing or skipped test receipt")
    return {"suites": rows, "independent_test_count": None, "scope": "historical execution receipt"}
