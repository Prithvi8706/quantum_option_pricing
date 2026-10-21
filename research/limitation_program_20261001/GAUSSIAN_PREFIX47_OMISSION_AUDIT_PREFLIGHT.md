# Exact-bin Gaussian omission audit preflight

Author-stage plan only. The smallest next A03 candidate parses the existing
q10 archive and certifies exactly its 47 absent rotation slots by an analytic
symmetry argument. It computes no Gaussian CDF values, conditional angles,
Walsh table, statevector, synthesis, full-loader error or financial price. Its
JSON companion names every absent slot by level, target, Gray index, Walsh mask
and the following archived CNOT's line/control. The inventory came from reading
the saved QASM and source text; there is no new executed audit receipt.

`gaussian_10.qasm` contains all 1,022 cyclic Gray CNOT slots and 976 RY rows. The
original `experiment_gaussian.prepare` visits index `i` with Walsh mask
`h=i xor (i>>1)`, emits an RY only when the floating Walsh value differs from
zero, and always emits the following CNOT at levels 1 through 9. These retained
CNOTs identify the 47 absences without regenerating any probability or angle.
Every absent slot's mask is nonzero and has even Hamming weight.

For the exact intended Gaussian bins, the boundaries are rational
`e_j=-6+12*j/1024`. The standard Gaussian density is positive and even, so exact
normalized bin masses obey `p_j=p_(1023-j)`. At level l the binary prefix j and
its bitwise complement `jbar=2^l-1-j` have reflected blocks and complementary
left conditional masses. With the archived convention
`theta_j=2*acos(sqrt(left_mass_j/total_mass_j))`, positivity and the principal
range `[0,pi]` imply `theta_j+theta_jbar=pi` exactly.

The archived in-place butterfly is the ordinary binary Walsh transform
`beta_h=2^-l sum_j theta_j*(-1)^popcount(j&h)`. Under prefix complementation,
the character is multiplied by `(-1)^popcount(h)`. For a nonzero even-weight h,
paired angles sum to pi and the nontrivial character sums to zero, hence
`beta_h=0` exactly. `beta_0=pi/2`; odd-weight masks have no zero conclusion.
The future independent audit checks this argument against the literal density,
bin construction, normalization, Ry convention, butterfly ordering and cyclic
Gray control-bit indexing, and binds each of the 47 absent masks to it.

This theorem concerns the exact intended bin law. The archived construction
converts 90-digit probabilities to binary64, uses numerical conditional sums
and arccos, and serializes approximate RYs to QASM. It does not establish exact
symmetry of the historical floating targets or accuracy of all QASM literals.
The QASM additionally has 740 emitted `ry(0)` rows: 455 at even-weight masks and
285 at odd-weight masks. They are distinct from the 47 absences; their literal
accuracy remains a separate defect ledger. No accuracy inference for those
740 rows follows from omission indexing, and no numerical regeneration is
included in this candidate.

After the fixed18 queue and `WAVE10_run001` reconciliation, author a fresh
independent read-only auditor with one 60-second CPU / 120-second wall budget,
45-second work-admission limit, one thread, no JIT cache and no retries. Freeze
its literal code, exact archived inputs, interpreter and dependency origins
before scanning. It must preserve all 47 records, verify the complete archived
Gray CNOT sequence, independently verify source conventions and the symbolic
argument, and emit a narrow omission-audit receipt or explicit terminal
rejection/censor. It imports no numerical Gaussian, Walsh, synthesis or producer
evaluation functions. It credits zero new pytest cases and no earlier fixtures.

Even a successful omission-only audit leaves the 1,020 other conditional-node
angle certificates, numerical/QASM approximation, phase-correct full loader,
complete error allocation and financial-law adoption unresolved. All 110
program obligations remain in scope; A03 would remain partial.
