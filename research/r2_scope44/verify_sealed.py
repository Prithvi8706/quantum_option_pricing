"""Scope #44 R2 saved verifier. Checks a sealed run against docs/r2_scope44/PREREGISTRATION.md.

It imports nothing from steps.py, sealed_run.py or the R1 scripts. Each pass criterion is recomputed here by a
different route: an mpmath parts 1-2 bound for every certified c, the closed-form root of the Delta quadratic for
every N, integer square roots for the EB widths, and its own reading of the classical inputs.

    .context/frontier_t0_env/Scripts/python.exe -I -B research/r2_scope44/verify_sealed.py ROOT [--author-run]

--author-run (real runs only) also writes .context/R2_SCOPE44_VERIFICATION_RUN.json. mpmath is needed, so no -S.
"""
import hashlib
import json
import math
import sys
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

import mpmath as mp

REPO = Path(__file__).resolve().parents[2]
PREREG = REPO / "docs/r2_scope44/PREREGISTRATION.md"
MANIFEST = REPO / "research/r2_scope44/manifest.json"
SEED_TAG = {"real": b"r2-scope44-u1-seed-v1\n", "dry": b"r2-scope44-u1-DRY-RUN-seed-v1\n"}

# Restated from PREREGISTRATION.md (typed independently of steps.py).
EXPECT_C = {"window": ("3.87", F(3, 1000), F(4179, 1000)), "stage1": ("5.72", F(1, 10000), F(6052, 1000)),
            "stage2": ("3.88", F(29, 10000), F(4197, 1000))}
RESERVE34 = F(4, 10 ** 6)
N0, N_MAX = 800, 1048575
S = F(8192, 211)
E_STAT = F(9, 20) * F(1, 1000)
READOUT = F(1, 2 ** 39)
L1 = F(45202052, 10 ** 9)
BIAS_R1 = F(6703058386012589, 2 ** 64)
DELTA_U = DELTA_L = F(1, 10000)
RANGE, SLACK = F(40), F(1, 10 ** 9)
EXPLICIT = ("primary", "all_free_oracle", "one_lane_one_core", "symmetric_distfree")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load(p):
    sys.set_int_max_str_digits(0)
    return json.loads(Path(p).read_text(encoding="utf-8"))


def fr(pair):
    return F(int(pair[0]), int(pair[1]))


def lam_lower(N, c, beta):
    """Parts 1-2 lower bound on lambda0(N, c/N), gamma = 0, from P2_DERIVATION.md section 3 (40-digit mpmath)."""
    mp.mp.dps = 40
    N, c, b = mp.mpf(N), mp.mpf(str(c)), mp.mpf(beta)
    b2 = b * b

    def Phi(eta):
        q = b2 - eta * eta
        if q > 0:
            return 2 * mp.sinh(mp.sqrt(q)) / mp.sqrt(q)
        return 2 * mp.sin(mp.sqrt(-q)) / mp.sqrt(-q) if q < 0 else mp.mpf(2)

    phi0 = Phi(mp.mpf(0))
    i_tot = 2 * mp.pi * mp.quad(lambda x: mp.besseli(0, b * mp.sqrt(1 - x * x)) ** 2, [-1, 0, 1])
    i_c = 2 * mp.quad(lambda e: Phi(e) ** 2, [0, b, c] if c > b else [0, c])
    eta_min = N * mp.pi
    kappa = (1 + 1 / mp.sqrt(eta_min ** 2 - b2)) / (1 - b2 / eta_min ** 2)
    alias = b2 * kappa / (4 * N)
    c_r = alias + 2 / mp.pi
    eta1 = 2 * b
    a1 = 2 / ((1 + mp.sqrt(3) / 2) * (mp.sqrt(3) / 2)) * b2 * (1 + 2 / (mp.sqrt(3) * eta1))
    l1 = 2 * (eta1 * (phi0 - 2) + a1 / eta1) + 4 * (1 + mp.log(N * mp.pi))
    l1eta = 2 * (eta1 ** 2 * (phi0 - 2) / 2 + a1 * mp.log(N * mp.pi / eta1)) + 8 * N
    x = (alias * l1 + (2 / mp.pi ** 2) * l1eta / N) / mp.pi
    x_band = (alias + (2 / mp.pi ** 2) * c / N) * 2 * c * phi0 / mp.pi
    return (N * i_c / (2 * mp.pi) - x_band) / (N * i_tot / (2 * mp.pi) + x + c_r ** 2)


def n_exact(c, m):
    """Smallest N with c/N <= the exact largest Delta: the positive root of (S/4) D^2 + sqrt(m(S-m)) D = e - 2^-39."""
    mp.mp.dps = 60

    def q(x):
        return mp.mpf(x.numerator) / x.denominator

    a = mp.sqrt(q(m * (S - m)))
    d = (-a + mp.sqrt(a * a + q(S) * q(E_STAT - READOUT))) / (q(S) / 2)
    return int(mp.ceil(q(F(c)) / d))


def sqrt_up(x, bits=200):
    x = F(x)
    r = isqrt((x.numerator << (2 * bits)) // x.denominator)
    return F(r + 1, 1 << bits)


def ln_up(x):
    mp.mp.dps = 60
    return F(mp.nstr(mp.log(mp.mpf(x.numerator) / x.denominator), 55)) + F(1, 10 ** 50)


def eb_half(var, n, delta):
    lg = ln_up(2 / delta)
    return sqrt_up(2 * var * lg / n) + 7 * RANGE * lg / (3 * (n - 1))


def budget34(N, c):
    g = math.ceil(math.log2(2 * N + 1))
    eps3 = F(2 * N + 1) * (1 + 4 * F(str(c))) / (2 ** g * 2 ** 40)
    rot = 2 ** g + 2 * (g + 1) + 3 * g * (g - 1) // 2  # 3 rotations per controlled phase (conservative)
    return eps3 + 2 * (rot * F(1, 2 ** 40) + 2 ** g * F(4, 10 ** 15))


def classical():
    r = lambda p: load(REPO / p)  # noqa: E731
    ov = r("results/c10_challengers_20261022/overrides_run006.json")
    key = "B8x52_H140|0.001"
    speed = ov["f32_applied"][key]["speedup_run005"] * ov["f32_applied"][key]["f32_over_fast"]
    cand = []
    for p in ("results/frontier_classical_20261001/c2/c2_timing.json",
              "results/frontier_classical_20261001/c5/timing/c5_timing.json"):
        for block, val in r(p)["blocks"].items():
            if block.startswith("B8x52/"):
                for e_key, rec in val["t_c"].items():
                    if abs(float(e_key) - 0.001) < 1e-15:
                        cand.append(rec["primary"] / (speed if block.endswith("/preint") else 1.0))
    n1 = r("results/plan110_n1/headline/floor_sheet.json")["cases"]["B8x52"]
    w0 = r("results/plan110_w0/ws_floor/floor.json")["headline"]["B8x52"]["W1e7"]

    def dmin(n1_key, w0_key):
        return min(n1[n1_key]["by_width"]["W1e7"]["1e12|100ns"]["D_eff"],
                   w0[w0_key]["comparison"][0]["by_t_layer"]["100ns"]["base"]["eff_depth_supply_1e12"])

    sig = r("results/frontier_classical_20261001/sigma_dev/sigma_dev.json")["cases"]["B8x52"]["sigma_q"]
    return dict(T_C=min(cand), sigma_q=sig, D=dmin("primary_n72", "box_muller_current_law"),
                D_free=dmin("all_free_n48_f32", "all_free_and_narrow"),
                h16=ov["overrides"]["h16_ratio"][key], distfree=ov["overrides"]["distfree_factor"][key])


def main(argv):
    root = Path(argv[0]).resolve()
    author = "--author-run" in argv[1:]
    checks = {}

    def check(name, ok, **detail):
        checks[name] = dict(ok=bool(ok), **detail)

    receipt = load(root / "RECEIPT.json")
    started = load(root / "STARTED.json")
    mode = receipt["mode"]
    # V1 integrity
    listed = receipt["outputs_sha256"]
    actual = {str(p.relative_to(root)).replace("\\", "/"): sha(p.read_bytes()) for p in root.rglob("*")
              if p.is_file() and p.name not in ("RECEIPT.json", "VERIFICATION.json")}
    check("V1_outputs_match_receipt", listed == actual, missing=sorted(set(listed) - set(actual)),
          unlisted=sorted(set(actual) - set(listed)),
          changed=sorted(k for k in listed if k in actual and listed[k] != actual[k]))
    check("V1_status_pass", receipt["status"] == "PASS", status=receipt["status"])
    # V2 provenance
    prereg, manifest = PREREG.read_bytes(), MANIFEST.read_bytes()
    check("V2_prereg_and_manifest_unchanged", sha(prereg) == started["prereg_sha256"]
          and sha(manifest) == started["manifest_sha256"])
    files = json.loads(manifest)["files"]
    check("V2_manifest_files_unchanged", all(sha((REPO / p).read_bytes()) == h for p, h in files.items()),
          n_files=len(files))
    check("V2_seed_derivation", sha(SEED_TAG[mode] + prereg + b"\n" + manifest) == started["seed_hex"], mode=mode)
    if mode == "real":
        check("V2_git_head_recorded", bool(started.get("git_head")), git_head=started.get("git_head"))
    # V3 P2
    p2 = load(root / "p2.json")["certificates"]
    for key, (beta, delta, c_exp) in EXPECT_C.items():
        rec = p2[key]
        target = 1 - (delta - RESERVE34)
        ind = lam_lower(N0, c_exp, beta)
        check(f"V3_p2_{key}", F(rec["c"]) == c_exp and F(rec["lambda_lower_N0"]) >= target
              and ind >= mp.mpf(target.numerator) / target.denominator and rec["beta"] == beta,
              c=rec["c"], lambda_recorded=rec["lambda_lower_N0"][:14], lambda_independent=mp.nstr(ind, 14),
              target=float(target))
    # V4 A2a
    a2a = load(root / "a2a.json")
    summ = load(root / "a2a" / "run" / "summary.json")
    bias = fr(a2a["bias_upper"])
    check("V4_a2a", summ["all_checks_pass"] and bias == BIAS_R1 and bias <= F(11, 20) / 1000,
          bias=float(bias))
    # V5 U1 sample
    smp = load(root / "u1_sample.json")
    r1 = load(REPO / "results/claim_debts_20261022/u1/run001/eb_sample.json")
    rep = smp["reproduction_R1"]
    check("V5_u1_reproduces_R1", rep["sum"] == r1["sum"] and rep["sum_sq"] == r1["sum_sq"] and rep["n"] == r1["n"])
    words = [int(started["seed_hex"][8 * i:8 * i + 8], 16) for i in range(8)]
    fresh = smp["fresh"]
    check("V5_u1_fresh_seed_and_n", fresh["seed"] == words and fresh["n"] == 2 ** 23
          and 0 <= fresh["min"] and fresh["max"] <= 40)
    # V6 U1 bound
    ub = load(root / "u1_bound.json")
    n = fresh["n"]
    s1, s2 = F(fresh["sum"]), F(fresh["sum_sq"])
    mean, var = s1 / n, (s2 - s1 * s1 / n) / (n - 1)
    m_u = mean + SLACK + eb_half(var, n, DELTA_U) + bias
    m_l = mean - SLACK - eb_half(var, n, DELTA_L) - bias
    tol = F(1, 10 ** 35)
    check("V6_u1_bounds", abs(fr(ub["m_U"]) - m_u) < tol and abs(fr(ub["m_L"]) - m_l) < tol and m_u <= S / 2,
          m_U=float(m_u), m_L=float(m_l))
    # V7 N, k, M and the decision; V8 budgets
    hl = load(root / "headline.json")
    ci = classical()
    price = F(str(load(REPO / "results/frontier_classical_20261001/c1/c1_summary.json")["port_check"]["B8x52"]["price"]))
    se = F(str(ci["sigma_q"])) / E_STAT
    d1 = F(7, 2000)
    n1 = max(math.ceil(F(6052, 1000) / d1), N0)
    err = d1 / 2 + d1 * d1 / 4
    c_w, c_2 = F(4179, 1000), F(4197, 1000)
    mine = {"W_cont": [(n_exact(c_w, price + L1), c_w)], "W_proto": [(n_exact(c_w, m_u), c_w)],
            "W_oracle": [(n_exact(c_w, m_l), c_w)],
            "Q_cont": [(n1, F(6052, 1000)), (n_exact(c_2, price + 2 * S * err), c_2)],
            "Q_lower": [(n1, F(6052, 1000)), (n_exact(c_2, m_l), c_2)]}
    valid = {"W_cont": m_u <= price + L1}

    def M(k, D, tc):
        return k * 10.0 * float(se) * D * 1e-7 / tc

    no_go_mine, n_ok, b_ok, m_ok = True, True, True, True
    for name, stages in mine.items():
        step_row = hl["rows"][name]
        n_mine = sum(nn for nn, _ in stages)
        n_ok = n_ok and step_row["N_total"] - n_mine in (0, 1)
        for nn, c in stages:
            b_ok = b_ok and budget34(nn, c) <= RESERVE34 and N0 <= nn <= N_MAX
        k = n_mine / float(se)
        cols = {"primary": M(k, ci["D"], ci["T_C"]), "all_free_oracle": M(k, ci["D_free"], ci["T_C"]),
                "one_lane_one_core": M(k, ci["D"], ci["T_C"] * ci["h16"]),
                "symmetric_distfree": M(k, ci["D"], ci["T_C"] * ci["distfree"])}
        scale = step_row["N_total"] / n_mine
        m_ok = m_ok and all(abs(step_row["M"][c] / scale - v) <= 1e-12 * v for c, v in cols.items())
        if valid.get(name, True):
            no_go_mine = no_go_mine and all(cols[c] > 1 for c in EXPLICIT)
        checks.setdefault("V7_rows", {})[name] = dict(N_step=step_row["N_total"], N_verifier=n_mine,
                                                      M_primary_verifier=cols["primary"],
                                                      min_explicit_verifier=min(cols[c] for c in EXPLICIT))
    check("V7_N_within_one_of_exact", n_ok)
    check("V7_M_recomputed", m_ok)
    check("V7_continuity_R1", hl["continuity_1e9"] is True)
    check("V7_decision_agrees", hl["decision"]["no_go"] == no_go_mine and hl["decision"]["outcome"] ==
          ("NO_GO_CERTIFIED" if no_go_mine and hl["decision"]["eligible_on_certified_bias"] and b_ok
           else "NO_GO_NOT_CERTIFIED"), step=hl["decision"]["outcome"], verifier_no_go=no_go_mine)
    check("V8_parts34_budgets_3_rotations_per_cphase", b_ok)
    rows = checks.pop("V7_rows")
    verdict = "VERIFIED" if all(v["ok"] for v in checks.values()) else "NOT_VERIFIED"
    doc = dict(schema="r2-scope44-verification-v1", mode=mode, run=receipt["run"], verdict=verdict,
               outcome=hl["decision"]["outcome"], checks=checks, rows=rows, classical_inputs=ci,
               receipt_sha256=sha((root / "RECEIPT.json").read_bytes()), verifier_sha256=sha(Path(__file__).read_bytes()),
               python=sys.version, note="Software verification only. R2 also needs the human result review.")
    body = json.dumps(doc, indent=1, default=str).encode("utf-8")
    with open(root / "VERIFICATION.json", "xb") as f:
        f.write(body)
    if author:
        if mode != "real":
            raise SystemExit("--author-run applies to real runs only")
        with open(REPO / ".context" / f"R2_SCOPE44_VERIFICATION_{receipt['run']}.json", "xb") as f:
            f.write(body)
    print(verdict, hl["decision"]["outcome"])
    for k, v in checks.items():
        print(("PASS " if v["ok"] else "FAIL ") + k)


if __name__ == "__main__":
    main(sys.argv[1:])
