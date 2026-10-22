"""Register run002: the 110-item register (results/plan110_w0/register/run001, unchanged) updated with the 21-22 Oct
frontier-probe evidence. Every change is an explicit delta below; untouched rows are copied verbatim.

Trigger evaluation uses the probe's round-2 numbers (results/frontier_probe_20261021/headline/run002, derived/run001):
best explicit M at the binding cell 10.29 (window, delta 0.003) / 8.64 (delta 0.01); all-free 0.511; symmetric
distribution-free 0.279; loader-and-exponential near-free 0.965; canonical explicit 232.0; certified today 801.5.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/frontier_probe_20261021/register_run002.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN1 = ROOT / "results/plan110_w0/register/run001/register.json"
OUT = ROOT / "results/plan110_w0/register/run002"
EV = dict(
    p1="results/frontier_probe_20261021/p1/run001/p1_span.json; p1/run002/p1b_hybrid.json",
    p2="results/frontier_probe_20261021/p2/run002/p2_window.json; docs/frontier_probe_20261021/P2_DERIVATION.md",
    lit="results/frontier_probe_20261021/p2/lit_check.jsonl",
    head="results/frontier_probe_20261021/headline/run002/headline_table.json; derived/run001/derived.json",
    p3="results/frontier_probe_20261021/p3/run002/p3_desk.json",
    rev="results/frontier_probe_20261021/review/p1_review.jsonl; review/p2_review.jsonl",
    status="docs/frontier_probe_20261021/STATUS.md",
)
DISP = {"T1": "decision-critical (W0 done)", "T2": "credited screen value / branch-A lever",
        "T3": "deferred certification debt", "T4": "closed or folded into N1", "T5": "dormant until trigger",
        "T6": "parked: different task (TRIG-G0)"}

# id: dict(tier, live_status, wave_or_trigger, reopen_rule, evidence, note, trigger_fired)
DELTAS = {
    "F20": dict(tier="T4", live_status="closed (probe P1)", wave_or_trigger="CLOSED 22 Oct (frontier probe P1)",
                reopen_rule="Closed. Any control with a closed-form mean is continuous at the arithmetic-basket barrier, where "
                            "the payoff jumps by $38.6, so the residual span is >= $38.6 of $38.8 for every beta (net <= 1.59 "
                            "with U1). Reopen only for a control with a certified mean that carries the arithmetic barrier "
                            "on every date.", evidence=EV["p1"] + "; " + EV["rev"]),
    "F04": dict(tier="T4", live_status="closed (probe P1)", wave_or_trigger="CLOSED 22 Oct (frontier probe P1 run002)",
                reopen_rule="Closed on evaluated costs, not on the withdrawn F20 zero-depth credit. Coherent preintegration "
                            "nets 1.70; clipped/hybrid 3.42 at D ratio 1 and 2.62 at the structure-aware 1.30; k = 2-3 "
                            "directions <= 0.70 (consistent gain pairing; kill threshold 4). Reopen only with a coherent "
                            "preintegration oracle cheaper than the plain payoff oracle.", evidence=EV["p1"] + "; " + EV["rev"]),
    "E25": dict(tier="T4", live_status="closed (kill rule met)", wave_or_trigger="CLOSED 22 Oct (literature check)",
                reopen_rule="Kill rule met: none of 8 further primary sources (KO, Hamoudi, Rall, Kimmel-Low-Yoder, "
                            "Belliardo-Giovannetti, AQAE, RQAE, Labib) gives a worst-case coverage theorem below canonical; "
                            "the best explicit is AQAE Thm 2, c(0.003) ~ 409. The window estimator (C11) supersedes this "
                            "route. Reopen on TRIG-LIT.", evidence=EV["lit"]),
    "C11": dict(tier="T3", live_status="partial (bracket updated)", wave_or_trigger="W0-WS3 (bracket); probe P2; A3 (compile)",
                reopen_rule="Bracket now 1.85 (counting floor) to 8.762 (certified Kaiser-window constant, parts 1-4 "
                            "explicit, AI R2 reviewed, conditional on U1/U2 + direction-select). TRIGGER FIRED: per-call depth "
                            "(2,296) is 10.3x k*D_max, inside 30x; the full iterate compile is now due but needs circuit work "
                            "(not authorized; branch A).", evidence=EV["p2"] + "; " + EV["head"], trigger_fired=["C11-30x"]),
    "E01": dict(reopen_rule="Access-model card stands. Achievability bracket 1.85 to 8.762 (was ~198): gap ~4.7x. "
                            "Structural escapes F04/F20 closed (probe P1); F05 live again under the window class.",
                evidence="research/plan110_n1/estimator/estimator_card.md; " + EV["p2"]),
    "E03": dict(reopen_rule="Credit <=2x stands; U2 now also enters the window constant (without U2: k 25.8, M 30.3 at "
                            "the primary convention). Certify the support-tight wrapper only on branch A.",
                evidence=EV["head"]),
    "E08": dict(reopen_rule="Closed for the canonical schedule (15 vs 11 shots). Window class at failure 0.01: k 7.359 "
                            "(M 8.64) vs 8.762 at 0.003.", evidence=EV["p2"]),
    "F05": dict(tier="T2", live_status="partial (lever live again)", wave_or_trigger="W0-WS2 (parameter); probe P3",
                reopen_rule="Kill rule (close if >=10x miss remains) no longer met under the window class: free loader "
                            "alone gives M 5.43, loader + free exponential 0.965, all-free 0.511. Stays closed for the "
                            "canonical class (122). Costing a real loader is A02-A04 work (TRIG-R2 not fired at primary).",
                evidence=EV["p3"]),
    "C03": dict(wave_or_trigger="A3; TRIGGER FIRED (plausible-tier miss 10.29 <= 30)",
                reopen_rule="Trigger fired: a cell now reaches plausible-tier miss <= 30 (window class 10.29). Completing "
                            "the confidence-allowance skeleton is claim-grade (R2) work; needs user authorization.",
                evidence=EV["head"], trigger_fired=["C03-30"]),
    "C09": dict(wave_or_trigger="N1 envelope slice (done); A1 full G4; TRIGGER FIRED (miss <= 30)",
                reopen_rule="Envelope slice done in N1 (36.9x). Trigger fired (miss 10.29 <= 30): a full G4 timed successful "
                            "price is now due before any claim at the symmetric convention.", evidence=EV["head"],
                trigger_fired=["C09-30"]),
    "C10": dict(live_status="partial (challenger wave started 22 Oct)",
                wave_or_trigger="N1 label; TRIGGER FIRED (scenario miss <= 3); C10 challenger wave",
                reopen_rule="Trigger fired: scenarios reach miss <= 3 (all-free 0.511, symmetric 0.279). Implement CPU "
                            "challengers on the binding cell B8x52 $0.001 (with F06/F07). A faster eligible challenger lowers "
                            "T_C and raises M.", evidence=EV["head"], trigger_fired=["C10-3"]),
    "C12": dict(reopen_rule="Labelling stands. Trigger formally fired (all-free floor brings miss <= 10 under the window "
                            "class), but a new backend is circuit work: not authorized.", trigger_fired=["C12-10"]),
    "C14": dict(reopen_rule="Rule 'publish the scoped no-tenfold if min miss > 10 at every corner >= 100 ns' NO LONGER "
                            "HOLDS: window class 10.29 (failure 0.003) / 8.64 (failure 0.01) at the primary corner, 0.511 at "
                            "the all-free corner. The scoped negative must be restated as conditional on the primary "
                            "convention and the current-law oracle (MEMO edits 1-3).", evidence=EV["head"],
                trigger_fired=["C14-10"]),
    "E07": dict(wave_or_trigger="A3; TRIGGER FIRED (favourable miss <= 1)",
                reopen_rule="Trigger fired: the favourable ledger reaches miss <= 1 (all-free + window 0.511). The 4 open "
                            "ledger obligations are now live certification debt (claim-grade; needs authorization).",
                evidence=EV["head"], trigger_fired=["E07-1"]),
    "F06": dict(live_status="ready (activated)", wave_or_trigger="TRIG-F31-10x FIRED; C10 challenger wave",
                reopen_rule="Activated (optimistic T_Q within 10x of T_C: window 8.64-10.29 at primary). CPU-only screen of "
                            "the active barrier-date switching surface, as a classical challenger input.",
                evidence=EV["head"], trigger_fired=["TRIG-F31-10x"]),
    "F07": dict(live_status="ready (activated)", wave_or_trigger="TRIG-F31-10x FIRED; C10 challenger wave",
                reopen_rule="Activated with F06. Archived survival/tail-share screen of rare-event proposals, CPU-only.",
                evidence=EV["head"], trigger_fired=["TRIG-F31-10x"]),
    "F31": dict(reopen_rule="Never killed: the master ledger. Rerun 22 Oct with the probe inputs (headline run002): "
                            "minimum explicit M 10.29 (window) / 232.0 (canonical) / 801.5 (certified today).",
                evidence=EV["head"]),
    "E04": dict(reopen_rule="Zero-cost screen stands (1.75x). The window class keeps a QFT readout; E04's QFT-removal "
                            "question does not apply to it."),
    "E20": dict(reopen_rule="Width bound stands; the window class is one coherent chain (no lane credit)."),
}
# TRIG-HWACT: best credible D_reaction x k / T_C within 10x of the 100 ns budget (window: 8.64-10.29) -> fired (marginal)
for i in ("H04", "H05", "H06", "H07", "H08", "H09", "H10", "H11", "H13", "H17", "H18"):
    DELTAS.setdefault(i, {})
    DELTAS[i]["trigger_fired"] = ["TRIG-HWACT (marginal: window M 8.64-10.29 at 100 ns)"]
    DELTAS[i]["note"] = ("TRIG-HWACT fired marginally on the window class; latency anchors are unchanged and hardware "
                         "architecture work stays frozen pending user authorization.")
for i in ("A02", "A03", "A04", "A05", "A07", "A14", "A13"):
    DELTAS.setdefault(i, {})
    DELTAS[i]["note"] = ("TRIG-R2/R1.5 not fired at the primary floor (residual 10.29). P3: M <= 1 at the primary "
                         "conventions needs BOTH the loader and the exponential near-free (0.965); either alone >= 4.36.")


def main():
    OUT.mkdir(parents=False, exist_ok=False)
    r1 = json.loads(RUN1.read_text(encoding="utf-8"))
    items = r1["items"]
    ids = {r["id"] for r in items}
    assert len(items) == 110 and set(DELTAS) <= ids, set(DELTAS) - ids
    changes = []
    out = []
    for r in items:
        r2 = dict(r)
        d = DELTAS.get(r["id"])
        if d:
            before = {k: r.get(k) for k in d}
            for k, v in d.items():
                r2[k] = v
            if "tier" in d:
                r2["disposition"] = DISP[d["tier"]]
            r2["updated"] = "run002 (22 Oct 2026, frontier probe)"
            changes.append(dict(id=r["id"], before={k: v for k, v in before.items() if v is not None},
                                after=d))
        out.append(r2)
    tiers = {k: sum(x["tier"] == k for x in out) for k in DISP}
    meta = dict(script="research/frontier_probe_20261021/register_run002.py", python=sys.version, base="run001",
                base_sha256=hashlib.sha256(RUN1.read_bytes()).hexdigest(), count=len(out), tiers=tiers,
                tiers_run001=r1["meta"]["tiers"], changed=len(changes), evidence=EV)
    with open(OUT / "register.json", "x", encoding="utf-8") as f:
        json.dump(dict(meta=meta, items=out, changes=changes), f, indent=1)
    md = ["# 110-item closure register, run002 (22 Oct 2026)", "",
          f"Base: run001 (unchanged). Count {len(out)}/110. Tiers: {tiers} (run001: {r1['meta']['tiers']}). "
          f"{len(changes)} rows updated with the frontier-probe evidence; see CHANGES.md.", "",
          "| ID | Title | Live status | Tier | Disposition | Wave / trigger | Reopen / kill rule |",
          "|---|---|---|---|---|---|---|"]
    for x in out:
        rule = x["reopen_rule"] + (f" [{x['note']}]" if x.get("note") else "")
        md.append(f"| {x['id']} | {x['title']} | {x['live_status']} | {x['tier']} | {x['disposition']} | "
                  f"{x['wave_or_trigger']} | {rule} |")
    with open(OUT / "REGISTER.md", "x", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    ch = ["# Register run002: changes from run001", "",
          "Evidence keys: " + "; ".join(f"{k} = {v}" for k, v in EV.items()), ""]
    fired = sorted({t for c in changes for t in c["after"].get("trigger_fired", [])})
    ch.append("Triggers fired by the probe numbers: " + ", ".join(fired) + ".")
    ch.append("")
    for c in changes:
        a = c["after"]
        ch.append(f"- **{c['id']}**: " + "; ".join(
            f"{k}: {c['before'].get(k, '-')} -> {v}" if k in ("tier", "live_status") else f"{k} updated"
            for k, v in a.items()))
    with open(OUT / "CHANGES.md", "x", encoding="utf-8") as f:
        f.write("\n".join(ch) + "\n")
    print(json.dumps(dict(tiers=tiers, changed=len(changes), fired=fired), indent=1))


if __name__ == "__main__":
    main()
