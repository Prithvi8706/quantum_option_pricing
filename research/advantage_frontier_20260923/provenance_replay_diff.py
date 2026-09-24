"""Diff archived advantage-frontier outputs against a replay from the committed scripts.

Usage: provenance_replay_diff.py <replay_checkout_root> [<archive_root>]
Compares every JSON field recursively. Fields whose key names indicate wall-clock timing
(and fields derived from timing: classical seconds, D_max, ratios, stop-rule margins) are
reported as re-measurement fields, not as mismatches. Everything else must match exactly.
Writes results/advantage_frontier_20260923/provenance_replay_20260924.json in the archive.
"""

import json
import os
import sys

FILES = ["classical_exponent_pilot.json", "barrier_oss_pilot.json",
         "barrier_fast_classical.json", "barrier_oracle_depth.json",
         "barrier_decision.json", "frontier.json"]
TIMING = ("second", "acquisition", "wall", "elapsed", "per_point", "sec_", "t_c",
          "d_max", "dmax", "ratio", "classical_seconds", "max_seconds_per_call",
          "max_t_depth_per_call", "eps_for_d", "stop", "decision", "python", "numpy",
          "platform", "processor", "numba", "purpose", "cpu_count")


def timing_key(path):
    low = path.lower()
    return any(t in low for t in TIMING)


def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            walk(a.get(k), b.get(k), f"{path}/{k}", out)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, f"{path}[{i}]", out)
    else:
        kind = "timing" if timing_key(path) else "exact"
        out[kind]["compared"] += 1
        if a != b:
            out[kind]["differ"].append(path)


def main():
    replay = sys.argv[1]
    archive = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..")
    report = {}
    for name in FILES:
        a = json.load(open(os.path.join(archive, "results", "advantage_frontier_20260923", name)))
        b = json.load(open(os.path.join(replay, "results", "advantage_frontier_20260923", name)))
        out = {"exact": {"compared": 0, "differ": []}, "timing": {"compared": 0, "differ": []}}
        walk(a, b, "", out)
        report[name] = {"exact_fields": out["exact"]["compared"],
                        "exact_mismatches": out["exact"]["differ"],
                        "timing_fields": out["timing"]["compared"],
                        "timing_fields_changed": len(out["timing"]["differ"])}
        print("%-32s exact %5d fields, %3d mismatches; timing-derived %5d fields, %4d changed"
              % (name, out["exact"]["compared"], len(out["exact"]["differ"]),
                 out["timing"]["compared"], len(out["timing"]["differ"])))
        for p in out["exact"]["differ"][:10]:
            print("   MISMATCH", p)
    dest = os.path.join(archive, "results", "advantage_frontier_20260923",
                        "provenance_replay_20260924.json")
    with open(dest, "w") as f:
        json.dump(dict(purpose=__doc__, replay_root=os.path.abspath(replay), files=report), f,
                  indent=1)
    print("wrote", dest)


if __name__ == "__main__":
    main()
