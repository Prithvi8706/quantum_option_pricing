"""Strict live integrity and separately checked historical snapshot integrity.

All V2 file maps still name legitimate expectations. Recovered snapshots never
alter those expectations or remove a live mismatch from the strict result.
"""

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DRIFT_PATHS = frozenset(
    "research/frontier_classical_20261001/" + name + ".py"
    for name in (
        "c1_rates",
        "c2_timing",
        "c4_coverage",
        "c5_smoothers",
        "c7_c8_cases",
        "decision",
        "fit",
        "kernels",
        "scrambles",
    )
)
AFFECTED_RECEIPTS = frozenset(("A18_run001", "A18_B4_run001", "A01_run015", "A01_run016"))
ARCHIVE_RECEIPT = "A01_drift_run001"


def digest(path):
    """No hash is persisted or trusted across validator invocations."""
    if not path.is_file():
        return None
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            value.update(block)
    return value.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def archive_evidence(program, workspace, reconciliation, manifest_data):
    """Validate an explicitly supplied proof; never infer an override."""
    archive = Path(reconciliation).resolve()
    require(archive.is_relative_to(program), "Reconciliation is outside the scanned program")
    receipt = archive.parent
    require(receipt.name == ARCHIVE_RECEIPT, "Unlisted reconciliation receipt")
    require(archive.is_relative_to(workspace), "Reconciliation escaped the workspace")
    owner_manifest = receipt / "manifest.json"
    require(owner_manifest in manifest_data, "Reconciliation owner manifest is not scanned")
    owner_files = manifest_data[owner_manifest].get("files", {})
    archive_key = archive.relative_to(workspace).as_posix()
    require(owner_files.get(archive_key) == digest(archive), "Reconciliation file binding failed")
    evidence = read(archive)
    require(
        evidence.get("passed") is True
        and evidence.get("historical_snapshot_integrity") is True
        and evidence.get("legitimate_expected_hashes_waived") is False,
        "Reconciliation does not assert unwaived historical integrity",
    )
    affected = evidence["affected_receipts"]
    require(
        affected and len(affected) == len(set(affected)) and set(affected) <= AFFECTED_RECEIPTS,
        "Unlisted or duplicate affected receipt",
    )
    manifests_by_receipt = {}
    for name in affected:
        matches = [path for path in manifest_data if path.parent.name == name]
        require(len(matches) == 1, "Affected manifest is absent or ambiguous: " + name)
        manifests_by_receipt[name] = matches[0]
    covered, rows = {}, []
    original_paths = set()
    require(evidence["rows"], "No reconstructed historical rows")
    for row in evidence["rows"]:
        original = row["path"]
        require(original in DRIFT_PATHS, "Unknown historical drift path: " + original)
        require(original not in original_paths, "Duplicate historical drift row")
        original_paths.add(original)
        expected = row["expected_old_sha256"]
        require(
            isinstance(expected, str)
            and len(expected) == 64
            and set(expected) <= set("0123456789abcdef"),
            "Invalid expected old SHA256",
        )
        require(
            row.get("historical_old_bytes_recovered") is True
            and row.get("expected_hash_waived") is False,
            "Historical row waives or lacks exact old bytes",
        )
        snapshot_name = Path(row["recovered_snapshot_path"])
        require(not snapshot_name.is_absolute(), "Absolute recovered snapshot path")
        snapshot = (workspace / snapshot_name).resolve()
        require(snapshot.is_relative_to(receipt), "Recovered snapshot escaped its receipt")
        snapshot_key = snapshot.relative_to(workspace).as_posix()
        require(
            digest(snapshot)
            == row["recovered_snapshot_sha256"]
            == expected
            == owner_files.get(snapshot_key),
            "Recovered snapshot SHA or receipt membership failed",
        )
        references = row["references"]
        reference_names = [ref["receipt"] for ref in references]
        require(
            len(reference_names) == len(set(reference_names))
            and set(reference_names) == set(affected),
            "Historical row references differ from affected manifests",
        )
        for reference in references:
            manifest = manifests_by_receipt[reference["receipt"]]
            require(
                digest(manifest) == reference["manifest_sha256"],
                "Affected manifest SHA differs from reference",
            )
            require(
                manifest_data[manifest].get("frozen_inputs", {}).get(original)
                == reference["expected_sha256"]
                == expected,
                "Historical reference is not a member of affected frozen inputs",
            )
            if "protocol_sha256" in reference:
                require(
                    digest(manifest.parent / "protocol.json") == reference["protocol_sha256"],
                    "Affected protocol SHA differs from reference",
                )
            covered[(str(manifest), str((workspace / original).resolve()), expected)] = dict(
                original_path=original,
                recovered_snapshot_path=snapshot_key,
                recovered_snapshot_sha256=expected,
                reference_receipt=reference["receipt"],
            )
        rows.append(
            dict(
                path=original,
                expected_old_sha256=expected,
                recovered_snapshot_path=snapshot_key,
                recovered_snapshot_sha256=expected,
                affected_manifest_references=reference_names,
            )
        )
    return covered, rows


def validate(
    program,
    reconciliation=None,
    *,
    workspace_root=ROOT,
    emit=True,
    raise_on_failure=True,
):
    program, workspace = Path(program).resolve(), Path(workspace_root).resolve()
    checked, mismatches, manifest_data = {}, [], {}

    def check(path, expected, manifest, field, name):
        path = path.resolve()
        if path not in checked:
            checked[path] = digest(path)
        if checked[path] != expected:
            mismatches.append(
                dict(
                    path=str(path),
                    expected=expected,
                    actual=checked[path],
                    manifest=str(manifest),
                    manifest_basename=manifest.parent.name,
                    source_map=field,
                    source_key=name,
                )
            )

    manifests = sorted(
        set(program.rglob("manifest.json")) | set(program.rglob("TOP_MANIFEST.json"))
    )
    for manifest in manifests:
        data = read(manifest)
        manifest_data[manifest] = data
        if data and all(isinstance(value, str) and len(value) == 64 for value in data.values()):
            for name, expected in data.items():
                check(manifest.parent / name, expected, manifest, "flat", name)
        if "external_files" in data:
            for name, expected in data.get("files", {}).items():
                check(manifest.parent / name, expected, manifest, "files", name)
            for name, expected in data["external_files"].items():
                check(workspace / name, expected, manifest, "external_files", name)
        else:
            for name, expected in data.get("files", {}).items():
                check(workspace / name, expected, manifest, "files", name)
        for field in ("frozen_inputs", "dependency_sha256", "additional_files", "report"):
            for name, expected in data.get(field, {}).items():
                check(workspace / name, expected, manifest, field, name)
        for name, expected in data.get("sha256", {}).items():
            check(manifest.parent / name, expected, manifest, "sha256", name)
        for row_name, row in data.get("inputs", {}).items():
            if isinstance(row, dict):
                for field, value in row.items():
                    if field.endswith("_path") and field[:-5] + "_sha256" in row:
                        check(
                            Path(value),
                            row[field[:-5] + "_sha256"],
                            manifest,
                            "inputs." + row_name,
                            field,
                        )
        protocol_file = manifest.parent / "protocol.json"
        if protocol_file.is_file():
            for index, row in enumerate(read(protocol_file).get("executed_dependencies", [])):
                check(
                    manifest.parent / row["snapshot"],
                    row["sha256"],
                    manifest,
                    "executed_dependencies",
                    str(index),
                )
    covered, archives, archive_errors = {}, [], []
    if reconciliation is not None:
        try:
            covered, archives = archive_evidence(program, workspace, reconciliation, manifest_data)
        except (OSError, ValueError, KeyError, TypeError) as error:
            archive_errors.append(dict(type=type(error).__name__, message=str(error)))
    unresolved, recovered_references = [], []
    for mismatch in mismatches:
        key = (mismatch["manifest"], mismatch["path"], mismatch["expected"])
        if key in covered and mismatch["source_map"] == "frozen_inputs":
            recovered_references.append(dict(mismatch=mismatch, archival_evidence=covered[key]))
        else:
            unresolved.append(mismatch)
    result = dict(
        passed=not mismatches,
        global_live_integrity=not mismatches,
        manifest_count=len(manifests),
        distinct_hashed_files=len(checked),
        mismatches=mismatches,
        reconciliation_input=str(Path(reconciliation).resolve())
        if reconciliation is not None
        else None,
        archived_or_current_integrity_passed=not unresolved and not archive_errors,
        archival_proof_errors=archive_errors,
        validated_recovered_snapshots=archives,
        live_mismatches_with_separate_archival_evidence=recovered_references,
        unresolved_archived_or_current_mismatches=unresolved,
        legitimate_expected_hashes_waived=False,
        runtime_nonexecution_claim=False,
        scope=(
            "Known V2 file maps and executed snapshots in frozen manifests; strict passed "
            "requires every live expectation to match. Explicit byte-exact archive evidence "
            "is a separate historical-integrity claim, with every live mismatch retained. "
            "Valid hashes do not turn failed preparations into successful experiments."
        ),
    )
    if emit:
        print(json.dumps(result, indent=2), flush=True)
    if mismatches and raise_on_failure:
        raise SystemExit(1)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--program", type=Path, default=ROOT / "results/limitation_program_20261001"
    )
    parser.add_argument("--reconciliation", type=Path)
    args = parser.parse_args()
    validate(args.program, args.reconciliation)
