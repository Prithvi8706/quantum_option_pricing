"""Sound, deliberately incomplete integer range audit of the financial SSA.

Bounds concern every finite input word, not sampled paths. Correlations are
discarded except for three explicitly checked elementary-function identities.
An unresolved interval overflow is not a demonstrated reachable overflow.
"""

from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from unittest.mock import patch

from research.compound_feasibility.model import MODELS
from research.controlled_source_completion import finance
from research.controlled_source_completion.ir import Graph, evaluate


class WitnessGraph(Graph):
    """Identical graph construction, with proof-only structural annotations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.witnesses = {}

    def interpolate(self, name, x):
        start = len(self.nodes)
        result = super().interpolate(name, x)
        nodes = self.nodes[start:]
        lookup = next(n for n in nodes if n["op"] == "lookup")
        index = lookup["args"][0]
        by_id = {i: n for n in self.nodes for i in n["out"]}
        index_node = by_id[index]
        assert index_node["op"] == "bits"
        step = 1 << index_node["params"]["shift"]
        # The last subtraction before lookup is x_clipped minus its cell center.
        local = [n for n in nodes[: nodes.index(lookup)] if n["op"] == "sub"][-1]
        self.witnesses[local["out"][0]] = ("local", step, name)
        return result

    def log(self, x):
        start = len(self.nodes)
        result = super().log(x)
        shift = next(n for n in self.nodes[start:] if n["op"] == "shift")
        self.witnesses[shift["out"][0]] = ("mantissa",)
        return result

    def exp(self, x):
        start = len(self.nodes)
        result = super().exp(x)
        nodes = self.nodes[start:]
        cs = [n for n in nodes if n["op"] == "cmul"]
        residual = next(n for n in nodes if n["op"] == "sub")
        self.witnesses[residual["out"][0]] = (
            "exp_residual",
            x,
            cs[0]["params"]["c"],
            cs[1]["params"]["c"],
            cs[0]["out"][0],
            cs[1]["out"][0],
        )
        return result


def signed_width(bounds):
    lo, hi = bounds
    return max(1, (max(0, hi)).bit_length() + 1, (max(0, -lo - 1)).bit_length() + 1)


def financial_witnesses(graph, assets):
    """Recognize exact summation identities before adding correlated bounds."""
    nodes = {i: n for n in graph.nodes for i in n["out"]}
    q = 1 << graph.f

    def constant(i, value):
        n = nodes[i]
        return n["op"] == "const" and n["params"]["value"] == value

    def sums(i):
        n = nodes[i]
        if constant(i, 0):
            return []
        if n["op"] != "add":
            raise ValueError("not a constructed summation")
        return sums(n["args"][0]) + [n["args"][1]]

    def cmul(i, coefficient=None):
        n = nodes[i]
        assert n["op"] == "cmul"
        assert coefficient is None or n["params"]["c"] == coefficient
        return n["args"][0], n["params"]["c"]

    def square(i):
        n = nodes[i]
        assert n["op"] == "mul" and n["args"][0] == n["args"][1]
        return n["args"][0]

    def denominator(i):
        n = nodes[i]
        assert n["op"] == "select"
        flag, one, original = n["args"]
        assert constant(one, 1)
        assert nodes[flag]["op"] == "lt" and nodes[flag]["args"] == [original, one]
        return original

    for node in graph.nodes:
        if node["op"] != "divide":
            continue
        a, guard = node["args"]
        try:
            den = denominator(guard)
            ea = square(den)
            basket, rate = cmul(ea)
            assert rate >= q
            total, _ = cmul(basket, q // assets)
            stocks = sums(total)
            assert len(stocks) == assets
            inner, _ = cmul(a, q // (assets * assets))
            assert nodes[inner]["op"] == "add"
            t1, t2 = nodes[inner]["args"]
            sqtotal, common = cmul(t1)
            squared_sum, extra = cmul(t2)
            assert common >= 0 and extra >= 0
            assert sums(square(sqtotal)) == stocks
            assert [square(i) for i in sums(squared_sum)] == stocks
            graph.witnesses[node["out"][0]] = (
                "moment_ratio",
                basket,
                common + extra,
                assets,
                tuple(stocks),
            )
        except (AssertionError, ValueError):
            pass
        try:
            basket = denominator(guard)
            total, _ = cmul(basket, q // assets)
            stocks = sums(total)
            assert len(stocks) == assets
            root = nodes[a]
            assert root["op"] == "sqrt"
            positive = nodes[root["args"][0]]
            assert positive["op"] == "positive"
            difference = nodes[positive["args"][0]]
            while difference["op"] == "positive":
                difference = nodes[difference["args"][0]]
            assert difference["op"] == "sub"
            mean_square, bsquare = difference["args"]
            assert square(bsquare) == basket
            squared_sum, _ = cmul(mean_square, q // assets)
            assert [square(i) for i in sums(squared_sum)] == stocks
            graph.witnesses[node["out"][0]] = ("dispersion", basket, assets, tuple(stocks))
        except (AssertionError, ValueError):
            pass
    assert assets in (4, 8) and q % (assets * assets) == 0
    return graph


class Audit:
    def __init__(self, data, witnesses=None):
        self.data = data
        self.w = data["width"]
        self.f = data["fraction_bits"]
        self.mod = 1 << self.w
        self.half = self.mod // 2
        self.full = (-self.half, self.half - 1)
        self.bounds = {}
        self.nodes = {i: n for n in data["nodes"] for i in n["out"]}
        self.witnesses = witnesses or {}
        self.unresolved = []
        self.wrap_ids = set()
        self.lemmas = Counter()

    def normalize(self, bounds):
        lo, hi = bounds
        first, last = (lo + self.half) // self.mod, (hi + self.half) // self.mod
        if first != last:
            return self.full
        return lo - first * self.mod, hi - first * self.mod

    def raw(self, bounds):
        lo, hi = bounds
        if lo >= 0:
            return lo, hi
        if hi < 0:
            return lo + self.mod, hi + self.mod
        return 0, self.mod - 1

    def fixed(self, lo, hi):
        return lo >> self.f, hi >> self.f

    def run(self):
        for n in self.data["nodes"]:
            op, p = n["op"], n["params"]
            args = n["args"]
            b = [self.bounds[i] for i in args]
            vals = None
            if op == "input":
                vals = [(0, (1 << p["bits"]) - 1)]
            elif op == "const":
                vals = [(p["value"], p["value"])]
            elif op == "add":
                vals = [(b[0][0] + b[1][0], b[0][1] + b[1][1])]
            elif op == "sub":
                vals = [(b[0][0] - b[1][1], b[0][1] - b[1][0])]
            elif op == "mul":
                if args[0] == args[1]:
                    lo = 0 if b[0][0] <= 0 <= b[0][1] else min(x * x for x in b[0])
                    hi = max(x * x for x in b[0])
                else:
                    products = [x * y for x in b[0] for y in b[1]]
                    lo, hi = min(products), max(products)
                vals = [self.fixed(lo, hi)]
            elif op == "cmul":
                products = [x * p["c"] for x in b[0]]
                vals = [self.fixed(min(products), max(products))]
            elif op == "lt":
                vals = [(1, 1) if b[0][1] < b[1][0] else (0, 0) if b[0][0] >= b[1][1] else (0, 1)]
            elif op == "select":
                vals = [
                    b[1]
                    if b[0] == (1, 1)
                    else b[2]
                    if b[0] == (0, 0)
                    else (min(b[1][0], b[2][0]), max(b[1][1], b[2][1]))
                ]
                cond = self.nodes[args[0]]
                if cond["op"] == "lt":
                    ca, cb = cond["args"]
                    if args[1:] == [cb, ca]:
                        vals = [(max(b[1][0], b[2][0]), max(b[1][1], b[2][1]))]
                    elif args[1:] == [ca, cb]:
                        vals = [(min(b[1][0], b[2][0]), min(b[1][1], b[2][1]))]
                    # abs(x) implemented as select(x < 0, 0-x, x).
                    neg = self.nodes[args[1]]
                    if (
                        args[2] == ca
                        and self.bounds[cb] == (0, 0)
                        and neg["op"] == "sub"
                        and neg["args"] == [cb, ca]
                    ):
                        xlo, xhi = self.bounds[ca]
                        vals = [
                            (
                                0 if xlo <= 0 <= xhi else min(abs(xlo), abs(xhi)),
                                max(abs(xlo), abs(xhi)),
                            )
                        ]
            elif op == "positive":
                vals = [(max(0, b[0][0]), max(0, b[0][1]))]
            elif op == "divide":
                a, d = self.raw(b[0]), self.raw(b[1])
                vals = (
                    [((a[0] << self.f) // d[1], (a[1] << self.f) // d[0])]
                    if d[0]
                    else [(0, self.mod - 1)]
                )
            elif op == "sqrt":
                a = self.raw(b[0])
                vals = [(math.isqrt(a[0] << self.f), math.isqrt(a[1] << self.f))]
            elif op == "msb":
                a = self.raw(b[0])
                vals = [(max(0, a[0].bit_length() - 1), max(0, a[1].bit_length() - 1))]
            elif op == "bits":
                a = b[0] if p.get("signed") else self.raw(b[0])
                s = p["shift"]
                a = (a[0] >> s, a[1] >> s) if s >= 0 else (a[0] << -s, a[1] << -s)
                modulus = 1 << p["width"]
                vals = (
                    [(a[0] % modulus, a[1] % modulus)]
                    if a[0] // modulus == a[1] // modulus
                    else [(0, modulus - 1)]
                )
                # A full-width signed right shift preserves its signed interval.
                if p.get("signed") and p["width"] == self.w and s >= 0:
                    vals = [a]
                if p["width"] == self.w and s < 0:
                    # Signed/unsigned left shifts agree modulo 2^w.
                    vals = [(b[0][0] << -s, b[0][1] << -s)]
            elif op == "shift":
                shiftvals = []
                for k in range(max(-self.w, b[1][0]), min(self.w, b[1][1]) + 1):
                    if k >= self.w:
                        shiftvals.extend([0, 0])
                    elif k <= -self.w:
                        shiftvals.extend([-1 if x < 0 else 0 for x in b[0]])
                    else:
                        shiftvals.extend([x << k if k >= 0 else x >> -k for x in b[0]])
                if b[1][0] < -self.w:
                    shiftvals.extend([-1 if x < 0 else 0 for x in b[0]])
                if b[1][1] > self.w:
                    shiftvals.append(0)
                vals = [(min(shiftvals), max(shiftvals))]
            elif op == "lookup":
                rows = self.data["tables"][p["table"]]
                # Index masking is accounted for by using every row if needed.
                a = self.raw(b[0])
                chosen = rows[a[0] : a[1] + 1] if a[1] < len(rows) else rows
                vals = [(min(col), max(col)) for col in zip(*chosen)]
            else:
                raise ValueError(op)
            witness = self.witnesses.get(n["out"][0])
            if witness:
                kind = witness[0]
                if kind == "local":
                    # The constructed clip, cell index and center make this exact.
                    half_step = witness[1] // 2
                    vals = [(-half_step, half_step - 1)]
                    self.lemmas[kind] += 1
                elif kind == "mantissa":
                    vals = [(1 << self.f, (1 << (self.f + 1)) - 1)]
                    self.lemmas[kind] += 1
                elif kind == "exp_residual":
                    _, x, c, ell, cmul1, cmul2 = witness
                    if cmul1 not in self.wrap_ids and cmul2 not in self.wrap_ids:
                        # k=floor(X*c/2^(2f)); r=X-k*ell.
                        denominator = 1 << (2 * self.f)
                        errors = [v * (denominator - c * ell) for v in self.bounds[x]]
                        lower = -((-min(errors)) // denominator)
                        upper = (max(errors) + ell * denominator - 1) // denominator
                        vals = [(lower, upper)]
                        self.lemmas[kind] += 1
                elif kind in ("moment_ratio", "dispersion"):
                    # These identities use sums of nonnegative guarded stocks.
                    # Every premise about the recognized arithmetic preceding
                    # this division must already be range-safe.
                    basket = witness[1]
                    minimum = self.bounds[basket][0]
                    q = 1 << self.f
                    nonnegative = all(self.bounds[s][0] >= 0 for s in witness[-1])
                    if minimum > 0 and minimum * minimum > q and nonnegative and not self.wrap_ids:
                        if kind == "moment_ratio":
                            coefficient = witness[2]
                            upper = coefficient * (minimum + 1) ** 2 // (minimum * minimum - q)
                        else:
                            d = witness[2]
                            numerator = (d - 1) * minimum * minimum + 2 * d * minimum + d + q
                            upper = math.isqrt(q * q * numerator // (minimum * minimum))
                        vals = [(0, upper)]
                        self.lemmas[kind] += 1
            for out, bound in zip(n["out"], vals):
                if bound[0] < -self.half or bound[1] >= self.half:
                    if op not in ("const", "bits"):
                        self.unresolved.append(dict(node=out, op=op, raw_interval=list(bound)))
                        self.wrap_ids.add(out)
                self.bounds[out] = self.normalize(bound)
        return self


def build(model):
    with patch.object(finance, "Graph", WitnessGraph):
        graph = finance.build_finance(model, 40, 32)
    return financial_witnesses(graph, model.assets)


def canonical_values(data):
    """Semantic expression keys under the existing exact optimizer's rules."""
    mask = (1 << data["width"]) - 1
    keys, constants = {}, {}
    for node in data["nodes"]:
        op, args, params = node["op"], node["args"], node["params"]
        folded = None
        if op == "const":
            folded = [params["value"] & mask]
        elif op != "input" and all(a in constants for a in args):
            miniature = [
                dict(op="input", args=[], params=dict(name=str(j), bits=data["width"]), out=[j])
                for j in range(len(args))
            ]
            miniature.append(
                dict(
                    op=op,
                    args=list(range(len(args))),
                    params=params,
                    out=list(range(len(args), len(args) + len(node["out"]))),
                )
            )
            _, trace = evaluate(
                dict(data, nodes=miniature, outputs={}, inputs=list(range(len(args)))),
                {str(j): constants[a] for j, a in enumerate(args)},
                trace=True,
            )
            folded = trace[len(args) :]
        if folded is not None:
            for out, raw in zip(node["out"], folded):
                constants[out] = raw
                keys[out] = "constant:%d" % raw
            continue
        alias = None
        if op == "add":
            if constants.get(args[0]) == 0:
                alias = args[1]
            elif constants.get(args[1]) == 0:
                alias = args[0]
        elif op == "sub" and constants.get(args[1]) == 0:
            alias = args[0]
        elif op == "select" and keys[args[1]] == keys[args[2]]:
            alias = args[1]
        elif op == "cmul" and params["c"] == 1 << data["fraction_bits"]:
            alias = args[0]
        elif op == "bits" and params["shift"] == 0 and params["width"] == data["width"]:
            alias = args[0]
        if alias is not None:
            keys[node["out"][0]] = keys[alias]
            if alias in constants:
                constants[node["out"][0]] = constants[alias]
            continue
        argkeys = [keys[a] for a in args]
        if op in ("add", "mul"):
            argkeys.sort()
        if op == "input":
            params = dict(params, preparation=params.get("preparation", "uniform"))
        expression = [op, argkeys, params]
        key = hashlib.sha256(json.dumps(expression, sort_keys=True).encode()).hexdigest()
        for j, out in enumerate(node["out"]):
            keys[out] = key + ":%d" % j
    return keys


def ranges_for_compiled(data, model):
    """Return rigorous raw signed ranges for an unchanged optimized f40 target.

    Raises on any unmatched expression, table change, or output change. This is
    a range certificate only, not a price approximation certificate. Returned
    range keys are actual compiled-target SSA IDs; no numbering is assumed.
    """
    if data["width"] != 72 or data["fraction_bits"] != 40:
        raise ValueError("This certificate is restricted to f40/q32 finance")
    graph = build(model)
    source = graph.as_dict()
    from research.controlled_source_completion.optimize import optimize

    regenerated = optimize(finance.prune(source, list(data["outputs"])))
    # Old manifests omit the now-explicit default uniform preparation field.
    comparable = json.loads(json.dumps(data))
    for n in comparable["nodes"]:
        if n["op"] == "input":
            n["params"].setdefault("preparation", "uniform")
    if json.dumps(regenerated, sort_keys=True) != json.dumps(comparable, sort_keys=True):
        differing = [
            k
            for k in data
            if json.dumps(data[k], sort_keys=True) != json.dumps(regenerated.get(k), sort_keys=True)
        ]
        raise ValueError("Regenerated optimized target differs: %s" % differing)
    if source["tables"] != data["tables"]:
        # JSON replaces tuples by lists; compare their canonical serialization.
        if json.dumps(source["tables"], sort_keys=True) != json.dumps(
            data["tables"], sort_keys=True
        ):
            raise ValueError("Coefficient tables differ")
    audit = Audit(source, graph.witnesses).run()
    sourcekeys, targetkeys = canonical_values(source), canonical_values(data)
    by_expression = {}
    for ident, key in sourcekeys.items():
        lo, hi = audit.bounds[ident]
        if key in by_expression:
            oldlo, oldhi = by_expression[key]
            lo, hi = max(lo, oldlo), min(hi, oldhi)
            if lo > hi:
                raise AssertionError("Incompatible bounds for an identical expression")
        by_expression[key] = lo, hi
    for name, ident in data["outputs"].items():
        if (
            name not in source["outputs"]
            or targetkeys[ident] != sourcekeys[source["outputs"][name]]
        ):
            missing = [
                (i, n)
                for n in data["nodes"]
                for i in n["out"]
                if targetkeys[i] not in by_expression
            ]
            raise ValueError(
                "Financial output expression differs; first unmatched %s" % missing[:1]
            )
    result = {ident: by_expression[key] for ident, key in targetkeys.items()}
    digest = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    return dict(
        target_sha256=digest,
        bounds=result,
        guaranteed=True,
        signed_overflow_sites=audit.unresolved,
        fraction_bits=40,
        width=72,
        guarantee=(
            "Every reachable signed raw value is enclosed; "
            "constants and repeated expressions are exact."
        ),
    )


def main():
    rows = []
    for model in MODELS:
        graph = build(model)
        data = graph.as_dict()
        audit = Audit(data, graph.witnesses).run()
        muls = [n for n in data["nodes"] if n["op"] == "mul"]
        widths = Counter(max(signed_width(audit.bounds[i]) for i in n["args"]) for n in muls)
        row = dict(
            model=model.name,
            fractional_bits=40,
            random_bits=32,
            source_sha256=hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest(),
            nodes=len(data["nodes"]),
            values=len(audit.bounds),
            structural_lemmas=dict(audit.lemmas),
            unresolved_overflow_sites=audit.unresolved,
            multiplier_max_operand_width_histogram=dict(sorted(widths.items())),
            outputs={k: list(audit.bounds[v]) for k, v in data["outputs"].items()},
            warning=(
                "Integer intervals, not approximation errors; "
                "unresolved means proof inconclusive, not reachable overflow."
            ),
        )
        rows.append(row)
        print(
            json.dumps(
                {
                    k: row[k]
                    for k in (
                        "model",
                        "nodes",
                        "structural_lemmas",
                        "multiplier_max_operand_width_histogram",
                    )
                }
            ),
            flush=True,
        )
        print(
            "unresolved",
            len(audit.unresolved),
            Counter(n["op"] for n in audit.unresolved),
            flush=True,
        )
    path = Path("results/controlled_priority_completion/range_audit.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            dict(
                status="partial rigorous range audit; full arithmetic certificate remains open",
                models=rows,
            ),
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
