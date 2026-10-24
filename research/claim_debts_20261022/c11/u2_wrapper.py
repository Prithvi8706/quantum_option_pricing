"""C11/U2: emit and verify the support-tight selector flag = [sel_b < c*Y] for B8x52 (c = 211, b = 53).

Design: docs/parallel_E11_unblock_20261010/U2_MEAN_AWARE_SCHEDULE.md section 4 (obligation O7). The circuit is the
saved E02 comparator (journal_sprint.reversible_fixed_point.less_than: copy, subtract, CX, undo) with the copy of Y
into the comparator's extended register replaced by an exact shift-add multiply by c (Cuccaro adders). Everything
inside the comparator block is undone, so the selector is clean, as in the saved 46-bit selector.

Outputs (exclusive create): results/claim_debts_20261022/c11/<run>/{u2_selector.npy? no: u2_selector_gates.json,
u2_wrapper.json}.
Run: ../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B research/claim_debts_20261022/c11/u2_wrapper.py run001
"""
import json
import platform
import random
import sys
from fractions import Fraction

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from c11_common import ROOT, progress, read_npy_int32, resources, run_gates, sha, write_new  # noqa: E402

sys.path.insert(0, ROOT)
from research.journal_sprint.reversible_fixed_point import Program, add, copy, less_than, subtract  # noqa: E402

RUN = sys.argv[1] if len(sys.argv) > 1 else "run001"
OUT = ROOT + f"results/claim_debts_20261022/c11/{RUN}/"
E02 = ROOT + "results/limitation_program_20261001/E02_financial_run002/"
IN = dict(
    iterate=E02 + "B8x52/iterate.json",
    selector=E02 + "B8x52/selector.npy",
    cert_B8=ROOT + "results/limitation_program_20261001/E03_support_run001/B8x52_certificate.json",
    audit_B8=ROOT + "results/limitation_program_20261001/E03_support_audit_run002/B8x52_audit.json",
    lib=ROOT + "research/journal_sprint/reversible_fixed_point.py",
)
C, B, YB, W = 211, 53, 46, 72


def rows(p):
    d = p.gates.data
    return [tuple(d[4 * i:4 * i + 4]) for i in range(len(p.gates))]


def make_saved_selector(word_width=72, selector_bits=46):
    """Literal re-statement of native_payoff_estimator_v2.make_selector (stdlib)."""
    p = Program(compact=True)
    value, uniform = p.register(word_width), p.register(selector_bits)
    flag = p.register(1)[0]
    difference, extended, helper = p.register(selector_bits + 1), p.register(selector_bits + 1), p.register(1)[0]
    less_than(p, uniform, value[:selector_bits], flag, difference, extended, helper)
    return p, dict(value=value, uniform=uniform, flag=flag, scratch=difference + extended + (helper,))


def make_u2_selector(word_width, y_bits, c, b):
    """flag XOR= [unsigned(sel_b) < c*unsigned(value[:y_bits])]; clean scratch.

    Requires the support premise c*Y < 2**b (checked by the caller) and value bits >= y_bits zero.
    """
    if not (c >= 1 and b >= y_bits and c * ((1 << y_bits) - 1) >= 0):
        raise ValueError("bad parameters")
    p = Program(compact=True)
    value, uniform = p.register(word_width), p.register(b)
    flag = p.register(1)[0]
    difference, extended, helper = p.register(b + 1), p.register(b + 1), p.register(1)[0]
    shifts = [i for i in range(c.bit_length()) if (c >> i) & 1]
    yext = p.register(b + 1) if len(shifts) > 1 else ()
    if any(b + 1 - i < y_bits for i in shifts):
        raise ValueError("shifted Y would be truncated")
    start = len(p.gates)
    copy(p, uniform, difference[:b])
    i0 = shifts[0]
    copy(p, value[:y_bits], extended[i0:i0 + y_bits])          # first partial product
    if yext:
        copy(p, value[:y_bits], yext[:y_bits])                 # zero-extended Y for the adders
        for i in shifts[1:]:
            add(p, yext[:b + 1 - i], extended[i:], helper)     # extended += Y << i (exact: c*Y < 2**b)
    subtract(p, extended, difference, helper)                  # difference = sel - c*Y (mod 2**(b+1))
    end = len(p.gates)
    p.gate(difference[-1], flag)
    p.undo(start, end)
    return p, dict(value=value, uniform=uniform, flag=flag, scratch=difference + extended + (helper,) + tuple(yext),
                   shifts=shifts)


def basis(reg, v):
    return sum(((v >> i) & 1) << q for i, q in enumerate(reg))


def read(state, reg):
    return sum(((state >> q) & 1) << i for i, q in enumerate(reg))


def check(gates, regs, y, sel, c):
    s0 = basis(regs["value"], y) | basis(regs["uniform"], sel)
    s1 = run_gates(gates, s0)
    flag = (s1 >> regs["flag"]) & 1
    ok_flag = flag == (1 if sel < c * y else 0)
    clean = (s1 & ~(1 << regs["flag"])) == s0
    back = run_gates(gates, s1, inverse=True) == s0
    return ok_flag and clean and back


def exhaustive(word_width, y_bits, c, b):
    p, regs = make_u2_selector(word_width, y_bits, c, b)
    g = rows(p)
    n = 0
    for y in range(1 << y_bits):
        if c * y >= 1 << b:
            continue  # outside the support premise
        for sel in range(1 << b):
            if not check(g, regs, y, sel, c):
                return dict(word_width=word_width, y_bits=y_bits, c=c, b=b, cases=n, passed=False, failing=[y, sel])
            n += 1
    return dict(word_width=word_width, y_bits=y_bits, c=c, b=b, cases=n, passed=True)


# ---------- exact readout: price = S' * sin^2(phi_hat/2), rounded to the 2^-40 dollar grid ----------
def pi_enclosure(terms=90):
    def atan_inv(x, n):
        s, lo_hi = Fraction(0), []
        for k in range(n):
            s += Fraction((-1) ** k, (2 * k + 1) * x ** (2 * k + 1))
            lo_hi.append(s)
        return min(lo_hi[-1], lo_hi[-2]), max(lo_hi[-1], lo_hi[-2])
    a = atan_inv(5, terms); b = atan_inv(239, terms)
    return 16 * a[0] - 4 * b[1], 16 * a[1] - 4 * b[0]


PI_LO, PI_HI = pi_enclosure()


def sin_enclosure(r, terms=40):
    """Enclosure of sin(pi*r) for rational r in [0, 1/2]."""
    if not 0 <= r <= Fraction(1, 2):
        raise ValueError("reduce r first")
    x = (PI_LO + PI_HI) / 2 * r
    s, t = Fraction(0), x
    for k in range(terms):
        s += t
        t = -t * x * x / ((2 * k + 2) * (2 * k + 3))
    rem = abs(t)                                  # alternating series, |terms| decreasing for x <= 2
    lip = (PI_HI - PI_LO) / 2 * r                 # |sin x - sin x'| <= |x - x'|
    return s - rem - lip, s + rem + lip


def readout(j, G, l, K, span=Fraction(8192, 211)):
    """phi_hat = 2*pi*j/G - tau, tau = 2*pi*l/(G*K); a_hat = sin^2(phi_hat/2) = sin^2(pi*r)."""
    r = Fraction(j * K - l, G * K) % 1
    if r > Fraction(1, 2):
        r = 1 - r
    lo, hi = sin_enclosure(r)
    lo = max(lo, Fraction(0))
    a_lo, a_hi = lo * lo, hi * hi
    p_lo, p_hi = span * a_lo, span * a_hi
    q = Fraction(1, 1 << 40)
    mid = (p_lo + p_hi) / 2
    out = Fraction(round(mid / q)) * q            # nearest 2^-40 grid point
    err = max(abs(out - p_lo), abs(out - p_hi))   # bound on |out - S'*a_hat_exact|
    return out, err, p_hi - p_lo


def main():
    progress(dict(step="u2_start", run=RUN))
    it = json.load(open(IN["iterate"], encoding="utf-8"))
    cert = json.load(open(IN["cert_B8"], encoding="utf-8"))
    audit = json.load(open(IN["audit_B8"], encoding="utf-8"))
    sup = it["binding"]["payoff_raw_bounds"][1]
    assert cert["payoff_raw_bounds"] == audit["payoff_raw_bounds"] == it["binding"]["payoff_raw_bounds"]
    assert it["binding"]["payoff_raw_bounds"][0] == 0 and sup < 1 << YB
    support = dict(sup_Yraw=sup, c=C, b=B, c_times_sup=C * sup, two_pow_b=1 << B,
                   holds=C * sup < 1 << B, slack=(1 << B) - C * sup,
                   span_dollars=str(Fraction(1 << (B - 40), C)), span_float=float(Fraction(1 << (B - 40), C)),
                   y_below_2_46=sup < 1 << YB,
                   source="E03 certificate and independent audit payoff_raw_bounds (all-input support), "
                          "equal to the E02 wrapper binding")
    assert support["holds"]

    # 1. IR check: the stdlib restatement of the saved selector equals the saved selector.npy row by row.
    saved = read_npy_int32(IN["selector"])
    ps, regs_s = make_saved_selector()
    ir_equal_saved = rows(ps) == saved
    # c = 1, b = 46 instance of the U2 builder reproduces the saved selector exactly.
    p1, _ = make_u2_selector(W, YB, 1, YB)
    u2_c1_equals_saved = rows(p1) == saved
    progress(dict(step="u2_ir_checks", ir_equal_saved=ir_equal_saved, u2_c1_equals_saved=u2_c1_equals_saved))

    # 2. Exhaustive small-width verification (same builder; 211 itself at small width included).
    small = [exhaustive(6, 4, 3, 6), exhaustive(6, 4, 13, 8), exhaustive(7, 5, 11, 9), exhaustive(5, 3, 211, 11),
             exhaustive(6, 4, 5, 7), exhaustive(5, 3, 1, 3)]
    progress(dict(step="u2_exhaustive", passed=all(s["passed"] for s in small),
                  cases=sum(s["cases"] for s in small)))

    # 3. Full-width production circuit, randomized + edge cases.
    pu, regs = make_u2_selector(W, YB, C, B)
    g = rows(pu)
    rng = random.Random(2026102211)
    ys = [0, 1, 2, sup, sup - 1, sup // 2, (1 << B) // C - 1, (1 << B) // C]
    ys = [y for y in ys if C * y < 1 << B and y <= sup] + [rng.randrange(0, sup + 1) for _ in range(300)]
    full_cases, full_fail = 0, []
    for y in ys:
        sels = {0, 1, (1 << B) - 1, max(C * y - 1, 0), C * y, min(C * y + 1, (1 << B) - 1)}
        sels |= {rng.randrange(0, 1 << B) for _ in range(8)}
        for sel in sels:
            full_cases += 1
            if not check(g, regs, y, sel, C):
                full_fail.append([y, sel])
    # Outside the support (documentation of why the premise is needed): Y = 2^46 - 1.
    y_bad = (1 << YB) - 1
    sel_bad = (C * y_bad) % (1 << B)  # any sel below the true product exposes the wrap
    outside = dict(y=y_bad, c_times_y_ge_2_b=C * y_bad >= 1 << B,
                   flag_correct_at_sel_0=check(g, regs, y_bad, 0, C),
                   note="outside the certified support; the comparator need not be correct there")
    progress(dict(step="u2_full_width", cases=full_cases, failures=len(full_fail)))

    # 4. Resources: stdlib recount (seven-T convention) of forward and inverse, vs the saved selector.
    qb_u2, qb_saved = pu.qubits, ps.qubits
    r_u2 = dict(forward=resources(g, qb_u2), inverse=resources(g, qb_u2, inverse=True))
    r_saved = dict(forward=resources(saved, qb_saved), inverse=resources(saved, qb_saved, inverse=True))
    saved_recorded = it["selector_costs"]
    recount_matches_recorded = all(r_saved[d][k] == saved_recorded[d][k]
                                   for d in ("forward", "inverse") for k in saved_recorded[d])
    delta = {k: r_u2["forward"][k] + r_u2["inverse"][k] - r_saved["forward"][k] - r_saved["inverse"][k]
             for k in ("source_gates", "x", "cx", "ccx", "t_count", "t_depth", "clifford_t_depth", "toffoli_depth")}
    width = dict(u2_selector_qubits=qb_u2, saved_selector_qubits=qb_saved,
                 extra_selector_uniform_bits=B - YB,
                 u2_private_scratch=len(regs["scratch"]), saved_private_scratch=len(regs_s["scratch"]),
                 private_capacity=it["private_capacity"],
                 fits_private_bank=len(regs["scratch"]) <= it["private_capacity"],
                 old_output_buffer_use=B + 2, old_output_buffer_width=W,
                 qpe_controls_left_in_old_buffer=W - B - 2)

    # 5. Readout allowance (exact): price output = S' * sin^2(phi_hat/2) rounded to 2^-40 dollars.
    rr = random.Random(7)
    G, K = 1 << 18, 1 << 12
    worst_err, worst_w = Fraction(0), Fraction(0)
    samples = [(0, 0), (G // 2, 0), (1, K - 1), (G - 1, 1)] + [(rr.randrange(G), rr.randrange(K)) for _ in range(400)]
    for j, l in samples:
        _, err, wdt = readout(j, G, l, K)
        worst_err, worst_w = max(worst_err, err), max(worst_w, wdt)
    bound = Fraction(1, 1 << 41) + worst_w
    readout_rule = dict(
        procedure="exact rational phase r=(jK-l)/(GK); sin(pi r) enclosed with a Machin pi enclosure and a 40-term "
                  "alternating Taylor series with remainder and Lipschitz terms; price = S'*a_hat rounded to the "
                  "nearest 2^-40 dollar. No binary64 libm call.",
        error_bound_statement="|price_out - S'*sin^2(phi_hat/2)| <= 2^-41 + S'*(enclosure width) (the rounding half-step plus "
                              "the enclosure); enclosure width observed <= worst_enclosure_width over the samples",
        samples=len(samples), worst_observed_error=float(worst_err), worst_enclosure_width=float(worst_w),
        allowance_used=float(bound), placeholder_2_pow_m39=2.0 ** -39,
        within_placeholder=bound <= Fraction(1, 1 << 39),
        pi_enclosure_width=float(PI_HI - PI_LO),
        label="mod (exact for the stated procedure; the width bound is checked on samples, the formula holds for every j,l)")

    out = dict(
        schema="c11-u2-support-tight-selector-v1", run=RUN, case="B8x52",
        design="flag = [sel_53 < 211*Yraw]; a' = E[211*Yraw]/2^53 = E[Y_dollars]/S', S' = 8192/211 USD",
        construction=dict(shifts=regs["shifts"], adders=[dict(shift=i, width=B + 1 - i) for i in regs["shifts"][1:]],
                          comparator_width=B + 1, block="copy sel; partial products of 211*Y into the extended "
                          "register (copy + 4 Cuccaro adds); subtract; CX(msb, flag); undo"),
        support=support, ir_equal_saved=ir_equal_saved, u2_c1_equals_saved=u2_c1_equals_saved,
        exhaustive_small=small, full_width=dict(cases=full_cases, failures=full_fail, seed=2026102211),
        outside_support=outside, resources_u2=r_u2, resources_saved_recount=r_saved,
        saved_recount_matches_iterate_json=recount_matches_recorded, delta_selector_pair=delta, width=width,
        readout=readout_rule,
        labels=dict(gate_list="meas (emitted and simulated)", counts="meas (exact counts of the emitted list)",
                    support="cert (E03 certificate + independent audit)",
                    t_convention="exact seven-T CCX, as in the saved E02 costs; no measurement-based uncompute"),
        inputs={k: dict(path=v.replace(ROOT, ""), sha256=sha(v)) for k, v in IN.items()},
        interpreter=platform.python_version(), flags=sys.flags.isolated,
    )
    write_new(OUT + "u2_wrapper.json", out)
    write_new(OUT + "u2_selector_gates.json", dict(qubits=qb_u2, regs={k: (list(v) if isinstance(v, tuple) else v)
                                                                        for k, v in regs.items()}, gates=g))
    ok = (ir_equal_saved and u2_c1_equals_saved and all(s["passed"] for s in small) and not full_fail
          and recount_matches_recorded and readout_rule["within_placeholder"])
    progress(dict(step="u2_done", ok=ok, delta=delta))
    print(json.dumps(dict(ok=ok, delta=delta, support_slack=support["slack"], full=full_cases,
                          small=[(s["c"], s["cases"], s["passed"]) for s in small],
                          readout_bound=float(bound)), indent=1))


if __name__ == "__main__":
    main()
