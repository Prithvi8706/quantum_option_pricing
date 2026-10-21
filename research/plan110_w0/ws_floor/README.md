# WS-floor (plan110 W0): idealized clean-call oracle floor

This workstream covers item A01, with A16, A09, A08, A02, A07, A13, F05 and F20 as parameters. A03 and A04 were also costed for the loader slot. Rigour is the R0 screen: spec, then script, then JSON with input SHA256s, then one self-check.

## Files

| File | What it is |
|---|---|
| `SPEC.md` | The model and its labels, written before the run |
| `floor_model.py` | The coarse stage model and the DAG reweight. Stdlib only. Run as `.context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_w0/ws_floor/floor_model.py --out results/plan110_w0/ws_floor` |
| `render_md.py` | Renders `floor.md` from `floor.json` |
| `results/plan110_w0/ws_floor/floor.json` | All numbers, with label and direction. The `primary_summary` block feeds the decision table. SHA256 469b2a19…e8229 |
| `results/plan110_w0/ws_floor/floor.md` | Readable tables. SHA256 325157e7…8c3f |
| `results/plan110_w0/ws_floor/rows.jsonl` | 233 rows, one per sub-result |

## Self-check

The DAG code passed its self-check. With the archived leaf T-depths, it reproduces the A01_run014 forward dependency T-depth exactly: 145,786 for B4x12 and 184,525 for B8x52. The normal, increment and exponential counts also match.

## Headline (W0 primary conventions)

Conventions: W = 1e7, 100 ns per reaction layer, 1e12 T/s, e = 0.45 eps. All numbers are modelled and quantum-favourable.

| | B4x12 | B8x52 |
|---|---|---|
| Call floor with the current Box-Muller law, idealized (reaction layers = T-layers at r_T=1) | 326 | 740 |
| Call floor with the best loader (alias sampling, q=10 grid; changes the law) | 234 | 472 |
| Loader share of the floor (Box-Muller / best) | 36% / 10% | 39% / 5% |
| T per call (Box-Muller) | 6.5e7 | 3.2e8 |
| Required T/s at 100 ns (Box-Muller) | 2.0e12 | 4.4e12 |
| Supply-limited call depth at 1e12 T/s (Box-Muller / best) | 364 / 236 | 2,296 / 1,293 |
| Current accepted source, measured capped call T-depth | 555,774 | 663,704 |

- **Unlimited width.** The floors are 258 / 274 with Box-Muller (174 / 190 with a free loader). Their T counts, about 3e10 and 3e11, need about 1e15-1e16 T/s.
- **W = 1e6.** B4x12 is 742. For B8x52 the crude width model gives 11,034, because full retention does not fit.
- **The DAG refinement** keeps the current algorithm and gives call floors of 1,322 (B4x12) and 1,398 (B8x52) at unlimited width. There the loader is 53-56% of the floor, which is at or above the F7 threshold of 50%.
- **Costed loader alternatives** (forward loader depth): A03 GR with synthesized rotations about 1.2e5; A04 MPS bond 8 about 5,760; GR-QROM direct preparation 91; alias q10 12; ICDF 24-110; idealized Box-Muller 42-146.

**k_10x.** This is the largest estimator constant that still reaches 10x, at W = 1e7 and 100 ns. For B8x52 at eps = 0.10, which is an overhead-dominated classical cell:

| B8x52, eps = 0.10 | Unlimited supply | 1e12 T/s |
|---|---|---|
| Box-Muller | 4.9 | 1.6 |
| Best loader | 7.6 | 2.8 |

The remaining cells:

- **B8x52 at eps = 0.001** (eligible at zero bias): 2.6 / 0.85 with Box-Muller and 4.1 / 1.5 with the best loader.
- **B4x12:** k_10x is at most 2.2 in every cell.
- **F20 sigma credit:** it multiplies these by about 4.5.

**Early stop.** It does not fire from the floor side. At the primary conventions, the threshold k_lat that would trigger it is 47 (Box-Muller with 1e12 supply), 146 (unlimited supply) or 83 / 228 (best loader). Taken over every convention, the threshold is at least 471, against a current k_eff of 586-1,067.

## Not claimed

These numbers are not lower bounds; they are idealized literature constructions. Several ingredients are unproved or need G2:

- the grid loaders;
- the A07 narrow widths;
- the 100 ns layer time;
- overlapped garbage cleanup.

`floor.md` §6 lists the caveats.
