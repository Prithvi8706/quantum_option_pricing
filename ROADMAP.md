# Quantum Option Pricing — Research Roadmap
> **Repo:** github.com/Prithvi8706/quantum_option_pricing
> **Live dashboard:** web-production-559db.up.railway.app
> **Author:** Prithvi Raghu, VIT Vellore
> **Last updated:** June 2026
> **Status:** Papers A and B submission-ready. Paper C planned.

---

## What this project is

A deployed Dash dashboard that prices European call options three ways side by side — Black-Scholes (exact), Monte Carlo (animated convergence), and Quantum Amplitude Estimation (QAE, 600-point precomputed grid). The defining trait of this project is **honest empiricism**: it openly shows that QAE does not beat Monte Carlo on today's hardware, and shows exactly where it theoretically would. Most quantum finance papers hide this. This one doesn't. That framing is the backbone of the entire 3-paper program and must be preserved in all future work.

---

## Current state (June 2026)

- Dashboard live on Railway, code health 10/10 (pytest / mypy / ruff all clean)
- Break-even visualizer shipped, grounded in Woerner & Egger (2019) and Stamatopoulos et al. (2020)
- 600-point QAE grid precomputed in `qae_grid.pkl`
- Paper A — written, IEEE two-column format, **submission-ready**
- Paper B — written, corrected, IEEE two-column format, **submission-ready**
- Paper C — planned, no fabricated data, not started

---

## Frozen canonical numbers

These are verified and locked. Do not update without a full re-run and audit.

| Number | Value | Source |
|---|---|---|
| Paper A: mean price error at p=0 (ideal sim) | $0.203 (~20x above epsilon=0.01 target) | recomputed from data (0.2033) |
| Paper A: mean price error at p=1e-3 | $0.657 | recomputed from data (0.6570) |
| Paper A: oracle query depth | ~14 queries (13.6-14.5, noise-invariant) | recomputed |
| Hardware result: p-hat | 0.2842 (1.1 sigma from theory 0.30) | ibm_marrakesh job d8nvd2bqv2lc7389d9e0 |
| Hardware: shots | 1024 | ibm_marrakesh |
| Hardware: job ID | d8nvd2bqv2lc7389d9e0 | ibm_marrakesh |
| Paper B: European call RQMC slope | -1.04 | Paper B Table III |
| Paper B: RQMC slope at d=1 | -0.98 [-1.06, -0.90] | 100-trial stability sweep |
| Paper B: RQMC slope at d=64 | -0.77 (advantage persists through d=64) | 100-trial stability sweep |
| QAE grid bias at n=5 | 2.16e-02 | PROJECT_UPDATE_2026-06-10.md |

**Important:** The earlier d=1 slope of -1.14 and d=64 slope of -0.65 from the 10-trial sweep were finite-trial artifacts. The 100-trial stability sweep is the correct source. Paper B has been corrected in all 6 locations. Do not use the old values.

---

## Environment

| Environment | Purpose | Key packages |
|---|---|---|
| Paper A/B venv | Simulation, experiments | qiskit==0.45.3, qiskit-finance==0.4.0, qiskit-algorithms==0.3.1, qiskit-aer==0.12.2 |
| Anaconda | IBM hardware runtime only | qiskit-ibm-runtime==0.47.0, qiskit==2.4.2 |

**Critical:** Do NOT merge the two environments. scipy pinned at 1.13.1 in the venv — upgrading breaks Sobol reproducibility.
**IBM backends available:** ibm_kingston, ibm_fez, ibm_marrakesh (all 156-qubit Heron r2). ibm_brisbane is retired.
**IBM credentials:** `.env` in project root, gitignored. Uses `channel="ibm_cloud"`.

---

## The 3-paper program

### Paper A — *NISQ Noise Shifts the QAE Break-Even for Option Pricing*

**Status:** Submission-ready (IEEE two-column DOCX, 4 figures embedded, 8 references)
**Venue target:** EPJ Quantum Technology / arXiv
**Core claim:** Even at p=0 (ideal simulation), QAE already misses the epsilon=0.01 precision target by 20x ($0.203 mean error). With realistic depolarizing noise (p=1e-3), error rises to $0.657. The break-even point shifts substantially with noise — this gap in the existing literature is the paper's contribution.
**Key finding:** Oracle query depth is noise-invariant (~14 queries at all noise levels). Clean standalone publishable insight.
**Hardware validation:** ibm_marrakesh, 1024 shots, p-hat=0.2842, 1.1 sigma from theory. Job ID locked.

**Remaining before arXiv:**
- [ ] Final author proofread
- [ ] arXiv account + endorsement (first submission requires endorser — plan for this)
- [ ] Submit

---

### Paper B — *The Wrong Baseline: Variance-Reduced MC vs QAE in Option Pricing*

**Status:** Submission-ready (IEEE two-column DOCX, figures embedded, 6 corrections applied)
**Venue target:** Quantitative Finance / Physica A / arXiv
**Core claim:** Every prior QAE break-even calculation uses naive Monte Carlo as the classical baseline. Quants don't use naive MC — they use variance-reduced methods. With RQMC (scrambled Sobol), the classical convergence slope reaches -1.04 for European calls, matching QAE's theoretical O(1/N) asymptotically. This eliminates QAE's claimed advantage on the European benchmark.
**Key finding:** RQMC advantage degrades with dimension — slope goes from -0.98 at d=1 to -0.77 at d=64. Advantage persists through d=64 (stronger than originally thought), making multi-asset pricing the real opportunity for quantum.

**Remaining before arXiv:**
- [ ] Final author proofread
- [ ] Submit (can follow Paper A by ~1-2 weeks)

---

### Paper C — *Unified Quantum Advantage Frontier for Option Pricing* `[planned]`

**Status:** Not started. No fabricated data. Shown in portfolio with PROJECTED watermark.
**Venue target:** Quantum journal
**Core claim:** A unified figure showing the quantum advantage region as a function of (epsilon, noise rate p, MC variance reduction factor VRF). Under joint realistic assumptions — variance-reduced MC and NISQ noise — quantum advantage in European call pricing requires conditions more stringent than commonly assumed. Multi-dimensional Asian options are the better near-term target.
**Opening figure:** The dimension-decay figure from Paper B (d=1 to d=64 RQMC slope sweep) serves as the entry point.
**Novel contribution:** The honest, unified framework the field has been missing.

**Prerequisites before starting:**
- Papers A and B on arXiv (gives Paper C its foundation)
- ~2-3 months of focused work after A and B are out

---

## Timeline

| Milestone | Target |
|---|---|
| Paper A arXiv preprint | July 2026 |
| Paper B arXiv preprint | July-August 2026 |
| Paper C start | September 2026 |
| Paper C draft | November-December 2026 |
| Paper C submission | Early 2027 |

**Honest caveat:** This assumes steady progress. Exams, DRDO report, FQCNN, and Entangled Equilibria will eat weeks. The checkpoint structure means a slow month only delays one paper, not the whole program. The arXiv preprint for A alone is already a strong outcome — everything after is compounding.

---

## Immediate next actions (in order)

1. **Final proofread Paper A** — one pass, author's eyes only
2. **Submit Paper A to arXiv** — set up account + find endorser if needed
3. **Final proofread Paper B** — one pass
4. **Submit Paper B to arXiv** — ~1-2 weeks after A
5. **Start Paper C** — only after A and B are live

---

## Files

| File | Location | Status |
|---|---|---|
| Paper_A_NISQ_Noise_QAE.docx | repo outputs/ | Submission-ready |
| Paper_B_The_Wrong_Baseline.docx | repo outputs/ | Submission-ready |
| qae_grid.pkl | repo data/ | Locked, do not regenerate |
| ibm_hardware_validation.json | repo results/ | Hardware validation point — Paper A (job d8nvd2bqv2lc7389d9e0) |
| noise_sweep_*.pkl / .csv | repo data/ | Noise/dimension sweep data for Papers A and B |
| .env | repo root | Gitignored — IBM credentials |

---

## References (locked)

1. Woerner & Egger (2019) — Quantum risk analysis. npj Quantum Information.
2. Stamatopoulos et al. (2020) — Option pricing using quantum computers. Quantum.
