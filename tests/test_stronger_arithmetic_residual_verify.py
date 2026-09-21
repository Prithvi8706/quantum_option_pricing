"""Residual verifier tests with tiny actual gates and synthetic financial archives."""

from copy import deepcopy
import json

import pytest

from research.stronger_arithmetic import verify_residual as v


def put(path, value):
    path.write_text(json.dumps(value, allow_nan=False), encoding="utf-8")


def seal(path):
    put(
        path / "complete.json",
        {"sha256": {p.name: v.sha256(p) for p in path.iterdir() if p.name != "complete.json"}},
    )


def mutate(path, name, change):
    value = v.read(path / name)
    change(value)
    put(path / name, value)
    seal(path)


@pytest.fixture(scope="module")
def tiny():
    from research.stronger_arithmetic.components import components
    from research.stronger_arithmetic.residual_components import residual_components

    parent = dict(
        normal_qubits=2,
        selector_bits=4,
        width=6,
        fraction_bits=1,
        affine_rows=[(0, [1, 1]), (0, [1, 0])],
        reductions=0,
        spot=1,
        exp_budget=dict(
            coefficients=[2, 2],
            intermediate_magnitude_upper="3",
            reductions=0,
            spot=1,
            output_integer_bounds=[0, 6],
            overflow_safe=True,
        ),
        strike_sum=5,
        overflow_safe=True,
    )
    base = components(parent, reuse=True, reduced=True)
    base["parent_plan"] = deepcopy(parent)
    cert = dict(
        schema="signed_residual_plan_v1",
        parent_plan=deepcopy(parent),
        width=6,
        fraction_bits=1,
        strike_sum=5,
        dimension=2,
        selector_bits=4,
        reciprocal_integer=2,
        control_coefficients=[2, 1, 0, 0, 0],
        control_scale_integer=2,
        shift_integer=8,
        residual_integer_bounds=[-3, 3],
        threshold_integer_bounds=[5, 11],
        overflow_safe=True,
        overflow_failures=[],
    )
    component = residual_components(parent, cert, base)
    return v.normalized((parent, cert, base, component))


@pytest.fixture
def acquisition(tmp_path, monkeypatch, tiny):
    parent, cert, base, component = deepcopy(tiny)
    path = tmp_path / "archive"
    path.mkdir()
    loading = dict(resources=dict(cx=2, u=3, qubits=10, depth=4), error_upper="0.00001")
    budget = dict(
        components={"representation": "0.25"},
        deterministic_upper="0.25",
        beta_upper_rational="1",
        schedule=v.schedule(1, "0.25"),
    )
    offsets = {c: {"case": c, "offset": 12.0} for c in v.CONFIG["cases"]}
    primary = {
        "loader.json": loading,
        "results.json": {
            "summary": [
                dict(
                    case=c,
                    best_arithmetic=dict(
                        resources=dict(control_cancelled_total_cx_projection=2000)
                    ),
                    reflection_reference=dict(
                        resources=dict(control_cancelled_total_cx_projection=1000)
                    ),
                )
                for c in v.CONFIG["cases"]
            ]
        },
    }
    monkeypatch.setattr(v, "provenance", lambda planned: (primary, [1, 0, 1, 0, 1]))
    monkeypatch.setattr(
        v, "prepare_case", lambda case, low: (case, {10: (None, None, offsets[case])})
    )

    def replay(context, spec, low, parent_record, loading_record):
        assert loading_record["error_upper"] == "0.00001"
        return deepcopy((cert, budget, [{"q": 1}, {"q": 2}]))

    monkeypatch.setattr(v, "replay_certificate", replay)
    put(
        path / "planned.json",
        dict(config=v.CONFIG, git_head="a" * 40, source_sha256={}, input_sha256={}),
    )
    rows, finite = [], []
    for case in v.CONFIG["cases"]:
        put(path / (case + "_offset.json"), offsets[case])
        for i, spec in enumerate(v.SPECS):
            primary[f"{case}_{i:02}.json"] = dict(
                spec=spec,
                plan=parent,
                budget=budget,
                status="ideal_plan",
                components={
                    "reused": {k: value for k, value in base.items() if k != "parent_plan"}
                },
            )
            native = {k: component["native"][k] + 2 * loading["resources"][k] for k in ("u", "cx")}
            native["u"] += cert["selector_bits"] + 1
            resources = v.ledger(native, component["qubits"], 30, budget["schedule"])
            record = dict(
                case=case,
                spec=spec,
                certificate=cert,
                budget=budget,
                status="ideal_plan",
                components=component,
                resources=resources,
            )
            put(path / f"{case}_{i:02}.json", record)
            rows.append({k: record[k] for k in ("case", "spec", "budget", "status", "resources")})
            finite.append(dict(case=case, spec=spec, diagnostics=[{"q": 1}, {"q": 2}]))
    put(path / "finite.json", finite)
    put(
        path / "results.json",
        dict(
            rows=rows,
            summary=v.summary(rows, primary["results.json"]),
            candidate_status="standby",
            production_choice=None,
            quantum_over_classical_advantage=False,
            confirmation_admitted=False,
        ),
    )
    seal(path)
    return path, primary


def test_full_default_metadata_replay(acquisition, monkeypatch):
    path, _ = acquisition

    def forbidden(*args):
        pytest.fail("default must not emit gates")

    monkeypatch.setattr(v, "reemit_component", forbidden)
    monkeypatch.setattr(v.primary_verify, "reemit_loader", forbidden)
    result = v.verify(path)
    assert result["rows_checked"] == result["certificates_replayed"] == 18
    assert result["logical_cx_ledgers_checked"] == 36
    assert result["oracle_acquisitions_reemitted"] == 0
    assert result["oracle_acquisitions_total"] == 18
    assert result["all_gates_reconstructed"] is False
    assert result["inputs_source_head_checked"] is True


@pytest.mark.parametrize("all_oracles", [False, True])
def test_optional_emission_coverage_and_parent_binding(acquisition, monkeypatch, tiny, all_oracles):
    path, primary = acquisition
    calls = []

    def emit(parent, certificate, base):
        assert base["parent_plan"] == parent
        assert base["reuse"] is True
        calls.append(parent)
        return tiny[3]

    monkeypatch.setattr(v, "reemit_component", emit)
    monkeypatch.setattr(v.primary_verify, "reemit_loader", lambda: primary["loader.json"])
    monkeypatch.setattr(v.primary_verify, "reemit_zero", lambda n: 30)
    result = v.verify(path, reemit=all_oracles, reemit_selected=not all_oracles)
    assert result["oracle_acquisitions_reemitted"] == len(calls) == (18 if all_oracles else 2)
    if not all_oracles:
        assert result["reemitted_configurations"] == ["D1_00", "D2_00"]
    assert result["inherited_primary_gates_reemitted"] is False
    assert result["all_gates_reconstructed"] is False
    with pytest.raises(ValueError, match="choose"):
        v.verify(path, reemit=True, reemit_selected=True)


def test_independent_component_mapping_accepts_actual_tiny_gates(tiny):
    parent, cert, base, component = tiny
    v.component_metadata(component, parent, cert, base)


@pytest.mark.parametrize(
    "change",
    [
        lambda c: c["total"].update(cx=0),
        lambda c: c["native"].update(u=0),
        lambda c: c.update(qubits=2),
        lambda c: c.update(depth_upper=1),
        lambda c: c.update(actual_remapped_depth=True),
        lambda c: c.update(base_component_sha256="0" * 64),
        lambda c: c["semantic_checks"][0].update(inverse_checked=False),
        lambda c: c["wire_layout"].update(shared_conversion_scratch=0),
        lambda c: c["complete_postoracle"].update(cx=8_000_001),
    ],
)
def test_component_metadata_tampering(tiny, change):
    parent, cert, base, component = deepcopy(tiny)
    change(component)
    with pytest.raises(ValueError):
        v.component_metadata(component, parent, cert, base)


@pytest.mark.parametrize(
    "change",
    [
        lambda d: d["rows"].pop(),
        lambda d: d["rows"].__setitem__(1, deepcopy(d["rows"][0])),
        lambda d: d["rows"][0]["resources"].update(total_cx_projection=1),
        lambda d: d["rows"][0]["resources"].update(control_cancelled_total_cx_projection=1),
        lambda d: d.update(candidate_status="selected"),
        lambda d: d.update(confirmation_admitted=0),
        lambda d: d.update(confirmation_admitted=True),
        lambda d: d.update(quantum_over_classical_advantage=True),
        lambda d: d.update(production_choice="residual_arithmetic"),
        lambda d: d["summary"][0].update(lowest_cost_routes=["residual_arithmetic"]),
    ],
)
def test_rehashed_rows_summary_and_promotion_rejected(acquisition, change):
    path, _ = acquisition
    mutate(path, "results.json", change)
    with pytest.raises(ValueError):
        v.verify(path)


@pytest.mark.parametrize(
    "name,change",
    [
        ("planned.json", lambda d: d["config"].update(q=2)),
        ("D1_00.json", lambda d: d["certificate"].update(shift_integer=0)),
        ("D1_00.json", lambda d: d["budget"]["schedule"].update(M=2)),
        ("D1_offset.json", lambda d: d.update(offset=13.0)),
        ("finite.json", lambda d: d.pop()),
    ],
)
def test_certificates_offsets_finite_and_fixed_menu(acquisition, name, change):
    path, _ = acquisition
    mutate(path, name, change)
    with pytest.raises(ValueError):
        v.verify(path)


@pytest.mark.parametrize("text", ['{"x":1,"x":2}', '{"x":NaN}', '{"x":1e999}'])
def test_strict_json(acquisition, text):
    path, _ = acquisition
    (path / "D1_00.json").write_text(text, encoding="utf-8")
    seal(path)
    with pytest.raises(ValueError):
        v.verify(path)


def test_exclusive_inventory_hash_and_output(acquisition, tmp_path):
    path, _ = acquisition
    output = tmp_path / "verified.json"
    v.main([str(path), str(output)])
    assert v.read(output)["passed"] is True
    with pytest.raises(FileExistsError):
        v.main([str(path), str(output)])
    with pytest.raises(ValueError, match="outside"):
        v.main([str(path), str(path / "verified.json")])
    (path / "extra").mkdir()
    with pytest.raises(ValueError, match="inventory"):
        v.verify(path)
    (path / "extra").rmdir()
    (path / "D1_00.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="hash"):
        v.verify(path)


def test_primary_spec_missing_and_duplicate(acquisition):
    path, primary = acquisition
    row = primary.pop("D1_00.json")
    with pytest.raises(ValueError, match="spec"):
        v.verify(path)
    primary["D1_00.json"] = row
    primary["D1_extra.json"] = deepcopy(row)
    with pytest.raises(ValueError, match="spec"):
        v.verify(path)


def test_cap_failure_preserved_and_reemission_requires_failure(acquisition, monkeypatch):
    path, primary = acquisition
    reason = "residual oracle exceeds 8M gates or 4096 wires"

    def cap(record):
        record.pop("components")
        record.update(status="resource_cap", resources=None, reason=reason)

    mutate(path, "D1_00.json", cap)

    def rows(d):
        d["rows"][0].update(status="resource_cap", resources=None)
        d["summary"] = v.summary(d["rows"], primary["results.json"])

    mutate(path, "results.json", rows)
    assert v.verify(path)["oracle_acquisitions_total"] == 17
    monkeypatch.setattr(v.primary_verify, "reemit_loader", lambda: primary["loader.json"])
    monkeypatch.setattr(v, "reemit_component", lambda *args: {})
    with pytest.raises(ValueError, match="cap not reproduced"):
        v.verify(path, reemit=True)


@pytest.mark.parametrize(
    "primary_cost,reflection_cost,residual_cost,routes,winner",
    [
        (10, 20, 30, ["primary_arithmetic"], "reflection"),
        (10, 10, 10, ["reflection", "primary_arithmetic", "residual_arithmetic"], "tie"),
        (30, 20, 10, ["residual_arithmetic"], "residual_arithmetic"),
    ],
)
def test_summary_independent_ties_and_comparisons(
    primary_cost, reflection_cost, residual_cost, routes, winner
):
    from research.stronger_arithmetic.run_residual import summarize

    def resource(cost):
        return dict(resources=dict(control_cancelled_total_cx_projection=cost))

    primary = {
        "summary": [
            dict(
                case=c,
                best_arithmetic=resource(primary_cost),
                reflection_reference=resource(reflection_cost),
            )
            for c in v.CONFIG["cases"]
        ]
    }
    rows = [dict(case=c, status="ideal_plan", **resource(residual_cost)) for c in v.CONFIG["cases"]]
    result = v.summary(rows, primary)
    assert result == summarize(rows, primary)
    assert all(
        r["lowest_cost_routes"] == routes and r["winner_vs_reflection"] == winner for r in result
    )
    assert all(r["best_residual"] is None for r in v.summary([], primary))


def test_full_acquisition_comparison(acquisition):
    path, _ = acquisition
    assert v.verify_replay(path, path)["exact_replay"] is True


@pytest.fixture
def provenance_tree(tmp_path, monkeypatch):
    names = [
        "research/stronger_arithmetic/" + n + ".py"
        for n in (
            "run_residual",
            "residual",
            "residual_circuits",
            "residual_components",
            "verify_residual",
            "verify",
            "run_study",
        )
    ]
    legacy = "research/release_checks/json_io.py"
    names += [legacy, v.PROTOCOL]
    for name in names:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"source\r\n" if name == legacy else b"source\n")
    old_input = v.primary_verify.REFERENCE + "/case_D1.json"
    path = tmp_path / old_input
    path.parent.mkdir(parents=True)
    put(path, {})
    primary = {
        "planned.json": dict(
            config=v.primary_verify.CONFIG, input_sha256={old_input: v.sha256(path)}
        ),
        "results.json": dict(
            rows=[],
            summary=[],
            candidate_status="standby",
            production_choice=None,
            confirmation_admitted=False,
            quantum_over_classical_advantage=False,
        ),
    }
    folder = tmp_path / v.PRIMARY
    folder.mkdir(parents=True)
    for name, value in primary.items():
        put(folder / name, value)
    seal(folder)
    path = tmp_path / v.LOW_MODEL
    path.parent.mkdir(parents=True)
    put(path, {"low_coefficients": [1, 0, 1, 0, 1]})
    seal(path.parent)
    inputs = {v.PRIMARY + "/" + n: v.sha256(folder / n) for n in set(primary) | {"complete.json"}}
    inputs.update(primary["planned.json"]["input_sha256"])
    inputs.update({n: v.sha256(tmp_path / n) for n in (v.LOW_MODEL, v.LOW_COMPLETE)})
    planned = dict(
        git_head="a" * 40,
        tracked_tree_dirty=False,
        input_sha256=inputs,
        source_sha256={n: v.sha256(tmp_path / n) for n in names},
    )
    blobs = {
        n: (tmp_path / n).read_bytes().replace(b"\r\n", b"\n") for n in set(names) | set(inputs)
    }

    def git(root, *args):
        if args[0] == "ls-tree":
            return "\n".join(n for n in names if n.endswith(".py")).encode()
        return blobs[args[1].split(":", 1)[1]]

    # The primary archive/provenance helper has its own separate test suite;
    # isolate residual source/input binding while keeping actual file hashing.
    monkeypatch.setattr(v, "archive", lambda *args: primary)
    monkeypatch.setattr(v.primary_verify, "provenance", lambda *args: {})
    monkeypatch.setattr(v.primary_verify, "summary", lambda *args: [])
    monkeypatch.setattr(v.primary_verify, "git", git)
    return tmp_path, planned, blobs


def test_provenance_exact_inputs_and_legacy_newline_binding(provenance_tree):
    root, planned, _ = provenance_tree
    assert v.provenance(planned, root)[1] == [1, 0, 1, 0, 1]


@pytest.mark.parametrize(
    "attack",
    [
        "source_inventory",
        "input_inventory",
        "input_commit",
        "source_commit",
        "source_hash",
        "untracked",
        "dirty",
    ],
)
def test_provenance_tampering(provenance_tree, attack):
    root, planned, blobs = provenance_tree
    source = "research/stronger_arithmetic/run_residual.py"
    if attack == "source_inventory":
        planned["source_sha256"].pop(source)
    elif attack == "input_inventory":
        planned["input_sha256"].pop(v.LOW_COMPLETE)
    elif attack == "input_commit":
        blobs[v.LOW_MODEL] = b"different committed input"
    elif attack == "source_commit":
        (root / source).write_bytes(b"source\r\n")
        planned["source_sha256"][source] = v.sha256(root / source)
    elif attack == "source_hash":
        (root / source).write_bytes(b"edited source")
    elif attack == "untracked":
        (root / "research/release_checks/hidden.py").write_text("hidden", encoding="utf-8")
    else:
        planned["tracked_tree_dirty"] = 0
    with pytest.raises(ValueError):
        v.provenance(planned, root)
