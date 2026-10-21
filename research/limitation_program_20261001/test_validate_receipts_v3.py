"""Tiny receipt fixtures verify strict hashes and separately admitted archives."""

import hashlib
import json

import pytest

from research.limitation_program_20261001 import validate_receipts_v3 as validator


ORIGINAL = "research/frontier_classical_20261001/kernels.py"


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def file(path, payload=b"fixture"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return sha(payload)


def relative(path, root):
    return path.relative_to(root).as_posix()


def inspect(root, archive=None):
    return validator.validate(
        root / "program", archive, workspace_root=root, emit=False, raise_on_failure=False
    )


def archive_fixture(root):
    program = root / "program"
    source = root / ORIGINAL
    expected = sha(b"original\n")
    file(source, b"changed\n")
    affected = program / "A18_run001"
    protocol = affected / "protocol.json"
    write(protocol, dict(frozen_inputs={ORIGINAL: expected}))
    manifest = affected / "manifest.json"
    write(
        manifest,
        dict(
            files={relative(protocol, root): validator.digest(protocol)},
            frozen_inputs={ORIGINAL: expected},
        ),
    )
    archive_dir = program / "A01_drift_run001"
    snapshot = archive_dir / "recovered_original_inventory/kernels.py"
    file(snapshot, b"original\n")
    archive = archive_dir / "reconciliation.json"
    proof = dict(
        passed=True,
        historical_snapshot_integrity=True,
        legitimate_expected_hashes_waived=False,
        affected_receipts=["A18_run001"],
        rows=[
            dict(
                path=ORIGINAL,
                expected_old_sha256=expected,
                historical_old_bytes_recovered=True,
                expected_hash_waived=False,
                recovered_snapshot_path=relative(snapshot, root),
                recovered_snapshot_sha256=expected,
                references=[
                    dict(
                        receipt="A18_run001",
                        expected_sha256=expected,
                        manifest_sha256=validator.digest(manifest),
                        protocol_sha256=validator.digest(protocol),
                    )
                ],
            )
        ],
    )
    case = dict(
        root=root,
        archive=archive,
        proof=proof,
        snapshot=snapshot,
        manifest=manifest,
        source=source,
        expected=expected,
    )
    rebind_proof(case)
    return case


def rebind_proof(case):
    write(case["archive"], case["proof"])
    write(
        case["archive"].parent / "manifest.json",
        dict(
            files={
                relative(case["archive"], case["root"]): validator.digest(case["archive"]),
                relative(case["snapshot"], case["root"]): case["expected"],
            }
        ),
    )


def test_valid_live_receipt_needs_no_archival_exception(tmp_path):
    expected = file(tmp_path / "research/input.py")
    write(
        tmp_path / "program/live/manifest.json",
        dict(frozen_inputs={"research/input.py": expected}),
    )
    result = inspect(tmp_path)
    assert result["passed"] and result["global_live_integrity"]
    assert result["archived_or_current_integrity_passed"] and not result["mismatches"]
    assert result["validated_recovered_snapshots"] == []


def test_every_v2_map_and_declared_snapshot_keeps_its_resolution(tmp_path):
    program = tmp_path / "program"
    leaf = program / "leaf"
    files = {
        name: file(tmp_path / name)
        for name in (
            "research/external.py",
            "research/workspace.py",
            "research/frozen.py",
            "research/dependency.py",
            "research/additional.py",
            "research/report.py",
        )
    }
    local_sha = file(leaf / "local.py")
    relative_sha = file(leaf / "sha-map.py")
    input_file = tmp_path / "absolute-input.py"
    input_sha = file(input_file)
    snapshot_sha = file(leaf / "executed.py")
    write(
        leaf / "protocol.json",
        dict(executed_dependencies=[dict(snapshot="executed.py", sha256=snapshot_sha)]),
    )
    write(
        leaf / "manifest.json",
        dict(
            files={"local.py": local_sha},
            external_files={"research/external.py": files["research/external.py"]},
            frozen_inputs={"research/frozen.py": files["research/frozen.py"]},
            dependency_sha256={"research/dependency.py": files["research/dependency.py"]},
            additional_files={"research/additional.py": files["research/additional.py"]},
            report={"research/report.py": files["research/report.py"]},
            sha256={"sha-map.py": relative_sha},
            inputs={"provided": dict(source_path=str(input_file), source_sha256=input_sha)},
        ),
    )
    write(
        program / "workspace/manifest.json",
        dict(files={"research/workspace.py": files["research/workspace.py"]}),
    )
    flat_sha = file(program / "flat/local.txt")
    write(program / "flat/manifest.json", {"local.txt": flat_sha})
    top_sha = file(program / "top/local.txt")
    write(program / "top/TOP_MANIFEST.json", {"local.txt": top_sha})
    result = inspect(tmp_path)
    assert result["passed"] and result["manifest_count"] == 4
    assert result["distinct_hashed_files"] == 12 and not result["mismatches"]
    file(leaf / "executed.py", b"changed execution")
    failed = inspect(tmp_path)
    assert not failed["passed"] and len(failed["mismatches"]) == 1
    assert failed["mismatches"][0]["source_map"] == "executed_dependencies"


def test_exact_archive_is_separate_from_visible_failed_live_integrity(tmp_path):
    case = archive_fixture(tmp_path)
    result = inspect(tmp_path, case["archive"])
    assert not result["passed"] and not result["global_live_integrity"]
    assert result["archived_or_current_integrity_passed"]
    assert (
        len(result["mismatches"])
        == len(result["live_mismatches_with_separate_archival_evidence"])
        == 1
    )
    assert not result["unresolved_archived_or_current_mismatches"]
    assert result["mismatches"][0]["expected"] == case["expected"]
    assert not result["legitimate_expected_hashes_waived"]
    assert not result["runtime_nonexecution_claim"]


@pytest.mark.parametrize(
    "damage",
    [
        "corrupt_snapshot",
        "wrong_old_SHA",
        "wrong_recovered_SHA",
        "unknown_original_path",
        "unlisted_reference",
        "wrong_manifest_SHA",
        "missing_frozen_membership",
        "missing_snapshot_membership",
        "snapshot_path_escape",
        "absolute_snapshot_path",
        "corrupt_reconciliation_binding",
    ],
)
def test_invalid_archive_cannot_reconcile_live_expectations(tmp_path, damage):
    case = archive_fixture(tmp_path)
    row = case["proof"]["rows"][0]
    rebind = True
    if damage == "corrupt_snapshot":
        file(case["snapshot"], b"corrupt snapshot")
    elif damage == "wrong_old_SHA":
        row["expected_old_sha256"] = sha(b"different expected")
    elif damage == "wrong_recovered_SHA":
        row["recovered_snapshot_sha256"] = sha(b"different claimed snapshot")
    elif damage == "unknown_original_path":
        row["path"] = "research/unknown.py"
    elif damage == "unlisted_reference":
        row["references"][0]["receipt"] = "unlisted"
    elif damage == "wrong_manifest_SHA":
        row["references"][0]["manifest_sha256"] = sha(b"wrong manifest")
    elif damage == "missing_frozen_membership":
        write(case["manifest"], dict(frozen_inputs={}))
        row["references"][0]["manifest_sha256"] = validator.digest(case["manifest"])
    elif damage == "missing_snapshot_membership":
        rebind_proof(case)
        owner = validator.read(case["archive"].parent / "manifest.json")
        del owner["files"][relative(case["snapshot"], tmp_path)]
        write(case["archive"].parent / "manifest.json", owner)
        rebind = False
    elif damage == "snapshot_path_escape":
        escaped = tmp_path / "outside.py"
        file(escaped, b"original\n")
        row["recovered_snapshot_path"] = relative(escaped, tmp_path)
    elif damage == "absolute_snapshot_path":
        row["recovered_snapshot_path"] = str(case["snapshot"])
    elif damage == "corrupt_reconciliation_binding":
        case["archive"].write_text("{}", encoding="utf-8")
        rebind = False
    if rebind:
        rebind_proof(case)
    result = inspect(tmp_path, case["archive"])
    assert not result["archived_or_current_integrity_passed"]
    assert result["archival_proof_errors"]
    assert not result["legitimate_expected_hashes_waived"]


def test_same_known_path_in_unlisted_manifest_still_fails_archival_integrity(tmp_path):
    case = archive_fixture(tmp_path)
    write(
        tmp_path / "program/unlisted/manifest.json",
        dict(frozen_inputs={ORIGINAL: case["expected"]}),
    )
    result = inspect(tmp_path, case["archive"])
    assert not result["passed"] and not result["archived_or_current_integrity_passed"]
    assert len(result["mismatches"]) == 2
    assert len(result["unresolved_archived_or_current_mismatches"]) == 1
    assert result["unresolved_archived_or_current_mismatches"][0]["manifest_basename"] == "unlisted"


def test_reconciliation_pointer_cannot_escape_scanned_program(tmp_path):
    case = archive_fixture(tmp_path)
    result = inspect(tmp_path, tmp_path / "outside.json")
    assert not result["archived_or_current_integrity_passed"]
    assert "outside" in result["archival_proof_errors"][0]["message"]
    assert len(result["mismatches"]) == 1
    assert case["source"].read_bytes() == b"changed\n"


def test_strict_exit_failure_survives_a_valid_historical_archive(tmp_path):
    case = archive_fixture(tmp_path)
    with pytest.raises(SystemExit) as failure:
        validator.validate(
            tmp_path / "program", case["archive"], workspace_root=tmp_path, emit=False
        )
    assert failure.value.code == 1


def test_streamed_digest_detects_later_changes_without_persistent_cache(tmp_path):
    path = tmp_path / "large.fixture"
    payload = b"a" * ((1 << 20) + 17)
    file(path, payload)
    assert validator.digest(path) == sha(payload)
    path.write_bytes(payload[:-1] + b"b")
    assert validator.digest(path) != sha(payload)
