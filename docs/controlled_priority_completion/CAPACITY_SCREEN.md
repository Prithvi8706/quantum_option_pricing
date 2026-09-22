# Capacity constraints for the fixed controlled-compound workload

This page preserves the screen of the **previous conservative estimator**.
The same-candidate estimator refinement is assessed separately in
[CAPACITY_REVISED.md](CAPACITY_REVISED.md); its lower query counts materially
change the bare work screen and must be used for the current decision.

22 September 2026. **The emitted estimator fails optimistic work-capacity
screens under the declared 10-million-physical-qubit cap.** This result uses
total work, not the earlier serial leaf-schedule upper bound. It is conditional
on the stated primitives and current emitted workload. It is not an
impossibility theorem for this option, another compiler or all quantum methods.

The [machine-readable calculation](../../results/controlled_priority_completion/capacity_screen.json)
binds all counts to the preceding arithmetic ledger and individual sources by
SHA-256. Four rows cover C4/H8, f40, and the conditional continuous-moment versus
rigorous digital-support-moment schedules. The strongest conclusions below
grant the smaller continuous moment for free.

## Work conservation without a scheduling assumption

Let P be the physical-qubit cap, a the minimum physical-qubit occupancy per
operation lane, tau the minimum lane occupation time, and N the fixed number
of operations. At most floor(P/a) lanes can operate at once. Integrating their
occupancy gives

    T >= N * tau / floor(P/a).

We grant every physical qubit to those lanes, free data storage, free routing,
free Clifford gates and free perfect magic states. We do not charge the source's
actual dependency depth or initialization. Omitting these obligations makes the
screen favorable; a passing screen would not establish feasibility.

For P=10,000,000, a=1 and tau=1 nanosecond:

| Conditional tight-moment f40 job | C4 | H8 |
|---|---:|---:|
| Actual arithmetic T count | 2.094708e18 | 3.146744e19 |
| Conditional minimum time from T work | 209.471 s | 3,146.744 s |
| 10x budget against controlled RQMC | 1.110592 s | 1.384721 s |
| Required per-lane duration if all other assumptions stay free | <=5.302 ps | <=0.440 ps |
| Arithmetic CCX count | 2.992440e17 | 4.495348e18 |
| One native CCX per 1 ns per physical lane, all else free | 29.924 s | 449.535 s |

The native-CCX sensitivity replaces each seven-T Toffoli by one primitive and
still grants it just one physical lane, even though an ordinary Toffoli acts
on three qubits. It therefore tests an additional favorable change; it is not
a compiled native-CCX implementation. Both screens fail. The C4 fixed-iid
comparator has a 26.783737-second tenfold budget. It also fails the 209.471-second
T-work screen and narrowly fails the 29.924-second one-lane native-CCX screen.

The calculation varies lane durations from 1 ns through 1 microsecond and
occupancy from 1 through 449 physical qubits. Those are explicit sensitivity
coordinates, not verified hardware capabilities. Reducing query count or
arithmetic work changes N and requires recalculation. A compiler that cancels
or replaces these operations is outside the fixed-workload premise. No universal
per-physical-qubit T-rate law is being asserted.

## Why the constant-one oracle thought experiment is different

The older favorable source screen assumed 218 C4 or 508 H8 clean-source calls,
with no proved estimator realizing that schedule. Their aggregate T counts are
2.937006e11 and 2.536043e12. The same one-physical-qubit/1-ns capacity inequality
only gives 0.00002937 s and 0.00025360 s. Thus **work capacity alone does not rule
out that hypothetical query count**. It would be incorrect to use the failure
of the actual conservative estimator to reject every variance-sensitive method.

Conversely, the constant-one formula is not a query lower bound or an explicit
algorithm. Its favorable capacity result does not establish attainable depth,
available memory, confidence, phase accuracy or full pricing accuracy. The root
investigation separately examines actual dependency schedules and an explicit
estimator refinement.

## Surface-code storage and noise coordinates

For the currently allocated circuit, one rotated surface-code patch per logical
qubit needs d^2 data qubits and d^2-1 syndrome qubits before routing or factories.
Even distance 3 therefore needs 11,208,270 physical qubits for C4 and 39,590,824
for H8. Both exceed the cap. This is a mapping constraint for the present
allocation, not a memory lower bound on a compiler with recomputation or fewer
live registers. The patch construction is in
[Fowler and Gidney, Section II](https://arxiv.org/html/1808.06709v4#S2).

For illustration, the archived fit

    p_L = 0.1 * (100 p)^((d+1)/2)

and Q*ceil(budget/cycle)*p_L <= 0.001 give conditional *sufficient* distances
for retaining the current data allocation for the entire tenfold budget. With
1-microsecond cycles, p=1e-3/1e-4/1e-5/1e-6 gives C4 distances 27/13/9/7 and H8
29/15/9/7. Even the smallest resulting data allocation is 63.95 million C4 or
225.90 million H8 physical qubits. The fit is approximate and decoder-dependent;
the union test is sufficient, not necessary. Failure of that test at a smaller
distance does not prove an actual failure probability. See
[Fowler and Gidney, Section XV](https://arxiv.org/html/1808.06709v4#S15).

## Finite factory capacity, separately conditional

Let rho be delivered high-fidelity states per physical-qubit second. With at
most P pre-stored one-qubit states, even granting their storage without taking
space from factories,

    T_supply >= max(0, N_T - P) / (P * rho).

The JSON exposes the required rho via the per-qubit work rate. It does not fill
that unknown with an optimistic vendor number. A separate, specified-family
screen assumes a 15-to-1 top stage occupies at least 11 tiles for 11d cycles per
output. This deliberately understates the 15d upper stage when its inputs are
already distilled, ignores all earlier stages and rejects, and gives every
physical qubit to top-stage factories. For that chosen family,

    T_supply >= max(0, N_T-P) * 121 * (2d^2-1) * d * cycle / P.

At d=3 and a 1-ns code cycle, this lower capacity constraint is 1.29e6 seconds
for the actual C4 arithmetic and 1.94e7 seconds for H8. For the unimplemented
constant-one clean-source workloads it is 0.181 s and 1.565 s. At d=7 the latter
become 2.413 s and 20.836 s. These are constraints on that factory family and
chosen distance, not lower bounds on all distillation, catalysis or native-gate
architectures. The tile schedules are in
[Litinski, Sections 3.3 and 3.5](https://arxiv.org/html/1808.02892v3#S3).

Quality is kept separate from throughput. The archived conservative recurrence
e_next <= 455 e^3/(1-e)^15 gives enough concatenation levels for
N_T*e_final <= 0.0005 under independent accepted stochastic Z errors and no
logical faults. The JSON varies raw errors 1e-3 through 1e-6. These are levels
sufficient under that particular bound, not proof fewer levels cannot work.
Lower levels, acceptance, storage and logical faults must be charged by any
actual factory proposal; this optimistic screen grants them for free.

## Decision and limits

More parallel execution of the unchanged conservative estimator cannot pass the
declared budget under any listed capacity coordinate. The conclusion does not
depend on the previous serial upper schedule. Under the most favorable 1-ns,
one-physical-qubit lane coordinate, the arithmetic work must fall by at least
189x for C4 or 2,273x for H8 before this necessary screen can pass against RQMC.
Real encoding, storage and factory costs would demand further improvement.

This analysis completes a falsifiable check of one proposed escape from the
failed cost gate. It does not complete financial certification, a physical
layout, a journal contribution or an advantage confirmation. A new explicit
estimator schedule can be inserted into the same work formula without preserving
the old negative conclusion by assumption.

Reproduce from the repository root:

```text
python -m research.controlled_priority_completion.capacity_screen
python -m pytest research/controlled_priority_completion/test_capacity_screen.py -q
```

Executed result: all five accounting tests passed. Source reading on 22 September
2026 was limited to the cited storage, noise-fit and factory sections of the
existing architecture references; no alternative advantage direction was searched.
