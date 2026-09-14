# Week 3 PR gate

## Local discovery deliverables

- Completed: actual-circuit/noise checks; readout/dependence stress; 480-row
  classical European/Asian matrix; pinned BAE/BIQAE source smokes; 20 larger
  logical circuit profiles; fresh-environment circuit replay; regression checks.
- Decision completed: **hold held-out confirmation**. Response-model failures,
  conditional delivery-risk semantics and matched-cost comparison design must
  be resolved before freezing a confirmatory protocol. No adaptive superiority
  or practical quantum advantage is established.
- Automated independent review: requested with `gpt-6-astra`; findings addressed
  and final corrected-artifact check completed. No new demonstrated
  scientific-invalidating bug found. Not a human referee review.
- Final integrated regression: 253 tests passed, 11 legacy warnings; Ruff and
  tracked whitespace checks passed. Fresh-environment sprint: 89 tests passed.
- **Blocked external gate:** Macroscope not installed/connected. User must
  complete account setup and confirm permitted credit use. No PR created.

See [results and review details](WEEK_3_BASELINES_AND_REVIEW.md).

## Proposed publication-safe PR scope

Include sprint source/tests, protocols, current discovery summaries and explicit
environment recipes; include the existing vendored comparator's license and
notice. Select small machine-readable evidence deliberately, retaining source
hashes and reproduction commands. Check links against the actual PR package.

Do not bulk-stage `results/journal_sprint`: it contains downloaded papers,
third-party source caches, complete virtual environments, historical manuscript
snapshots and intermediate diagnostic outputs. Do not redistribute unlicensed
third-party source merely because it was cloned for local inspection.

Preserve unrelated user modifications in `research/paper_a`, existing plan
files, `.claude`, and `outputs/paper_a_springer`; do not include them implicitly.
No author names, contributor approval, submission or payment is authorized by
this technical handoff. Before creating a PR, verify its exact diff/base and
both requested review outcomes, then report any remaining scope limitations.

Current branch `paper-a-foundation-e0` is 19 local commits ahead of the fetched
`origin/main`; those commits contain required Paper A foundations. No remote
foundation branch or existing PR was found in the read-only check. A PR against
main would therefore include that history in addition to staged sprint work.
Do not describe it as an isolated week-3-only diff without changing the base.
