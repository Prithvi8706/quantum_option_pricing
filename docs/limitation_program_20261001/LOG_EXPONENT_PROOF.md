# The logarithm exponent admits an exact signed seven-bit operand

Local proof and checks, 1 October 2026. **All 30 B4x12 and 234 B8x52 logarithm-derived ln(2) calls admit a seven-bit signed operand contract.** The other 48 and 416 ln(2) calls are exponential range reduction and remain under their existing signed 32-bit contract. This supplies a smaller exact specialization interface; no new multiplier has been integrated and no resource gain is claimed.

The [prospective protocol](../../results/limitation_program_20261001/A07_run001/protocol.json), [result](../../results/limitation_program_20261001/A07_run001/result.json), [checks](../../results/limitation_program_20261001/A07_run001/checks.json), [verification](../../results/limitation_program_20261001/A07_run001/verification.json) and [manifest](../../results/limitation_program_20261001/A07_run001/manifest.json) identify the exact current graph/source hashes. Existing coefficient, precision, law, payoff and archived circuits are unchanged.

## The exact graph pattern

The structural checker matches this complete producer chain in one validated SSA graph:

~~~text
raw  = any 72-bit producer output
x    = select(lt(raw, const_int(1)), const_int(1), raw)
j    = msb(x)
q    = sub(j, const_int(40))
A    = bits(q, shift=-40, width=72, signed=False)
Y    = cmul(A, c=762123384786)
~~~

The unit constant is the integer word 1, representing the smallest positive fixed-point quantum; it is not the fixed-point word for the real number 1. The comparison is signed. The same unit SSA value must appear in the comparison and the selected branch. The final coefficient remains the original positive integer.

The checker verifies unique ordered SSA outputs, earlier same-graph producers, exact argument identities and literal parameters. It rejects a coefficient-only match, a wrong shift/width/sign flag, a different subtraction constant, a non-msb producer, an incorrect positive guard, duplicate outputs and foreign/dangling references. Its dispatch interface accepts a graph and node index, not an arbitrary caller-supplied producer map. Repeated lookups use a validated graph snapshot.

Each matched node is also bound to its actual current source forward-call index and leaf key. Full chains are preserved in [B4 provenance](../../results/limitation_program_20261001/A07_run001/B4x12_provenance.json) and [B8 provenance](../../results/limitation_program_20261001/A07_run001/B8x52_provenance.json).

## Why the signed range holds for every allowed input

For any unsigned 72-bit word, the local definition is

~~~text
msb(x) = max(0, bit_length(x) - 1).
~~~

It is therefore in [0,71], including x=0. Subtraction of the unscaled integer 40 gives q in **[-40,31]**. No signed 72-bit overflow is possible. This alone fits the signed seven-bit interval [-64,63].

The actual log guard proves something stronger. Every zero or negative signed raw word selects 1. Every other selected raw word lies in [1,2^71-1]. Thus x is always positive and msb(x) is in [0,70], giving the sharper reachable range **[-40,30]**. This argument covers every 72-bit pattern and hence every allowed finite financial input; it does not depend on sampled paths. The conservative [-40,31] contract remains convenient for specialization.

Although the bit-extraction node treats q's word as unsigned, its left shift is reduced modulo 2^72. For negative q, the unsigned representation is 2^72+q, so the shifted word is still q·2^40 modulo 2^72. Since q lies in [-40,31], signed interpretation gives exactly

~~~text
signed72(A) = q · 2^40
floor(signed72(A) · 762123384786 / 2^40)
    = q · 762123384786.
~~~

Negative-number truncation is therefore unchanged. The conservative product range is [-30,484,935,391,440, 23,625,824,928,366], which fits signed 46 bits. The output contract nevertheless retains the original full 72-bit XOR output. The 46-bit bound concerns this proved q range, not all possible signed seven-bit values.

## The storage promise is sign extension

For the actual multiplier argument A:

- Bits 0–39 are zero.
- Bits 40–46 encode q as a signed seven-bit integer.
- Bits 47–71 equal bit 46.

The higher bits are redundant sign bits, not generally zero. Existing compact storage based on possible-one masks cannot erase them using a zero-only proof. For example q=-40 has seven-bit raw representation 88: naively forming 88·2^40 gives positive 88 rather than -40. The negative control detects this error.

A future leaf may read only bits 40–46 under this static sign-extension promise while preserving the full input and output interfaces. A future signed-storage compiler needs its own legal binding and cleanup design. Neither change is made by this proof.

## Exponential calls remain a separate proof question

The remaining chains use

~~~text
k = bits(cmul(x, c=1586259972792), shift=40, width=72, signed=True)
A = bits(k, shift=-40, width=72, signed=False).
~~~

A signed 72-bit arithmetic right shift by 40 has the primitive range [-2^31,2^31-1]. It does not by itself justify seven bits. A generic shifted word yielding k=100 is a checked counterexample to that proposed structural inference. It is not claimed reachable in the archived guarded financial graph. A separate reachable-domain certificate may later tighten these exponential operands.

| Case | Log calls: signed7 proved | Exp calls: signed32 retained | Unclassified ln(2) calls |
|---|---:|---:|---:|
| B4x12 | 30 | 48 | 0 |
| B8x52 | 234 | 416 | 0 |

## Checks and next implementation

The run saved its protocol before classifications or checks. It then passed all 72 possible raw msb indices; 496 exhaustive guarded-chain inputs at widths 4–8; 145 production-width raw-pattern checks including zero and negative words; 442 literal production msb/sub/left-shift gate replays with nonzero outputs, inverse execution, input preservation and scratch restoration; and 13 structural negative controls. These support the implementation of the algebraic proof. They do not constitute a full-source replay or a continuous-price certificate.

[prove_log_exponent.py](../../research/limitation_program_20261001/prove_log_exponent.py) ran in the existing pinned Python 3.12 environment. The proof/check phase took approximately 2.43 seconds. Ruff and whitespace checks passed.

The [next interface](../../results/limitation_program_20261001/A07_run001/NEXT.md) is an exact signed7 coefficient leaf with the recorded same-graph dispatch and fallback. Test every signed7 word, negative and extreme products, nonzero output and clean inverse; then measure complete capped sources after the compact-storage integration. Keep the existing signed32 leaf if the combined source fails to improve. No arithmetic precision or financial-law relaxation is needed for this route.

