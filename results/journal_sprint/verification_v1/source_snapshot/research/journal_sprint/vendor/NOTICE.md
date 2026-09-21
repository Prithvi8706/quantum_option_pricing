# Geometric-ladder maximum-likelihood comparator

`mlqae_core.py` is an unchanged copy (apart from newline normalization) of
`mlqae/core.py` from https://github.com/unitaryfoundation/csAE at commit
`202ffb8a462828d04dab13eef5005e295270d0e3` (retrieved 9 September 2026).
Author: Farrokh Labib / Unitary Foundation. License: Apache-2.0, reproduced in
`LICENSE-csAE`. Paper: https://arxiv.org/abs/2609.02715v1.

This file is a comparator, not this project's contribution. Its simulation
convention estimates `b=sin(theta)` from `cos((2*k+1)*theta)^2` observations.
The project's pricing prototype estimates a probability `a=sin(theta)^2`.
Published constants and source query accounting are reproduced separately and
must not be silently relabeled as probability-error or price-error results.

No claim is made that the upstream finite-grid ML search proves global numerical
optimality on every input. Source self-checks and independent benchmark
replication are recorded separately from the conditional interval construction.
