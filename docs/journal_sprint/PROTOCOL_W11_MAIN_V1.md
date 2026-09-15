# Week-11 stages B/C acquisition decision

Recorded after stage-A pilot, before any stage-B/C observations, 2026-09-15.
Extends [baseline protocol v1](PROTOCOL_W11_BASELINES_V1.md); no confirmation claim.

Pilot `w11_baseline_pilot_v1` completed 128 main pilot rows and four warmups in
7.8744 acquisition seconds. Replay checked 234 files/132 rows. Peak process
working set: 97,746,944 bytes. Sampled system CPU utilization ranged 0-60%; no
agent-launched concurrent benchmark/test, but external load was uncontrolled.

Feasibility forecast: extrapolate each method/asset/date group's mean N=1024
evaluation time linearly in N, retain setup/training costs, multiply by three
strikes and planned repetitions. This gives 253.02 seconds for stage B and
602.68 seconds for stage C, excluding archive overhead. This is a conservative
planning extrapolation, NOT measured scaling or a runtime result.

Decision: retain full proposed matrices. Stage B: 12 contracts x 32 independent
raw-control scrambles x N=32768 = 384 estimates. Fit each reference coefficient
on its own independent 1024-evaluation pilot; no main/training/reference stream
reuse. Proceed to C only if all twelve reference SEs <= .001; this remains a
diagnostic precision gate, not a formal absolute-error certificate.

Stage C: 12 contracts x four methods x N=1024/4096/16384 x 16 independent
deployments = 2304 estimates. Add four unscored global warmups (one per method
on 2 assets/12 dates/strike 100/N=256) to avoid an unrecorded cold-start exclusion.
Every deployment recomputes its required setup and fits its own 1024-observation
control, except raw RQMC which needs no fitting. Reuse counts 10/100 are only
secondary accounting scenarios, not additional measured workloads.

Methods are permuted within asset/date/strike/N/repetition blocks using a separate
order stream. Purposes `reference`, `main`, `main_warmup`, training and evaluation
are disjoint from stage A and each other. None of the eight reserved held-out
cases is used. Preserve all rows; no accuracy-based stopping or method selection.

Soft wall caps: stage B 15 minutes, stage C 25 minutes, checked between individual
deployments; archive initialization excluded. A cap leaves a partial archive,
not a silently smaller complete experiment. Each stage uses a new exclusive
directory, durable events, source/protocol snapshots, environment/dirty patch,
timing and system-load telemetry. Run stages and regression tests sequentially.

Main analysis is per contract/N/method: reference-relative single-deployment
RMSE; between-deployment SD; approximate 95% t interval for the mean of all 16
deployments; mean setup/training/evaluation/standalone time; and explicit cost
of that 16-deployment mean. Do not attach the mean's interval to single-run cost.
Keep reference uncertainty visible, especially for errors near the reference SE.
Main-tolerance summaries are descriptive, not certified delivery rates. No
quantum speedup, asymptotic slope or general runtime crossover is inferred.
