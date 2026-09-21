# Calibration-first encoding decision: frozen local check

Declared 2026-09-15 before new stochastic observations. This is a new-method
development check on six previously studied contracts, not external preregistration
or confirmation on unseen contracts. Do not retune after outcomes.

- Fixed two-representation menu: existing linearized and exact_table at n=6.
  Import unchanged circuit profiles/bounds from rescue_encoding_v2 after checking
  their archive hashes. Statevector amplitudes are simulator inputs ONLY: the
  selector receives sensitivity, offset, bias, cost, calibration and budgets.
- Contracts E001, E014, E025, E030, E038, E049; 30 repetitions each;
  guard 0, .003, .03; objective shots and logical CX; 1080 trial identities.
- Dollar tolerance 1. Stationary synthetic readout f=.02, g=.07. Supplied guards
  are uncertainty allowances, not sampled or demonstrated hardware drift.
- Each encoding independently acquires 16384 zero and 16384 one calibration
  shots. Charge all 65536 calibration shots even on refusal. Across-menu CP
  noncoverage .025, shared equally over four coordinate intervals.
- Midpoint calibration estimator, uniform Hoeffding radius, validation alpha .025.
  Select the least-cost certifiable encoder before any pricing observations;
  tie by name. Fixed pricing sample size selected from calibration only.
- Shots objective: each candidate cap 32768, per-shot cost 1, calibration cost 1.
  Logical-CX objective: each cap floor(32768*old_k0_CX/candidate_k0_CX),
  per-shot cost candidate CX, calibration CX cost 0 (single-qubit calibration).
  Always retain separate total-shot accounting. No routing, setup, wall-clock,
  state-preparation compilation or error-correction cost claim.
- Fresh RNG namespace encoding_decision_v1; separate keys for contract, guard,
  objective, repetition, encoding and calibration/validation purpose.
  No pricing observations for rejected encoders. No reused rescue/pilot paths.
- Save all decisions, candidate scores, calibration counts, selected terminal
  count/interval, target containment and midpoint error. Truth is only used by
  the experiment evaluator, never the decision function.
- Report all cells, refusal reasons, observed misses/errors and cost. No required
  positive-result threshold. Refusal is failure of a sufficient certificate,
  not a lower bound or evidence of fundamental impossibility.
- Per-trial unconditional erroneous-declaration bound .05 under assumptions;
  not conditional-on-declaration coverage, nor simultaneous across all trials.
- Archive exclusive output, source/protocol/input snapshots and SHA256 inventory.
  Verify deterministic replay; unit-check endpoint propagation and selection.

This k=0 rule has ordinary sampling scaling, not amplitude-estimation speedup.
Closed-form pricing / 64-term classical summation remain the baseline to beat.
