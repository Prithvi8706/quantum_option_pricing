"""Independent direct-leaf reconciliation of the combined estimator cost artifact."""

from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path


ROOT = Path("results/controlled_priority_completion")


def read(path):
    return json.loads(path.read_text())


def main():
    paths = [ROOT / "combined_cost.json", ROOT / "combined_replay.json",
             ROOT / "estimator_hadamard.json", ROOT / "estimator_bounded.json",
             Path("results/controlled_completion_followup/synthesis_rotations.json")]
    combined, replay, hadamard, bounded, synthesis = [read(path) for path in paths]
    original = {(r["model"], r.get("mode", "unconditional_digital_support")): r
                for r in hadamard + bounded}
    phase = read(ROOT / "parallel_v1/phase_f64_limit_all.json")
    selector = read(ROOT / "estimator_bounded_selector.json")["resources"]
    epsilon = Fraction(*synthesis["common_operator_epsilon_exact"])
    reviewed = []
    for row in combined["rows"]:
        model, method = row["model"], row["method"]
        source = read(ROOT / "range_parallel_v1" / (model + "_f40_limit_all.json"))
        manifest = read(ROOT / "range_compile_v1" / (model + "_f40/source.json"))
        r = source["resources"]
        # Independently reconstruct source depth from emitted independent waves.
        depth = 2 * sum(group["t_depth"] for group in source["groups"])
        assert depth == r["t_depth"]
        assert r["t_count"] == manifest["resources"]["t_count"]
        prior = original[model, row["mode"]]
        a = prior["allocation"]
        random = sum(n["params"]["bits"] for n in manifest["inputs"])
        qpe_t, qpe_depth, usage = 0, 0, Counter()
        if method == "hadamard":
            calls = sum(s["T"] * s["repetitions"] for s in a["stages"])
            phase_depth = 2 * sum(group["t_depth"] for group in phase["groups"])
            unit_t = r["t_count"] + phase["resources"]["t_count"] + 14 * (random - 1)
            unit_depth = depth + phase_depth + 12 * (random - 1)
            qubits = r["logical_qubits"] + phase["resources"]["logical_qubits"] + random
            for bit in range(67):
                value = Fraction(2**bit, 2**65)
                key = "radian_%d_%d" % (value.numerator, value.denominator)
                target = synthesis["rotations"][key]["target"]
                assert target["kind"] == "radian"
                assert Fraction(target["numerator"], target["denominator"]) == value
                usage[key] += 3 * calls
            assert sum(usage.values()) == prior["additional_single_qubit_rotations"]
        else:
            random += 48
            bits, repetitions = a["qpe_bits"], a["repetitions"]
            calls = repetitions * (2**bits - 1)
            unit_t = r["t_count"] + 2 * selector["t_count"] + 14 * (random - 1)
            unit_depth = depth + 2 * selector["t_depth"] + 12 * (random - 1)
            qubits = r["logical_qubits"] + selector["qubits"] + random + bits
            # Enumerate actual IQFT wire pairs, not the aggregate gap formula.
            for control in range(bits):
                for target_wire in range(control):
                    gap = control - target_wire
                    if gap == 1:
                        qpe_t += 3 * repetitions
                        qpe_depth += 2 * repetitions
                    else:
                        key = "pi_1_%d" % 2 ** (gap + 1)
                        target = synthesis["rotations"][key]["target"]
                        assert target == dict(kind="pi", numerator=1, denominator=2 ** (gap + 1))
                        usage[key] += 3 * repetitions
            assert sum(usage.values()) == prior["arbitrary_single_qubit_IQFT_rotations"]
        assert calls == row["controlled_iterations"]
        assert unit_depth == row["single_iterate_arithmetic_T_depth"]
        # Hadamard preserves one redundant workspace bit from its old envelope;
        # this is a harmless explicit upper allocation, not an undercount.
        allocation_slack = row["logical_qubits_upper"] - qubits
        assert allocation_slack == (1 if method == "hadamard" else 0)
        assert usage == row["synthesis_usage"]
        synthesized_t = sum(synthesis["rotations"][key]["matrix_product_gates"].count("T") * n
                            for key, n in usage.items())
        arithmetic_t = calls * unit_t + qpe_t
        combined_depth = calls * unit_depth + qpe_depth + synthesized_t
        assert arithmetic_t == row["arithmetic_T_count"]
        assert synthesized_t == row["synthesized_rotation_T_count"]
        assert arithmetic_t + synthesized_t == row["complete_logical_T_count"]
        assert combined_depth == row["wave_plus_serial_rotations_T_depth"]
        assert 2 * sum(usage.values()) * epsilon <= Fraction(5, 10000)
        reviewed.append(dict(model=model, method=method, mode=row["mode"],
                             logical_T=arithmetic_t + synthesized_t,
                             scheduled_T_depth=combined_depth,
                             logical_qubits_upper=row["logical_qubits_upper"],
                             unused_allocation_slack=allocation_slack))
    assert {r["model"] for r in replay} == {"C4", "H8"}
    for row in replay:
        assert row["phase_cleanup"]
        assert [r["marked"] for r in row["selector"]] == [True, False]
        assert all(r["cleanup"] for r in row["selector"])
    output = dict(status="Combined counts and archived composed basis checks reconcile.",
                  review_scope="The author of this review did not author combined_cost or replay.",
                  input_sha256={p.as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in paths}, rows=reviewed)
    (ROOT / "capacity_integration_review.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
