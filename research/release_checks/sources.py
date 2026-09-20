"""Validate frozen source bytes and the separately recorded study protocol."""

import re
from .hashes import digest, verify_hashes
from .paths import normalized, within


def verify_sources(root, planned, protocol, required):
    if not required or not re.fullmatch("[0-9a-f]{40}", planned["git_head"]):
        raise ValueError("explicit source requirements and Git identity required")
    entries = normalized(planned["source_sha256"])
    if not set(required) <= set(entries):
        raise ValueError("mandatory source missing")
    count = verify_hashes(root, entries)
    if digest(within(root, protocol)) != planned["config"]["protocol_sha256"]:
        raise ValueError("protocol hash mismatch")
    return {
        "source_files": count,
        "protocol_checked": True,
        "scope": "recorded byte identity; not proof of commit cleanliness",
    }
