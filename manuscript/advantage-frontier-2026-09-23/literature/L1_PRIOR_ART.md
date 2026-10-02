# L1 prior-art screen and Day-2 checkpoint

**Date:** 1 October 2026. **Branch:** `research/advantage-frontier-paper`. **Affiliation:** VIT Vellore.

**Checkpoint decision: GO_NARROWED.** The candidate novelty survives only as a *measured
instantiation in derivative pricing* of an argument that is already published in general
and illustrative form. Section 5 names the narrowings.

**Verdict:** unchanged. No defensible significant quantum advantage has been established yet.

**What kind of document this is.** An AI agent ran a selective literature screen. It is not
exhaustive and it is not peer review. It can miss papers, especially recent ones, those
behind paywalls, and those in venues the search tools index poorly. The author and a named
human expert still need to check the decision before submission.

---

## 1. Method

**Inputs.**
- `l1_thresholds.jsonl`: 23 rows on break-even and threshold analyses in any domain.
- `l1_finance.jsonl`: 17 rows on finance and quasi-Monte Carlo (QMC).
- The screens these built on:
  - `docs/research_investigation/2026-09-23/SCREENING_TABLE.md` (152 rows);
  - `docs/novelty_assessment/2026-09-21/NEAREST_PRIOR_ART_MATRIX.md`.

Search agents wrote both JSONL files. The thresholds searcher was cut off by a usage limit
after saving its rows; the finance searcher finished, but this verification worked from the
saved rows of both. This
screen re-checks their work adversarially.

**What was re-verified.** I re-opened the primary source for every row with overlap level
partial or substantial: 16 threshold rows and 6 finance rows. No row was marked "preempts".
Two background rows were also checked:
- F10, because it was marked `verified_primary=false`;
- L1-T10, because it recorded a discrepancy with `WHY_NO_ADVANTAGE.md`.

For each row I checked existence, authors, version history and status, what the paper does,
and the overlap with C1–C7. The sources I used were:
- arXiv abstract pages;
- arXiv HTML or PDF full text, searched for the specific numbers the rows cite;
- Crossref, OpenAlex and Semantic Scholar metadata for publication status and abstracts;
- publisher pages, where they were reachable.

Results are in `l1_verification.jsonl` (34 lines):
- 24 verification records;
- 2 status addenda;
- 8 new rows marked `new_row: true`.

**Searches of my own** (1 October 2026), aimed at a pre-empting paper the searchers missed:
1. Web search: measured classical GPU or CPU versus compiled quantum amplitude estimation,
   break-even, logical clock and T-depth for option pricing.
2. Web search: "what would it take" for quantum advantage in option or derivative pricing.
3. Web search: quantum advantage in derivative pricing with a quasi-Monte Carlo comparator.
4. Web search: discrete barrier and knock-out options, RQMC convergence rate, smoothing and
   conditioning, 2023–2026.
5. Web search: strong classical baseline, GPU runtime and logical-clock crossover for
   quantum Monte Carlo pricing.
6. Web search: quasi-Monte Carlo eroding the quadratic speedup, and end-to-end surveys.
7. Web search: barrier and knock-out amplitude-estimation resource estimates on baskets.
8. Web search: time-to-accuracy of RQMC or GPU versus fault-tolerant runtime.
9. Web search: Japanese-group work on quantum Monte Carlo integration versus classical
   (Kaneko, Miyamoto).
10. Citation screen of Chakrabarti et al. 2021 and Stamatopoulos–Zeng 2024: all 70 works
    indexed by OpenAlex from June 2023 onward.
11. Citation screen of Babbush et al. 2021: 102 works indexed by OpenAlex from June 2023
    onward.
12. Three arXiv API queries:
    - abstracts with quantum, "option pricing" and advantage;
    - "amplitude estimation" with "quasi-Monte Carlo";
    - barrier with "quasi-Monte Carlo" and smoothing, preintegration or conditioning.

**Limits.**
- **Unread full texts.** Two load-bearing full texts could not be read:
  - Laura et al. 2026 returned HTTP 403 from both MDPI and preprints.org.
  - Xie, He and Wang 2019 is closed access.

  For these I relied on abstracts from OpenAlex and Semantic Scholar, plus one
  search-engine snippet.
- **Incomplete citation index.** OpenAlex citation coverage of arXiv-only preprints is
  incomplete. Chakrabarti et al. show 101 citations in total, but only journal-indexed
  citers appear.
- **Sources not searched:** Google Scholar, SSRN, the full proceedings of the Winter
  Simulation Conference and MCQMC 2026, patents, and non-English literature.
- **Search-engine summaries.** These were used only to find candidates. Nothing in this
  document rests on a summary unless it says so.

---

## 2. What the verification found

No row is fabricated. Every checked source exists, and its authors and main content match
the row. These corrections matter for the paper:

1. **Case (arXiv 2502.17731 v2, 16 Sep 2026) is closer to our work than the row said.**
   - Table 8 is confirmed. On a single-asset Asian with an up-and-out barrier, first-PC
     preintegration moves the exponent only from about −0.54 to about −0.55/−0.56 at
     m = 64, 121 and 256. The digital moves to about −1.06/−1.07.
   - Sec. 12 does report equal-cost comparisons. It does not report a time-to-accuracy
     at a dollar target.
   - Secs. 11.1–11.2 describe the non-unique PCA basis inside a degenerate eigenspace at
     zero correlation, and show that the basis choice can change the measured exponent.
     This is the phenomenon behind our ERRATA E10 (the Stage B 8×52 Q0 mismatch). E10
     and the paper should cite it.
2. **Xie, He and Wang (EJOR 2019) is still unresolved, but its abstract is now read.**
   - It claims an improved convergence rate for discrete barriers. The method is
     sequential importance sampling plus a tailored path generation.
   - It also warns that removing the discontinuities may not restore QMC's advantage in
     high dimension.
   - The exponents and the asset count are unknown.
3. **Laura et al. (Information 17(9):908, 17 Sep 2026): abstract confirmed, full text
   unread.**
   - The abstract confirms an illustrative sensitivity analysis of the AE crossover
     against classical throughput, oracle depth and comparison window. It labels its
     numbers as scenarios, not calibrated hardware forecasts.
   - A search-engine snippet suggests the model is plain MC at 1 ns per sample, against
     √N amplitude-estimation steps at an oracle depth of 5×10⁵. That would put the
     crossover near N ≈ 2×10¹⁵ at 10 MHz.
   - If the snippet is accurate, this is a Babbush-style crossover with scenario inputs.
     It does not use a measured RQMC comparator.
4. **Chakrabarti et al. 2021: all F11 details confirmed from the v3 PDF.**
   - Contract: a 3-asset autocallable with a knock-in put over 20 barrier dates.
   - Costs: the Q operator has T-depth 9.5k with 8k qubits; the payoff circuit has
     T-depth 3.2k.
   - Assumptions: 68% confidence, and 10 MHz needed at a 1 s target.
   - The classical cost is an anecdote: "five to ten seconds" with at least 40k paths.
   - Nuance: the paper notes that such contracts are priced with MC *or quasi-MC*, but its
     comparison uses only the MC rate.
5. **The Grand Challenge discrepancy is resolved.**
   - The v3 text never says "finance" or "option".
   - However, the Table 3 caption cites Chakrabarti et al. among detailed resource
     estimates that it leaves out because they involve only a quadratic speedup.
   - The paper is now published as PRX Quantum 7, 020101 (2026).
   - Rewording for `WHY_NO_ADVANTAGE.md`: "cites the derivative-pricing threshold estimate
     among quadratic-only resource estimates (Table 3 caption)".
6. **One downgrade.** L1-T05 (Quantum Deep Learning) goes from partial to background. It
   contains no Monte Carlo or pricing analysis.
7. **Metadata fixes:**
   - Choi–Moses–Thompson: Proc. IEEE 113(2):113–124 (2025).
   - QEA calculator: IEEE QCE 2025, pp. 1873–1883.
   - Costa et al.: Phys. Rev. A 112, 022429 (2025).
   - He–Wang: Comput. Econ. 57(2):693–718.
   - Jaques et al.: EUROCRYPT 2020, LNCS pp. 280–310.
   - Do not quote the "~2^34" figure in the Jaques row; it was not verified.
   - F10: the rate n^(−1/2−1/(4d−2)) is attributed in He's own restatement to He, Math.
     Comp. 2018, not jointly to He–Wang 2015.

**New finds that change the picture:**
- **Dalzell et al. (survey; Cambridge University Press book, 2025).** It already states in
  prose that QMC and MLMC "cut into" the quadratic speedup, and gives about 50 MHz as the
  clock needed to compete with classical MC. It was in the 23-September screen but missing
  from the L1 rows.
- **Incudini and Mazzola (arXiv 2607.22818, July 2026).** It does a full fault-tolerant
  compilation and compares against classical step times measured on CPU and an H100 GPU,
  with a runtime crossover. The setting is Monte Carlo, but it is MCMC sampling with a
  super-quadratic speedup.

Six background rows were also added. None pre-empts the paper.

---

## 3. Nearest-prior-art matrix

The "Verified" column means the primary source was opened in this session (1 Oct 2026):
- *yes*: full text or the relevant section was read;
- *abstract*: only the abstract or metadata was read.

| Source (link) | What it does | Overlapping claims | Overlap | Precise difference from our paper | Verified |
|---|---|---|---|---|---|
| [Chakrabarti et al., Quantum 5, 463 (2021)](https://arxiv.org/abs/2012.03819) | Full logical resource estimate for AE pricing of a 3-asset autocallable with a 20-date knock-in put and a TARF. 8k qubits, total T-depth 5.4×10⁷ at 68% confidence. A 1 s target implies a 10 MHz T rate | Framing, C3, C4, C6 | Substantial | Its classical side is an assumed 1 s at 68% against the plain-MC rate. Ours is timed RQMC with fitted exponents at 99%. It gives one operating point, not a frontier. Its oracle is hand-counted; ours is emitted and basis-replayed. Its per-Q depth (9.5k) is about 600× below our generic emitted 6.0×10⁶, so it is the optimistic reference for C3/C4 | yes |
| [Stamatopoulos & Zeng, Quantum 8, 1322 (2024)](https://arxiv.org/abs/2307.14310) | QSP payoff encoding: about 16× fewer T gates and about 4× fewer qubits. Advantage needs 4.7k qubits and 10⁹ T at 45 MHz | C3, C4, C6 | Partial | A single required-clock number on the inherited classical target. No measured comparator and no barrier basket. It defines the quantum-favourable oracle family that the frontier must show | abstract and metadata (body not re-read) |
| [Laura et al., Information 17(9):908 (2026)](https://doi.org/10.3390/info17090908) | Survey of quantum trading algorithms. Illustrative sensitivity of the AE crossover to classical throughput, oracle depth and comparison window, for derivative pricing | Framing, C1, C6 | Substantial | Per the abstract and a snippet, its inputs are scenarios: plain MC at 1 ns per sample, oracle depth 5×10⁵, no RQMC. It does not appear to have its own compiled oracle, k, a 99% contract, a width axis, a knock-out or a calculator. **Full text unread; this is the main residual risk** | abstract |
| [Babbush et al., PRX Quantum 2, 010103 (2021)](https://arxiv.org/abs/2011.04149) | Break-even model T_Q = M·t_Q against T_C = M^d·t_C, with Amdahl parallelism and a faster-Toffoli factor. Quadratic speedups fail on early fault-tolerant hardware | Framing, C1, C6 | Substantial | It is the source of C1. Its t_C is one classical primitive. It has no variance or accuracy contract, no k, no Monte Carlo instance and no width axis. It names Monte Carlo pricing only as an example of oracle logic | yes |
| [Hoefler, Häner & Troyer, CACM 66(5) (2023)](https://arxiv.org/abs/2307.00523) | Inverts the crossover into the maximum operations per call for a 10⁶ s crossover. For a quadratic speedup: 0.2 fp16, 0.003 int32 or 68 binary operations. Lists Monte Carlo via quantum walks among likely dead ends | Framing, C1, C6 | Substantial | Generic form of the D_max inversion. It uses peak chip throughput, not a measured solver, and abstract operation counts, not a compiled oracle. It has no accuracy model and no k | yes |
| [Dalzell et al., survey (arXiv 2310.03011; CUP 2025)](https://arxiv.org/abs/2310.03011) | End-to-end survey. Its option-pricing section says QMC and MLMC cut into the quadratic speedup, asserts a curse of dimensionality for QMC, and gives about 50 MHz to compete with classical MC | Framing, C2, C6 | Partial (new row) | The QMC erosion is stated qualitatively, not measured. Our preintegrated call and digital rates on 48- and 416-dimensional baskets (near n⁻¹ at 48 dimensions; basis-dependent at 416, see C2 in §4) bear directly on its dimensionality caveat. No oracle, no frontier | yes (relevant section) |
| [Campbell, Khurana & Montanaro, Quantum 3, 167 (2019)](https://arxiv.org/abs/1810.05582) | Measured strong SAT and colouring solvers against depth-optimised Grover and backtracking oracles. Three hardware regimes, a one-day cap, and oracle depth 10³ versus 5×10⁵. Speedup scales about as c⁻² with depth | Framing, C1, C3, C4, C6, benchmark | Substantial | The measured-requirements template, for combinatorial search. No variance, accuracy or confidence model, no k, no RQMC rate effect, discrete regimes rather than a continuous frontier, and no calculator | yes |
| [Brehm & Weggemans, Quantum 10, 1975 (2026)](https://arxiv.org/abs/2412.13274) | Hybrid benchmarking of quantum backtracking and Grover against the measured 2023 SAT winner, with T-depth and T-count cost models and a one-day requirement. Speedups mostly vanish | Framing, C3, C4, C6, benchmark | Substantial | Current state of the art of the same method in search. A precedent that a domain transfer with a measured comparator is publishable in Quantum. No mean estimation and no pricing | abstract and metadata |
| [Incudini & Mazzola, arXiv 2607.22818 (2026)](https://arxiv.org/abs/2607.22818) | Fully-quantum Metropolis walks. Full fault-tolerant compilation; CPU and H100 GPU step times measured, FPGA estimated. The crossover drops from about 10³ years (quadratic walks) to under a day | Framing, C1, C6 | Partial (new row) | Closest measured-GPU-versus-compiled-quantum Monte Carlo study, but for MCMC sampling with a super-quadratic speedup. It times per step, not to accuracy, under no accuracy contract, with no RQMC and no payoff | yes (HTML sections) |
| [McArdle et al., "Fast for the Curious" (2025)](https://arxiv.org/abs/2510.26078) | Levers for logical clock speed. Advocates working backward from workflow time to the required clock. Table I: options pricing at 10⁴ logical qubits, 10¹⁰ T, 2.9×10⁷ physical qubits and 3.7 days per repetition at 1 µs | C6, C7 | Partial | Conceptual precursor of C7's required clock. No measured comparator, no crossing depth and no frontier | yes |
| [Mejia et al., QEA calculator, IEEE QCE 2025](https://arxiv.org/abs/2508.21031); [Choi, Moses & Thompson, Proc. IEEE 2025](https://arxiv.org/abs/2310.15505) | A public web calculator for quantum economic advantage, built from asymptotic runtime expressions, roadmaps, gate times and overheads. Presets: factoring, search and TSP | Calculator, C6 | Partial | Pre-empts "first break-even calculator". It has no AE accuracy or variance model, no k, no measured T_C(ε) and no pricing preset | yes |
| [Case, arXiv 2502.17731 v2 (2026)](https://arxiv.org/abs/2502.17731) | Bootstrap intervals for RQMC exponents. Single-asset barrier: preintegration changes the exponent by less than 0.04 while cutting error 6–9×, while the digital gains about 0.5. Explains the residual kinks. Also covers the degenerate PCA basis | C2, benchmark, E10 | Substantial | Single asset, one smoother, no one-step survival, no basket barrier, no time-to-accuracy contract, no quantum budget | yes |
| [Achtsis, Cools & Nuyens, SIAM J. Financial Math. 4 (2013)](https://arxiv.org/abs/1111.4808) | Conditional sampling with the LT construction under RQMC. On a 4-asset, 130-date Asian with a barrier on S₁, std-dev exponents are 0.55–0.73. The authors say conditioning gives variance reduction, not necessarily a better rate | C2 | Substantial | Their barrier is on one asset inside the basket; ours is on the basket average. They use the LT construction; we use PCA and the bridge, with preintegration as a second smoother. No bootstrap and no timing. Our 0.48–0.63 overlaps their range; its lower end (0.48, one-step survival at 8×52) lies below it | yes |
| [He & Wang, Comput. Econ. 57 (2021); arXiv 1709.02577](https://arxiv.org/abs/1709.02577) | VPO smoothing plus modified QR path generation. Single-asset discrete down-and-out: VRFs are moderate and shrink with dimension because of cusps from the max over dates | C2 | Partial | Single asset, reports VRFs not exponents, no quantum link. It independently supports the C2 mechanism | yes |
| [Xie, He & Wang, EJOR 274(2) (2019)](https://doi.org/10.1016/j.ejor.2018.10.030) | Sequential importance-sampling smoother for discrete barriers plus path generation, under Black–Scholes and Variance Gamma. The abstract claims an improved convergence rate | C2 | Partial (potential qualifier) | A different smoother from those we ran. The exponents, asset count and dates are unknown. It must be cited, and C2 limited to the smoothers executed | abstract |
| [Beverland et al., arXiv 2211.07629 (2022)](https://arxiv.org/abs/2211.07629) | Layered resource estimator (Azure). Practical advantage needs superquadratic speedups and sub-µs operations for one-month runs | C6, C7, calculator | Partial | No quadratic application and no classical comparator. A possible cross-check for our compiled oracle | yes |
| [Jaques et al., EUROCRYPT 2020](https://arxiv.org/abs/1910.01700) | Depth-limited Grover oracles for AES and LowMC, with depth-width trade-offs and released Q# code | C3, C6 | Partial | Cryptanalytic cost models; no measured comparator and no clock mapping | abstract and metadata |
| [Sanders et al., PRX Quantum 1, 020312 (2020)](https://arxiv.org/abs/2007.07391) | Toffoli-level compilation of quadratic optimisation heuristics. Concludes they are unlikely to win without surface-code improvements | Framing, C3, C4 | Partial | Per-step classical comparison, no accuracy model, no frontier | abstract and metadata |

Also partial, lower threat:
- [Cade et al., Quantum 7, 1133 (2023)](https://arxiv.org/abs/2203.04975): constant-inclusive Grover query counts on instances.
- [Costa et al., PRA 112, 022429 (2025)](https://arxiv.org/abs/2412.13035): simple classical methods match the quantum SK heuristics studied.

None of the 30 distinct sources checked or added in this screen does all four of the
following:
1. measures a strong classical estimator's time to a dollar accuracy under a stated
   confidence for an option price;
2. uses the RQMC convergence exponent of that estimator inside the budget;
3. places an emitted, executed quantum pricing oracle with its width on the result;
4. reports the result as a multi-axis frontier (depth, clock, k, width, ε).

That combination is what survives.

---

## 4. Claim by claim (C1–C7, plus the reusable outputs)

| Claim | Status | Nearest prior art | Suggested wording |
|---|---|---|---|
| C1 budget identity | **Known** (correctly labelled "adapted") | Babbush 2021 (Eqs. 1–5); Hoefler 2023 (Table 2, the per-call budget inversion); Dalzell (qualitative QMC erosion) | "We use the break-even form of Babbush et al. and the per-call budget inversion of Hoefler et al., written in financial units, D_max = T_C/(10·k·(σ/e)·t_layer). It is an identity under a stated cost model, not a contribution. For plain MC it reduces to z²(σ/e)/(10k). Against RQMC with r ≈ 1 the sample-count advantage becomes a constant, as Dalzell et al. note qualitatively." |
| C2 smoothing restores calls and digitals, not knock-outs | **Known phenomenon; needs rewording.** The new part is the measurement on new shapes | Achtsis et al. 2013 (Table 2: 0.55–0.73 on a 4-asset, 130-date barrier); He & Wang 2017/2021 (cusps); Case 2026 v2 (Sec. 10, Table 8); Glasserman & Staum 2001 (method source); Xie, He & Wang 2019 (claims a rate improvement; unresolved) | "Consistent with earlier single-asset and single-barrier-asset studies (Achtsis et al. 2013; He and Wang; Case 2026), first-PC preintegration restores near-n⁻¹ RQMC for basket calls and digitals at 4×12 dates (48 dimensions). At 8×52 dates (416 dimensions), under the canonical factor, it restores the digital (r = 0.987, 95% interval [0.937, 1.042]) and is inconclusive for the call (r = 0.950, [0.897, 1.006]). This depends on the basis: under one of the six other valid PCA factors neither restores (call 0.849, [0.801, 0.896]; digital 0.848, [0.805, 0.895]). The two smoothers we executed on the knock-out (first-PC preintegration, and one-step-survival conditioning after Glasserman and Staum) leave knock-outs monitored on the basket average at 4×12 and 8×52 dates (48 and 416 dimensions) at exponents 0.48–0.63, with bootstrap intervals. We did not execute the sequential importance-sampling smoother of Xie, He and Wang (2019), which reports an improved rate for discrete barriers. C2 is therefore limited to the smoothers tried." The call and digital labels follow the Stage C claim C2 rule applied to item C1 (`results/frontier_classical_20261001/c1/c1_summary.json`; at 4×12 both restore under all seven factors). One-step survival was run on the knock-out only (`barrier_oss_pilot.json`), so it supports no call or digital claim. |
| C3 compiled knock-out oracle bracket | **Novel as an artefact; needs rewording.** No priority claim | Chakrabarti 2021 (hand-counted multi-asset barrier payoff, Q operator T-depth 9.5k); Stamatopoulos–Zeng 2024 (QSP); Jaques 2020 (depth-limited compiled oracles) | "In the project's reversible IR, a generic emitted and basis-replayed knock-out source has a clean scheduled T-depth of 6.0×10⁶ (4×12) and 6.4×10⁶ (8×52). The bracket is compiler-specific, and widths and T-counts are reported. A hand-counted re-parameterized arithmetic oracle of the Chakrabarti et al. type (T-depth 9.5×10³ per Q operator, for a smaller 3-asset autocallable) marks the optimistic end. Neither bound is a lower bound on other constructions." Avoid "first compiled". |
| C4 decision-point miss factors | **Novel as a measured result; needs rewording** | Chakrabarti 2021 (single-point threshold); Campbell 2019 and Brehm & Weggemans 2026 (same kind of verdict in search) | Report the miss factors at both ends of the C3 bracket. State explicitly that much of the gap at the emitted end reflects generic arithmetic (72-bit words, coherent Box–Muller, generic leaves) rather than any intrinsic requirement. Keep the corner list. Cite Chakrabarti for the earlier single-point threshold. |
| C5 six constructions, harmonized | **Novel** (project-internal); no external overlap found | none | Keep the shared-toolchain caveat. Say that this is a harmonized re-analysis of one group's attempts, not independent confirmation. |
| C6 requirements frontier | **Concept known; needs rewording.** The novelty is the measured inputs | Babbush 2021; Hoefler 2023; Chakrabarti 2021; Stamatopoulos–Zeng 2024; McArdle 2025; Dalzell 2025; Laura et al. 2026 (illustrative crossover sensitivity for pricing); Incudini & Mazzola 2026 (measured-GPU crossover, MCMC) | "We instantiate the published break-even argument for option pricing with measured inputs. These are the strongest classical time-to-accuracy we measured (timed RQMC with fitted exponents, 99% intervals) and the depth and width of emitted oracle sources. We report the oracle depth, logical clock, k, width and ε at which break-even and a 10× win would occur. Earlier pricing thresholds used an assumed classical target or scenario throughputs." |
| C7 hardware clock gap | **Framing known; data contribution only; needs rewording** | McArdle 2025 (required clock from workflow time); Beverland 2022 (sub-µs requirement); Dalzell (about 50 MHz) | "Consistent with earlier required-clock analyses (Chakrabarti; Stamatopoulos–Zeng; McArdle et al.), none of the N dated hardware sources screened on [date] demonstrates or credibly projects sustained reaction-limited logical T-layers of ≤ X ns." |
| Benchmark (cases, T_C(ε), D_max tables) | **Novel** (none found) | Case 2026 (RQMC protocol, single asset) | Keep. Cite Case's interval protocol where it is used. |
| D_max calculator | **Needs rewording** | QEA calculator (Mejia et al., QCE 2025); Azure Resource Estimator (Beverland 2022) | "A domain-specific calculator that places a user's oracle (T-depth, width, k) against measured classical time-to-accuracy tables. General break-even calculators exist (Mejia et al.); ours adds the accuracy, variance and confidence contract and measured classical inputs." |
| Checklist for advantage claims | **Needs citation** | Hoefler 2023 (guidelines); Grand Challenge (stage pipeline); Viamontes et al. 2004 | Present it as a pricing-specific consolidation of published guidance. |

---

## 5. Checkpoint decision: GO_NARROWED

**Reasons for not choosing GO.**

Each part of the plan's candidate novelty is weaker than §1 of IMPLEMENTATION_PLAN.md
assumed:
- *Measured classical methods with a failing payoff class.* The knock-out failure is
  published (Achtsis et al. 2013), its mechanism is explained (He and Wang; Case 2026), and
  it was re-measured two weeks ago on a single asset (Case v2). Only the basket-barrier
  shapes and the use of the exponent inside a quantum budget are new.
- *Frontier.* The generic argument (Babbush, Hoefler) and the pricing thresholds
  (Chakrabarti, Stamatopoulos–Zeng) are established. An illustrative pricing crossover
  sensitivity in oracle depth and classical throughput appeared on 17 September 2026
  (Laura et al.). The methodology of a measured strong solver plus a compiled oracle plus a
  runtime cap is established outside finance (Campbell et al.; Brehm and Weggemans). A
  measured-GPU versus compiled-quantum Monte Carlo crossover appeared in July 2026
  (Incudini and Mazzola, for MCMC).
- *Calculator.* A public break-even calculator exists (Mejia et al.).

**Reasons for not choosing RE_SCOPE.**

The plan's trigger is that "the frontier argument itself is already published". The plan
had already conceded the generic argument: C1 is labelled "adapted from Babbush", and
WHY_NO_ADVANTAGE.md §2.4 and §8 say the content lies in the measured inputs. Read that way,
the question is whether a *measured* frontier for option pricing is published. No checked
or newly found source:
- measures a strong classical time-to-accuracy for a price under a stated confidence;
- uses the classical convergence exponent in the budget;
- places an emitted oracle with width on a multi-axis frontier.

The prior finance thresholds use an assumed 1 s at 68% against the plain-MC rate. Laura et
al.'s inputs are labelled scenarios. Brehm and Weggemans show that a domain transfer of a
known measured-requirements method can be publishable. The candidate novelty therefore
survives, but only in narrowed form.

**A strict reading would give RE_SCOPE.** If the author reads the trigger strictly (any
published pricing crossover or frontier argument), then Chakrabarti et al. plus Laura et
al. already meet it, and the fallback applies. In practice the two readings differ less
than the labels suggest. The narrowed paper's defensible claims are nearly the fallback
list (measured knock-out exponents, compiled oracle bracket, harmonized budget,
benchmark), plus the measured frontier as the frame that ties them together.

**Named narrowings (binding on the draft):**

- **N1. Frontier.** "A measured instantiation for option pricing of the published
  break-even argument". Not "a new framework" and not "the first requirements frontier".
  Cite Babbush, Hoefler, Chakrabarti, Stamatopoulos–Zeng, McArdle, Dalzell and Laura et al.
- **N2. C2.** Rewrite as in §4: a known phenomenon, confirmed on basket-average barriers
  and limited to the smoothers executed. Xie, He and Wang must be cited as an unexecuted
  smoother that reports a rate improvement.
- **N3. C3.** No priority wording. The Chakrabarti-type hand count is the optimistic end
  of the bracket. The decision must be reported at both ends. The Stage C decision-point
  table (claim C4) carries this end as a labelled hypothetical row at T-depth 9.5×10³.
  That table's "favourable leaf-table score" (QF) row is a different optimistic end: it is
  compiler-based, charging the project's own oracle the cheapest certified leaf per
  operation, at 0.26–0.27 of the compiled forward dependency depth. The two are not
  interchangeable.
- **N4. Calculator.** Domain-specific; cite the QEA calculator.
- **N5. Methodology.** Cite Campbell et al., Brehm and Weggemans, and Incudini and Mazzola
  as the measured-comparator templates. Claim only the transfer to mean estimation for
  pricing, where the classical exponent and the accuracy/confidence contract change the
  budget.
- **N6. Title.** Keep the negative result in the title. Consider "a measured requirements
  frontier" → "measured requirements" or "a measured break-even analysis", so the title
  does not imply a new kind of object. This is the author's call.

**Venue implication.** The narrowed claim set suits a computational-finance or benchmark
venue at least as well as a quantum one. A Quantum-style venue stays possible on the
Brehm–Weggemans precedent. This is an input to the L2 venue decision, not a decision.

**What would flip this to RE_SCOPE.** Either of these:
1. Laura et al.'s full text turns out to use measured classical timings (RQMC or GPU), or
   to include width, k or a calculator.
2. Another source turns up that places a compiled pricing oracle against a measured RQMC
   time-to-accuracy.

**What would weaken C2 further.** Xie, He and Wang's tables show near-n⁻¹ on multi-date
barriers. If so, C2 becomes "the smoothers tried fail; a published SIS smoother reportedly
improves the rate", and the knock-out exponent room in the frontier would need that
smoother measured, or a disclosure.

---

## 6. Gaps and follow-ups

1. **Laura et al. 2026, full text.** MDPI is open access but was blocked to this agent. The
   author should open it in a browser and record:
   - the sensitivity model;
   - its classical inputs (measured or assumed);
   - whether width, k or confidence appear;
   - whether a tool or code is released.

   This is the main residual risk to GO_NARROWED.
2. **Xie, He and Wang 2019, full text** (library access). Record the exponents, the asset
   count, the monitoring dates and the path-generation method before freezing C2. Read the
   rate tables of Achtsis et al.'s Heston follow-up (arXiv 1207.6566) at the same time.
3. **Stamatopoulos–Zeng body text.** Re-read it to confirm the inherited 1 s target and
   68% confidence. Only the abstract and metadata were checked here.
4. **Cite Case v2 Secs. 11.1–11.2 in ERRATA E10**, as the published description of the
   non-unique PCA basis effect.
5. **Update WHY_NO_ADVANTAGE.md §7 and §10:**
   - the Grand Challenge wording (point 5 of §2), citing PRX Quantum 7, 020101;
   - add Achtsis et al. 2013, Case 2026 v2 and Xie, He and Wang 2019 to the references.
6. **Coverage gaps not closed:**
   - Google Scholar "cited by" for Chakrabarti et al. and Babbush et al., which catches
     arXiv-only citers;
   - Winter Simulation Conference proceedings 2019–2025 on barrier RQMC;
   - MCQMC 2026 talks;
   - patents (a Goldman Sachs patent on re-parameterization resource estimation appeared
     in results and was not examined);
   - non-English literature.
7. **Who should check this.** A human expert in QMC for finance should confirm that no
   multi-asset basket-barrier RQMC rate study exists beyond those listed. A human expert in
   fault-tolerant resource estimation should judge whether the N1–N5 narrowings are
   sufficient.

The record of every check is `l1_verification.jsonl` in this folder. This screen was done
by an AI agent on 1 October 2026. It is selective, it is not exhaustive, and it is not
peer review.
