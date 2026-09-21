import numpy as np
import pytest

from research.journal_sprint.pricing_bounds import bounds_for
from research.paper_a.benchmark import C6, by_id
from research.paper_a.payoff import a_calc, to_price
from research.paper_a.references import (
    black_scholes_call,
    grid_points,
    grid_probabilities,
    p_grid,
    support_audit,
)


@pytest.mark.parametrize("cid", C6)
def test_deterministic_ladder_and_affine_map(cid):
    c = by_id(cid)
    support = support_audit(c, 1e-5)
    bs = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
    for n in (3, 4, 5, 6):
        for scale in (0.125, 0.25, 0.5):
            b = bounds_for(c, n, scale)
            grid = p_grid(c, b.lower, b.upper, n)
            x = grid_points(b.lower, b.upper, n)
            weights = grid_probabilities(c, b.lower, b.upper, n)
            a = a_calc(weights, x, c.K, b.upper, scale)
            encoded = to_price(a, c.K, b.upper, scale, c.r, c.T)
            assert abs(support.P_support - bs) <= b.support + 1e-9
            assert abs(grid - support.P_support) <= b.grid + 1e-9
            assert abs(encoded - grid) <= b.encoding + 1e-9
            assert abs(encoded - bs) <= b.total + 1e-9
            for probability in (0.0, a, 0.5, 1.0):
                assert b.offset + b.sensitivity * probability == pytest.approx(
                    to_price(probability, c.K, b.upper, scale, c.r, c.T), abs=1e-10
                )


@pytest.mark.parametrize("cid", C6)
def test_actual_ideal_pricing_state(cid):
    from research.paper_a.european.circuits import build_european, statevector_amplitude

    c = by_id(cid)
    b = bounds_for(c, 3, 0.25)
    circuit = build_european(c, b.lower, b.upper, 3, 0.25)
    a = a_calc(
        grid_probabilities(c, b.lower, b.upper, 3),
        grid_points(b.lower, b.upper, 3),
        c.K,
        b.upper,
        0.25,
    )
    assert statevector_amplitude(circuit) == pytest.approx(a, abs=1e-10)


def test_budget_and_invalid_parameters():
    c = by_id(C6[0])
    b = bounds_for(c, 3, 0.25)
    assert b.probability_budget(b.total / 2) == 0
    assert b.probability_budget(b.total + 1) == pytest.approx(1 / b.sensitivity)
    for n, scale in ((0, 0.25), (3.5, 0.25), (True, 0.25), (3, 0), (3, np.nan)):
        with pytest.raises(ValueError):
            bounds_for(c, n, scale)


def test_runner_serializes_numpy_diagnostics(tmp_path, monkeypatch):
    import json
    from research.journal_sprint import run_pricing_gate

    output = tmp_path / "pricing_gate"
    monkeypatch.setattr(run_pricing_gate, "C6", (C6[0],))
    monkeypatch.setattr("sys.argv", ["run_pricing_gate", "--output", str(output)])
    run_pricing_gate.main()
    rows = json.loads((output / "rows.json").read_text())
    assert len(rows) == 12
    assert all(row["bound_checks_pass"] is True for row in rows)
    assert (output / "complete.json").exists()
