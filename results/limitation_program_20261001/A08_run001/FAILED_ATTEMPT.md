# Preserved initial A08 harness failure

The root `protocol.json`, `executed_code/` and `failure.json` describe the first prospective attempt. It passed 20 arithmetic/prefix tests and failed two toy integration assertions because the test tried to XOR a scaled floating-point evaluator output with a raw integer initial output.

The corrected harness requests `evaluate(target, sample, True)` and uses the raw integer SSA trace to form expected XOR words. `carry_lookahead.py` and its arithmetic semantics were unchanged. The first attempt ran no static financial-source screen and no financial gate replay.

The successful fresh prospective attempt is stored in `attempt002/`. Its protocol and snapshots were saved before its tests and screens. All22 tests passed; both prefix families then missed the preregistered2% complete-source T-depth threshold. The accepted A10 inverse source remains the baseline.

The failed root receipts remain distinct from the successful nested receipts; do not treat their dependency hashes as one executed-code version.
