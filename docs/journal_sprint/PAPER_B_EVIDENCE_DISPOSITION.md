# Paper B dimension-sweep evidence disposition

Decision: **exclude both historical slope sets from the replacement manuscript**. This closes the immediate evidence-reconciliation decision by retirement, not by confirming either set or recovering missing raw data.

The manuscript snapshot retains the earlier approximately -1.14/-0.65 statements. Repository documentation also referred to a 100-trial update with approximately -.98/-.77. The checked-in `src/plot_dimension_sweep.py` instead specifies `N_TRIALS=10`, `N_REP=30`, five N values from 2^10 through 2^14 and 2,000 bootstrap resamples. The script stores per-trial arrays in memory and produces a figure; a figure alone does not establish the underlying historical run.

The evidence audit preserved the actual DOCX, available figure, producing-code candidates and recoverable Git provenance. On 10 September, a further read-only search covered the working-tree CSV/NPZ/NPY/JSONL/PKL files outside the environment and generated sprint artifacts, plus reachable Git history under data, results, outputs, figures, src and research. It located the dimension-sweep script and figure but no raw 100-trial dimension-sweep dataset. Search output is retained in `results/journal_sprint/week12_closeout_v1/paper_b_git_search.json`; earlier document extraction is in the historical audit artifacts.

This is a bounded repository search, not proof that no copy exists on another machine, private storage, deleted/unreachable Git objects or a collaborator's system. A path's latest commit is not proof of the revision that generated a result. No pickle was executed to investigate this discrepancy.

Neither choosing the more favorable slopes nor rerunning the current 10-trial script would validate a claimed old 100-trial run. If this experiment remains relevant, replace it with a prospectively specified run that records every estimate, reference, scramble, path count, seed, timing and bootstrap input. Label it a new experiment and use a distinct versioned output directory.

The first-two-week requirement “reconcile before reuse” is satisfied by **no reuse**. Recovery and independent reproduction remain future possibilities, not completed tasks. Original files were not deleted or rewritten.
