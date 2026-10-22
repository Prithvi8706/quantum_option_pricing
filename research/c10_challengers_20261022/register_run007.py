"""Register run007 = run006 (unchanged) + float32-GEMM challenger (headline run006) and the r3 review (22 Oct 2026). Explicit deltas only.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/register_run007.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN2 = ROOT / "results/plan110_w0/register/run006/register.json"
OUT = ROOT / "results/plan110_w0/register/run007"
EV = "docs/c10_challengers_20261022/STATUS.md; results/c10_challengers_20261022/; " \
     "results/frontier_probe_20261021/headline/run003/headline_table.json"
DISP = {"T1": "decision-critical (W0 done)", "T2": "credited screen value / branch-A lever",
        "T3": "deferred certification debt", "T4": "closed or folded into N1", "T5": "dormant until trigger",
        "T6": "parked: different task (TRIG-G0)"}
EV = EV + "; results/c10_challengers_20261022/c09/; results/c10_challengers_20261022/h16_fast/run001/; "           "results/frontier_probe_20261021/headline/run004/headline_table.json; derived/run002/derived.json"
EV4 = ("docs/plan110_status_20261022/CURRENT_NUMBERS.md; results/frontier_probe_20261021/headline/run006/headline_table.json; "
       "results/c10_challengers_20261022/timing_f32/run001/; results/c10_challengers_20261022/f32/run001.json; "
       "results/frontier_probe_20261021/review/r3_review.jsonl")
DELTAS = {
    "C10": dict(reopen_rule="Adopted: fast preint (same estimand) and, at B8x52 $0.001, float32 GEMM (passes eps/10; 1.22x). "
                "Primary T_C at the binding cell 8.89 s (Stage C 22.53 s). Killed: CV under RQMC, two-direction smoothing, "
                "F06, F07. Untried: GPU, PDE/sparse grids, MLMC/MIMC, surrogates.", evidence=EV4),
    "F31": dict(reopen_rule="Master ledger, headline run006 (current): minimum explicit M 26.1 (window), 588 (canonical), "
                "2,032 (certified today); all-free 1.30; 1 lane 2.71; symmetric 1.50; two departures 0.075.", evidence=EV4),
    "C14": dict(reopen_rule="Run006: no single favourable departure reaches M <= 1 for any explicit class (closest: window "
                "all-free 1.30); two departures do (all-free + symmetric 0.075).", evidence=EV4),
    "F05": dict(reopen_rule="Under the window class (run006): free loader alone about 13.8, loader + free exponential 2.45, "
                "all-free 1.30; M <= 1 needs D_eff <= 88 layers (p3/run006).", evidence=EV4),
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
            r3["updated"] = "run007 (22 Oct 2026, f32 + r3)"
            changes.append(dict(id=r["id"], before={k: v for k, v in before.items() if v is not None}, after=d))
        out.append(r3)
    tiers = {k: sum(x["tier"] == k for x in out) for k in DISP}
    meta = dict(script="research/c10_challengers_20261022/register_run007.py", python=sys.version, base="run006",
                base_sha256=hashlib.sha256(RUN2.read_bytes()).hexdigest(), count=len(out), tiers=tiers, changed=len(changes))
    with open(OUT / "register.json", "x", encoding="utf-8") as f:
        json.dump(dict(meta=meta, items=out, changes=changes), f, indent=1)
    md = ["# 110-item closure register, run007 (22 Oct 2026, current)", "",
          f"Base: run006 (unchanged). Count {len(out)}/110. Tiers: {tiers}. {len(changes)} rows updated; see CHANGES.md.", "",
          "| ID | Title | Live status | Tier | Disposition | Wave / trigger | Reopen / kill rule |", "|---|---|---|---|---|---|---|"]
    for x in out:
        rule = x["reopen_rule"] + (f" [{x['note']}]" if x.get("note") else "")
        md.append(f"| {x['id']} | {x['title']} | {x['live_status']} | {x['tier']} | {x['disposition']} | "
                  f"{x['wave_or_trigger']} | {rule} |")
    with open(OUT / "REGISTER.md", "x", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(OUT / "CHANGES.md", "x", encoding="utf-8") as f:
        f.write("# Register run007: changes from run006\n\nEvidence: " + EV + "\n\n" + "\n".join(
            f"- **{c['id']}**: " + "; ".join(f"{k}: {c['before'].get(k, '-')} -> {v}" if k in ("tier", "live_status")
                                             else f"{k} updated" for k, v in c["after"].items()) for c in changes) + "\n")
    print(json.dumps(dict(tiers=tiers, changed=len(changes))))


if __name__ == "__main__":
    main()
