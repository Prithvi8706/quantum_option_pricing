import json
import pytest
from research.journal_sprint import verify_barrier_replay as verifier
from research.journal_sprint.storage import sha256, write_json


def archives(tmp_path, monkeypatch):
    monkeypatch.setattr(verifier, "CONFIG", {"degrees": [2]})
    monkeypatch.setattr(verifier, "SOURCES", ())
    roots = [tmp_path/"first", tmp_path/"replay"]
    for root in roots:
        root.mkdir()
        write_json(root/"planned.json", dict(config={"degrees": [2]}, source_sha256={}))
        for name in ("signal_plans.json", "tiny_integrated.json", "results.json", "phase_2.json"):
            write_json(root/name, {"value": .25})
        write_json(root/"complete.json", dict(sha256={p.name: sha256(p) for p in root.iterdir()}))
    return roots


def test_exact_replay(tmp_path, monkeypatch):
    first, replay = archives(tmp_path, monkeypatch)
    receipt = tmp_path/"receipt.json"
    verifier.verify(first, replay, receipt)
    result = json.loads(receipt.read_text())
    assert result["hashes_checked"] == 10
    assert len(result["exact_numeric_payloads"]) == 4


@pytest.mark.parametrize("kind", ["extra", "hash", "numerical"])
def test_reject_tampering(tmp_path, monkeypatch, kind):
    first, replay = archives(tmp_path, monkeypatch)
    if kind == "extra":
        write_json(replay/"extra.json", {})
    else:
        (replay/"results.json").write_text('{"value": 0.5}', encoding="utf-8")
        if kind == "numerical":
            manifest = json.loads((replay/"complete.json").read_text())
            manifest["sha256"]["results.json"] = sha256(replay/"results.json")
            (replay/"complete.json").write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match={"extra": "inventory", "hash": "hash", "numerical": "payload"}[kind]):
        verifier.verify(first, replay, tmp_path/"receipt.json")
