# Removing reverse Toffoli gates from temporary AND cleanup

Investigation date: 1 October 2026. This is an ideal-circuit component result, not a pricing benchmark or a change to the production compiler.

The original document's section 3 says that reversing intermediate calculations doubles the work. That describes the current construction. It is not a necessary rule for every intermediate. We verified one small exception: a temporary AND bit can be erased without a reverse Toffoli, while preserving its useful output and quantum coherence.

## The exact small problem

Two input bits are called `a` and `b`. A clean temporary bit `t` receives their AND, `t = a AND b`. The computation uses `t` to flip a separate output `y`. We want to restore `t` to zero while preserving the transformation of `y`. Inputs and output may be in superposition and entangled with a reference qubit.

The current style of implementation uses:

1. `Toffoli(a, b, t)` to compute the temporary AND.
2. `CNOT(t, y)` to use it.
3. `Toffoli(a, b, t)` to erase it.

The reverse Toffoli in step 3 is the only part this experiment replaces.

## The alternative and its proof

Apply a Hadamard to `t`, measure it in the computational basis, and call the outcome `m`. If `m = 1`, apply `CZ(a, b)`. Reset the measured temporary bit to zero.

For arbitrary amplitudes, immediately before cleanup the state has the form

`sum alpha[a,b,y,r] |a,b,ab,y XOR ab,r>`.

The Hadamard and measurement multiply each surviving amplitude by

`(-1)^(m ab) / sqrt(2)`.

The conditional CZ contributes the same sign, so the signs cancel. After resetting the measured bit, **each measurement branch** is exactly

`(1/sqrt(2)) sum alpha[a,b,y,r] |a,b,0,y XOR ab,r>`.

Each outcome has probability one half, independent of the logical input. Consequently, the outcome reveals no information about the inputs, and discarding that outcome does not destroy their coherence. This is a linear-map identity, including for inputs entangled with an arbitrary reference.

Measurement-based temporary-AND cleanup is established prior art; Gidney's construction also reduces its preparation cost. We verified the cleanup identity independently and did not implement the paper's four-T preparation circuit. [Gidney, Halving the cost of quantum addition](https://arxiv.org/abs/1709.06648).

## What was actually executed

The standard-library script [verify_and_cleanup.py](../../research/limitation_audit_20261001/verify_and_cleanup.py) simulated five ideal qubits: `a`, `b`, `t`, `y`, and a reference. It checked both unnormalized measurement branches against the reference unitary divided by `sqrt(2)`.

| Check | Result |
|---|---|
| All columns on the temporary-zero input subspace | 16 of 16 passed for both branches |
| Additional seeded complex superpositions, allowing reference entanglement | 64 of 64 passed for both branches |
| Maximum amplitude difference from the expected branch | 0 in the executed floating-point calculation |
| Maximum probability deviation from one half | 2.78e-16 |
| Deliberately omit the phase correction | Output fidelity falls to 0.625 on the chosen superposition |

The negative control matters: checking only classical output bits could miss the phase error. The successful branch-column comparison and the algebra above check the coherent transformation.

The saved [JSON receipt](../../results/limitation_audit_20261001/and_cleanup_v1.json) records Python 3.9.13 and the scope. Reproduce without creating another receipt:

```powershell
python research/limitation_audit_20261001/verify_and_cleanup.py
```

## What this saves and what it costs

Under the repository's exact seven-T Toffoli lowering, this eligible cleanup changes **seven T gates to zero T gates**. The replacement needs a Hadamard, a measurement, and conditional Clifford correction/reset. The compute and use stages are unchanged. See [compiler.py](../../research/controlled_source_completion/compiler.py) and [primitives.py](../../research/controlled_source_completion/primitives.py) for the existing lowering.

This is not a sevenfold speedup of the oracle, and it does not halve its runtime. Measurement and feedback consume time; eligible temporary ANDs are only part of the computation. A different native gate set also changes the relevant cost comparison.

## Conditions that must hold before using it in the compiler

The temporary must start clean. At cleanup, its value must still equal the AND of the controls used for the correction. Its intervening uses must preserve that relationship. The output use in this experiment is a CNOT. Arbitrarily measuring a scratch register after arbitrary arithmetic is not covered.

A compiler integration must identify eligible lifetimes, maintain the phase correction through scheduling, and implement dynamic measurement and classical feedforward. It must check the source and inverse interfaces on their promised workspace subspaces. The current unitary gate-list backend does not gain those capabilities from this demonstration.

The next bounded experiment is one real arithmetic leaf containing a recognised temporary AND: compare its full coherent channel, T count, measurement depth and workspace against its existing emitted circuit. Accept it only if exact semantics and scratch cleanup hold, and report latency under an explicit feedback model. Reject a proposed rewrite when the controls change before cleanup without a valid replacement correction.

**Status: the small cleanup identity is solved in the literature and verified here. Its profitable application to this pricing compiler remains to be demonstrated.**
