"""Pre-acquisition schedule, audit, recovery and no-truth boundary tests."""

import json

import pytest

from research.journal_sprint import run_w12 as runner


def profiles():
    return {
        label: dict(
            bounds=dict(sensitivity=scale, offset=0.0, support=0.01, grid=0.01, encoding=0.0),
            amplitude=0.2,
            profiles={"0": {"gates": {"cx": 126}}},
        )
        for label, scale in (("linearized", 10.0), ("exact_table", 2.0))
    }


@pytest.fixture(autouse=True)
def isolated_inputs_and_streams(tmp_path, monkeypatch):
    source = tmp_path / "fixture_profiles"
    source.mkdir()
    for name in runner.C6:
        runner.write_json(source / f"profile_{name}.json", profiles())
    runner.finish_run(source)
    monkeypatch.setattr(runner, "SOURCE", source)
    monkeypatch.setattr(
        runner,
        "NAMESPACES",
        {phase: "TEST_ONLY_week12_" + phase for phase in ("pilot", "primary", "secondary")},
    )


def test_schedule_counts_namespaces_and_order():
    pilot, main = runner.schedule("pilot"), runner.schedule("main")
    assert len(pilot) == 90 and len(main) == 7400
    assert main == runner.schedule("main")
    assert sum(s["phase"] == "primary" for s in main) == 2000
    assert sum(s["phase"] == "secondary" for s in main) == 5400
    for specs in (pilot, main):
        assert len({tuple(sorted(s.items())) for s in specs}) == len(specs)
        for i in range(0, len(specs), 5):
            assert {s["arm"] for s in specs[i : i + 5]} == set(runner.ARMS)


@pytest.mark.parametrize("arm", runner.ARMS)
def test_trial_events_costs_and_determinism(arm):
    spec = dict(runner.schedule("pilot")[0], arm=arm)
    events = []
    a = runner.trial(spec, profiles(), events.append)
    assert a == runner.trial(spec, profiles())
    assert a["total_shots"] == sum(a[k] for k in ("pilot_shots", "m0", "m1", "n"))
    completed = [e for e in events if e["event"] == "draw_completed"]
    assert sum(e["shots"] for e in completed) == a["total_shots"]
    assert sum(e["logical_cx"] for e in completed) == a["total_cx"]
    assert len({e["purpose"] for e in completed}) == len(completed)
    assert a["total_shots"] <= 65536
    first_terminal = next(i for i, e in enumerate(events) if e.get("purpose") == "calibration_0")
    assert next(i for i, e in enumerate(events) if e["event"] == "plan_frozen") < first_terminal
    if arm in ("fixed_cp", "fixed_target"):
        assert all(e.get("purpose") != "pilot" for e in events)


def test_bias_refusal_precedes_any_sampling():
    p = profiles()
    for item in p.values():
        item["bounds"]["grid"] = 2.0
    events = []
    row = runner.trial(runner.schedule("pilot")[0], p, events.append)
    assert row["total_shots"] == 0 and row["penalized_cost"] == 65536
    assert not events and row["plan"] is None


def test_policy_never_receives_truth(monkeypatch):
    original = runner.choose_batch
    seen = []

    def spy(encoding, arm, pilot, guard):
        assert set(encoding.__dataclass_fields__) == {
            "name",
            "sensitivity",
            "offset",
            "bias",
            "cost_per_shot",
        }
        seen.append((encoding, arm, pilot, guard))
        return original(encoding, arm, pilot, guard)

    monkeypatch.setattr(runner, "choose_batch", spy)
    runner.trial(runner.schedule("pilot")[0], profiles())
    assert len(seen) == 1


def configure(monkeypatch):
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        monkeypatch.setenv(key, "1")
    monkeypatch.setattr(runner, "inventory_environment", lambda: {"test_fixture": True})
    tiny = runner.schedule("pilot")[:5]
    monkeypatch.setattr(runner, "schedule", lambda stage: tiny)


def test_tiny_archive_strict_replay_and_exclusive_output(tmp_path, monkeypatch):
    configure(monkeypatch)
    out = tmp_path / "pilot"
    assert runner.run(out, "pilot")["completed"] == 5
    assert runner.verify(out)["rows"] == 5
    with pytest.raises(FileExistsError):
        runner.run(out, "pilot")
    # Delete an event file only in pytest-owned disposable fixture.
    (out / "events.jsonl").unlink()
    with pytest.raises(ValueError, match="inventory"):
        runner.verify(out)


def test_failure_preserves_draw_evidence(tmp_path, monkeypatch):
    configure(monkeypatch)
    spec = dict(runner.schedule("pilot")[0], arm="unequal_target", attempt=0)
    monkeypatch.setattr(runner, "schedule", lambda stage: [spec])

    def failure(spec, profiles, emit):
        emit(dict(event="draw_started", purpose="pilot", shots=1024, logical_cx=126 * 1024))
        raise RuntimeError("injected failure")

    out = tmp_path / "failed"
    with pytest.raises(RuntimeError, match="injected"):
        runner.run(out, "pilot", acquire=failure)
    assert (out / "failure.json").exists() and not (out / "complete.json").exists()
    events = [json.loads(line) for line in (out / "events.jsonl").read_text().splitlines()]
    assert [e["event"] for e in events] == ["started", "draw_started"]


def test_main_requires_pilot_before_output(tmp_path, monkeypatch):
    configure(monkeypatch)
    with pytest.raises(ValueError, match="pilot required"):
        runner.run(tmp_path / "blocked", "main")
    assert not (tmp_path / "blocked").exists()


def test_zero_declaration_denominator_and_penalty():
    p = profiles()
    for item in p.values():
        item["bounds"]["grid"] = 2.0
    row = runner.trial(runner.schedule("pilot")[0], p)
    cell = runner.analyze([row])["cells"][0]
    assert cell["erroneous_among_declarations"]["fraction"] is None
    assert cell["actual_cost"]["mean"] == 0
    assert cell["penalized_cost"]["mean"] == 65536
    assert runner.analyze([row])["primary_interest"] is None


def test_unknown_bias_excludes_only_affected_candidate():
    p = profiles()
    p["exact_table"]["bounds"]["grid"] = None
    row = runner.trial(runner.schedule("pilot")[0], p)
    assert row["choice"]["selected"] == "linearized"
    p["linearized"]["bounds"]["grid"] = None
    events = []
    row = runner.trial(runner.schedule("pilot")[0], p, events.append)
    assert row["choice"]["selected"] is None and not events


@pytest.mark.parametrize("purpose", ["pilot", "calibration_0", "calibration_1", "pricing"])
def test_interrupt_after_completed_draw_retains_costs(tmp_path, monkeypatch, purpose):
    configure(monkeypatch)
    spec = dict(runner.schedule("pilot")[0], arm="unequal_target", attempt=0)
    monkeypatch.setattr(runner, "schedule", lambda stage: [spec])

    def interrupted(spec, profiles, emit):
        def wrapped(event):
            emit(event)
            if event["event"] == "draw_completed" and event["purpose"] == purpose:
                raise RuntimeError("injected after draw")

        return runner.trial(spec, profiles, wrapped)

    out = tmp_path / "interrupted"
    with pytest.raises(RuntimeError):
        runner.run(out, "pilot", acquire=interrupted)
    audit = runner.reconcile(out)
    assert audit["started"] == 1 and audit["completed"] == 0
    assert audit["completed_shots"] >= 1024 and audit["unresolved_shots_upper"] == 0
    assert audit["mean_penalized_cost_among_started"] == 65536


def rewrite_fixture(out, filename, mutate):
    # Corrupt only a pytest-owned temporary archive, then reseal hashes to test semantics.
    value = json.loads((out / filename).read_text())
    mutate(value)
    (out / filename).unlink()
    runner.write_json(out / filename, value)
    (out / "complete.json").unlink()
    runner.finish_run(out)


@pytest.mark.parametrize("fault", ["sources", "projection", "duration", "stage", "cap"])
def test_semantic_tampering_rejected_even_with_updated_manifest(tmp_path, monkeypatch, fault):
    configure(monkeypatch)
    out = tmp_path / "pilot"
    runner.run(out, "pilot")
    if fault == "sources":
        rewrite_fixture(out, "planned.json", lambda d: d["config"].update(replay_sources={}))
    elif fault == "cap":
        rewrite_fixture(out, "planned.json", lambda d: d["config"].update(cap_seconds=-1))
    elif fault == "stage":
        rewrite_fixture(out, "summary.json", lambda d: d.update(stage="main"))
    elif fault == "duration":
        rewrite_fixture(out, "row_00000.json", lambda d: d.update(elapsed_seconds=-1))
    else:
        rewrite_fixture(out, "summary.json", lambda d: d.update(projection_seconds=-1))
    with pytest.raises(ValueError):
        runner.verify(out)


def test_deadline_is_checked():
    with pytest.raises(TimeoutError):
        runner.check_deadline(0.0)


def test_cap_before_first_trial_records_unattempted(tmp_path, monkeypatch):
    configure(monkeypatch)
    out = tmp_path / "capped"
    result = runner.run(out, "pilot", cap_seconds=1e-12)
    assert result["status"] == "time_cap_partial" and result["completed"] == 0
    audit = runner.reconcile(out)
    assert audit["started"] == 0 and audit["unattempted"] == 5
    with pytest.raises(ValueError, match="incomplete"):
        runner.verify(out)


def test_raw_row_before_completion_failure_is_reconciled(tmp_path, monkeypatch):
    configure(monkeypatch)
    original = runner.append_event

    def failing_append(output, event):
        if event["event"] == "completed":
            raise OSError("injected completion persistence failure")
        original(output, event)

    monkeypatch.setattr(runner, "append_event", failing_append)
    out = tmp_path / "raw_before_event"
    with pytest.raises(OSError):
        runner.run(out, "pilot")
    audit = runner.reconcile(out)
    assert audit["states"]["0"] == "raw_needs_reconciliation"
    assert audit["completed_shots"] > 0
    assert audit["mean_penalized_cost_among_started"] == 65536


def test_main_verifies_copied_pilot_with_isolated_fixtures(tmp_path, monkeypatch):
    pilot_specs, main_specs = runner.schedule("pilot")[:5], runner.schedule("main")[:5]
    configure(monkeypatch)
    monkeypatch.setattr(
        runner, "schedule", lambda stage: pilot_specs if stage == "pilot" else main_specs
    )
    pilot, main = tmp_path / "pilot", tmp_path / "main"
    runner.run(pilot, "pilot")
    result = runner.run(main, "main", pilot)
    assert result["verification"]["verified"] and result["workflow_seconds"] < 7200
    assert runner.verify(main)["rows"] == 5
    rewrite_fixture(
        main / "input", "profile_E001.json", lambda d: d["exact_table"].update(amplitude=0.3)
    )
    with pytest.raises(ValueError):
        runner.same_inputs(main / "input", pilot / "input")


def test_deadline_expiring_during_final_analysis_is_rejected(tmp_path, monkeypatch):
    configure(monkeypatch)
    out = tmp_path / "pilot"
    runner.run(out, "pilot")
    original = runner.analyze

    def expires(rows):
        result = original(rows)
        monkeypatch.setattr(runner.time, "perf_counter", lambda: 10.0)
        return result

    monkeypatch.setattr(runner.time, "perf_counter", lambda: 0.0)
    monkeypatch.setattr(runner, "analyze", expires)
    with pytest.raises(TimeoutError):
        runner.verify(out, deadline=5.0)


def test_inclusive_delivery_boundary_uses_counts():
    rows = []
    for arm in runner.ARMS:
        for rep in range(400):
            target = arm == "unequal_target"
            delivered = rep < (380 if target else 388)
            rows.append(
                dict(
                    spec=dict(
                        phase="primary",
                        contract="E001",
                        scenario="design_match",
                        guard=0.0,
                        arm=arm,
                        rep=rep,
                    ),
                    status="precision_met" if delivered else "not_certified",
                    interval=[0.0, 1.0],
                    contains=True,
                    erroneous=False,
                    plan=None,
                    total_shots=32768 if target else 65536,
                    total_cx=0,
                    penalized_cost=32768 if target and delivered else 65536,
                )
            )
    result = runner.analyze(rows)["primary_interest"]
    assert result["passed"]


def test_torn_tail_and_raw_preserve_durable_draws(tmp_path):
    spec = dict(runner.schedule("pilot")[0], arm="unequal_target", attempt=0)
    out = tmp_path / "torn"
    out.mkdir()
    runner.write_json(out / "schedule.json", [spec])
    runner.append_event(out, dict(attempt=0, event="started"))
    runner.append_event(
        out, dict(attempt=0, event="draw_started", purpose="pilot", shots=1024, logical_cx=0)
    )
    runner.append_event(
        out,
        dict(
            attempt=0,
            event="draw_completed",
            purpose="pilot",
            shots=1024,
            logical_cx=0,
            successes=30,
        ),
    )
    with (out / "events.jsonl").open("ab") as stream:
        stream.write(b'{"attempt":0,"event":')
    with (out / "row_00000.json").open("x") as stream:
        stream.write('{"result":')
    audit = runner.reconcile(out)
    assert audit["completed_shots"] == 1024 and audit["truncated_event_tail"]
    assert not audit["resource_accounting_complete"]
    assert audit["states"]["0"] == "raw_needs_reconciliation"


@pytest.mark.parametrize("fault", ["late_pilot", "wrong_count", "over_budget"])
def test_invalid_recovery_contract_is_rejected(tmp_path, fault):
    spec = dict(runner.schedule("pilot")[0], arm="fixed_cp", attempt=0)
    out = tmp_path / "invalid"
    out.mkdir()
    runner.write_json(out / "schedule.json", [spec])
    runner.append_event(out, dict(attempt=0, event="started"))
    if fault == "late_pilot":
        runner.append_event(
            out, dict(attempt=0, event="draw_started", purpose="pilot", shots=1024, logical_cx=0)
        )
    else:
        plan = dict(
            arm="fixed_cp",
            pilot_shots=0,
            m0=16384,
            m1=16384,
            n=65536 if fault == "over_budget" else 32768,
        )
        runner.append_event(out, dict(attempt=0, event="plan_frozen", plan=plan))
        runner.append_event(
            out,
            dict(
                attempt=0, event="draw_started", purpose="calibration_0", shots=1024, logical_cx=0
            ),
        )
    with pytest.raises(ValueError):
        runner.reconcile(out)


def test_failure_handler_preserves_torn_event_prefix(tmp_path, monkeypatch):
    configure(monkeypatch)
    original = runner.append_event

    def torn_append(output, event):
        if event["event"] == "draw_completed":
            with (output / "events.jsonl").open("ab") as stream:
                stream.write(b'{"attempt":0,"event":')
            raise OSError("injected torn persistence")
        original(output, event)

    monkeypatch.setattr(runner, "append_event", torn_append)
    out = tmp_path / "torn_failure"
    with pytest.raises(OSError, match="torn persistence"):
        runner.run(out, "pilot")
    assert (out / "failure.json").exists()
    assert (out / "events.jsonl").read_bytes().endswith(b'{"attempt":0,"event":')
    audit = runner.reconcile(out)
    assert audit["truncated_event_tail"] and audit["unresolved_shots_upper"] > 0
    assert not audit["resource_accounting_complete"]
