# A20 two-closure diagnostic handoff

One prospectively fixed structural diagnostic PASS, under30 process CPU /90
controller wall seconds /1MiB. Observations were0.21875 process CPU and0.063
controller wall seconds; these are administrative diagnostic observations, not
matched performance or complete-process timing. No source builder was imported,
stock point evaluated, table constructed, gate emitted, fit or price called.

The two date0 source closures for assets0 and1 each have45 nodes and the same
signed72/F40 clamp literals: low=-12193974156573, high=9145480617430. Their selected
clipped-log SSA values are3579 and3697; stock outputs4021 and4417. The strict
original ordered-template premise fails on exactly these argument pairs:

| Normalized output | Operation | Asset0 args | Asset1 args |
| --- | --- | --- | --- |
| 11 | mul | 6,10 | 10,6 |
| 18 | mul | 6,17 | 17,6 |
| 22 | mul | 6,21 | 21,6 |
| 31 | mul | 6,30 | 30,6 |
| 35 | mul | 6,34 | 34,6 |

No missing asset-dependent spot multiplication or clamp difference was diagnosed.
The specific failure is strict ordered-argument matching. The original V4
FAILED_UNSEALED remains failed; this diagnostic does not mathematically approve a
shared table or reapprove the producer.

Post-execution peer review identified a generic limitation: Python dictionary
equality can merge1,True and1.0. The diagnostic retains the original JSON values,
and the five observed argument inequalities remain valid. Generic typed-literal
equality is not certified by its comparison function. ROOT separately checked
the actual fixed closures using canonical JSON spelling before proposing V5;
that lemma and A14's independent semantic/cost review are separate author-stage
evidence, not retroactive producer approval.

The missing authorization is scalar native multiplication commutativity plus
SSA induction for these exact templates. Even with that authorization, ordered
narrow backend costs differ and cannot be shared or set to zero. Any future
source/backend adoption needs its own contracts and cost proof. V5 proposes a
separate semantic comparison signature while retaining raw ordered arrays,
hashes, scalar evaluations and backend cost boundaries.

Artifacts:

- Protocol/code: `research/limitation_program_20261001/continuation_20261004/A13/A20_TWO_CLOSURE_DIAGNOSTIC_PROTOCOL_run001.json` and `diagnose_a20_two_stock_closures_v1.py`.
- Receipt: `results/limitation_program_20261001/A20_continuation_20261004_template_diagnostic_run001/`.
- Manifest SHA256: `5935f7871819a283dd395a6b09b6bd4cd4f40860d9d57aba95336bf901532d19`.
- Post-execution static qualification: `docs/limitation_program_20261001/continuation_20261004/E12/A20_STATIC_REVIEW_run001.json`.

Scientific component approval, new fixture/replay credit, finance draws, adoption
and advantage remain false/zero. ROOT handles complete failed-packet integrity
separately; no failed source, receipt, prepared map or expected SHA was edited.
