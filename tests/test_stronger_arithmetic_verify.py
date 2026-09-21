"""Adversarial verifier tests; synthetic acquisitions do not claim gate replay."""

from copy import deepcopy
from fractions import Fraction
import json

import pytest

from research.stronger_arithmetic import verify as v


def put(path, value):
    path.write_text(json.dumps(value, allow_nan=False), encoding="utf-8")


def seal(path):
    put(
        path / "complete.json",
        {"sha256": {p.name: v.sha256(p) for p in path.iterdir() if p.name != "complete.json"}},
    )


def certificates(case, spec, error):
    assert error == "0.00001"
    plan = dict(overflow_safe=True, affine_rows=[[0, [1]]], selector_bits=2)
    budget = dict(
        beta_upper=1.0,
        deterministic_upper="0.25",
        components={"arithmetic": "0.25"},
        schedule=v.schedule(1, "0.25"),
    )
    return plan, budget, [{"q": 1}, {"q": 2}]


def component(plan, reduced):
    return {
        layout: dict(
            total=dict(x=4, cx=3, ccx=2),
            native=dict(cx=15, u=22),
            qubits=7 if layout == "reused" else 9,
            logical_depth=12,
            reuse=layout == "reused",
            reduced=reduced,
        )
        for layout in ("retained", "reused")
    }


@pytest.fixture
def acquisition(tmp_path, monkeypatch):
    path = tmp_path / "archive"
    path.mkdir()
    refs = {
        c: {
            "arithmetic_plan": certificates(c, None, "0.00001")[0],
            "alternatives": [
                dict(mode="reflection", resources=dict(control_cancelled_total_cx_projection=1000)),
                dict(mode="ripple", resources=dict(control_cancelled_total_cx_projection=3000)),
            ],
        }
        for c in ("D1", "D2")
    }
    monkeypatch.setattr(v, "provenance", lambda planned: refs)
    monkeypatch.setattr(v, "replay_certificate", certificates)
    put(
        path / "planned.json",
        dict(config=v.CONFIG, source_sha256={}, input_sha256={}, git_head="a" * 40),
    )
    loading = dict(resources=dict(cx=2, u=3, qubits=10, depth=4), error_upper="0.00001")
    put(path / "loader.json", loading)
    rows, finite = [], []
    for case in ("D1", "D2"):
        for index, spec in enumerate(v.SPECS):
            plan, budget, diagnostic = certificates(case, spec, loading["error_upper"])
            arm = "workspace_only" if spec is None else "range_reduced"
            comp = component(plan, spec is not None)
            put(
                path / f"{case}_{index:02}.json",
                dict(
                    case=case,
                    spec=spec,
                    arm=arm,
                    plan=plan,
                    budget=budget,
                    status="ideal_plan",
                    components=comp,
                ),
            )
            finite.append(dict(case=case, spec=spec, diagnostics=diagnostic))
            for layout in ("retained", "reused"):
                rows.append(
                    dict(
                        case=case,
                        spec=spec,
                        arm=arm,
                        layout=layout,
                        budget=budget,
                        status="ideal_plan",
                        arithmetic_depth=12,
                        resources=v.ledger(
                            dict(cx=17, u=28), comp[layout]["qubits"], 30, budget["schedule"]
                        ),
                    )
                )
    put(path / "finite.json", finite)
    put(
        path / "results.json",
        dict(
            rows=rows,
            summary=v.summary(rows, refs),
            residual_arm=dict(
                status="not_admitted",
                reason="signed residual certificate and emitted oracle required",
            ),
            candidate_status="standby",
            quantum_over_classical_advantage=False,
            confirmation_admitted=False,
            production_choice=None,
        ),
    )
    seal(path)
    return path, refs


def mutate(path, name, change):
    value = v.read(path / name)
    change(value)
    put(path / name, value)
    seal(path)


def test_complete_default_distinguishes_metadata(acquisition, monkeypatch):
    path, _ = acquisition

    def forbidden(*args):
        pytest.fail("default must not re-emit gates")

    monkeypatch.setattr(v, "reemit_components", forbidden)
    monkeypatch.setattr(v, "reemit_loader", forbidden)
    monkeypatch.setattr(v, "reemit_zero", forbidden)
    result = v.verify(path)
    assert result["rows_checked"] == 148
    assert result["logical_cx_ledgers_checked"] == 296
    assert result["inputs_source_head_checked"] is True
    assert result["gate_reconstruction"] is False
    assert "recorded metadata" in result["scope"]


def test_summary_best_arithmetic_includes_baseline_but_winner_compares_reduced(acquisition):
    path, refs = acquisition
    rows = v.read(path / "results.json")["rows"]
    for row in rows:
        row["resources"]["control_cancelled_total_cx_projection"] = (
            10 if row["arm"] == "workspace_only" else 2000
        )
    for item in v.summary(rows, refs):
        assert item["best_arithmetic"]["arm"] == "workspace_only"
        assert item["best_reduced"]["arm"] == "range_reduced"
        assert item["winner"] == "reflection"
    assert all(item["best_arithmetic"] is None for item in v.summary([], refs))


def test_archived_baseline_drift_rejected(acquisition):
    path, refs = acquisition
    refs["D1"]["arithmetic_plan"]["selector_bits"] += 1
    with pytest.raises(ValueError, match="baseline/model drift"):
        v.verify(path)


def test_optional_reemit_and_full_acquisition_comparison(acquisition, monkeypatch):
    path, _ = acquisition
    calls = []

    def emit(plan, reduced):
        calls.append(reduced)
        return component(plan, reduced)

    monkeypatch.setattr(v, "reemit_components", emit)
    monkeypatch.setattr(v, "reemit_loader", lambda: v.read(path / "loader.json"))
    monkeypatch.setattr(v, "reemit_zero", lambda n: 30)
    assert v.verify(path, reemit=True)["component_acquisitions_reemitted"] == 74
    assert len(calls) == 74
    assert v.verify_replay(path, path)["exact_replay"] is True
    monkeypatch.setattr(v, "reemit_zero", lambda n: 31)
    with pytest.raises(ValueError, match="reflection"):
        v.verify(path, reemit=True)


def test_selected_reemits_baselines_and_best_both_layouts(acquisition, monkeypatch):
    path, _ = acquisition
    calls, reflections = [], []

    def emit(plan, reduced):
        calls.append(reduced)
        return component(plan, reduced)

    def zero(qubits):
        reflections.append(qubits)
        return 30

    monkeypatch.setattr(v, "reemit_components", emit)
    monkeypatch.setattr(v, "reemit_loader", lambda: v.read(path / "loader.json"))
    monkeypatch.setattr(v, "reemit_zero", zero)
    report = v.verify(path, reemit_selected=True)
    assert calls == [False, True, False, True]
    assert sorted(reflections) == [7, 9]
    assert report["component_acquisitions_reemitted"] == 4
    assert report["component_acquisitions_total"] == 74
    assert report["component_rows_reemitted"] == 8
    assert report["reemitted_configurations"] == ["D1_00", "D1_01", "D2_00", "D2_01"]
    assert report["gate_reconstruction"] is False
    assert report["gate_reconstruction_mode"] == "selected"
    assert report["loader_reemitted"] is True
    with pytest.raises(ValueError, match="either"):
        v.verify(path, reemit=True, reemit_selected=True)


@pytest.mark.parametrize("text", ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":1e999}'])
def test_strict_json_even_after_rehash(acquisition, text):
    path, _ = acquisition
    (path / "D1_00.json").write_text(text, encoding="utf-8")
    seal(path)
    with pytest.raises(ValueError):
        v.verify(path)


@pytest.mark.parametrize("extra", ["extra.json", "failed.json", "directory"])
def test_extra_inventory_rejected(acquisition, extra):
    path, _ = acquisition
    if extra == "directory":
        (path / extra).mkdir()
    else:
        put(path / extra, {})
    with pytest.raises(ValueError, match="inventory"):
        v.verify(path)


def test_hash_and_missing_inventory(acquisition):
    path, _ = acquisition
    (path / "D1_00.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="hash"):
        v.verify(path)
    (path / "D1_00.json").unlink()
    with pytest.raises(ValueError, match="inventory"):
        v.verify(path)


@pytest.mark.parametrize(
    "field,value",
    [
        ("candidate_status", "promoted"),
        ("confirmation_admitted", True),
        ("confirmation_admitted", 0),
        ("quantum_over_classical_advantage", True),
        ("production_choice", "arithmetic"),
    ],
)
def test_no_standby_promotion(acquisition, field, value):
    path, _ = acquisition
    mutate(path, "results.json", lambda d: d.update({field: value}))
    with pytest.raises(ValueError, match="promotion"):
        v.verify(path)


@pytest.mark.parametrize(
    "change",
    [
        lambda d: d["rows"].pop(),
        lambda d: d["rows"].append(deepcopy(d["rows"][0])),
        lambda d: d["rows"].__setitem__(1, deepcopy(d["rows"][0])),
        lambda d: d["rows"][0]["resources"].update(total_cx_projection=1),
        lambda d: d["rows"][0]["resources"].update(control_cancelled_total_cx_projection=1),
        lambda d: d["summary"][0].update(winner="arithmetic"),
    ],
)
def test_menu_ledgers_and_summary_rehashed_tampering(acquisition, change):
    path, _ = acquisition
    mutate(path, "results.json", change)
    with pytest.raises(ValueError):
        v.verify(path)


@pytest.mark.parametrize(
    "name,change",
    [
        ("planned.json", lambda d: d["config"].update(call_cap=999)),
        ("planned.json", lambda d: d["config"].update(confirmation=0)),
        ("D1_00.json", lambda d: d["plan"].update(overflow_safe=False)),
        ("D1_00.json", lambda d: d["budget"]["schedule"].update(M=2)),
        ("D1_00.json", lambda d: d["components"]["reused"]["native"].update(cx=3)),
        ("finite.json", lambda d: d.pop()),
    ],
)
def test_fixed_configuration_certificates_and_diagnostics(acquisition, name, change):
    path, _ = acquisition
    mutate(path, name, change)
    with pytest.raises(ValueError):
        v.verify(path)


def test_cap_rows_preserved_and_optional_cap_reconstruction(acquisition, monkeypatch):
    path, refs = acquisition
    reason = "conversion exceeds 4096 wires"

    def cap(d):
        d.pop("components")
        d.update(status="resource_cap", reason=reason)

    mutate(path, "D1_00.json", cap)

    def cap_rows(d):
        for r in d["rows"][:2]:
            r.pop("arithmetic_depth")
            r.update(status="resource_cap", resources=None, reason=reason)
        d["summary"] = v.summary(d["rows"], refs)

    mutate(path, "results.json", cap_rows)
    assert v.verify(path)["resource_cap_rows"] == 2
    monkeypatch.setattr(v, "reemit_loader", lambda: v.read(path / "loader.json"))
    monkeypatch.setattr(v, "reemit_components", component)
    with pytest.raises(ValueError, match="cap not reproduced"):
        v.verify(path, reemit=True)


@pytest.mark.parametrize(
    "beta,deterministic", [(1, "0"), (100, "0.2"), (1, "1"), (1, "2"), (10**9, "0"), (10**20, "0")]
)
def test_independent_schedule_matches_frozen_contract(beta, deterministic):
    from research.journal_sprint.claim_assessment import schedule

    assert v.schedule(beta, deterministic) == schedule(Fraction(beta), Fraction(deterministic))


def test_integer_ledgers_include_qft_swaps_and_both_directions():
    result = v.ledger(dict(cx=20, u=13), 4, 41, dict(M=8, phase_qubits=3, repetitions=17))
    assert result["total_cx_projection"] == 17 * (20 + 7 * (2 * 146 + 41 + 1) + 6 + 3)
    assert result["control_cancelled_total_cx_projection"] == 17 * (20 + 7 * (40 + 41 + 1) + 6 + 3)
    assert result["total_qubits"] == 9
    with pytest.raises(ValueError):
        v.ledger(dict(cx=True, u=13), 4, 41, {})


@pytest.mark.parametrize("name", ["../escape", "/absolute", "a\\b", "C:foo", "a//b"])
def test_manifest_paths_fail_closed(tmp_path, name):
    with pytest.raises(ValueError):
        v.safe_file(tmp_path, name)


def test_provenance_binds_source_input_inventory_and_git(tmp_path, monkeypatch):
    source_names = [
        "research/stronger_arithmetic/" + n + ".py"
        for n in ("run_study", "budget", "circuits", "components", "verify")
    ]
    legacy = "research/release_checks/json_io.py"
    source_names += [legacy, v.PROTOCOL]
    for name in source_names:
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"source\r\n" if name == legacy else b"source\n")
    reference = tmp_path / v.REFERENCE
    reference.mkdir(parents=True)
    for case in ("D1", "D2"):
        put(reference / f"case_{case}.json", {})
    seal(reference)
    planned = dict(
        git_head="a" * 40,
        tracked_tree_dirty=False,
        source_sha256={n: v.sha256(tmp_path / n) for n in source_names},
        input_sha256={v.REFERENCE + "/" + p.name: v.sha256(p) for p in reference.iterdir()},
    )
    committed = {
        n: (tmp_path / n).read_bytes().replace(b"\r\n", b"\n")
        for n in {*planned["source_sha256"], *planned["input_sha256"]}
    }

    def git(root, *args):
        if args[0] == "ls-tree":
            return "\n".join(n for n in source_names if n.endswith(".py")).encode()
        return committed[args[1].split(":", 1)[1]]

    monkeypatch.setattr(v, "git", git)
    assert v.provenance(planned, tmp_path) == {"D1": {}, "D2": {}}
    original = source_names[0]
    (tmp_path / original).write_bytes(b"source\r\n")
    planned["source_sha256"][original] = v.sha256(tmp_path / original)
    with pytest.raises(ValueError, match="commit"):
        v.provenance(planned, tmp_path)
    (tmp_path / original).write_bytes(committed[original])
    planned["source_sha256"][original] = v.sha256(tmp_path / original)
    planned["input_sha256"].pop(next(iter(planned["input_sha256"])))
    with pytest.raises(ValueError, match="input inventory"):
        v.provenance(planned, tmp_path)


def test_cli_exclusive_output_and_archive_immutability(acquisition, tmp_path):
    path, _ = acquisition
    output = tmp_path / "verification.json"
    v.main([str(path), str(output)])
    assert v.read(output)["passed"] is True
    with pytest.raises(FileExistsError):
        v.main([str(path), str(output)])
    with pytest.raises(ValueError, match="outside"):
        v.main([str(path), str(path / "verification.json")])
