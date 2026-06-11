<div align="center">

# ⚛️ Quantum Option Pricing

**A deployed dashboard that prices European call options three ways — and honestly shows where quantum loses.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Railway-brightgreen?style=for-the-badge)](https://web-production-559db.up.railway.app)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Qiskit](https://img.shields.io/badge/Qiskit-0.45-purple?style=for-the-badge)](https://qiskit.org)
[![Health](https://img.shields.io/badge/Health-10%2F10-success?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](#)

[**→ Open Live Dashboard**](https://web-production-559db.up.railway.app)

</div>

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

**The honest framing is the point.** The QAE advantage is real in theory. On today's noisy hardware, the crossover is out of reach. This project shows both, with citations.

---

## Live dashboard

[**→ web-production-559db.up.railway.app**](https://web-production-559db.up.railway.app)

- Adjust S₀, K, T, σ, r with sliders
- Watch Monte Carlo converge in real time
- See QAE results from the precomputed 600-point grid
- Break-even chart: where QAE wins (ideal) vs where it sits (NISQ)

---

## Research program

This project is the foundation for three research papers, each extending the honest-framing thesis.

### Paper A — *NISQ Noise Shifts the Break-Even* `[in progress]`
> **Venue target:** EPJ Quantum Technology / arXiv preprint

Every existing paper assumes perfect quantum hardware. This one doesn't.

IQAE circuit run through Qiskit's AerSimulator with `NoiseModel.from_backend()` across IBM backends. Sweep noise levels p ∈ {0, 1e-4, 1e-3, 5e-3, 1e-2}. Break-even frontier shown as a 2D heatmap over (ε, p).

**Key finding:** Even at p=0 (noiseless simulation), mean price error is already ~20× above the ε=0.01 target — the state-preparation cost alone is prohibitive before hardware noise enters the picture.

**Open item:** One real IBM hardware run for at least one data point. This is the highest-leverage remaining item in the program — simulation-only results are expected by reviewers to be backed by at least one hardware confirmation.

**Novel contribution:** No existing paper maps break-even vs noise rate for option pricing circuits.

---

### Paper B — *The Wrong Baseline: How Variance-Reduced Monte Carlo Erases QAE's Advantage in Option Pricing* `[complete — preparing submission]`
> **Venue target:** Quantitative Finance / Physica A

The QAE literature compares against naive Monte Carlo. Practitioners don't use naive Monte Carlo — they use antithetic variates, control variates, and quasi-MC (Sobol sequences). This paper re-derives the break-even equation with the right baseline.

**Key findings (all empirically verified with bootstrap 95% CIs, 2000 resamples):**

| Baseline | Break-even oracle queries | QAE hurdle vs naive |
|---|---|---|
| Naive MC | M ≈ 314 | 1× (reference) |
| Antithetic (VRF 2.0×) | M ≈ 222 | 1.41× harder |
| Control variate (VRF 6.8×) | M ≈ 120 | 2.61× harder |
| RQMC (Sobol) | changes convergence *exponent* | asymptotic advantage gone |

RQMC achieves empirical convergence slope −0.94 [−0.80, −1.10] at d=1 — matching QAE's claimed O(1/N) rate. This advantage degrades with dimension (slope −0.71 [−0.60, −0.83] at d=64), with crossover around d≈16–32. Even on discontinuous payoffs (European digital cash-or-nothing), RQMC slope is −0.98 [−0.90, −1.06], consistent with He & Wang (2015) theoretical prediction of −1.0 at d=1.

**Novel contribution:** Methodological critique of the QAE option pricing literature. The classical baseline used in every prior break-even calculation is not the baseline quants deploy.

---

### Paper C — *Unified Quantum Advantage Frontier* `[planned — awaiting A and B]`
> **Venue target:** Quantum journal

Combine Papers A and B into one unified figure: the quantum advantage region as a function of (ε, noise rate p, MC variance reduction factor).

**Main claim:** Under joint realistic assumptions — variance-reduced MC and NISQ noise — quantum advantage in European option pricing requires ε < X on hardware with error rate p < Y.

**Novel contribution:** The unified honest framework the field has been missing.

---

## Canonical numbers (Paper B — frozen)

These numbers are verified and frozen. If a re-run produces different values, investigate before updating.

| Experiment | Value |
|---|---|
| European call RQMC convergence slope | −1.04 |
| Dimension sweep d=1 RQMC slope | −0.94 [−1.10, −0.80] |
| Dimension sweep d=64 RQMC slope | −0.71 [−0.83, −0.60] |
| Digital RQMC slope | −0.98 [−1.06, −0.90] |
| QAE grid bias at n=5 qubits (digital) | 2.16×10⁻² |
| Table IV N window | [1024, 16384] (5 points) |

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
  plot_dimension_sweep.py      # Geometric dimension sweep → Table IV (Paper B)
  plot_digital_convergence.py  # Digital convergence experiment → Section VII (Paper B)
  plot_break_even_shift.py     # Break-even framing
  noise_experiments.py         # Paper A noise sweep (AerSampler)
data/
  qae_grid.pkl                 # 600 points: S₀ × K × T × σ
tests/
  test_pricing.py              # 10 tests
  test_digital.py              # 15 tests (all passing)
  test_asian_cv_ref.py         # 3 tests
docs/
  PROJECT_UPDATE_2026-06-10.md # Latest session record
```

**QAK grid:** 600 points = 5 S₀ × 5 K × 6 T × 4 σ  
**Runtime stack:** numpy, scipy, dash, plotly, gunicorn (no Qiskit at runtime)  
**Dev stack:** + qiskit==0.45, qiskit-aer==0.12.2, qiskit-finance, qiskit-algorithms  
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

---

## References

- Woerner & Egger (2019). *Quantum risk analysis.* npj Quantum Information. [arXiv:1806.06893](https://arxiv.org/abs/1806.06893)
- Stamatopoulos et al. (2020). *Option pricing using quantum computers.* Quantum. [arXiv:1905.02666](https://arxiv.org/abs/1905.02666)
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
| Paper B — fair MC baseline | ✅ Complete — preparing submission |
| Paper A — NISQ noise sweep | 🔬 In progress (IBM hardware run pending) |
| Paper C — unified frontier | 📋 Planned — awaits A and B |

---

<div align="center">

Built by [Prithvi](https://github.com/Prithvi8706) · VIT Chennai · 2026

*Quantum advantage is real. On current hardware, it's not here yet. This project shows both.*

</div>