# Fixed polar-safe h1/128 payoff squared-L2 bridge (scope #43)

This current metadata-authored SOURCE binds saved #42 fields only: the sealed #42 profile records, summary,
reconciliation, manifest, executed adapter and controller, and the ROOT saved
verification. lambda=2^-18, h=1/128, M=4608, sqrt128 and the coupling are
inherited unchanged; nothing is retuned and the two profiles stay separate.

Per own profile the SOURCE first reads /all12_fixed_basket_criterion_passed and
/all12_simultaneous_on_same_fixed_safe_event. Only when both are true does it
decode E_s, p and the saved mean. With U, eta, tau, avg, polar_bad and B_band
from the own saved components it forms C_J=40*(U+eta)+tau and, in exact
Fractions, L2SQ=E_s^2*(1-p)+C_J^2*p (identical to E_s^2+(C_J^2-E_s^2)*p),
BASE=E_s^2+1600*p, L1=E_s*(1-p)+C_J*p and RMS=outward_fixed_sqrt128(L2SQ).
Checks: R1 E_s==U*avg+40*eta+tau; R2 polar_bad==60*lambda,
B_band==(1/1176)*(1+1/963379197), p==min(1,polar_bad+B_band); R3
mean==E_s+40*p; R4 E_s<=C_J<=40; R5 L2SQ<=BASE; R6 L2SQ<=C_J^2; R7 L1<=mean.
R5-R7 stay None unless R1-R4 all hold. The (1-p,p) vertex is the exact maximum
of the LP relaxation, not the sharpest bound for the actual coupling.

The pointwise bound |Y_N-Y|<=E_s is used only on G=E&SS_N&SS (1_G restriction
mandatory); on B=E^c u M both payoffs are nonnegative and below C_J. P(B) uses
the union bound 60*lambda and the unconditional ideal band P(E&band)<=P(band);
no native, error, safe-event or band independence is assumed.

target.json (a7a68273, pinned by the #42 adapter, #42 manifest and the native
runtime manifest) is read directly for node 13 (const 0), 5643 (140Q), 5644
(strict lt), the twelve quarter baskets and their binary max tree, the 48-stock
sum tree and nodes 5692-5697; ir.py fixes select/lt/cmul semantics. Each own
discount archive (primary smooth_payoff_bounds via the #42 adapter;
independent130 557ad358 with A02 audit code 063f8bf7) must give the saved U and
eta exactly, with eta equal to the endpoint maximum of |D_lit-L|,|D_lit-U|, so
eta>=|D_lit-d| for d=exp(-3/100) in [L,U].

An inherited False or any failed check seals all 13 files with outcome
negative_fixed_bridge_feasibility and L2SQ/BASE/L1/RMS None; no fallback, no
retuning and no cross-profile minimum. P11 (a certified continuous B4x12 second
moment) is missing, so no moment or variance transfer and no estimator saving
is claimed; this is an upper certificate on the coupling bridge only.

Default4300, 180 CPU/150 admission/600 wall seconds, 150 MiB RSS, 131072
reduced/524288 temporary bits, 4096 limbs, 256-bit emitted JSON integers and the
exact 13-file/128 MiB ledger remain unchanged. Five artificial metadata controls
(JUMP_CONSTANT, PROBABILITY, LP_FORM fixed to the single Young split value,
FAILED_CRITERION, INDEPENDENCE) are checked after the positive interface. No
SOURCE or scientific function was called during metadata authoring. A fresh
current SOURCE static peer, ROOT static review and closed 14-key READY are
required before ROOT alone runs SCI. All current result and SCI pins are None.

The actual authoring gate is True after ROOT full plaintext review of the three
changed definitions, header and preflight (scope #43, user-authorized after the
#42 stop). This is not SCI authority. The preserved prepare-helper run001
ordering assertion is author metadata ancestry; no production SOURCE was run.
