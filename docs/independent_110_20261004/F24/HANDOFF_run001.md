F24's exact D1 date-update formulation and two prescribed grid diagnostics
passed. Full continuum-price and quantum-transfer acceptance remain open.

- Mathematical packet: `docs/independent_110_20261004/F24/FORMULATION_run001.txt`.
- Author: `research/independent_110_20261004/F24/pde_screen_v1.py`, SHA256
  `cbb10a1d432ab29f46b7b3600ad91b53f59d55f37dfd11270b785d39fbdb0f5e`.
- Frozen protocol: `results/independent_110_20261004/F24/run001/protocol.json`,
  SHA256 `c725fe448e186f012197c4f8d1181f226509fdf975d057651ef460b048d2da22`.
  Six files/1,107,771 bytes;10CPU/30wall/4MiB input/2MiB output/16file caps.
- Result: `results/independent_110_20261004/F24/run001/summary.json`, SHA256
  `d988bc9c3e0ecb62bf475810aeaabff0cbdf7887303f071575ca47c4b170a8b2`.
  `grid_17.npz`, `grid_33.npz`, `SUCCESS.json` and `manifest.json` retained.

Existing plain development D1 is unchanged: one asset, two fixings at0.5
and1, sigma0.2, strike95. Its cumulative half-sum state is constant between
dates and shifts at each fixing. The q>=K branch has exact linear
continuation. A discrete basket barrier jump is specified formally for the
original contract; D1 acquired no barrier and no barrier workload ran.

Checks: static source AST/compile, original D1 declaration/default binding,
metadata prepare, then one two-grid NumPy diagnostic invocation. Both
central stencils have nonnegative rates and the implicit matrices satisfy
the exact rational diagonal-dominance/infinity-condition bounds. Seventeen
and33-point axes produced $9.71728325545 and $10.07089801076 respectively.
The $0.35361475530 difference is a diagnostic, not a price error bound.
Finite-X boundaries, time/event discretization and floating enclosures
are still uncertified; no classical reference with certified bias exists.

The [Miyamoto/Kubo primary](https://arxiv.org/html/2109.12896v1), Assumption2.1
and Theorems3.1/5.1, requires derivative, matrix-access, state/norm and
extraction premises. Those premises were not proved across D1 date/payoff
kinks or for the augmented event interface. Matrix/state loading, event
cost, point-price extraction, physical costs and strongest eligible
classical comparison remain null. No quantum compilation, B4/B8 numerical
validation, matched timing, delivered-price or advantage claim follows.
