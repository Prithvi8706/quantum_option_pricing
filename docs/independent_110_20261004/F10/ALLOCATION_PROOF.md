# F10 bounded archived-menu allocation audit

This is an accounting and conditional allocation decision for the existing A1/A4
antithetic Heston development menu, not a new workload. The fixed contract has
twelve contractual monitoring dates, levels 0--5 with 12,24,48,96,192,384 internal
steps, and tolerances 0.10,0.03,0.01. It is distinct from the GBM G0 B4/B8 menu.
The two archived precisions are f=24/32. Every one of the 64 assignments of these
six levels to classical or quantum estimation is retained for each row: 768
assignments. No sampling, pilot, compilation or performance measurement occurs.

The archived approximately 570--600-fold antithetic correction variance benefit
is retained as historical component evidence shared by both architectures. This
audit neither reacquires nor promotes that component to a population certificate.

## Explicit conditional premises

For each level, select the existing iid MC pilot: unconditional level-0 power 12,
and unconditional correction powers 10. Let m_l and v_l be its archived decimal
mean and sample variance. The working moment is

    H_l = 4[v_l + 1_(l>0) m_l^2].

The base is about its archived pilot center; correction centers are zero. To
cover decimal reconstruction of the archive's floating arithmetic, the common
working value V_l is max(H_l, all archived schedule second moments for that
case/level) plus max(1,that maximum)*2^-40. This padding is an explicit chosen
model premise, not a statistical confidence certificate. Both the classical
Gaussian floating law and quantum finite circuit law must have second moment
about that center at most V_l before the following calculations apply. Neither
premise is proved by sample variance, observed cancellation, or this padding.
Finite-law, arithmetic and centering bridges remain null. There is no RQMC-as-iid
substitution. Training independence, valid support and exact ideal source are
also conditional assumptions for the archive's quantum schedule.

Fix statistical dollar budget B=9 epsilon/20 and delta_l=1/1500, giving total
statistical failure 6/1500=0.004. The remainder 11 epsilon/20 of the dollar
budget and 0.006 of the failure ledger are unallocated obligations, not valid
bounds. Setup, preprocessing, continuous bias, cap, finite input, overflow,
rotation synthesis, source error, physical failure, decoding and output have
explicit null certified fields. Thus delivered 99% eligibility is false even
when conditional statistical calculations pass.

## Classical finite allocation

For iid samples and E[(Y-c)^2]<=V, variance<=V and Chebyshev gives
P(|mean_n-EY|>=e)<=V/(n e^2). Choose n=ceil(V/(delta_l e^2)), subject to fixed
n<=2^60. This proof includes base uncertainty and allows signed corrections.
It does not require independent level estimators for the union bound, but each
level's draws must be iid under its respective fixed law. The observed archive
is not sampled again. Its timing anchor is (seconds-fit_seconds)/(replicates
times 2^power), used solely in a labelled linear warm-cost extrapolation. No
sample rate, setup, full runtime or matched timing is newly measured or proved.
The archived level-0 fit anchor is always separately charged once, including
when level 0 is quantum; further setup and preprocessing remain null.

Use 64 equal error slots h=B/64. Each classical level receives positive integer
k_l slots, e_l=k_l h. For a fixed quantum subset, subtract its outward-rounded
conditional quantum slots, then minimize sum c_l n_l over the remaining finite
classical allocations. Dynamic programming removes the smallest remaining
level and tries every positive k up to remaining slots. By induction every
feasible allocation appears exactly once in a candidate decomposition. An empty
classical set costs zero and may leave slots unused. Lexicographic slot ties are
deterministic. This proves optimality on this finite grid and conditional cost
model only. No continuous/global optimality or sum of mixed-unit costs is used.
Slots/n-cap failures are retained without enlarging the grid or cap.

## Archived quantum accounting and conditional outward checks

Schedules and bin M/repetition counts are fixed archive inputs, not reoptimized.
For each signed bin, r independent ideal AE repetitions with power-of-two M use
rM source forwards, r(M-1) inverses, r(M-1) of each reflection, and rm QPE
readout bits, m=log2 M. The archive's calls_A=r(2M-1), Grover count r(M-1),
and QFT controlled phase count r m(m-1)/2 are independently recomputed. Its
macro native T count/depth, loader U/CX/rotation envelope, source directions,
and maximum single-QPE serial macro depth are joined using integer arithmetic.
These are source-bound macro compositions from emitted blocks, not an emitted
monolithic financial circuit, certified lower bound, or physical runtime.

Montanaro 1504.06987v3, introduction, Section 1.2, and Section 2.1/Theorem 2 and
proof of Theorem 3, supplies the iid variance inequality, inverse access model,
and ideal AE error 2*pi*sqrt(p(1-p))/M+pi^2/M^2 with success at least 8/pi^2.
This audit's finite schedule and grid are our explicit derivation, not the
paper's hidden-constant algorithm. With pi<22/7, single-repetition bad probability
is at most 23/121. Exact rational odd-majority binomial tails are summed over
signed bins and required <=delta_l. No noise/readout success is inferred.

For centered Y, the lowest bin has upper b between sqrt(V) and 2sqrt(V).
For all disjoint signed bins, sum b_i E[|Y|1_bin] <= b E|Y|+2EY^2 <=4V.
Cauchy--Schwarz gives sum sqrt(b_i E[|Y|1_bin]) <=2sqrt(number_of_bins*V).
Consequently a shared M has ideal total AE error at most

    4*pi*sqrt(number_of_bins*V)/M + pi^2*sum b_i/M^2.

Add V/cutoff for unresolved tail unless the *assumed*, separately uncertified
centered support 1024 is covered. In that conditional support case tail is
mathematically zero, while the actual support certificate remains null. The
archive's identical-M, signed-pair, contiguous-bin geometry and base inequalities
are checked; violations reject conditional certification. Square roots use
isqrt rational outward rounding at 2^-64. Quantum slots are the exact ceiling
of this derived rational upper bound divided by h. This replaces decimal error
fields with an outward mathematical bound under the explicitly assumed V/law.
Failure-budget misses or insufficient fixed slots remain rejected rows.

## Stop and decision scope

Enumerate the menu once. There is no scalar conversion from logical gates to
seconds, and no selected physical quantum winner. Check six historical hybrid
fixed allocations with free corrections: remaining warm base time plus observed
fit time must exceed the archive's warm total/10 to close that fixed allocation
under those legacy cost assumptions. This is an exact comparison of archived
decimal observations, not a bound on retuned methods or hardware. The broader
base-mean replacement and missing analytic coarse mean belong to F11. An
analytic geometric GBM control does not supply the Heston coarse Asian mean.
No alternative is assigned a fabricated zero oracle cost. Retain the archived
classical/coupling menu, compile no winner, and leave full F10/financial
acceptance unresolved unless its complete prerequisites actually become proved.

Primary source: https://arxiv.org/pdf/1504.06987v3 (local pinned copy). The source
does not provide this finance moment/support/source/runtime certification.
