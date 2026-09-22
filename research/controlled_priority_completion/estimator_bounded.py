"""Unconditional digital-output QAE using an exact shifted uniform selector.

The implemented source has |Y| < 100, so (Y + 128)/256 is a probability.
Its binary fixed-point value is encoded by a comparator with a fresh uniform
selector.  The source, comparator and their inverse are charged in every
Grover iterate.  No variance certificate or atan source is needed.
"""

from fractions import Fraction
import argparse
import hashlib
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np

from research.antithetic_feasibility.estimator import schedule
from research.antithetic_feasibility.reversible import clifford_t_resources
from research.controlled_priority_completion.estimator_hadamard import exact_tail
from research.controlled_source_completion.compiler import (
    apply_graph_half,
    mapped_gates,
    reflection_cost,
)
from research.controlled_source_completion.ir import evaluate
from research.journal_sprint.reversible_fixed_point import Program, constant, copy, less_than


ROOT = Path("results/controlled_priority_completion")
COMPILED = Path("results/controlled_completion_followup/arithmetic_v1")


def shifted_selector(word_width=72, fraction_bits=40, shift=128):
    """Compute flag=[u<Y+shift] with every scratch register restored to zero.

    Since shift=2**k and |Y|<shift, the low f+k+1 bits of the signed source
    plus shift are obtained by flipping their highest bit.  Higher sign bits
    are irrelevant within the declared source bound.
    """
    if shift <= 0 or shift & (shift - 1):
        raise ValueError("shift must be a positive power of two")
    n = fraction_bits + shift.bit_length()
    if n > word_width:
        raise ValueError("source word must contain the shifted value")
    p = Program(compact=True)
    value = p.register(word_width)
    selector = p.register(n)
    flag = p.register(1)[0]
    shifted = p.register(n)
    diff, extended, helper = p.register(n + 1), p.register(n + 1), p.register(1)[0]
    copy(p, value[:n], shifted)
    constant(p, shifted, shift << fraction_bits)
    less_than(p, selector, shifted, flag, diff, extended, helper)
    constant(p, shifted, shift << fraction_bits)
    copy(p, value[:n], shifted)
    return p, (value, selector), (flag,)


def bounded_schedule(error, failure=0.003, span=256):
    """Explicit QAE error and confidence certificate for a probability."""
    mp.iv.dps = 80
    M = 1
    target = mp.iv.mpf(Fraction(error).numerator) / Fraction(error).denominator
    # sqrt(p(1-p)) <= 1/2 for all probabilities, including this source.
    while not ((mp.iv.pi / M + mp.iv.pi**2 / M**2) * span <= target):
        M *= 2
    bad_interval = 1 - 8 / mp.iv.pi**2
    den = 1 << 40
    p_bad = Fraction(math.ceil((1 - 8 / math.pi**2) * den) + 1, den)
    assert (mp.iv.mpf(p_bad.numerator) / p_bad.denominator > bad_interval) is True
    r = 1
    while exact_tail(r, p_bad, lower=r // 2 + 1) > Fraction(failure):
        r += 2
    return dict(
        error=error,
        ideal_test_failure=failure,
        span=span,
        M=M,
        qpe_bits=M.bit_length() - 1,
        repetitions=r,
        certified_ideal_failure=float(exact_tail(r, p_bad, lower=r // 2 + 1)),
        elementary_failure_upper_exact=[p_bad.numerator, p_bad.denominator],
        controlled_grover_calls=r * (M - 1),
        ideal_error_upper=span * (math.pi / M + math.pi**2 / M**2),
        bound_certification=(
            "80-digit interval arithmetic for pi/error; exact rational binomial tail"
        ),
    )


def emitted_wrapper(source, manifest_path, selector, ins, outs):
    """Bind every financial/selector/reflection wire in a hierarchical iterate."""
    w = source["word_width"]
    offset = source["resources"]["logical_qubits"]
    y_offset = source["outputs"]["Y_6"] * w
    mapping = [y_offset + j if j < w else offset + j - w for j in range(selector.qubits)]
    random = [
        node["out"][0] * w + j for node in source["inputs"] for j in range(node["params"]["bits"])
    ]
    random += [mapping[j] for j in ins[1]]
    scratch = offset + selector.qubits - w
    source_forward = dict(
        gate="call_graph_half",
        manifest=str(manifest_path).replace("\\", "/"),
        base=0,
        inverse=False,
    )
    source_inverse = dict(source_forward, inverse=True)
    selector_ops = [
        dict(gate=("x", "cx", "ccx")[len(gate) - 1], wires=[mapping[j] for j in gate])
        for gate in selector.gates
    ]
    ops = (
        [source_forward]
        + selector_ops
        + [dict(gate="cz", wires=["control", mapping[outs[0]]])]
        + list(reversed(selector_ops))
        + [source_inverse]
    )
    ops += [dict(gate="h", wires=[j]) for j in random] + [dict(gate="x", wires=[j]) for j in random]
    ladder = [dict(gate="ccx", wires=[random[0], random[1], scratch])]
    ladder += [
        dict(gate="ccx", wires=[scratch + j - 2, random[j], scratch + j - 1])
        for j in range(2, len(random))
    ]
    ops += (
        ladder
        + [dict(gate="cz", wires=[scratch + len(random) - 2, "control"])]
        + list(reversed(ladder))
    )
    ops += (
        [dict(gate="x", wires=[j]) for j in random]
        + [dict(gate="h", wires=[j]) for j in random]
        + [dict(gate="z", wires=["control"])]
    )
    return dict(
        format="controlled-bounded-mean-grover-v1",
        operations=ops,
        random_wires=random,
        control_semantics="Replace control with active QPE qubit; all other addresses explicit.",
        qpe_register_base=scratch + len(random) - 1,
        selector_wire_mapping=mapping,
        source_manifest_sha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    )


def replay_predicate(name, source, selector, ins, outs, wrapper):
    """Execute complete emitted F/predicate/inverses on an active basis input.

    This verifies the diagonal marking oracle, not a full QPE statevector.
    """
    old_cases = json.loads(
        Path(
            "results/controlled_source_completion/validation_v2/full_source_basis.json"
        ).read_text()
    )
    inputs = next(
        row["inputs"] for row in old_cases if row["model"] == name and row["fraction_bits"] == 40
    )
    target = json.loads((COMPILED / "compile_v2" / (name + "_f40") / "target.json").read_text())
    expected, trace = evaluate(target, inputs, True)
    y_raw = trace[target["outputs"]["Y_6"]]
    if y_raw >= 1 << (source["word_width"] - 1):
        y_raw -= 1 << source["word_width"]
    mapping = np.array(wrapper["selector_wire_mapping"], dtype=np.int64)
    gates = np.frombuffer(selector.gates.data, dtype=np.int32).reshape(-1, 4)
    cache = {}
    rows = []
    for selector_value in (y_raw + (128 << 40) - 1, y_raw + (128 << 40)):
        state = np.zeros(wrapper["qpe_register_base"], np.uint8)
        for node in source["inputs"]:
            raw = inputs[node["params"]["name"]]
            offset = node["out"][0] * source["word_width"]
            for j in range(source["word_width"]):
                state[offset + j] = (raw >> j) & 1
        for j, wire in enumerate(ins[1]):
            state[mapping[wire]] = (selector_value >> j) & 1
        before = state.copy()
        apply_graph_half(source, state, cache=cache)
        mapped_gates(gates, state, mapping, False)
        actual = bool(state[mapping[outs[0]]])
        wanted = selector_value < y_raw + (128 << 40)
        assert actual == wanted
        mapped_gates(gates, state, mapping, True)
        apply_graph_half(source, state, inverse=True, cache=cache)
        assert np.array_equal(state, before)
        rows.append(
            dict(
                selector_value=selector_value,
                predicate=actual,
                controlled_phase_if_control_one=(-1 if actual else 1),
                all_inputs_preserved_and_workspace_clean=True,
            )
        )
    return dict(
        model=name,
        source_Y=expected["Y_6"],
        rows=rows,
        status=(
            "Complete emitted financial and selector gates/inverses executed; "
            "reflection/QPE not statevector simulated."
        ),
    )


def main(replay=False):
    ROOT.mkdir(parents=True, exist_ok=True)
    selector, ins, outs = shifted_selector()
    selector_resources = clifford_t_resources(selector)
    gate_data = bytes(selector.gates.data)
    selector_record = dict(
        description="Clean shifted-uniform comparator for p=(Y+128)/256",
        word_width=72,
        fraction_bits=40,
        source_contract="|Y| < 100; exact f40 signed fixed-point output",
        inputs=ins,
        outputs=outs,
        resources=selector_resources,
        gate_bytes_sha256=hashlib.sha256(gate_data).hexdigest(),
        emitted_gate_records=[list(selector.gates[i]) for i in range(len(selector.gates))],
    )
    (ROOT / "estimator_bounded_selector.json").write_text(
        json.dumps(selector_record, indent=2) + "\n"
    )
    old_rows = json.loads((COMPILED / "cost_v3_phase64/ledger.json").read_text())
    rows = []
    for name in ("C4", "H8"):
        manifest_path = COMPILED / "compile_v2" / (name + "_f40") / "source.json"
        source = json.loads(manifest_path.read_text())
        wrapper = emitted_wrapper(source, manifest_path, selector, ins, outs)
        (ROOT / ("estimator_bounded_" + name + "_wrapper.json")).write_text(
            json.dumps(wrapper, indent=2) + "\n"
        )
        if replay:
            record = replay_predicate(name, source, selector, ins, outs, wrapper)
            (ROOT / ("estimator_bounded_" + name + "_replay.json")).write_text(
                json.dumps(record, indent=2) + "\n"
            )
        old = next(
            row
            for row in old_rows
            if row["model"] == name and row["f"] == 40 and row["mode"] == "digital_support_bound"
        )
        discount = math.exp(-0.03 * (0.5 if name == "C4" else 1.5))
        allocation = bounded_schedule(0.002 / discount)
        calls = allocation["controlled_grover_calls"]
        resources = source["resources"]
        n_random = resources["random_hadamards"] + len(ins[1])
        # Same exact clean-AND controlled reflection as the existing envelope.
        reflection_ccx = 2 * (n_random - 1)
        reflection = reflection_cost(n_random)
        unit_t = resources["t_count"] + 2 * selector_resources["t_count"] + 7 * reflection_ccx
        # Disjoint selector copies/compute do not overlap with source passes in
        # this valid conservative schedule. Source cleanup's output CX does not
        # change T depth and is omitted from the fused recipe.
        unit_depth = resources["t_depth"] + 2 * selector_resources["t_depth"] + 6 * reflection_ccx
        qft_exact_cp = allocation["repetitions"] * (allocation["qpe_bits"] - 1)
        qft_cp = (
            allocation["repetitions"] * allocation["qpe_bits"] * (allocation["qpe_bits"] - 1) // 2
        )
        rotations = 3 * (qft_cp - qft_exact_cp)
        depth = calls * unit_depth + 2 * qft_exact_cp
        alternative = schedule(old["moment"], 0.002 / discount, 0.003, max_magnitude=100.0)
        row = dict(
            model=name,
            allocation=allocation,
            compiled_selector_resource=selector_resources,
            single_iterate_T_count=unit_t,
            single_iterate_T_depth=unit_depth,
            single_iterate_clifford_CX=resources["clifford_cx"]
            - source["word_width"]
            + 2 * selector_resources["cx"]
            + reflection["clifford_cx"]
            + 1,
            single_iterate_clifford_H=resources["clifford_h"]
            + 2 * selector_resources["h"]
            + reflection["clifford_h"]
            + 2,
            single_iterate_X=resources["x"] + 2 * selector_resources["x"] + reflection["x"],
            single_iterate_Z=1,
            arithmetic_T_count=calls * unit_t + 3 * qft_exact_cp,
            serial_arithmetic_T_depth=depth,
            logical_qubits_upper=resources["logical_qubits"]
            + selector_resources["qubits"]
            + n_random
            - 1
            + allocation["qpe_bits"]
            + 1,
            random_uniform_preparation_H=allocation["repetitions"] * n_random,
            qpe_preparation_and_IQFT_H=2 * allocation["repetitions"] * allocation["qpe_bits"],
            arbitrary_single_qubit_IQFT_rotations=rotations,
            IQFT_controlled_phase_gates=qft_cp,
            IQFT_controlled_phase_decomposition_CX=2 * qft_cp,
            IQFT_swap_CX=3 * allocation["repetitions"] * (allocation["qpe_bits"] // 2),
            measured_QPE_bits=allocation["repetitions"] * allocation["qpe_bits"],
            random_input_reset_bits=allocation["repetitions"] * n_random,
            required_each_rotation_error=0.0005 / (2 * rotations),
            source_and_inverse_passes=2 * calls,
            selector_and_inverse_calls=2 * calls,
            longest_single_chain_arithmetic_T_depth=(allocation["M"] - 1) * unit_depth,
            old_support_complex_phase_calls=old["ledger"]["controlled_U_calls"],
            same_support_signed_bin_QAE_calls=alternative["grover_iterates"],
            optimistic_serial_seconds_at_1ns_T_layer=depth * 1e-9,
            optimistic_serial_seconds_at_100ns_T_layer=depth * 1e-7,
            tenfold_total_budget_seconds=old["tenfold_total_budget_seconds"],
            required_T_layer_seconds_for_10x=old["tenfold_total_budget_seconds"] / depth,
            full_financial_certificate_complete=False,
            physical_runtime_seconds=None,
            gate_passes=False,
            iterate_recipe=[
                "Apply emitted financial graph F forward retaining SSA values",
                "Bind source SSA Y to clean shifted-selector input and execute selector",
                "CZ(external QPE control, predicate flag)",
                "Execute selector inverse and financial F inverse",
                "Apply signed controlled reflection around uniform random+selector state",
            ],
            obligation=(
                "This estimates the implemented digital Y mean only. Full financial "
                "arithmetic/policy/regret/surrogate and physical runtime obligations remain; "
                "arithmetic-only serial schedule is not a hardware prediction or lower bound."
            ),
        )
        rows.append(row)
        print(
            json.dumps(
                {
                    key: row[key]
                    for key in (
                        "model",
                        "optimistic_serial_seconds_at_1ns_T_layer",
                        "required_T_layer_seconds_for_10x",
                    )
                }
            ),
            flush=True,
        )
    (ROOT / "estimator_bounded.json").write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    main(parser.parse_args().replay)
