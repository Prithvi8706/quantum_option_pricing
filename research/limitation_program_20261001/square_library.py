"""Proof-dispatched signed squares, retaining all archived fallback bytes."""

from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.signed_square import build_signed_square, leaf_spec
from research.limitation_program_20261001.constant_library import canonical
from research.limitation_program_20261001.prove_square_input import (
    INTEGRATION_LOWERING,
    is_square_entry,
    prove_square_site,
    validate_square_entry,
)
from research.limitation_program_20261001.sqrt_library import NarrowSqrtIntegrationLibrary


class SquareIntegrationLibrary(NarrowSqrtIntegrationLibrary):
    def __init__(self, path, target, source):
        # Parent validates archived sqrt promises; it never dispatches here.
        super().__init__(path, target, source, active_bits=min(46, target["width"]))

    def _validate_original_contract(self, index, node, entry):
        if is_square_entry(entry):
            validate_square_entry(self.context.target, node, entry)
            return
        super()._validate_original_contract(index, node, entry)

    def get(self, node):
        index = self._requested_node(node)
        proof = prove_square_site(self.context.target, node)
        if proof is None:
            key, entry = self._copy_original(self._old_keys[index])
            self._record(index, node, key, "fallback", None)
            return key, entry
        spec = dict(
            leaf_spec(self.w, self.f, "brent-kung"), integration_lowering=INTEGRATION_LOWERING
        )
        key, entry = self._new_leaf(node, spec, lambda: build_signed_square(self.w, self.f))
        validate_square_entry(self.context.target, node, entry)
        self._record(index, node, key, "signed-square", proof)
        return key, entry


def compile_square_graph(target, path, library):
    if canonical(target) != canonical(library.context.target):
        raise ValueError("compiler target differs from the immutable target snapshot")
    return compile_graph(target, path, library)
