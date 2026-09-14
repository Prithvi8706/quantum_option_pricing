# Week 3 larger-register logical resource protocol

Discovery only. Profile E001/E014/E025/E049 at n=5/6, payoff scale .125,
Grover k=0/1; additionally E001 at scale .25 (20 circuits). These are the
four contracts with dollar-feasible representations in the earlier grid study;
not every n/scale in this matrix is itself dollar-feasible. Save each bound.

First run E001/n5/.125/k0 as a time/memory smoke. Continue only if its
build, compilation and ideal simulation finish within 120 seconds and its
estimated dense state storage is below 16 MiB. The full run has a 15-minute
between-case time limit. No density matrices, noise or hardware jobs here.
Memory figures are array-size estimates, not measured peak process memory.

Use the previously validated full-register Grover construction, u/cx basis,
optimization level zero, seed 317, no device topology. Compare every ideal
statevector marginal with the analytic amplified grid objective at 1e-9.
Archive sources, QPY, per-case timing, gates and depth; preserve failures.
These logical counts do not establish speedup or hardware feasibility.
