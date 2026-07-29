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
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()


def capture_environment() -> dict:
    """Return the complete environment lock for a result record."""
    return {
        "python_version": sys.version.split()[0],
        "packages": _package_versions(),
        "git_commit": _git_commit(),
        "platform": platform.platform(),
        "captured_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }
