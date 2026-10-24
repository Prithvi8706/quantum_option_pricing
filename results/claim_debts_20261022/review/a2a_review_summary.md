# A2a clip-split certificate: adversarial review (AI, R2-style)

22 October 2026. Object: `docs/claim_debts_20261022/A2A_CLIP_SPLIT_CERTIFICATE.md`, its three scripts and
`results/claim_debts_20261022/a2a/run001/`. Findings, one per line: `a2a_review.jsonl`. This is an AI review, not a
human peer review. No existing file was edited and nothing was committed.

## Verdict: sound, with minor fixes

No major findings. The claimed bound |E Y_N - E Y| <= 3.63374e-4 (B8x52) and <= 1.20743e-5 (B4x12) holds on the
run002 and run003 premises.

## Major findings

None.

## Minor findings (doc and guard fixes only; the result is unaffected)

- **A2A-R04: band-ordering assert is missing.** The doc says the band ordering "is asserted", but neither script checks
  0 < lo <= up. It holds because run002 guards a_j <= 1 <= b_j. Fix: add the assert, or reword the doc.
- **A2A-R10: one stated number is wrong.** "Bernstein exponent >= 73 at every site" is false; the minimum is 72.268 at
  elapsed date 52. P_fin(C) <= 2.83e-30 is unaffected.

## What was checked

1. **Step 1 (pointwise split).** H maps the same q32 input words to the hybrid path (468 distinct words, two per pair),
   so E_H Y_N = E_fin Y_N. Both payoffs lie in [0, 40]: native_cap_upper < 40, and the ideal is capped at 40e^-0.03.
2. **Step 2 (ell -> beta on C^c).** In run002, ell appears only at the lower band endpoint (v2.py:2892) and in the smooth
   leak max(beta, ell) (v2.py:2989). The upper-clamp guards, the eager clamp inventory and the eager tail safety do not
   use ell. An upper clip only lowers S_N, so the upper envelope still holds on C^c.
3. **Step 3 (reused lemmas).** The radial and angular TV <= 4 arguments and the Gaussian factorisation are
   endpoint-generic. A_j does not depend on the endpoints.
4. **Step 4 (clip event).**
   - The clipable-site list is complete. Bounds are identical across assets; elapsed date 39 gives -10.847 >= L = -11.0904,
     elapsed 40 gives -11.243 < L; B4x12 never goes below -5.30.
   - The source clamp is a strict lt.
   - Midpoint angle grid: the +3/4 wrap gives sin(theta) exactly, and the moments are exact because N = 2^32 does not
     divide 1 or 2.
   - From the run002 pair-role incidence, sum (a_k^2 + b_k^2) = j*9/(100nt) for all 416 and 48 prefixes.
   - The KS and eta second-moment routes are valid. The range bound M is valid but loose.
   - The Bernstein and Bennett forms are one-sided and plugged in outward (monotonicity in s, V and M checked).
   - The union bound over sites is correct. A hand check at j = 52 reproduces exponent 72.27 (Bernstein) and about
     156.5 (Bennett).
5. **Arithmetic.**
   - Scratch copies in `C:\Users\prith\AppData\Local\Temp\review_a2a\`, run with frontier_t0_env 3.12.4 -I -S -B,
     reproduce certificate.json and independent.json exactly: same `cases`, same input hashes. The summarize step
     prints ALL_OK.
   - All script, output and premise sha256 match the doc.
   - A separate float recompute from the raw JSONs gives a total of 3.633735e-4.
6. **Total identity.** The new formula reduces to the run002 identity with ell restored and P(C) = 0. The code asserts
   this exactly for zeta and the total, and outward for g_j.

## Residual caveats (already stated in the doc)

- Everything rests on the run002 and run003 premises: product-uniform q32 input law, the lambda, alpha and B envelopes,
  D_S and eta, and the transport lemmas.
- The two numeric paths share one proof skeleton, so their agreement does not test steps 1-4. That is R1, not R2.
- The E07 G2 ledger has not been recomposed at eps = 1/1000.
