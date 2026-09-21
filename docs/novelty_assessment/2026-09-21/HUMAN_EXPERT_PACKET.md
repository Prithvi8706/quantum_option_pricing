# Packet for a qualified human expert

Prepared 2026-09-21; **not sent**. No human has agreed to review or endorsed the
work. The user has not authorized external contact. This packet is intended
for a researcher familiar with quantum algorithms, reversible arithmetic and
numerical pricing; different experts may cover different parts.

## Self-contained problem and result

Price a discretely monitored arithmetic Asian-basket call under correlated
GBM: `V=exp(-rT) E[(d^-1 sum exp(mu_i+F_i Z)-K)+]`, independent normal Z.
D1 has one asset/two dates, sigma=.2/K=95; D2 has two assets/two dates,
sigma=.25/K=105/correlation=.4. Both use spot 100, rate .03, maturity 1, cutoff 4
and 10 bits per Gaussian coordinate. The target tolerance is $1 at ≥95%
confidence under ideal controlled logical gates/QFT, with 17 canonical AE
repetitions. Physical errors are unknown.

We compare a separable shared-reflection/QSP residual signal with emitted
fixed-point arithmetic. Arithmetic now has shared clean scratch, reduced
exponentiation and a degree-four classical control with a signed shifted
selector. The control expectation is certified from finite-model moments and
restored in decoding. Known primitives and the control/residual principle
are explicitly attributed.

| Case | Reflection CX / wires | Residual arithmetic CX / wires |
| --- | --- | --- |
| D1 | 36,469,403,102 / 55 | 104,719,289,723 / 4,733 |
| D2 | 1,101,392,680,835 / 103 | 375,312,500,844 / 5,162 |

These are control-cancelled logical projections, not runtime measurements.
D2's ratio is 2.9346, or 3.2892 in the conservative ledger. Against the exact
raw arithmetic parent, the new D2 oracle costs 13.78% more per A but uses
eightfold smaller AE M. This explains the correction to the earlier
reflection-over-raw-comparator conclusion.

## Most important novelty threats

Novak [eq.(25)](https://arxiv.org/pdf/quant-ph/0008124v3) explicitly combines
classical approximation integration with quantum residual estimation.
Stamatopoulos–Zeng [§4](https://arxiv.org/html/2307.14310v2) already provides
signed shifted comparator encoding and QSP pricing. Cibrario et al.
[§IV](https://arxiv.org/html/2507.19039v1) identifies normalization/query
tradeoffs. Chakrabarti's full resource study, Häner's optimized arithmetic
and Prakash's Asian running-average alternative are further necessary
comparators. Our proposed contribution is the certified implementation
comparison and its local consequence, not these general principles.

## Questions requiring reasons, not an approval score

1. Does the concrete matched-comparator/width/error result add enough knowledge
   for a paper beyond a useful implementation report? What exact earlier
   source most threatens it?
2. Is the independent-cube normalization result accurately restricted, and
   is any unproved assumption hiding in its QSP signal-plane use?
3. Is the residual certificate chain complete in its stated domain, including
   sum-scaled units, floor rounding, overflow, moment offset and the new
   exact-label conversion adapter?
4. Are the two logical ledgers sufficient for the proposed narrowly worded
   claim? Which common compiler or stronger arithmetic baseline is essential,
   rather than merely desirable?
5. Does the D2 width increase and classical tractability make the practical
   motivation too weak? Is the methodological/negative-result framing still
   meaningful?
6. Would one bounded common-policy oracle comparison resolve the main issue,
   or is substantial new research needed? If so, recommend narrowing or
   stopping rather than an open-ended advantage search.

## Materials and review record

Read [project state](PROJECT_STATE.md), [claim matrix](CLAIM_BY_CLAIM_ASSESSMENT.md),
[nearest methods](NEAREST_PRIOR_ART_MATRIX.md), [math audit](MATHEMATICAL_AUDIT.md),
[fairness audit](COMPARATOR_FAIRNESS_AUDIT.md), [decision](PUBLICATION_DECISION.md)
and [independent review record](REVIEW_RECORD.md). Source freeze `9511bc0c`,
residual source `23f8d948`, primary evidence-archive commit `60e735e1` and closeout `49b8f0a5`
are preserved in dev history. The project state links exact archives/receipts.

Current limits: no physical execution, no proved quantum-over-classical
advantage, no fresh confirmation, no final manuscript or submission. AI
reviewers examined distinct scopes but do not supply human expertise or
publication endorsement.

After actual review, record identity/affiliation with consent, expertise,
conflicts, inspected commit/documents, precise objections/references,
disagreements, corrections and residual uncertainty. Do not infer approval
from silence. Authorship and acknowledgement require actual contribution and
the eventual venue's policy, not a placeholder name in this packet.
