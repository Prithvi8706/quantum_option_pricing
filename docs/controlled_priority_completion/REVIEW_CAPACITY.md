# Independent review of capacity and combined-cost accounting

22 September 2026. Reviewer: the separate `range_audit` subagent, which did not
author `capacity_screen.py`, `capacity_revised.py`, `combined_cost.py`, their
capacity artifacts, or the physical-capacity conclusions. This review does not
serve as independent approval of the reviewer's own financial range or joint
arithmetic work.

**No mathematical blocking finding identified for the stated conditional
screens and constructed logical schedules.** They do not establish a physical
crossover or a complete financial-price certificate.

## Executed independent checks

- Recomputed all 360 work-conservation coordinates in `capacity_range.json`
  directly using exact rational clock values and integer lane occupancies.
  Checked both the numerical floor and every pass/fail flag.
- Recomputed all deadline patch-round exposures, sufficient-distance union
  tests, and restricted-factory spacetime floors independently of the generating
  functions.
- Matched all six revised arithmetic T counts to `combined_cost.json`, checked
  the substituted source hashes, and verified the capacity artifact uses the
  smaller serial allocation while the combined wave schedule pays additional
  scratch storage.
- Ran the nine capacity tests: **9 passed in 0.47 seconds**.
- Read both generators and the complete combined-cost generator, including
  financial forward/inverse substitution, QFT contributions, rotation synthesis
  multiplicities, error allocation, source-wave depth and omitted price terms.

## Findings and scope limits

1. **Work floor versus schedule.** `N*tau/floor(P/a)` is a valid occupancy
   lower bound under the explicitly adopted lane-duration and occupancy
   assumptions. It deliberately relaxes indivisible batches; replacing it by
   a ceiling would strengthen a restricted schedule assumption, which is not
   needed. The combined T-depth is separately an upper schedule for the emitted
   implementation, with Clifford durations excluded from the
   one-nanosecond sensitivity. It is not used as a universal runtime floor.

2. **Changed results are retained.** The latest conditional Hadamard C4/H8
   rows pass the unencoded one-qubit/one-nanosecond work screen. The documents
   state that change explicitly. Distance-three 17-qubit lanes fail the stated
   RQMC budget, but C4's conditional row misses only narrowly; the prose does
   not exaggerate that coordinate into an architecture-independent no-go.

3. **Factory screen is restricted.** The factory inequality applies only to
   the specified final-stage schedule with at least 11 tiles for 11d rounds.
   The literature gives an 11-tile/11-step construction and notes additional
   injection/control costs; its concatenated upper stage uses 15 steps.
   The code's 11d premise is therefore favorable for that restricted family,
   not a universal distillation lower bound. The calculation grants all
   physical qubits to top-level production, free lower levels/rejects/routing,
   and P perfect initial states without deducting their memory. This extra
   generosity weakens the floor and does not invalidate its negative result.
   Checked against [Litinski, Sections 3.3 and 3.5](https://arxiv.org/html/1808.02892v3#S3).

4. **Memory and noise are conditional.** `(2d^2-1)*allocated_qubits` is the
   selected rotated-patch mapping requirement. It is not a universal memory
   lower bound. The noise fit and exposure calculation give sufficient
   conditional distances; failing that test at a smaller distance does not
   prove physical failure. The approximate fit matches the stated source,
   [Fowler and Gidney, Section XV](https://arxiv.org/html/1808.06709v4#S15).
   Layout, decoder behavior, routing and measured device error assumptions
   remain unvalidated.

5. **Quality is not throughput.** The conservative distillation recurrence
   concerns independent accepted stochastic Z errors, separately from logical
   faults. Its levels are sufficient under that bound, not necessary levels
   for every factory. Capacity calculations omit synthesis work deliberately;
   their quality rows correspond to that arithmetic-only workload. They are
   not a full hardware failure certificate. The combined logical artifact
   restores the certified rotation T counts and makes its error contribution
   explicit.

6. **Full price remains open.** `full_price_latency_seconds` is null.
   Baseline estimation, policy-regret acquisition, any tight-moment certificate,
   classical setup, decoding, physical I/O and layout are listed as omitted.
   The conditional Hadamard rows retain the unproved tight-moment transfer;
   the bounded-QAE rows avoid it but estimate the digital residual only.
   The cost tables are screens, not positive matched-guarantee crossover claims.
   Old real-policy baseline/confidence data cannot be silently reused for the
   implemented digital policy.

One minor reproducibility observation was sent to the root agent: the current
combined JSON's `scope` prose differed from the current generator's prose,
without changing any resource value or meaning. Regenerate the artifact after
the final source freeze; this is not a mathematical finding.

## Reviewed content hashes

Hashes identify the independently checked snapshot. A prose-only regeneration
can change the final JSON hash without changing the verified numerical rows.

| File | SHA-256 |
|---|---|
| `capacity_screen.py` | `cf9f5c38b595a26f829be16125f1398dfe4d4f09f83a7fe8a72601034831a2a5` |
| `capacity_revised.py` | `9932c4f31b52c46516bb93b5cf2721d8a2e9cc61468ed474a5ce743d55e0320c` |
| `combined_cost.py` | `2b4d8f1917d641483d8da2ce982ee0647d19f07dcf07f24826b5f6436ef20135` |
| `capacity_range.json` | `35291b860b97670203b1efc35558ebfa1c80ef4570b6f4f284842f4400435a98` |
| `combined_cost.json` | `b170ad6fa5b71bd3e25e0d020704fa22cfc0c06e0b8b6f0f53497dc9de1866b5` |

Review conclusion: retain the conditional negative end-to-end decision and
the explicit open obligations. Neither the work floors nor this review proves
that a different estimator/compiler/architecture can never achieve advantage.
