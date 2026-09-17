"""Provenance failures must not turn into successful secondary-study receipts."""

import shutil
from pathlib import Path

import pytest

from research.journal_sprint.verify_claim_assessment import verify_archive, within


BASE = Path(__file__).resolve().parents[1]/"results/journal_sprint/claim_assessment_v1"


def test_complete_secondary_archive_recomputes():
    assert verify_archive(BASE)["recomputed"]


def test_changed_payload_is_rejected(tmp_path):
    archive = tmp_path/"copy"
    shutil.copytree(BASE, archive)
    with (archive/"results.json").open("a", encoding="utf-8") as stream:
        stream.write(" ")
    with pytest.raises(ValueError, match="artifact hash"):
        verify_archive(archive)


def test_missing_artifact_is_rejected(tmp_path):
    archive = tmp_path/"copy"
    shutil.copytree(BASE, archive)
    (archive/"inputs.json").unlink()
    with pytest.raises(ValueError, match="inventory"):
        verify_archive(archive)


def test_parent_path_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="escapes"):
        within(tmp_path, "../outside.json")
