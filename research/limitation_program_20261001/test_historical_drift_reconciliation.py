"""Byte-exact recovery never waives the original expected live hash."""

import hashlib

import pytest

from research.limitation_program_20261001 import historical_drift_reconciliation as audit


@pytest.mark.parametrize(
    "payload,transform,expected",
    [
        (b"x\n", "identity", b"x\n"),
        (b"x\r\n", "normalize_CRLF_to_LF", b"x\n"),
        (b"x\n", "materialize_LF_as_CRLF", b"x\r\n"),
        (b"x\r\n", "materialize_LF_as_CRLF", b"x\r\n"),
    ],
)
def test_only_declared_line_ending_materializations(payload, transform, expected):
    assert audit.transformed(payload, transform) == expected


def test_matching_old_hash_requires_identical_bytes_after_declared_transform():
    expected = audit.hash_bytes(b"x\r\n")
    assert audit.matching_transform(b"x\n", expected) == "materialize_LF_as_CRLF"
    assert audit.matching_transform(b"different\n", expected) is None


def test_git_object_identity_includes_blob_header():
    payload = b"x\n"
    oid = hashlib.sha1(b"blob 2\0" + payload).hexdigest()
    audit.verify_git_object(payload, oid, "sha1")
    with pytest.raises(ValueError, match="identity"):
        audit.verify_git_object(b"y\n", oid, "sha1")


def test_live_expectation_does_not_match_reconstructed_historical_version():
    expected = audit.hash_bytes(b"old\r\n")
    archived = audit.transformed(b"old\n", "materialize_LF_as_CRLF")
    assert audit.hash_bytes(archived) == expected
    assert audit.hash_bytes(b"new\r\n") != expected


def test_literal_import_closure_uses_snapshot_and_never_executes_module(tmp_path):
    package = tmp_path / "research"
    package.mkdir()
    (package / "dep.py").write_text("raise RuntimeError('must never run')\n", encoding="utf-8")
    snapshot = tmp_path / "snapshot.py"
    snapshot.write_text("from research.dep import value\n", encoding="utf-8")
    found, dynamic = audit.project_import_closure(
        tmp_path, [dict(original="research/main.py", snapshot_workspace_path="snapshot.py")]
    )
    assert set(found) == {"research/main.py", "research/dep.py"} and not dynamic


def test_workspace_paths_cannot_escape_named_root(tmp_path):
    with pytest.raises(ValueError, match="escaped"):
        audit.local(tmp_path, "../outside.py")
