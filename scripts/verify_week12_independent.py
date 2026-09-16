"""Independent stdlib-only audit; run with the extracted week-12 archive path."""

import collections
import json
import math
from pathlib import Path
import statistics
import sys

root = Path(sys.argv[1])
rows = [json.loads(p.read_text())["result"] for p in sorted(root.glob("row_*.json"))]
stage = json.loads((root / "summary.json").read_text())["stage"]
expected = 90 if stage == "pilot" else 7400
assert len(rows) == expected
groups = collections.defaultdict(list)
for row in rows:
    s = row["spec"]
    groups[(s["phase"], s["contract"], s["scenario"], s["guard"], s["arm"])].append(row)
    assert row["total_shots"] == sum(row[k] for k in ("pilot_shots", "m0", "m1", "n"))
    assert row["total_shots"] <= 65536
    delivered = row["status"] == "precision_met"
    assert row["penalized_cost"] == (row["total_shots"] if delivered else 65536)
    if row["interval"] is not None:
        lo, hi = row["interval"]
        assert math.isclose(row["radius"], (hi - lo) / 2, rel_tol=1e-12, abs_tol=1e-12)
    if delivered:
        assert row["radius"] <= 1.0
    if s["arm"] in ("fixed_cp", "fixed_target"):
        assert row["pilot_shots"] == 0 and row["pilot_successes"] is None
analysis = json.loads((root / "analysis.json").read_text())
assert len(groups) == len(analysis["cells"]) == (30 if stage == "pilot" else 185)
for c in analysis["cells"]:
    key = tuple(c[k] for k in ("phase", "contract", "scenario", "guard", "arm"))
    group = groups[key]
    n = len(group)
    assert n == (3 if stage == "pilot" else 400 if key[0] == "primary" else 30)
    assert c["observations"] == n
    deliveries = sum(r["status"] == "precision_met" for r in group)
    assert c["delivery"]["count"] == deliveries
    assert c["delivery"]["fraction"] == deliveries / n
    assert c["actual_cost"]["mean"] == statistics.mean(r["total_shots"] for r in group)
    assert c["penalized_cost"]["mean"] == statistics.mean(r["penalized_cost"] for r in group)
    assert c["erroneous"]["count"] == sum(r["erroneous"] for r in group)
    assert c["erroneous_among_declarations"]["denominator"] == deliveries
    assert c["misses_among_intervals"]["denominator"] == sum(
        r["interval"] is not None for r in group
    )
counts = collections.Counter(r["spec"]["phase"] for r in rows)
if stage == "main":
    assert counts == {"primary": 2000, "secondary": 5400}
    primary = {c["arm"]: c for c in analysis["cells"] if c["phase"] == "primary"}
    target = primary["unequal_target"]
    checks = []
    for arm in ("fixed_cp", "fixed_target"):
        base = primary[arm]
        tg = groups[("primary", "E001", "design_match", 0.0, "unequal_target")]
        bg = groups[("primary", "E001", "design_match", 0.0, arm)]
        checks.append(
            20 * sum(r["penalized_cost"] for r in tg) <= 17 * sum(r["penalized_cost"] for r in bg)
            and target["delivery"]["count"] - base["delivery"]["count"] >= -8
        )
    assert analysis["primary_interest"]["passed"] == (
        target["delivery"]["count"] >= 380 and all(checks)
    )
events = [json.loads(s) for s in (root / "events.jsonl").read_text().splitlines()]
completed = [e for e in events if e["event"] == "draw_completed"]
assert sum(e["shots"] for e in completed) == sum(r["total_shots"] for r in rows)
assert sum(e["logical_cx"] for e in completed) == sum(r["total_cx"] for r in rows)
assert sum(e["event"] == "started" for e in events) == len(rows)
assert sum(e["event"] == "completed" for e in events) == len(rows)
print(
    json.dumps(
        dict(
            verified=True,
            rows=len(rows),
            cells=len(groups),
            phases=dict(counts),
            total_shots=sum(r["total_shots"] for r in rows),
            total_logical_cx=sum(r["total_cx"] for r in rows),
            scope="independent arithmetic/event audit, not new observations",
        ),
        indent=2,
    )
)
