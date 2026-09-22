"""Optimistic fixed-workload capacity screens, not universal no-go results.

These screens use work conservation, not the previous serial upper schedule.
Every assumption is serialized, including deliberately unrealistically cheap
primitive operations. No clock or noise coordinate is a hardware prediction.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results/controlled_completion_followup/arithmetic_v1"
DEFAULT_LEDGER = BASE / "cost_v3_phase64/ledger.json"
DEFAULT_OUTPUT = ROOT / "results/controlled_priority_completion/capacity_screen.json"
PHYSICAL_CAP = 10_000_000
CLOCKS = (1e-9, 1e-8, 1e-7, 1e-6)
NOISES = (1e-3, 1e-4, 1e-5, 1e-6)
STRICT_C4_SECONDS = 267.8373668


def capacity_bound(work, physical_qubits, physical_qubits_per_lane, seconds_per_op):
    """A necessary elapsed time for a specified uniform-lane primitive.

    Assume at most floor(P/a) operations can run simultaneously, each occupying
    its lane for at least tau. Integrating occupancy gives time >= N*tau/lanes.
    This grants free setup, routing, data storage, Clifford gates and factories.
    """
    if work < 0 or physical_qubits < 1 or physical_qubits_per_lane < 1:
        raise ValueError("Work must be nonnegative and capacities positive")
    if seconds_per_op <= 0:
        raise ValueError("Primitive duration must be positive")
    lanes = physical_qubits // physical_qubits_per_lane
    if lanes == 0:
        return None
    return work * seconds_per_op / lanes


def patch_qubits(distance):
    """Rotated surface-code data and syndrome qubits, without routing."""
    if distance < 1 or distance % 2 == 0:
        raise ValueError("Distance must be a positive odd integer")
    return 2 * distance * distance - 1


def logical_error_fit(physical_error, distance):
    """Approximate model coordinate; not a rigorously bounded device error."""
    if not 0 < physical_error < 0.01:
        raise ValueError("Physical error outside this model's stated domain")
    return 0.1 * (100 * physical_error) ** ((distance + 1) // 2)


def certificate_distance(logical_qubits, budget_seconds, cycle_seconds, physical_error):
    """First odd distance satisfying the adopted exposure test at the deadline.

    This is a sufficient-distance calculation conditional on the noise fit.
    Failure of the union-bound test at a smaller distance is NOT proof that the
    true failure probability exceeds the allowance.
    """
    exposure = logical_qubits * math.ceil(budget_seconds / cycle_seconds)
    for distance in range(1, 201, 2):
        bound = exposure * logical_error_fit(physical_error, distance)
        if bound <= 0.001:
            return dict(
                distance=distance,
                data_patch_rounds=exposure,
                modeled_data_fault_union_bound=bound,
                physical_data_qubits=logical_qubits * patch_qubits(distance),
                fits_data_cap=logical_qubits * patch_qubits(distance) <= PHYSICAL_CAP,
            )
    raise ValueError("Distance search exhausted")


def distillation_certificate(work, raw_error):
    """Levels sufficient using the archived all-orders independent-Z bound."""
    error = raw_error
    levels = 0
    while work * error > 0.0005:
        error = math.comb(15, 3) * error**3 / (1 - error) ** 15
        levels += 1
        if levels > 8:
            raise ValueError("Certificate did not converge")
    return dict(
        levels_sufficient_under_bound=levels,
        accepted_error_bound=error,
        total_accepted_error_union_bound=work * error,
    )


def magic_supply_bound(work, physical_cap, distance, cycle_seconds):
    """Chosen 15-to-1 family: ideal top-stage spacetime capacity only.

    Assume each output consumes at least 11 tiles for 11*d rounds, weaker than
    the 15*d top-level construction for already-distilled inputs. This is a
    screen of that specified family, not of all distillation or native-T codes.
    All available physical qubits are generously granted to top-level factories;
    data, lower levels, rejected attempts, buffering and routing are omitted.
    Also grant up to physical_cap perfect pre-stored states without charging
    their space against the factories. This intentionally double-grants space.
    """
    online = max(0, work - physical_cap)
    space_time = 11 * patch_qubits(distance) * 11 * distance
    return online * space_time * cycle_seconds / physical_cap


def contract_records(row):
    records = [dict(
        name="empirical_rqmc",
        classical_seconds=row["classical_full_price_seconds"],
        contract="Archived strong controlled RQMC; empirical uncertainty",
    )]
    if row["model"] == "C4":
        records.append(dict(
            name="fixed_iid",
            classical_seconds=STRICT_C4_SECONDS,
            contract="Archived fixed-iid acquisition plus training; ideal-premise guarantee",
        ))
    return records


def one_row(row):
    source_path = BASE / "compile_v2" / f"{row['model']}_f40" / "source.json"
    source = json.loads(source_path.read_text())["resources"]
    ledger = row["ledger"]
    actual_t = ledger["arithmetic_t_count"]
    actual_ccx = row["single_U"]["ccx"] * ledger["controlled_U_calls"]
    assert actual_t == 7 * actual_ccx
    ideal_calls = row["ideal_unit_constant_source_calls"]
    workloads = {
        "actual_arithmetic_T": actual_t,
        "actual_native_CCX_sensitivity": actual_ccx,
        "ideal_unit_constant_clean_source_T": ideal_calls * source["t_count"],
        "ideal_unit_constant_clean_source_CCX": ideal_calls * source["ccx"],
    }
    records = []
    for contract in contract_records(row):
        budget = min(contract["classical_seconds"] / 10, 60.0)
        workload_records = {}
        for name, work in workloads.items():
            workload_records[name] = dict(
                operations=work,
                largest_per_lane_seconds_to_fit_with_one_physical_qubit_per_lane=(
                    budget * PHYSICAL_CAP / work
                ),
                required_operations_per_physical_qubit_per_second=work / budget / PHYSICAL_CAP,
                sensitivity=[dict(
                    primitive_seconds=clock,
                    physical_qubits_per_lane=space,
                    minimum_work_seconds=capacity_bound(work, PHYSICAL_CAP, space, clock),
                    passes_necessary_work_screen=(
                        capacity_bound(work, PHYSICAL_CAP, space, clock) <= budget
                    ),
                ) for clock in CLOCKS for space in (1, 3, 17, 49, 97, 449)],
            )
        records.append(dict(
            **contract,
            tenfold_budget_seconds=budget,
            workload_screens=workload_records,
            surface_code_deadline_sensitivity=[dict(
                physical_error=p,
                cycle_seconds=clock,
                **certificate_distance(row["single_U"]["logical_qubits"], budget, clock, p),
            ) for p in NOISES for clock in CLOCKS],
        ))
    return dict(
        model=row["model"],
        mode=row["mode"],
        fraction_bits=40,
        source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
        emitted_logical_qubits=row["single_U"]["logical_qubits"],
        minimum_distance_three_patch_qubits=row["single_U"]["logical_qubits"] * patch_qubits(3),
        actual_controlled_U_calls=ledger["controlled_U_calls"],
        ideal_unit_constant_source_calls=ideal_calls,
        contract_screens=records,
        magic_state_quality_sensitivity=[dict(
            raw_error=p,
            **distillation_certificate(actual_t, p),
        ) for p in NOISES],
        optimistic_15_to_1_top_stage_supply=[dict(
            distance=distance,
            cycle_seconds=clock,
            minimum_seconds_for_actual_arithmetic_T=magic_supply_bound(
                actual_t, PHYSICAL_CAP, distance, clock
            ),
            minimum_seconds_for_ideal_source_T=magic_supply_bound(
                workloads["ideal_unit_constant_clean_source_T"], PHYSICAL_CAP, distance, clock
            ),
        ) for distance in (3, 5, 7, 15, 25, 35) for clock in CLOCKS],
    )


def generate(ledger_path=DEFAULT_LEDGER):
    rows = json.loads(ledger_path.read_text())
    return dict(
        schema="controlled-compound-optimistic-capacity-v1",
        generated_date="2026-09-22",
        ledger=str(ledger_path.relative_to(ROOT)).replace("\\", "/"),
        ledger_sha256=hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        physical_qubit_cap=PHYSICAL_CAP,
        interpretation={
            "actual_work": "Fixed emitted arithmetic only; missing operations increase it",
            "ideal_work": (
                "Hypothetical constant-one sample schedule, not an algorithm or lower bound"
            ),
            "native_ccx": "Sensitivity that replaces every seven-T decomposition by one primitive",
            "capacity": (
                "Conditional work-conservation lower bound for the stated primitive and workload"
            ),
            "storage": (
                "Current allocated source mapped one qubit per rotated patch; "
                "not a memory lower bound on all rewrites"
            ),
            "noise": (
                "Approximate fit gives conditional sufficient certificate distances, "
                "not necessary physical distances"
            ),
            "factory": (
                "Specified 15-to-1 top-stage family only; not a universal magic-state lower bound"
            ),
            "passes": (
                "Passing a necessary screen is not enough to establish feasibility or advantage"
            ),
        },
        sources=[
            "https://arxiv.org/html/1808.06709v4#S2",
            "https://arxiv.org/html/1808.06709v4#S15",
            "https://quantum-journal.org/papers/q-2019-03-05-128/",
        ],
        rows=[one_row(row) for row in rows if row["f"] == 40],
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = generate(args.ledger.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(result['rows'])} fixed-workload screens to {args.output}")


if __name__ == "__main__":
    main()
