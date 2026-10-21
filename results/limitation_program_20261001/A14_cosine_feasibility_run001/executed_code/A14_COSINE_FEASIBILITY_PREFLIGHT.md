# A14 paper preflight: one charged reversible cosine screen

Status: **AUTHOR_ONLY_PAPER_READY_PENDING_IMPLEMENTATION_AND_ROOT_READY**.
Fix one CORDIC feasibility row and one degree6 Taylor comparator, with at most one
separately authorized future production candidate. This is a conditional paper
design, not an executor, fit, numerical certificate, emitted circuit, resource
improvement or release. Existing evidence is immutable. All work is local;
no remote query, quantum device or author-side science is authorized.

## Original source and comparison

The scope is A14 in `docs/limitation_audit_20261001/implementation_plan/ARITHMETIC.md`.
The cached `ARITHMETIC_AND_LOADING.md` identifies the cited quantum CORDIC
paper as an arcsine construction; `.context/four_papers_v1/arithmetic.txt`
supplies arithmetic context. Neither supplies a cosine certificate, a free
controlled adder, or a complete-source resource factor. No external query was made.

Original A10 clean-XOR arithmetic uses signed72/f40. Its cosine uses64 centers
`(2*i+1)/128`, eight coefficients and seven Horner products. `cos_unit`
approximates `cos(2*pi*u)` directly, with no rounded two-pi multiply. Actual
inputs are exact q32 midpoints `(k+1/2)/2^32`; the second coordinate uses exact
`(u+3/4) mod1`, hence positive sine. Keep both coordinates jointly: B4 has30
pairs/60 cosine sites, B8 has234/468, including cross-date roles. Never divide
whole-source cost by the number of cosine sites to invent a function cost.

Fix a NEW total digital input map: signed-clamp the full72 input to
`[0,Q]`, Q=2^40, then approximate the closed [0,1]-turn cosine. This explicitly
differs from the old public clamp `[0,Q-1]` on arbitrary input words. Arbitrary
signed/high bits are never silently reduced mod1. Reached original midpoints
and exact wrap are strictly between0 andQ; implementation must bind/prove this
reachability. Axes `0,Q/4,Q/2,3Q/4,Q` return `Q,0,-Q,0,Q` exactly, so endpoint1
is digitally equal to endpoint0. Charge every clamp, equality, endpoint-to-zero
selection, axis branch, bank, copy and inverse. Root must authorize this new
total map before emission. Preserve full72 dirty-output-XOR ABI, input and clean
workspace; no exact old public-function/G2 equivalence is asserted.

Both rows must certify `E_candidate<=E_old`, the actual original cosine error
upper in `A02_BM_native_financial_bridge_run002/cosine_envelope.json`, source
manifest `78a8eea9dc937883b810cb6b3e2e26aec41297551b984a9c12bb15a435523162`,
audit manifest `62074efc3bd5a20a9cbe72b3d020fd5c6bf13e32d41b188ef57570225dade2a0`.
No author evaluated E_old. CORDIC has the stronger paper target E<2^-40; the
unchanged original propagated seven-Horner-floor term is
`2^-40*sum_(k=0..6)(1/128)^k`, hence at least2^-40, requiring
an actual source/formula binding before comparison. The comparator need not
meet one ULP. This is not A13's stock-relative alpha allocation.

## Fixed CORDIC and paper proof

Fix signed72/f56, N=48, e=2^-56, not the earlier internal80/f48 brainstorm.
Angles are `a_i=atan(2^-i)/(2*pi)`, i=0..47, finite gain
`K_N=product_i sqrt(1+2^-2i)`. Actual f56 angle and reciprocal-gain literals use
nearest ties-even. Future primary90/independent130 outward intervals must prove
their actual half-ULP errors; nearest rounding alone does not certify that premise.
Start `(x,y)=(round(K_N^-1),0)`.

Nearest-quarter folding is exact integer arithmetic:
`j=floor((4*m+Q/2)/Q)`, j=0..4, `t56=(m<<16)-(j<<54)`.
This is t=u-j/4 in[-1/8,1/8); reconstruct cosine from `[x,-y,-x,y]` for j mod4,
with exact-axis overrides. At z=0 choose d=+1, otherwise its sign. Simultaneously
use OLDx/OLDy for
`x'=x-d*floor_f56(y*2^-i)`,
`y'=y+d*floor_f56(x*2^-i)`,
`z'=z-d*ahat_i`.
Compute both branches unconditionally: three full72 ADD, three full72 SUB and
three full72 SELECT operations/stage. Two signed BITS shifts copy/sign-extend
their full output words; every old state, sign, input and discarded bit remains
available to literal inverse. Never use updatedx in y or infer reversibility
from final coordinates alone.

Each exact rotation has2-norm sqrt(1+2^-2i).
`K_N<sqrt(2)*exp(1/6)<(3/2)*(6/5)<2`, using exp(t)<1/(1-t).
Each stage's two floor errors have norm<sqrt(2)*e; subsequent gain<2 gives total
coordinate error<(3*N+1)*e including initial gain error. Exact
`a_(i-1)<2*a_i` and rounded greedy induction from |z0|<=1/8 give
`|z_N|<=a_47+N*e/2`; true-angle residual adds at most anotherN*e/2. A conservative
radian bound is `2^-(N-1)+3*pi*N*e`. The real rotations follow the actual
direction sequence; no norm preservation is asserted for floored coordinates.

Final f56-to-f40 nearest ties-even is explicitly paid:
`q=floor(c/65536)`, `r=c-65536*q in[0,65535]`;
incrementq iff r>32768 or (r==32768 and q odd). This also handles negativec.
Charge comparisons, residual/parity copies, Boolean flags, ADD and cleanup.
It costs at most2^-41 rounding error. Paid projection to[-Q,Q] is nonexpansive
relative to ideal cosine; exact-axis selection cannot increase error. Thus

`E_CORDIC<=2^-47+(3*pi*48+3*48+1)*2^-56+2^-41<2^-40`.

With pi<4 its exact e-unit sum is512+721+32768<65536. This is a paper inequality,
not an evaluated certificate. Actual48 literals, gain, folding/axes, signed
rounding, every selected AND unselected eager branch and all integer carries/
ranges must be independently proved before READY. Broad72/f56 headroom alone
is not an overflow proof.

## Charged resources and complete source

Fix ONE fullwidth72 Brent-Kung ADD/SUB family from measured A08 attempt002.
Ripple and Kogge-Stone remain reference-only, with no family search. Measured
clean full72 units: ripple T2016/T-depth1152/q289; Brent-Kung T4662/T-depth127,
q621 ADD/q693 SUB; Kogge-Stone T11354/T-depth583,q1099 ADD/q1171 SUB.
A08 retained its whole-source baseline. These are not controlled-add prices.
Fraction-label reuse f40→f56 is allowed ONLY after actual raw modular ADD/SUB
bit-map, ABI, copied-source and gate-hash equivalence; no73-bit embedding or
f40 multiplier price is transferred.

Charge per stage6 ADD/SUB,3 SELECT,2 shifts,1 sign bank and1 angle constant.
Before folding/rounding/clamp/private scratch, retain
`3*(N+1)+2*N+6*N+N+N=627` full72 words for states, shifts, candidate outputs,
signs and constants. One-bit flags still occupy full72 banks. Gain/zeros,
quadrant bits, negations, exact axes, every copied input/output and actual leaf
private scratch are additional. Fix standalone clean-function workspace cap
131072 qubits; no history is discarded to fit it.

Every inner call pays2*arity*72 argument-copy CNOTs and actual clean-leaf cost.
The candidate function is F /72 output-XOR /F^-1. The complete financial source
invokes that clean function in BOTH global directions, each with144 outer
argument-copy CNOTs: insertion is `2*sites*(clean_function+144CX)`. Never insert
once after subtracting two old directions. Remove old leaves only through an
exact actual-users fixed point, authorizing the cosine-output→radius-product
replacement edge alone; shared constants and every other consumer, original
log/radius/wrap and dead eager path stay charged. Original qubit storage is not
subtracted without a proved removal/liveness construction.

Report function T/T-depth/Clifford+T depth/private qubits/events/banks and complete
source estimates under actual B4/B8 caps550141/4460479. Bind matched original
measured metadata T520720662/4267435214 and T-depth555774/663704 before comparison.
Serialize candidate scratch and compare original/candidate under the same
conservative serial sum-depth accounting; measured depths remain a separate
reference, with no inferred parallel placement. Cost/schedule rows are
ESTIMATES until an emitted audited
construction exists. Missing contract-matched full72 LT/SELECT/BITS/lookup
units reject the resource row; never substitute a narrow leaf.

Fix the direct full72 primitives prospectively before any execution. Signed LT
flips both argument MSBs, then retains72 generate,72 propagate and72 borrow
bits with `G=(not a)&b`, `P=not(a xor b)`, `borrow=G xor(P&previous)`; disjoint
terms prove the Boolean recurrence. Copy final borrow and reverse all work.
Its286CCX/433CX/436X/private216 are charged. EQ retains72 XOR differences
and71 AND-chain bits:142CCX/289CX/144X/private143. SELECT retains72 differences:
72CCX/360CX/private72. Every direct CCX uses the pinned exact seven-T macro
with conservative serial7T/15Clifford+T depth, without a measured adder depth
discount. BITS copies its explicit full72 output map, including sign extension;
all argument copies remain full72. Flags use paid CCX/CX Boolean recipes.
The QROM equality/output/inverse recipe below is charged in full.

All original source storage and scratch remain allocated. One additional clean
function workspace may be reused across the declared serialized calls: every
F/output-XOR/literal-inverse invocation returns its noninput/private banks to
zero. This constructive clean-call liveness argument does not remove any old
SSA storage, imply a parallel placement or supply an emitted gate certificate.

## One fixed Taylor comparator

Fix degree6×64 original centered intervals, INTERNAL AND EXTERNAL72/f40,
local |t|<=1/128. Seven words/segment give448 signed72 coefficient literals;
also pay64 centers `center_raw=(2*i+1)<<33`. The coherent lookup has512 total
table literals and eight full72 output banks (center plus seven coefficients).
Charge one
coherent lookup, center subtraction, six full signed144-product/f40 Horner
MUL+ADD, every table/address/SSA bank, argument copy and inverse. MUL must have
an actual explicit universal full72/f40 descriptor. Same closed-domain clamp,
endpoint/axes and saturation policy; no f56 multiplication price substitution.
Before the eager lookup, paid-select endpointm=Q to lookup input0, then derive
the valid six-bit address. A later axis override never excuses an eager
address64 access or its unselected arithmetic.

Root prospectively replaced the earlier unexecuted minimax proposal on
2026-10-03 after independent paper review. No original executor/evidence was
changed. There is no fitter, exchange transcript, bracket search, Bernstein
certificate or minimax optimality claim in this fixed experiment.

For centeri and degreej=0..6, primary90 outward intervals enclose the true
coefficient `(2*pi)^j*cos(2*pi*center+j*pi/2)/j!`. Choose each literal by exact
ties-even rounding of `Q*(lo+hi)/2`, where lo/hi are the saved rational90
endpoints. No hidden binary64 is used. Independently bind all448 signed72
literals and pay each actual absolute error against the true coefficient;
do not assume half-ULP merely because a rounding function was invoked. Any
claimed true-nearest/half-ULP property must be certified by the actual interval.

On every CLOSED local interval, uniform error is the actual weighted sum
of seven coefficient errors, plus the degree6 Taylor tail
`(2*pi/128)^7/7!`, plus six propagated Horner floors
`2^-40*sum_(k=0..5)(1/128)^k`. Independent130 rebuilds the true448 coefficient
enclosures, tail and native floor/range induction and authorizes every claimed
primary error upper at the PRIMARY's actual selected literal values.
Retain all coefficient endpoints/error rows and all eager72/144 guards.

Paper feasibility only: `pi<22/7<16/5` bounds tail by
`1/(20^7*5040)<2^-40/5`. Conditional on actually proved half-ULP literals,
quantization is at most `(64/127)*2^-40` and six floor propagation at most
`(128/127)*2^-40`. These bounds do NOT imply E<=E_old. Retain a rejected row
if the actual source-bound threshold is missed; no savings/pass is promised.
No degree, segments, literal policy, precision or witness escalation is allowed.

The fixed coherent lookup uses five exact7T CCX chain operations for each
six-bit equality, literal-popcount controlled-CNOT output writes, and five
inverse CCX operations, for each of64 rows. Charge before/after X gates for
negative controls, five selector scratch qubits, full72 copied address bank
(bits6..71 proven zero), eight full72 output banks, every caller copy and the
lookup in F and F^-1. No old mismatched lookup descriptor or free coherent
classical table is borrowed. Its resource count remains an estimate until an
actual native source/gate realization is independently bound.

## Financial gate and finite stop

Use newly certifiedE, original native radiusB and fresh remaining-coordinate
error `delta_Z=B*E+2^-40`. The polar/hybrid ledger already pays native log/root
radius errors; never add old radial/grid/Holder radius terms again. Preserve
joint pairs. A13 stock-relative alpha is not inherited. The residual11/2000
dollars is not a per-cosine allowance.

Before a changed-source G2 label, freshly bind all60/468 calls/reached domains,
exact wrap, eager signed72/144 safety, raw-prefix sensitivity, native floors,
both clipping guards, closed barrier-band TV4, actual point-value ties,
smooth payoff and both contracts. No old G2, cost, estimator, sampler or
adoption label transfers from a component certificate.

Prospective screen and independent audit each300CPU/270work-admission/900wall,
90/130 digits, one thread,64 owned files/128MiB,0 new fixtures/replays/price
experiments. One invocation covers the two rows and both complete sources.
No adaptive widths/iterations/degrees/segments/families/precision/brackets/
restarts. Before evaluation implementations freeze source/runtime/interpreter/
base/package/cache, complete accepted bridge producer/audit maps, and original
owner-manifest bytes with explicitly selected original metadata/gate/source
members. Unselected owner circuits are outside this component's integrity claim.
Charge bootstrap/I/O/hash/work,
cache independently observed SHA/stat only, fresh-recheck every alias and full
observed/frozen/external union before exclusive terminal sealing. No expected
SHA override, retry, provisional-manifest overwrite or unsealed-success
promotion. Exact executable/runtime/member pins and detailed realizable
removal/liveness/primitive ledgers remain implementation gates, not tuning rights.

Reject missing uniform/domain/resource/safety evidence, either source cap
violation, or failure to beat matched original completeT AND conservative serial
depth on BOTH sources. Stop when cleanup/history eliminates advantage or the
active roadmap no longer needs the component. At most one future emission needs
a separate exact-source external ROOT READY and independent financial/cost/
schedule review. No saving, physical runtime improvement or quantum advantage
is promised. Separate executable author drafts remain unexecuted; no A14
evaluated bound, fit, gate, preparation or result receipt was created.

