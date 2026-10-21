"""N1-headline step 1: analytic formula sheet for the idealized clean-call reaction-layer floor.

Independent of W0 (floor_model.py was not read or run). Path: closed-form primitive costs from cited
literature structures, a per-stage critical path, then supply-limited effective depth per Grover iterate.

Primitive conventions (all literature-based; numbers derived here are 'modelled'):
  * AND / Toffoli = 4 T, reaction depth 1 (Jones, PRA 87, 022328 (2013): T-depth-1 Toffoli;
    Gidney, Quantum 2, 74 (2018): temporary logical-AND, 4 T compute, 0 T measurement-based uncompute).
  * Reaction-limited model: one logical layer per layer of T/measurement-dependent operations, Cliffords
    free (Fowler, arXiv:1210.4626 'time-optimal quantum computation').
  * Adder: Kogge-Stone parallel-prefix carry lookahead (Kogge & Stone, IEEE TC C-22 (1973)); quantum CLA
    feasibility Draper-Kutin-Rains-Svore, QIC 6, 351 (2006) [quant-ph/0406142]. depth 1+ceil(log2 n).
  * Multi-operand reduction: Dadda 3:2 tree (Dadda, Alta Frequenza 34 (1965); Wallace, IEEE TEC 13 (1964)),
    one AND per full adder via MAJ(a,b,c)=a^((a^b)&(a^c)) (Cuccaro et al. quant-ph/0410184).
  * QROM coefficient lookup: L-1 Toffolis for L entries (Babbush et al., PRX 8, 041015 (2018)); with free
    width the one-hot decode is an AND tree, depth ceil(log2 s)+1 (assumed).
  * Piecewise polynomial evaluation: Chebyshev interpolation error bound
    M_{d+1} (b-a)^{d+1} / (2^{2d+1} (d+1)!) per segment; Estrin scheme depth ceil(log2(d+1)) FMA levels
    (Haener, Roetteler, Svore arXiv:1805.12445 for piecewise polynomial quantum arithmetic).
  * Amplitude encoding by comparator against a uniform register (Chakrabarti et al., Quantum 5, 463 (2021)).
  * Grover iterate Q = A S0 A^dag S_chi with A = compute (garbage kept): one iterate = one uncompute + one
    compute = one clean call; controlled-Q for QPE controls only the reflections (+1 layer).
Run: .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/headline/floor_sheet.py
"""
import json
import sys
from math import ceil, factorial, log2

ROOT = "C:/Users/prith/quantum_option_pricing/"
OUT = ROOT + "results/plan110_n1/headline/"


def row(d):
    with open(OUT + "rows.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(d, sort_keys=True) + "\n")


def clog2(x):
    return 0 if x <= 1 else ceil(log2(x))


# ---------------- primitives: (reaction depth, Toffolis, output qubits) ----------------
def add(n):
    L = clog2(n)
    t = n + sum(2 * max(n - 2 ** j, 0) for j in range(L))
    return dict(d=1 + L, t=t, o=n + 1)


def cmp_(n):
    return dict(d=1 + clog2(n), t=n + 2 * (n - 1), o=1)


def dadda(r):
    """3:2 stages to reduce r rows to 2 (Dadda heights 2,3,4,6,9,13,...)."""
    h, k = 2, 0
    while h < r:
        h, k = (3 * h) // 2, k + 1
    return k


def mul_trunc(n, g=8, addend=False):
    """Truncated fixed-point n x n -> n bits (+g guard columns); favourable vs full product."""
    pp = n * (n + 1) // 2 + g * n
    rows = n + (1 if addend else 0)
    fa = max(pp + (n if addend else 0) - 2 * (n + g), 0)
    a = add(n + g)
    return dict(d=1 + dadda(rows) + a["d"], t=pp + fa + a["t"], o=n + g)


def cmul(n, final_add=True):
    w = ceil(n / 3)  # canonical-signed-digit weight ~ n/3 (Reitwiesner 1960)
    a = add(n) if final_add else dict(d=0, t=0)
    return dict(d=dadda(w) + a["d"], t=max(w - 2, 0) * n + a["t"], o=n)


def lookup(s, words):
    if s == 0:
        return dict(d=0, t=0, o=0)
    return dict(d=clog2(s) + 1, t=2 ** s - 1, o=2 ** s + words)


def barrel(n, kbits):
    return dict(d=kbits, t=kbits * n, o=n)


def lzc(n):
    L = clog2(n)
    return dict(d=L + 1, t=n * L + n, o=L)


DERIV = {  # max |f^(k)| on the reduced interval; interval length
    "ln_1_2": (lambda k: factorial(k - 1), 1.0),
    "sqrt_1_4": (lambda k: _sqrt_d(k), 3.0),
    "exp2_0_1": (lambda k: 2 * (0.6931471805599453 ** k), 1.0),
    "cos2pi_0_q": (lambda k: (2 * 3.141592653589793) ** k, 0.25),
}


def _sqrt_d(k):
    c = 0.5
    for j in range(1, k):
        c *= abs(0.5 - j)
    return c


def poly(func, n, f):
    """Best (d, s) for |err| <= 2^-(f+1): minimise depth, then Toffolis."""
    Md, length = DERIV[func]
    best = None
    fma = mul_trunc(n, addend=True)
    sq = mul_trunc(n)
    for s in range(0, 13):
        h = length / 2 ** s
        for d in range(1, 30):
            err = Md(d + 1) * h ** (d + 1) / (2 ** (2 * d + 1) * factorial(d + 1))
            if err <= 2.0 ** -(f + 1):
                lv = clog2(d + 1)
                lk = lookup(s, (d + 1) * n)
                depth = lk["d"] + lv * fma["d"]
                tof = lk["t"] + d * fma["t"] + max(lv - 1, 0) * sq["t"]
                outq = lk["o"] + (d + lv) * fma["o"]
                cand = (depth, tof, d, s, outq)
                if best is None or cand[:2] < best[:2]:
                    best = cand
                break
    depth, tof, d, s, outq = best
    return dict(d=depth, t=tof, o=outq, degree=d, segments_log2=s)


def ser(*ps):
    return dict(d=sum(p["d"] for p in ps), t=sum(p["t"] for p in ps), o=sum(p["o"] for p in ps))


def par(*ps):
    return dict(d=max(p["d"] for p in ps), t=sum(p["t"] for p in ps), o=sum(p["o"] for p in ps))


def times(p, k):
    return dict(d=p["d"], t=p["t"] * k, o=p["o"] * k)


# ---------------- per-call oracle ----------------
def oracle(A, D, n=72, f=40, nu=32, nb=46, free_loader=False, free_exp=False):
    N = D * (A + 1)
    P = N // 2
    st = {}
    zero = dict(d=0, t=0, o=0)
    st["1_uniform_prep"] = dict(d=0, t=0, o=N * nu, note="Hadamards on N*nu qubits; Clifford")
    if free_loader:
        st["2_box_muller"] = dict(zero, o=N * n, note="free loader (departure)")
    else:
        ln_br = ser(lzc(nu), barrel(n, clog2(nu)), poly("ln_1_2", n, f), add(n))
        sq_br = ser(lzc(n), barrel(n, clog2(n)), poly("sqrt_1_4", n, f), barrel(n, clog2(n) - 1))
        tr = poly("cos2pi_0_q", n, f)
        trig = ser(dict(d=1, t=n, o=n), par(tr, tr), dict(d=1, t=2 * n, o=2 * n))
        pair = ser(par(ser(ln_br, sq_br), trig), par(mul_trunc(n), mul_trunc(n)))
        st["2_box_muller"] = dict(times(pair, P), per_pair_depth_parts=dict(
            ln=ln_br["d"], sqrt=sq_br["d"], trig=trig["d"], final_mul=mul_trunc(n)["d"]),
            poly=dict(ln=poly("ln_1_2", n, f), sqrt=poly("sqrt_1_4", n, f), cos=tr))
    w = ceil(n / 3)
    corr1 = dict(d=dadda(2 * w + 1), t=(2 * w - 1) * n, o=2 * n)  # carry-save output, no final adder
    st["3_correlation"] = times(corr1, A * D)
    pre_t = 0
    for t in range(1, D + 1):
        r = 2 * t + 1
        pre_t += max(r - 2, 0) * n + add(n)["t"]
    st["4a_prefix_logspot"] = dict(d=dadda(2 * D + 1) + add(n)["d"], t=pre_t * A, o=A * D * (n + 1))
    clip = ser(par(cmp_(n), cmp_(n)), dict(d=1, t=n, o=n))
    st["4b_clip"] = times(clip, A * D)
    if free_exp:
        st["4c_exp"] = dict(zero, o=A * D * n, note="free exponential (departure)")
    else:
        ex = ser(cmul(n), poly("exp2_0_1", n, f), barrel(n, 5))
        st["4c_exp"] = dict(times(ex, A * D), poly=poly("exp2_0_1", n, f))
    pay = dict(d=dadda(A * D + 1) + add(n)["d"], t=(A * D - 1) * n + add(n)["t"], o=n + 1)
    bar1 = ser(dict(d=dadda(A), t=max(A - 2, 0) * n, o=2 * n), add(n), cmp_(n))
    bar = ser(times(bar1, D), dict(d=clog2(D), t=D - 1, o=D - 1))
    st["5_6_basket_barrier_vs_payoff_sum"] = dict(par(pay, bar), payoff_branch=pay["d"], barrier_branch=bar["d"])
    st["7a_flag_mask"] = dict(d=2, t=1 + n, o=1 + n)
    st["7b_encode_cmp"] = dict(cmp_(nb), o=nb + 1)
    C = sum(v["d"] for v in st.values())
    T_tof = sum(v["t"] for v in st.values())
    outq = sum(v["o"] for v in st.values())
    m = N * nu + nb
    refl = dict(d=2 * clog2(m) + 1, t=m)  # S0 AND-tree compute+uncompute, +1 for QPE control
    return dict(A=A, D=D, N=N, n=n, f=f, nu=nu, nb=nb, stages=st, compute_depth=C,
                compute_toffolis=T_tof, persistent_outputs=outq, refl=refl)


OP_DEPTH = 19  # typical op (truncated 72-bit FMA) reaction depth, used to spread a stage's garbage


def iterate(o, W, rate, tl):
    """Grover iterate depth, T count and width under budget W (None = unlimited).

    Per stage: 'keep' its AND garbage until the A^dag pass (4 T per AND, depth d in each pass) or
    'clean' it locally after copy-out (A^dag must recompute it: 8 T per AND, depth d + 2d = 3d).
    A cleaned stage holds transient garbage ~ t_stage / max(1, d_stage // OP_DEPTH) (assumed even
    spread over sequential op levels); if that exceeds the free width, its instances are batched.
    All 2^S keep/clean choices are enumerated and the one minimising D_eff = max(depth, T/(rate*tl))
    is returned (quantum-favourable choice)."""
    st = [v for v in o["stages"].values() if v["t"] > 0]
    R, outs = o["refl"], o["persistent_outputs"]
    best = None
    for mask in range(2 ** len(st)):
        keep = [s for i, s in enumerate(st) if mask >> i & 1]
        clean = [s for i, s in enumerate(st) if not mask >> i & 1]
        kept = sum(s["t"] for s in keep)
        free = None if W is None else W - outs - kept
        if free is not None and free <= 0:
            continue
        depth, T, ok, maxb = R["d"], 4 * R["t"], True, 1
        for s in keep:
            depth += 2 * s["d"]
            T += 4 * s["t"]
        for s in clean:
            trans = s["t"] / max(1, s["d"] // OP_DEPTH)
            b = 1 if free is None else ceil(trans / free)
            maxb = max(maxb, b)
            depth += 3 * s["d"] * b
            T += 8 * s["t"]
        # stages with zero Toffolis still contribute depth twice (none currently)
        depth += sum(2 * v["d"] for v in o["stages"].values() if v["t"] == 0)
        deff = max(depth, T / (rate * tl))
        cand = (deff, T, depth, mask, maxb, kept)
        if best is None or cand[:2] < best[:2]:
            best = cand
    if best is None:
        return dict(model="infeasible: persistent registers alone exceed W (needs output serialisation)",
                    kept_stages=[], depth=None, T=None, max_batching=None, width=outs, D_eff=None,
                    binding=None, rate_needed_T_per_s=None)
    deff, T, depth, mask, maxb, kept = best
    names = [k for k, v in o["stages"].items() if v["t"] > 0]
    kept_names = [nm for i, nm in enumerate(names) if mask >> i & 1]
    allkeep = len(kept_names) == len(names)
    return dict(model="keep all garbage" if allkeep else "hybrid keep/clean",
                kept_stages=kept_names, depth=depth, T=T, max_batching=maxb,
                width=kept + outs if allkeep else (W if W is not None else kept + outs),
                D_eff=deff, binding="supply" if T / (rate * tl) > depth else "reaction",
                rate_needed_T_per_s=T / (depth * tl))


def main():
    out = dict(meta=dict(script="research/plan110_n1/headline/floor_sheet.py", python=sys.version,
                         labels="all modelled from literature structures (cited in script docstring); "
                                "direction: idealized floor = quantum-favourable",
                         t_layer_s=1e-7), cases={})
    for name, A, D in (("B4x12", 4, 12), ("B8x52", 8, 52)):
        cfgs = {"primary_n72": dict(), "free_loader_exp_n72": dict(free_loader=True, free_exp=True),
                "all_free_n48_f32": dict(free_loader=True, free_exp=True, n=48, f=32)}
        out["cases"][name] = {}
        for cname, kw in cfgs.items():
            o = oracle(A, D, **kw)
            res = dict(compute_depth=o["compute_depth"], compute_toffolis=o["compute_toffolis"],
                       compute_T=4 * o["compute_toffolis"], persistent_outputs=o["persistent_outputs"],
                       stages={k: {kk: vv for kk, vv in v.items()} for k, v in o["stages"].items()},
                       refl=o["refl"], by_width={})
            for wname, W in (("W1e6", 10 ** 6), ("W1e7", 10 ** 7), ("W1e8", 10 ** 8), ("unlimited", None)):
                eff = {}
                for rname, Rate in (("1e11", 1e11), ("1e12", 1e12), ("1e13", 1e13)):
                    for tl_name, tl in (("10ns", 1e-8), ("100ns", 1e-7), ("1us", 1e-6), ("10us", 1e-5)):
                        eff[f"{rname}|{tl_name}"] = iterate(o, W, Rate, tl)
                res["by_width"][wname] = eff
            out["cases"][name][cname] = res
            for wname in ("W1e7", "unlimited"):
                for key in ("1e11|100ns", "1e12|100ns", "1e13|100ns"):
                    p = res["by_width"][wname][key]
                    row(dict(ws="headline", step="1_floor", case=name, config=cname, width=wname,
                             supply_tl=key, compute_depth=o["compute_depth"],
                             T_compute_per_call=4 * o["compute_toffolis"], iterate_depth=p["depth"],
                             iterate_T=p["T"], width_model=p["model"], kept=p["kept_stages"],
                             D_eff=p["D_eff"], binding=p["binding"],
                             rate_needed_T_per_s=p["rate_needed_T_per_s"],
                             label="modelled (literature constants)",
                             direction="quantum-favourable (idealized floor)"))
                    print(name, cname, wname, key, "C=", o["compute_depth"],
                          "Tcomp=%.3e" % (4 * o["compute_toffolis"]), p["model"], "depth", p["depth"],
                          "T", p["T"], "Deff", p["D_eff"], p["binding"], "need", p["rate_needed_T_per_s"])
    with open(OUT + "floor_sheet.json", "x", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
