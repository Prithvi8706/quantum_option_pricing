"""Inventory license evidence; deliberately does not infer legal compatibility."""

from .hashes import digest
from .paths import relative_name, within


def license_inventory(root, names):
    names = [relative_name(n) for n in names]
    if not names or len(set(names)) != len(names):
        raise ValueError("nonempty unique license scope required")
    entries = []
    for name in names:
        path = within(root, name)
        if not path.read_text(encoding="utf-8").strip():
            raise ValueError("empty license evidence: " + name)
        entries.append({"path": name, "sha256": digest(path), "bytes": path.stat().st_size})
    return {
        "files": entries,
        "compatibility_review_complete": False,
        "dependency_license_review_complete": False,
    }
