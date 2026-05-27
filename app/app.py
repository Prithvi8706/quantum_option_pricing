import os
import pickle
import sys
import time

import numpy as np
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, ctx, dcc, html

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
_N_SCHED = np.unique(np.logspace(np.log10(100), np.log10(50_000), 35).astype(int)).tolist()

_SLIDER_IDS = {"sl-s0", "sl-k", "sl-t", "sl-sg"}

# ── Colours ───────────────────────────────────────────────────────────────────
_C_BS = "#22c55e"
_C_MC = "#f59e0b"
_C_QA = "#818cf8"

# ── Shared chart layout (defined early so layout + figures can both use it) ───
_DARK_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=46, r=8, t=8, b=32),
    height=158,
    showlegend=False,
    xaxis=dict(showgrid=False, color="#888", tickfont=dict(size=9, color="#888")),
    yaxis=dict(showgrid=False, color="#888", tickfont=dict(size=9, color="#888")),
)


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


# ── Default values computed once at startup (both sub-millisecond) ─────────────
_DEF_BS  = black_scholes_call(100.0, 100.0, _R_FIXED, 0.20, 1.0)
_DEF_QAE = _qae_lookup(100.0, 100.0, 1.0, 0.20)
_DEF_QP  = _DEF_QAE["price"]   or 0.0
_DEF_QMS = (_DEF_QAE["elapsed"] or 0.0) * 1000

# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(__name__, suppress_callback_exceptions=False, serve_locally=True, title="Quantum Option Pricing")
server = app.server  # gunicorn entry point


def _slider(sid, label, mn, mx, val, marks):
    return html.Div([
        html.Label(label, className="slider-label"),
        dcc.Slider(id=sid, min=mn, max=mx, value=val, step=None,
                   marks={str(m): str(m) for m in marks}),
    ], className="slider-wrap")


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
                dcc.Interval(id="mc-iv", interval=120, n_intervals=0, disabled=True),
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
        dcc.Graph(id="scatter", config={"displayModeBar": False}),
    ], className="scatter-wrap"),

    dcc.Store(id="mc-store", data={"step": 0, "hist": [], "params": None}),
], className="page")


@app.callback(
    Output("mc-store",  "data"),
    Output("mc-iv",     "disabled"),
    Output("mc-graph",  "figure"),
    Output("mc-price",  "children"),
    Output("mc-meta",   "children"),
    Output("bs-price",  "children"),
    Output("bs-meta",   "children"),
    Output("qae-price", "children"),
    Output("qae-meta",  "children"),
    Output("qae-note",  "children"),
    Output("scatter",   "figure"),
    Input("mc-iv",  "n_intervals"),
    Input("sl-s0",  "value"),
    Input("sl-k",   "value"),
    Input("sl-t",   "value"),
    Input("sl-sg",  "value"),
    State("mc-store", "data"),
    prevent_initial_call=True,
)
def _update(n_iv, S0, K, T, sigma, store):
    try:
        r = _R_FIXED
        params = {"S0": S0, "K": K, "T": T, "sigma": sigma}
        slider_fired = ctx.triggered_id in _SLIDER_IDS

        # ── Interval tick while still in initial state: do nothing ─────────────
        if store["params"] is None and not slider_fired:
            from dash.exceptions import PreventUpdate
            raise PreventUpdate

        # ── First slider move or params changed: reset animation ───────────────
        if store["params"] != params:
            store = {"step": 0, "hist": [], "params": params}

        step = store["step"]
        hist = store["hist"]

        # Black-Scholes (sub-ms, recompute every tick)
        t0 = time.perf_counter()
        bs = black_scholes_call(S0, K, r, sigma, T)
        bs_ms = (time.perf_counter() - t0) * 1000

        # QAE exact key lookup (sliders snap to grid values)
        entry = _qae_lookup(S0, K, T, sigma)
        qp    = entry["price"]   or 0.0
        qe_ms = (entry["elapsed"] or 0.0) * 1000

        # Advance MC animation one step
        if step < len(_N_SCHED):
            N = _N_SCHED[step]
            t1 = time.perf_counter()
            mc_p, mc_err = monte_carlo_call(S0, K, r, sigma, T, N)
            mc_ms = (time.perf_counter() - t1) * 1000
            hist.append({"N": N, "p": mc_p, "lo": mc_p - 1.96 * mc_err,
                         "hi": mc_p + 1.96 * mc_err, "ms": mc_ms})
            store["step"] = step + 1
            store["hist"] = hist

        done = store["step"] >= len(_N_SCHED)
        last = hist[-1] if hist else None

        mc_price_str = f"${last['p']:.4f}" if last else "—"
        mc_ci        = (last["hi"] - last["lo"]) / 2 if last else 0
        mc_meta_str  = f"N = {last['N']:,} · ±{mc_ci:.4f} (95% CI)" if last else "Starting…"

        return (
            store,
            done,
            _mc_fig(hist, bs),
            mc_price_str,
            mc_meta_str,
            f"${bs:.4f}",
            "< 1 ms · exact closed-form",
            f"${qp:.4f}",
            f"{qe_ms:.0f} ms · pre-computed on Qiskit statevector",
            "",
            _scatter_fig(hist, bs, bs_ms, qp, qe_ms),
        )
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print(f"CALLBACK ERROR: {exc}", flush=True)
        raise


# ── Figures ───────────────────────────────────────────────────────────────────

def _mc_fig(hist, bs_price):
    fig = go.Figure(layout=_DARK_LAYOUT)
    if not hist:
        return fig

    Ns  = [h["N"]  for h in hist]
    ps  = [h["p"]  for h in hist]
    los = [h["lo"] for h in hist]
    his = [h["hi"] for h in hist]

    fig.add_trace(go.Scatter(
        x=Ns + Ns[::-1], y=his + los[::-1],
        fill="toself", fillcolor="rgba(245,158,11,0.12)",
        line=dict(color="rgba(0,0,0,0)"), hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=Ns, y=ps,
        line=dict(color=_C_MC, width=2),
        hovertemplate="N=%{x:,}<br>$%{y:.4f}<extra></extra>",
    ))
    fig.add_hline(y=bs_price, line=dict(color=_C_BS, width=1, dash="dot"))
    fig.update_xaxes(type="log")
    return fig


def _scatter_fig(hist, bs_price, bs_ms, qp, qe_ms):
    fig = go.Figure()

    # Black-Scholes — near-zero error, near-zero time
    fig.add_trace(go.Scatter(
        x=[max(bs_ms, 0.05)], y=[5e-5],
        mode="markers+text", text=["Black-Scholes"], textposition="top right",
        marker=dict(color=_C_BS, size=15),
        hovertemplate="Black-Scholes<br>~0 ms · exact<extra></extra>",
        name="Black-Scholes",
    ))

    # Monte Carlo progression
    if hist:
        xs = [max(h["ms"], 1e-3) for h in hist]
        ys = [max(abs(h["p"] - bs_price), 1e-5) for h in hist]
        if len(hist) > 1:
            fig.add_trace(go.Scatter(
                x=xs[:-1], y=ys[:-1], mode="markers",
                marker=dict(color=_C_MC, size=5, opacity=0.25),
                showlegend=False, hoverinfo="skip",
            ))
        fig.add_trace(go.Scatter(
            x=[xs[-1]], y=[ys[-1]],
            mode="markers+text", text=["Monte Carlo"], textposition="top right",
            marker=dict(color=_C_MC, size=15),
            customdata=[hist[-1]["N"]],
            hovertemplate="Monte Carlo<br>N=%{customdata:,}<br>Error: $%{y:.4f}<extra></extra>",
            name="Monte Carlo",
        ))

    # QAE
    fig.add_trace(go.Scatter(
        x=[max(qe_ms, 0.1)], y=[max(abs(qp - bs_price), 1e-5)],
        mode="markers+text", text=["QAE"], textposition="top right",
        marker=dict(color=_C_QA, size=15, symbol="diamond"),
        hovertemplate="QAE (pre-computed)<br>Time: %{x:.0f} ms<br>Error: $%{y:.4f}<extra></extra>",
        name="Quantum (QAE)",
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text="Accuracy vs Compute Time", font=dict(size=15), x=0.5),
        xaxis=dict(type="log", title="Compute Time (ms)",
                   gridcolor="rgba(255,255,255,0.07)"),
        yaxis=dict(type="log", title="Error vs Black-Scholes ($)",
                   gridcolor="rgba(255,255,255,0.07)"),
        margin=dict(l=70, r=20, t=55, b=55),
        height=360,
        legend=dict(x=0.01, y=0.01, bgcolor="rgba(0,0,0,0.4)"),
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
