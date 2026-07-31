import json

from research.paper_a.schema import read_records, validate_record
from research.paper_a.scripts.run_smoke import run_smoke


def test_smoke_produces_a_complete_experiment_directory(tmp_path):
    summary = run_smoke(tmp_path, shots=256)
    for name in ("raw.jsonl", "resources.jsonl", "validation.json", "COMPLETE"):
        assert (tmp_path / name).exists(), f"{name} missing"
    assert summary["attempts"] == 4  # 2 configs x 2 seeds, ideal only


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
    marker = json.loads((tmp_path / "COMPLETE").read_text())
    assert marker["raw_sha256"] and marker["resources_sha256"]


def test_rerun_is_idempotent_and_does_not_duplicate(tmp_path):
    run_smoke(tmp_path, shots=256)
    first = len(read_records(tmp_path / "raw.jsonl"))
    run_smoke(tmp_path, shots=256)
    assert len(read_records(tmp_path / "raw.jsonl")) == first
