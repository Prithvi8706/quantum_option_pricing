# Claim-grade debts: status (22 October 2026)

The user authorized all claim-grade debts on 22 Oct 2026 ("Everything incl. circuits"), including lifting the
scope-#43 stop and doing circuit work.

**What was delivered.** Every debt is done at **R1**. Each one has:
- two independent computation paths, or one exact path plus an independent recount;
- inputs cited by sha256;
- exclusive-create outputs.

**What is not done.** None of this is **R2**. R2 additionally needs:
- preregistration through the limitation program's lifecycle;
- a sealed run with a saved verifier and a ROOT receipt under `.context/`, which this session may not write;
- human peer review.

Nothing here is committed.

**Naming.** "#44" means two different things in the repo. In PLAN_110 §4 it is the merged headline scope. In the
E11 notes it is the four-target E11 draft (U4). This record uses the PLAN_110 meaning. The E11/U4 route stays closed
on its own economics.

## Results at the binding cell (B8x52, ε = $0.001, primary conventions)

| Debt | Result | Rigour | Evidence |
|---|---|---|---|
| **A2a bias** (formerly the A02 bridge rerun plus the A07/A13 re-proofs) | ≤ 6703058386012589/2^64 = **3.634e-4 ≤ 0.55ε**, with the source unchanged, by splitting out the lower-clip event. P_fin(clip) ≤ 1e-29 over 104 sites. **The binding cell is eligible.** The re-proofs are not needed | R1. Paths agree to 9.4e-13. An independent AI review found it sound, with 2 minor doc fixes, both applied | [A2A_CLIP_SPLIT_CERTIFICATE.md](A2A_CLIP_SPLIT_CERTIFICATE.md), `results/claim_debts_20261022/a2a/run001`, `review/a2a_review_summary.md` |
| **U1 mean certificate** | m = **3.28804 ≥ E[g]** with probability 1 − 1e-4: EB with R = 40 on 2^23 raw payoffs, plus A2a. This covers P2's assumed m = 3.32682, so k = 8.762 rests on a certified premise | R1 (two arithmetic paths) | [U1_CERTIFICATE.md](U1_CERTIFICATE.md), `results/claim_debts_20261022/u1/run001` |
| **U2 wrapper** | ×211 multiplier with a 53-bit comparator, built. 40,000 exhaustive and 4,281 full-width cases pass. 211·sup Yraw < 2^53. Cost +11,578 T per iterate (2.7e-6 relative) and 0 qubits. Readout ≤ 2^-39 | R1 | [C11_U2_COMPILE.md](C11_U2_COMPILE.md) |
| **C11 compile** | Full controlled iterate: 4,267,659,718 T (literal) or 2.44e9 T (4 T per Toffoli); 609.7M Toffolis; 4,460,627 qubits; Toffoli depth 201,263. **Compiled window M = 2,290** (floor conventions), 8,828 literal, ≥ 277 in every reading | R1 (two recount paths agree exactly; 17 checks) | [C11_U2_COMPILE.md](C11_U2_COMPILE.md), `results/claim_debts_20261022/c11/run001` |
| **C03 / E07 complete-price ledger** | Failure total 0.01: estimator 0.003 (cert); U1 1e-4 (window class) or 0 (quantum-only mean); bridge, source and acquisition 0 (cited); physical 0.0069 / 0.007 as an explicit hardware premise. Dollar: 0.45ε plus 3.634e-4 plus 2^-39, inside ε. **Complete for both window classes** | R1 desk (exact arithmetic) | `results/claim_debts_20261022/c03/run001/c03_ledger.json` |
| **H18** | Physical premise: ≤ 2.9e-16 logical failure per T at the floor, and ≤ 2.8e-17 per T for the compiled iterate | R1 desk | the same ledger |
| **H17** | M ≤ 1 needs ≤ 11.6 ns per reaction layer, or ≥ 2.61e13 T/s (26× the budget), at the floor. The saved source needs 11.4 ps or 4.85e14 T/s | R1 desk | [H06_H17_DESK.md](H06_H17_DESK.md), `h06_h17/run004` |
| **H06** | Catalysed-CCZ supply convention: window M 13.0. 1 CCZ per slot: 8.63, reaction-bound. Never below M 8.40. No single-departure flip | R1 desk | the same |
| **Scope #44** (merged headline) | Independent new-code recompute matches run006 **exactly**. Window M **26.08**; quantum-only mean 26.96; all-free 1.29; symmetric 1.50; one lane 2.71; all-free + symmetric 0.075; compiled iterate 2,286. Binding cell eligible on certified bias. **NO-GO holds under every single departure** | R1. R2 is required by PLAN_110 §4 because the margin is < 30× | [SCOPE44_PROSPECTUS.md](SCOPE44_PROSPECTUS.md), `results/claim_debts_20261022/scope44/run001/scope44_receipt.json` |

**Register.** run009 (`results/plan110_w0/register/run009`) updates 13 rows. The tiers are unchanged: T1 4, T2 6,
T3 11, T4 31, T5 33, T6 25.

**Compiled M versus C11's own figure.** Scope #44 gives 2,286 using iterate depth only. C11 gives 2,290 because it
also includes the estimator-level overhead: the step code and phase register.

## What this changes in the paper

1. The binding-cell eligibility caveat is gone. Its bias is certified at R1, below 0.55ε.
2. The complete-price claim at the binding cell is now complete at R1. The physical-failure share is stated as an
   explicit hardware premise; it is not certified, and it cannot be.
3. The headline floor is shown to be quantum-favourable by about 88× against the compiled circuit at floor
   conventions. So the NO-GO is conservative on the quantum side.
4. U1 and U2 are certified at R1, so window k = 8.762 no longer rests on uncertified premises. The P2 constant
   itself has had only an AI review, and still needs a human check.

## Open, in order

1. **Human peer review** of: P2_DERIVATION.md; A2a proof steps 2 and 4; the U1 iid and slack premises; the C11
   provenance drift note (the `_storage` lookup key).
2. **R2 lifecycle** for scope #44: preregistration, a sealed run and a receipt. Writing under `.context/` is reserved
   for the user.
3. **Optional.** Build the window state-preparation rotation network. Its count is currently modelled at 130 T per
   rotation (lit).
