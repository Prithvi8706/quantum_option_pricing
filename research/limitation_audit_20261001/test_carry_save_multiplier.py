"""Signed oracle comparison, scratch cleanup, inverse and resource tradeoff."""

import random

import pytest

from research.controlled_source_completion.carry_save_multiplier import build_multiplier
from research.controlled_completion_followup.truncated_multiplier import (
    build_multiplier as baseline,
)
from research.controlled_completion_followup.test_truncated_multiplier import check_case
from research.controlled_source_completion.primitives import resources


@pytest.mark.parametrize("width", [1, 2, 3, 4])
def test_every_small_signed_product(width):
    for fraction in range(width + 1):
        p, args, outs = build_multiplier(width, fraction)
        for a in range(1 << width):
            for b in range(1 << width):
                check_case(p, args, outs, width, fraction, a, b, a ^ b)


@pytest.mark.parametrize("width,fraction", [(32, 12), (72, 40), (96, 64)])
def test_real_width_signed_edges_random_and_inverse(width, fraction):
    p, args, outs = build_multiplier(width, fraction)
    rng = random.Random(20261004 + width)
    mask = (1 << width) - 1
    edges = [0, 1, mask, 1 << (width - 1), (1 << (width - 1)) - 1, 1 << fraction]
    pairs = [(a, b) for a in edges for b in edges]
    pairs += [(rng.getrandbits(width), rng.getrandbits(width)) for _ in range(40)]
    for i, (a, b) in enumerate(pairs):
        check_case(p, args, outs, width, fraction, a, b, rng.getrandbits(width), bool(i % 2))


def test_production_resource_tradeoff():
    old, new = resources(baseline(72, 40)[0]), resources(build_multiplier(72, 40)[0])
    assert new["t_count"] < old["t_count"]
    assert new["t_depth"] < old["t_depth"]
    assert new["qubits"] > old["qubits"]
