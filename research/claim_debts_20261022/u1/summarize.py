"""Write results/claim_debts_20261022/u1/RUN/summary.json from the certificate, the independent recompute and the sample.
Run (worktree root): <frontier_t0_env python> -I -S -B research/claim_debts_20261022/u1/summarize.py RUN
"""
import hashlib
import json
import os
import sys

RUN = sys.argv[1]
OUT = os.path.join("results", "claim_debts_20261022", "u1", RUN)


def load(name):
    with open(os.path.join(OUT, name), encoding="utf-8") as f:
        return json.load(f)


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


cert, ind, eb = load("u1_certificate.json"), load("u1_independent.json"), load("eb_sample.json")
wc = cert["window_class"]
summary = dict(
    schema="u1-certificate-summary-v1",
    rigour="R1 (two arithmetic paths agree; fixed-n sample); NOT R2: no preregistration, sealed run or human review",
    cell="B8x52, eps = $0.001, window class (S = 8192/211, e = 0.45 eps, failure 3/1000 with the part-4 budget)",
    all_checks_pass=bool(ind["agree"] and cert["p2_assumption_covered"]),
    m_cert=cert["m_cert"], m_cert_float=cert["m_cert_float"],
    pieces=dict(sample_mean=cert["sample"]["mean"], eb_half_width=cert["eb_half_width"],
                float_slack=cert["sample"]["float_slack"], ucb_EY=cert["ucb_EY_float"],
                a2a_bias=cert["a2a_bias_float"]),
    delta_U=cert["delta_U"], failure_share=cert["failure_share"],
    p2_assumed_m=cert["p2_assumed_m"]["value"], p2_assumption_covered=cert["p2_assumption_covered"],
    margin_to_p2_m=cert["margin_to_p2_m"],
    window_k_certified_premise=wc["k_certified_premise"], window_M_certified_premise=wc["at_p2_m"]["M"],
    window_k_at_m_cert=wc["at_m_cert"]["k"], window_M_at_m_cert=wc["at_m_cert"]["M"],
    independent=dict(m_cert_abs_diff=ind["m_cert_abs_diff_vs_primary"], N_calls_match=ind["agree"]),
    machine_idle=[m.get("idle") for m in eb["machine"]],
    machine_note="not idle (another session's python process at ~5 CPU-s per 5 s); irrelevant to correctness, "
                 "the sample is not a timing measurement",
    files_sha256={n: sha(os.path.join(OUT, n)) for n in ("eb_sample.json", "u1_certificate.json", "u1_independent.json")},
    producers_sha256={p: sha(os.path.join("research", "claim_debts_20261022", "u1", p))
                      for p in ("eb_sample.py", "u1_certificate.py", "u1_independent.py", "summarize.py")},
    interpreter=sys.version,
)
with open(os.path.join(OUT, "summary.json"), "x", encoding="utf-8") as f:
    json.dump(summary, f, indent=1)
print(json.dumps({k: summary[k] for k in ("all_checks_pass", "m_cert_float", "pieces", "window_k_certified_premise",
                                           "window_M_certified_premise", "window_k_at_m_cert", "window_M_at_m_cert")},
                 indent=1))
