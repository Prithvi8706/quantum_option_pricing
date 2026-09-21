# Stronger arithmetic comparator: bounded development protocol

Date: 2026-09-21. Authorized development follow-up to the prepared baseline design.
Implementation and small correctness checks precede the frozen acquisition.
The acquisition manifest records exact source, protocol and input hashes; source
changes require a new output archive. No confirmation or hardware execution occurs.

## Fixed scope

Retain archived D1/D2 arithmetic Asian-basket contracts, Gaussian coefficients,
cutoff 4, ten bits per coordinate, $1 absolute pricing error, at least 95%
confidence, 17 AE repetitions and the 10,000,000-call cap. Use both historical
logical CX ledgers with corrected inverse-QFT swaps. Physical errors are unknown.
Keep all original evidence immutable. Do not inspect new held-out cases.

## Ordered ablations

1. Re-emit the original width-40, fraction-20, degree-24 arithmetic conversion.
   Compare retained and shared clean scratch layouts for the identical integer
   map. Only zero, disentangled scratch can be reused; retain row log/spot outputs.
   Count actual emitted gates and track dependency depth in each layout.
   Both new layouts also share the clean aggregation/postpayoff/comparator carry;
   this saves two wires versus the archived allocation, without changing gates.
2. Range-reduced exponential: signed arithmetic shift by s; fixed-point Horner
   for exp(x/2^s); s fixed-point squarings; exact integer spot multiplication.
   Evaluate the full Cartesian menu of fractional bits {20,24}, widths {40,48},
   degrees {8,12,16}, and s {1,2,3}, for each D case (72 configurations total).
   Retained and reused scratch are paired layouts, giving 144 reduced-route rows.
   Preserve infeasible entries; do not choose precision after observing winners.
3. Assess the signed residual/control route separately. Its admission requires
   a universal residual bound, shifted signed encoding, certified offset and
   decoder, and emitted control compute/uncompute costs. If any is missing,
   record a blocked arm with explicit reasons; do not fabricate a combined cost.

Use efficient ripple aggregation. The earlier fixed-menu Fourier finding is
retained; repeating the more expensive aggregation is outside this conversion
study. A comparison across layouts is separate from changing the exponential.

## Certification and bounded execution

Directed decimal certificates include affine quantization, signed shift rounding,
coefficient/Horner errors, Taylor remainder, every squaring, final spot scaling,
signed range of all intermediate stages and sums/poststrike, and selector range.
Carry these into the existing continuous representation/loading/decoder/AE ledger.
Failed certification yields an infeasible row, not a fabricated resource result.

Before acquisition, test small signed inputs exhaustively against independent
integer evaluation; test nonzero XOR outputs, clean scratch, complex amplitudes
and inverses. For production conversions check packed zero and maximum inputs.
Exhaust small q=1/2 financial grids as diagnostics (not statistical trials).

Per emitted conversion cap: 8,000,000 X/CX/CCX gates and 4,096 wires. Per full
arithmetic component cap: 100,000,000 emitted gate applications. Stop a row on
cap failure and preserve the reason. Stream/remap components rather than allocate
a production statevector. Two independent case workers are allowed; collection
order is fixed. No full AE circuit simulation is attempted.

## Outcomes and closeout

Primary: minimum feasible control-cancelled logical CX projection per contract
over the entire menu. Secondary: conservative CX, allocated qubits, arithmetic
dependency depth, deterministic dollar bound and AE calls. Include original
arithmetic and archived reflection references with explicit compiler limitations.
Report ties and reversals. These are projections, not runtime measurements.

Freeze executable sources before acquisition, retain complete manifest/failed runs,
replay certificates and finite diagnostics for every row in the separate pinned
environment, and re-emit the old baseline and selected reduced circuit per case.
The verifier also supports the more expensive complete circuit re-emission;
report which scope actually ran. Obtain independent AI code/math review.
AI review does not substitute for the prepared human novelty assessment.
Candidate status remains standby; production selection and confirmation admission
remain unset regardless of this bounded experiment's outcome.
