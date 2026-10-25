# Scope #44 at R2: packet for the human reviewer

**For the reviewer.** You are asked to check one negative result: under explicit, certified constants, no window
quantum amplitude-estimation protocol prices the B8x52 knock-out basket to ε = $0.001 ten times faster than the
best classical method. The headline margin is M ≈ 26.

Your review is the step no software or AI review can supply. Four AI reviews exist (listed at the end). Treat them as
aids, not as evidence.

**Time.** Part A takes about half a day: two short derivations and a ~160-line note. Part B takes about an hour.

**Independence.** Please state your relationship to the author on each sign-off form. Co-authors and advisors are
fine if stated.

## Part A: the method (before the sealed run)

Please answer each question **accept**, **accept with changes** (say which) or **reject** (say why).

**A1. The P2 window constant** (`docs/frontier_probe_20261021/P2_DERIVATION.md`). The rest of the paper rests on this.
Please check §1 to §4:
- **§1.** The outcome law F(φ + τ − 2πj/G)/G for G ≥ 2N+1. The mixture over the ±φ eigen-branches. The error rule
  |â − a| ≤ √(a(1−a))Δ + Δ²/4.
- **§2.** The lattice-sum loss h(TV + sup F), using sup F ≤ 2N+1 and |F′| ≤ 2N(2N+1).
- **§3, the core.**
  - The split φ_γ = φ₁ + (1−γ)·1, with Poisson summation for φ₁ and the half-weight rectangle DTFT
    sin(Nω)cot(ω/2).
  - The decay bound |Φ₁(η)| ≤ β²κ/η², and the constant 2/((1+√3/2)(√3/2)) = 1.2376043.
  - The alias sum π²/8.
  - The cot Laurent-series step, giving |cot(ω/2) − 2/ω| ≤ (2/π²)|ω|.
  - The energy expansion to λ0 ≥ (N·I_c/2π − X_band)/(N·I_tot/2π + X + C_R²).
  - Monotonicity in N. The 24 Oct note gives an analytic argument.
- **§4.** The rotation-error budget. Note that 3 rotations per controlled phase is the safer count.
- **The question:** is c(0.003) = 4.179 a valid constant for 800 ≤ N ≤ 1,048,575?
- **Background for you.** A numerical sanity check (`results/review_20261024/run001/checks.json`) shows the Kaiser
  window within 0.12% of the provably optimal window (the DPSS) at every N tested.

**A2. The A2a bias, steps 2 and 4** (`docs/claim_debts_20261022/A2A_CLIP_SPLIT_CERTIFICATE.md`).
- **Step 2.** When no stock site clips, the run002 clamp leak `ell` may be replaced by β = 2^-40. In the source,
  `ell` is defined at `experiment_box_muller_native_financial_bridge_v2.py:2844` and used at :2892 and :2989.
- **Step 4.** The Bernstein bound on the clip event:
  - zero mean and exact second moments on the 2^32-point midpoint angle grid;
  - |Y_k| ≤ B√2·max(a, b);
  - independence across whole pairs, and of radius and angle within a pair;
  - a union bound over 104 sites.
- **The question:** does the bias bound 3.634e-4 ≤ 0.55ε hold, given the run002 premises?

**A3. The U1 premises** (`docs/claim_debts_20261022/U1_CERTIFICATE.md`).
- Maurer & Pontil (2009) Theorem 4: is it applied correctly, one-sided, with R = 40?
- Is it acceptable to treat numpy PCG64 draws as iid?
- Is the 1e-9 slack adequate for rounding? Barrier flips are covered by headroom instead (24 Oct note, R-U1-1).

**A4. The preregistration** (`docs/r2_scope44/PREREGISTRATION.md`).
- Are the five rows of §5 the right ones? In particular, should the headline be W_proto (the protocol as run) rather
  than v4's W_cont?
- Is the decision rule of §6 right? It uses single departures only, and excludes the stacked column (M = 0.075).
- Is δ_L = 1e-4 a sensible choice?
- Is the condensed lifecycle of §9 acceptable?

**A5. The cited premises** (PREREGISTRATION.md §10). Is it acceptable to cite these without re-verifying them: σ_q,
T_C, D_eff, the RQMC price, the run002 A2a premises, and U2's E[g] = E[Y_N]?

**A6. The code, optional.**
- `research/r2_scope44/steps.py` (the sealed steps) and `verify_sealed.py` (the saved verifier).
- The dry run in `results/r2_scope44_dryrun/dry_run001/`: VERIFIED, 17 of 17 checks. It uses a different U1 seed
  from the real run.

**Sign-off A.**

| Item | Verdict | Comments |
|---|---|---|
| A1 P2 | | |
| A2 A2a | | |
| A3 U1 | | |
| A4 Preregistration | | |
| A5 Cited premises | | |
| A6 Code (optional) | | |

Name: ________  Affiliation: ________  Relationship to the author: ________  Date: ________

## Part B: the result (after the sealed run)

The author will give you:
- `results/r2_scope44/run001/`;
- `.context/R2_SCOPE44_SEALED_RECEIPT_run001.json`;
- `.context/R2_SCOPE44_VERIFICATION_run001.json`.

**B1.** Do the receipt and the verification say `PASS`, `VERIFIED` and `NO_GO_CERTIFIED`? Were all the deterministic
reproductions exact (PREREGISTRATION.md §8)?

**B2.** Do the results fall within the predictions of PREREGISTRATION.md §7? List any deviation, and say whether it
matters.

**B3.** Was anything changed after the preregistration was committed? Compare the commit in the receipt
(`git_head`) with the preregistration's commit.

**B4.** Is the paper's statement supported at R2? The statement is the W_proto M, the smallest explicit M, and
"NO-GO holds under every single departure".

**Sign-off B.** Verdict: R2 supported / not supported. Comments: ________

Name: ________  Date: ________

## For the author: finishing R2

1. **Find the reviewer.** Send them this packet and get part A back.
2. **Make any changes part A asks for,** then refreeze the manifest:
   `.context/frontier_t0_env/Scripts/python.exe -I -S -B research/r2_scope44/freeze_manifest.py`.
   Paste the new hash into PREREGISTRATION.md §3, then dry-run again with a new run name.
3. **Approve.** Fill in the Approval block, then commit and push to dev. Do not edit the preregistration after this:
   the seed comes from its bytes.
4. **Run the sealed step:**
   `.context/frontier_t0_env/Scripts/python.exe -I -S -B research/r2_scope44/sealed_run.py --author-run run001`
   (about 4 minutes).
5. **Run the verifier:**
   `.context/frontier_t0_env/Scripts/python.exe -I -B research/r2_scope44/verify_sealed.py results/r2_scope44/run001 --author-run`.
6. **Get part B** from the reviewer.
7. **Record R2.** Only after part B is signed: record R2 in `CURRENT_NUMBERS` and in the paper, with the reviewer
   named as they agreed.

## AI reviews so far (aids, not evidence)

- `results/frontier_probe_20261021/review/p2_review.jsonl` (P2, 21 rows);
- `results/frontier_probe_20261021/review/r3_review.jsonl` (self-mean);
- `results/claim_debts_20261022/review/a2a_review_summary.md` (A2a);
- `docs/review_20261024/REVIEW.md` (P2, A2a and U1, with independent numerical checks).
