# Rotation synthesis and conditional fault-tolerant accounting

22 September 2026. The remaining single-qubit rotations are now synthesized and
independently checked. The physical accounting is an explicit **conditional
resource model**, not a physical implementation or a demonstrated runtime. P5's
rotation obligation is closed for the archived estimator schedules; the complete
physical/full-price obligation remains open.

## What was executed

[synthesis_rotations.json](../../results/controlled_completion_followup/synthesis_rotations.json)
contains all 95 distinct absolute rotation targets: 67 dyadic radian angles and
28 inverse-QFT pi-rational angles. Targets are reconstructed from integers and
pi intervals. The strictest common operator tolerance is

    epsilon = 1 / 380759062412124000 = 2.626332761891364...e-18.

It covers all eight original model/precision/moment schedules and their updated
arithmetic versions, whose controlled-U counts and phase angles are unchanged.
The per-schedule rotation multiplicities reconcile exactly with the original
ledger. Eight smallest rotations are replaced by identity, with their errors
included; the other 87 sequences use 366–376 T gates each. Maximum certified
Frobenius error is 2.453269466693399e-18, an upper bound on operator error.
The most expensive certified error is an intentional identity approximation.

Generation used pygridsynth 1.1.0 and mpmath 1.3.0 at 120 decimal digits and took
56.21 seconds on this development machine. This is recorded setup work, not
quantum execution. Reuse is valid because the angles do not depend on the
financial paths or adaptive left endpoints. A fresh compilation can charge this
setup cost; the artifact is reusable by all listed schedules.

The installed pygridsynth release uses `int.bit_count`, absent in the project's
Python 3.9. A local function substitution computes the identical trailing-zero
valuation with `bit_length`; no installed package source was changed. Near-axis
targets caused slow grid searches in that release. The actual generated
construction composes approximations to `Rz(theta+1/2)` and `Rz(-1/2)`, using
`X Rz(1/2) X` for the latter. Each component requests epsilon/16. The composed
sequence, rather than an error estimate for its ingredients, is then verified.
This doubles synthesis cost but is negligible beside financial arithmetic; no
T-optimality claim is made. The method and package are documented in the
[upstream primary repository](https://github.com/quantum-programming/pygridsynth).

Verification does not use generator fidelities, binary64 target angles, or
subtraction of nearly equal double-precision fidelities. It independently
multiplies 2-by-2 H/S/T/X/W matrices with directed mpmath interval arithmetic,
encloses each squared entry error, and proves the Frobenius norm bound against
the exact rational/pi target. The interval upper endpoint is converted to an
exact rational before comparison and outward serialization. This is a
reproducible certificate under that interval implementation, not a formally
verified implementation of arbitrary-precision arithmetic.

Stored strings are matrix products read left to right, hence execute right to
left. Negative targets use the complete product's adjoint, reversing order and
replacing T/S with T-dagger/S-dagger at unchanged resource counts. W is the
global phase exp(i*pi/4), included in verification and omitted from physical
gates. Substituting Rz for the three **unconditional** one-qubit P gates in the
CP decomposition changes only its global phase, including the zero-control
subspace. It does not discard a controlled relative phase. Additional tests
reconstruct both signs of all 95 controlled phases as 4-by-4 matrices at 100
digits and check the composition/wire convention against diagonal CP matrices.

## Updated logical totals

[ft_scenarios.json](../../results/controlled_completion_followup/ft_scenarios.json)
is bound by SHA-256 to the new truncated-multiply ledger at
`arithmetic_v1/cost_v3_phase64/ledger.json` and the synthesized rotation library.
Representative 40-bit financial, 64-bit phase results:

| Model and moment | Additional synthesized T gates | Complete logical T gates | Synthesis / arithmetic |
|---|---:|---:|---:|
| C4, conditional continuous moment | 101,581,724,177,082 | 2,094,809,776,342,041,600 | 0.00485% |
| H8, conditional continuous moment | 414,624,368,145,966 | 31,467,851,602,424,366,175 | 0.00132% |
| C4, digital support moment | 30,678,540,653,530,440 | 632,652,284,459,850,815,974 | 0.00485% |
| H8, digital support moment | 31,230,767,711,281,776 | 2,370,256,720,918,051,025,412 | 0.00132% |

Complete T totals include exact inverse-QFT rotations. Clifford counts include
synthesis, both CXs in every CP decomposition, QFT swaps, reflection, state
preparation and constant loads. The physical scenario serializes all of these
gates; it never converts an arithmetic-only T depth into a complete runtime.

## Physical model, with its conditions exposed

The input noise coordinates are p=1e-3 or 1e-4, a 1 microsecond code cycle and
10 microsecond classical feedback. They are sensitivity assumptions. The
per-patch/per-round relation

    p_L(d) = 0.1 (100p)^((d+1)/2)

is the approximate decoder/noise-dependent fit in Section XV of
[Fowler and Gidney](https://arxiv.org/pdf/1808.06709), not a universal theorem.
The same paper supplies the rotated-patch qubit count and adjacent CNOT timing
used as modeling primitives. Extrapolating the fit to enormous lifetimes is a
condition of these calculations, not evidence that such lifetimes are practical.

All data, factory, buffer and routing tiles remain live for the entire schedule.
The code picks the first odd distance with

    number_of_tiles * total_code_cycles * p_L(d) <= 0.001.

This includes idle exposure and finite retry waits. Each tile costs at most
`2*d*d` physical qubits in the accounting formula. Data plus factory/buffer
tiles are doubled for routing and spare space, an explicit allowance rather
than a validated layout. All algorithm gates and QPE executions are serial.
Sibling nodes inside the single dedicated factory tree may run in parallel.

Two routing coordinates are retained: one hop per logical interaction is an
optimistic adjacency sensitivity; Q-1 hops is a deliberately slow line-routing
alternative for Q algorithm qubits. To restore placement, h hops cost 2h SWAPs,
each decomposed into three adjacent CNOTs. The code charges `(12h+2)d` rounds
per CX and `(12h+4)d + feedback` per T injection, in addition to state production.
One-qubit Cliffords receive 4d rounds. Initial data preparation, measurements,
resets, QPE feedback and adaptive-stage feedback are added. These constants
assume distance-preserving logical primitives and sufficient classical decoding
throughput; no device layout or decoder was constructed or benchmarked.

Factories use a full 15-ary tree of 15-to-1 blocks, each allocated 11 protocol
tiles plus 16 input/output buffers; each raw injection lane receives two tiles,
before the extra routing allowance. The 11-tile protocol and 15-step upper-level
distillation construction are described by
[Litinski, Sections 3.3–3.5](https://quantum-journal.org/papers/q-2019-03-05-128/).
This model conditionally budgets at most `15d + feedback` per block, plus
generation of its children, and assumes a raw injection succeeds with at least
probability 1/2 in three rounds with accepted stochastic Z-error at most p.
These are conditional primitive bounds, not measured factory specifications.

The familiar leading-order `35 e^3` is **not** used as an exact error bound.
For independent input Z-errors of probability at most e, the protocol detects
all weight-one and weight-two faults. A union over triples bounds the error
numerator by `binom(15,3)e^3`; the zero-error case gives acceptance probability
at least `(1-e)^15`. Thus the conservative all-orders recurrence is

    e_next <= 455 e^3 / (1-e)^15.

It is conditioned on no logical fault, since all logical faults anywhere in a
factory are already included in the whole-machine patch-round union bound.
Independent accepted inputs from distinct invocations are another explicit
noise assumption. All listed cases need three levels at p=1e-3 and two at p=1e-4.

Every factory and raw injection has a finite retry cap. A union bound over the
complete worst-case tree of retries assigns at most 0.0001 to exhausted caps.
Reported throughput is one delivered state per worst-case production interval
on the no-abort event, not a mean-rate substitution. This intentionally slow
schedule makes time, capacity and failure exposure mutually consistent.

For the conditional continuous-moment f=40 cases, p=1e-3 with one-hop routing
gives distances 67/71 and about 12.08/47.23 billion physical qubits for C4/H8.
The corresponding conservative serial-schedule bounds are 1.750e19/3.338e20
seconds. At p=1e-4 the distances are 31/33 and the bounds are
3.056e17/5.926e18 seconds. These deliberately conservative **conditional upper
bounds** do not prove a runtime lower bound or disprove faster physical designs.
The much simpler arithmetic feasibility screens remain the relevant rejection
evidence for this implementation.

The physical failure allocation is 0.001 logical faults, 0.0005 accepted magic
states, 0.0001 exhausted retries and 0.0004 controller faults, totaling the
inherited 0.002 allocation. The controller reliability term is an assumed
requirement. Five local controller replays per schedule provide diagnostics of
the exact interval update, not worst-case device-feedback/decoder certification.

## Remaining full-price obligations

The output explicitly retains

    T_training + T_certificates + T_surrogate + T_device
        + T_decoder_and_IO + T_outputs <= T_classical / 10.

Archived classical certificate/training times are included when applicable.
Online surrogate and regret costs, a completed digital financial certificate,
training not already charged, and device decoding/output costs are unclosed
and stored as null, never zero. Fresh sequence generation adds its recorded
56.21-second setup cost unless legitimately reused. A complete 99% price claim
also requires the still-failing/unclosed P4 financial terms. No completed
fault-tolerant financial price, physical runtime, or quantum advantage is claimed.

## Reproduction

The generator depends on `pygridsynth==1.1.0` and `mpmath==1.3.0`; checking the
archived sequences only needs mpmath, and does not import pygridsynth. From the
repository root with the research environment:

```text
python -m research.controlled_completion_followup.synthesis_rotations --verify-only
python -m research.controlled_completion_followup.ft_model --ledger results/controlled_completion_followup/arithmetic_v1/cost_v3_phase64/ledger.json
python -m pytest research/controlled_completion_followup/test_ft_checks.py -q
```

Omit `--verify-only` to generate a fresh library. Factoring timeouts can make
fresh sequences differ across machines; the committed sequences are immutable
review targets with independent interval certificates and exact target bindings.
