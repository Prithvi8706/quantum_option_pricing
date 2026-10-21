import os
import sys

import numpy as np

from research.frontier_classical_20261001.basis import canonical_factor
from research.frontier_classical_20261001.scrambles import Case, eigh_factor, run_scramble

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "advantage_frontier_20260923"))
import barrier_fast_classical as p3  # noqa: E402


def test_eigh_port_reproduces_p3_prefixes():
    old = p3.scramble_run((4, 12, 0))["prefix"]
    new = run_scramble((Case(0, 4, 12), "eigh", (p3.ROOT_SEED, 48, 0), 13))
    for m in (8, 10, 12, 13):
        got = new["prefix"][5, new["ms"].index(m)]
        assert abs(got - old[m]) <= 1e-12 * abs(old[m]), m


def test_eigh_factor_equals_p3_setup():
    assert np.array_equal(eigh_factor(Case(0, 4, 12)), p3.setup(4, 12)[0])


def test_canonical_and_rotation_tasks_run():
    for basis in ("canonical", ("rotation", 1), "archived"):
        r = run_scramble((Case(0, 4, 12), basis, (2026100111, 0, 0, 0, 0), 7))
        assert r["prefix"].shape == (6, 2) and np.isfinite(r["prefix"]).all()
    L, _ = canonical_factor(4, 12, 0.3, 0.4, 1.0)
    assert L.shape == (48, 48)
