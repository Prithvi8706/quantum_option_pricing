import pytest

from research.journal_sprint import run_representation_pilot as runner
from research.journal_sprint.closeout_representation_pilot import analyze, validate_config


def entry(n, eligible=True):
    return dict(
        n=n,
        eligible=eligible,
        bound_total=0.1,
        bounds=dict(sensitivity=1.0, offset=0.0),
        ladder_cx=60,
        profiles={
            str(k): dict(gates=dict(cx=20, u=10), depth=30, total_qubits=n + 1) for k in range(3)
        },
    )


def test_matrix():
    assert len(set(runner.cells())) == 54


@pytest.mark.parametrize("elapsed,size", [(901, 0), (0, 250_000_001)])
def test_execution_limits(elapsed, size):
    with pytest.raises(RuntimeError, match="limit"):
        runner.check_limits(elapsed, size)


def test_execution_limit_boundary():
    runner.check_limits(900, 250_000_000)


def test_selector_ranking_ties_and_empty():
    assert runner.select_candidate([dict(n=5, radius=2), dict(n=6, radius=1)]) == 6
    assert runner.select_candidate([dict(n=6, radius=1), dict(n=5, radius=1)]) == 5
    assert runner.select_candidate([dict(n=6, radius=None), dict(n=5, radius=None)]) == 5


@pytest.mark.parametrize(
    "scores",
    [
        [],
        [dict(n=5, radius=1, exact_price=10)],
        [dict(n=5, radius=-1)],
        [dict(n=5, radius=float("nan"))],
        [dict(n=5, radius=1), dict(n=5, radius=2)],
    ],
)
def test_selector_rejects_bad_or_oracle_input(scores):
    with pytest.raises(ValueError):
        runner.select_candidate(scores)


def test_refusal_and_sole_candidate_bypass():
    menu = {"5": entry(5, False), "6": entry(6)}
    truth = {"6": dict(amplitude=0.2, price=0.2)}
    fixed = runner.trial(("E049", "stationary", "fixed_n5"), 0, menu, {})
    assert fixed["status"] == "pre_refusal" and set(fixed["cost"].values()) == {0}
    selected = runner.trial(("E049", "stationary", "pilot_select"), 0, menu, truth)
    assert selected["selected_n"] == 6 and selected["pilots"] == []
    assert selected["cost"]["calibration_shots"] == 32768


def test_event_before_fresh_batch_and_cost(monkeypatch):
    committed = []
    original = runner.batch
    phases = []

    def wrapped(seed, phase, *args):
        phases.append(phase)
        if phase == "final":
            assert len(committed) == 1 and "final" not in committed[0]
            assert len(committed[0]["pilots"]) == 2
        return original(seed, phase, *args)

    monkeypatch.setattr(runner, "batch", wrapped)
    row = runner.trial(
        ("E001", "stationary", "pilot_select"),
        0,
        {str(n): entry(n) for n in (5, 6)},
        {str(n): dict(amplitude=0.2, price=0.2) for n in (5, 6)},
        committed.append,
    )
    assert phases == ["pilot", "pilot", "final"]
    assert row["cost"]["pricing_logical_cx"] <= runner.CX_CAP
    assert row["cost"]["calibration_shots"] == 49152
    assert row["validation_shots"] == (runner.CX_CAP - 2 * 1024 * 60) // 60
    assert row["cost"]["max_circuit_depth"] == 30


def test_config_mutation():
    config = runner.configuration({}, {})
    validate_config(config, {})
    config["guard"] = 0
    with pytest.raises(ValueError, match="configuration"):
        validate_config(config, {})


def fake_rows():
    return [
        dict(
            contract=cid,
            condition=c,
            policy=p,
            executed=0 if cid in ("E030", "E038") else 100,
            declared=0 if cid in ("E030", "E038") else 95 if p == "pilot_select" else 50,
            false_declarations=0,
            acquisition_totals=dict(total_shots=100),
        )
        for cid, c, p in runner.cells()
    ]


def test_analysis_and_screen():
    rows = fake_rows()
    result = analyze(rows)
    assert len(result["comparisons"]) == 36
    assert len(result["readiness"]["cells"]) == 12
    assert result["readiness"]["passes"]
    assert result["readiness"]["mean_gains"]["fixed_n5"] == pytest.approx(0.45)
    with pytest.raises(ValueError, match="matrix"):
        analyze(rows[:-1])
