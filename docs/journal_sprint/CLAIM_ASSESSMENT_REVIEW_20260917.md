# Separate AI review record and dispositions

Date: 2026-09-17. These are separate agent reviews commissioned for the current
claim-assessment work, not human expert reports or external journal review.
No human expert was contacted and no review is attributed to a collaborator.

## Mathematical/code reviewer: Ampere

Agent01a0ae98-754e-7062-8dfd-77de7a899c08 independently inspected the existing
signal and W2 pipeline and ran36 tests. It confirmed the restricted cube-norm
proof and conditional continuous-cost optimum, while stressing scalar versus
circuit uniqueness, correlated-support limitations, degeneracies and the need
for Hermitian-involution structure downstream.

Finding: the original interval sign test mishandles [-epsilon,0]. The reviewer
provided the means=[-1e-80], factor=[[0]], K=.5 reproducer. A versioned corrected
class uses negative_constant=(constant.lo<0) after the inherited rejection of
strictly straddling intervals. The reviewer accepted the repair and reran21
new tests. Original experiment code remains frozen; the reviewed version is
available for new acquisitions and has not been silently substituted into them.

Further independent checks reported by the reviewer:

- Exact rational production intervals show all four centered constants strictly
  positive; none of the32 rows encounters the defective endpoint.
- Machin pi-enclosure width is approximately5.55e-61, with conservative AE bound.
- All164 sensitivity plans returning a schedule have a previous power of two
  that fails under the lower pi bound; selected M is minimal for the criterion.
- Independent inverse-QFT compilation for1–12 phase qubits agrees with the
  per-repetition CX formula m(m-1)+3*floor(m/2).
- All32 original schedules/corrected costs agree. The outcome counts and the
  E2/$2/$0.05 ranking reversal agree with the lead's analysis.

Disposition: pass for the stated retrospective logical analysis. No admission
to confirmation or hardware. Nonblocking limitation retained: archived budget
and component costs are inputs, and tiny counts are copied from their trusted
hashed archive; the tiny-copy helper is not a general duplicate-inventory
validator. Numerical tests are not a formal proof of every upstream certificate.

## Literature reviewer: Darwin

Agent01a0ae98-7368-7ef3-9429-9031ecdaad35 inspected the complete signal source,
method notes and targeted primary-paper passages listed in
[the prior-art note](CLAIM_PRIOR_ART_20260917.md). It judged the construction
plausibly useful as an implementation/certification study, with no demonstrated
new primitive or superior Asian-pricing algorithm.

It identified external arithmetic/Fourier comparators and the KL paper's
running-average alternative as important gaps. It supported GO for bounded
external comparator development and continued standby for confirmation and
manuscript promotion.

Follow-up document review requested four wording corrections, all applied:

1. Make equal remaining allowance explicit in the B-squared cost criterion;
   give the unequal-allowance correction separately.
2. Charge factor-to-price arithmetic to methods that actually use it; the
   reflection implementation pays for its own marginal rotations instead.
3. Label source readings as targeted passages and distinguish literature
   review from mathematical/numerical validation.
4. Distinguish the independent cube from the closure of correlated support.

The reviewer also checked the72 cell outcomes and emphasized dependent,
retrospective evidence, menu-specific feasibility and hypothetical bias allowances.

## Remaining external requirement

Independent human novelty/correctness assessment remains open. The unsent brief
in the prior-art note supplies concrete questions and evidence for that review.
Neither AI reviewer predicts acceptance or establishes priority over all prior work.
