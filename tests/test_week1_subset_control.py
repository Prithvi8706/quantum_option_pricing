import numpy as np
import pytest
from qiskit.quantum_info import Operator
from research.journal_sprint.centered_factorized_signal import CenteredFactorizedSignal
from research.journal_sprint.week1_subset_control import circuit


@pytest.mark.parametrize('strike',[.1,.8,10.])
def test_shared_subset_target(strike):
    p = CenteredFactorizedSignal([.1,-.2],[[.3,-.15],[-.2,.25]],strike,1,1.5)
    u = Operator(circuit(p)).data
    n = 1 << p.path_qubits
    values = []
    for word in range(n):
        z = [p.nodes[j,(word >> j)&1] for j in range(p.d)]
        values.append((np.exp(p.means+p.factor@z).mean()-strike)/p.B)
    np.testing.assert_allclose(u[:n,:n],np.diag(values),atol=3e-13)
    np.testing.assert_allclose(u@u,np.eye(len(u)),atol=3e-13)
