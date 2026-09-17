"""Directed canonical-AE outcome decoding, without trusting binary libm sin."""
from .decimal_enclosure import Interval as I, pi_interval
from .normal_loader_budget import sine_cosine


def amplitude_interval(label, M):
    if type(M) is not int or M<2 or M & (M-1) or type(label) is not int or not 0<=label<M:
        raise ValueError('integer outcome of a power-of-two canonical AE required')
    folded = min(label,M-label)
    sine,_ = sine_cosine(pi_interval()*folded/M)
    result = sine.absolute()**2
    return I(max(0,result.lo),min(1,result.hi))


def median_price(labels,M,offset,beta):
    if not labels or len(labels)%2==0 or beta<=0:
        raise ValueError('odd nonempty sample and positive price scale required')
    intervals = [amplitude_interval(y,M) for y in labels]
    middle = len(labels)//2
    median = I(sorted(x.lo for x in intervals)[middle],sorted(x.hi for x in intervals)[middle])
    price = I(offset)+I(beta)*(1-2*median)
    value = float((price.lo+price.hi)/2)
    return dict(value=value,enclosure=price.record(),
                rounding_upper=str((I(value)-price).absolute().hi),
                scope='exact canonical outcome labels and exact stored binary offset/beta')
