"""Independent signed-integer specification and nonzero-output cleanup checks."""

import random

import pytest

from research.controlled_completion_followup.truncated_multiplier import build_multiplier
from research.controlled_source_completion.primitives import basis_run


def check_case(p, args, outs, w, f, a, b, initial, inverse=False):
    mask = (1 << w) - 1

    def signed(x):
        return x - (1 << w) if x & (1 << (w - 1)) else x

    expected = initial ^ (((signed(a) * signed(b)) >> f) & mask)
    observed, clean, preserved, _ = basis_run(p, args, outs, [a, b], [initial], inverse=inverse)
    assert observed == [expected]
    assert clean and preserved


@pytest.mark.parametrize("w", [1, 2, 3, 4])
def test_exhaustive_signed_small(w):
    for f in range(w + 1):
        p, args, outs = build_multiplier(w, f)
        for a in range(1 << w):
            for b in range(1 << w):
                check_case(p, args, outs, w, f, a, b, a ^ b)


@pytest.mark.parametrize("w,f", [(56, 24), (72, 40), (96, 64)])
def test_production_edges_random_and_inverse(w, f):
    p, args, outs = build_multiplier(w, f)
    rng = random.Random(2026092701 + w)
    mask = (1 << w) - 1
    edges = [0, 1, mask, 1 << (w - 1), (1 << (w - 1)) - 1, 1 << f]
    pairs = [(a, b) for a in edges for b in edges]
    pairs += [(rng.getrandbits(w), rng.getrandbits(w)) for _ in range(40)]
    for i, (a, b) in enumerate(pairs):
        check_case(p, args, outs, w, f, a, b, rng.getrandbits(w), bool(i % 2))
