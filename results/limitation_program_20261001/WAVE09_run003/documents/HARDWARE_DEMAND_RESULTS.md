# Whole-estimator logical demand and physical requirements

The source-compatible, synthesized15-shot price schedule now has independently reconciled logical demand. This fixes the accounting interface for H17/H18; physical execution remains unproved.

| Case | Consumed T states | Elementary logical gates | Native CCX positions | Maximum simultaneous native private qubits |
|---|---:|---:|---:|---:|
| B4x12 | 511,911,060,861,915 | 1,182,602,002,711,185 | 73,130,151,300,300 | 195,017 |
| B8x52 | 4,195,204,814,583,315 | 9,691,531,767,803,025 | 599,314,973,260,500 | 1,516,959 |

Counts include literal forward/inverse financial arrays, argument-copy fanout, both selector directions, signed reflections and markers, fresh uniform/QPE preparations and all terminal IQFT tokens. Native CCX uses the audited exact seven-T decomposition. SWAP expands to three CX. The terminal IQFT is counted once. Forty-three final fixtures pass; the first38-fixture attempt's schema failure is preserved with zero demand ledgers emitted. [Demand receipt](../../results/limitation_program_20261001/H17_demand_run002/summary.json), [independent audit](../../results/limitation_program_20261001/H17_demand_audit_run001/summary.json).

The declared physical failure allowance0.003 is split equally between data, T-state and control faults. The required marginal error per consumed T state is at most `1/(1000*N_T)`: approximately1.95e-18 for B4 and2.38e-19 for B8. Necessary per-elementary-operation data/control targets are approximately8.46e-19 and1.03e-19. The union accounting does not assume independent faults. Failing such a sufficient bound would not establish the actual failure probability.

These targets exclude uncounted idle code cycles, reset/readout feedback and physical routing opportunities. Code distance, protected storage and factory footprint, accepted-state delivery/retry rate, operation clocks and executable latency remain null. No physical architecture was admitted. The compiler's logical-qubit limits are not physical-qubit caps; the archived C4/H8 capacity and clock grid do not transfer to these B4/B8 cases. A parameterized maximum of reaction, supply and routing terms is a conditional lower bound and cannot establish an achievable runtime. G5 remains open.


The bounded [two-method factory screen](FACTORY_SUPPLY.md) and independent finite-error arithmetic audit are complete. Published compatible output quality remains conditional on its model; no physical factory mapping, rate, footprint, clock or runtime was admitted. The [onefold/tenfold ledger](RUNTIME_FRONTIERS.md) keeps actual runtime ratios null and lists necessary supply thresholds separately.
