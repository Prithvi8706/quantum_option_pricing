"""Small synthetic fixtures only; seeds here are TEST-only, not experiment seeds."""

import numpy as np
import pytest
from qiskit import QuantumCircuit, transpile
from qiskit.algorithms import EstimationProblem, IterativeAmplitudeEstimation

from research.journal_sprint import w14_comparators as adapters


TEST_SEED = 713
TEST_TRUTH = 0.173


@pytest.fixture
def preparation():
    circuit = QuantumCircuit(2)
    circuit.ry(2 * np.arcsin(np.sqrt(TEST_TRUTH)), 0)
    circuit.cx(0, 1)
    return circuit


def test_native_interval_and_actual_compiled_cost(preparation):
    events = []
    row = adapters.native_iqae(
        preparation, 12, -2, TEST_SEED, checkpoint=lambda *args: events.append(args), tolerance=0.4
    )
    assert row["status"] == "completed"
    assert row["delivery"] == "native_interval"
    assert row["epsilon_target"] == pytest.approx(0.4 / 12)
    assert row["alpha"] == 0.05 and row["confint_method"] == "beta"
    assert row["price_interval"] == pytest.approx(
        [-2 + 12 * value for value in row["amplitude_interval"]]
    )
    assert row["price_estimate"] == pytest.approx(-2 + 12 * row["amplitude_estimate"])
    assert row["price_interval"][1] - row["price_interval"][0] <= 0.8
    assert row["native_querycount_matches_ledger"] is True
    assert row["native_querycount"] == row["totals"]["grover_queries"]
    assert len(events) == 2 * len(row["ledger"])
    problem = EstimationProblem(preparation, objective_qubits=[1])
    algorithm = IterativeAmplitudeEstimation(0.1, 0.05)
    for i, batch in enumerate(row["ledger"]):
        assert sum(batch["counts"].values()) == batch["shots"] == 256
        compiled = transpile(
            algorithm.construct_circuit(problem, batch["k"], True),
            basis_gates=["u", "cx"],
            optimization_level=0,
            seed_transpiler=14001,
        )
        assert batch["compiled_cx"] == compiled.count_ops().get("cx", 0)
        assert batch["compiled_u"] == compiled.count_ops().get("u", 0)
        assert batch["compiled_depth"] == compiled.depth()
        assert (
            batch["compiled_unitary_depth"]
            == compiled.remove_final_measurements(inplace=False).depth()
        )
        assert batch["compiled_unitary_depth"] < batch["compiled_depth"]
        assert batch["compiled_qubits"] == compiled.num_qubits == 2
        assert batch["seed_transpiler"] == 14001
        for field in ("compile_seconds", "sampler_seconds"):
            assert np.isfinite(batch[field]) and batch[field] >= 0
        assert events[2 * i][0:2] == ("native_iqae", "sampler_batch_started")
        assert events[2 * i + 1][2]["batch"] == batch
    ledger = row["ledger"]
    assert row["totals"] == {
        "batches": len(ledger),
        "shots": 256 * len(ledger),
        "a_equivalent_queries": sum(256 * (2 * b["k"] + 1) for b in ledger),
        "grover_queries": sum(256 * b["k"] for b in ledger),
        "cx": sum(256 * b["compiled_cx"] for b in ledger),
        "max_depth": max(b["compiled_depth"] for b in ledger),
        "max_unitary_depth": max(b["compiled_unitary_depth"] for b in ledger),
    }
    assert row["depth_conventions"]["max_depth"] == "measurement-inclusive"
    assert row["depth_conventions"]["compiled_depth"] == "measurement-inclusive"
    assert "native IQAE oracle decomposition" in row["depth_conventions"]["decomposition"]


def test_sampler_persistent_rng_and_replay(preparation):
    circuit = preparation.copy()
    circuit.measure_all()
    circuit.metadata = {"grover_power": 0}
    streams = []
    for _ in range(2):
        sampler = adapters._LedgerSampler(TEST_SEED, None)
        rng = sampler.sampler.options.seed
        assert isinstance(rng, np.random.Generator)
        for _ in range(3):
            sampler.run([circuit]).result()
            assert sampler.sampler.options.seed is rng
        streams.append([batch["counts"] for batch in sampler.ledger])
    assert streams[0] == streams[1]
    assert streams[0][0] != streams[0][1]


@pytest.mark.parametrize(
    "k,completed,reason", [(17, 0, "max_k"), (0, 64, "max_batches"), (16, 7, "max_a_equivalents")]
)
def test_exact_safety_caps(preparation, k, completed, reason):
    sampler = adapters._LedgerSampler(TEST_SEED, None)
    circuit = preparation.copy()
    circuit.measure_all()
    circuit.metadata = {"grover_power": k}
    for _ in range(completed):
        sampler.run([circuit]).result()
    before = adapters._totals(sampler.ledger)
    with pytest.raises(adapters._ResourceCapError, match=reason):
        sampler.run([circuit])
    assert len(sampler.ledger) == completed
    assert adapters._totals(sampler.ledger) == before
    assert sampler.attempted["k"] == k
    assert sampler.attempted["reason"] == reason


def test_cap_wrapped_by_native_preserves_completed_ledger(monkeypatch, preparation):
    powers = iter([0, 17])
    monkeypatch.setattr(
        IterativeAmplitudeEstimation, "_find_next_k", lambda *args, **kwargs: (next(powers), True)
    )
    row = adapters.native_iqae(preparation, 10000, 0, TEST_SEED)
    assert row["status"] == "resource_capped"
    assert row["delivery"] == "none"
    assert row["price_interval"] is None and row["amplitude_interval"] is None
    assert row["native_querycount"] is None
    assert row["native_querycount_matches_ledger"] is None
    assert len(row["ledger"]) == 1
    assert row["totals"]["shots"] == 256
    assert row["attempted"]["k"] == 17


def test_native_untouched_schedule_can_exceed_cap(preparation):
    row = adapters.native_iqae(preparation, 12, -2, TEST_SEED, tolerance=0.2)
    assert row["status"] == "resource_capped"
    assert row["attempted"]["k"] > 16
    assert [batch["k"] for batch in row["ledger"]] == [0, 2]
    assert row["price_interval"] is None


def test_a_equivalent_cap_allows_exact_boundary(preparation):
    sampler = adapters._LedgerSampler(TEST_SEED, None)
    circuit = preparation.copy()
    circuit.measure_all()
    for k in [16] * 7 + [12]:
        circuit.metadata = {"grover_power": k}
        sampler.run([circuit])
    assert adapters._totals(sampler.ledger)["a_equivalent_queries"] == 65536
    circuit.metadata = {"grover_power": 0}
    with pytest.raises(adapters._ResourceCapError, match="max_a_equivalents"):
        sampler.run([circuit])


def test_epsilon_clamp(preparation):
    row = adapters.native_iqae(preparation, 1, 0, TEST_SEED)
    assert row["epsilon_target"] == 0.49
    assert row["status"] == "completed"


def test_no_exact_probability_fallback(monkeypatch, preparation):
    original = adapters.Sampler.run

    def without_shots(self, *args, **kwargs):
        result = original(self, *args, **kwargs).result()
        result.metadata[0].pop("shots")
        return adapters._CompletedJob(result)

    monkeypatch.setattr(adapters.Sampler, "run", without_shots)
    row = adapters.native_iqae(preparation, 10, 0, TEST_SEED)
    assert row["status"] == "error"
    assert row["delivery"] == "none" and row["price_interval"] is None
    assert "finite shot" in row["error"]["cause"]


def test_counts_checkpointed_before_native_postprocess(monkeypatch, preparation):
    events = []

    def fail(*args, **kwargs):
        assert events[-1][1] == "sampler_batch_completed"
        assert sum(events[-1][2]["batch"]["counts"].values()) == 256
        raise RuntimeError("postprocess failed, not a cap")

    monkeypatch.setattr(IterativeAmplitudeEstimation, "_good_state_probability", fail)
    row = adapters.native_iqae(
        preparation, 10, 0, TEST_SEED, checkpoint=lambda *args: events.append(args)
    )
    assert row["status"] == "error"
    assert row["error"]["type"] == "RuntimeError"
    assert row["totals"]["shots"] == 256
    assert row["price_interval"] is None


def test_sampler_failure_is_error_not_cap(monkeypatch, preparation):
    def fail(*args, **kwargs):
        raise RuntimeError("max_k is a misleading error message")

    monkeypatch.setattr(adapters.Sampler, "run", fail)
    row = adapters.native_iqae(preparation, 10, 0, TEST_SEED)
    assert row["status"] == "error"
    assert row["totals"]["shots"] == 0
    assert row["totals"]["max_depth"] == row["totals"]["max_unitary_depth"] == 0
    assert "misleading" in row["error"]["cause"]
    assert row["costs_unknown"] is True
    assert row["totals_scope"] == "completed_batches_only"
    assert row["attempted"]["stage"] == "sampler_run"
    assert row["attempted"]["requested_shots"] == 256


@pytest.mark.parametrize("event", ["sampler_batch_started", "sampler_batch_completed"])
def test_checkpoint_failure_propagates_original(monkeypatch, preparation, event):
    failure = OSError("checkpoint storage unavailable")
    original = adapters.Sampler.run
    submitted = []

    def record(self, *args, **kwargs):
        submitted.append(True)
        return original(self, *args, **kwargs)

    def checkpoint(stage, current_event, value):
        if current_event == event:
            if event == "sampler_batch_completed":
                assert sum(value["batch"]["counts"].values()) == 256
            raise failure

    monkeypatch.setattr(adapters.Sampler, "run", record)
    with pytest.raises(OSError) as caught:
        adapters.native_iqae(preparation, 12, -2, TEST_SEED, checkpoint, tolerance=0.4)
    assert caught.value is failure
    assert len(submitted) == (1 if event == "sampler_batch_completed" else 0)


@pytest.mark.parametrize("stage", ["sampler_run", "sampler_result"])
def test_unknown_expense_after_completed_batch(monkeypatch, preparation, stage):
    original = adapters.Sampler.run
    submitted = []

    class FailedJob:
        def result(self):
            raise RuntimeError("result unavailable after submission")

    def fail_second(self, *args, **kwargs):
        submitted.append(True)
        if len(submitted) == 2:
            if stage == "sampler_run":
                raise RuntimeError("submission outcome unknown")
            return FailedJob()
        return original(self, *args, **kwargs)

    monkeypatch.setattr(adapters.Sampler, "run", fail_second)
    row = adapters.native_iqae(preparation, 12, -2, TEST_SEED, tolerance=0.4)
    assert row["status"] == "error" and row["delivery"] == "none"
    assert row["costs_unknown"] is True
    assert row["totals"]["shots"] == 256
    assert row["totals_scope"] == "completed_batches_only"
    assert row["attempted"]["stage"] == stage
    assert row["attempted"]["batch"] == 1
    assert row["attempted"]["requested_shots"] == 256
    assert row["attempted"]["compiled_cx"] > 0
    for field in ("compile_seconds", "sampler_seconds"):
        assert np.isfinite(row["attempted"][field]) and row["attempted"][field] >= 0


@pytest.mark.parametrize("corruption", ["query_count", "processed_interval"])
def test_native_result_failure_cannot_deliver_interval(monkeypatch, preparation, corruption):
    original = IterativeAmplitudeEstimation.estimate

    def corrupt(self, *args, **kwargs):
        result = original(self, *args, **kwargs)
        if corruption == "query_count":
            result.num_oracle_queries += 1
        else:
            result.confidence_interval_processed = None
        return result

    monkeypatch.setattr(IterativeAmplitudeEstimation, "estimate", corrupt)
    row = adapters.native_iqae(preparation, 12, -2, TEST_SEED, tolerance=0.4)
    assert row["status"] == "error" and row["delivery"] == "none"
    for field in ("amplitude_estimate", "price_estimate", "amplitude_interval", "price_interval"):
        assert row[field] is None
    assert row["costs_unknown"] is False
    assert row["totals"]["shots"] == 512
    if corruption == "query_count":
        assert row["native_querycount_matches_ledger"] is False
        assert row["native_querycount"] == row["totals"]["grover_queries"] + 1
        assert "does not match" in row["error"]["message"]


def test_transpiler_seed_is_passed(monkeypatch, preparation):
    original = adapters.transpile
    seeds = []

    def record(*args, **kwargs):
        seeds.append(kwargs["seed_transpiler"])
        return original(*args, **kwargs)

    monkeypatch.setattr(adapters, "transpile", record)
    row = adapters.native_iqae(preparation, 12, -2, TEST_SEED, tolerance=0.4)
    assert seeds == [14001] * len(row["ledger"])
    assert seeds and row["status"] == "completed"
    assert row["timing_scope"] == "local_wall_clock_not_device_time"
    assert row["costs_unknown"] is False
    assert row["attempted"] is None


def test_csae_source_cosine_counts_and_sine_squared_mapping():
    row = adapters.native_csae(TEST_TRUTH, TEST_SEED, 0.02, None)
    depths, shots = adapters.mlqae_core.flagship_schedule(4, base=64)
    source = adapters.mlqae_core.evaluate_schedule(
        depths,
        shots,
        16,
        TEST_SEED,
        a_range=(np.sqrt(TEST_TRUTH), np.sqrt(TEST_TRUTH)),
        return_extra=True,
        eta=0.02,
        model_eta=0.02,
    )
    assert row["depths"] == depths and row["shots"] == shots
    for key, value in source.items():
        np.testing.assert_equal(row["source_outputs"][key], value)
    np.testing.assert_equal(row["amplitude_estimates"], np.sin(source["theta_hat"]) ** 2)
    rng = np.random.default_rng(TEST_SEED)
    truth = rng.uniform(np.sqrt(TEST_TRUTH), np.sqrt(TEST_TRUTH), 16)
    d = 2 * np.asarray(depths) + 1
    visibility = 0.98**d
    bad_probability = visibility * np.cos(np.outer(np.arcsin(truth), d)) ** 2 + (1 - visibility) / 2
    np.testing.assert_equal(
        row["counts"], rng.binomial(np.asarray(shots)[None, :], bad_probability)
    )
    assert np.mean(np.asarray(row["counts"])[:, 0]) / shots[0] > 0.7
    assert row["counts_flag"] == "BAD"
    assert row["delivery"] == "point_only" and row["confidence_interval"] is None
    assert row["known_eta_assumption"] is True
    assert row["fixed_truth_exposure"] == "evaluator_sampling_and_error_diagnostics_only"
    assert row["seed"] == TEST_SEED


def test_csae_mismatch_changes_model_only():
    matched = adapters.native_csae(TEST_TRUTH, TEST_SEED, 0.15, 0.15)
    mismatch = adapters.native_csae(TEST_TRUTH, TEST_SEED, 0.15, 0)
    assert matched["counts"] == mismatch["counts"]
    assert matched["amplitude_estimates"] != mismatch["amplitude_estimates"]
    assert mismatch["known_eta_assumption"] is False
    assert mismatch["noise_assumption"] == "mismatched_eta"


@pytest.mark.parametrize(
    "field,value",
    [
        ("scale", 0),
        ("scale", -1),
        ("offset", np.inf),
        ("tolerance", 0),
        ("seed", -1),
        ("seed", True),
    ],
)
def test_iqae_invalid_inputs(preparation, field, value):
    args = dict(circuit=preparation, scale=10, offset=0, seed=TEST_SEED, tolerance=1)
    args[field] = value
    with pytest.raises(ValueError):
        adapters.native_iqae(**args)


@pytest.mark.parametrize(
    "field,value",
    [
        ("amplitude", -0.1),
        ("amplitude", 1.1),
        ("amplitude", np.nan),
        ("eta", -0.1),
        ("model_eta", 1.1),
        ("trials", 0),
        ("trials", 1.5),
        ("seed", -1),
    ],
)
def test_csae_invalid_inputs(field, value):
    args = dict(amplitude=TEST_TRUTH, seed=TEST_SEED, eta=0, model_eta=None, trials=16)
    args[field] = value
    with pytest.raises(ValueError):
        adapters.native_csae(**args)
