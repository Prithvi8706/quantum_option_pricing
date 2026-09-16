# Week-12 acquisition/analysis implementation contract

2026-09-16, declared before runtime-pilot or main observations. Complements the
unchanged [design manifest](WEEK_12_DESIGN_MANIFEST.md) and
[policy specification](PROTOCOL_W12_POLICY_V1.md).

`run_w12.py` implements pilot (90) and main (2000 primary + 5400 secondary) rows.
Within each contract/scenario/guard/repetition block, five arms have deterministic
random order. Purpose-separated namespaces are `w12_asymmetric_pilot_v1`,
`w12_asymmetric_primary_v1`, `w12_asymmetric_secondary_v1`, keyed by full trial
identity, selected encoding and pilot/calibration_0/calibration_1/pricing purpose.

Pre-acquisition amendment: archive unit tests initially sampled the first five
pilot-v1 identities using actual C6 profiles in temporary fixtures. No main-phase
identities were acquired. Those test calls invalidate a blanket assertion of no
pilot-v1 exposure, despite no production archive or result-dependent policy tuning.
Use fresh `w12_asymmetric_pilot_v2` for the actual runtime pilot. Primary/secondary
namespaces remain unchanged and unexposed. Tests now substitute fixture profiles
and `TEST_ONLY_week12_*` namespaces for every phase. This correction was made
before production pilot/main acquisition, not after observing study outcomes.
The current attempt counter affects archival order only. All draws are synthetic
binomial samples; no quantum circuits or physical noise are executed here.

Encoding preselection uses metadata before any pilot. Unknown/exhausted bias
precludes acquisition. Evaluator amplitude supplies a Bernoulli sampler only;
the policy receives metadata and paid pilot count, never truth or terminal data.
Clipping the pilot-derived design amplitude is the predeclared out-of-model
forecast fallback; it does not authorize assuming the design readout is correct.
Historical equal-pilot selection radius is stored separately from the common
delta diagnostic. Unequal-full versus historical equal-pilot changes the search
menu and forecast as well as symmetry; it is not a symmetry-only causal ablation.

Before each attempt and draw, append/fsync a started event. Persist every completed
draw's counts and resource totals before proceeding. Freeze the selected plan
before terminal calibration/pricing. Persist each completed row exclusively before
the completed event. On failure, retain events, any raw rows, failure.json and
no completion manifest. A started draw without completion is an unresolved cost,
not silently zero. A row saved before interruption may lack a completion event;
the strict verifier rejects it rather than overwriting/resuming it invisibly.
Exception diagnostics never append to a potentially torn event log. Separate
failure/recovery artifacts are attempted independently; if storage remains
unavailable, the original error is preserved and successful diagnostics are not
assumed. Resource recovery relies on the surviving valid prefix.
Failed/partial campaigns remain separate evidence; do not report only survivors.
`w12_recovery.py` reconciles failed/unsealed archives without requiring a completion
manifest. It records started/completed/unattempted states, known consumed resources,
upper bounds on unresolved in-flight resources, and failure-penalized outcomes for
every started attempt. Unattempted trials are not silently successful or acquired.
Torn final event/row writes are flagged, preserving the valid event prefix and
known resource lower bounds. A torn event tail makes resource accounting incomplete;
unknown missing events are not silently assigned zero resources. Interior corrupt
events or violations of draw order, plan counts, arm requirements and total budget
are rejected. Complete archives require exact event replay with no truncated tail.

Logical CX uses archived k=0 pricing-CX per shot, charging pilot+pricing.
Computational-basis calibration has zero modeled CX but nonzero shots; this is
an explicitly limited logical model, not end-to-end physical runtime or matched-CX
comparison. All costs include pilot counts; failure penalty 65536 is an analysis
convention kept separate from actual consumption.

## Runtime gate and stopping

Pilot soft acquisition cap is 900s. After a COMPLETE 90-row pilot, define
`projection_seconds = 4 * 7400 * max(max_row_seconds, acquisition_seconds/90)`.
The factor four reserves acquisition plus replay and a factor-two safety margin;
fsync/record overhead is included through observed per-row or aggregate time.
Strictly verify the pilot first; permit main only when this projection <=7200s.
Main acquisition soft cap is 3600s, reserving the other hour for verification.
An overall 7200s monotonic deadline begins before main's pilot verification/setup
and applies to acquisition and the automatic final replay. It is checked between
trials/replay rows; an individual operation may overrun slightly. A deadline failure
is reported, never promoted to successful workflow completion. Pilot evidence is
copied intact into main's archive; main verification rechecks that preserved gate.
Soft caps are checked between trials, not mid-binomial batch. A partial run fails
the completeness gate. Do not tune the policy or thresholds on pilot outcomes.
Any runtime amendment must precede main and preserve the first pilot.

## Analysis and interpretation

Each complete primary/secondary cell reports pointwise 95% CP delivery,
interval-miss and erroneous-declaration proportions, unconditional and among
declarations; a zero declaration denominator is null, never zero estimated risk.
Report actual/penalized mean shots with approximate t intervals, logical CX,
missing intervals, forecast/observed radius on comparable rows and optimism count.
Individual intervals are descriptive, not simultaneous or ratio/noninferiority
tests. Raw rows retain allocation and count-level detail for independent checks.
Additional summaries include interval-conditional misses, success-conditioned
actual costs, conservative CP-difference intervals using a .025 per-arm error
budget, and approximate delta-method cost-reduction intervals. No ratio interval
is represented as exact or as a confirmation test.
Primary interest gate uses exactly the predeclared point thresholds against both
fixed comparators; no post-result modification, pooling of primary/secondary cells
or independent-confirmation claim. Trials are independently seeded across arms,
not paired. Cost intervals are approximate and must not be called rigorous.
Inclusive primary boundaries are compared using integer counts/cost sums:
target deliveries >=380, difference >=-8 out of 400, and
20*target_penalized_sum <=17*comparator_penalized_sum. This avoids float boundary
misclassification without changing the original .95/.02/.15 thresholds.

Strict replay checks every inventoried file, producing source/snapshot hashes,
complete schedule and event sequence, raw results and recomputed analysis.
Immutable original archives and source snapshots are retained. Existing Windows
Python environment is reused; cross-platform bitwise replay is not established.
