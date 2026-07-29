import hashlib

import numpy as np
import pytest

from research.paper_a.streams import (
    NAMESPACES, PURPOSES, TRANSPILER_SEED, generator, seed_sequence,
    stream_key,
)

ARGS = dict(namespace="paper-a/main/v1", experiment_uuid="abc-123",
            phase="E3", config_id="E022", n=3, replicate=7,
            condition="ideal", purpose="shots")


def test_key_is_the_exact_literal_annex_d_format():
    assert stream_key(**ARGS) == (
        "paper-a/v1 | paper-a/main/v1 | abc-123 | E3 | E022 | 3 | 7 "
        "| ideal | shots"
    )


def test_frozen_namespaces_and_purposes():
    assert NAMESPACES == frozenset({"paper-a/pilot/v1", "paper-a/main/v1",
                                    "paper-a/mc/v1", "paper-a/asian/v1"})
    assert {"shots", "noise", "bootstrap", "audit"} <= PURPOSES


def test_unknown_namespace_or_purpose_is_rejected():
    with pytest.raises(ValueError):
        stream_key(**{**ARGS, "namespace": "paper-a/rogue/v1"})
    with pytest.raises(ValueError):
        stream_key(**{**ARGS, "purpose": "vibes"})


def test_seed_sequence_uses_first_128_digest_bits_as_four_be_uint32():
    key = stream_key(**ARGS)
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    expected = [int.from_bytes(digest[i:i + 4], "big") for i in range(0, 16, 4)]
    assert list(seed_sequence(key).entropy) == expected


def test_generator_is_pcg64dxsm_and_reproducible():
    key = stream_key(**ARGS)
    g1, g2 = generator(key), generator(key)
    assert isinstance(g1.bit_generator, np.random.PCG64DXSM)
    assert np.array_equal(g1.random(16), g2.random(16))


def test_distinct_conditions_give_independent_streams():
    ideal = generator(stream_key(**{**ARGS, "condition": "ideal"}))
    noisy = generator(stream_key(**{**ARGS, "condition": "p1e-3"}))
    assert not np.array_equal(ideal.random(16), noisy.random(16))


def test_pilot_and_main_namespaces_never_collide():
    pilot = generator(stream_key(**{**ARGS, "namespace": "paper-a/pilot/v1"}))
    main = generator(stream_key(**{**ARGS, "namespace": "paper-a/main/v1"}))
    assert not np.array_equal(pilot.random(16), main.random(16))


def test_every_field_changes_the_stream():
    base = generator(stream_key(**ARGS)).random(8)
    for field, value in [("namespace", "paper-a/mc/v1"),
                         ("experiment_uuid", "zzz"), ("phase", "E4"),
                         ("config_id", "E023"), ("n", 4), ("replicate", 8),
                         ("condition", "p1e-3"), ("purpose", "noise")]:
        other = generator(stream_key(**{**ARGS, field: value})).random(8)
        assert not np.array_equal(base, other), f"{field} did not change stream"


def test_transpiler_seed_is_frozen():
    assert TRANSPILER_SEED == 20260727
