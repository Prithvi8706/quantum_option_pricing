from types import SimpleNamespace

import pytest
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler

from research.paper_a.recording import RecordingSampler, transpile_frozen
from research.paper_a.streams import TRANSPILER_SEED

FROZEN_BASIS = ["rz", "sx", "x", "cx", "measure"]


def _bell_with_measure():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


class _FakeSampler:
    """Inner sampler stub that reports a fixed, caller-chosen metadata dict."""

    def __init__(self, metadata):
        self._metadata = metadata

    def run(self, circuits, **kwargs):
        return SimpleNamespace(
            result=lambda: SimpleNamespace(metadata=self._metadata)
        )


def test_transpilation_targets_only_the_frozen_basis():
    isa, _ = transpile_frozen(_bell_with_measure())
    assert set(isa.count_ops()) <= set(FROZEN_BASIS)


def test_transpilation_is_deterministic_under_the_frozen_seed():
    a, hash_a = transpile_frozen(_bell_with_measure())
    b, hash_b = transpile_frozen(_bell_with_measure())
    assert hash_a == hash_b
    assert a.count_ops() == b.count_ops()


def test_transpiled_hash_changes_with_the_circuit():
    _, h1 = transpile_frozen(_bell_with_measure())
    other = _bell_with_measure()
    other.x(0)
    _, h2 = transpile_frozen(other)
    assert h1 != h2


def test_sampler_records_one_invocation_per_run_call():
    sampler = RecordingSampler(Sampler(), shots=512)
    sampler.run([_bell_with_measure()]).result()
    sampler.run([_bell_with_measure()]).result()
    assert [i.ordinal for i in sampler.invocations] == [0, 1]


def test_repeated_identical_circuits_stay_distinct_invocations():
    sampler = RecordingSampler(Sampler(), shots=512)
    for _ in range(3):
        sampler.run([_bell_with_measure()]).result()
    assert len(sampler.invocations) == 3
    assert len({i.ordinal for i in sampler.invocations}) == 3


def test_effective_shots_come_from_result_metadata_not_the_default():
    # Configured default (2048) deliberately differs from what the fake
    # inner sampler reports (999), so a passing test proves the value was
    # actually read from metadata rather than echoed from the default.
    sampler = RecordingSampler(_FakeSampler([{"shots": 999}]), shots=2048)
    sampler.run([_bell_with_measure()]).result()
    inv = sampler.invocations[0]
    assert inv.requested_shots == 2048
    assert inv.effective_shots == 999


def test_missing_shots_key_raises_instead_of_falling_back_to_the_default():
    """A primitive that omits 'shots' from result metadata must not have its
    absence silently masked by the configured default: that would let a
    record look authoritative when the value was never actually measured."""
    sampler = RecordingSampler(_FakeSampler([{}]), shots=512)
    with pytest.raises(KeyError):
        sampler.run([_bell_with_measure()])
    assert len(sampler.invocations) == 1
    inv = sampler.invocations[0]
    assert inv.status == "failed"
    assert "shots" in inv.exception
    assert inv.effective_shots is None
    assert inv.isa_depth > 0, "pre-execution resources must still be retained"


def test_logical_and_isa_hashes_are_both_recorded_before_execution():
    sampler = RecordingSampler(Sampler(), shots=512)
    sampler.run([_bell_with_measure()]).result()
    inv = sampler.invocations[0]
    assert len(inv.logical_qpy_sha256) == 64
    assert len(inv.isa_qpy_sha256) == 64
    assert inv.isa_depth > 0
    assert set(inv.isa_ops) <= set(FROZEN_BASIS)


def test_partial_resources_survive_an_exception():
    """Annex I: on failure, completed records and the failing invocation's
    available resources remain durable."""
    class Exploding:
        def run(self, circuits, **kwargs):
            raise RuntimeError("simulated backend failure")

    sampler = RecordingSampler(Exploding(), shots=512)
    with pytest.raises(RuntimeError):
        sampler.run([_bell_with_measure()])
    assert len(sampler.invocations) == 1
    inv = sampler.invocations[0]
    assert inv.status == "failed"
    assert "simulated backend failure" in inv.exception
    assert inv.isa_depth > 0, "pre-execution resources must be retained"
    assert inv.effective_shots is None


def test_seed_is_the_frozen_value():
    assert TRANSPILER_SEED == 20260727
