# Original Box–Muller polar-CDF/BV implementation admission

This is an author-only implementation companion to the unchanged held method
`BOX_MULLER_POLAR_CDF_BV_PREFLIGHT.md` and
`box_muller_polar_cdf_bv_preflight.json`. No producer, proof, source walker,
interval calculation, preparation, test, pricing estimator or circuit has run.
Both executable source hashes must be populated and root/peer-reviewed before
preparation; null pins block admission.

The producer is `experiment_box_muller_polar_cdf_bv.py`; the independent auditor
is `audit_box_muller_polar_cdf_bv.py`. Their fresh receipts are respectively
`A02_polar_cdf_bv_run001` and `A02_polar_cdf_bv_audit_run001`, each with
`prepare|run --output` and the exact corresponding ROOT-relative destination.
The pinned launcher must start with `-B -m`. Each process keeps the root-fixed
180 CPU / 150 admission CPU / 600 wall-second limits, including verification,
bootstrap, copies, output encoding/hash work and failure retention. CPU is the
actual whole-process CPU; wall origin is derived from the actual Windows process
creation FILETIME, then enforced with the monotonic clock. There is no retry or
precision escalation. The primary uses 90 decimal digits and the independent
auditor uses 130, with exact rational endpoints of outward intervals.

Preparation uses only the standard library. Before lazy mpmath import, it freezes
the actual interpreter and launcher, isolated venv configuration, all venv
Scripts, full actual base Lib/DLL trees and adjacent base files, full mpmath
package including existing bytecode, and every actual distribution metadata
byte. Startup must already disable bytecode writes; user-site and inherited path
overrides are rejected. `MPMATH_NOGMPY=1` and `MPMATH_NOSAGE=1` are set before
import; the actual backend must be `python` with no GMP, Sage, NumPy, SciPy, JIT,
builder or audited-module import. Loaded source/cache origins are independently
SHA-checked before source/transcendental kernels and after work. The runtime
inventory cap is 24,000 files / 2 GiB. Runtime feasibility has not been measured.

The original 17 selected source pins and their original owner memberships remain
unchanged. A10 has an exact historical flat manifest; C06 has nested owned/frozen
maps. ROOT-confined, equal-SHA selected memberships are required without waivers.
No statement about global LIVE integrity is inferred from these selected inputs;
the historical 36-reference / 9-path differences remain separate.

The root-authorized implementation extension freezes thirteen additional native
root inputs and the original A01 owner manifest. These comprise both A10
unsigned46 root descriptors and actual gate files, the archived root emitter and
input-contract validator and reversible dependencies, the A01_run011 algebraic
all-guarded-input certificate and actual gate-structure audit and executed
auditor, and the original A11 descriptor/gate array to which that audit applies.
The two A10 arrays must have the identical SHA as the prior audited array;
descriptor specifications, all 264 actual invocation leaf IDs and SSA
argument/output mappings, full 72-bit copy banks and the 144 argument-copy CX
metadata are checked. The prior induction and full 43-stage structural parser
provide universal root semantics; finite fixtures are not promoted to universal
proof. No new gate-array scan, replay, cost analysis or synthesis is authorized.
The fresh all-q32 radius bound must satisfy
`root_argument_upper * 2^40 < 2^46`, which proves that native argument bits 46–71
are zero. Generic signed72 no-wrap alone does not satisfy this contract.

Run walks the accepted actual SSA without rebuilding a numerical Graph. It binds
every original pair midpoint, exponent, log/Horner, shared root, direct cosine
table and exact positive-sine `+.75` wrap. It independently recovers every raw
cumulative financial-log prefix, monitored basket and average role from the
accepted outputs. Actual rounded coefficients and clipped stock arithmetic are
recorded as source facts; ideal coefficients and unclipped GBM semantics remain
separate. Cross-date pair roles and one occurrence of each earlier driver are
retained. All 30 / 234 joint pairs support the ideal norm bound `sigma² T/nt`.

The finite interval kernel recomputes 288 log coefficients (32 bins × 9), ln2,
Taylor remainder, coefficient errors, native Horner floors and signed safety.
Thirty-three nonempty exponent classes −33…−1 partition all q32 midpoint words
by exact integer endpoints, without a grid sweep. It derives the native internal
radius envelope, squared-radius error and exponential KS envelope. Exact small
formal polynomial identities and written analytic premises make the conditional
radial TV4C and angular TV2C(nt+1) obligations reviewer-checkable. Both strict
`B² sigma² T/nt < 2` guards are required before writing the angular/ideal-hybrid
dollar certificate. A failed guard is a retained rejection, not budget censoring.

The optional 512-coefficient cosine envelope is **out of this implementation**.
The computed hybrid already pays the native-radius log/root error and both grid
discrepancies. A future native-normal bridge must freshly pay `B*E_cos+ulp` and
prove cosine/product safety; it must not add the old Holder radius term again.
Native financial literals/floors, stock approximation, clipping and eager safety,
strict ties/closed-band TV4 transfer and complete native-price G2 remain open.
The unchanged $0.0055 residual is context for a partial bound only; it is neither
spent nor reallocated. All new fixture, cost, adoption and full-G2 credits are zero.

Every output is exclusive. Actual SHA caches are invocation-local and guarded by
complete file identity and metadata; expected hashes never substitute for reads.
Bounded source/JSON reads hash the same chunks that are parsed, require unchanged
file identity, and reject disagreement with the previously observed actual SHA
before executing source or interval kernels. Source-AST reads use this same path.
Terminal verification fresh-resolves every observed alias and fully hashes the
unique frozen/observed union, including scoped external base-runtime paths.
Verification and output hashing precede one terminal manifest. A partial write
or exhausted hard budget produces an explicit `FAILED_UNSEALED.json` with zero
credit and stops hashing; neither an earlier success summary nor a partial
manifest can serve as a successful terminal receipt.
