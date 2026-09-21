# Invalid smoke: adapter stream reset

Do not use this result to assess BIQAE accuracy or coverage. The local adapter
passed an integer seed to Qiskit 1.4.2 StatevectorSampler; it restarted the
same random stream for successive jobs, duplicating k=0 measurement batches.
This is our sampling-adapter defect, not a finding against the upstream algorithm.
The corrected retry uses one advancing NumPy Generator. Original files retained.
