"""Read-only hash validation for the local programme's frozen receipt formats."""

import argparse
import hashlib
import json
from pathlib import Path

from research.limitation_program_20261001.progress import ROOT


def validate(program):
    program = program.resolve()
    checked, mismatches = {}, []

    def check(path, expected):
        path = path.resolve()
        if path not in checked:
            checked[path] = (
                hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            )
        if checked[path] != expected:
            mismatches.append(dict(path=str(path), expected=expected, actual=checked[path]))

    manifests = sorted(
        set(program.rglob("manifest.json")) | set(program.rglob("TOP_MANIFEST.json"))
    )
    for manifest in manifests:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data and all(isinstance(v, str) and len(v) == 64 for v in data.values()):
            for name, expected in data.items():
                check(manifest.parent / name, expected)
        for field in ("files", "frozen_inputs", "dependency_sha256", "additional_files", "report"):
            for name, expected in data.get(field, {}).items():
                check(ROOT / name, expected)
        for name, expected in data.get("sha256", {}).items():
            check(manifest.parent / name, expected)
        for row in data.get("inputs", {}).values():
            if isinstance(row, dict):
                for field, value in row.items():
                    if field.endswith("_path") and field[:-5] + "_sha256" in row:
                        check(Path(value), row[field[:-5] + "_sha256"])
        protocol_file = manifest.parent / "protocol.json"
        if protocol_file.is_file():
            protocol = json.loads(protocol_file.read_text(encoding="utf-8"))
            for row in protocol.get("executed_dependencies", []):
                check(manifest.parent / row["snapshot"], row["sha256"])
    result = dict(
        passed=not mismatches,
        manifest_count=len(manifests),
        distinct_hashed_files=len(checked),
        mismatches=mismatches,
        scope="Known file maps and executed snapshots in existing frozen manifests. "
        "Failed setup receipts remain historical records; valid hashes do not "
        "turn those failed preparations into successful experiments.",
    )
    print(json.dumps(result, indent=2), flush=True)
    if mismatches:
        raise SystemExit(1)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--program", type=Path, default=ROOT / "results/limitation_program_20261001"
    )
    args = parser.parse_args()
    validate(args.program)
