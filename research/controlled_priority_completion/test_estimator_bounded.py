"""Basis, inverse, probability and estimator checks for bounded-output QAE."""

from fractions import Fraction
from collections import Counter
import json
import math
from pathlib import Path

import numpy as np
import pytest

from research.antithetic_feasibility.estimator import qae_distribution
from research.controlled_priority_completion.estimator_bounded import (
    bounded_schedule,
    shifted_selector,
)
from research.controlled_priority_completion.estimator_hadamard import exact_tail
from research.journal_sprint.reversible_fixed_point import basis, read


def test_shifted_selector_exhaustive_small_probability():
    p, (value, selector), (flag,) = shifted_selector(6, 2, 4)
    for raw in range(-15, 16):
        count = 0
        for u in range(32):
            initial = basis(value, raw) | basis(selector, u)
            final = p.run(initial)
            expected = u < raw + 16
            assert final == initial ^ (int(expected) << flag)
            count += read(final, (flag,))
        assert Fraction(count, 32) == Fraction(raw + 16, 32)


def test_shifted_selector_production_edges_and_inverse():
    p, (value, selector), (flag,) = shifted_selector()
    rng = np.random.default_rng(2026092802)
    inputs = [-(100 << 40), -1, 0, 1, 100 << 40]
    inputs.extend(map(int, rng.integers(-(100 << 40), 100 << 40, size=15)))
    for raw in inputs:
        threshold = raw + (128 << 40)
        for u in (0, threshold - 1, threshold, threshold + 1, (1 << len(selector)) - 1):
            for flag_initial in (0, 1):
                initial = basis(value, raw) | basis(selector, u) | (flag_initial << flag)
                final = p.run(initial)
                assert final == initial ^ (int(u < threshold) << flag)
                # Applying this clean XOR oracle again is its inverse.
                assert p.run(final) == initial


def test_bounded_schedule_error_and_exact_confidence():
    for tau in (0.5, 1.5):
        error = 0.002 / math.exp(-0.03 * tau)
        result = bounded_schedule(error)
        assert result["M"] == 524288
        assert result["repetitions"] == 15
        assert result["ideal_error_upper"] < error
        p = Fraction(*result["elementary_failure_upper_exact"])
        assert exact_tail(15, p, lower=8) <= Fraction(0.003)


def test_qae_bound_independent_probability_grid():
    for p in (0.0, 1e-6, 0.02, 0.3, 0.5, 0.9, 1.0):
        for M in (16, 64):
            estimates, mass = qae_distribution(p, M)
            error = 2 * math.pi * math.sqrt(p * (1 - p)) / M + math.pi**2 / M**2
            success = mass[np.abs(estimates - p) <= error + 1e-14].sum()
            assert success >= 8 / math.pi**2 - 1e-12


def test_shifted_selector_rejects_invalid_register_contract():
    with pytest.raises(ValueError):
        shifted_selector(10, 5, 3)
    with pytest.raises(ValueError):
        shifted_selector(3, 2, 4)


def test_emitted_wrapper_counts_and_addresses():
    root = Path("results/controlled_priority_completion")
    rows = json.loads((root / "estimator_bounded.json").read_text())
    for row in rows:
        wrapper = json.loads(
            (root / ("estimator_bounded_" + row["model"] + "_wrapper.json")).read_text()
        )
        count = Counter(op["gate"] for op in wrapper["operations"])
        source_calls = [op for op in wrapper["operations"] if op["gate"] == "call_graph_half"]
        assert len(source_calls) == 2
        assert [op["inverse"] for op in source_calls] == [False, True]
        source = json.loads(Path(source_calls[0]["manifest"]).read_text())
        resources = source["resources"]
        assert resources["t_count"] + 7 * count["ccx"] == row["single_iterate_T_count"]
        assert (
            resources["clifford_cx"]
            - source["word_width"]
            + count["cx"]
            + 6 * count["ccx"]
            + count["cz"]
            == row["single_iterate_clifford_CX"]
        )
        assert (
            resources["clifford_h"] + count["h"] + 2 * count["ccx"] + 2 * count["cz"]
            == row["single_iterate_clifford_H"]
        )
        assert count["z"] == 1
        for op in wrapper["operations"]:
            wires = op.get("wires", [])
            assert len(set(wires)) == len(wires)
            assert all(
                wire == "control" or 0 <= wire < wrapper["qpe_register_base"] for wire in wires
            )
