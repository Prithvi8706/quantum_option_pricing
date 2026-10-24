# C11 + U2: compiled controlled Grover iterate and window estimator at B8x52 $0.001

22 October 2026. This covers register item C11 (the full iterate compile) and U2 (the support-tight wrapper,
obligation O7 of `docs/parallel_E11_unblock_20261010/U2_MEAN_AWARE_SCHEDULE.md` §4). The user authorized circuit work
on 22 Oct ("Everything incl. circuits").

**Rigour: R1.** The counts were made along two independent paths, and both agree exactly. Every check is in
`results/claim_debts_20261022/c11/run001/summary.json` (`all_checks_pass: true`). There has been no peer review and
there is no lifecycle receipt, so this is not R2.

**Labels:** meas = exact count of an emitted gate list; mod = modelled; assm = assumed; lit = literature. q+ means
quantum-favourable and q− quantum-unfavourable.

## Answer

| Quantity (B8x52 $0.001, primary conventions) | W0 floor (headline) | Compiled, floor conventions (QF) | Compiled, literal 7-T |
|---|---:|---:|---:|
| T per iterate | 2.30e8 (mod, q+) | **2.44e9** (4 T/Toffoli), 10.6× | **4.27e9** (meas), 18.6× |
| Reaction layers per iterate | — | **201,263** Toffoli layers (meas) | 776,965 T layers (meas) |
| Supply layers per iterate (1e5 T per 100 ns layer) | 2,296 | 24,387 | 42,677 |
| D_eff per iterate = max(reaction, supply) | **2,296** | **201,263** (reaction-bound), 87.7× | 776,965, 338× |
| Window M (N = 100,924; T_C = 8.89 s) | **26.1** | **2,290** | 8,828 |
| Quantum-only-mean M (1,730 + 102,602 calls) | 27.0 | 2,367 | 9,126 |

Most favourable reading of the compiled leaves (mod, q+). It uses the dependency-only leaf schedule, as if width
were unlimited, and replaces the emitted linear reflection ladder with a log-depth AND tree that was not emitted.
That gives D_eff = 95,101 and **M = 1,084**, which is 41.6× the floor. A supply-only reading that ignores reaction
depth gives M = 277 (QF) and 485 (literal).

**The compile can only raise M relative to the floor.** Every compiled reading is at least 10.6× the floor's D_eff,
so every compiled M is at least 277. The headline's floor stays the quantum-favourable bound it was labelled as. The
NO-GO is strengthened, not weakened. The floor was an idealized, literature-structure model (N1/W0, q+). The real
emitted circuit:
- uses Cuccaro ripple-carry arithmetic, not Kogge-Stone;
- has a memory-capped schedule;
- uses exact seven-T CCX;
- has a linear 15,029-wire reflection ladder.

**U2 cost:** +11,578 T per iterate (+2.7e-6 relative), +6,609 T-depth and +1,640 Toffoli layers per iterate, and
0 extra logical qubits.

## 1. U2 wrapper: flag = [sel₅₃ < 211·Yraw]

**Construction.** The circuit is the saved E02 comparator (`reversible_fixed_point.less_than`: copy, subtract,
CX(msb, flag), undo) with one change. The copy of Y into the comparator's 54-bit extended register is replaced by an
exact shift-add multiply by 211:
- 211 = 2^0 + 2^1 + 2^4 + 2^6 + 2^7, so the multiply is one copy plus four Cuccaro adds, of widths 53, 50, 48 and 47;
- a zero-extended copy of Y feeds the adders;
- the whole block is undone, so all scratch returns to zero.

The probability law is a′ = E[211·Yraw]/2^53 = E[Y$]/S′, with S′ = 8192/211 USD. The gate list is
`run001/u2_selector_gates.json` (IR rows (kind, a, b, c), the same encoding as the E02 arrays).

| Check | Result |
|---|---|
| Stdlib restatement of the saved 46-bit selector equals `selector.npy` row by row | yes |
| The U2 builder at c = 1, b = 46 reproduces `selector.npy` exactly | yes |
| Exhaustive small widths: (c, b) = (3, 6), (13, 8), (11, 9), (211, 11), (5, 7), (1, 3); flag correct, scratch clean, inverse restores | 40,000 / 40,000 cases |
| Full width (72-bit Y word, 53-bit selector), edge and random cases: Y ∈ {0, 1, 2, sup, sup−1, …} plus 300 random; sel ∈ {0, 1, 2^53−1, 211Y−1, 211Y, 211Y+1} plus 8 random | 4,281 cases, 0 failures |
| Support (cert, from the E03 certificate and its independent audit): 211 × 42,680,645,956,484 = 9,005,616,296,818,124 < 2^53 = 9,007,199,254,740,992 | holds; slack 1.58e12 |
| Outside the support (Y = 2^46 − 1) | wraps, as expected; the premise is needed |

**Cost (meas, seven-T convention).**

| | Saved 46-bit selector | U2 selector | Delta |
|---|---:|---:|---:|
| Toffolis per selector | 188 | 1,008 | +820 |
| Selector pair per iterate: T | 2,632 | 14,112 | **+11,480** |
| Selector pair per iterate: T-depth | 1,504 | 8,064 | +6,560 |
| Reflection (14,976 + 53 random wires): T | 210,294 | 210,392 | +98 |
| Reflection T-depth | 105,148 | 105,197 | +49 |

**Width.**
- The 53 selector bits, the flag and the control use 55 of the 72-bit old output buffer, leaving 17 wires for phase
  controls.
- The selector scratch (163 wires) and the reflection scratch (15,028) reuse the financial private bank (capacity
  1,516,959).
- Logical qubits are unchanged at 4,460,479.

**Readout allowance (re-derived, exact).** The phase is the exact rational r = (jK − l)/(GK). sin(πr) is enclosed
using:
- a Machin π enclosure of width 7e-127;
- a 40-term alternating Taylor series with its remainder;
- a Lipschitz term.

Then price = S′·â, rounded to the nearest 2^-40 USD, with no binary64 libm call. The error is
|price − S′·sin²(φ̂/2)| ≤ 2^-41 + S′·width:
- the analytic width is below 1e-100 for every r ∈ [0, ½];
- the observed width is 2.1e-103 over 404 samples;
- the allowance is therefore 4.55e-13 ≤ the 2^-39 placeholder (mod: the procedure is exact; the width is bounded
  analytically and checked on samples).

## 2. The iterate, recounted from the raw leaves

The bound source is A10 min-depth B8x52:
- 41,186 calls of 60 leaves in 166 memory-capped batches;
- sha256 checked against the E02 binding.

The iterate is F; selector; CZ(control, flag); selector⁻¹; F⁻¹; controlled uniform reflection. Only the CZ and the
reflection are controlled, so a controlled iterate costs the same as an uncontrolled one.

**Two recount paths.**
- **Path A** (`iterate_compile.py`) runs the repository's own counting functions read-only: `_native_cost`,
  `extended_resources` and `make_reflection`, with numpy and numba. It re-costs every leaf from its `.npy` file.
- **Path B** (`recount_independent.py`) uses stdlib only. It parses `.npy` files itself, re-implements the seven-T
  ASAP schedule, sums counts over calls rather than batches, and rebuilds the reflection from its definition. The
  rebuilt reflection equals `reflection.npy`.

Both paths reproduce iterate.json `financial_resources` and `resources` exactly: T 4,267,648,140, T-depth 770,356 =
663,704 + 1,504 + 105,148 (the WS-small convention), and 4,460,479 qubits. They agree exactly on every U2 field.

**Compiled U2 iterate (meas; paths A and B agree).**

| | Value |
|---|---:|
| Toffolis | 609,665,674 |
| T (exact seven-T) | 4,267,659,718 |
| T (4 T per Toffoli, Jones/Gidney; floor convention, q+) | 2,438,662,696 |
| T-depth (E02 convention: capped batches, ASAP inside leaves) | 776,965 |
| Toffoli depth (reaction convention, Cliffords free) | 201,263 = 2 × 84,595 (F, F⁻¹) + 2 × 1,008 + 1 + 30,056 (linear reflection ladder) |
| Dependency-only F Toffoli depth (unlimited width; lower bound) | 46,528 per direction |
| Dependency-only forward T-depth | 184,525 (equals the recorded `dependency_only_forward_t_depth`) |
| Logical qubits | 4,460,479 (≤ 1e7 primary width) |

One provenance note. In this checkout `compact_parallel_v7._storage` stops at a lookup-leaf key provenance check: the
current `LOOKUP_LOWERING` no longer hashes to the archived keys. That check affects no count. Path A therefore reads
the widths from `schedule_capped.json`, whose hash equals the E02 binding and which E02 asserted equal to `_storage`
at emission.

## 3. Estimator level (window class, per shot)

| Piece | Construction | Cost |
|---|---|---|
| Window state | g = ⌈log₂(2N+1)⌉ = 18 qubits, two's-complement n | ≤ 2^18 rotations (P2 count) |
| Offset e^{inτ} | diagonal | 2(g+1) rotations |
| Step code | (sign, 16 binary bits, top) out of place from n; weights 1…2^15 and 35,389 (sum N); **emitted and verified for every \|n\| ≤ N** (201,849 cases; also N = 1,730 and 102,602) | 148 Toffolis, computed and uncomputed |
| Controlled powers | step j applies d_j controlled U2 iterates on code bit j | N = 100,924 iterates |
| Direction-select | Q^{−n} = R Q^{n} R, where R is the controlled reflection (an involution); two reflections controlled on the sign | 420,784 T |
| Inverse QFT over Z_G | | g(g−1) rotations |
| Rotations | 262,488 per shot at 130 T each (lit: Ross-Selinger, 2^-40; same as P2), counted fully serial (q−) | 3.41e7 T |

The overhead outside the iterates is 0.17% of the layers (QF). Per shot this gives:
- T: 2.46e14 (QF) or 4.31e14 (literal);
- quantum time: 2,035 s (QF) or 7,845 s (literal), against T_C = 8.89 s.

Width: 4,460,479 + 18 (phase register) + 130 (step-code scratch) = 4,460,627, an upper count, inside the primary 1e7.

**M.** M = 10 × (layers per shot) × t_layer / T_C. This is the headline identity with k·(σ/e) = N, and it reproduces
the run006 floor M of 26.076 to 1e-9.

## 4. What this does and does not establish

- **Established (R1, meas):**
  - the U2 wrapper exists as a verified clean circuit, with the support and readout premises discharged;
  - the full controlled iterate and the estimator wrapper are counted exactly from emitted arrays;
  - the compiled iterate is 10.6-338× the floor per iterate, depending on convention, so the headline floor M is a
    valid quantum-favourable lower reading.
- **Modelled:**
  - the rotation T cost: 130 per rotation, lit;
  - the 4-T Toffoli QF reading;
  - the log-depth-reflection favourable reading (not emitted);
  - the window state-preparation rotation network, counted by the P2 count, with its gates not emitted.
- **Not compiled (out of scope; H items, frozen until HW-ACT):**
  - physical layout and routing: the schedule is all-to-all logical;
  - magic-state factories (H06);
  - decoder and reaction latencies beyond the 100 ns convention (H17);
  - physical error rates (H18).
- **Still open for R2:** independent peer review, a preregistered scope and a saved verifier and receipt. A re-check
  of the `_storage` provenance drift is also needed before any lifecycle run. That drift sits in repository code,
  not in these counts.

## 5. Files

- **Scripts** (`research/claim_debts_20261022/c11/`): `c11_common.py`, `u2_wrapper.py`, `iterate_compile.py`
  (path A, `-B -m`, numpy/numba), `recount_independent.py` (path B), `estimator_compile.py` and `summary.py`. All
  scripts except path A run under `.context/frontier_t0_env` 3.12.4 with `-I -S -B`. Script sha256s are in
  `summary.json`.
- **Outputs** (`results/claim_debts_20261022/c11/run001/`, exclusive-create): `u2_wrapper.json`,
  `u2_selector_gates.json`, `iterate_compile.json`, `iterate_recount_pathB.json`, `estimator_compile.json` and
  `summary.json`. The progress rows are in `results/claim_debts_20261022/c11/progress.jsonl`, which also holds rows
  from one smoke run whose output folder was deleted.

## 6. Premises (path, sha256)

| Premise | sha256 |
|---|---|
| results/limitation_program_20261001/E02_financial_run002/B8x52/iterate.json | 47b29f687e8ea4384034512cb0c34dc48f1c9143759301e9e3f7774f0adeaba8 |
| …/E02_financial_run002/B8x52/selector.npy | b68fa5ea2cb1b2bbf64300b497ce66eff1042fed5e3557f1f9956de5eef96f74 |
| …/E02_financial_run002/B8x52/reflection.npy | 837b10dfb1e60da28b7a5a9dcd218ba37c1fb8bc65b30c513a2b452547f101c6 |
| results/limitation_program_20261001/A10_coefficient_run001/B8x52/min-depth/source.json | b1a920b5cf3f20775ab042f43368bc2fc578bfeef7488c00d8d9ce4ad26a6ef8 |
| …/min-depth/target.json | 267dcaa74aa9dd5cb1339c65006b122389331f42f0002f483bd6eed05c31090b |
| …/min-depth/schedule_capped.json | 1a94a9ef56d9d982fa54a97289710129e119fea24c92ce6e835784028d555c71 |
| …/min-depth/leaves/*.npy | each checked against its leaf JSON sha256 |
| results/limitation_program_20261001/E03_support_run001/B8x52_certificate.json | 1bdfff95f143236549e928d305440eb5e522a69822aeb743e87563e8008ec8a8 |
| results/limitation_program_20261001/E03_support_audit_run002/B8x52_audit.json | babcab95778dd1b8ca920e265ad30e0e7249ad7fe0f577f75e5624cc2276c00a |
| results/frontier_probe_20261021/p2/run002/p2_window.json | 0447dd06e08262f53cd52d32d3c16c24e21c56044b45339619321719aced1094 |
| results/frontier_probe_20261021/p2/run003_self_mean/p2c_self_mean.json | 184cfe14576b6b48d443aca6dca7aec44a0a52c64ca84009acf02fcf1cf11dec |
| results/frontier_probe_20261021/headline/run006/headline_table.json | fd1eba885642fa61fae7cdc6abf67b875ed395d5c2bfd9c4cbfdd07c73057c7c |
| research/journal_sprint/reversible_fixed_point.py (imported read-only) | 52584dee87c84541b9f9e2f070114d7276de3d49d306d33c471214795b729b8b |
| research/limitation_program_20261001/native_payoff_estimator_v2.py (path A, read-only) | f25781deef230c08bb519d5f8782481a1959837838847c5f1d66ae0048fb5f07 |
| research/limitation_program_20261001/checkpoint_circuit.py (path A, read-only) | 304c4f3835ce1895427307ed77b691fb8f24b4a0c77855407f832b3da489315e |
| research/controlled_source_completion/primitives.py (convention reference) | 02b983af3f5afb538f5448aad372e214f6a3740a0c19fb017d633e302a278daf |
