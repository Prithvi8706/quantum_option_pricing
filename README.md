# Quantum Option Pricing

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Qiskit](https://img.shields.io/badge/Qiskit-1.x-6929C4?logo=ibm&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-4.x-008DE4?logo=plotly&logoColor=white)
![Railway](https://img.shields.io/badge/deployed_on-Railway-0B0D0E?logo=railway&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-22c55e)

**[Live Demo →](https://quantum-option-pricing.up.railway.app)**

An interactive benchmark of three approaches to pricing European call options: the exact **Black-Scholes** formula, a **Monte Carlo** simulation that animates convergence in real time, and **Quantum Amplitude Estimation (QAE)** via Qiskit. The dashboard lets you explore how each method performs across a wide parameter grid — and makes the theoretical quantum speedup concrete and visible.

---

## The Core Idea

Pricing a European call requires computing an expectation value E[max(S_T − K, 0)] under the risk-neutral measure. Classical Monte Carlo estimates this by averaging N sampled paths and converges at O(1/√N) — to halve the error you need four times as many samples. QAE encodes the same expectation as a quantum amplitude and recovers it with Iterative Amplitude Estimation, converging at **O(1/M)** in oracle calls — a provable quadratic speedup in query complexity.

The catch (acknowledged honestly in the UI): this implementation runs on Qiskit's statevector simulator, which is exponentially slow on classical hardware. The advantage lives in oracle call counts, not wall-clock time. That gap closes on real quantum hardware.

---

## Three Methods Side by Side

| | Black-Scholes | Monte Carlo | Quantum (QAE) |
|---|---|---|---|
| **Approach** | Closed-form analytic solution | Simulate N GBM paths, average payoffs | Encode payoff as amplitude, extract with IAE |
| **Convergence** | Exact | O(1/√N) | O(1/M) oracle calls |
| **Speed** | < 1 ms | ~50–500 ms (N=50k) | ~150 ms (pre-computed, statevector) |
| **Error** | Zero | Stochastic, with 95% CI | Bounded by ε target (set to 0.01) |
| **Limitation** | European options only; no path-dependence | Slow convergence, high variance at small N | Requires quantum hardware for real advantage |

---

## Architecture Decisions

**Precomputed QAE grid.** Running IAE inside a web callback would block the server for 100–300 ms per call. Instead, `app/precompute_qae.py` computes all 600 parameter combinations offline (5 S₀ × 5 K × 6 T × 4 σ) and stores results in `data/qae_grid.pkl`. Runtime lookup is O(1). The script is resumable — it skips already-computed keys — and handles edge cases where deep OTM/ITM strikes fall outside the log-normal support domain by clamping bounds to always include K.

**Keyframe MC animation.** Rather than showing only the final answer, the Monte Carlo card animates convergence through 35 log-spaced steps from N=100 to N=50,000, driven by a `dcc.Interval` ticker. This makes the O(1/√N) error decay visible. Animation only triggers on slider interaction — page load shows a static dark placeholder with zero computation.

**Zero-cost initial render.** All three cards are populated from the layout's HTML before any callback fires: BS price and QAE result are baked in at server startup (both sub-millisecond). The MC chart renders a dark-themed placeholder figure with a dashed BS price line. No blocking work happens at startup or on page load.

**Honest simulator tradeoffs.** The scatter plot charts error vs compute time for all three methods. QAE oracle call counts are derived from IAE round powers (∑(2k+1)) rather than wall-clock time, since the statevector sampler makes wall-clock comparisons misleading. This separates quantum query complexity from classical simulation overhead.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Quantum circuit | Qiskit 1.x, `qiskit-algorithms` (IAE), `qiskit-finance` (LogNormalDistribution, EuropeanCallPricingObjective) |
| Classical pricing | NumPy (GBM paths), SciPy (Black-Scholes CDF) |
| Dashboard | Plotly Dash 4.x, Plotly, custom CSS (dark theme, rc-slider overrides) |
| Deployment | Gunicorn (1 worker, 120s timeout), Railway |
| Offline precompute | `app/precompute_qae.py` with `tqdm` progress and resumable pkl |

---

## Running Locally

```bash
git clone https://github.com/Prithvi8706/quantum_option_pricing.git
cd quantum_option_pricing
pip install -r requirements.txt

# Precompute QAE grid (~2 min, skips already-done keys)
python app/precompute_qae.py

# Launch dashboard
python app/app.py
# → http://localhost:8050
```

The precomputed grid is committed to the repo (`data/qae_grid.pkl`), so you can skip the precompute step and run the dashboard immediately.

For the exploration notebooks:

```bash
pip install -r requirements-dev.txt
jupyter notebook
```

Notebooks 01–04 cover MC theory and convergence, Black-Scholes derivation, QAE circuit construction step-by-step, and a full three-way benchmark.

---

## Project Structure

```
quantum_option_pricing/
├── app/
│   ├── app.py               # Dash dashboard (layout, callbacks, figures)
│   ├── precompute_qae.py    # Offline QAE grid generation (600 pts)
│   └── assets/style.css     # Dark theme
├── src/
│   ├── black_scholes.py     # Closed-form pricer
│   ├── classical.py         # Monte Carlo pricer (GBM)
│   └── quantum.py           # QAE pricer (IAE + Qiskit Finance)
├── data/qae_grid.pkl        # Precomputed 600-point grid
├── 01_classical_monte_carlo.ipynb
├── 02_black_scholes.ipynb
├── 03_quantum_pricer.ipynb
├── 04_comparison.ipynb
└── Procfile                 # gunicorn entry point for Railway
```
