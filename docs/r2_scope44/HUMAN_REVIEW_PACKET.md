# Scope #44 at R2: packet for the human reviewer

**Start here.** This is the only document you need. Every file it names is in the public repository
<https://github.com/Prithvi8706/quantum_option_pricing>, branch `dev`, at the path given. In part B the author will also
send you two files that are not on GitHub.

## Before you start

**The claim, in one paragraph.** The paper says that a quantum computer cannot price this option (an 8-asset, 52-date
knock-out basket, to $0.001 accuracy) ten times faster than the best classical method. That holds even with the best
explicit quantum estimator. The result is one number, M:
- M is how far the quantum method falls short of a 10× speedup. M ≤ 1 would mean it reaches 10×.
- The headline is M ≈ 26.
- The weakest case is M ≈ 1.29, in the "free oracle" column. It is still above 1.

**Your job.** Check that the math behind M is correct, and that the planned rerun is fair. You are not asked to fix,
re-run or improve anything. You read, check, and record a verdict.

**What you need.** The repository, pen and paper, about half a day for part A and an hour for part B.

**Verdicts.** For each item, write one of:
- **accept**;
- **accept with changes** (say what);
- **reject** (say why).

A **major** issue could change a number or the conclusion. A **minor** issue is wording or presentation.

**Independence.** You must not be the author. Co-authors and advisors are fine, as long as you state the relationship
on the forms.

**The AI reviews.** Four AI reviews exist, listed at the end. Use them as reading aids, not as evidence. Your review is
the step no software or AI review can supply.

## Part A: the method (before the sealed run)

### Step 1. Understand what M is made of (15 min)

Read §1 and §5 of `docs/r2_scope44/PREREGISTRATION.md`. M is a product of a few pieces:
- **k**, the quantum cost constant. It comes from **c**, the window constant (step 2).
- **The mean bound m**, which lets the quantum method use fewer calls (step 4).
- **The bias**, which must stay below 55% of the error budget for this cell to count at all (step 3).
- **The classical inputs** (T_C, σ, D_eff). These are cited, not re-checked here (step 6).

When you can say in your own words what each piece does, move on.

### Step 2. The P2 window constant, the most important item (2-3 hours)

File: `docs/frontier_probe_20261021/P2_DERIVATION.md`, about 160 lines. Everything later depends on it. Go through it
in order and check each inequality by hand.

| | Where | What it says | What you check |
|---|---|---|---|
| 2a | §1, lines 12-22 | After the window state, the Grover powers and an inverse QFT, outcome j has probability F(φ + τ − 2πj/G)/G | Write the inverse QFT of Σ w_n e^{in(φ+τ)}\|n⟩ yourself. Get amplitude W(·)/(‖w‖√G). Confirm that G ≥ 2N+1 is needed so no two exponents collide mod G |
| 2b | §1, lines 24-29 | A phase error ≤ Δ gives an amplitude error ≤ √(a(1−a))·Δ + Δ²/4 | Taylor-expand sin²(x/2): the first derivative is sin(x)/2 and the second is at most 1/2. Both eigen-branches (±φ) give the same estimate, because sin² is even |
| 2c | §2 | A random known phase offset turns the success probability into a fine lattice sum, close to an integral | sup F ≤ 2N+1 and \|F′\| ≤ 2N(2N+1), each by Cauchy-Schwarz in one line. The loss is about 1e-11. (The doc says "below 1e-11"; the worst case is 1.6e-11. That is a known wording slip) |
| 2d | §3, lines 46-57 | The window is split into a smooth part (Poisson summation) plus a flat rectangle (an exact sum) | The identity Σ_{\|n\|<N} e^{inω} + cos(Nω) = sin(Nω)·cot(ω/2). Also that the smooth part is continuous and 0 at ±1, which is what makes Poisson summation valid |
| 2e | §3, lines 59-65 | \|Φ₁(η)\| ≤ β²κ/η², and for η ≥ 2β the constant is 1.2376·β²(…) | The mean-value step on sin(t)/t, and the arithmetic 2/((1+√3/2)(√3/2)) = 1.2376043 |
| 2f | §3, line 67 | The aliasing sum is bounded by β²κ/(4N) | Σ_{k≥1} 1/(2k−1)² = π²/8 |
| 2g | §3, lines 70-73 | \|cot(ω/2) − 2/ω\| ≤ (2/π²)\|ω\| on [−π, π] | Every Laurent coefficient has the same sign, so the ratio grows with ω. Evaluate it at ω = π |
| 2h | §3, lines 75-90 | λ0 ≥ (in-band energy − errors) / (total energy + errors) | The direction of every inequality: the numerator must be bounded below and the denominator above. Dropping R² in the numerator is fine because R² ≥ 0 |
| 2i | §3, line 92 | The bound only improves as N grows, so proving it at N = 800 covers every larger N | Each error term divided by N shrinks as N grows. `docs/review_20261024/REVIEW.md` gives a one-paragraph argument |
| 2j | §4 | About a million rotations at 2^-40 each cost at most 1.9e-6 of failure probability | The counting. The doc uses 2 rotations per controlled phase; the textbook count is 3. It does not change the result, but say whether you agree |

**The question for your verdict:** is c(0.003) = 4.179 a valid constant for 800 ≤ N ≤ 1,048,575?

### Step 3. The A2a bias, proof steps 2 and 4 only (1 hour)

File: `docs/claim_debts_20261022/A2A_CLIP_SPLIT_CERTIFICATE.md`.

**Proof step 2** (starts at line 53).
- **The idea.** The old bound paid a large "leak" term in case a stock hit its lower floor (the clamp). When no stock
  hits the floor, that term can be replaced by a tiny one, β = 2^-40.
- **Check the chain.**
  1. An unclipped stock satisfies S_N ≤ b·S_I + β.
  2. Averaging over the stocks gives the basket bound B_N ≤ b·B_H + β.
  3. So a barrier decision can flip only if the ideal basket lies inside the narrow band [(140 − β)/b, (140 + 2β)/a].
- **In code**, the leak is defined at
  `research/limitation_program_20261001/experiment_box_muller_native_financial_bridge_v2.py` line 2844. It is used at
  lines 2892 and 2989, only through `max(β, ell)` and `140 − ell`.

**Proof step 4** (starts at line 70).
- **The idea.** To hit the floor, a stock would have to fall from $100 to about $0.00002 in a year. That is
  astronomically unlikely, and a Bernstein inequality makes it precise.
- **Check:**
  - The increments have mean zero: cos and sin average to zero on the 2^32-point angle grid.
  - The variance formula, V_j = (E[R̂²]/2)·j·9/(100·nt).
  - The bound on each increment, B·√2·max(a, b).
  - Independence across pairs. This one is a premise.
  - The union bound over 104 sites. The smallest exponent is 72.27, so P ≤ 1e-29.

**The question for your verdict:** given the older run002 results it builds on, does bias ≤ 3.634e-4 ≤ 5.5e-4 hold?

### Step 4. The U1 assumptions (30 min)

File: `docs/claim_debts_20261022/U1_CERTIFICATE.md`. Read "Statement and proof" (from line 45) and "Assumptions" (from
line 120).

**The idea.** A classical Monte Carlo sample gives an upper bound on the option's mean price. The quantum method uses
it to save calls.

**Check:**
1. **The theorem.** Is Maurer & Pontil (2009) Theorem 4 quoted and used correctly? It should be one-sided, use
   ln(2/δ), and be scaled to the range [0, 40].
2. **iid.** Is it acceptable to treat the computer's pseudo-random generator as truly independent draws? It is
   standard practice, but it is a judgment you should state.
3. **The 1e-9 slack.** It covers rounding. It does not cover a rounding error that flips a barrier decision. That case
   is covered by headroom instead: the conclusion survives even if the mean were 0.039 higher. Is that acceptable?

### Step 5. The plan for the rerun (30 min)

File: `docs/r2_scope44/PREREGISTRATION.md`. Here you judge whether the plan is fair, not whether it is correct.

- **§5, the rows.** There are five readings of the quantum cost, from cautious to most generous to quantum. Is any
  missing? Should the headline be W_proto (the protocol as run, about 25.9) rather than v4's W_cont (26.1)?
- **§6, the decision rule.** The NO-GO needs M > 1 in four single-change columns. The stacked column makes two generous
  assumptions at once, gives 0.075, and is excluded. Is excluding it acceptable? It matters for how the paper words
  its claim.
- **§8, failures.** Is "report it as found, never rerun for a better answer" strict enough?
- **§9, the lifecycle.** It uses 7 steps instead of the program's ~19. Is that acceptable?

### Step 6. Inputs taken on trust (15 min)

§10 of the preregistration lists inputs this scope does not re-verify: the classical timing T_C, σ, the circuit depth
D_eff, the RQMC price, the run002 bridge results, and U2's E[g] = E[Y_N]. For each, decide whether citing it is
acceptable or whether it needs checking too.

### Step 7. The code (optional, 30 min)

- Skim `research/r2_scope44/steps.py` (the sealed steps) and `research/r2_scope44/verify_sealed.py` (the verifier).
- Open `results/r2_scope44_dryrun/dry_run001/VERIFICATION.json`. It should show 17 checks passing. That run uses a
  different random seed from the real run, on purpose.

### Step 8. Sign-off A

| Item | Verdict | Major or minor? | Comments |
|---|---|---|---|
| Step 2: P2 window constant | | | |
| Step 3: A2a bias | | | |
| Step 4: U1 assumptions | | | |
| Step 5: Preregistration | | | |
| Step 6: Cited inputs | | | |
| Step 7: Code (optional) | | | |

Name: ________  Affiliation: ________  Relationship to the author: ________  Date: ________

Send the completed form back to the author. If you ask for changes, the author makes them before approving the
preregistration. You may then be asked to look again.

## Part B: the result (after the author's sealed run, about 1 hour)

**What you will have.**
- **On GitHub:** `results/r2_scope44/run001/`, which holds `RECEIPT.json`, `VERIFICATION.json` and every output.
- **From the author by email:** `R2_SCOPE44_SEALED_RECEIPT_run001.json` and `R2_SCOPE44_VERIFICATION_run001.json`. These
  live in the author's ignored `.context/` folder, so they are not on GitHub.

### Step 9. Statuses

The receipt, the verification and both emailed files should say `PASS`, `VERIFIED` and `NO_GO_CERTIFIED`. The
`receipt_sha256` inside the emailed receipt should equal the sha256 of `results/r2_scope44/run001/RECEIPT.json`.

### Step 10. Predictions

Compare the results with §7 of the preregistration:
- c = 4.179, 6.052 and 4.197 exactly;
- the bias exactly as in R1;
- the R1 sample reproduced bit for bit;
- m_U ≈ 3.29 ± 0.004;
- W_proto M ≈ 25.9-26.0;
- the smallest explicit M ≈ 1.29.

List any deviation, and say whether it matters.

### Step 11. Nothing changed after the plan was locked

The receipt records a git commit (`git_head`). Run `git log -- docs/r2_scope44/PREREGISTRATION.md`. It should show
no commit after the approval commit, and the approval commit should come before `git_head` or be it.

### Step 12. Sign-off B

Is the paper's statement supported at R2? The statement is: "M ≈ 26 at the binding cell; the NO-GO holds under every
single departure".

Verdict: R2 supported / not supported. Comments: ________

Name: ________  Date: ________

## What not to do

- Don't treat the AI reviews as evidence.
- Don't fix problems yourself. Write them down; the author fixes them.
- Don't check the classical timings or other cited inputs unless you flag them in step 6.

## AI reviews so far (aids, not evidence)

- `results/frontier_probe_20261021/review/p2_review.jsonl`: P2, 21 rows.
- `results/frontier_probe_20261021/review/r3_review.jsonl`: the quantum-only mean class.
- `results/claim_debts_20261022/review/a2a_review_summary.md`: A2a.
- `docs/review_20261024/REVIEW.md`: P2, A2a and U1, with independent numerical checks.

## For the author: what to send, and finishing R2

1. **Send the reviewer one link:**
   <https://github.com/Prithvi8706/quantum_option_pricing/blob/dev/docs/r2_scope44/HUMAN_REVIEW_PACKET.md>.
   Ask for sign-off A back.
2. **Make any changes part A asks for.** Then refreeze the manifest
   (`.context/frontier_t0_env/Scripts/python.exe -I -S -B research/r2_scope44/freeze_manifest.py`), paste the new hash
   into PREREGISTRATION.md §3, and dry-run again under a new run name.
3. **Approve.** Fill in the Approval block, then commit and push it on its own. Don't edit the preregistration after
   that, because the seed comes from its bytes.
4. **Run the sealed step** (about 4 min):
   `.context/frontier_t0_env/Scripts/python.exe -I -S -B research/r2_scope44/sealed_run.py --author-run run001`.
5. **Run the verifier:**
   `.context/frontier_t0_env/Scripts/python.exe -I -B research/r2_scope44/verify_sealed.py results/r2_scope44/run001 --author-run`.
6. **Commit and push `results/r2_scope44/run001/`.** Email the reviewer the two `.context/R2_SCOPE44_*_run001.json`
   files, and ask for sign-off B.
7. **Record R2** in `CURRENT_NUMBERS` and in the paper, and only after sign-off B. Name the reviewer as they agreed.
