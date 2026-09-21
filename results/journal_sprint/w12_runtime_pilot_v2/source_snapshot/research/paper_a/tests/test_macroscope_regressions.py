"""Review regressions independent of expensive stochastic smoke acquisitions."""

import json
from types import SimpleNamespace

import pytest
from qiskit import QuantumCircuit

from research.paper_a.benchmark import DomainError, validate_domain
from research.paper_a.recording import RecordingSampler
from research.paper_a.schema import append_record, read_records, validate_record
from research.paper_a.tests.test_schema import _record


@pytest.mark.parametrize("field", ["S0", "K", "r", "T", "sigma", "dividend"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_contract_is_rejected(field, value):
    inputs = dict(S0=100, K=100, r=0.05, T=1, sigma=0.2, dividend=0)
    inputs[field] = value
    with pytest.raises(DomainError, match="NONFINITE_INPUT"):
        validate_domain(**inputs)


@pytest.mark.parametrize(
    "ci", [[], [0.2], [0.2, 0.3, 0.4], "ab", {}, [True, 0.5], ["0", 1], [float("nan"), 1]]
)
def test_malformed_interval_returns_violation(ci):
    assert validate_record(_record(raw_confidence_interval=ci))


def test_append_requests_fsync(tmp_path, monkeypatch):
    from research.paper_a import schema

    calls = []
    monkeypatch.setattr(schema.os, "fsync", lambda descriptor: calls.append(descriptor))
    append_record(tmp_path / "raw.jsonl", _record())
    assert len(calls) == 1


def test_sampler_preserves_all_batch_members_and_metadata():
    submitted = []

    class Inner:
        def run(self, circuits, **kwargs):
            submitted.extend(circuits)
            return SimpleNamespace(
                result=lambda: SimpleNamespace(metadata=[{"shots": 17}, {"shots": 23}])
            )

    first, second = QuantumCircuit(1), QuantumCircuit(1)
    second.x(0)
    sampler = RecordingSampler(Inner(), 32)
    sampler.run([first, second])
    assert len(submitted) == 2
    assert [r.ordinal for r in sampler.invocations] == [0, 1]
    assert [r.effective_shots for r in sampler.invocations] == [17, 23]
    assert all(r.status == "complete" for r in sampler.invocations)
    assert sampler.invocations[0].logical_qpy_sha256 != sampler.invocations[1].logical_qpy_sha256


def test_batch_failure_retains_every_member():
    class Inner:
        def run(self, circuits, **kwargs):
            raise RuntimeError("backend failed")

    sampler = RecordingSampler(Inner(), 32)
    with pytest.raises(RuntimeError, match="backend failed"):
        sampler.run([QuantumCircuit(1), QuantumCircuit(1)])
    assert len(sampler.invocations) == 2
    assert all(r.status == "failed" for r in sampler.invocations)


def test_interrupted_pair_recovers_original_resource_payload(tmp_path, monkeypatch):
    from research.paper_a.scripts import run_smoke as runner

    raw, res = tmp_path / "raw.jsonl", tmp_path / "resources.jsonl"
    record, resource = (
        {"idempotency_key": "key", "value": 1},
        {"idempotency_key": "key", "provenance": "actual", "value": 2},
    )
    original = runner.append_record

    def fail_resource(path, payload):
        if path == res:
            raise OSError("interrupted between appends")
        original(path, payload)

    monkeypatch.setattr(runner, "append_record", fail_resource)
    with pytest.raises(OSError):
        runner._persist_pair(tmp_path, raw, res, record, resource)
    monkeypatch.setattr(runner, "append_record", original)
    assert runner._recover_pairs(tmp_path, raw, res) == {"key"}
    assert runner._recover_pairs(tmp_path, raw, res) == {"key"}
    assert read_records(raw) == [record]
    assert read_records(res) == [resource]


def test_legacy_partial_record_is_not_falsely_completed(tmp_path):
    from research.paper_a.scripts import run_smoke as runner

    raw, res = tmp_path / "raw.jsonl", tmp_path / "resources.jsonl"
    append_record(raw, {"idempotency_key": "key"})
    (tmp_path / "COMPLETE").write_text("stale success")
    with pytest.raises(ValueError, match="unpaired legacy"):
        runner.run_smoke(tmp_path)
    assert not (tmp_path / "COMPLETE").exists()
    assert read_records(raw) == [{"idempotency_key": "key"}]
    assert not res.exists()


def test_invalid_records_never_receive_complete(tmp_path, monkeypatch):
    from research.paper_a.scripts import run_smoke as runner

    record = _record(idempotency_key="key", raw_confidence_interval=[])
    append_record(tmp_path / "raw.jsonl", record)
    append_record(tmp_path / "resources.jsonl", {"idempotency_key": "key"})
    (tmp_path / "COMPLETE").write_text("stale success")
    monkeypatch.setattr(runner, "CONFIGS", ())
    with pytest.raises(ValueError, match="validation failed"):
        runner.run_smoke(tmp_path)
    assert not (tmp_path / "COMPLETE").exists()
    assert json.loads((tmp_path / "validation.json").read_text())["violations"]


@pytest.mark.parametrize("target", ["h_inverse", "to_price"])
def test_independent_dollar_gate_detects_conversion_mutation(monkeypatch, target):
    from research.paper_a import validation
    from research.paper_a.benchmark import by_id

    original = getattr(validation, target)
    monkeypatch.setattr(validation, target, lambda *args: original(*args) + 1)
    gates = validation.run_e0_gates([by_id("E025")], 1e-4, (2,), 0.25)
    assert not next(g for g in gates if g.name == "dollar_round_trip").passed
