"""Bounded research comparators; no production execution or exact-probability fallback.

IQAE takes a unitary state preparation with the GOOD flag on its last qubit.
Checkpoints receive ("native_iqae", event, JSON-compatible snapshot). A completed
batch is checkpointed before handing its sampled result back to native IQAE.
csAE is a fixed-truth simulation evaluator, not a circuit-backed estimator.
"""

from copy import deepcopy
from numbers import Integral, Real
from time import perf_counter

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.algorithms import EstimationProblem, IterativeAmplitudeEstimation
from qiskit.primitives import Sampler

from .vendor import mlqae_core


SHOTS = 256
MAX_K = 16
MAX_BATCHES = 64
MAX_A_EQUIVALENTS = 65536
SEED_TRANSPILER = 14001


def _real(name, value, lower=None, upper=None, positive=False):
    if isinstance(value, bool) or not isinstance(value, Real) or not np.isfinite(value):
        raise ValueError(f"{name} must be a finite real number")
    value = float(value)
    if (
        (positive and value <= 0)
        or (lower is not None and value < lower)
        or (upper is not None and value > upper)
    ):
        raise ValueError(f"{name} is outside its allowed range")
    return value


def _integer(name, value, minimum=0):
    if isinstance(value, bool) or not isinstance(value, Integral) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return int(value)


def _totals(ledger):
    return {
        "batches": len(ledger),
        "shots": sum(b["shots"] for b in ledger),
        "a_equivalent_queries": sum(b["shots"] * (2 * b["k"] + 1) for b in ledger),
        "grover_queries": sum(b["shots"] * b["k"] for b in ledger),
        "cx": sum(b["shots"] * b["compiled_cx"] for b in ledger),
        "max_depth": max((b["compiled_depth"] for b in ledger), default=0),
        "max_unitary_depth": max((b["compiled_unitary_depth"] for b in ledger), default=0),
    }


class _ResourceCapError(RuntimeError):
    pass


class _CheckpointFailureError(RuntimeError):
    pass


class _TaggedIQAE(IterativeAmplitudeEstimation):
    def construct_circuit(self, estimation_problem, k=0, measurement=False):
        circuit = super().construct_circuit(estimation_problem, k, measurement)
        circuit.metadata = dict(circuit.metadata or {}, grover_power=int(k))
        return circuit


class _CompletedJob:
    def __init__(self, result):
        self._result = result

    def result(self):
        return self._result


class _LedgerSampler:
    """Synchronous boundary around the installed finite-shot Sampler."""

    def __init__(self, seed, checkpoint):
        self.sampler = Sampler(options={"shots": SHOTS, "seed": np.random.default_rng(seed)})
        self.checkpoint = checkpoint
        self.ledger = []
        self.attempted = None
        self.cap_error = None
        self.costs_unknown = False

    def emit(self, event, value):
        if self.checkpoint is not None:
            try:
                self.checkpoint("native_iqae", event, deepcopy(value))
            except Exception as error:
                raise _CheckpointFailureError(event) from error

    def run(self, circuits):
        if len(circuits) != 1:
            raise ValueError("Native IQAE must submit one circuit per batch")
        circuit = circuits[0]
        k = _integer("grover_power", circuit.metadata["grover_power"])
        totals = _totals(self.ledger)
        attempted = {
            "batch": len(self.ledger),
            "k": k,
            "shots": SHOTS,
            "requested_shots": SHOTS,
            "stage": "cap_check",
        }
        self.attempted = attempted
        reason = None
        if k > MAX_K:
            reason = "max_k"
        elif len(self.ledger) >= MAX_BATCHES:
            reason = "max_batches"
        elif totals["a_equivalent_queries"] + SHOTS * (2 * k + 1) > MAX_A_EQUIVALENTS:
            reason = "max_a_equivalents"
        if reason is not None:
            self.attempted = dict(attempted, reason=reason)
            self.cap_error = _ResourceCapError(reason)
            raise self.cap_error
        attempted.update(
            stage="compile",
            seed_transpiler=SEED_TRANSPILER,
            compile_seconds=0.0,
            sampler_seconds=0.0,
        )
        started = perf_counter()
        try:
            compiled = transpile(
                circuit,
                basis_gates=["u", "cx"],
                optimization_level=0,
                seed_transpiler=SEED_TRANSPILER,
            )
        finally:
            attempted["compile_seconds"] = perf_counter() - started
        ops = compiled.count_ops()
        batch = dict(
            attempted,
            compiled_u=int(ops.get("u", 0)),
            compiled_cx=int(ops.get("cx", 0)),
            compiled_depth=int(compiled.depth()),
            compiled_unitary_depth=int(compiled.remove_final_measurements(inplace=False).depth()),
            compiled_qubits=compiled.num_qubits,
        )
        self.attempted = batch
        batch["stage"] = "sampler_batch_started"
        self.emit("sampler_batch_started", batch)
        batch["stage"] = "sampler_run"
        self.costs_unknown = True
        started = perf_counter()
        try:
            job = self.sampler.run([compiled])
            batch["stage"] = "sampler_result"
            result = job.result()
        finally:
            batch["sampler_seconds"] = perf_counter() - started
        batch["stage"] = "sampler_counts_validation"
        if result.metadata[0].get("shots") != SHOTS:
            raise RuntimeError("Sampler did not return the requested finite shot count")
        counts = {
            key: int(round(value * SHOTS))
            for key, value in result.quasi_dists[0].binary_probabilities().items()
        }
        if sum(counts.values()) != SHOTS or any(value < 0 for value in counts.values()):
            raise RuntimeError("Sampler result is not finite-shot counts")
        batch["counts"] = counts
        batch["stage"] = "sampler_batch_completed"
        self.ledger.append(batch)
        self.costs_unknown = False
        self.emit("sampler_batch_completed", {"batch": batch, "totals": _totals(self.ledger)})
        self.attempted = None
        return _CompletedJob(result)


def native_iqae(circuit, scale, offset, seed, checkpoint=None, tolerance=1.0):
    """Run native beta IQAE; cap/error results deliver no estimate or interval.

    Price = offset + scale * GOOD-flag probability. Resource totals describe
    completed batches only; ``native_querycount`` is absent (None) unless native
    estimation returns a result, and crosschecks Grover queries, not A equivalents.
    Unknown sampler expense is flagged separately from completed-ledger totals.
    Checkpoint failures propagate to the caller; other failures return error rows.
    Timings are local wall-clock durations, not quantum-device execution times.
    """
    scale = _real("scale", scale, positive=True)
    offset = _real("offset", offset)
    tolerance = _real("tolerance", tolerance, positive=True)
    seed = _integer("seed", seed)
    epsilon = min(0.49, tolerance / scale)
    if epsilon <= 0 or not np.isfinite(offset + scale):
        raise ValueError("Price mapping or epsilon is not representable")
    if not isinstance(circuit, QuantumCircuit) or circuit.num_qubits < 1:
        raise ValueError("circuit must be a nonempty QuantumCircuit")
    if (
        circuit.num_clbits
        or circuit.num_parameters
        or any(item.operation.name in {"measure", "reset"} for item in circuit.data)
    ):
        raise ValueError("circuit must be a bound, unitary state preparation")
    if checkpoint is not None and not callable(checkpoint):
        raise ValueError("checkpoint must be callable")
    sampler = _LedgerSampler(seed, checkpoint)
    row = {
        "method": "qiskit.algorithms.IterativeAmplitudeEstimation",
        "seed": seed,
        "alpha": 0.05,
        "epsilon_target": epsilon,
        "confint_method": "beta",
        "scale": scale,
        "offset": offset,
        "tolerance": tolerance,
        "objective_qubits": [circuit.num_qubits - 1],
        "caps": {
            "max_k": MAX_K,
            "max_batches": MAX_BATCHES,
            "max_a_equivalents": MAX_A_EQUIVALENTS,
        },
        "status": "error",
        "delivery": "none",
        "amplitude_estimate": None,
        "amplitude_interval": None,
        "price_estimate": None,
        "price_interval": None,
        "native_querycount": None,
        "native_querycount_matches_ledger": None,
        "seed_transpiler": SEED_TRANSPILER,
        "timing_scope": "local_wall_clock_not_device_time",
        "totals_scope": "completed_batches_only",
        "depth_conventions": {
            "compiled_depth": "measurement-inclusive",
            "max_depth": "measurement-inclusive",
            "compiled_unitary_depth": "final measurements removed via remove_final_measurements",
            "max_unitary_depth": "maximum compiled_unitary_depth across completed batches",
            "decomposition": (
                "native IQAE oracle decomposition; not normalized to fixed-response circuits"
            ),
        },
    }
    try:
        algorithm = _TaggedIQAE(
            epsilon_target=epsilon, alpha=0.05, confint_method="beta", sampler=sampler
        )
        problem = EstimationProblem(
            state_preparation=circuit,
            objective_qubits=[circuit.num_qubits - 1],
            post_processing=lambda a: offset + scale * a,
        )
        result = algorithm.estimate(problem)
        row["native_querycount"] = _integer("native_querycount", result.num_oracle_queries)
        row["native_querycount_matches_ledger"] = (
            row["native_querycount"] == _totals(sampler.ledger)["grover_queries"]
        )
        if not row["native_querycount_matches_ledger"]:
            raise RuntimeError("Native query count does not match completed-ledger Grover queries")
        row.update(
            status="completed",
            delivery="native_interval",
            amplitude_estimate=float(result.estimation),
            amplitude_interval=list(map(float, result.confidence_interval)),
            price_estimate=float(result.estimation_processed),
            price_interval=list(map(float, result.confidence_interval_processed)),
        )
    except Exception as error:
        row.update(
            status="error",
            delivery="none",
            amplitude_estimate=None,
            amplitude_interval=None,
            price_estimate=None,
            price_interval=None,
        )
        # Terra wraps sampler failures in AlgorithmError. Match our exact cap
        # exception through the cause chain; never classify by error message.
        cause = error
        while cause is not None and cause is not sampler.cap_error:
            if isinstance(cause, _CheckpointFailureError):
                raise cause.__cause__ from None
            cause = cause.__cause__
        if sampler.cap_error is not None and cause is sampler.cap_error:
            row.update(status="resource_capped", attempted=sampler.attempted)
        else:
            row["error"] = {
                "type": type(error).__name__,
                "message": str(error),
                "cause": repr(error.__cause__),
            }
    row.update(
        ledger=deepcopy(sampler.ledger),
        totals=_totals(sampler.ledger),
        attempted=deepcopy(sampler.attempted),
        costs_unknown=sampler.costs_unknown,
    )
    return row


def native_csae(amplitude, seed, eta, model_eta, trials=16):
    """Evaluate the unchanged vendored schedule, returning point estimates only.

    ``amplitude`` is GOOD probability a. Source a_true is sqrt(a), source
    counts are BAD flags with cos²((2k+1)theta), and estimates are sin²(theta).
    Fixed truth enters only the source evaluator's sampling/error diagnostics;
    the source likelihood searches its original global theta grid. No truth-
    restricted estimator search or confidence interval is introduced.
    """
    amplitude = _real("amplitude", amplitude, lower=0, upper=1)
    seed = _integer("seed", seed)
    eta = _real("eta", eta, lower=0, upper=1)
    model_eta = eta if model_eta is None else _real("model_eta", model_eta, lower=0, upper=1)
    trials = _integer("trials", trials, minimum=1)
    depths, shots = mlqae_core.flagship_schedule(4, base=64)
    source = mlqae_core.evaluate_schedule(
        depths,
        shots,
        trials,
        seed,
        a_range=(np.sqrt(amplitude), np.sqrt(amplitude)),
        return_extra=True,
        eta=eta,
        model_eta=model_eta,
    )
    outputs = {
        key: value.tolist() if isinstance(value, np.ndarray) else value
        for key, value in source.items()
    }
    return {
        "method": "vendored mlqae_core.flagship_schedule/evaluate_schedule",
        "status": "completed",
        "delivery": "point_only",
        "confidence_interval": None,
        "seed": seed,
        "trials": trials,
        "eta": eta,
        "model_eta": model_eta,
        "known_eta_assumption": model_eta == eta,
        "noise_assumption": "known_eta_matched" if model_eta == eta else "mismatched_eta",
        "fixed_truth_exposure": "evaluator_sampling_and_error_diagnostics_only",
        "truth_good_probability": amplitude,
        "counts_flag": "BAD",
        "counts_probability": "(1-eta)**(2*k+1)*cos((2*k+1)*theta)**2 + (1-(1-eta)**(2*k+1))/2",
        "depths": list(depths),
        "shots": list(shots),
        "counts": outputs["counts"],
        "amplitude_estimates": (np.sin(source["theta_hat"]) ** 2).tolist(),
        "source_outputs": outputs,
        "per_trial_cost": {
            "shots": int(sum(shots)),
            "grover_queries": int(np.dot(shots, depths)),
            "a_equivalent_queries": int(np.dot(shots, 2 * np.asarray(depths) + 1)),
            "source_queries": int(source["nq"]),
        },
    }
