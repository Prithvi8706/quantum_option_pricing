# Claim-specific prior-art and separate AI assessment

Date: 2026-09-17. This is a targeted review, not exhaustive novelty clearance.
The lead inspected the existing method/code, primary source passages and new
search results. A separate AI reviewer, Darwin (agent
01a0ae98-7368-7ef3-9429-9031ecdaad35), read the complete signal implementation
and method notes and performed the targeted source readings described below.
Readings are targeted full-text passages, not complete-paper readings. This
does not fulfill the pending human expert assessment requirement. The literature
review does not independently certify numerical error bounds or implementation
correctness; the mathematical/code review is attributed separately to Ampere.

## Nearest comparisons

| Primary source | Material inspected by separate reviewer | Consequence for our claim |
| --- | --- | --- |
| [Low/Chuang, qubitization](https://arxiv.org/pdf/1610.06546) | Section3.1, equations8–10, Lemma5 | PREP/SELECT and coefficient normalization are established |
| [Gilyen et al., QSVT](https://arxiv.org/pdf/1806.01838) | Section4.3 Definition51/Lemma52; Theorem17/Corollary18 | LCU and projected polynomial transformation are established |
| [Stamatopoulos/Zeng, QSP derivative pricing](https://arxiv.org/html/2307.14310v2) | Sections3–4 equations4,9–28; Section5.1 equations29–41 | Arithmetic-reducing QSP payoff encoding and its pricing pipeline predate us |
| [Karhunen–Loeve Asian pricing](https://arxiv.org/html/2402.10132v1) | Section3.3 equations42–45/Theorem3.3; Section5 equations70–73/Theorem5.1 | Both nested-estimation and running-average alternatives must be considered |
| [Wang/Kan, stochastic-volatility pricing](https://arxiv.org/html/2312.15871v3) | Section4.3 equations92–99 and Section4.4 equations110–112 | Explicit exponential/Asian-payoff arithmetic is another external baseline |
| [Kim, Cui, Lee and Park, Fourier-arithmetic payoff-oracle preprint](https://www.researchgate.net/publication/408635511_Scalable_Quantum_Derivative_Pricing_through_Fourier-Arithmetic_Payoff-Oracle_Design) | Sections3.1–3.5, Theorem1/equation3, Proposition2/Corollary3, equations4–5, Section4 and appendices | Same-payoff oracle redesign and Asian aggregation savings are already an active contribution category |

The July2026 preprint is author-uploaded, dated July8 and uploaded July9, with
ResearchGate DOI10.13140/RG.2.2.23693.50404. We did not establish a journal
publication or separate arXiv version. Its inputs are digitized prices and its
reported savings concern aggregation; our inputs are Gaussian factors and our
signal encodes their separable exponentials. Its assumed payoff rotation and
our full pipeline costs prevent importing its headline ratios into our ledger.

The KL paper's Section5 includes a coherent running average and final AE, not
only the nested construction in Section3.3. Therefore “avoids inner AE” is an
insufficient distinction from that paper as a whole. The earlier W1 note's
qualification about the *particular* inner-estimation construction remains
necessary. The alternative's model/precision assumptions differ from ours.

The Wang/Kan paper uses Heston dynamics, but its log-return exponentiation and
Asian payoff arithmetic are relevant subroutines. Its normalization assumptions
need reconciliation before any certified comparison in our GBM setting.

## Assessment

The probability-to-reflection identity and sharing a reflection between
block-diagonal preparations follow directly from known constructions. The
restricted normalization proposition is a useful correctness result but not
a standalone claim of a newly invented primitive.

The plausible contribution is the concrete separable-basket implementation,
logical numerical-error accounting, and measured normalization/circuit-cost
tradeoffs with an encoding-aware decision. No inspected source was shown to
contain the identical implementation; that absence is not proof of priority.
Independent human assessment and a matched external arithmetic comparison are
still missing. We should not describe these findings as sufficient for a
particular journal or as guaranteed novelty.

## Next bounded comparator study recommended by the review

Use the same GBM Gaussian factors, contract, cutoff, coordinate precision and
dollar tolerance. Compare the reviewed reflection construction against both
an efficient conventional arithmetic route and Fourier aggregation. Charge:

1. Common loading plus each implementation's own conversion costs. Arithmetic
   routes require factor-to-price conversion including exponentiation; the
   reflection route charges its exponential marginal rotations instead of a
   fictitious extra price-register conversion.
2. Aggregation, positive-part/payoff encoding and all uncomputation.
3. Representation, approximation and synthesis allowances on the same basis.
4. AE calls, controls, workspace and logical costs under the same conventions.

Begin with D1/D2 at simulator-feasible precision to verify identical targets,
then price the larger circuits only when their error model supports it. Freeze
the exact test menu and primary comparison before acquisition. Treat Fourier
aggregation as one component; comparing its aggregation count to our complete
signal or total AE count would be invalid. This is proposed follow-up work,
not an implemented or completed external benchmark.

## Human expert review brief (prepared, not sent)

Provide this note, CLAIM_THEOREMS_20260917.md, the W1/W2 methods/results and
the new sensitivity archive. Ask a quantum algorithms researcher:

- Is the exact shared-reflection/multiplexer realization already published?
- Is the correctness/error argument complete for the stated logical model?
- Does the implementation and decision result add enough beyond established
  LCU/QSP constructions to justify a distinct methodological contribution?
- Which additional comparator or theorem would change that assessment?

Request written reasons and references, record actual reviewer contributions,
and retain disagreements. No expert has been contacted or credited here.
