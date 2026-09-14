# Historical baseline reconstruction

Macroscope correctly found that the V2A historical snapshot omits PROTOCOL_V1,
although the original planned source hashes record that dependency. The snapshot
is an immutable historical capture, not a self-contained executable repository.
Do not edit it or regenerate its completion manifest to hide the omission.

The supplemental original V1 protocol is now distributed separately at
`results/journal_sprint/v2a_replay_supplement_v1/PROTOCOL_V1.md`. Its SHA-256 is
`a99f2faf3e6e262574dc9099d9eacc0f00d3ef2ab2386bef9a33e9d6ac99912f`, exactly the
hash already recorded in the baseline's original `planned.json`.

From the repository root, create a new reconstruction directory:

```text
python -m research.journal_sprint.materialize_baseline PATH_TO_NEW_DIRECTORY
```

This verifies the baseline manifest and supplemental protocol, copies the
historical sources, and adds the missing protocol plus the comparator license,
notice and candidate legacy environment recipe. It refuses existing destinations.
The supplemental files are not silently claimed as original snapshot members.
Install the recipe in a separate Python 3.9 environment if execution is required.
Materialization does not execute benchmarks or establish environment equivalence.
Other historical provenance gaps are not cured merely by supplying V1.
