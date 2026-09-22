import math
import numpy as np
from research.journal_sprint.reversible_fixed_point import Program,basis,read
from .reversible import clean_sqrt,constant_product,step_program,clifford_t_resources


def test_sqrt_all_inputs_and_clean_scratch():
    for w,f in [(4,0),(5,2),(6,3)]:
        p=Program(compact=True);x=p.register(w);o=p.register(w);clean_sqrt(p,x,o,f)
        for v in range(2**(w-1)):
            initial=basis(x,v);state=p.run(initial)
            expected=math.isqrt(v*2**f)
            assert read(state,o)==expected
            assert state==initial|basis(o,expected)


def test_constant_product_exact_signed_and_cleanup():
    w=5;f=2
    for c in [-11,-1,0,3,12]:
        p=Program(compact=True);x=p.register(w);o=p.register(w)
        constant_product(p,x,o,c,f)
        for v in range(-16,16):
            state=p.run(basis(x,v));expected=(v*c//2**f)%2**w
            assert state==basis(x,v)|basis(o,expected)


def test_step_inverse_cleans_all_wires():
    p,ins,outs=step_program(9,5,1/12)
    initial=0
    for reg,v in zip(ins,[0,3,2,-1]):initial|=basis(reg,v)
    state=p.run(initial)
    mask=sum(1<<z for reg in ins+outs for z in reg)
    assert state & ~mask == 0
    end=len(p.gates);p.undo(0,end)
    assert p.run(initial)==initial


def test_toffoli_decomposition_matches_unitary_and_ledger():
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Operator
    p=Program();q=p.register(3);p.gate(*q)
    r=clifford_t_resources(p);assert r['t_count']==7
    c=QuantumCircuit(3)
    c.h(2);c.cx(1,2);c.tdg(2);c.cx(0,2);c.t(2);c.cx(1,2);c.tdg(2);c.cx(0,2)
    c.t(1);c.t(2);c.h(2);c.cx(0,1);c.t(0);c.tdg(1);c.cx(0,1)
    ideal=QuantumCircuit(3);ideal.ccx(0,1,2)
    np.testing.assert_allclose(Operator(c).data,Operator(ideal).data,atol=1e-14)
