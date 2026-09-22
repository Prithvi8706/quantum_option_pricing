"""Clean fixed multiply specialized to independently certified operand ranges."""

import hashlib
import json
import shutil

import numpy as np

from research.journal_sprint.reversible_fixed_point import Program, add, subtract
from research.controlled_source_completion.primitives import Library, array_gates, resources


def build(w, f, a_width, b_width):
    if not (1 <= a_width <= w and 1 <= b_width <= w and 0 <= f <= w):
        raise ValueError("invalid widths")
    p = Program(compact=True)
    a, b, out = (p.register(w) for _ in range(3))
    n = min(w + f, a_width + b_width)
    product, partial = p.register(n), p.register(n)
    helper = p.register(1)[0]
    start = len(p.gates)
    for i in range(min(b_width, n)):
        first = len(p.gates)
        for j in range(min(a_width, n - i)):
            p.gate(a[j], b[i], partial[j])
        last = len(p.gates)
        add(p, partial[: n - i], product[i:], helper)
        p.undo(first, last)
    # Product modulo 2^n; the double-sign term is divisible by 2^n.
    for sign, operand, offset in ((a[a_width - 1], b, a_width), (b[b_width - 1], a, b_width)):
        count = n - offset
        if count <= 0:
            continue
        first = len(p.gates)
        for j in range(count):
            p.gate(sign, operand[j], partial[j])
        last = len(p.gates)
        subtract(p, partial[:count], product[offset:], helper)
        p.undo(first, last)
    last = len(p.gates)
    for j, target in enumerate(out):
        # If all product bits were retained, extend its sign before slicing.
        p.gate(product[min(f + j, n - 1)], target)
    p.undo(start, last)
    return p, [a, b], [out]


class RangedLibrary(Library):
    def __init__(self, path, w, f, tables, base_path, bounds):
        super().__init__(path, w, f, tables)
        self.base = Library(base_path, w, f, tables)
        self.bounds = bounds

    def get(self, node):
        if node["op"] != "mul":
            self.base.tables.update(self.tables)
            key, entry = self.base.get(node)
            if key not in self.entries:
                for suffix in (".json", ".npy"):
                    target = self.path / (key + suffix)
                    if not target.exists():
                        shutil.copy2(self.base.path / (key + suffix), target)
                self.entries[key] = entry
            return key, entry
        from research.controlled_priority_completion.range_audit import signed_width

        widths = [signed_width(self.bounds[i]) for i in node["args"]]
        spec = dict(
            op="mul",
            width=self.w,
            fraction_bits=self.f,
            operand_signed_widths=widths,
            backend="certified-range-mul-v1",
        )
        key = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:20]
        if key not in self.entries:
            meta, binary = self.path / (key + ".json"), self.path / (key + ".npy")
            if meta.exists() and binary.exists():
                entry = json.loads(meta.read_text())
                if hashlib.sha256(binary.read_bytes()).hexdigest() != entry["sha256"]:
                    raise ValueError("Cached leaf hash mismatch")
            else:
                p, args, outs = build(self.w, self.f, *widths)
                np.save(binary, array_gates(p))
                entry = dict(
                    key=key,
                    op="mul",
                    params={},
                    spec=spec,
                    args=[list(a) for a in args],
                    outs=[list(o) for o in outs],
                    resources=resources(p),
                    gate_file=binary.name,
                    sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
                    table_bits=0,
                    validity="Only on the certified signed operand intervals; "
                    "the gate program remains reversible outside that domain.",
                )
                meta.write_text(json.dumps(entry, indent=2) + "\n")
            self.entries[key] = entry
        return key, self.entries[key]
