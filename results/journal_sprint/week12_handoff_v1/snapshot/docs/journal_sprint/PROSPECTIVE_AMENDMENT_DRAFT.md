# Prospective amendment: delivered-precision pricing study

Status: a completed **protocol draft**, not a frozen main experiment and not a retrospective registration of V1–V2C. The July Paper A protocol remains unchanged. V2A, V2B and V2C have their own prospective discovery protocols and immutable outputs. This amendment incorporates their outcomes and the literature review; its confirmation phase has not run.

## Question and promotion rule

Test whether contract-aware representation/resource selection improves delivered dollar precision at a fully counted budget over strong fixed configurations. Keep the conservative fixed procedure as the default. Adaptation is promoted only if confirmation shows a practically material benefit without unacceptable erroneous declarations or hidden refusal costs.

The main outcome is delivery of a finite interval with radius at most the requested tolerance. An erroneous declaration means that delivery was declared but the reported midpoint differs from the independently defined continuous price by more than that tolerance. Report both unconditional error frequency and frequency among declarations; the latter is not guaranteed to be at most the nominal alpha by the existing proposition.

## Targets and representations

Keep distinct the continuous model value, support-conditioned value, implemented finite-grid value, ideal encoded-circuit value, finite-shot estimator and noisy procedure output. Retain signed differences in validation, but use analytical upper bounds—not observed absolute differences—as controller inputs.

Initial discovery candidates remain n=3,4,5,6, c=.125,.25,.5, q_total=1e-5. After a resource smoke test, an explicitly versioned discovery extension may consider n=7,8 and c=.0625. It must preserve old runs and count the new loading costs. Do not silently add configurations after examining confirmation outcomes.

For each candidate compute the payoff transformation `P_circ(a)=L_P*a+b`, with `L_P=exp(-r*T)*(U-K)*2/(pi*c)`. Form deterministic bound `B=B_support+B_grid+B_encoding`. For tolerance tau, a positive statistical allowance requires `tau>B`; the probability-radius allowance is `(tau-B)/L_P`. Failure is a sufficient-bound refusal, not an impossibility theorem.

Absolute tolerance is $1 for direct continuity with V2C. A separate secondary tolerance is 1% of spot, not 1% of the unknown option value. These are research thresholds, not a claim about a trading use case.

## Discovery and confirmation separation

C6 is discovery. The historical 50-contract benchmark has been inspected and must not be relabeled unseen. Use new contracts for confirmation, generated only after the controller and comparator implementations pass discovery gates and their source/configuration hashes are frozen.

Proposed confirmation generator: 24 independent synthetic contracts, spot fixed at 100, log-moneyness `log(K/S0)` uniform on [-.25,.25], rate uniform on [0,.08], maturity log-uniform on [.25,2], volatility uniform on [.1,.5]. Freeze a purpose-separated seed and generated contract manifest in the final amendment before drawing response observations. These ranges define an experimental population, not real-market calibration. Include fixed edge/stress contracts separately and do not mix their results into population averages.

The lead may change this proposal before freezing it, documenting the reason. After any confirmation results are inspected, a method change requires fresh confirmation; old cases become discovery evidence. Do not select only cases with attractive bound feasibility.

## Controller and validation contract

Allowed inputs are contract parameters, candidate menu, analytical bounds, resource profiles, tolerances, confidence budgets and independent pilot/calibration observations. Forbidden inputs are exact target amplitudes, Black–Scholes/quadrature prices, confirmation outcomes and post hoc best-performing choices. Exact answers remain available only to the data generator and evaluator.

The existing V2C selector is a bound-only baseline, not the final controller. A proposed adaptive controller chooses one candidate and one fixed validation schedule, or refuses. Its objective must use expected delivery and full resource cost, rather than residual probability allowance alone. Pilot counts may inform scheduling but may not be reused as if they were an independent fixed validation batch.

The initial menu of depth caps is k_max=0,2,8,32. The exact intermediate ladders, pilot allocation and utility weights must be selected using discovery only and included in the final frozen configuration. Use a separate seed namespace for selection, calibration and validation. Every pilot, calibration, retry and refused task retains a cost record.

Perform one fixed validation batch after selection. Preserve all feasible amplitude components, then use their hull for the reported dollar interval, expanded by the deterministic bound. Do not clip negative lower endpoints to improve apparent width. For repeated validation, first introduce a valid sequential confidence method or preallocated error spending; repeated fixed-alpha testing is forbidden.

## Statistical assumptions and numerical validity

For the response-model tier, observations are independent stationary binomials conditional on the contract and declared noise model. Set alpha_stat=.05 with simultaneous allocation across the fixed validation depths. An illustrative supplied envelope carries no inferred calibration guarantee. The resulting statement is conditional on its validity.

For a future empirically calibrated tier, propose alpha_stat=.04 and alpha_cal=.01, with a simultaneous calibration statement and explicit union-bound argument before use. Deterministic model-discrepancy and numerical-enclosure allowances must be derived separately. A fitted exponential decay or a passed goodness-of-fit test is not a proved noise envelope.

The current 2e-14 numerical padding is a practical safeguard, not a verified floating-point error bound. A formal numerical certificate requires outward-rounded inversion and special-function enclosures or a justified additional enclosure budget. Until then, use “conditional analytical guarantee with tested numerical implementation,” not “formally certified software.”

## Required comparator tiers

| Tier | Required comparisons | Fairness condition |
|---|---|---|
| Representation | Fixed n/c; bound-only selector; proposed controller | Same candidate discovery and full setup cost |
| Quantum observations | Direct k=0; fixed depth-limited inversion; pinned IQAE | Same target and counted A/A-dagger calls |
| Modern estimators | Reproduced geometric schedule; BAE; screen BIQAE | Preserve native interval interpretation; count calibration and fitting |
| Strong low-depth candidates | Screen Erle–Koczor and Huang–Koczor | Full reading/source audit before inclusion |
| Classical European | Black–Scholes; independent quadrature; control-variate MC; scrambled Sobol RQMC | Continuous target and total work, not quantum-style oracle fiction |
| Classical path-dependent | Arithmetic Asian MC with geometric control; RQMC with bridge/PCA | Same monitoring dates; all paths and independent scrambles counted |

BAE and BIQAE are not claimed as reproduced in this sprint. If implementation or licensing blocks a candidate, record that limitation; do not silently substitute a weak method and claim a state-of-the-art comparison. Verify the actual IQAE stopping rule before adopting Miyamoto's correction, and count any fresh-batch overhead.

For RQMC use power-of-two points per scramble, initially 32 independent scrambles, recording all scramble means and total paths. Any interval based on replicate means must state its approximation and be assessed empirically; it is not automatically an exact confidence interval. Estimate control coefficients with independent pilot observations or explicitly account for dependence.

## Circuit and noise gates

Before launching confirmation, verify actual pricing circuits on a small cross-section of n/c choices and depths. Compare objective probabilities with the response generator in the ideal case. For noisy simulation, audit which gates receive each channel, include zero-noise and strong-noise positive controls, and record transpiler/backend configuration.

Test at least depolarizing, asymmetric readout and amplitude-damping examples, with drift/correlation as deliberately out-of-model stress tests. Passing the simple decay model under one channel does not validate it under the others. Keep response-table simulation, full circuit simulation and hardware as separate evidence tiers.

No paid hardware is authorized or required for this draft. Add hardware only after the matched-circuit gate passes and an explicit hardware budget is available. A single-Ry demonstration does not substitute for a pricing circuit.

## Outcomes, resources and inference

Record attempted, executed, nonempty, precision-met, unresolved, incompatible and pre-refused counts. Primary delivery denominators include every attempted contract/trial. Report interval containment among executed trials and among nonempty outputs separately. Failed first attempts are retained and linked to retries.

Count `sum_j N_j*(2*k_j+1)` A-equivalent calls, `sum_j N_j*k_j` Grover calls, shots, circuits, maximum depth, total compiled one-/two-qubit gates, state-preparation and uncomputation cost, calibration, pilot and classical processing. Report host simulation time separately from projected device execution time. Query counts alone do not establish practical speedup.

Proposed confirmation size is 1,000 independent trials per contract/method/condition, contingent on the resource smoke test. At a 95% event rate this gives an approximate standard error of .69 percentage points; use exact marginal binomial intervals for event rates and identify multiplicity. A 200-trial discovery cell cannot resolve tiny differences in reliability. Do not use pooled IID intervals across heterogeneous contracts.

Analyze fixed-benchmark contrasts by resampling within contracts. For the generated population, report a separate hierarchical analysis that includes between-contract uncertainty. Do not infer broad finance performance from a handful of selected successes. Freeze analysis code and primary contrasts before inspecting confirmation.

## Go/no-go sequence

1. Pass target, deterministic-bound and numerical-inversion tests.
2. Pass actual-circuit response and noise positive controls, or explicitly retain model-only scope.
3. Reproduce stronger comparators and classical baselines with complete cost records.
4. Measure time/memory for a tiny discovery matrix and cap total local compute before expansion.
5. Freeze the controller, confirmation generator, budgets, stopping/failure rules and analysis manifest.
6. Run confirmation. A provisional practical benefit threshold is at least 10% lower full counted cost at matched delivery, or at least 10 percentage points higher delivery at matched cost. The final choice and uncertainty rule must be fixed before this run.
7. If adaptation does not pass, publish the fixed-method reliability result only if it is substantively informative; do not manufacture an adaptive win.

## Staffing and publication constraints

The lead owns implementation and analysis. The two limited collaborator packages remain those in [TEAM_WORK_PACKAGES.md](TEAM_WORK_PACKAGES.md); they require genuine independent execution/review and later manuscript approval. Acceptance, actual time and fee ceiling remain unconfirmed. Local-only compute and no paid services are the current operating assumptions, not an invented agreement.

The first-two-week deliverable is this prospective draft and a feasibility decision. Main-matrix execution, transfer validation and submission belong to later stages. No acceptance date or journal outcome is promised.
