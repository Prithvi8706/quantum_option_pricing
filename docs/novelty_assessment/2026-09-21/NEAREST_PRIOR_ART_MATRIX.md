# Nearest-method comparison

Date 2026-09-21. Source IDs resolve to the
[verified bibliography](PRIMARY_SOURCE_BIBLIOGRAPHY.md); exact inspected
versions and access limits are retained there and in reviewer notes. The
comparisons below are our assessment of inspected material, not statements
that an external implementation was reproduced.

## Common notation

Our target is `D E[(A-K)+]`, where `A=d^-1 sum exp(mu_i+F_i z)`.
For radius B, `x=(A-K)/B`, `C(A)=B(x+p4(x))/2`, and
`r=(A-K)+-C(A)`. Reflection uses a QSP approximation to the residual and
Hadamard probability `a_ref=(1-Re E[U_QSP])/2`; arithmetic computes a signed
integer residual R and uses `a_ar=(E[R]+H)/2^m`.
Offsets restore the original target. The arithmetic affine decoder is
`O-DH/(dQ)+D 2^m a_ar/(dQ)`; its slope, not the nominal polynomial degree,
sets statistical sensitivity. Our symbol Q=2^f is fixed-point scale, not an
oracle query count.

## Formula-specific nearest overlaps

| Source and location | Source-to-project map | Nature of difference and consequence |
| --- | --- | --- |
| [N1 Novak, §3 eq.(25), pp.8–10](https://arxiv.org/pdf/quant-ph/0008124v3) | `f → payoff`, `P_n f → C`, `I(P_n f) → O/D`, quantum integral of remainder → `E[r]` | Classical approximation plus quantum residual is an explicit predecessor. Fixed truncated-normal moments and reversible error accounting specialize it; no new residual-estimation principle. Hölder-class rates do not transfer automatically through the payoff kink. |
| [N2 Stamatopoulos–Zeng, §4 eqs.(20)–(27)](https://arxiv.org/html/2307.14310v2) | shifted digital x, scale 2^p → our `R+H`, `2^m`; invert affine map → restored residual mean | Uniform comparison and signed shifting are established. Our signed overflow, exact floor operation order and offset certificate add implementation obligations, not a distinct primitive. |
| [N2 §§3–5 eqs.(9)–(17), (29)–(41)](https://arxiv.org/html/2307.14310v2) | digital log-return signal/QSP payoff → separable basket signal/QSP residual | Different signal realization and application; polynomial transformation/AE pipeline already known. An arithmetic-free payoff label alone cannot carry novelty. |
| [N3 Cibrario et al., §IV-A eq.(25), §IV-E](https://arxiv.org/html/2507.19039v1) | normalization R → our probability-to-dollar slope L; target payoff precision → available dollar margin | Normalization can outweigh a shallower oracle. Our discrete certified menu and observed reversal are specific evidence of this established tradeoff, not its discovery. |
| [N4 Prakash et al., §§3.3,5 eqs.(42)–(45),(70)–(73), Theorem 5.1](https://arxiv.org/html/2402.10132v1) | running average Gbar → A; payoff maximum scale → B-type normalization | Section 5 already avoids nested AE by coherent arithmetic and final AE. Shared reflection differs concretely, but “no inner AE” is insufficient novelty. Different path approximation and asymptotic precision prevent numerical cost transplantation. |
| [R1 Chakrabarti et al., §4.2, eq.(42), AppendixC](https://arxiv.org/pdf/2012.03819v3) | Gaussian reparameterization and fixed-point conversion → archived `mu,F` and w/f conversion; summed error allowances → dollar ledger | Full pricing-resource/error analysis predates us. Our directed certificates, control matching and full evidence archive are more specific; this is not the first complete resource accounting. |
| [R2 Häner et al., §III TablesI–II and appendices](https://arxiv.org/pdf/1805.12445v1) | Horner/pebbling → our Horner scratch; piecewise minimax exp → our reduced Taylor plus squaring | A stronger arithmetic alternative remains unimplemented here. Shared clean scratch is a standard optimization; an external comparable implementation could change rankings. |
| [N6 Herman et al., §§4.2–4.3 eqs.(4.1)–(4.16), Theorem 4.1](https://arxiv.org/html/2602.03725v1) | `f∘g`, independent primitive density → positive-part lognormal payoff, Gaussian factors | Truncation/quadrature/arithmetic/loading/AE coupling is prior work. Exact cell masses and midpoint versus density quadrature are substantive target discretization differences, not proof of superiority. |

These eight source-specific comparisons are the principal novelty tests.
Further relevant mechanisms: [N5 published §3.1 and AppendixB](https://link.springer.com/article/10.1140/epjqt/s40507-025-00328-3)
estimates signed real amplitudes using mRQAE; our shifted Bernoulli encoding
is different but cannot claim first signed pricing. [K1 §3, AppendixA](https://www.researchgate.net/publication/408635511_Scalable_Quantum_Derivative_Pricing_through_Fourier-Arithmetic_Payoff-Oracle_Design)
replaces aggregation of already-digitized prices and assumes the payoff
rotation in its preservation statement. Our Gaussian-to-price conversion and
complete AE ledger are additional costs. Its aggregation savings are not a
matched full-pipeline result.

## Complete comparison contract

The cells below identify what must match before a numerical head-to-head claim.
“Not matched” is an assessment limitation, not an accusation that the source
failed its own stated purpose.

| Dimension | This project | Closest source-specific difference |
| --- | --- | --- |
| Financial payoff/model | Discretely monitored GBM arithmetic Asian basket, fixed D1/D2 | N2/N3/R1 autocallable and/or TARF examples; N4 Asian path construction; N8 Heston; N5 broader signed payoffs |
| Continuous vs finite | Exact conditional normal cell masses/midpoints with separate continuous-model bound | N6 density/quadrature discretization; N1 unit-cube integration; K1 digitized price register |
| State preparation | Dense marginal multiplexers, loading and inverse charged | N4 KL path preparation; R1 variational/integrator alternatives; N10 assumes oracles; R4 excludes asset-state loading from loading-component comparison |
| Signal/amplitude | Separable row reflection plus QSP, or integer residual selector | N2 digital log-return QSP/comparator; N5 expectation as signed amplitude; N3 exponential integration loading |
| Normalization | Universal cube B, signed shift H, explicit decoder sensitivity | N2/N3 similarly price rescaling; N4 path maximum; N8 sampled-maximum convention requires extra justification for our uniform contract |
| Classical control/offset | Fixed degree-four finite-model moments, directed offset bridge | N1 establishes approximation-plus-residual principle; external pricing sources do not supply our identical control-cost-matched benchmark |
| Polynomial approximation | QSP menu 16/32/64/128; arithmetic Taylor degrees 8/12/16 and s=1/2/3 | R2 piecewise minimax/Horner; N2 payoff-specific QSP; N1 abstract approximation class |
| Precision/rounding | Exact archived binary inputs; signed floors; w40/48, f20/24 | R1/R2 fixed precision under different domains/error contracts; external rows not translated into ours |
| Signed residual | Universal magnitude, strict shift, no clipping, certified affine restoration | N2 already shifted comparison; N5 sign-aware amplitude readout; implementation distinction, not first signed encoding |
| Uncomputation | Emitted conversion/control inverses, retained allocations | R2 TableII compute-only must be doubled/composed appropriately; N4/K1 explicitly describe cleanup; no free inverse assumption here |
| Controlled operations | Conservative controlled-gate and cancellation ledgers, QFT swaps | External gate controls/AE constructions differ; full controlled-oracle costs must be reconstructed before import |
| AE/confidence | Canonical AE, 17 independent repetitions, ≥95% theorem convention | N2/R1 estimates use 68%; N3/R4 use IQAE conventions; N5 mRQAE; N1/F2 oracle-level integration algorithms |
| Deterministic allowance | Representation, arithmetic/QSP, loading, offset, discount and decoder | N6 and R1 already split full errors, but with different discretizations/bounds; “first error budget” unsupported |
| Basis/compiler | Component U/CX decomposition, no global optimization or native synthesis | N2/R1 Clifford+T; K1 `{cx,u3}` WeightedAdder aggregation table; R5 Q#/Azure physical model |
| Width | All allocated wires and reflection ancillas, including shared workspace | R2/R3 pebbling could improve arithmetic width; R4 depth analysis assumes unrestricted allocation |
| Depth | Primary remapped dependency depth; residual serial upper bound | External T-depth/parallel loading/scheduler conventions differ; no matched depth winner currently |
| Classical preprocessing | Offset cell/exp counts and setup separate, no CX/seconds addition | N1 deterministic approximation work; N2 phases; R1/R5 compiler/setup assumptions differ |
| Hardware assumptions | Ideal controlled gates/QFT; physical allowance null | R1/R5 architecture-specific runtime estimates; these cannot be imported to turn our CX ratio into speedup |

## Distinctions that survive the mapping

The concrete separable-basket realization, coherent scratch layout, directed
signed arithmetic certificate and recoverable complete comparison are useful
application and engineering contributions. The consequential result is an
auditable cost-order change when a previously unmatched control is supplied.
No inspected source was verified to contain this exact D1/D2 implementation
table; this is evidence about the comparison's specificity, not proof of
world-first priority. A convincing paper must explain what the comparison
teaches beyond implementing known building blocks and must retain its
unfavorable width, absolute costs and comparator limitations.
