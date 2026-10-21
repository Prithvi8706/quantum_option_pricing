"""Exact non-restoring sqrt dispatch with adopted signed7 shift fallbacks."""

from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.nonrestoring_sqrt import (
    build_nonrestoring_sqrt,
    leaf_spec,
)
from research.limitation_program_20261001.constant_library import canonical
from research.limitation_program_20261001.prove_nonrestoring_input import (
    INTEGRATION_LOWERING,
    is_nonrestoring_entry,
    prove_nonrestoring_site,
    validate_nonrestoring_entry,
)
from research.limitation_program_20261001.shift_library import ShiftIntegrationLibrary


class NonRestoringIntegrationLibrary(ShiftIntegrationLibrary):
    def __init__(self, path, target, source, active_bits=46):
        if type(active_bits) is not int or not 1 <= active_bits <= target["width"]:
            raise ValueError("invalid unsigned non-restoring input width")
        # The parent's sqrt constructor computes bound_graph before its source
        # validation dispatches here. Preserve the separate requested bit count:
        # that constructor also assigns its own historical active_bits field.
        self.nonrestoring_active_bits = active_bits
        super().__init__(path, target, source, count_bits=min(7, target["width"]))

    def _validate_original_contract(self, index, node, entry):
        if is_nonrestoring_entry(entry):
            validate_nonrestoring_entry(self.context.target, node, entry, self.bounds)
            return
        # ShiftIntegrationLibrary revalidates adopted signed-count leaves;
        # NarrowSqrtIntegrationLibrary revalidates historical roots and log leaves.
        super()._validate_original_contract(index, node, entry)

    def get(self, node):
        index = self._requested_node(node)
        proof = prove_nonrestoring_site(
            self.context.target, node, self.bounds, self.nonrestoring_active_bits
        )
        if proof is None:
            key, entry = self._copy_original(self._old_keys[index])
            self._record(index, node, key, "fallback", {"sqrt_range_not_proved": True})
            return key, entry
        spec = dict(
            leaf_spec(self.w, self.f, active_bits=self.nonrestoring_active_bits),
            integration_lowering=INTEGRATION_LOWERING,
        )
        key, entry = self._new_leaf(
            node,
            spec,
            lambda: build_nonrestoring_sqrt(
                self.w, self.f, active_bits=self.nonrestoring_active_bits
            ),
        )
        validate_nonrestoring_entry(self.context.target, node, entry, self.bounds)
        self._record(index, node, key, "sqrt-nonrestoring", proof)
        return key, entry


def compile_nonrestoring_graph(target, path, library):
    """Bind every input, operation, literal table and named output to one target."""
    if canonical(target) != canonical(library.context.target):
        raise ValueError("compiler target differs from the immutable target snapshot")
    return compile_graph(target, path, library)
