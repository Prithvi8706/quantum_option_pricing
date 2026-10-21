# WS-floor spec (R0 screen)

Item A01, with A16, A09, A08, A02, A07, A13, F05 and F20 as parameters. Written before the script runs.

## Question

What is the idealized reaction-layer depth of one complete coherent oracle call (forward plus uncompute) for the B4x12 and B8x52 knock-out payoffs? It is evaluated under a width budget W of 1e7 logical qubits (the W0 card primary), at unlimited width and at 1e6. The comparison is against the tenfold threshold depth D_max from `gap_ledger.json`.

## Model (all labelled per number in floor.json)

1. **Unit.** A reaction layer is one layer of parallel temporary-AND gates (A16; Gidney 2018, arXiv:1709.06648). Compute costs 4 T. Uncompute is measured and costs 0 T. Each leaf's garbage cleanup overlaps with downstream compute, which is assumed and quantum-favourable. A clean call is 2 x forward in reaction layers. The reverse pass recomputes leaf internals, so call T-count = 2 x 4 x forward ANDs. T-layers = reaction layers x r_T, with r_T = 1 (T-depth-1 AND; Jones 2013, PRA 87, 022328) as the floor, and 2 (Gidney AND) and 4 (repo-measured CCX ratio, `ccx_depth_screen.json`) as sensitivities. Cliffords, fan-out copies and the payoff-to-amplitude envelope cost zero.
2. **Primitive depths (literature constants, modelled).**
   - Adder and comparator (Kogge-Stone, A08): ceil(log2 w) + 1.
   - Dadda 3:2 reduction of h rows: the stage count of the Dadda sequence 2, 3, 4, 6, 9, ..., at one AND layer per stage (MAJ = a xor (a xor b)(a xor c)).
   - Multiplier (A09): 1 + Dadda(rows) + adder(product width).
   - Constant multiplier: Dadda(CSD weight) + adder, which is zero for powers of two.
   - QROM lookup with b address bits (fan-out minterms): ceil(log2 b) layers and 2^(b+1) ANDs.
   - Barrel shift: ceil(log2 c) + 1. Priority encoder: ceil(log2 w).
   - Transcendental function (A13): segment lookup + Estrin polynomial of degree d, with (d+1)*b >= precision bits. Each Estrin level is one fused multiply-add on (p - b) local bits.
   - Box-Muller and the alternative loaders: see `floor_model.py` docstrings.
3. **Coarse floor.** Stage chain: uniforms -> normals -> increments (carry-save) -> date prefix sums -> carry-propagate -> clip -> exp -> {basket barrier, average} -> payoff mask. Instances of a stage run in parallel up to W. Retained words and peak garbage are charged against W. If one round does not fit, the stage runs in ceil(peak / free) rounds. If retention alone exceeds W, stage-local compute-copy-uncompute is used, which doubles that stage's depth.
4. **Refinement (only if the trigger fires).** Reweight the accepted A10_coefficient source DAG (the A01_run014 effective source) with the same primitive depths, and take the longest path. Self-check: the same code, run with the archived leaf T-depths, must reproduce the A01_run014 `independent_forward_dependency_t_depth` (145,786 and 184,525) exactly. Variants: as-is DAG; loader replaced by the best coarse loader; free loader (F05); free exponential (A13); unproved narrow width (A07). Width is handled by a capped list schedule.
5. **Loader share.** Report it two ways: critical-path contribution and marginal share (1 - F_free_loader / F). If it is >= 50%, cost A04 (MPS bond 8), A03 (Grover-Rudolph with synthesized rotations) and direct state preparation (QROM/phase-gradient Grover-Rudolph; coherent alias sampling) at the floor.
6. **Supply and width.** Report call T-count, peak width, and required accepted T/s = T_call / (depth x t_layer). Report the supply-limited depth max(depth, T_call / (R x t_layer)) at R = 1e12 T/s, with 1e11 and 1e13 as sensitivities.
7. **Comparison.** k_10x = D_max(k=1) / floor, which is the largest estimator constant k that still reaches 10x. Report it per cell and convention: t_layer, e = 0.45 eps vs eps, and the F20 zero-depth sigma credit. The early-stop k is k_es = 30 x D_max(k=1) / floor.

## Self-check

Rebuild the archived critical-path T-depths from the DAG (point 4). Also check that the normal, increment and exponential counts match nt(na+1), na*nt and na*nt.

## Not claimed

These are not lower bounds. With truly unlimited width, any function of N input bits has AND-depth ceil(log2 N) + 1, through an exponential-width lookup, so "unlimited width" here means the literature constructions above with table address bits b <= 20.
