"""Bounded-memory, byte-exact SHA256 checks; no line-ending normalization."""

import hashlib
import re
from .paths import normalized, within


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def verify_hashes(root, entries):
    entries = normalized(entries)
    if not entries:
        raise ValueError("empty hash inventory")
    for name, expected in entries.items():
        if not isinstance(expected, str) or not re.fullmatch("[0-9a-f]{64}", expected):
            raise ValueError("invalid SHA256: " + name)
        if digest(within(root, name)) != expected:
            raise ValueError("hash mismatch: " + name)
    return len(entries)
