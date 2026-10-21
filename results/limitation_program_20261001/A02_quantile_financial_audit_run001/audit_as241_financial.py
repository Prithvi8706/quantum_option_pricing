"""Independent bounded audit of two source-bound native AS241 financial bounds.

No audited helper imports. Source correspondence is rebuilt from saved SSA;
stock polynomials use dense coefficient vectors and iterative integer ranges.
Independent analytic log/exp series and a different pi/CDF enclosure verify
the saved outward bounds. No finance samples, graph construction or gates.
"""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import factorial
from pathlib import Path
import shutil
import sys
import time
import traceback
import xml.etree.ElementTree as ET

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "results/limitation_program_20261001"
SOURCE = PROGRAM / "A02_quantile_financial_run005"
FRONTEND = PROGRAM / "A02_quantile_financial_target_run001"
SCALAR = PROGRAM / "A02_quantile_scalar_run001"
TRANSFORM = PROGRAM / "A02_quantile_transform_run002"
CASES = {"B4x12": (4, 12), "B8x52": (8, 52)}
Q, N, G = 1 << 40, 1 << 32, Fraction(13, 2)
ULP = Fraction(1, Q)
ALLOWANCE = Fraction(11, 2000)
DPS, CPU, WALL = 110, 240, 900
LOG_TERMS, EXP_TERMS, CDF_DEGREE = 200, 160, 176
LAW = "independent q32 midpoint inputs, mathematical-native signed-restored AS241"
PREFLIGHT = ROOT / "research/limitation_program_20261001/as241_financial_audit_preflight.json"


class BudgetCensoredError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, allow_nan=False)
        handle.write("\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return Path(path).resolve().relative_to(ROOT.resolve()).as_posix()


def fingerprint(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    ).hexdigest()


def fraction(value):
    require(isinstance(value, list) and len(value) == 2, "Exact rational receipt pair")
    require(all(type(x) is int for x in value) and value[1] > 0, "Integer rational endpoints")
    result = Fraction(*value)
    require([result.numerator, result.denominator] == value, "Canonical rational pair")
    return result


def pair(value):
    value = Fraction(value)
    return [value.numerator, value.denominator]


def signed(value):
    value %= 1 << 72
    return value - (1 << 72) if value >= 1 << 71 else value


def independent_semantic_words(semantics, assets, dates):
    """Independently decode literal metadata; never decode SSA IDs or flags."""

    def one(raw, name):
        require(
            type(raw) is int and 0 <= raw < 1 << 72,
            "Canonical unsigned72 semantic integer: " + name,
        )
        return raw if raw < 1 << 71 else raw - (1 << 72)

    decoded = {}
    for name in (
        "initial_log_raw",
        "lower_log_raw",
        "upper_log_raw",
        "basket_coefficient_raw",
        "average_coefficient_raw",
        "discount_coefficient_raw",
        "native_exp_inverse_ln2_raw",
        "native_exp_ln2_raw",
    ):
        decoded[name] = one(semantics[name], name)
    for name, expected in (
        ("common_coefficients_raw_by_date", dates),
        ("native_exp_coefficients_raw", 13),
    ):
        vector = semantics[name]
        require(type(vector) is list and len(vector) == expected, "Complete native vector: " + name)
        decoded[name] = [one(raw, name) for raw in vector]
    for name in (
        "idiosyncratic_coefficients_raw_by_date_asset",
        "drift_literals_raw_by_date_asset",
    ):
        matrix = semantics[name]
        require(
            type(matrix) is list and len(matrix) == dates, "Complete native date matrix: " + name
        )
        decoded[name] = []
        for vector in matrix:
            require(
                type(vector) is list and len(vector) == assets,
                "Complete native asset vector: " + name,
            )
            decoded[name].append([one(raw, name) for raw in vector])
    return decoded


def ceiling(a, b):
    quotient, remainder = divmod(a, b)
    return quotient + bool(remainder)


def budget(started):
    if time.process_time() - started[0] > CPU or time.monotonic() - started[1] > WALL:
        raise BudgetCensoredError("Fixed240CPU/900wall audit budget")


def iv(value):
    value = Fraction(value)
    return mp.iv.mpf(value.numerator) / value.denominator


def endpoints(value):
    def one(raw):
        sign, mantissa, exponent, _ = raw
        return Fraction((-1) ** sign * mantissa) * Fraction(2) ** exponent

    return tuple(one(raw) for raw in value._mpi_)


def enclosure(a, b):
    require(a <= b, "Ordered audit interval")
    return mp.iv.mpf([iv(a).a, iv(b).b])


def maximum(value):
    return endpoints(value)[1]


def absolute(value):
    return max(map(abs, endpoints(value)))


def independent_pi():
    # atan(1/2)+atan(1/3)=pi/4; a different identity from producer Machin.
    pieces = []
    for d in (2, 3):
        partial = sum(
            (Fraction((-1) ** j, (2 * j + 1) * d ** (2 * j + 1)) for j in range(240)), Fraction(0)
        )
        pieces.append((partial, partial + Fraction(1, 481 * d**481)))
    return enclosure(4 * sum(p[0] for p in pieces), 4 * sum(p[1] for p in pieces))


def log_point(x):
    """Exact binary reduction and positive atanh series, not mp.iv.ln."""
    x = Fraction(x)
    require(x > 0, "Positive analytic logarithm")
    k = x.numerator.bit_length() - x.denominator.bit_length()
    y = x / Fraction(2) ** k
    if y < 1:
        k -= 1
        y *= 2
    require(1 <= y <= 2, "Deterministic binary logarithm reduction")

    def series(z):
        z = iv(z)
        term, total = z, iv(0)
        for j in range(LOG_TERMS):
            total += term / (2 * j + 1)
            term *= z * z
        tail = Fraction(2, 401) * Fraction(1, 3) ** 401 / Fraction(8, 9)
        return 2 * total + enclosure(0, tail)

    return series((y - 1) / (y + 1)) + k * series(Fraction(1, 3))


def exp_point(x):
    """Positive degree160 sum with geometric tail; reciprocal for negative."""
    x = Fraction(x)
    s = abs(x)
    require(s <= 40, "Fixed independent exponential domain")
    term, total = iv(1), iv(1)
    for k in range(1, EXP_TERMS + 1):
        term = term * iv(s) / k
        total += term
    tail = s ** (EXP_TERMS + 1) / factorial(EXP_TERMS + 1) / (1 - s / Fraction(EXP_TERMS + 2))
    result = total + enclosure(0, tail)
    return 1 / result if x < 0 else result


def endpoint_proof(saved, started):
    budget(started)
    pi = independent_pi()
    z = iv(G)
    term, total = iv(1), iv(1)
    for k in range(1, CDF_DEGREE + 1):
        term *= z * z / (2 * k)
        total += (-1) ** k * term / (2 * k + 1)
    rem = G ** (2 * CDF_DEGREE + 3) / (
        2 ** (CDF_DEGREE + 1) * factorial(CDF_DEGREE + 1) * (2 * CDF_DEGREE + 3)
    )
    cdf = iv(Fraction(1, 2)) - (z * total + enclosure(-rem, rem)) / mp.iv.sqrt(2 * pi)
    a, b = endpoints(cdf)
    recorded = tuple(map(fraction, saved["Phi_minus_6p5_interval_exact"]))
    require(
        recorded[0] <= a <= b <= recorded[1] < Fraction(1, 2 * N),
        "Saved TRUE quantile endpoint encloses independent CDF",
    )
    require(
        fraction(saved["true_quantile_absolute_upper_exact"]) == G
        and saved["symmetry_and_strict_CDF_monotonicity_cover_all_q32_midpoints"] is True
        and saved["approximate_quantile_range_used_as_true_range"] is False,
        "TRUE all-q32 bracket scope",
    )
    return {
        "Phi_minus6p5_independent_interval_exact": [pair(a), pair(b)],
        "independent_integrated_CDF_degree": CDF_DEGREE,
        "independent_pi_identity": "4*(atan1/2+atan1/3)",
        "true_all_midpoint_quantile_bracket_exact": pair(G),
    }


def producer_map(target):
    require((target["width"], target["fraction_bits"]) == (72, 40), "Native72/f40 source")
    source = {}
    for index, node in enumerate(target["nodes"]):
        require(all(v in source for v in node["args"]), "Topological source arguments")
        for slot, value in enumerate(node["out"]):
            require(type(value) is int and value not in source, "Unique actual producer")
            source[value] = (index, node, slot)
    return source


def closure(target, boundaries):
    source, seen, used = producer_map(target), set(), set()
    boundaries = set(boundaries)
    work = list(target["outputs"].values())
    while work:
        value = work.pop()
        if value in boundaries:
            used.add(value)
            continue
        index, node, _ = source[value]
        if index in seen:
            continue
        require(node["op"] != "input", "No free normal in financial closure")
        seen.add(index)
        work.extend(node["args"])
    require(used == set(boundaries), "All date-major normal boundaries used")
    return sorted(seen)


def normalized_hash(target, normals, indices):
    tokens = {v: fingerprint(["normal_boundary", i]) for i, v in enumerate(normals)}
    rows = []
    for index in indices:
        node = target["nodes"][index]
        row = dict(
            op=node["op"],
            args=[tokens[v] for v in node["args"]],
            params=node["params"],
            outputs=len(node["out"]),
        )
        if node["op"] == "lookup":
            row["table_sha256"] = fingerprint(target["tables"][node["params"]["table"]])
        token = fingerprint(row)
        for slot, value in enumerate(node["out"]):
            tokens[value] = fingerprint([token, slot])
        rows.append(row)
    return fingerprint(
        dict(
            width=72,
            fraction_bits=40,
            normal_count=len(normals),
            nodes=rows,
            outputs={k: tokens[v] for k, v in target["outputs"].items()},
        )
    )


def bind_source(case, started):
    """Reconstruct disjoint correspondence and semantic roots without labels."""
    budget(started)
    na, nt = CASES[case]
    target, bundle, ledger = [
        read(FRONTEND / case / name)
        for name in ("target.json", "bundle.json", "new_source_matched_ledger.json")
    ]
    semantic_words = independent_semantic_words(bundle["semantics"], na, nt)
    scalar = read(SCALAR / "scalar_target.json")
    pair_binding = read(PROGRAM / "C06_pair_run001/certificate.json")["source_bindings"][case]
    old = read(ROOT / pair_binding["target"].replace("\\", "/"))
    old_normals = pair_binding["normal_values"]
    require(
        (target["width"], target["fraction_bits"]) == (72, 40)
        and (old["width"], old["fraction_bits"]) == (72, 40)
        and (scalar["width"], scalar["fraction_bits"]) == (72, 40),
        "Explicit actual new/original/scalar native72/f40 precision",
    )
    require(
        set(target["outputs"]) == set(old["outputs"]) == {"Y"}
        and set(scalar["outputs"]) == {"Z"}
        and len(scalar["inputs"]) == 1,
        "Actual one namedY financial / one namedZ scalar interfaces",
    )
    require(
        bundle["schema"] == "as241-financial-target-bundle-v1"
        and (
            bundle["case"],
            bundle["assets"],
            bundle["dates"],
            bundle["width"],
            bundle["fraction_bits"],
            bundle["uniform_bits_each"],
        )
        == (case, na, nt, 72, 40, 32),
        "Actual matched bundle shape/precision/independent uniform contract",
    )
    require(
        target["format"] == old["format"] and target["semantics"] == old["semantics"],
        "Original actual native arithmetic format/semantics",
    )
    require(
        sha(ROOT / pair_binding["target"].replace("\\", "/")) == pair_binding["target_sha256"],
        "Original audited source bytes",
    )
    require(bundle["target_sha256"] == fingerprint(target), "Actual new source hash")
    require(
        bundle["normal_source"]["scalar_target_sha256"] == fingerprint(scalar),
        "Scalar source fingerprint",
    )
    values = sum(len(n["out"]) for n in scalar["nodes"])
    mapping, normals, inputs = {}, [], []
    require(
        len(bundle["normal_source"]["invocations"]) == len(old_normals),
        "Every actual scalar role record",
    )
    for coordinate, old_normal in enumerate(old_normals):
        budget(started)
        offset = coordinate * values
        date, role = divmod(coordinate, na + 1)
        expected_invocation = dict(
            coordinate=coordinate,
            date_index=date,
            role="common" if role == 0 else "idiosyncratic",
            asset_index=None if role == 0 else role - 1,
            input_name="as241_uniform_" + str(coordinate),
            input_value=offset + scalar["inputs"][0],
            output_value=offset + scalar["outputs"]["Z"],
            value_offset=offset,
            scalar_values=values,
        )
        require(
            bundle["normal_source"]["invocations"][coordinate] == expected_invocation,
            "Actual date-major independent scalar role metadata",
        )
        for j, node in enumerate(scalar["nodes"]):
            expected = dict(
                node,
                args=[offset + v for v in node["args"]],
                out=[offset + v for v in node["out"]],
                params=dict(node["params"]),
            )
            if node["op"] == "input":
                expected["params"]["name"] = "as241_uniform_" + str(coordinate)
                inputs.append(expected["out"][0])
                require(
                    expected["params"]["bits"] == 32
                    and expected["params"]["preparation"] == "uniform",
                    "Independent uniform inputs",
                )
            require(
                target["nodes"][coordinate * len(scalar["nodes"]) + j] == expected,
                "Actual complete scalar invocation",
            )
        normal = offset + scalar["outputs"]["Z"]
        mapping[old_normal] = normal
        normals.append(normal)
    require(
        len(normals) == (na + 1) * nt
        and target["inputs"] == inputs
        and bundle["normal_values"] == normals,
        "Independent role count/source boundaries",
    )
    old_indices, new_indices = closure(old, old_normals), closure(target, normals)
    scalar_nodes = len(normals) * len(scalar["nodes"])
    require(
        new_indices == list(range(scalar_nodes, len(target["nodes"])))
        and len(new_indices) == len(old_indices),
        "Exactly appended disjoint financial region",
    )
    for old_index, new_index in zip(old_indices, new_indices, strict=True):
        before, after = old["nodes"][old_index], target["nodes"][new_index]
        require(
            before["op"] == after["op"]
            and before["params"] == after["params"]
            and [mapping[v] for v in before["args"]] == after["args"]
            and len(before["out"]) == len(after["out"]),
            "Verbatim original financial operations/literals",
        )
        mapping.update(zip(before["out"], after["out"], strict=True))
    require(
        mapping
        == {int(k): v for k, v in bundle["financial_normalization"]["original_to_new"].items()},
        "Independently reconstructed original mapping",
    )
    expected_tables = dict(scalar["tables"])
    for i in old_indices:
        old_node = old["nodes"][i]
        if old_node["op"] == "lookup":
            name = old_node["params"]["table"]
            expected_tables[name] = old["tables"][name]
    require(target["tables"] == expected_tables, "Complete actual scalar/financial table inventory")
    ns = bundle["normal_source"]
    require(
        ns["law"] == LAW
        and ns["scalar_receipt"] == relative(SCALAR)
        and ns["scalar_actual_source"] == relative(SCALAR / "candidate64/source.json"),
        "Actual scalar source receipt/law",
    )
    for field, name in (
        ("scalar_target_file_sha256", "scalar_target.json"),
        ("scalar_bindings_file_sha256", "semantic_bindings.json"),
        ("scalar_proofs_file_sha256", "new_site_proofs.json"),
        ("scalar_actual_source_file_sha256", "candidate64/source.json"),
    ):
        require(ns[field] == sha(SCALAR / name), "Actual scalar source/proof byte binding")
    old_hash, new_hash = (
        normalized_hash(old, old_normals, old_indices),
        normalized_hash(target, normals, new_indices),
    )
    require(
        old_hash == new_hash == bundle["financial_normalization"]["normalized_closure_sha256"],
        "Complete normalized financial hashes",
    )
    require(
        bundle["financial_normalization"]["original_boundary_values"] == old_normals,
        "Original ordered pair normal roles",
    )
    source = producer_map(target)

    def node(v, op=None):
        _, n, slot = source[v]
        require(slot == 0 and len(n["out"]) == 1, "Single financial output")
        require(op is None or n["op"] == op, "Actual financial op: " + str(op))
        return n

    def leaves(v):
        n = node(v)
        return leaves(n["args"][0]) + leaves(n["args"][1]) if n["op"] == "add" else [v]

    support = read(PROGRAM / "E03_support_run001" / (case + "_certificate.json"))
    stocks = [[mapping[v] for v in support["stock_ids"][i * nt : (i + 1) * nt]] for i in range(na)]
    clips = [
        [mapping[v] for v in support["clipped_log_ids"][i * nt : (i + 1) * nt]] for i in range(na)
    ]
    require(
        stocks == bundle["semantics"]["stock_values"]
        and clips == bundle["semantics"]["clipped_log_values"],
        "Audited actual stock/clip IDs",
    )
    sites, coeff_a, coeff_b, drifts, raws = [], [], [], [], []
    initial = low = high = None
    for i in range(na):
        raw_row = []
        for j in range(nt):
            budget(started)
            p, k = node(stocks[i][j], "shift")["args"]
            kn = node(k, "bits")
            inv = node(kn["args"][0], "cmul")
            require(
                kn["params"] == dict(shift=40, width=72, signed=True)
                and inv["args"] == [clips[i][j]],
                "Actual native exponent extraction",
            )
            _, middle, h_id = node(clips[i][j], "select")["args"]
            f, l_id, raw = node(middle, "select")["args"]
            require(node(f, "lt")["args"] == [raw, l_id], "Actual lower stock-only clamp")
            upper_flag = node(clips[i][j])["args"][0]
            require(
                node(upper_flag, "lt")["args"] == [middle, h_id], "Actual upper stock-only clamp"
            )
            l_word, h_word = (
                signed(node(l_id, "const")["params"]["value"]),
                signed(node(h_id, "const")["params"]["value"]),
            )
            if low is None:
                low, high = l_word, h_word
            require((low, high) == (l_word, h_word), "All clamp literals identical")
            prefix = leaves(raw)
            multipliers = [node(v) for v in prefix if node(v)["op"] == "cmul"]
            constants = [
                signed(node(v)["params"]["value"]) for v in prefix if node(v)["op"] == "const"
            ]
            require(
                len(constants) + len(multipliers) == len(prefix), "Only raw linear native prefixes"
            )
            actual = {n["args"][0]: n["params"]["c"] for n in multipliers}
            wanted = [normals[t * (na + 1)] for t in range(j + 1)] + [
                normals[t * (na + 1) + i + 1] for t in range(j + 1)
            ]
            require(
                sorted(n["args"][0] for n in multipliers) == sorted(wanted),
                "Original common/idiosyncratic prefix multiset",
            )
            if i == j == 0:
                require(len(constants) == 2, "Initial native spot/drift")
                initial, mu = max(constants), min(constants)
            require(sum(constants) == initial + (j + 1) * mu, "Exact original drift contributions")
            a, b = actual[normals[j * (na + 1)]], actual[normals[j * (na + 1) + i + 1]]
            if i == 0:
                coeff_a.append(a)
                coeff_b.append(b)
                drifts.append(mu)
            require(
                a == coeff_a[j] and b == coeff_b[j] and a > 0 and b > 0,
                "Actual positive increment literals",
            )
            require(
                all(
                    actual[normals[t * (na + 1)]] == coeff_a[t]
                    and actual[normals[t * (na + 1) + i + 1]] == coeff_b[t]
                    for t in range(j + 1)
                ),
                "All accumulated coefficients",
            )
            work, seen, candidates = [p], set(), []
            while work:
                value = work.pop()
                if value in seen:
                    continue
                seen.add(value)
                n = node(value)
                if n["op"] == "sub" and n["args"][0] == clips[i][j]:
                    ln = node(n["args"][1], "cmul")
                    scaled = node(ln["args"][0], "bits")
                    require(
                        scaled["args"] == [k]
                        and scaled["params"] == dict(shift=-40, width=72, signed=False),
                        "Exact scaled exponent interface",
                    )
                    candidates.append((value, ln, scaled))
                    continue
                require(n["op"] in ("const", "mul", "add"), "Actual stock Estrin DAG")
                work.extend(n["args"])
            require(len(candidates) == 1, "One stock range reduction remainder")
            r, ln, scaled = candidates[0]
            sites.append(
                dict(
                    stock=stocks[i][j],
                    clipped=clips[i][j],
                    raw=raw,
                    p=p,
                    k=k,
                    r=r,
                    inverse=inv["out"][0],
                    scaled=scaled["out"][0],
                    ln=ln["out"][0],
                    cinv=inv["params"]["c"],
                    cln=ln["params"]["c"],
                    semantic_exp_coefficients_signed=semantic_words["native_exp_coefficients_raw"],
                )
            )
            raw_row.append(raw)
        raws.append(raw_row)
    require(raws == bundle["semantics"]["raw_log_values"], "Raw logs never fed back from clips")
    require(
        (low, high) == (semantic_words["lower_log_raw"], semantic_words["upper_log_raw"]),
        "Independently decoded signed semantic clamp literals match actual constants",
    )
    require(
        initial == semantic_words["initial_log_raw"]
        and coeff_a == semantic_words["common_coefficients_raw_by_date"]
        and [[value] * na for value in coeff_b]
        == semantic_words["idiosyncratic_coefficients_raw_by_date_asset"]
        and [[value] * na for value in drifts]
        == semantic_words["drift_literals_raw_by_date_asset"],
        "Independently decoded complete initial/common/idiosyncratic/drift literal inventory",
    )
    output = target["outputs"]["Y"]
    alive, payoff, zero = node(output, "select")["args"]
    require(signed(node(zero, "const")["params"]["value"]) == 0, "Dead output zero")
    maximum, h_value = node(alive, "lt")["args"]
    require(signed(node(h_value, "const")["params"]["value"]) == 140 * Q, "Strict barrier140")
    baskets = []
    for j in range(nt):
        wanted = sorted(stocks[i][j] for i in range(na))
        matches = [
            n["out"][0]
            for n in target["nodes"][scalar_nodes:]
            if n["op"] == "cmul"
            and n["params"]["c"] * na == Q
            and sorted(leaves(n["args"][0])) == wanted
        ]
        require(len(matches) == 1, "Actual whole basket at each date")
        baskets.append(matches[0])

    def max_leaves(v):
        if v in baskets:
            return [v]
        flag, right, left = node(v, "select")["args"]
        require(node(flag, "lt")["args"] == [left, right], "Actual all-date maximum")
        return max_leaves(left) + max_leaves(right)

    require(max_leaves(maximum) == baskets, "Every original monitored strict decision")
    cd = node(payoff, "cmul")["params"]["c"]
    pos = node(payoff)["args"][0]
    difference = node(pos, "positive")["args"][0]
    avg, strike = node(difference, "sub")["args"]
    require(signed(node(strike, "const")["params"]["value"]) == 100 * Q, "Exact Asian strike100")
    ca, total = node(avg, "cmul")["params"]["c"], node(avg)["args"][0]
    require(
        semantic_words["basket_coefficient_raw"] == Q // na
        and ca == semantic_words["average_coefficient_raw"]
        and cd == semantic_words["discount_coefficient_raw"],
        "Independent complete basket/Asian/discount literal inventory",
    )
    require(
        all(
            site["cinv"] == semantic_words["native_exp_inverse_ln2_raw"]
            and site["cln"] == semantic_words["native_exp_ln2_raw"]
            for site in sites
        ),
        "Independent complete range-reduction literal inventory",
    )
    require(
        sorted(leaves(total)) == sorted(v for row in stocks for v in row),
        "Every asset/date Asian sum",
    )
    require(len(sites) == na * nt, "All original stock exponentials")
    require(
        ledger == bundle["new_source_matched_ledger"]
        and ledger["source_target_sha256"] == fingerprint(target)
        and ledger["law"] == LAW,
        "New actual source-matched ledger",
    )
    for key, wanted in (
        ("epsilon_dollars_exact", Fraction(1, 100)),
        ("statistical_allowance_dollars_exact", Fraction(9, 2000)),
        ("residual_financial_allowance_dollars_exact", ALLOWANCE),
    ):
        require(fraction(ledger[key]) == wanted, "Original new source accuracy allocation")
    require(
        ledger["source_resources"] is ledger["wrapper_resources"] is None
        and ledger["accepted_joint_Box_Muller_obligation_filled"] is False
        and ledger["old_E02_source_or_wrapper_costs_transferred"] is False,
        "No old source adoption",
    )
    return (
        target,
        source,
        dict(
            case=case,
            na=na,
            nt=nt,
            normals=normals,
            sites=sites,
            initial=initial,
            mu=drifts,
            low=low,
            high=high,
            a=coeff_a,
            b=coeff_b,
            ca=ca,
            cd=cd,
            finance_indices=new_indices,
            target_hash=fingerprint(target),
            normalized_hash=new_hash,
        ),
    )


def original_contract():
    builder = ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
    expected = tuple(map(Fraction, (".3", ".4", "100", ".03", "1", "100", "140")))
    parameter_names = ("SIGMA", "CORR", "S0", "RATE", "T", "K", "H")
    found = []
    for node in ast.parse(builder.read_text(encoding="utf-8")).body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Tuple)
        ):
            names = tuple(n.id for n in node.targets[0].elts if isinstance(n, ast.Name))
            if names == parameter_names:
                found.append(tuple(Fraction(str(x)) for x in ast.literal_eval(node.value)))
    require(found == [expected], "Original economic builder parameters")
    task_names = (
        "annual_volatility_each_asset",
        "equicorrelation",
        "spot_each_asset_dollars",
        "annual_rate",
        "maturity_years",
        "strike_dollars",
        "barrier_dollars",
    )
    for case, (na, nt) in CASES.items():
        task = read(PROGRAM / "G0_run003" / (case + "_task.json"))
        require(
            (task["assets"], task["dates"]) == (na, nt)
            and tuple(Fraction(str(task[k])) for k in task_names) == expected,
            "Original matched economic task",
        )
    return {
        "original_builder_sha256": sha(builder),
        "parameters_exact": dict(zip(parameter_names, map(pair, expected), strict=True)),
    }


def polynomial_layout(target, source, site):
    require((target["width"], target["fraction_bits"]) == (72, 40), "Independent native template")
    seen, work = set(), [site["p"]]
    while work:
        v = work.pop()
        if v == site["r"] or v in seen:
            continue
        seen.add(v)
        _, node, slot = source[v]
        require(
            slot == 0 and node["op"] in ("const", "add", "mul"),
            "Independent stock polynomial layout",
        )
        work.extend(node["args"])
    order = sorted(seen, key=lambda v: source[v][0])
    labels = {site["r"]: "remainder"}
    for value in order:
        _, node, _ = source[value]
        if node["op"] == "const":
            require(
                node["args"] == []
                and set(node["params"]) == {"value"}
                and type(node["params"]["value"]) is int
                and 0 <= node["params"]["value"] < 1 << 72,
                "Independent exact native polynomial constant",
            )
            children = []
        else:
            require(
                len(node["args"]) == 2 and node["params"] == {},
                "Independent exact binary native polynomial add/mul",
            )
            children = sorted(labels[v] for v in node["args"])
        labels[value] = fingerprint([node["op"], node["params"], children])
    return order, labels


def word(bounds):
    require(-(1 << 71) <= bounds[0] <= bounds[1] < 1 << 71, "Independent stored72 overflow")
    return bounds


def product(a, b, square=False):
    values = [x * y for x in a for y in b]
    low, high = min(values), max(values)
    if square:
        low = 0 if a[0] <= 0 <= a[1] else min(x * x for x in a)
        high = max(x * x for x in a)
    require(-(1 << 143) <= low <= high < 1 << 143, "Independent product144 overflow")
    return word((low // Q, high // Q))


def polynomial_cell(source, site, order, raw_range):
    radius = Fraction(max(map(abs, raw_range)), Q)
    integers = {site["r"]: word(raw_range)}
    dense = {site["r"]: ([Fraction(0), Fraction(1)], Fraction(0))}
    step_errors = {}
    for value in order:
        _, node, _ = source[value]
        if node["op"] == "const":
            c = signed(node["params"]["value"])
            integers[value] = word((c, c))
            p, e = [Fraction(c, Q)], Fraction(0)
        else:
            left, right = node["args"]
            a, ea = dense[left]
            b, eb = dense[right]
            ma = sum(abs(c) * radius**j for j, c in enumerate(a))
            mb = sum(abs(c) * radius**j for j, c in enumerate(b))
            if node["op"] == "add":
                p = [Fraction(0)] * max(len(a), len(b))
                for j, c in enumerate(a):
                    p[j] += c
                for j, c in enumerate(b):
                    p[j] += c
                e = ea + eb
                ia, ib = integers[left], integers[right]
                integers[value] = word((ia[0] + ib[0], ia[1] + ib[1]))
            else:
                p = [Fraction(0)] * (len(a) + len(b) - 1)
                for j, ca in enumerate(a):
                    for k, cb in enumerate(b):
                        p[j + k] += ca * cb
                e = (ma + ea) * (mb + eb) - ma * mb + ULP
                require(
                    (ma + ea) * (mb + eb) * Q * Q < 1 << 143,
                    "Independent polynomial magnitude product",
                )
                integers[value] = product(integers[left], integers[right], left == right)
        mag = sum(abs(c) * radius**j for j, c in enumerate(p)) + e
        require(mag * Q < 1 << 71, "Independent symbolic magnitude stored72")
        dense[value] = p, e
        step_errors[value] = (mag, e)
    p, e = dense[site["p"]]
    require(
        len(p) == 13 and all(c > 0 for c in p),
        "Actual dense degree12 positive coefficient polynomial",
    )
    require(
        p == [Fraction(raw, Q) for raw in site["semantic_exp_coefficients_signed"]],
        "Independent actual degree0..12 coefficients match decoded semantic inventory",
    )
    coefficient = sum(abs(c - Fraction(1, factorial(j))) * radius**j for j, c in enumerate(p))
    return integers, radius, e, coefficient, step_errors


def audit_exponential(target, source, scope, saved, started):
    ref = scope["sites"][0]
    order, labels = polynomial_layout(target, source, ref)
    bindings = []
    for site in scope["sites"]:
        budget(started)
        layout, tokens = polynomial_layout(target, source, site)
        require(
            tokens[site["p"]] == labels[ref["p"]]
            and (site["cinv"], site["cln"]) == (ref["cinv"], ref["cln"]),
            "All actual financial stock templates",
        )
        bindings.append((site, layout, tokens))
    require(
        saved["stock_sites"] == len(bindings)
        and saved["actual_template_sha256"] == labels[ref["p"]],
        "Actual464-site template binding",
    )
    cinv, cln, lo, hi = ref["cinv"], ref["cln"], scope["low"], scope["high"]
    require(
        cinv > 0
        and cln > 0
        and lo < hi
        and -17 <= lo * cinv // (Q * Q) <= hi * cinv // (Q * Q) <= 12,
        "Actual native exponent domain contained in unchanged fixed30 classes",
    )
    word((lo * cinv // Q, hi * cinv // Q))
    require(-(1 << 143) <= lo * cinv <= hi * cinv < 1 << 143, "Actual inverse product safety")
    ln_error = absolute(iv(Fraction(cln, Q)) - log_point(2))
    rows = saved["classes"]
    require(
        len(rows) == 30 and [r["k"] for r in rows] == list(range(-17, 13)), "All30 integer classes"
    )
    union, records, alpha, high_stock, previous = {}, [], Fraction(0), None, None
    for k, row in zip(range(-17, 13), rows, strict=True):
        budget(started)
        left, right = max(lo, ceiling(k * Q * Q, cinv)), min(hi, ceiling((k + 1) * Q * Q, cinv) - 1)
        require(
            row["clipped_log_raw_bounds"] == [left, right], "Actual exact integer class endpoints"
        )
        if left > right:
            require(row["empty"] is True, "Empty class explicitly retained")
            continue
        require(
            row["empty"] is False
            and (previous is None and left == lo or previous is not None and left == previous + 1),
            "Gap-free whole-word partition",
        )
        previous = right
        rem = left - k * cln, right - k * cln
        word((k * Q, k * Q))
        word((k * cln, k * cln))
        require(-(1 << 143) <= k * Q * cln < 1 << 143, "Exact exponent scaling product")
        ints, radius, floors, coefficient, steps = polynomial_cell(source, ref, order, rem)
        p = ints[ref["p"]]
        shifted = tuple(v << k for v in p) if k >= 0 else tuple(v >> (-k) for v in p)
        require(p[0] > 0 and word(shifted)[0] > 0, "All stock outputs positive/no shift overflow")
        require(
            row["remainder_raw_bounds"] == list(rem)
            and row["polynomial_raw_bounds"] == list(p)
            and row["stock_raw_bounds"] == list(shifted)
            and fraction(row["radius_exact"]) == radius,
            "Independent integer stock ranges",
        )
        require(
            fraction(row["polynomial_floor_error_upper_exact"]) == floors
            and fraction(row["coefficient_error_upper_exact"]) == coefficient,
            "Dense polynomial floor/coefficient errors",
        )
        saved_steps = {item["value"]: item for item in row["polynomial_floor_and_magnitude_steps"]}
        require(set(saved_steps) == set(steps), "Every actual polynomial step")
        for value, (mag, e) in steps.items():
            require(
                fraction(saved_steps[value]["magnitude_upper_exact"]) == mag
                and fraction(saved_steps[value]["floor_error_upper_exact"]) == e,
                "All actual magnitude/floor recurrences",
            )
        taylor = maximum(exp_point(radius) * iv(radius) ** 13 / factorial(13))
        require(
            fraction(row["degree12_Taylor_remainder_upper_exact"]) >= taylor,
            "Independent Taylor remainder enclosed",
        )
        denominator = endpoints(exp_point(Fraction(rem[0], Q)))[0]
        relative = (floors + coefficient + taylor) / denominator
        require(
            fraction(row["relative_polynomial_error_upper_exact"]) >= relative
            and fraction(row["ln2_literal_error_upper_exact"]) >= ln_error,
            "Conservative relative/ln2 bounds",
        )
        ratio_l = endpoints(iv(1 - relative) * exp_point(-abs(k) * ln_error))[0]
        ratio_h = maximum(iv(1 + relative) * exp_point(abs(k) * ln_error))
        cell_alpha = max(Fraction(0), 1 - ratio_l, ratio_h - 1)
        require(
            fraction(row["relative_stock_error_upper_exact"]) >= cell_alpha,
            "Independent multiplicative stock bound",
        )
        alpha = max(alpha, cell_alpha)
        for value, interval in ints.items():
            before = union.get(value, interval)
            union[value] = min(before[0], interval[0]), max(before[1], interval[1])
        if right == hi:
            point, _, _, _, _ = polynomial_cell(source, ref, order, (hi - k * cln, hi - k * cln))
            high_stock = point[ref["p"]][0] << k if k >= 0 else point[ref["p"]][0] >> (-k)
        records.append(
            dict(
                k=k, independent_alpha_upper_exact=pair(cell_alpha), stock_raw_bounds=list(shifted)
            )
        )
    require(
        previous == hi and saved["whole_clipped_word_domain_covered"] is True,
        "Complete clipped-domain cover",
    )
    require(
        {str(v): list(b) for v, b in union.items()} == saved["polynomial_value_union_bounds"],
        "Independent correlated union ranges",
    )
    require(
        fraction(saved["alpha_upper_exact"])
        == max(fraction(r["relative_stock_error_upper_exact"]) for r in rows if not r["empty"])
        and fraction(saved["alpha_upper_exact"]) >= alpha
        and fraction(saved["alpha_upper_exact"]) < 1
        and fraction(saved["beta_upper_exact"]) == ULP,
        "Uniform alpha/beta reconciliation",
    )
    require(saved["native_exp_upper_clamp_raw"] == high_stock, "Exact native upper-clamp exp word")
    return dict(
        alpha=alpha,
        beta=ULP,
        union=union,
        bindings=bindings,
        reference_labels=labels,
        high_stock=high_stock,
        records=records,
    )


def audit_dead_words(target, source, scope, exp, saved, error, started):
    bound = ceiling((G + error).numerator * Q, (G + error).denominator)
    overrides = {v: (-bound, bound) for v in scope["normals"]}
    ref = scope["sites"][0]
    tokens = exp["reference_labels"]
    token_ranges = {tokens[v]: b for v, b in exp["union"].items() if v != ref["r"]}
    # Derive all six range-reduction aliases directly; do not read producer overrides.
    kinv = scope["low"] * ref["cinv"] // Q, scope["high"] * ref["cinv"] // Q
    rem = exp["union"][ref["r"]]
    stock = (
        min(r["stock_raw_bounds"][0] for r in exp["records"]),
        max(r["stock_raw_bounds"][1] for r in exp["records"]),
    )
    for site, layout, labels in exp["bindings"]:
        for v in layout:
            overrides[v] = token_ranges[labels[v]]
        for key, value in (
            ("stock", stock),
            ("r", rem),
            ("k", (-17, 12)),
            ("inverse", kinv),
            ("scaled", (-17 * Q, 12 * Q)),
            ("ln", (-17 * site["cln"], 12 * site["cln"])),
            ("clipped", (scope["low"], scope["high"])),
        ):
            overrides[site[key]] = value
    computed = dict(overrides)
    actual_financial = []
    for index in scope["finance_indices"]:
        budget(started)
        node = target["nodes"][index]
        v = node["out"][0]
        require(len(node["out"]) == 1, "Actual native financial arity")
        if v not in computed:
            args = [computed[a] for a in node["args"]]
            op = node["op"]
            if op == "const":
                r = (signed(node["params"]["value"]),) * 2
            elif op == "add":
                r = args[0][0] + args[1][0], args[0][1] + args[1][1]
            elif op == "sub":
                r = args[0][0] - args[1][1], args[0][1] - args[1][0]
            elif op == "cmul":
                r = product(args[0], (signed(node["params"]["c"]),) * 2)
            elif op == "mul":
                r = product(args[0], args[1], node["args"][0] == node["args"][1])
            elif op == "lt":
                r = (0, 1)
            elif op == "select":
                r = min(args[1][0], args[2][0]), max(args[1][1], args[2][1])
            elif op == "positive":
                r = max(0, args[0][0]), max(0, args[0][1])
            else:
                raise AssertionError("Uncertified extra financial operation: " + op)
            computed[v] = word(r)
        word(computed[v])
        actual_financial.append(v)
    saved_values = {item["value"]: tuple(item["raw_bounds"]) for item in saved["values"]}
    require(
        len(saved_values) == len(saved["values"]), "No duplicated saved financial interval values"
    )
    require(
        set(saved_values) == set(actual_financial) | set(scope["normals"]),
        "Every saved financial/boundary value and no ghost",
    )
    require(
        all(saved_values[v] == computed[v] for v in saved_values),
        "Independent all-dead-path native intervals",
    )
    require(
        saved["all_dead_path_financial_values"] == len(actual_financial)
        and saved["all_stock_sites_template_bound"] == len(scope["sites"]),
        "Actual financial count reconciliation",
    )
    return dict(
        actual_financial_values=len(actual_financial),
        native_normal_raw_bound=bound,
        signed72_product144_all_dead_paths_safe=True,
        stock_sites=len(scope["sites"]),
    )


def audit_logs(scope, saved, error, started):
    require(
        fraction(saved["same_input_quantile_error_upper_exact"]) == error,
        "Same actual all-input scalar E",
    )
    a = iv(Fraction(3, 10)) * mp.iv.sqrt(iv(Fraction(2, 5 * scope["nt"])))
    b = iv(Fraction(3, 10)) * mp.iv.sqrt(iv(Fraction(3, 5 * scope["nt"])))
    initial = absolute(iv(Fraction(scope["initial"], Q)) - log_point(100))
    require(
        fraction(saved["initial_log_literal_error_upper_exact"]) >= initial,
        "Independent initial log literal",
    )
    running = fraction(saved["initial_log_literal_error_upper_exact"])
    independent = initial
    rows = []
    require(len(saved["dates"]) == scope["nt"], "Every date log bound")
    for j, row in enumerate(saved["dates"]):
        budget(started)
        ahat, bhat = Fraction(scope["a"][j], Q), Fraction(scope["b"][j], Q)
        da, db = absolute(iv(ahat) - a), absolute(iv(bhat) - b)
        dm = abs(Fraction(scope["mu"][j], Q) - Fraction(-3, 200 * scope["nt"]))
        require(
            row["date"] == j + 1
            and row["common_coefficient_raw"] == scope["a"][j]
            and row["idiosyncratic_coefficient_raw"] == scope["b"][j]
            and row["drift_literal_raw"] == scope["mu"][j],
            "Actual per-date literals",
        )
        sa, sb, sm = (
            fraction(row["common_literal_error_upper_exact"]),
            fraction(row["idiosyncratic_literal_error_upper_exact"]),
            fraction(row["drift_literal_error_exact"]),
        )
        require(sa >= da and sb >= db and sm == dm, "True analytic coefficient errors")
        increment = (ahat + bhat) * error + (sa + sb) * G + 2 * ULP + dm
        independent += (ahat + bhat) * error + (da + db) * G + 2 * ULP + dm
        running += increment
        require(
            fraction(row["increment_error_upper_exact"]) == increment
            and fraction(row["raw_log_error_upper_exact"]) == running,
            "Signed floors/exact prefix log accounting",
        )
        rows.append(
            dict(
                date=j + 1,
                independent_raw_log_error_upper_exact=pair(independent),
                saved_raw_log_error_upper_exact=pair(running),
            )
        )
    require(
        saved["signed_constant_multiplication_floors_per_increment"] == 2
        and saved["prefix_addition_rounding_terms"] == 0
        and saved["AS241_KS_E_or_Box_Muller_coupling_added"] is False,
        "No extra or dropped raw-log term",
    )
    return rows


def audit_support(scope, saved):
    m = scope["na"] * scope["nt"]
    ca, cd = scope["ca"], scope["cd"]
    require(0 < ca < Q and 0 < cd <= Q, "Actual positive Asian/discount coefficients")
    total = m * 140 * Q - scope["nt"]
    average = total * ca // Q
    payoff = max(0, average - 100 * Q) * cd // Q
    require(
        saved["strict_alive_stock_sum_raw_upper"] == total
        and saved["surviving_rounded_asian_average_raw_upper"] == average
        and saved["native_payoff_raw_bounds"] == [0, payoff]
        and 0 <= payoff < 40 * Q,
        "Actual rounded Asian support below40",
    )
    return dict(native_payoff_raw_bounds=[0, payoff], actual_upward_Asian_rounding_charged=True)


def audit_bands_and_bias(scope, saved, exponential, logs, smooth, row, started):
    alpha, beta = (
        fraction(exponential["alpha_upper_exact"]),
        fraction(exponential["beta_upper_exact"]),
    )
    ell = fraction(saved["lower_clamp_additive_upper_exact"])
    require(
        ell >= maximum(iv(1 + alpha) * exp_point(Fraction(scope["low"], Q)) + iv(beta))
        and 0 <= ell < 140,
        "Paid deterministic lower clamp",
    )
    require(
        exponential["native_exp_upper_clamp_raw"] >= scope["na"] * 140 * Q,
        "Native high clamp knockout",
    )
    pi = independent_pi()
    switch, mean = Fraction(0), Fraction(0)
    require(len(saved["dates"]) == scope["nt"], "All monitored date bands")
    for j, band in enumerate(saved["dates"], 1):
        budget(started)
        lam = fraction(logs["dates"][j - 1]["raw_log_error_upper_exact"])
        require(
            band["date"] == j
            and fraction(band["raw_log_error_upper_exact"]) == lam
            and fraction(band["lower_clamp_additive_upper_exact"]) == ell,
            "Actual date/log/lower-clamp band binding",
        )
        a, b = fraction(band["a_lower_exact"]), fraction(band["b_upper_exact"])
        require(
            0 < a <= endpoints(iv(1 - alpha) * exp_point(-lam))[0] <= 1
            and b >= maximum(iv(1 + alpha) * exp_point(lam))
            and b >= 1,
            "Saved stock sandwich is conservative",
        )
        high = endpoints(exp_point(Fraction(scope["high"], Q) - lam))[0]
        require(
            fraction(band["ideal_upper_clamp_stock_lower_exact"]) <= high
            and fraction(band["ideal_upper_clamp_stock_lower_exact"]) > scope["na"] * 140,
            "Both ideal/native high-clamp knockout",
        )
        low, up = (140 - ell) / b, (140 + beta + ULP) / a
        require(
            fraction(band["ideal_band_lower_exact"]) == low
            and fraction(band["ideal_band_upper_exact"]) == up,
            "Closed strict/tie band endpoints",
        )
        variance = Fraction(9 * j, 250 * scope["nt"])
        require(
            fraction(band["accumulated_common_variance_exact"]) == variance,
            "Accumulated common variance",
        )
        independent = min(
            Fraction(1), maximum(log_point(up / low) / mp.iv.sqrt(2 * pi * iv(variance)))
        )
        continuous = fraction(band["continuous_unconditional_band_probability_upper_exact"])
        require(
            continuous >= independent and continuous <= 1,
            "Independent common-factor density probability",
        )
        allowance = Fraction((scope["na"] + 1) * j, N)
        grid = min(Fraction(1), continuous + allowance)
        require(
            fraction(band["grid_band_law_allowance_exact"]) == allowance
            and fraction(band["grid_closed_band_probability_upper_exact"]) == grid,
            "Closed-band BV2 finite-grid transfer",
        )
        require(
            band["native_equality_included"] is True
            and band["conditioning_on_survival_or_no_clamp"] is False,
            "No dropped tie or Gaussian conditioning",
        )
        switch += grid
        mean += 140 * max(1 - a, b - 1) + max(beta, ell)
    switch = min(Fraction(1), switch)
    mean /= scope["nt"]
    require(
        fraction(saved["switch_probability_upper_exact"]) == switch
        and saved["AS241_KS_E_added"] is False
        and saved["exact_grid_closed_band_BV_per_coordinate"] == 2,
        "All-date band union and no KS double count",
    )
    m = scope["na"] * scope["nt"]
    rounding = m * 140 * abs(Fraction(scope["ca"], Q) - Fraction(1, m))
    asian = mean + rounding + ULP
    discount = Fraction(scope["cd"], Q)
    error = absolute(iv(discount) - exp_point(Fraction(-3, 100)))
    recorded = fraction(smooth["actual_discount_literal_error_upper_exact"])
    require(recorded >= error, "Independent discount literal error")
    zeta = discount * asian + 40 * recorded + ULP
    for key, value in (
        ("both_alive_mean_stock_error_upper_exact", mean),
        ("actual_Asian_coefficient_error_upper_exact", rounding),
        ("native_Asian_floor_upper_exact", ULP),
        ("Asian_error_upper_exact", asian),
        ("native_discount_floor_upper_exact", ULP),
        ("already_discounted_smooth_error_upper_exact", zeta),
    ):
        require(fraction(smooth[key]) == value, "All smooth Asian/discount terms paid once")
    require(smooth["discount_applied_again"] is False, "No double discount")
    grid_bias = Fraction(40 * (scope["na"] + 1) * scope["nt"], N)
    total = grid_bias + zeta + 40 * switch
    for key, value in (
        ("ideal_continuous_to_exact_grid_bias_upper_exact", grid_bias),
        ("already_discounted_smooth_bias_upper_exact", zeta),
        ("barrier_switch_bias_upper_exact", 40 * switch),
        ("complete_original_contract_bias_upper_exact", total),
    ):
        require(fraction(row[key]) == value, "Exact complete financial bias sum")
    fit = total <= ALLOWANCE
    require(
        row["bias_fits_frozen_residual_financial_allowance"] is fit
        and fraction(row["residual_financial_allowance_dollars_exact"]) == ALLOWANCE,
        "Unchanged residual comparison",
    )
    return dict(
        complete_financial_bias_upper_exact=pair(total),
        bias_fits_frozen_residual_financial_allowance=fit,
        grid_price_bias_exact=pair(grid_bias),
        smooth_bias_exact=pair(zeta),
        switch_bias_exact=pair(40 * switch),
    )


def scalar_error():
    c = read(TRANSFORM / "native_transform_certificate.json")
    fresh = read(TRANSFORM / "fresh_tail_sensitivity.json")
    require(
        c["certified"] is True and c["budget_censored"] is False,
        "Uncensored scalar transform premise",
    )
    require(
        len(fresh["rows"]) == 1024
        and [r["cell_index"] for r in fresh["rows"]] == list(range(1024)),
        "Complete fresh native tail premise",
    )
    totals = []
    for r in fresh["rows"]:
        t = fraction(r["saved_real_approximation_error_upper_exact"]) + fraction(
            r["fresh_native_rational_error_upper_exact"]
        )
        require(
            t == fraction(r["actual_native_tail_quantile_error_upper_exact"])
            and r["previous_conditional_floor_arithmetic_error_added"] is False,
            "Same-input native tail accounting",
        )
        totals.append(t)
    tail, central = max(totals), fraction(c["central_quantile_error_upper_exact"])
    require(
        tail == fraction(c["actual_native_tail_quantile_error_upper_exact"]), "Native tail maximum"
    )
    combined = max(tail, central)
    require(
        combined == fraction(c["combined_mathematical_native_quantile_error_upper_exact"])
        and 0 <= combined <= Fraction(1, 100000000),
        "All-input native scalar maximum",
    )
    return combined


def verify(frozen):
    for path, digest in frozen.items():
        require(isinstance(digest, str) and len(digest) == 64, "Explicit frozen SHA mapping")
        actual = (ROOT / path.replace("\\", "/")).resolve()
        actual.relative_to(ROOT.resolve())
        require(sha(actual) == digest, "Frozen financial audit dependency changed: " + path)


def bind_frozen(frozen, name, digest):
    require(isinstance(name, (str, Path)), "Explicit frozen dependency path")
    require(
        isinstance(digest, str)
        and len(digest) == 64
        and all(char in "0123456789abcdef" for char in digest),
        "Explicit canonical SHA256 expectation",
    )
    path = (ROOT / str(name).replace("\\", "/")).resolve()
    path.relative_to(ROOT.resolve())
    normalized = relative(path)
    require(
        normalized not in frozen or frozen[normalized] == digest,
        "Existing frozen SHA expectation may not be replaced: " + normalized,
    )
    frozen[normalized] = digest


def add_receipt(frozen, directory, financial=False):
    summary = read(directory / "summary.json")
    allowed_rejected = (
        financial
        and summary.get("passed") is False
        and summary.get("reason") == "financial_bias_exceeds_frozen_residual"
        and summary.get("all_two_actual_source_math_bounds_completed") is True
        and summary.get("budget_censored") is False
    )
    require(
        summary.get("passed") is True or allowed_rejected,
        "Complete successful or solely-overbudget financial prerequisite",
    )
    require(summary.get("budget_censored", False) is False, "No censored premise adoption")
    if financial:
        require(
            summary.get("all_two_actual_source_math_bounds_completed") is True,
            "Both full bounds required",
        )
        for case in CASES:
            require(
                (directory / (case + "_certificate.json")).is_file(),
                "Both completed case certificates",
            )
    receipt = read(directory / "manifest.json")
    allowed_fields = {"files", "frozen_inputs", "manifest_self_hash_excluded"}
    if "historical_receipts_unchanged" in receipt:
        require(
            directory.name == "C06_pair_run001"
            and receipt["historical_receipts_unchanged"] is True,
            "Only demonstrated C06_pair historical receipt marker may be true",
        )
        allowed_fields.add("historical_receipts_unchanged")
    require(
        {"files", "frozen_inputs"}.issubset(receipt) and set(receipt).issubset(allowed_fields),
        "Structured prerequisite manifest",
    )
    require(receipt.get("manifest_self_hash_excluded", True) is True, "Exact self-exclusion marker")
    for field in ("files", "frozen_inputs"):
        for name, digest in receipt[field].items():
            bind_frozen(frozen, name, digest)
    bind_frozen(frozen, directory / "manifest.json", sha(directory / "manifest.json"))


def prepare(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if output.exists():
        raise FileExistsError("Fresh prospective financial audit receipt required")
    frozen = {}
    try:
        prepare_body(output, frozen)
    except BaseException as failure:
        if output.exists():
            if not (output / "protocol.json").exists():
                save(
                    output / "protocol.json",
                    dict(
                        local_only=True,
                        frozen_inputs=frozen,
                        terminal_partial_preparation=True,
                        new_test_credit=0,
                    ),
                )
            save(
                output / "preparation_failure.json",
                dict(
                    failure_type=type(failure).__name__,
                    message=str(failure),
                    traceback=traceback.format_exc(),
                    partial_files_preserved=True,
                    fixed_receipt_terminal_no_retry=True,
                ),
            )
            save(
                output / "summary.json",
                dict(
                    passed=False,
                    preparation_failed=True,
                    budget_censored=isinstance(failure, (BudgetCensoredError, TimeoutError)),
                    new_test_credit=0,
                    partial_files_preserved=True,
                    fixed_receipt_terminal_no_retry=True,
                    new_financial_samples_graphs_gates_or_compilation=0,
                    new_financial_sampler_or_estimator_adopted=False,
                ),
            )
            finish(output, {"frozen_inputs": frozen})
        raise


def prepare_body(output, frozen):
    add_receipt(frozen, SOURCE, financial=True)
    for name in (
        "A02_quantile_financial_target_run001",
        "A02_quantile_scalar_run001",
        "A02_quantile_scalar_audit_run001",
        "A02_quantile_transform_run002",
        "A02_quantile_transform_audit_run001",
        "A02_quantile_law_run001",
        "A02_quantile_law_audit_run001",
        "C06_quantile_grid_audit_run001",
        "C06_pair_audit_run001",
        "E03_support_audit_run002",
    ):
        add_receipt(frozen, PROGRAM / name)
    for path in (Path(__file__).resolve(), PREFLIGHT, Path(sys.executable)):
        bind_frozen(frozen, path, sha(path))
    builder = ROOT / "research/advantage_frontier_20260923/barrier_oracle_depth.py"
    bind_frozen(frozen, builder, sha(builder))
    for case in CASES:
        task = PROGRAM / "G0_run003" / (case + "_task.json")
        bind_frozen(frozen, task, sha(task))
    for path in Path(mp.__file__).parent.rglob("*.py"):
        bind_frozen(frozen, path, sha(path))
    verify(frozen)
    output.mkdir()
    shutil.copy2(__file__, output / Path(__file__).name)
    shutil.copy2(PREFLIGHT, output / PREFLIGHT.name)
    for original in (Path(__file__).resolve(), PREFLIGHT):
        require(
            sha(output / original.name) == frozen[relative(original)],
            "Frozen financial audit snapshot differs: " + original.name,
        )
    verify(frozen)
    save(
        output / "protocol.json",
        dict(
            created_utc=datetime.now(timezone.utc).isoformat(),
            local_only=True,
            before_new_audit_bounds=True,
            partial_preparation_failures_are_terminal_and_preserved=True,
            copied_source_bytes_and_frozen_inputs_reverified_before_protocol=True,
            frozen_inputs=frozen,
            cases=list(CASES),
            all_stock_exp_sites=464,
            fixed_exponent_classes=list(range(-17, 13)),
            interval_decimal_digits=DPS,
            dense_polynomial_degree=12,
            independent_log_atanh_terms=LOG_TERMS,
            independent_exp_positive_terms=EXP_TERMS,
            independent_integrated_CDF_degree=CDF_DEGREE,
            independent_pi_identity="atan1/2+atan1/3",
            new_test_credit=0,
            source_receipt=relative(SOURCE),
            producer_unique_fixtures_reconciled_not_recredited=25,
            modular72_semantic_clamps_independently_decoded=True,
            arithmetic_audit_success_distinct_from_financial_bound_budget_fit=True,
            complete_uncensored_solely_overbudget_financial_method_is_auditable=True,
            no_precision_partition_source_retry=True,
            no_finance_samples_graphs_gates_or_compilation=True,
            process_CPU_limit_seconds=CPU,
            elapsed_wall_limit_seconds=WALL,
            python=sys.version,
            executable=sys.executable,
        ),
    )
    verify(frozen)
    print("Independent two-contract financial audit prospectively frozen", flush=True)


def receipt_files(output):
    return {
        relative(p): sha(p)
        for p in sorted(output.rglob("*"))
        if p.is_file() and p.name != "manifest.json"
    }


def finish(output, protocol, checked_files=None):
    if checked_files is None:
        checked_files = receipt_files(output)
    else:
        # The successful path verified dependencies and hashed every existing
        # output BEFORE its terminal budget check; only its new summary remains.
        checked_files[relative(output / "summary.json")] = sha(output / "summary.json")
    save(
        output / "manifest.json",
        dict(
            files=checked_files,
            frozen_inputs=protocol["frozen_inputs"],
            manifest_self_hash_excluded=True,
        ),
    )


def run(output):
    output = Path(output).resolve()
    output.relative_to(PROGRAM.resolve())
    if (output / "summary.json").exists():
        raise FileExistsError("Financial audit already terminal")
    protocol = read(output / "protocol.json")
    started = time.process_time(), time.monotonic()
    cases = []
    try:
        verify(protocol["frozen_inputs"])
        mp.iv.dps = DPS
        xml = list(ET.parse(SOURCE / "tests.xml").getroot().iter("testcase"))
        require(
            len(xml) == len({(x.attrib.get("classname"), x.attrib["name"]) for x in xml}) == 25
            and not any(
                x.find(t) is not None for x in xml for t in ("error", "failure", "skipped")
            ),
            "Exactly25 v5 fixtures including actual clipped-domain regression; zero recredit",
        )
        contract = original_contract()
        save(output / "original_contract_binding.json", contract)
        error = scalar_error()
        endpoint = endpoint_proof(read(SOURCE / "true_midpoint_quantile_bracket.json"), started)
        save(output / "independent_true_quantile_endpoint.json", endpoint)
        all_sites = 0
        for case in CASES:
            target, source, scope = bind_source(case, started)
            row = read(SOURCE / (case + "_certificate.json"))
            bound_source = row["actual_source_binding"]
            require(
                bound_source["actual_new_target_sha256"] == scope["target_hash"]
                and bound_source["normalized_financial_closure_sha256"] == scope["normalized_hash"]
                and bound_source["all_stock_exp_sites"] == len(scope["sites"]),
                "Financial math receipt actual source binding",
            )
            require(
                (
                    bound_source["literal_scope"]["lower_log_raw"],
                    bound_source["literal_scope"]["upper_log_raw"],
                )
                == (scope["low"], scope["high"]),
                "Saved financial scope uses independently verified signed clamp endpoints",
            )
            literal_scope = bound_source["literal_scope"]
            for field, expected in (
                ("initial_log_raw", scope["initial"]),
                ("common_coefficients", scope["a"]),
                ("idiosyncratic_coefficients", scope["b"]),
                ("drift_literals", scope["mu"]),
                ("average_coefficient", scope["ca"]),
                ("discount_coefficient", scope["cd"]),
            ):
                require(
                    literal_scope[field] == expected,
                    "Saved literal scope independently signed/source-bound: " + field,
                )
            require(
                row["new_source_matched_native_financial_bias_certified"] is True
                and fraction(row["same_input_quantile_error_upper_exact"]) == error
                and fraction(row["ideal_true_grid_normal_bound_exact"]) == G,
                "Actual full native financial premise",
            )
            for key in (
                "accepted_joint_Box_Muller_obligation_filled",
                "old_E02_source_or_wrapper_costs_transferred",
                "AS241_KS_E_or_previous_quantile_ULP_added",
                "coherent_financial_source_or_estimator_adopted",
                "quantum_advantage_established",
            ):
                require(row[key] is False, "No scope/resource adoption: " + key)
            require(
                row["actual_new_source_or_wrapper_quantum_cost"]
                is row["physical_runtime_or_error"]
                is None,
                "New quantum/physical costs unknown",
            )
            log_rows = audit_logs(scope, row["raw_log_error_proof"], error, started)
            exp = audit_exponential(target, source, scope, row["stock_exponential_proof"], started)
            words = audit_dead_words(
                target, source, scope, exp, row["all_dead_path_native_safety"], error, started
            )
            support = audit_support(scope, row["native_support_proof"])
            result = audit_bands_and_bias(
                scope,
                row["barrier_band_proof"],
                row["stock_exponential_proof"],
                row["raw_log_error_proof"],
                row["smooth_payoff_proof"],
                row,
                started,
            )
            result.update(
                case=case,
                actual_source_sha256=scope["target_hash"],
                normalized_financial_sha256=scope["normalized_hash"],
                independent_logs=log_rows,
                independent_exp_classes=exp["records"],
                all_dead_path_safety=words,
                native_support=support,
                independent_arithmetic_and_source_audit_passed=True,
                source_sampler_or_estimator_adopted=False,
            )
            save(output / (case + "_audit.json"), result)
            cases.append(result)
            all_sites += len(scope["sites"])
        require(all_sites == 464, "All464 source exponential sites audited")
        producer_summary = read(SOURCE / "summary.json")
        fit = all(c["bias_fits_frozen_residual_financial_allowance"] for c in cases)
        require(
            producer_summary["both_new_native_financial_bias_bounds_fit_residual"] is fit,
            "Summary fit arithmetic",
        )
        require(
            producer_summary["passed"] is fit and producer_summary["budget_censored"] is False,
            "Complete original math PASS versus sole budget rejection",
        )
        require(
            producer_summary["new_unique_fixtures_passed"] == 25
            and producer_summary["previous_fixture_counts_credited_again"] == 0,
            "Original fixture ledger; no audit recredit",
        )
        require(
            producer_summary["new_test_credit"] == (25 if fit else 0),
            "Rejected financial methods receive zero new test credit",
        )
        if not fit:
            require(
                producer_summary["reason"] == "financial_bias_exceeds_frozen_residual",
                "Only declared budget rejection is auditable",
            )
        require(
            [c["case"] for c in producer_summary["cases"]] == list(CASES),
            "Both original summary case rows",
        )
        for c in producer_summary["cases"]:
            certificate = read(SOURCE / (c["case"] + "_certificate.json"))
            require(
                all(c[key] == certificate[key] for key in c),
                "Every saved summary cost/error claim matches full certificate",
            )
        verify(protocol["frozen_inputs"])
        checked_files = receipt_files(output)
        budget(started)
        save(
            output / "summary.json",
            dict(
                passed=True,
                budget_censored=False,
                new_test_credit=0,
                original_unique_fixtures_reconciled_not_recredited=25,
                independent_financial_source_and_arithmetic_audit_passed=True,
                all_stock_exp_sites_audited=all_sites,
                cases=cases,
                both_saved_bounds_fit_frozen_residual=fit,
                original_method_rejected_solely_for_financial_budget=not fit,
                new_financial_sampler_source_or_estimator_adopted=False,
                old_joint_Box_Muller_obligation_filled=False,
                old_E02_costs_transferred=False,
                new_source_cost_or_physical_time=None,
                quantum_advantage_established=False,
                new_financial_samples_graphs_gates_or_compilation=0,
                process_CPU_seconds=time.process_time() - started[0],
                wall_seconds=time.monotonic() - started[1],
            ),
        )
    except BaseException as exc:
        save(
            output / "failure.json",
            dict(
                failure_type=type(exc).__name__,
                message=str(exc),
                traceback=traceback.format_exc(),
                budget_censored=isinstance(exc, (BudgetCensoredError, TimeoutError)),
                new_test_credit=0,
                partial_files_preserved=True,
            ),
        )
        save(
            output / "summary.json",
            dict(
                passed=False,
                budget_censored=isinstance(exc, (BudgetCensoredError, TimeoutError)),
                terminal_failure=traceback.format_exc(),
                completed_cases=cases,
                new_test_credit=0,
                new_financial_samples_graphs_gates_or_compilation=0,
                new_financial_sampler_or_estimator_adopted=False,
                process_CPU_seconds=time.process_time() - started[0],
                wall_seconds=time.monotonic() - started[1],
            ),
        )
        finish(output, protocol)
        raise
    finish(output, protocol, checked_files)
    print(
        "Independent native financial arithmetic audit retained; budget fit reported separately",
        flush=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run"))
    parser.add_argument(
        "--output", type=Path, default=PROGRAM / "A02_quantile_financial_audit_run001"
    )
    args = parser.parse_args()
    (prepare if args.mode == "prepare" else run)(args.output)
