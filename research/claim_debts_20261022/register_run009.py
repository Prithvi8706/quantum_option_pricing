"""Register run009 = run008 (unchanged) + the 22 Oct claim-grade debt work (user-authorized, R1). Explicit deltas only.
Run (worktree root): ../../../.context/frontier_t0_env/Scripts/python.exe -I -S -B research/claim_debts_20261022/register_run009.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/plan110_w0/register/run008/register.json"
OUT = ROOT / "results/plan110_w0/register/run009"
DOC = "docs/claim_debts_20261022/"
RES = "results/claim_debts_20261022/"
EV = (DOC + "CLAIM_DEBTS_STATUS.md; " + RES + "{a2a,c03,c11,u1,h06_h17,scope44}/run00x; "
      + RES + "review/a2a_review_summary.md")
DISP = {"T1": "decision-critical (W0 done)", "T2": "credited screen value / branch-A lever",
        "T3": "deferred certification debt", "T4": "closed or folded into N1", "T5": "dormant until trigger",
        "T6": "parked: different task (TRIG-G0)"}
R2 = " R2 still open: preregistration, sealed run with receipt, human peer review."
DELTAS = {
    "C02": dict(reopen_rule="B8 eps=0.001 is now ELIGIBLE on a certified bias: clip-split certificate 3.634e-4 <= 0.55 eps "
                "(R1; two paths agree to 9.4e-13; independent AI review: sound, no major). Source unchanged.",
                evidence=DOC + "A2A_CLIP_SPLIT_CERTIFICATE.md"),
    "A02": dict(note="22 Oct: binding-cell eligibility no longer needs the A02 bridge rerun (stock classes 30->33); "
                "the clip-split certificate (R1) bounds the bias at 3.634e-4 with the source unchanged."),
    "A07": dict(note="22 Oct: the A07 re-proofs for the lowered clamp are not needed for eligibility (clip-split route); "
                "TRIG-R2 still not fired."),
    "A13": dict(note="22 Oct: the A13 re-proofs for the lowered clamp are not needed for eligibility (clip-split route); "
                "TRIG-R1.5 still not fired."),
    "C03": dict(live_status="complete at R1 (22 Oct)",
                reopen_rule="Complete-price ledger at B8x52 $0.001, both window classes. Failure: estimator 0.003 (cert) + "
                "U1 1e-4 (cert R1; window class) or 0 (quantum-only mean) + bridge/source 0 (cited: deterministic pay-once "
                "bound) + acquisition 0 + physical 0.0069/0.007 (explicit hardware premise). Dollar: 0.45 eps statistical + "
                "bias 3.634e-4 + readout 2^-39, within 0.55 eps." + R2,
                wave_or_trigger="A3 (user-authorized 22 Oct); R1 done", evidence=RES + "c03/run001/c03_ledger.json"),
    "E07": dict(live_status="complete at R1 for eps = 1/1000 (22 Oct)",
                reopen_rule="Obligations mapped and closed in the C03 run001 ledger: finite law, clipped tail and native "
                "arithmetic in A2a (3.634e-4); physical_execution an explicit premise (<= 2.9e-16 per T at the floor, "
                "<= 2.8e-17 per T for the compiled iterate)." + R2, evidence=RES + "c03/run001/c03_ledger.json"),
    "C11": dict(live_status="compiled at R1 (22 Oct)",
                reopen_rule="Full controlled-iterate compile of the binding cell with the U2 wrapper: 4,267,659,718 T literal "
                "(18.6x the floor) or 2.44e9 T at 4 T per Toffoli (10.6x), 609,665,674 Toffolis, 4,460,627 logical qubits, "
                "Toffoli depth 201,263. Compiled window M 2,290 (floor conventions), 8,828 literal, >= 277 in every "
                "reading: the compile only raises M, so the floor stays a quantum-favourable reading." + R2,
                wave_or_trigger="A3 (user-authorized circuit work 22 Oct); R1 done", evidence=DOC + "C11_U2_COMPILE.md"),
    "E03": dict(reopen_rule="U2 support-tight wrapper built and verified at R1 (x211 multiplier, 53-bit comparator: "
                "40,000 exhaustive and 4,281 full-width cases pass; support 211*sup Yraw < 2^53; +11,578 T per iterate, "
                "0 qubits; readout <= 2^-39). U1 mean certificate at R1: m = 3.28804 >= E[g] with probability "
                "1 - 1e-4 (EB, R = 40, plus A2a), covering P2's m = 3.32682." + R2,
                evidence=DOC + "C11_U2_COMPILE.md; " + DOC + "U1_CERTIFICATE.md"),
    "E11": dict(wave_or_trigger="Scope-#43 stop lifted by the user (22 Oct); the U1/U2 estimator credits are certified at R1",
                reopen_rule="U1 (EB + A2a) and U2 (compiled wrapper) are done at R1 as estimator credits. The known-moment "
                "L2 route (U4/U5) stays closed on its own economics (~7.6-8.3M calls vs 983,025 bounded); reopen only "
                "if a known-moment design comes in below 0.5x bounded calls at b=0.",
                evidence=DOC + "U1_CERTIFICATE.md; " + DOC + "C11_U2_COMPILE.md"),
    "E23": dict(note="22 Oct: the C03 run001 ledger carries QSP/window parts 1-4 (incl. rotation synthesis to 2^-40), "
                "bias and readout in one budget at R1 for the binding cell."),
    "H06": dict(live_status="desk done (22 Oct, R1)",
                reopen_rule="Floor T is all AND: 57,400,792 per call, i.e. 6.5e12 CCZ/s for M <= 1. Supply-convention "
                "column: 4 T per AND 26.08 (primary); catalysed CCZ = 2 T 13.04; 1 CCZ per slot 8.63 (reaction-bound). No "
                "supply convention goes below the 740-layer reaction floor (M >= 8.40), so no single-departure flip.",
                note="TRIG-HWACT not fired; no physical layout modelled.", evidence=DOC + "H06_H17_DESK.md"),
    "H17": dict(live_status="desk done (22 Oct, R1)",
                reopen_rule="Necessary-condition columns (other resource unlimited), window class: floor iterate needs "
                "<= 11.6 ns per reaction layer or >= 2.61e13 T/s for M <= 1 (116 ns / 2.61e12 for M <= 10); the saved "
                "source iterate needs 11.4 ps or 4.85e14 T/s (M 8,749 at the primary conventions).",
                note="TRIG-HWACT not fired; no architecture attached.", evidence=DOC + "H06_H17_DESK.md"),
    "H18": dict(live_status="desk done (22 Oct, R1)",
                reopen_rule="With the C03 allocation (physical share 0.007 / 0.0069): <= 2.92e-16 / 2.98e-16 logical failure "
                "per T at the floor (104,332 / 100,924 iterates), and <= 2.75e-17 / 2.80e-17 per T for the compiled "
                "iterate (2.44e9 T at 4 T per Toffoli).",
                note="Necessary conditions only; hardware architecture stays frozen (TRIG-HWACT not fired).",
                evidence=RES + "c03/run001/c03_ledger.json"),
}


def main():
    OUT.mkdir(parents=False, exist_ok=False)
    base = json.loads(BASE.read_text(encoding="utf-8"))
    items, changes, out = base["items"], [], []
    assert len(items) == 110 and set(DELTAS) <= {r["id"] for r in items}
    for r in items:
        r2 = dict(r)
        d = DELTAS.get(r["id"])
        if d:
            before = {k: r.get(k) for k in d}
            r2.update(d)
            if "tier" in d:
                r2["disposition"] = DISP[d["tier"]]
            r2["updated"] = "run009 (22 Oct 2026, claim-grade debts at R1)"
            changes.append(dict(id=r["id"], before={k: v for k, v in before.items() if v is not None}, after=d))
        out.append(r2)
    tiers = {k: sum(x["tier"] == k for x in out) for k in DISP}
    meta = dict(script="research/claim_debts_20261022/register_run009.py", python=sys.version, base="run008",
                base_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(), count=len(out), tiers=tiers,
                changed=len(changes))
    with open(OUT / "register.json", "x", encoding="utf-8") as f:
        json.dump(dict(meta=meta, items=out, changes=changes), f, indent=1)
    md = ["# 110-item closure register, run009 (22 Oct 2026, current)", "",
          f"Base: run008 (unchanged). Count {len(out)}/110. Tiers: {tiers}. {len(changes)} rows updated; see CHANGES.md.", "",
          "| ID | Title | Live status | Tier | Disposition | Wave / trigger | Reopen / kill rule |",
          "|---|---|---|---|---|---|---|"]
    for x in out:
        rule = x["reopen_rule"] + (f" [{x['note']}]" if x.get("note") else "")
        md.append(f"| {x['id']} | {x['title']} | {x['live_status']} | {x['tier']} | {x['disposition']} | "
                  f"{x['wave_or_trigger']} | {rule} |")
    with open(OUT / "REGISTER.md", "x", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(OUT / "CHANGES.md", "x", encoding="utf-8") as f:
        f.write("# Register run009: changes from run008\n\nEvidence: " + EV + "\n\n" + "\n".join(
            f"- **{c['id']}**: " + "; ".join(f"{k}: {c['before'].get(k, '-')} -> {v}" if k in ("tier", "live_status")
                                             else f"{k} updated" for k, v in c["after"].items()) for c in changes) + "\n")
    print(json.dumps(dict(tiers=tiers, changed=len(changes))))


if __name__ == "__main__":
    main()
