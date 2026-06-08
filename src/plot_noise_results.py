import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use("dark_background")

_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "noise_sweep_results.csv")
_FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")

_NOISE_LEVELS = [0, 1e-4, 1e-3, 5e-3, 1e-2]
_XLABELS = ["0", "1e-4", "1e-3", "5e-3", "1e-2"]


def _load() -> pd.DataFrame:
    return pd.read_csv(_CSV)


def _ylabels(df: pd.DataFrame) -> list[str]:
    base = df[df["p"] == 0].sort_values("pt_idx")
    labels = []
    for _, row in base.iterrows():
        sigma_str = f"{row['sigma']:.2f}".rstrip("0").rstrip(".")
        labels.append(
            f"P{int(row['pt_idx'])}  S0={row['S0']:.0f}  K={row['K']:.0f}"
            f"  T={row['T']:.2g}  σ={sigma_str}"
        )
    return labels


def fig_heatmap(df: pd.DataFrame) -> None:
    pivot = (
        df.pivot_table(index="pt_idx", columns="p", values="delta", aggfunc="mean")
        .reindex(columns=_NOISE_LEVELS)
    )
    matrix = pivot.values  # shape (10, 5)

    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto", vmin=0, vmax=8)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Price Error |Δ| ($) — capped at $8 for visibility", color="white")
    cbar.ax.yaxis.set_tick_params(color="white")

    ax.text(
        0.02, 0.97, "QAE ε=0.01 threshold: all points exceed it",
        transform=ax.transAxes, color="white", fontsize=8, va="top",
    )

    ax.set_xticks(range(len(_NOISE_LEVELS)))
    ax.set_xticklabels(_XLABELS, fontsize=9)
    ax.set_xlabel("Depolarizing noise rate p", fontsize=10)

    ylabs = _ylabels(df)
    ax.set_yticks(range(len(ylabs)))
    ax.set_yticklabels(ylabs, fontsize=8)

    ax.set_title("NISQ Noise vs Price Error — 10 Option Configurations", fontsize=11, pad=12)

    # Annotate each cell with its value
    for r in range(matrix.shape[0]):
        for c in range(matrix.shape[1]):
            val = matrix[r, c]
            text_color = "black" if val > matrix.max() * 0.6 else "white"
            ax.text(c, r, f"{val:.3f}", ha="center", va="center",
                    fontsize=7, color=text_color)

    plt.tight_layout()
    out = os.path.join(_FIG_DIR, "fig_noise_heatmap.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved {out}")
    plt.close(fig)


def fig_mean_delta(df: pd.DataFrame) -> None:
    stats = (
        df.groupby("p")["delta"]
        .agg(["mean", "min", "max"])
        .reindex(_NOISE_LEVELS)
        .reset_index()
    )

    # p=0 plotted at x=1e-5 so log axis works
    x_plot = stats["p"].replace(0, 1e-5).values

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.fill_between(x_plot, stats["min"], stats["max"],
                    alpha=0.25, color="#4fc3f7", label="Min–max band")
    ax.plot(x_plot, stats["mean"], color="#4fc3f7", marker="o",
            linewidth=2, markersize=6, label="Mean |Δ|")

    # Reference lines
    ax.axhline(0.01, color="#ef5350", linestyle="--", linewidth=1.2,
               label="QAE ε=0.01 precision target")
    ax.axvline(1e-3, color="#90a4ae", linestyle="--", linewidth=1.2,
               label="Current IBM hardware")

    ax.set_xscale("log")
    ax.set_yscale("log")

    # Custom x-ticks: show p=0 as "0 (ideal)", rest as-is
    xtick_vals = [1e-5, 1e-4, 1e-3, 5e-3, 1e-2]
    xtick_labels = ["0\n(ideal)", "1e-4", "1e-3", "5e-3", "1e-2"]
    ax.set_xticks(xtick_vals)
    ax.set_xticklabels(xtick_labels, fontsize=9)
    ax.set_xlim(5e-6, 2e-2)

    ax.set_xlabel("Noise rate p", fontsize=11)
    ax.set_ylabel("Mean |Δ| ($)", fontsize=11)
    ax.set_title("Mean Price Error vs Depolarizing Noise Rate", fontsize=12, pad=10)

    ax.legend(fontsize=9, framealpha=0.3)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)

    out = os.path.join(_FIG_DIR, "fig_mean_delta_vs_noise.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved {out}")
    plt.close(fig)


def main() -> None:
    os.makedirs(_FIG_DIR, exist_ok=True)
    df = _load()
    fig_heatmap(df)
    fig_mean_delta(df)


if __name__ == "__main__":
    main()
