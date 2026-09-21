# V2C: finite-shot dollar-interval feasibility

Freeze before observing V2C random outcomes. Discovery only; no hardware or
compiled-noise claim. Reuse C6 and the completed V2B representation matrix.

Compare a fixed n=6,c=.125 representation with a deterministic bound-only
selector. The selector maximizes the positive probability-radius allowance for
$1 over V2B's n/c choices, breaking ties by smaller n then smaller c. It receives
only n, c, sensitivity and deterministic bounds, never exact prices/amplitudes.
If no positive allowance exists, record pre-execution refusal and zero quantum
cost. This is not an adaptive pilot controller or a resource-optimal selector.

For every contract/arm, use k=(0,1,2,4,8), shots/depth=(512,8192,32768), 200
independent trials, and conditions ideal, true/known eta=.01, and true eta=.01
inside envelope [.005,.015]. Use the V1 stationary response model, simultaneous
exact binomial inversion at alpha=.05, V2B bias expansion and $1 tolerance.
Baseline: direct k=0 sampling at equal A-equivalent budget (35*shots). Record
refusals for selected and direct arms on infeasible contracts; fixed arms execute
and can still remain unresolved. Keep all six contracts in pooled denominators.

Record raw counts, selected representation, probability containment, full
Black-Scholes-price interval containment, completion, incompatible/refused state,
unconditional and declaration-conditional >$1 errors, interval radius and all
shots/Grover/A-equivalent counts. A-equivalent counts are NOT full pricing costs.
Classical preprocessing/setup times are recorded separately; no speedup claim.
Seeds include version, contract, arm, condition, shot count, repetition and purpose.

Archive source/protocol, baseline hashes, planned cells, raw JSONL and summaries.
Flush/fsync each completed cell and retain first failures; no overwritten retries.
Use <=60 minutes response-simulation time. Exact amplitudes/prices are allowed
only in the data generator and evaluation, after representation selection.
