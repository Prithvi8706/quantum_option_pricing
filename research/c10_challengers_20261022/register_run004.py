"""Register run004 = run003 (unchanged) + C09 measured and H16 re-measured (22 Oct 2026). Explicit deltas only.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/register_run004.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN2 = ROOT / "results/plan110_w0/register/run003/register.json"
OUT = ROOT / "results/plan110_w0/register/run004"
EV = "docs/c10_challengers_20261022/STATUS.md; results/c10_challengers_20261022/; " \
     "results/frontier_probe_20261021/headline/run003/headline_table.json"
DISP = {"T1": "decision-critical (W0 done)", "T2": "credited screen value / branch-A lever",
        "T3": "deferred certification debt", "T4": "closed or folded into N1", "T5": "dormant until trigger",
        "T6": "parked: different task (TRIG-G0)"}
EV = EV + "; results/c10_challengers_20261022/c09/; results/c10_challengers_20261022/h16_fast/run001/; "           "results/frontier_probe_20261021/headline/run004/headline_table.json; derived/run002/derived.json"
DELTAS = {
    "C09": dict(live_status="complete for the decision cells (measured)", wave_or_trigger="C09 measured 22 Oct",
                reopen_rule="Timed successful distribution-free 99% prices (empirical Bernstein, R = 17.30 from the probe's "
                            "analytic bound) in all four decision cells; measured same-state factors 33.8 (B8x52 $0.001), "
                            "37.6, 16.1, 10.3 (N1 modelled 36.9, 40.3, 18.9, 10.6). Symmetric-convention M now measured: "
                            "window 0.684 with U1/U2, 1.22 without U1. Reopen if T_C or the estimator changes.", evidence=EV),
    "H16": dict(reopen_rule="Done; re-measured 22 Oct with the C10 fast method: 1/16-worker ratio 9.62 (B8x52 $0.001), "
                            "9.89, 8.86, 11.03 (same-state; 1 lane vs 1 core window M 2.40).", evidence=EV),
    "F31": dict(reopen_rule="Master ledger, headline run004 (all measured inputs): minimum explicit M 23.1 (window), 521 "
                            "(canonical), 1,800 (certified today); all-free 1.15; 1 lane vs 1 core 2.40; symmetric 0.684 "
                            "(1.22 without U1).", evidence=EV),
    "C14": dict(reopen_rule="Run004: minimum miss at the primary corner 23.1 / 19.4 (failure 0.003 / 0.01). The scoped "
                            "negative holds at every 100 ns corner except the symmetric distribution-free convention, and "
                            "there only with the U1 orientation-price credit (0.684; 1.22 without U1).", evidence=EV),
    "C10": dict(reopen_rule="Wave 1 adopted the fast preint (2.25x; primary T_C 10.03 s). C09/H16 re-measured with it. "
                            "Killed: CV under RQMC, two-direction smoothing, F06, F07. Untried: GPU, PDE/sparse grids, "
                            "MLMC/MIMC, surrogates.", evidence=EV),
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
            r3["updated"] = "run004 (22 Oct 2026, C09/H16 measured)"
            changes.append(dict(id=r["id"], before={k: v for k, v in before.items() if v is not None}, after=d))
        out.append(r3)
    tiers = {k: sum(x["tier"] == k for x in out) for k in DISP}
    meta = dict(script="research/c10_challengers_20261022/register_run004.py", python=sys.version, base="run003",
                base_sha256=hashlib.sha256(RUN2.read_bytes()).hexdigest(), count=len(out), tiers=tiers, changed=len(changes))
    with open(OUT / "register.json", "x", encoding="utf-8") as f:
        json.dump(dict(meta=meta, items=out, changes=changes), f, indent=1)
    md = ["# 110-item closure register, run004 (22 Oct 2026, after C10, C09 and H16)", "",
          f"Base: run003 (unchanged). Count {len(out)}/110. Tiers: {tiers}. {len(changes)} rows updated; see CHANGES.md.", "",
          "| ID | Title | Live status | Tier | Disposition | Wave / trigger | Reopen / kill rule |", "|---|---|---|---|---|---|---|"]
    for x in out:
        rule = x["reopen_rule"] + (f" [{x['note']}]" if x.get("note") else "")
        md.append(f"| {x['id']} | {x['title']} | {x['live_status']} | {x['tier']} | {x['disposition']} | "
                  f"{x['wave_or_trigger']} | {rule} |")
    with open(OUT / "REGISTER.md", "x", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(OUT / "CHANGES.md", "x", encoding="utf-8") as f:
        f.write("# Register run004: changes from run003\n\nEvidence: " + EV + "\n\n" + "\n".join(
            f"- **{c['id']}**: " + "; ".join(f"{k}: {c['before'].get(k, '-')} -> {v}" if k in ("tier", "live_status")
                                             else f"{k} updated" for k, v in c["after"].items()) for c in changes) + "\n")
    print(json.dumps(dict(tiers=tiers, changed=len(changes))))


if __name__ == "__main__":
    main()
