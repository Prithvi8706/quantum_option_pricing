# N1 hardware/classical workstream (hwclassical)

The card is [`hw_classical_card.md`](hw_classical_card.md), with a machine-readable summary in `hw_classical_card.json`. Rigour is R1: the numbers are recomputed along a path independent of WS-floor/decision, and the self-check passes.

## Files

- `hw_classical_v2.py` produces the numbers of record in `results/plan110_n1/hwclassical/hw_classical_card_v2.json`. It is stdlib-only and runs under `.context/frontier_t0_env/Scripts/python.exe -I -S -B` from the repo root.
- `hw_classical.py` is v1, kept but superseded. It read the raw T_C instead of the T_C_env envelope, so its self-check failed in the ε = 0.03 overhead cells. Its output, `results/plan110_n1/hwclassical/hw_classical_card.json`, is superseded too.
- `results/plan110_n1/hwclassical/rows.jsonl` has one row per sub-result. It covers anchors A01-A12, the run records, the necessary conditions, where 100 ns sits, C09, H16, C10, and the H14/H04/H07 lines.

## History

The run was resumed after a logout on 12 October 2026. Anchors A01-A09 came from the earlier run and were reused unchanged; A10-A12 were added. 15 fetches were used in total, which is the cap.

## Headline

- **100 ns.** It is below every verified anchor. It is 5.5× faster than the only demonstrated complete loop (550 ns, d = 3) and 10× faster than the projected d = 25 cycles.
- **Binding cell (B8x52 at $0.001).** For a 10× win, the best explicit constant needs a 1.34 ns layer, 3.3e14 T/s and 1e7 logical qubits. That is 75× faster than 100 ns and 326× the W0 supply budget.
- **H16 (measured).** Going from 1 worker to 16 gives a 6.4-10.2× speedup.
- **C09.** Moving from the practice CI to a distribution-free 99% CI slows the classical side 10.6-40×, not 2-5×. The explicit-best M becomes 6.3 instead of 232, so the NO-GO holds but the margin falls below 30×. Adding the all-free oracle gives M = 0.31.
- **C10.** The label is "strongest tested classical method". Untested challengers could only strengthen the negative.
