"""Register run003 = run002 (unchanged) + the C10 challenger wave (22 Oct 2026). Explicit deltas only.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/register_run003.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN2 = ROOT / "results/plan110_w0/register/run002/register.json"
OUT = ROOT / "results/plan110_w0/register/run003"
EV = "docs/c10_challengers_20261022/STATUS.md; results/c10_challengers_20261022/; " \
     "results/frontier_probe_20261021/headline/run003/headline_table.json"
DISP = {"T1": "decision-critical (W0 done)", "T2": "credited screen value / branch-A lever",
        "T3": "deferred certification debt", "T4": "closed or folded into N1", "T5": "dormant until trigger",
        "T6": "parked: different task (TRIG-G0)"}
DELTAS = {
    "C10": dict(live_status="partial (challenger wave 1 done)", wave_or_trigger="C10 wave 1 done 22 Oct",
                reopen_rule="Wave 1 adopted one challenger: the same preint estimand with closed-form date roots and AS241 "
                            "normals, 2.25x faster at B8x52 $0.001 (paired, 20 reps); primary T_C 10.03 s (was 22.53). "
                            "Killed: control variates under RQMC (sd ratio 1.00), two-direction smoothing (2.2x slower at "
                            "equal accuracy), F06, F07. Untried: GPU, PDE/sparse grids, MLMC/MIMC, surrogates. Label stays "
                            "'strongest tested'.", evidence=EV),
    "F06": dict(tier="T4", live_status="closed (screened)", wave_or_trigger="CLOSED 22 Oct (C10 wave)",
                reopen_rule="Screened: the binding barrier date is spread over late dates (top 3 = 30% for B8x52) and the "
                            "two smallest roots are within 0.05 in 44% of paths; the switching surface is dense, not "
                            "isolatable. Reopen only with a smoothing that removes the date-switching kink.", evidence=EV),
    "F07": dict(tier="T4", live_status="closed (screened)", wave_or_trigger="CLOSED 22 Oct (C10 wave)",
                reopen_rule="Screened: not rare-event dominated (P(KO) 0.097, P(f>0) 0.425, top 1% of payoffs carry 6.6% "
                            "of the price); importance sampling has no region to concentrate on. Reopen for a contract with "
                            "a rare payoff region.", evidence=EV),
    "F31": dict(reopen_rule="Master ledger. Rerun 22 Oct with C10 (headline run003): minimum explicit M 23.1 (window), "
                            "521 (canonical), 1,800 (certified today); all-free 1.15; symmetric 0.63.", evidence=EV),
    "C14": dict(reopen_rule="With C10 the minimum miss at the primary corner is 23.1 (window, failure 0.003) / 19.4 "
                            "(0.01), above 10; the all-free corner gives 1.15 and the symmetric convention 0.63. The scoped "
                            "negative holds at every 100 ns corner except the symmetric distribution-free convention.",
                evidence=EV),
    "E07": dict(wave_or_trigger="A3; trigger (favourable miss <= 1) NO LONGER FIRED after C10 (all-free + window 1.15); "
                                "fires only with the symmetric convention",
                reopen_rule="Deferred again on the oracle side: the all-free favourable ledger is 1.15 after C10. It fires "
                            "only under the symmetric distribution-free convention (0.63).", evidence=EV),
    "F05": dict(reopen_rule="Under the window class after C10: free loader alone 12.2, loader + free exponential 2.17, "
                            "all-free 1.15 (primary). Kill rule (>= 10x) met again for the free loader alone; F05 stays a "
                            "parameter of the joint loader+exponential lever.", evidence=EV),
    "C09": dict(reopen_rule="Trigger fired (miss <= 30; window 23.1 after C10). The full G4 symmetric-convention timing "
                            "should use the C10 fast kernel.", evidence=EV),
    "H16": dict(reopen_rule="Done in W0. Re-measure the 1-16 worker ratio with the C10 fast kernel (1 lane vs 1 core "
                            "column still uses the Stage C ratio)."),
}


def main():
    OUT.mkdir(parents=False, exist_ok=False)
    r2 = json.loads(RUN2.read_text(encoding="utf-8"))
    items, changes, out = r2["items"], [], []
    assert len(items) == 110 and set(DELTAS) <= {r["id"] for r in items}
    for r in items:
        r3 = dict(r)
        d = DELTAS.get(r["id"])
        if d:
            before = {k: r.get(k) for k in d}
            r3.update(d)
            if "tier" in d:
                r3["disposition"] = DISP[d["tier"]]
            r3["updated"] = "run003 (22 Oct 2026, C10 wave)"
            changes.append(dict(id=r["id"], before={k: v for k, v in before.items() if v is not None}, after=d))
        out.append(r3)
    tiers = {k: sum(x["tier"] == k for x in out) for k in DISP}
    meta = dict(script="research/c10_challengers_20261022/register_run003.py", python=sys.version, base="run002",
                base_sha256=hashlib.sha256(RUN2.read_bytes()).hexdigest(), count=len(out), tiers=tiers, changed=len(changes))
    with open(OUT / "register.json", "x", encoding="utf-8") as f:
        json.dump(dict(meta=meta, items=out, changes=changes), f, indent=1)
    md = ["# 110-item closure register, run003 (22 Oct 2026, after the C10 challenger wave)", "",
          f"Base: run002 (unchanged). Count {len(out)}/110. Tiers: {tiers}. {len(changes)} rows updated; see CHANGES.md.", "",
          "| ID | Title | Live status | Tier | Disposition | Wave / trigger | Reopen / kill rule |", "|---|---|---|---|---|---|---|"]
    for x in out:
        rule = x["reopen_rule"] + (f" [{x['note']}]" if x.get("note") else "")
        md.append(f"| {x['id']} | {x['title']} | {x['live_status']} | {x['tier']} | {x['disposition']} | "
                  f"{x['wave_or_trigger']} | {rule} |")
    with open(OUT / "REGISTER.md", "x", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(OUT / "CHANGES.md", "x", encoding="utf-8") as f:
        f.write("# Register run003: changes from run002\n\nEvidence: " + EV + "\n\n" + "\n".join(
            f"- **{c['id']}**: " + "; ".join(f"{k}: {c['before'].get(k, '-')} -> {v}" if k in ("tier", "live_status")
                                             else f"{k} updated" for k, v in c["after"].items()) for c in changes) + "\n")
    print(json.dumps(dict(tiers=tiers, changed=len(changes))))


if __name__ == "__main__":
    main()
