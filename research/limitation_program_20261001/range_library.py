"""Exact signed operand-bin dispatch with byte-identical accepted fallbacks."""

from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.range_multiplier import build_range_multiplier, leaf_spec
from research.limitation_program_20261001.constant_library import canonical
from research.limitation_program_20261001.nonrestoring_library import NonRestoringIntegrationLibrary
from research.limitation_program_20261001.prove_range_input import (
    INTEGRATION_LOWERING,
    is_range_entry,
    select_range_site,
    validate_allowed_bits,
    validate_range_entry,
)


class RangeIntegrationLibrary(NonRestoringIntegrationLibrary):
    def __init__(self, path, target, source, allowed_bits=(24, 40, 72), eligible_pairs=None):
        self.allowed_bits = validate_allowed_bits(allowed_bits, target["width"])
        if eligible_pairs is not None and (
            not isinstance(eligible_pairs, (list, tuple, set, frozenset))
            or any(
                not isinstance(pair, (list, tuple))
                or len(pair) != 2
                or any(type(bits) is not int or bits not in self.allowed_bits for bits in pair)
                or tuple(pair) == (target["width"], target["width"])
                for pair in eligible_pairs
            )
        ):
            raise ValueError("eligible signed operand pairs must use declared non-native bins")
        self.eligible_pairs = (
            None if eligible_pairs is None else frozenset(tuple(pair) for pair in eligible_pairs)
        )
        super().__init__(path, target, source, active_bits=min(46, target["width"]))

    def _validate_original_contract(self, index, node, entry):
        if is_range_entry(entry):
            validate_range_entry(
                self.context.target,
                node,
                entry,
                self.bounds,
                locations=self.context.locations,
            )
            return
        super()._validate_original_contract(index, node, entry)

    def get(self, node):
        index = self._requested_node(node)
        proof = select_range_site(
            self.context.target,
            node,
            self.bounds,
            self.allowed_bits,
            locations=self.context.locations,
        )
        if proof is None or (
            self.eligible_pairs is not None
            and tuple(proof["signed_operand_bits"]) not in self.eligible_pairs
        ):
            key, entry = self._copy_original(self._old_keys[index])
            self._record(index, node, key, "fallback", {"signed_operand_range_not_selected": True})
            return key, entry
        bits = proof["signed_operand_bits"]
        spec = dict(leaf_spec(self.w, self.f, *bits), integration_lowering=INTEGRATION_LOWERING)
        key, entry = self._new_leaf(
            node, spec, lambda: build_range_multiplier(self.w, self.f, *bits)
        )
        validate_range_entry(
            self.context.target,
            node,
            entry,
            self.bounds,
            locations=self.context.locations,
        )
        self._record(index, node, key, "mul-signed-range", proof)
        return key, entry


def compile_range_graph(target, path, library):
    if canonical(target) != canonical(library.context.target):
        raise ValueError("compiler target differs from the immutable target snapshot")
    return compile_graph(target, path, library)
