"""Register run008 = run007 (unchanged) + C10 untried-challenger dispositions and the float32 consistency check (22 Oct 2026). Explicit deltas only.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/register_run008.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN2 = ROOT / "results/plan110_w0/register/run007/register.json"
OUT = ROOT / "results/plan110_w0/register/run008"
EV = "docs/c10_challengers_20261022/STATUS.md; results/c10_challengers_20261022/; " \
     "results/frontier_probe_20261021/headline/run003/headline_table.json"
DISP = {"T1": "decision-critical (W0 done)", "T2": "credited screen value / branch-A lever",
        "T3": "deferred certification debt", "T4": "closed or folded into N1", "T5": "dormant until trigger",
        "T6": "parked: different task (TRIG-G0)"}
EV = EV + "; results/c10_challengers_20261022/c09/; results/c10_challengers_20261022/h16_fast/run001/; "           "results/frontier_probe_20261021/headline/run004/headline_table.json; derived/run002/derived.json"
EV5 = ("docs/c10_challengers_20261022/STATUS.md (untried dispositions); results/c10_challengers_20261022/"
       "f32_consistency/run001/f32_consistency.json; docs/plan110_status_20261022/CURRENT_NUMBERS.md")
DELTAS = {
    "C10": dict(live_status="complete for applicable challengers (22 Oct)", tier="T4",
                wave_or_trigger="CLOSED 22 Oct (C10 wave; label 'strongest tested' kept)",
                reopen_rule="Adopted: fast preint (same estimand) and float32 GEMM at B8x52 $0.001; primary T_C 8.89 s "
                "(Stage C 22.53 s). Killed: CV under RQMC, two-direction smoothing, F06, F07. Desk: PDE/sparse grids "
                "infeasible (8 assets x 52 dates), MLMC/MIMC not applicable (exact dates), surrogates expected ~1x (CV "
                "result). Untested: GPU (no CUDA; q-). Reopen on a new candidate method or a GPU.", evidence=EV5),
    "C09": dict(reopen_rule="Measured, minimum over methods (replicated RQMC, EB, R = 17.30): factor 17.3 (B8x52 $0.001; "
                "17.5 when re-measured with the float32 method), 17.9 (B4x12 $0.001); iid EB 16.1 / 10.3 at $0.01. "
                "Window symmetric M 1.49-1.50 (run006).", evidence=EV5),
    "H16": dict(reopen_rule="Re-measured 22 Oct: 1/16 ratio 9.62 (fast) / 9.56 (float32) at B8x52 $0.001; 9.89, 8.86, "
                "11.03 elsewhere (fast).", evidence=EV5),
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
            r3["updated"] = "run008 (22 Oct 2026, C10 complete)"
            changes.append(dict(id=r["id"], before={k: v for k, v in before.items() if v is not None}, after=d))
        out.append(r3)
    tiers = {k: sum(x["tier"] == k for x in out) for k in DISP}
    meta = dict(script="research/c10_challengers_20261022/register_run008.py", python=sys.version, base="run007",
                base_sha256=hashlib.sha256(RUN2.read_bytes()).hexdigest(), count=len(out), tiers=tiers, changed=len(changes))
    with open(OUT / "register.json", "x", encoding="utf-8") as f:
        json.dump(dict(meta=meta, items=out, changes=changes), f, indent=1)
    md = ["# 110-item closure register, run008 (22 Oct 2026, current)", "",
          f"Base: run007 (unchanged). Count {len(out)}/110. Tiers: {tiers}. {len(changes)} rows updated; see CHANGES.md.", "",
          "| ID | Title | Live status | Tier | Disposition | Wave / trigger | Reopen / kill rule |", "|---|---|---|---|---|---|---|"]
    for x in out:
        rule = x["reopen_rule"] + (f" [{x['note']}]" if x.get("note") else "")
        md.append(f"| {x['id']} | {x['title']} | {x['live_status']} | {x['tier']} | {x['disposition']} | "
                  f"{x['wave_or_trigger']} | {rule} |")
    with open(OUT / "REGISTER.md", "x", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(OUT / "CHANGES.md", "x", encoding="utf-8") as f:
        f.write("# Register run008: changes from run007\n\nEvidence: " + EV + "\n\n" + "\n".join(
            f"- **{c['id']}**: " + "; ".join(f"{k}: {c['before'].get(k, '-')} -> {v}" if k in ("tier", "live_status")
                                             else f"{k} updated" for k, v in c["after"].items()) for c in changes) + "\n")
    print(json.dumps(dict(tiers=tiers, changed=len(changes))))


if __name__ == "__main__":
    main()
