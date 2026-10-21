# E12 fixed anytime moment-acquisition toy controller, version 1

This is a prospective bounded statistical component experiment for the previously unstarted E12 item. No experiment has been executed under this packet. ROOT must independently review and freeze the implementation and both method files before preparing the one new receipt route. No financial source, law, policy, arithmetic, estimator, or classical comparator is being changed.

## Problem and exact scope

The existing fixed-N moment pilot cannot be inspected repeatedly with its original pointwise failure probability. This component constructs a valid optional-stopping rule for a normalized bounded observation and retains a separately budgeted fixed-N fallback. It tests only Bernoulli observations. Both probabilities and all confidence radii are represented exactly; seeded traces are computational diagnostics, not proofs that pseudorandom samples are independent.

For a later residual with a proved support `|Y| <= W`, the hypothetical normalized observation is `X = Y^2/W^2` in `[0,1]`, and a certified normalized mean upper bound would multiply by `W^2`. This packet supplies no such finance support, IID group, residual-policy, finite-evaluation, or moment-transfer certificate. The original B4/B8 G2 certificate does not establish these different residual premises. Dependent Sobol points are ineligible as individual IID observations.

## Primary theorem and independent derivation

[Howard, Ramdas, McAuliffe and Sekhon, arXiv:1810.08240v5](https://arxiv.org/html/1810.08240v5), Theorem 4, permits any predictable bounded predictor and a sub-exponential uniform boundary for the empirical sum of squared prediction errors. Lemma 1 gives the corresponding linear boundary. The relevant statements and Appendix A.8 were read for this preflight. We choose the predictor zero before observing any data, so the Bernoulli empirical process is exactly its success count `V_n = k_n`.

The following boundary is our conservative finite construction, rather than a gamma-mixture implementation from the paper. For `lambda_j = 2^-j`, `j=1,...,16`, use

```
psi_E(lambda) = -log(1-lambda) - lambda
psi_bar(lambda) = lambda^2 / (2*(1-lambda))
u(v) = min_j (12 + psi_bar(lambda_j)*v)/lambda_j
```

The power series gives `psi_E(lambda) = sum_{m>=2} lambda^m/m <= psi_bar(lambda)` for these positive lambda values. Replacing the original boundary by this larger linear boundary preserves its guarantee. Each sign and each lambda receives failure `1/64000`; the union over sixteen lambdas and two signs is `0.0005`. A strict rational Taylor partial sum of `exp(12)` proves `exp(12)>64000`, so the integer intercept 12 exceeds the required logarithm without floating-point evaluation. For Bernoulli count `k`, an independent algebraic expression is

```
u(k) = min_{d=2,4,...,65536} (24*d*(d-1)+k)/(2*(d-1)).
```

Thus the CS radius is `u(k_n)/n`. It applies uniformly in time under the theorem's bounded conditional-mean assumptions. A constant IID mean is required for this packet's single mean target. The controller looks only at the twelve frozen times `64,128,...,131072` and selects the first radius at most `1/128`. No observed truth, empirical favorable law, or later tuning selects the lambda family, failure allocation, precision, or looks. Clipping the interval to `[0,1]` is allowed, but clipping is not used to make its radius meet the stopping target. All-zero observations give `u(0)=24`, not a zero uncertainty term.

Because the lambda family is finite, this boundary has a positive asymptotic radius floor. It is designed for this fixed tolerance and cap; no arbitrary-precision or asymptotically shrinking confidence-sequence claim is made.

## Fixed-N fallback and total failure allocation

[Maurer and Pontil, arXiv:0907.3740v1](https://arxiv.org/pdf/0907.3740), Theorem 4, supplies the fixed-N empirical-Bernstein inequality for IID bounded observations. Applying it to both signs with total fallback failure `0.0005` gives the factor `log(4/0.0005)=log(8000)`. A strict rational Taylor partial sum of `exp(9)` proves this is less than 9. We use the conservative exact radius

```
v_sample = k*(n-k)/(n*(n-1))
r_fixed(n,k) = sqrt_upper(18*v_sample/n) + 21/(n-1)
```

Here `sqrt_upper` is the minimal upper enclosure on the dyadic grid with denominator `2^64`, computed by integer square root. The enclosure is checked by squaring both it and the preceding grid value. No floating-point radius is used in a stopping decision.

At the frozen cap `N=131072`, `k*(N-k) <= N^2/4` implies `v_sample <= N/(4*(N-1))`. Therefore every Bernoulli dataset has

```
r_fixed <= sqrt_upper(9/(2*(N-1))) + 21/(N-1) < 1/128.
```

This deterministic cap guarantee is checked with rational arithmetic before the traces. It is a radius guarantee, not an assertion that every possible dataset covers its true mean. If the CS has not delivered, use this interval at the fixed cap. The data-dependent choice of CS or fallback has total miscoverage at most `0.0005+0.0005=0.001` by a union bound. Reusing either full failure allowance without this split would be invalid. No financial estimation, physical-failure, or other price failure budget is consumed or reassigned by this standalone toy experiment.

## Frozen corpus and actual accounting

Exactly three ideal laws are considered: `p=1/2`, `p=2^-8`, `p=2^-16`. There are sixteen frozen seeds, integers `202610040000` through `202610040015`, per law. Python's local `Random(seed).getrandbits(b)==0` generates deterministic diagnostic traces for a law represented by `b=1,8,16`. It realizes the stated Bernoulli probabilities under ideal IID uniform bits; this pseudorandom implementation is not itself an IID or confidence theorem.

For each trace the experiment actually generates the complete cap-sized sequence so the fixed baseline and the stopped controller use the same observations. It records each frozen look, the first qualifying CS stop, the selected branch, exact radius/interval, diagnostic truth inclusion, and the cap baseline. Claimed sample reductions refer to the controller's selected sample count; they are not measured financial latency reductions. The diagnostic CPU includes complete paired generation for all 48 traces and is recorded separately from total receipt/runtime verification cost. The full generated draw count is `48*131072`, and no generated observation is credited as a program fixture or financial replay.

The frozen algebraic checks cover 510 complete binary histories of lengths one through eight and three exact history-probability normalizations at each length. These are short exact structural diagnostics, not a full-horizon crossing-probability calculation. The statistical coverage proof comes from the stated theorem and complete failure union. Seven rational square-root cases check unique upward dyadic enclosures, and the positive zero-observation term and universal capped radius have explicit checks.

Acceptance means all fixed structural checks, all 48 traces, strict input/runtime hashes, and bounded lifecycle complete. Favorable sample counts are not required to call the implementation correct. The outcome remains a conditional statistical component. Promotion requires an independently certified same-law finance observation source and a smaller complete acquisition-plus-estimation latency than the matching fixed-N/analytic/support alternatives. At most one future finance acquisition is permitted under a separate frozen packet and the plan's cap; this packet executes none.

## Admission, runtime and preservation

The only new scientific implementation is `experiment_e12_anytime_moment_v1.py`; the existing fixed-N source is read solely as a pinned reference and is never imported. The other pinned references are the original roadmap and its statistical audit document. The root READY contains exactly these six source/method/reference hashes. Its required header is `root-e12-anytime-moment-static-READY-v1`, with `passed=true`, `static_review_only=true`, `scientific_execution_approved=true` for this bounded toy, and `financial_adoption_approved=false`. ROOT creates and hashes this new READY file. The program adds the READY hash to its frozen input map; old expected hashes are never replaced by observations.

Invoke the actual pinned launcher by direct script using `-I -S -B`. These flags isolate Python from environment/user paths, disable site startup hooks and site-packages, and prohibit bytecode writes. Exact `sys.path`, executable, base prefix, prefix, absent `python312.zip`, and loaded module origins are checked. The complete installed `Lib` tree excluding unused site-packages, complete `DLLs` tree, all base-directory regular files, and the workspace launcher are captured, including existing bytecode caches. Every loaded module origin and existing declared cache is covered. No workspace scientific module is imported. Standard library and interpreter hashes are separate external-runtime inputs; they do not assert that Windows system DLLs or the whole OS have been hashed.

The root-created READY is prerequisite to `prepare`, which does no bound evaluation or sampling. Prepare captures the prospective runtime hashes and writes the one `protocol.json`, then performs complete fresh source/runtime/protocol verification before reporting its hash. ROOT then reviews and freezes the protocol hash before `run`; a required CLI argument admits only those prospective bytes. That original protocol expectation is retained through both fresh run unions and the final owned-file hash at sealing; a changed protocol cannot acquire authority through a new observed hash. Run checks full runtime membership and hashes before and after computation, without expected-hash waivers. Both source and runtime files must be stable during each read, including Windows file-attribute/reparse identity, and retain exact resolved absolute paths before and after reading. Runtime directory aliases, loaded-origin aliases and loaded-cache aliases are rejected. Runtime file membership additions/removals fail the comparison. Every loaded absent cache route is recorded in the prepared protocol and must remain absent, including no dangling cache alias, at run admission and terminal verification. The absent standard-library ZIP receives the same check. ROOT_READY itself counts toward the frozen-file and frozen-byte caps.

Each prepare/run phase has 180 process-CPU seconds, admission stops at 150 CPU seconds, and 600 wall seconds anchored to the actual Windows process creation time. Work checks occur throughout inventory/hash loops, exact checks, per trace and per block of at most 4096 draws. There is one process, no subprocess, cloud, GPU, or numerical-library thread. Limits are 4096 runtime files/512 MiB, 16 frozen files/8 MiB, and 16 owned files/16 MiB; no file exceeds 64 MiB. These limits are prospective and are not silently raised.

The sole output route is `results/limitation_program_20261001/E12_anytime_moment_run001`; it must not exist before prepare. A run requires the route contain only the frozen prepared protocol. After complete admission and before any structural checks or traces, it exclusively creates `run_started.json`; no repeated run can satisfy the fresh-route predicate. Successful owned members are protocol, run_started, checks, traces, summary, verification, and manifest. All JSON outputs use exclusive creation, guarded incremental encoding/IO and exact UTF8 newlines. Each exclusive write checks the prospective remaining owned file/byte capacity while encoding, and checks exact complete actual ownership afterward; prepared protocol retention therefore obeys16files/16MiB before prepare can report success. The manifest's own map excludes its self-referential bytes; ROOT records its SHA separately. Its complete prospective encoding nevertheless counts toward the16-file/16MiB ownership caps before it is written, and the full actual final inventory/count/bytes are checked again after writing. Only the exact complete success members are admitted at sealing; a failure marker or extra member cannot enter a successful manifest.

One outer failure handler covers prepare failures after route creation and run admission, numerical and sealing failures. Guarded failure metadata is retained when the normal clocks allow it. An exclusive minimal `FAILED_UNSEALED.json` is retained on any owned incomplete attempt, even when the ordinary hard clock cannot permit normal serialization. It explicitly invalidates partial success, leaves the hard-budget state uncertified and carries zero fixture/finance credit; it is not a continuation or scientific budget exemption. A manifest written just before a later guard failure is overridden by this authoritative marker. No failure is resealed, retried or overwritten, and accidental calls against an already executed/sealed route do not acquire ownership of its bytes. No partial trace delivery approves a controller or financial result. The manifest time is a pre-seal snapshot and final printed timing is a later observed process snapshot, rather than a claimed operating-system exit CPU reading.

All program fixture credit, financial replays, quantum emissions, financial G2/G3 transfer, classical-comparator status, source adoption and physical runtime claims remain zero or false. ROOT owns progress registration; this author does not modify the live ledger or any executed/frozen file. No commits, pushes, uploads, external application writes, or user-process interference are authorized.

## Exact commands after independent ROOT release

```
.context/frontier_t0_env/Scripts/python.exe -I -S -B research/limitation_program_20261001/experiment_e12_anytime_moment_v1.py prepare --root-ready-sha256 <ROOT_READY_SHA>
.context/frontier_t0_env/Scripts/python.exe -I -S -B research/limitation_program_20261001/experiment_e12_anytime_moment_v1.py run --root-ready-sha256 <ROOT_READY_SHA> --protocol-sha256 <PREPARED_PROTOCOL_SHA>
```

Those placeholder digests must be concrete previously frozen expected hashes before an actual command is issued. This author has performed no scientific execution and no fixture generation while preparing this packet.
