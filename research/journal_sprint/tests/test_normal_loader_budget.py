from decimal import Decimal
import pytest
from research.journal_sprint.normal_loader_budget import loader_plan, circuit, sine_cosine


@pytest.mark.parametrize("value", [0, .001, .2, 1, 1.57, 2])
def test_trig_directed_against_mpmath(value):
    import mpmath as mp
    sine, cosine = sine_cosine(value)
    with mp.workdps(120):
        x = mp.mpf(float(value))
        for interval, actual in ((sine, mp.sin(x)), (cosine, mp.cos(x))):
            assert mp.mpf(str(interval.lo)) <= actual <= mp.mpf(str(interval.hi))


@pytest.mark.parametrize("bits", [1, 2, 3, 4])
def test_loader_actual_statevector_and_inverse(bits):
    import numpy as np
    from scipy.special import ndtr
    from qiskit.quantum_info import Statevector
    plan = loader_plan(bits)
    loader = circuit(plan)
    state = Statevector.from_instruction(loader)
    edges = np.linspace(-4, 4, (1 << bits)+1)
    weights = np.diff(ndtr(edges))/(ndtr(4)-ndtr(-4))
    # Floating simulator comparison is a sanity check, not the certificate.
    assert np.max(abs(abs(state.data)**2-weights)) < 2e-14
    assert abs(state.evolve(loader.inverse()).data[0]) == pytest.approx(1)
    assert Decimal(plan["operator_error_upper"]) < Decimal("1e-12")


def test_loader_plan_rejects_unsupported_inputs():
    for bits in (0, True, 13):
        with pytest.raises(ValueError):
            loader_plan(bits)
    with pytest.raises(ValueError):
        sine_cosine(-.1)
