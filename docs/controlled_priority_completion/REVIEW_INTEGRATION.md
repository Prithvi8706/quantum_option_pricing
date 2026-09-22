# Independent review of combined resources and manuscript claims

22 September 2026. Reviewer: the capacity/publication subagent. The combined
cost code, composed replay and companion manuscript were authored by the root
agent. This is an independent review of those items. Because this reviewer
authored the capacity model, discussion of that model below is a **self-check**,
not a claim of independent capacity validation.

**Finding: no computational blocker found in the combined residual-estimator
resource ledger.** Two draft completions were requested: replace the descriptive
Herman reference with its actual paper title, and put the final reviewed joint
arithmetic bounds and their exact scope in the manuscript itself. A further
replay improvement was requested to use H8's selected normalizer, rather than
only the valid exponent-4 phase input used in its first composed diagnostic.
These requests do not change any T count or the scoped non-advantage result.

## Independent quantitative checks

[capacity_integration_review.py](../../research/controlled_priority_completion/capacity_integration_review.py)
reconstructs the integration directly from financial wave groups, phase wave
groups, random-bit counts, selector resources, exact controlled-reflection
costs, the selected estimator repetitions and actual rotation strings. It does
not invoke `combined_cost.main` or copy its old-minus-new substitution. Its
[SHA-bound output](../../results/controlled_priority_completion/capacity_integration_review.json)
reconciles all six rows.

- Financial forward plus inverse contributes one clean financial-source T count.
  Hadamard adds one clean phase source and its signed controlled reflection;
  bounded QAE adds two clean selectors and the enlarged random-register
  reflection. No costly source is counted as a single classical sample.
- IQFT controlled phases were independently enumerated by wire pairs. Each
  controlled-pi/2 contributes three exact T gates and a valid two-T-layer serial
  schedule. Remaining controlled phases contribute all three constituent
  single-qubit rotations, with their actual target keys and string T counts.
- The f64 phase word contributes all 67 signed fixed-point bits. Negative-angle
  inverses have equal T/T-dagger resources; signs do not remove any factor.
  Rotation-target metadata matches the rational angle used by each multiplicity.
- The prior synthesis library was independently rerun in verify-only mode:
  **95 exact-target interval certificates passed**. The new cumulative operator
  error bounds are below the reserved 0.0005. Treating serialized rotation T
  counts as added T depth is a valid upper schedule when Clifford time is set
  to zero; it is not an optimal depth or a lower runtime bound.
- The Hadamard workspace upper allocations retain one redundant bit from the
  old envelope. Direct required-register accounting is one bit smaller, so
  this is a harmless upper allocation rather than an undercount. Bounded-QAE
  allocations reconcile exactly. Neither difference changes physical capacity.
- Both composed replay records contain correct selector outcomes on either
  side of the active threshold and complete financial/selector/phase cleanup.
  These are recorded basis executions, not a full QAE simulation or hardware
  timing. The previous isolated estimator suite passed all 14 supplied tests.

| Selected row | Reconciled total logical T | Reconciled scheduled T depth |
|---|---:|---:|
| C4 conditional Hadamard | 699,762,085,324,240 | 19,399,520,724,480 |
| H8 conditional Hadamard | 6,238,068,915,404,940 | 58,849,178,234,560 |
| C4 bounded digital QAE | 4,473,763,507,420,080 | 91,501,694,555,070 |
| H8 bounded digital QAE | 16,431,638,006,636,040 | 120,669,080,596,830 |

These are costs for one implemented residual mean. The baseline, regret
certification, optional tight-moment acquisition, classical I/O, device layout,
decoding and physical execution are not completed by summing these logical
resources. The artifact leaves full-price latency null and the significance
gate false. Its omitted-term list and manuscript qualification are necessary.

## Classical contract and financial interpretation

The manuscript's financial parameter table matches the implemented C4/C8/H4/H8
models. The monitored Asian payoff is discretely monitored by contract; a
finite Gaussian input law remains a numerical approximation. The baseline-plus-
residual identity is stated for a common exercise decision and is not confused
with the optimal compound value. Numerical errors, regret and confidence terms
have separate allocations totaling one cent and 0.01 failure respectively.

The detailed quantum cost is for strike 6. Both archived classical timings
include three strikes, so the manuscript correctly labels the entire classical
time as a deliberately quantum-favorable rejection screen. It retains the
faster archived H8 implementation and does not replace it with a slower parity
run. Empirical RQMC intervals are distinguished from the fixed-iid C4 confidence
screen. None is represented as the same certified digital-baseline contract
without a transfer argument. This is a defensible feasibility comparison;
it is insufficient for an affirmative matched-contract advantage claim.

The newly reviewed joint arithmetic certificate controls the combined digital
baseline and residual with the same digital decision. It is not a bound on the
separately estimated baseline, on the old real-arithmetic policy, or on policy
regret. The manuscript must retain those restrictions when incorporating the
new numerical values. A 32-sample exact-baseline timing screen is a planning
diagnostic, not statistical confirmation; projected days of Python execution
are not a lower bound on a compiled classical implementation.

## Capacity and publication claims

As a self-check of the reviewer's capacity contribution, the manuscript correctly
reports that both range-specialized tight Hadamard rows pass the most permissive
bare work screen. It scopes encoded-lane and 15-to-1 factory failures to explicit
throughput/family assumptions, and scopes memory to the allocated mapping.
It does not infer impossibility from a constructed serial or parallel schedule.
No device-specific layout, decoder or demonstrated clock is claimed.

The paper's proposed contribution is an auditable benchmark and selected
certificates. Existing compound-option applications, known Hadamard estimation,
prior derivative-resource estimates and quantized-control bias are attributed.
No new-algorithm, first-resource-analysis, or significant-advantage claim is
made. Journal suitability is not journal acceptance. Author identities,
attestations, substantive AI-use disclosure and archive/submission choices
remain separate prerequisites.

The exact primary title requested for reference 6 is **Quantum Speedups for
Derivative Pricing Beyond Black-Scholes**, Herman et al., arXiv:2602.03725v1,
3 February 2026. [Primary record](https://arxiv.org/abs/2602.03725).
The Lemaire title and JCAM publication record were also rechecked against the
[primary record](https://arxiv.org/abs/1903.10330). These bibliographic facts are
available now and should not be left as unverified placeholders in a frozen
research draft.

Reproduction:

```powershell
$env:PYTHONNOUSERSITE='1'
.context/controlled_closeout_repro/Scripts/python.exe -m research.controlled_priority_completion.capacity_integration_review
.context/controlled_closeout_repro/Scripts/python.exe -m research.controlled_completion_followup.synthesis_rotations --verify-only
```

The reviewed integration supports a scoped negative feasibility result and
large quantum implementation improvements. It does not fulfill the user's
significant-advantage objective or close the remaining scientific obligations.
