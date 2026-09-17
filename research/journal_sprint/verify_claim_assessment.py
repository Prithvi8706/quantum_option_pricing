"""Verify complete secondary-analysis archives, source identity and recomputation."""

import argparse
import json
from pathlib import Path

from .claim_assessment import analyze
from .storage import ROOT, sha256, write_json


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def within(root, name):
    target = (root/name).resolve()
    if root.resolve() not in target.parents:
        raise ValueError("path escapes root")
    return target


def verify_archive(path):
    expected = {"planned.json", "inputs.json", "results.json"}
    if {p.name for p in path.iterdir()} != expected | {"complete.json"}:
        raise ValueError("archive inventory differs")
    manifest = read(path/"complete.json")["sha256"]
    if set(manifest) != expected:
        raise ValueError("manifest inventory differs")
    for name, digest in manifest.items():
        if sha256(within(path, name)) != digest:
            raise ValueError("artifact hash mismatch")
    planned = read(path/"planned.json")
    for name, digest in planned["source_sha256"].items():
        if sha256(within(ROOT, name)) != digest:
            raise ValueError("source hash mismatch: "+name)
    protocol = ROOT/"docs/journal_sprint/CLAIM_ASSESSMENT_PROTOCOL_20260917.md"
    if sha256(protocol) != planned["config"]["protocol_sha256"]:
        raise ValueError("protocol mismatch")
    inputs = read(path/"inputs.json")
    if set(inputs["paths"]) != {"production", "authoritative", "tiny"}:
        raise ValueError("input inventory differs")
    data = {}
    for key, name in inputs["paths"].items():
        target = within(ROOT, name)
        if sha256(target) != inputs["sha256"][key]:
            raise ValueError("input hash mismatch")
        data[key] = read(target)
    recomputed = analyze(**data)
    if recomputed != read(path/"results.json"):
        raise ValueError("analysis differs from recomputation")
    return {"sources_checked": len(planned["source_sha256"]), "artifacts_checked": 3,
            "inputs_checked": 3, "recomputed": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("first", type=Path)
    parser.add_argument("replay", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    checks = [verify_archive(p) for p in (args.first, args.replay)]
    for name in ("results.json", "inputs.json"):
        if read(args.first/name) != read(args.replay/name):
            raise ValueError("replay mismatch")
    write_json(args.output, {"passed": True, "checks": checks,
                            "exact_replay": True, "verifier_sha256": sha256(Path(__file__)),
                            "scope": "secondary numerical reanalysis; not independent expert signoff"})
    print("Both archives verified; numerical analysis exactly reproduced.")


if __name__ == "__main__":
    main()
