"""Same-payoff reflection centering with a shared SELECT and ideal error bound.

Known probability/reflection and LCU identities; no global novelty claim.
No path-probability preparation, physical synthesis, or advantage claim.
"""
import math
from fractions import Fraction
from .decimal_enclosure import Interval as I
from .encoding_enclosure import upward_float
from .factorized_signal import FactorizedSignal, projected_phase
from .four_paper_probes import multiplexer
from .normal_loader_budget import sine_cosine


def exp_interval(x):
    return I(1) if x.lo == x.hi == 0 else x.exp()


def probability(x):
    if x.hi < 0 or x.lo > 1:
        raise ArithmeticError('invalid probability interval')
    return I(max(0,x.lo), min(1,x.hi))


def angle_for_zero_probability(p):
    p = probability(p)
    angle = 2*math.acos(math.sqrt(float(p.lo)))
    s,c = sine_cosine(I(angle)/2)
    # Exact-real RY operator distance equals first-column distance.
    error = ((c-p.sqrt()).absolute()**2+(s-(1-p).sqrt()).absolute()**2).sqrt()
    return angle,error


def mux_rounding(angles):
    """l1 of coefficient rounding bounds all control blocks, /2 for RY norm."""
    values = [Fraction(float(a)) for a in angles]
    n = len(values)
    step = 1
    while step < n:
        for start in range(0,n,2*step):
            for j in range(start,start+step):
                a,b = values[j],values[j+step]
                values[j],values[j+step] = a+b,a-b
        step *= 2
    total = sum((abs(Fraction(float(v/n))-v/n) for v in values),Fraction(0))/2
    return I(total.numerator)/total.denominator


def prep_tree(weights):
    """Angles against exact interval weights; zero-mass branches use identity."""
    from qiskit import QuantumCircuit
    n = len(weights)
    bits = (n-1).bit_length()
    if n != 1 << bits:
        raise ValueError('power-of-two weight array required')
    qc = QuantumCircuit(bits)
    total_error = I(0)
    levels = []
    for level in range(bits):
        span = n >> level
        angles, errors = [], []
        for prefix in range(1 << level):
            left,right = prefix*span,(prefix+1)*span
            middle = (left+right)//2
            mass = sum(weights[left:right],I(0))
            if mass.hi == 0:
                angle,error = 0.,I(0)
            elif mass.lo <= 0:
                raise ArithmeticError('unresolved preparation mass')
            else:
                angle,error = angle_for_zero_probability(sum(weights[left:middle],I(0))/mass)
            angles.append(angle)
            errors.append(error.hi)
        total_error += I(max(errors))+mux_rounding(angles)
        qc.compose(multiplexer(angles),[bits-level-1]+list(range(bits-level,bits)),inplace=True)
        levels.append(angles)
    return qc,total_error,levels


class ReflectionSignal(FactorizedSignal):
    """Finite-grid real-model block (A-K)/B, without joint-table enumeration.

    Modes reflection/original share the exact same consolidated multiplexers.
    Only original uses the larger B=C+K; reflection uses B=C/2+|C/2-K|.
    B_interval is the mathematical scale; B is an outward binary upper bound.
    """
    def __init__(self, means, factor, strike, q, L, mode='reflection', nodes=None):
        if mode not in ('reflection','original'):
            raise ValueError('invalid mode')
        if type(q) is not int or not 1 <= q <= 10 or not 1 <= len(means) <= 16:
            raise ValueError('bounded study supports d1..16, q1..10')
        super().__init__(means,factor,strike,q,L,nodes)
        self.mode = mode
        self.row_intervals = [exp_interval(I(float(mu))+sum(
            (I(float(b)).absolute()*I(self.L) for b in row),I(0)))/self.d
            for mu,row in zip(self.means,self.factor)]
        self.C = sum(self.row_intervals,I(0))
        if mode == 'reflection':
            self.constant = self.C/2-I(self.strike)
            weights = [c/2 for c in self.row_intervals]
        else:
            self.constant = -I(self.strike)
            weights = list(self.row_intervals)
        if self.constant.lo < 0 < self.constant.hi:
            raise ArithmeticError('constant sign unresolved; refine precision')
        self.negative_constant = self.constant.hi < 0
        weights += [self.constant.absolute()]
        self.weights = weights+[I(0)]*((1 << self.index_bits)-len(weights))
        self.B_interval = sum(self.weights,I(0))
        if self.B_interval.lo <= 0:
            raise ValueError('zero/unresolved signal normalization')
        self.B = upward_float(self.B_interval.hi)

    def metadata(self):
        return dict(mode=self.mode,d=self.d,q=self.q,qubits=self.num_qubits,
                    coefficient_slots=self.d+1,index_bits=self.index_bits,
                    marginal_input_entries=self.d*self.d*(1 << self.q),
                    padded_mux_entries=self.d*(1 << (self.q+self.index_bits)),
                    radius=self.B,radius_interval=self.B_interval.record(),
                    joint_path_table=False,signal_only=True)


def phase_on_word(qc, wires, word):
    """Exact Clifford/Toffoli sign on an index word; no floating pi phase."""
    zeros = [wire for j,wire in enumerate(wires) if not ((word >> j) & 1)]
    if zeros:
        qc.x(zeros)
    if len(wires) == 1:
        qc.z(wires[0])
    else:
        qc.h(wires[-1])
        qc.mcx(wires[:-1],wires[-1])
        qc.h(wires[-1])
    if zeros:
        qc.x(zeros)


def signal_circuit(plan):
    """Returns circuit plus full ideal logical operator-error certificate.

    Certificate compares with exact-real model/cube constants, not hardware.
    Triangle bounds account for PREP twice, multiplexed V twice for reflection,
    or once for the original tensor reflections. All sign reflections exact.
    """
    from qiskit import QuantumCircuit
    if not isinstance(plan,ReflectionSignal):
        raise TypeError('ReflectionSignal required')
    index = list(range(plan.path_qubits+plan.d,plan.num_qubits))
    signals = list(range(plan.path_qubits,plan.path_qubits+plan.d))
    prep,prep_error,_ = prep_tree(plan.weights)
    v = QuantumCircuit(plan.num_qubits)
    v_error = I(0)
    coordinate_errors = []
    for j in range(plan.d):
        angles = []
        max_error = I(0)
        for row in range(1 << plan.index_bits):
            for z in plan.nodes[j]:
                if row >= plan.d:
                    angle,error = 0.,I(0)
                else:
                    b = I(float(plan.factor[row,j]))
                    log_a = b*I(float(z))-b.absolute()*I(plan.L)
                    a = probability(exp_interval(log_a))
                    # Original cos(theta/2)=a; reflection cos(theta/2)=sqrt(a).
                    angle,error = angle_for_zero_probability(a if plan.mode == 'reflection' else a*a)
                angles.append(angle)
                max_error = I(max(max_error.hi,error.hi))
        err = max_error+mux_rounding(angles)
        v_error += err
        coordinate_errors.append(str(err.hi))
        controls = list(range(j*plan.q,(j+1)*plan.q))+index
        v.compose(multiplexer(angles),[signals[j]]+controls,inplace=True)
    qc = QuantumCircuit(plan.num_qubits,name=plan.mode+'_shared_signal')
    qc.compose(prep,index,inplace=True)
    if plan.mode == 'reflection':
        qc.compose(v,inplace=True)
        # 2|0..0><0..0|-I: negative of a phase flip on zero.
        phase_on_word(qc,signals,0)
        qc.global_phase += math.pi
        if plan.negative_constant:
            phase_on_word(qc,index,plan.d)
        qc.compose(v.inverse(),inplace=True)
        total = 2*prep_error+2*v_error
    else:
        qc.z(signals)
        qc.compose(v,inplace=True)
        if plan.negative_constant:
            phase_on_word(qc,index,plan.d)
        total = 2*prep_error+v_error
    qc.compose(prep.inverse(),index,inplace=True)
    # Qiskit represents global pi as a stored binary angle. Its discrepancy
    # from real pi is bounded, including when this circuit becomes controlled.
    if plan.mode == 'reflection':
        from .decimal_enclosure import pi_interval
        total += (I(math.pi)-pi_interval()).absolute()
    certificate = dict(operator_error_upper=str(total.hi),prep_error_upper=str(prep_error.hi),
                       coordinate_error_upper=coordinate_errors,
                       radius_interval=plan.B_interval.record(),
                       scope='exact logical stored-angle RY, X,H,Z,CX,MCX; physical synthesis/noise excluded')
    return qc,certificate


def phased_circuit(plan, signal, phases):
    qc = projected_phase(plan.num_qubits,plan.good_qubits,float(phases[0]))
    for phi in phases[1:]:
        qc.compose(signal,inplace=True)
        qc.compose(projected_phase(plan.num_qubits,plan.good_qubits,math.pi/2),inplace=True)
        qc.global_phase -= math.pi/2
        qc.compose(projected_phase(plan.num_qubits,plan.good_qubits,float(phi)),inplace=True)
    return qc
