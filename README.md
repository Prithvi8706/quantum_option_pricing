# Quantum Option Pricing

## Overview

This project benchmarks **Quantum Amplitude Estimation (QAE)** against **Classical Monte Carlo simulation** and the exact **Black-Scholes formula** for pricing European call options. By encoding the risk-neutral payoff distribution into a quantum circuit, QAE achieves a quadratic speedup in the number of oracle calls relative to classical Monte Carlo — converging at O(1/M) instead of O(1/√N) — making it a compelling candidate for near-term quantum advantage in computational finance.

## Project Structure

```
quantum-option-pricing/
├── src/
│   ├── __init__.py          # Package init
│   ├── classical.py         # Monte Carlo pricer (geometric Brownian motion)
│   ├── black_scholes.py     # Exact Black-Scholes analytical formula
│   └── quantum.py           # Quantum Amplitude Estimation pricer (Qiskit Finance)
├── 01_classical_monte_carlo.ipynb   # MC theory, implementation, convergence plot
├── 02_black_scholes.ipynb           # BS formula, price vs spot curve
├── 03_quantum_pricer.ipynb          # QAE theory and implementation walkthrough
├── 04_comparison.ipynb              # Side-by-side benchmark of all three methods
├── requirements.txt
└── README.md
```

| File | Purpose |
|---|---|
| `src/classical.py` | `monte_carlo_call` — simulates N GBM paths and returns price + standard error |
| `src/black_scholes.py` | `black_scholes_call` — closed-form price via `scipy.stats.norm` |
| `src/quantum.py` | QAE implementation using `qiskit_finance` and `qiskit_algorithms` |
| Notebooks 01–02 | Self-contained explorations of the classical methods |
| Notebook 03 | Step-by-step quantum circuit construction and simulation |
| Notebook 04 | Convergence rate and accuracy comparison across all methods |

## Installation

```bash
pip install -r requirements.txt
```

Python 3.9+ is recommended. For GPU-accelerated simulation, install `qiskit-aer` separately:

```bash
pip install qiskit-aer
```

## Usage

```python
from src.classical import monte_carlo_call
from src.black_scholes import black_scholes_call

S0, K, r, sigma, T = 100, 105, 0.05, 0.2, 1.0

price_bs = black_scholes_call(S0, K, r, sigma, T)
price_mc, std_err = monte_carlo_call(S0, K, r, sigma, T, N=100_000)

print(f"Black-Scholes : {price_bs:.4f}")
print(f"Monte Carlo   : {price_mc:.4f} ± {std_err:.4f}")
```

Launch the notebooks for guided walkthroughs:

```bash
jupyter notebook
```

## Roadmap

- **Asian options** — path-dependent payoffs via time-averaged spot price encoded in the quantum state
- **VarQITE for exotic options** — Variational Quantum Imaginary Time Evolution to prepare thermal/risk-neutral states for barrier, lookback, and other exotic payoff structures
- Multi-asset correlation via entangled log-normal distributions
- Benchmarking on real quantum hardware via IBM Quantum
