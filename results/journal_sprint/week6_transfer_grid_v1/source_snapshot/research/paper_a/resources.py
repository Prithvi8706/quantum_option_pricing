"""Executed resource accounting.

Three distinct conventions, never conflated:
  M_A_logical  = sum_j (2k_j + 1)        unweighted A/A-inverse invocations
  M_A_executed = sum_j N_j (2k_j + 1)    shot-weighted
  M_Q_executed = sum_j N_j k_j           Grover applications
"""
from __future__ import annotations

from collections import Counter
from typing import Sequence

from research.paper_a.recording import Invocation


def executed_powers(powers: Sequence[int],
                    invocations: Sequence[Invocation]) -> list[int]:
    """Drop Qiskit's leading sentinel 0 unless an invocation proves it ran.

    IQAE seeds `powers = [0]` before its loop, so len(powers) is normally
    one greater than the number of submitted circuits.
    """
    values = list(powers)
    if len(values) == len(invocations) + 1:
        return values[1:]
    if len(values) == len(invocations):
        return values
    raise ValueError(
        f"cannot reconcile {len(values)} powers with "
        f"{len(invocations)} recorded invocations")


def m_a_logical(powers: Sequence[int]) -> int:
    return sum(2 * k + 1 for k in powers)


def _paired(powers: Sequence[int], shots: Sequence[int]):
    if len(powers) != len(shots):
        raise ValueError(
            f"powers ({len(powers)}) and shots ({len(shots)}) must align")
    return zip(powers, shots)


def m_a_executed(powers: Sequence[int], shots: Sequence[int]) -> int:
    return sum(n * (2 * k + 1) for k, n in _paired(powers, shots))


def m_q_executed(powers: Sequence[int], shots: Sequence[int]) -> int:
    return sum(n * k for k, n in _paired(powers, shots))


def shot_weighted_gates(invocations: Sequence[Invocation]) -> dict[str, int]:
    """Shot-weighted gate burden. Invocations with no effective shots
    contribute nothing but still retain their depth."""
    burden: Counter = Counter()
    for inv in invocations:
        if inv.effective_shots is None:
            continue
        for op, count in inv.isa_ops.items():
            burden[op] += inv.effective_shots * count
    return dict(burden)


def max_executed_depth(invocations: Sequence[Invocation]) -> int:
    """Maximum, never a sum. Failed attempts keep the depth they consumed."""
    return max((inv.isa_depth for inv in invocations), default=0)
