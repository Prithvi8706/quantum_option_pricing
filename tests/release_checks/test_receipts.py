import pytest
from research.release_checks.receipts import junit


def test_case_counts_must_match_summary(tmp_path):
    p = tmp_path / "tests.xml"
    p.write_text('<testsuite tests="1"><testcase name="a"/></testsuite>', encoding="utf-8")
    assert junit(p)["suites"][0]["passed"] == 1
    assert junit(p)["independent_test_count"] is None
    p.write_text('<testsuite tests="2"><testcase name="a"/></testsuite>', encoding="utf-8")
    with pytest.raises(ValueError, match="counters"):
        junit(p)


def test_skipped_is_not_passed(tmp_path):
    p = tmp_path / "tests.xml"
    p.write_text(
        '<testsuite tests="1" skipped="1"><testcase><skipped/></testcase></testsuite>',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="skipped"):
        junit(p)
