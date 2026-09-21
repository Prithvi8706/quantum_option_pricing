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


def archive_names(names):
    result = {relative_archive_path(name).as_posix() for name in names}
    if len(result) != len(names):
        raise ValueError("aliased archive names")
    return result


def require_archives(base, names):
    missing = [name for name in names if not (base / name / "complete.json").is_file()]
    if missing:
        raise FileNotFoundError(
            f"Complete local archives missing at {base}: {', '.join(missing)}. "
            "Supply --archive-root (or --source for a single archive). "
            "See docs/journal_sprint/ARCHIVE_INPUTS.md; bundled summaries are not full archives."
        )


def require(condition, detail="protocol integrity check failed"):
    if not condition:
        raise ValueError(detail)
