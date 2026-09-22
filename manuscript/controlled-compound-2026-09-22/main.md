# Auditable digital-oracle resources for controlled compound Asian-basket pricing

Research draft, 22 September 2026. Author identities, affiliations, declarations
and human approval are pending. This separate companion draft preserves the
September Asian-basket implementation-comparison manuscript. It is not a
submitted article or a claim of significant quantum advantage.

## Abstract

Quantum mean-estimation guarantees do not by themselves establish a practical
option-pricing advantage. We study a controlled compound Asian-basket pricing
implementation with an explicit finite input law, reversible source, classical
comparison and finite-confidence estimation schedule. Sound integer ranges
allow narrower exact multipliers; parallel schedules reduce the arithmetic
depth while paying for extra workspace. A concrete Hadamard-test implementation
and a bounded-output amplitude estimator substantially improve the earlier
quantum implementation. Their costs still do not establish the declared
classical crossover. We separate verified digital computation from remaining
financial certification and conditional physical-resource assumptions.

Keywords: quantum algorithms; option pricing; amplitude estimation; reversible
arithmetic; resource estimation; classical control variates.

## 1. Question and contribution

The question is whether a compiled quantum estimator can price a financially
specified compound Asian-basket option with a meaningful complete-latency
advantage over strong controlled classical methods. The acceptance target is
tenfold latency improvement at one-cent absolute price error and 99% per-price
confidence, under a declared physical-qubit cap of ten million. Tenfold is a
practical robustness margin for uncertain future execution assumptions; it is
not a statistical significance threshold. A successful selected instance would
still require confirmation over a frozen parameter region. No such confirmation
has been performed because the prerequisite gates do not pass.

We contribute an auditable case study of a particular implementation. It joins
exact digital source execution, explicit estimation constants, a range-dependent
compiler optimization, a finite-law control-bias analysis, and strong classical
comparators. The range and schedule transformations retain the digital output;
their improvements are relative to a named earlier quantum implementation.
They are not improvements over classical pricing.

The negative crossover outcome is scoped. A constructed schedule that is slow
does not lower-bound every possible circuit. A capacity inequality applies only
to the fixed operation workload and throughput model used to derive it.
Neither result proves quantum advantage impossible for these options.

## 2. Relation to existing work

Blanchet et al. [1] explicitly discuss compound-option pricing as nonlinear
Monte Carlo. Consequently, neither selecting a compound payoff nor introducing
nested quantum estimation establishes originality. Kothari and O'Donnell [2]
already provide variance-sensitive source-code mean estimation and describe
Hadamard tests as an alternative to phase estimation. Our contribution is a
concrete finite-confidence realization and its cost for this source, not a new
mean-estimation theorem. The bounded alternative uses standard amplitude
estimation with the explicit guarantee summarized by Montanaro [3].

Chakrabarti et al. [4] and Wang and Kan [5] already perform detailed derivative
resource estimates including state preparation and arithmetic. Herman et al.
[6] formulate a derivative-pricing framework that separates truncation,
discretization, arithmetic and estimation errors. Our particular midpoint
Box-Muller law, guarded paths and control combination require their own
quantitative analysis; we do not claim a first general error framework.
Lemaire, Montes and Pages [7, Section 4.1] explicitly account for bias from a
quantized approximate control expectation and price a compound option using
analytic inner integration [7, Section 4.2.2]. Approximate-control bias and
removal of nesting by conditional formulas are therefore established principles.

The proposed journal contribution is the reusable, inspectable integration and
its specific numerical findings. This bounded prior-art comparison is not a
proof of publication priority or sufficient journal novelty.

## 3. Financial contract and classical comparison

We use equal-weight arithmetic Asian baskets under correlated geometric
Brownian motion, spot 100, risk-free rate 0.03 and inner strike 100. The inner
payoff averages all specified monitoring dates and assets. A compound call at
time tau=T/2 pays max(C(X)-Kc,0), where C(X) is the time-tau continuation price
of the inner call conditional on the past state X. Its time-zero price is
`exp(-r*tau) E[max(C(X)-Kc,0)]`. Monitoring is discrete by financial definition;
the Gaussian probability law is continuous. A finite midpoint law used by the
circuit is a further numerical approximation, not a redefinition of the target.

| Model | Assets | Dates | Volatility | Correlation | Maturity |
|---|---:|---:|---:|---:|---:|
| C4 | 4 | 12 | 0.20 | 0.20 | 1 |
| C8 | 8 | 12 | 0.40 | 0.20 | 1 |
| H4 | 4 | 12 | 0.40 | 0.70 | 3 |
| H8 | 8 | 24 | 0.40 | 0.20 | 3 |

Development uses compound strikes 3, 6 and 9. The detailed emitted quantum
source comparison uses C4/H8 and strike 6. C4/H8 and all earlier development
cases are not independent confirmation. In particular, D1/D2 belong to the
separate original manuscript and do not validate the present model.

The classical pipeline exploits a conditional linear/geometric control,
moment-matched approximation, regression where useful, conditional sampling,
randomized QMC, and antithetic correction diagnostics. It is not plain Monte
Carlo. The archived favorable screening times are 11.1059177 seconds for C4 and
13.847206 seconds for H8, including all three strikes. Charging that full
three-output time against one quantum strike deliberately favors quantum in
this rejection screen. H8 uses the faster preserved controlled cap/tail result;
a later slower parity run does not replace it just to improve the quantum ratio.
These empirical randomized-QMC intervals and reference-overlap diagnostics are
not distribution-free rigorous confidence certificates.

A separate fixed-iid C4 comparator costs 267.8373668 seconds including its
archived training charge, under the stated iid/exact-evaluation premises. It
provides a second, more conservative confidence-contract screen. Neither
comparator supplies a completed certificate for the quantum implemented policy.
Both sides must receive the same useful controls and comparable opportunities
for preprocessing and amortization in any future affirmative comparison.

## 4. Controlled decomposition and error obligations

Let a(X) be the already accrued arithmetic average contribution and let A and
G be the future arithmetic and geometric averages. Write k=2(100-a),
q=exp(-r(T-tau))/2, F=q(E[A|X]-k), and
Pg=q E[(k-G)+|X]. Define

    c0 = F + Pg,
    R  = q*((k-G)+ - (k-A)+).

Under the intended continuous model C=c0-E[R|X]. For a computable approximation
V(X), take the decision d(X)=1{V(X)>Kc} and the signed residual
`Y=d(X)*(c0-V-R)`. Then

    E[(V-Kc)+] + E[Y] = E[d(X)*(C(X)-Kc)].

The optimal compound value adds nonnegative regret
E[(C-Kc)+-d(C-Kc)]. This is the tower property and elementary algebra. It is
useful because the baseline and residual should be analyzed jointly: their V
terms cancel. It does not make implemented-policy regret free. A circuit uses
a clipped finite-law version of Y, so transfer of the continuous analytic
control identity must also be bounded rather than assumed exact.

The price budget remains 0.002 for numerical errors, 0.003 for the baseline
expectation, 0.002 for the residual mean and 0.003 for policy regret. The failure
budget is 0.002 baseline, 0.001 moment acquisition, 0.001 regret, 0.003 ideal
estimation, 0.0005 coherent phase-function error, 0.0005 rotation synthesis and
0.002 physical execution. Bounded-output QAE does not need moment acquisition
or the phase-function oracle; unused allowances are not silently reallocated.

The previously certified q=32 law/clipping/control bridge is below 0.000029
for the stated models in real arithmetic. This follow-up proves complete
integer ranges for f=40/q=32 and bounds the joint arithmetic expectation by
0.000099876, 0.000051936, 0.000011763 and 0.000021978 dollars for C4, C8, H4 and
H8 respectively. Independent internal review found no remaining blocker for
this restricted claim: baseline and correction must use exactly the same
digital policy and decision. The finite-policy regret, its baseline-confidence
transfer and the tight
digital second moment remain distinct obligations. No complete one-cent/99%
continuous-model quantum price is reported.

## 5. Digital source and verified compiler changes

Each random input is an independent q=32 midpoint-uniform variate prepared by
Hadamards. Reversible Box-Muller generation supplies correlated normals without
QRAM or an exponentially large Gaussian table. The financial source uses
40 fractional bits in 72-bit signed words, guarded spots between 2^-16 and
4096, and the archived log-state reset at the conditioning time. Elementary
function coefficient tables, arithmetic floors and the reset are included in
the model bridge. All source temporaries are retained; this deliberately
simple reversible storage policy is not an optimized memory lower bound.

Sound interval propagation over the entire reachable finite support initially
loses correlations in repeated variables. Structural witnesses for normalized
logarithms, interpolation coordinates, exponent range reduction and moment
ratios recover the needed dependencies. The full financial graphs of all four
models have no unresolved signed arithmetic overflow sites. Canonical expression
binding transfers these intervals to the pruned, common-subexpression-eliminated
source without assuming graph identity from a few test cases.

For a multiplication with certified signed operand widths a and b, we retain
n=min(w+f,a+b) product bits. Unsigned partial products plus the two signed
correction terms compute the signed product modulo 2^n; the double-sign term
vanishes modulo 2^n. The output is the f-shifted slice, sign-extended when the
entire product is shorter than the output. The clean XOR circuit is therefore
identical to the original fixed-point multiplication on the certified domain.
Outside that domain it remains reversible but need not compute the same value.

Parallel source schedules group independent leaves by dependency level and
allocate disjoint input/scratch slots to every simultaneously active leaf.
Copies from a shared SSA control are charged in separate rounds. Inverse waves
repeat the clean XOR leaves in reverse dependency order. This is a valid
coherent inverse on their clean-workspace subspace. It does not assume a
serial-depth count is an optimal schedule or free shared workspace.

| Source | New T count | New wave T depth | Source logical qubits | T improvement | Depth improvement |
|---|---:|---:|---:|---:|---:|
| C4 f40 | 568,839,250 | 11,609,892 | 855,344 | 2.3684x | 38.4312x |
| H8 f40 | 2,089,294,634 | 15,258,820 | 3,153,512 | 2.3894x | 108.1126x |

Improvements use the preceding exact truncated-multiplier serial source as the
denominator. Whole-source basis execution checks the emitted primitive gates,
nonzero output XOR, preserved inputs and cleanup against exact integer targets.
Exhaustive small-width tests and production edge cases supplement the proofs.
They are not executions of the complete quantum estimator.

## 6. Explicit estimators

### 6.1 Variance-sensitive Hadamard schedule

Suppose E[Y^2]<=s^2 and the current mean interval is [a,a+W]. For rational
0<c<1 set e=W/(1+3c), `t=a+c*e`, z=(Y-t)/N and epsilon=e/N, with N a power of two.
Since |t|<=s, sqrt(E[z^2])<=s0=2s/N. Theorem 3.21 of [2] bounds the eigenphase
of U=(2|psi><psi|-I)diag(exp(-2i atan(z))) on a spectral event of probability
at least 1-2/C^2, for `C*s0<1`. Writing m=|E[z]|, safe bounds are

    2m/(sqrt(1+s0^2)*(1+C*s0)) <= |theta| <= 2 asin(m/(1-C*s0)).

The maintained interval also gives `m<=(1+2c)*epsilon`. One Hadamard test with
controlled U^T has plus probability `E[(1+cos(T*theta))/2]`. Interval-certified
trigonometric bounds distinguish `m<=c*epsilon` from m>=epsilon. We select an
integer T and an integer count threshold; exact rational binomial tails bound
both errors. Stage allocations sum to 0.003. If the test says small, retain
[a,a+qW], and otherwise [a+2cW/(1+3c),a+W], where q=(1+c)/(1+3c). Both updates
remain valid for permitted answers in the ambiguity gap. Exact rational
controller intervals prevent accumulated endpoint drift.

The selected C4/H8 tight-moment designs use 1,203,320/2,967,610 controlled
iterations, versus 1,540,372,419/6,287,324,746 in the earlier explicit QPE
implementation. This 1,280x/2,119x reduction is a quantum implementation result.
Its tight second moments are still conditional on digital transfer. The phase
source is f=64; actual previously certified Clifford+T rotation strings are
reused, with their new multiplicities paid.

### 6.2 Unconditional digital bounded-output schedule

The digital residual obeys |Y|<100. Add 48 uniform selector bits u and compute
`u<raw(Y)+128*2^40`. The exact flag probability is p=E[(Y+128)/256]. The shift is
an exact high-bit flip in the relevant signed word, followed by a clean
comparator. No data-dependent rotation or second-moment certificate is needed.
The controlled Grover iterate computes financial source, selector, predicate
phase, selector inverse and financial inverse, then reflects on all random
and selector bits with the controlled relative sign retained.

The standard QAE bound is `2*pi*sqrt(p*(1-p))/M+pi^2/M^2` with success at least
8/pi^2 [3, Theorem 2]. Uniformly bounding `sqrt(p*(1-p))` by 1/2 gives M=524,288
for the required mean error. Fifteen repetitions and a median bound failure
below 0.003 by an exact binomial calculation. The total is 7,864,305 controlled
iterations. State preparation, both inverse passes, reflections, IQFT and
synthesized rotations are included. This establishes a digital residual mean
estimator, not the full continuous-model price.

## 7. Combined costs and conditional capacity

The following results include the new source, explicit estimator and actual
synthesized rotations. Seconds are a deliberately favorable sensitivity at
one nanosecond per scheduled T layer with Clifford time and physical overhead
set to zero. They are not quantum hardware timings.

| Method | Model | Total logical T | Logical qubits | Scheduled seconds at 1 ns/T layer | 10x budget, seconds |
|---|---|---:|---:|---:|---:|
| Hadamard, conditional tight moment | C4 | 6.9976e14 | 879,289 | 19,399.5 | 1.11059 |
| Hadamard, conditional tight moment | H8 | 6.2381e15 | 3,182,449 | 58,849.2 | 1.38472 |
| Bounded QAE, unconditional digital support | C4 | 4.4738e15 | 857,599 | 91,501.7 | 1.11059 |
| Bounded QAE, unconditional digital support | H8 | 1.6432e16 | 3,160,759 | 120,669.1 | 1.38472 |

Independent tests could run on multiple source copies within an adaptive stage.
Their full workspaces must then be paid. The table is a constructed single-copy
schedule, and its failure does not preclude all alternative scheduling choices.

An orthogonal necessary capacity condition is `t>=N_T*t_lane*q_lane/P` for P
available physical qubits, `q_lane` physical qubits per T-consuming lane, and
lane interval `t_lane`. It deliberately gives all qubits to consumption lanes and
makes source data, routing and factories free. With P=10^7, `q_lane=1` and
`t_lane=1 ns`, the arithmetic-only Hadamard floors are 0.06997/0.62379 seconds.
Both pass this extremely permissive necessary screen; claiming otherwise would
overstate the evidence. At 17 physical qubits per lane they are 1.18946/10.60439
seconds. These are assumptions about a fixed implementation, not a theorem
about arbitrary quantum computers or native non-Clifford gates.

For the stated 15-to-1 factory family, even a final-stage-only capacity bound
with all ten million qubits assigned to factories, distance 3 and a one-ns code
cycle gives 431.77/3,849.39 seconds for the conditional Hadamard arithmetic.
Lower factory stages, rejection, data storage, routing and synthesis would add
cost. This fails both empirical screening budgets and the fixed-iid C4 budget
of 26.7837 seconds. The actual parallel source allocation also exceeds the
ten-million cap under a distance-3 patch assignment. Other factories, native
resources, storage policies and device models are not ruled out by this bound.

The complete crossover equation is

    Tsetup_Q/A + Tbaseline + Tregret + Tmean + Tphysical_IO <= Tclassical/10,

where A is the declared amortization count. None of these terms may be silently
removed to claim a full price. Positive setup/certification costs strengthen the
failure of the studied mapping. Repeated prices do not amortize the coherent
iterations that must be performed for each required output.

## 8. Reproducibility, limits and conclusion

The repository retains prior evidence and adds separate source, coefficient,
range, estimator, schedule and capacity artifacts. Hashes bind emitted leaves
to manifests; an artifact manifest binds this release. The pinned research
environment and reproduction commands are provided with the companion report.
Separate AI agents review work they did not author; this is an internal check,
not journal peer review or a replacement for named human authors' responsibility.

The financial range proof and digital-estimator guarantees do not imply a
completed continuous-price certificate. Policy regret, baseline confidence and
tight-moment transfer must retain their explicit status. No device layout or
decoder was validated, no full QAE price was simulated or run on hardware, and
no held-out advantage confirmation was attempted. The possible benchmark
contribution requires human mathematical review and an editorial assessment of
novelty before submission.

**No defensible significant quantum advantage established yet.** The work
removes substantial implementation weaknesses without closing the practical
crossover. The result is useful evidence about this compiled workload; it does
not fulfill the original advantage objective or establish an impossibility
result. A future reopening needs a quantified change in complete execution
cost, not a relabeling of the implementation improvements reported here.

## Data, code and assistance statements

Source and generated evidence are in the accompanying repository under
`research/controlled_priority_completion`, `results/controlled_priority_completion`
and `docs/controlled_priority_completion`. The release manifest specifies the
exact artifacts. A permanent archival DOI and an author-approved data statement
remain to be supplied before submission.

AI coding assistants were used extensively in investigation, implementation,
derivation, internal review and drafting. Named human authors have not yet
approved this draft or certified their responsibility for it. Author contributions,
funding, competing interests, originality and concurrent-submission declarations
must be supplied and approved by those authors; none is inferred here.

## References

1. Blanchet, Hamoudi, Szegedy and Wang. *Quantum speedup of non-linear Monte
   Carlo problems*. NeurIPS 2025. https://arxiv.org/abs/2502.05094.
2. Kothari and O'Donnell. *Mean estimation when you have the source code; or,
   quantum Monte Carlo methods*. SODA 2023. Theorem 3.21, equations (48)-(55),
   Section 3.6 and Lemma 4.3. https://arxiv.org/abs/2208.07544.
3. Montanaro. *Quantum speedup of Monte Carlo methods*. Proceedings of the
   Royal Society A 471 (2015), corrected arXiv version, Section 2, Theorem 2.
   https://arxiv.org/abs/1504.06987.
4. Chakrabarti et al. *A threshold for quantum advantage in derivative pricing*.
   Quantum 5, 463 (2021). https://arxiv.org/abs/2012.03819.
5. Wang and Kan. *Option pricing under stochastic volatility on a quantum
   computer*. Quantum 8, 1504 (2024). https://arxiv.org/abs/2312.15871.
6. Herman et al. *Quantum Speedups for Derivative Pricing Beyond Black-Scholes*.
   arXiv preprint (2026), Sections 4.2-4.3. https://arxiv.org/abs/2602.03725.
7. Lemaire, Montes and Pages. *New weak error bounds and expansions for optimal
   quantization*. Journal of Computational and Applied Mathematics 371 (2020),
   Sections 4.1 and 4.2.2. https://arxiv.org/abs/1903.10330.

The linked primary records are the source of record. Reading depth and known
access limits are recorded separately in the focused novelty audit.
