# Paper A Foundation and E0 Reference Ladder — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the isolated `research/paper_a/` package through the E0 gate — the frozen benchmark, deterministic stream derivation, the four-layer deterministic price reference ladder, the recording sampler contract, and the resource metrics — so that no stochastic experiment can start until every deterministic semantic check passes.

**Architecture:** A standalone package under `research/paper_a/`, importable as `research.paper_a.*`, with zero imports from `src/` or `app/`. Pure-function modules (`benchmark`, `streams`, `references`, `payoff`) carry no Qiskit dependency and are testable in milliseconds; Qiskit lives only in `european/circuits.py`, `recording.py`, and `resources.py`. Every deterministic quantity is computed twice — once independently in NumPy/SciPy, once by Qiskit — and the two must agree to a frozen tolerance. That double-computation *is* the E0 gate.

**Tech Stack:** Python 3.9.13, qiskit-terra 0.46.3, qiskit-aer 0.12.2, qiskit-algorithms 0.3.1, qiskit-finance 0.4.0, numpy 2.0.2, scipy 1.13.1, pytest 8.4.2, ruff, mypy.

**Spec:** `docs/superpowers/specs/2026-07-27-paper-a-error-budget-roadmap-design.md` (approved 2026-07-29). Annex references below are normative and point at that document.

---

## ✅ RESOLVED 2026-07-29 — Annex B Amended To `paper-a-historical-py39-v2`

The discrepancy below was confirmed by Task 1 and resolved in the user's favour of
the evidence: Annex B now declares the historical candidate as the actual venv
(`qiskit-terra 0.46.3`, `numpy 2.0.2`, no `qiskit` metapackage). See the amendment
record in the spec's Annex B. The Task 1 STOP is lifted; Task 2 onward may proceed.
The original finding is kept below as the reasoning behind that amendment.

## ⚠️ Blocking Finding — Annex B Is Wrong About The Historical Environment

The spec's Annex B declares the historical candidate as `qiskit==0.45.3; qiskit-terra==0.45.3; numpy==1.26.4` and states "the stale README reference to Qiskit 0.46.3 is not authoritative."

**The live `venv/` that produced the existing 250-row dataset is:**

| Package | Annex B says | `venv/` actually has |
|---|---|---|
| `qiskit-terra` | 0.45.3 | **0.46.3** |
| `qiskit` (metapackage) | 0.45.3 | **not installed at all** |
| `numpy` | 1.26.4 | **2.0.2** |
| `qiskit-aer` | 0.12.2 | 0.12.2 ✓ |
| `qiskit-algorithms` | 0.3.1 | 0.3.1 ✓ |
| `qiskit-finance` | 0.4.0 | 0.4.0 ✓ |
| `scipy` | 1.13.1 | 1.13.1 ✓ |
| Python | 3.9.13 | 3.9.13 ✓ |

`README.md:9` and `README.md:185` were correct; `requirements-dev.txt` and `ROADMAP.md:52` are the stale sources. Annex B inverted which one to trust.

**Task 1 produces the evidence; the Annex B amendment is a human decision and must be made before Task 2.** Do not silently reconcile this in code. Per Annex B's own rule, a frozen value changes only via a versioned amendment recorded before affected outputs are inspected.

## Preliminary Signal Worth Knowing

A scratch run of the Annex C construction on `E022` (`S0=98.75778005, T=0.25, sigma=0.30`) at `n=3`, `q_total=1e-4` gives:

```
P_BS = 5.904262   P_grid = 6.271061   P_circuit = 6.951916
e_grid = +0.3668  e_encode = +0.6809
```

Encoding error is roughly **twice** grid error at `c=0.25`, and both exceed the manuscript's current `$0.203` "three-qubit discretization floor". This is one contract at one `q_total`, not a result — but it is direct early support for the spec's premise that `$0.203` conflates layers, and for Figure 6 (the `c` sweep) being worth its place.

Two spec claims were confirmed against the live environment while checking this:
- Qiskit's `LogNormalDistribution.probabilities` **is** the normalized pointwise density `pi_i = f(x_i)/sum_l f(x_l)` (L1 difference `9.1e-16`), exactly as Annex A asserts. Integrated bin masses are not being used.
- Annex C's `h(a)` reproduces `LinearAmplitudeFunction.post_processing(a)` to `0.0` absolute difference.

---

## Global Constraints

Every task's requirements implicitly include this section. Values are copied verbatim from the spec's Frozen Protocol Annex.

- **Isolation.** `research/paper_a/` imports nothing from `src/`, `app/`, or `ibm_validation.py`. The deployed dashboard environment is never modified.
- **Strike, rate, dividends.** `K=100`, `r=0.05`, dividends zero for all 50 benchmark rows.
- **Benchmark construction.** `m_F = S0*e^{rT}/K`, therefore `S0 = 100*m_F*e^{-0.05T}`, stored to 8 decimals, never recomputed from a rounded display value.
- **Weights.** Every benchmark row has analysis weight `1/50 = 0.02`. Weights never change after results are inspected.
- **Domain.** `S0>0`, `K>0`, `r in [0,0.10]`, zero dividends, `T in [0.25,2.00]`, `sigma in [0.15,0.30]`. Out-of-domain input raises a named error; **no clamping is permitted in the research package** (this is the opposite of `src/quantum.py:23`, which clamps `sigma` to 0.15 for the dashboard — do not copy that behaviour).
- **Named domain errors.** `NONPOSITIVE_SPOT`, `NONPOSITIVE_STRIKE`, `RATE_OUT_OF_RANGE`, `MATURITY_OUT_OF_RANGE`, `VOLATILITY_OUT_OF_RANGE`, `NONZERO_DIVIDEND_UNSUPPORTED`, `UNSUPPORTED_PAYOFF`.
- **Payoff rescaling.** `c = 0.25`, frozen for all shot-based work.
- **Support rule.** `L = min(F^-1(q_total/2), 0.98K)`, `U = max(F^-1(1-q_total/2), 1.02K)`; fixed across `n` per configuration.
- **Grid.** `x_i = L + i(U-L)/(2^n - 1)` for `i` in `0..2^n-1`; `pi_i = f(x_i)/sum_l f(x_l)`.
- **Inverse map.** `h(a) = (U-K) * (2/(pi*c)) * (a - 1/2 + pi*c/4)`. Applied exactly once; discounting applied exactly once.
- **IQAE fields.** Point estimate is raw `result.estimation`; interval is raw `result.confidence_interval` with `confint_method="beta"`, `epsilon_target=0.01`, `alpha=0.05`. `epsilon_target` is in raw objective-probability units, never dollars.
- **Never substitute** `mle`, `estimate`, `estimation_processed`, or any presentation-clipped value for the selected raw fields.
- **Negative prices are retained.** `presentation_clipped_price = max(0, price)` may be displayed but never enters error, interval, completion, or failure calculations.
- **Stream key.** `paper-a/v1 | namespace | experiment_uuid | phase | config_id | n | replicate | condition | purpose`, SHA-256, first 128 digest bits as four big-endian `uint32` seeding `SeedSequence`, generator `PCG64DXSM`. Python `hash()` is forbidden.
- **Transpiler seed.** `20260727`, fixed everywhere.
- **Deterministic tolerances (E0).** normalization residual `<=1e-12`; PMF max elementwise `<=1e-12` and L1 `<=1e-10`; `|a_calc - a_sv| <= 1e-10`; post-processing/discount/round-trip residual `<=1e-10*max(1,S0)`; signed error-identity residual `<=1e-10*max(1,S0)`.
- **Objective qubit selection.** Selected by qubit/register identity, never by hand-written integer bit shifts. (Verified: for `LinearAmplitudeFunction` with `breakpoints=[L,K]` the objective qubit sits at index `num_state_qubits`, with 3 ancillas above it at `n=3`.)
- **Frozen subsets (Annex A.1).** `C12 = {E001,E006,E009,E014,E017,E022,E025,E030,E033,E038,E042,E049}`; `C6 = {E001,E014,E025,E030,E038,E049}`; `N5 = {E001,E009,E030,E042}`. `C6 ⊂ C12`, `N5 ⊂ C12`, `C12 ⊂ E001..E050`.
- **Health stack.** test `venv/Scripts/pytest.exe`; typecheck `mypy src/ app/ tests/ research/`; lint `venv/Scripts/ruff.exe check .`. Ruff: line-length 100, rules `E,F,W,N`, with `N803`/`N806` ignored so finance notation (`S0`, `K`, `T`, `P_BS`) is legal.
- **Commit discipline.** One commit per task minimum. No `Co-Authored-By` trailer.

---

## Plan Series

This spec spans eight weeks and E0–E7. A single plan cannot cover it without placeholders, because **the E3/E4 matrices are defined by measured E2 outcomes** (shot budget, `R`, `n=5` promotion) that do not exist yet. Writing them now would mean writing "TBD from pilot" — a plan failure.

| Plan | Covers | Spec weeks | Status |
|---|---|---|---|
| **1. Foundation + E0** (this document) | package, benchmark, streams, reference ladder, recording contract, resources, E0 gate, smoke run | 1–2 | ready |
| 2. E1 + E2 pilot | deterministic scaling incl. `c` sweep, shot/replicate pilot, GO gate | 3–4 | write after Plan 1 lands |
| 3. E3 + E4 + E5/E5b | ideal study, controlled noise, resource frontier, MC context | 4–5 | write after E2 freezes its outcomes |
| 4. E6 + E7 + manuscript | Asian stress test, hardware checks, statistics, rewrite | 6–8 | write after Plan 3 lands |

Each plan produces working, testable software on its own. Plan 1's deliverable is a package that can compute and validate every deterministic price layer for all 50 contracts and pass an end-to-end smoke experiment.

---

## File Structure

```text
research/
├── __init__.py                      # namespace only
└── paper_a/
    ├── __init__.py                  # namespace only
    ├── README.md                    # how to run E0, what the gates mean
    ├── environment.py               # T1  environment lock capture
    ├── benchmark.py                 # T2,T3  Annex A table, domain, subsets, replacement pool
    ├── streams.py                   # T4  Annex D deterministic stream derivation
    ├── references.py                # T5,T6  P_BS, P_support, tail audit, support-rule selection, P_grid
    ├── payoff.py                    # T7  Annex C objective probability + inverse map
    ├── errors.py                    # T9  signed error ladder + identity
    ├── schema.py                    # T10 versioned records + append-only JSONL store
    ├── recording.py                 # T11 RecordingSampler + transpilation service (Annex I)
    ├── resources.py                 # T12 M_A_logical, M_A_executed, M_Q_executed, powers accounting
    ├── validation.py                # T13 E0 gate battery
    ├── european/
    │   ├── __init__.py
    │   └── circuits.py              # T8  state prep + payoff circuit, statevector a_sv, P_circuit
    ├── configs/
    │   └── e0.json                  # T13 immutable E0 config
    ├── scripts/
    │   ├── __init__.py
    │   ├── run_e0.py                # T13 E0 runner
    │   └── run_smoke.py             # T14 end-to-end smoke experiment
    └── tests/
        ├── __init__.py
        ├── test_environment.py
        ├── test_benchmark.py
        ├── test_streams.py
        ├── test_references.py
        ├── test_payoff.py
        ├── test_circuits.py
        ├── test_errors.py
        ├── test_schema.py
        ├── test_recording.py
        ├── test_resources.py
        └── test_smoke_pipeline.py
```

**Deviation from the spec's architecture sketch, deliberate and non-normative:** the spec's file list folds stream derivation into `config.py` and the error ladder into `references.py`. Annex D's stream derivation and the Annex C payoff algebra are each a single pure responsibility with their own dense test surface, so they get their own modules (`streams.py`, `payoff.py`, `errors.py`). The Research-Package Architecture section is not part of the normative Frozen Protocol Annex, so this needs no amendment. `config.py`, `noise.py`, `statistics.py`, `asian/`, and the remaining `scripts/` land in Plans 2–4 when they have a caller.

---

### Task 1: Package skeleton and environment lock capture

**Files:**
- Create: `research/__init__.py`, `research/paper_a/__init__.py`, `research/paper_a/european/__init__.py`, `research/paper_a/scripts/__init__.py`, `research/paper_a/tests/__init__.py`
- Create: `research/paper_a/environment.py`
- Create: `research/paper_a/tests/test_environment.py`
- Modify: `pyproject.toml` (add pytest `pythonpath` so `research.paper_a.*` imports resolve from the repo root)

**Interfaces:**
- Consumes: nothing.
- Produces: `capture_environment() -> dict` returning keys `python_version: str`, `packages: dict[str,str]`, `git_commit: str`, `platform: str`, `captured_at_utc: str`. Every later task's record schema embeds this dict under `environment`.

- [ ] **Step 1: Create the package directories with empty `__init__.py` files**

```bash
mkdir -p research/paper_a/european research/paper_a/configs research/paper_a/scripts research/paper_a/tests
touch research/__init__.py research/paper_a/__init__.py research/paper_a/european/__init__.py \
      research/paper_a/scripts/__init__.py research/paper_a/tests/__init__.py
```

- [ ] **Step 2: Add pytest path config so `research.paper_a` imports resolve**

Append to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["tests", "research/paper_a/tests"]
```

- [ ] **Step 3: Write the failing test**

`research/paper_a/tests/test_environment.py`:

```python
import re

from research.paper_a.environment import capture_environment

REQUIRED_PACKAGES = ("qiskit-terra", "qiskit-aer", "qiskit-algorithms",
                     "qiskit-finance", "numpy", "scipy")


def test_capture_returns_all_required_keys():
    env = capture_environment()
    assert set(env) == {"python_version", "packages", "git_commit",
                        "platform", "captured_at_utc"}


def test_capture_records_every_required_package():
    env = capture_environment()
    for name in REQUIRED_PACKAGES:
        assert name in env["packages"], f"{name} missing from environment lock"
        assert re.match(r"^\d+\.\d+", env["packages"][name])


def test_git_commit_is_a_full_sha():
    env = capture_environment()
    assert re.fullmatch(r"[0-9a-f]{40}", env["git_commit"])


def test_timestamp_is_utc_iso8601():
    env = capture_environment()
    assert env["captured_at_utc"].endswith("+00:00")


def test_capture_is_stable_except_for_timestamp():
    a, b = capture_environment(), capture_environment()
    a.pop("captured_at_utc")
    b.pop("captured_at_utc")
    assert a == b
```

- [ ] **Step 4: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_environment.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.environment'`

- [ ] **Step 5: Write the implementation**

`research/paper_a/environment.py`:

```python
"""Environment lock capture.

Every result record embeds the output of `capture_environment()` so a frozen
experiment directory can be reproduced without consulting the working tree.
"""
from __future__ import annotations

import datetime as _dt
import platform
import subprocess
import sys
from importlib import metadata

TRACKED_PACKAGES = (
    "qiskit-terra",
    "qiskit-aer",
    "qiskit-algorithms",
    "qiskit-finance",
    "numpy",
    "scipy",
)


def _package_versions() -> dict[str, str]:
    versions = {}
    for name in TRACKED_PACKAGES:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            versions[name] = "ABSENT"
    return versions


def _git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()


def capture_environment() -> dict:
    """Return the complete environment lock for a result record."""
    return {
        "python_version": sys.version.split()[0],
        "packages": _package_versions(),
        "git_commit": _git_commit(),
        "platform": platform.platform(),
        "captured_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_environment.py -v`
Expected: 5 passed

- [ ] **Step 7: Record the Annex B discrepancy as evidence**

Run and save the output — this is the artifact the Annex B amendment decision rests on:

```bash
venv/Scripts/python.exe -c "import json; from research.paper_a.environment import capture_environment; print(json.dumps(capture_environment(), indent=2))" > research/paper_a/ENVIRONMENT_ACTUAL.json
```

- [ ] **Step 8: Commit**

```bash
git add research/ pyproject.toml
git commit -m "Add Paper A research package skeleton and environment lock capture

Records the actual venv contents (qiskit-terra 0.46.3, numpy 2.0.2), which
contradict Annex B's historical candidate pins. Amendment decision pending."
```

**STOP.** Do not start Task 2 until the Annex B discrepancy above has a written amendment decision.

---

### Task 2: Frozen benchmark table and domain validation

**Files:**
- Create: `research/paper_a/benchmark.py`
- Create: `research/paper_a/tests/test_benchmark.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `Contract` dataclass with fields `id: str`, `S0: float`, `K: float`, `r: float`, `T: float`, `sigma: float`, `m_F: float`, `m_stratum: str`, `t_stratum: str`, `vol_stratum: str`, `weight: float`. `BENCHMARK: tuple[Contract, ...]` (50 rows, canonical order). `by_id(cid: str) -> Contract`. `DomainError(Exception)` with attribute `code: str`. `validate_domain(S0, K, r, T, sigma, dividend=0.0) -> None`.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_benchmark.py`:

```python
import math

import pytest

from research.paper_a.benchmark import (
    BENCHMARK, Contract, DomainError, by_id, validate_domain,
)


def test_benchmark_has_fifty_rows_with_unique_ids():
    assert len(BENCHMARK) == 50
    assert len({c.id for c in BENCHMARK}) == 50
    assert [c.id for c in BENCHMARK] == [f"E{i:03d}" for i in range(1, 51)]


def test_every_s0_reproduces_the_construction_rule():
    """S0 = 100 * m_F * exp(-0.05 T), stored to 8 decimals."""
    for c in BENCHMARK:
        expected = round(100.0 * c.m_F * math.exp(-0.05 * c.T), 8)
        assert c.S0 == expected, f"{c.id}: stored {c.S0}, rule gives {expected}"


def test_weights_are_equal_and_sum_to_one():
    assert all(c.weight == 0.02 for c in BENCHMARK)
    assert math.isclose(sum(c.weight for c in BENCHMARK), 1.0, abs_tol=1e-12)


def test_canonical_order_is_moneyness_then_maturity_then_volatility():
    keys = [(c.m_F, c.T, c.sigma) for c in BENCHMARK]
    assert keys == sorted(keys)


def test_grid_is_the_full_cartesian_product():
    assert sorted({c.m_F for c in BENCHMARK}) == [0.80, 0.90, 1.00, 1.10, 1.20]
    assert sorted({c.T for c in BENCHMARK}) == [0.25, 0.50, 1.00, 1.50, 2.00]
    assert sorted({c.sigma for c in BENCHMARK}) == [0.15, 0.30]


def test_fixed_parameters_are_frozen():
    assert all(c.K == 100 and c.r == 0.05 for c in BENCHMARK)


def test_by_id_round_trips():
    assert by_id("E022").sigma == 0.30
    assert by_id("E022").T == 0.25
    with pytest.raises(KeyError):
        by_id("E051")


def test_spot_check_against_frozen_annex_a_values():
    assert by_id("E001").S0 == 79.00622404
    assert by_id("E025").S0 == 95.12294245
    assert by_id("E050").S0 == 108.58049016


@pytest.mark.parametrize("kwargs,code", [
    (dict(S0=0.0), "NONPOSITIVE_SPOT"),
    (dict(S0=-1.0), "NONPOSITIVE_SPOT"),
    (dict(K=0.0), "NONPOSITIVE_STRIKE"),
    (dict(r=-0.01), "RATE_OUT_OF_RANGE"),
    (dict(r=0.11), "RATE_OUT_OF_RANGE"),
    (dict(T=0.24), "MATURITY_OUT_OF_RANGE"),
    (dict(T=2.01), "MATURITY_OUT_OF_RANGE"),
    (dict(sigma=0.1499), "VOLATILITY_OUT_OF_RANGE"),
    (dict(sigma=0.3001), "VOLATILITY_OUT_OF_RANGE"),
    (dict(dividend=0.01), "NONZERO_DIVIDEND_UNSUPPORTED"),
])
def test_out_of_domain_inputs_raise_named_errors(kwargs, code):
    base = dict(S0=100.0, K=100.0, r=0.05, T=1.0, sigma=0.20, dividend=0.0)
    base.update(kwargs)
    with pytest.raises(DomainError) as exc:
        validate_domain(**base)
    assert exc.value.code == code


def test_domain_boundaries_are_inclusive():
    for kwargs in (dict(T=0.25), dict(T=2.00), dict(sigma=0.15),
                   dict(sigma=0.30), dict(r=0.0), dict(r=0.10)):
        base = dict(S0=100.0, K=100.0, r=0.05, T=1.0, sigma=0.20)
        base.update(kwargs)
        validate_domain(**base)  # must not raise


def test_no_clamping_occurs():
    """The research package rejects low sigma; it never silently clamps
    to 0.15 the way the dashboard's src/quantum.py does."""
    with pytest.raises(DomainError):
        validate_domain(S0=100.0, K=100.0, r=0.05, T=1.0, sigma=0.10)


def test_every_benchmark_row_is_in_domain():
    for c in BENCHMARK:
        validate_domain(S0=c.S0, K=c.K, r=c.r, T=c.T, sigma=c.sigma)


def test_strata_labels_are_consistent_with_parameters():
    m_expected = {0.80: "M1", 0.90: "M2", 1.00: "M3", 1.10: "M4", 1.20: "M5"}
    t_expected = {0.25: "T1", 0.50: "T2", 1.00: "T3", 1.50: "T4", 2.00: "T5"}
    for c in BENCHMARK:
        assert c.m_stratum.startswith(m_expected[c.m_F])
        assert c.t_stratum.startswith(t_expected[c.T])
        assert c.vol_stratum.startswith("V1" if c.sigma == 0.15 else "V2")


def test_contract_is_immutable():
    with pytest.raises(Exception):
        BENCHMARK[0].S0 = 1.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_benchmark.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.benchmark'`

- [ ] **Step 3: Write the implementation**

`research/paper_a/benchmark.py`:

```python
"""Annex A: the frozen 50-contract European benchmark and supported domain.

The table is GENERATED from the construction rule and the strata grid, then
asserted against the frozen literal values in the spec by the test suite. That
direction matters: the rule is normative, the printed table is its rendering.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

K_FIXED = 100.0
R_FIXED = 0.05
WEIGHT = 0.02

MONEYNESS = ((0.80, "M1 deep OTM"), (0.90, "M2 OTM"), (1.00, "M3 ATM"),
             (1.10, "M4 ITM"), (1.20, "M5 deep ITM"))
MATURITY = ((0.25, "T1 short"), (0.50, "T2 short"), (1.00, "T3 medium"),
            (1.50, "T4 long"), (2.00, "T5 long"))
VOLATILITY = ((0.15, "V1 low"), (0.30, "V2 high"))

R_MIN_RATE, R_MAX_RATE = 0.0, 0.10
T_MIN, T_MAX = 0.25, 2.00
SIGMA_MIN, SIGMA_MAX = 0.15, 0.30


class DomainError(ValueError):
    """Raised for any input outside the supported research domain."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code


@dataclass(frozen=True)
class Contract:
    id: str
    S0: float
    K: float
    r: float
    T: float
    sigma: float
    m_F: float
    m_stratum: str
    t_stratum: str
    vol_stratum: str
    weight: float


def _build() -> tuple[Contract, ...]:
    rows = []
    idx = 1
    for m_F, m_label in MONEYNESS:
        for T, t_label in MATURITY:
            for sigma, v_label in VOLATILITY:
                S0 = round(100.0 * m_F * math.exp(-R_FIXED * T), 8)
                rows.append(Contract(
                    id=f"E{idx:03d}", S0=S0, K=K_FIXED, r=R_FIXED, T=T,
                    sigma=sigma, m_F=m_F, m_stratum=m_label,
                    t_stratum=t_label, vol_stratum=v_label, weight=WEIGHT,
                ))
                idx += 1
    return tuple(rows)


BENCHMARK: tuple[Contract, ...] = _build()
_BY_ID = {c.id: c for c in BENCHMARK}


def by_id(cid: str) -> Contract:
    return _BY_ID[cid]


def validate_domain(S0: float, K: float, r: float, T: float, sigma: float,
                    dividend: float = 0.0) -> None:
    """Reject any out-of-domain input with a named error. Never clamps."""
    if S0 <= 0:
        raise DomainError("NONPOSITIVE_SPOT", f"S0={S0}")
    if K <= 0:
        raise DomainError("NONPOSITIVE_STRIKE", f"K={K}")
    if not R_MIN_RATE <= r <= R_MAX_RATE:
        raise DomainError("RATE_OUT_OF_RANGE", f"r={r}")
    if not T_MIN <= T <= T_MAX:
        raise DomainError("MATURITY_OUT_OF_RANGE", f"T={T}")
    if not SIGMA_MIN <= sigma <= SIGMA_MAX:
        raise DomainError("VOLATILITY_OUT_OF_RANGE", f"sigma={sigma}")
    if dividend != 0.0:
        raise DomainError("NONZERO_DIVIDEND_UNSUPPORTED", f"q={dividend}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_benchmark.py -v`
Expected: all passed (the parametrized domain test contributes 10)

- [ ] **Step 5: Verify the generated table against the spec's literal Annex A rows**

This guards against the rule and the printed table drifting apart:

```bash
venv/Scripts/python.exe -c "
from research.paper_a.benchmark import BENCHMARK
for c in BENCHMARK[:3] + BENCHMARK[-2:]:
    print(c.id, c.S0, c.T, c.sigma, c.m_F)
"
```
Expected: `E001 79.00622404 0.25 0.15 0.8` … `E050 108.58049016 2.0 0.3 1.2`, matching the spec's Annex A table rows exactly.

- [ ] **Step 6: Commit**

```bash
git add research/paper_a/benchmark.py research/paper_a/tests/test_benchmark.py
git commit -m "Add frozen 50-contract benchmark table and domain validation

Table is generated from the Annex A construction rule and asserted against
the frozen literal values. Domain rejection is by named error with no
clamping, unlike the dashboard pricer."
```

---

### Task 3: Frozen subsets and the deterministic replacement pool

**Files:**
- Modify: `research/paper_a/benchmark.py`
- Modify: `research/paper_a/tests/test_benchmark.py`

**Interfaces:**
- Consumes: `Contract`, `BENCHMARK`, `by_id` from Task 2.
- Produces: `C12: tuple[str, ...]`, `C6: tuple[str, ...]`, `N5: tuple[str, ...]`, `VALIDATION_SET: tuple[Contract, ...]` (the 12 `V01`–`V12` deterministic fixtures), `replacement_id(m_stratum, t_stratum, vol_stratum) -> str`.

- [ ] **Step 1: Write the failing test**

Append to `research/paper_a/tests/test_benchmark.py`:

```python
from collections import Counter

from research.paper_a.benchmark import (
    C6, C12, N5, VALIDATION_SET, replacement_id,
)


def test_frozen_subsets_have_exactly_the_annex_a1_members():
    assert C12 == ("E001", "E006", "E009", "E014", "E017", "E022",
                   "E025", "E030", "E033", "E038", "E042", "E049")
    assert C6 == ("E001", "E014", "E025", "E030", "E038", "E049")
    assert N5 == ("E001", "E009", "E030", "E042")


def test_subsets_are_nested_inside_the_benchmark():
    ids = {c.id for c in BENCHMARK}
    assert set(C12) <= ids
    assert set(C6) <= set(C12)
    assert set(N5) <= set(C12)


def test_c12_balance_matches_the_documented_claim():
    rows = [by_id(i) for i in C12]
    assert Counter(r.m_stratum[:2] for r in rows) == {
        "M1": 3, "M2": 2, "M3": 3, "M4": 2, "M5": 2}
    assert Counter(r.vol_stratum[:2] for r in rows) == {"V1": 6, "V2": 6}
    t_counts = Counter(r.t_stratum[:2] for r in rows)
    assert set(t_counts) == {"T1", "T2", "T3", "T4", "T5"}
    assert min(t_counts.values()) >= 2


def test_c6_covers_every_moneyness_and_maturity_stratum():
    rows = [by_id(i) for i in C6]
    assert len({r.m_stratum[:2] for r in rows}) == 5
    assert len({r.t_stratum[:2] for r in rows}) == 5
    assert Counter(r.vol_stratum[:2] for r in rows) == {"V1": 3, "V2": 3}


def test_c6_contains_the_moneyness_maturity_diagonal():
    diagonal = {("M1", "T1"), ("M2", "T2"), ("M3", "T3"),
                ("M4", "T4"), ("M5", "T5")}
    present = {(by_id(i).m_stratum[:2], by_id(i).t_stratum[:2]) for i in C6}
    assert diagonal <= present


def test_n5_has_balanced_volatility_and_corner_coverage():
    rows = [by_id(i) for i in N5]
    assert Counter(r.vol_stratum[:2] for r in rows) == {"V1": 2, "V2": 2}
    assert {r.t_stratum[:2] for r in rows} == {"T1", "T5"}


def test_validation_set_is_disjoint_from_the_benchmark():
    """V01-V12 are deterministic fixtures only; they carry no stochastic
    claim and must never be mistaken for benchmark rows."""
    assert len(VALIDATION_SET) == 12
    assert {c.S0 for c in VALIDATION_SET} <= {80.0, 90.0, 100.0, 110.0, 120.0}
    assert not ({c.S0 for c in VALIDATION_SET} & {c.S0 for c in BENCHMARK})


def test_validation_set_is_in_domain():
    for c in VALIDATION_SET:
        validate_domain(S0=c.S0, K=c.K, r=c.r, T=c.T, sigma=c.sigma)


def test_replacement_pool_covers_every_broad_cell_uniquely():
    seen = set()
    for m in ("M1", "M2", "M3", "M4", "M5"):
        for t in ("S", "M", "L"):
            for v in ("V1", "V2"):
                rid = replacement_id(m, t, v)
                assert rid == f"R-{m}-{t}-{v}"
                assert rid not in seen
                seen.add(rid)
    assert len(seen) == 30
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_benchmark.py -v`
Expected: FAIL — `ImportError: cannot import name 'C6'`

- [ ] **Step 3: Write the implementation**

Append to `research/paper_a/benchmark.py`:

```python
# --- Annex A.1: frozen nested subsets -------------------------------------
# Selected before E1 from financial strata only, never from observed results.

C12: tuple[str, ...] = ("E001", "E006", "E009", "E014", "E017", "E022",
                        "E025", "E030", "E033", "E038", "E042", "E049")
C6: tuple[str, ...] = ("E001", "E014", "E025", "E030", "E038", "E049")
N5: tuple[str, ...] = ("E001", "E009", "E030", "E042")

# --- E0 deterministic validation fixtures ---------------------------------
# Disjoint from BENCHMARK by construction (round spots). Semantics and
# boundary coverage only: no stochastic claim, no replicate mean, no
# cross-n comparison ever uses these.

_VALIDATION_ROWS = (
    ("V01", 80.0, 0.25, 0.20), ("V02", 80.0, 1.00, 0.30),
    ("V03", 90.0, 0.50, 0.15), ("V04", 90.0, 2.00, 0.30),
    ("V05", 100.0, 0.25, 0.15), ("V06", 100.0, 0.50, 0.20),
    ("V07", 100.0, 1.00, 0.20), ("V08", 100.0, 2.00, 0.30),
    ("V09", 110.0, 0.25, 0.15), ("V10", 110.0, 1.00, 0.25),
    ("V11", 120.0, 0.50, 0.20), ("V12", 120.0, 2.00, 0.30),
)

VALIDATION_SET: tuple[Contract, ...] = tuple(
    Contract(id=vid, S0=S0, K=K_FIXED, r=R_FIXED, T=T, sigma=sigma,
             m_F=S0 * math.exp(R_FIXED * T) / K_FIXED,
             m_stratum="fixture", t_stratum="fixture",
             vol_stratum="fixture", weight=0.0)
    for vid, S0, T, sigma in _VALIDATION_ROWS
)


def replacement_id(m_stratum: str, t_stratum: str, vol_stratum: str) -> str:
    """Annex A replacement pool: exactly one candidate per broad cell.

    Usable only before E1 and only for a deterministic construction failure
    that correcting the implementation does not repair.
    """
    if m_stratum not in {"M1", "M2", "M3", "M4", "M5"}:
        raise ValueError(f"unknown moneyness stratum {m_stratum}")
    if t_stratum not in {"S", "M", "L"}:
        raise ValueError(f"unknown broad maturity stratum {t_stratum}")
    if vol_stratum not in {"V1", "V2"}:
        raise ValueError(f"unknown volatility stratum {vol_stratum}")
    return f"R-{m_stratum}-{t_stratum}-{vol_stratum}"
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_benchmark.py -v`
Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add research/paper_a/benchmark.py research/paper_a/tests/test_benchmark.py
git commit -m "Add frozen C12/C6/N5 subsets, validation fixtures, replacement pool

Tests assert the Annex A.1 balance claims (C12 vol 6/6, every maturity
stratum twice, C6 moneyness-maturity diagonal) and that V01-V12 are
disjoint from the benchmark."
```

---

### Task 4: Deterministic stream derivation (Annex D)

**Files:**
- Create: `research/paper_a/streams.py`
- Create: `research/paper_a/tests/test_streams.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `NAMESPACES: frozenset[str]`, `PURPOSES: frozenset[str]`, `TRANSPILER_SEED: int = 20260727`, `stream_key(...) -> str`, `seed_sequence(key: str) -> numpy.random.SeedSequence`, `generator(key: str) -> numpy.random.Generator`.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_streams.py`:

```python
import hashlib

import numpy as np
import pytest

from research.paper_a.streams import (
    NAMESPACES, PURPOSES, TRANSPILER_SEED, generator, seed_sequence,
    stream_key,
)

ARGS = dict(namespace="paper-a/main/v1", experiment_uuid="abc-123",
            phase="E3", config_id="E022", n=3, replicate=7,
            condition="ideal", purpose="shots")


def test_key_is_the_exact_literal_annex_d_format():
    assert stream_key(**ARGS) == (
        "paper-a/v1 | paper-a/main/v1 | abc-123 | E3 | E022 | 3 | 7 "
        "| ideal | shots"
    )


def test_frozen_namespaces_and_purposes():
    assert NAMESPACES == frozenset({"paper-a/pilot/v1", "paper-a/main/v1",
                                    "paper-a/mc/v1", "paper-a/asian/v1"})
    assert {"shots", "noise", "bootstrap", "audit"} <= PURPOSES


def test_unknown_namespace_or_purpose_is_rejected():
    with pytest.raises(ValueError):
        stream_key(**{**ARGS, "namespace": "paper-a/rogue/v1"})
    with pytest.raises(ValueError):
        stream_key(**{**ARGS, "purpose": "vibes"})


def test_seed_sequence_uses_first_128_digest_bits_as_four_be_uint32():
    key = stream_key(**ARGS)
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    expected = [int.from_bytes(digest[i:i + 4], "big") for i in range(0, 16, 4)]
    assert list(seed_sequence(key).entropy) == expected


def test_generator_is_pcg64dxsm_and_reproducible():
    key = stream_key(**ARGS)
    g1, g2 = generator(key), generator(key)
    assert isinstance(g1.bit_generator, np.random.PCG64DXSM)
    assert np.array_equal(g1.random(16), g2.random(16))


def test_distinct_conditions_give_independent_streams():
    ideal = generator(stream_key(**{**ARGS, "condition": "ideal"}))
    noisy = generator(stream_key(**{**ARGS, "condition": "p1e-3"}))
    assert not np.array_equal(ideal.random(16), noisy.random(16))


def test_pilot_and_main_namespaces_never_collide():
    pilot = generator(stream_key(**{**ARGS, "namespace": "paper-a/pilot/v1"}))
    main = generator(stream_key(**{**ARGS, "namespace": "paper-a/main/v1"}))
    assert not np.array_equal(pilot.random(16), main.random(16))


def test_every_field_changes_the_stream():
    base = generator(stream_key(**ARGS)).random(8)
    for field, value in [("experiment_uuid", "zzz"), ("phase", "E4"),
                         ("config_id", "E023"), ("n", 4), ("replicate", 8),
                         ("purpose", "noise")]:
        other = generator(stream_key(**{**ARGS, field: value})).random(8)
        assert not np.array_equal(base, other), f"{field} did not change stream"


def test_transpiler_seed_is_frozen():
    assert TRANSPILER_SEED == 20260727
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_streams.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.streams'`

- [ ] **Step 3: Write the implementation**

`research/paper_a/streams.py`:

```python
"""Annex D: deterministic random-stream derivation.

Python's built-in hash() is salted per process and is FORBIDDEN here. Every
stream is reproducible from its literal key string alone.
"""
from __future__ import annotations

import hashlib

import numpy as np

NAMESPACES = frozenset({
    "paper-a/pilot/v1", "paper-a/main/v1", "paper-a/mc/v1", "paper-a/asian/v1",
})
PURPOSES = frozenset({"shots", "noise", "bootstrap", "audit"})
TRANSPILER_SEED = 20260727

_PREFIX = "paper-a/v1"
_SEP = " | "


def stream_key(namespace: str, experiment_uuid: str, phase: str,
               config_id: str, n: int, replicate: int, condition: str,
               purpose: str) -> str:
    """Build the literal Annex D stream key. No whitespace normalization."""
    if namespace not in NAMESPACES:
        raise ValueError(f"unknown namespace {namespace!r}")
    if purpose not in PURPOSES:
        raise ValueError(f"unknown purpose {purpose!r}")
    return _SEP.join([_PREFIX, namespace, experiment_uuid, phase, config_id,
                      str(n), str(replicate), condition, purpose])


def seed_sequence(key: str) -> np.random.SeedSequence:
    """SHA-256 the key; use the first 128 bits as four big-endian uint32."""
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    words = [int.from_bytes(digest[i:i + 4], "big") for i in range(0, 16, 4)]
    return np.random.SeedSequence(words)


def generator(key: str) -> np.random.Generator:
    return np.random.Generator(np.random.PCG64DXSM(seed_sequence(key)))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_streams.py -v`
Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add research/paper_a/streams.py research/paper_a/tests/test_streams.py
git commit -m "Add Annex D deterministic stream derivation

SHA-256 to SeedSequence to PCG64DXSM, with the literal key format asserted
and every field proven to change the stream."
```

---

### Task 5: Continuous and support-conditioned references

**Files:**
- Create: `research/paper_a/references.py`
- Create: `research/paper_a/tests/test_references.py`

**Interfaces:**
- Consumes: `Contract` from Task 2.
- Produces: `black_scholes_call(S0, K, r, sigma, T) -> float`; `SupportAudit` dataclass with `L, U, m, omitted_mass, C_tail, normalization, P_support, support_bias`; `support_bounds(c, q_total) -> tuple[float, float]`; `support_audit(c, q_total) -> SupportAudit`; `select_support_rule(contracts, candidates) -> float`.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_references.py`:

```python
import math

import pytest

from research.paper_a.benchmark import BENCHMARK, VALIDATION_SET, by_id
from research.paper_a.references import (
    black_scholes_call, select_support_rule, support_audit, support_bounds,
)


def test_black_scholes_matches_known_atm_value():
    assert abs(black_scholes_call(100, 100, 0.05, 0.20, 1.0) - 10.4506) < 1e-3


def test_black_scholes_respects_put_call_parity():
    S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
    call = black_scholes_call(S0, K, r, sigma, T)
    put = call - S0 + K * math.exp(-r * T)
    assert abs(put - 5.5735) < 1e-3


def test_support_bounds_bracket_the_strike():
    for c in BENCHMARK:
        L, U = support_bounds(c, 1e-4)
        assert L < c.K < U
        assert L <= 0.98 * c.K
        assert U >= 1.02 * c.K


def test_support_bounds_are_fixed_across_n():
    """The rule depends on q_total only, never on the qubit count."""
    c = by_id("E025")
    assert support_bounds(c, 1e-4) == support_bounds(c, 1e-4)


def test_wider_budget_gives_narrower_support():
    c = by_id("E025")
    tight_L, tight_U = support_bounds(c, 1e-4)
    loose_L, loose_U = support_bounds(c, 1e-2)
    assert loose_L >= tight_L and loose_U <= tight_U


def test_exact_identity_p_bs_equals_m_times_p_support_plus_tail():
    """Annex A: P_BS = m * P_support + C_tail, exactly."""
    for cid in ("E001", "E025", "E050"):
        c = by_id(cid)
        a = support_audit(c, 1e-4)
        reconstructed = a.m * a.P_support + a.C_tail
        assert abs(reconstructed - black_scholes_call(
            c.S0, c.K, c.r, c.sigma, c.T)) < 1e-10 * max(1.0, c.S0)


def test_audit_stores_each_quantity_separately():
    a = support_audit(by_id("E025"), 1e-4)
    assert 0 < a.m <= 1
    assert abs(a.omitted_mass - (1 - a.m)) < 1e-15
    assert a.C_tail >= 0
    assert abs(a.normalization - 1.0 / a.m) < 1e-12


def test_selected_rule_satisfies_all_three_gates_on_all_50():
    q = select_support_rule(BENCHMARK, (1e-2, 1e-3, 1e-4, 1e-5, 1e-6))
    for c in BENCHMARK:
        a = support_audit(c, q)
        assert a.omitted_mass <= 1e-4
        assert a.C_tail <= 1e-4 * c.S0
        assert abs(a.support_bias) <= 1e-4 * c.S0


def test_selected_rule_is_the_least_wide_that_passes():
    """Least-wide means the LARGEST passing q_total, since larger q trims
    more tail. Verify nothing larger also passes."""
    candidates = (1e-2, 1e-3, 1e-4, 1e-5, 1e-6)
    q = select_support_rule(BENCHMARK, candidates)
    for bigger in [x for x in candidates if x > q]:
        failed = any(
            support_audit(c, bigger).omitted_mass > 1e-4
            or support_audit(c, bigger).C_tail > 1e-4 * c.S0
            or abs(support_audit(c, bigger).support_bias) > 1e-4 * c.S0
            for c in BENCHMARK)
        assert failed, f"q={bigger} also passes; {q} is not least-wide"


def test_rule_also_passes_on_the_validation_fixtures():
    q = select_support_rule(BENCHMARK, (1e-2, 1e-3, 1e-4, 1e-5, 1e-6))
    for c in VALIDATION_SET:
        a = support_audit(c, q)
        assert a.omitted_mass <= 1e-4


def test_no_candidate_passing_raises():
    with pytest.raises(ValueError, match="no candidate"):
        select_support_rule(BENCHMARK, (0.5,))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_references.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.references'`

- [ ] **Step 3: Write the implementation**

`research/paper_a/references.py`:

```python
"""Reference price ladder, layers 1-2: continuous and support-conditioned.

Nothing in this module touches Qiskit. These are the independent references
that circuit output is checked against.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
from scipy import integrate
from scipy.stats import lognorm, norm

from research.paper_a.benchmark import Contract


def black_scholes_call(S0: float, K: float, r: float, sigma: float,
                       T: float) -> float:
    """P_BS: continuous, untruncated Black-Scholes call price."""
    d1 = (math.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S0 * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)


def _lognormal(c: Contract):
    """Risk-neutral terminal-price distribution as a frozen scipy object."""
    mu_ln = (c.r - 0.5 * c.sigma ** 2) * c.T + math.log(c.S0)
    s_ln = c.sigma * math.sqrt(c.T)
    return lognorm(s=s_ln, scale=math.exp(mu_ln))


@dataclass(frozen=True)
class SupportAudit:
    L: float
    U: float
    m: float
    omitted_mass: float
    C_tail: float
    normalization: float
    P_support: float
    support_bias: float


def support_bounds(c: Contract, q_total: float) -> tuple[float, float]:
    """L = min(F^-1(q/2), 0.98K), U = max(F^-1(1-q/2), 1.02K)."""
    dist = _lognormal(c)
    L = min(float(dist.ppf(q_total / 2.0)), 0.98 * c.K)
    U = max(float(dist.ppf(1.0 - q_total / 2.0)), 1.02 * c.K)
    return L, U


def support_audit(c: Contract, q_total: float) -> SupportAudit:
    """Store retained mass, omitted mass, omitted payoff, and bias separately."""
    dist = _lognormal(c)
    L, U = support_bounds(c, q_total)
    D = math.exp(-c.r * c.T)
    m = float(dist.cdf(U) - dist.cdf(L))

    def payoff_density(s: float) -> float:
        return max(0.0, s - c.K) * dist.pdf(s)

    inside, _ = integrate.quad(payoff_density, L, U, limit=400)
    below, _ = integrate.quad(payoff_density, 0.0, L, limit=400)
    above, _ = integrate.quad(payoff_density, U, np.inf, limit=400)

    P_support = (D / m) * inside
    C_tail = D * (below + above)
    P_bs = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
    return SupportAudit(L=L, U=U, m=m, omitted_mass=1.0 - m, C_tail=C_tail,
                        normalization=1.0 / m, P_support=P_support,
                        support_bias=P_support - P_bs)


def select_support_rule(contracts: Iterable[Contract],
                        candidates: Sequence[float]) -> float:
    """Freeze the least-wide q_total passing all three gates on every contract.

    Least-wide support = largest q_total, so candidates are tried from
    largest to smallest and the first that passes everywhere wins.
    """
    rows = list(contracts)
    for q in sorted(candidates, reverse=True):
        if all(
            (a := support_audit(c, q)).omitted_mass <= 1e-4
            and a.C_tail <= 1e-4 * c.S0
            and abs(a.support_bias) <= 1e-4 * c.S0
            for c in rows
        ):
            return q
    raise ValueError("no candidate q_total passes all support gates")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_references.py -v`
Expected: all passed

- [ ] **Step 5: Record the selected support rule**

```bash
venv/Scripts/python.exe -c "
from research.paper_a.benchmark import BENCHMARK
from research.paper_a.references import select_support_rule, support_audit
q = select_support_rule(BENCHMARK, (1e-2,1e-3,1e-4,1e-5,1e-6))
print('selected q_total =', q)
worst = max(BENCHMARK, key=lambda c: support_audit(c,q).omitted_mass)
a = support_audit(worst,q)
print('worst omitted mass', worst.id, a.omitted_mass, 'C_tail', a.C_tail)
"
```
Note the selected value — it is frozen input for every later task.

- [ ] **Step 6: Commit**

```bash
git add research/paper_a/references.py research/paper_a/tests/test_references.py
git commit -m "Add continuous and support-conditioned reference layers

Validates the exact identity P_BS = m*P_support + C_tail and freezes the
least-wide q_total passing all three support gates on all 50 contracts."
```

---

### Task 6: Finite-grid reference

**Files:**
- Modify: `research/paper_a/references.py`
- Modify: `research/paper_a/tests/test_references.py`

**Interfaces:**
- Consumes: `Contract`, `support_bounds` from Tasks 2 and 5.
- Produces: `grid_points(L, U, n) -> numpy.ndarray`; `grid_probabilities(c, L, U, n) -> numpy.ndarray`; `p_grid(c, L, U, n) -> float`.

- [ ] **Step 1: Write the failing test**

Append to `research/paper_a/tests/test_references.py`:

```python
import numpy as np

from research.paper_a.references import grid_points, grid_probabilities, p_grid


def test_grid_is_the_frozen_linear_rule():
    pts = grid_points(10.0, 20.0, 3)
    assert len(pts) == 8
    assert pts[0] == 10.0 and pts[-1] == 20.0
    assert np.allclose(np.diff(pts), 10.0 / 7.0)


def test_grid_size_doubles_with_each_qubit():
    for n in (2, 3, 4, 5, 6):
        assert len(grid_points(50.0, 150.0, n)) == 2 ** n


def test_probabilities_are_normalized_pointwise_densities():
    c = by_id("E025")
    L, U = support_bounds(c, 1e-4)
    pi = grid_probabilities(c, L, U, 3)
    assert abs(pi.sum() - 1.0) <= 1e-12
    assert (pi > 0).all()


def test_probabilities_are_not_integrated_bin_masses():
    """Guard against silently substituting bin integrals for point densities."""
    from scipy.stats import lognorm
    import math
    c = by_id("E025")
    L, U = support_bounds(c, 1e-4)
    x = grid_points(L, U, 3)
    mu = (c.r - 0.5 * c.sigma ** 2) * c.T + math.log(c.S0)
    dist = lognorm(s=c.sigma * math.sqrt(c.T), scale=math.exp(mu))
    density = dist.pdf(x)
    assert np.allclose(grid_probabilities(c, L, U, 3),
                       density / density.sum(), atol=1e-15)


def test_p_grid_uses_the_exact_payoff_evaluated_classically():
    import math
    c = by_id("E025")
    L, U = support_bounds(c, 1e-4)
    x = grid_points(L, U, 3)
    pi = grid_probabilities(c, L, U, 3)
    expected = math.exp(-c.r * c.T) * float(
        (pi * np.maximum(0.0, x - c.K)).sum())
    assert abs(p_grid(c, L, U, 3) - expected) < 1e-14


def test_grid_error_shrinks_as_n_grows():
    c = by_id("E025")
    L, U = support_bounds(c, 1e-4)
    from research.paper_a.references import support_audit
    target = support_audit(c, 1e-4).P_support
    errs = [abs(p_grid(c, L, U, n) - target) for n in (3, 4, 5, 6)]
    assert errs[-1] < errs[0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_references.py -k grid -v`
Expected: FAIL — `ImportError: cannot import name 'grid_points'`

- [ ] **Step 3: Write the implementation**

Append to `research/paper_a/references.py`:

```python
def grid_points(L: float, U: float, n: int) -> np.ndarray:
    """x_i = L + i(U-L)/(2^n - 1), the frozen finite point grid."""
    count = 2 ** n
    return L + np.arange(count) * (U - L) / (count - 1)


def grid_probabilities(c: Contract, L: float, U: float, n: int) -> np.ndarray:
    """pi_i = f(x_i) / sum_l f(x_l): normalized POINTWISE densities.

    This matches Qiskit's LogNormalDistribution semantics. Integrated bin
    masses are a different quantity and are never substituted here.
    """
    density = _lognormal(c).pdf(grid_points(L, U, n))
    return density / density.sum()


def p_grid(c: Contract, L: float, U: float, n: int) -> float:
    """P_grid: exact expectation on the frozen grid, exact payoff, classical."""
    x = grid_points(L, U, n)
    pi = grid_probabilities(c, L, U, n)
    payoff = np.maximum(0.0, x - c.K)
    return math.exp(-c.r * c.T) * float((pi * payoff).sum())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_references.py -v`
Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add research/paper_a/references.py research/paper_a/tests/test_references.py
git commit -m "Add exact finite-grid reference layer

Point-grid rule and normalized pointwise densities, with an explicit guard
against substituting integrated bin masses."
```

---

### Task 7: Objective probability and dollar post-processing (Annex C)

**Files:**
- Create: `research/paper_a/payoff.py`
- Create: `research/paper_a/tests/test_payoff.py`

**Interfaces:**
- Consumes: nothing (pure algebra over arrays).
- Produces: `C_RESCALING: float = 0.25`; `objective_amplitudes(x, K, U, c) -> np.ndarray`; `a_calc(pi, x, K, U, c) -> float`; `h_inverse(a, K, U, c) -> float`; `to_price(a, K, U, c, r, T) -> float`; `presentation_clipped(price) -> float`.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_payoff.py`:

```python
import math

import numpy as np
import pytest

from research.paper_a.payoff import (
    C_RESCALING, a_calc, h_inverse, objective_amplitudes,
    presentation_clipped, to_price,
)

K, U, C = 100.0, 177.24074841962909, C_RESCALING


def test_rescaling_factor_is_frozen():
    assert C_RESCALING == 0.25


def test_amplitudes_follow_the_frozen_angle_formula():
    x = np.array([90.0, 100.0, 140.0, U])
    y = np.maximum(0.0, x - K) / (U - K)
    theta = (math.pi / 4) * (1 - C) + (math.pi * C / 2) * y
    assert np.allclose(objective_amplitudes(x, K, U, C), np.sin(theta) ** 2)


def test_amplitudes_stay_in_the_unit_interval():
    x = np.linspace(0.0, U, 500)
    a = objective_amplitudes(x, K, U, C)
    assert (a >= 0).all() and (a <= 1).all()


def test_y_is_bounded_by_one_at_the_upper_support():
    """max x_i is U, so y = g/(U-K) never exceeds 1."""
    assert objective_amplitudes(np.array([U]), K, U, C)[0] <= 1.0


def test_zero_payoff_region_is_the_constant_baseline():
    baseline = math.sin((math.pi / 4) * (1 - C)) ** 2
    a = objective_amplitudes(np.array([10.0, 50.0, K]), K, U, C)
    assert np.allclose(a, baseline)


def test_h_inverse_round_trips_the_linearization():
    """h is the exact inverse of the LINEARIZED map, so it round-trips y."""
    for y in (0.0, 0.25, 0.5, 1.0):
        a_lin = 0.5 + (math.pi * C / 2) * y - math.pi * C / 4
        assert abs(h_inverse(a_lin, K, U, C) - y * (U - K)) < 1e-10


def test_h_matches_qiskit_post_processing_exactly():
    from qiskit.circuit.library import LinearAmplitudeFunction
    laf = LinearAmplitudeFunction(
        3, slope=[0.0, 1.0], offset=[0.0, 0.0], domain=(55.165149432260606, U),
        image=(0.0, U - K), rescaling_factor=C,
        breakpoints=[55.165149432260606, K])
    for a in (0.2, 0.339439213658, 0.5, 0.7):
        assert abs(h_inverse(a, K, U, C) - laf.post_processing(a)) < 1e-12


def test_discount_is_applied_exactly_once():
    r, T, a = 0.05, 0.25, 0.339439213658
    assert abs(to_price(a, K, U, C, r, T)
               - math.exp(-r * T) * h_inverse(a, K, U, C)) < 1e-14


def test_negative_prices_are_retained_not_clipped():
    price = to_price(0.0, K, U, C, 0.05, 1.0)
    assert price < 0
    assert presentation_clipped(price) == 0.0
    assert price != presentation_clipped(price)


def test_a_calc_is_the_probability_weighted_mean_amplitude():
    x = np.array([80.0, 100.0, 120.0, 160.0])
    pi = np.array([0.4, 0.3, 0.2, 0.1])
    expected = float((pi * objective_amplitudes(x, K, U, C)).sum())
    assert abs(a_calc(pi, x, K, U, C) - expected) < 1e-15


def test_smaller_c_shrinks_the_amplitude_span():
    """The E1 c-sweep tradeoff: smaller c means a more accurate
    linearization but a smaller signal to estimate."""
    x = np.linspace(K, U, 64)
    spans = [np.ptp(objective_amplitudes(x, K, U, cc))
             for cc in (0.05, 0.25, 0.5)]
    assert spans[0] < spans[1] < spans[2]


@pytest.mark.parametrize("bad_c", [0.0, -0.1])
def test_nonpositive_rescaling_is_rejected(bad_c):
    with pytest.raises(ValueError):
        h_inverse(0.5, K, U, bad_c)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_payoff.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.payoff'`

- [ ] **Step 3: Write the implementation**

`research/paper_a/payoff.py`:

```python
"""Annex C: objective probability and dollar post-processing.

h() is the exact inverse of the LINEARIZED sin^2 map, matching Qiskit's
LinearAmplitudeFunction.post_processing. The gap between the true sin^2 and
its linearization is precisely the encoding error e_encode, and it is a
direct function of the rescaling factor c.
"""
from __future__ import annotations

import math

import numpy as np

C_RESCALING = 0.25


def _check_c(c: float) -> None:
    if c <= 0:
        raise ValueError(f"rescaling factor must be positive, got {c}")


def objective_amplitudes(x: np.ndarray, K: float, U: float,
                         c: float) -> np.ndarray:
    """a_i = sin^2(theta_i) with theta_i = (pi/4)(1-c) + (pi c/2) y_i."""
    _check_c(c)
    y = np.maximum(0.0, x - K) / (U - K)
    theta = (math.pi / 4.0) * (1.0 - c) + (math.pi * c / 2.0) * y
    return np.sin(theta) ** 2


def a_calc(pi: np.ndarray, x: np.ndarray, K: float, U: float,
           c: float) -> float:
    """Independently calculated objective probability sum_i pi_i a_i."""
    return float((pi * objective_amplitudes(x, K, U, c)).sum())


def h_inverse(a: float, K: float, U: float, c: float) -> float:
    """h(a) = (U-K)(2/pi c)(a - 1/2 + pi c/4). Applied exactly once."""
    _check_c(c)
    return (U - K) * (2.0 / (math.pi * c)) * (a - 0.5 + math.pi * c / 4.0)


def to_price(a: float, K: float, U: float, c: float, r: float,
             T: float) -> float:
    """Discounted dollar price. Discount applied exactly once."""
    return math.exp(-r * T) * h_inverse(a, K, U, c)


def presentation_clipped(price: float) -> float:
    """Display-only. Never used for error, interval, or failure accounting."""
    return max(0.0, price)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_payoff.py -v`
Expected: all passed, including the exact match against Qiskit's `post_processing`

- [ ] **Step 5: Commit**

```bash
git add research/paper_a/payoff.py research/paper_a/tests/test_payoff.py
git commit -m "Add Annex C objective probability and dollar post-processing

h() is asserted equal to Qiskit's LinearAmplitudeFunction.post_processing.
Negative prices are retained; clipping is display-only."
```

---

### Task 8: European circuit and exact statevector reference

**Files:**
- Create: `research/paper_a/european/circuits.py`
- Create: `research/paper_a/tests/test_circuits.py`

**Interfaces:**
- Consumes: `Contract`; `support_bounds`, `grid_points`, `grid_probabilities`; `objective_amplitudes`, `a_calc`, `to_price`.
- Produces: `EuropeanCircuit` dataclass with `circuit: QuantumCircuit`, `objective_qubit: int`, `L: float`, `U: float`, `n: int`; `build_european(c, L, U, n, rescaling) -> EuropeanCircuit`; `statevector_amplitude(ec) -> float`; `p_circuit(c, ec, rescaling) -> float`.

**Verified construction facts** (checked against qiskit-terra 0.46.3 in this venv):
- `LinearAmplitudeFunction(n, slope=[0.0, 1.0], offset=[0.0, 0.0], domain=(L,U), image=(0.0,U-K), rescaling_factor=c, breakpoints=[L,K])` is the correct European call objective. `slope` and `image` must share units — `slope=1.0` with `image=(0, U-K)`. Using `slope=1/(U-K)` with the same image silently produces a wrong `a_sv`.
- At `n=3` this yields `num_qubits=7`: 3 state qubits, the objective at index `num_state_qubits`, and 3 ancillas above it.
- `LogNormalDistribution(n, mu=mu_ln, sigma=s_ln**2, bounds=(L,U))` — note `sigma` is the **variance** of the log, not the standard deviation.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_circuits.py`:

```python
import math

import numpy as np
import pytest

from research.paper_a.benchmark import BENCHMARK, by_id
from research.paper_a.european.circuits import (
    build_european, p_circuit, statevector_amplitude,
)
from research.paper_a.payoff import C_RESCALING, a_calc
from research.paper_a.references import (
    grid_points, grid_probabilities, p_grid, support_bounds,
)

Q_TOTAL = 1e-4


def _setup(cid, n):
    c = by_id(cid)
    L, U = support_bounds(c, Q_TOTAL)
    return c, L, U, build_european(c, L, U, n, C_RESCALING)


def test_objective_qubit_is_located_by_identity_not_bit_shifts():
    _, _, _, ec = _setup("E025", 3)
    assert ec.objective_qubit == 3
    assert ec.circuit.num_qubits == 7


def test_circuit_pmf_matches_independently_calculated_probabilities():
    """Max elementwise <= 1e-12 and L1 <= 1e-10 (E0 gate)."""
    c, L, U, ec = _setup("E025", 3)
    from qiskit.quantum_info import Statevector
    probs = Statevector(ec.circuit).probabilities(range(ec.n))
    pi = grid_probabilities(c, L, U, ec.n)
    assert np.abs(probs - pi).max() <= 1e-12
    assert np.abs(probs - pi).sum() <= 1e-10


def test_calculated_and_statevector_objective_probabilities_agree():
    """|a_calc - a_sv| <= 1e-10 (E0 gate). This is the check that catches
    slope/image unit errors in the amplitude function."""
    for cid in ("E001", "E022", "E025", "E042", "E050"):
        c, L, U, ec = _setup(cid, 3)
        expected = a_calc(grid_probabilities(c, L, U, 3),
                          grid_points(L, U, 3), c.K, U, C_RESCALING)
        assert abs(statevector_amplitude(ec) - expected) <= 1e-10, cid


def test_agreement_holds_across_all_qubit_counts():
    c, L, U = by_id("E025"), None, None
    L, U = support_bounds(c, Q_TOTAL)
    for n in (2, 3, 4, 5):
        ec = build_european(c, L, U, n, C_RESCALING)
        expected = a_calc(grid_probabilities(c, L, U, n),
                          grid_points(L, U, n), c.K, U, C_RESCALING)
        assert abs(statevector_amplitude(ec) - expected) <= 1e-10, n


def test_p_circuit_differs_from_p_grid_only_by_encoding_error():
    c, L, U, ec = _setup("E022", 3)
    encode_error = p_circuit(c, ec, C_RESCALING) - p_grid(c, L, U, 3)
    assert abs(encode_error) > 1e-6, "encoding error should be measurable"
    assert abs(encode_error) < 10.0, "encoding error should be bounded"


def test_encoding_error_shrinks_as_rescaling_shrinks():
    """The E1 c-sweep premise: smaller c means a better linearization."""
    c, L, U = by_id("E022"), *support_bounds(by_id("E022"), Q_TOTAL)
    grid = p_grid(c, L, U, 3)
    errs = []
    for cc in (0.5, 0.25, 0.05):
        ec = build_european(c, L, U, 3, cc)
        errs.append(abs(p_circuit(c, ec, cc) - grid))
    assert errs[0] > errs[1] > errs[2]


@pytest.mark.slow
def test_every_benchmark_contract_builds_and_agrees_at_n3():
    for c in BENCHMARK:
        L, U = support_bounds(c, Q_TOTAL)
        ec = build_european(c, L, U, 3, C_RESCALING)
        expected = a_calc(grid_probabilities(c, L, U, 3),
                          grid_points(L, U, 3), c.K, U, C_RESCALING)
        assert abs(statevector_amplitude(ec) - expected) <= 1e-10, c.id
```

- [ ] **Step 2: Register the `slow` marker**

Append to `pyproject.toml` under `[tool.pytest.ini_options]`:

```toml
markers = ["slow: full-benchmark sweeps, excluded from the fast loop"]
```

- [ ] **Step 3: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_circuits.py -v -m "not slow"`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.european.circuits'`

- [ ] **Step 4: Write the implementation**

`research/paper_a/european/circuits.py`:

```python
"""Exact ideal-statevector circuit layer.

The objective qubit is located from the amplitude function's own register
layout, never by a hand-written bit shift, per the E0 gate.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from qiskit import QuantumCircuit
from qiskit.circuit.library import LinearAmplitudeFunction
from qiskit.quantum_info import Statevector
from qiskit_finance.circuit.library import LogNormalDistribution

from research.paper_a.benchmark import Contract
from research.paper_a.payoff import h_inverse


@dataclass(frozen=True)
class EuropeanCircuit:
    circuit: QuantumCircuit
    objective_qubit: int
    L: float
    U: float
    n: int


def build_european(c: Contract, L: float, U: float, n: int,
                   rescaling: float) -> EuropeanCircuit:
    """State preparation composed with the linear payoff objective.

    LogNormalDistribution takes the log-VARIANCE as `sigma`.
    LinearAmplitudeFunction's `slope` and `image` must share units: the
    payoff is f(x) = x - K on [K, U], so slope is 1.0 and image is (0, U-K).
    """
    mu_ln = (c.r - 0.5 * c.sigma ** 2) * c.T + math.log(c.S0)
    s_ln = c.sigma * math.sqrt(c.T)

    distribution = LogNormalDistribution(
        n, mu=mu_ln, sigma=s_ln ** 2, bounds=(L, U))
    objective = LinearAmplitudeFunction(
        n,
        slope=[0.0, 1.0],
        offset=[0.0, 0.0],
        domain=(L, U),
        image=(0.0, U - c.K),
        rescaling_factor=rescaling,
        breakpoints=[L, c.K],
    )

    circuit = QuantumCircuit(objective.num_qubits)
    circuit.append(distribution.to_gate(), range(n))
    circuit.append(objective.to_gate(), range(objective.num_qubits))
    return EuropeanCircuit(circuit=circuit, objective_qubit=n, L=L, U=U, n=n)


def statevector_amplitude(ec: EuropeanCircuit) -> float:
    """a_sv: marginal probability that the named objective qubit reads 1."""
    marginal = Statevector(ec.circuit).probabilities([ec.objective_qubit])
    return float(marginal[1])


def p_circuit(c: Contract, ec: EuropeanCircuit, rescaling: float) -> float:
    """P_circuit = e^{-rT} h(a_sv)."""
    return math.exp(-c.r * c.T) * h_inverse(
        statevector_amplitude(ec), c.K, ec.U, rescaling)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_circuits.py -v -m "not slow"`
Expected: all passed

- [ ] **Step 6: Run the full-benchmark sweep**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_circuits.py -v -m slow`
Expected: PASS. If any contract fails the `1e-10` gate, **stop** — that is an E0 gate failure and blocks all stochastic work.

- [ ] **Step 7: Commit**

```bash
git add research/paper_a/european/circuits.py research/paper_a/tests/test_circuits.py pyproject.toml
git commit -m "Add European circuit construction and exact statevector reference

Objective qubit is located by register identity. a_calc vs a_sv agreement
is asserted to 1e-10 across n=2..5 and all 50 contracts."
```

---

### Task 9: Signed error ladder and identity

**Files:**
- Create: `research/paper_a/errors.py`
- Create: `research/paper_a/tests/test_errors.py`

**Interfaces:**
- Consumes: all reference layers from Tasks 5–8.
- Produces: `ErrorLadder` dataclass with `P_BS, P_support, P_grid, P_circuit, e_support, e_grid, e_encode`; `deterministic_ladder(c, q_total, n, rescaling) -> ErrorLadder`; `total_mean_error(ladder, e_est_mean, delta_noise) -> float`; `identity_residual(ladder, e_est_mean, delta_noise, e_total_mean) -> float`.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_errors.py`:

```python
import pytest

from research.paper_a.benchmark import BENCHMARK, by_id
from research.paper_a.errors import (
    deterministic_ladder, identity_residual, total_mean_error,
)
from research.paper_a.payoff import C_RESCALING

# The value selected over the full benchmark; 1e-4 breaches the support gate.
Q = 1e-5


def test_ladder_layers_are_stored_separately():
    lad = deterministic_ladder(by_id("E022"), Q, 3, C_RESCALING)
    values = [lad.P_BS, lad.P_support, lad.P_grid, lad.P_circuit]
    assert len(set(values)) == 4, "layers must not collapse onto each other"


def test_signed_components_telescope_to_p_circuit_minus_p_bs():
    for cid in ("E001", "E022", "E025", "E050"):
        lad = deterministic_ladder(by_id(cid), Q, 3, C_RESCALING)
        total = lad.e_support + lad.e_grid + lad.e_encode
        assert abs(total - (lad.P_circuit - lad.P_BS)) <= 1e-10 * max(
            1.0, by_id(cid).S0)


def test_each_component_is_the_difference_of_its_own_two_layers():
    lad = deterministic_ladder(by_id("E025"), Q, 3, C_RESCALING)
    assert abs(lad.e_support - (lad.P_support - lad.P_BS)) < 1e-14
    assert abs(lad.e_grid - (lad.P_grid - lad.P_support)) < 1e-14
    assert abs(lad.e_encode - (lad.P_circuit - lad.P_grid)) < 1e-14


def test_full_identity_residual_is_within_the_frozen_tolerance():
    c = by_id("E025")
    lad = deterministic_ladder(c, Q, 3, C_RESCALING)
    e_est, d_noise = 0.031, -0.017
    e_total = total_mean_error(lad, e_est, d_noise)
    residual = identity_residual(lad, e_est, d_noise, e_total)
    assert abs(residual) <= 1e-10 * max(1.0, c.S0)


def test_identity_detects_a_corrupted_total():
    c = by_id("E025")
    lad = deterministic_ladder(c, Q, 3, C_RESCALING)
    bad = total_mean_error(lad, 0.031, -0.017) + 0.5
    assert abs(identity_residual(lad, 0.031, -0.017, bad)) > 1e-10 * c.S0


def test_signs_are_preserved_so_cancellation_stays_visible():
    """Components must be able to cancel. If any contract has mixed-sign
    components, stacking absolute magnitudes must give a different answer
    from the signed sum -- that difference IS the cancellation the paper
    reports, and it is destroyed if signs are dropped anywhere."""
    found_mixed = False
    for c in BENCHMARK:
        lad = deterministic_ladder(c, Q, 3, C_RESCALING)
        parts = (lad.e_support, lad.e_grid, lad.e_encode)
        if len({p > 0 for p in parts}) > 1:
            found_mixed = True
            assert abs(sum(parts) - sum(abs(p) for p in parts)) > 1e-9, c.id
    assert found_mixed, "no mixed-sign contract found; cancellation untested"


def test_support_error_is_small_under_the_frozen_rule():
    for cid in ("E001", "E025", "E050"):
        c = by_id(cid)
        lad = deterministic_ladder(c, Q, 3, C_RESCALING)
        assert abs(lad.e_support) <= 1e-4 * c.S0


@pytest.mark.slow
def test_identity_holds_for_every_contract_and_qubit_count():
    for c in BENCHMARK:
        for n in (3, 4):
            lad = deterministic_ladder(c, Q, n, C_RESCALING)
            total = lad.e_support + lad.e_grid + lad.e_encode
            assert abs(total - (lad.P_circuit - lad.P_BS)) <= 1e-10 * max(
                1.0, c.S0), f"{c.id} n={n}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_errors.py -v -m "not slow"`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.errors'`

- [ ] **Step 3: Write the implementation**

`research/paper_a/errors.py`:

```python
"""Signed deterministic error ladder.

The five-term decomposition telescopes by construction, so the identity
check is a float-arithmetic guard on the bookkeeping, not evidence about
the physics. Report it as such.
"""
from __future__ import annotations

from dataclasses import dataclass

from research.paper_a.benchmark import Contract
from research.paper_a.european.circuits import build_european, p_circuit
from research.paper_a.references import (
    black_scholes_call, p_grid, support_audit,
)


@dataclass(frozen=True)
class ErrorLadder:
    P_BS: float
    P_support: float
    P_grid: float
    P_circuit: float
    e_support: float
    e_grid: float
    e_encode: float


def deterministic_ladder(c: Contract, q_total: float, n: int,
                         rescaling: float) -> ErrorLadder:
    audit = support_audit(c, q_total)
    bs = black_scholes_call(c.S0, c.K, c.r, c.sigma, c.T)
    grid = p_grid(c, audit.L, audit.U, n)
    ec = build_european(c, audit.L, audit.U, n, rescaling)
    circuit = p_circuit(c, ec, rescaling)
    return ErrorLadder(
        P_BS=bs, P_support=audit.P_support, P_grid=grid, P_circuit=circuit,
        e_support=audit.P_support - bs,
        e_grid=grid - audit.P_support,
        e_encode=circuit - grid,
    )


def total_mean_error(ladder: ErrorLadder, e_est_mean: float,
                     delta_noise: float) -> float:
    """e_total_mean = e_support + e_grid + e_encode + e_est_mean + Delta_noise."""
    return (ladder.e_support + ladder.e_grid + ladder.e_encode
            + e_est_mean + delta_noise)


def identity_residual(ladder: ErrorLadder, e_est_mean: float,
                      delta_noise: float, e_total_mean: float) -> float:
    return total_mean_error(ladder, e_est_mean, delta_noise) - e_total_mean
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_errors.py -v`
Expected: all passed (including the slow sweep)

- [ ] **Step 5: Commit**

```bash
git add research/paper_a/errors.py research/paper_a/tests/test_errors.py
git commit -m "Add signed deterministic error ladder and identity check

Layers are asserted distinct and signs preserved so cancellation stays
visible as a result rather than being hidden by absolute values."
```

---

### Task 10: Versioned records and append-only store

**Files:**
- Create: `research/paper_a/schema.py`
- Create: `research/paper_a/tests/test_schema.py`

**Interfaces:**
- Consumes: `capture_environment` from Task 1.
- Produces: `SCHEMA_VERSION: str`; `RunRecord` dataclass; `validate_record(record: dict) -> list[str]` returning violation strings; `append_record(path, record) -> None`; `read_records(path) -> list[dict]`; `idempotency_key(...) -> str`.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_schema.py`:

```python
import json

import pytest

from research.paper_a.schema import (
    SCHEMA_VERSION, append_record, idempotency_key, read_records,
    validate_record,
)


def _record(**overrides):
    base = {
        "schema_version": SCHEMA_VERSION,
        "experiment_uuid": "u1", "phase": "E0", "config_id": "E025",
        "n": 3, "replicate": 0, "condition": "ideal",
        "attempt_kind": "first_planned",
        "raw_estimation": 0.34, "raw_confidence_interval": [0.33, 0.35],
        "raw_price": 6.95, "presentation_clipped_price": 6.95,
        "completion_state": "complete", "environment": {"python_version": "3.9.13"},
        "actual_circuit_depth": 120, "reconstructed_circuit_depth": None,
    }
    base.update(overrides)
    return base


def test_valid_record_has_no_violations():
    assert validate_record(_record()) == []


def test_missing_required_field_is_reported():
    r = _record()
    del r["raw_estimation"]
    assert any("raw_estimation" in v for v in validate_record(r))


def test_estimate_outside_unit_interval_is_invalid():
    assert validate_record(_record(raw_estimation=1.2))
    assert validate_record(_record(raw_estimation=-0.01))


def test_unordered_or_out_of_range_interval_is_invalid():
    assert validate_record(_record(raw_confidence_interval=[0.4, 0.3]))
    assert validate_record(_record(raw_confidence_interval=[-0.1, 0.3]))
    assert validate_record(_record(raw_confidence_interval=[0.3, 1.4]))


def test_mixed_actual_and_reconstructed_provenance_is_invalid():
    """Annex I: no mixed actual/reconstructed record may pass validation."""
    r = _record(actual_circuit_depth=120, reconstructed_circuit_depth=118)
    assert any("provenance" in v.lower() for v in validate_record(r))


def test_reconstructed_only_record_is_valid():
    r = _record(actual_circuit_depth=None, reconstructed_circuit_depth=118)
    assert validate_record(r) == []


def test_negative_price_is_retained_and_valid():
    r = _record(raw_price=-0.4, presentation_clipped_price=0.0)
    assert validate_record(r) == []


def test_clipped_price_must_equal_max_zero_price():
    assert validate_record(_record(raw_price=-0.4,
                                   presentation_clipped_price=-0.4))


def test_append_is_append_only_and_readable(tmp_path):
    path = tmp_path / "raw.jsonl"
    append_record(path, _record(replicate=0))
    append_record(path, _record(replicate=1))
    records = read_records(path)
    assert [r["replicate"] for r in records] == [0, 1]
    assert len(path.read_text().strip().splitlines()) == 2


def test_append_never_rewrites_earlier_lines(tmp_path):
    path = tmp_path / "raw.jsonl"
    append_record(path, _record(replicate=0))
    first = path.read_text()
    append_record(path, _record(replicate=1))
    assert path.read_text().startswith(first)


def test_records_are_json_serializable(tmp_path):
    path = tmp_path / "raw.jsonl"
    append_record(path, _record())
    for line in path.read_text().strip().splitlines():
        json.loads(line)


def test_idempotency_key_is_stable_and_discriminating():
    args = dict(experiment_uuid="u1", phase="E3", config_id="E022", n=3,
                replicate=4, condition="ideal", purpose="shots")
    assert idempotency_key(**args) == idempotency_key(**args)
    assert idempotency_key(**args) != idempotency_key(**{**args, "replicate": 5})


def test_schema_version_is_present_and_checked():
    assert any("schema_version" in v
               for v in validate_record(_record(schema_version="v0-bogus")))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_schema.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.schema'`

- [ ] **Step 3: Write the implementation**

`research/paper_a/schema.py`:

```python
"""Versioned result records and the append-only JSONL store.

Retries never overwrite a first planned attempt, and reconstructed circuit
fields never populate actual_* fields (Annex I).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "paper-a-record-v1"

REQUIRED_FIELDS = (
    "schema_version", "experiment_uuid", "phase", "config_id", "n",
    "replicate", "condition", "attempt_kind", "raw_estimation",
    "raw_confidence_interval", "raw_price", "presentation_clipped_price",
    "completion_state", "environment",
)

_ACTUAL_PREFIXES = ("actual_circuit_", "actual_isa_", "actual_gate_")
_RECONSTRUCTED_PREFIXES = ("reconstructed_logical_", "reconstructed_isa_",
                           "reconstructed_resource_", "reconstructed_circuit_")


def _populated(record: dict, prefixes: tuple[str, ...]) -> bool:
    return any(record.get(k) is not None
               for k in record
               if k.startswith(prefixes))


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return a list of violations; empty means the record is valid."""
    violations: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in record:
            violations.append(f"missing required field {field}")
    if violations:
        return violations

    if record["schema_version"] != SCHEMA_VERSION:
        violations.append(
            f"schema_version {record['schema_version']} != {SCHEMA_VERSION}")

    est = record["raw_estimation"]
    if est is not None and not 0.0 <= est <= 1.0:
        violations.append(f"raw_estimation {est} outside [0,1]")

    ci = record["raw_confidence_interval"]
    if ci is not None:
        lo, hi = ci
        if not (0.0 <= lo <= hi <= 1.0):
            violations.append(f"invalid interval {ci}")

    price, clipped = record["raw_price"], record["presentation_clipped_price"]
    if price is not None and clipped != max(0.0, price):
        violations.append(
            f"presentation_clipped_price {clipped} != max(0, {price})")

    if _populated(record, _ACTUAL_PREFIXES) and _populated(
            record, _RECONSTRUCTED_PREFIXES):
        violations.append(
            "mixed provenance: actual_* and reconstructed_* both populated")

    return violations


def append_record(path: Path, record: dict[str, Any]) -> None:
    """Durably append one record. Never rewrites earlier lines."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
        handle.flush()


def read_records(path: Path) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8").strip()
    return [json.loads(line) for line in text.splitlines()] if text else []


def idempotency_key(experiment_uuid: str, phase: str, config_id: str, n: int,
                    replicate: int, condition: str, purpose: str) -> str:
    return "/".join([experiment_uuid, phase, config_id, str(n),
                     str(replicate), condition, purpose])
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_schema.py -v`
Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add research/paper_a/schema.py research/paper_a/tests/test_schema.py
git commit -m "Add versioned run records and append-only JSONL store

Enforces raw-field ranges, the clipped-price relationship, and the Annex I
prohibition on mixed actual/reconstructed provenance."
```

---

### Task 11: RecordingSampler and transpilation service (Annex I)

**Files:**
- Create: `research/paper_a/recording.py`
- Create: `research/paper_a/tests/test_recording.py`

**Interfaces:**
- Consumes: `TRANSPILER_SEED` from Task 4.
- Produces: `Invocation` dataclass with `ordinal, requested_shots, effective_shots, logical_qpy_sha256, isa_qpy_sha256, isa_depth, isa_ops, status, exception`; `RecordingSampler(inner, shots)` exposing `.run(circuits)` and `.invocations: list[Invocation]`; `transpile_frozen(circuit) -> tuple[QuantumCircuit, str]`.

**Verified IQAE call pattern** (read from `qiskit_algorithms.amplitude_estimators.iae` in this venv):
- IQAE calls `self._sampler.run([circuit])` with **no** shot argument — shots come from the sampler instance's own options.
- It reads effective shots via `ret.metadata[0].get("shots")`, exactly as Annex I requires.
- `powers` is initialized to `[0]` **before** the loop and then appended per iteration, confirming the leading sentinel is not an executed round.
- Repeated `k` values produce separate `.run()` calls, so each stays a distinct invocation.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_recording.py`:

```python
import pytest
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler

from research.paper_a.recording import RecordingSampler, transpile_frozen
from research.paper_a.streams import TRANSPILER_SEED

FROZEN_BASIS = ["rz", "sx", "x", "cx", "measure"]


def _bell_with_measure():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def test_transpilation_targets_only_the_frozen_basis():
    isa, _ = transpile_frozen(_bell_with_measure())
    assert set(isa.count_ops()) <= set(FROZEN_BASIS)


def test_transpilation_is_deterministic_under_the_frozen_seed():
    a, hash_a = transpile_frozen(_bell_with_measure())
    b, hash_b = transpile_frozen(_bell_with_measure())
    assert hash_a == hash_b
    assert a.count_ops() == b.count_ops()


def test_transpiled_hash_changes_with_the_circuit():
    _, h1 = transpile_frozen(_bell_with_measure())
    other = _bell_with_measure()
    other.x(0)
    _, h2 = transpile_frozen(other)
    assert h1 != h2


def test_sampler_records_one_invocation_per_run_call():
    sampler = RecordingSampler(Sampler(), shots=512)
    sampler.run([_bell_with_measure()]).result()
    sampler.run([_bell_with_measure()]).result()
    assert [i.ordinal for i in sampler.invocations] == [0, 1]


def test_repeated_identical_circuits_stay_distinct_invocations():
    sampler = RecordingSampler(Sampler(), shots=512)
    for _ in range(3):
        sampler.run([_bell_with_measure()]).result()
    assert len(sampler.invocations) == 3
    assert len({i.ordinal for i in sampler.invocations}) == 3


def test_effective_shots_come_from_result_metadata_not_the_default():
    sampler = RecordingSampler(Sampler(), shots=2048)
    sampler.run([_bell_with_measure()]).result()
    inv = sampler.invocations[0]
    assert inv.requested_shots == 2048
    assert inv.effective_shots == 2048
    assert isinstance(inv.effective_shots, int) and inv.effective_shots > 0


def test_logical_and_isa_hashes_are_both_recorded_before_execution():
    sampler = RecordingSampler(Sampler(), shots=512)
    sampler.run([_bell_with_measure()]).result()
    inv = sampler.invocations[0]
    assert len(inv.logical_qpy_sha256) == 64
    assert len(inv.isa_qpy_sha256) == 64
    assert inv.isa_depth > 0
    assert set(inv.isa_ops) <= set(FROZEN_BASIS)


def test_partial_resources_survive_an_exception():
    """Annex I: on failure, completed records and the failing invocation's
    available resources remain durable."""
    class Exploding:
        def run(self, circuits, **kwargs):
            raise RuntimeError("simulated backend failure")

    sampler = RecordingSampler(Exploding(), shots=512)
    with pytest.raises(RuntimeError):
        sampler.run([_bell_with_measure()])
    assert len(sampler.invocations) == 1
    inv = sampler.invocations[0]
    assert inv.status == "failed"
    assert "simulated backend failure" in inv.exception
    assert inv.isa_depth > 0, "pre-execution resources must be retained"
    assert inv.effective_shots is None


def test_seed_is_the_frozen_value():
    assert TRANSPILER_SEED == 20260727
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_recording.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.recording'`

- [ ] **Step 3: Write the implementation**

`research/paper_a/recording.py`:

```python
"""Annex I: ordered append-only sampler recording and frozen transpilation.

Every primitive call is recorded BEFORE execution so that an exception still
leaves the invocation's logical and ISA resources durable.
"""
from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from typing import Any, Optional

from qiskit import QuantumCircuit, qpy, transpile

from research.paper_a.streams import TRANSPILER_SEED

FROZEN_BASIS = ["rz", "sx", "x", "cx", "measure"]
OPTIMIZATION_LEVEL = 1


def _qpy_sha256(circuit: QuantumCircuit) -> str:
    buffer = io.BytesIO()
    qpy.dump(circuit, buffer)
    return hashlib.sha256(buffer.getvalue()).hexdigest()


def transpile_frozen(circuit: QuantumCircuit) -> tuple[QuantumCircuit, str]:
    """Transpile once against the frozen controlled-simulator target."""
    isa = transpile(
        circuit,
        basis_gates=FROZEN_BASIS,
        coupling_map=None,           # all-to-all
        optimization_level=OPTIMIZATION_LEVEL,
        seed_transpiler=TRANSPILER_SEED,
    )
    return isa, _qpy_sha256(isa)


@dataclass
class Invocation:
    ordinal: int
    requested_shots: int
    logical_qpy_sha256: str
    isa_qpy_sha256: str
    isa_depth: int
    isa_ops: dict
    effective_shots: Optional[int] = None
    status: str = "planned"
    exception: Optional[str] = None


class RecordingSampler:
    """Wraps a sampler primitive, recording every invocation in order.

    IQAE calls `.run([circuit])` with no shot argument, so shots are fixed on
    this instance and echoed into the recorded invocation.
    """

    def __init__(self, inner: Any, shots: int) -> None:
        self._inner = inner
        self._shots = shots
        self.invocations: list[Invocation] = []

    def run(self, circuits, **kwargs):
        circuit = circuits[0]
        isa, isa_hash = transpile_frozen(circuit)
        record = Invocation(
            ordinal=len(self.invocations),
            requested_shots=self._shots,
            logical_qpy_sha256=_qpy_sha256(circuit),
            isa_qpy_sha256=isa_hash,
            isa_depth=isa.depth(),
            isa_ops=dict(isa.count_ops()),
            status="running",
        )
        self.invocations.append(record)   # durable BEFORE execution

        try:
            job = self._inner.run([isa], shots=self._shots, **kwargs)
            result = job.result()
        except Exception as exc:
            record.status = "failed"
            record.exception = f"{type(exc).__name__}: {exc}"
            raise

        record.effective_shots = int(result.metadata[0].get("shots",
                                                            self._shots))
        record.status = "complete"
        return job
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_recording.py -v`
Expected: all passed

- [ ] **Step 5: Prove the contract against a real IQAE run**

This is the Week-2 exit gate — either actual capture works, or the study is
restricted to `reconstructed-only-v1` terminology:

```bash
venv/Scripts/python.exe -c "
from qiskit.primitives import Sampler
from qiskit_algorithms import EstimationProblem, IterativeAmplitudeEstimation
from research.paper_a.benchmark import by_id
from research.paper_a.european.circuits import build_european
from research.paper_a.payoff import C_RESCALING
from research.paper_a.recording import RecordingSampler
from research.paper_a.references import support_bounds

c = by_id('E025'); L,U = support_bounds(c,1e-4)
ec = build_european(c,L,U,3,C_RESCALING)
rec = RecordingSampler(Sampler(), shots=512)
iqae = IterativeAmplitudeEstimation(epsilon_target=0.05, alpha=0.05,
                                    confint_method='beta', sampler=rec)
res = iqae.estimate(EstimationProblem(state_preparation=ec.circuit,
                                      objective_qubits=[ec.objective_qubit]))
print('powers        :', res.powers)
print('invocations   :', len(rec.invocations))
print('effective shots:', [i.effective_shots for i in rec.invocations])
print('estimation    :', res.estimation)
" 2>&1 | grep -v -i warning
```
Expected: `len(rec.invocations)` equals `len(res.powers) - 1` (the leading `0` is the sentinel, not an executed round). If invocation count and powers disagree, **stop and record the discrepancy** — it determines Predeclared Pilot Outcome #2.

- [ ] **Step 6: Commit**

```bash
git add research/paper_a/recording.py research/paper_a/tests/test_recording.py
git commit -m "Add Annex I recording sampler and frozen transpilation service

Invocations are recorded before execution so partial resources survive an
exception. Effective shots come from result metadata, not the default."
```

---

### Task 12: Resource accounting

**Files:**
- Create: `research/paper_a/resources.py`
- Create: `research/paper_a/tests/test_resources.py`

**Interfaces:**
- Consumes: `Invocation` from Task 11.
- Produces: `executed_powers(powers, invocations) -> list[int]`; `m_a_logical(powers) -> int`; `m_a_executed(powers, shots) -> int`; `m_q_executed(powers, shots) -> int`; `shot_weighted_gates(invocations) -> dict[str,int]`; `max_executed_depth(invocations) -> int`.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_resources.py`:

```python
import pytest

from research.paper_a.recording import Invocation
from research.paper_a.resources import (
    executed_powers, m_a_executed, m_a_logical, m_q_executed,
    max_executed_depth, shot_weighted_gates,
)


def _inv(ordinal, shots, depth, ops):
    return Invocation(ordinal=ordinal, requested_shots=shots,
                      logical_qpy_sha256="0" * 64, isa_qpy_sha256="1" * 64,
                      isa_depth=depth, isa_ops=ops, effective_shots=shots,
                      status="complete")


def test_leading_sentinel_zero_is_excluded():
    """Qiskit initializes powers=[0] before the loop; that entry was never
    submitted unless an invocation proves it."""
    invocations = [_inv(0, 512, 10, {"cx": 4}), _inv(1, 512, 20, {"cx": 8})]
    assert executed_powers([0, 0, 1], invocations) == [0, 1]


def test_sentinel_kept_when_an_invocation_proves_k_zero_was_submitted():
    invocations = [_inv(i, 512, 10, {"cx": 4}) for i in range(3)]
    assert executed_powers([0, 0, 1], invocations) == [0, 0, 1]


def test_repeated_powers_remain_separate():
    invocations = [_inv(i, 512, 10, {"cx": 4}) for i in range(3)]
    assert executed_powers([0, 2, 2, 2], invocations) == [2, 2, 2]


def test_m_a_logical_is_an_invocation_count_not_a_depth():
    assert m_a_logical([0, 1, 2]) == (2 * 0 + 1) + (2 * 1 + 1) + (2 * 2 + 1)
    assert m_a_logical([0, 1, 2]) == 9


def test_m_a_executed_is_shot_weighted():
    assert m_a_executed([0, 1], [512, 2048]) == 512 * 1 + 2048 * 3


def test_m_q_executed_matches_qiskit_oracle_query_convention():
    """Qiskit accumulates num_oracle_queries += shots * k."""
    assert m_q_executed([0, 1, 3], [512, 512, 1024]) == (
        512 * 0 + 512 * 1 + 1024 * 3)


def test_unweighted_and_weighted_metrics_are_different_quantities():
    powers, shots = [0, 1, 2], [512, 512, 8192]
    assert m_a_logical(powers) != m_a_executed(powers, shots)
    assert m_a_executed(powers, shots) != m_q_executed(powers, shots)


def test_mismatched_lengths_are_rejected():
    with pytest.raises(ValueError):
        m_a_executed([0, 1], [512])


def test_shot_weighted_gate_burden_sums_per_operation():
    invocations = [_inv(0, 512, 10, {"cx": 4, "sx": 6}),
                   _inv(1, 2048, 20, {"cx": 8, "sx": 2})]
    assert shot_weighted_gates(invocations) == {
        "cx": 512 * 4 + 2048 * 8, "sx": 512 * 6 + 2048 * 2}


def test_max_executed_depth_is_the_maximum_not_the_sum():
    invocations = [_inv(0, 512, 10, {}), _inv(1, 512, 37, {}),
                   _inv(2, 512, 22, {})]
    assert max_executed_depth(invocations) == 37


def test_failed_invocations_retain_their_consumed_resources():
    failed = Invocation(ordinal=0, requested_shots=512,
                        logical_qpy_sha256="0" * 64, isa_qpy_sha256="1" * 64,
                        isa_depth=44, isa_ops={"cx": 3}, effective_shots=None,
                        status="failed", exception="boom")
    assert max_executed_depth([failed]) == 44
    assert shot_weighted_gates([failed]) == {}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_resources.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.resources'`

- [ ] **Step 3: Write the implementation**

`research/paper_a/resources.py`:

```python
"""Executed resource accounting.

Three distinct conventions, never conflated:
  M_A_logical  = sum_j (2k_j + 1)        unweighted A/A-inverse invocations
  M_A_executed = sum_j N_j (2k_j + 1)    shot-weighted
  M_Q_executed = sum_j N_j k_j           Grover applications
"""
from __future__ import annotations

from collections import Counter
from typing import Sequence

from research.paper_a.recording import Invocation


def executed_powers(powers: Sequence[int],
                    invocations: Sequence[Invocation]) -> list[int]:
    """Drop Qiskit's leading sentinel 0 unless an invocation proves it ran.

    IQAE seeds `powers = [0]` before its loop, so len(powers) is normally
    one greater than the number of submitted circuits.
    """
    values = list(powers)
    if len(values) == len(invocations) + 1:
        return values[1:]
    if len(values) == len(invocations):
        return values
    raise ValueError(
        f"cannot reconcile {len(values)} powers with "
        f"{len(invocations)} recorded invocations")


def m_a_logical(powers: Sequence[int]) -> int:
    return sum(2 * k + 1 for k in powers)


def _paired(powers: Sequence[int], shots: Sequence[int]):
    if len(powers) != len(shots):
        raise ValueError(
            f"powers ({len(powers)}) and shots ({len(shots)}) must align")
    return zip(powers, shots)


def m_a_executed(powers: Sequence[int], shots: Sequence[int]) -> int:
    return sum(n * (2 * k + 1) for k, n in _paired(powers, shots))


def m_q_executed(powers: Sequence[int], shots: Sequence[int]) -> int:
    return sum(n * k for k, n in _paired(powers, shots))


def shot_weighted_gates(invocations: Sequence[Invocation]) -> dict[str, int]:
    """Shot-weighted gate burden. Invocations with no effective shots
    contribute nothing but still retain their depth."""
    burden: Counter = Counter()
    for inv in invocations:
        if inv.effective_shots is None:
            continue
        for op, count in inv.isa_ops.items():
            burden[op] += inv.effective_shots * count
    return dict(burden)


def max_executed_depth(invocations: Sequence[Invocation]) -> int:
    """Maximum, never a sum. Failed attempts keep the depth they consumed."""
    return max((inv.isa_depth for inv in invocations), default=0)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_resources.py -v`
Expected: all passed

- [ ] **Step 5: Commit**

```bash
git add research/paper_a/resources.py research/paper_a/tests/test_resources.py
git commit -m "Add executed resource accounting

Three distinct A/Q conventions tested independently, sentinel-zero power
excluded, repeated powers retained, failed attempts keep consumed depth."
```

---

### Task 13: E0 gate battery and runner

**Files:**
- Create: `research/paper_a/validation.py`
- Create: `research/paper_a/configs/e0.json`
- Create: `research/paper_a/scripts/run_e0.py`
- Create: `research/paper_a/tests/test_validation.py`

**Interfaces:**
- Consumes: everything from Tasks 2–9.
- Produces: `GateResult` dataclass with `name: str`, `passed: bool`, `worst: float`, `tolerance: float`, `detail: str`; `run_e0_gates(contracts, q_total, qubit_counts, rescaling) -> list[GateResult]`; `all_passed(results) -> bool`.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_validation.py`:

```python
from research.paper_a.benchmark import VALIDATION_SET, by_id
from research.paper_a.payoff import C_RESCALING
from research.paper_a.validation import all_passed, run_e0_gates

GATES = ("probability_normalization", "pmf_max_elementwise", "pmf_l1",
         "objective_probability", "dollar_round_trip", "error_identity",
         "discount_applied_once", "raw_and_clipped_separate")


def test_every_named_gate_is_reported():
    results = run_e0_gates([by_id("E025")], 1e-4, (3,), C_RESCALING)
    assert {r.name for r in results} == set(GATES)


def test_gates_pass_on_the_validation_fixtures():
    results = run_e0_gates(list(VALIDATION_SET)[:4], 1e-4, (2, 3),
                           C_RESCALING)
    failures = [r for r in results if not r.passed]
    assert not failures, [(f.name, f.worst, f.tolerance) for f in failures]


def test_gates_pass_across_all_specified_qubit_counts():
    results = run_e0_gates([by_id("E025")], 1e-4, (2, 3, 4, 5), C_RESCALING)
    assert all_passed(results)


def test_each_result_reports_its_worst_value_and_tolerance():
    for r in run_e0_gates([by_id("E025")], 1e-4, (3,), C_RESCALING):
        assert r.tolerance >= 0   # boolean gates carry tolerance 0.0
        assert r.worst >= 0
        assert r.passed == (r.worst <= r.tolerance)


def test_all_passed_is_false_when_any_gate_fails():
    from research.paper_a.validation import GateResult
    mixed = [GateResult("a", True, 0.0, 1e-10, ""),
             GateResult("b", False, 1.0, 1e-10, "")]
    assert not all_passed(mixed)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_validation.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.validation'`

- [ ] **Step 3: Write the E0 config**

`research/paper_a/configs/e0.json`:

```json
{
  "config_version": "e0-v1",
  "phase": "E0",
  "q_total_candidates": [0.01, 0.001, 0.0001, 0.00001, 0.000001],
  "qubit_counts": [2, 3, 4, 5],
  "rescaling_factor": 0.25,
  "tolerances": {
    "probability_normalization": 1e-12,
    "pmf_max_elementwise": 1e-12,
    "pmf_l1": 1e-10,
    "objective_probability": 1e-10,
    "dollar_round_trip_relative": 1e-10,
    "error_identity_relative": 1e-10
  }
}
```

- [ ] **Step 4: Write the implementation**

`research/paper_a/validation.py`:

```python
"""E0 gate battery.

No stochastic experiment starts until every gate here passes. Tolerances are
frozen; changing one requires a versioned amendment before E1 outputs are
inspected.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np
from qiskit.quantum_info import Statevector

from research.paper_a.benchmark import Contract
from research.paper_a.errors import deterministic_ladder
from research.paper_a.european.circuits import (
    build_european, p_circuit, statevector_amplitude,
)
from research.paper_a.payoff import (
    a_calc, h_inverse, presentation_clipped, to_price,
)
from research.paper_a.references import (
    grid_points, grid_probabilities, support_audit,
)

TOL_NORMALIZATION = 1e-12
TOL_PMF_MAX = 1e-12
TOL_PMF_L1 = 1e-10
TOL_OBJECTIVE = 1e-10
TOL_RELATIVE = 1e-10


@dataclass(frozen=True)
class GateResult:
    name: str
    passed: bool
    worst: float
    tolerance: float
    detail: str


def _gate(name: str, worst: float, tolerance: float, detail: str) -> GateResult:
    return GateResult(name, worst <= tolerance, worst, tolerance, detail)


def run_e0_gates(contracts: Sequence[Contract], q_total: float,
                 qubit_counts: Sequence[int],
                 rescaling: float) -> list[GateResult]:
    worst = {k: (0.0, "") for k in (
        "probability_normalization", "pmf_max_elementwise", "pmf_l1",
        "objective_probability", "dollar_round_trip", "error_identity",
        "discount_applied_once", "raw_and_clipped_separate")}

    def bump(key: str, value: float, detail: str) -> None:
        if value > worst[key][0]:
            worst[key] = (value, detail)

    for c in contracts:
        audit = support_audit(c, q_total)
        scale = max(1.0, c.S0)
        for n in qubit_counts:
            tag = f"{c.id} n={n}"
            x = grid_points(audit.L, audit.U, n)
            pi = grid_probabilities(c, audit.L, audit.U, n)
            bump("probability_normalization", abs(pi.sum() - 1.0), tag)

            ec = build_european(c, audit.L, audit.U, n, rescaling)
            circuit_pmf = Statevector(ec.circuit).probabilities(range(n))
            bump("pmf_max_elementwise",
                 float(np.abs(circuit_pmf - pi).max()), tag)
            bump("pmf_l1", float(np.abs(circuit_pmf - pi).sum()), tag)

            expected_a = a_calc(pi, x, c.K, audit.U, rescaling)
            a_sv = statevector_amplitude(ec)
            bump("objective_probability", abs(a_sv - expected_a), tag)

            # Dollar round trip: price -> amplitude -> price.
            price = to_price(a_sv, c.K, audit.U, rescaling, c.r, c.T)
            undiscounted = h_inverse(a_sv, c.K, audit.U, rescaling)
            bump("dollar_round_trip",
                 abs(price - math.exp(-c.r * c.T) * undiscounted) / scale, tag)

            # Discount applied EXACTLY once: the price must match a single
            # discount and must be measurably far from a doubled one.
            once = math.exp(-c.r * c.T) * undiscounted
            twice = math.exp(-2.0 * c.r * c.T) * undiscounted
            single_gap = abs(price - once) / scale
            double_gap = abs(price - twice) / scale
            bump("discount_applied_once",
                 single_gap if double_gap > TOL_RELATIVE else 1.0, tag)

            # Raw and clipped must be genuinely separate quantities. Drive the
            # amplitude below the zero-price point so the raw value is negative
            # and the clipped value provably differs from it.
            negative_raw = to_price(0.0, c.K, audit.U, rescaling, c.r, c.T)
            clipped = presentation_clipped(negative_raw)
            separated = negative_raw < 0.0 and clipped == 0.0 \
                and clipped != negative_raw
            bump("raw_and_clipped_separate", 0.0 if separated else 1.0, tag)

            ladder = deterministic_ladder(c, q_total, n, rescaling)
            telescoped = (ladder.e_support + ladder.e_grid + ladder.e_encode)
            bump("error_identity",
                 abs(telescoped - (ladder.P_circuit - ladder.P_BS)) / scale, tag)

    tolerances = {
        "probability_normalization": TOL_NORMALIZATION,
        "pmf_max_elementwise": TOL_PMF_MAX,
        "pmf_l1": TOL_PMF_L1,
        "objective_probability": TOL_OBJECTIVE,
        "dollar_round_trip": TOL_RELATIVE,
        "error_identity": TOL_RELATIVE,
        "discount_applied_once": TOL_RELATIVE,
        "raw_and_clipped_separate": 0.0,
    }
    return [_gate(name, value, tolerances[name], detail)
            for name, (value, detail) in worst.items()]


def all_passed(results: Sequence[GateResult]) -> bool:
    return all(r.passed for r in results)
```

- [ ] **Step 5: Write the runner**

`research/paper_a/scripts/run_e0.py`:

```python
"""Run the E0 gate battery over the full benchmark and print a report."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from research.paper_a.benchmark import BENCHMARK, VALIDATION_SET
from research.paper_a.environment import capture_environment
from research.paper_a.references import select_support_rule
from research.paper_a.validation import all_passed, run_e0_gates

CONFIG = json.loads(
    (Path(__file__).parent.parent / "configs" / "e0.json").read_text())


def main() -> int:
    contracts = list(BENCHMARK) + list(VALIDATION_SET)
    q_total = select_support_rule(BENCHMARK, CONFIG["q_total_candidates"])
    print(f"selected q_total = {q_total}")
    print(f"environment      = {capture_environment()['packages']}")

    results = run_e0_gates(contracts, q_total, CONFIG["qubit_counts"],
                           CONFIG["rescaling_factor"])
    width = max(len(r.name) for r in results)
    for r in sorted(results, key=lambda x: x.name):
        status = "PASS" if r.passed else "FAIL"
        print(f"  {status}  {r.name:<{width}}  worst={r.worst:.3e}  "
              f"tol={r.tolerance:.1e}  {r.detail}")

    if all_passed(results):
        print("\nE0 PASSED - stochastic experiments are unblocked.")
        return 0
    print("\nE0 FAILED - no stochastic experiment may start.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_validation.py -v`
Expected: all passed

- [ ] **Step 7: Run the full E0 battery**

Run: `venv/Scripts/python.exe -m research.paper_a.scripts.run_e0`
Expected: every gate `PASS`, exit code 0. `n=5` over 62 contracts takes a few minutes.

**If any gate fails, stop.** That is the E0 gate doing its job; diagnose before proceeding.

- [ ] **Step 8: Commit**

```bash
git add research/paper_a/validation.py research/paper_a/configs/ \
        research/paper_a/scripts/ research/paper_a/tests/test_validation.py
git commit -m "Add E0 gate battery and runner

Eight frozen gates over the full benchmark and validation fixtures at
n=2..5. Exit code is non-zero unless every gate passes."
```

---

### Task 14: End-to-end smoke experiment

**Files:**
- Create: `research/paper_a/scripts/run_smoke.py`
- Create: `research/paper_a/tests/test_smoke_pipeline.py`
- Create: `research/paper_a/README.md`

**Interfaces:**
- Consumes: everything above.
- Produces: `run_smoke(output_dir, shots=512) -> dict` writing `raw.jsonl`, `resources.jsonl`, `validation.json`, and `COMPLETE`.

- [ ] **Step 1: Write the failing test**

`research/paper_a/tests/test_smoke_pipeline.py`:

```python
import json

from research.paper_a.schema import read_records, validate_record
from research.paper_a.scripts.run_smoke import run_smoke


def test_smoke_produces_a_complete_experiment_directory(tmp_path):
    summary = run_smoke(tmp_path, shots=256)
    for name in ("raw.jsonl", "resources.jsonl", "validation.json", "COMPLETE"):
        assert (tmp_path / name).exists(), f"{name} missing"
    assert summary["attempts"] == 4  # 2 configs x 2 seeds, ideal only


def test_every_smoke_record_validates(tmp_path):
    run_smoke(tmp_path, shots=256)
    for record in read_records(tmp_path / "raw.jsonl"):
        assert validate_record(record) == [], record


def test_records_carry_full_provenance(tmp_path):
    run_smoke(tmp_path, shots=256)
    for record in read_records(tmp_path / "raw.jsonl"):
        assert record["environment"]["git_commit"]
        assert record["stream_key"].startswith("paper-a/v1 | ")
        assert record["P_BS"] and record["P_grid"] and record["P_circuit"]


def test_resources_are_recorded_per_invocation(tmp_path):
    run_smoke(tmp_path, shots=256)
    resources = read_records(tmp_path / "resources.jsonl")
    assert resources
    for r in resources:
        assert r["m_a_logical"] >= 1
        assert r["m_a_executed"] >= r["m_a_logical"]
        assert r["max_executed_depth"] > 0


def test_complete_marker_is_written_last(tmp_path):
    run_smoke(tmp_path, shots=256)
    marker = json.loads((tmp_path / "COMPLETE").read_text())
    assert marker["raw_sha256"] and marker["resources_sha256"]


def test_rerun_is_idempotent_and_does_not_duplicate(tmp_path):
    run_smoke(tmp_path, shots=256)
    first = len(read_records(tmp_path / "raw.jsonl"))
    run_smoke(tmp_path, shots=256)
    assert len(read_records(tmp_path / "raw.jsonl")) == first
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_smoke_pipeline.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'research.paper_a.scripts.run_smoke'`

- [ ] **Step 3: Write the implementation**

`research/paper_a/scripts/run_smoke.py`:

```python
"""Tiny end-to-end experiment: 2 configs, n=3, 2 seeds, ideal only.

Exercises config -> references -> circuit -> recorded IQAE -> raw records ->
resources -> validation -> COMPLETE, so the pipeline is proven before any
full experiment runs.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qiskit.primitives import Sampler
from qiskit_algorithms import EstimationProblem, IterativeAmplitudeEstimation

from research.paper_a.benchmark import by_id
from research.paper_a.environment import capture_environment
from research.paper_a.errors import deterministic_ladder
from research.paper_a.european.circuits import build_european
from research.paper_a.payoff import C_RESCALING, presentation_clipped, to_price
from research.paper_a.recording import RecordingSampler
from research.paper_a.references import support_bounds
from research.paper_a.resources import (
    executed_powers, m_a_executed, m_a_logical, m_q_executed,
    max_executed_depth, shot_weighted_gates,
)
from research.paper_a.schema import (
    SCHEMA_VERSION, append_record, idempotency_key, read_records,
    validate_record,
)
from research.paper_a.streams import stream_key

CONFIGS = ("E001", "E025")
REPLICATES = (0, 1)
Q_TOTAL = 1e-4
N = 3
EXPERIMENT_UUID = "smoke-0001"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_smoke(output_dir, shots: int = 512) -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    raw_path, res_path = out / "raw.jsonl", out / "resources.jsonl"

    done = {r["idempotency_key"] for r in read_records(raw_path)} \
        if raw_path.exists() else set()
    environment = capture_environment()
    attempts = 0

    for cid in CONFIGS:
        contract = by_id(cid)
        L, U = support_bounds(contract, Q_TOTAL)
        ladder = deterministic_ladder(contract, Q_TOTAL, N, C_RESCALING)
        ec = build_european(contract, L, U, N, C_RESCALING)

        for replicate in REPLICATES:
            attempts += 1
            key = idempotency_key(EXPERIMENT_UUID, "SMOKE", cid, N, replicate,
                                  "ideal", "shots")
            if key in done:
                continue

            skey = stream_key("paper-a/pilot/v1", EXPERIMENT_UUID, "SMOKE",
                              cid, N, replicate, "ideal", "shots")
            sampler = RecordingSampler(Sampler(options={"seed": replicate}),
                                       shots=shots)
            iqae = IterativeAmplitudeEstimation(
                epsilon_target=0.05, alpha=0.05, confint_method="beta",
                sampler=sampler)
            result = iqae.estimate(EstimationProblem(
                state_preparation=ec.circuit,
                objective_qubits=[ec.objective_qubit]))

            price = to_price(result.estimation, contract.K, U, C_RESCALING,
                             contract.r, contract.T)
            record = {
                "schema_version": SCHEMA_VERSION,
                "experiment_uuid": EXPERIMENT_UUID, "phase": "SMOKE",
                "config_id": cid, "n": N, "replicate": replicate,
                "condition": "ideal", "attempt_kind": "first_planned",
                "idempotency_key": key, "stream_key": skey,
                "raw_estimation": float(result.estimation),
                "raw_confidence_interval": [float(x) for x in
                                            result.confidence_interval],
                "raw_price": price,
                "presentation_clipped_price": presentation_clipped(price),
                "completion_state": "complete", "environment": environment,
                "P_BS": ladder.P_BS, "P_support": ladder.P_support,
                "P_grid": ladder.P_grid, "P_circuit": ladder.P_circuit,
                "e_support": ladder.e_support, "e_grid": ladder.e_grid,
                "e_encode": ladder.e_encode,
            }
            append_record(raw_path, record)

            powers = executed_powers(result.powers, sampler.invocations)
            shot_list = [i.effective_shots for i in sampler.invocations]
            append_record(res_path, {
                "idempotency_key": key, "config_id": cid, "n": N,
                "replicate": replicate,
                "invocations": len(sampler.invocations),
                "powers": powers,
                "m_a_logical": m_a_logical(powers),
                "m_a_executed": m_a_executed(powers, shot_list),
                "m_q_executed": m_q_executed(powers, shot_list),
                "max_executed_depth": max_executed_depth(sampler.invocations),
                "shot_weighted_gates": shot_weighted_gates(
                    sampler.invocations),
                "provenance": "actual",
            })

    violations = {r["idempotency_key"]: validate_record(r)
                  for r in read_records(raw_path)}
    (out / "validation.json").write_text(json.dumps(
        {"violations": {k: v for k, v in violations.items() if v},
         "records": len(violations)}, indent=2))

    (out / "COMPLETE").write_text(json.dumps({
        "raw_sha256": _sha256(raw_path),
        "resources_sha256": _sha256(res_path),
        "environment": environment,
    }, indent=2))
    return {"attempts": attempts, "records": len(violations)}


if __name__ == "__main__":
    print(run_smoke(Path("data/paper_a/smoke")))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv/Scripts/pytest.exe research/paper_a/tests/test_smoke_pipeline.py -v`
Expected: all passed

- [ ] **Step 5: Write the package README**

`research/paper_a/README.md`:

```markdown
# Paper A Research Package

Isolated from `src/` and `app/`. The deployed dashboard is never affected by
anything here.

## Gates

    venv/Scripts/python.exe -m research.paper_a.scripts.run_e0

Exit code 0 means every deterministic semantic check passed and stochastic
experiments are unblocked. Non-zero means **no stochastic experiment may
start**. See the spec's E0 section for what each gate proves.

## Smoke run

    venv/Scripts/python.exe -m research.paper_a.scripts.run_smoke

Writes `data/paper_a/smoke/` with `raw.jsonl`, `resources.jsonl`,
`validation.json`, and `COMPLETE`. Re-running is idempotent.

## Frozen values

Benchmark, subsets, support rule, rescaling factor, streams, and tolerances
are frozen in the spec's Frozen Protocol Annex. Changing any of them requires
a versioned amendment recorded **before** the affected output is inspected.

## Deliberate differences from `src/`

`src/quantum.py` clamps `sigma` to 0.15 for dashboard display. This package
**rejects** out-of-domain input with a named error and never clamps.
```

- [ ] **Step 6: Run the whole suite plus lint and typecheck**

```bash
venv/Scripts/pytest.exe research/paper_a/tests/ -v
venv/Scripts/ruff.exe check research/
venv/Scripts/python.exe -m mypy research/
```
Expected: all tests pass, ruff clean, mypy clean.

- [ ] **Step 7: Commit**

```bash
git add research/paper_a/scripts/run_smoke.py \
        research/paper_a/tests/test_smoke_pipeline.py \
        research/paper_a/README.md
git commit -m "Add end-to-end smoke experiment and package README

Proves config to references to circuit to recorded IQAE to raw records to
resources to validation to COMPLETE, with idempotent re-runs."
```

---

## Week 2 Exit Gate

Plan 1 is done when all of these hold:

- [ ] `run_e0` exits 0 with every gate PASS over all 50 benchmark rows plus the 12 fixtures at `n=2,3,4,5`.
- [ ] The smoke experiment creates, resumes, validates, and freezes a small dataset with one command.
- [ ] Every reference layer agrees with its independent calculation inside the frozen tolerance.
- [ ] The recording adapter either captures actual submitted round circuits and effective shots, **or** the `reconstructed-only-v1` fallback is documented with its claim restrictions (Predeclared Pilot Outcome #2 resolved either way).
- [ ] The Annex B environment discrepancy has a written amendment decision.
- [ ] `ruff` and `mypy` are clean over `research/`.

Only then does Plan 2 (E1 deterministic scaling and the E2 pilot) get written.

---

## Self-Review

**Spec coverage.** E0's reference ladder → Tasks 5–8; support-rule selection → Task 5; domain rejection with named errors → Task 2; error identity → Task 9; Annex A benchmark and A.1 subsets → Tasks 2–3; Annex C payoff semantics → Task 7; Annex D streams → Task 4; Annex I recording and provenance → Tasks 10–11; resource conventions → Task 12; deterministic tolerances → Task 13; smoke run → Task 14.

**Deferred to later plans, deliberately:** Annex E compute thresholds and `n=5` promotion (Plan 2, needs measured runtimes); Annex F controlled-noise ISA (Plan 3, first noisy run); Annex G Monte Carlo context (Plan 3); Annex H Asian protocol (Plan 4); `statistics.py` bootstrap and `R_min` (Plan 2, first aggregate); the `c` sweep itself (Plan 2 — its *algebra* is tested here in Task 7, but the E1 sweep needs the E1 runner). The transpilation cache key is stubbed to a single frozen target in Task 11; its full contract lands in Plan 3 when a second target exists.

**Known gap carried forward:** Annex E's runtime gates are non-binding against the compute budget (~1.6 min median per attempt is what 105 hours affords at `R=10`, versus a `p95 ≤ 10 min` gate). Plan 2's E2 pilot must project from measured medians, not from gate headroom.
