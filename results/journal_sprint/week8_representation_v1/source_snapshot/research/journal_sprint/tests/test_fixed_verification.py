import json

import pytest

from research.journal_sprint.storage import ROOT
from research.journal_sprint.verify_fixed_discovery import validate_config


@pytest.mark.parametrize(
    "field,value",
    [
        ("tolerance", 2),
        ("alpha_validation", 0.05),
        ("alpha_calibration", 0.05),
        ("repetitions", 99),
        ("transfer_bounds", [0.04, 0.03]),
    ],
)
def test_configuration_rejects_changed_declaration(field, value):
    source = ROOT / "results/journal_sprint/week5_fixed_discovery_v1/planned.json"
    config = json.loads(source.read_text())["config"]
    manifests = config["input_manifests"]
    validate_config(config, manifests)
    config[field] = value
    with pytest.raises(ValueError, match="declared configuration"):
        validate_config(config, manifests)
