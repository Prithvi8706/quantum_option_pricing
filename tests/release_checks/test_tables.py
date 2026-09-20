import csv
import io
from research.release_checks.tables import render
from .test_targets import evidence


def test_export_keeps_failures_and_exact_integer_costs():
    data = evidence()
    text = render(data)
    assert text == render(data)
    rows = list(csv.DictReader(io.StringIO(text)))
    assert len(rows) == 12
    assert sum(r["status"] == "ideal_plan" for r in rows) == 8
    assert rows[0]["projected_CX"] == ""
    assert rows[2]["projected_CX"] == "354203646982"
    assert all("not runtime" in r["scope"] for r in rows)
