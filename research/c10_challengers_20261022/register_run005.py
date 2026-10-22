"""Register run005 = run004 (unchanged) + C03 skeleton, H18 desk condition, TRIG-HWACT correction (22 Oct 2026). Explicit deltas only.
Run (repo root): .context/frontier_t0_env/Scripts/python.exe -I -S -B research/c10_challengers_20261022/register_run005.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN2 = ROOT / "results/plan110_w0/register/run004/register.json"
OUT = ROOT / "results/plan110_w0/register/run005"
EV = "docs/c10_challengers_20261022/STATUS.md; results/c10_challengers_20261022/; " \
     "results/frontier_probe_20261021/headline/run003/headline_table.json"
DISP = {"T1": "decision-critical (W0 done)", "T2": "credited screen value / branch-A lever",
        "T3": "deferred certification debt", "T4": "closed or folded into N1", "T5": "dormant until trigger",
        "T6": "parked: different task (TRIG-G0)"}
EV = EV + "; results/c10_challengers_20261022/c09/; results/c10_challengers_20261022/h16_fast/run001/; "           "results/frontier_probe_20261021/headline/run004/headline_table.json; derived/run002/derived.json"
EV2 = "docs/c03_skeleton_20261022/C03_SKELETON.md; results/frontier_probe_20261021/headline/run004/headline_table.json"
HW = ("TRIG-HWACT NOT fired after C10 (window M 23.1 > 10 at 100 ns); the run002 marginal flag is withdrawn. "
      "Hardware architecture items stay dormant.")
DELTAS = {
    "C03": dict(live_status="partial (skeleton frozen 22 Oct)", wave_or_trigger="A3; trigger fired (miss 23.1 <= 30); "
                "skeleton frozen", reopen_rule="Skeleton frozen with explicit unknown rows: estimator 0.003 of the 0.01 "
                "certified (window, P2); 0.007 unallocated across the U1 mean certificate, the source/financial bridge "
                "and physical failures; bias reserve 0.55 eps with 4.73e-4 modelled (A02/A07/A13 debt). Completing it "
                "is claim-grade work needing authorization.", evidence=EV2),
    "E07": dict(reopen_rule="Favourable-ledger trigger not fired after C10 (all-free + window 1.15). Its 4 open "
                "obligations map onto C03 rows B2-B4 and A2b/A2c (unknown).", evidence=EV2),
    "H18": dict(live_status="ready (desk condition computed)", wave_or_trigger="A3; G3 count fixed by P2 (N = 100,924)",
                reopen_rule="Desk necessary condition: 2.32e13 T and 2.32e15 qubit-layers per estimate at the binding "
                "cell, so a physical-failure share of 0.001-0.006 needs <= 4.3e-17 to 2.6e-16 logical failure per T gate "
                "(<= 4.3e-19 to 2.6e-18 per qubit-layer). Recompute if N or D_eff changes.", evidence=EV2),
}
for _i in ("H04", "H05", "H06", "H07", "H08", "H09", "H10", "H11", "H13", "H17"):
    DELTAS[_i] = dict(trigger_fired=[], note=HW)


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
            r3["updated"] = "run005 (22 Oct 2026, C03/H18)"
            changes.append(dict(id=r["id"], before={k: v for k, v in before.items() if v is not None}, after=d))
        out.append(r3)
    tiers = {k: sum(x["tier"] == k for x in out) for k in DISP}
    meta = dict(script="research/c10_challengers_20261022/register_run005.py", python=sys.version, base="run004",
                base_sha256=hashlib.sha256(RUN2.read_bytes()).hexdigest(), count=len(out), tiers=tiers, changed=len(changes))
    with open(OUT / "register.json", "x", encoding="utf-8") as f:
        json.dump(dict(meta=meta, items=out, changes=changes), f, indent=1)
    md = ["# 110-item closure register, run005 (22 Oct 2026, after C10, C09, H16, C03/H18)", "",
          f"Base: run004 (unchanged). Count {len(out)}/110. Tiers: {tiers}. {len(changes)} rows updated; see CHANGES.md.", "",
          "| ID | Title | Live status | Tier | Disposition | Wave / trigger | Reopen / kill rule |", "|---|---|---|---|---|---|---|"]
    for x in out:
        rule = x["reopen_rule"] + (f" [{x['note']}]" if x.get("note") else "")
        md.append(f"| {x['id']} | {x['title']} | {x['live_status']} | {x['tier']} | {x['disposition']} | "
                  f"{x['wave_or_trigger']} | {rule} |")
    with open(OUT / "REGISTER.md", "x", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(OUT / "CHANGES.md", "x", encoding="utf-8") as f:
        f.write("# Register run005: changes from run004\n\nEvidence: " + EV + "\n\n" + "\n".join(
            f"- **{c['id']}**: " + "; ".join(f"{k}: {c['before'].get(k, '-')} -> {v}" if k in ("tier", "live_status")
                                             else f"{k} updated" for k, v in c["after"].items()) for c in changes) + "\n")
    print(json.dumps(dict(tiers=tiers, changed=len(changes))))


if __name__ == "__main__":
    main()
