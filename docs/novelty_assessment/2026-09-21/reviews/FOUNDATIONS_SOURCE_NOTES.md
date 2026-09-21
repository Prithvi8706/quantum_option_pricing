# Lead assessor's foundation-source reading

Date 2026-09-21. These are the lead's readings, not a fourth independent review.
Primary metadata pages and complete relevant method passages were opened.

| Source | Verified version/publication | Inspected content | Relevance and limit |
| --- | --- | --- | --- |
| Gilles Brassard, Peter Høyer, Michele Mosca, Alain Tapp, *Quantum Amplitude Amplification and Estimation* | [quant-ph/0005055v1](https://arxiv.org/abs/quant-ph/0005055), 15 May 2000; AMS Contemporary Mathematics 305:53–74 (2002), [DOI](https://doi.org/10.1090/conm/305/05215) | [§4, Theorem 12 and algorithm steps](https://arxiv.org/html/quant-ph/0005055v1) | Exact-label AE probability theorem is inherited. No gate synthesis or floating-point sine guarantee is supplied by it. |
| Ashley Montanaro, *Quantum speedup of Monte Carlo methods* | [1504.06987v3](https://arxiv.org/abs/1504.06987), 11 July 2017 revision; Proc. R. Soc. A 471:20150301 (2015), [DOI](https://doi.org/10.1098/rspa.2015.0301) | [§§1.2, 2.2–2.3, Algorithm 3, Theorem 5 and proof](https://arxiv.org/html/1504.06987v3) | Signed mean estimation and centering with a variance bound are established. Our uniform-residual-scale canonical AE is not a new bounded-variance algorithm or a replication of this complexity theorem. |
| Steven Herbert, *The Problem with Grover-Rudolph State Preparation for Quantum Monte-Carlo* | [2101.02240v2](https://arxiv.org/abs/2101.02240), 18 May 2021; Phys. Rev. E 103:063302 (2021), [DOI](https://doi.org/10.1103/PhysRevE.103.063302) | [§§II–III, Theorem 1 and proof, multivariate appendix](https://arxiv.org/html/2101.02240v2) | Numerical integration during loading can consume the apparent query gain. Apply the proof's assumptions, particularly its classical MC integration step, rather than asserting every analytically specified normal loader is impossible. |
| Steven Herbert, *Quantum Monte Carlo Integration: The Full Advantage in Minimal Circuit Depth* | [2105.09100v4](https://arxiv.org/abs/2105.09100), 27 September 2022; Quantum 6:823 (2022), [DOI](https://doi.org/10.22331/q-2022-09-29-823) | [§3 Proposition 2/Theorem 3 and proof; §4 extension; §5 numerical comparison](https://arxiv.org/html/2105.09100v4) | Fourier expectation encoding and oracle-cost/query tradeoffs predate this project. Its smoothness conditions and 16-point univariate demonstration are not our nonsmooth multivariate Asian payoff or a matched circuit benchmark. |

Queries used: `quantum amplitude estimation control variates signed residual
expectation estimation pricing`; `QCE quantum Asian basket option pricing
quantum signal processing IEEE 2024 2025 2026`; `quantum Monte Carlo integration
advantages mean squared error Herbert 2021 state preparation`; four targeted
arXiv queries for BHMT, Montanaro, Herbert and Cui/control variates. Broader
results included tutorials, company documentation and aggregation sites;
these were not used as algorithmic priority evidence. The two Herbert papers
answer different questions and must not be conflated.
