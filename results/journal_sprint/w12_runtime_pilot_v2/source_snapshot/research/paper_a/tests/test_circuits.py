import numpy as np
import pytest

from research.paper_a.benchmark import BENCHMARK, by_id
from research.paper_a.european.circuits import (
    build_european, p_circuit, statevector_amplitude,
)
from research.paper_a.payoff import C_RESCALING, a_calc
from research.paper_a.references import (
    grid_points, grid_probabilities, p_grid, support_bounds,
)

Q_TOTAL = 1e-4


def _setup(cid, n):
    c = by_id(cid)
    L, U = support_bounds(c, Q_TOTAL)
    return c, L, U, build_european(c, L, U, n, C_RESCALING)


def test_objective_qubit_is_located_by_identity_not_bit_shifts():
    _, _, _, ec = _setup("E025", 3)
    assert ec.objective_qubit == 3
    assert ec.circuit.num_qubits == 7


def test_circuit_pmf_matches_independently_calculated_probabilities():
    """Max elementwise <= 1e-12 and L1 <= 1e-10 (E0 gate)."""
    c, L, U, ec = _setup("E025", 3)
    from qiskit.quantum_info import Statevector
    probs = Statevector(ec.circuit).probabilities(range(ec.n))
    pi = grid_probabilities(c, L, U, ec.n)
    assert np.abs(probs - pi).max() <= 1e-12
    assert np.abs(probs - pi).sum() <= 1e-10


def test_calculated_and_statevector_objective_probabilities_agree():
    """|a_calc - a_sv| <= 1e-10 (E0 gate). This is the check that catches
    slope/image unit errors in the amplitude function."""
    for cid in ("E001", "E022", "E025", "E042", "E050"):
        c, L, U, ec = _setup(cid, 3)
        expected = a_calc(grid_probabilities(c, L, U, 3),
                          grid_points(L, U, 3), c.K, U, C_RESCALING)
        assert abs(statevector_amplitude(ec) - expected) <= 1e-10, cid


def test_agreement_holds_across_all_qubit_counts():
    c, L, U = by_id("E025"), None, None
    L, U = support_bounds(c, Q_TOTAL)
    for n in (2, 3, 4, 5):
        ec = build_european(c, L, U, n, C_RESCALING)
        expected = a_calc(grid_probabilities(c, L, U, n),
                          grid_points(L, U, n), c.K, U, C_RESCALING)
        assert abs(statevector_amplitude(ec) - expected) <= 1e-10, n


def test_p_circuit_differs_from_p_grid_only_by_encoding_error():
    c, L, U, ec = _setup("E022", 3)
    encode_error = p_circuit(c, ec, C_RESCALING) - p_grid(c, L, U, 3)
    assert abs(encode_error) > 1e-6, "encoding error should be measurable"
    assert abs(encode_error) < 10.0, "encoding error should be bounded"


def test_encoding_error_shrinks_as_rescaling_shrinks():
    """The E1 c-sweep premise: smaller c means a better linearization."""
    c, L, U = by_id("E022"), *support_bounds(by_id("E022"), Q_TOTAL)
    grid = p_grid(c, L, U, 3)
    errs = []
    for cc in (0.5, 0.25, 0.05):
        ec = build_european(c, L, U, 3, cc)
        errs.append(abs(p_circuit(c, ec, cc) - grid))
    assert errs[0] > errs[1] > errs[2]


@pytest.mark.slow
def test_every_benchmark_contract_builds_and_agrees_at_n3():
    for c in BENCHMARK:
        L, U = support_bounds(c, Q_TOTAL)
        ec = build_european(c, L, U, 3, C_RESCALING)
        expected = a_calc(grid_probabilities(c, L, U, 3),
                          grid_points(L, U, 3), c.K, U, C_RESCALING)
        assert abs(statevector_amplitude(ec) - expected) <= 1e-10, c.id
