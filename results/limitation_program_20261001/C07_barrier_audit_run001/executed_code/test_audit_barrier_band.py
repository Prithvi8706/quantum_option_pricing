"""Independent arithmetic/receipt guard fixtures; no financial samples."""

from fractions import Fraction
import json

import pytest

from research.limitation_program_20261001 import audit_barrier_band as audit


@pytest.mark.parametrize("value", [Fraction(0), Fraction(1, 3), Fraction(-7, 9)])
def test_interval_conversion_encloses_exact_input(value):
    lo, hi = audit.endpoints(audit.iv(value))
    assert lo <= value <= hi


@pytest.mark.parametrize("delta", [Fraction(0), Fraction(1, 10**8), Fraction(1, 2)])
def test_relative_log_positive_series_and_geometric_endpoint(delta):
    from math import factorial

    lower = 140 * sum((delta**k / factorial(k) for k in range(1, 81)), Fraction(0))
    upper = lower + 140 * delta**81 / factorial(81) / (1 - delta / 82)
    reference = audit.independent_radius_enclosure(delta, 140)
    audit.enclose_claim([audit.pair(lower), audit.pair(upper)], reference, "Relative radius")


def test_zero_continuous_band_has_zero_probability():
    result = audit.independent_band_enclosure(0, 140, Fraction(3, 1000))
    assert result["density"] == result["centered_interval_maximum"] == [[0, 1], [0, 1]]


@pytest.mark.parametrize("field", ["files", "frozen_inputs"])
def test_manifest_rejects_changed_file(tmp_path, field):
    receipt = tmp_path / "receipt"
    receipt.mkdir()
    target = receipt / "data.json"
    target.write_text("{}", encoding="utf-8")
    digest = audit.sha(target)
    target.write_text("[]", encoding="utf-8")
    manifest = {
        "files": {"receipt/data.json": audit.sha(target)},
        "frozen_inputs": {},
        "manifest_self_hash_excluded": True,
    }
    manifest[field]["receipt/data.json"] = digest
    (receipt / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="changed"):
        audit.verify_manifest(tmp_path, receipt)


def test_manifest_rejects_unrecorded_artifact(tmp_path):
    receipt = tmp_path / "receipt"
    receipt.mkdir()
    (receipt / "extra.json").write_text("{}", encoding="utf-8")
    (receipt / "manifest.json").write_text(
        json.dumps({"files": {}, "frozen_inputs": {}, "manifest_self_hash_excluded": True}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="inventory"):
        audit.verify_manifest(tmp_path, receipt)


def test_manifest_path_cannot_escape_workspace(tmp_path):
    with pytest.raises(ValueError, match="escaped"):
        audit.local(tmp_path, "../outside.json")


def test_outward_claim_rejects_upper_below_reference():
    with pytest.raises(ValueError, match="enclose"):
        audit.enclose_claim([[0, 1], [1, 4]], [[0, 1], [1, 3]], "Upper")


def test_outward_claim_rejects_lower_above_reference():
    with pytest.raises(ValueError, match="enclose"):
        audit.enclose_claim([[1, 4], [1, 1]], [[1, 5], [1, 3]], "Lower")


def test_original_source_contract_is_structural_without_graph_execution():
    result = audit.source_contract(
        audit.ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
    )
    assert result["common_log_variance_exact"] == [3, 1000]
    assert result["strict_alive_less_than_barrier"]
    assert not result["digital_endpoint_mass_claimed_zero"]
