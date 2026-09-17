"""Strict numerical replay; only explicitly named timing fields are excluded."""

import argparse
import json
from pathlib import Path
from .run_normalization_approximation import CONFIG, SOURCES
from .storage import ROOT, sha256, write_json


def without_timings(name, payload):
    if name == "moments.json":
        for record in payload.values():
            record.pop("elapsed_seconds")
    elif name == "controls.json":
        for family in payload.values():
            for record in family["by_precision"].values():
                record.pop("elapsed_seconds")
    return payload


def verify(first, replay, receipt):
    expected = {"planned.json", "model.json", "signal_plans.json", "loader.json",
                "encoding.json", "moments.json", "controls.json", "results.json"}
    expected |= {f"{kind}_{d}.json" for kind in ("truncated", "minimax") for d in CONFIG["degrees"]}
    roots, checked = [Path(first), Path(replay)], 0
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
        left, right = [without_timings(name, json.loads((root/name).read_text())) for root in roots]
        if left != right:
            raise ValueError(f"numeric replay mismatch: {name}")
    write_json(receipt, dict(exact_numeric_payloads=payloads, hashes_checked=checked,
               excluded_timings=["moments.*.elapsed_seconds", "controls.*.by_precision.*.elapsed_seconds"],
               manifests={str(root): sha256(root/"complete.json") for root in roots},
               verifier_sha256=sha256(Path(__file__)),
               qualification="same-producer separate-environment replay, not independent scientific validation"))
    print(f"{len(payloads)} numeric payloads, {checked} hashes checked", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("first")
    parser.add_argument("replay")
    parser.add_argument("receipt")
    args = parser.parse_args()
    verify(args.first, args.replay, args.receipt)
