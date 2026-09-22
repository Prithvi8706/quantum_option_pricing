"""Machine-readable gate envelope around the compiled arithmetic subroutines."""
from fractions import Fraction
from pathlib import Path


def inverse_qft(bits):
    ops=[]
    for j in range(len(bits)//2):ops.append(dict(gate='swap',wires=[bits[j],bits[-1-j]]))
    for j in range(len(bits)):
        for k in range(j):ops.append(dict(gate='cp',wires=[bits[k],bits[j]],angle_pi=[-1,2**(j-k)]))
        ops.append(dict(gate='h',wires=[bits[j]]))
    return ops


def controlled_U(source,phase,fused=False):
    w=source['word_width'];pw=phase['word_width'];offset=source['resources']['logical_qubits']
    source_output=source['values']*w;phase_output=offset+phase['values']*pw
    if fused:
        source_output=next(iter(source['outputs'].values()))*w
        phase_output=offset+next(iter(phase['outputs'].values()))*pw
    pinputs={n['params']['name']:offset+n['out'][0]*pw for n in phase['inputs']}
    random=[n['out'][0]*w+j for n in source['inputs'] for j in range(n['params']['bits'])]
    scratch=offset+phase['resources']['logical_qubits'];shift=phase['fraction_bits']-source['fraction_bits']
    assert shift>=0
    def call(which,base,inverse):return dict(gate='call_graph_half' if fused else 'call_clean_hierarchy',manifest=which['path'],base=base,inverse=inverse)
    copies=[dict(gate='cx',wires=[source_output+j,pinputs['Y']+shift+j]) for j in range(w)]
    ops=[call(source,0,False)]+copies+[call(phase,offset,False)]
    for j in range(phase['fraction_bits']+3):
        angle=Fraction((-1 if j==phase['fraction_bits']+2 else 1)*2**max(0,j-phase['fraction_bits']),2**max(0,phase['fraction_bits']-j))
        ops.append(dict(gate='cp',wires=['control',phase_output+j],angle_radians=[angle.numerator,angle.denominator]))
    ops += [call(phase,offset,True)]+list(reversed(copies))+[call(source,0,True)]
    ops += [dict(gate='h',wires=[q]) for q in random]+[dict(gate='x',wires=[q]) for q in random]
    ladder=[dict(gate='ccx',wires=[random[0],random[1],scratch])]
    ladder += [dict(gate='ccx',wires=[scratch+j-2,random[j],scratch+j-1]) for j in range(2,len(random))]
    ops += ladder+[dict(gate='cz',wires=[scratch+len(random)-2,'control'])]+list(reversed(ladder))
    ops += [dict(gate='x',wires=[q]) for q in random]+[dict(gate='h',wires=[q]) for q in random]+[dict(gate='z',wires=['control'])]
    return dict(format='hierarchical-controlled-U-gates-v1',fused_compute_phase_uncompute=fused,operations=ops,random_wires=random,
        phase_classical_input_offsets=dict(left=pinputs['left'],scale_exponent=pinputs['scale_exponent']),
        qpe_register_base=scratch+len(random)-1,
        call_semantics='Bind every arithmetic hierarchy wire to base+local_wire. call_clean_hierarchy executes the full clean schedule. call_graph_half executes only forward_calls, or its inverse; retained SSA values are uncomputed after phase kickback.',
        control_semantics='Replace control by the active QPE register wire; all other wires have explicit integer addresses.',
        angle_semantics='angle_radians is an exact rational; angle_pi is an exact rational multiple of pi. Rotations remain unsynthesized.')


def validate_qft():
    import math
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import QFT
    from qiskit.quantum_info import Operator
    for b in (2,3,4):
        qc=QuantumCircuit(b)
        for op in inverse_qft(list(range(b))):
            wires=op['wires']
            if op['gate']=='h':qc.h(*wires)
            elif op['gate']=='swap':qc.swap(*wires)
            else:qc.cp(math.pi*op['angle_pi'][0]/op['angle_pi'][1],*wires)
        assert np.max(np.abs(Operator(qc).data-Operator(QFT(b,inverse=True,do_swaps=True)).data))<1e-12


if __name__=='__main__':validate_qft();print('Explicit inverse-QFT gate order agrees for 2, 3 and 4 qubits.')
