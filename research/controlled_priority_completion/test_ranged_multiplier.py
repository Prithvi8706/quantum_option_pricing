"""Exhaustive asymmetric ranges, sign extension, floor and inverse semantics."""

import random

from research.controlled_priority_completion.ranged_multiplier import build
from research.controlled_source_completion.primitives import basis_run


def test_exhaustive_small_asymmetric_and_slice_above_product():
    w = 5
    for f in range(w + 1):
        for aw, bw in ((1, 1), (1, 3), (2, 3), (3, 2), (3, 4), (5, 5)):
            p, args, outs = build(w, f, aw, bw)
            for a in range(-(1 << (aw - 1)), 1 << (aw - 1)):
                for b in range(-(1 << (bw - 1)), 1 << (bw - 1)):
                    initial = (a ^ b) & 31
                    got, clean, preserved, _ = basis_run(p, args, outs, [a, b], [initial])
                    assert got == [initial ^ (((a * b) >> f) & 31)]
                    assert clean and preserved


def test_production_width_valid_domain_and_inverse():
    rng = random.Random(2026092801)
    w, f = 72, 40
    mask = (1 << w) - 1
    for aw, bw in ((1, 41), (41, 1), (40, 35), (55, 55), (72, 42), (72, 72)):
        p, args, outs = build(w, f, aw, bw)
        edges_a = [-(1 << (aw - 1)), (1 << (aw - 1)) - 1, 0, -1]
        edges_b = [-(1 << (bw - 1)), (1 << (bw - 1)) - 1, 0, -1]
        pairs = [(a, b) for a in edges_a for b in edges_b]
        pairs += [
            (
                rng.randrange(-(1 << (aw - 1)), 1 << (aw - 1)),
                rng.randrange(-(1 << (bw - 1)), 1 << (bw - 1)),
            )
            for _ in range(20)
        ]
        for i, (a, b) in enumerate(pairs):
            initial = rng.getrandbits(w)
            got, clean, preserved, _ = basis_run(
                p, args, outs, [a, b], [initial], inverse=bool(i % 2)
            )
            assert got == [initial ^ (((a * b) >> f) & mask)]
            assert clean and preserved
