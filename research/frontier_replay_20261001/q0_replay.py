"""Q0: provenance replay of the six advantage-frontier scripts in the T0 environment.

Usage, from the repository root: python research/frontier_replay_20261001/q0_replay.py <commit>
Creates a detached worktree of <commit>, runs the six committed scripts there with the T0
interpreter in the 24 September order, and diffs the regenerated JSON against the archive
with the unchanged 24 September field classification (ANALYSIS_SPEC_STAGE_B.md).
"""

import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research" / "advantage_frontier_20260923"))
from provenance_replay_diff import FILES, walk  # noqa: E402

PY = ROOT / ".context" / "frontier_t0_env" / "Scripts" / "python.exe"
CHECKOUT = ROOT / ".context" / "frontier_q0_replay_20261001"
OUT = ROOT / "results" / "frontier_replay_20261001"
REPORT = OUT / "q0_provenance_replay.json"
ARCHIVE = ROOT / "results" / "advantage_frontier_20260923"
REPLAYED = CHECKOUT / "results" / "advantage_frontier_20260923"
SCRIPTS = [("P3", "barrier_fast_classical.py"), ("P1", "classical_exponent_pilot.py"),
           ("P2", "barrier_oss_pilot.py"), ("Q1", "barrier_oracle_depth.py"),
           ("DEC", "barrier_decision.py"), ("FR", "frontier.py")]


def get_path(obj, path):
    for key, index in re.findall(r"/([^/\[]*)|\[(\d+)\]", path):
        obj = obj[int(index)] if index else (obj or {}).get(key)
    return obj


def run_scripts():
    runs = []
    for label, script in SCRIPTS:
        start = time.time()
        proc = subprocess.run([str(PY), f"research/advantage_frontier_20260923/{script}"],
                              cwd=CHECKOUT, capture_output=True, text=True)
        seconds = round(time.time() - start, 1)
        (OUT / "q0_logs" / f"{label}_{script[:-3]}.log").write_text(proc.stdout + proc.stderr)
        runs.append(dict(label=label, script=script, returncode=proc.returncode, seconds=seconds))
        print(f"{label:4s} exit {proc.returncode} in {seconds} s", flush=True)
    return runs


def compare():
    expected = json.loads((ARCHIVE / "provenance_replay_20260924.json").read_text())["files"]
    files = {}
    for name in FILES:
        archived = json.loads((ARCHIVE / name).read_text())
        replayed = json.loads((REPLAYED / name).read_text())
        out = {"exact": {"compared": 0, "differ": []}, "timing": {"compared": 0, "differ": []}}
        walk(archived, replayed, "", out)
        files[name] = dict(
            exact_fields=out["exact"]["compared"],
            exact_fields_20260924=expected[name]["exact_fields"],
            exact_mismatches=[dict(path=p, archived=get_path(archived, p),
                                   replayed=get_path(replayed, p))
                              for p in out["exact"]["differ"]],
            timing_fields=out["timing"]["compared"],
            timing_fields_changed=len(out["timing"]["differ"]))
        print("%-32s exact %5d (24 Sep %5d), mismatches %d; timing %5d, changed %d"
              % (name, out["exact"]["compared"], expected[name]["exact_fields"],
                 len(out["exact"]["differ"]), out["timing"]["compared"],
                 len(out["timing"]["differ"])))
    return files


def decision(results):
    return json.loads((results / "barrier_decision.json").read_text())["decision"]


def main():
    commit = sys.argv[1]
    if REPORT.exists() or (OUT / "q0_logs").exists():
        raise SystemExit(f"refusing to overwrite {REPORT} or its logs")
    (OUT / "q0_logs").mkdir(parents=True)
    subprocess.run(["git", "worktree", "add", "--detach", str(CHECKOUT), commit], cwd=ROOT,
                   check=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=CHECKOUT, capture_output=True,
                          text=True, check=True).stdout.strip()
    runs = run_scripts()
    files = compare() if all(r["returncode"] == 0 for r in runs) else {}
    report = dict(
        spec="manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_B.md",
        checkout_commit=head, interpreter=str(PY), runs=runs, files=files,
        exact_fields_total=sum(f["exact_fields"] for f in files.values()),
        exact_mismatches_total=sum(len(f["exact_mismatches"]) for f in files.values()),
        decision_archived=decision(ARCHIVE),
        decision_replayed=decision(REPLAYED) if files else None)
    report["q0_passed"] = bool(files) and report["exact_mismatches_total"] == 0 and all(
        f["exact_fields"] == f["exact_fields_20260924"] for f in files.values())
    REPORT.write_text(json.dumps(report, indent=1, default=str) + "\n")
    print("Q0 passed:", report["q0_passed"], "| wrote", REPORT)


if __name__ == "__main__":
    main()
