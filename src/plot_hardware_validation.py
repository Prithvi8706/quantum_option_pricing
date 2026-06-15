"""
IBM Quantum hardware validation figure — Paper A, Section IV.

Deviation-from-theory lollipop: the theoretical target p = 0.30 is drawn as a
reference line, and each measured single-qubit estimate of P(|1>) hangs from it
by a stem whose length is the absolute error |p_hat - 0.30|. Two settings:
    - Real hardware  (ibm_marrakesh, read from results JSON)
    - Local simulator (AerSimulator dry run, seed 42)

A shaded band marks +/-1 sigma of shot noise around theory
(sigma = sqrt(p(1-p)/shots) = 0.0143 for p=0.30, shots=1024). Hardware's stem
is the shorter one, i.e. its deviation sits at the shot-noise floor; the
hardware-vs-simulator gap (~0.6 sigma) is itself within shot noise, so this
shows "no detectable device error", not that hardware out-performs simulation.

Style matches the rest of the Paper A figures (dark_background, dpi=150).
"""
import os
import json

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("dark_background")

HERE = os.path.dirname(__file__)
JSON_PATH = os.path.join(HERE, "..", "results", "ibm_hardware_validation.json")
OUT_PATH = os.path.join(HERE, "..", "results", "hardware_validation_plot.png")

# ── Data ────────────────────────────────────────────────────────────────────
with open(JSON_PATH) as f:
    hw = json.load(f)

P_THEORY = hw["theoretical_p"]                 # 0.30
P_HARDWARE = hw["p_hat"]                        # 0.2842 (ibm_marrakesh)
P_SIM = 0.2754                                  # AerSimulator dry run, seed 42
SHOTS = hw["shots"]
SIGMA = 0.0143                                  # sqrt(p(1-p)/shots), p=0.3, shots=1024

points = [
    # (x, value, color, label, sublabel)
    (0, P_HARDWARE, "#4fc3f7", "Hardware", hw["backend"]),
    (1, P_SIM, "#ffa726", "Simulator", "AerSim (seed 42)"),
]

# ── Figure ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))

# +/-1 sigma shot-noise band around theory + theory reference line
ax.axhspan(P_THEORY - SIGMA, P_THEORY + SIGMA, color="#cfd8dc", alpha=0.13,
           zorder=1, label=r"$\pm 1\sigma$ shot noise ($\sigma = 0.0143$)")
ax.axhline(P_THEORY, color="#66bb6a", linestyle="--", linewidth=1.6, zorder=2,
           label=r"Theoretical  $p = 0.30$")

# Lollipop stems (length = absolute error) + markers
for xi, v, color, *_ in points:
    ax.vlines(xi, v, P_THEORY, color=color, linewidth=3.0, alpha=0.9, zorder=3)
ax.scatter([p[0] for p in points], [p[1] for p in points],
           s=190, c=[p[2] for p in points], edgecolor="white", linewidth=1.2,
           zorder=4)

# Per-point annotation: actual p_hat, absolute error, sigma-multiple
for xi, v, color, *_ in points:
    err = abs(v - P_THEORY)
    ax.annotate(f"$\\hat{{p}}$ = {v:.4f}\n|err| {err:.4f}  ({err / SIGMA:.1f}$\\sigma$)",
                xy=(xi, v), xytext=(xi + 0.18, v), va="center", ha="left",
                fontsize=9.5, color="white", zorder=5)

ax.set_xlim(-0.6, 1.9)
ax.set_ylim(0.262, 0.307)
ax.set_xticks([p[0] for p in points])
ax.set_xticklabels([f"{lbl}\n{sub}" for _, _, _, lbl, sub in points], fontsize=10)
ax.set_ylabel(r"Estimated  $P(|1\rangle)$", fontsize=12)
ax.set_title(
    "IBM Quantum Hardware Validation — Deviation from Theory\n"
    f"Single-qubit $P(|1\\rangle)$ encoding of p = 0.30   ·   {SHOTS} shots",
    fontsize=11, pad=12,
)
ax.legend(fontsize=9, framealpha=0.3, loc="lower right")
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
fig.savefig(OUT_PATH, dpi=150, bbox_inches="tight")
print(f"Saved: {os.path.normpath(OUT_PATH)}")
for xi, v, color, lbl, sub in points:
    err = abs(v - P_THEORY)
    print(f"  {lbl:<10} p_hat={v:.4f}  |err|={err:.4f}  ({err / SIGMA:.2f} sigma)")
plt.close(fig)
