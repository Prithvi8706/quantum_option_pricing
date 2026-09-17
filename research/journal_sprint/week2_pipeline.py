"""Standby encoding integration; logical certificates are not hardware certificates."""
import math
from qiskit import QuantumCircuit
from .decimal_enclosure import Interval as I, pi_interval
from .encoding_enclosure import upward_float
from .reflection_centered_signal import phase_on_word, mux_rounding
from .factorized_signal import projected_phase
from .four_paper_probes import folded_loader
from .normal_loader_budget import loader_plan
from .control_offset_enclosure import control_enclosure


def up(x):
    return upward_float(I.coerce(x).hi)


def loader(q):
    plan = loader_plan(q,4)
    rounding = I(0)
    for level in range(q):
        angles = [n['angle'] for n in plan['nodes'] if n['level']==level]
        rounding += mux_rounding(angles)
    return folded_loader(plan), I(plan['operator_error_upper'])+rounding


def phase_error(qc, phi):
    # The projected_phase setter wraps -phi modulo the stored binary 2*pi.
    actual = float(qc.global_phase)
    turns = round((actual+phi)/(2*math.pi))
    return (I(actual)+I(phi)-2*turns*pi_interval()).absolute()


def walk(plan, signal, phases):
    """Atomic gate boundaries avoid accumulating QSP globals in binary floats."""
    result = QuantumCircuit(plan.num_qubits)
    reflection = QuantumCircuit(plan.num_qubits)
    phase_on_word(reflection,list(plan.good_qubits),0)
    reflection.global_phase = math.pi
    reflection_error = (I(float(reflection.global_phase))-pi_interval()).absolute()
    error = I(0)
    for index, phi in enumerate(phases):
        if index:
            result.append(signal.to_gate(),range(plan.num_qubits))
            result.append(reflection.to_gate(),range(plan.num_qubits))
            error += reflection_error
        phase = projected_phase(plan.num_qubits,plan.good_qubits,float(phi))
        result.append(phase.to_gate(),range(plan.num_qubits))
        error += phase_error(phase,float(phi))
    return result,error


def readout(plan, unitary, marginal_loader):
    result = QuantumCircuit(plan.num_qubits+1)
    for j in range(plan.d):
        result.append(marginal_loader.to_gate(),range(j*plan.q,(j+1)*plan.q))
    test = plan.num_qubits
    result.h(test)
    result.append(unitary.to_gate().control(),[test]+list(range(test)))
    result.h(test)
    return result


def ae_schedule(beta, deterministic, tolerance=1., alpha=.05, cap=10_000_000):
    """Canonical AE worst-case theorem, independent median failure<=alpha.

    Exact ideal controlled powers/QFT assumed; native execution is not admitted.
    Counts include A and A inverse inside every Grover query.
    """
    if not all(math.isfinite(v) for v in (beta,deterministic,tolerance,alpha)):
        raise ValueError('finite inputs required')
    if beta<=0 or deterministic<0 or tolerance<=0 or not 0<alpha<1:
        raise ValueError('invalid schedule inputs')
    allowance = I(tolerance)-I(deterministic)
    if allowance.lo<=0:
        return dict(status='deterministic_budget_exhausted',M=None,a_calls=None)
    M = 2
    while (2*I(beta)*(pi_interval()/M+pi_interval()**2/(M*M))).hi>allowance.lo:
        M *= 2
        if M>2**40:
            return dict(status='precision_cap',M=None,a_calls=None)
    # p_success >= 8/pi^2 > 0.8; Hoeffding for median of independent trials.
    repetitions = 1
    log_failure = I(1)/I(alpha)
    while (I('0.18')*repetitions).lo < log_failure.ln().hi:
        repetitions += 2
    calls = repetitions*(2*M-1)
    return dict(status='ideal_plan' if calls<=cap else 'query_cap',M=M,
        phase_qubits=M.bit_length()-1,repetitions=repetitions,
        a_calls=calls,grover_calls=repetitions*(M-1),
        statistical_dollar_bound=up(2*I(beta)*(pi_interval()/M+pi_interval()**2/(M*M))),
        confidence=1-alpha,hardware_admitted=False)


def budget(contract, plan, record, low, moments, representation, signal_error,
           loader_error, projector_error):
    """Directed deterministic dollar envelope for the abstract logical pipeline."""
    degree = len(record['synthesis']['phases'])-1
    discount = math.exp(-contract.rate*contract.maturity)
    f = I(discount)*I(plan.B)/2
    rho = record['residual']['rho']
    beta = f*I(rho)
    beta_float = float((beta.lo+beta.hi)/2)
    offset_interval = control_enclosure(moments,contract.strike,plan.B,discount,low)['value']
    offset = float((offset_interval.lo+offset_interval.hi)/2)
    # |x_real-x_stored| <= |B_stored-B_real|/B_stored on the good block.
    dx = (I(plan.B)-plan.B_interval).absolute()/I(plan.B)
    derivative = sum((I(float(c)).absolute()*k*k
                      for k,c in enumerate(record['residual']['coefficients'])),I(0))
    parts = dict(
        representation=I(representation['partial_sum']['upper']),
        discount_bridge=((-I(str(contract.rate))*I(str(contract.maturity))).exp()-I(discount)).absolute()*plan.C,
        payoff=f*I(record['candidate']['uniform_error_upper']),
        residual_coefficients=f*I(record['residual']['coefficient_bridge_upper']),
        phase_response=beta*I(record['phase_certificate']['uniform_error_upper']),
        signal=beta*degree*I(signal_error),
        preparation=2*beta*plan.d*I.coerce(loader_error),
        projector=beta*I.coerce(projector_error),
        radius_bridge=beta*derivative*dx,
        offset=(I(offset)-offset_interval).absolute(),
        beta_rounding=(I(beta_float)-beta).absolute(),
        # Binary64 decoding offset+beta*(1-2p), at most four operations,
        # |p|<=1. Conservative gamma bound includes subnormal absolute error.
        decoding_rounding=I(16)*I(2.**-52)*(I(abs(offset))+3*I(abs(beta_float)))+I(2.**-1022))
    total = sum(parts.values(),I(0))
    return dict(degree=degree,offset=offset,beta=beta_float,
        components={k:up(v) for k,v in parts.items()},deterministic_upper=up(total),
        logical_scope='ideal controlled logical gates; exact AE/QFT; not native transpiler or hardware',
        physical_execution_error=None,confirmation_admitted=False,
        schedule=ae_schedule(beta_float,up(total)))


def controlled_zero(n):
    """Controlled zero-state sign with explicitly charged clean workspace."""
    if type(n) is not int or n<2:
        raise ValueError('at least two target wires')
    qc = QuantumCircuit(2*n-1)
    qc.x(list(range(n)))
    qc.h(n-1)
    qc.mcx([n]+list(range(n-1)),n-1,list(range(n+1,2*n-1)),mode='v-chain')
    qc.h(n-1)
    qc.x(list(range(n)))
    return qc


def composition_resources(plan, signal_cost, loader_cost, phases, schedule):
    """Explicit gate-by-gate controlled U/CX composition, not optimized runtime.

    CU uses two CX, CCX six CX; projected gates compiled separately below.
    AE controls A again: each extra control bounded by 6*(all native gates),
    deliberately conservative. No synthesized T counts or hardware timings.
    """
    from .run_minimal_pivot_week1 import cost
    controlled_signal = 6*signal_cost['cx']+2*signal_cost['u']
    projector_cx = 0
    projector_u = 0
    for phi in phases:
        p = projected_phase(plan.num_qubits,plan.good_qubits,float(phi))
        c = cost(p.to_gate().control())
        projector_cx += c['cx']
        projector_u += c['u']
    r = QuantumCircuit(plan.num_qubits)
    phase_on_word(r,list(plan.good_qubits),0)
    r.global_phase = math.pi
    rc = cost(r.to_gate().control())
    degree = len(phases)-1
    # CU decomposition has <=6 single-qubit gates, CCX <=9, plus global phase.
    signal_u_bound = 9*signal_cost['cx']+6*signal_cost['u']+1
    a_cx = plan.d*loader_cost['cx']+degree*(controlled_signal+rc['cx'])+projector_cx
    a_u = plan.d*loader_cost['u']+degree*(signal_u_bound+rc['u'])+projector_u+2
    controlled_a_cx = 6*a_cx+2*a_u
    zero = controlled_zero(plan.num_qubits+1)
    zero_cx = cost(zero)['cx']
    total = None
    if schedule['status']=='ideal_plan':
        M,runs = schedule['M'],schedule['repetitions']
        m = schedule['phase_qubits']
        total = runs*(a_cx+(M-1)*(2*controlled_a_cx+zero_cx+1)+m*(m-1))
    return dict(a_cx_projection=a_cx,controlled_a_cx_projection=controlled_a_cx,
        zero_reflection_cx_projection=zero_cx,total_cx_projection=total,
        projection_scope='conservative gate-by-gate composition with compiled clean-workspace zero reflection; not optimized measured full-circuit cost',
        clean_workspace_qubits=plan.num_qubits-1,
        total_qubits=None if schedule.get('phase_qubits') is None else 2*plan.num_qubits+schedule['phase_qubits'],
        state_preparation_included=True,inverses_included=True,qft_included=True)


def choose(rows):
    eligible = [r for r in rows if r['budget']['schedule']['status']=='ideal_plan'
                and r['resources']['total_cx_projection'] is not None]
    winner = min(eligible,key=lambda r:(r['resources']['total_cx_projection'],r['mode'],r['budget']['degree'])) if eligible else None
    return dict(ideal_choice=None if winner is None else dict(mode=winner['mode'],degree=winner['budget']['degree']),
                production_choice=None,reason='physical execution budget unavailable',
                confirmation_admitted=False)
