<div align="center">

# ⚛️ Quantum Option Pricing

**A deployed dashboard that prices European call options three ways — and honestly shows where quantum loses.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Railway-brightgreen?style=for-the-badge)](https://web-production-559db.up.railway.app)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-0.46.3-purple?style=for-the-badge)](https://qiskit.org)
[![Health](https://img.shields.io/badge/Health-10%2F10-success?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](#)

[**→ Open Live Dashboard**](https://web-production-559db.up.railway.app)

</div>

---

## Contents

- [What this is](#what-this-is)
- [Live dashboard](#live-dashboard)
- [Research program](#research-program)
- [Canonical numbers (frozen)](#canonical-numbers-frozen)
- [How it's built](#how-its-built)
- [Math](#math)
- [Running locally](#running-locally)
- [References](#references)
- [Project status](#project-status)

---

## What this is

Most quantum finance projects claim quantum computers will revolutionize option pricing. This one shows you exactly when — and more importantly, **exactly when they won't.**

Three pricing methods run side by side:

| Method | Approach | Error Scaling | Status |
|---|---|---|---|
| **Black-Scholes** | Closed-form formula | Exact | ✅ Live |
| **Monte Carlo** | Simulates thousands of random futures | O(1/√N) | ✅ Live (animated) |
| **Quantum (QAE)** | Iterative Amplitude Estimation circuit | O(1/M) ideal | ✅ Live (precomputed grid) |

The break-even visualizer shows the crossover point where QAE theoretically beats Monte Carlo — and the NISQ overhead band showing how far current hardware sits from that threshold.

**The honest framing is the point.** The QAE advantage is real in theory. On today's noisy hardware, the crossover is out of reach. This project shows both, with citations and a real-hardware validation run to back it.

---

## Live dashboard

[**→ web-production-559db.up.railway.app**](https://web-production-559db.up.railway.app)

- Adjust S₀, K, T, σ, r with sliders
- Watch Monte Carlo converge in real time
- See QAE results from the precomputed 600-point grid
- Break-even chart: where QAE wins (ideal) vs where it sits (NISQ)

---

## Research program

This project is the foundation for three research papers, each extending the honest-framing thesis. **Papers A and B are complete and preparing submission; Paper C is planned.**

### Paper A — *NISQ Noise Shifts the Break-Even* `[complete — preparing submission]`
> **Venue target:** EPJ Quantum Technology / arXiv preprint

Every existing paper assumes perfect quantum hardware. This one doesn't.

An IQAE circuit is run through Qiskit's AerSimulator across a noise-rate sweep p ∈ {0, 1e-4, 1e-3, 5e-3, 1e-2} — **50 option configurations × 5 noise levels = 250 runs**. The break-even frontier is reported over option configuration and noise rate, alongside a mean-error-vs-noise curve and a noise-invariant oracle-depth panel.

**Key findings:**
- At current IBM hardware noise (p ≈ 1e-3), mean price error is **$0.657** — roughly **66×** the ε = 0.01 precision target.
- Even at **p = 0** (noiseless), mean price error is already **$0.203** — about **20×** the target. The 3-qubit discretization imposes an irreducible floor *before* any noise enters.
- IQAE oracle-query depth is **noise-invariant** (~14 queries, range 13.6–14.5, across every p). The query budget never inflates; accuracy decays silently.

**Hardware validation:** A single-qubit state-preparation primitive (Rᵧ(2·arcsin√0.3), encoding p = 0.30) was run on **ibm_marrakesh (Heron r2)** at 1024 shots (Job `d8nvd2bqv2lc7389d9e0`, counts `{"0": 733, "1": 291}`). Empirical **p̂ = 0.2842** — absolute error **0.0158**, within the 1024-shot binomial noise band (σ = √(0.3·0.7/1024) = **0.0143**, deviation **1.1σ**). The amplitude-encoding step is faithful on real hardware, with no detectable device error beyond shot noise.

> Processor family "Heron r2" is a known external fact about `ibm_marrakesh`; it is not stored in the result JSON, which records only the backend name.

**Novel contribution:** No existing paper maps break-even vs noise rate for option pricing circuits, or shows the discretization floor dominates at near-term scale.

---

### Paper B — *The Wrong Baseline: How Variance-Reduced Monte Carlo Erases QAE's Advantage in Option Pricing* `[complete — preparing submission]`
> **Venue target:** Quantitative Finance / Physica A

The QAE literature compares against naive Monte Carlo. Practitioners don't use naive Monte Carlo — they use antithetic variates, control variates, and quasi-MC (Sobol sequences). This paper re-derives the break-even equation with the right baseline.

**Key findings (empirically verified with bootstrap 95% CIs, 2000 resamples):**

| Baseline | Break-even oracle queries | QAE hurdle vs naive |
|---|---|---|
| Naive MC | M ≈ 314 | 1× (reference) |
| Antithetic (VRF 2.0×) | M ≈ 222 | 1.41× harder |
| Control variate (VRF 6.8×) | M ≈ 120 | 2.61× harder |
| RQMC (Sobol) | changes convergence *exponent* | asymptotic advantage gone |

On the European call benchmark, RQMC achieves empirical convergence slope **−1.04** — matching QAE's claimed O(1/N) rate. The advantage **degrades mildly but persists through d = 64** (geometric Asian dimension sweep, below): RQMC stays well steeper than the classical −0.5 rate at *every* dimension tested, sliding only from −0.98 at d = 1 to −0.77 at d = 64. Even on discontinuous payoffs (European digital cash-or-nothing), RQMC slope is **−0.98 [−1.06, −0.90]**, consistent with He & Wang (2015), whose theory predicts −1.0 at d = 1.

**Dimension sweep (Table IV — 100-trial stabilized slopes, supersedes earlier 10-trial estimates):**

| d | RQMC slope | 95% CI |
|---|---|---|
| 1 | −0.98 | [−1.04, −0.92] |
| 2 | −1.06 | [−1.13, −0.99] |
| 4 | −0.89 | [−0.97, −0.81] |
| 8 | −0.86 | [−0.93, −0.79] |
| 16 | −0.79 | [−0.85, −0.71] |
| 32 | −0.85 | [−0.92, −0.78] |
| 64 | −0.77 | [−0.84, −0.69] |

The trend is a **mild degradation with dimension, not a crossover** — RQMC's edge over classical Monte Carlo persists across the full range to d = 64.

**Novel contribution:** Methodological critique of the QAE option pricing literature. The classical baseline used in every prior break-even calculation is not the baseline quants deploy.

---

### Paper C — *Unified Quantum Advantage Frontier* `[planned — A and B complete]`
> **Venue target:** Quantum journal

Combine Papers A and B into one unified figure: the quantum advantage region as a function of (ε, noise rate p, MC variance reduction factor).

**Main claim:** Under joint realistic assumptions — variance-reduced MC and NISQ noise — quantum advantage in European option pricing requires ε < X on hardware with error rate p < Y.

**Novel contribution:** The unified honest framework the field has been missing.

---

## Canonical numbers (frozen)

These numbers are verified and frozen. If a re-run produces different values, investigate before updating.

| Experiment | Value |
|---|---|
| Paper A — mean price error @ p = 0 (ideal) | $0.203 |
| Paper A — mean price error @ p = 1e-3 (current IBM) | $0.657 |
| Paper A — IQAE oracle depth (all p, noise-invariant) | ~14 (13.6–14.5) |
| Paper A — hardware validation (ibm_marrakesh, 1024 shots) | p̂ = 0.2842 (1.1σ from 0.30) |
| Paper B — European call RQMC convergence slope | −1.04 |
| Paper B — dimension sweep d=1 RQMC slope | −0.98 [−1.04, −0.92] |
| Paper B — dimension sweep d=64 RQMC slope | −0.77 [−0.84, −0.69] |
| Paper B — digital RQMC slope | −0.98 [−1.06, −0.90] |
| Paper B — QAE grid bias at n=5 qubits (digital) | 2.16×10⁻² |
| Paper B — Table IV N window | [1024, 16384] (5 points) |

---

## How it's built

```
app/
  app.py                       # Dash layout, callbacks, break-even chart
  precompute_qae.py            # 600-point grid generator
  assets/style.css             # Dark theme, WCAG AA, responsive
src/
  black_scholes.py             # Closed-form pricer + digital_bs_price
  classical.py                 # Monte Carlo
  quantum.py                   # QAE circuit (IQAE) + quantum_digital_call
  digital_option.py            # Digital MC, antithetic, RQMC pricers
  asian_option.py              # Asian pricers + arithmetic CV reference
  plot_convergence.py          # European call convergence → RQMC slope (Paper B)
  plot_dimension_sweep.py      # Geometric dimension sweep → Table IV (Paper B)
  plot_digital_convergence.py  # Digital convergence experiment → Section VII (Paper B)
  plot_break_even_shift.py     # Break-even framing
  plot_hardware_validation.py  # Hardware validation figure (Paper A)
  noise_experiments.py         # Paper A noise sweep (AerSampler)
ibm_validation.py              # Paper A real-hardware run (ibm_marrakesh)
data/
  qae_grid.pkl                 # 600 points: S₀ × K × T × σ
  noise_sweep_expanded.csv     # Paper A noise sweep: 250 runs (50 pts × 5 levels)
results/
  ibm_hardware_validation.json # Hardware run result (Job d8nvd2bqv2lc7389d9e0)
tests/
  test_pricing.py              # 10 tests
  test_digital.py              # 15 tests
  test_asian_cv_ref.py         # 3 tests
docs/
  PROJECT_UPDATE_2026-06-10.md # Latest session record
```

**QAE grid:** 600 points = 5 S₀ × 5 K × 6 T × 4 σ (r fixed)
**Runtime stack:** numpy, scipy, dash, plotly, gunicorn (no Qiskit at runtime)
**Dev stack:** + qiskit==0.46.3, qiskit-aer==0.12.2, qiskit-finance, qiskit-algorithms
**Hardware stack (separate env):** qiskit-ibm-runtime — for the `ibm_marrakesh` validation run, in a separate anaconda environment (do not merge it with the pinned dev venv)
**Pinned:** scipy==1.13.1 (Sobol results depend on this version — do not upgrade)
**Deployment:** Railway (auto-deploys on push to main)

---

## Math

**QAE error bound** (Stamatopoulos et al. 2020, eq. 3):

```
|a - ã| ≤ π/M + π²/M²  =  O(M⁻¹)
```

**Monte Carlo error:**

```
ε_MC = 1.96 / √N  =  O(N⁻¹ᐟ²)
```

**Break-even crossover (naive MC):**

```
M_crossover = π√N / 1.96  ≈  1.604 × √N
```

At ε = 0.01: Monte Carlo needs N ≈ 38,416 samples. QAE needs M ≈ 314 oracle queries — a ~120× query reduction **against naive MC**. Paper B shows this crossover shifts significantly when the baseline is variance-reduced Monte Carlo, which is what practitioners actually deploy.

---

## Running locally

```bash
git clone https://github.com/Prithvi8706/quantum_option_pricing
cd quantum_option_pricing
pip install -r requirements-dev.txt
python app/app.py
```

Health check:

```bash
pytest tests/        # 28 tests
mypy src/ app/       # type check
ruff check .         # lint
```

> **Note:** Before running any experiment scripts, confirm `scipy==1.13.1` is installed:
> ```bash
> python -c "import scipy; print(scipy.__version__)"
> ```

> **Hardware run:** `ibm_validation.py` runs in a separate environment with `qiskit-ibm-runtime` and an IBM Quantum Platform API key + instance CRN (stored in `.env`, gitignored). The dev env stays pinned to qiskit 0.46.3; do not merge the two.

---

## References

- Woerner & Egger (2019). *Quantum risk analysis.* npj Quantum Information. [arXiv:1806.06893](https://arxiv.org/abs/1806.06893)
- Stamatopoulos et al. (2020). *Option pricing using quantum computers.* Quantum. [arXiv:1905.02666](https://arxiv.org/abs/1905.02666)
- Grinko et al. (2021). *Iterative quantum amplitude estimation.* npj Quantum Information. [arXiv:1912.05559](https://arxiv.org/abs/1912.05559)
- Carrera Vazquez & Woerner (2020). *Efficient state preparation for quantum amplitude estimation.* [arXiv:2009.05756](https://arxiv.org/abs/2009.05756)
- He & Wang (2015). *On the convergence rate of randomized quasi–Monte Carlo for discontinuous functions.* SIAM J. Numer. Anal. 53(5):2488–2503.

---

## Project status

| Component | Status |
|---|---|
| Dashboard (BS + MC + QAE) | ✅ Live |
| Break-even visualizer | ✅ Live |
| Design system (WCAG AA) | ✅ Done |
| Health (pytest/mypy/ruff) | ✅ 10/10 — 28 tests passing |
| Paper A — NISQ noise sweep | ✅ Complete — hardware run done (ibm_marrakesh), preparing submission |
| Paper B — fair MC baseline | ✅ Complete — preparing submission |
| Paper C — unified frontier | 📋 Planned — A and B complete |

---

<div align="center">

Built by [Prithvi](https://github.com/Prithvi8706) · VIT Vellore · 2026

*Quantum advantage is real. On current hardware, it's not here yet. This project shows both.*

</div>
