"""Proof-dispatched narrowed shift counts, retaining archived fallback bytes."""

from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.narrow_shift import build_narrow_shift, leaf_spec
from research.limitation_program_20261001.constant_library import canonical
from research.limitation_program_20261001.prove_shift_input import (
    INTEGRATION_LOWERING,
    is_narrow_shift_entry,
    prove_shift_site,
    validate_shift_entry,
)
from research.limitation_program_20261001.sqrt_library import NarrowSqrtIntegrationLibrary


class ShiftIntegrationLibrary(NarrowSqrtIntegrationLibrary):
    def __init__(self, path, target, source, count_bits=7):
        if type(count_bits) is not int or not 1 <= count_bits <= target["width"]:
            raise ValueError("invalid signed shift count width")
        self.count_bits = count_bits
        # Parent validates accepted sqrt/log promises and computes same-SSA bounds.
        # Its dispatch is deliberately unused: nonspecialized leaves keep old bytes.
        super().__init__(path, target, source, active_bits=min(46, target["width"]))

    def _validate_original_contract(self, index, node, entry):
        if is_narrow_shift_entry(entry):
            validate_shift_entry(self.context.target, node, entry, self.bounds)
            return
        super()._validate_original_contract(index, node, entry)

    def get(self, node):
        index = self._requested_node(node)
        proof = prove_shift_site(self.context.target, node, self.bounds, self.count_bits)
        if proof is None:
            key, entry = self._copy_original(self._old_keys[index])
            self._record(index, node, key, "fallback", {"shift_range_not_proved": True})
            return key, entry
        spec = dict(
            leaf_spec(self.w, self.f, self.count_bits),
            integration_lowering=INTEGRATION_LOWERING,
        )
        key, entry = self._new_leaf(
            node, spec, lambda: build_narrow_shift(self.w, self.f, self.count_bits)
        )
        validate_shift_entry(self.context.target, node, entry, self.bounds)
        self._record(index, node, key, "shift-narrow", proof)
        return key, entry


def compile_shift_graph(target, path, library):
    """Bind input declarations, tables, operations and outputs to one snapshot."""
    if canonical(target) != canonical(library.context.target):
        raise ValueError("compiler target differs from the immutable target snapshot")
    return compile_graph(target, path, library)
