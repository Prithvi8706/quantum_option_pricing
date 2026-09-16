# Conditional pilot-mixture discovery follow-up

Declared 2026-09-15 AFTER the initial rescue results. The Jeffreys anytime
variant improved both axes for only E025, failing its two-contract screen.
This follow-up reuses the same stored synthetic paths; it is post-result
method development, NOT an independent replication or a new acquisition.

One variant only: use the first 1024 observations as a paid pilot. Conditional
on that pilot, fix Beta(s_p+1/2,1024-s_p+1/2) as the mixing law. For each later
look, form the likelihood ratio using ONLY post-pilot observations; do not count
pilot data twice. Keep alpha_val=.025, original independent calibration,
original guards, caps, representation bounds, and all original 2160 acquisition
identities (including refusals). No declarations from the pilot alone. Inspect
only the remaining saved looks and stop at first $1 declaration or the cap.

Report all outcomes and compare against the original anytime and fixed-time
rows. Same promotion screen: improvement over the original linearized fixed
baseline on at least two non-E001 contracts, guard zero, both axes, zero
erroneous declarations observed. Also report the same-policy exact versus
linearized contrast. No post hoc significance or generalization claim.

Conditional validity follows because the mixing law is fixed before the
validation observations, and every null likelihood-ratio mixture is a
unit-initialized nonnegative martingale regardless of how the pilot chose the
mixing law. The initial calibration remains independent; its uncertainty is
not replaced with a point estimate. This is established sample-split inference,
not a newly invented martingale theorem.

Use an exclusive output directory, retain source-manifest hash, source
snapshots and every derived record. Verify the input archive before analysis.
