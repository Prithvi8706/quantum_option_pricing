"""Stdlib independent formula audit, not circuit execution or a bias certificate."""

import argparse
import json
import math
from pathlib import Path


def close(a, b):
    if (isinstance(a, bool) or not isinstance(a, (int, float)) or not math.isfinite(a)
            or not math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-10)):
        raise ValueError(f"independent formula mismatch: {a} != {b}")


def cdf(x):
    return math.erfc(-x / math.sqrt(2)) / 2


def audit(path):
    plan = json.loads((path / "planned.json").read_text())["config"]
    max_error = 0.0
    summaries = []
    for index, case in enumerate(plan["cases"]):
        record = json.loads((path / f"case_{index}.json").read_text())
        if record["case"] != case:
            raise ValueError("case mismatch")
        if [r["representation"] for r in record["rows"]] != ["raw", "residual"]:
            raise ValueError("representation inventory mismatch")
        assets, dates, q = case
        dim, levels, cutoff = assets * dates, 2**q, plan["cutoff"]
        basket = record["basket"]
        sigma, maturity, rate, strike = (basket[k] for k in ("sigma", "maturity", "rate", "strike"))
        discount = math.exp(-rate * maturity)
        means, factor = record["means"], record["factor"]
        if len(means) != dim or len(factor) != dim or any(len(row) != dim for row in factor):
            raise ValueError("model dimensions mismatch")
        covariance = [[sigma**2 * min((i % dates + 1) * maturity / dates,
                                     (j % dates + 1) * maturity / dates)
                       * (1 if i // dates == j // dates else basket["correlation"])
                       for j in range(dim)] for i in range(dim)]
        for i in range(dim):
            close(means[i], math.log(basket["spot"])
                  + (rate - sigma**2 / 2) * (i % dates + 1) * maturity / dates)
            for j in range(dim):
                close(math.fsum(factor[i][k] * factor[j][k] for k in range(dim)), covariance[i][j])
        mass = cdf(cutoff) - cdf(-cutoff)
        marginal = [(cdf(-cutoff + (j + 1) * 2 * cutoff / levels)
                     - cdf(-cutoff + j * 2 * cutoff / levels)) / mass for j in range(levels)]
        weights, raw, controls = [], [], []
        if any(len(record[name]) != levels**dim
               for name in ("normals", "weights", "raw", "control")):
            raise ValueError("table length mismatch")
        for j in range(levels**dim):
            digits = [(j // levels**k) % levels for k in range(dim)]
            normals = [-cutoff + (digit + .5) * 2 * cutoff / levels for digit in digits]
            if len(record["normals"][j]) != dim:
                raise ValueError("normal coordinate count mismatch")
            for a, b in zip(record["normals"][j], normals):
                close(a, b)
            weight = math.prod(marginal[digit] for digit in digits)
            logs = [means[i] + math.fsum(factor[i][k] * normals[k] for k in range(dim))
                    for i in range(dim)]
            value = discount * max(math.fsum(math.exp(x) for x in logs) / dim - strike, 0)
            control = discount * max(math.exp(math.fsum(logs) / dim) - strike, 0)
            close(record["weights"][j], weight)
            close(record["raw"][j], value)
            close(record["control"][j], control)
            weights.append(weight)
            raw.append(value)
            controls.append(control)
        mu_g = math.fsum(means) / dim
        var_g = math.fsum(x for row in covariance for x in row) / dim**2
        d2 = (mu_g - math.log(strike)) / math.sqrt(var_g)
        analytic_control = discount * (math.exp(mu_g + var_g / 2) * cdf(d2 + math.sqrt(var_g))
                                       - strike * cdf(d2))
        raw_mean = math.fsum(w * x for w, x in zip(weights, raw))
        control_mean = math.fsum(w * x for w, x in zip(weights, controls))
        expected_spots = [math.exp(means[i] + covariance[i][i] / 2) for i in range(dim)]
        tail = discount / dim * math.fsum(expected_spots[i] * math.fsum(
            cdf(-cutoff - x) + cdf(-cutoff + x) for x in factor[i]) for i in range(dim))
        tail += (1 - mass**dim) / mass**dim * discount * math.fsum(expected_spots) / dim
        raw_lip = discount / dim * math.fsum(
            math.exp(means[i] + cutoff * math.fsum(abs(x) for x in factor[i]))
            * math.fsum(abs(x) for x in factor[i]) for i in range(dim))
        geom_l1 = math.fsum(abs(math.fsum(factor[i][j] for i in range(dim)) / dim)
                            for j in range(dim))
        geom_lip = discount * math.exp(mu_g + cutoff * geom_l1) * geom_l1
        for row in record["rows"]:
            if [c["loader"] for c in row["circuits"]] != ["product", "dense"]:
                raise ValueError("loader inventory mismatch")
            residual = row["representation"] == "residual"
            values = [a - g for a, g in zip(raw, controls)] if residual else raw
            mean = math.fsum(w * x for w, x in zip(weights, values))
            scale = max(values)
            close(row["expectation"], mean)
            close(row["finite_price"], raw_mean)
            close(row["finite_control"], control_mean)
            close(row["application_approximation"], mean + (analytic_control if residual else 0))
            close(row["application_minus_finite"], analytic_control-control_mean if residual else 0)
            close(row["contract"]["offset"], analytic_control if residual else 0)
            close(row["contract"]["sensitivity"], scale)
            close(row["variance"], math.fsum(w * (x - mean)**2 for w, x in zip(weights, values)))
            close(row["analytic_bounds"]["tail_and_renormalization"], tail)
            close(row["analytic_bounds"]["discretization"],
                  (raw_lip + (geom_lip if residual else 0)) * cutoff / levels)
            if row["readiness"] != "unknown_bias":
                raise ValueError("unexpected application promotion")
            for circuit in row["circuits"]:
                close(circuit["probability"], mean / scale)
                close(circuit["expected_probability"], mean / scale)
                if circuit["shots"] != 0 or circuit["quantum_device_seconds"] is not None:
                    raise ValueError("unexpected hardware/shot claim")
                if (circuit["acquisition"]["cx"]
                        != circuit["loading"]["cx"] + circuit["payoff"]["cx"]):
                    raise ValueError("CX composition mismatch")
                for diagnostic in ("max_joint_probability_error", "inverse_return_error",
                                   "state_fidelity_error"):
                    error = circuit[diagnostic]
                    if (isinstance(error, bool) or not isinstance(error, (int, float))
                            or not math.isfinite(error) or not 0 <= error <= 1e-10):
                        raise ValueError("failed circuit diagnostic")
                max_error = max(max_error, circuit["max_joint_probability_error"])
        reference = record["classical_reference"]
        if len(reference["replicates"]) != plan["scrambles"]:
            raise ValueError("replicate count mismatch")
        if reference["shared_path_evaluations"] != plan["scrambles"] * 2**plan["rqmc_power"]:
            raise ValueError("reference evaluation count mismatch")
        for name in ("raw", "residual"):
            values = [r[name] for r in reference["replicates"]]
            mean = math.fsum(values) / len(values)
            se = math.sqrt(math.fsum((x - mean)**2 for x in values) / (len(values)-1) / len(values))
            close(reference["summaries"][name]["mean"], mean)
            close(reference["summaries"][name]["standard_error"], se)
        summaries.append(dict(case=case, finite_price=raw_mean, analytic_control=analytic_control))
    return dict(audited_cases=len(summaries), independent_stdlib_formulas=True,
                max_recorded_joint_error=max_error, summaries=summaries, certified=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.archive), indent=2))
