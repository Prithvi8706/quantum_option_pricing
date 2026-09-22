"""Bit-exact signed fixed multiplication without unobserved high product bits.

For unsigned words A,B and sign bits a,b, signed(A)*signed(B) equals
A*B - a*B*2**w - b*A*2**w modulo 2**(w+f).  The omitted cross term
a*b*2**(2*w) vanishes for 0 <= f <= w.  Copy bits f:f+w, then undo.
This changes the emitted implementation, never the digital financial law.
"""

import hashlib
import json
import shutil

import numpy as np

from research.journal_sprint.reversible_fixed_point import (
    Program,
    add,
    copy,
    subtract,
)
from research.controlled_source_completion.primitives import (
    Library,
    array_gates,
    resources,
)


def build_multiplier(w, f):
    if type(w) is not int or w < 1 or type(f) is not int or not 0 <= f <= w:
        raise ValueError("integer width >= 1 and 0 <= fraction <= width required")
    p = Program(compact=True)
    a, b, out = (p.register(w) for _ in range(3))
    n = w + f
    product, partial = p.register(n), p.register(n)
    helper = p.register(1)[0]
    start = len(p.gates)
    for i in range(w):
        first = len(p.gates)
        for j in range(min(w, n - i)):
            p.gate(a[j], b[i], partial[j])
        last = len(p.gates)
        add(p, partial[: n - i], product[i:], helper)
        p.undo(first, last)
    if f:
        for sign, operand in ((a[-1], b), (b[-1], a)):
            first = len(p.gates)
            for j in range(f):
                p.gate(sign, operand[j], partial[j])
            last = len(p.gates)
            subtract(p, partial[:f], product[w:], helper)
            p.undo(first, last)
    last = len(p.gates)
    copy(p, product[f : f + w], out)
    p.undo(start, last)
    return p, [a, b], [out]


class TruncatedLibrary(Library):
    """Reuse immutable prior leaves; emit and hash the new multiplier."""

    def __init__(self, path, w, f, tables, base_path):
        super().__init__(path, w, f, tables)
        self.base = Library(base_path, w, f, tables)

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
        spec = dict(op="mul", width=self.w, fraction_bits=self.f, backend="truncated-signed-v1")
        key = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:20]
        if key not in self.entries:
            meta, binary = self.path / (key + ".json"), self.path / (key + ".npy")
            if meta.exists() and binary.exists():
                entry = json.loads(meta.read_text())
                if hashlib.sha256(binary.read_bytes()).hexdigest() != entry["sha256"]:
                    raise ValueError("Cached multiplier hash mismatch")
            else:
                p, args, outs = build_multiplier(self.w, self.f)
                np.save(binary, array_gates(p))
                entry = dict(
                    key=key,
                    op="mul",
                    params={},
                    backend=spec["backend"],
                    args=[list(a) for a in args],
                    outs=[list(o) for o in outs],
                    resources=resources(p),
                    gate_file=binary.name,
                    sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),
                    table_bits=0,
                )
                meta.write_text(json.dumps(entry, indent=2) + "\n")
            self.entries[key] = entry
        return key, self.entries[key]
