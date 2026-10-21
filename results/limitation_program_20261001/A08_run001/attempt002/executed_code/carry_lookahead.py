"""Exact clean-XOR modular add/sub leaves with two explicit prefix networks.

Every gate is X, CX or CCX. Prefix (generate, propagate) pairs represent
contiguous intervals and obey G*P=0, so their carry OR is an exact XOR.
The output is written only after computation and never controls a gate.
"""
from __future__ import annotations

from research.journal_sprint.reversible_fixed_point import Program

VARIANTS = ("brent-kung", "kogge-stone")
LOWERING = "clean-xor-prefix-add-sub-v1"


def _compose(program, high, low):
    """Return a new high:low pair; the source pairs remain untouched.

    G = Gh XOR (Ph AND Gl), P = Ph AND Pl. Gh and Ph cannot both be
    one; therefore the two generate terms are disjoint. The new G and P
    are disjoint too, since Gl*Pl=0. Reversal later clears both new wires.
    """
    generate, propagate = program.register(2)
    gh, ph = high
    gl, pl = low
    program.gate(gh, generate)
    program.gate(ph, gl, generate)
    program.gate(ph, pl, propagate)
    return generate, propagate


def prefix_pairs(program, pairs, variant):
    """Inclusive prefixes, without padding, of low-to-high singleton pairs.

    Brent-Kung performs its sparse reduction and distribution stages;
    Kogge-Stone doubles the contiguous interval at every dense stage.
    Out-of-place nodes prevent the within-stage ordering changing semantics.
    The truncated last stage works for non-power-of-two widths as well.
    """
    if variant not in VARIANTS:
        raise ValueError("unknown prefix variant")
    pairs = list(pairs)
    count = len(pairs)
    if variant == "kogge-stone":
        distance = 1
        while distance < count:
            previous = pairs
            pairs = previous.copy()
            for index in range(distance, count):
                pairs[index] = _compose(program, previous[index], previous[index - distance])
            distance *= 2
    else:
        distance = 1
        while distance < count:
            previous = pairs
            pairs = previous.copy()
            for index in range(2 * distance - 1, count, 2 * distance):
                pairs[index] = _compose(program, previous[index], previous[index - distance])
            distance *= 2
        distance //= 4
        while distance >= 1:
            previous = pairs
            pairs = previous.copy()
            for index in range(3 * distance - 1, count, 2 * distance):
                pairs[index] = _compose(program, previous[index], previous[index - distance])
            distance //= 2
    return pairs


def build_carry_lookahead(op, width, variant="brent-kung"):
    """Return |a,b,z,0> -> |a,b,z XOR ((a +/- b) mod 2**w),0>.

    Subtraction computes a+(~b)+1. All bit patterns are permitted; signed
    two's-complement and unsigned interpretations share this modular map.
    There are no precision, range or source-law promises on these leaves.
    """
    if op not in ("add", "sub"):
        raise ValueError("add or sub required")
    if type(width) is not int or width < 1:
        raise ValueError("positive integer width required")
    if variant not in VARIANTS:
        raise ValueError("unknown prefix variant")
    program = Program(compact=True)
    arguments = [program.register(width), program.register(width)]
    outputs = [program.register(width)]
    propagate = program.register(width)
    # The carry out is discarded in modular arithmetic, so no g for bit w-1.
    generate = program.register(width - 1) if width > 1 else ()
    second = program.register(width) if op == "sub" else arguments[1]
    start = len(program.gates)
    if op == "sub":
        for source, target in zip(arguments[1], second):
            program.gate(target)
            program.gate(source, target)
    for index in range(width):
        program.gate(arguments[0][index], propagate[index])
        program.gate(second[index], propagate[index])
        if index < width - 1:
            program.gate(arguments[0][index], second[index], generate[index])
    prefixes = prefix_pairs(
        program, list(zip(generate, propagate[:width - 1])), variant,
    )
    end = len(program.gates)
    for index, target in enumerate(outputs[0]):
        program.gate(propagate[index], target)
        if index:
            carry_generate, carry_propagate = prefixes[index - 1]
            program.gate(carry_generate, target)
            if op == "sub":
                # c0=1, hence c_i=G_[i-1:0] XOR P_[i-1:0].
                program.gate(carry_propagate, target)
        elif op == "sub":
            program.gate(target)
    program.undo(start, end)
    return program, arguments, outputs


def leaf_spec(op, width, fraction_bits, variant):
    if op not in ("add", "sub") or variant not in VARIANTS:
        raise ValueError("unknown operation or prefix variant")
    if type(width) is not int or width < 1:
        raise ValueError("positive integer width required")
    if type(fraction_bits) is not int or not 0 <= fraction_bits < width:
        raise ValueError("fraction bits must lie in the word")
    return {
        "op": op, "width": width, "fraction_bits": fraction_bits,
        "params": {}, "variant": variant, "lowering": LOWERING,
        "input_contract": {},
    }
