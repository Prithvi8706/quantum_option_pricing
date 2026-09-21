import json

from research.paper_a.schema import (
    SCHEMA_VERSION, append_record, idempotency_key, read_records,
    validate_record,
)


def _record(**overrides):
    base = {
        "schema_version": SCHEMA_VERSION,
        "experiment_uuid": "u1", "phase": "E0", "config_id": "E025",
        "n": 3, "replicate": 0, "condition": "ideal",
        "attempt_kind": "first_planned",
        "raw_estimation": 0.34, "raw_confidence_interval": [0.33, 0.35],
        "raw_price": 6.95, "presentation_clipped_price": 6.95,
        "completion_state": "complete", "environment": {"python_version": "3.9.13"},
        "actual_circuit_depth": 120, "reconstructed_circuit_depth": None,
    }
    base.update(overrides)
    return base


def test_valid_record_has_no_violations():
    assert validate_record(_record()) == []


def test_missing_required_field_is_reported():
    r = _record()
    del r["raw_estimation"]
    assert any("raw_estimation" in v for v in validate_record(r))


def test_estimate_outside_unit_interval_is_invalid():
    assert validate_record(_record(raw_estimation=1.2))
    assert validate_record(_record(raw_estimation=-0.01))


def test_unordered_or_out_of_range_interval_is_invalid():
    assert validate_record(_record(raw_confidence_interval=[0.4, 0.3]))
    assert validate_record(_record(raw_confidence_interval=[-0.1, 0.3]))
    assert validate_record(_record(raw_confidence_interval=[0.3, 1.4]))


def test_mixed_actual_and_reconstructed_provenance_is_invalid():
    """Annex I: no mixed actual/reconstructed record may pass validation."""
    r = _record(actual_circuit_depth=120, reconstructed_circuit_depth=118)
    assert any("provenance" in v.lower() for v in validate_record(r))


def test_reconstructed_only_record_is_valid():
    r = _record(actual_circuit_depth=None, reconstructed_circuit_depth=118)
    assert validate_record(r) == []


def test_negative_price_is_retained_and_valid():
    r = _record(raw_price=-0.4, presentation_clipped_price=0.0)
    assert validate_record(r) == []


def test_clipped_price_must_equal_max_zero_price():
    assert validate_record(_record(raw_price=-0.4,
                                   presentation_clipped_price=-0.4))


def test_append_is_append_only_and_readable(tmp_path):
    path = tmp_path / "raw.jsonl"
    append_record(path, _record(replicate=0))
    append_record(path, _record(replicate=1))
    records = read_records(path)
    assert [r["replicate"] for r in records] == [0, 1]
    assert len(path.read_text().strip().splitlines()) == 2


def test_append_never_rewrites_earlier_lines(tmp_path):
    path = tmp_path / "raw.jsonl"
    append_record(path, _record(replicate=0))
    first = path.read_text()
    append_record(path, _record(replicate=1))
    assert path.read_text().startswith(first)


def test_records_are_json_serializable(tmp_path):
    path = tmp_path / "raw.jsonl"
    append_record(path, _record())
    for line in path.read_text().strip().splitlines():
        json.loads(line)


def test_idempotency_key_is_stable_and_discriminating():
    args = dict(experiment_uuid="u1", phase="E3", config_id="E022", n=3,
                replicate=4, condition="ideal", purpose="shots")
    assert idempotency_key(**args) == idempotency_key(**args)
    assert idempotency_key(**args) != idempotency_key(**{**args, "replicate": 5})


def test_schema_version_is_present_and_checked():
    assert any("schema_version" in v
               for v in validate_record(_record(schema_version="v0-bogus")))
