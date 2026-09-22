"""Render the decision from recorded artifacts, without fitting a winning case."""
import json
from pathlib import Path
from research.controlled_source_completion.run import ROOT


def main():
    sources=json.loads((ROOT/'compile_v2'/'summary.json').read_text())
    costs=json.loads((ROOT/'cost_v3_phase64'/'ledger.json').read_text())
    diagnostics=json.loads((ROOT/'diagnostic_v1'/'summary.json').read_text())['rows']
    tests=json.loads((ROOT/'validation_v2'/'tests.json').read_text())
    audit=json.loads((ROOT/'validation_v2'/'resource_reconciliation.json').read_text())
    selected={n:next(r for r in costs if r['model']==n and r['f']==40 and r['mode']=='continuous_moment_conditional') for n in ('C4','H8')}
    resources={n:next(r['resources'] for r in sources if r['model']==n and r['f']==40) for n in ('C4','H8')}
    source_table='\n'.join('| %s | %s | %s | %s | %.3f |'%(n,format(resources[n]['logical_qubits'],','),format(resources[n]['t_count'],','),format(resources[n]['t_depth'],','),resources[n]['t_depth']*1e-7) for n in selected)
    cost_table='\n'.join('| %s | %.3f | %.3f | %s | %.2f |'%(n,r['classical_full_price_seconds'],r['tenfold_total_budget_seconds'],format(r['ideal_unit_constant_source_calls'],','),r['ideal_unit_constant_source_seconds_100ns']/3600) for n,r in selected.items())
    modern_table='\n'.join('| %s | %s | %.4g | %s | %.4g |'%(n,format(r['ledger']['controlled_U_calls'],','),r['ledger']['arithmetic_t_count'],format(r['ledger']['logical_qubits'],','),r['sensitivity'][2]['serial_arithmetic_seconds']) for n,r in selected.items())
    numeric_table='\n'.join('| %s | %d/%d | %.3g | %.3g |'%(r['model'],r['fraction_bits'],r['uniform_bits'],max(r['max_errors']['Y_%d'%k]['max_abs'] for k in (3,6,9)),max(r['max_errors']['base_%d'%k]['max_abs'] for k in (3,6,9))) for r in diagnostics)
    body=f'''# Controlled compound source: completed feasibility investigation

22 September 2026. **No defensible significant quantum advantage established yet.**
The recommended complete-source/explicit-estimator investigation is now executed.
The first two follow-up priorities, independent validation and resource/precision
reconciliation, are complete as specified in [CHECKLIST.md](CHECKLIST.md). The
result rejects this constructed implementation under the stated latency screens.
It does not prove that every quantum approach to this financial model is impossible.

## Decision and acceptance contract

Keep the original compound call on the arithmetic Asian-basket continuation
value, the four development models, strikes 3/6/9 and the same controls. The
acceptance criterion remains a penny of absolute error, 99% per-price confidence
and at least a tenfold latency improvement over a strong eligible classical
implementation. A full price, its uncertainty and all setup/output costs count.
No held-out case was opened, and no manuscript claim was changed.

The previous variance pilot answered whether the put-complement residual was
small. This work answers whether an explicit coherent source and estimator can
exploit it affordably. They cannot in this implementation. Sampling savings are
overwhelmed by reversible path generation and analytic-control/policy arithmetic.
The same controls already make classical full pricing inexpensive.

The completed work is a resource/implementation result, evidence level 4. Generic
source-access quantum mean-estimation advantages remain literature-level results
at level 3, with no project-specific lower bound against structured classical
pricing. Neither level 1 hardware advantage nor level 2 conditional end-to-end
fault-tolerant advantage is established.

## What was actually implemented

The hierarchical source includes midpoint-uniform preparation, a reversible
Box-Muller transform, both halves of every GBM path, guarded stock evaluation,
arithmetic and geometric averages, geometric put/call controls, moment-matched
continuation, the existing regression where selected, analytic lower/upper
clipping, exercise decision, signed residual and inverse cleanup. There is no
free Gaussian loader, QRAM, path-price lookup table or assumed arithmetic leaf.
Finite one-dimensional coefficient QROMs are paid as emitted gates.

Every arithmetic leaf has a gate file. The source contains hundreds of millions
to billions of gates, represented hierarchically to reuse definitions. Its gate
executor traverses that hierarchy; it is not an analytic oracle-count formula.
Version 2 removes repeated expressions and folds constants exactly, reducing
T counts by about 10% from the preserved initial compilation.
The final estimator also fuses compute/phase/uncompute, removing a redundant
internal cleanup pair. This approximately halves the arithmetic of its earlier
modular wrapper. Both stages of resource evidence are preserved.

The estimator implements an explicit, conservative known-moment variant of
[Kothari-O'Donnell](https://arxiv.org/abs/2208.07544), using Theorem 3.19 and an
adaptive interval contraction. Integer QPE powers, majority repetitions, source
and inverse calls, controlled reflection sign, full inverse QFT, random-register
resets, classical endpoint loads, measurement and decoding are specified.
A machine-readable controlled-U gate envelope binds every wire. Arbitrary
rotations remain unsynthesized and are recorded as an outstanding cost.

This is not the paper's unknown-variance algorithm or a demonstration of its
optimal constants. The conservative confidence schedule is especially expensive;
its failure is not a refutation of the optimal query theorem. A separate ideal
query sensitivity below grants much better constants and still fails.

## Complete source cost

Representative strike-6 sources, 40 fractional arithmetic bits and 32 random
bits per uniform, after exact expression reuse:

| Model | Logical qubits, clean Y source | T gates, one clean Y | T layers, serial leaf schedule | Seconds per Y at hypothetical 100 ns/T layer |
|---|---:|---:|---:|---:|
{source_table}

A clean Y evaluation includes its internal inverse cleanup. The final controlled U
runs the financial graph forward, then the angle graph, applies phases and
inverts both graphs before reflection. Its redundant internal cleanups are fused;
the table still omits the angle and reflection cost of one iterate. Depth is a valid
schedule for this compiler, not a lower bound on arbitrary arithmetic circuits.
The logical timing assumption is hypothetical; CPU simulator timings were not
converted into quantum performance.

## Classical comparison and deliberately favorable crossover screen

The retained classical baseline uses controlled, vectorized randomized QMC and
policy/Jensen price brackets, with prior independent reference agreement. C4
retains the faster new parity implementation; H8 retains the faster earlier
implementation. Each measured time includes all three strikes and is charged
in full to one requested price, favoring the quantum comparison. Empirical 99%
intervals are distinguished from the stricter fixed-iid statistical contract.
The source's finite-law financial bridge is not yet proved; the screen below
grants it at zero cost rather than claiming mismatched targets are equivalent.

For illustration, suppose the entire quantum mean estimate required only
ceil(sqrt(moment)/error) clean Y calls, with coefficient one, no extra inverse,
no confidence amplification, free baseline/regret handling and free setup.
This is a sensitivity coordinate, **not** the implemented algorithm or a
universal query lower bound. Give it the previous tight continuous-model moment
bound for free, despite the unproved transfer:

| Model | Measured classical full-price seconds | Total budget for 10x win, seconds | Idealized Y calls | Arithmetic-only hours at 100 ns/T layer |
|---|---:|---:|---:|---:|
{cost_table}

Even at 1 ns/T layer, these favorable totals are approximately
{selected['C4']['ideal_unit_constant_source_seconds_100ns']/100:.1f} s and
{selected['H8']['ideal_unit_constant_source_seconds_100ns']/100:.1f} s. The stricter
C4 classical statistical bound cost 267.84 s, implying a 26.784 s tenfold budget;
the C4 ideal screen still fails that budget even at 1 ns/T layer. No GPU or
additional classical method needs to be weakened or excluded to get this result.

The explicit conservative estimator is much more costly. With the tight
continuous-model moment *conditionally granted*, financial source f=40 and
phase f=64:

| Model | Controlled U calls | Arithmetic T gates | Logical qubits per serial execution | Arithmetic-only seconds at 100 ns/T layer |
|---|---:|---:|---:|---:|
{modern_table}

These very large numbers are reproducible costs of this chosen schedule, not
predicted device runtimes or optimal-algorithm lower bounds. Giving all repeated
QPE runs independent hardware still leaves longest single QPE chains of
{selected['C4']['sensitivity'][2]['longest_QPE_arithmetic_seconds']:.4g} s (C4) and
{selected['H8']['sensitivity'][2]['longest_QPE_arithmetic_seconds']:.4g} s (H8) under
the same schedule/timing assumption. Optimizing constants cannot be confused
with a demonstrated crossover.

A separate schedule uses the unconditional digital support bound E[Y_d^2]<=B^2.
It needs roughly 4.65e11/4.74e11 controlled-U calls for C4/H8. Thus removing the
costly classical moment-certificate acquisition does not rescue this construction.
Using the tighter previous certificate would additionally charge 75.11 s/254.72 s
of acquisition including policy training, unless reuse is justified and shared
with the classical method. Surrogate pricing and regret certification are further
costs; H8's previous regret certificate also failed its assigned error budget.

In consistent units, a completed comparison would require

    T_setup + T_device + T_measurement/feedback + T_classical_outputs <= T_classical/10,
    T_device >= max(D_T * seconds_per_T_layer, N_T / delivered_T_states_per_second).

The known arithmetic already fails under generous assumptions. Synthesis,
non-T gate timing, routing, factories and error correction add obligations.
For example, even the illustrative data-only formula 2*d^2*Q at d=15 gives
{selected['C4']['data_physical_qubits_sensitivity']['15']:,} and
{selected['H8']['data_physical_qubits_sensitivity']['15']:,} physical qubits. These
distances are not justified for the enormous failure exposure, and factories
and routing are excluded. This is sensitivity analysis, not a physical design.

## First priority completed: independent validation

The focused test suite reports **{tests['pytest_summary']}**. In addition:

- All four financial models were evaluated on 64 paired finite-input paths at
  each of two precisions: 512 development pairs, with all three strikes checked.
- Every emitted gate was executed for C4 and H8 at both precisions, before and
  after optimization: eight complete source executions. Outputs were bit-exact,
  inputs preserved and all scratch clean. Each used a nonzero residual case.
- Sixteen extra random cases per compiled source verified bit-for-bit agreement
  before/after optimization. Production-width arithmetic leaves were checked.
- Three complete high-precision angle circuits were executed. Thirty-six
  nontrivial finite spectral laws passed their promised test cases. An actual
  nine-qubit QPE statevector agreed with the independent distribution formula
  within 3.19e-14. Explicit QFT order and controlled-reflection sign were checked.
- Four combined financial/phase arithmetic traversals checked the final cleanup
  fusion at both precisions for C4/H8, with bit-exact angles and restored inputs
  and scratch. The diagonal phases were checked by their computed basis values;
  the enormous pricing statevector was not simulated.

The independent financial evaluator used NumPy/SciPy on the *same finite inputs*:

| Model | Fractional/random bits | Maximum absolute Y discrepancy over strikes | Maximum discounted baseline discrepancy |
|---|---:|---:|---:|
{numeric_table}

There were no sampled exercise-classification mismatches. These are development
diagnostics, not confidence coverage, tail/overflow proofs or held-out success.
No complete pricing QPE, noisy device or fault-tolerant machine was simulated.

## Second priority completed: cost and precision reconciliation

An independent audit recomputed gate counts from {audit['unique_leaf_files']}
distinct referenced gate files, checked their hashes/wires and reconciled the
forward/copy/inverse totals for the four final financial sources and the 64-bit
phase source. No hidden arithmetic leaf remains. All source calls and QPE powers
are explicit. The full logical ledger also lists outstanding synthesized-phase
and physical costs instead of filling them with favorable guesses.

Forty fractional phase bits failed the conservative accumulated error budget.
The separate 64-bit phase implementation fixes that issue: all 288 atan table
coefficients were verified by exact rational rounding intervals, and the derived
uniform phase error bound is 2.143e-16. This fits the allocated coherent
approximation failure for both the tight-moment and support-only schedules.
It does not certify the financial elementary functions or the finite-input law.
Single-qubit rotation sequences at the remaining per-rotation tolerance have
not been synthesized. Their count and error tolerance are recorded explicitly.

The inherited dollar budget remains .003 surrogate mean + .002 flat correction
+ .003 exercise regret + .002 financial numerical error = .01. Failure budgets
are .002 surrogate + .001 moment + .001 regret + .003 ideal quantum tests
+ .0005 phase-function error + .0005 rotation synthesis + .002 physical = .01.
Several terms remain obligations, so no completed 99% full-price certificate is
claimed. Finishing an audit is different from passing every obligation it lists.

## Claim ledger and next decision

| Claim | Status |
|---|---|
| Same compound financial research direction, existing policy/controls retained | Implemented; prior evidence preserved |
| Complete clean digital residual source and explicit estimator gate schedule | Implemented hierarchically; arbitrary phases specified, not synthesized |
| Correctness on the stated independent diagnostics | Executed; limits above |
| About 10% fewer source T gates and removal of redundant estimator cleanup | Quantum implementation improvements only |
| Tiny sampled f=40 financial arithmetic discrepancies | Observed; no global financial error guarantee |
| Uniform 64-bit complex-phase arithmetic bound within its allocation | Derived and coefficient rounding checked |
| Tight continuous moment/regret certificates apply to the digital source | Unproved |
| Full continuous-price numerical/statistical/physical certificate | Incomplete |
| Significant quantum advantage or supported physical crossover | Not established; current construction fails the resource gate |
| All possible quantum implementations of this contract are ruled out | Unsupported |
| Novelty or journal acceptance from this work | Not established; requires a separate review of the concrete claim |

The remaining work is ranked in [CHECKLIST.md](CHECKLIST.md). P1 and P2 are done.
P3 is a substantial reduction of the coherent cost within this same direction;
P4 is the financial bridge; P5 is synthesis/physical/full-price accounting; P6
is frozen confirmation and a supported manuscript claim. Larger variance pilots
or held-out sweeps are not the next useful step after this failed gate.

For the paper, the defensible current contribution is a reproducible feasibility
and resource analysis with controls and explicit failure/error accounting.
Publication would require a clear contribution beyond standard components and
independent technical review. These results cannot support an advantage title.
The existing manuscript has been left unchanged.

## Reproduce and inspect

[Code and commands](../../research/controlled_source_completion/README.md),
[derivation](DERIVATION.md), [checklist](CHECKLIST.md),
[final ledger](../../results/controlled_source_completion/cost_v3_phase64/ledger.json),
[validation records](../../results/controlled_source_completion/validation_v2/tests.json),
[full-source gate runs](../../results/controlled_source_completion/validation_v2/full_source_basis.json).
Initial versions, new development amendments, gate files, raw paired values and
previous experiments remain available. These artifacts complete the requested
investigation and checks; they do not fulfill the quantum-advantage objective.
'''
    Path('docs/controlled_source_completion/RESULTS.md').write_text(body,encoding='utf-8')
    print('Wrote docs/controlled_source_completion/RESULTS.md',flush=True)


if __name__=='__main__':main()
