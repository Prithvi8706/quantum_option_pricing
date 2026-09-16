import math
import json

import mpmath as mp
import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.circuit.library import UCRYGate
from qiskit.quantum_info import Statevector
from scipy.special import betaln

from research.journal_sprint.anytime_readout import bernoulli_cs, calibrated_cs
from research.journal_sprint.exact_payoff import exact_components
from research.paper_a.benchmark import by_id
from research.paper_a.references import p_grid
from research.journal_sprint.run_rescue import acquisition


@pytest.mark.parametrize(
    "s,n", [(0, 128), (128, 128), (64, 128), (1, 100000), (50000, 100000), (99999, 100000)]
)
def test_cs_encloses_high_precision(s, n):
    lo, hi = bernoulli_cs(s, n, 0.025)
    with mp.workdps(80):
        constant = mp.log(
            mp.beta(s + mp.mpf(".5"), n - s + mp.mpf(".5")) / mp.beta(mp.mpf(".5"), mp.mpf(".5"))
        )
        threshold = mp.log(40)

        def accept(p):
            return (
                constant - (s * mp.log(p) if s else 0) - ((n - s) * mp.log1p(-p) if n > s else 0)
                <= threshold
            )

        a, b = mp.mpf(0), mp.mpf(s) / n
        for _ in range(100):
            mid = (a + b) / 2
            if mid == 0 or accept(mid):
                b = mid
            else:
                a = mid
        reference_lo = a
        a, b = mp.mpf(s) / n, mp.mpf(1)
        for _ in range(100):
            mid = (a + b) / 2
            if mid == 1 or accept(mid):
                a = mid
            else:
                b = mid
        assert mp.mpf(lo) <= reference_lo
        assert mp.mpf(hi) >= b


@pytest.mark.parametrize("p", [0.001, 0.1, 0.5, 0.9, 0.999])
def test_exact_finite_horizon_crossing(p):
    # Propagate all counts, discarding paths immediately on first CS crossing.
    alive = np.ones(1)
    for n in range(1, 65):
        nxt = np.zeros(n + 1)
        nxt[:-1] += alive * (1 - p)
        nxt[1:] += alive * p
        for s in range(n + 1):
            lo, hi = bernoulli_cs(s, n, 0.05)
            if not lo <= p <= hi:
                nxt[s] = 0
        alive = nxt
    assert 1 - alive.sum() <= 0.05 + 1e-12


def test_mixture_expectation():
    n = 12
    for p in (0.1, 0.5, 0.9):
        expected = sum(
            math.comb(n, s)
            * p**s
            * (1 - p) ** (n - s)
            * math.exp(
                betaln(s + 0.5, n - s + 0.5)
                - betaln(0.5, 0.5)
                - s * math.log(p)
                - (n - s) * math.log1p(-p)
            )
            for s in range(n + 1)
        )
        assert abs(expected - 1) < 1e-12


def test_invalid_and_empty():
    assert bernoulli_cs(0, 0, 0.05) == (0.0, 1.0)
    for args in [(1, 0, 0.05), (True, 1, 0.05), (0, True, 0.05), (0, 1, 0), (0, 10000001, 0.05)]:
        with pytest.raises(ValueError):
            bernoulli_cs(*args)
    with pytest.raises(ValueError):
        calibrated_cs([0, 0], [1, 1], [0, 0], [0, 0], [64, 64])
    assert calibrated_cs([0], [0], [0], [0, 0], [64, 64]).hull == (0.0, 1.0)


def test_acquisition_serialization_and_costs():
    fixture = dict(
        bounds=dict(support=0.0, grid=0.0, encoding=0.0, sensitivity=10.0, offset=0.0),
        amplitude=0.05,
        profiles={"0": {"gates": {"cx": 100}}},
    )
    fixed, sequential = acquisition(by_id("E001"), "exact_table", fixture, 0.0, "cx", 0, 200)
    json.dumps([fixed, sequential], allow_nan=False)
    assert fixed["shots"] == 65536
    assert sequential["shots"] <= fixed["shots"]
    assert sequential["pricing_cx"] == 100 * sequential["shots"]
    assert fixed["synthetic_path"][-1][0] == fixed["shots"]


@pytest.mark.parametrize("name", ["E001", "E014", "E025", "E030", "E038", "E049"])
def test_exact_oracle_grid_and_basis_order(name):
    c = by_id(name)
    qc, b, a, y = exact_components(c, 3)
    assert abs(float(Statevector(qc).probabilities([3])[1]) - a) < 1e-12
    assert abs(b.offset + b.sensitivity * a - p_grid(c, b.lower, b.upper, 3)) < 1e-11
    assert b.encoding == 0
    # Exercise every basis input independently; excludes endianness coincidence.
    for i in range(8):
        trial = QuantumCircuit(4)
        for j in range(3):
            if (i >> j) & 1:
                trial.x(j)
        trial.append(UCRYGate((2 * np.arcsin(np.sqrt(y))).tolist()), [3, 0, 1, 2])
        assert abs(float(Statevector(trial).probabilities([3])[1]) - y[i]) < 1e-12
