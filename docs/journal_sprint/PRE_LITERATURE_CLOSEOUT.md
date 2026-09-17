# Current-version closeout before the four-paper audit

Baseline: `72622546` on `research/confirmation-gate-bounds`.

## Completed development deliverable

- Combined-feature ablations, QSP residual normalization, symmetric phases,
  separable and centered signals, minimax candidates and directed partial error
  accounting are implemented and archived. Failed/negative outcomes retained.
- Full regression:1071passed/12legacywarnings (488.91s), receipt
  `results/journal_sprint/normalization_full_tests_v1.xml`.
- Clean implementation checkout `e6894c82`:102new tests passed; existing isolated
  week15 environment, not a newly installed environment. Stored numerical replay
  and source/artifact checks passed from that checkout.
- Closeout recheck at the baseline reproduced the archive comparison:
  15numeric payloads/74hash entries; receipt `pre_literature_replay_check_v1.json`.
  This rechecked stored acquisitions, not a new full acquisition or regression.
- Independent agent mathematical/code review previously completed; not human
  collaborator sign-off. Tracked working tree was clean at the start of closeout.

This closes the **bounded development version**, not the scientific confirmation
campaign. The following are explicitly NOT completed and must not be silently
marked done when the literature work begins:

1. Bound for the implemented signal operator, including stored rotations,
   LCU preparation, normalization and controlled global phases.
2. An explicit execution/synthesis/noise model with a justified bound.
3. Complete target-price accuracy and statistical-delivery contract.
4. Same-continuous-target strong classical resource/runtime comparison.
5. Demonstration of quantum advantage, novelty assessment and human sign-off.

The best known-component sum ($0.807293, q10/degree128 centered/minimax) remains
partial. Its higher circuit cost is retained. No paper-ready accuracy guarantee,
hardware result, classical superiority, remote push, PR or merge is implied.

## Handoff boundary

Freeze old producers and acquisitions. Four-paper work goes into new audit and
test artifacts. Separate (a) authors' claims, (b) independently checked identities,
(c) assumptions transferable to our arithmetic Asian basket, (d) alternative
contracts requiring a separate study, and (e) measured versus projected gains.

An improvement over a prior quantum circuit is not quantum-over-classical
advantage. A hypothesis is not a result. Do not search until a favorable claim
is manufactured: retain adverse tests and report if no advantage is established.
