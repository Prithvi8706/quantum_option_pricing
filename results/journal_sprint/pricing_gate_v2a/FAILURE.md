# Retained failed first attempt

The deterministic runner completed computation but failed while serializing
`rows.json`: a NumPy boolean was not JSON serializable. That file is incomplete
and must not be analyzed. There is no completion marker.

Fix: explicitly convert the validation status to a native bool. No scientific
parameters changed. Rerun is linked as `../pricing_gate_v2a_retry1/`; the original
source snapshot and partial output are retained. This is not a successful run.
