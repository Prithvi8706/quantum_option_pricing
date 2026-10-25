"""Freeze research/r2_scope44/manifest.json: the sha256 of every code file and input the sealed run uses.

Re-run after any change to a listed file, then update the manifest sha256 cited in PREREGISTRATION.md.
    .context/frontier_t0_env/Scripts/python.exe -I -S -B research/r2_scope44/freeze_manifest.py
"""
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
A02 = "results/limitation_program_20261001/A02_BM_native_financial_bridge_run002/"
POLAR = "results/limitation_program_20261001/A02_polar_cdf_bv_run003/"
FILES = {
    "sealed-run code": [
        "research/r2_scope44/steps.py",
        "research/r2_scope44/sealed_run.py",
        "research/r2_scope44/verify_sealed.py",
    ],
    "reused R1 code (executed by file path)": [
        "research/frontier_probe_20261021/p2_window_constant.py",
        "research/frontier_probe_20261021/p2b_parts34.py",
        "research/claim_debts_20261022/a2a/clip_split_certificate.py",
        "research/claim_debts_20261022/a2a/independent_recompute.py",
        "research/claim_debts_20261022/a2a/summarize.py",
        "research/claim_debts_20261022/u1/u1_certificate.py",
    ],
    "R1 sampler (copied into steps.py; reproduction target)": [
        "research/claim_debts_20261022/u1/eb_sample.py",
        "results/claim_debts_20261022/u1/run001/eb_sample.json",
    ],
    "A2a premises (run002 bridge, polar run003)": [
        A02 + n for n in ("closed_barrier_bands.json", "smooth_payoff_bounds.json", "complete_financial_bounds.json",
                          "stock_exponential_envelopes.json", "raw_log_prefix_envelopes.json", "summary.json")
    ] + [POLAR + "log_radius_envelope.json", POLAR + "ideal_hybrid_bounds.json"],
    "cited inputs (not re-verified by this scope)": [
        "results/frontier_classical_20261001/sigma_dev/sigma_dev.json",
        "results/frontier_classical_20261001/c1/c1_summary.json",
        "results/frontier_classical_20261001/c2/c2_timing.json",
        "results/frontier_classical_20261001/c5/timing/c5_timing.json",
        "results/c10_challengers_20261022/overrides_run006.json",
        "results/plan110_w0/ws_floor/floor.json",
        "results/plan110_n1/headline/floor_sheet.json",
        "results/claim_debts_20261022/c11/run001/summary.json",
    ],
    "R1 records the run must reproduce": [
        "results/claim_debts_20261022/a2a/run001/summary.json",
        "results/claim_debts_20261022/scope44/run001/scope44_receipt.json",
        "results/frontier_probe_20261021/p2/run002/p2_window.json",
        "results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json",
    ],
}


def main():
    groups = {g: {p: hashlib.sha256((REPO / p).read_bytes()).hexdigest() for p in ps} for g, ps in FILES.items()}
    flat = {p: h for g in groups.values() for p, h in g.items()}
    doc = dict(schema="r2-scope44-manifest-v1", files=flat, groups={g: sorted(v) for g, v in groups.items()})
    body = json.dumps(doc, indent=1, sort_keys=True).encode("utf-8") + b"\n"
    (REPO / "research/r2_scope44/manifest.json").write_bytes(body)
    print("manifest sha256", hashlib.sha256(body).hexdigest(), "files", len(flat))


if __name__ == "__main__":
    main()
