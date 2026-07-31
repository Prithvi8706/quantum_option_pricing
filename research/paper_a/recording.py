"""Annex I: ordered append-only sampler recording and frozen transpilation.

Every primitive call is recorded BEFORE execution so that an exception still
leaves the invocation's logical and ISA resources durable.
"""
from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from typing import Any, Optional

from qiskit import QuantumCircuit, qpy, transpile

from research.paper_a.streams import TRANSPILER_SEED

FROZEN_BASIS = ["rz", "sx", "x", "cx", "measure"]
OPTIMIZATION_LEVEL = 1


def _qpy_sha256(circuit: QuantumCircuit) -> str:
    # The circuit name is deliberately excluded from circuit identity here:
    # Qiskit's auto-generated default name ("circuit-<n>") embeds a
    # process-global counter, not circuit content, so leaving it in would
    # make hashes non-reproducible across processes/runs. As a consequence,
    # two structurally identical circuits with different custom names will
    # also hash identically.
    normalized = circuit.copy()
    normalized.name = "circuit"
    buffer = io.BytesIO()
    qpy.dump(normalized, buffer)
    return hashlib.sha256(buffer.getvalue()).hexdigest()


def transpile_frozen(circuit: QuantumCircuit) -> tuple[QuantumCircuit, str]:
    """Transpile once against the frozen controlled-simulator target."""
    isa = transpile(
        circuit,
        basis_gates=FROZEN_BASIS,
        coupling_map=None,           # all-to-all
        optimization_level=OPTIMIZATION_LEVEL,
        seed_transpiler=TRANSPILER_SEED,
    )
    return isa, _qpy_sha256(isa)


@dataclass
class Invocation:
    ordinal: int
    requested_shots: int
    logical_qpy_sha256: str
    isa_qpy_sha256: str
    isa_depth: int
    isa_ops: dict
    effective_shots: Optional[int] = None
    status: str = "planned"
    exception: Optional[str] = None


class RecordingSampler:
    """Wraps a sampler primitive, recording every invocation in order.

    IQAE calls `.run([circuit])` with no shot argument, so shots are fixed on
    this instance and echoed into the recorded invocation.
    """

    def __init__(self, inner: Any, shots: int) -> None:
        self._inner = inner
        self._shots = shots
        self.invocations: list[Invocation] = []

    def run(self, circuits, **kwargs):
        circuit = circuits[0]
        isa, isa_hash = transpile_frozen(circuit)
        record = Invocation(
            ordinal=len(self.invocations),
            requested_shots=self._shots,
            logical_qpy_sha256=_qpy_sha256(circuit),
            isa_qpy_sha256=isa_hash,
            isa_depth=isa.depth(),
            isa_ops=dict(isa.count_ops()),
            status="running",
        )
        self.invocations.append(record)   # durable BEFORE execution

        try:
            job = self._inner.run([isa], shots=self._shots, **kwargs)
            result = job.result()
        except Exception as exc:
            record.status = "failed"
            record.exception = f"{type(exc).__name__}: {exc}"
            raise

        metadata = result.metadata[0]
        if "shots" not in metadata:
            record.status = "failed"
            record.exception = (
                "primitive result metadata has no 'shots' key; "
                "effective shots cannot be established"
            )
            raise KeyError(record.exception)

        record.effective_shots = int(metadata["shots"])
        record.status = "complete"
        return job
