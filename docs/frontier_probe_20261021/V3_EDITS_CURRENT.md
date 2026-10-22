# Suggested v3 edits, current as of 22 Oct 2026 (not applied)

> **Current numbers:** see [CURRENT_NUMBERS.md](../plan110_status_20261022/CURRENT_NUMBERS.md) (headline run006; window 26.1, all-free 1.30, symmetric 1.50, no single departure reaches M <= 1). Figures below may be from earlier runs.

This list consolidates MEMO.md's 12 items, the round-3 numbers and the 22 Oct checklist work. Apply only after:
- your human check of P2 (`P2_DERIVATION.md`);
- the sign-off decision (N1 card).

**Headline source:** `results/frontier_probe_20261021/headline/run005/headline_table.json` (binding cell B8x52
$0.001, all inputs measured, QF choices where uncertain).

**Current headline numbers**

| Class | k | Primary | All-free | 1 lane vs 1 core | Symmetric (min over methods) | Minimal departures |
|---|---:|---:|---:|---:|---:|---:|
| Certified today | 682.7 | 1,666 | 82.7 | 173 | 96.0 | 3 |
| Canonical explicit (U1 + U2 + non-dyadic) | 197.6 | 482 | 23.9 | 50.1 | 27.8 | 3 |
| **Window, certified constant (U1 + U2 + direction-select)** | **8.762** | **21.4** | **1.06** | 2.22 | **1.23** | **2** |
| Window, quantum-only mean (U2 + direction-select) | 9.058 | 22.1 | 1.10 | 2.30 | 1.27 | 2 |
| Window, no U1/U2 | 25.8 | 62.9 | 3.13 | 6.54 | 3.63 | — |

Classical inputs:
- **T_C:** 10.84 s (Stage C 22.53 s; C10 fast preint, QF end of 2.08-2.25×).
- **Symmetric factor:** 17.3× (replicated RQMC with EB; iid EB 33.8×; N1 modelled 36.9×).
- **One-core ratio:** 9.62.

## Edits

1. **Abstract M table.** Replace it with the current table above (primary and symmetric columns). The window row
   becomes "explicit worst-case constant (this work)". Keep canonical as "canonical with U1/U2"; certified today
   becomes 1,666.
2. **Abstract and §1: the comparator.** "The strongest tested classical method" is now Stage C preintegrated RQMC
   with closed-form date roots and AS241 normals, which is the same estimator. Its T_C is 10.84 s; the 22.53 s Stage
   C value becomes a sensitivity.
3. **Abstract "checkable threshold" and §3.** For the window class, M ≤ 1 needs about 107 reaction layers and about
   1.1e7 T per iterate. The all-free floor (114) misses by 6%.
4. **Abstract and §8 robustness.**
   - Replace "robust only at the primary practice-CI convention" with "robust to any single favourable departure at
     the primary conventions (the closest, the idealized all-free oracle, gives 1.06)".
   - State that two departures together overturn it, for example all-free + symmetric distribution-free (0.061).
5. **§4.2 estimator.**
   - Add the P2 certificate (window, bound, N0 = 800, parts 1-4, c(0.003) = 4.179, k 8.762) and the two-stage
     quantum-only mean (k 9.058; removes the circular U1 price).
   - Add the literature rows: AQAE 2407.16795 Thm 2 at about 409; Rall 2103.09717 Prop 5 and Hamoudi 2108.12172
     Prop 4.1 as canonical plus medians; KO, Rall-QSP, Kimmel-Low-Yoder and Belliardo-Giovannetti not explicit or
     RMSE-only.
6. **§4.3 classical confidence (C09).**
   - Replace the modelled 36.9× with measured, timed distribution-free prices in every decision cell. The minimum
     over methods is 17.3 (B8x52 $0.001), 17.9, 16.1 and 10.3.
   - Use R = 17.30 from the analytic bound on the preintegrated payoff, not the assumed $40.
   - Name the replicated-RQMC estimator.
7. **§4.3 parallelism (H16).** The one-core ratio for the fast method is 9.62 at the binding cell; the 1 lane vs 1
   core window M is 2.22.
8. **§4.3 coverage (C10).**
   - **Tried and adopted:** the fast kernel.
   - **Tried and killed:** CV under RQMC (sd ratio 1.00); two-direction smoothing (1.3-1.5× slower at an
     acceptable bias); barrier importance sampling (not rare-event dominated: the top 1% of payoffs carry 6.6% of the
     price); switching-surface isolation (dense).
   - **Still untried:** GPU, PDE / sparse grids, MLMC / MIMC, surrogates.
9. **§4.2 and §8 achievability gap.** The gap between the counting floor and the best explicit constant is now
   8.76 / 1.85, about 4.7×.
10. **§5.1-5.3 tables.**
    - Add the window rows and use the run005 numbers.
    - Minimal departures: window 2, canonical 3, certified 3.
    - Update the "Reading" paragraph and §9.1 item 4.
11. **§6 levers.**
    - Lever 1 is met: c = 4.179 against a target of about 4.2.
    - Lever 2, with the window constant: M ≤ 1 needs D_eff ≤ 107 layers. Loader + free exponential gives 2.0 and
      all-free 1.06.
    - Lever 3: the symmetric convention alone gives 1.23.
    - Lever 5 (F20/F04): closed; move it to §7.1 with the P1 evidence.
12. **§7.1 closed escapes.** Add F20/F04 (P1), E25 (literature), F06/F07 (screens), CV-under-RQMC and two-direction
    smoothing as classical-side negatives.
13. **§8 limitations.**
    - **Complete-price ledger (C03).** The estimator's 0.003 is certified; the remaining 0.007 of the failure budget
      is unallocated. The 0.55ε bias reserve rests on the modelled 4.73e-4.
    - **H18 necessary condition.** At most about 1e-16 logical failure per T gate.
    - **Machine-state caveat.** Today's laptop ran the unchanged Stage C harness 2.2× faster than on 1 October, under
      the Best-performance overlay. Timings are therefore quoted as same-state ratios, taking the QF end.
14. **§8 rigour.** The 30× R1 justification now holds for the certified-today and canonical classes. The window
    class sits at 21× and has had two AI R2 reviews (P2; C10/C09), but no human review.
15. **§9 discrepancies.** Add:
    - WS-k window c (DPSS 4.168, uncertified) against the certified Kaiser 4.179;
    - N1 symmetric factor 36.9 (modelled) against 17.3 (measured, minimum over methods);
    - Stage C T_C 22.53 s against the C10 value of 10.84 s.

## Changelog line (suggested)

> v3 → v4: frontier probe P1-P3 (21 Oct) and checklist items C10, C09, H16, C03 and H18 (22 Oct), with two AI R2
> reviews. The explicit-constant margin moves 232 → 21.4. The negative is now robust to any single departure.
