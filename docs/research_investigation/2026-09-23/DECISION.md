# Independent search for a significant quantum advantage in option pricing

Investigation dates: 22–23 September 2026. Literature priority: 22 September 2024
onward, especially 22 March–22 September 2026, with foundational work traced where
needed. This is a selective, primary-source investigation, not exhaustive coverage
or priority clearance. The 22 September manuscript, every earlier study and every
archived result are unchanged. Nothing here is held-out confirmation.

## 1. Verdict

**No defensible significant quantum advantage established yet.**

- **Level 1** (demonstrated end-to-end hardware advantage): none exists for option
  pricing, in this project or in the 152 screened sources and venues.
- **Level 2** (conditional end-to-end fault-tolerant crossover): none exists. The
  canonical finance threshold needs a sustained ~10 MHz logical T-rate just to *match* a
  one-second classical target. That target was a weak comparator at 68% confidence
  ([Chakrabarti et al., Quantum 2021](https://arxiv.org/abs/2012.03819)).
- **Level 3** (algorithmic/query advantage): established only generically. Amplitude
  estimation and quantum multilevel Monte Carlo are at most quadratic against Monte
  Carlo (MC), roughly zero against randomized QMC (RQMC) on smoothable payoffs, and there
  is no proven classical lower bound for structured financial integrands.
- **Level 4** (improvement over another quantum implementation): the current manuscript
  and the five feasibility studies.

This investigation adds something the earlier ones lacked: a single quantitative law
that explains all five executed failures. It was then measured against a stronger
classical side, including the one payoff class where classical smoothing fails. For a
10× win, a complete coherent source call may cost at most

    rho_max = N_C(eps) * e_stat / (10 * k * sigma_Q)          [in classical-sample units]
    D_max   = T_C(eps) / (10 * k * (sigma_Q / e_stat) * t_layer)  [in logical T-layers]

where
- N_C(ε) and T_C(ε) are the sample count and complete latency of the strongest
  classical method;
- σ_Q is the per-sample standard deviation available to the quantum estimator;
- e_stat is the statistical error allowance;
- k collects the estimator, inverse-call and confidence constants;
- t_layer is the time of one logical T-layer.

Measured on 416-dimensional basket workloads, the D_max budget is a few to a few
thousand T-layers per call (§3). The best published per-call depth is ~10⁴, and this
project's certified source is 1.2×10⁷. Realistic logical T-layers are 1–100 µs.

**Best remaining falsifiable hypothesis (H1).** Discretely monitored multi-asset
knock-out (barrier/autocallable-type) payoffs. These are the only workloads found where
the strongest classical smoothing tried here leaves RQMC near the Monte Carlo rate.
Measured classical exponents are p_C ≈ 1.6–2.1, against a quantum p_Q = 1. Even so, H1
reaches a 10× crossover at a penny per $100 only by combining four optimistic
assumptions:
- a single-thread interpreted classical implementation;
- an ideal estimator constant, k = 1;
- 100 ns logical T-layers;
- a ~10⁴-depth oracle for an 8-asset × 52-date barrier.

With one GPU, k = 10 and 1 µs T-layers, the budget falls to about 4 T-layers per call.
It would need a price accuracy of about $3×10⁻⁷ per $100 to fit a 10⁴-depth oracle. H1
is therefore a hardware- and implementation-conditional level-2 hypothesis whose
cheapest falsifier costs one week (§6). It is not a result.

This conclusion does not reflect insufficient effort in the earlier work. Its studies
removed conservative estimators (1,280–2,119× fewer iterations) and serial arithmetic
(38–108× shallower). Each time, the remaining gap was set by the same two facts:
- the precision speedup is at most quadratic and vanishes against RQMC;
- a logical operation on a fault-tolerant machine costs 10⁴–10⁹ times a classical
  floating-point operation.

The published expert position agrees. Derivative pricing is placed in the
quadratic-speedup-only class by
[Babbush et al., PRX Quantum 2021](https://arxiv.org/abs/2011.04149),
[Hoefler–Häner–Troyer, CACM 2023](https://arxiv.org/abs/2307.00523) and
[The Grand Challenge of Quantum Applications, 2025](https://arxiv.org/abs/2511.09124).
Two 2025–2026 pricing papers claiming exponential or separation results were withdrawn
or corrected by their own authors (§4).

## 2. Diagnosis of the current project

### One law, five failures

| Executed study (all development cases) | Classical side that won | Reported miss | Term of the law that decided it |
|---|---|---|---|
| Antithetic quantum MLMC, correlated Heston baskets ([results](../../antithetic_feasibility/RESULTS.md)) | Controlled RQMC base + antithetic MLMC, 13.75 s warm / 45.68 s cold for $0.01 | 32–523× even with k=1, 100 ns/T-layer and only square-root depth charged | Classical base level is cheap RQMC (p_C≈1); corrections free to both |
| Compound Asian, quantum-inside-quantum ([results](../../compound_feasibility/RESULTS.md)) | GBM factor reuse + conditional geometric control, 8–16 s | per-source budget 2–44 ns vs 7.6 ms for one multiply | Classical structure removed the nesting; ρ ≫ ρ_max |
| Controlled parity residual ([results](../../controlled_residual_feasibility/RESULTS.md)) | Same controls, 11.1 s / 13.8 s | ≤3–5 ms per complete source needed | Variance reduction helps both sides equally (σ_Q and σ_C shrink together) |
| Complete source + explicit estimator ([results](../../controlled_source_completion/RESULTS.md)) | As above | seconds-to-years scale | k and depth both large |
| Priority completion: Hadamard estimator, narrow multipliers, wave schedules ([results](../../controlled_priority_completion/RESULTS.md)) | As above | 17,468× / 42,499× at a hypothetical 1 ns/T-layer | Per-call wave T-depth 1.16×10⁷ / 1.53×10⁷ ([combined_cost.json](../../../results/controlled_priority_completion/combined_cost.json)) against a measured ρ_max of ≈0.1–24 classical point-evaluations |

From the project's own artifacts, one clean C4 source call has a wave-scheduled T-depth
of 1.16×10⁷ and ~5.7×10⁸ T gates. The compound classical comparator spent ~2.6 µs per
inner sample. Hence ρ ≈ 4.5×10³ at a hypothetical 1 ns per T-layer, and ≈ 4.5×10⁶ at
1 µs. The measured ρ_max at $0.01 is only ≈0.1–24 classical point-evaluations for
k = 10–1, or ≈1–170 plain-path evaluations (§3). One complete coherent call may cost
no more than a few classical paths.

### Fundamental obstacles (persist under better compilation)

1. **Precision exponents.** Quantum mean estimation is at most quadratic against
   randomized classical sampling. In Sobolev/Hölder classes the gap is
   1/(s+½) − 1/(s+1) ≤ 1, falling to 0 as the smoothness-to-dimension ratio s grows
   (Heinrich–Novak quantum integration results, screened by lane L04). Scrambled nets
   reach RMSE ≈ n^(−3/2) on smooth integrands, so on preintegrated payoffs generic
   amplitude estimation (n^(−1)) is *asymptotically worse*.
2. **Per-operation latency.** A 33-bit reaction-limited carry-lookahead addition takes
   ~20 µs even with a 1 µs reaction time, and ~1.6 ms by ripple-carry lattice surgery.
   A CPU addition takes under 1 ns; a GPU does roughly one floating-point operation per
   picosecond ([The Fast for the Curious, 2025](https://arxiv.org/abs/2510.26078)).
   Demonstrated decoder latency is ~63 µs
   ([Willow, Nature 2025](https://arxiv.org/abs/2408.13687)).
3. **Parallelism asymmetry.** Parallel amplitude estimation now appears to scale
   linearly in the number P of devices ([arXiv 2508.06121](https://arxiv.org/abs/2508.06121),
   which corrects an earlier √P lower bound). But each lane needs a full copy of the
   coherent oracle workspace. Under a physical-qubit ceiling, P_Q is ~1–10, while a
   classical node has 10⁴+ lanes.
4. **Classical access to integrand structure.** Controls, conditioning, preintegration
   and factor reuse reduce σ and raise the RQMC rate for both sides' *target*. Only the
   classical side exploits them at native speed.

### Implementation limitations (real, but insufficient)

| Limitation | Plausible remaining gain | Evidence |
|---|---|---|
| Serial / ripple reversible arithmetic | ~10–100× (reaction-limited carry-lookahead, at large qubit/factory cost) | 2510.26078 §V; project wave schedules already 38–108× |
| Estimator constants | Bounded: the project's ideal-query sensitivities already grant k = 1 and still miss, after the 1,280–2,119× estimator redesign | controlled_priority_completion |
| Gaussian loading and exp/sqrt precision | ≤ ~10× (payoff-loading modules are a small share; see [2507.19039](https://arxiv.org/abs/2507.19039)) | L07 rows |
| Memory policy / retained history | qubit count, not latency | earlier studies |

The combined optimistic gain is ~10³ at most. The latest miss is 1.7–4.2×10⁴ at an
already-favourable 1 ns T-layer. At realistic 1–10 µs layers the miss is 10⁷–10⁸.

### Reusable assets

- Directed price-error ledgers and continuous-to-finite-law bridges.
- The certified signed fixed-point compiler: range proofs, narrow multipliers, wave
  schedules and emitted gate files.
- Explicit estimator schedules with finite-confidence certificates.
- Strong classical baselines: PCA/conditional RQMC, antithetic MLMC, geometric and
  parity controls, empirical-Bernstein fixed-N contracts.
- The six-oracle common-policy comparison, provenance tooling and test suites.
- Two new executed pilots (§3) and a 152-row screen (§4).

These are exactly the ingredients of a measured advantage-frontier study (§6).

### What could change the outcome (and by how much)

| Assumption | Current choice | What changing it buys |
|---|---|---|
| Logical T-layer time | 1 ns–1 µs sensitivities | Must reach ≲100 ns *sustained, reaction-limited* for H1 even against slow classical code; no roadmap projects this (§3) |
| Classical implementation | project: vectorized CPU; pilot: single-thread numpy | A GPU makes classical 10²–10³× faster (STAC-A2: ≤1 ns per Heston asset-step per H100); this *removes* the only favourable corner |
| Payoff class | smooth Asian call | Discontinuous multi-date payoffs are the only class with measured p_C ≈ 1.6–2.1 after the smoothing tried |
| Accuracy contract | $0.01–$0.10 absolute | The quantum budget grows like ε^(−(p_C−1)); a 10× win at fair assumptions needs ε ≲ $10⁻⁶ per $100 |
| Output contract | one price | Multi-output favours classical (AAD, shared paths); aggregate pricing reduces to one expectation (L09) |

## 3. Executed calculations (development only)

All scripts, raw JSON and logs are in
[`research/advantage_frontier_20260923/`](../../../research/advantage_frontier_20260923/)
and [`results/advantage_frontier_20260923/`](../../../results/advantage_frontier_20260923/).
The contract throughout is exact-date correlated GBM, so neither side pays SDE bias. The
basket has equal weights, σ=.3, equicorrelation .4, S0=K=100, r=.03, T=1. Knock-out
occurs when any date's basket value is at least 140. There are 32 independent Owen
scrambles of Sobol points up to 2¹⁵ each, and fixed development seeds. Rates are fitted
to one-scramble RMSE for n ≥ 2⁸. Timings are single-thread numpy on an Intel
16-core/22-thread laptop, a deliberately *weak* classical implementation that favours
quantum.

### P1: best-classical error-vs-work exponents

In the table, r is the fitted RQMC error rate (error ∝ n⁻ʳ), p_C = 1/r is the classical
cost exponent, and preint is RQMC after analytic preintegration along the first
principal direction.

| Case (dim) | Payoff | Plain RQMC r | + geometric control r | + first-PC preintegration r | Pointwise σ, raw → best ($) |
|---|---|---:|---:|---:|---:|
| 4×12 (48) | call | 0.926 | 0.794 | **0.986** | 9.18 → 0.95 |
| 8×52 (416) | call | 0.961 | 0.767 | **0.958** | 8.15 → 0.81 |
| 4×12 | digital ($100) | 0.548 | 0.611 | **1.012** | 48.5 → 5.14 |
| 8×52 | digital | 0.532 | 0.608 | **0.969** | 48.5 → 4.94 |
| 4×12 | knock-out call | 0.596 | n/a | **0.631** | 5.73 → 1.25 |
| 8×52 | knock-out call | 0.568 | n/a | **0.571** | 5.15 → 1.14 |

All estimators agree within their standard errors. For example, the 8×52 knock-out
price is 3.28247 ± .00139 plain and 3.28156 ± .00021 preintegrated. Preintegration is
exact and analytic: every asset/date loading on the first principal direction is
positive, so each payoff is monotone or interval-supported along it.

**Finding.** Smoothing restores near-n⁻¹ convergence for the call and the digital. It
does *not* for the multi-date knock-out: after preintegration, the kinks from the max
over dates remain in the other directions.

### P2: one-step-survival conditioning for the knock-out

This is the Glasserman–Staum estimator adapted to the basket: at each date the survival
indicator is replaced by its conditional probability along the first asset principal
component, with a truncated-normal draw. It is unbiased (4×12: 3.5166 ± .0016; 8×52:
3.2844 ± .0029). Its time-ordered construction gives rates of r = 0.571 (4×12) and
**0.479** (8×52), with pointwise σ of 4.4–4.5. It is worse than first-PC
preintegration. The strongest classical barrier method measured here therefore has
p_C ≈ 1.6–1.75.

**Untried and eligible** (these could still close H1):
- multi-direction numerical smoothing ([Bayer et al.](https://arxiv.org/abs/2111.01874));
- conditional pathwise smoothing with effective-dimension reduction for barrier payoffs
  ([Albieri et al., arXiv 2504.11576](https://arxiv.org/abs/2504.11576), presented at
  MCQMC 2024; abstract-only here);
- Brownian-bridge-ordered one-step survival;
- importance sampling toward the barrier;
- GPU execution.

### Frontier (quantum budget from P1's strongest barrier method)

Here g is the classical speed-up over the measured single-thread numpy: 1 is as
measured, 16 is one multicore CPU, 100 is one GPU, conservative by STAC-A2.

| Case | g | k | t_layer | D_max at $0.01 | ε at which D_max = 10⁴ | ε at which D_max = 1.2×10⁷ |
|---|---:|---:|---:|---:|---:|---:|
| 8×52 | 1 | 1 | 100 ns | 4.0×10⁴ | ≥ $0.01 (fits) | $5×10⁻⁶ |
| 8×52 | 1 | 10 | 1 µs | 404 | $1.4×10⁻⁴ | $1×10⁻⁸ |
| 8×52 | 16 | 10 | 1 µs | 25 | $3.5×10⁻⁶ | $3×10⁻¹⁰ |
| 8×52 | 100 | 10 | 1 µs | **4** | **$3×10⁻⁷** | $2.5×10⁻¹¹ |
| 4×12 | 100 | 10 | 1 µs | 0.4 | $3×10⁻¹⁰ | — |

Full grid: [`frontier.json`](../../../results/advantage_frontier_20260923/frontier.json).
The smooth call and digital payoffs are strictly worse. For example, the 8×52 call at
$0.01 with g=1, k=1 and 1 µs allows 409 T-layers
([`classical_exponent_pilot.json`](../../../results/advantage_frontier_20260923/classical_exponent_pilot.json)).

These are sensitivity coordinates, not device predictions and not lower bounds on all
algorithms.

### Hardware grounding

The screen found no verified technical result that completes the causal chain from
changed resource assumption to a ≥10³ cut in ρ.

- **Superconducting:** memory cycle 1.1 µs and decoder latency ~63 µs are demonstrated
  (Willow). The latency is for a d=5 real-time decoder and excludes feedback into a
  logical circuit, and the Λ=2.14 figure uses an offline decoder; it was a memory
  experiment with no logical gates. A reaction time of 1–10 µs is projected; Gidney
  2025 assumes 10 µs, a 25 µs CCZ/lattice-surgery period, and ~2 ms per 33-bit addition
  including uncompute.
- **Chakrabarti's pricing estimate on a standard machine:** under Fast for the Curious's
  standard assumptions (1 µs rounds, one T per d rounds, p = 10⁻³), the options-pricing
  row of its Table I is 10⁴ logical qubits, 10¹⁰ T, 2.9×10⁷ physical qubits and **3.7
  days for one circuit repetition**. The classical target was ~1 s.
- **Magic-state cultivation** lowers T-state spacetime cost, not serial latency.
- **Trapped ions:** Helios demonstrates ~55 ms per all-to-all layer.
- **Neutral atoms:** transversal logic removes a factor of d, but layers stay
  millisecond-scale.
- **IBM bivariate-bicycle codes** trade qubits for longer per-T time. The Starling and
  Blue Jay gate budgets (10⁸–10⁹) are below one complete penny-accuracy pricing run.
- **Microsoft:** the Majorana/tetron path is the only one with a projected ~100 ns
  physical clock, and it is not demonstrated (June 2026 critique).

Details and links are in the screening table and in §8 (reading list).

## 4. Source screening

The [full screening table](SCREENING_TABLE.md) has 152 rows: 114 sources from 14 search
lanes, plus 38 venue, vendor and industry rows from the gap-filling pass. Each row gives
the source, date and status, reading depth, mechanism and claim, strongest classical
comparator and hidden costs, evidence level, escape criterion and decision.

A source was allowed to change the decision only if it supplied at least one of:
- **(a)** a precision-exponent gap of at least 2 against the best classical method;
- **(b)** a credible ≥10³ reduction in ρ;
- **(c)** a ≥10³ increase in intrinsic classical per-sample cost without a matching
  coherent cost;
- **(d)** a mechanism outside query counting.

Decision-relevant rows:

| Source | Status / depth | Mechanism → verdict |
|---|---|---|
| [Chakrabarti et al. 2012.03819](https://arxiv.org/abs/2012.03819) | Quantum 2021; focused | Autocallable/TARF compiled threshold: Q-operator ~8k logical qubits, T-depth 9.5k; ~10 MHz to match 1 s vs plain-MC anecdote at 68% → anchor, no advantage |
| [Stamatopoulos–Zeng](https://arxiv.org/abs/2307.14310) | Quantum 2024; focused | QSP payoff, ~16× T-count cut → L4 |
| [2507.19039 autocallable loading](https://arxiv.org/abs/2507.19039) | QCE25; focused | ~50× shallower payoff-loading module; dominant modules unchanged → L4 |
| [Babbush et al. 2011.04149](https://arxiv.org/abs/2011.04149) | PRX Quantum 2021; full | Quadratic speedups need ≥ cubic–quartic separations or ~10³ faster logic → framework, confirmed here |
| [Grand Challenge 2511.09124](https://arxiv.org/abs/2511.09124) | 2025 preprint; focused | Derivative pricing in the quadratic-only bucket → background |
| [Fast for the Curious 2510.26078](https://arxiv.org/abs/2510.26078) | 2025 preprint; focused | 33-bit add ~1.6 ms ripple / ~20 µs reaction-limited carry-lookahead vs <1 ns CPU; Table I prices Chakrabarti's options circuit at 3.7 days per repetition → (b) not met |
| [Parallel AE 2508.06121](https://arxiv.org/abs/2508.06121) | preprint v3 Jun 2026; focused | Linear-in-P parallel AE, but P oracle copies → no net change under qubit cap |
| [Recchia et al. QqMC 2609.03625](https://arxiv.org/abs/2609.03625) | preprint Sep 2026; full | "Window" compares an upper bound with the Koksma–Hlawka bound of *unscrambled* Sobol; vs scrambled RQMC the gap is 0 to −⅓ → reject |
| [Sun et al. 2602.08120](https://arxiv.org/abs/2602.08120) | ICML 2026 poster; v1 focused-full | Repeated nesting ε⁻¹·log^(3D+1) vs classical ε⁻² → gap 1, shrinking in D → reject as advantage |
| [Belomestny et al. multilevel dual](https://doi.org/10.1007/s00780-013-0208-1) | Finance Stoch. 2013; focused | Certified dual upper bound ε⁻²ln² classically → kills "quantum vs nested dual" |
| [Doriguello et al. optimal stopping](https://arxiv.org/abs/2111.15332) | published; focused | Gap ~1 vs LSM, shared curse of dimension → background |
| [Giles–Waterhouse MLQMC](https://people.maths.ox.ac.uk/gilesm/files/jcf07.pdf) | 2009; focused | Digital under discretized SDE stays ~ε⁻² → **only classical-degradation evidence; basis of H2** |
| [Bayer–Ben Hammouda–Tempone numerical smoothing 2111.01874](https://arxiv.org/abs/2111.01874) | published; focused | Smoothing restores RQMC slopes (GBM digital −0.64→−0.92; Heston −0.52→−0.85) → classical challenger for H1/H2 |
| [He–Wang conditional QMC 1708.09512](https://arxiv.org/abs/1708.09512) | SINUM 2019; focused | O(n^(−1+ε)) after valid conditioning; plain RQMC on discontinuous high-d integrands only ~MC-rate → consistent with P1 |
| [Rough Bergomi ASGQ/QMC 1812.08533](https://arxiv.org/abs/1812.08533) | Quant. Fin. 2020; focused | Classical slopes ε⁻¹·³–ε⁻¹·⁶ → rough vol is not a lever |
| [Guseynov et al. PDE 2605.26610](https://arxiv.org/abs/2605.26610) | 2026 preprint; focused | Beats full-grid FD only; single-point readout exponential in d → reject |
| [Forward Kolmogorov 2511.04942](https://arxiv.org/abs/2511.04942) | 2025 preprint; focused | Readout sampling-limited → reject |
| [KL-expansion pricing 2402.10132](https://arxiv.org/abs/2402.10132) (JPMorganChase) | 2024 preprint; focused | Gain only when monitoring dates ≫ ε⁻² → reject |
| [Infinite-variance QMC 2401.07497](https://arxiv.org/abs/2401.07497) | preprint; focused | Formal gap ≥2 for heavy tails, removed by share-measure change for call-type prices → reject |
| [Montanaro 1504.06987 §3.2](https://arxiv.org/abs/1504.06987) | published; focused | Only τ-growing quantum mechanism (walk annealing); no financially required slow-mixing target → background (H3) |
| [Rebentrost et al. incomplete markets 2209.08867](https://arxiv.org/abs/2209.08867) | preprint; focused | ε-exponent worse (3 vs 2); √K gain only → reject |
| [Stamatopoulos et al. gradients 2111.12509](https://arxiv.org/abs/2111.12509) | Quantum 2022; focused | Many-Greeks gain vs finite differences; AAD kills it → reject |
| [2501.15614](https://arxiv.org/abs/2501.15614) | withdrawn in v3 by authors | "Exponential" Asian claim does not hold → caution |
| [2604.24289](https://arxiv.org/abs/2604.24289) | corrected in v2 | Separation withdrawn once randomized classical rates were used → caution |
| [STAC-A2 (H100)](https://docs.stacresearch.com/system/files/resource/files/STAC-Summit-30-May-2024-STAC-A2.pdf) | audited benchmark; focused | ≤ ~1 ns per Heston asset-step per GPU including Greeks → raises ρ |
| [Willow 2408.13687](https://arxiv.org/abs/2408.13687), [Gidney 2505.15917](https://arxiv.org/abs/2505.15917), [cultivation 2409.17595](https://arxiv.org/abs/2409.17595), [Helios 2511.05465](https://arxiv.org/abs/2511.05465), [neutral atoms 2506.20661](https://arxiv.org/abs/2506.20661), [bicycle codes 2506.03094](https://arxiv.org/abs/2506.03094) | demonstrated / projected | Set t_layer at 1–100 µs (SC), ms (ions/atoms) → no ≥10³ ρ cut |

Channels searched include:
- **IEEE QCE25:** technical papers, posters and the finance workshop, which had no
  pricing talk.
- **IEEE QCE26:** full keyword screen of the technical-paper schedule and the
  workshop/tutorial schedule. There are zero option-pricing or amplitude-estimation
  pricing papers and no finance workshop; finance appears only as optimization and
  time-series work, plus one application area in the QC4PDE workshop.
- **Theory and ML venues:** official accepted-paper lists or targeted searches for QIP
  2025/2026, TQC 2025/2026, STOC 2025/2026, FOCS 2025, SODA 2025/2026, NeurIPS 2025 and
  ICML 2026. None contains a quantum Monte Carlo, amplitude-estimation, integration or
  pricing paper. The nearest super-quadratic item is a quartic speedup for *planted
  inference* (SODA 2025), which is not a pricing task. Access limits: the official SODA
  2025/2026 lists blocked automated access (403 and anti-bot), so SODA was screened by
  search. QIP 2025 was screened from a partial sample. NeurIPS 2025 and ICML 2026 were
  covered by targeted keyword search, not a full list screen.
- **MCQMC 2024:** classical advances only (QMC Fourier multi-asset pricing, multilevel
  RQMC for nested integration, conditional smoothing for barrier Greeks). The MCQMC 2026
  talk list was not accessible.
- **Preprints:** arXiv quant-ph, q-fin.CP and q-fin.PR listings to September 2026.
- **Journals:** Quantum, PRX Quantum, Nature, SIAM J. Numer. Anal., Finance Stoch.,
  Quantitative Finance.
- **Financial institutions:**
  - *JPMorganChase:* KL-expansion pricing; [Herman et al. 2026](https://arxiv.org/abs/2602.03725),
    which gives a quadratic speedup for CIR/Heston against *plain* MC only.
  - *Goldman Sachs:* the threshold and QSP papers. An April 2026 Bloomberg report says the
    team was wound down after internal resource estimates; this is press-secondary,
    not evidence.
  - *HSBC/IBM:* the 2025 bond-trading "34%" result
    ([2509.17715](https://arxiv.org/abs/2509.17715)) is ML fill-probability
    classification. The authors attribute the gain to hardware noise, and it is
    independently critiqued. It is not pricing.
  - *Fidelity:* public observation pages only.
  - *DBS/Classiq:* simulator exposure studies.
- **Hardware vendors:** IBM, Google, Quantinuum, Microsoft, IonQ/Oxford Ionics, AWS
  Ocelot, PsiQuantum, QuEra/Harvard, and the STAC benchmarks. None publishes a logical
  clock or T-state rate that completes the causal chain.

### Adversarial verification of load-bearing claims

A separate agent tried to refute the eight claims this report depends on most, working
from the primary texts.

| Claim | Verdict | Correction or caveat |
|---|---|---|
| Parallel AE 2508.06121: O(1/ε) queries, depth O(1/(Pε)+log P); corrected Ω(1/(εP)) lower bound | Confirmed | RMSE metric, not a 99% interval |
| Fast for the Curious: 1.6 ms ripple add, ~20 µs reaction-limited carry-lookahead, kHz–MHz clocks | Partly correct | The pricing row gives 3.7 days per repetition; it is not labelled "impractically slow" |
| Willow: Λ≈2.14, 0.143%/cycle at d=7, 1.1 µs cycle, 63 µs decoding latency | Confirmed | Offline decoder for Λ; latency at d=5 excludes feedback; memory only |
| Gidney 2025: 10 µs reaction, 25 µs period, ms-scale additions, <1 week, <1M qubits | Confirmed | 33-bit add ≤1.6 ms rounded to 2 ms |
| Chakrabarti: Q-operator 8k qubits, T-depth 9.5k; total 5.4e7 / 1.2e10; ~10 MHz for 1 s | Confirmed | Confidence 68%, not 99% |
| Sun et al.: ε⁻¹·log^(3(D−d)+1) vs classical ε⁻² | Confirmed | D and Lipschitz-dependent constants hidden |
| Giles–Waterhouse: MLQMC ~ε⁻¹ European; digital ~ε⁻² | Partly correct | Only the European ε⁻¹ is stated; Asian/lookback rates are inferred from figures; digital ≈ε⁻² confirmed |
| Recchia et al.: window compares upper bounds against unscrambled Sobol | Confirmed | No scrambling or RQMC appears anywhere in the paper |

Search logs from the interrupted lanes were partially lost when the account usage limit
was reached. The saved rows were written before interruption and are retained. Coverage
is selective, and abstract-only rows are labelled as such.

## 5. Ranked shortlist and deep analysis

Ranking weighs plausible advantage, strength of evidence, financial relevance, novelty,
resources and time to decisive evidence.

### H1 (primary): multi-date discontinuous basket payoffs where classical smoothing fails

> For discretely monitored equal-weight knock-out basket calls (4–16 GBM assets, 12–52
> monitoring dates), a price to $0.01 absolute at 99% per-price confidence, a
> variance-sensitive quantum estimator on a compiled coherent path oracle reduces
> complete latency ≥10× below the fastest validated classical method. The classical
> finalists are preintegrated/smoothed RQMC, one-step survival and multilevel QMC on a
> multicore CPU and a GPU. This holds provided logical T-layers of t ≤ 1 µs, an explicit
> estimator constant k ≤ 10, and a per-call T-depth below D_max(ε).

- **Mechanism.** Unlike smooth Asian payoffs, the max-over-dates knock-out leaves kinks
  after preintegration. The strongest measured classical exponent is p_C ≈ 1.6–1.75. The
  weaker one-step-survival variant without dimension reduction is at 2.1, which is not
  the comparator. The quantum precision exponent stays at 1, and the quantum budget
  grows like ε^(−(p_C−1)).
- **What would falsify it.**
  - Any eligible classical method (multi-direction numerical smoothing, bridge-ordered
    one-step survival, barrier importance sampling) restores r ≥ 0.9.
  - Or, with the measured fastest classical (GPU) time, the minimal compiled oracle depth
    exceeds 10×D_max for every ε ≥ $0.001 at t ≤ 1 µs and k ≥ 3.
  - The frontier table already shows the second condition failing by ~2,500× against a
    10⁴-depth oracle at $0.01. H1 therefore survives only if a much shallower oracle
    exists or the classical GPU speed-up is far smaller than assumed.
- **Already known.** Discontinuities degrade QMC (He–Wang). Smoothing repairs single
  discontinuities (Bayer et al.; Liu CAS). Autocallables were the Goldman threshold case.
- **What this work would add.** A measured, certified frontier for the hardest standard
  payoff class against the strongest classical smoothing. That is a new, falsifiable
  statement, not a new primitive.
- **Occupancy.** No located source measures the post-smoothing RQMC rate for
  multi-date basket knock-outs against a compiled quantum oracle. This is not priority
  clearance.

### H2 (fallback): discontinuity combined with discretized stochastic volatility

For digital or barrier payoffs under Heston-type models that require time-stepping,
Giles–Waterhouse report that multilevel QMC stays near ε⁻² for the digital. Bayer et al.
report that smoothed RQMC slopes reach only about −0.85 under Heston. Quantum MLMC reaches
ε⁻¹ only with strong order greater than 2, which requires Lévy-area-type terms, an extra
coherent cost ([An et al. Cor. 3](https://arxiv.org/abs/2012.06283)).

- **Gap.** At most ~0.5–1, and it does not grow with any problem parameter.
- **Falsifier.** Exact or quadratic-exponential Heston sampling plus conditioning restores
  r ≈ 0.9; or H1's frontier arithmetic applies with a larger oracle.
- **Burden.** Higher than H1. It reuses the antithetic study's Heston coupling and its
  failed resource numbers, so it is ranked below H1.

### H3 (background; larger scope change): gaps that grow with a problem parameter

Quantum-walk annealing ([Montanaro §3.2](https://arxiv.org/abs/1504.06987)) is the only
rigorous mechanism found whose gap grows with the mixing time τ: roughly
√τ·(σ/ε) versus τ·(σ/ε)². It applies only if a pricing task *requires* a slowly mixing
Markov chain; Bayesian parameter-uncertainty pricing is the obvious candidate. None was
found. Posteriors of financial models are low-dimensional and near-Gaussian, and
classical sequential Monte Carlo parallelizes the same annealing schedule. Retain this
only as a watch item.

### Rejected with reasons

| Mechanism | Reason |
|---|---|
| Nested / compound / Bermudan | Classical multilevel dual reaches ε⁻²ln² and reuse removes nesting; the quantum polylog grows with D; the project's compound study failed |
| QqMC pre-asymptotic window | Upper-bound artefact against unscrambled nets |
| Quantum PDE | Readout and normalization; only beats full-grid finite differences |
| Multi-output / Greeks / portfolios | AAD and shared paths; a vector of prices costs √K more on the quantum side |
| Heavy tails | Measure change gives bounded classical estimators |
| Robust / LP / MOT bounds | Quantum ε-exponent is worse |
| Rough volatility | Classical ~ε⁻¹·³–ε⁻¹·⁶ via ASGQ/QMC/Markovian lifts |
| Analog encoding / KL expansion | Dequantized, or gain only at unrealistic date counts |
| Newer hardware | No verified ≥10³ latency cut |

## 6. Recommended direction and staged experiment

### Paper direction (independent of H1's outcome)

Keep the 22 September manuscript as the validated comparator study, and do not add an
advantage claim to it. Start a separate prospective paper, provisionally titled:

**"Where quadratic quantum speedups meet strong classical option pricing: a measured
advantage frontier."**

Proposed claim, if the data hold: for standard multi-asset path-dependent contracts, a
10× quantum pricing win against measured strong classical methods requires the stated
combinations of per-call oracle depth, logical T-layer time and accuracy. The paper maps
where the project's certified compiled oracles and published estimates fall relative to
that frontier.

Contributions:
- the ρ_max/D_max law in financial units;
- measured post-smoothing classical exponents, including the knock-out failure mode;
- five executed, certified negative feasibility studies as data;
- hardware-grounded sensitivity.

This is a level-2 *conditional frontier*. It is not an advantage result and must not be
presented as one. Nearest prior art: Babbush 2021, Chakrabarti 2021, Hoefler 2023,
Grand Challenge 2025 and Fast for the Curious 2025. The difference is strong classical
baselines, measured exponents and certified compiled oracles. Novelty has not yet been
cleared.

### Research direction: falsify or promote H1

**Research question.** Is there any ε ≥ $0.001 and any credible (t_layer, k) at which the
minimal compiled knock-out oracle fits under D_max(ε), measured against the fastest
eligible classical implementation?

**What to retain.** The reversible compiler with range proofs and wave schedules, the
explicit estimator schedules, the error-ledger structure, the classical RQMC/control
code, and the P1/P2 pilots.

**What to change.** Switch the payoff to a knock-out basket, move the classical baseline
to a GPU plus multi-direction smoothing, and state the claim as a frontier.

**Strongest classical baseline, implemented first.** Compiled (Numba or C/OpenMP)
multicore and CuPy/CUDA versions (an RTX 4060 is available) of:
1. first-PC preintegration;
2. multi-direction numerical smoothing (Bayer–Ben Hammouda–Tempone);
3. Brownian-bridge-ordered one-step survival;
4. importance sampling toward the barrier.

Also run plain MC on the GPU as a throughput anchor. Pay all setup, and use equal control
information on both sides.

**Cheapest ruling-out experiment (≤ 1 week, ≤ 16 CPU-hours, ≤ 4 GPU-hours, no paid
hardware).**
- *Days 1–2:* run the classical finalists on development cases 4×12, 8×52 and 16×52
  with barriers H ∈ {120, 140, 160}. Use 32 scrambles, n = 2⁶…2¹⁶, whole-scramble
  resampling for rate intervals, and record T_C(ε) at $0.10/$0.03/$0.01/$0.001.
- *Days 3–4:* emit the minimal coherent knock-out oracle with the existing compiler. It
  computes GBM log-paths from finite Gaussian inputs, per-date basket exponentials, the
  running max comparator, the arithmetic average, the payoff and the inverse. Record
  T-count, T-depth and logical qubits at f = 24/32 under serial, wave and
  reaction-limited carry-lookahead models; take k from the explicit Hadamard/QAE
  schedules already certified.
- *Day 5:* evaluate D_min(oracle) against D_max(ε) over t ∈ {0.1, 1, 10} µs,
  k ∈ {3, 10}, and measured CPU and GPU times. Write the frontier figure and decide.

**Stop, continue or revise.**
- **Stop H1** if any classical finalist reaches r ≥ 0.9 on all development cases. Also
  stop if D_min > 10·D_max($0.001) for t ≥ 100 ns, k ≥ 3 and the measured best classical
  method on every case. In both cases publish the frontier paper as a negative or
  requirements study.
- **Continue** only if some region with ε ≥ $0.001, t ≥ 100 ns, k ≥ 3 and a GPU classical
  comparator has D_min ≤ D_max. Then proceed to weeks 2–6.
- **Revise** only if a named component (for example the exponential or comparator
  circuit) has a demonstrated ≥10× reduction that brings some region within 10×. Any
  outcome-driven change requires new development cases.

**Weeks 2–6 (only after a continue).**

| Week | Work | Deliverable |
|---|---|---|
| 2–3 | Certified error ledger for the knock-out oracle: finite-law, arithmetic, and barrier-indicator sensitivity to fixed-point error (discontinuity makes this binding); explicit confidence schedule | Source-bound ideal-logical ledger |
| 4 | Independent reference prices with a two-construction reference within ε/10, using one-step survival and preintegration; freeze code, tolerances and hardware menus | Frozen methods |
| 5–6 | Open 24 held-out cases; compute frontier membership for each | Conditional level-2 table, or a negative result |

**Held-out confirmation design (not yet generated).**
- Six strata: (assets, dates) ∈ {(4,12), (4,52), (8,12), (8,52), (16,12), (16,52)},
  with four cases j = 0…3 each.
- K/S0 ∈ {.9, 1, 1.1} chosen as (s+j) mod 3.
- Draw independently: H/S0 ~ U[1.15, 1.6], σ ~ U[.15, .45], equicorrelation ~ U[.1, .7],
  T ∈ {1, 2} = 1 + (j mod 2); r = .03.
- Use PCG64 with SeedSequence words [2026092301, s, j], in the stated draw order. Use 64
  scrambles per method and two reference constructions.
- **Pass:** ≥ 20/24 cases at ≥ 10× and every case at ≥ 3× within the declared
  (t_layer, k) region, with all accuracy contracts met.
- **Reporting:** paired timing and error uncertainty. The 99% guarantee is per price;
  reference failure is allocated separately (0.001 total).
- Development cases (P1/P2 and the week-1 cases) never enter confirmation.

## 7. Claim ledger

| Claim | Status |
|---|---|
| Quadratic AE/QMLMC query speedups over MC under oracle access | Established literature, level 3 (vs MC; not a structured-finance lower bound) |
| All five project feasibility studies fit one law, 10× ⇔ ρ ≤ ρ_max, with measured ρ_max ≈ 0.1–24 classical point-evaluations (≈1–170 plain paths) at $0.01 | Established here from archived artifacts and P1 (development) |
| Smoothing restores near-n⁻¹ RQMC for basket calls and digitals (48- and 416-dim GBM) | Executed P1 diagnostic, empirical rates |
| Multi-date basket knock-outs keep r ≈ 0.57–0.63 after first-PC preintegration and 0.48–0.57 with one-step survival | Executed P1/P2 diagnostic; other smoothing untried |
| A ≥10× crossover exists for the knock-out at $0.01 under fair (GPU, k≥3, ≥1 µs) assumptions | Unsupported; the frontier indicates misses of ~10³ or more |
| A crossover exists under slow classical code, k=1 and 100 ns T-layers | Conditional sensitivity corner only; not a fair comparison |
| Hardware developments cut ρ by ≥10³ | Unsupported; no verified causal chain |
| Nested, PDE, multi-output, heavy-tail, LP and QqMC routes give significant advantage | Unsupported / rejected (§5) |
| The frontier paper is novel or publishable | Unestablished; requires prior-art check and review |
| Quantum pricing advantage is impossible | Not established; no universal lower bound; H1–H3 remain falsifiable |
| This investigation fulfils the advantage objective | **False** |

## 8. Prioritized reading list

1. [Babbush et al., "Focus beyond quadratic speedups"](https://arxiv.org/abs/2011.04149):
   §II break-even model and Table I/II. This is the obstruction in general form; compare
   its ~cubic/quartic requirement with §3 here.
2. [Chakrabarti et al., Quantum 2021](https://arxiv.org/abs/2012.03819): Table 1, §5.1
   resources, Appendix A.4 classical timing, confidence choice (§3). It is the only
   compiled finance threshold, and its classical comparator is weak.
3. [The Fast for the Curious](https://arxiv.org/abs/2510.26078): Table I, §III.B
   (reaction time), §V.A and Table III (adders). Sets realistic t_layer and the ~80×
   reaction-limited lever.
4. [Willow](https://arxiv.org/abs/2408.13687) (logical error scaling; real-time decoding
   latency) and [Gidney 2025](https://arxiv.org/abs/2505.15917) §3.2 (factory and
   lattice-surgery periods): demonstrated versus projected clock anchors.
5. [He–Wang, conditional QMC for discontinuous functions](https://arxiv.org/abs/1708.09512)
   §5–6, and [Bayer–Ben Hammouda–Tempone numerical smoothing](https://arxiv.org/abs/2111.01874)
   §4.1–4.5 (slopes, Table 4.2). These are the classical tools most likely to kill H1.
6. [Giles–Waterhouse MLQMC](https://people.maths.ox.ac.uk/gilesm/files/jcf07.pdf) §6.1–6.5,
   with [An et al.](https://arxiv.org/abs/2012.06283) Theorem 2 and Corollary 3: the
   H2 mechanism and its limit.
7. [Recchia et al. QqMC](https://arxiv.org/abs/2609.03625) §§4–6: read to see why a
   bound-vs-bound window is not an advantage.
8. [Sun et al.](https://arxiv.org/abs/2602.08120) Thm 1.6, Prop 3.4, and
   [Belomestny et al. multilevel dual](https://doi.org/10.1007/s00780-013-0208-1)
   Thm 3.3 and §4: the nested/early-exercise exponents on both sides.
9. [Parallel amplitude estimation 2508.06121](https://arxiv.org/abs/2508.06121)
   Theorems 1–2: the parallelism leg (linear in P, but P oracle copies).
10. [STAC-A2 H100 results](https://docs.stacresearch.com/system/files/resource/files/STAC-Summit-30-May-2024-STAC-A2.pdf):
    classical GPU throughput to plug into ρ.

## 9. Single next action

**Update, 23 September 2026: executed.** The H1 falsifier below was run, and its
pre-registered stop rule fired. The minimal compiled knock-out oracle is 1,138–5,765×
deeper than the 10× budget against the measured compiled classical pricer at $0.001,
100 ns and k = 3. See [H1_FALSIFIER_RESULTS.md](H1_FALSIFIER_RESULTS.md). The text below
is kept as originally written.

Run the **one-week H1 falsifier** in §6: a compiled CPU/GPU knock-out pricer with the
strongest smoothing, plus the minimal compiled coherent knock-out oracle, placed on one
D_min-versus-D_max(ε) chart.

It is the cheapest experiment that could change the decision. If any classical smoother
restores r ≈ 1, or the GPU-timed budget stays ≥10× below the compiled depth at
ε ≥ $0.001, the direct-pricing advantage search should stop and the project should
publish the measured frontier. If a region survives, it defines the only place where a
conditional level-2 pricing advantage could still exist.
