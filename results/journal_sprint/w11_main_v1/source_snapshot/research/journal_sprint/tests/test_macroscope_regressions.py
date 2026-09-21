"""Regression coverage for PR #1's Macroscope findings (September 2026)."""

import ast
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

from research.journal_sprint.checks import archive_path, relative_archive_path
from research.journal_sprint.intervals import MAX_DEPTH, invert, sine_preimage
from research.journal_sprint.storage import ROOT, sha256
from research.journal_sprint.verify_numerical_check import checked_archive


def test_production_integrity_gates_are_not_assert_statements():
    for path in (ROOT / "research/journal_sprint").glob("*.py"):
        assert not any(
            isinstance(node, ast.Assert) for node in ast.walk(ast.parse(path.read_text()))
        )


def test_optimized_analysis_rejects_tampered_archive(tmp_path):
    source = tmp_path / "results/journal_sprint/week3_circuits_v1_retry1"
    source.mkdir(parents=True)
    (source / "summary.json").write_text('{"rows": []}')
    (source / "complete.json").write_text(json.dumps({"sha256": {"summary.json": "bad"}}))
    code = (
        "from pathlib import Path; "
        "from research.journal_sprint import analyze_circuit_gate as m; "
        f"m.ROOT = Path({str(tmp_path)!r}); m.main()"
    )
    result = subprocess.run(
        [sys.executable, "-O", "-c", code], cwd=ROOT, capture_output=True, text=True, timeout=30
    )
    assert result.returncode != 0 and "ValueError: summary.json" in result.stderr
    assert not (tmp_path / "results/journal_sprint/week3_circuit_analysis_v1").exists()


@pytest.mark.parametrize("depth", [MAX_DEPTH + 1, 10**9, 10**30, float("inf")])
def test_excessive_depth_is_rejected(depth):
    with pytest.raises(ValueError):
        sine_preimage(0.1, 0.2, depth)
    with pytest.raises(ValueError):
        invert([1], [10], [depth])


def test_maximum_depth_is_supported():
    assert sine_preimage(0.0, 1.0, MAX_DEPTH)


def test_windows_manifest_names_are_portable(tmp_path):
    target = tmp_path / "source_snapshot/research/example.py"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"original\r\n")
    name = "source_snapshot\\research\\example.py"
    assert relative_archive_path(name).parts == ("source_snapshot", "research", "example.py")
    (tmp_path / "complete.json").write_text(json.dumps({"sha256": {name: sha256(target)}}))
    checked_archive(tmp_path)
    target.write_bytes(b"tampered")
    with pytest.raises(ValueError, match="hash mismatch"):
        checked_archive(tmp_path)


@pytest.mark.parametrize("name", ["../outside", "a/../../outside", "C:\\outside", "/outside"])
def test_manifest_traversal_is_rejected(tmp_path, name):
    with pytest.raises(ValueError):
        archive_path(tmp_path, name)


def test_dirty_biqae_checkout_rejected_before_import(tmp_path, monkeypatch):
    from research.journal_sprint import biqae_smoke as runner

    checkout, output = tmp_path / "checkout", tmp_path / "output"
    (checkout / "src").mkdir(parents=True)
    (checkout / "src/biae.py").write_text("raise RuntimeError('must not execute')")

    def git_output(command, **kwargs):
        return (
            "bbd28a3efa659e1c0feec6b86ba13389cb127dbd\n"
            if command[1] == "rev-parse"
            else " M src/biae.py\n"
        )

    monkeypatch.setattr(runner.subprocess, "check_output", git_output)
    monkeypatch.setattr(sys, "argv", ["runner", str(checkout), str(output)])
    with pytest.raises(RuntimeError, match="not clean"):
        runner.main()
    assert not (output / "complete.json").exists()


@pytest.mark.parametrize(
    "body", [b"<html>Log into wifi</html>", b"<article><h1>Consent</h1></article>"]
)
def test_http_200_non_article_is_not_a_reading(body):
    from research.journal_sprint.fetch_readings import SOURCES, validated_article

    with pytest.raises(ValueError, match="full-text article"):
        validated_article("bae", SimpleNamespace(url=SOURCES["bae"], content=body))


def test_article_identity_and_structure_required():
    from research.journal_sprint.fetch_readings import SOURCES, validated_article

    body = (
        '<article><h1 class="ltx_title_document">Bayesian Quantum Amplitude Estimation'
        '</h1><div class="ltx_abstract">Abstract</div>' + "text " * 300 + "</article>"
    )
    response = SimpleNamespace(url=SOURCES["bae"], content=body.encode())
    assert validated_article("bae", response).find("article")
    response.url = "https://example.com/consent"
    with pytest.raises(ValueError, match="redirected"):
        validated_article("bae", response)


def test_pilot_timeout_preserves_record_without_completion(tmp_path, monkeypatch):
    from research.journal_sprint import run_prototype as runner

    monkeypatch.setattr(runner, "CONDITIONS", {})
    monkeypatch.setattr(runner, "AMPLITUDES", [0.17])
    ticks = iter([0.0, 3601.0])
    monkeypatch.setattr(runner.time, "perf_counter", lambda: next(ticks))
    monkeypatch.setattr(sys, "argv", ["runner", "--output", str(tmp_path / "pilot")])
    with pytest.raises(TimeoutError, match="pilot records retained"):
        runner.main()
    assert not (tmp_path / "pilot/complete.json").exists()
    records = list((tmp_path / "pilot").glob("*.jsonl"))
    assert len(records) == 1
    assert json.loads(records[0].read_text().splitlines()[0])["experiment"] == "split_pilot"


def test_materialized_baseline_has_pinned_protocol_and_recipe(tmp_path):
    from research.journal_sprint.materialize_baseline import materialize

    output = materialize(tmp_path / "replay")
    assert sha256(output / "docs/journal_sprint/PROTOCOL_V1.md") == (
        "a99f2faf3e6e262574dc9099d9eacc0f00d3ef2ab2386bef9a33e9d6ac99912f"
    )
    assert (output / "research/journal_sprint/requirements-legacy-circuit.txt").is_file()
    assert (output / "research/journal_sprint/vendor/LICENSE-csAE").is_file()
    with pytest.raises(FileExistsError):
        materialize(output)


def test_snapshot_recipe_is_included():
    from research.journal_sprint import verify

    assert (
        'ROOT / "research/journal_sprint/requirements-legacy-circuit.txt"'
        in Path(verify.__file__).read_text()
    )
