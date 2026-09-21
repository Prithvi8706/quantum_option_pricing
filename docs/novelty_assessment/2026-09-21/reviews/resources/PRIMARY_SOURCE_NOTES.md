# Resource-review source notes and search record

AI resource/comparator reviewer; search date 2026-09-21. This is a scoped
supplement to the main literature review, not a claim to exhaustiveness.
Full papers were available for the methods below; the locations listed identify
what was actually examined. No external implementation or physical estimate was
rerun. Metadata, mathematical relevance and access limitations are distinguished.

## Core sources

### R1 — Chakrabarti et al., derivative-pricing resource threshold

Shouvanik Chakrabarti, Rajiv Krishnakumar, Guglielmo Mazzola, Nikitas
Stamatopoulos, Stefan Woerner and William J. Zeng, **A Threshold for Quantum
Advantage in Derivative Pricing**, *Quantum* 5, 463 (2021), published June 1,
2021; [publisher/DOI](https://quantum-journal.org/papers/q-2021-06-01-463/).
[arXiv:2012.03819v3](https://arxiv.org/abs/2012.03819v3), May 25, 2021; v1 was
December 7, 2020. Peer-reviewed publication verified.

Inspected §§2–4.2.3, §5 and Appendix C.1–C.2, with Table 1 and Eq. (65)–(66).
Eq. (42) allocates truncation, discretization, arithmetic and AE error; the
paper already includes Gaussian reparameterization, price-space conversion,
payoff arithmetic and cleanup. Its §4.2.3 benchmark confidence is 0.68,
not this project's 0.95. Appendix C uses piecewise polynomial exponentials
from R2 and first-order approximations in parts of its error analysis.

Mapping: their path dimension `dT` is our flattened asset/date count; their
fixed-point `(n,p)` corresponds to `(width,width-fraction_bits)`. Different
contracts, payoff scales, loader assumptions and T-depth costs preclude
transferring their headline resource numbers into our CX comparison.

### R2 — Häner, Roetteler and Svore, optimized arithmetic

Thomas Häner, Martin Roetteler and Krysta M. Svore, **Optimizing Quantum
Circuits for Arithmetic**, [arXiv:1805.12445v1](https://arxiv.org/abs/1805.12445v1),
May 31, 2018. The inspected arXiv record gives no journal version; no publication
status beyond that record is inferred.

Inspected §§III–IV, Appendix A/B and Table II. Horner evaluation, reversible
piecewise minimax approximation and register/depth tradeoffs are prior art.
Table I supplies optimal pebbling steps for a line of Horner iterations;
Table II covers `exp(-x)` and explicitly reports compute-only Toffoli counts.
Its piecewise approximation differs from our single range-reduced Taylor
polynomial and repeated squaring, but is a consequential missing optimized
arithmetic comparator. Its counts cannot be pasted into our ledger: signed
domain reduction, spot scaling, error certification, interval selection and
cleanup must match first. Source describes an automatic circuit-generation
software module; that module was not executed here.

### R3 — Meuli et al., reversible memory management

Giulia Meuli, Mathias Soeken, Martin Roetteler, Nikolaj Bjørner and Giovanni
De Micheli, **Reversible Pebbling Game for Quantum Memory Management**,
DATE 2019; [arXiv:1904.02121v1](https://arxiv.org/abs/1904.02121v1), April 3,
2019. The arXiv record explicitly identifies DATE publication. An author-hosted
[EPFL paper](https://si2.epfl.ch/demichel/publications/archive/2019/Reversible%20Pebbling%20Game%20for%20Quantum%20Memory%20Management.pdf)
also supplied the full method.

Inspected §II, Definitions 2–3, §III and §IV/Fig. 3–4. Computing and uncomputing
vertices under predecessor constraints formalizes the same cleanliness
obligation used by our shared conversion scratch. Their SAT method explores
space/operation tradeoffs; our fixed manual wire remapping is a simpler
application, not a new pebbling algorithm. This rules out novelty from scratch
reuse itself. No claim is made that their compiler was applied to our circuits.

### R4 — Cibrario et al., non-IonQ QCE pricing comparison

Francesca Cibrario, Or Samimi Golan, Giacomo Ranieri, Emanuele Dri, Mattia
Ippoliti, Ron Cohen, Christian Mattia, Bartolomeo Montrucchio, Amir Naveh and
Davide Corbelletto, **Quantum Amplitude Loading for Rainbow Options Pricing**,
IEEE QCE 2024, pp. 211–220,
[DOI 10.1109/QCE60285.2024.00034](https://doi.org/10.1109/QCE60285.2024.00034).
Publication verified through the authors' [Politecnico institutional record](https://iris.polito.it/handle/11583/2991825)
and official [QCE accepted-program document](https://qce.quantum.ieee.org/2024/wp-content/uploads/sites/8/2024/08/QCE24-Accepted-Technical-Papers-by-Track-QALG-QSYS-QAPP-QPHO-QNET-QTEM-QML.pdf).
[arXiv:2402.05574v3](https://arxiv.org/abs/2402.05574v3), October 1, 2024;
v1 February 8, 2024.

Inspected §§II–V, especially Eqs. (5)–(10), loading constructions and
(26)–(32). Monotonicity moves a rainbow maximum into log space; this does
not turn our arithmetic mean of exponentials into an exponential of a mean.
It compares direct and integration loading, so application-specific encoding
comparisons predate this project. §IV excludes asset state preparation and
maximum arithmetic, and assumes unrestricted qubits in its depth analysis.
Its IQAE/simulator results are not a matched certified D1/D2 resource baseline.
Author implementation link is reference [34]; code was not rerun. Publisher
DOI retrieval failed; full methods were read in the author arXiv version.

### R5 — Fedoriaka, Goldsmith and Chen, non-IonQ QCE arithmetic selection

Dmytro Fedoriaka, Brian Goldsmith and Yingrong Chen, **Quantum Arithmetic
Algorithms: Implementation, Resource Estimation, and Comparison**, IEEE QCE
2025, pp. 349–355,
[DOI 10.1109/QCE65121.2025.00047](https://doi.org/10.1109/QCE65121.2025.00047).
[arXiv:2509.07015v1](https://arxiv.org/abs/2509.07015v1), September 6, 2025,
now explicitly records the QCE publication and DOI. Do not label it solely
an unpublished preprint.

Inspected §§II–IV, Figs. 1–2 and §IV.G. The paper's Q# library covers unsigned
integer arithmetic, algorithm selection and space/runtime crossovers, with
Azure's stated hardware/error model. Its modular exponentiation is unrelated
to a real financial exponential. §IV.G explains how its scheduling convention
can conceal logical parallelism and why coherent cleanup must be charged.
Our signed rounding/overflow and dollar contracts remain extra obligations.
Their [author code](https://github.com/fedimser/quant-arith-re) is already
discussed by the project's earlier audit; no new source execution is claimed.

### R6 — Quetschlich et al., resource-driven application development

Nils Quetschlich, Mathias Soeken, Prakash Murali and Robert Wille,
**Utilizing Resource Estimation for the Development of Quantum Computing
Applications**, [arXiv:2402.12434v2](https://arxiv.org/abs/2402.12434v2),
August 20, 2024; v1 February 19, 2024. QCE24 acceptance verified in the
[official program](https://qce.quantum.ieee.org/2024/wp-content/uploads/sites/8/2024/08/QCE24-Accepted-Technical-Papers-by-Track-QALG-QSYS-QAPP-QPHO-QNET-QTEM-QML.pdf).
No unverified proceedings DOI is supplied.

Inspected §III, §IV and Table III. Algorithm/encoding selection driven by
resource estimates is established methodology. Their full-stack examples
show why logical width/count changes need not propagate proportionally to
physical width/runtime. Our fixed-menu argmin is not a new general selection
principle. Their chemistry case study is not a pricing competitor, and neither
their hardware assumptions nor resource numbers were imported into our study.

### R7 — Liu and Owen, strong classical Asian-basket comparator

Sifan Liu and Art B. Owen, **Preintegration via Active Subspace**, *SIAM Journal
on Numerical Analysis* 61(2), 495–514 (2023),
[DOI 10.1137/22M1479129](https://epubs.siam.org/doi/10.1137/22M1479129).
Author preprint titled **Pre-integration via Active Subspaces**,
[arXiv:2202.02682v1](https://arxiv.org/abs/2202.02682v1), February 6, 2022.
Publisher metadata/abstract accessed; formula references here identify the
accessible 27-page author preprint, not an asserted page-identical final version.

Inspected §3/Theorem 3.2, §4/Algorithm 1 and §5.1–5.2, Eqs. (15)–(16).
For positive first-column loadings, their strike-root conditional expectation
maps directly to `asian_basket.conditional_call`: with root `gamma`, it is
`sum(c_i exp(b_i^2/2) Phi(b_i-gamma))-K Phi(-gamma)`. This classical mechanism
is prior work. The paper studies arithmetic Asian baskets as well as Asian
options, and warns about cost and monotonicity conditions. Our paid pilot and
finite floating diagnostics do not create a new conditional-integration method
or a rigorous end-to-end classical interval.

### R8 — Liu, constrained directions for conditional QMC

Sifan Liu, **Conditional Quasi-Monte Carlo with Constrained Active Subspaces**,
*SIAM Journal on Scientific Computing* 46(5), A2999–A3021 (2024),
[DOI 10.1137/23M1548918](https://epubs.siam.org/doi/10.1137/23M1548918).
Publication metadata also verified in the author's [Duke record](https://scholars.duke.edu/publication/1682994).
[arXiv:2212.13232v2](https://arxiv.org/abs/2212.13232v2), July 24, 2023;
v1 December 26, 2022.

Inspected preprint §3, Theorem 3.1/Algorithm 1, and §4 option examples and
Table 5. It optimizes remaining directions subject to a tractable
preintegration direction. This extends the menu of relevant strong classical
comparators beyond vanilla Monte Carlo. It does not by itself certify the
project's finite classical intervals. The final publisher text was not
compared line-by-line with the author preprint.

## Search trail, coverage and exclusions

Queries were issued in these groups; searches led to primary paper records,
full arXiv/author PDFs, proceedings programs and institutional metadata. Snippets
were used only for discovery, never as the sole support for mathematical claims.

| Query group (actual strings or close, recorded query terms) | Disposition |
| --- | --- |
| `Chakrabarti Krishnakumar Mazzola Stamatopoulos Woerner Zeng threshold quantum advantage derivative pricing 2021 resource`; exact title | R1 included; full relevant methods and resource appendix read |
| `Häner Roetteler Svore Optimizing Quantum Circuits Arithmetic 2018 polynomial evaluation exponential`; exact title/arXiv | R2 included; general piecewise circuit comparator is relevant, direct published-table cost comparison is not |
| `quantum reversible pebbling space time tradeoff Bennett 1989 logical reversibility computation`; exact Meuli title | R3 included; Bennett primary theorem not separately audited in this scope, no theorem quotation inferred from secondary summaries |
| `QCE quantum option pricing resource estimation Asian basket arithmetic 2024 2025`; `site.qce.quantum.ieee.org pricing`; exact Rainbow title | R4 included; official QCE24 program also located R6 |
| `Quantum Arithmetic Algorithms: Implementation, Resource Estimation, and Comparison`; arXiv2509.07015 | R5 included; current publication metadata corrected; unrelated modular exponentiation excluded as payoff substitute |
| `Utilizing Resource Estimation for the Development of Quantum Computing Applications`; title plus QCE60285 | R6 included as methodology prior art, not matched finance experiment |
| `conditional quasi-Monte Carlo Asian options Glasserman`; `Asian preintegration Griebel Kuo Sloan`; exact Liu/Owen and Liu titles | R7/R8 included as strong classical prior art; barrier/Heston-only papers were secondary leads, not nearest D1/D2 comparators |
| `Quantum Amplitude Loading for Rainbow Options Pricing 10.1109`; exact Meuli title plus DOI | Institutional publication record verified R4; proceedings DOI access errors retained as limits |

An additional current lead, Jiaxin Yu and Xiaoqun Wang, **Importance sampling
and active subspace method in quasi-Monte Carlo**, [arXiv:2603.01763](https://arxiv.org/abs/2603.01763),
March 2, 2026, was found through classical-method search. Only abstract-level
screening was completed; its claimed out-of-the-money improvements were not
used as verified performance facts. It is a follow-up reading item if the
project pursues classical superiority. This scoped search does not certify
absence of newer work, non-English work or inaccessible industrial algorithms.

The browser's IEEE DOI retrieval returned internal errors for R4; the author
preprint and institutional record were usable. SIAM publication pages exposed
metadata/abstracts; formulas were reviewed in author versions. Secondary
patent/aggregator/AI-summary pages discovered during searches were excluded as
technical evidence. No correspondence, access purchase or cloud/hardware job
was initiated.
