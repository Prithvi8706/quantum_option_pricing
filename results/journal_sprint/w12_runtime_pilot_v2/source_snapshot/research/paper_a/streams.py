"""Annex D: deterministic random-stream derivation.

Python's built-in hash() is salted per process and is FORBIDDEN here. Every
stream is reproducible from its literal key string alone.
"""

from __future__ import annotations

import hashlib

import numpy as np

NAMESPACES = frozenset(
    {
        "paper-a/pilot/v1",
        "paper-a/main/v1",
        "paper-a/mc/v1",
        "paper-a/asian/v1",
    }
)
PURPOSES = frozenset({"shots", "noise", "bootstrap", "audit"})
TRANSPILER_SEED = 20260727

_PREFIX = "paper-a/v1"
_SEP = " | "


def stream_key(
    namespace: str,
    experiment_uuid: str,
    phase: str,
    config_id: str,
    n: int,
    replicate: int,
    condition: str,
    purpose: str,
) -> str:
    """Build the literal Annex D stream key. No whitespace normalization."""
    if namespace not in NAMESPACES:
        raise ValueError(f"unknown namespace {namespace!r}")
    if purpose not in PURPOSES:
        raise ValueError(f"unknown purpose {purpose!r}")
    for value in (experiment_uuid, phase, config_id, condition):
        if not isinstance(value, str) or _SEP in value:
            raise ValueError(f"stream fields must be strings without {_SEP!r}")
    if any(
        not isinstance(value, (int, np.integer)) or isinstance(value, bool) or value < 0
        for value in (n, replicate)
    ):
        raise ValueError("n and replicate must be nonnegative integers")
    return _SEP.join(
        [
            _PREFIX,
            namespace,
            experiment_uuid,
            phase,
            config_id,
            str(n),
            str(replicate),
            condition,
            purpose,
        ]
    )


def seed_sequence(key: str) -> np.random.SeedSequence:
    """SHA-256 the key; use the first 128 bits as four big-endian uint32."""
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    words = [int.from_bytes(digest[i : i + 4], "big") for i in range(0, 16, 4)]
    return np.random.SeedSequence(words)


def generator(key: str) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64DXSM(seed_sequence(key)))
