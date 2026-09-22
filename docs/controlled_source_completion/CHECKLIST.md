# Completion checklist

22 September 2026. The first two priorities were declared in
[PROTOCOL.md](PROTOCOL.md) before their validation runs. Both have now been
executed. “Complete” below refers to the specified implementation check, not
to achieving quantum advantage or certifying the original continuous price.

| Priority | Work and completion condition | Status / evidence |
|---|---|---|
| P1 | Independently validate the source, cleanup and estimator conventions | **Complete.** All four financial models checked at two precisions on 64 paired inputs each; full emitted-gate execution of C4 and H8 at both precisions, before and after optimization; 3 full phase-circuit runs; 4 combined financial/phase cleanup-fusion runs; 36 finite spectral cases; actual 9-qubit QPE statevector; exact controller and leaf tests. Raw results in `validation_v1`, `validation_v2`, `validation_v3`, `diagnostic_v1`. |
| P2 | Reconcile the complete logical source/estimator cost and precision obligations | **Complete as an audit.** Independent gate-file counts and hashes, source/inverse/control/QFT/repetition/output accounting, fixed error/failure allocations, 64-bit phase coefficient/range bound, explicit unsynthesized-rotation costs and physical unknowns. The feasibility gate **fails**. Audit completion is not completion of synthesis or a full financial certificate. |
| P3 | Reduce the coherent cost enough to reopen the same candidate | **Not achieved.** Require an emitted source plus estimator with a credible total budget below 1.111 s for C4 and 1.385 s for H8, then recheck stronger classical alternatives. Current complete-source cost fails even an ideal unit-constant query screen. Small variance or gate-count improvements alone do not meet this condition. Do not run a bigger financial sweep to evade this gate. |
| P4 | Certify the continuous financial output for the implemented source | **Open.** Bound midpoint-Gaussian/clipping bias, signed arithmetic/approximation/overflow effects, the conditional-control identity under the finite law, policy-boundary effects, surrogate mean and regret. Transfer or replace the tight moment certificate. H8's existing regret certificate also fails its budget. A small paired diagnostic is insufficient. |
| P5 | Finish fault-tolerant execution and the comparable full-price budget | **Open, gated by P3.** Synthesize the remaining rotations at their recorded tolerance; allocate code distance, routing, factories, failure probabilities, measurement and feedback; include policy training, certificate acquisition, surrogate pricing, decoding and all outputs. Current hypothetical T-layer timings are not hardware predictions. |
| P6 | Confirm advantage and prepare a supported paper claim | **Not started.** Only after P3-P5 pass: frozen parameter region, stronger eligible classical tuning, matched uncertainty, held-out 24-case protocol and robustness thresholds. For a feasibility/benchmark paper instead, conduct an independent novelty and technical review before changing the manuscript's framing. No advantage or acceptance claim is currently supportable. |

The recommended stopping point for this implementation is now reached: retain
the tested source, derivation and reproducibility package; do not spend on a
large confirmation campaign or physical deployment. The advantage objective
remains unmet. P3 is the next technical gate if this same direction is pursued
further; P4-P6 are not hidden completed work.
