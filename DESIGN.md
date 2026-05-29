---
name: Quantum Option Pricing
description: Three option-pricing methods benchmarked side by side — Black-Scholes, Monte Carlo, QAE.
colors:
  bg: "#0a0e1a"
  card: "#111827"
  border-subtle: "rgba(255,255,255,0.07)"
  text-primary: "#e5e7eb"
  text-secondary: "#9ca3af"
  formula-green: "#22c55e"
  simulation-amber: "#f59e0b"
  quantum-indigo: "#818cf8"
  warning-amber: "#fbbf24"
typography:
  display:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "2.1rem"
    fontWeight: 800
    letterSpacing: "-0.02em"
  data:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "2.1rem"
    fontWeight: 700
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 500
  label:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 700
    letterSpacing: "0.1em"
  caption:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 500
rounded:
  surface: "14px"
  focus: "3px"
spacing:
  xs: "6px"
  sm: "10px"
  md: "16px"
  lg: "20px"
  xl: "28px"
  section: "36px"
components:
  card-primary:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.surface}"
    padding: "22px 20px 16px"
  card-bs:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.surface}"
    padding: "22px 20px 16px"
  card-mc:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.surface}"
    padding: "22px 20px 16px"
  card-qae:
    backgroundColor: "{colors.card}"
    rounded: "{rounded.surface}"
    padding: "22px 20px 16px"
  link-muted:
    textColor: "{colors.text-secondary}"
  link-accent:
    textColor: "{colors.quantum-indigo}"
---

# Design System: Quantum Option Pricing

## 1. Overview

**Creative North Star: "The Rigorous Witness"**

The Rigorous Witness observes algorithms without editorializing. It shows what Black-Scholes, Monte Carlo, and Quantum Amplitude Estimation compute — exactly as computed, with their error bars, their timing, their honest limitations. The visual language is a direct extension of the README's intellectual honesty: no gradient implies more than the numbers deliver, no flourish oversells a 600-point precomputed grid as live quantum hardware.

The system is dark because quant researchers work in low ambient light, staring at terminals and notebooks. The background (`#0a0e1a`) is deep navy with a trace of blue — not arbitrary black, not a generic "cool dark." Card surfaces (`#111827`) lift one tonal step from the background, and hairline white-alpha borders mark container edges without adding visual noise. No shadows. The chart is the depth.

Three method identity colors carry the entire chromatic load: Formula Green for Black-Scholes (the exact closed-form answer), Simulation Amber for Monte Carlo (the stochastic convergence path), Quantum Indigo for QAE (the quantum algorithm result, and the tool's global accent). Outside those three and the structural neutrals, nothing is colored. This system explicitly rejects generic SaaS dashboard aesthetics — colorful metric cards with gradient accents — and the dark-mode cliché of 2024: neon glow, purple gradients, glassmorphism.

**Key Characteristics:**
- Three-color method vocabulary, used exclusively for method identity — never decoration
- Flat surfaces, hairline borders, zero shadows — the chart is the only depth
- Single sans family (Inter), two weights (800 display / 700 data and labels)
- Uppercase text reserved for method identifiers and the parameters panel label only
- All numeric displays use tabular-nums for column alignment under changing values

## 2. Colors: The Rigorous Witness Palette

A minimal dark palette with three precisely assigned identity colors. The neutrals handle structure; the three method colors handle meaning.

### Primary
- **Quantum Indigo** (`#818cf8`): The QAE method's identity color and the tool's sole global accent. Used on the QAE card price, the slider thumb and fill, focus rings, and the QAE chart trace. Its violet hue distinguishes the quantum method from the classical two without reference to any other domain.

### Secondary
- **Formula Green** (`#22c55e`): Black-Scholes identity color. Used on the BS card price, the BS chart trace, and the top border of the BS card. Green signals correctness and the closed-form reference value — every other method's accuracy is measured against it.
- **Simulation Amber** (`#f59e0b`): Monte Carlo identity color. Used on the MC card price, the MC convergence chart, and the MC card border. Amber communicates variance and uncertainty without implying error.

### Neutral
- **Night Console** (`#0a0e1a`): Page background. Deep navy with a trace of blue — not pure black, not generic charcoal.
- **Working Panel** (`#111827`): Card and container surface. One tonal step above the background; the only elevation mechanism.
- **Border Hairline** (`rgba(255,255,255,0.07)`): Container outlines. Present enough to define the edge; absent enough to not compete with chart content.
- **Primary Ink** (`#e5e7eb`): Body text and primary UI values.
- **Secondary Ink** (`#9ca3af`): Labels, metadata, slider marks, footer, citations. ≥7.5:1 contrast on both `--bg` and `--card`.
- **Warning Amber** (`#fbbf24`): QAE snap notes only ("Nearest match used: σ=0.20"). Not a decoration color; a functional signal that the lookup grid snapped to a neighbor.

### Named Rules
**The Three Witnesses Rule.** Formula Green, Simulation Amber, and Quantum Indigo are reserved for method identity. Never repurpose them for hover states, decorative borders, or UI elements that don't directly represent one of the three pricing methods.

**The Contrast Floor Rule.** Secondary Ink (`#9ca3af`) is the lightest text color in the system. It must not be made lighter. It was deliberately chosen to pass WCAG AA (≥4.5:1) on both surface tones; `#6b7280` — its predecessor — failed that bar at 4.0:1.

## 3. Typography

**Body / UI Font:** Inter (with `system-ui, -apple-system, sans-serif` fallback)

One family, two weights, consistent scale. Inter's geometric sans construction reads precisely at small sizes — essential for the 0.7rem–0.75rem label layer where this UI spends most of its text budget. No display font is needed; the price numbers at 2.1rem / 800 weight carry enough visual presence on their own.

### Hierarchy
- **Display** (800, 2.1rem, -0.02em): Page title ("Quantum Option Pricing"). One instance. The only element that announces the tool.
- **Data** (700, 2.1rem, -0.02em, tabular-nums): Price output values on method cards. Same scale as display, distinct weight; tabular-nums keeps decimal columns stable during animation.
- **Body** (500, 0.85rem): Fixed-rate display, general UI prose. Line length does not apply here — the UI is dense by design.
- **Label** (700, 0.72rem, 0.1em, uppercase): Method identifiers ("BLACK-SCHOLES", "MONTE CARLO", "QUANTUM (QAE)") and the parameters panel label ("PARAMETERS"). Short uppercase labels only.
- **Caption** (500, 0.75–0.78rem): Slider labels, meta text, footer text, citation text. Color: Secondary Ink.

### Named Rules
**The Uppercase Restriction Rule.** Uppercase text appears in exactly two contexts: method name labels on cards and the parameters panel header. It is a naming convention for named system components, not a general label treatment. Any new uppercase text must serve the same "identifying a named thing" function.

**The Tabular-Nums Rule.** Every numeric value that changes at runtime — prices, confidence intervals, N counts, oracle queries — must use `font-variant-numeric: tabular-nums`. Proportional digits cause layout shift as values animate.

## 4. Elevation

This system is flat by design. No `box-shadow` values exist anywhere. Depth is conveyed through two mechanisms only: tonal difference between the page background (`#0a0e1a`) and card surfaces (`#111827`), and hairline white-alpha borders (`rgba(255,255,255,0.07)`) that mark container edges. The chart content is the only "raised" element, and it earns its prominence through visual complexity, not shadow.

### Named Rules
**The No-Shadow Rule.** Shadows are prohibited on all surfaces — cards, containers, inputs, buttons. Adding `box-shadow` to any element would immediately read as generic SaaS decoration, which is PRODUCT.md's primary anti-reference. Depth is structural. If a new component needs to feel elevated, increase the surface tonal step — do not add a shadow.

## 5. Components

### Method Cards
The defining component of this interface. Three cards sit in a row, each representing one pricing method. They share structure; their identity comes from the top border and the price color.

- **Corner Style:** Gently curved (14px radius) — firm, not playful
- **Background:** Working Panel (`#111827`)
- **Border:** 1px hairline (`rgba(255,255,255,0.07)`)
- **Top Accent Border:** 3px solid, method color — the only colored border in the system. Formula Green for BS, Simulation Amber for MC, Quantum Indigo for QAE
- **Shadow:** None (No-Shadow Rule)
- **Internal Padding:** 22px top, 20px horizontal, 16px bottom — the asymmetry grounds the card visually
- **Price Value:** 2.1rem, 700 weight, method color, tabular-nums

### Chart Containers
Same structural shape as method cards (14px radius, hairline border, `--card` background). Lighter internal padding (6px). The chart itself provides all visual content; the container is a neutral frame.

### Sliders (Dash/RC-Slider)
- **Track:** `rgba(255,255,255,0.10)` — barely visible; the track is not the focus
- **Range Fill:** Quantum Indigo at 45% opacity (`rgba(129,140,248,0.45)`)
- **Thumb:** Quantum Indigo solid (`#818cf8`) — the most saturated CSS element on the page outside chart traces
- **Tick Labels:** `#cbd5e1` — one step brighter than Secondary Ink for the numeric marks

### Links
- **Muted (footer):** Secondary Ink (`#9ca3af`), transitions to Primary Ink (`#e5e7eb`) on hover, 150ms ease
- **Accent (citations):** Quantum Indigo (`#818cf8`), transitions to Primary Ink with underline on hover, 150ms ease
- **Focus:** 2px Quantum Indigo outline, 2px offset, 3px radius

### Sidebar
Same structural shape as a method card but full-width on mobile. Contains the parameter control set. Header label ("PARAMETERS") uses the label style — uppercase, Secondary Ink, 0.72rem, 700 weight.

## 6. Do's and Don'ts

### Do:
- **Do** use Formula Green, Simulation Amber, and Quantum Indigo exclusively for their respective method contexts. The Three Witnesses Rule is absolute.
- **Do** use Secondary Ink (`#9ca3af`) for all secondary text — labels, metadata, captions. Never drop below this value; it sits exactly at the WCAG AA floor on both surfaces.
- **Do** use `font-variant-numeric: tabular-nums` on all price outputs, confidence intervals, and numeric values that animate.
- **Do** keep containers flat: `border: 1px solid rgba(255,255,255,0.07)`, no `box-shadow`. The No-Shadow Rule applies universally.
- **Do** use `text-wrap: balance` on any headline that could wrap, and `transition: color 150ms ease` on any link that changes color on hover.
- **Do** cite WCAG AA (4.5:1) as the hard floor for any text color on any surface. The contrast fix from `#6b7280` to `#9ca3af` was non-optional.

### Don't:
- **Don't** use `background-clip: text` with a gradient. The title's original gradient was removed precisely because it is theatrical, not honest. The Rigorous Witness has no use for decorative text effects.
- **Don't** add `box-shadow` to any card, container, or interactive element. The No-Shadow Rule exists because shadows read immediately as generic SaaS decoration — PRODUCT.md's primary anti-reference.
- **Don't** apply glassmorphism (`backdrop-filter`, blurred card backgrounds). The system is flat by design; glass is the opposite of honest structural depth.
- **Don't** use colorful metric cards with gradient accents. This is the "generic SaaS dashboard" PRODUCT.md explicitly names as what this tool must not look like.
- **Don't** use neon glow, ambient Quantum Indigo lighting, or purple gradients. Quantum Indigo is a precise method identifier. Using it as an ambient glow converts a rigorous signal into dark-mode cliché decoration.
- **Don't** add uppercase text to any element that isn't a method name or a named system label. The Uppercase Restriction Rule is not a typographic preference; it is a scope limit.
- **Don't** introduce a second typeface. One family with weight contrast reads as precise. Two competing sans-serifs read as indecision.
