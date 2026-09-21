import hashlib
from pathlib import Path

import numpy as np
import pytest

from research.journal_sprint.run_comparator import quantile_interval
from research.journal_sprint.run_prototype import aggregate, describe, mle_batch
from research.journal_sprint.intervals import ConfidenceSet
from research.journal_sprint.vendor.mlqae_core import evaluate_schedule


def test_pinned_source_unchanged():
    source = Path(__file__).resolve().parents[1] / "vendor/mlqae_core.py"
    normalized = source.read_text().rstrip() + "\n"
    assert hashlib.sha256(normalized.encode()).hexdigest() == (
        "e45c987ed4de98b189e73bf70dd08cee7ebbfba6bccfc30762194d2b82da7014"
    )


def test_comparator_same_counts_when_only_likelihood_changes():
    args = ([0, 1, 2, 4], [8, 6, 4, 2], 40, 123)
    matched = evaluate_schedule(*args, eta=0.02, return_extra=True)
    ignored = evaluate_schedule(*args, eta=0.02, model_eta=0, return_extra=True)
    assert np.array_equal(matched["counts"], ignored["counts"])
    assert matched["nq"] == 30


def test_quantile_interval_order_statistics():
    values = np.arange(1000) / 1000
    lo, hi = quantile_interval(values, 2)
    assert lo < 1.9 < hi


def test_missing_truth_not_reported_as_coverage():
    row = describe(ConfidenceSet((), 0.05), None)
    summary = aggregate([row])
    assert summary["contains_mean"] is None
    assert summary["erroneous_conditional_0.01"] is None
    assert summary["incompatible_mean"] == 1


def test_grid_mle_probability_convention():
    estimates = mle_batch(np.full((1, 5), 500), 1000, 0.01)
    assert estimates[0] == pytest.approx(0.5, abs=1e-4)
