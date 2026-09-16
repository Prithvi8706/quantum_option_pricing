# Week 13: structured route and accuracy-dependent costs

Status: implemented product-normal loader plus finite payoff table; reversible
arithmetic below is an assessed extension, NOT implemented or priced. The
[protocol](PROTOCOL_W13_ENCODING_V1.md) fixes the executed study. None of this
establishes a new algorithm or quantum advantage.

## What is and is not structured

The independent Gaussian registers really can be loaded separately before
correlation is applied in the payoff computation. With d=assets*dates, q bits per
normal, generic one-dimensional loading has O(d*2^q) gate work, O(2^q) distinct
classical cell masses, and dq data qubits. Computing these masses uses CDFs;
arbitrary-angle synthesis and numerical error are not free. The dense comparison
is a correctness baseline, not the best classical or quantum algorithm.

The present UCRY payoff still has 2^(dq) entries. Classical setup evaluates every
path, including covariance multiplication, exponentials, averages, both calls,
square root and arcsine. These functions are compiled into stored rotation
angles, not magically executed for free on the quantum computer. A finite
expectation is then already available by direct summation. Product loading alone
does not rescue the overall exponential table. An unoptimized compiler may also
recognize factorization inside the generic dense loader: compare actual counts,
not a presumed loader improvement.

## One assessed extension: reversible arithmetic after product loading

Use bounded fixed-point normals, compute x=mu+Bz reversibly, exponentiate to
spots, accumulate arithmetic/geometric means and calls, compute normalized
payoff into a register, rotate the flag, then reverse all temporary arithmetic.
Beta1 geometric residual avoids signed output; intermediate log variables remain
signed. No root-finding or conditional CDF is needed for this chosen residual.
The analytic geometric mean's CDF evaluation is a charged classical offset setup.
Conditional-root encoding is not a second tested representation.

For p-bit work precision, with reversible multiplication cost M(p), addition
cost A(p), exponential approximation cost E(p,H,eta_exp) on |x|<=H, and
flag cost R(p,eta_rot), an explicit symbolic forward-work model is

`Cwork = d²[M(p)+A(p)] + d E(p,H,eta_exp) + O(d A(p))`

for raw; residual adds a log mean, one exponential, a second call and subtraction.
This deliberately uses dense covariance arithmetic rather than assuming an
unimplemented sparse factorization. A full clean-oracle call costs approximately
`Cload + 2 Cwork + R`, including reversal of temporary work after flag encoding.
Additional reverse angle-arithmetic may be necessary depending on R's interface.
AE repeats A and A-inverse and reflections: one Grover step is not one loader.
Workspace depends on pebbling/recomputation, at most a straightforward polynomial
register construction if the chosen arithmetic subroutines have polynomial space;
no measured qubit/T count is available for this unbuilt extension.

Explicit accuracy dependence: if coefficient error <=eta_B and each normal
rounding <=eta_z=L/2^q, log-price error <=d L eta_B + ||B_i||_1 eta_z
plus accumulated arithmetic rounding. Exponentiation amplifies a log error e_x
by at most exp(H+e_x)*e_x. Add eta_exp for polynomial/rounding error, averaging
and call arithmetic errors. Raw call is1-Lipschitz; residual adds the geometric
channel's error. Flag-probability error eta_a contributes scale*eta_a dollars.
For marginal state errors bounded in trace distance by eta_load each, product
trace distance is at most d*eta_load, contributing at most scale*d*eta_load.
Use the trace-distance convention half the trace norm. Offset rounding, tail
and discretization remain separate. Choose p, polynomial degrees and rotation
precision from a proved allocation of these terms; picking p=32 is not a proof.

Unresolved prerequisites for that extension: separate midpoint discretization
from fixed-point arithmetic error so neither is double counted; include errors
in mu and B, and prove that the enlarged log domain including these errors fits
the exponential approximation's interval. The executed max(table) normalization
requires enumeration. A scalable route instead needs a non-enumerative safe
scale (for example the conservative cube payoff upper bound), together with
the cost/error of computing and dividing by it. A larger safe scale can erase
the small-table residual's apparent estimation benefit. No such normalized
arithmetic circuit or precision allocation has been certified here.

The midpoint bound in the protocol requires q at least
`ceil(log2(L*Lipschitz/bias_discretization_budget))` when this is positive.
Increasing L reduces tail bias but increases the cube Lipschitz bound
exponentially. Consequently O(d*2^q) loading is itself accuracy-dependent.
At q=2, the 2asset/12date target already has48 normal qubits and2^48 payoff
entries; 4asset/52date has416 normal qubits and2^416 entries. These are exact
table-size calculations, NOT generated tables or measured circuit resources.
At fixed q, changing monitoring dates also changes the contract.

## Prior-work checks and exclusions

[Chakrabarti et al.](https://quantum-journal.org/papers/q-2021-06-01-463/)
provide end-to-end resource estimates for autocallables and TARFs, including
state preparation and payoff circuitry. Their estimates are not measured Asian
resources and cannot be copied into our ledger.

[Herbert](https://arxiv.org/abs/2101.02240) identifies the cost problem when
classical Monte Carlo integration is used inside Grover-Rudolph preparation.
Our analytically specified Gaussian cell masses avoid that particular Monte
Carlo subroutine; they do not establish efficient full payoff loading.

[Stamatopoulos and Zeng](https://arxiv.org/html/2307.14310v2) use QSP to reduce
payoff arithmetic for particular derivative constructions. This supports a
future cost-reduction option, not a direct replacement of a multivariate Asian
sum-of-exponentials residual without a new block encoding, degree/error analysis
and preparation cost. No QSP circuit was implemented in this week.

[Iaconis, Johri and Zhu's normal-distribution MPS work](https://www.nature.com/articles/s41534-024-00805-0)
is relevant to replacing generic marginal loading. It requires its own
approximation and circuit audit; a normal loader does not compute the basket
payoff. No MPS fidelity or complexity result is claimed for this implementation.

Reading is a focused feasibility/prior-work check, not an exhaustive field
survey. The bounded [Heston/nested audit](WEEK_13_ALTERNATIVE_AUDIT.md) retains
both alternatives as unestablished. Route decision: keep small Asian circuits as
correctness/resource diagnostics; block a certified continuous-price or scalable
advantage claim until the numerical enclosure and arithmetic route are built.
