"""Independent bounded identities and deterministic loader compilation.

Not author-code reproduction, a hardware experiment, or an advantage claim.
"""
import math
from fractions import Fraction
import numpy as np
from scipy.special import ndtr


def normal_probabilities(q, cutoff=4):
    if type(q) is not int or not 1 <= q <= 12:
        raise ValueError('q must be 1..12')
    p = np.diff(ndtr(np.linspace(-cutoff, cutoff, (1 << q)+1)))
    return p / p.sum()


def geometric(q, a):
    """Stable finite distribution, including a=0 and negative a."""
    x = a*np.arange(1 << q, dtype=float)
    p = np.exp(x-x.max())
    return p/p.sum()


def geometric_product(q, a):
    p = np.ones(1 << q)
    for bit in range(q):
        # Logistic form avoids overflow in atan(exp(...)).
        t = a*(1 << bit)
        one = np.exp(-np.logaddexp(0, -t))
        zero = np.exp(-np.logaddexp(0, t))
        p *= np.where((np.arange(1 << q) >> bit) & 1, one, zero)
    return p


def walsh_branch(f, epsilon, omit_mean=False):
    """Exact analytic success branch of H-controlled-exp-H-P(-pi/2).

    Includes the k-dependent phase, not merely sin(epsilon*f/2).
    """
    f = np.asarray(f, dtype=float)
    g = f-f.mean() if omit_mean else f
    return np.exp(-.5j*epsilon*g)*np.sin(.5*epsilon*g)/np.sqrt(len(f))


def branch_metrics(branch, target):
    p = float(np.vdot(branch, branch).real)
    target = np.asarray(target)/np.linalg.norm(target)
    fidelity = float(abs(np.vdot(target, branch))**2/p) if p else None
    return dict(success_probability=p, fidelity=fidelity,
                expected_attempts=1/p if p else None)


def multiplexer(angles):
    """Known cyclic Gray-code RY synthesis, without hidden angle pruning.

    Walsh coefficients are calculated with exact rationals from stored floats;
    each final rotation is rounded once to binary float.
    """
    from qiskit import QuantumCircuit
    count = len(angles)
    if count < 1 or count & (count-1):
        raise ValueError('power-of-two angle count required')
    level = count.bit_length()-1
    values = [Fraction(float(a)) for a in angles]
    step = 1
    while step < count:
        for start in range(0,count,2*step):
            for j in range(start,start+step):
                a,b = values[j],values[j+step]
                values[j],values[j+step] = a+b,a-b
        step *= 2
    result = QuantumCircuit(level+1)
    for j in range(count):
        gray = j ^ (j >> 1)
        angle = float(values[gray]/count)
        if angle != 0:
            result.ry(angle,0)
        if level:
            nxt = (j+1) % count
            change = gray ^ (nxt ^ (nxt >> 1))
            result.cx(change.bit_length(),0)
    return result


def folded_loader(plan):
    """Group disjoint prefix RYs without changing their stored angles.

    Each layer is a multiplexer, not a postselected loader. Ancilla-free.
    Uses known uniformly controlled rotations; no algorithmic novelty claimed.
    """
    from qiskit import QuantumCircuit
    q = plan['normal_bits']
    if type(q) is not int or not 1 <= q <= 12:
        raise ValueError('unsupported register size')
    nodes = {(n['level'], n['prefix']): n['angle'] for n in plan['nodes']}
    expected = {(l, p) for l in range(q) for p in range(1 << l)}
    if set(nodes) != expected or len(nodes) != len(plan['nodes']):
        raise ValueError('invalid/duplicate tree nodes')
    result = QuantumCircuit(q)
    for level in range(q):
        angles = [nodes[level, p] for p in range(1 << level)]
        if not all(math.isfinite(a) for a in angles):
            raise ValueError('nonfinite angle')
        result.compose(multiplexer(angles), [q-level-1]+list(range(q-level, q)), inplace=True)
    return result


def folded_rounding_bound(plan):
    """Exact rational audit of binary-float decomposition angles.

    Fix each control word, track target-X parity, sum signed RY angles exactly.
    Norm(RY(a)-RY(b)) <= |a-b|/2. Max over blocks, sum over layers.
    No physical synthesis, noise, or libm certificate is implied.
    """
    total = Fraction(0)
    for level in range(plan['normal_bits']):
        angles = [n['angle'] for n in sorted(plan['nodes'], key=lambda n:n['prefix'])
                  if n['level'] == level]
        qc = multiplexer(angles)
        if float(qc.global_phase) != 0:
            raise ValueError('unexpected global phase')
        layer = Fraction(0)
        for prefix, target in enumerate(angles):
            parity, angle = 0, Fraction(0)
            for item in qc.data:
                indices = [qc.find_bit(b).index for b in item.qubits]
                if item.operation.name == 'ry' and indices == [0]:
                    angle += (-1 if parity else 1)*Fraction(float(item.operation.params[0]))
                elif item.operation.name == 'cx' and indices[1] == 0:
                    parity ^= (prefix >> (indices[0]-1)) & 1
                else:
                    raise ValueError('unexpected gate in multiplexer')
            if parity:
                raise ValueError('multiplexer leaves a target X')
            layer = max(layer, abs(angle-Fraction(target))/2)
        total += layer
    return dict(exact_numerator=total.numerator, exact_denominator=total.denominator,
                operator_error_upper=math.nextafter(float(total), math.inf))


def run_identities():
    exp_error = max(float(np.max(abs(geometric(q,a)-geometric_product(q,a))))
                    for q in range(1,9) for a in (-3,-.1,0,.1,3))
    f = np.array([.8, 1.1, 1.3, .9])
    walsh = {str(e): dict(correct=branch_metrics(walsh_branch(f,e),f),
                         missing_mean=branch_metrics(walsh_branch(f,e,True),f))
             for e in (.1,.01,.001)}
    loaders = []
    for q in (2,4,6,8,10):
        p = normal_probabilities(q)
        # Regression's sin(x) branch; exact arcsin repair of that branch.
        old = np.sin(np.sqrt(p))/np.sqrt(len(p))
        repaired = np.sin(np.arcsin(np.sqrt(p/p.max())))/np.sqrt(len(p))
        loaders.append(dict(q=q, small_angle=branch_metrics(old,np.sqrt(p)),
                            exact_scaled=branch_metrics(repaired,np.sqrt(p))))
    return dict(geometric_product_max_absolute_error=exp_error,
                walsh=walsh, postselection=loaders,
                quantum_advantage_established=False)
