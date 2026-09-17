"""Strict source/inventory and exact numerical replay checks, timings excluded."""

import argparse
import json
from pathlib import Path
from .storage import ROOT, sha256, write_json


def verify(first, replay, receipt, kind):
    if kind == "combined":
        from .run_combined_development import CONFIG, SOURCES
        expected = {"planned.json", "discovery.json", "representations.json", "qsp.json",
                    "integrated_lcu.json", "mps.json", "combined_screen.json"}
        timing = {"discovery.json": ("fwht_seconds", "greedy_seconds")}
    elif kind == "residual":
        from .run_polynomial_residual import CONFIG, SOURCES
        expected = {"planned.json", "moments.json", "synthesis_8.json", "synthesis_16.json",
                    "synthesis_32.json", "results.json"}
        timing = {"moments.json": ("setup_seconds",)}
    else:
        raise ValueError("unknown replay kind")
    roots = [Path(first), Path(replay)]
    checked = 0
    for root in roots:
        if {p.name for p in root.iterdir()} != expected | {"complete.json"}:
            raise ValueError("archive inventory mismatch")
        complete = json.loads((root/"complete.json").read_text())
        if set(complete["sha256"]) != expected:
            raise ValueError("manifest inventory mismatch")
        for name, digest in complete["sha256"].items():
            if sha256(root/name) != digest:
                raise ValueError("artifact hash mismatch")
            checked += 1
        planned = json.loads((root/"planned.json").read_text())
        if planned["config"] != CONFIG or set(planned["source_sha256"]) != set(SOURCES):
            raise ValueError("configuration/source mismatch")
        for name, digest in planned["source_sha256"].items():
            if sha256(ROOT/name) != digest:
                raise ValueError("source hash mismatch")
            checked += 1
    equal = []
    for name in sorted(expected-{"planned.json"}):
        left, right = [json.loads((root/name).read_text()) for root in roots]
        for field in timing.get(name, ()):
            left.pop(field)
            right.pop(field)
        if left != right:
            raise ValueError(f"exact numerical replay mismatch: {name}")
        equal.append(name)
    write_json(receipt, dict(kind=kind, exact_numeric_payloads=equal, excluded_timing_fields=timing,
                            hashes_checked=checked,
                            manifests={str(root): sha256(root/"complete.json") for root in roots},
                            verifier_sha256=sha256(Path(__file__)),
                            independent_scientific_review=False,
                            qualification="same-producer separate-environment replay, not independent derivation or hardware validation"))
    print(f"{kind}: {len(equal)} exact numeric payloads, {checked} hashes verified", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=("combined", "residual"))
    parser.add_argument("first")
    parser.add_argument("replay")
    parser.add_argument("receipt")
    args = parser.parse_args()
    verify(args.first, args.replay, args.receipt, args.kind)
