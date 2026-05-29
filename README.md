# Quantum Option Pricing

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Qiskit](https://img.shields.io/badge/Qiskit-0.45.3-6929C4?logo=ibm&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-4.x-008DE4?logo=plotly&logoColor=white)
![Railway](https://img.shields.io/badge/deployed_on-Railway-0B0D0E?logo=railway&logoColor=white)

**[Live Demo →](https://web-production-559db.up.railway.app)**

An interactive dashboard that prices European call options using three methods — Black-Scholes, Monte Carlo simulation, and Quantum Amplitude Estimation (QAE) — and lets you compare them side by side. Adjust stock price, strike, expiry, and volatility with sliders; Black-Scholes updates instantly, Monte Carlo animates through 15 log-spaced sample sizes from N=100 to N=50,000 so you can watch the confidence interval shrink, and the QAE result loads from a precomputed grid in under a millisecond.

---

## Live Demo

https://web-production-559db.up.railway.app

---

## The Three Methods

### Black-Scholes

The Black-Scholes formula gives an exact closed-form price for a European call option under the assumptions of geometric Brownian motion, no dividends, constant volatility, and continuous trading. It evaluates in under 1 ms and serves as the accuracy reference for the other two methods.

```
C = S₀ · N(d₁) − K · e^(−rT) · N(d₂)
d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)
d₂ = d₁ − σ√T
```

**Limitation:** Only applies to European options with no path-dependence.

### Monte Carlo

The Monte Carlo pricer simulates N stock price paths under geometric Brownian motion, computes `max(S_T − K, 0)` for each, and returns the discounted average payoff. The dashboard animates the estimate across 15 sample sizes (N = 100 → 50,000) so the O(1/√N) error decay is visible in real time. To halve the error you need four times as many paths.

`src/classical.py` uses `numpy.random.default_rng()` with fresh entropy on every call — intentionally non-reproducible. Pass a `seed=` argument for deterministic tests.

**Limitation:** Slow convergence; error stays high unless N is large.

### Quantum Amplitude Estimation (QAE)

QAE encodes the option payoff E[max(S_T − K, 0)] as a quantum amplitude using a `LogNormalDistribution` state-preparation circuit and a `EuropeanCallPricingObjective` payoff circuit. Iterative Amplitude Estimation (IAE) then recovers the amplitude with O(1/M) oracle query complexity — a provable quadratic speedup over classical Monte Carlo's O(1/√N).

**Honest note:** QAE on a statevector simulator is slower and less accurate than large-N Monte Carlo. This is expected — the simulator tracks 2^10 = 1024 amplitudes. The quadratic speedup is theoretically proven but only materializes on fault-tolerant quantum hardware. The dashboard shows theoretical convergence curves (O(1/√N) vs O(1/M)), not fake benchmarks.

The QAE results are precomputed offline (see [Precomputing the QAE Grid](#precomputing-the-qae-grid) below) and served from a lookup table at runtime.

---

## Local Setup

**Requirements:** Python 3.9+

```bash
git clone https://github.com/Prithvi8706/quantum_option_pricing.git
cd quantum_option_pricing

# Install runtime + dev dependencies (includes Qiskit for precompute and notebooks)
pip install -r requirements-dev.txt
```

`data/qae_grid.pkl` is committed to the repo, so you can skip precomputation and run the dashboard immediately:

```bash
python app/app.py
# → http://localhost:8050
```

If `data/qae_grid.pkl` is missing, the app refuses to start with a clear error message pointing you to `precompute_qae.py`.

### Exploration notebooks

```bash
jupyter notebook
```

Notebooks `01`–`04` cover Monte Carlo convergence theory, Black-Scholes derivation, QAE circuit construction step by step, and a full three-way benchmark.

---

## Precomputing the QAE Grid

`app/precompute_qae.py` computes IAE option prices over a 600-point parameter grid and writes results to `data/qae_grid.pkl`.

**Grid definition (600 = 5 × 5 × 6 × 4 combinations):**

| Parameter | Values |
|---|---|
| S₀ (stock price) | 80, 90, 100, 110, 120 |
| K (strike) | 90, 95, 100, 105, 110 |
| T (expiry, years) | 0.25, 0.5, 0.75, 1.0, 1.5, 2.0 |
| r (risk-free rate) | 0.05 (fixed) |
| σ (volatility) | 0.15, 0.20, 0.25, 0.30 |

**Run the full grid (~10 minutes):**

```bash
python app/precompute_qae.py
```

**Smoke-test with 3 representative points (~30 seconds):**

```bash
python app/precompute_qae.py --dry-run
```

The script is **resumable**: it loads any existing `qae_grid.pkl` at startup and skips keys that are already populated. If the process is interrupted, re-run the same command and it picks up from where it left off. Results are saved after each point, so no work is lost on a crash or `Ctrl-C`.

Each grid entry stores:

```python
{
    "price":          float,          # discounted expected payoff
    "conf_int":       (float, float), # IAE confidence interval
    "elapsed":        float,          # wall-clock seconds for this run
    "oracle_queries": int,            # IAE oracle call count (for speedup chart)
}
```

**If you change the grid constants** (add values to `S0_VALUES`, `K_VALUES`, etc.), delete `data/qae_grid.pkl`, re-run the script, and commit the new pkl before pushing. The app imports grid constants directly from `precompute_qae.py`, so slider snap points stay in sync automatically.

---

## Railway Deployment

The app deploys to Railway via GitHub push. Setup steps are one-time; after that, `git push origin main` is the only deploy action needed.

**How the deploy works:**

- `requirements.txt` contains only runtime dependencies (`numpy scipy dash plotly gunicorn`). Qiskit, Jupyter, and `tqdm` are in `requirements-dev.txt` and are not installed on the Railway dyno.
- `Procfile` starts gunicorn: `web: gunicorn app.app:server --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`
- Railway injects `PORT` as an environment variable; `app.py` reads it with `int(os.environ.get("PORT", 8050))` and binds to `0.0.0.0`.
- `data/qae_grid.pkl` is committed to the repo and loaded at startup. Precomputation does not run as a build step — it is too slow for CI.

**To redeploy after a code change:**

```bash
git push origin main
# Railway auto-deploys within ~2 minutes
```

**If you regenerated the pkl locally**, commit it before pushing:

```bash
git add data/qae_grid.pkl
git commit -m "data: regenerate QAE grid"
git push origin main
```

Railway is used instead of Render's free tier because Render spins down inactive dynos after 15 minutes. A judge visiting the URL after a break would wait ~30 seconds on a blank page — which is worse than the QAE latency problem the precompute design exists to solve.

---

## Running Tests

Tests cover Black-Scholes and Monte Carlo without any extra dependencies. The two quantum tests require Qiskit and are automatically skipped if it is not installed.

```bash
python -m pytest tests/ -v
```

| Test | What it checks |
|---|---|
| `test_bs_atm` | ATM price matches analytical value (~$10.45) |
| `test_bs_deep_itm` | Deep ITM price exceeds intrinsic value |
| `test_bs_deep_otm` | Deep OTM price is near zero |
| `test_bs_put_call_parity` | Put via C − P = S₀ − Ke^(−rT) parity |
| `test_bs_sigma_sensitivity` | Higher volatility → higher call price (vega > 0) |
| `test_mc_close_to_bs` | MC at N=20,000 is within $1 of Black-Scholes |
| `test_mc_err_decreases_with_n` | Standard error shrinks as N grows |
| `test_mc_nonnegative` | Option price is always ≥ 0 |
| `test_sigma_floor_clamps_below_015` | QAE clamps sigma < 0.15 (skipped without Qiskit) |
| `test_sigma_floor_passes_above_015` | QAE does not clamp sigma = 0.20 (skipped without Qiskit) |

---

## Project Structure

```
quantum_option_pricing/
├── app/
│   ├── app.py               # Dash layout, server callback, client-side animation
│   ├── precompute_qae.py    # Offline QAE grid generation (600 pts, resumable)
│   └── assets/style.css     # Dark theme
├── src/
│   ├── black_scholes.py     # Closed-form pricer (scipy.stats.norm)
│   ├── classical.py         # Monte Carlo pricer (GBM, non-reproducible by design)
│   └── quantum.py           # QAE pricer (IAE + Qiskit Finance); only called during precompute
├── data/
│   └── qae_grid.pkl         # Precomputed 600-point grid (committed to repo)
├── tests/
│   └── test_pricing.py      # BS, MC, and sigma-floor smoke tests
├── 01_classical_monte_carlo.ipynb
├── 02_black_scholes.ipynb
├── 03_quantum_pricer.ipynb
├── 04_comparison.ipynb
├── Procfile                 # gunicorn entry point for Railway
├── requirements.txt         # Runtime: numpy scipy dash plotly gunicorn
└── requirements-dev.txt     # + qiskit==0.45.3, qiskit-finance, qiskit-algorithms, jupyter, tqdm
```

---

## Open Items

- **Circuit diagram** — Out of scope. `src/quantum.py` builds the full Qiskit circuit; rendering it as a `circuit.draw()` PNG in the dashboard was explicitly deferred and is not needed for the demo.
- **Exhaustive QAE unit tests** — The sigma-floor tests require Qiskit installed locally. Full IAE round-trip accuracy tests are not included; each takes 30–300 seconds.
- **Slider resolution** — The QAE grid has 600 discrete points. Slider values that fall between grid points snap to the nearest neighbor; the dashboard shows a note when this happens (e.g., "Nearest match used: σ=0.20 (you selected 0.23)").
- **Real quantum hardware** — The quadratic speedup advantage of IAE is theoretical on a statevector simulator. Running on IBM Quantum hardware would demonstrate it on actual qubits but is outside the scope of this project.

---

Built with [Qiskit](https://qiskit.org) · [Plotly Dash](https://dash.plotly.com) · deployed on [Railway](https://railway.app)
