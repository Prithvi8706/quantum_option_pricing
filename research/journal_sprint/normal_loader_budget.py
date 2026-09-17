"""Binary-tree product-normal loader, certified in an ideal controlled-RY model.

No hardware synthesis/noise certificate. Float angles are candidate constants;
their error is bounded by directed trig series, not trusted libm accuracy.
"""

import math
from .decimal_enclosure import Interval, normal_cdf


def sine_cosine(x):
    x = Interval.coerce(x)
    if x.lo < 0 or x.hi > 2:
        raise ValueError("trig certificate supports [0,2]")
    values = []
    for odd in (True, False):
        term = x if odd else Interval(1)
        total = Interval(0)
        for k in range(64):
            total += term if k % 2 == 0 else -term
            n = 2*k + (1 if odd else 0)
            term = term*x*x/((n+1)*(n+2))
        # Subsequent terms decrease: absolute first omitted term bounds tail.
        values.append(total + Interval(term.hi.copy_negate(), term.hi))
    return tuple(values)


def loader_plan(normal_bits, cutoff=4):
    if type(normal_bits) is not int or not 1 <= normal_bits <= 12:
        raise ValueError("loader audit supports 1..12 bits per normal")
    l = Interval(cutoff)
    if not 0 < l.lo <= l.hi <= 6:
        raise ValueError("cutoff must lie in (0,6]")
    n = 1 << normal_bits
    cdf = [normal_cdf(-l + 2*l*i/n) for i in range(n+1)]
    nodes, total_error = [], Interval(0)
    for level in range(normal_bits):
        span = n >> level
        for prefix in range(1 << level):
            left, right = prefix*span, (prefix+1)*span
            middle = (left+right)//2
            mass = cdf[right]-cdf[left]
            if mass.lo <= 0:
                raise ArithmeticError("unresolved positive node mass")
            ratio = (cdf[middle]-cdf[left])/mass
            ratio = Interval(max(0, ratio.lo), min(1, ratio.hi))
            angle = 2*math.acos(math.sqrt(float(ratio.lo)))
            sine, cosine = sine_cosine(Interval(angle)/2)
            # For real RY blocks, operator norm difference equals Euclidean
            # difference between their first columns; square interval absolute
            # bounds avoid squaring a sign-straddling interval incorrectly.
            error = ((cosine-ratio.sqrt()).absolute()**2
                     + (sine-(1-ratio).sqrt()).absolute()**2).sqrt()
            total_error += error
            nodes.append(dict(level=level, prefix=prefix, angle=angle,
                              operator_error_upper=str(error.hi)))
    return dict(schema="ideal_normal_loader_v1", normal_bits=normal_bits,
                cutoff=str(l.lo), nodes=nodes,
                operator_error_upper=str(total_error.hi),
                scope="exact logical controlled-RY gates at stored binary angles; no hardware claim")


def circuit(plan):
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import RYGate
    q = plan["normal_bits"]
    result = QuantumCircuit(q)
    for node in plan["nodes"]:
        level, prefix, angle = node["level"], node["prefix"], node["angle"]
        controls = list(reversed(range(q-level, q)))
        zero_controls = [b for i, b in enumerate(controls) if not (prefix >> (level-1-i)) & 1]
        for b in zero_controls:
            result.x(b)
        if controls:
            result.append(RYGate(angle).control(level), controls+[q-level-1])
        else:
            result.ry(angle, q-1)
        for b in zero_controls:
            result.x(b)
    return result
