# Audit D: the missing Walsh constant phase

Primary author version: [Pellini and Ferrari Dacrema,
arXiv:2502.05193v1](https://arxiv.org/abs/2502.05193v1), 4 pages. The arXiv record
links QCE DOI 10.1109/QCE65121.2025.00039. Publisher title is *On the Correct
Implementation of the Walsh Series Loader*. All author-version text and figure captions
reviewed; the six-page publisher PDF could not be retrieved, and has not been
certified equivalent. Equation numbering below is **preprint numbering**.

## Equation ledger

| Eq. | Independent check / transfer requirement |
|---|---|
| 1 | The printed normalization starts its sum at i=1 while the vector starts at zero; use all entries. Otherwise a vector supported only at zero is undefined. |
| 2 | Complete Walsh expansion requires an orthonormal discrete convention; truncated expansion needs its own approximation bound. |
| 3 | With zero-based bit indices the displayed k_(n-j) is out of range at j=0. Define bit reversal explicitly rather than copy the index literally. |
| 4 | For M<N, identify which grid points are sampled. The author code uses strided samples f[::N/M], not simply the first M entries of the original grid. |
| 5 | Walsh diagonal factors commute. Their product equals the diagonal exponential of the reconstructed function, including the constant. |
| 6 | Tensor ordering is bit-reversed relative to the transform convention. Check basis states before synthesizing. |
| 7 | A zero exponent is identity, one is Pauli Z. |
| 8 | A parity CNOT ladder collects the active support onto one target; it must have an inverse. |
| 9 | Conjugating one Z by that ladder gives the desired Pauli string. Check control/target direction and register width. |
| 10 | For nonempty support, exponentiating the parity Z uses RZ(2*a), including its phase convention. |
| 11 | Empty support gives a scalar phase; once controlled it becomes a relative phase on the control. It cannot be dropped. |
| 12 | Target normalization uses every grid entry; zero-norm inputs require rejection, not division by zero. |
| 13 | Two ancilla branches before interference are both necessary to derive success; one cannot normalize the good branch prematurely. |
| 14 | Omitting h=0 exponentiates f-a0 rather than f. Ancilla P(-epsilon*a0) restores the intended controlled exponential. |

Unnumbered infidelity expression is phase-insensitive. Full controlled-unitary
equivalence is stronger. Epsilon0, series truncation epsilon1, normalized-state
error and success probability are different quantities and must remain separate.

## Independent branch derivation

Start data in a uniform superposition and control exp(-i*epsilon*f(k)) by an
ancilla in |+>. After H and P(-pi/2) on the ancilla, its successful branch is

`b_k = exp(-i*epsilon*f(k)/2)*sin(epsilon*f(k)/2)/sqrt(N)`.

Consequently `p_success = mean(sin(epsilon*f/2)^2)`. The **k-dependent phase**
must be included when comparing statevectors. Discarding it while checking only
amplitude magnitudes overstates correctness. Small epsilon improves the
conditional approximation but reduces success quadratically.

If a0 is omitted, replace f by f-mean(f). For a constant nonzero target this
gives exactly zero success probability. For a varying positive target it can
produce a largely orthogonal state, even as epsilon tends to zero. The local
probe confirms this and records both fidelity and expected attempts.

Do not conclude from difficult GHZ examples that entanglement alone diagnoses
loader complexity. A GHZ state has a short dedicated circuit. Also distinguish
the Pauli string w_h, a tensor product, from its exponential W_h: the latter
can entangle. For example exp(-i*pi*Z⊗Z/4)|++> has nonzero determinant in its
two-by-two amplitude matrix and is maximally entangled. The relevant restriction
is the selected truncated Walsh family, ordering and approximation regime.

## Source-code and experimental audit

Author notebook inspected at `qcpolimi/WSL` commit
`9f4e633fb8a1acf2ea9fa8b288105545302a98ff`; no code imported or executed.
It includes the h=0 phase explicitly and strided coefficient sampling. Its
postselected state calculation divides by successful-branch norm. That makes
conditional fidelity measurable but does not account for the preparation rate.
Its dense Walsh matrix and full operator simulation are small-example reference
techniques, not scalable algorithms. A fast Walsh transform could reduce
classical preprocessing, but cannot remove arbitrary classical data access.

The notebook's circuit uses controlled parity operations. One can often share
compute/uncompute work across parity gadgets, but must prove exact controlled
equivalence before claiming reduced counts. Its AGPL license was not used as
permission to incorporate source into this project: all new code is independently
written from mathematical identities and standard synthesis.

## Decision for the basket project

Keep the zero-phase correction as a mandatory correctness rule for controlled
LCU/QSP/loading transformations. Our new tests compare controlled operators and
include a phase-insensitive-fidelity counterexample. Do not replace the existing
certified product-normal loader with a truncated probabilistic WSL on the basis
of fidelity plots alone. Require success-aware cost, cell-mass target fidelity,
price-level error, coefficient-generation cost and a deterministic/coherent
preparation contract. No such superiority was established here.
