# Explicit estimator redesign for the same controlled compound price

22 September 2026. **The cost gate still fails.** This investigation replaces
the earlier deliberately conservative QPE schedule by two much cheaper explicit
estimators, with no change to the financial source or acceptance threshold.
The large reductions below are quantum-implementation improvements; they are
not quantum-over-classical advantages.

The source is still the emitted f40/q32 controlled compound residual Y at strike
6. The error allocated to its undiscounted mean is 0.002/exp(-r*tau), and ideal
estimation failure remains 0.003. Source arithmetic, law, control, policy regret,
surrogate price, coherent approximation and physical failures remain separate
obligations. A total price must meet the original penny/99% contract and take
at most 1.110592 seconds for C4 or 1.384721 seconds for H8 to beat the existing
classical comparator by 10 times. Those comparators are the favorable empirical
RQMC screen, not a replacement for matched rigorous financial certification.

## Executed result

| Estimator | Model | Controlled iterations | Arithmetic T count | Serial arithmetic seconds at hypothetical 1 ns/T layer |
|---|---|---:|---:|---:|
| Hadamard, conditional tight moment | C4 | 1,203,320 | 1.636360e15 | 542,257.420 |
| Hadamard, conditional tight moment | H8 | 2,967,610 | 1.485259e16 | 4,908,968.101 |
| Shifted-amplitude QAE, unconditional bounded digital Y | C4 | 7,864,305 | 1.059543e16 | 3,509,112.644 |
| Shifted-amplitude QAE, unconditional bounded digital Y | H8 | 7,864,305 | 3.926105e16 | 12,974,180.632 |

The Hadamard schedule reduces the previous tight-moment controlled-U counts by
1,280.10 times for C4 and 2,118.65 times for H8. The bounded-output schedule
avoids both the still-unproved tight-moment transfer and the costly atan phase
function. It is also cheaper than the existing signed-bin estimator under the
loose support moment: that estimator uses 39,845,850 Grover iterations for either
model, versus 7,864,305 here. Under the tight moment the existing signed-bin
counts are 7,962,138/11,468,450 and the new Hadamard method is cheaper.

Even with all remaining costs set favorably to zero, the selected tight-moment
Hadamard schedules miss the 10x budget by approximately 488,260/3,545,096 times.
The requisite scheduled T-layer times are 2.0481e-15/2.8208e-16 seconds. These
are sensitivity requirements for the emitted serial arithmetic schedule,
**not physical predictions or lower bounds against all possible circuits**.
The unconditional digital schedules miss by still larger factors. Parallelism,
reversible storage redesign and physical factory capacity must be assessed
separately; fewer QPE calls do not make those costs disappear.

## A. Hadamard tests with exact confidence accounting

The primary result is [Kothari and O'Donnell, arXiv:2208.07544](https://arxiv.org/abs/2208.07544),
Theorem 3.21 and its proof, equations (48)--(55), followed by Section 3.6 and
Lemma 4.3. These sections were read from the preserved full paper. Section 3.6
already proposes replacing QPE by Hadamard tests. This work supplies explicit
constants and a compiled-oracle cost for this project; it does not claim that
the Hadamard idea, source-access speedup or mean-estimation theorem is new.

Let E[Y^2] <= s^2, with s rounded upwards exactly at 64 bits. Initially
mu=E[Y] is in [-s,s]. Maintain an interval [a,a+W] containing mu. For a rational
parameter 0<c<1, set

    e = W / (1+3c),    target = a+c*e,
    z = (Y-target)/N,  epsilon = e/N,
    q = (1+c)/(1+3c).

Here N is a power of two, at least 16. As target stays inside [-s,s],
sqrt(E[z^2]) <= 2s/N = s0. The circuit is the existing
U = (2|psi><psi|-I) diag(exp(-2i atan(z))), including its controlled reflection
sign. No distribution table or new state preparation is introduced.

For an integer C with C*s0<1, Theorem 3.21 gives a spectral good event of
probability at least 1-eta, eta=2/C^2. On it, for m=|E[z]|,

    2m/[sqrt(1+s0^2)*(1+C*s0)] <= |theta|
    |theta| <= 2 asin(m/(1-C*s0)).

The upper inequality deliberately drops sqrt(1+s_actual^2), weakening it safely.
All evaluated arguments are certified to lie in [0,1). The lower inequality
uses asin(x)>=x. The theorem's zero-mean/zero-phase case follows by continuity,
as in its proof.

The hypotheses to distinguish are m<=c*epsilon (small) and m>=epsilon (large).
Because the current interval contains mu, m<=(1+2c)*epsilon always. Let

    gamma = 2 asin(c*epsilon/(1-C*s0)),
    alpha = 2epsilon/[sqrt(1+s0^2)*(1+C*s0)],
    beta  = 2 asin((1+2c)*epsilon/(1-C*s0)).

Prepare a fresh |psi>, prepare one control in |+>, apply controlled-U exactly T
times, apply H to the control and measure. Its plus probability is
E_theta[(1+cos(T*theta))/2]. Choose an integer T satisfying T*gamma<pi and
0<T*alpha<=T*beta<2pi. The small-promise probability is at least

    a_prob = (1-eta)*(1+cos(T*gamma))/2.

The large-promise probability is at most

    b_prob = eta+(1-eta)*(1+max(cos(T*alpha),cos(T*beta)))/2.

This accounts pessimistically for the spectral bad event. The cosine maximum
on the certified interval inside [0,2pi] occurs at an endpoint. Every selected
angular inequality and probability bound is checked with 80-digit interval
arithmetic. Rational probability bounds on a 2^-30 mesh are then rounded
outwards and rechecked against those intervals.

Repeat r times with fresh input states; output small if the plus count is at
least integer k. Both binomial failure tails are evaluated as **exact rational
sums**, not a normal approximation. Stage j receives
delta_j = 0.003*T_j/sum(T_j); hence the total ideal failure is at most 0.003 by
the union bound, including adaptive intervals. The finite design search uses
only the supplied second moment and error, not prices or favorable measured
outcomes. It explores 175 constant choices, scores valid designs by a cheap
Hoeffding estimate, and refines the best eight using certified binomial tails.
It is a bounded search, not a claim of globally optimal constants.

If the result is small, retain [a,a+qW]. If large, retain
[a+2cW/(1+3c),a+W], also of width qW. On the event of correct answers to the
two promises, these updates are valid even in the indeterminate gap:
small excludes m>=epsilon, while large excludes m<=c*epsilon. Stop when the
radius is at most the requested error. Exact rational interval endpoints avoid
controller-rounding drift; the target is rounded only when loaded into the
existing 64-bit phase source. That load error is already within its separate
coherent phase-function allowance.

The selected C4 design uses N=16,C=5,c=1/8, 27 stages, 1,301 fresh Hadamard
tests and a longest chain of 5,762 controlled U calls. H8 uses N=64,C=6,c=1/6,
25 stages, 918 tests and a longest chain of 23,663 calls. The existing phase
certificate applies because |Y|,|target|<=100 and N>=16. The actual rotation
strings from the preceding investigation meet a stricter per-rotation tolerance
than needed here; IQFT is absent entirely. Gate multiplicities, measurement,
state preparations and classical-load upper counts are recorded explicitly.

The continuous tight moment is still conditional on a valid finite-source
transfer. The same Hadamard derivation with the rigorous bounded-output moment
is also emitted, but it is dominated here by method B.

## B. An exact bounded-output alternative

Since the digital source is clipped to |Y|<100, define p=E[(Y+128)/256]. Its
mean can be estimated without a second-moment acquisition or atan oracle.
At f=40, append 48 uniform selector bits u and compute the clean predicate

    u < raw(Y) + 128*2^40.

For fixed Y this predicate's exact probability is (Y+128)/256. Its clean
gate-emitted comparator preserves Y and u and uncomputes all scratch. The
signed shift is exactly a flip of the highest bit among the low 48 source
bits, under the proved source range. No arbitrary data-dependent rotation,
Gaussian table, QRAM or hidden preparation oracle is involved.

The Grover iterate is the controlled reflection about the uniform state times
the controlled predicate phase flip. It executes the financial forward graph,
the clean predicate, its phase flip, the predicate inverse and financial inverse;
then it reflects on *both* the financial-random and selector bits. The existing
controlled-reflection minus sign is retained. Every address and primitive gate
is emitted in the hierarchical wrapper files. A source output copy is removed
by reading its retained SSA word directly. The counts include both inverse
operations, the extra random bits and reflection workspace.

[Montanaro, corrected arXiv:1504.06987](https://arxiv.org/abs/1504.06987), Section 2,
Theorem 2, gives QAE error at most

    2*pi*sqrt(p*(1-p))/M + pi^2/M^2

with probability at least 8/pi^2. Since sqrt(p*(1-p))<=1/2, multiplying by 256
gives a uniform mean-error bound. An 80-digit interval calculation certifies
M=524,288 for both requested errors. Fifteen independent QPE runs and a median
reduce failure below 0.003; the binomial calculation again uses an outward
rational bound and exact arithmetic. There are 15*(M-1)=7,864,305 Grover calls.
Only 6,885 arbitrary single-qubit IQFT rotations remain. The prior synthesis
library contains these targets with much stricter tolerances than required.

This completes a **digital residual mean estimator**, not the financial price
certificate. The same source arithmetic, implemented policy, regret and
surrogate obligations remain. The unused phase-function error allowance is not
silently reassigned to another term.

## Reproduction and verification

Run from the repository root with the existing research environment:

    .context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_priority_completion.estimator_hadamard
    .context/antithetic_feasibility_env/Scripts/python.exe -m research.controlled_priority_completion.estimator_bounded --replay
    .context/antithetic_feasibility_env/Scripts/python.exe -m pytest research/controlled_priority_completion/test_estimator_hadamard.py research/controlled_priority_completion/test_estimator_bounded.py -q

Artifacts are `results/controlled_priority_completion/estimator_*.json`.
The author's initial 14-test run used user-site pytest through that interpreter.
An independent reviewer reran all 14 supplied tests with `PYTHONNOUSERSITE=1`
and `.context/controlled_closeout_repro/Scripts/python.exe`; all passed in that
isolated environment. See `REVIEW_ESTIMATORS.md` for the separate review and
additional matrix/interval checks.
The tests verify exact union-bound allocation, balanced interval geometry,
both legal ambiguity choices, finite-unitary Hadamard probabilities including
skewed two-point laws, full small-register selector truth tables, production
boundary inputs, nonzero output flags, cleanup and inverse behavior, and the
QAE probability guarantee on an independent grid. They are implementation
checks supplementing the stated proofs, not sampled substitutes for them.

The `--replay` run executes the entire emitted financial source, comparator and
both inverses on an active preserved input for each model and on either side
of its predicate boundary. It verifies the diagonal marking operation and
workspace cleanup. It does **not** simulate the full price QPE or turn a basis
execution into hardware timing. All earlier evidence is preserved.

The next scientific decision should use the revised counts, not the superseded
billion-query QPE schedule. They eliminate a real implementation weakness but
still do not establish the requested significant advantage.
