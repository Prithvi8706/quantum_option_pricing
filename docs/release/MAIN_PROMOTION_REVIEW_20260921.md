# Independent AI review for main promotion

Date: 2026-09-21. Reviewer task: `promotion_review`, a separate AI agent that
did not author the implementation under review. This is scoped integration
review, not human peer review or publication approval.

## Scope and disposition

Reviewed the ten-commit range from stable remote main
`da3080d19a8f746cab31bbee157a5d591c6b56fb` through dev
`0146372fc3ab85e787906ea9181fae982d7156e2`. This covers completed batches 1–4
of the [promotion plan](../novelty_assessment/2026-09-21/MAIN_BATCH_PLAN.md):
stronger arithmetic, its frozen evidence, the preserved historical artifacts,
the separate numerical label interface, and the scientific assessment.

**Disposition: no actionable blocker found for integrating this complete
reviewed snapshot into main while preserving its commits.** This approval
does not extend to future experiments, physical execution, confirmation
admission, human novelty clearance, or manuscript submission. The user's
new main-promotion instruction supersedes the earlier task's instruction to
leave main unchanged; the earlier records remain correct historical records.

## Inspection and verification

- Read the label adapter, its final verifier and tests, the underlying directed
  interval and canonical-label decoder, and selected signed-residual certificate
  and component accounting code. Inspected the prior source/acquisition review,
  mathematical and resource audit receipts, review record, comparator fairness
  audit, publication decision and batch dependencies.
- Verified by Git comparison that no previously tracked source, evidence,
  tests or release documents from the completed research snapshot `49b8f0a5`
  were modified or removed in the reviewed later commits. New files are
  additions, not replacements of frozen producers or acquisitions.
- Independently read all 13,783 original artifacts listed for consolidation
  in the preservation manifest. Their lengths and SHA-256 values match:
  254,488,741 bytes preserved. This is byte preservation, not scientific
  revalidation of historical experiments. The old manuscript's explicit
  archival notice prevents its old readiness assertions from becoming current
  status claims.
- Inspected the actual receipts for 384 label possibilities across 18 schedules,
  18 independently checked residual certificates and 1,332 fixed diagnostic
  nodes, and 148 primary plus 18 residual resource rows. Historical test receipts
  report 1,645 integrated tests and 315 overlapping pinned tests; these are
  neither newly rerun here nor additive independent test populations.
- Freshly reran the archived resource checker successfully: all 148 primary
  rows, 18 residual rows, 332 ledgers and two reflection references passed.
  Local execution output is `.context/promotion_resource_review_20260921.json`;
  the committed historical checker and receipt identify the reproducible
  procedure. This checks existing artifacts, not new circuit acquisition.
- The lead separately reports a fresh 19-test adapter/decoder run, passing
  targeted Ruff, 300 local documentation links and 143 receipt/input/source
  hash bindings. Those are the lead's checks, not this reviewer's independent
  test run. Delivery/protection checks and the actual push belong to the lead's
  promotion record.

## Findings

1. **Numerical interface is correctly scoped.** `label_amplitude` bounds the
   distance between the actual binary64 result and an outward enclosure of
   the exact canonical label. It does not rely on an assumed libm error.
   Coordinatewise monotonicity of order statistics justifies the median
   enclosure, including overlapping intervals and folded probability ordering.
   The positive-sensitivity allowance is outward multiplied. The frozen
   decoder's affine rounding allowance and this extra input-conversion allowance
   address distinct errors; neither certifies physical gates.

2. **Final schedule minimality correction is sound.** The independent rational
   Machin enclosure uses an upper pi endpoint for feasibility and a lower
   endpoint to reject the preceding dyadic schedule. The initial v1 receipt
   remains explicitly historical. Integrating the complete snapshot avoids
   presenting the initial envelope-relative check as the final proof.

3. **Resource interpretation is appropriately limited.** The assessment
   reports ratios of the declared logical-resource projections, recognizes
   compiler-policy differences, the 103-versus-5,162 D2 width tradeoff, duplicate
   nominal configurations and the query-reduction explanation. It does not
   convert those figures into physical runtime or quantum-over-classical
   advantage. Common-policy compilation is a future research requirement for
   stronger claims, not a defect preventing integration of an honest current
   case study.

4. **Scientific novelty is not inflated.** Established residual estimation,
   affine encoding and circuit techniques are separated from the narrower
   certified comparative finding. The recommended conditional-go framing and
   technical-report fallback are consistent with the recorded evidence and
   unresolved human significance assessment.

5. **Historical verification must remain historical.** The assessment delivery
   verifier intentionally asserts the old local/remote main pointers. It will
   fail after authorized promotion and must not be described as a reusable
   postpromotion delivery check. Preserve it and its old receipt; create a new
   promotion record with actual remote SHAs. Similarly, the old batch plan's
   “no promotion in this task” describes the previous task, not this one.

## Limits and integration conditions

This pass did not re-emit every circuit, rerun the 1,645-test suite, rederive
every certificate, or repeat the full literature search. It relies on scoped
prior reviews and source-bound receipts for unchanged code, augmented by the
inspection and byte-preservation verification above. No review is represented
as exhaustive certification.

Promote by ordinary fast-forward or history-preserving merge, subject to live
protection rules. Preserve the producer/acquisition hashes. Record the actual
push and equal remote/local SHAs separately, and keep only main/dev as permanent
branches. Future comparison/manuscript batches remain incomplete after this
integration.
