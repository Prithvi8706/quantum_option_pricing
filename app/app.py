import os
import pickle
import sys
import time

import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.black_scholes import black_scholes_call
from src.classical import monte_carlo_call
from app.precompute_qae import (
    K_VALUES as _KG,
    R_FIXED as _R_FIXED,
    S0_VALUES as _S0G,
    SIGMA_VALUES as _SG,
    T_VALUES as _TG,
)

# ── QAE grid ──────────────────────────────────────────────────────────────────
_PKL = os.path.join(os.path.dirname(__file__), "..", "data", "qae_grid.pkl")
if not os.path.exists(_PKL):
    raise FileNotFoundError(
        f"QAE grid not found: {_PKL!r}\nRun:  python app/precompute_qae.py"
    )
with open(_PKL, "rb") as _f:
    _QAE: dict = pickle.load(_f)



def _snap(v, grid):
    """Return the nearest grid value — guards against float imprecision."""
    return min(grid, key=lambda g: abs(g - v))


_QAE_MISSING = {"price": None, "elapsed": None, "conf_int": (None, None), "oracle_queries": None}

def _qae_lookup(S0, K, T, sigma):
    key = (_snap(S0, _S0G), _snap(K, _KG), _snap(T, _TG), _R_FIXED, _snap(sigma, _SG))
    result = _QAE.get(key)
    if result is None:
        print(f"QAE MISS: key={key}, available={list(_QAE.keys())[:3]}…", flush=True)
        return dict(_QAE_MISSING)
    return result


# ── Monte Carlo sample schedule (log-spaced N from 100 → 50 000) ──────────────
_N_SCHED = np.unique(np.logspace(np.log10(100), np.log10(50_000), 15).astype(int)).tolist()

# ── Colours ───────────────────────────────────────────────────────────────────
_C_BS = "#22c55e"
_C_MC = "#f59e0b"
_C_QAE = "#818cf8"

# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(
    __name__,
    suppress_callback_exceptions=False,
    serve_locally=True,
    title="Quantum Option Pricing",
)
server = app.server  # gunicorn entry point


def _slider(sid, label, mn, mx, val, marks):
    return html.Div([
        html.Label(label, className="slider-label"),
        dcc.Slider(id=sid, min=mn, max=mx, value=val, step=None,
                   marks={m: str(m) for m in marks}),
    ], className="slider-wrap")


# ── Default values computed once at startup (both sub-millisecond) ─────────────
_DEF_BS  = black_scholes_call(100.0, 100.0, _R_FIXED, 0.20, 1.0)
_DEF_QAE = _qae_lookup(100.0, 100.0, 1.0, 0.20)
_DEF_QP  = _DEF_QAE["price"]   if _DEF_QAE["price"]   is not None else 0.0
_DEF_QMS = (_DEF_QAE["elapsed"] if _DEF_QAE["elapsed"] is not None else 0.0) * 1000


def _mc_placeholder_fig(bs_price):
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        margin=dict(l=46, r=8, t=8, b=32),
        height=158,
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False, color="#888"),
        yaxis=dict(showgrid=False, showticklabels=False, color="#888"),
    )
    fig.add_hline(y=bs_price, line=dict(color=_C_BS, width=1, dash="dot"))
    fig.add_annotation(
        x=0.5, y=0.5, xref="paper", yref="paper",
        text="Move a slider to start simulation",
        showarrow=False,
        font=dict(color="#9ca3af", size=11),
    )
    return fig


def _scatter_placeholder():
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text="Accuracy vs Compute Time", font=dict(size=15), x=0.5),
        xaxis=dict(type="log", title="Compute Time (ms)",
                   gridcolor="rgba(255,255,255,0.07)", showticklabels=False),
        yaxis=dict(type="log", title="Error vs Black-Scholes ($)",
                   gridcolor="rgba(255,255,255,0.07)", showticklabels=False),
        margin=dict(l=70, r=20, t=55, b=55),
        height=360,
    )
    fig.add_annotation(
        x=0.5, y=0.5, xref="paper", yref="paper",
        text="Move a slider to compare methods",
        showarrow=False, font=dict(color="#9ca3af", size=13),
    )
    return fig


def _breakeven_placeholder():
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(
            text="QAE Break-Even: Oracle Queries vs Monte Carlo Samples",
            font=dict(size=15), x=0.5
        ),
        xaxis=dict(
            type="log", title="Required Precision ε (error in option price $)",
            gridcolor="rgba(255,255,255,0.07)", showticklabels=False,
        ),
        yaxis=dict(
            type="log", title="Compute Cost (samples or oracle queries)",
            gridcolor="rgba(255,255,255,0.07)", showticklabels=False,
        ),
        margin=dict(l=70, r=20, t=55, b=55),
        height=360,
    )
    fig.add_annotation(
        x=0.5, y=0.5, xref="paper", yref="paper",
        text="Move a slider to see break-even analysis",
        showarrow=False, font=dict(color="#9ca3af", size=13),
    )
    return fig


def _build_breakeven_fig(qae_result: dict, bs_price: float, sigma: float):
    """
    QAE vs MC break-even (Stamatopoulos eq.3, Woerner eq.2):
        QAE error:   ε = π / M         (M = oracle queries)
        MC error:    ε = 1.96 / √N     (N = samples, 95% CI)
        Break-even:  M_be = π√N / 1.96 ≈ 1.604 × √N
    """
    eps = np.logspace(-3, 0, 200)

    N_mc        = (1.96 / eps) ** 2
    M_qae       = np.pi / eps
    M_nisq_lo   = 100  * M_qae
    M_nisq_hi   = 1000 * M_qae

    oracle_q  = qae_result.get("oracle_queries")
    qae_price = qae_result.get("price")

    if qae_price is not None and bs_price is not None:
        eps_current = max(abs(qae_price - bs_price), 1e-3)
    else:
        eps_current = None

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=np.concatenate([eps, eps[::-1]]),
        y=np.concatenate([M_nisq_hi, M_nisq_lo[::-1]]),
        fill="toself",
        fillcolor="rgba(129,140,248,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        name="NISQ overhead band (100×–1000×)",
        showlegend=True,
    ))

    fig.add_trace(go.Scatter(
        x=eps, y=M_qae,
        mode="lines",
        line=dict(color=_C_QAE, width=2),
        name="QAE ideal  O(1/ε)",
        hovertemplate="ε = $%{x:.4f}<br>Oracle queries = %{y:.0f}<extra>QAE ideal</extra>",
    ))

    fig.add_trace(go.Scatter(
        x=eps, y=N_mc,
        mode="lines",
        line=dict(color=_C_MC, width=2),
        name="Monte Carlo  O(1/ε²)",
        hovertemplate="ε = $%{x:.4f}<br>Samples needed = %{y:.0f}<extra>Monte Carlo</extra>",
    ))

    eps_ref       = 0.01
    n_mc_ref      = (1.96 / eps_ref) ** 2
    m_qae_ref     = np.pi / eps_ref
    m_nisq_ref_lo = 100 * m_qae_ref

    fig.add_annotation(
        x=eps_ref, y=m_nisq_ref_lo,
        text=(
            f"At ε=$0.01:<br>MC needs {n_mc_ref:,.0f} samples<br>"
            f"QAE ideal needs {m_qae_ref:.0f} queries<br>"
            f"NISQ needs >{m_nisq_ref_lo:,.0f} queries"
        ),
        showarrow=True,
        arrowhead=2,
        arrowcolor="#6b7280",
        font=dict(color="#9ca3af", size=10),
        bgcolor="rgba(17,24,39,0.85)",
        bordercolor="#374151",
        borderwidth=1,
        ax=80, ay=-60,
    )

    if oracle_q is not None and eps_current is not None:
        fig.add_trace(go.Scatter(
            x=[eps_current],
            y=[oracle_q],
            mode="markers+text",
            text=["This run"],
            textposition="top right",
            marker=dict(color=_C_QAE, size=14, symbol="diamond",
                        line=dict(color="white", width=1)),
            name=f"This QAE run ({oracle_q} queries)",
            hovertemplate=(
                f"QAE pre-computed<br>"
                f"Oracle queries: {oracle_q}<br>"
                f"Error vs BS: $%{{x:.4f}}<extra></extra>"
            ),
        ))

    if eps_current is not None:
        fig.add_vline(
            x=eps_current,
            line=dict(color="#6b7280", width=1, dash="dot"),
            annotation_text="Current ε",
            annotation_font=dict(color="#6b7280", size=10),
            annotation_position="top",
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        title=dict(
            text="QAE Break-Even: Oracle Queries vs Monte Carlo Samples",
            font=dict(size=15), x=0.5,
        ),
        xaxis=dict(
            type="log",
            title="Required Precision ε (error in option price, $)",
            gridcolor="rgba(255,255,255,0.07)",
            color="#e5e7eb",
            autorange="reversed",
        ),
        yaxis=dict(
            type="log",
            title="Compute Cost (samples or oracle queries)",
            gridcolor="rgba(255,255,255,0.07)",
            color="#e5e7eb",
        ),
        legend=dict(
            x=0.02, y=0.98,
            bgcolor="rgba(17,24,39,0.7)",
            bordercolor="#374151",
            borderwidth=1,
            font=dict(size=11),
        ),
        margin=dict(l=70, r=20, t=55, b=55),
        height=400,
    )

    return fig


app.layout = html.Div([
    html.Div([
        html.H1("Quantum Option Pricing", className="title"),
        html.P(
            "Black-Scholes · Monte Carlo · Quantum Amplitude Estimation",
            className="subtitle",
        ),
    ], className="header"),

    html.Div([
        # Sidebar
        html.Div([
            html.H3("Parameters", className="sidebar-title"),
            _slider("sl-s0", "S₀ — Stock Price ($)", 80, 120, 100, [80, 90, 100, 110, 120]),
            _slider("sl-k",  "K — Strike Price ($)",  90, 110, 100, [90, 95, 100, 105, 110]),
            _slider("sl-t",  "T — Expiry (years)",   0.25, 2.0, 1.0,
                    [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]),
            _slider("sl-sg", "σ — Volatility",       0.15, 0.30, 0.20, [0.15, 0.20, 0.25, 0.30]),
            html.Div([
                html.Label("r — Risk-free Rate", className="slider-label"),
                html.Div("5% (fixed)", className="fixed-param"),
            ], className="slider-wrap"),
        ], className="sidebar"),

        # Method cards
        html.Div([
            # Black-Scholes
            html.Div([
                html.Div("Black-Scholes", className="method-label"),
                html.Div(f"${_DEF_BS:.4f}", id="bs-price", className="price-big"),
                html.Div("< 1 ms · exact closed-form", id="bs-meta", className="meta"),
            ], className="card card-bs"),

            # Monte Carlo
            html.Div([
                html.Div("Monte Carlo", className="method-label"),
                html.Div("—", id="mc-price", className="price-big"),
                html.Div("Move a slider to start simulation", id="mc-meta", className="meta"),
                dcc.Graph(id="mc-graph", figure=_mc_placeholder_fig(_DEF_BS),
                          config={"displayModeBar": False}, className="mini-chart"),
            ], className="card card-mc"),

            # QAE
            html.Div([
                html.Div("Quantum (QAE)", className="method-label"),
                html.Div(f"${_DEF_QP:.4f}", id="qae-price", className="price-big"),
                html.Div(f"{_DEF_QMS:.0f} ms · pre-computed on Qiskit statevector",
                         id="qae-meta", className="meta"),
                html.Div("", id="qae-note", className="qae-note"),
            ], className="card card-qae"),
        ], className="cards"),
    ], className="main-row"),

    html.Div([
        dcc.Graph(id="scatter", figure=_scatter_placeholder(),
                  config={"displayModeBar": False}),
    ], className="scatter-wrap"),

    html.Div([
        dcc.Graph(
            id="breakeven-chart",
            figure=_breakeven_placeholder(),
            config={"displayModeBar": False},
        ),
        html.Div([
            html.Span("Break-even formula: M = π√N / 1.96  ·  ", className="be-citation"),
            html.A("Stamatopoulos et al. (2020) eq. (3)",
                   href="https://arxiv.org/abs/1905.02666",
                   target="_blank", rel="noopener noreferrer",
                   className="be-citation-link"),
            html.Span("  ·  ", className="be-citation"),
            html.A("Woerner & Egger (2019) eq. (2)",
                   href="https://arxiv.org/abs/1806.06893",
                   target="_blank", rel="noopener noreferrer",
                   className="be-citation-link"),
        ], className="be-citation-row"),
    ], className="breakeven-wrap"),

    html.Footer([
        html.Span("Prithvi"),
        html.Span(" · "),
        html.A("GitHub", href="https://github.com/Prithvi8706/quantum_option_pricing",
               target="_blank", rel="noopener noreferrer"),
        html.Span(" · Built with Qiskit · Plotly Dash · Railway"),
    ], className="footer"),

    # Full computed dataset for the current params (filled once per slider move)
    dcc.Store(id="mc-data"),
    html.Div(id="anim-sink", style={"display": "none"}),  # Output sink for clientside_callback
], className="page")


# ══════════════════════════════════════════════════════════════════════════════
# SERVER CALLBACK — fires ONCE per slider change.
# Computes the entire MC convergence series + BS + QAE in a single pass and
# stores it. After this returns, the server is never touched again, so nothing
# can queue up or hang.
# ══════════════════════════════════════════════════════════════════════════════
@app.callback(
    Output("mc-data",  "data"),
    Output("bs-price", "children"),
    Output("qae-price", "children"),
    Output("qae-meta",  "children"),
    Output("qae-note",  "children"),
    Output("mc-price", "children"),
    Output("mc-meta",  "children"),
    Output("breakeven-chart", "figure"),
    Input("sl-s0", "value"),
    Input("sl-k",  "value"),
    Input("sl-t",  "value"),
    Input("sl-sg", "value"),
    prevent_initial_call=True,
)
def _compute(S0, K, T, sigma):
    r = _R_FIXED

    t_bs = time.perf_counter()
    bs = black_scholes_call(S0, K, r, sigma, T)
    bs_ms = (time.perf_counter() - t_bs) * 1000

    entry = _qae_lookup(S0, K, T, sigma)
    qp    = entry["price"]   if entry["price"]   is not None else 0.0
    qe_ms = (entry["elapsed"] if entry["elapsed"] is not None else 0.0) * 1000

    if entry["price"] is None:
        qae_note = "No precomputed result for this parameter combination"
    else:
        snapped = (_snap(S0, _S0G), _snap(K, _KG), _snap(T, _TG), _snap(sigma, _SG))
        inputs  = (S0, K, T, sigma)
        labels  = ("S₀", "K", "T", "σ")
        diffs = [
            f"{lbl}={s} (selected {i})"
            for lbl, s, i in zip(labels, snapped, inputs)
            if abs(s - i) > 1e-9
        ]
        qae_note = f"Nearest match used: {', '.join(diffs)}" if diffs else ""

    frames = []
    for N in _N_SCHED:
        t1 = time.perf_counter()
        mc_p, mc_err = monte_carlo_call(S0, K, r, sigma, T, N)
        mc_ms = (time.perf_counter() - t1) * 1000
        frames.append({
            "N": int(N),
            "p": float(mc_p),
            "lo": float(mc_p - 1.96 * mc_err),
            "hi": float(mc_p + 1.96 * mc_err),
            "ms": float(mc_ms),
        })

    last = frames[-1]
    ci = (last["hi"] - last["lo"]) / 2
    mc_price_str = f"${last['p']:.4f}"
    mc_meta_str  = f"N = {last['N']:,} · ±{ci:.4f} (95% CI)"

    # schema consumed by clientside_callback:
    # {bs, bs_ms, qp, qe_ms, frames:[{N,p,lo,hi,ms}], colors:{bs,mc,qae}}
    data = {
        "bs": float(bs),
        "bs_ms": float(max(bs_ms, 1e-3)),
        "qp": float(qp),
        "qe_ms": float(qe_ms),
        "frames": frames,
        "colors": {"bs": _C_BS, "mc": _C_MC, "qae": _C_QAE},
    }

    be_fig = _build_breakeven_fig(qae_result=entry, bs_price=bs, sigma=sigma)

    return (
        data,
        f"${bs:.4f}",
        f"${qp:.4f}",
        f"{qe_ms:.0f} ms · pre-computed on Qiskit statevector",
        qae_note,
        mc_price_str,
        mc_meta_str,
        be_fig,
    )


# ══════════════════════════════════════════════════════════════════════════════
# CLIENT-SIDE CALLBACK — renderer with eased transition.
# Draws the full curves, and animates markers/line gliding from their previous
# positions to the new ones via Plotly.animate(). Pure browser-side; never hits
# the server. Returns no_update for the figure outputs because the actual redraw
# is done imperatively through Plotly.animate on the existing graph divs.
# ══════════════════════════════════════════════════════════════════════════════
app.clientside_callback(
    """
    function(data) {
        const nu = window.dash_clientside.no_update;
        if (!data || !data.frames || data.frames.length === 0) {
            return "";
        }

        const frames = data.frames;
        const C = data.colors;

        const Ns  = frames.map(d => d.N);
        const ps  = frames.map(d => d.p);
        const los = frames.map(d => d.lo);
        const his = frames.map(d => d.hi);

        // ── MC mini-chart traces ─────────────────────────────────────────
        const xMin = Ns[0];
        const xMax = Ns[Ns.length - 1];
        const mcData = [
            {
                // Black-Scholes reference line as a TRACE so it glides (animate
                // tweens trace data; layout shapes would snap instantly).
                x: [xMin, xMax],
                y: [data.bs, data.bs],
                mode: "lines",
                line: {color: C.bs, width: 1, dash: "dot"},
                hoverinfo: "skip",
                type: "scatter",
            },
            {
                x: Ns.concat(Ns.slice().reverse()),
                y: his.concat(los.slice().reverse()),
                fill: "toself",
                fillcolor: "rgba(245,158,11,0.12)",
                line: {color: "rgba(0,0,0,0)"},
                hoverinfo: "skip",
                type: "scatter",
            },
            {
                x: Ns, y: ps,
                mode: "lines+markers",
                line: {color: C.mc, width: 2},
                marker: {color: C.mc, size: 6},
                type: "scatter",
                hovertemplate: "N=%{x:,}<br>$%{y:.4f}<extra></extra>",
            },
        ];
        const mcLayout = {
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            margin: {l: 46, r: 8, t: 8, b: 32},
            height: 158,
            showlegend: false,
            font: {color: "#888"},
            xaxis: {type: "log", showgrid: false, color: "#888",
                    tickfont: {size: 9, color: "#888"}},
            yaxis: {showgrid: false, color: "#888",
                    tickfont: {size: 9, color: "#888"}},
        };

        // ── Scatter traces (accuracy vs compute time) ────────────────────
        const xs = frames.map(d => Math.max(d.ms, 1e-3));
        const ys = frames.map(d => Math.max(Math.abs(d.p - data.bs), 1e-5));
        const bsY = Math.min(...ys) / 10;

        const scatterData = [
            {
                x: [data.bs_ms], y: [bsY],
                mode: "markers+text", text: ["Black-Scholes"],
                textposition: "top right",
                marker: {color: C.bs, size: 15},
                type: "scatter",
                hovertemplate: "Black-Scholes<br>~0 ms · exact<extra></extra>",
            },
            {
                x: xs.slice(0, -1), y: ys.slice(0, -1),
                mode: "markers",
                marker: {color: C.mc, size: 5, opacity: 0.25},
                type: "scatter", hoverinfo: "skip",
            },
            {
                x: [xs[xs.length - 1]], y: [ys[ys.length - 1]],
                mode: "markers+text", text: ["Monte Carlo"],
                textposition: "top right",
                marker: {color: C.mc, size: 15},
                type: "scatter",
                hovertemplate: "Monte Carlo<br>Error: $%{y:.4f}<extra></extra>",
            },
            {
                x: [Math.max(data.qe_ms, 0.1)],
                y: [Math.max(Math.abs(data.qp - data.bs), 1e-5)],
                mode: "markers+text", text: ["QAE"],
                textposition: "top right",
                marker: {color: C.qae, size: 15, symbol: "diamond"},
                type: "scatter",
                hovertemplate: "QAE (pre-computed)<br>Time: %{x:.0f} ms<br>" +
                               "Error: $%{y:.4f}<extra></extra>",
            },
        ];
        const scatterLayout = {
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            font: {color: "#e5e7eb"},
            title: {text: "Accuracy vs Compute Time", font: {size: 15}, x: 0.5},
            xaxis: {type: "log", title: {text: "Compute Time (ms)"},
                    gridcolor: "rgba(255,255,255,0.07)", color: "#e5e7eb"},
            yaxis: {type: "log", title: {text: "Error vs Black-Scholes ($)"},
                    gridcolor: "rgba(255,255,255,0.07)", color: "#e5e7eb"},
            margin: {l: 70, r: 20, t: 55, b: 55},
            height: 360,
            showlegend: false,
        };

        const transition = {duration: 700, easing: "cubic-in-out"};
        const animOpts = {
            transition: transition,
            frame: {duration: 700, redraw: false},
        };

        // Defer to let Dash finish its DOM updates, then animate imperatively.
        setTimeout(function() {
            const Plotly = window.Plotly;
            if (!Plotly) { return; }

            function drawOrAnimate(gdId, traceData, layout) {
                const gd = document.getElementById(gdId);
                if (!gd) { return; }
                // .js-plotly-plot and .data are undocumented Plotly internals — fragile on a
                // major version bump. If animation breaks after a Plotly upgrade, check here first.
                const plotDiv = gd.querySelector(".js-plotly-plot") || gd;
                const hasPlot = plotDiv && plotDiv.data && plotDiv.data.length > 0;
                if (!hasPlot) {
                    // First render for these params: draw fresh (no tween possible).
                    Plotly.react(plotDiv, traceData, layout, {displayModeBar: false});
                } else {
                    // Subsequent render: relayout (axes) then animate traces to glide.
                    Plotly.relayout(plotDiv, layout);
                    Plotly.animate(plotDiv, {data: traceData}, animOpts);
                }
            }

            drawOrAnimate("mc-graph", mcData, mcLayout);
            drawOrAnimate("scatter", scatterData, scatterLayout);
        }, 0);

        // Figures are driven imperatively above; nothing reads this sink.
        return "";
    }
    """,
    Output("anim-sink", "children"),
    Input("mc-data", "data"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
