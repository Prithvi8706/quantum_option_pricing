"""
IBM Quantum hardware validation figure — Paper A, Section IV.

Bar chart comparing the single-qubit state-prep estimate of the benchmark
probability p = 0.30 across three settings:
    - Theoretical target          (0.3000)
    - Real hardware  (ibm_marrakesh, read from results JSON)
    - Local simulator (AerSimulator dry run, seed 42)

A horizontal band marks +/-1 sigma of shot noise around the theoretical value
(sigma = sqrt(p(1-p)/shots) = 0.0143 for p=0.30, shots=1024). Bars keep a zero
baseline so heights are truthful; per-bar sigma-distance annotations carry the
precision message.

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

P_THEORY = hw["theoretical_p"]          # 0.30
P_HARDWARE = hw["p_hat"]                # 0.2842 (ibm_marrakesh, 1024 shots)
P_SIM = 0.2754                          # AerSimulator dry run, seed 42
SHOTS = hw["shots"]
SIGMA = 0.0143                          # sqrt(p(1-p)/shots), p=0.3, shots=1024

labels = ["Theoretical", "Hardware", "Simulator"]
sublabels = ["p = 0.30", hw["backend"], "AerSim (seed 42)"]
values = [P_THEORY, P_HARDWARE, P_SIM]
colors = ["#66bb6a", "#4fc3f7", "#ffa726"]   # green / blue / orange (Paper A palette)

# ── Figure ──────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 6))

x = np.arange(len(values))
bars = ax.bar(x, values, width=0.6, color=colors, edgecolor="white",
              linewidth=0.8, zorder=3)

# +/-1 sigma shot-noise band around theoretical
ax.axhspan(P_THEORY - SIGMA, P_THEORY + SIGMA, color="#cfd8dc", alpha=0.15,
           zorder=1, label=r"$\pm 1\sigma$ shot noise ($\sigma=0.0143$)")
ax.axhline(P_THEORY, color="#66bb6a", linestyle="--", linewidth=1.2, alpha=0.8,
           zorder=2, label="Theoretical  p = 0.30")

# Per-bar annotations: value, and sigma-distance for the two estimates
for xi, v, lab in zip(x, values, labels):
    if lab == "Theoretical":
        note = f"{v:.4f}"
    else:
        sig_dist = (v - P_THEORY) / SIGMA
        note = f"{v:.4f}\n({sig_dist:+.1f}$\\sigma$)"
    ax.text(xi, v + 0.006, note, ha="center", va="bottom",
            fontsize=10, color="white", zorder=4)

ax.set_xticks(x)
ax.set_xticklabels([f"{l}\n{s}" for l, s in zip(labels, sublabels)], fontsize=10)
ax.set_ylabel(r"Estimated  $P(|1\rangle)$", fontsize=12)
ax.set_ylim(0, 0.34)
ax.set_title(
    "IBM Quantum Hardware Validation — Single-Qubit State Preparation\n"
    f"$P(|1\\rangle)$ encoding of benchmark p = 0.30   ·   {SHOTS} shots",
    fontsize=11, pad=12,
)
ax.legend(fontsize=9, framealpha=0.3, loc="lower center")
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
fig.savefig(OUT_PATH, dpi=150, bbox_inches="tight")
print(f"Saved: {os.path.normpath(OUT_PATH)}")
print(f"  theoretical = {P_THEORY:.4f}")
print(f"  hardware    = {P_HARDWARE:.4f}  ({(P_HARDWARE-P_THEORY)/SIGMA:+.2f} sigma)")
print(f"  simulator   = {P_SIM:.4f}  ({(P_SIM-P_THEORY)/SIGMA:+.2f} sigma)")
plt.close(fig)
