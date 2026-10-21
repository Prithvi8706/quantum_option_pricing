"""Exactly32 fixed actual native before/dirty-XOR/literal-inverse fixtures."""

import os
from pathlib import Path

import pytest

from research.limitation_program_20261001.two_draw_loader_source_v2 import (
    DIRTY,
    LABELS,
    PAIRS,
    canonical,
    fixture_row,
    read,
    require,
)

FIXTURES = [
    (label, pair, dirty)
    for label in LABELS
    for pair in range(len(PAIRS))
    for dirty in range(len(DIRTY))
]


@pytest.mark.parametrize(
    "label,pair_index,dirty_index",
    FIXTURES,
    ids=[f"{label}-pair{pair}-dirty{dirty}" for label, pair, dirty in FIXTURES],
)
def test_actual_complete_native_loader_and_literal_inverse(label, pair_index, dirty_index):
    # All gate execution has already happened under the one shared producer
    # budget. Each actual fixed lane gets its own full-state fixture identity.
    import numpy as np

    output = Path(os.environ["TWO_DRAW_LOADER_SOURCE"]).resolve()
    root = output.parents[2]
    wrapper = read(output / "wrappers.json")[label]
    target = read(output / "selected_original_targets.json")[label]
    literals = read(
        root / "results/limitation_program_20261001/A02_quantile_scalar_run001/literals.json"
    )
    states = [
        np.load(output / (label + suffix + ".npy"), mmap_mode="r", allow_pickle=False)
        for suffix in ("_before", "_after", "_restored")
    ]
    require(
        all(
            state.dtype == np.dtype("uint64") and state.shape == (wrapper["logical_qubits"],)
            for state in states
        ),
        "Actual complete packed state array ABI",
    )
    actual = fixture_row(wrapper, target, literals, *states, pair_index, dirty_index)
    rows = read(output / "actual_gate_replays.json")["rows"]
    require(len(rows) == 32, "All fixed actual basis records preserved")
    selected = [
        row
        for row in rows
        if (row["loader"], row["pair_index"], row["dirty_index"])
        == (label, pair_index, dirty_index)
    ]
    require(
        len(selected) == 1 and canonical(selected[0]) == canonical(actual),
        "Actual physical gate-state record reconciles independent integer outputs "
        "and every allocated bit",
    )
