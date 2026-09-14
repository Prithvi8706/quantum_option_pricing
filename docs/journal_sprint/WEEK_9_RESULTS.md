# Week 9 numerical and claim-audit results

14 September 2026. No new pricing trials or controller tuning.

## Numerical diagnostic

Archive: `results/journal_sprint/week9_numerical_v1`.
Replay: `results/journal_sprint/week9_verify_v1`.
The [protocol](PROTOCOL_W9_NUMERICAL.md) was saved before execution.

- 312 cases, zero missing reference components; elapsed 8.703 seconds.
- 18 empty references and 78 full references. Empty-reference enclosure is
  vacuous, not an informative accuracy success. No final reference set had
  multiple components. The remaining 216 cases had a nonempty, nonfull interval.
- Maximum endpoint slack: 1.1003482766924545e-13 in amplitude units.
- Independent implementation: mpmath 1.3.0, 80 decimal digits, 160 bisections;
  beta-CDF inversion and explicit k=0,1,2 amplitude polynomials. Production
  uses SciPy quantiles and trigonometric inversion. Comparison checks each whole
  reference component inside a single production component, with no added
  comparison tolerance or float conversion of reference endpoints.

The replay reproduced every saved case and summary. It checked 71 archive
hashes, all 67 planned source-snapshot hashes, and live identity of the six
producing modules/protocol dependencies. The verifier itself changed after the
original run to distinguish immutable producer provenance from an evolving audit
tool; its executed version is copied into the verification archive. We do not
claim all 67 live files still equal their historical snapshots.

This is a finite diagnostic, not formal interval arithmetic, a coverage
experiment, universal enclosure certification or large-production-count beta-tail
validation. Five-branch inversion has a separate unit test but the declared
final-intersection matrix did not exercise disconnected final reference sets.

## Historical evidence integrity

The verifier checked complete manifests and reconstructed declaration totals from
saved summaries: week 5, 67 hashes / 516 declarations; week 6, 71 / 2729;
week 7, 77 / 5042 inference-arm declarations; week 8 v2, 81 / 900.
These checks are not new full pricing replays. Prior closeouts retain their own
replay evidence. Week-7 arms share observations and week-8 v2 is not a new seed
replicate. See `week9_verify_v1/claim_sources.json` for manifest digests.

## Regression and synthesis

Nine new numerical unit tests passed (14.01 seconds). The integrated suite then
passed **337 tests**, with 11 upstream Qiskit deprecation warnings, in 192.80
seconds. XML: `results/journal_sprint/tests_week9_integrated_v1.xml`.
The subsequent verifier-only change was exercised by the successful complete
312-case replay; it was not part of that earlier full-suite run. Ruff passed for
the three new modules and numerical test file after the change.

The [new manuscript](MANUSCRIPT_RELIABILITY_DRAFT.md) incorporates weeks 5–9;
the [claim matrix](WEEK_9_CLAIM_EVIDENCE.md) distinguishes demonstrated results
from gaps. Historical drafts now link to their superseding documents without
overwriting their original content. The [research refresh](WEEK_9_RESEARCH_REFRESH.md)
separates newly screened abstracts from prior full-text readings.
