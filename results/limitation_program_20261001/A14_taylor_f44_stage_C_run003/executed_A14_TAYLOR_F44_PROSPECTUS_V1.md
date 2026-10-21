# A14: one Taylor6 cosine with internal F44

Status: **AUTHOR_ONLY_PROSPECTUS_PENDING_IMPLEMENTATION_AND_ROOT_READY**. This
prospectus fixes one additional component proposal. It authorizes no numerical
evaluation, gate generation, source walker, fixture, prepare/run, emission,
candidate adoption or financial acceptance. All work stays local. The prior
CORDIC and F40 Taylor screens remain completed audited rejections, with zero
eligible rows; their evidence and author files remain immutable.

The original source manifest is
`bdb01b0c69d8fab3ee3d61f1c48ce5764f1ae09488f564d186f658f180e4156b`;
the actual independent audit003 manifest is
`52c88dc17c6a53b1df30bd93a431d3e263cb202462901589aaaa30bb87631f0f`.
Audit003's static release is
`db63fda477c28adecde7038a928541661b3a2e5278dfe1b817a15764e41624a4`.
These are root-issued expected pins. Future controllers must verify their
complete owned/frozen/external maps and exact inventories, including the
retained prior failure/diagnostic history. A new observed SHA never replaces an
owner's expected SHA. No global historical/current LIVE integrity is asserted.

## One fixed map and polynomial

The proposed row is `TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38`. Fix external
signed72/f40 input and full72 dirty-output-XOR; preserve the input and return all
private and history banks to zero by literal inverse. Internal arithmetic is
signed72/f44. Degree6, 64 centers and all448 coefficients are fixed; there is no
fit, minimax exchange, search, adaptive segmentation, alternative width or
alternate multiplier family in this release. At most one later production
candidate could be authorized by a separate release.

Use the prior A14 proposal's explicit NEW total map: signed-clamp arbitrary
full72 input `m` to `[0,Q]`, `Q=2^40`, and return the cosine of the resulting turn.
This differs from the original public clamp `[0,Q-1]` on arbitrary words. Original
q32 midpoint turns and the exact `+3/4 mod1` second coordinate are strictly
inside the interval; binding those actual inputs remains mandatory. No exact
old public-function equivalence is claimed. The source uses cosine directly
in turns, without an inserted rounded `2*pi` multiply; the second coordinate
retains positive sine and the pair remains joint.

For eager arithmetic, first paid-select `u=0` when the clamped input is `Q`,
otherwise `u=m`. Thus `0<=u<Q` BEFORE lookup, center subtraction or multiplication.
Fix `bin=floor(u/2^34)`, with six actual address bits and high bits zero, and
`center44=(2*bin+1)<<37`. Equivalently the exact local operand is

```text
local44 = (u - bin*2^34 - 2^33) << 4.
```

Euclidean division gives `0<=u-bin*2^34<=2^34-1`, hence
`-2^33<=u-bin*2^34-2^33<=2^33-1`, and exactly
`-2^37<=local44<=2^37-16`. This is a signed38 promise: bits38..71 are its
sign extension, and bits0..3 are zero. It is derived from the complete digital
map, not from sampled inputs or an assumed same-date Gaussian role. Endpoint
`Q` must route to input0, not merely lookup address0 while retaining a large
local operand. Every selected AND unselected eager path must satisfy the promise.

At clamped inputs `0,Q/4,Q/2,3Q/4,Q`, paid selections return external raw values
`Q,0,-Q,0,Q` exactly. Negative/high arbitrary words follow the stated signed
clamp. Charge equality, endpoint routing, address extraction, sign extension,
rescaling, axis selection, projection to `[-Q,Q]`, every bank and inverse.

## Conditional error, with actual literal authorization required

Let `h=1/128`, `eps40=2^-40`, `eps44=2^-44=eps40/16`. At center
`c_i=(2*i+1)/128`, fix the seven true Taylor coefficients
`a_ij=(2*pi)^j*cos(2*pi*c_i+j*pi/2)/j!`, `j=0..6`.
Primary90 and independent130 outward enclosures must bind every one of the448
fresh signed literals. Quantize by exact ties-even rounding of
`2^44*(lo+hi)/2`, with saved rational primary endpoints and no binary64 step.
Pay each literal's actual absolute error against the true coefficient. Calling
nearest rounding does not itself prove true-nearest or half-ULP accuracy.

The following is conditional on actual coefficient errors at most `eps44/2`,
exact centers/local rescaling, exactly six signed Horner product floors, exact
additions without wrap, and genuine nearest/ties-even final conversion:

```text
coefficient error <= (eps44/2) * sum(h^j, j=0..6)
six floor errors <= eps44 * sum(h^j, j=0..5)
their sum <= 12*eps40/127
final rounding <= eps40/2
Taylor tail < eps40/5
total < (1009/1270)*eps40 < eps40 <= E_old.
```

Here each geometric sum is below `128/127`. The order7 tail is
`(2*pi*h)^7/7!`; `pi<16/5` bounds it by `1/(20^7*5040)<eps40/5`
(equivalently `63*5^7>2^22`). These are paper inequalities; no coefficient or
error envelope has been evaluated during authoring. The actual accepted
`E_old` must be source-bound from the original bridge cosine envelope; its
seven-floor term includes `eps40`, so this comparison requires that unchanged
formula and all nonnegative terms to be verified.

If any actual half-ULP premise is uncertified, retain rejection; a future code
release may report the actual-error envelope but must not substitute the
conditional `1009/1270` bound without its premises. No extra precision, refit,
table or candidate is tried. The closed continuous polynomial proof includes
both `-h` and `+h`; the native signed38 promise is separately digital. No actual
signed38 multiplier call at a hypothetical positive endpoint `+2^37` is claimed.
The closed proof is a conservative error bound for all reached digital words.

Final f44-to-f40 rounding is defined for negative values as well:
`q=floor(z/16)`, `r=z-16*q in[0,15]`; increment `q` iff `r>8` or
(`r==8` and `q` is odd). A simple add8/rightshift has a different tie rule.
All quotient/residual/parity/Boolean/increment history and copies are paid.
Projection and exact-axis selections cannot increase distance to true cosine.

## Native arithmetic and the one fresh multiplier

The paper derivative bound `pi<16/5` gives `|a_ij|<(32/5)^j/j!<96`
for `j=0..6`. Under the actual literal premise, a conservative Horner induction
gives `|accumulator| <= (96+3*eps44/2)/(1-h)<97`. Thus its raw f44 word has
magnitude below `97*2^44<2^51`, giving a signed52 promise. Fresh literal and
all eager intermediate integer ranges must establish that promise before use;
neither 72-bit headroom nor a real-valued error theorem proves native safety.

Fix ONE new multiplier contract: signed52 first operand, signed38 second
operand, sign-extended full72 input ports, fraction44, full72 dirty-output-XOR,
input preservation and clean private workspace. Its semantic multiplication
is signed144; the retained representation has116 bits and output window44..115.
The full signed product of the generic52x38 contract needs90 bits (the two
minimum operands can produce `+2^88`); the remaining retained high bits must be
correct sign extensions. Do not accidentally truncate to signed89. Require an
actual explicit descriptor with width72, fraction44, product_width116,
active_operand_bits `[52,38]`, port/argument maps, gate-file SHA and literal
inverse. The precise input promises must be independently tied to every caller.

Build, structurally prove, phase-authorize and independently count this NEW
realization. The old F40/product112 arrays, active promises and resource numbers
are ineligible. No generic F40 ABI, narrow descriptor, classical fixture or
timing factor is substituted. ADD/SUB raw full72 map reuse is allowed only with
the prior measured source/ABI/gate proof; it supplies no multiplier or controlled
adder discount. All raw additions, shifts, constants, products and unselected
branches must remain within signed72/output contracts without eager overflow.

## Fixed staged QA before a full component screen

Stage K is a small fresh multiplier/rounding QA, not a cosine or financial
certificate. Register these exact eight operand pairs before any run. Put
`xmin=-2^51`, `xmax=2^51-1`, `ymin=-2^37`, `ymax=2^37-1`:

```text
(0,0), (0,1), (1,0), (-1,1),
(xmin,ymin), (xmax,ymax), (xmin,ymax), (xmax,ymin).
```

Use each pair with dirty output word0 and `2^72-1`:16 native basis diagnostics.
Rounding uses `z=16*q+r` for all `q in{-2,-1,0,1}` and
`r in{0,7,8,9,15}`, each with those same two dirty words:40 diagnostics.
Additionally exhaust the32 combinations of remainder0..15 and quotient parity
for the exact rounding increment predicate. Total fixed diagnostic cases:88.
Each native diagnostic replays the actual full-port forward and literal inverse,
checks all allocated wires, preserved input and zero private workspace, and
retains exact integer reference comparisons. No random corpus, reduced-width
proxy, operator matrix on72 qubits, or full53/q32 statevector is allowed.

These finite checks do not prove the whole-input arithmetic or phase. Stage K
also requires a universal structural signed-product/rounding proof matched to
the actual emitted array and exact seven-T CCX phase macro; every opcode and
macro must be recognized, with no unexplained phase or dropped gates. A separate
independent checker is mandatory. Prospective producer and checker each use
180 CPU/150 admission/600 process-creation wall seconds, one thread, no JIT,
64 owned files/128MiB, at most1,000,000 native rows across the two primitives.
All bookkeeping, runtime/source hashing, generation, proof, replay, encoding,
copies and terminal work are charged. Exhaustion is retained failure, no retry.

Only after both Stage K packets and fresh ROOT integrity PASS could root release
Stage C: one complete `TAYLOR_D6_S64_W72_F44_TO_F40_MUL52x38` cosine component
screen, primary90/independent130, each300 CPU/270 admission/900 wall seconds,
one thread/no JIT, 64 files/128MiB and at most2,000,000 native rows for one
clean cosine prototype. Global B4/B8 financial gate emission remains unauthorized.
The fixed literal corpus is all448 coefficients
plus64 exact centers; no center, coefficient or segment is sampled or dropped.
Retain actual error/native/resource gates and a rejected row if any fails.
Optional numerical backends are forbidden; mpmath is1.3.0 pure Python with
NOGMPY/NOSAGE set before import. Full actual runtime/package/cache/metadata and
all code/owner memberships must be frozen before evaluation. Any additional
gate serializer/compiler dependency must be explicitly fixed in its separate
implementation release, not loaded opportunistically.

No future executor, auditor, gate file, accepted packet or ROOT_READY exists
because this prospectus names it. Code and actual prerequisite pins remain
unresolved until separately reviewed. Fresh receipts, budgets, physical path
confinement, stat-guarded actual-SHA caches and two uncached fresh full-input
union verifications must be fixed before execution. Failure or partial sealing
gets authoritative FAILED_UNSEALED, never a promoted partial PASS. New fixture
credit, fullG2, gate adoption and advantage credit stay zero/false.

## Actual resources and complete-source comparison

Load center plus seven coefficients coherently:512 classical table literals,
eight full72 output banks. The address is a full72 copied bank whose high66 bits
are proved zero; its five equality scratch bits and all negative-control X,
forward/inverse CCX, literal-popcount CX and cleanup are paid. Charge every new
F44 table bit, center subtraction, exact left rescale, six new MUL+ADD calls,
axis/clamp/rounding/projection, every full72 SSA/flag/history/argument/output bank
and actual reusable private scratch. No old QROM literal count is reused.

Each inner call pays the actual clean leaf AND `2*arity*72` argument-copy CX.
Let F be the complete charged forward recipe, including those inner copies;
the clean function is `C=F /72 output-XOR /literal F^-1`, thus `C=2F+72CX` for
the conservative event/sum-depth ledger, EXCLUDING outer caller copies. The
whole source adds `2*sites*(C+144CX)`, with60 B4 and468 B8 sites: both global
directions and both outer copies are counted. The actual clean primitive
counts, exact CCX phase convention, full event chronology, matched serial
T/Clifford+T schedule and complete qubit-bank inventory must be independent.

Original log/radius/wrap/financial paths and all source storage remain charged.
Remove old cosine work only through a complete actual-users fixed point with
the cosine-output to radius-product replacement edge explicitly authorized;
shared literals, other users and eager dead work remain. A single additional
clean-function workspace may be reused only under the stated serialized calls
and proved full cleanup. No parallel schedule or original-storage subtraction
is inferred. Bind the actual B4/B8 baselines and caps from the already audited
source; reject missing/mismatched primitives or unaffordable total cost.

Uniform comparison alone does not validate a changed source, a financial/G2
certificate, physical feasibility or adoption. The original native financial
sensitivity could support a later separately source-bound proof with the actual
new cosine bound, native radius and unchanged final-product charge, but no
source/cost/estimator/advantage transfer occurs here. The existing A14 rejections
remain in the ledger, and no aggregate financial allowance becomes a per-call
allocation. Root must issue separate READY for each finite stage before work.
