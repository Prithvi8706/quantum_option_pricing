# Product

## Register

product

## Users

Quant researchers and CS practitioners who already know what Black-Scholes, Monte Carlo, and QAE mean. They come to the tool to watch the algorithms compete — not to be introduced to them. Secondary audience: hiring managers and technical reviewers following a GitHub link; they may lack domain depth but can read a chart and judge signal from noise.

## Product Purpose

An interactive dashboard that prices European call options using three methods and makes their accuracy-vs-compute tradeoffs visible in real time. Sliders drive live recomputation; the Monte Carlo result animates through 15 sample sizes so the O(1/√N) convergence is observable. QAE results load from a precomputed grid. Black-Scholes is the accuracy reference. Success: a quant researcher adjusts parameters and immediately reads whether QAE or MC is closer to the closed-form price at their chosen inputs, and why the break-even point shifts.

## Brand Personality

Rigorous · Precise · Honest

The tool does not oversell quantum computing. The README explicitly names the limitations (statevector simulator, NISQ overhead). The visual language should carry that same intellectual honesty: no decorative flourishes that imply more than the math delivers.

## Anti-references

- Generic SaaS dashboard: colorful metric cards with gradient accents, rounded-everything cards, Vercel-marketing-page energy. This is a technical tool, not a no-code product.
- Dark-mode cliché: neon glow, purple gradients, glassmorphism, every-AI-startup-2024 look. The dark background exists because it reduces eye strain during data analysis and makes chart colors pop, not as aesthetic theater.

## Design Principles

1. **Data over decoration.** The Plotly charts are the product. Every visual decision should make the charts more readable, not compete with them.
2. **Honest signals only.** No visual element should imply higher precision or speed than the underlying algorithm delivers. No decorative status badges, no fake "live" indicators.
3. **Earned familiarity.** Use the vocabulary quant researchers already know from their tools. Standard controls, predictable layout, no invented affordances.
4. **Show, don't sell.** Labels describe what a parameter is. Copy describes what the result means. Nothing is written to impress; everything is written to inform.
5. **Portfolio-grade finish within product constraints.** The dark theme, method color coding, and chart quality already signal care. Polish comes from fixing contrast, spacing rhythm, and responsive behavior — not from decorative additions.

## Accessibility & Inclusion

WCAG AA: 4.5:1 minimum contrast on all body and label text. Keyboard navigation for sliders. Screen reader labels on Plotly figures where Dash permits. No accessibility accommodations beyond the AA baseline were specified.
