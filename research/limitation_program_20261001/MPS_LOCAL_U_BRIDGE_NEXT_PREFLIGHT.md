# Next bounded MPS SDK bridge preflight

Author-stage plan only, after fixed18 and the prospective `WAVE10_run001`
cumulative reconciliation. No new implementation, preparation, SDK call,
matrix/Gram/overlap evaluation, native emission, test or synthesis occurs here.
All completed MPS structural/component helpers, tests, preflights and
`A04_mps_run001` artifacts remain immutable. The JSON companion binds the exact
saved inputs and distinguishes the next local bridge probe from a possible
later bond8 method.

The completed component screen passed 16 fixtures and retained every outcome.
Bond2 emitted ten local SDK blocks and 144 native rotations but had no eligible
component row. Bond4 stopped at SDK translation from `u,cx` to `ry,rz,cx`.
Bond8 stopped in right canonicalization at the fixed `1e-12` rank threshold;
it has saved compressed cores and compression bounds, but no canonical cores
or structure plan. These failures receive no retry or revised completion.

The next probe uses exactly the first saved eight-dimensional bond4 transition:
`A04_mps_run001/bond4/structure_plan.json`,
`transitions[1].completed_local_matrix`. It is an 8-by-8 matrix with 64 saved
complex-rational entries, site1, left rank2/right rank4 and physical local
wires `[10,11,8]`. Its canonical literal fingerprint is
`4f91a35a9d13366d3e02b79d23271f581dc30514a946155598950a3632415066`.
Do not complete a new matrix, select another site after a failure or rebuild
the Gaussian/SVD/canonicalization pipeline.

Use one pinned local SDK call with `UnitaryGate(check_input=True)`, basis
`[u,cx]`, optimization level0 and seed0. The installed Qiskit0.45.3 U matrix is

`U(theta,phi,lambda) = exp(i*(phi+lambda)/2) Rz(phi) Ry(theta) Rz(lambda)`.

Thus the chronological native replacement is `Rz(lambda)`, `Ry(theta)`,
`Rz(phi)`, with scalar phase `(phi+lambda)/2`. Convert each finite SDK parameter
to its exact binary64 rational first; add phases as exact rationals, including
the SDK circuit's own saved global phase. Preserve the original gate order,
wire map, all three angles of every U and all CX rows. Do not prune tiny angles
or reduce phases using rounded pi. Reject any other SDK operation. Store the
aggregate exact phase and its full provenance; the literal inverse negates it
and every rotation angle while reversing all gate rows.

Certify all 64 entries of the complete native local operator against the saved
matrix with 160-digit outward interval arithmetic and a 256-bit outward root.
The squared Frobenius residual uses exact-rational target entries, all Ry/Rz
entries and the full scalar phase. No column-only comparison, fidelity test,
phase minimization or floating SDK unitarity predicate can replace it. The
local residual must be at most `1/74880000000`, the tightest old scalar target
divided by four and ten. This is a narrow bridge threshold; a later complete
loader still pays its norm/gauge, completion, per-block SDK error, compression
and table error separately. Any controlled use must implement and charge the
recorded scalar phase on the controlling register in its later synthesis
ledger. No phase contribution or controlled cost is declared free.

The fresh local receipt is provisionally `A04_mps_u_bridge_run001`, with one
matrix and one SDK call, three local wires, at most 1,024 SDK U/CX rows and
4,096 native primitive slots including the aggregate phase. Its whole producer
budget is CPU120 seconds, admission90 seconds, wall300 seconds and one thread.
A separate fresh independent auditor has CPU120/admission90/wall300 and zero
SDK calls or new test credit. It reconstructs every exact U conversion and
wire, expands both original U/CX and native Ry/Rz/CX operators independently,
checks the aggregate phase, all full-matrix residual entries, the inverse
contract and all frozen source/installed-package bindings. Freeze both new
implementations before any work; ordinary unsupported results and global
censors remain terminal. This is one local operator check, with no inherited
fixture credit and no Gaussian preparation or synthesis.

The static bond8 alternative is feasible to formulate as a different future
method. The saved compression uses left-to-right SVD: its first nine cores
are retained U columns, with approximate column isometries; the last core
contains the residual tensor. Define, without conjugating any coefficient,
`B_i[r,s,l] = A_(9-i)[l,s,r]`, reversing core order and transposing axes `(2,1,0)`.
For every reversed core after the first, its row Gram is the conjugate of the
corresponding original column Gram and is close to identity only to the extent
proved for the exact saved literals. The first reversed residual core requires
one paid positive normalization. This avoids a right-to-left QR of small
Schmidt coefficients; it does not assert exact numerical isometry or bypass
the fixed completion threshold.

Tensor transposition and reversal preserve coefficients and yield the original
compressed vector with physical bits reversed. Emit reversed site i on
physical wire `q[i]`, so the original Gaussian bin labels retain their original
bit significance. With bond wires `[10,11,12]`, the fixed bond8 rank path is
`[1,2,4,8,8,8,8,8,4,2,1]`; final rank1 still supplies the structural fresh-input
scratch cleanup route. A future version must explicitly support and verify
this output order; the existing plan validator requires descending outputs
and must remain unchanged. No relabeling is silently inherited from the old
component proof.

Before a bond8 emission, a separate new method must certify all ten exact
Gram matrices, complete active-column residuals, norm products, exact reversed
contraction and overlap, and the first normalization/rounding/complex phase.
Retain complex phases from the SVD tensors; no absolute-value or conjugate
substitution is allowed. Require a certified positive tensor norm and positive
minimum active-column Gram eigenvalue; keep `1e-12` for normalization and
completion rejection, with no rank drop or threshold/precision retry. The full
future route would use the unchanged q10 target, saved bond8 cores, no new CDF
or SVD, one emitted candidate, at most ten SDK calls, local dimension16,
13 preparation wires, 14 dirty-reference wires, 20,000 native slots and
4,096 rotations. Retain CPU900/admission840/wall1800, 160 digits and 256-bit
outward roots. Assess all three old scalar targets
`1/18720000`, `1/187200000`, `1/1872000000`, keeping the separate synthesis
reserve `1/7488000000`; no synthesis is included in this proposal.

The local bridge must first pass its independent audit, followed by review and
a fresh prospective bond8 method protocol. Neither route repairs the failed
q10 uniform-grid financial-law certificate. Full preparation Clifford+T cost,
native financial cost and adoption remain null/open. Higher-q Gaussian work
requires its own new preflight. All 110 program obligations remain in scope.
