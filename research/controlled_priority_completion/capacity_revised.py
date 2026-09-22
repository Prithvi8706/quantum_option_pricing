"""Capacity accounting for the explicit Hadamard and bounded-QAE refinements."""

import argparse
import hashlib
import json
from pathlib import Path

from research.controlled_priority_completion.capacity_screen import (
    CLOCKS,
    BASE,
    NOISES,
    PHYSICAL_CAP,
    ROOT,
    STRICT_C4_SECONDS,
    capacity_bound,
    certificate_distance,
    distillation_certificate,
    magic_supply_bound,
    patch_qubits,
)


DIRECTORY = ROOT / "results/controlled_priority_completion"


def revised_rows(hadamard, bounded):
    """Extract fixed counts; intentionally omit synthesis from all work floors."""
    rows = []
    for source in hadamard:
        rows.append(dict(
            model=source["model"],
            method="hadamard_" + source["mode"],
            calls=source["allocation"]["controlled_U_calls"],
            arithmetic_t=source["arithmetic_T_count"],
            arithmetic_ccx=(
                source["single_U"]["ccx"] * source["allocation"]["controlled_U_calls"]
            ),
            allocated_qubits_upper=source["logical_qubits_upper"],
            required_budget_seconds=source["tenfold_total_budget_seconds"],
        ))
    for source in bounded:
        calls = source["allocation"]["controlled_grover_calls"]
        assert source["single_iterate_T_count"] % 7 == 0
        rows.append(dict(
            model=source["model"],
            method="bounded_shifted_QAE",
            calls=calls,
            arithmetic_t=source["arithmetic_T_count"],
            arithmetic_ccx=calls * (source["single_iterate_T_count"] // 7),
            allocated_qubits_upper=source["logical_qubits_upper"],
            required_budget_seconds=source["tenfold_total_budget_seconds"],
        ))
    return rows


def replace_financial_source(row, source_root):
    """Rebind fixed financial F/F-inverse work; preserve all other iterate work.

    Both estimators use exactly one financial forward and inverse per iterate,
    which equals the clean financial oracle's T/CCX work. This substitution does
    not treat its doubled passes as two clean sources. Output-copy CXs do not
    contribute T/CCX. The source must preserve the exact digital output contract.
    """
    old_path = BASE / "compile_v2" / f"{row['model']}_f40" / "source.json"
    new_path = source_root / f"{row['model']}_f40" / "source.json"
    old, new = [json.loads(path.read_text()) for path in (old_path, new_path)]
    if (old["word_width"], old["fraction_bits"], old["inputs"], old["outputs"]) != (
        new["word_width"], new["fraction_bits"], new["inputs"], new["outputs"]
    ):
        raise ValueError("Financial source interface changed; cannot substitute counts")
    old_res, new_res = old["resources"], new["resources"]
    result = dict(row)
    result["arithmetic_t"] += row["calls"] * (new_res["t_count"] - old_res["t_count"])
    result["arithmetic_ccx"] += row["calls"] * (new_res["ccx"] - old_res["ccx"])
    result["allocated_qubits_upper"] += (
        new_res["logical_qubits"] - old_res["logical_qubits"]
    )
    result["substituted_source"] = dict(
        path=str(new_path.relative_to(ROOT)).replace("\\", "/"),
        old_sha256=hashlib.sha256(old_path.read_bytes()).hexdigest(),
        new_sha256=hashlib.sha256(new_path.read_bytes()).hexdigest(),
        old_resources=old_res,
        new_resources=new_res,
        obligation="Same digital output semantics must be proved by the source validation",
    )
    return result


def screen(row):
    budget = row["required_budget_seconds"]
    contracts = [("empirical_RQMC", budget)]
    if row["model"] == "C4":
        contracts.append(("fixed_iid", STRICT_C4_SECONDS / 10))
    return dict(
        **row,
        contracts=[dict(
            contract=name,
            tenfold_budget_seconds=contract_budget,
            free_data_free_factory_work_capacity=[dict(
                primitive=primitive,
                operations=work,
                lane_physical_qubits=space,
                primitive_seconds=clock,
                minimum_work_seconds=capacity_bound(work, PHYSICAL_CAP, space, clock),
                passes_necessary_screen=(
                    capacity_bound(work, PHYSICAL_CAP, space, clock) <= contract_budget
                ),
            ) for primitive, work in (
                ("T", row["arithmetic_t"]), ("native_CCX_sensitivity", row["arithmetic_ccx"])
            ) for space in (1, 3, 17, 49, 97) for clock in CLOCKS],
            required_magic_states_per_physical_qubit_second=(
                max(0, row["arithmetic_t"] - PHYSICAL_CAP) / contract_budget / PHYSICAL_CAP
            ),
            deadline_certificate_sensitivity=[dict(
                physical_error=p,
                cycle_seconds=clock,
                **certificate_distance(
                    row["allocated_qubits_upper"], contract_budget, clock, p
                ),
            ) for p in NOISES for clock in CLOCKS],
        ) for name, contract_budget in contracts],
        allocated_rotated_patch_storage=[dict(
            distance=d,
            data_only_physical_qubits=row["allocated_qubits_upper"] * patch_qubits(d),
            fits_cap=row["allocated_qubits_upper"] * patch_qubits(d) <= PHYSICAL_CAP,
        ) for d in (1, 3, 5, 7, 15, 25)],
        free_data_patch_lane_capacity=[dict(
            distance=d,
            cycle_seconds=clock,
            rounds_per_T=rounds,
            minimum_T_work_seconds=capacity_bound(
                row["arithmetic_t"], PHYSICAL_CAP, patch_qubits(d), rounds * clock
            ),
        ) for d in (3, 5, 7, 15, 25) for clock in CLOCKS for rounds in (1, d)],
        free_data_15_to_1_top_stage_supply=[dict(
            distance=d,
            cycle_seconds=clock,
            minimum_supply_seconds=magic_supply_bound(
                row["arithmetic_t"], PHYSICAL_CAP, d, clock
            ),
        ) for d in (3, 5, 7, 15, 25) for clock in CLOCKS],
        sufficient_factory_quality=[dict(
            raw_error=p,
            **distillation_certificate(row["arithmetic_t"], p),
        ) for p in NOISES],
    )


def generate(directory=DIRECTORY, source_root=None):
    files = [directory / "estimator_hadamard.json", directory / "estimator_bounded.json"]
    loaded = [json.loads(path.read_text()) for path in files]
    rows = revised_rows(*loaded)
    if source_root is not None:
        rows = [replace_financial_source(row, source_root) for row in rows]
    return dict(
        schema="controlled-compound-revised-capacity-v1",
        physical_qubit_cap=PHYSICAL_CAP,
        input_sha256={path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
        assumptions=[
            "No serial-depth upper bound is used as a runtime lower bound.",
            "Work capacity assumes fixed operations and explicitly bounded lane throughput.",
            "Native CCX replaces each arithmetic CCX by one primitive and omits other work.",
            "Factory capacity is for the stated 15-to-1 family, not all architectures.",
            "Allocated storage is a mapping constraint, not a universal memory lower bound.",
            "Noise-fit union tests give sufficient conditional certificates only.",
            "Fresh price setup, financial certificate costs and output costs remain additional.",
        ],
        rows=[screen(row) for row in rows],
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--output", type=Path, default=DIRECTORY / "capacity_revised.json")
    args = parser.parse_args()
    output = generate(source_root=args.source_root.resolve() if args.source_root else None)
    path = args.output
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(output['rows'])} revised capacity screens to {path}")


if __name__ == "__main__":
    main()
