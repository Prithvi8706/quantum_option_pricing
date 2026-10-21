"""Exact unsigned square-root leaves under a proved high-input-zero promise.

The external input/output stay full width. The promised operand is unsigned,
including its highest active bit. Output XOR, input preservation and complete
remainder cleanup are retained; this module does not prove a graph's promise.
"""

from math import isqrt

from research.controlled_source_completion.primitives import build
from research.journal_sprint.reversible_fixed_point import (
    Program,
    constant,
    copy,
    less_than,
    subtract,
)

LOWERING = "unsigned-narrow-sqrt-v1"
ALGORITHMS = ("padded-historical", "tight-digit-by-digit")
EMBEDDINGS = ("clean-child-twice", "fused-child-copy")


def input_contract(active_bits=46):
    if type(active_bits) is not int or active_bits < 1:
        raise ValueError("positive integer active input width required")
    return {"unsigned_input_bits": active_bits}


def contract_holds(value, width=72, active_bits=46):
    return (
        type(width) is int
        and type(active_bits) is int
        and 1 <= active_bits <= width
        and type(value) is int
        and 0 <= value < 1 << active_bits
    )


def leaf_spec(
    width=72,
    fraction_bits=40,
    active_bits=46,
    algorithm="tight-digit-by-digit",
    embedding="fused-child-copy",
):
    if (
        type(width) is not int
        or type(fraction_bits) is not int
        or type(active_bits) is not int
        or width < 1
        or not 0 <= fraction_bits <= width
        or not 1 <= active_bits <= width
        or algorithm not in ALGORITHMS
        or embedding not in EMBEDDINGS
    ):
        raise ValueError("valid widths, exact algorithm and embedding required")
    radicand_bits = active_bits + fraction_bits
    result_bits = isqrt(((1 << active_bits) - 1) << fraction_bits).bit_length()
    padded_width = max(active_bits, fraction_bits)
    return {
        "op": "sqrt",
        "width": width,
        "fraction_bits": fraction_bits,
        "active_input_bits": active_bits,
        "domain": "unsigned high bits zero; highest active bit may be one",
        "radicand_bits": radicand_bits,
        "result_bits": result_bits,
        "child_input_bits": padded_width if algorithm == ALGORITHMS[0] else active_bits,
        "child_output_bits": padded_width if algorithm == ALGORITHMS[0] else result_bits,
        "remainder_bits": padded_width + 2 if algorithm == ALGORITHMS[0] else result_bits + 2,
        "input_contract": input_contract(active_bits),
        "algorithm": algorithm,
        "embedding": embedding,
        "lowering": LOWERING,
    }


def tight_child(active_bits, fraction_bits):
    """Restoring square root with just k root bits and k+2 remainder bits.

    At stage s the previous remainder is less than 2*q+1 for the s-bit
    accumulated root q. Before subtraction, 4*r+digit is less than 2**(s+3).
    The largest stage has s=k-1, so k+2 bits hold every intermediate exactly.
    Its trial 4*q+1 also fits. Each comparison/subtraction is unchanged from
    the historical digit-by-digit recurrence, with all remainders uncomputed.
    """
    k = (active_bits + fraction_bits + 1) // 2
    remainder_width = k + 2
    p = Program(compact=True)
    argument, output = p.register(active_bits), p.register(k)
    roots = p.register(k)
    remainders = [p.register(remainder_width) for _ in range(k + 1)]
    trial, conditional = p.register(remainder_width), p.register(remainder_width)
    diff, extended = p.register(remainder_width + 1), p.register(remainder_width + 1)
    helper = p.register(1)[0]
    start = len(p.gates)
    for stage in range(k):
        position = k - 1 - stage
        previous, next_remainder = remainders[stage : stage + 2]
        for bit in range(remainder_width - 2):
            p.gate(previous[bit], next_remainder[bit + 2])
        for bit in (0, 1):
            source = 2 * position + bit - fraction_bits
            if 0 <= source < active_bits:
                p.gate(argument[source], next_remainder[bit])
        constant(p, trial, 1)
        for bit in range(position + 1, k):
            p.gate(roots[bit], trial[bit - position + 1])
        less_than(p, next_remainder, trial, roots[position], diff, extended, helper)
        p.gate(roots[position])
        for bit in range(remainder_width):
            p.gate(roots[position], trial[bit], conditional[bit])
        subtract(p, conditional, next_remainder, helper)
        for bit in range(remainder_width):
            p.gate(roots[position], trial[bit], conditional[bit])
        for bit in range(position + 1, k):
            p.gate(roots[bit], trial[bit - position + 1])
        constant(p, trial, 1)
    stop = len(p.gates)
    copy(p, roots, output)
    p.undo(start, stop)
    return p, [argument], [output]


def split_clean_child(child, output):
    """Require the literal compute/output-XOR/exact-reverse boundary."""
    count = len(output)
    remainder = len(child.gates) - count
    if remainder < 0 or remainder % 2:
        raise ValueError("child has no canonical clean-copy boundary")
    boundary = remainder // 2
    forward = child.gates[:boundary]
    middle = child.gates[boundary : boundary + count]
    reverse = child.gates[boundary + count :]
    if reverse != list(reversed(forward)):
        raise ValueError("child reverse is not the exact forward inverse")
    output_wires = set(output)
    if any(set(gate) & output_wires for gate in forward):
        raise ValueError("child output participates before clean copy")
    if any(
        len(gate) != 2 or gate[1] != target or gate[0] in output_wires
        for gate, target in zip(middle, output)
    ):
        raise ValueError("child copy is not the declared output XOR")
    sources = tuple(gate[0] for gate in middle)
    if len(set(sources)) != count:
        raise ValueError("child result copy has aliased source bits")
    return forward, middle, reverse


def build_narrow_sqrt(
    width=72,
    fraction_bits=40,
    active_bits=46,
    algorithm="tight-digit-by-digit",
    embedding="fused-child-copy",
):
    """Emit full-width out XOR isqrt(unsigned(argument) << fraction_bits).

    This formula is guaranteed only for argument < 2**active_bits. Both
    wrappers leave high output bits unchanged and restore all private scratch.
    """
    spec = leaf_spec(width, fraction_bits, active_bits, algorithm, embedding)
    if algorithm == "padded-historical":
        child, arguments, outputs = build("sqrt", spec["child_input_bits"], fraction_bits)
    else:
        child, arguments, outputs = tight_child(active_bits, fraction_bits)
    argument_width, output_width = len(arguments[0]), len(outputs[0])
    if arguments != [tuple(range(argument_width))] or outputs != [
        tuple(range(argument_width, argument_width + output_width))
    ]:
        raise ValueError("unexpected child register interface")
    outer = Program(compact=True)
    argument, output = outer.register(width), outer.register(width)
    padding_width = argument_width - active_bits
    padding = outer.register(padding_width) if padding_width else ()
    scratch = outer.register(child.qubits - argument_width - output_width)
    if embedding == "clean-child-twice":
        product = outer.register(output_width)
        mapping = argument[:active_bits] + padding + product + scratch
        for gate in child.gates:
            outer.gate(*(mapping[wire] for wire in gate))
        copy(outer, product, output[:output_width])
        for gate in child.gates:
            outer.gate(*(mapping[wire] for wire in gate))
    else:
        forward, middle, reverse = split_clean_child(child, outputs[0])
        mapping = argument[:active_bits] + padding + output[:output_width] + scratch
        for gate in forward + middle + reverse:
            outer.gate(*(mapping[wire] for wire in gate))
    return outer, [argument], [output]
