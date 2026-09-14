"""Materialize a supplemented historical source tree without editing its archive."""

import argparse
import json
from pathlib import Path
import shutil

from .checks import require
from .storage import ROOT, sha256, write_json
from .verify_numerical_check import checked_archive


def materialize(output):
    archive = ROOT / "results/journal_sprint/pricing_gate_v2a_retry1"
    checked_archive(archive)
    supplement = ROOT / "results/journal_sprint/v2a_replay_supplement_v1/PROTOCOL_V1.md"
    planned = json.loads((archive / "planned.json").read_text())
    expected = planned["source_sha256"]["docs\\journal_sprint\\PROTOCOL_V1.md"]
    require(sha256(supplement) == expected, "supplement must match original planned V1 hash")
    output = Path(output)
    # copytree refuses existing destinations. All original snapshots stay untouched.
    shutil.copytree(archive / "source_snapshot", output)
    shutil.copy2(supplement, output / "docs/journal_sprint/PROTOCOL_V1.md")
    for name in ("requirements-legacy-circuit.txt", "vendor/LICENSE-csAE", "vendor/NOTICE.md"):
        (output / "research/journal_sprint" / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(
            ROOT / "research/journal_sprint" / name, output / "research/journal_sprint" / name
        )
    write_json(
        output / "PREPARED.json",
        {
            "archive_manifest_sha256": sha256(archive / "complete.json"),
            "supplement_sha256": expected,
            "scope": "source reconstruction; not execution or environment certification",
        },
    )
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(materialize(args.output))


if __name__ == "__main__":
    main()
