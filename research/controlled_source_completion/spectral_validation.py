"""Independent finite-unitary and circuit/QPE checks of the mean-test schedule."""
import json
import math
import numpy as np
from scipy.stats import binom
from research.controlled_source_completion.modern_mean import unitary,spectral_law,exact_qpe_test_probability,plan
from research.controlled_source_completion.run import ROOT,dump


def main():
    rng=np.random.default_rng(2026092602);eps=.02;M=2**15;rows=[]
    for mu in (0.,-.005,.005,-.01,.01,-.02,.02,-.03,.03):
        for j in range(4):
            p=rng.dirichlet(np.ones(8));noise=rng.normal(size=8);noise-=noise@p;noise*=.025/math.sqrt((noise*noise)@p)
            values=noise+mu;rms=math.sqrt((values*values)@p);assert rms<=1/16
            large=exact_qpe_test_probability(values,p,M,1.42*eps)
            success=1-large if abs(mu)<=eps/2 else large
            assert success>=2/3-1e-10,(mu,success)
            rows.append(dict(mean=mu,rms=rms,large_probability=large,success=success))
    # An actual small QPE statevector, independent of the Fejer-distribution code.
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import QFT,UnitaryGate
    from qiskit.quantum_info import Statevector
    b=8;values=np.array([-.027,.041]);p=np.array([.3,.7]);U,start=unitary(values,p)
    qc=QuantumCircuit(b+1);qc.initialize(start,[b]);qc.h(list(range(b)))
    for j in range(b):qc.append(UnitaryGate(np.linalg.matrix_power(U,2**j)).control(),[j,b])
    qc.append(QFT(b,do_swaps=True,inverse=True),range(b))
    observed=Statevector.from_instruction(qc).probabilities(qargs=list(range(b)))
    phases,weights=spectral_law(values,p);grid=2*math.pi*np.arange(2**b)/2**b;expected=np.zeros(2**b)
    for angle,weight in zip(phases,weights):
        delta=(angle-grid+math.pi)%(2*math.pi)-math.pi
        expected+=weight*(np.sinc(2**b*delta/(2*math.pi))/np.sinc(delta/(2*math.pi)))**2
    assert abs(expected.sum()-1)<1e-10
    error=float(np.max(np.abs(observed-expected)));assert error<1e-10
    # Verify the entire planned confidence union bound numerically, not just r.
    allocation=plan(.194480643,.002/math.exp(-.015),.003)
    union=sum(float(binom.sf(s['repetitions']//2,s['repetitions'],1/3)) for s in allocation['stages'])
    assert union<=.003
    # Controlled reflection sign: when ROT=I, |p> must have eigenvalue +1.
    R,start=unitary([0,0],p);assert np.max(np.abs(R@start-start))<1e-12
    out=dict(distribution_cases=rows,min_promised_success=min(r['success'] for r in rows),
             qpe_statevector_qubits=b+1,qpe_distribution_max_error=error,majority_union_failure=union,
             interpretation='Finite-dimensional spectral tests and a small actual QPE statevector; full pricing QPE is too large to simulate and is not reported as executed.')
    dump(ROOT/'validation_v2'/'spectral.json',out);print(json.dumps({k:v for k,v in out.items() if k!='distribution_cases'}),flush=True)


if __name__=='__main__':main()
