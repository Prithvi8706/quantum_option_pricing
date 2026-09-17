# Audit B: quantum arithmetic and resource estimation

Primary: [Fedoriaka et al., arXiv:2509.07015v1](https://arxiv.org/abs/2509.07015v1),
7 pages, all sections and figure/caption/table material read. Formulae are mostly
unnumbered; locations below identify them. No Azure estimates rerun.

## Formula ledger and independent interpretation

| Location | Check / required correction before use |
|---|---|
| II-A in-place sum | Arithmetic is modulo 2^n. A signed fixed-point interpretation is extra structure; overflow must be excluded or explicitly modeled. |
| II-A out-of-place sum | The displayed zero-target action specifies only a subspace. Our coherent oracle needs a reversible extension and clean workspace. |
| II-A constant sum | Constants reduce modulo 2^n; exploit classical constants rather than allocate a second full quantum input. |
| II-A radix choice | The chosen radix is an experimental algorithm parameter, not a hardware-independent optimal value. |
| II-B product | n+n input bits and 2n result bits represent exact unsigned multiplication. Truncating fixed-point products requires a separate error bound and reversible discarded bits. |
| II-C division display | As printed, output uses a/c although the retained divisor is b. The map on arbitrary c is not a valid complete unitary specification. Do not copy it as an oracle contract. |
| II-C subtraction | Bitwise-complement identity gives modular subtraction; it does not by itself establish signed overflow behavior. |
| II-D ModExp display | The repeated U on the displayed RHS is a notation problem; the intended clean-target output is a^x mod N. Modular exponentiation is not real exp(log-price). |
| II-D window rule | Rounded 2*log2(n) is a fit-driven heuristic, not universally optimal. Our tiny fixed-point widths are not that experiment. |
| III-B width grid | Geometrically spaced bit counts explore resource scaling; a finite-range regression does not prove an asymptotic complexity class. |
| III-B constants | Verify constants are reduced to the chosen register width, especially the displayed alternating-bit constant near the boundary. Fixed constants can favor particular designs. |
| IV-D runtime model | Differentiate n*(c1*2^w+c2*n^2)/w: stationarity is c1*2^w*(w*ln2-1)=c2*n^2. Integer search and valid window bounds still required. |
| IV-D optimum notation | Minimizing runtime requires argmin; the printed argmax statement is inconsistent with the surrounding objective. |
| IV-F fitted slopes | Physical runtime includes code-distance/factory effects; a slope above a logical complexity exponent is not automatically an algorithmic violation. |
| IV-G cleanup | Compute-copy-uncompute preserves basis functions coherently. A reset of entangled garbage is not a valid substitute. Measurement-assisted uncomputation needs its correction/feed-forward contract. |

From the stationarity equation, the leading estimate 2*log2(n) has logarithmic
corrections and coefficient dependence. It cannot be imported as a theorem that
the paper's heuristic minimizes every resource model. Similarly, a multiplier
crossover at thousands of bits says little about tens-of-bits payoff arithmetic.

## Methodology audit

Compare Pareto points only under the same physical error rates, code, tolerated
failure budget, instruction times and available factories. The paper's estimates
use a specific default hardware model and error budget 0.001; those defaults are
not a hardware result for our application. A compiler scheduling model can mask
algorithmic parallelism. Neither T-count nor T-depth alone is runtime.

For an AE oracle define a cost ledger containing `A`, `A^-1`, predicate phase,
zero reflection and classical setup. If arithmetic keeps garbage, invert all of
it; if it cleans garbage before measuring a flag, count that cleanup. Do not
double count a cleanup already included inside A, nor omit its inverse on the
assumption that 'garbage is not measured'. Keep live width and depth separately.

Our current QSP signal largely avoids arithmetic, so replacing its non-existent
multiplier produces no savings. Arithmetic selection instead matters to the
explicit-payoff competitor and any genuinely log-domain autocallable branch.
Shor-style ModExp optimizations are not relevant to computing a financial
exponential with specified absolute error.

## Author-code inspection and phase test requirement

Pinned `fedimser/quant-arith-re` commit
`cc31e48d0eb62ab5b4f7893501b2ca36e584be95`:

- `ConstAdder.qs`: constant reduction, trailing-zero removal, controlled paths,
  overflow/comparison routines, and use of AND/adjoint AND inspected. This is
  not a verification of every transitive primitive or installed Q# version.
- `re_utils.py`: reads/caches estimated physical quantities and fits log-log
  trends. Its cache key is operation/width in the inspected helper; our archive
  must additionally freeze hardware parameters, compiler and source identity.
- `superposition_test_utils.py`: inspected tests compare marginal probabilities
  after taking absolute squares. This can detect wrong arithmetic outcomes but
  does not certify relative phases or correlations with retained inputs.

Independent counterexample: a correct permutation U and D*U, with nonconstant
diagonal phases D, produce identical computational-basis probabilities on each
output but differ coherently. Hence our acceptance tests require full operators
on bounded widths, entangled inputs or inverse/interference checks. The new
loader checks controlled full operators and inverses for precisely this reason.

Decision: adopt cost-accounting and width-specific selection discipline. Do not
claim a new multiplier, executed physical resource reduction, or pricing
advantage from this paper. Adding an arithmetic backend needs dedicated signed,
fixed-point, controlled and uncomputation validation before admission.
