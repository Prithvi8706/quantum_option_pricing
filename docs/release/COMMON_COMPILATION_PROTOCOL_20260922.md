# Fixed common-compilation protocol

Date: 2026-09-22. Freeze this file, producer and tests in Git before full acquisition.
This is a deterministic resource follow-up on existing development cases, not
fresh confirmation, simulated pricing data, or physical execution.

## Question and fixed menu

Does the D1/D2 projected CX ordering survive a common explicit logical compiler?
Only six configurations: D1/D2 reflection degrees 64/128, raw arithmetic parents
`stronger_arithmetic_v1/D1_28.json` and `D2_28.json`, and signed residual
`signed_residual_arithmetic_v1/D1_00.json` and `D2_00.json`. Keep the original
Gaussian midpoint target, q=10, cutoff 4, financial models, $1 absolute tolerance,
95% ideal confidence, 17 repetitions and existing AE sizes. Reject model drift
by exact equality of regenerated fixed-point parent plans before compiling.

## Common policy

Pin Qiskit Terra **0.46.3** (reject other versions), and record its version and the
source commit. Translate every finite loader, signal, reflection and projector
block to U/CX with `optimization_level=0`, seed 717, unrestricted connectivity.
No old optimization-level-1 block counts enter new counts. Re-emit arithmetic
X/CX/CCX streams using unchanged frozen producers, and check complete component
records against archives. Translate X to one U, CCX to nine U and six CX, exactly
the same opt0 decomposition checked on small circuits.

Control every native U with the same fixed five-U/two-CX template (one of the
five U is explicit identity padding), every CX with nine U/six CX. Add one U on
the new control for each controlled block's global phase, including zero phase.
No special-angle simplification, identity removal or neighboring cancellation
is allowed. Arithmetic's historical one-U phase allowance is retained as one
explicit identity U, alongside the selector Hadamards. Loader costs are charged
once per independent coordinate; reflection readout charges both Hadamards.

Apply the same two AE ledgers to all routes: (1) controlled A/A-inverse, (2)
unconditional A/A-inverse around controlled reflections, using the exact
control-cancellation identity. This identity is the only permitted nonlocal
rewrite. Inverses preserve native counts. Controlled zero reflections use the
same clean v-chain emitter and opt0 translation for each allocated A width.
Charge good-state CZ, the Grover global minus sign on its control, phase-register
Hadamards, full inverse QFT including swaps, and every repeated iterate. No
billions-gate AE circuit is materialized. Total allocated wires are
`2*A_width - 2 + log2(M)` including the clean zero-reflection workspace.

U/CX counts describe exact ideal decomposition identities, not a certified
binary64 native transpiler output. Small matrix tests check the implementation
including nonzero global phases; they are not a universal numerical-rounding
certificate. Existing stored-angle ideal oracle certificates are retained.
Physical synthesis, transport and noise remain outside the guarantee.

## Depth, error bridge and classical work

Report `U+CX` as the depth of an explicitly serial common schedule, a valid
upper bound for every route. Do not compare unlike historical dependency depths
or claim an optimized-depth, spacetime, or runtime winner. This limitation is
intentional; obtaining optimal comparable DAG depths is not needed for the CX
question. Clifford+T results are unavailable because no common certified
rotation-synthesis error allocation has been established.

Use the separately reviewed canonical-label adapter to exhaust every label in
each fixed AE size. Add sensitivity times its certified conversion error, and
verify the fixed dollar contract remains feasible against exact rational pi
bounds. The independent-median conversion bound is inherited from order-statistic
monotonicity. No schedule retuning. Record offset input certificates, source and
archive hashes, component build/compilation CPU times, total CPU/wall time,
peak RSS and versions. Historical classical offset/preprocessing costs remain
separate from logical gates; this study does not reacquire or hide them.

## Limits, outputs, failure and review

Exclusive output: `results/journal_sprint/common_compilation_20260922_v1/`.
Do not overwrite attempts; any correction requires a new frozen source and
exclusive suffixed archive. Two CPU-hours and 16 GiB RSS maximum, guarded by a
monitor; retain partial rows and a resource-cap or failure record on stopping.
No statevectors except tiny unit tests; no hardware or paid execution.

Per row retain complete components, both AE ledgers, width, serial depth bound,
schedule, error bridge, and differences from historical resource counts. Retain
all six fixed outcomes. Success means a complete reconciled comparison, not
preservation of a preferred winner. Report a changed ranking honestly. Final
independent AI review must check controls, phase, inverse/cleanup accounting,
width, error assumptions and provenance before PR merge. Scientific human
review and submission remain open and are not implied by tests or AI review.

Command, from repository root in the pinned environment:

```powershell
.context/week15_env_v1/Scripts/python.exe -m research.common_compilation_20260922.run results/journal_sprint/common_compilation_20260922_v1
```
