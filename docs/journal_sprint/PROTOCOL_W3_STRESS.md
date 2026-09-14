# Week 3 readout and dependence stress protocol

Prospective discovery experiment; local response sampling, not hardware or a new
full-circuit execution. Use the four n=3 contract/scale groups from the completed
circuit gate, with k=0,1,2, 1024 shots per depth, 500 independent repetitions.
Verify the input manifest before execution. The ideal probabilities are the saved
actual circuit marginals. Their small numerical deviation from the analytical
model is below the prior 1e-9 gate tolerance.

Conditions: ideal independent binomial; asymmetric readout with P(report1|0)=.02
and P(report0|1)=.07; run-level drift with shared random sign and additive shifts
sign*.03*(-1,0,1) across the ordered depths, clipped to [0,1]; and beta-binomial
overdispersion with independent latent depth probabilities of mean q and
concentration 100. Draw counts conditionally binomial in both dependence cases.
Record the latent probabilities. Latent variation induces within-depth dependence
in the unconditional shot law; drift is an ordered-batch stress, not a detailed
time-resolved hardware simulation.

Analyze all four with the ideal independent-binomial inversion, intentionally
misspecified for the three stress conditions. Additionally analyze the exact same
readout counts using known affine readout inversion. This yields 8000 distinct
count datasets and 10000 inference records. The correction knows the stipulated
readout constants exactly; estimating their uncertainty is outside this test.

Nominal alpha=.05, Bonferroni over three depths; retain all branches. Primary
outcomes: true ideal amplitude containment, incompatible frequency, nonempty
frequency and containment among nonempty outputs. Secondary: hull radius, and
erroneous claims at amplitude radius .005 (unconditional and among declarations).
These are amplitude diagnostics, not dollar guarantees or practical speedups.

Every inference records counts, latent response, components and query counts.
Each physical synthetic dataset has 3072 shots, 9216 A-equivalent queries and
3072 Grover calls. Reanalysis of readout counts incurs no extra quantum sampling;
do not sum both analysis rows as independent acquisitions. Archive source,
protocol, input hash and planned events before outcomes. Use exclusive output
directories and preserve failures. No tuning or model fitting follows coverage
inspection in this run.
