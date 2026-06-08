import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use("dark_background")

_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "noise_sweep_expanded.csv")
_FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")

_NOISE_LEVELS = [0, 1e-4, 1e-3, 5e-3, 1e-2]
_X_PLOT = [1e-5, 1e-4, 1e-3, 5e-3, 1e-2]  # p=0 mapped to 1e-5 for log axis
_XLABELS = ["0\n(ideal)", "1e-4", "1e-3", "5e-3", "1e-2"]


def main() -> None:
    os.makedirs(_FIG_DIR, exist_ok=True)
    df = pd.read_csv(_CSV)

    stats = (
        df.groupby("p")["delta"]
        .agg(["mean", "std"])
        .reindex(_NOISE_LEVELS)
        .reset_index()
    )
    oq_stats = (
        df.groupby("p")["oracle_queries"]
        .agg(["mean", "std"])
        .reindex(_NOISE_LEVELS)
        .reset_index()
    )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # ── Left panel: break-even frontier ──────────────────────────────────────
    mean_delta = stats["mean"].values
    ax1.plot(_X_PLOT, mean_delta, color="#4fc3f7", marker="o", linewidth=2,
             markersize=6, zorder=3)

    # Shade above/below threshold
    y_top = max(mean_delta.max() * 2, 0.05)
    ax1.fill_between([5e-6, 2e-2], 0.01, y_top,
                     color="#ef5350", alpha=0.15, label="QAE advantage lost")
    ax1.fill_between([5e-6, 2e-2], 0, 0.01,
                     color="#66bb6a", alpha=0.15, label="QAE advantage holds")

    ax1.axhline(0.01, color="#ef5350", linestyle="--", linewidth=1.2,
                label="ε=0.01 target")
    ax1.axvline(1e-3, color="#90a4ae", linestyle="--", linewidth=1.2,
                label="Current IBM (~1e-3)")

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlim(5e-6, 2e-2)
    ax1.set_xticks(_X_PLOT)
    ax1.set_xticklabels(_XLABELS, fontsize=9)
    ax1.set_xlabel("Depolarizing noise rate p", fontsize=11)
    ax1.set_ylabel("Mean price error |Δ| ($)", fontsize=11)
    ax1.set_title("Break-Even Frontier vs Noise Rate", fontsize=12, pad=10)
    ax1.legend(fontsize=9, framealpha=0.3)

    # ── Right panel: oracle queries vs noise ─────────────────────────────────
    mean_oq = oq_stats["mean"].values
    std_oq = oq_stats["std"].values

    ax2.plot(_X_PLOT, mean_oq, color="#ffa726", marker="o", linewidth=2,
             markersize=6, zorder=3, label="Mean oracle queries")
    ax2.fill_between(_X_PLOT,
                     mean_oq - std_oq,
                     mean_oq + std_oq,
                     color="#ffa726", alpha=0.2, label="±1 std")

    ax2.axhline(14.5, color="#90a4ae", linestyle="--", linewidth=1.2,
                label="Noise-invariant query depth")

    ax2.set_xscale("log")
    ax2.set_xlim(5e-6, 2e-2)
    ax2.set_xticks(_X_PLOT)
    ax2.set_xticklabels(_XLABELS, fontsize=9)
    ax2.set_xlabel("Depolarizing noise rate p", fontsize=11)
    ax2.set_ylabel("Mean oracle queries", fontsize=11)
    ax2.set_title("Oracle Query Depth vs Noise Rate", fontsize=12, pad=10)
    ax2.legend(fontsize=9, framealpha=0.3)

    plt.tight_layout()
    out = os.path.join(_FIG_DIR, "fig_break_even_frontier.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
