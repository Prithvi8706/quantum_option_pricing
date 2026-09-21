"""Second-pass review findings and reconciled acquisition behavior."""

import json
from types import SimpleNamespace

import numpy as np
import pytest

from research.journal_sprint.checks import archive_names, require_archives
from research.journal_sprint.package_handoff import checked_test_report
from research.paper_a.schema import validate_record
from research.paper_a.tests.test_schema import _record


@pytest.mark.parametrize("field", ["raw_estimation", "raw_price", "presentation_clipped_price"])
def test_huge_integer_is_a_violation(field):
    assert validate_record(_record(**{field: 10**400}))


def test_huge_interval_element_is_a_violation():
    assert validate_record(_record(raw_confidence_interval=[0, 10**400]))


@pytest.mark.parametrize("c", [0, -1, 2, float("inf"), float("nan")])
def test_rescaling_domain_at_payoff_and_circuit(c):
    from research.paper_a.payoff import h_inverse
    from research.paper_a.european.circuits import build_european
    from research.paper_a.benchmark import by_id

    with pytest.raises(ValueError):
        h_inverse(0.5, 100, 200, c)
    with pytest.raises(ValueError):
        build_european(by_id("E025"), 50, 200, 2, c)


@pytest.mark.parametrize("field", ["experiment_uuid", "phase", "config_id", "condition"])
def test_stream_delimiter_collision_is_rejected(field):
    from research.paper_a.streams import stream_key
    from research.paper_a.tests.test_streams import ARGS

    with pytest.raises(ValueError):
        stream_key(**{**ARGS, field: "a | b"})


def test_git_environment_outside_cwd_and_unavailable(tmp_path, monkeypatch):
    from research.paper_a import environment

    expected = environment._git_commit()
    monkeypatch.chdir(tmp_path)
    assert environment._git_commit() == expected != "unavailable"
    monkeypatch.setattr(environment, "_REPO_ROOT", tmp_path)
    assert environment._git_commit() == "unavailable"
    assert environment._git_dirty() is None


def test_later_xml_suite_failure_is_rejected(tmp_path):
    path = tmp_path / "tests.xml"
    path.write_text(
        '<testsuites><testsuite tests="2" errors="0" failures="0"/>'
        '<testsuite tests="1" errors="0" failures="1"/></testsuites>'
    )
    with pytest.raises(ValueError):
        checked_test_report(path)
    path.write_text('<testsuite tests="2" errors="0" failures="0"/>')
    assert checked_test_report(path)["tests"] == "2"


def test_rqmc_result_is_json_serializable():
    from research.journal_sprint.classical_baselines import estimate

    spec = dict(kind="asian", d=8, S0=100, K=100, rate=0.05, sigma=0.2, maturity=1)
    result = estimate(spec, "rqmc", 128, ("review-json",))
    assert len(json.loads(json.dumps(result, allow_nan=False))["scramble_means"]) == 32


def test_unknown_experiment_rejected():
    from research.journal_sprint.analyze import validate_experiments

    records = [{"experiment": "fixed"}]
    assert validate_experiments(records, {"fixed": 1}) == {"fixed": 1}
    with pytest.raises(ValueError):
        validate_experiments(records + [{"experiment": "rogue"}], {"fixed": 1})


def test_archive_aliases_rejected_and_missing_inputs_actionable(tmp_path):
    with pytest.raises(ValueError, match="aliased"):
        archive_names(["a/b", "a\\b"])
    assert archive_names(["a\\b"]) == {"a/b"}
    with pytest.raises(FileNotFoundError, match="--archive-root"):
        require_archives(tmp_path, ["missing"])


@pytest.fixture
def smoke_stub(monkeypatch):
    from research.paper_a.scripts import run_smoke as runner
    from research.paper_a.recording import Invocation

    monkeypatch.setattr(runner, "CONFIGS", ("E001",))
    monkeypatch.setattr(runner, "REPLICATES", (0,))
    monkeypatch.setattr(
        runner, "build_european", lambda *a: SimpleNamespace(circuit=None, objective_qubit=0)
    )
    monkeypatch.setattr(runner, "EstimationProblem", lambda **k: None)
    state = {"calls": 0, "fail": False, "seeds": []}

    class Estimator:
        def __init__(self, **kwargs):
            self.sampler = kwargs["sampler"]

        def estimate(self, problem):
            state["calls"] += 1
            seed = self.sampler._inner.options.seed
            state["seeds"].append(seed)
            assert isinstance(seed, np.random.Generator)
            self.sampler.invocations.append(
                Invocation(0, 16, "a", "b", 3, {"cx": 2}, 16, "complete")
            )
            if state["fail"]:
                raise RuntimeError("after submitted round")
            return SimpleNamespace(estimation=0.2, confidence_interval=[0.1, 0.3], powers=[0])

    monkeypatch.setattr(runner, "IterativeAmplitudeEstimation", Estimator)
    return runner, state


def test_smoke_configuration_and_rng_reconciliation(tmp_path, smoke_stub):
    runner, state = smoke_stub
    runner.run_smoke(tmp_path, shots=16)
    runner.run_smoke(tmp_path, shots=16)
    assert state["calls"] == 1
    record = json.loads((tmp_path / "raw.jsonl").read_text())
    assert record["q_total"] == 1e-5 and record["shots"] == 16
    seed = state["seeds"][0]
    assert seed.random() != seed.random()
    with pytest.raises(ValueError, match="configuration changed"):
        runner.run_smoke(tmp_path, shots=32)
    assert state["calls"] == 1
    assert not (tmp_path / "COMPLETE").exists()


def test_failed_acquisition_records_actual_ledger(tmp_path, smoke_stub):
    runner, state = smoke_stub
    state["fail"] = True
    with pytest.raises(RuntimeError, match="submitted"):
        runner.run_smoke(tmp_path, shots=16)
    record = json.loads((tmp_path / "raw.jsonl").read_text())
    resources = json.loads((tmp_path / "resources.jsonl").read_text())
    assert record["completion_state"] == "failed"
    assert resources["known_effective_shots"] == 16
    assert resources["invocation_ledger"][0]["isa_depth"] == 3
    assert resources["query_costs"] is None
    assert not (tmp_path / "COMPLETE").exists()
    with pytest.raises(ValueError, match="failed attempt retained"):
        runner.run_smoke(tmp_path, shots=16)
    assert state["calls"] == 1
