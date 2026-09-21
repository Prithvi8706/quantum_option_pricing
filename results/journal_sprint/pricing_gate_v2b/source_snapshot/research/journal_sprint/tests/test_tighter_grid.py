import math

import numpy as np
import pytest

from research.journal_sprint.tighter_grid import (
    density_derivative,
    derivative_suprema,
    tighter_bounds_for,
)
from research.paper_a.benchmark import C6, by_id
from research.paper_a.references import p_grid, support_audit


@pytest.mark.parametrize("cid", C6)
def test_tighter_bound_encloses_grid_error(cid):
    c = by_id(cid)
    support = support_audit(c, 1e-5)
    for n in (3, 4, 5, 6):
        b, details = tighter_bounds_for(c, n, 0.125)
        actual = abs(p_grid(c, b.lower, b.upper, n) - support.P_support)
        assert actual <= b.grid + 1e-9
        assert b.grid <= details["old_grid_bound"] + 1e-12
        assert details["derivative_remainder"] >= 0
        mu = math.log(c.S0) + (c.r - c.sigma**2 / 2) * c.T
        s = c.sigma * math.sqrt(c.T)
        edges = np.linspace(b.lower, b.upper, 65)
        envelope = derivative_suprema(edges[:-1], edges[1:], mu, s)
        points = np.linspace(edges[:-1], edges[1:], 101)
        assert np.all(abs(density_derivative(points, mu, s)) <= envelope + 1e-12)


def test_runner_uses_new_bound_and_serializes(tmp_path, monkeypatch):
    import json
    from research.journal_sprint import run_tighter_gate

    monkeypatch.setattr(run_tighter_gate, "C6", (C6[0],))
    output = tmp_path / "run"
    monkeypatch.setattr("sys.argv", ["run_tighter_gate", "--output", str(output)])
    run_tighter_gate.main()
    rows = json.loads((output / "rows.json").read_text())
    assert len(rows) == 12
    assert all(row["checks_pass"] for row in rows)
    assert (output / "complete.json").exists()
