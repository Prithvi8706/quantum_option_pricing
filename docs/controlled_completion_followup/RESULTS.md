# Controlled compound pricing: remaining-priority investigation

22 September 2026. **No defensible significant quantum advantage established yet.**
The same compound-pricing candidate has now been taken through an exact
arithmetic redesign, a partial financial error certificate, actual rotation
synthesis, conditional fault-tolerant accounting and independent review. The
redesign improves the circuit substantially but does not reopen the advantage
gate. Some financial and physical certification conditions remain unmet; they
are not marked complete merely because the investigation is being published.

This report supersedes the *status* of the earlier completion checklist. All
earlier results, protocols and source snapshots remain preserved. The original
September 22 manuscript is unchanged. No new advantage direction was searched,
no paid quantum computation was run, and no held-out advantage trial was opened.

## Decision and comparable workload

The contract remains one classical compound-call price on a conditional
arithmetic Asian-basket continuation, absolute error $0.01 and 99% per-price
confidence. A significant advantage requires at least 10 times lower complete
latency against the strongest eligible classical implementation. The inherited
10-million-physical-qubit and 60-second planning screens also remain unchanged.
These are engineering acceptance thresholds, not statistical significance tests.

The development cases remain C4/C8/H4/H8, with compound strikes 3/6/9. Full
coherent compilation still covers C4 and H8 at strike 6, two financial precisions
and 64 phase bits. Four-model financial error analysis does not turn two-model
compilation into an independently confirmed advantage region.

The existing controlled, vectorized classical RQMC prices cost 11.106 seconds
for C4 and 13.847 seconds for H8. Those timings include three strikes and are
charged in full to one quantum price, favoring the quantum screen. They are
empirical uncertainty results. The separate stronger fixed-iid C4 contract has
a recorded acquisition-plus-training cost of 267.84 seconds; imports and final
serialization are outside that timer, so it is not a fresh-process cold timing.
The same useful controls are available to both sides. See the independent
[classical comparator review](REVIEW_CLASSICAL.md).

## P3: bit-exact arithmetic redesign, failed cost gate

The old multiplier generated a full sign-extended product before copying the
required fixed-point slice. The new multiplier emits only the necessary
`w+f` low product bits and subtracts the two sign corrections. For unsigned
words A and B and sign bits a and b,

    signed(A)*signed(B)
      = A*B - a*B*2^w - b*A*2^w  (mod 2^(w+f)),  0 <= f <= w.

The omitted cross term is divisible by that modulus. Copying bits `f:f+w`
therefore gives exactly the same signed-floor result, including negative inputs
and modular overflow. The full computation is reversed to clean all workspace.
This is a standard arithmetic identity used to improve this compiler, not a
new quantum multiplication theorem.

Every new target graph equals its previous graph exactly. All signed operand
pairs were checked for widths 1 through 4 at every fractional width, followed
by production-width edge/random tests with nonzero outputs and inverse runs.
Five complete emitted source/phase basis executions and four fused
financial/phase executions passed. Independent gate-file hashes, wire checks
and hierarchy counts reconcile. Historical verification confirmed 895 earlier
artifacts and 25 snapshot files are unchanged.

| f=40 source | T-count reduction | Scheduled T-depth reduction | Optimistic source-only total at 1 ns/T layer | Total budget for a 10x win |
|---|---:|---:|---:|---:|
| C4 | 1.906x | 1.731x | 97.268 s | 1.111 s |
| H8 | 1.909x | 1.735x | 838.033 s | 1.385 s |

The optimistic column grants the tight continuous-model moment for free, only
`ceil(sqrt(moment)/error)` clean source calls with constant one, no confidence
overhead, free setup and free surrogate/regret handling. It is a favorable
sensitivity calculation, **not an algorithm, universal lower bound, or hardware
prediction**. Even its C4 result misses the stronger fixed-iid 26.784-second
tenfold budget. The compiled leaf schedule is an upper schedule for this
implementation, not a claim that all possible quantum circuits need this depth.

The actual conservative mean-estimation schedule is far more expensive:

| f=40, conditional tight moment | Controlled-U calls | Arithmetic T count | Arithmetic seconds at hypothetical 100 ns/T layer |
|---|---:|---:|---:|
| C4 | 1,540,372,419 | 2.094708e18 | 6.941448e10 |
| H8 | 6,287,324,746 | 3.146744e19 | 1.040038e12 |

Its 10x break-even requirements are approximately 1.60e-18 / 1.33e-19 seconds
per scheduled T layer, or 1.89e18 / 2.27e19 magic states per second, before
additional costs. No supplied hardware evidence supports those assumptions.
The rigorous digital-support moment schedule is separately recorded and worse.
Improving variance, rotations or the multiplier alone cannot justify a claim
that this constructed estimator achieves the requested advantage.

## P4: probability-law bridge closed; full price certificate remains open

The new [financial derivation](FINANCIAL_BRIDGE.md) bounds the singular
Box--Muller midpoint cell, the remaining quantization error, lognormal clipping,
the reset at the exercise time, and the Gaussian analytic control's mismatch
with the finite input law. Deterministic 70-digit interval calculations bound
their combined price effect below $0.000029 for every development model at
32 random bits per uniform. This is an expectation bound, not a sampled maximum.

The control identity is not exactly preserved by the finite law. A reachable
guarded state supplies a counterexample, while the small expected control bias
is paid explicitly. Baseline and residual are analyzed jointly, so cancellation
does not require an unjustified assumption that every exercise decision is
stable under rounding.

A second counterexample refutes a uniform $0.002 arithmetic bound for the
low-precision f=24 source: H8's baseline error exceeds $0.0051738 on one
certified reachable input. Its rarity means this does not refute a $0.002
*expected* error. The f=40 diagnostics remain small but do not prove a global
arithmetic error or range bound.

Still required for a full continuous-model price: an f=40 joint arithmetic
certificate, surrogate-mean accuracy, the implemented finite policy's regret
certificate and, if used, transfer of the tight second moment. H8's existing
continuous regret upper bounds already miss their $0.003 allocation. The
rigorous replacement moment is the much looser bounded-output value B squared.
The new law bound therefore strengthens the evidence without completing P4.

## P5: rotations synthesized; physical execution remains conditional

All 95 distinct rotation magnitudes are now synthesized or certified as identity
within the strictest common operator tolerance, 2.6263e-18. Independent interval
matrix multiplication certifies the actual gate strings; separate high-precision
checks verify both signs and the controlled-phase convention. Total multiplicities
are reconciled exactly. Eight tiny angles use identity;
the other 87 need 366 to 376 T gates each.

Synthesis adds only about 0.00485% / 0.00132% to C4/H8 arithmetic T counts. It
does not explain, or repair, the failed feasibility screen. The new
[fault-tolerance report](FT_SYNTHESIS_AND_MODEL.md) charges Clifford operations,
code distance selected from whole-machine exposure, factories, finite retry
caps, routing sensitivities, measurements and feedback. It covers 32 conditional
model/precision/moment/noise/routing scenarios and records every assumption.

These deliberately serial physical schedules are conditional upper bounds,
not measured runtimes or lower bounds against better designs. The noise fit,
layout capacity, routing and decoder throughput are not validated hardware.
Unknown full-price costs remain null rather than being silently assigned zero.
No completed fault-tolerant price or level-2 advantage follows.

## P6: claim review instead of an invalid advantage confirmation

The computational gate still fails and the complete financial contract is not
certified. An advantage confirmation campaign would not be interpretable, so
the proposed 24-case campaign was not run or represented as passed. Its future
cases have not been opened or retrospectively selected from these diagnostics.

The supported research contribution is an auditable feasibility case study:
strong controls make classical compound pricing inexpensive, while a concrete
variance-sensitive coherent estimator retains a prohibitive source cost under
the evaluated schedules. The finite-law control correction and explicit
failure cases are useful technical evidence. Combining known components and
finding a failed crossover does not by itself establish algorithmic novelty.

A potential paper must distinguish this contract from the existing manuscript's
ideal-logical implementation comparison. The new evidence may support a
carefully scoped benchmark/methodology paper or companion study, subject to
novelty and editorial review. It does not support an advantage paper or a promise
of journal acceptance. See the [claim ledger](CLAIM_LEDGER.md),
[baseline review](REVIEW_BASELINE.md) and [final review](FINAL_REVIEW.md).

## Reproducibility and remaining work

The [reproduction guide](../../research/controlled_completion_followup/README.md)
lists the code, dependencies, immutable artifacts and checks. The
[current checklist](CHECKLIST.md) separates completed work from unmet scientific
conditions. The single consequential next research action, if this same
candidate is pursued further, is a new explicit source/estimator cost proposal
that passes the declared budget **before** another large financial sweep.
This investigation found no evidence that the current implementation can do so.
