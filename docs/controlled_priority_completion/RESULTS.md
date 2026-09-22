# Decision and completed priority investigation

22 September 2026. **No defensible significant quantum advantage established yet.**
This continuation stays with the controlled compound Asian-basket candidate.
It does not reopen the search for another specialization, reduce the tenfold
latency threshold, or replace the strongest preserved classical screen.

The investigation did produce substantial new results. The previous quantum
implementation was unnecessarily conservative in its estimator, multiplier
widths and scheduling. Those weaknesses have now been addressed and the
improvements composed. They change the resource estimates; they do not meet
the complete-price advantage objective.

## What changed

1. **Explicit estimators.** A finite-confidence Hadamard schedule based on the
   existing Kothari--O'Donnell construction reduces tight-moment controlled
   iterations by 1,280x for C4 and 2,119x for H8. Its tight digital moment remains
   conditional. A separately emitted shifted-selector QAE needs 7,864,305
   iterations and avoids that moment and the atan oracle entirely.
2. **Sound ranges and exact multiplication.** All four f40/q32 development
   financial graphs have no unresolved signed-overflow sites. Canonical
   expression matching binds these bounds to the optimized graphs. Specialized
   clean multipliers preserve the digital answer and reduce source T work by
   another 2.3684x/2.3894x relative to the prior truncated-multiplier source.
3. **Paid parallel execution.** Wave schedules allocate private scratch and pay
   repeated shared-control copies. Their source T-depth improvements are
   38.4312x/108.1126x against that same serial source, at 855,344/3,153,512 source
   logical qubits. Full emitted financial gates and inverses were executed and
   checked against exact integer targets. Combined selector and phase passes
   also clean up correctly.
4. **Joint arithmetic certificate.** Independently reviewed deterministic
   expectation bounds are $0.000099876/$0.000051936/$0.000011763/$0.000021978 for
   C4/C8/H4/H8. Together with the previously bounded q32 law/guard/control error,
   they fit the $0.002 numerical allocation. The baseline and residual must
   share exactly the same digital policy. This does not transfer old baseline,
   regret or tight-moment samples to that policy.

These are implementation and component-certificate results. They are not
evidence level 1 or 2 quantum-over-classical advantage.

## Complete logical work and the crossover

The following one-strike resources combine the range-specialized financial
source, wave schedule, estimator, inverse operations and actual synthesized
rotations. The classical screen charges the whole three-strike time against
one quantum strike, favoring quantum. It uses empirical RQMC confidence;
the separate fixed-iid C4 contract is considered in the capacity report.

| Estimator | Model | Logical T gates | Logical qubits | Scheduled time at hypothetical 1 ns/T layer | Required 10x time |
|---|---|---:|---:|---:|---:|
| Hadamard, conditional moment | C4 | 6.9976e14 | 879,289 | 19,399.5 s | 1.11059 s |
| Hadamard, conditional moment | H8 | 6.2381e15 | 3,182,449 | 58,849.2 s | 1.38472 s |
| QAE, unconditional digital support | C4 | 4.4738e15 | 857,599 | 91,501.7 s | 1.11059 s |
| QAE, unconditional digital support | H8 | 1.6432e16 | 3,160,759 | 120,669.1 s | 1.38472 s |

The first two schedules miss by approximately 17,468x/42,499x even in this
favorable T-layer sensitivity. Those times exclude positive Clifford, routing,
physical, baseline and setup costs. They are constructed scheduling results,
**not hardware predictions or lower bounds against every possible circuit**.
Parallelizing independent tests needs additional whole-source workspaces.

The necessary bare capacity screen now gives a more nuanced result than the
previous implementation: assigning every one of ten million physical qubits a
free one-T/ns lane gives conditional Hadamard arithmetic floors of 0.06997 and
0.62379 seconds. Both pass that necessary screen. A bare pass is not an
executable machine or a full-price advantage. At 17 physical qubits per lane,
the floors are 1.18946/10.60439 seconds. The current allocated memory also
exceeds the ten-million cap at distance 3.

For the explicitly stated 15-to-1 factory family, granting free data, routing,
lower-stage inputs and a one-ns code cycle still gives final-stage supply floors
of 431.774/3,849.392 seconds. C4 also fails the more generous 26.7837-second
budget derived from the fixed-iid classical contract. These bounds are
conditional on the fixed workload and primitive/factory models. Native gates,
different factories or different reversible storage are not ruled out by them.

The complete comparison must satisfy

    setup_Q/amortization + baseline + regret + quantum mean + physical I/O
        <= matched complete classical time / 10.

There is no validated positive full-price runtime to insert on the left. The
studied mapping fails before the unknown positive terms could rescue it.

## Why remaining certificates were not marked complete

The joint arithmetic proof cancels policy approximation error between two
expectations. It does not certify either expectation independently. A new
32-draw exact-digital C4 baseline screen measured 15.43 ms per sample. With its
proved range and the selected empirical-Bernstein inequality, even zero sample
variance would require more than 15.6 million samples for the allocated
$0.003/0.002 baseline contract: 2.79 serial days in that evaluator. The observed
32-sample variance suggests about 31 million, but is explicitly not a variance
certificate. These are method/evaluator-specific requirements, not universal
classical lower bounds.

A fixed same-policy regret experiment is specified, including independent
outer/future words, a clipped-Jensen estimator, deterministic bridge additions,
and a nonadaptive confidence test. It has not been run. Launching multi-day
certification of a candidate already failing the cost gate would not test
advantage. The confidence obligations therefore remain visibly open; no old
real-policy result is relabeled as new digital confirmation.

## Publication outcome

A separate [companion manuscript](../../manuscript/controlled-compound-2026-09-22/main.md)
and [PDF](../../manuscript/controlled-compound-2026-09-22/main.pdf) are prepared.
The plausible claim is an auditable feasibility/benchmark study. The targeted
prior-art check rejects broad novelty claims for controls, nested compounds,
Hadamard estimation, approximate-control bias or general resource accounting.
Whether the specific integration and certificates warrant journal publication
requires human review and editorial judgment.

Quantum Information Processing, Regular Article, is the recommended target
based on its verified scope, with both abstract lengths prepared because its
instructions conflict. The draft is not submission-ready: author identities,
declarations, human approval and a venue/fee decision are missing. No submission
or author attestation has been made. This publication route does not satisfy
the original advantage objective.

## Evidence map

- [Estimator derivation and schedules](ESTIMATOR_REDESIGN.md).
- [Full-support range proof](RANGE_AUDIT.md) and
  [joint arithmetic certificate](RANGE_JOINT_ARITHMETIC.md).
- [Remaining sampling requirements](RANGE_REMAINING_SAMPLING.md).
- [Capacity analysis for the new source](CAPACITY_RANGE.md).
- [Claim ledger](CLAIM_LEDGER.md), [checklist](CHECKLIST.md),
  [validation](VALIDATION.md), and [independent review](FINAL_REVIEW.md).

The scientifically justified stopping decision is to preserve and publish only
the scoped evidence. Reopening the advantage claim requires a concrete change
that passes the complete cost gate and then the outstanding price/physical
certificates; implementation improvements alone cannot be renamed advantage.
