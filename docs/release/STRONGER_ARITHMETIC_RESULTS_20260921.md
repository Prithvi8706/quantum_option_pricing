# Stronger arithmetic and signed residual comparison: results

Date: 2026-09-21. The bounded primary and signed-residual acquisitions completed
with all 148 primary layout rows and all 18 residual rows feasible under the
declared ideal-logical error/query budgets. The same D1/D2 Asian-basket targets,
q10, cutoff 4, $1 absolute tolerance and at least 95% confidence are retained.

## Supported finding

The preferred quantum construction changes with the contract. Reflection keeps
the lower CX projection in D1. In D2, reflection uses **2.9346 times as many
control-cancelled projected CX gates** as arithmetic with a comparable classical
control and signed residual; the conservative-ledger ratio is **3.2892**.
This reverses the earlier D2 comparison against the unoptimized raw arithmetic
route. The D2 residual route allocates **5,162 total qubits versus 103** for
reflection; lower CX comes with a substantial width tradeoff.

This supports an application-specific encoding-choice result under declared
implementations and resource models. It does not establish a new primitive,
global optimality, hardware speedup, or quantum-over-classical advantage.
Ratios of resource projections are not measured runtime ratios or bounds on
actual runtime ratios. Human assessment of publication-level novelty is open.

## Matched selected plans

All plans use 17 AE repetitions. CX counts below use standard control
cancellation, including initial preparation, both directions of the oracle,
zero-state reflections and the inverse-QFT swaps.

| Case | Route | Deterministic dollar allowance | AE M | Projected CX | Total allocated qubits |
| --- | --- | ---: | ---: | ---: | ---: |
| D1 | Reflection, QSP degree 64 | 0.45473744 | 128 | 36,469,403,102 | 55 |
| D1 | Best range-reduced raw arithmetic | 0.10284620 | 1,024 | 458,928,511,243 | 2,314 |
| D1 | Best signed-residual arithmetic | 0.10296484 | 128 | 104,719,289,723 | 4,733 |
| D2 | Reflection, QSP degree 128 | 0.60039730 | 512 | 1,101,392,680,835 | 103 |
| D2 | Best range-reduced raw arithmetic | 0.19044330 | 2,048 | 1,843,424,312,811 | 2,687 |
| D2 | Best signed-residual arithmetic | 0.20538904 | 256 | 375,312,500,844 | 5,162 |

The selected raw arithmetic plans use width 40, 20 fractional bits, Taylor
degree 8 and one reduction/squaring. The selected residual plans use width 48,
24 fractional bits, Taylor degree 8, one reduction/squaring, and the fixed
degree-four classical control. They use shared clean conversion scratch.
The full menus, not only these selected rows, remain in the archives and CSV.

Compared with the already strengthened raw arithmetic route, adding the signed
control reduces total CX projections by factors **4.3825 (D1)** and **4.9117 (D2)**.
Compared with the historical raw ripple implementation, the complete residual
route reduces projected CX by factors **5.3483** and **5.9903**. These comparisons
change more than one component; they are not causal estimates for centering alone.

## What the three changes contributed

1. **Scratch reuse:** preserves the original integer map and arithmetic gate
   counts. D1 arithmetic A allocation changes from 1,835 to 1,113 wires; D2 from
   3,465 to 1,299. Dependency depth rises from 1,457,262 to 2,905,250 in D1 and
   1,466,110 to 5,810,090 in D2. Both new layouts also save two clean carry wires
   versus the historical allocation. This is a width/depth tradeoff.
2. **Range reduction:** the best raw route lowers total projected CX about 18%
   relative to historical raw arithmetic. Reflection still wins both cases at
   this stage. Requested degrees 12 and 16 sometimes yield identical quantized
   coefficient lists after trailing-zero removal; their separate certificates
   and menu entries are retained.
3. **Signed residual/control:** a universal bound and explicit shift let the
   unsigned comparator encode a signed payoff-minus-control. Restoration of the
   directed classical offset gives the original financial target. Selected
   A/A-inverse calls fall from 34,799 to 4,335 in D1 and 69,615 to 8,687 in D2.
   The larger oracle and qubit allocation are fully charged. The reduced query
   count changes D2's preferred logical-CX route.

The exact negative residual witness, shifted encoding, reciprocal/Horner/scaling
errors, offset/discount bridge and signed overflow proof are in the
[residual method](SIGNED_RESIDUAL_METHOD_20260921.md). The residual uniform
bound controls normalization; it is not an additive approximation bias.

Classical offset preparation is recorded separately: D1 uses 28,672 cell visits
and 70 exp calls; D2 uses 245,760 cell visits and 549 exp calls, with 1,025 CDF
boundaries per case. These costs are not converted into quantum CX or included
in a claimed wall-clock speedup. Strong end-to-end classical comparison remains
open. The residual depth field is a conservative composition upper bound, not
the primary study's actual remapped dependency depth.

## Evidence and reproducibility

- [Primary archive](../../results/journal_sprint/stronger_arithmetic_v1/results.json):
  source freeze `9511bc0c`, complete 74 configuration acquisitions / 148 layout rows.
- [Residual archive](../../results/journal_sprint/signed_residual_arithmetic_v1/results.json):
  source implementation `23f8d948`; acquisition head `60e735e1` also commits its
  primary input archive. Complete 18 configurations.
- [All 166 new rows](../../results/journal_sprint/stronger_arithmetic_analysis_v1/all_rows.csv)
  and [combined decisions](../../results/journal_sprint/stronger_arithmetic_analysis_v1/summary.json).
  Historical reflection references are retained separately in the summaries.
- [Primary replay](../../results/journal_sprint/stronger_arithmetic_pinned_replay_20260921.json):
  all 74 certificates/finite diagnostics and 296 CX ledgers checked; selected
  baseline/best raw configurations re-emitted in both layouts, plus loading
  and their zero-state reflections. Other primary counts are archived metadata.
- [Residual replay](../../results/journal_sprint/signed_residual_pinned_replay_20260921.json):
  all 18 certificates/finite configurations, two offset certificates and 36 CX
  ledgers checked; the selected D1/D2 complete control oracles, loader and their
  reflections were re-emitted.
- [Selected residual parents](../../results/journal_sprint/residual_parent_pinned_replay_20260921.json):
  additionally re-emitted D1_28/D2_28 from the primary archive in both layouts,
  exactly matching their recorded component evidence. Thus the selected residual
  routes' conversion/aggregation evidence was also reconstructed. In total six
  distinct primary configurations and two residual oracles were re-emitted;
  no full-menu gate reconstruction is claimed.
- [Full test receipt](../../results/journal_sprint/stronger_arithmetic_full_tests_20260921.xml):
  **1,645 passed**, 12 legacy dependency warnings, 871.44 seconds.
- [Separate pinned tests](../../results/journal_sprint/stronger_arithmetic_pinned_tests_20260921.xml):
  **315 passed**, 17 dependency warnings, 167.32 seconds. These tests overlap the
  full suite and are not additive.
- [Review record](STRONGER_ARITHMETIC_REVIEW_20260921.md),
  [primary protocol](STRONGER_ARITHMETIC_PROTOCOL_20260921.md),
  [primary method](STRONGER_ARITHMETIC_METHOD_20260921.md), and
  [residual protocol](SIGNED_RESIDUAL_PROTOCOL_20260921.md).

All acquisitions and the recorded replay scopes passed. The independent AI
reviews are documented separately from the still-pending human novelty review.
The complete CSV, summary and input manifest regenerate byte-for-byte identically.
The final documentation check resolved 213 local link targets; it did not
validate external URLs or anchors.

## Scientific decision

Close this bounded implementation/comparison study with its recorded verification.
Retain both reflection and residual arithmetic as candidate routes in the logical
decision analysis. Do not promote either to production or confirmation. The
next scientific step is independent expert assessment of this narrowed
contribution, followed by an explicit paper-scope decision. Physical error and
runtime assumptions, matched classical superiority, fresh confirmation and the
integrated manuscript remain unresolved.
