"""Finite-target development comparisons; never admits a continuous-price claim."""

from dataclasses import asdict
import math

from .encoding_decision import Encoding
from .intervals import price_decision
from .storage import rng_for
from .unequal_allocation import ARMS, choose_batch, terminal_decision, PILOT
from .w14_circuits import DEPTHS, fixed_interval


def fixed_comparison(
    responses, scale, offset, truth, method, eta, assumed_eta, namespace, trials, emit
):
    """Independent finite binomial draws, probabilities checked by density circuits."""
    if method not in ("direct_shots", "direct_queries", "depth_limited"):
        raise ValueError("unknown comparison")
    depths = list(DEPTHS) if method == "depth_limited" else [0]
    shots = [128] * 5 if method == "depth_limited" else [640 if method == "direct_shots" else 3200]
    rows = []
    # matched/ignored inference share observations; assumed_eta absent from keys.
    probabilities = [responses[(k, eta)]["density_probability"] for k in depths]
    for trial in range(trials):
        counts = (
            rng_for(namespace, "fixed", method, eta, trial).binomial(shots, probabilities).tolist()
        )
        emit(f"draw_{trial}", dict(counts=counts, shots=shots, depths=depths))
        confidence = fixed_interval(counts, shots, depths, assumed_eta)
        decision = price_decision(confidence, scale, offset, 0.0, 1.0)
        interval = decision["interval"]
        estimate = None if interval is None else sum(interval) / 2
        rows.append(
            dict(
                trial=trial,
                counts=counts,
                decision=decision,
                estimate=estimate,
                contains=None if interval is None else interval[0] <= truth <= interval[1],
                absolute_error=None if estimate is None else abs(estimate - truth),
            )
        )
    cost = dict(
        shots=sum(shots),
        A_equivalents=sum(n * (2 * k + 1) for k, n in zip(depths, shots)),
        grover_queries=sum(n * k for k, n in zip(depths, shots)),
        logical_cx=sum(n * responses[(k, eta)]["circuit"]["cx"] for k, n in zip(depths, shots)),
        maximum_depth=max(responses[(k, eta)]["circuit"]["depth"] for k in depths),
        maximum_measurement_depth=max(
            responses[(k, eta)]["measurement_circuit"]["depth"] for k in depths
        ),
        depth_convention="maximum_depth is unitary-only",
        evidence_kind="projected_acquisition_cost_from_measured_circuit_counts",
        qubits=responses[(0, eta)]["circuit"]["qubits"],
    )
    return dict(
        method=method,
        eta=eta,
        assumed_eta=assumed_eta,
        trials=rows,
        per_trial_cost=cost,
        model_valid=eta == assumed_eta,
        guarantee=(
            "conditional fixed-schedule CP; no application certificate"
            if eta == assumed_eta
            else "outside assumed noise model; interval width is not a coverage guarantee"
        ),
    )


def policy_comparison(a, scale, offset, truth, arm, drift, guard, namespace, trials, cx, emit):
    if arm not in ARMS:
        raise ValueError("unknown policy")
    encoding = Encoding("finite_grid_diagnostic", scale, offset, 0.0, float(cx))
    f, g = 0.02, 0.07
    q = f + drift + (1 - f - g - 2 * drift) * a
    rows = []
    for trial in range(trials):
        # Same drift/arm sample streams for transfer-bound inference ablation.
        rng = rng_for(namespace, "policy", arm, drift, trial)
        pilot = (
            int(rng.binomial(PILOT, q))
            if arm in ("pilot_cp", "unequal_full", "unequal_target")
            else None
        )
        emit(f"pilot_{trial}", dict(successes=pilot, shots=0 if pilot is None else PILOT))
        plan = choose_batch(encoding, arm, pilot, guard=guard, tolerance=1.0)
        emit(f"plan_{trial}", asdict(plan))
        m0, m1, n = plan.m0, plan.m1, plan.n
        # Independent fresh terminal calibration and validation, never pilot reuse.
        calibration = [int(rng.binomial(m0, f)), int(rng.binomial(m1, g))]
        count = int(rng.binomial(n, q))
        emit(f"draw_{trial}", dict(calibration=calibration, count=count, m0=m0, m1=m1, n=n))
        decision = terminal_decision(encoding, count, n, calibration, m0, m1, guard=guard)
        interval = decision["interval"]
        estimate = None if interval is None else sum(interval) / 2
        # Calibration prepares basis states, not expensive A circuits.
        pricing_calls = n + plan.pilot_shots
        rows.append(
            dict(
                trial=trial,
                plan=asdict(plan),
                decision=decision,
                estimate=estimate,
                total_shots=plan.total_shots,
                A_equivalents=pricing_calls,
                logical_cx=pricing_calls * cx,
                calibration_shots=m0 + m1,
                calibration_cx=0,
                absolute_error=None if estimate is None else abs(estimate - truth),
                contains=None if interval is None else interval[0] <= truth <= interval[1],
            )
        )
    return dict(
        arm=arm,
        drift=drift,
        supplied_guard=guard,
        trials=rows,
        finite_diagnostic_only=True,
        model_valid=guard >= drift,
        note="basis-state calibration has zero logical CX, not zero runtime or physical cost",
    )


def classical_comparison(data, representation, offset, truth, namespace, trials, emit):
    values = data[representation]
    rows = []
    for trial in range(trials):
        indices = rng_for(namespace, "classical_path", trial).choice(
            len(values), 3200, p=data["weights"]
        )
        # Same classical paths across raw and residual representations.
        sampled = values[indices]
        estimate = float(sampled.mean()) + offset
        emit(f"draw_{trial}", dict(indices=indices.tolist()))
        rows.append(
            dict(
                estimate=estimate,
                absolute_error=abs(estimate - truth),
                sample_standard_error=float(sampled.std(ddof=1) / math.sqrt(len(sampled))),
                path_evaluations=len(sampled),
            )
        )
    return dict(
        method="iid_finite_paths_same_geometric_control",
        trials=rows,
        exact_finite_sum=float(data["weights"] @ values) + offset,
        finite_table_entries=len(values),
        setup_enumerates_entire_target=True,
        guarantee="sample SE is descriptive; no confidence certificate",
    )
