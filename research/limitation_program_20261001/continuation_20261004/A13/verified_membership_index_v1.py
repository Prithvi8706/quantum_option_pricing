"""Exact membership index over a fixed, already verified metadata-record snapshot.

This module performs no path resolution, hashing, receipt admission, or scientific work.
Its use in a scientific auditor requires a separate reviewed integration.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class VerifiedMembershipIndex:
    """Retain every full row and every duplicate position, with exact string keys."""

    records: tuple[Mapping[str, object], ...]
    positions: Mapping[tuple[str, str], tuple[int, ...]]

    def witnesses(self, verified_input_path: str, expected_sha256: str) -> tuple[int, ...]:
        return self.positions.get((verified_input_path, expected_sha256), ())

    def contains(self, verified_input_path: str, expected_sha256: str) -> bool:
        return bool(self.witnesses(verified_input_path, expected_sha256))


def build_verified_membership_index(records) -> VerifiedMembershipIndex:
    """Build a view only after the unchanged caller verifies all complete records.

    Keys are neither canonicalized nor case-folded. Full copied rows remain in original
    order, including duplicates and multiple hashes for one path. Invalid, incomplete
    rows are outside the equivalence contract and are explicitly rejected.
    """
    snapshots = []
    positions = {}
    for number, row in enumerate(records):
        if type(row) is not dict:
            raise ValueError("Expected a complete already verified record dictionary")
        path = row.get("verified_input_path")
        expected = row.get("original_expected_sha256")
        if type(path) is not str or type(expected) is not str:
            raise ValueError("Expected exact typed membership strings")
        snapshots.append(MappingProxyType(dict(row)))
        positions.setdefault((path, expected), []).append(number)
    return VerifiedMembershipIndex(
        tuple(snapshots),
        MappingProxyType({key: tuple(numbers) for key, numbers in positions.items()}),
    )
