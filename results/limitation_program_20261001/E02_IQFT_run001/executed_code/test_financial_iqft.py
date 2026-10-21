"""Check CP phase/sign and the actual reused IQFT strings against Fourier inversion."""

from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from research.limitation_program_20261001.experiment_checkpoint import read
from research.limitation_program_20261001.financial_iqft import iqft_operations, rz_operations


ROOT = Path(__file__).resolve().parents[2]


def records():
    return read(ROOT / "results/controlled_completion_followup/synthesis_rotations.json")[
        "rotations"
    ]


def matrix(operations, bits):
    dimension = 1 << bits
    result = np.eye(dimension, dtype=complex)
    for operation in operations:
        gate, wires = operation["gate"], operation["wires"]
        if gate in ("cx", "swap"):
            permutation = []
            for word in range(dimension):
                if gate == "cx":
                    changed = word ^ ((1 << wires[1]) if (word >> wires[0]) & 1 else 0)
                else:
                    changed = word ^ (
                        ((1 << wires[0]) | (1 << wires[1]))
                        if ((word >> wires[0]) ^ (word >> wires[1])) & 1
                        else 0
                    )
                permutation.append(changed)
            result = result[permutation, :]
        else:
            wire = wires[0]
            if gate in ("h", "x"):
                original = result.copy()
                for word in range(dimension):
                    flipped = word ^ (1 << wire)
                    if gate == "x":
                        result[word] = original[flipped]
                    elif not (word >> wire) & 1:
                        result[word] = (original[word] + original[flipped]) / np.sqrt(2)
                    else:
                        result[word] = (original[flipped] - original[word]) / np.sqrt(2)
            else:
                phase = {
                    "t": np.exp(1j * np.pi / 4),
                    "tdg": np.exp(-1j * np.pi / 4),
                    "s": 1j,
                    "sdg": -1j,
                }[gate]
                for word in range(dimension):
                    if (word >> wire) & 1:
                        result[word] *= phase
    return result


@pytest.mark.parametrize("bits", (2, 3, 4))
def test_actual_approximate_iqft_matches_inverse_fourier_up_to_scalar(bits):
    actual = matrix(iqft_operations(list(range(bits)), records()), bits)
    dimension = 1 << bits
    row, column = np.indices((dimension, dimension))
    expected = np.exp(-2j * np.pi * row * column / dimension) / np.sqrt(dimension)
    scalar = actual[0, 0] / expected[0, 0]
    assert np.max(np.abs(actual - scalar * expected)) < 1e-12
    assert np.max(np.abs(actual.conj().T @ actual - np.eye(dimension))) < 1e-12


def test_signed_string_inverse_preserves_controlled_relative_phase():
    source = records()
    positive = matrix(rz_operations(0, 2, 1, source), 1)
    negative = matrix(rz_operations(0, 2, -1, source), 1)
    assert np.max(np.abs(negative @ positive - np.eye(2))) < 1e-12
    ratio = positive[1, 1] / positive[0, 0]
    assert abs(ratio - np.exp(1j * np.pi / 8)) < 1e-12


def test_complete_rotation_error_is_below_declared_failure_allowance():
    library = read(ROOT / "results/controlled_completion_followup/synthesis_rotations.json")
    elementary = Fraction(*library["common_operator_epsilon_exact"])
    assert 2 * 4725 * elementary < Fraction(1, 1000)
