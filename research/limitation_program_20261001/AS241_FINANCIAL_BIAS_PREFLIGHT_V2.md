# Native AS241 financial bias v2 admission correction

Author-stage correction only. The original preparation failed with `ValueError:
Actual clamp literals` before creating `A02_quantile_financial_run001`; no
producer protocol, tests or numerical financial proof exists for that attempt.
The root-report diagnostic is preserved separately as
`A02_quantile_financial_admission_failure_run001`. Its three files and all seven
source bindings must remain immutable and are bound by the v2 producer before
any admission work. All original helper, certificate, producer, test and
`AS241_FINANCIAL_BIAS_PREFLIGHT.md` bytes remain unchanged.

The actual saved frontend targets and bundles serialize the lower stock clamp
as the canonical unsigned native72 word `4722366470675671057123`. It represents
the signed value `-12193974156573`; the upper word represents `9145480617430`.
The original helper decoded the actual constant before comparing it with the
bundle's undecoded modular word and would also have returned the undecoded
lower word to the numerical certificate. V2 checks canonical modular72 typing,
decodes both semantic clamp words for exact comparison with actual signed
constants, and returns those signed words in the financial scope. A changed
literal still fails equality. No target, clamp, coefficient, precision, proof
method, partition, budget, financial law or arithmetic operation changes.

The fresh attempt is exactly `A02_quantile_financial_run002`, implemented by
`as241_financial_native_v2.py`, `as241_financial_certificate_v2.py`,
`experiment_as241_financial_v2.py` and
`test_as241_financial_certificate_v2.py`. The certificate's mathematical code
changes only its helper import. The v2 test file retains all 21 original cases
and adds one actual B4 saved-frontend regression which checks the modular72
negative lower clamp, returned signed bounds, unchanged bundle word, and
rejection when that semantic lower literal is increased by one. The planned
count is 22, a documented delta of one; fixed18 planned fixtures become 249.
No tests or proof evaluation have been run by this author-stage correction.

The original prospective method remains the immutable specification:
`AS241_FINANCIAL_BIAS_PREFLIGHT.md`. The two contracts, q32 independent drivers,
native72/f40 arithmetic, original stock-only clamps, strict survival, all 464
stock sites and 30 exponent classes remain fixed. The producer retains its
90-digit intervals, 180-second process-CPU and 600-second wall budget. The
independent auditor remains a separate unexecuted implementation with its
110-digit, 240-second CPU and 900-second wall budget; it now binds run002,
reconciles 22 producer fixtures without recredit, independently checks the
bundle's canonical modular clamp words against the actual signed constants,
and checks the saved producer scope returns the same signed endpoints.

Preparation must freeze the fresh code and this preflight, bind every prior
diagnostic map with canonical no-override hashes, preserve the original source
expectations, verify all dependencies before/after, and retain terminal partial
failure/censor records. The original run001 directory must remain absent.
No retry of the original preparation, forged protocol, revised completed
manifest or restored financial credit is permitted. Both actual case bounds
and their independent audit must be retained even if the unchanged residual
financial allowance fails. Financial adoption, sampler/resource compilation,
full G2 and quantum advantage remain separate unresolved obligations.
