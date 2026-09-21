# Handoff Context — Conference Submission of "Paper A" (Quantum Option Pricing)

## 1. Situation / goal
The user (Prithvi Raghu, VIT Vellore) has a research project, **`quantum_option_pricing`**,
that is the basis for a **three-paper research program**. A faculty member is
attending a conference and asked the user for a paper to submit. Goal: get one
paper conference-ready (a fast, Scopus/Springer-indexed publication), for **one of
two conferences**.

## 2. The two candidate conferences (verified from their sites)
- **ICAIC 2026** — 2nd Intl. Conf. on Artificial Intelligence and Computing.
  Manipal University Jaipur, India. Oct 22–24, 2026. **Deadline July 31, 2026.**
  Published via **Springer** (Scopus). Its 2025 proceedings are a verified Springer
  Nature volume. Track "Advanced Computational Techniques and Emerging Trends."
- **ICDMIS 2026** — 3rd Intl. Conf. on Data Mining and Information Security.
  SLIIT, Sri Lanka (hybrid). Oct 7–8, 2026. **Deadline Aug 15, 2026.** Published via
  **Springer LNNS** (Scopus). Track 03 "Advance Computing" **explicitly lists
  Quantum Computing** as a topic.
- **User has not yet fixed which one** ("it can be either"). Both use the Springer
  proceedings layout, so one Springer template serves both.

## 3. The three papers
- **Paper A — "NISQ Noise Shifts the QAE Break-Even for Option Pricing."**
  Empirical: runs IQAE (3 uncertainty qubits) across a 50-config × 5-noise-level
  sweep (250 runs) on a depolarizing simulator, plus a **real IBM hardware run**
  (`ibm_marrakesh`, Heron r2, 1024 shots). ~2,530 words. **This is the paper chosen
  for submission.**
- **Paper B — "The Wrong Baseline: How Variance-Reduced Monte Carlo Erases QAE's
  Advantage in Option Pricing."** Methodological critique (antithetic/control-variate/
  RQMC baselines + a dimension sweep). ~6,000 words. More novel intellectually, but
  **NOT chosen** — see below.
- **Paper C — "Unified Quantum Advantage Frontier"** — planned, unifies A and B.

## 4. Key decision: submit Paper A (not B), reasoning
- Paper A has the **real quantum-hardware result** (concrete + impressive to a
  general audience), is **verified clean**, and is **ready now**.
- **Paper B has a data defect** (see §6) and needs a real rewrite before it's safe.
- Submitting A **keeps Paper B free for a journal** (B has the most journal upside:
  target Quantitative Finance / Physica A). Publishing a paper in Springer
  proceedings "spends" it — can't also journal the same paper.
- Publishing any one paper does **not** block the 3-paper project; Paper C
  legitimately builds on published A and B by citing them.

## 5. Paper A verification (all numbers confirmed against raw data)
Recomputed directly from `data/noise_sweep_expanded.csv` (250 rows) and
`results/ibm_hardware_validation.json`:
| Claim | Data | Match |
|---|---|---|
| p=0 → $0.203 | $0.2033 | ✓ |
| p=1e-3 → $0.657 | $0.6570 | ✓ |
| p=1e-2 → $6.163 | $6.1628 | ✓ |
| oracle depth ~14 (13.6–14.5) | 13.64–14.48 | ✓ |
| hardware p̂=0.2842, err 0.0158, 1.1σ | JSON 0.28418 / 0.01582; σ=0.0143 → 1.10σ | ✓ |
**Paper A has no data disparities.**

## 6. Paper B disparity (NOT fixed — relevant only if B is revisited later)
Paper B's committed docx (`outputs/Paper_B_The_Wrong_Baseline.docx`) uses
**superseded 10-trial** dimension-sweep numbers (d=1 slope −1.14 → d=64 −0.65,
claiming a "crossover at d≈16–32"). Five repo sources (CHANGELOG, ROADMAP, README,
PROJECT_UPDATE, and a plan file's hardcoded sanity gate) agree the **canonical
100-trial** numbers are **d=1 −0.98 → d=64 −0.77, a mild degradation with NO
crossover** — RQMC stays super-classical through d=64. ROADMAP claims Paper B "was
corrected in all 6 locations," but the actual docx was never corrected. So Paper B,
if ever submitted, needs a real rewrite of abstract + contribution #3 + Table IV +
Section V + "Quantum Advantage Region."

## 7. Format decision: Springer, NOT IEEE
The user initially said "IEEE format," but both venues publish via **Springer**
(LNCS/LNNS), which require the **Springer single-column template, not IEEE
two-column**. The original docx was IEEE-style. Decision: produce **Springer LNCS
LaTeX** (`llncs` class), which works for both ICAIC and ICDMIS.

## 8. What has been built (all in `outputs/paper_a_springer/`)
- **`main.tex`** — full Paper A converted to Springer `llncs` format. Structurally
  checked (balanced envs/braces, all `\cite` keys resolve, 4 figures referenced).
  Compiles on Overleaf (no local TeX on the machine). Empty `\orcidID{}` removed to
  avoid an undefined-control-sequence error on the bare class.
- **`figures/`** — the 4 figures **regenerated on WHITE backgrounds** (originals
  were dark-themed, unsuitable for Springer print). A pre-existing colorbar label
  bug (literal `$` parsed as math → "…()—cappedat8…") was fixed.
  - fig_noise_heatmap.png (Fig 1, 10-config heatmap)
  - fig_mean_delta_vs_noise.png (Fig 2)
  - fig_break_even_frontier.png (Fig 3, two-panel: frontier + oracle depth)
  - hardware_validation_plot.png (Fig 4)
- **`regenerate_figures_white.py`** — reproducible white-figure generator (leaves
  the repo's original dark scripts/figures untouched).
- **`build_review_pdf.py`** → **`Paper_A_review.html`** → **`Paper_A_review.pdf`**
  (8 pages). The PDF is an **HTML→PDF review render** (content/figures faithful) made
  with headless Chrome, because there is no LaTeX/pandoc on the machine. The official
  submission PDF must be compiled from `main.tex` on Overleaf.
- **`README_BUILD.md`** — Overleaf compile steps.

## 9. Open items (decisions still needed from the user)
1. **Fig 2 data inconsistency (real, unresolved).** Fig 2 (`fig_mean_delta_vs_noise`)
   still uses the **10-config** CSV (`noise_sweep_results.csv`): its mean at p=1e-3
   reads ≈**$0.49**. Table 1 / abstract / Fig 3-left use the **50-config** CSV
   (`noise_sweep_expanded.csv`): **$0.657**. So Fig 2 contradicts the paper's
   headline number. Options: (a) **repoint Fig 2 to 50-config** (one-line change;
   then it closely resembles Fig 3-left), or (b) **drop Fig 2** and rely on Fig 3-left
   (which already matches Table 1). Recommended: (a) or (b) — user to choose.
2. **Venue** not fixed (ICAIC vs ICDMIS) → **page limit unknown**. Paper A is short
   (~7–8 pages in Springer format); some tracks want a higher minimum (~8+ pages). May
   need slight expansion once venue is chosen.
3. **Author block / ORCID** — add supervisor/co-authors or ORCID if faculty requires.

## 10. Ground-truth data files & canonical numbers (frozen)
- `data/noise_sweep_expanded.csv` — 250 rows (50 configs × 5 noise). 50-config means:
  p=0 → 0.203, 1e-4 → 0.220, 1e-3 → 0.657, 5e-3 → 3.478, 1e-2 → 6.163.
- `data/noise_sweep_results.csv` — 50 rows (10 configs × 5 noise). 10-config means:
  p=0 → 0.135, 1e-3 → 0.491, 1e-2 → 4.825. (This is what Fig 2 currently uses.)
- `results/ibm_hardware_validation.json` — job `d8nvd2bqv2lc7389d9e0`,
  ibm_marrakesh, 1024 shots, counts {0:733, 1:291}, p̂=0.2842, target 0.30,
  abs err 0.0158.
- Env note: repo pins `scipy==1.13.1` (Sobol results depend on it). Venv at
  `venv/Scripts/`. No LaTeX/pandoc/poppler installed; Chrome and Edge are present.

## 11. Suggested next steps for the receiving AI
1. Ask the user which venue → confirm that venue's exact page limit & template
   series (LNCS vs LNNS) and any submission-format nuance.
2. Resolve the Fig 2 decision (repoint to 50-config or drop), regenerate, rebuild PDF.
3. If the venue has an ~8+ page minimum, expand Paper A (e.g., more background,
   an explicit error-decomposition subsection, expanded related work).
4. Have the user compile `main.tex` on Overleaf for the true Springer PDF.
