# Plan review R0: internal red-team of the implementation plan

24 September 2026. Four critic agents (feasibility, hostile referee, venue compliance,
factual consistency) reviewed plan v1 independently. They are internal AI-agent reviews
from a single model family, **not peer review**. The raw findings, with evidence and
proposed fixes, are in `plan_review_r0_findings.jsonl`. Findings that touched
already-committed evidence documents were checked against the artifacts before being
accepted, and are recorded in `docs/research_investigation/2026-09-23/ERRATA.md`.

Totals: 80 findings; 8 critical, 55 major, 17 minor.
All are accepted. None was rejected. Disposition references point to plan v2
(`IMPLEMENTATION_PLAN.md`) item IDs.

| ID | Lens | Severity | Finding (first sentence) | Disposition in plan v2 |
|---|---|---|---|---|
| F01 | feasibility | critical | G1a is either impossible or circular. | Q1 regression check + Q2 in-sample bracket (favourable <= exact); old G1a removed |
| F02 | feasibility | critical | The knock-out oracle cannot be emitted through the range-certified path in the time allotted, and the plan does not say which path G1b uses. | Q5 emit via stated leaf set (generic) + Q6 range certificate as stretch with fallback |
| F03 | feasibility | major | The 'favourable' table charges each knock-out node the cheapest leaf of that operation type in a library built for a different graph. | Q3 per-node cost model (cmul by constant, lookup by table); ERRATA E3 |
| F04 | feasibility | major | Nothing in the repository checks the knock-out IR against the priced contract (the P1 floating-point payoff), and G1b does not add such a check. | Q4 archived payoff-validation script with barrier-bias bound; ERRATA E4 |
| F05 | feasibility | major | G6 as written would produce a misleading or impossible comparison. | Q8 like-for-like f24/f40 generic leaves; no f=32; section 2 corrected |
| F06 | feasibility | major | Consolidating the three environments is more than a one-day side task, and the plan omits the re-run-and-diff it implies. | T0 isolated hash-pinned environment + Q0 replay/diff; rehearsal Day 5 |
| F07 | feasibility | major | The archived P3 timing, and therefore T_C and D_max, includes a fixed first-call overhead of about 5 s per worker (JIT or cache load and process start) that is spread across per-p... | C2 warm timing model T(n)=a+b*n, cold reported separately; ERRATA E5 |
| F08 | feasibility | major | G2 cannot be computed from archived data, and its effect on T_C($0.001) is large. | C1 new per-scramble archiving, P3 to 2^19, joint (A,r) bootstrap |
| F09 | feasibility | major | The G1b pass criterion is ambiguous in two ways. | Q5 gate: same-leaf-set dependency-only <= scheduled, else replaced |
| F10 | feasibility | major | G5's formula 'explicit calls / (sigma/e)' is ambiguous by more than an order of magnitude, and it transfers a schedule built for a different estimand. | L3 k from estimator theorems for the knock-out estimand + call-accounting table |
| F11 | feasibility | major | G8 is described as extraction, but C5 and figure F3 require re-analysis. | L4 native extraction (Day 4) + L5 harmonized re-evaluation (Day 7) |
| F12 | feasibility | major | Week 1 is scheduled as one serial thread whose realistic effort is about 9-10 person-days, and its dependency order is wrong. | Week 1 rebuilt as three parallel tracks with dependencies and a cut list |
| F13 | feasibility | major | The prior-art and novelty check is scheduled on Day 5, the evidence-freeze day. | L1 moved to Days 1-2 with go/re-scope checkpoint |
| F14 | feasibility | major | The Day-10 gate relies on a number-tracing script that does not exist, and matching numbers in prose after the fact is fragile. | Numbers registry + LaTeX macros + bare-digit tracer built Day 6 |
| F15 | feasibility | major | Week 3 has no capacity for review findings that need new evidence, and it runs citation verification at the same time as round 2. | G11 moved to Days 8-10; evidence-v2 slot Day 13 AM; replay rehearsals Days 5/10 |
| F16 | feasibility | minor | G1b validates only the 4x12 oracle, while C3 and C4 quote 8x52 depths (8.99x10^5 clean call) and the 8x52 case sets the smaller miss factor (1,138x). | Q5 also compiles and schedules 8x52 with basis runs |
| F17 | feasibility | minor | G4's plain iid MC reference is not sized, and the existing kernel is single-threaded. | C3 references sized in ANALYSIS_SPEC, numba multi-process, 40-60 CPU-h |
| F18 | feasibility | minor | The author receives v1 on Day 10 and round 1 of review starts on v1 on Day 11, but no slot incorporates the author's comments. | Draft to author end of Day 9; comments folded Day 10 AM before R1 |
| R01 | referee | critical | The oracle is scored with leaves that are far from best-known reversible arithmetic, and no work item tests this. | Q7 best-known-primitive rescoring; C3 stated as a bracket |
| R02 | referee | critical | Robustness is claimed one factor at a time, but joint quantum-favourable corners already in the archived grid give a modelled quantum speed-up. | X1 full joint factorial; every corner within 10x listed; ERRATA E1/E2 |
| R03 | referee | major | Certification is asymmetric and never tested. | C4 coverage experiment + symmetric-rigorous sensitivity; 'certified' only for certified leaves |
| R04 | referee | major | The 'pre-registered' claim cannot be verified, and deviations from the pre-registered protocol are not disclosed. | Ground rule 2 wording; PREREGISTRATION_DEVIATIONS.md; missing arms C7 |
| R05 | referee | major | All C2-C4 evidence comes from one GBM parameter set in two shapes, and no held-out case was ever generated. | C8 out-of-sample 24-case generator; C7 missing arms |
| R06 | referee | major | The plan calls the classical comparator 'strongest', yet it is CPU-only and s7 makes the GPU optional. | C6 GPU port (author-approved CUDA install) or g-sweep with 'strongest measured CPU' wording |
| R07 | referee | major | The knock-out 'smoothing failure mode' is presented as a contribution, but only two smoothers were tried, and the time-ordered OSS variant is known to be weak. | C5 stronger smoother; C2 wording follows result |
| R08 | referee | major | The frontier extrapolates fitted rates far outside the measured n window, uses a sigma_Q convention that differs from the decision's, and treats g as a hypothetical multiplier on ... | C1 intervals, extrapolation marked in F1; X2 canonical sigma convention |
| R09 | referee | major | D_max is the 10x-win definition rearranged, so 'one law explains all six failures' is true by construction and has no predictive content. | C1 reframed as budget identity adapted from Babbush et al.; content = measured inputs |
| R10 | referee | major | The six studies are not independent. | C5 reworded (three contracts, one toolchain); L5 harmonization; ERRATA E8 |
| R11 | referee | major | The novelty check comes too late and is scoped too narrowly to protect against desk rejection. | L1 widened (pre-2020, surveys, other domains) + fallback contribution fixed |
| R12 | referee | major | The frontier covers only per-call T-depth. | Q9 width, qubit-capped schedules, T-throughput in C6/F1 |
| R13 | referee | major | The oracle-correctness claim has no artifact. | Q4 payoff validation with bias bound; rotation/control listed as quantum-favourable exclusions |
| R14 | referee | major | G1a validates the scorer against a number produced by the same method, so it only checks the code for regressions. | Q1 labelled regression check; C3 gate uses emitted schedule (Q5) |
| R15 | referee | major | G5's method (explicit calls divided by sigma/e from the project's certified schedules) imports k from a different estimand. | L3 theorem-based k with explicit call accounting |
| R16 | referee | major | The published classical time for 4x12 is inflated about 2.6x by a fixed first-chunk overhead (worker compile-cache load), which the model spreads linearly over all points. | C2 timing model, run at n(eps); ERRATA E5 |
| R17 | referee | major | The schedule has several sequencing defects. | Sequencing fixed: L6 Day 4, mini-R0 Day 5, G11 Days 8-10, closure check Day 15, buffers |
| R18 | referee | major | The reviews are not independent in the sense a referee means. | External-model reviewers with author consent; model identity recorded; human review required |
| R19 | referee | major | The paper risks being read as a lab-notebook write-up of failed attempts. | Reframed around benchmark, D_max calculator and checklist; history to appendix |
| R20 | referee | major | G7's crossing-depth sweep is the right defence, but three gaps remain. | L6 oracle-family table with repetition-cost treatment; X1 crossing depths |
| R21 | referee | minor | The contract is set without sources, and C4 reports it at a single point. | L8 contract justification; report at break-even and 10x, 95/99/99.9% |
| R22 | referee | minor | C7 claims that no verified hardware development supplies a >=10^3 latency cut. | C7 reworded as dated selective screen (L7) |
| R23 | referee | minor | G6 mixes compiler generations and does not check the error side. | Q8 same-generation comparison + bias check at f=24 |
| R24 | referee | minor | G4's reference budget has not been checked. | C3 budgets pre-computed; numba OSS; pre-set tolerance |
| R25 | referee | minor | The plan never defines what t_layer means physically. | Q10 t_layer definition + Clifford-inclusive sensitivity |
| R26 | referee | minor | About 4 hours of author time is too little for an author who must take responsibility for every claim and answer referees. | Author time 10-12 h; VENUE.md records AI policy |
| R27 | referee | minor | A skimming reader or editor may read the working title 'a measured advantage frontier' as an advantage claim, which conflicts with the fixed negative verdict. | Retitled with the negative result in the title |
| R28 | referee | minor | The asset path for the five earlier studies is written as a brace glob that does not match the actual directory names. | Section 2 lists the five study directories explicitly |
| C01 | consistency | critical | The G1a hard gate cannot pass as written, and passing it would not validate what C3/C4 rely on. | Q1/Q2 as in F01 |
| C02 | consistency | major | C3 calls the oracle 'minimal' and says its depth is 'in the project's certified reversible IR'. | 'minimal'/'certified' removed; C3 bracket wording; ERRATA E3 |
| C03 | consistency | major | The numerical-correctness claim for the knock-out oracle has no archived script or artifact: 'bit-exact against the floating-point payoff, maximum error 2x10^-8, no knock-out misc... | Q4; 'bit-exact' wording removed; ERRATA E4 |
| C04 | consistency | major | The 4x12 classical time of 5.9 s behind '5,765x' is not a measured time to $0.001; | C4 wording 'modelled from measured per-point cost'; C2 timing; ERRATA E5 |
| C05 | consistency | critical | The archived decision grid contradicts C4's robustness clause. | C4 robustness reworded; X1; ERRATA E1/E2 (verified: 19 rows <=10x, one fit) |
| C06 | consistency | critical | The stop rule was written in advance, but the executed falsifier departed from the pre-registered protocol in DECISION.md §6 in at least eight ways. | PREREGISTRATION_DEVIATIONS.md; ground rule 2; C7/C8/C5/C6/Q5/L3 close arms |
| C07 | consistency | major | The miss range in C5 is wrong for the study it describes. | C5 corrected (priority-study misses 1.7-4.2e4 at 1 ns); ERRATA E8 |
| C08 | consistency | major | The repository holds two frontier artifacts that disagree by a factor of about 59, and the plan names neither nor picks one. | X2 canonical convention; ERRATA E6 |
| C09 | consistency | major | Both halves of the candidate-novelty sentence contradict the repository. | Candidate novelty rewritten ('strong, not exhaustive'; two complete compiled sources) |
| C10 | consistency | major | C7 is a universal negative ('No verified hardware development supplies the >=10^3 per-operation latency cut') with evidence level 'Literature'. | C7 reworded with baselines and dated screen |
| C11 | consistency | major | The '10^4 literature floor' is neither a floor nor a published figure for this oracle. | Relabelled 'hypothetical 9.5e3 oracle, not a floor'; L6 carries the argument |
| C12 | consistency | major | The repository cannot demonstrate the pre-registration. | Wording 'stated before the runs per the working record; not externally time-stamped'; ANALYSIS_SPEC committed before Week-1 runs |
| C13 | consistency | major | The fixed-decision block forbids tuning that would change the decision, but nothing forbids choices that preserve it. | Ground rule 1 symmetric; gates test execution-as-specified, not outcomes |
| C14 | consistency | major | None of the archived P1, P2 or P3 outputs was produced by the committed version of its script. | Q0 provenance replay; first replay executed 24 Sep (PROVENANCE_REPLAY_20260924.md) |
| C15 | consistency | major | The replay criterion cannot be tested as written. | Two-tier replay definition (exact vs re-measurement with tolerance) |
| C16 | consistency | major | 'Traced' has no defined mechanism, so the zero-untraced-numbers gate is either untestable or trivially met. | Numbers registry with keyed macros; tracer on bare digits |
| C17 | consistency | major | The plan makes human expert review weaker than the repository's own precedent. | Human expert review required pre-submission; SUBMISSION_READINESS states not submission-ready |
| C18 | consistency | major | The build tooling the plan calls 'in hand' cannot build this paper as it stands, and cannot run from a clean checkout. | Day 6 parameterized LaTeX build with pinned tools; no reliance on .context |
| C19 | consistency | major | G1b leaves out a prerequisite. | Q5 states leaf set; Q6 range certificate; like-with-like comparison |
| C20 | consistency | major | G4 is internally inconsistent and does not fit the compute budget. | C3 defined: two estimator-distinct constructions, pre-set targets, re-budgeted |
| C21 | consistency | major | The release and review steps drop parts of the repository's established release convention. | Day 14 release validation in precedent format (audit, pytest, ruff, receipt.json, FINAL_REVIEW) |
| C22 | consistency | minor | The headline goal and the Day-13 task use peer-review language ('passed ... | 'Internal AI-agent review (not peer review)' wording; R-D checks |
| C23 | consistency | minor | The archived data already show a borderline disagreement between two runs of the same knock-out estimator. | Risk raised to Medium; C3 resolves the P1/P3 gap |
| C24 | consistency | minor | G5 and G6 make two factual slips. | L3 wording (moment-conditional vs unconditional); Q8 no f=32 |
| C25 | consistency | minor | Several paths and references in the plan are imprecise. | Paths corrected; Day 1 defined relative to this commit on the branch |
| C26 | consistency | minor | The two forms in C1 are not equivalent in general. | C1 wording separates the identity from the plain-MC special case |
| C27 | consistency | minor | The proposition's parallel-copies term needs the oracle's logical qubit count, but no artifact records it for the knock-out oracle. | Q9 logical-qubit estimates for both cases |
| C28 | consistency | major | The G1b gate has no direction, so it passes whatever the result. | Q5 gate direction fixed |
| V01 | venue | critical | The only planned manuscript source is Markdown, rendered through Markdown 3.7 and headless Edge to HTML and PDF. | LaTeX + BibTeX canonical from Day 6; latexmk build receipt |
| V02 | venue | major | Venue choice is left to the author with no deadline, but the outline (Day 6), drafting (Days 8-9) and final build all depend on venue-specific structural requirements. | Venue decision gate Day 2 (author) with conformance checklist; superset structure fallback |
| V03 | venue | major | The plan has AI agents generate the whole manuscript text, the derivation, the figure code and the fixes. | L2 records AI-authorship policy; exclude incompatible venues unless authors rewrite |
| V04 | venue | major | The AI-use disclosure is a single Day-9 writing item with no provenance log. | AI_USE_LOG.md from Day 1; disclosure variants generated from it; R-D checks |
| V05 | venue | major | Every venue makes the human authors fully accountable for AI-generated content. | AUTHOR_VERIFICATION.md; >=10-12 author hours; not submission-ready until verified |
| V06 | venue | major | The arXiv and preprint route is missing. | arXiv account/endorsement/licence in section 8; L2 records preprint policies |
