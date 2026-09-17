"""Exact bounded-development replay and immutable source/artifact checks."""

import argparse
import json
from pathlib import Path
from .run_barrier_development import CONFIG, SOURCES
from .storage import ROOT, sha256, write_json


def verify(first, replay, receipt):
    expected = {"planned.json", "signal_plans.json", "tiny_integrated.json", "results.json"}
    expected |= {f"phase_{d}.json" for d in CONFIG["degrees"]}
    checked = 0
    roots = [Path(first), Path(replay)]
    for root in roots:
        if {p.name for p in root.iterdir()} != expected | {"complete.json"}:
            raise ValueError("archive inventory mismatch")
        manifest = json.loads((root/"complete.json").read_text())["sha256"]
        if set(manifest) != expected:
            raise ValueError("manifest inventory mismatch")
        for name, digest in manifest.items():
            if sha256(root/name) != digest:
                raise ValueError("artifact hash mismatch")
            checked += 1
        planned = json.loads((root/"planned.json").read_text())
        if planned["config"] != CONFIG or set(planned["source_sha256"]) != set(SOURCES):
            raise ValueError("configuration/source inventory mismatch")
        for name, digest in planned["source_sha256"].items():
            if sha256(ROOT/name) != digest:
                raise ValueError("source hash mismatch")
            checked += 1
    payloads = sorted(expected-{"planned.json"})
    for name in payloads:
        left, right = [json.loads((root/name).read_text()) for root in roots]
        if left != right:
            raise ValueError(f"numerical payload mismatch: {name}")
    write_json(receipt, dict(exact_numeric_payloads=payloads, hashes_checked=checked,
               manifests={str(root): sha256(root/"complete.json") for root in roots},
               verifier_sha256=sha256(Path(__file__)),
               qualification="same-producer separate-environment replay, not independent mathematical validation"))
    print(f"{len(payloads)} exact numeric payloads, {checked} hashes checked", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("first")
    parser.add_argument("replay")
    parser.add_argument("receipt")
    args = parser.parse_args()
    verify(args.first, args.replay, args.receipt)
