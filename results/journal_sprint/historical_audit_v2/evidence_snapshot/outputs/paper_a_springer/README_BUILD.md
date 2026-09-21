# Paper A — Springer LNCS build

Conference-ready (Springer template) version of **Paper A: "NISQ Noise Shifts the
Quantum Amplitude Estimation Break-Even for Option Pricing."** Works for either
ICAIC (Springer) or ICDMIS (Springer LNNS) — both use this same Springer layout.

## Files
- `main.tex` — the paper in Springer `llncs` class
- `figures/` — the 4 figures referenced (Fig. 1–4)

## Compile (Overleaf — easiest)
1. Go to overleaf.com → **New Project → Upload Project**.
2. Zip this whole `paper_a_springer/` folder and upload it (or upload
   `main.tex` and the `figures/` folder into a blank project).
3. Overleaf has the `llncs` class built in — no need to add `llncs.cls`.
4. Menu → **Compiler: pdfLaTeX** → **Recompile**. PDF appears on the right.

## Compile (local, if you install MiKTeX/TeX Live)
```
pdflatex main.tex
pdflatex main.tex   # run twice so \ref cross-references resolve
```

## What's verified
- Every number in the text and Table 1 was recomputed from the repo data
  (`data/noise_sweep_expanded.csv`, `results/ibm_hardware_validation.json`):
  p=0 → $0.203, p=1e-3 → $0.657, p=1e-2 → $6.163; oracle depth 13.6–14.5;
  hardware p̂=0.2842 (1.1σ). All match.
- Structure checked: balanced environments/braces, all `\cite` keys defined,
  4 figures all referenced in text.

## Still to do before you submit (see chat)
1. **Confirm page limit** for your chosen venue and, if there's a minimum
   (~8 pages is common), we may expand slightly — this paper is on the shorter
   side (~7 pages).
2. **Figures are dark-themed (black background).** Springer print proceedings
   expect white backgrounds. Recommended: regenerate the 4 figures white before
   camera-ready. (The plots come from `src/noise_experiments.py` /
   `plot_*` scripts + `plot_hardware_validation.py`.)
3. **Add ORCID** if you have one (`\author{Prithvi Raghu\orcidID{0000-...}}` —
   only on the Overleaf Springer template, which defines `\orcidID`).
4. **Author block**: currently "Vellore Institute of Technology, Vellore, India."
   Add department/co-authors/supervisor if required by your faculty.
