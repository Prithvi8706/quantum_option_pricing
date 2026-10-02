"""Run provenance shared by Stage C runners (ANALYSIS_SPEC_STAGE_C.md section 0, deviation D5).

Every runner added or amended after 2 October 2026 records the commit, whether the
checkout was dirty, and the SHA-256 of the spec, the T0 lock and every Stage C module.
"""

import hashlib
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SPEC = "manuscript/advantage-frontier-2026-09-23/ANALYSIS_SPEC_STAGE_C.md"
LOCK = "research/frontier_replay_20261001/t0_requirements.lock"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def meta(**extra):
    """Provenance block; `extra` carries item-specific roots and settings."""
    return dict(commit=git("rev-parse", "HEAD"), dirty=bool(git("status", "--porcelain")),
                spec_sha256=sha(ROOT / SPEC), lock_sha256=sha(ROOT / LOCK),
                code_sha256={p.name: sha(p) for p in sorted(Path(__file__).parent.glob("*.py"))},
                python=sys.version, numpy=np.__version__, **extra)


def require_clean():
    """Refuse to run from a dirty checkout (spec section 0: clean detached worktrees only)."""
    if git("status", "--porcelain"):
        raise SystemExit("refusing to run: the checkout is dirty; run from a clean worktree")
