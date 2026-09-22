# Capacity after exact range-specialized multiplication

22 September 2026. The new exact source materially changes the weakest capacity
screen: **both tight-moment Hadamard rows now pass the bare work test**. Neither
row establishes a physical crossover. The stated encoded-lane and factory
models still miss the latency budget, and the current allocated mapping exceeds
the physical-qubit cap. These statements concern these implementations and
explicit hardware premises; they are not an impossibility theorem for the
pricing problem.

The source substitution keeps the f40/q32 output law and estimator schedules.
It replaces the financial forward/inverse work by the range-specialized emitted
source, while retaining the phase or selector work and controlled reflection.
One forward plus one inverse equals one clean-source T count; it is not charged
as two clean sources. Both source manifests and estimator artifacts are bound by
SHA-256 in [capacity_range.json](../../results/controlled_priority_completion/capacity_range.json).
The separate range proof and full emitted-basis replay are obligations of this
source substitution. The numerical screen grants synthesis, data storage and
all unrelated computation for free unless explicitly restored below.

| Estimator | Model | Arithmetic T count | Bare 1 ns/T/physical-qubit floor | 10x RQMC budget | Bare screen |
|---|---|---:|---:|---:|---|
| Conditional tight-moment Hadamard | C4 | 699,682,731,183,520 | 0.069968 s | 1.110592 s | Pass |
| Conditional tight-moment Hadamard | H8 | 6,237,873,213,395,880 | 0.623787 s | 1.384721 s | Pass |
| Unconditional digital shifted QAE | C4 | 4,473,763,504,856,070 | 0.447376 s | 1.110592 s | Pass |
| Unconditional digital shifted QAE | H8 | 16,431,638,004,072,030 | 1.643164 s | 1.384721 s | Fail |

The first two rows still require a valid digital-source second-moment certificate.
The last two avoid that premise but estimate only the implemented digital
residual, not the complete financial price. The Hadamard schedules using only
the unconditional support moment are also recorded, with bare floors of
15.694141 s and 56.408093 s; they are dominated here by shifted QAE.

## Conditional encoded capacity

For fixed work N and at most floor(P/a) simultaneously active primitive lanes,
each occupying a physical qubits and taking tau seconds, work conservation gives

    time >= N*tau/floor(P/a).

This is valid only if the chosen primitive throughput bound applies. It grants
unlimited algorithmic parallelism and omits all other costs. A bare pass is a
necessary screening result, not a constructed execution or advantage.

At P=10,000,000, distance 3 and 17 physical qubits per rotated data/syndrome
patch, granting one T per patch per nanosecond gives:

| Estimator | C4 work floor | H8 work floor |
|---|---:|---:|
| Conditional tight-moment Hadamard | 1.189461 s | 10.604390 s |
| Unconditional digital shifted QAE | 7.605402 s | 27.933799 s |

All four fail the RQMC latency screen under this explicit injection model.
C4's tight row is close, so the result must not be exaggerated. Native gates,
different codes or a different primitive time change this model. The artifact
includes native-CCX sensitivities, several lane occupancies, code cycles from
1 ns to 1 microsecond, and one versus d cycles per injection. None of those
coordinates is asserted to be a demonstrated device capability.

For the explicitly restricted 15-to-1 final-stage family from
[CAPACITY_SCREEN.md](CAPACITY_SCREEN.md), every final output is assumed to
occupy at least 11 tiles for 11d code cycles. Even granting all ten million
physical qubits to those factories, free lower-stage states and up to ten
million perfect states at time zero gives the conditional supply floor

    max(0,N_T-P)*121*(2d^2-1)*d*cycle/P.

At d=3 and a 1-ns cycle, these floors are:

| Estimator | C4 final-stage supply | H8 final-stage supply |
|---|---:|---:|
| Conditional tight-moment Hadamard | 431.774 s | 3,849.392 s |
| Unconditional digital shifted QAE | 2,760.759 s | 10,139.964 s |

This is a restricted-factory capacity bound, not a universal distillation
bound. It is already favorable through free data storage, routing, lower
levels, rejection and retries. The C4 fixed-iid comparator's more generous
26.783737-second budget still does not pass this factory-family screen.

## Memory, failure and unknown constants

The allocated serial-map logical register counts are 659,289/2,328,849 for
Hadamard and 637,599/2,307,159 for shifted QAE. At d=3, their data-only mappings
need approximately 11.21/39.59 million and 10.84/39.22 million physical qubits.
The new range multiplication reduces arithmetic work but leaves retained SSA
storage unchanged. The separate DAG schedules allocate additional private
scratch and therefore do not cure this mapping limit. These are allocations,
not lower bounds on a future compiler with pebbling or recomputation.

The artifact independently varies physical error rates from 1e-3 to 1e-6 and
clock times to compute sufficient distances under the stated approximate
logical-error fit. A failed union-bound certificate at a smaller distance does
not prove physical failure. Factory quality, actual decoder performance,
spacetime layout, feed-forward, calibration, complete financial certification,
preprocessing, measurement and decoding are additional obligations. No favorable
unknown constant has been substituted for them.

The correct decision is therefore: no end-to-end significant quantum advantage
established; useful exact-source and estimator improvements have weakened the
earlier bare negative screen. A future result must exhibit a feasible full
schedule and matched price guarantee, or change and verify these explicit
hardware/resource premises. An old serial upper schedule cannot refute that
possibility.

Reproduction:

```text
python -m research.controlled_priority_completion.capacity_revised --source-root results/controlled_priority_completion/range_compile_v1 --output results/controlled_priority_completion/capacity_range.json
```

Nine capacity tests pass, including source replacement multiplicity, interface
rejection, correct single-control memory and the distinction between a bare
capacity pass and a complete pricing pass. Targeted Ruff checks pass.
