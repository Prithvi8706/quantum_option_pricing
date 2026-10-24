"""Register run006 = run005 (unchanged) + adoption of the C10/C09 R2 review and the quantum-only mean option (22 Oct 2026). Explicit deltas only.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/register_run006.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN2 = ROOT / "results/plan110_w0/register/run005/register.json"
OUT = ROOT / "results/plan110_w0/register/run006"
EV = "docs/c10_challengers_20261022/STATUS.md; results/c10_challengers_20261022/; " \
     "results/frontier_probe_20261021/headline/run003/headline_table.json"
DISP = {"T1": "decision-critical (W0 done)", "T2": "credited screen value / branch-A lever",
        "T3": "deferred certification debt", "T4": "closed or folded into N1", "T5": "dormant until trigger",
        "T6": "parked: different task (TRIG-G0)"}
EV = EV + "; results/c10_challengers_20261022/c09/; results/c10_challengers_20261022/h16_fast/run001/; "           "results/frontier_probe_20261021/headline/run004/headline_table.json; derived/run002/derived.json"
EV3 = ("docs/c10_challengers_20261022/STATUS.md section 6; results/c10_challengers_20261022/review/c10_review.jsonl; "
       "results/c10_challengers_20261022/c09b/; results/frontier_probe_20261021/headline/run005/headline_table.json; "
       "results/frontier_probe_20261021/p2/run003_self_mean/; derived/run004_self_mean_run005/")
DELTAS = {
    "C10": dict(reopen_rule="Wave 1 adopted the fast preint (same estimand). After the R2 review, primary T_C at B8x52 "
                "$0.001 is 10.84 s (QF end of the 2.08-2.25x same-state speedups; Stage C 22.53 s). Killed: CV under "
                "RQMC, two-direction smoothing (narrow: 1.3-1.5x slower at Q >= 16), F06, F07. Untried: GPU, PDE/sparse "
                "grids, MLMC/MIMC, surrogates.", evidence=EV3),
    "C09": dict(reopen_rule="Measured timed distribution-free 99% prices, minimum over methods: replicated RQMC (16-point "
                "digitally-shifted Sobol nets, EB on replicate means, R = 17.30) factor 17.3 (B8x52 $0.001) / 17.9 "
                "(B4x12 $0.001); iid EB 16.1 / 10.3 at $0.01. Window symmetric M 1.23 (does not reach 1).", evidence=EV3),
    "F31": dict(reopen_rule="Master ledger, headline run005 (measured inputs, QF choices, review adopted): minimum explicit "
                "M 21.4 (window), 482 (canonical), 1,666 (certified today); all-free 1.06; 1 lane 2.22; symmetric 1.23; "
                "two departures 0.061.", evidence=EV3),
    "C14": dict(reopen_rule="Run005: no single favourable departure reaches M <= 1 for any explicit class (closest: window "
                "all-free 1.06); two departures do (all-free + symmetric 0.061). The scoped negative holds at every "
                "single-departure corner >= 100 ns.", evidence=EV3),
    "E07": dict(reopen_rule="Favourable-ledger trigger not fired (all-free + window 1.06; symmetric 1.23). Obligations map "
                "onto C03 rows; U1's row (B2) can be removed by the quantum-only mean stage.", evidence=EV3),
    "C11": dict(reopen_rule="Bracket 1.85 to 8.762 (U1 + U2 + direction-select) or 9.058 with a quantum-only certified mean "
                "stage replacing U1 (no classical price). Trigger (per-call depth within 30x of k*D_max) fired; the "
                "compile needs circuit work (not authorized).", evidence=EV3),
    "E01": dict(reopen_rule="Access-model card stands. Achievability bracket 1.85 to 8.76 (9.06 without the classical "
                "price). Structural escapes F04/F20 closed.", evidence=EV3),
    "F05": dict(reopen_rule="Under the window class after the review: free loader alone 11.3, loader + free exponential 2.0, "
                "all-free 1.06 at the primary conventions; M <= 1 needs D_eff <= 107 layers (p3/run005).", evidence=EV3),
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
            r3["updated"] = "run006 (22 Oct 2026, review adoption)"
            changes.append(dict(id=r["id"], before={k: v for k, v in before.items() if v is not None}, after=d))
        out.append(r3)
    tiers = {k: sum(x["tier"] == k for x in out) for k in DISP}
    meta = dict(script="research/c10_challengers_20261022/register_run006.py", python=sys.version, base="run005",
                base_sha256=hashlib.sha256(RUN2.read_bytes()).hexdigest(), count=len(out), tiers=tiers, changed=len(changes))
    with open(OUT / "register.json", "x", encoding="utf-8") as f:
        json.dump(dict(meta=meta, items=out, changes=changes), f, indent=1)
    md = ["# 110-item closure register, run006 (22 Oct 2026, current)", "",
          f"Base: run005 (unchanged). Count {len(out)}/110. Tiers: {tiers}. {len(changes)} rows updated; see CHANGES.md.", "",
          "| ID | Title | Live status | Tier | Disposition | Wave / trigger | Reopen / kill rule |", "|---|---|---|---|---|---|---|"]
    for x in out:
        rule = x["reopen_rule"] + (f" [{x['note']}]" if x.get("note") else "")
        md.append(f"| {x['id']} | {x['title']} | {x['live_status']} | {x['tier']} | {x['disposition']} | "
                  f"{x['wave_or_trigger']} | {rule} |")
    with open(OUT / "REGISTER.md", "x", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(OUT / "CHANGES.md", "x", encoding="utf-8") as f:
        f.write("# Register run006: changes from run005\n\nEvidence: " + EV + "\n\n" + "\n".join(
            f"- **{c['id']}**: " + "; ".join(f"{k}: {c['before'].get(k, '-')} -> {v}" if k in ("tier", "live_status")
                                             else f"{k} updated" for k, v in c["after"].items()) for c in changes) + "\n")
    print(json.dumps(dict(tiers=tiers, changed=len(changes))))


if __name__ == "__main__":
    main()
