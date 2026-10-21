"""Proof-dispatched narrowed sqrt; archived fallbacks retain their exact bytes."""

from research.controlled_source_completion.narrow_sqrt import (
    ALGORITHMS,
    EMBEDDINGS,
    build_narrow_sqrt,
    leaf_spec,
)
from research.limitation_program_20261001.constant_library import (
    ConstantIntegrationLibrary,
    canonical,
)
from research.controlled_source_completion.compiler import compile_graph
from research.limitation_program_20261001.interval_bounds import bound_graph
from research.limitation_program_20261001.prove_sqrt_input import (
    INTEGRATION_LOWERING,
    is_narrow_sqrt_entry,
    prove_sqrt_site,
    validate_sqrt_entry,
)


class NarrowSqrtIntegrationLibrary(ConstantIntegrationLibrary):
    def __init__(
        self,
        path,
        target,
        source,
        algorithm="tight-digit-by-digit",
        embedding="fused-child-copy",
        active_bits=46,
    ):
        if algorithm not in ALGORITHMS or embedding not in EMBEDDINGS:
            raise ValueError("known exact square-root algorithm and embedding required")
        if type(active_bits) is not int or not 1 <= active_bits <= target["width"]:
            raise ValueError("invalid unsigned input width")
        self.algorithm, self.embedding, self.active_bits = algorithm, embedding, active_bits
        self.bounds, self.bound_rules = bound_graph(target)
        super().__init__(path, target, source, log_strategy=None)

    def _validate_original_contract(self, index, node, entry):
        if is_narrow_sqrt_entry(entry):
            validate_sqrt_entry(self.context.target, node, entry, self.bounds)
            return
        super()._validate_original_contract(index, node, entry)

    def get(self, node):
        index = self._requested_node(node)
        proof = prove_sqrt_site(self.context.target, node, self.bounds, self.active_bits)
        if proof is None:
            key, entry = self._copy_original(self._old_keys[index])
            self._record(index, node, key, "fallback", {"sqrt_range_not_proved": True})
            return key, entry
        spec = dict(
            leaf_spec(self.w, self.f, self.active_bits, self.algorithm, self.embedding),
            integration_lowering=INTEGRATION_LOWERING,
        )
        key, entry = self._new_leaf(
            node,
            spec,
            lambda: build_narrow_sqrt(
                self.w,
                self.f,
                self.active_bits,
                self.algorithm,
                self.embedding,
            ),
        )
        validate_sqrt_entry(self.context.target, node, entry, self.bounds)
        self._record(index, node, key, "sqrt-narrow", proof)
        return key, entry


def compile_sqrt_graph(target, path, library):
    """Bind the entire declared graph, including input nodes, before compiling."""
    if canonical(target) != canonical(library.context.target):
        raise ValueError("compiler target differs from the immutable target snapshot")
    return compile_graph(target, path, library)
