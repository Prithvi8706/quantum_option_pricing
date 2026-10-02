"""Oracle depths for items C7/C8 and the decision-point table (ANALYSIS_SPEC_STAGE_C.md).

(a) the historical favourable leaf-table score of `barrier_oracle_depth`, whose builder reads
module constants; `build_case` sets them to the case's parameters for the call and restores
them (the archived script is not edited). (b) the Stage A compile pipeline (optimize,
generic truncated library, compile, exact DAG, unrestricted wave schedule) writing fresh
task-local leaf libraries under the given output directory, never into archived ones.
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research" / "advantage_frontier_20260923"))
import barrier_oracle_depth as bod  # noqa: E402

from research.controlled_completion_followup.truncated_multiplier import TruncatedLibrary  # noqa: E402
from research.controlled_priority_completion.parallel_source import make_schedule  # noqa: E402
from research.controlled_source_completion.compiler import compile_graph  # noqa: E402
from research.controlled_source_completion.optimize import optimize  # noqa: E402
from research.frontier_completion_20260927.stage_a import exact_dag  # noqa: E402

CONSTANTS = ("SIGMA", "CORR", "S0", "RATE", "T", "K", "H")


def build_case(case, free_gaussians=False):
    saved = {k: getattr(bod, k) for k in CONSTANTS}
    try:
        for k, v in zip(CONSTANTS, (case.sigma, case.rho, case.spot, case.rate, case.maturity,
                                    case.strike, case.barrier)):
            setattr(bod, k, v)
        return bod.build(case.na, case.nt, free_gaussians=free_gaussians)
    finally:
        for k, v in saved.items():
            setattr(bod, k, v)


def favourable_score(case):
    fav, _ = bod.leaf_costs()
    return bod.score(build_case(case), fav)


def compiled_depths(case, out_dir):
    """Clean dependency-only (2 x forward) and clean scheduled (unrestricted wave) depths."""
    started = time.perf_counter()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=False)
    target = optimize(build_case(case).as_dict())
    lib = TruncatedLibrary(out_dir / "leaves_f40", 72, 40, target["tables"],
                           out_dir / "base_leaves_f40")
    source, _ = compile_graph(target, out_dir / "source", lib)
    exact = exact_dag(source)
    schedule = make_schedule(source, None)
    assert exact["forward_dependency_t_depth"] == schedule["dependency_only_forward_t_depth"]
    return dict(forward_dependency_t_depth=exact["forward_dependency_t_depth"],
                clean_dependency_t_depth=2 * exact["forward_dependency_t_depth"],
                clean_scheduled_t_depth=schedule["resources"]["t_depth"],
                clean_t_count=schedule["resources"]["t_count"],
                logical_qubits=schedule["resources"]["logical_qubits"],
                seconds=time.perf_counter() - started)
