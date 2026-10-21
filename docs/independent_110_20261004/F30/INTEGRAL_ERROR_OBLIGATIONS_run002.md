The F30 D1 fits supply finite weighted-grid diagnostics only. They do not
certify the original Gaussian Asian price within any G2 dollar allowance.

The 33 by 33 training weights are unnormalized Gaussian Gauss-Legendre
weights on [-4,4]^2. Their computed total product weight is
0.9998733190449346. The corresponding computed training integral is
10.190374782365748 dollars. Neither quantity is a directed numerical
enclosure of a continuum integral or probability mass.

For these fixed positive weights, weighted Cauchy gives
abs(sum(w_i*w_j*(F_ij-Fr_ij))) <= sqrt(sum(w_i*w_j))*weighted_residual.
The run checked this finite identity numerically for all three ranks. The
floating residuals and singular values are diagnostics; no rounding
enclosure was constructed. In particular, the rank8 residual near6e-15
does not prove an exact rank8 continuum representation.

The following original-price contributions remain unresolved:

- Gauss-Legendre quadrature error for the exercise kink and full integrand.
- The price contribution outside the Gaussian training cube; it is not
  bounded by the omitted probability mass alone for this unbounded payoff.
- Error of the prescribed per-core linear interpolation and endpoint
  extrapolation on unobserved points.
- Directed rounding and the bridge to the original dollar allowance.
- Error of any future signed/normalized coherent representation, its
  controlled rotations, synthesis, inverse and estimator.

The 512 validation normals have the separately declared Gaussian law
conditioned on the cube. Their fixed pointwise RMSE/max errors bound none
of these continuum contributions. The data were shared across all ranks,
and validation selected no rank. Negative fitted values were retained.

No certified coherent loader was supplied, so loading, inverse, sign and
normalization handling, workspace and cleanup, preparation, reflections,
estimation confidence, readout and physical overhead remain paid unknown
inputs. No matched contraction/loading time or20percent quantum improvement
was measured. Stop at the three frozen ranks; do not compile or adopt this
quantum tensor route from these diagnostics. Classical training, SVD and
all1,601 integrand evaluations remain charged to the nominated price.
