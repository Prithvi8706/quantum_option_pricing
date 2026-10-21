# E12 near-one lambda alternative, static proposal version 1

This packet proposes one new bounded confidence rule for the exact C4/compound-strike-6 finance screen retained by the other continuation. It adds `lambda=15/16` to the sixteen original dyadic lambdas. The resulting symbolic all-zero CS intercept is `64/5`; whether the financial floor passes its unchanged target has **not been calculated**. This is a mathematical and static proposal only: no implementation, READY, prepared protocol, numerical screen, statistical trace, or financial acquisition is created or authorized here.

The completed main E12 v1 Bernoulli toy remains a conditional component. Its successful manifest does not certify a financial observation source. The continuation's rejected financial screen remains an immutable result of its original fixed stopping rule; this proposal neither changes its bytes nor retrospectively repairs that result. Both histories, their methods, and the exact financial support enclosure and target are pinned in the companion JSON. Pinned manifest bytes are historical evidence, not a fresh recursive runtime verification.

## Fixed financial selection and copied premises

The selection remains exactly original uncapped C4, compound strike 6. The retained protocol gives the squared support as `B^2 = 10000*exp(-3/100)` dollars squared, from strike 100 and half-maturity discount `exp(-.015)`. The following strings are copied verbatim from `finance_admission.json`, whose SHA256 is `8fd4839d293686c40e34c5e2c156218871f9a1b2e27b3396ce934f6db9a372bc`:

```
B2_lower = 9704.4553354850817693252835195919433348673681552894362053211350044158042970360191
B2_upper = 9704.4553354850817693252835195919433348673681552894362053211350044158042970360193
T_dollars_squared = 0.19448064336973883
N_cap = 2^20 = 1048576
inner_group_size = 16
```

The endpoints enclose the retained ideal support expression; their existence is not a proof that an actual rounded residual evaluator obeys that support. The target is an archived desired certificate-quality literal, not an endorsement of the original pseudorandom or rounding premises. Neither the cap, target, support, selection nor group size may be tuned after a future freeze. The second moment stream retains its separate allocation; it does not inherit an unproved observation law merely because this selected C4 screen has a recorded bound. Each instantiated stream must have its own same-law support, target and observation definition admitted before acquisition.

For a prospective selected stream, freeze the financial observation as an outer-group average of squared single-path residuals:

```
X_i = (1/16) * sum_{l=1}^{16} Y_{i,l}^2 / B^2
S_n = sum_{i=1}^n X_i
V_n = sum_{i=1}^n X_i^2
mu = E[X_i] = E[Y^2]/B^2
```

This requires `0<=X_i<=1`, IID outer groups, fresh disjoint conditional IID inner draws of fixed size 16, independence across groups, and a policy trained independently and then held fixed. The common outer state can induce dependence within a group; each complete group is the one bounded IID observation. Condition on the independent policy training. Individual Sobol points, shared future factors across groups, adaptive inner sizes and policy refitting do not satisfy these premises without another theorem. Averaging `Y^2` preserves the desired moment by the tower property; squaring the average of `Y` changes it.

Choose the predictable predictor zero. For general finance data `V_n=sum X_i^2`, **not** the Bernoulli count shortcut from main v1. This extra sufficient statistic squares the bounded group observations; it does not redefine the target as a fourth moment. Finite residual evaluation, normalization and summation must be certified or enclosed outward. An implementation must preserve sound sides of every comparison, including the squared sufficient statistic; simply reusing nominal rounded samples is not an admitted exact observation source.

## Boundary and complete failure allocation

[Howard, Ramdas, McAuliffe and Sekhon, Theorem 4 and Lemma 1](https://arxiv.org/html/1810.08240v5) support a uniform empirical-Bernstein boundary with predictable bounded predictions and empirical squared prediction errors. This proposal uses their linear-boundary construction with a conservative rational cumulant majorant, not a mixture-boundary implementation:

```
Lambda = {15/16} union {2^-j : j=1,...,16}
psi_E(lambda) = -log(1-lambda) - lambda
psi_bar(lambda) = lambda^2 / [2*(1-lambda)]
u(V) = min_{lambda in Lambda} [12 + psi_bar(lambda)*V]/lambda
```

For every fixed `0<lambda<1`, the power series gives `psi_E(lambda)=sum_{m>=2}lambda^m/m <= psi_bar(lambda)`. Thus replacing each valid boundary by this larger boundary preserves its guarantee, including at `15/16`. The lambda grid has exactly seventeen members and stays fixed. All signs and all lambdas are included in the failure union, even if one boundary never wins.

Reserve total financial moment failure `1/1000` for two streams. Each stream receives `1/2000`; split it into CS `1/4000` and fixed-N fallback `1/4000`. The CS has 34 sign/lambda processes per stream. Allocate `1/136000` to each process, so `34/136000=1/4000`. Both stream allocations remain reserved even if only one source is instantiated. Across two streams the CS plus fallback total is `1/1000`. A union bound requires no independence between the two streams or between their intervals. The other retained price allocations remain surrogate `0.002`, regret `0.001`, quantum mean `0.004`, and physical `0.002`; none is borrowed by this proposal.

For a later exact finite screen, the logarithm majorant must be proved by the strict rational check

```
L_64(a) = sum_{k=0}^{64} a^k/k! < exp(a)
L_64(12) > 136000
```

This reuses main v1's exact recurrence with 64 increments after its constant term. Main v1's already checked weaker assertion `exp(12)>64000` does not by itself justify the new allocation. The stronger inequality above is a prospective required check; it is **not evaluated in this proposal**. Failure of either exact logarithm check rejects the candidate without tuning the intercept or family.

With the admitted source, a CS upper bound for the original moment is

```
U_CS(n) = B^2 * [S_n + u(V_n)]/n.
```

The frozen looks are `n=2^j`, `j=1,...,20`; no look above `N_cap` is permitted. Stop at the first look with the conservatively enclosed, untruncated `U_CS(n)<=T_dollars_squared`. Interval clipping to `[0,1]` is allowed for display but cannot trigger success. The family is finite and is not claimed to supply arbitrarily small tolerances or an asymptotically vanishing radius for all positive-variance sources.

For `d=2^j`, the dyadic branch is `12*d+V/[2*(d-1)]`. The new branch is

```
b_near(V) = 64/5 + (15/2)*V.
u(0) = 64/5.
```

These are symbolic identities. The near-one branch lowers the zero-observation intercept but penalizes positive squared observations more heavily. It need not win at positive `V`; all sixteen existing dyadic branches are retained and paid in the confidence union.

## Fixed-N fallback

[Maurer and Pontil, Theorem 4](https://arxiv.org/pdf/0907.3740) gives the fixed-N empirical-Bernstein inequality for IID observations in `[0,1]`. For one stream's fallback allocation `1/4000`, each sign receives `1/8000`; its logarithm is `log(16000)`. The future exact check is `L_64(10)>16000`, which permits the conservative radius

```
v_n = [V_n - S_n^2/n]/(n-1)
r_F(n) = sqrt_upper(20*v_n/n) + (70/3)/(n-1)
U_F(n) = B^2 * [S_n/n + r_F(n)].
```

The fallback is assessed only at the fixed cap. Repeated inspection of it with its fixed-N allowance would be invalid. `sqrt_upper` is the minimal upper enclosure on the dyadic grid `2^-64`, obtained with integer square root and validated by squaring it and the preceding grid point. The exponential and square-root checks are future exact computation, absent from this authoring step. Main v1's toy cap guarantee is not transferred to this larger-support, different-target finance rule. If neither CS nor fallback certifies the unchanged target, the result is undelivered; a support-only bound may be reported as such but cannot be relabelled a target delivery.

## Prospective zero-floor screen and positive-V frontier

Because `S_n,V_n>=0` and every branch has intercept at least `64/5`, the smallest CS upper endpoint possible at or below the cap is the all-zero endpoint at the cap. The future screen must use exact rational decimal parsing and record the following directed decisions before any financial draw:

```
CS_lower_floor = B2_lower * (64/5) / N_cap
CS_upper_floor = B2_upper * (64/5) / N_cap
if CS_lower_floor > T: reject every permitted CS look
if CS_upper_floor <= T: necessary zero-floor gate clears only
otherwise: unresolved support-enclosure comparison; do not claim clearance

F_lower_floor = B2_lower * (70/3) / (N_cap-1)
F_upper_floor = B2_upper * (70/3) / (N_cap-1)
if F_lower_floor > T: fallback cannot certify this target at the cap
if F_upper_floor <= T: fallback necessary zero-floor gate clears only
otherwise: unresolved support-enclosure comparison
```

Here `T` is the copied dollars-squared target. Clearing a necessary all-zero screen proves neither a useful positive-data boundary nor IID, support, rounding, acquisition or latency premises. If both channels are ruled out, reject this fixed candidate before acquisition. Rejecting the near-one branch alone does not reject the seventeen-branch CS. The old continuation's numerical floor and rejection apply to its original rule only; they are not substituted into these new comparisons. **All four new floor values and every comparison result remain unevaluated/null in this packet.**

For any fixed branch, the exact ideal-support delivery condition includes the empirical mean contribution:

```
S + 12/lambda + [lambda/(2*(1-lambda))]*V <= n*T/B^2
V <= [2*(1-lambda)/lambda] * [n*T/B^2 - S - 12/lambda].
```

For a sufficient conservative certification use `B2_upper` in the denominator on the right and enclose `S,V` soundly. For the near-one branch this is

```
S + (15/2)*V <= n*T/B2_upper - 64/5
V <= (2/15) * [n*T/B2_upper - S - 64/5].
```

The right side must be nonnegative. Omitting `S` yields only a weaker necessary radius condition and is not a positive-data delivery test. At a fixed `n,S`, existence of a qualifying branch in the full CS is equivalently

```
V <= max_{lambda in Lambda}
     [2*(1-lambda)/lambda] * [n*T/B2_upper - S - 12/lambda],
```

with a nonnegative right side. This is a frozen symbolic frontier, not data-driven retuning. Nonnegative bounded data obey `S^2/n<=V<=S<=n`; these constraints may be used in a later proof without manufacturing favorable observations. A lower support endpoint can prove impossibility; it cannot replace the upper endpoint in a sufficient delivery claim. No threshold is numerically evaluated here.

## Required future packet and fixed budget

One future exact **static screen** candidate may be implemented only after independent ROOT review of this proposal and a new separately frozen implementation/method packet. It must calculate the two rational exponential checks, the CS and fallback floor enclosures at the twenty frozen looks, and exact symbolic coefficient/intercept frontiers for all seventeen lambdas. It must use the pinned selected C4 support strings and target directly. It draws no Bernoulli or financial samples, generates no gates and probes no residual source. No lambda, cap, target, precision, allocation or policy revision is permitted after that future freeze. A censored or rejected candidate remains retained and is not silently rescued.

Fix pure standard-library integer/Fraction arithmetic under the retained local Python 3.12.4 launcher with `-I -S -B`; no scientific helper import, NumPy, mpmath or floating-point stopping decision is permitted. Decimal support endpoints and target must be parsed exactly from their retained strings. The square-root grid is exactly `2^-64`. The rational exponential recurrence has exactly 64 increments after its constant term. Financial observations and seeds in this future static screen remain zero/absent.

Each future prepare/run phase keeps 180 process-CPU seconds, 150 admission CPU seconds and 600 wall seconds anchored to actual Windows process creation; one process, no subprocess or numerical-library threads. Fix runtime retention at 4096 files/512 MiB, frozen retention at 16 files/8 MiB, owned retention at 16 files/16 MiB including the manifest, and an individual-file cap of 64 MiB. The companion JSON pins twelve immutable history files. These twelve plus this two-file proposal, one future implementation, and one new ROOT_READY exactly fill the sixteen frozen slots; a larger packet requires a separately reviewed successor rather than an implicit cap increase. Runtime inputs stay separate and all caps must be checked prospectively and again against actual final bytes.

The prospective route name `results/limitation_program_20261001/E12_near_one_lambda_static_screen_run001` is reserved in the proposal only. This author creates no route. ROOT_READY and protocol hashes must be independently issued before a future prepare/run; no CLI or approval is supplied here. A future implementation must admit those exact expected hashes, retain source/runtime/path/cache presence and absence, use exclusive writes and `RUN_STARTED`, retain authoritative failure markers, check the complete fresh terminal inventory, and enforce manifest-inclusive ownership caps. Existing main and continuation outputs may only be read as the pinned historical inputs, never overwritten or resealed. The historical integrity manifest covers its declared metadata scope and does not certify complete financial runtime provenance.

Even a favorable static screen leaves finance acquisition unauthorized. Same-law IID sampling, a proved original residual bound, independent fixed policy, finite arithmetic certification, both instantiated stream definitions, full price failure accounting and a charged complete acquisition-plus-estimation comparison against fixed-N/analytic/support alternatives are still required. An increased algebraic opportunity does not establish quantum advantage or a financial sample/latency reduction.

All new program fixture credit, statistical and financial draws, financial replays, quantum emissions, finance/source adoption, G2/G3 transfer, comparator delivery and performance claims are zero or false. ROOT owns ledger and actual execution. This work is local only; no executed bytes, namespace files, commits, pushes or uploads are changed.
