"""Exact 72-bit ln(2) leaf under a proved signed-seven-bit upper operand.

The static contract is low40 bits zero and the upper32 word equal to the sign
extension of its low7 bits. No dynamic promise check is emitted. Other sources,
including exponential range reduction, require their existing wider fallback.
"""
from research.controlled_source_completion.constant_multiplier import (
    STRATEGIES,
    build_constant_multiplier,
)
from research.journal_sprint.reversible_fixed_point import Program

LOWERING = "log-signed7-embedded47-v1"
COEFFICIENT = 762123384786
WIDTH, FRACTION, SIGNED_UPPER_BITS, CHILD_WIDTH = 72, 40, 7, 47
EMBEDDINGS = ("clean-child-twice", "fused-child-copy")


def input_contract():
    """Higher input bits are sign redundancy, not promised zero."""
    return {"zero_low_bits": FRACTION, "signed_upper_bits": SIGNED_UPPER_BITS}


def contract_holds(value):
    """Check a basis value for tests; this does not prove a coherent graph."""
    if type(value) is not int or not 0 <= value < 1 << WIDTH:
        return False
    if value & ((1 << FRACTION) - 1):
        return False
    upper = value >> FRACTION
    if upper & (1 << 31):
        upper -= 1 << 32
    return -64 <= upper <= 63


def site_proof(target, node_index):
    """Reuse the validated same-graph log-chain guard; reject exp-only chains."""
    from research.limitation_program_20261001.prove_log_exponent import prove_log_site

    return prove_log_site(target, node_index)


def leaf_spec(strategy="signed-digit-carry-save", embedding="fused-child-copy"):
    if strategy not in STRATEGIES or embedding not in EMBEDDINGS:
        raise ValueError("known arithmetic strategy and embedding required")
    return {
        "op": "cmul",
        "width": WIDTH,
        "fraction_bits": FRACTION,
        "coefficient": COEFFICIENT,
        "child_width": CHILD_WIDTH,
        "input_contract": input_contract(),
        "strategy": strategy,
        "embedding": embedding,
        "lowering": LOWERING,
    }


def split_child(child, child_out):
    """Validate the exact compute/copy/reverse boundary before fusing it."""
    count = len(child_out)
    remainder = len(child.gates) - count
    if remainder < 0 or remainder % 2:
        raise ValueError("child has no canonical clean-copy boundary")
    boundary = remainder // 2
    forward = child.gates[:boundary]
    middle = child.gates[boundary:boundary + count]
    reverse = child.gates[boundary + count:]
    if reverse != list(reversed(forward)):
        raise ValueError("child reverse is not its exact forward inverse")
    outputs = set(child_out)
    if any(set(gate) & outputs for gate in forward):
        raise ValueError("child output participates before clean copy")
    if any(
        len(gate) != 2 or gate[1] != target or gate[0] in outputs
        for gate, target in zip(middle, child_out)
    ):
        raise ValueError("child clean-copy boundary is not the declared output XOR")
    sources = tuple(gate[0] for gate in middle)
    if len(set(sources)) != count:
        raise ValueError("child product copy has aliased source bits")
    return forward, middle, reverse, sources


def build_log_constant_multiplier(
    strategy="signed-digit-carry-save", embedding="fused-child-copy"
):
    """Compute original full-width output XOR with preserved input and scratch.

    A=q*2^40 with signed7 q. The 47-bit child computes q*c exactly because
    -64*c >= -2^46 and 63*c < 2^46. Sign extension gives the original72 result.
    Both output interfaces support arbitrary initial words; outputs never control
    computation. The fused wrapper validates the literal child's clean boundary.
    """
    leaf_spec(strategy, embedding)
    if not -64 * COEFFICIENT >= -(1 << 46) or not 63 * COEFFICIENT < 1 << 46:
        raise ValueError("coefficient product does not fit signed47")
    child, child_args, child_outs = build_constant_multiplier(
        CHILD_WIDTH, FRACTION, COEFFICIENT, FRACTION, strategy
    )
    if tuple(child_args[0]) != tuple(range(CHILD_WIDTH)) or tuple(
        child_outs[0]
    ) != tuple(range(CHILD_WIDTH, 2 * CHILD_WIDTH)):
        raise ValueError("unexpected child register interface")
    outer = Program(compact=True)
    argument, output = outer.register(WIDTH), outer.register(WIDTH)
    if embedding == "clean-child-twice":
        product = outer.register(CHILD_WIDTH)
        private = outer.register(child.qubits - 2 * CHILD_WIDTH)
        mapping = argument[:CHILD_WIDTH] + product + private
        for gate in child.gates:
            outer.gate(*(mapping[wire] for wire in gate))
        for index, target in enumerate(output):
            outer.gate(product[min(index, CHILD_WIDTH - 1)], target)
        # The clean-XOR child is self-inverse on arbitrary output with clean
        # scratch. Repeating it erases the private product, not the outer output.
        for gate in child.gates:
            outer.gate(*(mapping[wire] for wire in gate))
    else:
        forward, middle, reverse, sources = split_child(child, child_outs[0])
        private = outer.register(child.qubits - 2 * CHILD_WIDTH)
        mapping = argument[:CHILD_WIDTH] + output[:CHILD_WIDTH] + private
        for gate in forward + middle:
            outer.gate(*(mapping[wire] for wire in gate))
        sign = mapping[sources[-1]]
        for target in output[CHILD_WIDTH:]:
            outer.gate(sign, target)
        for gate in reverse:
            outer.gate(*(mapping[wire] for wire in gate))
    return outer, [argument], [output]

