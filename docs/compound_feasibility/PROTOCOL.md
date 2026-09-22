# Compound Asian-basket feasibility protocol

Frozen 22 September 2026 before acquisition. Earlier manuscripts, results and
confirmation cases remain unchanged. This is a new direct-pricing contract.

Price exp(-r*tau) E[(C_tau-Kc)+], C_tau=E[exp(-r*(T-tau))
(A_T-K)+ | F_tau]. A_T averages all assets and all contractual monitoring dates,
including accrued fixings before tau. GBM transitions at monitoring dates are
exact in real arithmetic. No SDE time-step bias is manufactured. Spot100,r=.03,
tau=T/2, equal weights and equicorrelated Brownian drivers.

Development cases, fixed before outcomes: C4 (4 assets,12 dates,sigma.2,rho.2,T1),
C8 (8,12,.4,.2,T1), H4 (4,12,.4,.7,T3), H8 (8,24,.4,.2,T3), all inner strike100.
Outer strikes 3/6/9, priced and reported separately; these are financial dollar
strikes, not selected after looking at outcomes. No confirmation claim is made
from this development grid. A larger confirmation remains gated.

Accuracy: $.10/$.03/$.01 absolute, 99% per-price confidence. Significant advantage:
10x total latency versus best eligible classical algorithm, robust across a
separately frozen 24-case confirmation region (20/24 at10x, all at least3x),
with complete matched accuracy. Retain 10m physical-qubit/60s planning screen.
Empirical scramble intervals will not be called rigorous financial certificates.

Classical methods: exact-monitoring GBM with Brownian bridge/PCA; analytic
conditional geometric-Asian control; moment-matched and independently trained
residual-regression policies; independent policy lower bounds and Jensen upper
bounds from unbiased conditional averages; antithetic nested MLMC/RQMC.
Future returns may be reused across states and strikes, with setup charged.
Training/validation/evaluation randomness is separate. Source seed root2026092401;
training2026092402, evaluation2026092403, reference2026092404. All seed children
recorded. Start16 scrambles, outer2^10--2^12, inner2^2--2^8; escalate selected
development allocations to32 scrambles and outer2^14 if needed. Preserve failures.

Use a bounded inner payoff with cap chosen by an analytic lognormal call-tail
bound <=$.0005 for each case; publish the cap and restore that deterministic
allowance when bounding the original uncapped contract. Same cap on both sides.
No sample maximum supplies a support bound. Control means for capped geometric
payoffs use analytic call spreads. Conditional controls remain unbiased.

Quantum: implement the nonlinear paper's quantum-inner approximation hierarchy,
not naive double amplitude estimation. Produce explicit integer QAE sizes,
coherent-median repetitions, outer signed variance-sensitive estimation schedules,
source/inverse counts and a charged GBM/payoff macro from real compiled blocks.
Do not turn unknown modern-estimator constants into unit cost. Report a separate
optimistic ideal-source sensitivity; distinguish it from a constructed algorithm.
Uniform conditional raw second moments are required, not pooled sample variance.
Charge loading, inverses, controls, decoding and FT overhead or mark them open;
an incomplete cost screen can reject its construction, never establish advantage.

Validate deterministic/analytic cases, conditional control means, factorized
payoff against direct paths, telescoping, pointwise bounds and quantum hierarchy
on independently enumerable toy distributions. Pilot CPU budget16hours/16GiB,
no paid services. Stop scaling after a failed cost gate; do not silently replace
the financial question with CVA/risk or move accuracy thresholds.
