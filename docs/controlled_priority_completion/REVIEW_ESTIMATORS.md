# Independent review of the explicit estimator schedules

22 September 2026. Reviewer: the capacity/publication subagent, which did not
author either estimator. **No blocker was found in the ideal digital estimator
derivations or recorded schedules.** This is not approval of the tight digital
moment assumption, the full financial price certificate or physical feasibility.

Reviewed files: `estimator_hadamard.py`, `estimator_bounded.py`, their supplied
tests, generated schedules and bounded-selector wrappers, the compiler envelope
and signed-reflection implementation, and the relevant source papers. Existing
resource artifacts were read without regeneration. Independent checks are in
[capacity_estimator_review.py](../../research/controlled_priority_completion/capacity_estimator_review.py),
with SHA-bound output in
[capacity_estimator_review.json](../../results/controlled_priority_completion/capacity_estimator_review.json).

## Proof and implementation findings

The Hadamard derivation follows [Kothari and O'Donnell, Theorem 3.21,
equations (48)-(55), and Section 3.6](https://arxiv.org/abs/2208.07544).
The declared RMS upper bound safely weakens both angular bounds. The selected
cosine intervals remain inside the required monotonicity regions: the small
interval is below pi and the large interval lies inside (0,2pi), whose cosine
maximum is attained at an endpoint. The spectral bad event is charged on the
unfavorable side in both promise cases. Zero mean is the limiting case covered
by the cited proof; direct zero-mean unitary checks also passed.

Both interval updates preserve a valid mean-containing interval whenever the
promise test is correct. In the gap, either answer is valid; absolute distance
does not confuse a mean left of the anchor because that region lies wholly in
the small promise. The anchor and endpoint operations remain exact rational
arithmetic until the declared f64 load. Per-stage bounds are uniform in the
adaptive anchor, so a union bound remains valid without assuming independence
between stages. Independent fresh preparations are required within each
binomial test and are counted in the schedule.

The independent script re-evaluated all 149 selected stage inequalities with
100-digit interval arithmetic and recomputed both binomial tails using its own
exact rational sums. Worst-promise union bounds are 0.0023827702/0.0020174409
for tight C4/H8 and 0.0023800414/0.0023626978 for their support-moment versions,
all below the allocated 0.003. Controlled-U calls, preparation repetitions,
geometric stopping radii, arithmetic T counts and phase multiplicities reconcile.
An additional 288 direct matrix-power cases tested three-point laws, both signs,
zero and promise-boundary means, including rare outcomes of probability 1e-8.
The smallest observed probability margin was 0.07433. These sampled checks
support the implementation; they do not replace the theorem or certificates.

For shifted QAE, the exact signed shift/comparator maps the f40 source to
`p=(Y+128)/256` over 48 uniform selector bits. The declared source support makes
the bit-flip shift valid without modular ambiguity. The hierarchical wrapper
contains financial forward and inverse, selector and inverse, and a signed
controlled reflection over both random registers. The reflection's final Z on
the control is necessary and is present. In addition to the supplied exact
selector basis and inverse tests, independent finite-dimensional sign checks
verified the Grover cosine law in 186 cases.

[Montanaro, corrected Theorem 2](https://arxiv.org/abs/1504.06987) supplies the
uniform amplitude-estimation guarantee. The script independently verified its
M=524,288 error bound by interval arithmetic. The exact median failure is
0.00296846343 for 15 repetitions, below 0.003. All 7,864,305 controlled iterates,
the financial/selector inverse multiplicities, exact controlled-pi/2 T gates
and 6,885 remaining arbitrary IQFT rotations reconcile. State preparation and
all QPE measurements are reported separately from arithmetic work.

## Scope and resolved issues

No new mean-estimation theorem or first Hadamard construction is established.
The finite design search certifies its chosen schedule and does not prove
optimality. The conditional tight rows use a supplied moment; their ideal
failure guarantee is conditional on that bound applying to the implemented
digital law. The bounded-QAE rows remove that premise for the residual mean.
Neither closes the surrogate, policy-regret or real-versus-digital price bridge.
Approximation, rotation synthesis and physical failure budgets remain separate;
the estimator's 0.003 must not be advertised as total failure probability.

The first test attempt using the older research environment with user-site
packages disabled failed because pytest was absent there. The documented
reused-environment command passed 14 tests but drew pytest from the user site.
This review reran the same 14 tests successfully in the prior isolated
`controlled_closeout_repro` environment with `PYTHONNOUSERSITE=1`; the independent
review script passed there as well. The estimator author has been informed so
the reproduction text can report the actual environment rather than implying
isolation. The existing pinned requirements include pytest, NumPy, SciPy,
mpmath and numba.

The review also corrected the reviewer's own capacity extraction: it now uses
the new one-control Hadamard logical allocation instead of retaining the old
QPE register count. This removes 21/23 redundant logical qubits in tight C4/H8
and does not change the mapping decision. A targeted regression check protects
that interface.

Reproduction in PowerShell:

```powershell
$env:PYTHONNOUSERSITE='1'
.context/controlled_closeout_repro/Scripts/python.exe -m pytest research/controlled_priority_completion/test_estimator_hadamard.py research/controlled_priority_completion/test_estimator_bounded.py -q
.context/controlled_closeout_repro/Scripts/python.exe -m research.controlled_priority_completion.capacity_estimator_review
```

The remaining blockers are scientific/modeling obligations outside this ideal
estimator certificate: certify or abandon the tight digital moment, complete
the financial bridge, and exhibit a priced physical schedule satisfying the
declared latency/qubit cap. This review does not turn conditional upper resource
schedules into lower bounds against all quantum algorithms.
