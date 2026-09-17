import json
import pytest
from research.journal_sprint import verify_normalization_replay as verifier
from research.journal_sprint.storage import sha256, write_json


def archives(tmp_path, monkeypatch):
    monkeypatch.setattr(verifier, "CONFIG", {"degrees": []})
    monkeypatch.setattr(verifier, "SOURCES", ())
    roots = [tmp_path/"first", tmp_path/"replay"]
    for index, root in enumerate(roots):
        root.mkdir()
        write_json(root/"planned.json", dict(config={"degrees": []}, source_sha256={}))
        for name in ("model.json", "signal_plans.json", "loader.json", "encoding.json", "results.json"):
            write_json(root/name, {"value": .25})
        write_json(root/"moments.json", {"2": {"elapsed_seconds": index+1, "value": 2}})
        write_json(root/"controls.json", {"original": {"by_precision": {"2": {"elapsed_seconds": index+2, "value": 3}}}})
        write_json(root/"complete.json", dict(sha256={p.name: sha256(p) for p in root.iterdir()}))
    return roots


def test_exact_replay_excludes_only_named_times(tmp_path, monkeypatch):
    first, replay = archives(tmp_path, monkeypatch)
    verifier.verify(first, replay, tmp_path/"receipt.json")
    result = json.loads((tmp_path/"receipt.json").read_text())
    assert result["hashes_checked"] == 16
    assert len(result["exact_numeric_payloads"]) == 7


def test_self_consistent_numeric_tampering_rejected(tmp_path, monkeypatch):
    first, replay = archives(tmp_path, monkeypatch)
    path = replay/"model.json"
    path.write_text('{"value": 0.3}')
    manifest = json.loads((replay/"complete.json").read_text())
    manifest["sha256"][path.name] = sha256(path)
    (replay/"complete.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="numeric replay"):
        verifier.verify(first, replay, tmp_path/"receipt.json")
