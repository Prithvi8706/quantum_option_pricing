# Combined quantum development protocol v1 — 2026-09-17

User authorized bounded integration of representation discovery, QSP/loading,
and repeated-workload reuse. This protocol precedes the combined acquisition.
No confirmation seeds, physical jobs, paid services or old producers are changed.

## Fixed scope

Original two-asset/two-date GBM business contract. Finite development cube L4,
q2 per normal (256 paths), strikes90/95/100/105/110. Feature discovery uses
strike100 only and128 uniformly selected training path indices. Remaining128
indices measure representation generalization. Per-strike coefficients may be
refitted on training indices, with all labels/refits charged. Strikes95/105 are
feature-transfer diagnostics, not untouched statistical confirmation.

Quantum feature discovery is **Fourier sampling**, inspired by parity discovery
but not an implementation of IonQ's variational algorithm. Prepare normalized
training-weighted centered payoff amplitudes, apply H to all path bits, sample
Walsh words. Finite amplitude preparation reads the training vector; its table,
normalization and circuit cost are paid. Classical exact fast Walsh transform
gets precisely the same input; weighted greedy parity selection searches the
full candidate pool. Include a fitted geometric control baseline. Select four
nonconstant parity words. Quantum sampling:256and1024shots, eight repetitions.
This small fully classically tractable study cannot demonstrate quantum speedup.

QSP approximates absolute value, expressing a call as
D*B/2*(x+abs(x)), x=(basket-K)/B with fixed B from the finite table for this
prototype. Truncated even Chebyshev degrees4and8, rescaled into[-1,1], are
synthesized with bounded least-squares attempts (three fixed initial seeds,
maximum1500function evaluations). Record every attempt and failed fit. The
analytic truncation bound is separate from sampled phase-fit error, which is
not a uniform numerical certificate. Real QSP signal/phase circuits and inverse
are checked against scalar evaluation. The signal itself uses a fully paid
finite UCRY table; **no scalable basket signal oracle is claimed**.

Compose the signed QSP call and parity control into an LCU block using absolute
coefficient weights. Its normalization beta=sum(abs(coefficients)) is charged.
Test expectation recovery and clean PREP/SELECT/PREP-inverse semantics through
a controlled block/Hadamard test on a smaller q1,16path smoke case to bound
simulation cost. The q2 workload uses the same algebra for a prospective cost
screen; it is not a large integrated hardware run. LCU's extra normalization
can erase variance gains. Compare raw and controlled beta, not RMSE alone.

Loader component: TT-SVD/MPS compression diagnostics on the1024entry(q10)
normal amplitude vector for bonds1/2/4/8. Report reconstruction errors and tensor
parameter counts. No MPS circuit synthesis, statevector error certificate or
automatic admission is inferred from these diagnostics.

Reuse:1/5/25/100valuations. Quantum and classical methods both amortize feature
discovery and the unchanged probability loader; per-strike labels, fits, payoff
signal construction, measurements and residual estimation remain payable.
Record setup and recurring units separately. Do not sum simulator seconds with
logical gates or assign a hypothetical QPU clock rate as measured runtime.
Gate-weighted critical-path diagnostics use explicitly illustrative durations,
not a named hardware calibration. No observed standard deviation is an RMSE
certificate. Sampled price observations, if included, target the finite model.

## Research sources and integration decisions

- IonQ parity discovery: https://arxiv.org/html/2605.11213v1 — motivates
  representation discovery and classical shadow deployment, with full-pool
  classical search retained here. Fourier sampling is a different algorithm.
- IonQ/Synopsys workflow: https://arxiv.org/html/2603.15515v1 — motivates
  paying/amortizing setup while measuring downstream benefit.
- QSP pricing: https://arxiv.org/html/2307.14310v2 — motivates payoff amplitude
  transforms; its resource reductions cannot be assigned to our basket for free.
- MPS normals: https://arxiv.org/html/2303.01562v2 — compression/error tradeoff.
- QCE25, Tremba/Liu/Hovland: https://arxiv.org/abs/2505.16908 and official
  program https://qce.quantum.ieee.org/2025/wp-content/uploads/sites/12/2025/09/QCE25-Technical-Paper-Sessions.pdf
  — gate-aware depth, not unweighted depth as runtime.
- QCE26 magic-informed architecture search: https://arxiv.org/abs/2605.03932
  — non-Clifford resources are informative but magic alone is not application
  advantage; no architecture-search replication in this bounded study.
- QCE26 displacement-signal decision making: https://arxiv.org/abs/2601.16081
  — coherent signal-access assumption does not supply our digital payoff oracle;
  not a drop-in pricing implementation.
- QCE25 state preparation, ORNL author record:
  https://impact.ornl.gov/en/publications/optimizing-state-preparation-for-variational-quantum-regression-o/
  — supports explicit loading-cost attention; no unverified speedup imported.

Success is a reproducible composition/ablation with an honest advantage screen,
not a mandatory positive result. Complete mathematical bias, scalable oracle,
strong continuous comparators and human protocol review remain admission gates.
