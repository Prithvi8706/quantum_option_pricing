# Independent non-restoring square-root audit

R'=4R+d-(4Q+1) if old R>=0; R'=4R+d+(4Q+3) otherwise; Q'=2Q+int(R'>=0).

In either old-sign branch the trial equals M-(2Q+1)², with M=4N+d. If trial>=0 choose new Q=2Q+1 and R=M-Q'²; otherwise choose Q'=2Q and R=M-(Q'+1)². Since Q²<=N<(Q+1)², M lies between (2Q)² and (2Q+2)², so this choice is exactly isqrt(M).

-(2Q+1)<=R<=2Q, Q<2**stage. At final k stages, R lies strictly within [-2**(k+1),2**(k+1)), representable in signed k+2 bits.

4R+d may overflow signed k+2. All updates are modulo2**(k+2); the proved final exact remainder fits that signed word, so the final sign is correct. No promise that every pre-add intermediate fits.

Low bits11; each higher bit is Q_bit XOR NOT(old_R_sign). This equals -(4Q+1) or +(4Q+3) modulo2**(k+2), respectively.

Read radicand pair at original source indices 2*position+bit-fraction_bits; absent indices are zero. Leading padding and all lower fractional zeros are retained.

All k+1 remainder snapshots, private k root bits, operand and helper are charged. Operand construction is reversed per stage; complete compute is reversed after copying root bits to arbitrary output.

The actual signed-remainder gate array was parsed completely, including every Cuccaro MAJ/UMA, operand inverse, new-sign root bit, output XOR and exact reverse. Finite arithmetic bookkeeping checked 68,127 radicands; that enumeration is separate from the algebraic all-domain proof.

| Resource | Accepted restoring leaf | Non-restoring leaf |
|---|---:|---:|
| t_count | 219,128 | 54,180 |
| t_depth | 105,582 | 30,960 |
| clifford_t_depth | 312,836 | 93,052 |
| qubits | 2,350 | 2,213 |

The predeclared leaf screen allowed full-source testing.

| Case | T gates | T-depth | T-depth gain | CT-depth | Qubits / cap | Eligible |
|---|---:|---:|---:|---:|---:|---|
| B4x12 | 619,528,126 | 787,566 | 15.9311% | 2,342,011 | 550,141 / 550,141 | True |
| B8x52 | 5,095,520,430 | 820,268 | 15.3937% | 2,472,617 | 4,460,481 / 4,460,481 | True |

All30 B4 and234 B8 sqrt sites have unsigned46 intervals in their actual validated SSA graph. Every other leaf metadata and gate array matches the accepted baseline bytes, including signed7 shift and all32 lookup rows. Native copies, masks and retained SSA storage are unchanged. Counts, complete DAG, first-fit groups and actual caps were independently reconciled.

Adopted after both-case eligibility and four saved complete financial gate replays.

Use the accepted complete-source owner ranking for the next bounded local experiment. Keep G2-G5 open and all work local.

G2 continuous-dollar certification, G3 compatible99% estimator schedule, G4 matched classical timing and G5 physical10x runtime accounting remain unresolved. This audit establishes no quantum advantage. Everything stayed local.

Receipts: [summary](../../results/limitation_program_20261001/A01_run011/summary.json), [complete audit](../../results/limitation_program_20261001/A01_run011/), [auditor](../../research/limitation_program_20261001/reconcile_nonrestoring_v2.py).
