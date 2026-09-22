# Exploratory checks fixed before execution

Search/execution date: 22 September 2026. These checks do not open confirmation.
Preserve the manuscript and all existing evidence. The root GBM script refuses
overwrite. Reviewer scripts regenerate only their adjacent new outputs; preserve
those outputs before a timing rerun. Existing project archives are unchanged.

1. Replay the existing classical GBM implementation on D1, D2, and two explicitly
   exploratory extensions: 4 assets x 12 dates and 8 assets x 52 dates, spot 100,
   strike 100, sigma .3, equicorrelation .4, rate .03, maturity 1.
2. Independently fit geometric controls on 1,024 paths. Run antithetic MC and
   PCA scrambled Sobol at 256, 1,024, 4,096 paths per replicate, 16 independent
   replicates, deterministic seeds in the script. Include existing conditional
   integration for D1/D2. Charge setup, fitting and sampling. Limit BLAS to one
   thread. Keep every result; no claim of strongest-classical optimality.
3. Compute a D1 one-dimensional conditional quadrature reference, explicitly
   reporting its non-rigorous numerical error estimate. For larger cases report
   precision diagnostics and sample-size stability, not true error or coverage.
4. Separately test the Wang--Kan single-asset 256-step weak-Euler Heston Asian
   discrete target with a bounded script by the stochastic-volatility reviewer.
   State target/payoff cap/model and no continuous-time accuracy guarantee.
5. Derive required quantum throughput/depth thresholds from complete existing
   ledgers and explicit hypothetical layer times. They are engineering screens,
   not lower bounds for every quantum algorithm or actual hardware timings.

This is a low-cost falsification screen. A favorable empirical interval cannot
establish a confidence guarantee, and a unfavorable existing implementation
cannot establish impossibility of a future quantum method.
