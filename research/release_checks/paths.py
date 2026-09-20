"""Portable repository-relative names, including old Windows manifests."""
from pathlib import Path, PurePosixPath


def relative_name(name):
    if not isinstance(name, str) or not name or ':' in name or '\x00' in name:
        raise ValueError('invalid relative path')
    name = name.replace('\\', '/')
    parts = name.split('/')
    if any(p in ('', '.', '..') for p in parts):
        raise ValueError('absolute, traversal or ambiguous path')
    return PurePosixPath(name).as_posix()


def within(root, name):
    root = Path(root).resolve()
    target = (root / relative_name(name)).resolve()
    if root not in target.parents:
        raise ValueError('path or symlink escapes root')
    return target


def normalized(mapping):
    result = {}
    for name, value in mapping.items():
        key = relative_name(name)
        if key in result:
            raise ValueError('duplicate normalized path')
        result[key] = value
    return result
