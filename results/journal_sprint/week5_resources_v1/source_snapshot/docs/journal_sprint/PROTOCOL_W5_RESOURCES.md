# Week 5 missing k=2 logical resource profiles

Prospective discovery extension, not a modification of the week-3 archive.
Profile E001/E014/E025/E049 at n=5/6, c=.125, and additionally E001 at c=.25:
10 circuits, all k=2. Reuse week-3 k=0/1 profiles only after integrity checks.

Compile the full preparation/reflection/amplification circuit to u/cx,
optimization level 0, seed 317, without device topology. Save QPY and counts,
depth, preparation-plus-compilation time, total case time and estimated dense
statevector storage. Verify every objective marginal against the analytical
amplified finite-grid amplitude to 1e-9; no gate-noise or density simulation.

Initial E001/n5/c=.125/k2 must finish build/compile/statevector within 120 seconds
and estimated state array <=16 MiB. Apply the same 16 MiB check to all cases and
a 15-minute between-case run limit. These are soft timing gates, not a measured
peak-memory limit or a timeout capable of interrupting a single compile call.
Preserve failures; do not overwrite completed paths or silently reduce depth.

This fixes a missing cost profile, not practical hardware feasibility. Equal
A-equivalent costs need not imply equal compiled costs: the full-register zero
reflection is not free. CX comparisons remain one logical cost axis, not a
complete device runtime or total-cost model.
