"""Bounded independent assessment checks; see PROTOCOL.md before execution.

No project module imports, no frozen-file changes, no circuit execution.
"""

from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_EVEN
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from math import comb
from pathlib import Path
import platform
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
OUTPUT = HERE / "independent_checks.json"
Q = 1 << 24
DOWN = Context(prec=110, rounding=ROUND_FLOOR)
UP = Context(prec=110, rounding=ROUND_CEILING)
NEAR = Context(prec=110, rounding=ROUND_HALF_EVEN)
INPUTS = {}


def read(relative):
    path = ROOT / relative
    raw = path.read_bytes()
    INPUTS[relative] = hashlib.sha256(raw).hexdigest()
    return json.loads(raw)


def demand(test, message):
    if not test:
        raise AssertionError(message)


def display(value):
    value = F(value)
    return str(NEAR.divide(Decimal(value.numerator), Decimal(value.denominator)))


def atan_bounds(n, terms):
    total = sum((F((-1)**j, (2*j+1)*n**(2*j+1)) for j in range(terms)), F(0))
    following = total + F((-1)**terms, (2*terms+1)*n**(2*terms+1))
    return min(total, following), max(total, following)


P, T = atan_bounds(5, 120), atan_bounds(239, 40)
PI = 16*P[0]-4*T[1], 16*P[1]-4*T[0]


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def sub(a, b):
    return a[0]-b[1], a[1]-b[0]


def mul(a, b):
    values = [x*y for x in a for y in b]
    return min(values), max(values)


def singleton(value):
    value = F(value)
    return value, value


def exp_bound(value):
    value = F(value)
    args = (
        DOWN.divide(Decimal(value.numerator), Decimal(value.denominator)),
        UP.divide(Decimal(value.numerator), Decimal(value.denominator)),
    )
    return F(NEAR.next_minus(NEAR.exp(args[0]))), F(NEAR.next_plus(NEAR.exp(args[1])))


def magnitude(interval):
    return max(abs(interval[0]), abs(interval[1]))


def positive(interval):
    return max(F(0), interval[0]), max(F(0), interval[1])


def coefficients(binding):
    c = list(map(F, binding["low"]))
    return ((c[0]-c[2]+c[4])/2, (1+c[1]-3*c[3])/2,
            c[2]-4*c[4], 2*c[3], 4*c[4])


def check_record(name, record):
    cert, budget = record["certificate"], record["budget"]
    parent = cert["parent_plan"]
    d, B = cert["dimension"], F(cert["binding"]["radius"])
    g = coefficients(cert["binding"])
    demand(list(map(F, cert["polynomial"]["monomial_rationals"])) == list(g), name+": monomial")
    cs = [v.numerator//v.denominator for v in (Q*x for x in g)]
    k = (F(Q)/(d*B)).numerator//(F(Q)/(d*B)).denominator
    S = (Q*d*B).numerator//(Q*d*B).denominator
    demand(cert["control_coefficients"] == cs, name+": coefficients")
    demand(cert["reciprocal_integer"] == k and cert["control_scale_integer"] == S, name+": constants")
    c = list(map(F, cert["binding"]["low"]))
    exact_c = ((2/PI[1], 2/PI[0]), (F(0), F(0)),
               (4/(3*PI[1]), 4/(3*PI[0])), (F(0), F(0)),
               (-4/(15*PI[0]), -4/(15*PI[1])))
    eta = sum(max(abs(a-b[0]), abs(a-b[1])) for a, b in zip(c, exact_c))
    rho = 1/(5*PI[0])+eta/2
    demand(rho <= F(cert["polynomial"]["residual_normalized_upper"]), name+": rho")
    E = F(parent["exp_budget"]["total_error_upper"])
    dx = E/B+d*(B+E)*abs(F(k,Q)-1/(d*B))+F(1,Q)
    R = 1+dx
    h = abs(g[-1]-F(cs[-1],Q))
    for j in (3,2,1,0):
        h = R*h+F(1,Q)+abs(g[j]-F(cs[j],Q))
    derivative = sum(j*abs(g[j])*R**(j-1) for j in range(1,5))
    poly_bound = sum(abs(v)*R**j for j,v in enumerate(g))
    scale_error = abs(F(S,Q)-d*B)
    EC = d*B*(derivative*dx+h)+scale_error*(poly_bound+h)+F(1,Q)
    ER = d*E+EC
    for key, expression in (("normalization_error_upper",dx), ("horner_error_upper",h),
                            ("scale_error_upper",scale_error), ("control_sum_error_upper",EC),
                            ("residual_sum_error_upper",ER)):
        demand(expression <= F(cert[key]), name+": "+key)
    J = (Q*(d*B*rho+ER)).numerator//(Q*(d*B*rho+ER)).denominator
    H, m = cert["shift_integer"], cert["selector_bits"]
    demand(H == 1 << J.bit_length() and 2*H == 1 << m, name+": strict shift")
    demand(J < H and m < 48, name+": shift range")
    lo, hi = cert["residual_integer_bounds"]
    tlo, thi = cert["threshold_integer_bounds"]
    demand(-J <= lo <= hi <= J and (tlo,thi) == (lo+H,hi+H), name+": residual range")
    demand(0 < tlo <= thi < 1 << m, name+": selector")
    for stage in cert["integer_stages"]:
        low, high = stage["integer_bounds"]
        limit = 1 << (stage["width"]-1)
        demand(-limit <= low <= high < limit, name+": "+stage['operation'])
    discount = F(parent["discount_lower"]), F(parent["discount_upper"])
    arithmetic = discount[1]*ER/d
    demand(arithmetic <= F(cert["arithmetic_price_error_upper"]), name+": arithmetic")
    old_discount = F(cert["offset_certificate"]["discount"])
    bridge = max(abs(v-old_discount) for v in discount)*B*sum(map(abs,g))
    demand(bridge <= F(cert["offset_bridge_upper"]), name+": offset discount")
    slope = tuple(v*F(1 << m,d*Q) for v in discount)
    offset = F(cert["offset_certificate"]["offset"])
    intercept = offset-discount[1]*F(H,d*Q), offset-discount[0]*F(H,d*Q)
    sf, af = F(cert["decoder_scale"]), F(cert["decoder_intercept"])
    constant_error = max(abs(sf-v) for v in slope)+max(abs(af-v) for v in intercept)
    decode_error = constant_error+8*F(1,1 << 52)*(abs(sf)+abs(af))+F(1,1 << 1022)
    demand(decode_error <= F(cert["decoding_error_upper"]), name+": decoder")
    L = F(cert["sensitivity_upper"])
    demand(L >= slope[1], name+": sensitivity")
    total = F(budget["deterministic_upper"])
    demand(sum(map(F,budget["components"].values())) <= total, name+": dollar total")
    demand(F(budget["beta_upper_rational"]) == L/2, name+": beta")
    schedule = budget["schedule"]
    M = schedule["M"]
    statistical = L*(PI[1]/M+PI[1]**2/M**2)
    demand(statistical <= F(schedule["statistical_upper_rational"]), name+": statistical")
    demand(total+statistical <= 1 and M&(M-1) == 0, name+": feasible")
    demand(total+L*(PI[0]/(M//2)+PI[0]**2/(M//2)**2) > 1, name+": minimal M")
    demand(schedule["a_calls"] == 17*(2*M-1) <= 10000000, name+": calls")
    margin = F(schedule["fixed_schedule_margin_rational"])
    demand(margin <= 1-total-statistical, name+": recorded margin")
    conversion = L*F(1,1 << 53)
    demand(conversion < margin, name+": AE float allowance")
    return dict(name=name, M=M, sensitivity_upper=display(L),
                deterministic_upper=display(total),
                recorded_schedule_margin=display(margin),
                correctly_rounded_label_allowance=display(conversion),
                allowance_to_margin_ratio=display(conversion/margin),
                residual_at_zero_normalized=str(-g[0]),
                residual_at_one_normalized=str(1-sum(g)))


def integer_reference(indices, cert):
    parent = cert["parent_plan"]
    q, d = parent["normal_bits"], cert["dimension"]
    packed = sum(v << (q*j) for j,v in enumerate(indices))
    values = []
    for intercept, cs in parent["affine_rows"]:
        x = intercept+sum(((packed >> j)&1)*c for j,c in enumerate(cs))
        x //= 1 << parent["reductions"]
        y = parent["exp_budget"]["coefficients"][-1]
        for c in reversed(parent["exp_budget"]["coefficients"][:-1]):
            y = x*y//Q+c
        for _ in range(parent["reductions"]):
            y = y*y//Q
        values.append(parent["spot"]*y)
    delta = sum(values)-cert["strike_sum"]
    x = delta*cert["reciprocal_integer"]//Q
    y = cert["control_coefficients"][-1]
    for c in reversed(cert["control_coefficients"][:-1]):
        y = x*y//Q+c
    control = y*cert["control_scale_integer"]//Q
    residual = max(delta,0)-control
    return values, residual


def check_nodes(name, record):
    cert = record["certificate"]
    binding = cert["binding"]
    d, B, K = cert["dimension"], F(binding["radius"]), F(binding["strike"])
    means = list(map(F,binding["means"]))
    factors = [list(map(F,row)) for row in binding["factor"]]
    g = coefficients(binding)
    max_spot, max_residual, minimum_threshold, maximum_threshold = F(0), F(0), None, None
    count = 0
    for indices in product((0,1,511,512,1022,1023), repeat=d):
        nodes = [F(-4)+F(4,1024)+F(8*i,1024) for i in indices]
        spots = [exp_bound(mu+sum(a*z for a,z in zip(row,nodes))) for mu,row in zip(means,factors)]
        basket = (sum(s[0] for s in spots)/d, sum(s[1] for s in spots)/d)
        x = mul(sub(basket,singleton(K)),singleton(1/B))
        poly = singleton(g[-1])
        for coefficient in reversed(g[:-1]):
            poly = add(mul(poly,x),singleton(coefficient))
        residual = sub(positive(sub(basket,singleton(K))),mul(singleton(B),poly))
        ints, integer_residual = integer_reference(indices,cert)
        spot_error = max(magnitude(sub(singleton(F(a,Q)),b)) for a,b in zip(ints,spots))
        residual_error = magnitude(sub(singleton(F(integer_residual,Q)),mul(singleton(d),residual)))
        demand(spot_error <= F(cert["parent_plan"]["exp_budget"]["total_error_upper"]), name+": node exp")
        demand(residual_error <= F(cert["residual_sum_error_upper"]), name+": node residual")
        threshold = integer_residual+cert["shift_integer"]
        lo,hi = cert["threshold_integer_bounds"]
        demand(lo <= threshold <= hi, name+": node threshold")
        probability = F(threshold,1 << cert["selector_bits"])
        # Exact affine residual decoder cancels the shift, in per-basket units.
        restored = probability*F(1 << cert["selector_bits"],d*Q)-F(cert["shift_integer"],d*Q)
        demand(restored == F(integer_residual,d*Q), name+": pointwise decode")
        minimum_threshold = threshold if minimum_threshold is None else min(minimum_threshold,threshold)
        maximum_threshold = threshold if maximum_threshold is None else max(maximum_threshold,threshold)
        max_spot, max_residual = max(max_spot,spot_error), max(max_residual,residual_error)
        count += 1
    return dict(name=name, nodes=count, max_spot_error_enclosed=display(max_spot),
                parent_spot_bound=cert["parent_plan"]["exp_budget"]["total_error_upper"],
                max_sum_residual_error_enclosed=display(max_residual),
                sum_residual_bound=cert["residual_sum_error_upper"],
                threshold_min=minimum_threshold, threshold_max=maximum_threshold,
                scope="fixed selected q10 nodes only; no uniform or confirmation inference")


def quantized_duplicates():
    groups = {}
    for case in ("D1","D2"):
        for index in range(1,37):
            name = "%s_%02d" % (case,index)
            row = read("results/journal_sprint/stronger_arithmetic_v1/"+name+".json")
            spec = row["spec"]
            cs = list(row["plan"]["exp_budget"]["coefficients"])
            while len(cs)>1 and cs[-1] == 0:
                cs.pop()
            key = case,spec["fraction_bits"],spec["width"],spec["reductions"],tuple(cs)
            groups.setdefault(key,[]).append(dict(record=name,nominal_degree=spec["degree"]))
    return [dict(case=k[0],fraction_bits=k[1],width=k[2],reductions=k[3],
                 effective_degree=len(k[4])-1,records=values)
            for k,values in groups.items() if len(values)>1]


def main():
    demand(not OUTPUT.exists(), "refusing to overwrite check output")
    start = time.perf_counter()
    records = {}
    for case in ("D1","D2"):
        for index in range(9):
            name = "%s_%02d" % (case,index)
            records[name] = read("results/journal_sprint/signed_residual_arithmetic_v1/"+name+".json")
    inequalities = [check_record(name,record) for name,record in records.items()]
    failure = sum((F(comb(17,k))*F(1,5)**k*F(4,5)**(17-k) for k in range(9,18)),F(0))
    demand(8/PI[1]**2 > F(4,5) and failure < F(1,20), "confidence")
    nodes = [check_nodes(case+"_00",records[case+"_00"]) for case in ("D1","D2")]
    duplicates = quantized_duplicates()
    report = dict(date="2026-09-21",passed=True,python=platform.python_version(),
                  scope="independent rational residual audit and fixed-node diagnostics; not fresh confirmation",
                  certificate_rows_checked=len(inequalities),certificates=inequalities,
                  independent_pi_interval_width=display(PI[1]-PI[0]),
                  majority_failure_upper_rational=str(failure),majority_failure_upper=display(failure),
                  nodes=nodes,node_count=sum(n["nodes"] for n in nodes),
                  nominal_coefficient_duplicate_groups=duplicates,
                  restricted_norm_counterexample=dict(C="1",K="3/4",fixed_t="1",cube_norm="3/4",actual_norm="1/4"),
                  input_sha256=INPUTS,
                  protocol_sha256=hashlib.sha256((HERE/"PROTOCOL.md").read_bytes()).hexdigest(),
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  elapsed_seconds=time.perf_counter()-start)
    with OUTPUT.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(report,stream,indent=2,sort_keys=True)
        stream.write("\n")
    print(json.dumps({k:report[k] for k in ("passed","certificate_rows_checked","node_count","elapsed_seconds")}))


if __name__ == "__main__":
    main()
