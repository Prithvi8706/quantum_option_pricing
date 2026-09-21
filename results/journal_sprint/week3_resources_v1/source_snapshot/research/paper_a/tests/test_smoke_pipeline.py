import hashlib
import json

from research.paper_a.schema import read_records, validate_record
from research.paper_a.scripts.run_smoke import run_smoke


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_smoke_produces_a_complete_experiment_directory(tmp_path):
    summary = run_smoke(tmp_path, shots=256)
    for name in ("raw.jsonl", "resources.jsonl", "validation.json", "COMPLETE"):
        assert (tmp_path / name).exists(), f"{name} missing"
    assert summary["planned_attempts"] == 4  # 2 configs x 2 seeds, ideal only


def test_every_smoke_record_validates(tmp_path):
    run_smoke(tmp_path, shots=256)
    for record in read_records(tmp_path / "raw.jsonl"):
        assert validate_record(record) == [], record


def test_records_carry_full_provenance(tmp_path):
    run_smoke(tmp_path, shots=256)
    for record in read_records(tmp_path / "raw.jsonl"):
        assert record["environment"]["git_commit"]
        assert record["stream_key"].startswith("paper-a/v1 | ")
        assert record["P_BS"] and record["P_grid"] and record["P_circuit"]


def test_resources_are_recorded_per_invocation(tmp_path):
    run_smoke(tmp_path, shots=256)
    resources = read_records(tmp_path / "resources.jsonl")
    assert resources
    for r in resources:
        assert r["m_a_logical"] >= 1
        assert r["m_a_executed"] >= r["m_a_logical"]
        assert r["max_executed_depth"] > 0


def test_complete_marker_is_written_last(tmp_path):
    run_smoke(tmp_path, shots=256)
    raw_path = tmp_path / "raw.jsonl"
    resources_path = tmp_path / "resources.jsonl"
    validation_path = tmp_path / "validation.json"
    complete_path = tmp_path / "COMPLETE"
    marker = json.loads(complete_path.read_text())

    # The marker's hashes must match the FINISHED files on disk. A marker
    # written before the appends finished would carry stale hashes here.
    assert marker["raw_sha256"] == _sha256(raw_path)
    assert marker["resources_sha256"] == _sha256(resources_path)
    assert marker["validation_sha256"] == _sha256(validation_path)

    # Coarse Windows filesystem timestamp granularity rules out a strict `>`.
    assert complete_path.stat().st_mtime >= raw_path.stat().st_mtime
    assert complete_path.stat().st_mtime >= resources_path.stat().st_mtime


def test_rerun_is_idempotent_and_does_not_duplicate(tmp_path):
    run_smoke(tmp_path, shots=256)
    first = len(read_records(tmp_path / "raw.jsonl"))
    run_smoke(tmp_path, shots=256)
    assert len(read_records(tmp_path / "raw.jsonl")) == first
