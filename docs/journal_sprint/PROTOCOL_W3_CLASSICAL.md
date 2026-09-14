# Week 3 classical baseline protocol

Discovery smoke, not a speedup claim. European C6 plus arithmetic Asian call
S0=K=100,r=.05,sigma=.2,T=1, monitoring at j*T/d for d=8,32 (exclude time zero).
Methods: plain MC, independent-pilot CV MC, scrambled Sobol RQMC with PCA
Brownian construction. European control is discounted terminal stock (known
mean S0); Asian control is discounted geometric call with discrete closed form.
Asian RQMC also uses this independent-pilot geometric control.

Budgets: 4096/16384 evaluation paths, 10 independent repetitions. CV pilot 1024
extra paths, counted; RQMC uses exactly 32 independent scrambles, respectively
128/512 points each. Save every scramble mean, pilot coefficient, sample moments,
seed namespace, path count and timing. Do not call per-scramble points total N.

European references: Black–Scholes plus independent adaptive quadrature of the
normal-shock payoff. Asian reference: independent 32 scrambles x 16384 paths,
geometric control fitted from independent 4096-path pilot. Its standard error is
recorded; it is not exact truth. Asian errors against it are reference deviations,
not verified coverage. Reference generation precedes estimator trials.

Intervals use Student t on iid path values for MC or independent scramble means
for RQMC; they are approximate, not finite-sample exact. This ten-repetition smoke
tests plumbing and resource accounting, not 95% reliability. Record estimated
SE, radius and actual European error. All outputs exclusive, planned before runs.
Local compute only; no quantum or practical runtime-advantage comparison.
