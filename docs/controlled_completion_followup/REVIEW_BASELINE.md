# Independent review of the existing controlled-source completion

2026-09-22. This review covers `research/controlled_source_completion`, its
reported results, and the relevant preceding compound/parity implementation.
It precedes the remaining-priority follow-up and is **not** approval of the final
PR candidate. The reviewer did not implement the underlying financial source,
mean estimator or phase certificate. A small resource-accounting correction was
implemented only after reporting the finding and receiving the coordinating
agent's request; another reviewer should include the corrections in the final
candidate review. A later packaging pass also identified and repaired path
relocation, as recorded below.

## Severity-ranked findings

**Medium, fixed: gate libraries depended on the original working directory and
Windows path spelling.** Both execution functions first interpreted the archived
`library_workspace_relative` field directly with `Path`; on POSIX the stored
backslashes are ordinary filename characters. Falling back to the old machine's
absolute `library` path cannot recover a relocated checkout. Even on Windows,
changing the current directory could select the old absolute fallback instead of
the intended checkout's files.

[`resolve_library`](../../research/controlled_source_completion/compiler.py#L18)
now normalizes Windows/POSIX separators and resolves relative library paths
against the module's repository root. Legacy absolute archive paths are recovered
from their `results/` suffix; unrelated absolute-only legacy paths and parent
traversal are rejected. Explicit existing absolute workspace fields remain valid
for newly compiled temporary test libraries. Both execution paths and the
resource audit use the helper. Eight path regression cases cover relocation,
separator conventions, unrelated current directories and invalid archive paths.
Historical metadata is unchanged. These are simulated relocation tests, not an
executed Linux platform run.

**Low, fixed: shared CNOT controls invalidate the generic argument-copy depth
formula.** In
[`compiler.py`](../../research/controlled_source_completion/compiler.py#L68),
the original `4*len(calls)+1` Clifford+T depth allowance assumed every copy batch
occupied one layer. An invocation such as `mul(a,a)` copies each input bit to two
distinct local argument slots, so those CNOTs share a control and need two
layers. Named outputs that alias one SSA value have the same constraint.

Reproduction: a `Graph(3,5)` with one input `a` and output `mul(a,a)` declared
Clifford+T depth 14,343. Independently flattening its emitted leaf, argument
copies, output copy and inverse and scheduling the resulting gate sequence gave
14,344. The fix charges the maximum argument multiplicity for each invocation
and maximum output multiplicity. The new conservative ledger gives 14,347 for
this case. Regression checks cover both one named output and two names aliasing
the same output, and compare declared resources with the independently flattened
gate sequence.

This finding does **not** alter T counts, T depths, the financial computation or
the failed latency screen. The archived production sources' old Clifford+T depth
allowances remained conservative overall because they also charged nonexistent
copy layers to constant leaves. All historical manifests and snapshots remain
unchanged. Newly compiled artifacts use the corrected generic formula.

No high-severity defect or medium-severity mathematical, numerical or
resource-accounting defect was found in the reviewed completion candidate. This
is a bounded review, not a proof that no further defects exist.

## Checks and reasoning

The interval contraction agrees with the cited Theorem 3.19: the offset test
distinguishes `mu-L <= W/4` from `mu-L >= W/2`; both retained intervals contain
the indeterminate region. Outward dyadic rounding of the initial radius, exact
rational controller endpoints, and `S >= 32s` maintain the RMS hypothesis.
The `1.42 epsilon` threshold, `epsilon/6` phase tolerance and `2/9 + 1/9`
single-test failure budget match the theorem's constants in the already archived
primary paper. The circular QPE-tail estimate is conservative. All eight
archived schedules have a majority union failure below 0.003; their recorded
controlled-U counts and phase-error allocations reconcile independently.

The 64-bit phase proof has sufficient numerical allowance for the declared
`|Y|, |L| <= 100` and power-of-two `S >= 16` domain. The normalization shift,
nearest endpoint load, reciprocal truncation, endpoint clipping and geometrically
contracted Horner errors fit comfortably inside 32 ulps. The separate stored
pi constant allowance covers the reciprocal branch. The review checks the
coefficients actually stored in `compile_v2/phase_f64/target.json`, not merely a
freshly generated table. Rational interval helpers from the original certificate
are reused for this artifact-binding check; the phase-value reference uses
85-digit mpmath arithmetic.

The fused wrapper correctly executes financial forward computation, exact
fixed-point promotion, phase forward computation, controlled diagonal phases,
both inverse computations and the signed reflection. Removing the two clean
output copies accounts for the fused Clifford adjustment. The sign bit among
the `f+3` active phase bits is consistent with angles in `(-pi,pi)`. The final
Z on the QPE control supplies the reflection sign that cannot be dropped under
control. The preserved random-input preparation, reflection AND ladder, QPE
powers, full inverse QFT and repeated resets are visible in the ledger.

The classical comparison is explicitly favorable to the quantum implementation:
it charges an entire three-strike classical run to one requested price. Empirical
RQMC uncertainty is distinguished from the stronger iid contract. Conditional
continuous-moment schedules are labelled conditional, while support-only digital
moments are separately costed. The report correctly limits the failed crossover
conclusion to the implemented schedule and assumptions, rather than asserting a
lower bound on every possible quantum circuit.

## Executed evidence

[`review_baseline.py`](../../research/controlled_completion_followup/review_baseline.py)
and its
[`JSON result`](../../results/controlled_completion_followup/review_baseline.json)
record:

- 288 stored atan coefficients checked with exact rational rounding intervals.
- 680 phase cases at interpolation boundaries, reciprocal boundaries, signs,
  endpoint ranges and the recorded normalization scales. Largest observed error
  was `1.2253427040655417e-16`, below `2.1426634139061702e-16`.
- 60 finite spectral laws with rare outliers and RMS at the theorem's boundary.
  Minimum promised success probability was `0.9938538313171811`.
- All eight archived schedules reconciled; largest majority union failure was
  `0.0029436496070712596`.
- 1,001 deterministic controller means across the full initial interval, including
  endpoints. Maximum observed estimation error was `0.0015856059694669966`
  against an allocation of `0.002`.
- The existing focused suite: **55 passed, 3 upstream Qiskit deprecation warnings**
  in 53.80 seconds.
- New alias-copy regression suite: **2 passed** in 2.19 seconds.
- After adding path relocation: completion plus all ten review regression tests,
  **42 passed, 3 upstream Qiskit deprecation warnings** in 45.12 seconds.
- Ruff on the two new review Python files: **all checks passed**. Historical
  source formatting and archived snapshots were not rewritten.

Reproduce from the repository root:

```powershell
.context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_completion_followup.review_baseline
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
.context/antithetic_feasibility_env/Scripts/python.exe -m pytest research/controlled_source_completion/test_completion.py research/controlled_residual_feasibility research/compound_feasibility research/controlled_completion_followup/test_review_baseline.py -q
```

## Unresolved obligations, already disclosed by the reviewed report

The finite-input financial bridge, global financial arithmetic and overflow
certificate, conditional-control identity under the digital law, policy-boundary
effects, surrogate mean, regret and transfer of the tight moment certificate are
not established by these checks. Arbitrary-rotation synthesis and a supported
physical design remain incomplete. The source and phase basis checks do not
constitute a full pricing QPE execution. No continuous-price 99% certificate,
end-to-end fault-tolerant advantage, held-out success or novelty claim follows.

The final PR review should recheck the new follow-up artifacts and claims, include
the compiler correction, and exercise the exact repository candidate from a clean
checkout so that untracked local dependencies cannot mask packaging omissions.

The recorded historical virtual environment uses `include-system-site-packages
= true`; its Qiskit import resolves through the user's roaming Python site. The
recorded package versions are useful provenance, but that environment is not an
isolated reproduction. A release needs a fresh dependency installation and clean
checkout replay. Absolute provenance paths in historical JSON can remain as
evidence, provided current execution resolves the release's own files.

## Paper-claim and novelty assessment

This bounded assessment reread the locally archived primary Kothari--O'Donnell
paper, Montanaro paper, the relevant assumptions in Blanchet et al.'s nonlinear
Monte Carlo paper, and Herman et al.'s error framework. It also inspected the
current manuscript and the existing source-specific novelty assessment. It did
not search for a different advantage direction, assert an exhaustive literature
search, or establish world-first priority.

The new result supports a **specific negative feasibility case study**: compiling
this controlled compound Asian-basket residual into explicit reversible source
arithmetic and an explicit known-moment phase-estimation schedule exposes costs
that exceed the stated favorable latency screens. Controls can shrink statistical
work while making each coherent source evaluation expensive. The retained code,
failure cases, matched classical controls and resource/error interfaces make that
observation auditable. A defensible claim is:

> For the specified development contracts and emitted arithmetic schedule, the
> implemented controlled digital residual source fails the stated tenfold latency
> screen, even under the separately reported optimistic query and logical-timing
> assumptions. The evidence identifies remaining financial and physical
> certification obligations; it does not rule out other implementations.

The abstract must distinguish a grant of the continuous moment certificate from
a proved moment bound for the actual digital source, and an optimistic query
sensitivity from the implemented estimator. A generic “penny-accurate, 99%
quantum compound pricer” claim remains unsupported without the missing bridge
and complete price/error composition.

The main components have clear predecessors:

| Component | Existing primary overlap | Consequence for originality |
| --- | --- | --- |
| Signed variance-sensitive mean estimation | [Montanaro, Section 2.3, Algorithm 3 and Theorem 5](https://arxiv.org/abs/1504.06987v3) | Estimating signed residual means with variance information is established. |
| Complex phase and adaptive mean test | [Kothari--O'Donnell, Theorem 3.19, Lemma 4.3 and Appendix A](https://arxiv.org/abs/2208.07544) | The phase primitive and contraction mechanism are applications of prior theory; source gate cost is explicitly part of its computational model. The conservative known-moment implementation is not their full unknown-variance optimum. |
| Regression residual inside conditional estimation | [Blanchet et al., Section 3 assumptions](https://arxiv.org/abs/2502.05094) | Their discussion explicitly admits regression noise through a residual function. Substituting this financial control does not establish a new nested quantum speedup theorem. |
| Composed distribution/arithmetic/estimation error | [Herman et al., Sections 4.2-4.3](https://arxiv.org/abs/2602.03725) | Tracking truncation, discretization, arithmetic, distribution and estimation error is established methodology. A worked application certificate can be useful without being a new error-budget principle. |

The existing
[source-specific assessment](../novelty_assessment/2026-09-21/NEAREST_PRIOR_ART_MATRIX.md)
also records classical approximation plus quantum residual integration,
conditional Asian controls, reversible polynomial arithmetic, pebbling and prior
pricing resource studies. This review does not independently reverify every
publication/version claim in that earlier assessment. Compute/phase/uncompute
fusion and local circuit improvements should be presented as implementation
optimizations, with measured changes and exact assumptions, rather than new
quantum primitives.

The current
[manuscript](../../manuscript/2026-09-22/main.md#L14)
addresses a different, already qualified comparison: D1/D2 ordinary Asian-basket
calls, a one-dollar/95% ideal-logical contract, finite Gaussian cell-mass loading,
canonical AE and a common ideal U/CX decomposition. The new work uses compound
contracts, penny/99% targets, midpoint Box--Muller inputs, a different estimator,
and Clifford+T source ledgers. Its unfinished financial bridge must not inherit
the older manuscript's “certified” label. Combining the studies would require an
explicit separate experiment and contract table; leaving this new feasibility
study as a distinct technical report or artifact is coherent.

The negative result alone does not establish sufficient originality or
significance for a research journal. A stronger publication case would explain a
generalizable lesson through controlled component ablations, without promoting
one inefficient schedule into an impossibility theorem. A reproducible technical
report is already an honest form of dissemination. No journal acceptance,
human novelty clearance, submission readiness or researcher endorsement is
claimed, and no manuscript was edited during this review.
