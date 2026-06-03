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
> **Venue:** EPJ Quantum Technology / arxiv preprint

Every existing paper assumes perfect quantum hardware. This paper doesn't.

Run the IQAE circuit through Qiskit's AerSimulator with `NoiseModel.from_backend()` across 3–4 IBM backends. Sweep noise levels p ∈ {0, 1e-4, 1e-3, 5e-3, 1e-2}. Show the break-even frontier as a 2D heatmap over (ε, p).

**Main claim:** Under current IBM noise levels (~1e-3), QAE's advantage threshold shifts significantly from the ideal case, placing it outside practical tolerances for near-term option pricing.

**Novel contribution:** No existing paper maps break-even vs noise rate for option pricing circuits.

---

### Paper B — *Fair Break-Even with Variance-Reduced MC* `[planned]`
> **Venue:** Physica A / Quantitative Finance

The QAE literature compares against naive Monte Carlo. Practitioners don't use naive Monte Carlo — they use antithetic variates, Black-Scholes control variates, and quasi-MC (Sobol sequences). This paper re-derives the break-even equation with the right baseline.

**Main claim:** When QAE is compared against variance-reduced MC — the method quants actually deploy — the advantage threshold increases significantly, making the case for near-term QAE weaker than previously reported.

**Novel contribution:** Methodological critique of the entire QAE option pricing literature. "You've been comparing quantum to the wrong thing."

---

### Paper C — *Unified Quantum Advantage Frontier* `[planned]`
> **Venue:** Quantum journal

Combine Papers A and B. One unified figure: the quantum advantage region as a function of (ε, noise rate p, MC variance reduction factor).

**Main claim:** Under joint realistic assumptions — variance-reduced MC and NISQ noise — quantum advantage in European option pricing requires ε < X on hardware with error rate p < Y.

**Novel contribution:** The unified honest framework the field has been missing.

---

## How it's built

```
app/
  app.py                  # Dash layout, callbacks, break-even chart
  precompute_qae.py       # 600-point grid generator
  assets/style.css        # Dark theme, WCAG AA, responsive
src/
  black_scholes.py        # Closed-form pricer
  classical.py            # Monte Carlo
  quantum.py              # QAE circuit (IQAE + Qiskit Finance)
data/
  qae_grid.pkl            # 600 points: S₀ × K × T × σ
tests/
  test_pricing.py         # 10 tests, composite health 10/10
```

**QAE grid:** 600 points = 5 S₀ × 5 K × 6 T × 4 σ  
**Runtime stack:** numpy, scipy, dash, plotly, gunicorn (no Qiskit at runtime)  
**Dev stack:** + qiskit, qiskit-finance, qiskit-algorithms  
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

**Break-even crossover:**

```
M_crossover = π√N / 1.96  ≈  1.604 × √N
```

At ε = 0.01: Monte Carlo needs N ≈ 38,416 samples. QAE needs M ≈ 314 oracle queries — a ~120x query reduction. The NISQ overhead band (100x–1000x gate overhead) shows why this advantage doesn't hold on today's hardware.

---

## References

- Woerner & Egger (2019). *Quantum risk analysis.* npj Quantum Information. [arXiv:1806.06893](https://arxiv.org/abs/1806.06893)
- Stamatopoulos et al. (2020). *Option pricing using quantum computers.* Quantum. [arXiv:1905.02666](https://arxiv.org/abs/1905.02666)
- Carrera Vazquez & Woerner (2020). *Efficient state preparation for quantum amplitude estimation.* [arXiv:2009.05756](https://arxiv.org/abs/2009.05756)

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
pytest tests/                 # 10 tests
mypy src/ app/                # type check
ruff check .                  # lint
```

---

## Project status

| Component | Status |
|---|---|
| Dashboard (BS + MC + QAE) | ✅ Live |
| Break-even visualizer | ✅ Live |
| Design system (WCAG AA) | ✅ Done |
| Health (pytest/mypy/ruff) | ✅ 10/10 |
| Paper A — noise sweep | 🔬 In progress |
| Paper B — fair MC baseline | 📋 Planned |
| Paper C — unified frontier | 📋 Planned |

---

<div align="center">

Built by [Prithvi](https://github.com/Prithvi8706) · VIT Chennai · 2026

*Quantum advantage is real. On current hardware, it's not here yet. This project shows both.*

</div>
