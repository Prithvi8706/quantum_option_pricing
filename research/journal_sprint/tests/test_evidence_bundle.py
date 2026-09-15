"""Lossless extraction, integrity and no-overwrite checks for publication bundle."""

import json
import zipfile

import pytest

from research.journal_sprint.evidence_bundle import build, digest, extract, member_path, validate


def fixture_bundle(tmp_path):
    source = tmp_path / "source"
    (source / "run").mkdir(parents=True)
    (source / "run/data.json").write_bytes(b'{"value": 1}\r\n')
    (source / "run/complete.json").write_bytes(b'{"preserved": true}\n')
    prefix = tmp_path / "bundle"
    build(source, prefix, ("run",))
    return source, prefix


def test_lossless_roundtrip_and_existing_destination_refusal(tmp_path):
    source, prefix = fixture_bundle(tmp_path)
    output = tmp_path / "output"
    assert extract(prefix, output)["extracted"] == 2
    for path in (source / "run").iterdir():
        assert (output / "run" / path.name).read_bytes() == path.read_bytes()
    with pytest.raises(FileExistsError):
        extract(prefix, output)
    with pytest.raises(FileExistsError):
        build(source, prefix, ("run",))


@pytest.mark.parametrize("name", ["../a", "/a/b", "a/../b", "a\\b", "C:/a", "a//b", "a/./b"])
def test_traversal_rejected(name):
    with pytest.raises(ValueError):
        member_path(name)


def test_corruption_rejected_before_output_created(tmp_path):
    _, prefix = fixture_bundle(tmp_path)
    with prefix.with_suffix(".zip").open("ab") as stream:
        stream.write(b"tamper")
    with pytest.raises(ValueError, match="checksum"):
        extract(prefix, tmp_path / "output")
    assert not (tmp_path / "output").exists()


def test_member_checksum_is_checked_independently(tmp_path):
    _, prefix = fixture_bundle(tmp_path)
    index_path = prefix.with_suffix(".json")
    index = json.loads(index_path.read_text())
    index["entries"]["run/data.json"]["sha256"] = "0" * 64
    index_path.write_text(json.dumps(index))
    with pytest.raises(ValueError, match="member checksum"):
        validate(prefix)


def test_duplicate_member_rejected(tmp_path):
    _, prefix = fixture_bundle(tmp_path)
    with pytest.warns(UserWarning):
        with zipfile.ZipFile(prefix.with_suffix(".zip"), "a") as output:
            output.writestr("run/data.json", "duplicate")
    index_path = prefix.with_suffix(".json")
    index = json.loads(index_path.read_text())
    index["zip_sha256"] = digest(prefix.with_suffix(".zip").read_bytes())
    index_path.write_text(json.dumps(index))
    with pytest.raises(ValueError, match="inventory"):
        validate(prefix)
