# Independent A20 V2 static review from the A13 continuation

Verdict: hold V2 execution. One confirmed operational blocker prevents authentic
selected A10 ownership admission before scientific work. A separate operational
release must fix it and receive its own static freeze. No producer, auditor,
builder, Receipt method, gate recipe or scientific check was executed in this
review. The originals remain unchanged.

Reviewed exact files under `research/limitation_program_20261001/`:

| File | SHA256 |
| --- | --- |
| arithmetic_free_basket_signal_v2.py | 4d7a7169d3bf13ef79417f97cb9dcf33bc9a7d009f9e9e6294284760f0a6ea1a |
| a20_signal_receipt_v2.py | 25fcef657d3699a54f5ee7daf0783ccf5948359604dd10e293b545739f2498bd |
| experiment_arithmetic_free_basket_signal_v2.py | ca96c32e9d53e49da5e24b5d96df017d4f65b7ab913a3b74441d3e6d8645f4ed |
| audit_arithmetic_free_basket_signal_v2.py | 64327303b9658ecb920829241b1df9c42120773a2b3df3747e6d97af1ffd3c7d |
| A20_COMPARATOR_PHASE_IMPLEMENTATION_PREFLIGHT_V2.md | 3efd3f0850348f4a0c8759de84fca3632f029cca81c49e5689cb7f74512d4546 |
| a20_comparator_phase_implementation_preflight_v2.json | 66eb828afe1ce31ff4b9d0be97f7ef889f9c9cc696ee7372ce2193fae507bbb5 |

Confirmed blocker: `Receipt.owner_memberships` admits the exact flat A10 manifest,
then compares each selected owned key to `relative_to(...).as_posix()`. The actual
selected key is `B4x12\min-depth\target.json`, with canonical ROOT spelling
`results/limitation_program_20261001/A10_coefficient_run001/B4x12/min-depth/target.json`.
That selected path is in the immutable original prospectus, its manifest and
prospectus SHA values agree, and the V2 spelling predicate is false. Reading JSON
and reproducing only the pathlib comparison confirmed this without invoking any
scientific controller. Restrict the new legacy spelling acceptance to the exact
already pinned flat A10 owner; retain canonical actual containment, exact SHA,
canonical selected keys, no alias acceptance and unchanged membership demands.

The scientific construction is internally coherent at static review scope:

- Flipping both signed72 comparator MSBs maps signed order to unsigned order and
  is inverted. `Z(c); CZ(c,p)` gives absolute phase +1 for c=0 or p=1 and -1 for
  c=1,p=0. Literal comparator inverse restores predicate and temporary words.
- The low53 uniform reference and high19 zero promise make exactly F of 2^53
  states satisfy r<F for 0<=F<2^53. The resulting one-stock zero block is
  (2F-2^53)/2^53. Selector H, reversible address selection, paid QROM, its inverse
  and the final selector H give the pair block (F1+F2-2^53)/2^53. Reference and
  selector output garbage is explicitly allowed; other scratch/addresses restore.
- The strict native floor contract is correctly represented by survival sum<280Q
  and positive payoff sum>=200Q+2. The threshold half-lattice gap is 1/(2*2^53)
  for this affine signal. This leaves a difficult downstream threshold transform;
  it does not imply a QSP or financial loading solution.
- The producer computes source-bound native scalar floors/shifts and verifies
  identical two-stock templates before table sharing. The auditor independently
  reconstructs scalar templates, circuits and native truth, with exact rational
  phase interpreters. It imports no producer/builder module. Absolute CCX phase
  is separately rechecked on eight complete exact columns.
- Fixed check counts agree by inspection: 32+64+304+128+32+2048=2608. The pair53
  diagnostic removes exactly 106 reference H gates in an explicit test view;
  those gates remain in the actual emitted recipe and resource accounting. The
  universal reference claim rests on counting and recognized reversible-array
  structure, not native53 statevector evidence or just finite boundary cases.
- Native X/CX/CCX/H/Z/CZ counts and controls/inverses/preparation are charged.
  The seven-T/15-row exact CCX macro gives six CX and two H per CCX; CZ lowering
  pays one CX and two H. Reported depths are conservative component upper
  bounds, with full-source and physical runtime explicitly unresolved.

Operational guards are substantial: role-specific externally frozen READY,
original expected SHA retention, exact prepared inventory and externally pinned
protocol, exclusive RUN_STARTED, fresh actual SHA unions, independently captured
runtime with base site-packages rejection, reserved output caps before ordinary
file writes, and failure marker precedence. Run failures after mutation retain
failed evidence; pre-mkdir admission failures have no new receipt and require
preserving the CLI log. A terminal manifest is not scientific approval until the
independent audit and ROOT integrity release pass.

Unresolved before execution: budget fit cannot be established statically; runtime
inventory/absent-cache stability must pass for actual prepare/run processes; all
2608 checks, independent reconstruction and final retention remain unexecuted.
This review found no further scientific blocker in the examined construction, but
is not universal correctness or execution certification. General full72/q32
access, source reachability/joint law, scalable offline build/load cost, threshold
transform, full-price construction, financial bias/G2 and physical delivery stay
open. Passing the component would complete only the restricted comparator-phase
screen. No fixture, price, replay, adoption or quantum-advantage credit is claimed.

Checks performed: syntax AST parse of four exact Python files, parse of V2 JSON,
SHA256 capture of all six files, read-only authentic selected legacy membership
comparison, source/template/phase/cleanup/resource/controller static inspection.
