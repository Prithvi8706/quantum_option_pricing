# Week 3 circuit gate: prospective discovery protocol

Local-only simulation, no hardware, no confirmation data. Freeze this protocol
before generating results. It extends the week-1/2 feasibility study without
altering its source snapshots or the July protocol.

Ideal matrix: E001/E030, n=3/4, c=.125/.25, k=0/1/2: 24 circuits.
Construct the real distribution-plus-payoff A circuit, the objective Z reflection,
and A-inverse/zero-state-reflection/A for each Grover iteration. Reflect about
the complete all-zero input, including work qubits. Compare marginal objective
probability with the independently calculated grid objective amplified as
sin²((2k+1)arcsin(sqrt(a))). Tolerance: 1e-9 absolute probability.

Compile to u/cx at optimization level 0, seed 317, no coupling-map constraint.
Record total qubits (not just distribution-register size), depth, u/cx counts,
construction/transpilation/simulation times, and dense statevector/density-matrix
storage lower estimates. These are logical all-to-all circuit profiles, not
device timings or fully routed costs. Preserve QPY and a pre-execution event.

Noise subset: the 12 n=3 circuits. Use density-matrix probabilities without
sampling, separately for depolarizing lambda=.001 after every cx and amplitude
damping gamma=.005 after every u on its target qubit. All other gates are ideal.
These channel strengths are illustrative, not eta values in the old response
model. Retain noise-model dictionaries and targeted instruction counts.

Positive controls: density-matrix no-noise probability matches statevector;
X|0> then full amplitude damping on the u gate yields P(1)=0; prepare |11>
through u gates and apply cx with full two-qubit depolarization, giving marginal
P(1)=.5. Controls use the same basis and simulator, without optimizing away gates.
Tolerance 1e-9. Actual pricing noisy probabilities are diagnostics, not required
to fit exponential visibility. No fitted noise envelope or finite-shot coverage
claim follows from this gate.

Execution is single-threaded with a 15-minute between-circuit soft limit.
Retain errors and partial events, use a new directory for any retry. Do not
expand n or k during this run. Asymmetric readout, drift/correlation, stronger
comparators and classical baselines remain subsequent week-3 tasks.
