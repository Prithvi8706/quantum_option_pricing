"""Annex I: ordered append-only sampler recording and frozen transpilation.

Every primitive call is recorded BEFORE execution so that an exception still
leaves the invocation's logical and ISA resources in the in-memory ledger.
The caller is responsible for persisting that ledger.
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
        coupling_map=None,  # all-to-all
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
        circuits = [circuits] if isinstance(circuits, QuantumCircuit) else list(circuits)
        if not circuits:
            raise ValueError("circuit batch must not be empty")
        if "shots" in kwargs:
            raise ValueError("shots are fixed on RecordingSampler")
        batch, records = [], []
        for circuit in circuits:
            isa, isa_hash = transpile_frozen(circuit)
            batch.append(isa)
            records.append(
                Invocation(
                    ordinal=len(self.invocations) + len(records),
                    requested_shots=self._shots,
                    logical_qpy_sha256=_qpy_sha256(circuit),
                    isa_qpy_sha256=isa_hash,
                    isa_depth=isa.depth(),
                    isa_ops=dict(isa.count_ops()),
                    status="running",
                )
            )
        self.invocations.extend(records)  # record the entire batch before submission
        try:
            job = self._inner.run(batch, shots=self._shots, **kwargs)
            result = job.result()
            if len(result.metadata) != len(records):
                raise ValueError("sampler metadata length does not match circuit batch")
            for record, metadata in zip(records, result.metadata):
                if "shots" not in metadata:
                    raise KeyError("primitive result metadata has no 'shots' key")
                value = metadata["shots"]
                if isinstance(value, bool) or int(value) != value or value <= 0:
                    raise ValueError("invalid effective shots in primitive metadata")
                record.effective_shots = int(value)
                record.status = "complete"
        except Exception as exc:
            for record in records:
                if record.status != "complete":
                    record.status = "failed"
                    record.exception = f"{type(exc).__name__}: {exc}"
            raise
        return job
