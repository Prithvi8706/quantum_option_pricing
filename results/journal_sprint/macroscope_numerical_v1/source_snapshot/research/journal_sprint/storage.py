"""Exclusive, auditable local experiment outputs and purpose-separated streams."""

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
from datetime import datetime, timezone

import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[2]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rng_for(*keys):
    payload = json.dumps(keys, separators=(",", ":"), allow_nan=False).encode()
    seed = int.from_bytes(hashlib.sha256(payload).digest()[:16], "big")
    return np.random.default_rng(seed)


def write_json(path, value):
    with Path(path).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def start_run(path, config):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=False)
    sources = sorted((ROOT / "research/journal_sprint").rglob("*.py"))
    sources.append(ROOT / "docs/journal_sprint/PROTOCOL_V1.md")
    hashes = {str(p.relative_to(ROOT)): sha256(p) for p in sources}
    git = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()
    write_json(
        path / "planned.json",
        {
            "started_utc": datetime.now(timezone.utc).isoformat(),
            "config": config,
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "git_head": git,
            "source_sha256": hashes,
            "threads": {
                k: os.environ.get(k)
                for k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
            },
        },
    )
    return path


def finish_run(path):
    write_json(
        path / "complete.json",
        {
            "finished_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": {
                str(p.relative_to(path)): sha256(p) for p in sorted(path.rglob("*")) if p.is_file()
            },
        },
    )
