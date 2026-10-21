"""Create a read-only, snapshot-bound planning inventory; execute no experiments."""
from __future__ import annotations

import csv
import hashlib
import io
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs/independent_110_20261004/inventory_run001"
RESULTS = ROOT / "results/independent_110_20261004/inventory_run001"
INPUTS = {
    "progress": ROOT / "results/limitation_program_20261001/progress.json",
    "roadmap": ROOT / "docs/limitation_audit_20261001/implementation_plan/roadmap.json",
    "reservation": ROOT / ".context/parallel_110_chat_reservation_20261004.json",
}
PROTECTED = {"A13", "A14", "A20", "E12", "F31", "F03", "F32"}
GROUPS = {
    "reserved_elsewhere": {"F03", "F31", "F32"},
    "overlap_hold": {"E10", "E11", "E23", "F04", "F06", "F20", "C14"},
    "timing_hold": {"F01", "F07", "H16"},
    "new_contract_required": {"E18", "E19", "F09", "F21", "F22", "F26", "F27", "F28", "F29"},
    "local_prerequisite_chain": {"F05", "F19", "H01", "H02", "H04", "H08", "H10", "H14", "C08", "C10"},
}
FIRST = ["C15", "E01", "F18", "F13", "H03", "F08", "F16", "C12", "E08"]
NOTES = {
    "C05": "Analyze alternatives against a frozen original ledger only; do not change active error or confidence allocations.",
    "C12": "Map completed evidence and shared modules; defer verifier replacement and shared source edits.",
    "C15": "Audit exact versions, locators and cost boundaries of stable archived claims; keep corrections in new local files.",
    "E01": "Access-model cards for the unchanged single-price source; omit protected basket QSP, smoothness, walks and crossover redesign.",
    "E08": "Exact allocation arithmetic on frozen E02/E07 stage geometry; do not redesign E12 stopping or confidence.",
    "E09": "Review one unknown-variance controller on the specified bounded toy; no E12 acquisition or finance promotion.",
    "E14": "Fixed D=1 nested schedule and theorem assumptions; no protected source changes.",
    "E15": "Independent coherent two-state toy/controller reversibility audit; keep shared implementations read-only.",
    "E16": "Existing scalar lognormal moment/tail and three-construction cost screen; keep parity moment acquisition with E12.",
    "E17": "Relevance/moment audit for current workloads; do not invent a new heavy-tail contract.",
    "E20": "P=1,2,4 lane-memory/schedule screen for one frozen compatible source; missing physical inputs remain unresolved.",
    "E25": "Amplitude-design coverage theorem review and exact-law diagnostic plan; no E12 residual sampling redesign.",
    "F08": "Finite tilted single-indicator identity and normalization first; do not compile a new sampler yet.",
    "F10": "Archived multilevel allocation analysis with original frozen source costs; no pending arithmetic gains or concurrent timings.",
    "F11": "Derive two coarse controls first; postpone matched performance acquisition until timing ownership is clear.",
    "F12": "Freeze existing S4 parameters and audit coupling/bias assumptions first; no matched timing claims.",
    "F13": "S4 square-root-boundary theorem hypothesis map; no path simulations needed for this first step.",
    "F14": "Existing one-asset A1 exact-transition primitive and assumption inventory; no new workload or quantum emission yet.",
    "F15": "A1 negative-leverage tail/truncation proof; retain the failed direct theorem transfer without rerunning it.",
    "F16": "Prove the existing GBM future-factor reuse identity; no new model and no duplicate walk audit.",
    "F17": "Continuation-boundary bounds for the existing fixed policy; do not retrain it or alter E12's sampling contract.",
    "F18": "Compound-contract nesting, Lipschitz and error-norm theorem map; leave E12 moment/CS questions to its owner.",
    "F23": "Covariance omission-error proof on frozen B4/B8 laws; no shared basis/kernel edits or F03 integrand experiments.",
    "F24": "Specify the existing one-asset development Asian/barrier PDE; retain its separate development-task label.",
    "F25": "Audit the nominated forward-PDE normalization/overlap formula before any state evolution.",
    "F30": "Freeze the existing development integrand and rank-screen protocol first; no timed contraction-versus-loader acquisition yet.",
    "H03": "Reaction-dependency timeline for an original frozen F40 leaf/chain; exclude new A14 arithmetic and speedup claims.",
    "H07": "One archived adder gate-set translation and finite noise-assumption audit; no source adoption.",
    "H09": "Frozen source storage/active-logic/interface accounting; no substitution without a valid finite interface.",
    "H11": "One finite addressable-CCZ parameter/implementation audit; missing timings stay unresolved.",
    "H12": "Finite constants and construction audit; no asymptotic constant substituted as measured overhead.",
    "H13": "One original multiplier/chain active-volume mapping; keep the F31 crossover decision ledger with its owner.",
    "E10": "Hold: active E12 completion/fallback work examines the same C4 analytic global moment bound.",
    "E11": "Hold: requires E10 and overlaps E12 fallback moment/source-transfer accounting.",
    "E23": "Hold current signal/QSP work to avoid A20; a separately frozen distinct factor could later be reviewed.",
    "F04": "Hold: declared dependency on protected F03 smoothness assumptions and derivative certificates.",
    "F06": "Hold: barrier active-date switching and transforms overlap protected F03's integrand analysis.",
    "F20": "Hold conservatively: parity source-plus-estimator costing overlaps E12's fallback decision.",
    "C14": "Hold: same complete-time crossover question as protected F31.",
    "F01": "Archived slope/error extraction is permissible; next-size time-to-accuracy acquisition is deferred.",
    "F07": "Proposal protocol/archived review only; matched training/validation performance runs are deferred.",
    "H16": "Classical worker-scaling timing is deferred; C09 Stage C work remains owned elsewhere.",
    "F05": "Requires a frozen F01 comparator/interface first; no competing classical timing run.",
    "F19": "Follow F18's theorem/contract interface; do not hide deterministic depth constants.",
    "H01": "Follow C15's versioned timing anchors; no shared hardware ledger edits.",
    "H02": "Follow H01's endpoint-defined hardware timings.",
    "H04": "Follow H03's circuit/reaction interface; retain unresolved H18 fault inputs.",
    "H08": "Follow H07's usable finite gate/noise interface; retain unresolved H17/H18 inputs.",
    "H10": "Follow H09's finite memory-to-logic interface.",
    "H14": "Follow H13's active-volume/feedback chain interface.",
    "C08": "Requires F01's archived-error/fit interface; no new Stage C measurements.",
    "C10": "Requires F01's applicability/comparator interface; an initial paper applicability matrix is read-only.",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    if DOCS.exists() or RESULTS.exists():
        raise ValueError("Fresh list directories required; existing inventory is immutable.")
    captured = {key: path.read_bytes() for key, path in INPUTS.items()}
    parsed = {key: json.loads(data) for key, data in captured.items()}
    progress = parsed["progress"]["entries"]
    roadmap = {item["id"]: item for item in parsed["roadmap"]["entries"]}
    unstarted = {
        key for key, item in progress.items()
        if item.get("execution_status", "").strip().lower() == "not started"
    }
    reservation = parsed["reservation"]
    assert PROTECTED == set(reservation["main_chat_reserved_items"]) | set(reservation["separate_chat_suggested_items_in_order"])
    assigned = set()
    for group in GROUPS.values():
        assert not assigned & group
        assigned |= group
    assert assigned <= unstarted
    groups = {name: set(ids) for name, ids in GROUPS.items()}
    groups["independent_first_step"] = unstarted - assigned
    assert len(unstarted) == 64, "Changed ledger membership requires a new reviewed list version."
    assert len(groups["independent_first_step"]) == 32
    assert set(FIRST) <= groups["independent_first_step"]
    assert set().union(*groups.values()) == unstarted

    def ancestors(key: str, seen: set[str] | None = None) -> set[str]:
        seen = set() if seen is None else seen
        for dependency in roadmap[key].get("depends_on", []):
            if dependency not in seen:
                seen.add(dependency)
                if dependency in roadmap:
                    ancestors(dependency, seen)
        return seen

    rows = []
    for key in sorted(unstarted):
        item = roadmap[key]
        category = next(name for name, ids in groups.items() if key in ids)
        protected_ancestors = sorted(ancestors(key) & PROTECTED)
        if category == "independent_first_step":
            assert key not in PROTECTED and not protected_ancestors
        note = NOTES.get(key)
        if note is None and category == "reserved_elsewhere":
            note = "Reserved for the other chat; do not start or duplicate it."
        if note is None and category == "new_contract_required":
            note = "Dormant until a separately justified financial model/output contract is selected; no new workload is authorized by this list."
        assert note is not None, key
        rows.append({
            "item": key, "title": item["title"], "category": category,
            "recommended_order": FIRST.index(key) + 1 if key in FIRST else "",
            "plan_priority": item.get("priority"),
            "ledger_execution_status": progress[key]["execution_status"],
            "declared_inputs": item.get("depends_on", []),
            "unstarted_direct_inputs": [d for d in item.get("depends_on", []) if d in unstarted],
            "protected_ancestors": protected_ancestors,
            "independent_scope_or_hold_reason": note,
            "roadmap_next_action": item.get("next_action", ""),
            "existing_evidence": item.get("existing_evidence", []),
            "stopping_rule": item.get("stop_rule", ""),
        })
    DOCS.mkdir(parents=True)
    RESULTS.mkdir(parents=True)
    for key, data in captured.items():
        (RESULTS / f"{key}_snapshot.json").write_bytes(data)
    fields = ["item", "title", "category", "recommended_order", "plan_priority", "declared_inputs", "unstarted_direct_inputs", "protected_ancestors", "independent_scope_or_hold_reason", "roadmap_next_action"]
    for name, selected in [
        ("INDEPENDENT_FIRST_STEPS.csv", [r for r in rows if r["category"] == "independent_first_step"]),
        ("ALL_NOT_STARTED.csv", rows),
    ]:
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in selected:
            writer.writerow({k: "; ".join(v) if isinstance(v, list) else v for k, v in row.items()})
        (DOCS / name).write_text(stream.getvalue(), encoding="utf-8-sig", newline="")
    policy = [
        "This inventory starts no work and creates no new reservation.",
        "Protect A13, A14, A20, E12, F31, F03 and F32 while ownership is mixed.",
        "Independent means an initial bounded proof/accounting/protocol step can use existing frozen inputs; it does not mean every dependency interface or whole item is complete.",
        "Keep shared sources, receipts, expected hashes, progress, STATUS, README and manuscript read-only.",
        "Put future work only under research/independent_110_20261004/, docs/independent_110_20261004/ and results/independent_110_20261004/ in fresh per-item directories.",
        "Use frozen original source families and budgets; do not import pending A13/A14/A20 improvements or revise active error/confidence allocations.",
        "No competing Stage C or matched performance runs during concurrent work; administrative clocks are not matched timings.",
        "Before any future experiment freeze corpus, assumptions, acceptance criteria, budgets and stopping rule; preserve failed attempts.",
        "Follow the roadmap's bounded screen and required input interfaces. If an interface is missing, record it and move to another independent proof step.",
        "No financial-contract changes, commits, pushes, uploads, publishing, cloud execution or messages to others.",
        "Recheck the live ledger and ownership before executing a listed item; this file is a dated snapshot, not a scheduler lock.",
    ]
    created = datetime.now(timezone.utc).isoformat()
    inventory = {
        "schema": "independent-not-started-inventory-v1", "created_utc": created,
        "local_only": True, "experiments_executed": 0, "test_credit": 0,
        "source_files": {key: {"path": rel(INPUTS[key]), "sha256": sha(data)} for key, data in captured.items()},
        "membership_rule": "execution_status stripped and lowercased equals 'not started' in captured progress",
        "protected_items": sorted(PROTECTED), "count": len(rows),
        "category_counts": dict(Counter(r["category"] for r in rows)),
        "recommended_order": FIRST,
        "follow_on_chains": ["C15 -> H01 -> H02", "H03 -> H04", "H07 -> H08", "H09 -> H10", "H13 -> H14", "F18 -> F19"],
        "policy": policy, "items": rows,
        "checks": {
            "all64_members_bound_to_captured_ledger": True,
            "groups_disjoint_and_exhaustive": True,
            "independent32_have_no_declared_protected_ancestor": True,
            "all_independent_titles_and_next_actions_from_roadmap": True,
            "recommended9_are_independent_members": True,
            "shared_files_written_by_this_script": [],
        },
    }
    dump(RESULTS / "inventory.json", inventory)
    lines = [
        "UNSTARTED IMPLEMENTATION-PLAN WORK: INDEPENDENT FIRST STEPS",
        f"Captured UTC: {created}",
        "64 untouched items: 32 independent initial steps, 10 prerequisite-chain items, 7 overlap holds, 3 timing holds, 9 dormant new-contract branches, 3 reserved items.",
        "", "RECOMMENDED FIRST NINE",
    ]
    for n, key in enumerate(FIRST, 1):
        lines.append(f"{n}. {key}: {roadmap[key]['title']}")
    lines += ["", "ALL 32 INDEPENDENT INITIAL STEPS"]
    for prefix in ["E", "F", "H", "C"]:
        for row in rows:
            if row["item"].startswith(prefix) and row["category"] == "independent_first_step":
                lines.append(f"{row['item']}: {row['title']} | {row['independent_scope_or_hold_reason']}")
    for category in ["local_prerequisite_chain", "overlap_hold", "timing_hold", "new_contract_required", "reserved_elsewhere"]:
        lines += ["", category.upper()]
        lines += [f"{r['item']}: {r['independent_scope_or_hold_reason']}" for r in rows if r["category"] == category]
    lines += ["", "OPERATING RULES"] + [f"- {p}" for p in policy]
    (DOCS / "WORK_LIST.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    changed = [key for key, path in INPUTS.items() if sha(path.read_bytes()) != sha(captured[key])]
    dump(RESULTS / "verification.json", {
        "passed": True, "scope": "Planning inventory consistency only; no scientific tests or task completion.",
        "checks": inventory["checks"], "shared_inputs_changed_during_capture": changed,
        "source_snapshot_remains_authoritative": True,
    })
    owned = [p for directory in [DOCS, RESULTS] for p in directory.iterdir() if p.is_file()]
    dump(RESULTS / "manifest.json", {
        "schema": "local-planning-inventory-manifest-v1", "created_utc": created,
        "author": {"path": rel(Path(__file__).resolve()), "sha256": sha(Path(__file__).read_bytes())},
        "files": {rel(path): {"sha256": sha(path.read_bytes()), "bytes": path.stat().st_size} for path in sorted(owned)},
    })
    print(json.dumps({"passed": True, "category_counts": inventory["category_counts"], "list": rel(DOCS / "WORK_LIST.txt"), "experiments_executed": 0}))


if __name__ == "__main__":
    main()
