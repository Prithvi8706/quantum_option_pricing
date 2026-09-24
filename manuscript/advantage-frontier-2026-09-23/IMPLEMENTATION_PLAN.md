# Three-week implementation plan: the measured requirements-frontier paper

Version 2, 24 September 2026. It supersedes version 1 after an internal red-team of 80
findings (8 critical, 55 major, 17 minor) from four independent critic agents. The
dispositions are in [reviews/PLAN_REVIEW_R0.md](reviews/PLAN_REVIEW_R0.md), and the raw
findings in [reviews/plan_review_r0_findings.jsonl](reviews/plan_review_r0_findings.jsonl).

**Dates.** Day 1 is the first working day after this plan is committed on branch
`research/advantage-frontier-paper`. Day 15 is the end of Week 3, at five working days per
week. Affiliation: VIT Vellore. Author names and approvals are supplied by the author.

**Inputs.**
- [WHY_NO_ADVANTAGE.md](WHY_NO_ADVANTAGE.md): the foundation text.
- The investigation in `docs/research_investigation/2026-09-23/`: DECISION, H1 results,
  screening table, and the corrections in
  [ERRATA.md](../../docs/research_investigation/2026-09-23/ERRATA.md) and
  [PREREGISTRATION_DEVIATIONS.md](../../docs/research_investigation/2026-09-23/PREREGISTRATION_DEVIATIONS.md).

---

## 0. Goal, honest definition of done, and ground rules

### What Day 15 delivers

- A complete manuscript with a **LaTeX + BibTeX canonical source**. Every number is bound
  by placeholders to frozen artifacts, and the PDF is built by latexmk with a receipt.
- **Two rounds of internal AI-agent review.** This is not peer review. Every critical and
  major finding is closed with a linked change or a recorded rejection reason.
- A two-tier reproducibility receipt from a clean detached checkout, in the repository's
  established release format.
- `SUBMISSION_READINESS.md` stating plainly that the draft is **not submission-ready**
  until the author has personally verified it (`AUTHOR_VERIFICATION.md`) and a named
  human expert has reviewed it. This matches the repository's precedent in
  `manuscript/controlled-compound-2026-09-22/SUBMISSION_READINESS.md`.

### What "foolproof" can and cannot mean

- *It can mean:*
  - every number is generated rather than typed;
  - every claim is in a ledger with its evidence level;
  - every citation is checked against its primary source;
  - independent agents, some from a different model family if the author consents,
    tried to break each claim, and the record of those attempts is kept.
- *It cannot mean* external peer review, acceptance, or a guarantee that nothing was
  missed. No document may describe the internal reviews as peer review, refereeing or
  acceptance.

### Ground rules

1. **Symmetric pre-specification.** No analysis choice may be made or revised after
   seeing its effect on the decision, in either direction. Before any Week-1 analysis
   runs, `ANALYSIS_SPEC.md` is committed on Day 1. It fixes fit windows, bootstrap units,
   the k definitions, reference targets and agreement tests, sensitivity grids, the σ
   convention and the pass criteria. Gates check that an analysis was *executed as
   specified*. They never check that "the conclusion is unchanged"; outcomes are
   recorded, not required.
2. **The H1 decision is historical, not re-tuned.** It was made by a rule stated before
   the P3/Q1 runs, according to the working record, but it is not externally
   time-stamped. It was written after the P1/P2 pilots and executed with disclosed
   deviations. The paper says exactly that. Missing arms are executed in Week 1 as
   *disclosed robustness checks*, or reported as not done.
3. **Fixed verdict wording:** "No defensible significant quantum advantage established
   yet." The paper is a requirements and negative result. It claims neither advantage
   nor impossibility.
4. **Nothing overwrites archived evidence.** New runs write new versioned artifacts.
   Corrections go to `ERRATA.md`. The 22 September manuscript and the controlled-compound
   draft stay unchanged, and overlap with them is disclosed.
5. **Usage-limit hygiene.** Agent waves stay at ≤ 6 agents. Every agent appends its
   results incrementally. CPU work runs locally where possible.

---

## 1. The paper

**Working title.** *What quadratic quantum speedups would need to beat strong classical
option pricing: a measured requirements frontier.* The negative result is in the title,
so it cannot be read as an advantage claim.

**Framing: reusable outputs, with project history in an appendix.**
1. **A frozen benchmark:** the knock-out and Asian-basket development cases plus the
   24-case generator, with reference prices, T_C(ε) tables and D_max tables.
2. **A D_max calculator:** a script that lets others place their own oracle (T-depth,
   width, k) on the frontier.
3. **A checklist for future advantage claims:** the comparator, symmetric certification,
   joint sensitivity corners, and reporting at break-even and at 10×.
4. **The six constructions:** three contracts, one toolchain, as a harmonized table and an
   appendix. They are not presented as independent confirmations.

**Claims.** Each is recorded in `CLAIM_LEDGER.md` with its evidence level and artifact.

| ID | Claim (wording as it should appear) | Evidence level |
|---|---|---|
| C1 | Budget identity adapted from Babbush et al.: D_max = T_C / (10·k·(σ/e)·t_layer). In classical-sample units, ρ_max = N_C(ε)·e/(10kσ). This reduces to z²(σ/e)/(10k) for plain MC and to a constant-factor condition against RQMC with r ≈ 1. The content lies in the measured inputs | Identity under a stated cost model; assumptions and failure conditions in a proposition |
| C2 | On two GBM basket shapes (48 and 416 dimensions), plus the Week-1 extra cases, the smoothing methods tried restore near-n⁻¹ RQMC convergence for calls and digitals but not for discretely monitored knock-outs | Executed; rates with bootstrap intervals; methods listed |
| C3 | A depth-optimized knock-out oracle built in the project's reversible IR has clean-call T-depth bracketed by [cheapest-leaf score, compiled scheduled depth]. Width and T-count are reported | Compiler-specific; bracket validated on compiled sources |
| C4 | At the decision point (ε = $0.001, t = 100 ns, k = 3) the oracle exceeds the 10× budget by the factors in the frozen tables (regenerated in Week 1; the historical values are in ERRATA). The joint-sensitivity table lists every corner within 10× and why each lies outside credible assumptions | Executed decision rule plus a full factorial sensitivity |
| C5 | Six constructions over three contracts, all from one toolchain, each fail the 10× condition at their own operating point. Re-evaluated at one common operating point where the contract allows | Harmonized re-analysis; shared-component caveat |
| C6 | Requirements frontier in depth, width and T-throughput: the combinations of oracle depth, logical clock, k, accuracy and width at which a 10× win (and break-even) would occur | Sensitivity analysis, with extrapolated regions marked |
| C7 | Among the N dated hardware sources screened, none demonstrates or credibly projects sustained reaction-limited logical T-layers of ≤ X ns. That is a cut of about 10³ from the 100 ns assumption and 10⁴–10⁶ from the published 1–10 µs projections | Selective literature screen, dated |

**Non-claims, stated in the abstract and the conclusion.**
- No advantage claim and no impossibility theorem.
- No lower bound over all circuits or algorithms.
- No claim about models not studied.
- The classical comparator is "strong, not exhaustive".

**Candidate novelty.** It is to be confirmed by the Day-2 checkpoint (§4, Track L):
- measured strong (not exhaustive) classical methods, including one payoff class where the
  smoothing methods tried fail;
- complete compiled sources for two studies, partial compiled charges for three, and one
  compiled knock-out oracle, placed on one frontier with width and throughput;
- a reusable benchmark and calculator.

**Fallback contribution**, fixed now: if the Day-2 prior-art check finds the frontier
argument itself is already published, the paper claims only the measured knock-out
exponents, the compiled oracle bracket, the harmonized budget and the benchmark, and it
targets a benchmark or computational-finance venue.

---

## 2. Assets in hand, stated precisely

| Asset | Location | Caveat |
|---|---|---|
| Foundation text | `manuscript/advantage-frontier-2026-09-23/WHY_NO_ADVANTAGE.md` | Corrected 24 Sep |
| Investigation, 152-row screen, verified load-bearing claims | `docs/research_investigation/2026-09-23/` | Selective screen |
| P1, P2, P3, frontier, Q1, decision scripts and archived outputs | `research/` and `results/advantage_frontier_20260923/` | Outputs came from pre-lint versions. A 24-Sep replay from the committed scripts reproduced all 4,367 non-timing fields exactly ([record](../../docs/research_investigation/2026-09-23/PROVENANCE_REPLAY_20260924.md)); it is rerun in the pinned environment on Day 1 |
| Five earlier studies | `docs/antithetic_feasibility`, `docs/compound_feasibility`, `docs/controlled_residual_feasibility`, `docs/controlled_source_completion`, `docs/controlled_priority_completion`, and matching `results/` | Heterogeneous operating points |
| Range-specialized f=40 leaf library, compiled C4/H8 sources and wave schedules | `results/controlled_priority_completion/range_compile_v1/`, `range_parallel_v1/` | Certified only for C4/H8 operand ranges |
| Generic (unranged) leaf libraries | `results/controlled_source_completion/compile_v1/leaves_f24`, `leaves_f40`; `results/controlled_completion_followup/arithmetic_v1/leaves_f24`, `leaves_f40`, `leaves_f64` | There is **no f=32 library** |
| Compiler, IR, optimizer, range audit | `research/controlled_source_completion/`, `research/controlled_priority_completion/` | `ranges_for_compiled` is hard-wired to the compound model at f40/q32 |
| Explicit estimator schedules | `results/controlled_priority_completion/estimator_hadamard.json` (moment-conditional), `estimator_bounded.json` (unconditional) | Built for the compound residual estimand; not transferable as a constant |
| Precedent build and release tooling | `research/controlled_priority_completion/build_draft.py`, `RELEASE_RECEIPT.md`, `release_validation/` | Hard-wired to the companion paper; tools live in gitignored `.context/` |
| TeX toolchain | MiKTeX 25.12, latexmk 4.88 (local) | Versions recorded in the build receipt |

---

## 3. Work items (each closes named critic findings; see PLAN_REVIEW_R0.md)

### Track Q: quantum oracle (executed locally)

| Item | Work | Pass criterion (fixed in ANALYSIS_SPEC) |
|---|---|---|
| Q0 | **Provenance replay.** Rerun P1, P2, P3, Q1, the decision and the frontier from the committed scripts in the pinned environment (T0); diff every non-timing field exactly | Exact equality of prices, rates, fit constants and depths; mismatches go to ERRATA |
| Q1 | **Scorer consistency (regression check).** A per-node exact rescoring of the compiled C4/H8 sources reproduces 2,972,154 and 3,075,738 | Exact equality |
| Q2 | **In-sample bracket.** Cheapest-leaf and median-leaf table scores of C4/H8 relative to exact (currently 0.612/1.077 and 0.602/1.073) | Favourable ≤ exact; ratios reported |
| Q3 | **Per-node cost model.** Constant multiplies by their actual constant (leaves built on demand) and lookups by table size. Regenerate the knock-out depth (4×12 forward is expected to rise from 442,529 to about 638,003) | Model reproduces exact depth on C4/H8 |
| Q4 | **Payoff validation (G1c).** A committed script evaluates the IR against an independent NumPy payoff on ≥ 10⁴ draws, stratified near the barrier, plus edge draws (knocked out, A < K, spot-guard clip, extreme uniforms). It records maximum error, misclassification count and a barrier-bias bound: jump × P(\|max basket − H\| ≤ δ_fp) | Archived JSON; bias bound ≤ the ε/10 numerical allowance, otherwise reported as a limitation |
| Q5 | **Emit and schedule.** Optimize and compile the 4×12 and 8×52 knock-out IR with a stated leaf set; run basis-input execution (16 + edge inputs for 4×12, 2 for 8×52) against `ir.evaluate`; record make_schedule dependency-only depth, wave depth at limits {None, 128, 32}, and logical qubits | Bit-exact execution; same-leaf-set dependency-only score ≤ scheduled depth, otherwise the scheduled value replaces it |
| Q6 | **Range certificate** (stretch, Days 2–3): a witness for the Estrin exponential, generalize `ranges_for_compiled` to a builder callable, certify zero overflow sites, then do a ranged compile and per-node certified depth | If it slips, C3 uses the Q5 generic-leaf schedule and the favourable score as the bracket ends |
| Q7 | **Best-known-primitive rescoring.** Replace leaf costs with published constructions (logarithmic-depth adders, T-depth-1 Toffoli with ancillae, log-depth multiplier trees), each cited, and re-evaluate the decision grid | Reported as the optimistic end of C3 |
| Q8 | **Precision, like with like.** Compare f=24 and f=40 generic leaves from the same compiler generation; apply the ratio as a width-scaling bound; check the fixed-point error at f=24/q≤23 against the $0.001 budget with Q4's bias method | Ratio and error reported (no f=32 unless a w=64 library is built) |
| Q9 | **Width and throughput.** Logical qubits of each schedule, qubit-capped schedules (10⁴ and 10⁵ logical qubits), and the magic-state rate required at each t_layer | Columns in the frontier tables |
| Q10 | **Time model.** Define t_layer as the reaction-limited time per T layer with Clifford time set to zero (quantum-favourable); add a Clifford-inclusive sensitivity | Stated in the text; F4 sensitivity |

### Track C: classical side (CPU first, then GPU)

| Item | Work | Pass criterion |
|---|---|---|
| T0 | **Pinned environment** (Day 1). A fresh isolated venv (no system site-packages) with a hash-pinned lock: numba 0.60, one numpy, scipy, mpmath, matplotlib, pytest, qiskit, ruff, plus document tools (Markdown 3.7 for notes). The TeX toolchain version is recorded | Lock committed; Q0 runs in it |
| C1 | **Rates with uncertainty.** New P1/P3 versions archive per-scramble prefix estimates; extend P3 to 2¹⁹; bootstrap the joint (A, r) fit over scrambles; fit windows fixed in the spec; mark extrapolated regions | Intervals reported; n(ε) inside the measured range or flagged |
| C2 | **Timing model.** Fit T(n) = a + b·n on warm prefixes after the first chunk; report cold start separately; run the estimator at n(ε) to confirm the achieved half-width; record CPU, power plan and affinity; ≥ 5 warm repeats plus 1 cold | Median and range; the corrected 4×12 ratio is already recorded in ERRATA E5 |
| C3 | **References (G4).** Two constructions that differ from the P3 estimator: numba bridge-ordered one-step survival, and numba plain iid MC on 16 processes. SE target and agreement test (sum of half-widths within ε/10) pre-set; resolve the P1/P3 4×12 gap of 2.1 SE | Agreement or a documented discrepancy; budget 40–60 CPU-hours, run overnight on Days 2–4 |
| C4 | **Coverage.** ≥ 1,000 independent 16-scramble t-intervals at n = 2¹⁰–2¹³ against the C3 reference; Clopper–Pearson coverage | Coverage reported; symmetric-rigorous sensitivity: classical empirical-Bernstein cost vs quantum k_explicit |
| C5 | **Stronger smoother.** At least one of multi-direction numerical smoothing or first-PC preintegration plus bridge-ordered one-step survival | Rate and T_C reported; C2 wording follows the result |
| C6 | **GPU comparator.** Port the preintegration kernel to numba.cuda or CuPy. This needs CUDA toolkit wheels installed into the pinned environment, a download of several hundred MB, **with the author's OK on Day 1**. Time it under the C2 protocol | Used as the comparator in C4/C6; otherwise g ∈ {1, 10, 100} carried with the STAC-A2 anchor and the text says "strongest measured CPU implementation" |
| C7 | **Missing arms.** 16×52 and H ∈ {120, 160} through P3, Q-scoring and the unchanged rule | Reported as disclosed robustness checks |
| C8 | **Out-of-sample check.** The pre-fixed 24-case generator from DECISION §6 through P3, Q-scoring and the unchanged rule; distribution of oracle/D_max | Reported; no retuning |

### Track L: literature and analysis (agents, ≤ 6 per wave)

| Item | Work | Deadline |
|---|---|---|
| L1 | **Prior art and novelty**, wide: pre-2020 work, surveys, perspectives, break-even analyses in any domain, and finance thresholds (Chakrabarti et al. is itself a threshold paper). Nearest-prior-art matrix. **Go/re-scope checkpoint at the end of Day 2** | Day 2 |
| L2 | **Venue compliance** from official pages: format and source, length, abstract, keywords, required statements, **AI-authorship and disclosure policy**, data/code policy, preprint and arXiv policy, fees. Conformance checklist | Day 2 |
| L3 | **k from estimator theorems** for the knock-out's own range and σ at δ = 0.01: canonical QAE with median amplification, IQAE, and a variance-sensitive estimator with its log factors. A one-row call-accounting table defines "one call" identically for k and D. The project's explicit k is reported only with its caveat | Day 4 |
| L4 | **Six-construction extraction:** each study's native miss factor and assumptions (ε, k, t_layer, depth scope, classical warm/cold, σ convention), with a SHA-256 manifest | Day 4 |
| L5 | **Harmonized re-evaluation** of L4 at one common operating point where each contract allows; otherwise a stated reason | Day 7 (before F3) |
| L6 | **Oracle-family table:** Grover–Rudolph/KP-tree loading, re-parameterization, QSP payoff, arithmetic-free state preparation, learned loaders, KL/analog encodings, and low-depth/parallel AE with their repetition cost. Each placed against the crossing depth with a primary citation | Day 4 |
| L7 | **Dated hardware table**, demonstrated vs projected, with access dates; C7 wording from it | Day 5 |
| L8 | **Contract justification** (ε, 99%, 10×) from sources; reporting at break-even (1×) and 10×, and at 95/99/99.9% confidence | Day 5 |

### Cross-cutting analysis

| Item | Work |
|---|---|
| X1 | **Joint sensitivity factorial:** oracle ∈ {Box–Muller scheduled, free-Gaussian, cheapest-leaf, best-known primitives, hypothetical 9.5×10³ (not a floor)} × k ∈ {1, 3, 10, theorem-derived} × t_layer ∈ {10 ns, 100 ns, 1 µs, 10 µs} × σ ∈ {plain, preintegrated} × P_Q ∈ {1, 10} × classical ∈ {CPU, GPU or g}. Shade speed-up > 1 and > 10. Every corner within 10× is listed in the text with the reason it is not credible |
| X2 | **Canonical frontier convention:** `barrier_decision.json`-style (plain σ, P3 wall time). The P1 `frontier.json` is labelled a superseded sensitivity (ERRATA E6) |

---

## 4. Schedule

### Week 1: evidence hardening and freeze (Days 1–5), three parallel tracks

| Day | Track Q (quantum) | Track C (classical CPU/GPU) | Track L (agents) | Author |
|---|---|---|---|---|
| 1 | Commit ANALYSIS_SPEC.md and AI_USE_LOG.md before any run. Q1, Q2 | T0 environment; Q0 provenance replay in T0 | L1, L2 start | OK the CUDA download (C6)? |
| 2 | Q3 per-node model; Q4 payoff validation; Q5 emit and schedule 4×12 and 8×52 | C1 new P1/P3 versions; C3 references start overnight | L1 checkpoint (go/re-scope); L2 conformance | **Venue decision** (primary and fallback) from L2, recorded in VENUE.md |
| 3 | Q6 range certificate (stretch); Q8 precision | C2 timing model; C5 stronger smoother; C3 continues | L6 oracle families | — |
| 4 | Q7 best-known rescoring; Q9 width/throughput; Q10 | C4 coverage; C7 missing arms; C8 out-of-sample; C6 GPU if approved | L3 k from theorems; L4 extraction | — |
| 5 | X1 joint factorial; regenerate all C-claim tables from frozen JSON | Finish C3/C4 | L7 hardware; L8 contract; nearest-prior-art matrix | Review the evidence pack (~1 h) |

**Day 5, before the freeze: mini review R0.** Two agents with the quantum-resource and
computational-finance lenses review the evidence pack, so that any finding needing new
computation lands while compute is still scheduled. Then:
- rehearse the clean-checkout replay;
- tag `frontier-evidence-v1` (local tag, pushed with the branch);
- update CLAIM_LEDGER v1 and ERRATA.

**Week-1 exit gate.**
- Q0 provenance replay passes.
- Q1 is exact.
- Q2 and Q5 bracket directions hold, or the numbers are replaced as specified.
- Every item in ANALYSIS_SPEC was executed as specified, with its outcome recorded.
- C2–C6 claims have artifacts (C1 and C7 artifacts arrive in Week 2).

If a decision-relevant number changes, it goes to ERRATA, and the claim text follows the
new evidence. If the STOP itself fails under the stated rule, stop and re-plan with the
author before writing.

**Cut list if Week 1 slips**, applied in this order (each cut is disclosed in the paper):
1. C6 GPU → carry g.
2. Q6 range certificate → generic-leaf bracket.
3. C8 out-of-sample → report as not done.
4. C5 stronger smoother → weaken C2 to "for the two smoothers tried".

### Week 2: full draft in LaTeX (Days 6–10)

| Day | Work |
|---|---|
| 6 | Title and outline fixed against the claim ledger and VENUE.md (use the superset structure if the venue is undecided: both abstract lengths, key messages, a contributions subsection). **LaTeX skeleton** in the venue's class plus BibTeX. **Numbers registry**: `make_numbers.py` writes `numbers.json` from the frozen artifacts and renders `numbers.tex` macros, keyed by name with source path and format. A parameterized build script (latexmk, recorded MiKTeX/package versions, receipt). A tracer rejects bare digits outside macros and an allow-list |
| 7 | `make_figures.py` from frozen JSON: F1 frontier (depth × ε, with width and throughput panels, extrapolation marked); F2 convergence with bootstrap bands; F3 harmonized six-construction chart (after L5); F4 joint sensitivity (t_layer, k, σ, P_Q, g; break-even and 10×); F5 oracle depth anatomy |
| 8 | Draft introduction, related work (with the L6 oracle-family table), contract and budget identity (C1 as a proposition: assumptions, when it fails, units), classical methods. **Citation verification (G11) begins**: every reference checked against its primary page, recorded in CITATIONS_VERIFIED.md |
| 9 | Draft results (C2–C6), hardware (C7), limitations, the reusable benchmark, calculator and checklist, and the conclusion. Abstract; reproducibility and data availability; overlap statement; AI-use disclosure variants generated from AI_USE_LOG. **Draft to the author at end of day** |
| 10 | Morning: fold in the author's comments (v1.1). Finish G11. Tracer and build, then a clean-checkout replay rehearsal. `main.pdf` v1.1 with receipt |

**Week-2 exit gate.**
- v1.1 builds from LaTeX, with zero bare numbers outside macros or the allow-list.
- All references are verified.
- The author's comments are incorporated.
- The replay rehearsal passes.

### Week 3: internal review, revision and release (Days 11–15)

| Day | Work |
|---|---|
| 11 | **R1:** six lenses (§5), blind to each other. R-E (reproducibility) performs the formal clean-checkout run |
| 12 | A separate agent tries to refute every R1 critical or major finding; triage; fix text and artifacts |
| 13 | Morning: evidence re-runs demanded by R1 under tag `frontier-evidence-v2`, with automatic re-trace and rebuild. Afternoon: **R2**, with fresh reviewers for any lens that had critical or major findings, plus one whole-paper internal reviewer |
| 14 | R2 fixes. Release validation in the precedent's format: artifact audit before and after replay, pytest for new test files (scorer, emitter, bootstrap, extraction, numbers registry), ruff and whitespace checks, `release_validation/receipt.json` with commands, return codes, log hashes, all_passed and a clean final git status. The two-tier replay (below) |
| 15 | A fresh agent checks the closure of R2 fixes. FINAL_REVIEW.md (author/reviewer matrix), final CLAIM_LEDGER, SUBMISSION_READINESS.md, HUMAN_REVIEW_PACKET.md, AUTHOR_VERIFICATION.md template. Commit and push the branch; open a PR only if the author asks. Half-day buffer |

**Two-tier replay** (defined in REPRODUCE.md):
- *Exact tier:* every table, figure, `numbers.json` and the LaTeX source are regenerated
  byte-identically from the frozen artifacts. The PDF is compared by extracted text
  rather than by hash, because of CreationDate.
- *Re-measurement tier:* timings are rerun on the same machine, with the pre-stated
  tolerance that the median is within ±25% and the decision inequality keeps a ≥ 10×
  margin. The result is reported.

**Week-3 exit gate (definition of done).**
- No open critical or major internal findings.
- Both replay tiers pass.
- Citations are verified.
- The claim ledger matches the text.
- The LaTeX build receipt is present.
- `SUBMISSION_READINESS.md` lists author verification, human expert review and the
  author-only items as outstanding.

---

## 5. Internal review protocol

| Lens | Must try to break |
|---|---|
| R-A Statistics and numerics | Rate fits and bootstrap, references, coverage, timing model, extrapolation |
| R-B Quantum resource estimation | Bracket validation, per-node model, emitted schedule, best-known primitives, k accounting, t_layer model, width and throughput, oracle families |
| R-C Computational finance | Contract justification, strength and fairness of the classical methods, generality beyond the executed cases |
| R-D Claims and overstatement | Every sentence against the claim ledger; verdict and non-claims; no peer-review language; AI-use disclosure against AI_USE_LOG |
| R-E Reproducibility | The formal two-tier replay from a clean checkout |
| R-F Simulated desk review | Novelty against the L1 matrix, venue conformance checklist, title and abstract |

**Rules.**
- Reviewers see only the manuscript, the repository and primary sources, and default to
  "finding" when uncertain.
- Severities: *critical* invalidates a claim; *major* means a claim needs weakening or new
  evidence; *minor* is clarity.
- Every critical or major finding gets an independent refutation attempt.
- A finding closes only with a linked change or a recorded rejection reason.
- Round 2 uses fresh agents.
- **Model diversity:** if the author consents (Day 1) to sending the draft to an external
  model provider, R-B, R-C and the R2 whole-paper reviewer run on a different model
  family through the `codex` skill. Otherwise the reviews are recorded as single-family.
- Every review file records the reviewer's model identity.

---

## 6. Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| The Q0 provenance replay finds numeric drift in the new pinned environment | Low (the 24-Sep replay in the original interpreters had 0 mismatches over 4,367 fields) | ERRATA entry; regenerate claims before writing |
| Q6 range certificate slips | High | Generic-leaf bracket (Q5) plus the favourable score; disclosed |
| Per-node or best-known rescoring shrinks the margin materially | Medium | This is the point of Q3/Q7; C4 reports whatever results; X1 lists corners |
| A reviewer argues other oracle families invalidate C4 | High | L6 table plus X1 crossing-depth analysis, with primary citations |
| Prior art already states the frontier argument | Medium | Day-2 checkpoint; pre-committed fallback contribution |
| References disagree at $0.001 (a 2.1 SE gap already exists) | Medium | C3 resolves it; the paper's price is the reference, not a pilot |
| The CUDA toolchain cannot be installed | Medium | Carry g with the STAC-A2 anchor; wording "strongest measured CPU" |
| Venue AI policy forbids generative drafting | Medium | Decided on Day 2; exclude such venues unless the authors rewrite; recorded in VENUE.md |
| arXiv endorsement blocks a first-time submitter (a Quantum route needs quant-ph) | Medium | Author checks the account and endorsement in Week 1; fallback venue without an arXiv requirement |
| Usage limits or network outages interrupt agents (observed twice) | High | ≤ 6-agent waves, incremental saving, CPU-first tracks, a half-day buffer each week |
| Author time or approvals late | Medium | Only author-only items may remain open at Day 15; stated in SUBMISSION_READINESS |
| Scope creep into new advantage hunting | Medium | Out of scope; future-work paragraph only |

---

## 7. Resources

- **Compute:** about 60–80 CPU-hours (C3 references dominate, run overnight), ≤ 4 GPU-hours
  if C6 is approved, and single-digit hours for compiles and basis runs.
- **Agent waves:** Week 1, 2 waves (L1+L2, then L3+L4+L6 and R0); Week 2, 1 wave (G11);
  Week 3, 3 waves (R1, refutations, R2 and closure).
- **Author time:** at least 10–12 hours in total:
  - Day 1 approvals (CUDA download, external-model reviewers): 0.5 h;
  - Day 2 venue decision: 0.5 h;
  - Day 5 evidence pack: 1 h;
  - Day 9–10 read of v1 and comments: 3–4 h;
  - Days 13–15 verification of the proposition, the ledger and the AI-use disclosure, plus
    a referee-question drill from R1: 5–6 h.

## 8. Only the author can supply or do

- Author names and order; affiliation lines (VIT Vellore); corresponding email; funding,
  competing interests and contributions.
- Personal verification of the C1 proposition, the claim ledger and the text, recorded in
  AUTHOR_VERIFICATION.md, plus approval of the AI-use disclosure.
- Venue and fee choice (Day 2); confirmation of no concurrent submission; the overlap
  decision with respect to the two earlier drafts.
- An **arXiv account and endorsement**, the licence choice (irrevocable), and preprint
  timing relative to the companion drafts.
- Permission for external-model reviewers and for the CUDA toolkit download.
- **A named human expert review**, required before submission, not optional. Expertise
  needed: fault-tolerant resource estimation, and QMC/computational finance.
- An optional Zenodo or DOI archive of the evidence tag.
