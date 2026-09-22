"""Clean digital signed-bin selector: no data-dependent amplitude rotation."""
from research.journal_sprint.reversible_fixed_point import Program,copy,constant,add,less_than


def bin_for_bound(w,fraction_bits,lower,upper,sign):
    """Hadamards on selector wires give probability |Y|/upper inside a bin.

    The returned gate stream excludes those Clifford preparation Hadamards.
    """
    scale=2**fraction_bits
    bound=int(round(upper*scale));low=int(round(lower*scale))
    if bound<=0 or bound&(bound-1) or bound!=upper*scale or low!=lower*scale:
        raise ValueError('bin endpoints must be exactly representable; upper dyadic')
    bits=bound.bit_length()-1
    if bits<1:raise ValueError('selector requires at least one bit')
    return bin_program(w,bits,low,bound,sign)


def bin_program(w,selector_bits,lower,upper,sign):
    p=Program(compact=True);x=p.register(w);sel=p.register(selector_bits);flag=p.register(1)[0]
    n=max(w,selector_bits)
    mag=p.register(n);selector=p.register(n);one=p.register(n);lo=p.register(n);hi=p.register(n)
    diff=p.register(n+1);ext=p.register(n+1);helper=p.register(1)[0]
    checks=p.register(3);work=p.register(2)
    start=len(p.gates)
    copy(p,x,mag[:w]);copy(p,sel,selector[:selector_bits])
    # abs(x) modulo 2^w; zero extension takes place after signed negation.
    for b in mag[:w]:p.gate(x[-1],b)
    p.gate(x[-1],one[0]);add(p,one[:w],mag[:w],helper);p.gate(x[-1],one[0])
    constant(p,lo,lower);less_than(p,mag,lo,checks[0],diff,ext,helper);p.gate(checks[0])
    if upper>=2**n:p.gate(checks[1])
    else:
        constant(p,hi,upper);less_than(p,mag,hi,checks[1],diff,ext,helper)
    less_than(p,selector,mag,checks[2],diff,ext,helper)
    if sign>0:p.gate(x[-1])
    # Four controls, two clean work bits, exact Toffoli chain.
    p.gate(x[-1],checks[0],work[0]);p.gate(work[0],checks[1],work[1])
    p.gate(work[1],checks[2],flag)
    p.gate(work[0],checks[1],work[1]);p.gate(x[-1],checks[0],work[0])
    if sign>0:p.gate(x[-1])
    # Exclude the five-gate flag chain and sign toggles from the inverse.
    chain_end=len(p.gates);chain_length=7 if sign>0 else 5
    p.undo(start,chain_end-chain_length)
    return p,(x,sel),(flag,)
