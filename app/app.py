import os
import pickle
import sys
import time

import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, ctx, dcc, html
from dash.exceptions import PreventUpdate

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.black_scholes import black_scholes_call
from src.classical import monte_carlo_call

# ── QAE grid ──────────────────────────────────────────────────────────────────
_PKL = os.path.join(os.path.dirname(__file__), "..", "data", "qae_grid.pkl")
if not os.path.exists(_PKL):
    raise FileNotFoundError(
        f"QAE grid not found: {_PKL!r}\nRun:  python app/precompute_qae.py"
    )
with open(_PKL, "rb") as _f:
    _QAE: dict = pickle.load(_f)

_R_FIXED = 0.05
_S0G = [80.0, 90.0, 100.0, 110.0, 120.0]
_KG  = [90.0, 95.0, 100.0, 105.0, 110.0]
_TG  = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
_SGG = [0.15, 0.20, 0.25, 0.30]


def _snap(v, grid):
    """Return the nearest grid value — guards against float imprecision."""
    return min(grid, key=lambda g: abs(g - v))


_QAE_MISSING = {"price": None, "elapsed": None, "conf_int": (None, None), "oracle_queries": None}

def _qae_lookup(S0, K, T, sigma):
    key = (_snap(S0, _S0G), _snap(K, _KG), _snap(T, _TG), _R_FIXED, _snap(sigma, _SGG))
    result = _QAE.get(key)
    if result is None:
        print(f"QAE MISS: key={key}, available={list(_QAE.keys())[:3]}…", flush=True)
        return _QAE_MISSING
    return result


# ── Animation schedule (log-spaced N from 100 → 50 000) ───────────────────────
_N_SCHED = np.unique(np.logspace(np.log10(100), np.log10(50_000), 15).astype(int)).tolist()

# ── Colours ───────────────────────────────────────────────────────────────────
_C_BS = "#22c55e"
_C_MC = "#f59e0b"
_C_QA = "#818cf8"

# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(__name__, suppress_callback_exceptions=False, serve_locally=True, title="Quantum Option Pricing")
server = app.server  # gunicorn entry point


def _slider(sid, label, mn, mx, val, marks):
    return html.Div([
        html.Label(label, className="slider-label"),
        dcc.Slider(id=sid, min=mn, max=mx, value=val, step=None,
                   marks={str(m): str(m) for m in marks}),
    ], className="slider-wrap")


# ── Default values computed once at startup (both sub-millisecond) ─────────────
_DEF_BS  = black_scholes_call(100.0, 100.0, _R_FIXED, 0.20, 1.0)
_DEF_QAE = _qae_lookup(100.0, 100.0, 1.0, 0.20)
_DEF_QP  = _DEF_QAE["price"]   or 0.0
_DEF_QMS = (_DEF_QAE["elapsed"] or 0.0) * 1000


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
            _slider("sl-t",  "T — Expiry (years)",   0.25, 2.0, 1.0, [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]),
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

    html.Footer([
        html.Span("Prithvi"),
        html.Span(" · "),
        html.A("GitHub", href="https://github.com/Prithvi8706/quantum_option_pricing",
               target="_blank", rel="noopener noreferrer"),
        html.Span(" · Built with Qiskit · Plotly Dash · Railway"),
    ], className="footer"),

    # Full computed dataset for the current params (filled once per slider move)
    dcc.Store(id="mc-data"),
    # Current animation frame index, driven entirely client-side
    dcc.Store(id="mc-frame", data=0),
    # Client-side animation clock — runs in the browser, never hits the server
    dcc.Interval(id="anim-iv", interval=130, n_intervals=0),
], className="page")


# ══════════════════════════════════════════════════════════════════════════════
# SERVER CALLBACK — fires ONCE per slider change.
# Computes the entire MC convergence series + BS + QAE in a single pass and
# stores it. After this returns, the server is never touched again for the
# animation, so nothing can queue up or hang.
# ══════════════════════════════════════════════════════════════════════════════
@app.callback(
    Output("mc-data",  "data"),
    Output("bs-price", "children"),
    Output("qae-price", "children"),
    Output("qae-meta",  "children"),
    Input("sl-s0", "value"),
    Input("sl-k",  "value"),
    Input("sl-t",  "value"),
    Input("sl-sg", "value"),
    prevent_initial_call=True,
)
def _compute(S0, K, T, sigma):
    r = _R_FIXED

    # Black-Scholes (exact, sub-ms)
    bs = black_scholes_call(S0, K, r, sigma, T)

    # QAE pre-computed lookup
    entry = _qae_lookup(S0, K, T, sigma)
    qp    = entry["price"]   or 0.0
    qe_ms = (entry["elapsed"] or 0.0) * 1000

    # Full Monte Carlo convergence series — all frames in one pass
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

    data = {
        "bs": float(bs),
        "qp": float(qp),
        "qe_ms": float(qe_ms),
        "frames": frames,
        "n_frames": len(frames),
        "colors": {"bs": _C_BS, "mc": _C_MC, "qa": _C_QA},
    }

    return (
        data,
        f"${bs:.4f}",
        f"${qp:.4f}",
        f"{qe_ms:.0f} ms · pre-computed on Qiskit statevector",
    )


# ══════════════════════════════════════════════════════════════════════════════
# CLIENT-SIDE CALLBACK — frame advancer.
# On each browser interval tick, bump the frame index until we reach the last
# frame, then hold. Runs entirely in the browser; no server contact.
# ══════════════════════════════════════════════════════════════════════════════
app.clientside_callback(
    """
    function(n_intervals, data, current) {
        if (!data || !data.frames) {
            return window.dash_clientside.no_update;
        }
        const last = data.n_frames - 1;
        const cur = (current === null || current === undefined) ? 0 : current;
        if (cur >= last) {
            return window.dash_clientside.no_update;  // animation finished
        }
        return cur + 1;
    }
    """,
    Output("mc-frame", "data"),
    Input("anim-iv", "n_intervals"),
    State("mc-data", "data"),
    State("mc-frame", "data"),
    prevent_initial_call=True,
)


# ══════════════════════════════════════════════════════════════════════════════
# CLIENT-SIDE CALLBACK — renderer.
# Whenever the frame index OR the dataset changes, redraw both charts + the MC
# price/meta text. Pure browser-side Plotly; no server contact.
# ══════════════════════════════════════════════════════════════════════════════
app.clientside_callback(
    """
    function(frame, data) {
        const nu = window.dash_clientside.no_update;
        if (!data || !data.frames || data.frames.length === 0) {
            return [nu, nu, nu, nu];
        }

        const f = (frame === null || frame === undefined) ? 0 : frame;
        const upto = data.frames.slice(0, f + 1);
        const last = upto[upto.length - 1];
        const C = data.colors;

        // ── MC mini-chart ────────────────────────────────────────────────
        const Ns  = upto.map(d => d.N);
        const ps  = upto.map(d => d.p);
        const los = upto.map(d => d.lo);
        const his = upto.map(d => d.hi);

        const mcFig = {
            data: [
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
                    line: {color: C.mc, width: 2},
                    type: "scatter",
                    hovertemplate: "N=%{x:,}<br>$%{y:.4f}<extra></extra>",
                },
            ],
            layout: {
                template: undefined,
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
                shapes: [{
                    type: "line", xref: "paper", x0: 0, x1: 1,
                    yref: "y", y0: data.bs, y1: data.bs,
                    line: {color: C.bs, width: 1, dash: "dot"},
                }],
            },
        };

        // ── Scatter: accuracy vs compute time ────────────────────────────
        const xs = upto.map(d => Math.max(d.ms, 1e-3));
        const ys = upto.map(d => Math.max(Math.abs(d.p - data.bs), 1e-5));

        const scatterData = [
            {
                x: [0.05], y: [5e-5],
                mode: "markers+text", text: ["Black-Scholes"],
                textposition: "top right",
                marker: {color: C.bs, size: 15},
                type: "scatter",
                hovertemplate: "Black-Scholes<br>~0 ms · exact<extra></extra>",
            },
        ];

        if (xs.length > 1) {
            scatterData.push({
                x: xs.slice(0, -1), y: ys.slice(0, -1),
                mode: "markers",
                marker: {color: C.mc, size: 5, opacity: 0.25},
                type: "scatter", hoverinfo: "skip",
            });
        }
        scatterData.push({
            x: [xs[xs.length - 1]], y: [ys[ys.length - 1]],
            mode: "markers+text", text: ["Monte Carlo"],
            textposition: "top right",
            marker: {color: C.mc, size: 15},
            type: "scatter",
            hovertemplate: "Monte Carlo<br>N=" + last.N.toLocaleString() +
                           "<br>Error: $%{y:.4f}<extra></extra>",
        });
        scatterData.push({
            x: [Math.max(data.qe_ms, 0.1)],
            y: [Math.max(Math.abs(data.qp - data.bs), 1e-5)],
            mode: "markers+text", text: ["QAE"],
            textposition: "top right",
            marker: {color: C.qa, size: 15, symbol: "diamond"},
            type: "scatter",
            hovertemplate: "QAE (pre-computed)<br>Time: %{x:.0f} ms<br>" +
                           "Error: $%{y:.4f}<extra></extra>",
        });

        const scatterFig = {
            data: scatterData,
            layout: {
                paper_bgcolor: "rgba(0,0,0,0)",
                plot_bgcolor: "rgba(0,0,0,0)",
                font: {color: "#e5e7eb"},
                title: {text: "Accuracy vs Compute Time",
                        font: {size: 15}, x: 0.5},
                xaxis: {type: "log", title: {text: "Compute Time (ms)"},
                        gridcolor: "rgba(255,255,255,0.07)", color: "#e5e7eb"},
                yaxis: {type: "log",
                        title: {text: "Error vs Black-Scholes ($)"},
                        gridcolor: "rgba(255,255,255,0.07)", color: "#e5e7eb"},
                margin: {l: 70, r: 20, t: 55, b: 55},
                height: 360,
                showlegend: false,
            },
        };

        // ── MC price + meta text ─────────────────────────────────────────
        const ci = (last.hi - last.lo) / 2;
        const priceStr = "$" + last.p.toFixed(4);
        const metaStr = "N = " + last.N.toLocaleString() +
                        " · ±" + ci.toFixed(4) + " (95% CI)";

        return [mcFig, scatterFig, priceStr, metaStr];
    }
    """,
    Output("mc-graph", "figure"),
    Output("scatter",  "figure"),
    Output("mc-price", "children"),
    Output("mc-meta",  "children"),
    Input("mc-frame", "data"),
    Input("mc-data",  "data"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))