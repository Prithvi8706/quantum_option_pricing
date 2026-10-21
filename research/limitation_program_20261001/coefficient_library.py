"""Exact full-domain coefficient replacements with preserved accepted fallbacks.

This reader binds each replacement to the actual immutable ``cmul`` invocation.
There is no narrowed or zero-low input promise: every emitted leaf retains one
native signed input and one native clean-XOR output. Accepted range, root, shift
and logarithm contracts are revalidated by the inherited readers.
"""

from collections.abc import Mapping
import hashlib
import json

from research.controlled_source_completion.compiler import compile_graph
from research.controlled_source_completion.constant_multiplier import (
    build_constant_multiplier,
)
from research.controlled_source_completion.prefix_constant_multiplier import (
    STRATEGIES as PREFIX_STRATEGIES,
    build_prefix_constant_multiplier,
)
from research.limitation_program_20261001.constant_library import canonical
from research.limitation_program_20261001.range_library import RangeIntegrationLibrary
from research.limitation_program_20261001.prove_coefficient_input import (
    FRONTIER,
    STRATEGIES,
    coefficient_leaf_spec,
    is_coefficient_entry,
    validate_coefficient_entry,
)


class CoefficientIntegrationLibrary(RangeIntegrationLibrary):
    """Replace only declared cmul coefficients; byte-copy every other old leaf."""

    def __init__(self, path, target, source, replacements=None):
        replacements = {} if replacements is None else replacements
        declared = {
            node["params"].get("c")
            for node in target["nodes"]
            if node["op"] == "cmul" and type(node["params"].get("c")) is int
        }
        if (
            not isinstance(replacements, Mapping)
            or len(replacements) > 3
            or any(
                type(coefficient) is not int
                or coefficient not in declared
                or not isinstance(strategy, str)
                or strategy not in STRATEGIES
                for coefficient, strategy in replacements.items()
            )
        ):
            raise ValueError(
                "at most three actual integer cmul coefficients and known strategies required"
            )
        self.coefficient_replacements = dict(replacements)
        # The parent is used for original-contract validation only. Its range
        # dispatch is never called; bins merely satisfy the native constructor.
        width = target["width"]
        bins = tuple(sorted({min(24, width), min(40, width), width}))
        super().__init__(path, target, source, allowed_bits=bins)

    def _validate_original_contract(self, index, node, entry):
        if is_coefficient_entry(entry):
            validate_coefficient_entry(
                self.context.target, node, entry, locations=self.context.locations
            )
            return
        super()._validate_original_contract(index, node, entry)

    def get(self, node):
        index = self._requested_node(node)
        coefficient = node["params"].get("c")
        if node["op"] != "cmul" or coefficient not in self.coefficient_replacements:
            key, entry = self._copy_original(self._old_keys[index])
            self._record(index, node, key, "fallback", {"coefficient_not_selected": True})
            return key, entry
        strategy = self.coefficient_replacements[coefficient]
        spec = coefficient_leaf_spec(self.w, self.f, coefficient, strategy)
        # An outer marker preserves admission even if a cached specification is
        # replaced with a malformed value. It introduces no input restriction.
        expected_key = hashlib.sha256(canonical(spec).encode()).hexdigest()[:20]
        metadata_path = self.path / (expected_key + ".json")
        existing = expected_key in self.entries or metadata_path.exists()
        if metadata_path.exists() and expected_key not in self.entries:
            validate_coefficient_entry(
                self.context.target,
                node,
                json.loads(metadata_path.read_text(encoding="utf-8")),
                locations=self.context.locations,
            )

        def builder():
            if strategy in PREFIX_STRATEGIES:
                return build_prefix_constant_multiplier(self.w, self.f, coefficient, strategy)
            return build_constant_multiplier(self.w, self.f, coefficient, 0, strategy)

        key, entry = self._new_leaf(node, spec, builder)
        if not existing:
            entry["coefficient_frontier"] = FRONTIER
            metadata_path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
            self._remember_entry(key, entry)
        proof = validate_coefficient_entry(
            self.context.target, node, entry, locations=self.context.locations
        )
        self._record(index, node, key, "coefficient-full-domain", proof)
        return key, entry


def compile_coefficient_graph(target, path, library):
    if canonical(target) != canonical(library.context.target):
        raise ValueError("compiler target differs from the immutable target snapshot")
    return compile_graph(target, path, library)
