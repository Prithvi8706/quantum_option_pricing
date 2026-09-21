"""Environment lock capture.

Every result record embeds the output of `capture_environment()` so a frozen
experiment directory can be reproduced without consulting the working tree.
"""

from __future__ import annotations

import datetime as _dt
import platform
import subprocess
import sys
from importlib import metadata
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

TRACKED_PACKAGES = (
    "qiskit-terra",
    "qiskit-aer",
    "qiskit-algorithms",
    "qiskit-finance",
    "numpy",
    "scipy",
)


def _package_versions() -> dict[str, str]:
    versions = {}
    for name in TRACKED_PACKAGES:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "ABSENT"
    return versions


def _git_commit() -> str:
    if not (_REPO_ROOT / ".git").exists():
        return "unavailable"
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            cwd=_REPO_ROOT,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _git_dirty():
    if not (_REPO_ROOT / ".git").exists():
        return None
    try:
        output = subprocess.check_output(
            ["git", "status", "--porcelain"],
            text=True,
            cwd=_REPO_ROOT,
            stderr=subprocess.DEVNULL,
        )
        return bool(output.strip())
    except (OSError, subprocess.CalledProcessError):
        return None


def capture_environment() -> dict:
    """Return the complete environment lock for a result record."""
    return {
        "python_version": sys.version.split()[0],
        "packages": _package_versions(),
        "git_commit": _git_commit(),
        "git_dirty": _git_dirty(),
        "platform": platform.platform(),
        "captured_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }
