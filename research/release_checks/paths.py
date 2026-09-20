"""Portable repository-relative names, including old Windows manifests."""

from pathlib import Path, PurePosixPath


def relative_name(name):
    if not isinstance(name, str) or not name or ":" in name or "\x00" in name:
        raise ValueError("invalid relative path")
    name = name.replace("\\", "/")
    parts = name.split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise ValueError("absolute, traversal or ambiguous path")
    reserved = {"CON", "PRN", "AUX", "NUL"} | {
        prefix + str(i) for prefix in ("COM", "LPT") for i in range(1, 10)
    }
    if any(p.rstrip(" .") != p or p.split(".")[0].upper() in reserved for p in parts):
        raise ValueError("nonportable Windows device or trailing-dot/space alias")
    return PurePosixPath(name).as_posix()


def within(root, name):
    root = Path(root).resolve()
    target = (root / relative_name(name)).resolve()
    if root not in target.parents:
        raise ValueError("path or symlink escapes root")
    return target


def normalized(mapping):
    result = {}
    seen = set()
    for name, value in mapping.items():
        key = relative_name(name)
        if key.casefold() in seen:
            raise ValueError("duplicate normalized path")
        seen.add(key.casefold())
        result[key] = value
    return result
