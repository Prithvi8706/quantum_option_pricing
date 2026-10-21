"""Conservative exact integer intervals for a validated fixed-point SSA graph.

Refinements recognize normalization and bin-local residuals in the same graph.
Bounds describe the digital function, not its error against continuous finance.
Overflow or an unknown operation falls back to the full signed word interval.
"""

import math

from research.limitation_program_20261001.prove_log_exponent import SSAContext


def bound_graph(target):
    context = SSAContext(target)
    data = context.target
    width, fraction = data["width"], data["fraction_bits"]
    mask, sign = (1 << width) - 1, 1 << (width - 1)
    full = (-sign, sign - 1)
    bounds, rules = {}, {}

    def signed(raw):
        raw &= mask
        return raw - (1 << width) if raw & sign else raw

    def safe(pair):
        low, high = pair
        return pair if -sign <= low <= high < sign else full

    def unsigned(pair):
        low, high = pair
        if high < 0:
            return low + (1 << width), high + (1 << width)
        if low >= 0:
            return pair
        return 0, mask

    def raw_result(pair):
        low, high = pair
        if high < sign:
            return pair
        if sign <= low <= high <= mask:
            return low - (1 << width), high - (1 << width)
        return full

    def node(value, op, arity):
        producer = context.producers[value]
        return producer if producer["op"] == op and len(producer["args"]) == arity else None

    def literal(value):
        producer = node(value, "const", 0)
        return signed(producer["params"]["value"]) if producer else None

    def normalization(current):
        value, shift = current["args"]
        if bounds[value][0] < 1 or fraction + 1 >= width:
            return None
        negative = node(shift, "sub", 2)
        if not negative or literal(negative["args"][0]) != 0:
            return None
        exponent = node(negative["args"][1], "sub", 2)
        if not exponent or literal(exponent["args"][1]) != fraction:
            return None
        top = node(exponent["args"][0], "msb", 1)
        if not top or top["args"] != [value]:
            return None
        return 1 << fraction, (1 << (fraction + 1)) - 1

    def local_bin(current):
        value, centered = current["args"]
        center = node(centered, "add", 2)
        if not center:
            return None
        offset = literal(center["args"][1])
        shifted = node(center["args"][0], "bits", 1)
        if offset is None or not shifted:
            return None
        parameters = shifted["params"]
        shift = parameters.get("shift")
        if type(shift) is not int or shift >= 0:
            return None
        if parameters.get("width") != width or parameters.get("signed", False):
            return None
        index = node(shifted["args"][0], "bits", 1)
        if not index:
            return None
        ip = index["params"]
        bits = ip.get("width")
        if ip.get("shift") != -shift or type(bits) is not int or not 1 <= bits <= width:
            return None
        if ip.get("signed", False):
            return None
        relative = node(index["args"][0], "sub", 2)
        if not relative or relative["args"][0] != value:
            return None
        origin = literal(relative["args"][1])
        if origin is None:
            return None
        step = 1 << -shift
        low, high = bounds[value]
        if offset - origin != step // 2 or not origin <= low <= high < origin + (1 << bits) * step:
            return None
        # The preceding subtraction/left-shift/add must themselves avoid wrap.
        intermediates = (relative["out"][0], shifted["out"][0], centered)
        if any(bounds[v] == full for v in intermediates):
            return None
        return -(step // 2), step - step // 2 - 1

    for current in data["nodes"]:
        op, params = current["op"], current["params"]
        arguments = [bounds[v] for v in current["args"]]
        result, rule = [full] * len(current["out"]), "full-word fallback"
        if op == "input":
            bits = params["bits"]
            if type(bits) is not int or not 0 <= bits <= width:
                raise ValueError("invalid declared input width")
            if params.get("preparation", "uniform") == "uniform" and bits < width:
                result, rule = [(0, (1 << bits) - 1)], "uniform input domain"
        elif op == "const":
            value = signed(params["value"])
            result, rule = [(value, value)], "literal word"
        elif op in ("add", "sub", "mul"):
            (a, b), (c, d) = arguments
            if op == "add":
                pair = a + c, b + d
            elif op == "sub":
                pair = a - d, b - c
            else:
                products = (a * c, a * d, b * c, b * d)
                pair = min(products) >> fraction, max(products) >> fraction
            result, rule = [safe(pair)], "signed endpoints with overflow fallback"
            if op == "sub":
                refined = local_bin(current)
                if refined is not None:
                    result, rule = [refined], "same-SSA bin-local residual"
        elif op == "cmul":
            coefficient = params["c"]
            values = [endpoint * coefficient >> fraction for endpoint in arguments[0]]
            result, rule = [safe((min(values), max(values)))], "constant signed floor"
        elif op == "lt":
            (a, b), (c, d) = arguments
            pair = (1, 1) if b < c else (0, 0) if a >= d else (0, 1)
            result, rule = [raw_result(pair)], "signed comparison"
        elif op == "select":
            flag, left, right = arguments
            pair = (
                left
                if flag == (1, 1)
                else right
                if flag == (0, 0)
                else (min(left[0], right[0]), max(left[1], right[1]))
            )
            compare = node(current["args"][0], "lt", 2)
            if compare:
                x, y = compare["args"]
                xbounds, ybounds = bounds[x], bounds[y]
                if current["args"][1:] == [y, x]:
                    pair = tuple(max(a, b) for a, b in zip(xbounds, ybounds))
                elif current["args"][1:] == [x, y]:
                    pair = tuple(min(a, b) for a, b in zip(xbounds, ybounds))
            result, rule = [pair], "branch union or same-SSA min/max"
        elif op == "positive":
            result = [tuple(max(0, value) for value in arguments[0])]
            rule = "positive part"
        elif op == "msb":
            lo, hi = unsigned(arguments[0])
            result = [(max(0, lo.bit_length() - 1), max(0, hi.bit_length() - 1))]
            rule = "unsigned MSB"
        elif op == "bits":
            shift, bits = params["shift"], params["width"]
            lo, hi = arguments[0] if params.get("signed") else unsigned(arguments[0])
            lo, hi = (lo >> shift, hi >> shift) if shift >= 0 else (lo << -shift, hi << -shift)
            if bits == width:
                # Full-width left shifting acts identically on signed/raw words.
                if shift < 0:
                    lo, hi = (value << -shift for value in arguments[0])
                pair = safe((lo, hi))
            elif 0 <= lo <= hi < 1 << bits:
                pair = raw_result((lo, hi))
            else:
                pair = raw_result((0, (1 << bits) - 1))
            result, rule = [pair], "bit extraction with modulo fallback"
        elif op == "shift":
            refined = normalization(current)
            if refined is not None:
                result, rule = [refined], "same-SSA MSB normalization"
            else:
                (lo, hi), (first, last) = arguments
                pairs = []
                for shift in range(
                    max(-width, min(width, first)), max(-width, min(width, last)) + 1
                ):
                    if shift >= width:
                        pair = (0, 0)
                    elif shift <= -width:
                        pair = (-1 if lo < 0 else 0, -1 if hi < 0 else 0)
                    else:
                        pair = (
                            safe((lo << shift, hi << shift))
                            if shift >= 0
                            else (lo >> -shift, hi >> -shift)
                        )
                    pairs.append(pair)
                result = [(min(p[0] for p in pairs), max(p[1] for p in pairs))]
                rule = "shift endpoints with overflow fallback"
        elif op == "sqrt":
            lo, hi = unsigned(arguments[0])
            result = [raw_result((math.isqrt(lo << fraction), math.isqrt(hi << fraction)))]
            rule = "exact unsigned integer square root"
        elif op == "lookup":
            rows = data["tables"][params["table"]]
            result = [
                (min(signed(row[j]) for row in rows), max(signed(row[j]) for row in rows))
                for j in range(len(current["out"]))
            ]
            rule = "all literal coefficient rows"
        elif op == "divide" and arguments[0][0] >= 0 and arguments[1][0] > 0:
            (a, b), (c, d) = arguments
            result = [safe(((a << fraction) // d, (b << fraction) // c))]
            rule = "unsigned positive quotient endpoints"
        for value, pair in zip(current["out"], result):
            if not -sign <= pair[0] <= pair[1] < sign:
                raise AssertionError("invalid signed interval")
            bounds[value], rules[value] = pair, rule
    return bounds, rules
