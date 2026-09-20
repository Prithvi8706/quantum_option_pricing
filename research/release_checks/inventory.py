"""Require complete, closed archive inventories before interpreting results."""

from .hashes import verify_hashes
from .json_io import read
from .paths import normalized


def verify_archive(path):
    entries = normalized(read(path / "complete.json")["sha256"])
    mandatory = {"planned.json", "inputs.json", "results.json"}
    if not mandatory <= set(entries) or "complete.json" in entries:
        raise ValueError("missing evidence or self-referential manifest")
    paths = list(path.rglob("*"))
    if any(p.is_symlink() for p in paths):
        raise ValueError("archive symlinks are not release artifacts")
    actual = {p.relative_to(path).as_posix() for p in paths if p.is_file()}
    if actual != set(entries) | {"complete.json"} or "failed.json" in actual:
        raise ValueError("unrecorded, failed or missing archive files")
    return verify_hashes(path, entries)
