# Audit C: optimized preparation for variational regression

Primary: [Perkkola et al., arXiv:2505.17713v1](https://arxiv.org/abs/2505.17713v1),
10 pages. All main text, Tables I/II, figure captions and Appendices A/B reviewed.
Our pricing problem does not become a variational regression task by using its
circuit-synthesis ideas. No hardware training experiment independently repeated.

## Equation ledger

| Eq. | Independent check / transfer requirement |
|---|---|
| 1 | Uniform superposition over K entries assumes power-of-two allocation or padding. Preparing exactly K arbitrary entries is not free. |
| 2 | Diagonal data-selected phase is a multiplexed Z rotation on the ancilla. Sparse projectors have a shared circuit structure worth compiling jointly. |
| 3 | Direct expansion gives opposite phases on the ancilla branches. Keep both, including any common phase when later controlled. |
| 4 | Projection produces -i*sin(x_k)/sqrt(K), up to a global phase. The normalized conditional state and its success probability are separate outputs. Small-angle approximation needs a quantitative bound. |
| 5 | Coefficient selection acts on columns; it is not a fresh loader for every row. |
| 6 | Ancilla tensoring does not remove earlier postselection cost. |
| 7 | Opposite coefficient phases lead to cosine after plus projection. |
| 8 | Projected output is unnormalized. Renormalizing without tracking branch mass changes the subsequent objective. |
| 9 | I+X is twice a projector; the observable's norm grows with column-register size. Shot complexity cannot be inferred from gate count alone. |
| 10 | Expand the squared column sum. The stated MSE relation assumes the intended data amplitudes and correct unnormalized weighting; dividing by cos(phi0) requires it nonzero. |
| 11 | The naive cost is a particular repeated controlled-gate decomposition, not a lower bound on state preparation. Its improvement is against that construction. |
| 12 | H squared is identity; cancellations require matching wires and intervening identities. |
| 13 | Hadamard conjugation maps Z to X; corresponding CNOT direction reversal needs Hadamards on both wires, not arbitrary one-wire pushing. |
| 14 | An affine bit permutation plus phase polynomial describes this gate set. Literal RZ conventions introduce a constant phase that must be retained for controlled equivalence. |
| 15 | Collect coefficients of the same Boolean parity; use consistent radians versus turns. |
| 16 | Inner product is modulo two, not ordinary real multiplication/summation. |
| 17 | The CNOT convention has the second written bit controlling the first. Account for this before translating to Qiskit wire order. |
| 18 | Parenthesize XOR: theta*(x0 XOR x1), not an XOR involving a real coefficient. |
| 19 | Add the contributions from each rotation with signed coefficients. Include the RZ constant-phase term in an exact-unitary implementation. |
| 20 | Folding identical parities preserves the unitary when the phase convention is consistent; do not certify it only by measurement counts. |

## Loading mathematics and a bounded repair

For normalized real data f, the small-angle branch is
`b_k=sin(f_k)/sqrt(K)` and `p_success=sum(sin(f_k)^2)/K`, approximately 1/K.
Preparing conditional states therefore costs about K attempts, not one. A
coherent amplitude-amplification implementation changes that scaling but adds
preparations/inverses/reflections and still needs an error/failure analysis.

For a probability target p_k, choose a known envelope B>=max(sqrt(p_k)) and
`x_k=arcsin(sqrt(p_k)/B)`. Then the **same mathematical projection gadget** gives
exact conditional amplitudes sqrt(p_k) and success `1/(K*B^2)` in real arithmetic.
This removes the small-angle bias; arbitrary angle-table construction and loading
still cost O(K) (plus classical transform cost). It is standard transduction,
not a claimed new algorithm. Generic spiky data can still have success 1/K.

For one of our truncated Gaussian marginals with K cells across [-L,L],
`K*p_max -> 2L*phi(0)/Pr(|Z|<=L)` as the grid refines. Thus the best envelope
success tends to `Pr(|Z|<=L)*sqrt(2*pi)/(2L)`, about 0.3133 at L=4, rather than
1/K. Independent numeric branch calculations confirm this at q2,4,6,8,10.
Do not multiply four marginal successes and silently postselect the joint
40-qubit state: that would reintroduce a dimension-dependent penalty. Per-register
coherent amplification could avoid that product but must be explicitly built.
The present deterministic multiplexer avoids the issue altogether.

## Why we transferred compilation, not the regression algorithm

Known uniformly controlled rotations combine all mutually exclusive prefix
rotations of the Gaussian tree. For angles theta_k, a cyclic Gray-code sequence
uses coefficients

`alpha_j = 2^-l * sum_k (-1)^popcount(k & gray(j))*theta_k`.

For each fixed control word, the CNOTs flip the target and hence alternate
rotation signs. Orthogonality of the Walsh transform recovers the selected
theta_k; the cyclic CNOT sequence returns the target parity to zero. This proves
the entire multiplexer identity, not merely one prepared state. No postselection
or dense joint path table is required. Applying it to q-bit marginal trees costs
at most 2^q-2 CNOTs per marginal. It is still exponential in **marginal precision
bits**, and linear in the number of independent marginals—not poly(q) loading.

Our final compiler computes coefficients from exact rational representations of
the old stored float angles. The implemented float rotations receive a separate
operator-error bound; this is why the old loader certificate is reusable with a
small added error. This application is implementation improvement, not novelty
in the Gray-code/Walsh synthesis technique.

## Experimental claims and comparison limits

The paper executes an eight-qubit model on IQM hardware with optimization and
postprocessing, but its classical comparator performs better. Its elementary
gate reduction does not eliminate rejected shots, training iterations, gradient
circuits, readout calibration, routing or communication. Classical shadows do
not create missing successful preparation shots for free. Any shadow-based
claim also needs the relevant observable norm and estimator variance.

Theoretical regression complexity must include data access, normalized loss
precision, postselection, optimizer iterations and reading the answer. Comparing
O(K) circuit gates against O(KM) classical work without matching those quantities
does not establish practical advantage. For this project, retain classical
control-variate fitting unless a separately verified benefit warrants replacement.
