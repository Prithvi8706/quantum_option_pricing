# Branch N authorization card (plan110)

On 11 October 2026 the user chose "NO-GO → negative paper" at DP1. The DP1 memo is `docs/program_plan_20261010/DP1_MEMO.md`.

## Claim

**Claim:** "No design with certified constants reaches a 10× complete-latency advantage for the fixed B4x12/B8x52 knock-out task under the stated conventions."

The conventions are the ones fixed in `research/plan110_w0/W0_CARD.md`. The claim is about achievability, not query-lower-bound impossibility. Its scope is three things together:
- this construction family;
- the fixed task;
- the strongest tested classical method.

## Rigour

The headline is **R1**: an independent recompute along a different path, plus a receipt. R2 is not needed because the primary margin is M = 232, at least 30× (plan section 4, branch N). The user can still ask for R2.

## Writes

Agents may write only to:
- `research/plan110_n1/`
- `results/plan110_n1/`
- the new draft `manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT.md`, created with exclusive create.

Agents must not edit any of the following:
- existing manuscript files;
- `.context/`;
- `results/limitation_program_20261001/`;
- `docs/limitation_program_20261001/`;
- `docs/limitation_audit_20261001/`;
- `progress.json`;
- `primitives.py`.

Additional limits:
- No git operations.
- No SCI or ROOT lifecycle.
- Any script whose numbers are used runs under `.context/frontier_t0_env/Scripts/python.exe -I -S -B`.

## Waves

- **Wave 1** (3 agents):
  - (a) Independent headline recompute: decision table and oracle floor.
  - (b) Estimator access-model card.
  - (c) Hardware and classical card.
- **Wave 2:**
  - Manuscript draft.
  - Adversarial review of the draft.
- **Then:** user sign-off.

Every agent appends rows incrementally, so a usage-limit stop loses little.
