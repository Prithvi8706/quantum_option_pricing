"""Protocol gates that remain active under Python optimization."""

from pathlib import Path, PureWindowsPath


def relative_archive_path(name):
    """Accept portable relative manifest names; reject traversal and drive paths."""
    path = PureWindowsPath(name)
    if path.drive or path.root or not path.parts or ".." in path.parts:
        raise ValueError(f"unsafe archive path: {name}")
    return Path(*path.parts)


def archive_path(folder, name):
    path = folder / relative_archive_path(name)
    if folder.resolve() not in path.resolve().parents:
        raise ValueError(f"archive path escapes root: {name}")
    return path


def require(condition, detail="protocol integrity check failed"):
    if not condition:
        raise ValueError(detail)
