# Exact shift-count scope after the square screen

Every variable-shift count in the accepted A11 sources fits a signed seven-bit integer, while the data and native interfaces remain 72 bits. This is a proved input-domain component for the next experiment; no narrower shift circuit or resource saving has been credited.

| Case | Actual shift sites | Normalization counts | Exponential counts | Signed7 guard proved |
|---|---:|---:|---:|---:|
| B4×12 | 78 | 30 | 48 | 78 |
| B8×52 | 650 | 234 | 416 | 650 |

The same-SSA integer interval analysis bounds the normalization counts in `[1,33]` and exponential counts in `[-16,11]`. These bounds come from the actual validated target and its declared input law, using all literal table rows. They do not come from sampled execution maxima. The native shift's second argument is an unscaled signed integer; its meaning must remain unchanged.

A signed seven-bit count lies in `[-64,63]`. Its maximum magnitude is 64, strictly less than the data width 72. An exact specialized leaf can therefore use a seven-bit magnitude and omit the oversized-shift branch on the proved domain. It must preserve 72-bit modular left shifting, arithmetic right shifting with sign extension, arbitrary full-width output XOR, both native input registers, and complete workspace restoration. In particular, `-64` has magnitude 64 as an unsigned seven-bit value; interpreting that magnitude as signed would be incorrect.

The next experiment is one exact seven-bit-control barrel-shift leaf. Dispatch requires an interval proof at the actual shift-count SSA value. Generic or unproved shift sites retain their archived leaf, including oversized positive/negative shift behavior. The experiment will retain the existing data width, SSA masks and argument-copy contract, validate all small signed data/count patterns plus production endpoints, and compare both complete capped sources before any adoption or full financial replays.

The scope producer froze its code, target/source/schedule hashes and proof dependencies before analysis. Small exhaustive interval checks verify the minimum signed-width classification. The canonical [scope receipt](../../results/limitation_program_20261001/A07_shift_scope_run002/summary.json) and [site records](../../results/limitation_program_20261001/A07_shift_scope_run002/) preserve every actual guard. The earlier scope receipt remains historical; the versioned producer resolves its formatting issues without changing its mathematical result.

The current measured shift-depth attribution is 87,360 / 122,304 layers in B4/B8. This identifies an experiment, rather than predicting its attainable saving. G2 continuous-dollar error, G3 estimation, G4 matched classical performance and G5 physical advantage remain open.
