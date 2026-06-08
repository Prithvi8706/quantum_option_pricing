import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use("dark_background")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ── Left panel: break-even shift for constant-VRF methods ──────────────────
eps = np.logspace(-3, -1, 400)           # 0.001 → 0.1

methods_vrf = [
    ("Naive MC",       1.0,  "#4fc3f7"),
    ("Antithetic MC",  2.0,  "#81c784"),
    ("Control Variate", 6.8, "#ffb74d"),
]

for name, vrf, color in methods_vrf:
    N = (1.96 / eps) ** 2 / vrf          # classical samples for target ε
    M = np.pi * np.sqrt(N) / 1.96        # QAE oracle queries to match
    ax1.loglog(eps, M, color=color, linewidth=2.2,
               label=f"{name}  (VRF = {vrf})")

ax1.set_xlabel("Target precision  ε", fontsize=12)
ax1.set_ylabel("QAE oracle queries needed to win", fontsize=12)
ax1.set_title("Break-Even Shift: Constant-VRF Variance Reduction",
              fontsize=12, pad=10)
ax1.legend(fontsize=9.5, framealpha=0.3)
ax1.grid(True, which="both", alpha=0.2)
ax1.set_xlim(0.001, 0.1)

# Annotation: √VRF shrinks M by a factor of √VRF  (√6.8 ≈ 2.6)
ax1.annotate(
    "Each $\\sqrt{\\mathrm{VRF}}$ lowers the break-even M.\n"
    "Control Variate (VRF = 6.8) shifts the bar\n"
    "by $\\sqrt{6.8}$ ≈ 2.6×: QAE must work\n"
    "2.6× harder to claim the same relative edge.",
    xy=(0.038, 160), xytext=(0.004, 40),
    xycoords="data", textcoords="data",
    fontsize=8.5, color="white", alpha=0.85,
    arrowprops=dict(arrowstyle="->", color="white", alpha=0.5),
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#2a2a2a", alpha=0.75),
)

# ── Right panel: scaling parity with RQMC ──────────────────────────────────
N_arr = np.logspace(2, 6, 600)

M_naive = 1.604 * np.sqrt(N_arr)         # QAE queries to beat naive MC (M∝√N)
M_rqmc  = N_arr                          # C = π  →  M = πN/π = N  (parity)

# Shade "QAE cheaper" (M < N) and "QAE more expensive" (M > N)
ax2.fill_between(N_arr, M_naive, N_arr,
                 alpha=0.18, color="#4caf50", label="_nolegend_")
ax2.fill_between(N_arr, N_arr, N_arr.max() * 10,
                 alpha=0.10, color="#f44336", label="_nolegend_")

ax2.loglog(N_arr, M_naive, color="#4fc3f7", linewidth=2.2,
           label=r"vs Naive MC:  $M \propto \sqrt{N}$  (QAE wins)")
ax2.loglog(N_arr, M_rqmc,  color="#ce93d8", linewidth=2.2, linestyle="--",
           label=r"vs RQMC:  $M \propto N$  (scaling parity)")
ax2.loglog(N_arr, N_arr,   color="white",   linewidth=0.9, alpha=0.35,
           label=r"$M = N$  (break-even)")

ax2.set_xlim(1e2, 1e6)
ax2.set_ylim(10, 2e7)
ax2.set_xlabel("N  (total samples)", fontsize=12)
ax2.set_ylabel("QAE oracle queries  M", fontsize=12)
ax2.set_title("Scaling Parity: RQMC Erases QAE's Asymptotic Advantage",
              fontsize=12, pad=10)
ax2.legend(fontsize=9.5, framealpha=0.3)
ax2.grid(True, which="both", alpha=0.2)

# Region labels
ax2.text(1.4e2, 6e5, "QAE more\nexpensive",
         color="#ff8a80", fontsize=9.5, alpha=0.9, va="center")
ax2.text(1.4e2, 1.6e3, "QAE\ncheaper",
         color="#a5d6a7", fontsize=9.5, alpha=0.9, va="center")

# Key annotation
ax2.annotate(
    "Against RQMC, QAE needs $M \\propto N$\n"
    "— no asymptotic advantage remains.",
    xy=(4e4, 4e4), xytext=(3e3, 3e5),
    fontsize=8.5, color="white", alpha=0.9,
    arrowprops=dict(arrowstyle="->", color="white", alpha=0.5),
    bbox=dict(boxstyle="round,pad=0.45", facecolor="#2a2a2a", alpha=0.75),
)

plt.tight_layout()

out_path = os.path.join(os.path.dirname(__file__), "..", "figures",
                        "fig_break_even_shift.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved: {os.path.normpath(out_path)}")
plt.close(fig)
