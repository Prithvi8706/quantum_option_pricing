# Existing Stage C classical evidence and remaining comparison gaps

The read-only C09 audit captured121 existing files before interpreting their numerical results. Existing coverage workers and original receipts were left unchanged. Six of the16 C2 timing rows are actual20-replication confirmations, all with `scale=1`; six are small-prefix measurements and four are fitted timing rows. [Frozen inventory and audit](../../results/limitation_program_20261001/C09_audit_run001/summary.json).

| Continuous preintegration case, archived$0.001 target | Points actually run per scramble | Measured warm median wall time | Pooled16-scramble half-width |
|---|---:|---:|---:|
| B4x12 | 131,072 | 2.6880081 seconds | $0.0003304495 |
| B8x52 | 131,072 | 22.52928595 seconds | $0.0003482431 |

The plain-RQMC$0.001 rows reporting49.8223 and380.1586 seconds are fitted, rather than measured successful prices. Both independent reference pairs agree. Their combined agreement resolution is about$0.00053237 and$0.00063795, which does not support a$0.0001 reference check.

At that original snapshot, coverage contained only B4 levels10–13; B8 and B4 level17 and a scored result were absent. C1/C2/C4 code hashes match their local historical commit bytes; referenceA/B lack full code/spec/environment bindings. Current specification bytes differ from recorded versions. These are historical snapshot findings; the completed coverage update below retains its own receipt.

The classical ndtri/PCA/preintegration/OSS/iid constructions target the continuous financial law. The accepted quantum graph targets a finite paired Box–Muller law with clipping and native arithmetic. A complete G2 bridge or an exact finite-law comparator is still needed. Pooled scramble uncertainty and smoothed classical variance do not automatically transfer to the unsmoothed quantum payoff. These are concrete G4 prerequisites; measured timing is retained without declaring the full comparison closed.

The other agent completed all three declared coverage arms: 1,000 independent
16-scramble estimators for each development case at four nested prefixes, plus
the separate B4 131,072-point arm. The saved score now contains all nine sample
sizes and both nominal confidence levels, matching the 18-cell Bonferroni rule.

| Saved coverage cell | Observed nominal 99% coverage | Bonferroni interval |
|---|---:|---:|
| B4, 8,192 points | 98.7% | [97.2344%, 99.5195%] |
| B8, 8,192 points | 99.6% | [98.5720%, 99.9530%] |
| B4, 131,072 points | 99.5% | [98.4093%, 99.9202%] |

Neither primary 8,192-point cell triggers the declared undercoverage test, so
the rule calls for no empirical timing recalibration. This is a failure to
detect undercoverage, rather than a theorem that true-price delivery succeeds
at least 99% of the time. The intervals are scored against an estimated shared
reference. Adding reference uncertainty to their width is an optimistic proxy;
it does not establish a conservative lower bound on true-price coverage. B8
coverage at the decision-point sample size was explicitly outside the declared
study and remains assumed.

A new read-only snapshot verified 60 code/specification/lock bindings against
the recorded Git revision, including exact Windows line-ending materialization.
The later D12 specification is a distinct version; its mismatch with C4's
recorded D1-D11 bytes was reconciled without replacing any hash expectation.
The C2 timing file is byte-identical to the first audit. Reference agreement
resolution remains $0.00053237/$0.00063795; the narrower weighted-reference
half-width is a separate quantity and does not resolve that agreement test to
$0.0001. No new paths, tests or timing measurements were run by this program.
[Completed-results inspection](../../results/limitation_program_20261001/C09_stagec_update_run001/summary.json),
[saved observations](../../results/limitation_program_20261001/C09_stagec_update_run001/stage_c_observations.json).

At the inspection, C5 timing was still active and had saved only the B4 OSS-BB
block of four planned blocks. Its $0.01 row is a measured 0.73887245-second
confirmation; its $0.001 row is a modelled 22.56948229 seconds. A partially
written timing receipt does not complete the comparator minimum. The Stage C
markdown is an at-merge handoff and still says coverage is running; the saved
completed coverage receipt supplies the newer evidence. New limitation-program
experiments remain queued while the exclusive timing job runs.

A later live check on 2 October found two of the four C5 blocks: B4 OSS-BB
and B4 OSS. The OSS block adds a measured $0.01 confirmation of 1.35716945
seconds and a modelled $0.001 time of 64.67616646 seconds. The saved timing
file was last written at 14:22:11 IST; its live producer processes remained
present. Neither B8 block nor C7 timing, GPU timing or a final decision table
was present at this check. These mutable observations do not alter the earlier
one-block frozen snapshot or establish completion. The limitation program
continues static authoring and review, with execution held until the exclusive
timing jobs finish.

The next live check found the third C5 block, B8 OSS-BB, saved at 14:46:57 IST.
Its $0.01 row is a measured 18.60630880-second confirmation at 262,144 points
per scramble, with a pooled half-width of $0.00363976. Its $0.001 primary time
is a modelled 919.75377786 seconds. The fourth block, B8 OSS, was still absent
and the same C5 producer processes remained live. This new observation does
not replace the historical frozen snapshot or complete the final comparison.

The live parent process is Bash supervisor 33304 running
`.context/stage_c_day2b.sh`. Its actual script starts C7 timing immediately
after C5 timing. Execution clearance therefore requires this supervisor and
all exclusive timing Python jobs to be terminal; C5's disappearance alone
could race the queued C7 job. The script and jobs remain untouched.

At 15:17 IST on 2 October, all four C5 blocks were present and its Python
producer was terminal. The C5 file was finalized at 15:07:30 IST with SHA-256
`2492cc9129d1f4b1a118bb306cb2cf19e43d3f9c64ba7898875f30c2d90effda`.
This is a later read-only observation; the earlier one-block frozen snapshot
remains historical evidence.

| C5 block | Measured $0.01 confirmation, seconds | Modelled $0.001 primary time, seconds |
|---|---:|---:|
| B4 OSS-BB | 0.73887245 | 22.56948229 |
| B4 OSS | 1.35716945 | 64.67616646 |
| B8 OSS-BB | 18.60630880 | 919.75377786 |
| B8 OSS | 17.55944780 | 1438.36606754 |

The $0.001 C5 times are model estimates. They exceed the existing measured
preintegration times in both cases. At $0.01 the B8 OSS confirmation is faster
than OSS-BB, so the extra bridge is not a universal timing improvement. These
rows do not complete the final comparator minimum or prove true-price coverage.

The same script has moved to C7 timing. Its live handles are Bash 1572/31244
and Python 13324/30816; the original supervisor 33304 is no longer authoritative.
The C7 timing directory contains its metadata but no completed timing table at
this observation. Clearance requires every matching Stage C script supervisor
and exclusive timing descendant to be terminal, regardless of PID changes.
C8, GPU timing and a final decision table remain absent. No limitation-program
tests or proof evaluations have run during this exclusive chain.

A separate posthoc coverage diagnostic is now authored and statically reviewed.
For each saved interval with center `c` and half-width `h`, and shared reference
center `R` and radius `r`, it distinguishes guaranteed containment
`abs(c-R)+r <= h`, reference-point containment `abs(c-R) <= h`, and possible
overlap `abs(c-R) <= h+r`. It preserves the original float-generated intervals
and uses exact rational representations of their binary64 endpoints. The
planned 54 simultaneous binomial brackets round their endpoints outward using
exact integer tail comparisons. Its 21 fixtures have not run.

Even those stronger counts only sandwich true-price coverage on the event that
the reference interval contains the price. If both references were valid 99%
intervals and the conditional IID binomial count model held, the stated union
bound would be 93% jointly with the 95% simultaneous count event. These are
explicit unproved premises, not a 99% delivery theorem. The diagnostic changes
neither the declared Stage C rule nor the other agent's outputs.
[Author preflight](../../research/limitation_program_20261001/conservative_coverage_preflight.json).

C7 saved its first timing block at 15:20:51 IST: case 2 is 16 assets and
52 dates with the original barrier 140. Three warm all-16 runs reached
524,288 points per scramble. Its $0.001 time is a fitted 44.93578822 seconds
at an estimated 108,463.74 points, not a new 20-replication confirmation.
Only one of seven C7 timing blocks is present; the supervisor and producer
remain live. This partial update does not authorize concurrent experiments.

At 15:38 IST on 2 October, C7 contained five of seven final timing blocks.
Each contains three warm all-16 runs. The two remaining cases are the
16-asset, 52-date contracts with barriers 120 and 160. The supervisor and
both timing Python roots remain live, including pauses between worker pools.

| Saved C7 case | Assets and dates | Barrier | Fitted $0.001 all-16 time, seconds |
|---|---|---:|---:|
| 2 | 16 x 52 | 140 | 44.93578822 |
| 3 | 4 x 12 | 120 | 2.70566889 |
| 4 | 4 x 12 | 160 | 0.55519489 |
| 5 | 8 x 52 | 120 | 17.43812342 |
| 6 | 8 x 52 | 160 | 4.93554646 |

These are saved model outputs, not 20-run target-accuracy confirmations.
C8, GPU and final-decision directories are absent at this observation;
the existing decision tables are explicitly interim. Stage C is therefore
unfinished and supplies no new quantum-advantage finding.

The separate completed-timing snapshot inspector is authored and unexecuted.
It requires all four C5 and all seven C7 blocks, byte-identical original C4,
references and C2 evidence, and exact recorded Git source/specification/lock
materialization. It refuses every live Stage C supervisor and timing descendant
and every visible Python multiprocessing spawn or resource-tracker process,
including workers whose arguments contain no workspace path. C5 rates have
an archived commit marker but no recorded per-file rate-time digests; that
provenance distinction remains explicit. No partial timing observation changes
the previous frozen one-block snapshot.
[Timing-inspection preflight](../../research/limitation_program_20261001/stage_c_timing_update_preflight.json).


At 16:00:43 IST on 2 October, the Stage C day2b supervisor exited with code
zero after saving all seven C7 blocks. The completed C5/C7 evidence was then
frozen and inspected in
[C09_stagec_timing_update_run001](../../results/limitation_program_20261001/C09_stagec_timing_update_run001/summary.json).
Root and an independent reader verified all 135 output-file and 249 input
hashes with zero mismatches. Original C4, C2 and reference bytes remain equal
to the earlier snapshot. Process observations before and after inspection
found no surviving timing supervisor, descendant, spawn worker or resource
tracker. The earlier partial observations above remain historical records.

The final two C7 rows are case 7 (16 x 52, barrier 120), fitted 38.33502848
seconds, and case 8 (16 x 52, barrier 160), fitted 9.74925362 seconds at $0.001.
Every C7 case contains three warm timing repetitions; none is a 20-run
accuracy-delivery confirmation. Every C5 $0.001 time is also fitted and marked
extrapolated-high. The C5 $0.01 rows above are actual 20-run measured medians;
the scale-adjusted primary values equal those medians here because each scale
is one. These distinctions passed the inspector's saved-record algebra checks.

C8's fixed 24 out-of-sample cases, the GPU/MC anchors and final decision-table
integration remain outstanding. Stage C as a whole is unfinished. The next
frozen Stage C item is C8 rates followed by one warm timing per case in an
exclusive slot. Completed C4/C5/C7 evidence establishes no quantum advantage
and supplies no true-price 99% coverage theorem. The local limitation-proof
queue resumed only after the completed snapshot inspection passed.
