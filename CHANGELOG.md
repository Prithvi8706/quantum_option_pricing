# Changelog

All notable changes to this project are documented here.

## 2026-06 — Papers A & B complete

### Added
- IBM Quantum hardware validation: a single-qubit state-preparation primitive
  (Rᵧ(2·arcsin√0.3), encoding p = 0.30) run on `ibm_marrakesh` at 1024 shots.
  Empirical p̂ = 0.2842, within 1.1σ of the target — no detectable device error
  beyond shot noise. See `results/ibm_hardware_validation.json` and
  `ibm_validation.py`.
- Hardware validation figure (`src/plot_hardware_validation.py`).

### Changed
- README rebuilt from verified canonical numbers. Paper A marked complete
  (hardware run done). Paper B dimension-sweep slopes corrected to the
  100-trial stabilized values (d=1 −0.98, d=64 −0.77), framed as a mild
  degradation persisting through d=64 rather than a crossover.
