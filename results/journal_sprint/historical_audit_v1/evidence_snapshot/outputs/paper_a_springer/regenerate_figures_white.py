"""
Regenerate Paper A's four figures on a WHITE background for the Springer
submission. Faithful ports of the repo's dark-themed plotters
(src/plot_noise_results.py, src/plot_break_even.py, src/plot_hardware_validation.py)
with only the styling changed to white — data sources and values are identical.

Outputs into ./figures/ next to this script. The repo's original dark figures
and scripts are left untouched.

Run:  venv\\Scripts\\python.exe outputs\\paper_a_springer\\regenerate_figures_white.py
"""
import os
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# default (white) matplotlib style — no dark_background

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "data")
RESULTS = os.path.join(REPO, "results")
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

_NOISE_LEVELS = [0, 1e-4, 1e-3, 5e-3, 1e-2]
_XLABELS = ["0", "1e-4", "1e-3", "5e-3", "1e-2"]


# ── Fig 1: heatmap (10 configs) ──────────────────────────────────────────────
def fig_heatmap():
    df = pd.read_csv(os.path.join(DATA, "noise_sweep_results.csv"))
    pivot = df.pivot_table(index="pt_idx", columns="p", values="delta",
                           aggfunc="mean").reindex(columns=_NOISE_LEVELS)
    matrix = pivot.values

    base = df[df["p"] == 0].sort_values("pt_idx")
    ylabs = []
    for _, row in base.iterrows():
        s = f"{row['sigma']:.2f}".rstrip("0").rstrip(".")
        ylabs.append(f"P{int(row['pt_idx'])}  S0={row['S0']:.0f}  K={row['K']:.0f}"
                     f"  T={row['T']:.2g}  σ={s}")

    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto", vmin=0, vmax=8)
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(r"Price Error |Δ| (\$) — capped at \$8 for visibility")

    ax.text(0.02, 0.99, "QAE ε=0.01 threshold: all points exceed it",
            transform=ax.transAxes, color="black", fontsize=8, va="bottom")

    ax.set_xticks(range(len(_NOISE_LEVELS)))
    ax.set_xticklabels(_XLABELS, fontsize=9)
    ax.set_xlabel("Depolarizing noise rate p", fontsize=10)
    ax.set_yticks(range(len(ylabs)))
    ax.set_yticklabels(ylabs, fontsize=8)
    ax.set_title("NISQ Noise vs Price Error — 10 Option Configurations",
                 fontsize=11, pad=12)

    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            val = matrix[r, c]
            # dark cells (high value) -> white text; light cells -> black text
            tc = "white" if val > 4.8 else "black"
            ax.text(c, r, f"{val:.3f}", ha="center", va="center",
                    fontsize=7, color=tc)

    plt.tight_layout()
    out = os.path.join(OUT, "fig_noise_heatmap.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved", out)


# ── Fig 2: mean |delta| vs noise (10 configs — matches repo original) ─────────
def fig_mean_delta():
    df = pd.read_csv(os.path.join(DATA, "noise_sweep_results.csv"))
    stats = (df.groupby("p")["delta"].agg(["mean", "min", "max"])
             .reindex(_NOISE_LEVELS).reset_index())
    x_plot = stats["p"].replace(0, 1e-5).values

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.fill_between(x_plot, stats["min"], stats["max"], alpha=0.25,
                    color="#1f77b4", label="Min–max band")
    ax.plot(x_plot, stats["mean"], color="#1f77b4", marker="o", linewidth=2,
            markersize=6, label="Mean |Δ|")
    ax.axhline(0.01, color="#d62728", linestyle="--", linewidth=1.2,
               label="QAE ε=0.01 precision target")
    ax.axvline(1e-3, color="#7f7f7f", linestyle="--", linewidth=1.2,
               label="Current IBM hardware")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([1e-5, 1e-4, 1e-3, 5e-3, 1e-2])
    ax.set_xticklabels(["0\n(ideal)", "1e-4", "1e-3", "5e-3", "1e-2"], fontsize=9)
    ax.set_xlim(5e-6, 2e-2)
    ax.set_xlabel("Noise rate p", fontsize=11)
    ax.set_ylabel("Mean |Δ| ($)", fontsize=11)
    ax.set_title("Mean Price Error vs Depolarizing Noise Rate", fontsize=12, pad=10)
    ax.legend(fontsize=9, framealpha=0.9)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)
    out = os.path.join(OUT, "fig_mean_delta_vs_noise.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved", out)


# ── Fig 3: break-even frontier + oracle depth (50 configs) ───────────────────
def fig_frontier():
    df = pd.read_csv(os.path.join(DATA, "noise_sweep_expanded.csv"))
    stats = (df.groupby("p")["delta"].agg(["mean", "std"])
             .reindex(_NOISE_LEVELS).reset_index())
    oq = (df.groupby("p")["oracle_queries"].agg(["mean", "std"])
          .reindex(_NOISE_LEVELS).reset_index())
    x = [1e-5, 1e-4, 1e-3, 5e-3, 1e-2]
    xl = ["0\n(ideal)", "1e-4", "1e-3", "5e-3", "1e-2"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    md = stats["mean"].values
    ax1.plot(x, md, color="#1f77b4", marker="o", linewidth=2, markersize=6, zorder=3)
    y_top = max(md.max() * 2, 0.05)
    ax1.fill_between([5e-6, 2e-2], 0.01, y_top, color="#d62728", alpha=0.10,
                    label="QAE advantage lost")
    ax1.fill_between([5e-6, 2e-2], 0, 0.01, color="#2ca02c", alpha=0.12,
                    label="QAE advantage holds")
    ax1.axhline(0.01, color="#d62728", linestyle="--", linewidth=1.2, label="ε=0.01 target")
    ax1.axvline(1e-3, color="#7f7f7f", linestyle="--", linewidth=1.2, label="Current IBM (~1e-3)")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlim(5e-6, 2e-2)
    ax1.set_xticks(x)
    ax1.set_xticklabels(xl, fontsize=9)
    ax1.set_xlabel("Depolarizing noise rate p", fontsize=11)
    ax1.set_ylabel("Mean price error |Δ| ($)", fontsize=11)
    ax1.set_title("Break-Even Frontier vs Noise Rate", fontsize=12, pad=10)
    ax1.legend(fontsize=9, framealpha=0.9)

    mo = oq["mean"].values
    so = oq["std"].values
    ax2.plot(x, mo, color="#ff7f0e", marker="o", linewidth=2, markersize=6,
             zorder=3, label="Mean oracle queries")
    ax2.fill_between(x, mo - so, mo + so, color="#ff7f0e", alpha=0.2, label="±1 std")
    ax2.axhline(14.5, color="#7f7f7f", linestyle="--", linewidth=1.2,
                label="Noise-invariant query depth")
    ax2.set_xscale("log")
    ax2.set_xlim(5e-6, 2e-2)
    ax2.set_xticks(x)
    ax2.set_xticklabels(xl, fontsize=9)
    ax2.set_xlabel("Depolarizing noise rate p", fontsize=11)
    ax2.set_ylabel("Mean oracle queries", fontsize=11)
    ax2.set_title("Oracle Query Depth vs Noise Rate", fontsize=12, pad=10)
    ax2.legend(fontsize=9, framealpha=0.9)

    plt.tight_layout()
    out = os.path.join(OUT, "fig_break_even_frontier.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved", out)


# ── Fig 4: hardware validation lollipop ──────────────────────────────────────
def fig_hardware():
    with open(os.path.join(RESULTS, "ibm_hardware_validation.json")) as f:
        hw = json.load(f)
    P_THEORY = hw["theoretical_p"]
    P_HW = hw["p_hat"]
    P_SIM = 0.2754
    SHOTS = hw["shots"]
    SIGMA = 0.0143
    points = [(0, P_HW, "#1f77b4", "Hardware", hw["backend"]),
              (1, P_SIM, "#ff7f0e", "Simulator", "AerSim (seed 42)")]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axhspan(P_THEORY - SIGMA, P_THEORY + SIGMA, color="#b0bec5", alpha=0.35,
               zorder=1, label=r"$\pm 1\sigma$ shot noise ($\sigma = 0.0143$)")
    ax.axhline(P_THEORY, color="#2ca02c", linestyle="--", linewidth=1.6, zorder=2,
               label=r"Theoretical  $p = 0.30$")
    for xi, v, color, *_ in points:
        ax.vlines(xi, v, P_THEORY, color=color, linewidth=3.0, alpha=0.9, zorder=3)
    ax.scatter([p[0] for p in points], [p[1] for p in points], s=190,
               c=[p[2] for p in points], edgecolor="black", linewidth=1.2, zorder=4)
    for xi, v, color, *_ in points:
        err = abs(v - P_THEORY)
        ax.annotate(f"$\\hat{{p}}$ = {v:.4f}\n|err| {err:.4f}  ({err / SIGMA:.1f}$\\sigma$)",
                    xy=(xi, v), xytext=(xi + 0.18, v), va="center", ha="left",
                    fontsize=9.5, color="black", zorder=5)
    ax.set_xlim(-0.6, 1.9)
    ax.set_ylim(0.262, 0.307)
    ax.set_xticks([p[0] for p in points])
    ax.set_xticklabels([f"{lbl}\n{sub}" for _, _, _, lbl, sub in points], fontsize=10)
    ax.set_ylabel(r"Estimated  $P(|1\rangle)$", fontsize=12)
    ax.set_title("IBM Quantum Hardware Validation — Deviation from Theory\n"
                 f"Single-qubit $P(|1\\rangle)$ encoding of p = 0.30   ·   {SHOTS} shots",
                 fontsize=11, pad=12)
    ax.legend(fontsize=9, framealpha=0.9, loc="lower right")
    ax.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    out = os.path.join(OUT, "hardware_validation_plot.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved", out)


if __name__ == "__main__":
    fig_heatmap()
    fig_mean_delta()
    fig_frontier()
    fig_hardware()
    print("Done — 4 white-background figures in", OUT)
