"""
Build a self-contained REVIEW PDF of Paper A via an HTML rendering that Chrome
prints to PDF. This is a readable review copy (single-column, figures embedded),
NOT the Springer-typeset PDF — that comes from compiling main.tex on Overleaf.

Steps: read the 4 figures -> base64-embed into an HTML file -> return the html
path. The caller then runs Chrome --headless --print-to-pdf on it.
"""
import os
import base64

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figures")


def img(name):
    with open(os.path.join(FIG, name), "rb") as f:
        b = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b}"


HTML = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Paper A — Review PDF</title>
<style>
@page {{ size: A4; margin: 2cm; }}
body {{ font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt;
        line-height: 1.5; color: #111; text-align: justify; }}
h1 {{ font-size: 16pt; text-align: center; margin: 0 0 4px; line-height: 1.3; }}
.author {{ text-align: center; font-size: 11pt; margin: 6px 0 2px; }}
.affil {{ text-align: center; font-size: 10pt; color: #333; margin-bottom: 18px; }}
h2 {{ font-size: 12pt; border-bottom: 1px solid #ccc; padding-bottom: 2px;
      margin-top: 20px; }}
h3 {{ font-size: 10.8pt; margin-top: 14px; }}
.abstract {{ font-size: 9.8pt; background: #f7f7f7; border: 1px solid #e0e0e0;
             padding: 10px 14px; margin: 0 0 6px; }}
.abstract b {{ font-variant: small-caps; }}
.kw {{ font-size: 9.5pt; margin-bottom: 6px; }}
figure {{ break-inside: avoid; text-align: center; margin: 14px 0; }}
figure img {{ max-width: 100%; }}
figcaption {{ font-size: 8.8pt; color: #333; text-align: justify; margin-top: 4px; }}
table {{ border-collapse: collapse; margin: 12px auto; font-size: 9.5pt; }}
th, td {{ border: 1px solid #999; padding: 4px 10px; text-align: center; }}
th {{ background: #eee; }}
.tabcap {{ font-size: 8.8pt; text-align: center; color: #333; margin-bottom: 8px; }}
ol.contrib {{ margin: 4px 0 4px 18px; }}
.refs {{ font-size: 9pt; }}
.refs li {{ margin-bottom: 3px; }}
.note {{ font-size: 8.5pt; color: #b00; text-align: center; border: 1px dashed #b00;
         padding: 5px; margin-bottom: 14px; }}
p {{ margin: 6px 0; }}
</style></head><body>

<div class="note">REVIEW RENDERING (HTML&rarr;PDF). Content and figures are final;
the Springer-typeset layout comes from compiling <code>main.tex</code> on Overleaf.</div>

<h1>NISQ Noise Shifts the Quantum Amplitude Estimation<br>Break-Even for Option Pricing</h1>
<div class="author">Prithvi Raghu</div>
<div class="affil">Vellore Institute of Technology, Vellore, India &middot; prithviraghu080706@gmail.com</div>

<div class="abstract">
<b>Abstract.</b> Quantum amplitude estimation (QAE) is widely cited as offering a
quadratic speedup over classical Monte Carlo for derivative pricing, with the
canonical break-even occurring when the QAE oracle-query budget <i>M</i> falls
below the classical sample budget <i>N</i>. Nearly all such analyses assume
noiseless quantum hardware. We quantify how realistic depolarizing noise degrades
QAE-based European call pricing across a 50-point parameter sweep at five noise
levels (<i>p</i> &isin; {{0, 10<sup>&minus;4</sup>, 10<sup>&minus;3</sup>,
5&times;10<sup>&minus;3</sup>, 10<sup>&minus;2</sup>}}) using iterative QAE (IQAE)
with three uncertainty qubits on a depolarizing-noise simulator, validated against
a single-qubit state-preparation run on IBM hardware (ibm_marrakesh). We report
three findings. First, at the current IBM hardware noise level (<i>p</i> &approx;
10<sup>&minus;3</sup>) the mean absolute price error is $0.657 &mdash; roughly
66&times; the &epsilon; = 0.01 precision target that defines the theoretical
break-even. Second, and more strikingly, even at <i>p</i> = 0 the mean error is
$0.203, already &approx;20&times; above target: the three-qubit discretization
imposes an irreducible approximation error before any noise is introduced, so the
asymptotic advantage is unattainable on near-term devices regardless of noise.
Third, the IQAE oracle-query depth is noise-invariant at &approx;14 queries across
all <i>p</i>, because the amplitude-based stopping rule is blind to noise &mdash;
the query budget never inflates; accuracy simply decays silently. Together these
results show that the QAE break-even, evaluated under near-term conditions, sits
entirely inside the regime where QAE provides no usable advantage.
</div>
<div class="kw"><b>Keywords:</b> Quantum amplitude estimation &middot; Option
pricing &middot; NISQ &middot; Depolarizing noise &middot; Quantum finance
&middot; Break-even analysis</div>

<h2>1&nbsp;&nbsp;Introduction</h2>
<p>Monte Carlo (MC) simulation is the workhorse of derivative pricing. Its central
limitation is well known: the statistical error of an MC price estimate decays as
O(1/&radic;<i>N</i>) in the number of sample paths <i>N</i>, so halving the error
requires quadrupling the computational budget. Quantum amplitude estimation (QAE)
is the most frequently cited quantum remedy. By encoding the discounted payoff into
the amplitude of a marked quantum state and applying amplitude estimation, QAE
estimates the expectation with error decaying as O(1/<i>M</i>) in the number of
oracle queries <i>M</i> &mdash; a quadratic improvement in the convergence
exponent. This scaling underpins the widely reproduced claim that quantum computers
will price options faster than classical machines once a break-even query budget is
reached.</p>
<p>The break-even argument is almost always made in an idealized setting: perfect
qubits, no decoherence, and an oracle whose cost is counted in abstract query units
rather than transpiled physical gates. Real near-term (NISQ) devices satisfy none
of these assumptions. The question this paper addresses is concrete: when the
standard QAE option-pricing pipeline is run under realistic depolarizing noise at
current hardware error rates, where does the break-even actually land?</p>
<p>We answer this empirically. Using iterative QAE (IQAE) with three uncertainty
qubits &mdash; a configuration representative of the small instances that fit on
present hardware &mdash; we price a European call across a 50-point parameter sweep
and repeat the experiment at five depolarizing-noise levels spanning the noiseless
ideal through an order of magnitude above current hardware. We complement the
simulation with a single-qubit state-preparation circuit executed on IBM's
ibm_marrakesh device to confirm that the simulator's noise behavior is
representative of real hardware at the smallest scale. The contributions are:</p>
<ol class="contrib">
<li>a quantified noise-versus-error frontier for QAE option pricing showing the
break-even lies entirely within the no-advantage regime at NISQ noise rates;</li>
<li>the observation that the three-qubit discretization alone already pushes the
error &approx;20&times; above the precision target before noise is added; and</li>
<li>the finding that IQAE's oracle-query depth is noise-invariant, so noise
corrupts the answer without ever signaling increased cost.</li>
</ol>

<h2>2&nbsp;&nbsp;Background and Related Work</h2>
<h3>2.1&nbsp;&nbsp;QAE for Option Pricing</h3>
<p>The standard QAE pricing pipeline, established by Stamatopoulos et al. [1]
building on Woerner and Egger [2], proceeds in three stages. A state-preparation
operator loads the discretized risk-neutral distribution of the underlying asset
onto a register of <i>n</i> uncertainty qubits, producing 2<sup><i>n</i></sup>
discretization points. A payoff operator rotates an ancilla so that the probability
of measuring it in the |1&rang; state equals the (rescaled) discounted expected
payoff. Amplitude estimation then extracts that probability to precision
&epsilon; using O(1/&epsilon;) oracle queries, versus the O(1/&epsilon;<sup>2</sup>)
samples a classical estimator requires for the same precision.</p>
<p>Two costs are routinely understated in this framing. The first is
discretization: with <i>n</i> uncertainty qubits the distribution is represented at
only 2<sup><i>n</i></sup> points, introducing a bias that is independent of &mdash;
and additive to &mdash; the estimation error &epsilon;. The second is the gap
between an abstract &ldquo;oracle query&rdquo; and the physical gate sequence that
implements it after transpilation to a device's native gate set. Both costs are
central to our results.</p>
<h3>2.2&nbsp;&nbsp;Noise in Near-Term Devices</h3>
<p>NISQ hardware is characterized by gate error rates that, for two-qubit gates,
currently sit near 10<sup>&minus;3</sup> on leading superconducting devices. We
model this with the depolarizing channel, the standard worst-case-agnostic noise
model, applying single-qubit depolarizing error of rate <i>p</i> to the native
one-qubit gates and two-qubit depolarizing error of rate <i>p</i> to the entangling
(CX) gates. This isolates the effect of gate noise from idling and readout effects
and lets us sweep a single physical parameter.</p>

<h2>3&nbsp;&nbsp;Methodology</h2>
<h3>3.1&nbsp;&nbsp;Experimental Configuration</h3>
<p>We price European call options using IQAE with <i>n</i> = 3 uncertainty qubits.
The risk-neutral distribution is a log-normal loaded via a standard
state-preparation routine; the payoff is the truncated call payoff
max(<i>S</i>&minus;<i>K</i>, 0) rescaled into [0, 1]. Estimation uses the iterative
amplitude-estimation algorithm of Grinko et al. [3], which avoids the expensive
quantum phase-estimation register and is the practical choice for NISQ-scale
instances. The classical reference price is the closed-form Black&ndash;Scholes
value; the error metric throughout is the absolute price deviation
|&Delta;| = |price<sub>QAE</sub> &minus; price<sub>BS</sub>| in dollars.</p>
<h3>3.2&nbsp;&nbsp;Validation Gate</h3>
<p>Before running any noise experiments we established a Phase-0 validation gate.
The IQAE circuit is transpiled to the simulator's native gate set and run at
<i>p</i> = 0 against a precomputed price grid. The transpiled circuit expands from 2
high-level building blocks to 73 native gates &mdash; an early and quantitative
illustration of the oracle-cost gap discussed in Section 2.1. The validation run
returned a deviation of &delta; = 0.0048 against the grid, comfortably inside the
pass threshold, confirming the pipeline is correct before noise is introduced.</p>
<h3>3.3&nbsp;&nbsp;Noise Sweep</h3>
<p>The main experiment is a 50-point parameter sweep (fixed random seed for
reproducibility) repeated at five depolarizing-noise levels <i>p</i> &isin; {{0,
10<sup>&minus;4</sup>, 10<sup>&minus;3</sup>, 5&times;10<sup>&minus;3</sup>,
10<sup>&minus;2</sup>}}, for 250 IQAE runs in total. All 50 parameter points were
resolved by IQAE without any classical fallback. For each run we record the
absolute price error and the oracle-query count, computed as the sum over IQAE
powers of (2<i>k</i> + 1).</p>
<h3>3.4&nbsp;&nbsp;Hardware Validation</h3>
<p>To confirm the simulator's noise model is representative of real hardware, we
executed a minimal single-qubit state-preparation primitive &mdash; an
R<sub>y</sub>(2&middot;arcsin&radic;0.3) rotation encoding a benchmark amplitude of
<i>p</i> = 0.30, followed by measurement &mdash; on IBM's ibm_marrakesh device
(156-qubit Heron r2) with 1024 shots. This isolates the amplitude-encoding step
that underlies the full pipeline and validates it against a value with an exact
closed form, free of the multi-qubit confounds that would make a larger circuit's
deviation hard to attribute.</p>

<h2>4&nbsp;&nbsp;Results</h2>
<h3>4.1&nbsp;&nbsp;Noise Degrades Price Accuracy Far Beyond the Precision Target</h3>
<p>Table 1 reports the mean absolute price error at each noise level. The headline
numbers are stark. At the noiseless ideal (<i>p</i> = 0) the mean error is already
$0.203 &mdash; about 20&times; the &epsilon; = 0.01 precision target. At
<i>p</i> &approx; 10<sup>&minus;3</sup>, representative of current IBM hardware, the
error rises to $0.657, roughly 66&times; the target and 3.2&times; worse than the
ideal. At an order of magnitude above current hardware (<i>p</i> =
10<sup>&minus;2</sup>) the error reaches $6.163, some 30&times; the ideal. The full
per-configuration grid is shown in Fig. 1, and the aggregate mean with its min&ndash;max
band in Fig. 2.</p>

<div class="tabcap"><b>Table 1.</b> Mean absolute price error versus depolarizing
noise rate, over the 50-point parameter sweep. Values recomputed directly from the
run data.</div>
<table>
<tr><th>Noise rate <i>p</i></th><th>Mean |&Delta;| ($)</th>
<th>Multiple of &epsilon;=0.01 target</th><th>Mean oracle queries</th></tr>
<tr><td>0 (ideal)</td><td>0.203</td><td>20&times;</td><td>14.5</td></tr>
<tr><td>10<sup>&minus;4</sup></td><td>0.220</td><td>22&times;</td><td>13.6</td></tr>
<tr><td>10<sup>&minus;3</sup> (current IBM)</td><td>0.657</td><td>66&times;</td><td>14.5</td></tr>
<tr><td>5&times;10<sup>&minus;3</sup></td><td>3.478</td><td>348&times;</td><td>13.7</td></tr>
<tr><td>10<sup>&minus;2</sup></td><td>6.163</td><td>616&times;</td><td>13.7</td></tr>
</table>

<figure><img src="{img('fig_noise_heatmap.png')}">
<figcaption><b>Fig. 1.</b> Absolute price error across ten option configurations and
five noise levels. The colorscale is capped at $8 for visibility; configuration P5
(deep in-the-money, S<sub>0</sub> = 120) is the principal outlier, reaching $19.0 at
<i>p</i> = 10<sup>&minus;2</sup>. Errors exceed the &epsilon; = 0.01 break-even
threshold at every cell in the grid.</figcaption></figure>

<figure><img src="{img('fig_mean_delta_vs_noise.png')}" style="max-width:80%">
<figcaption><b>Fig. 2.</b> Mean absolute price error versus depolarizing noise rate
(log&ndash;log), with the min&ndash;max band across the sweep. The dashed lines mark
the &epsilon; = 0.01 precision target and the current IBM hardware noise level
(<i>p</i> &approx; 10<sup>&minus;3</sup>).</figcaption></figure>

<h3>4.2&nbsp;&nbsp;The Discretization Floor</h3>
<p>The most consequential result is the <i>p</i> = 0 value. That a noiseless
simulation already misses the precision target by a factor of 20 shows the dominant
error source at this scale is not decoherence but discretization. With <i>n</i> = 3
uncertainty qubits the risk-neutral distribution is represented at only eight
points, and the resulting bias is irreducible: no improvement in qubit quality
removes it. Noise then compounds an error that was already disqualifying. The
practical implication is that the theoretical break-even, which presumes the
estimation error &epsilon; is the only error, is inapplicable to instances small
enough to run on near-term hardware &mdash; the advantage was lost to discretization
before noise entered.</p>

<h3>4.3&nbsp;&nbsp;Oracle-Query Depth Is Noise-Invariant</h3>
<p>Figure 3 (right panel) reports the mean oracle-query count as a function of noise
rate. It is essentially flat at &approx;14 queries (range 13.6&ndash;14.5) across
all five noise levels. This follows from the structure of IQAE: its stopping
criterion is amplitude-based and contains no term sensitive to noise, so the
algorithm terminates at the same iteration depth regardless of <i>p</i>. The
consequence is operationally important &mdash; the query budget, the quantity the
break-even analysis tracks, does not inflate under noise. Instead the estimate the
algorithm returns at that fixed depth becomes progressively more corrupted. Noise
manifests as silent accuracy loss, not as visibly increased cost, which is precisely
the failure mode a budget-based break-even analysis cannot detect.</p>

<figure><img src="{img('fig_break_even_frontier.png')}">
<figcaption><b>Fig. 3.</b> Left: the break-even frontier (mean price error versus
noise rate) lies entirely within the region where QAE's advantage is lost &mdash;
the whole curve sits above the &epsilon; = 0.01 target across the swept noise range.
Right: mean oracle-query depth is noise-invariant at &approx;14 queries, with the
&plusmn;1 standard-deviation band, confirming the query budget does not respond to
noise.</figcaption></figure>

<h3>4.4&nbsp;&nbsp;Hardware Validation</h3>
<p>The single-qubit state-preparation run on ibm_marrakesh (Fig. 4) returned an
empirical estimate of p&#770; = 0.2842 against the encoded target of 0.3000 &mdash;
an absolute error of 0.0158. For 1024 shots the binomial sampling standard deviation
at <i>p</i> = 0.3 is &sigma; &approx; 0.0143, so the hardware deviation is
1.1&sigma;, within the shot-noise band. A matched noiseless simulator draw (seed 42)
gave p&#770; = 0.2754 (1.7&sigma;). In other words, for this minimal
state-preparation primitive, gate noise on real hardware is negligible relative to
sampling noise: the device behaves like the ideal simulator at this scale. This is
the appropriate validation claim &mdash; it confirms the amplitude-encoding step is
faithful on hardware, while the full-pipeline degradation reported above arises from
circuit depth and discretization, which a one-qubit primitive does not exercise.</p>

<figure><img src="{img('hardware_validation_plot.png')}" style="max-width:75%">
<figcaption><b>Fig. 4.</b> Hardware validation as deviation from theory. Both the
ibm_marrakesh hardware estimate (|err| = 0.0158, 1.1&sigma;) and a matched simulator
draw (|err| = 0.0246, 1.7&sigma;) fall within the &plusmn;1&sigma; shot-noise band
(&sigma; = 0.0143) around the theoretical <i>p</i> = 0.30. Job ID
d8nvd2bqv2lc7389d9e0, 1024 shots.</figcaption></figure>

<h2>5&nbsp;&nbsp;Discussion</h2>
<p>The results are best read as a separation of error sources. At NISQ scale the
total QAE pricing error decomposes into a discretization floor set by the number of
uncertainty qubits and a noise-dependent term that grows with the depolarizing rate.
Our sweep shows the floor alone is already 20&times; above the precision target, and
the noise term overtakes even the floor by <i>p</i> = 5&times;10<sup>&minus;3</sup>.
Increasing <i>n</i> to lower the floor multiplies circuit depth and therefore the
accumulated noise, so the two error sources cannot be reduced independently on
near-term hardware.</p>
<p>This reframes the break-even question. The canonical analysis asks at what query
budget <i>M</i> the O(1/<i>M</i>) quantum estimator overtakes the
O(1/&radic;<i>N</i>) classical one, holding the target precision &epsilon; fixed and
assuming &epsilon; is the only error. Our data show that on hardware small enough to
run, &epsilon; is not the only error and is not even the dominant one. A
budget-based crossover computed under the noiseless assumption therefore describes a
regime that current devices cannot enter.</p>
<p>The noise-invariance of the oracle-query depth sharpens this point. Because IQAE
does not lengthen its query schedule under noise, a practitioner monitoring only the
query budget would observe the algorithm terminating on schedule and reporting a
confident estimate, with no indication that the estimate has drifted by dollars. Any
honest break-even accounting must track delivered accuracy, not query count, under
realistic noise.</p>
<p><b>Limitations.</b> The depolarizing model omits idling, crosstalk, and readout
error, and the hardware validation exercises only the single-qubit encoding step
rather than the full transpiled pipeline; a full-circuit hardware run is the natural
next step but is beyond the open-plan runtime budget used here. The instances
studied are deliberately small (<i>n</i> = 3), matching what near-term hardware can
execute; the discretization floor we identify would recede at larger <i>n</i> on
fault-tolerant hardware, where this paper's near-term conclusions no longer apply.</p>

<h2>6&nbsp;&nbsp;Conclusion</h2>
<p>We have measured, rather than assumed, the conditions under which QAE prices
European options accurately on near-term hardware. Under realistic depolarizing
noise the mean price error exceeds the &epsilon; = 0.01 precision target by 66&times;
at current IBM error rates, and by 20&times; even with no noise at all, because the
three-qubit discretization imposes an irreducible floor. The oracle-query depth that
the break-even analysis tracks is noise-invariant, so the cost metric gives no
warning as accuracy decays. A single-qubit run on ibm_marrakesh confirms the
amplitude-encoding step is faithful to within shot noise, locating the degradation
in depth and discretization rather than the encoding itself. The practical
conclusion is that the QAE option-pricing break-even, evaluated under near-term
conditions, lies entirely within the regime where QAE offers no usable advantage
&mdash; a finding that motivates comparison against variance-reduced classical
estimators, which we take up in companion work.</p>

<h2>References</h2>
<ol class="refs">
<li>Stamatopoulos, N., Egger, D.J., Sun, Y., Zoufal, C., Iten, R., Shen, N.,
Woerner, S.: Option pricing using quantum computers. Quantum 4, 291 (2020)</li>
<li>Woerner, S., Egger, D.J.: Quantum risk analysis. npj Quantum Information 5(1),
15 (2019)</li>
<li>Grinko, D., Gacon, J., Zoufal, C., Woerner, S.: Iterative quantum amplitude
estimation. npj Quantum Information 7(1), 52 (2021)</li>
<li>Brassard, G., H&oslash;yer, P., Mosca, M., Tapp, A.: Quantum amplitude
amplification and estimation. Contemporary Mathematics 305, 53&ndash;74 (2002)</li>
<li>Montanaro, A.: Quantum speedup of Monte Carlo methods. Proceedings of the Royal
Society A 471(2181), 20150301 (2015)</li>
<li>Rebentrost, P., Gupt, B., Bromley, T.R.: Quantum computational finance: Monte
Carlo pricing of financial derivatives. Physical Review A 98(2), 022321 (2018)</li>
<li>Preskill, J.: Quantum computing in the NISQ era and beyond. Quantum 2, 79
(2018)</li>
<li>Qiskit contributors: Qiskit: An open-source framework for quantum computing
(2024)</li>
</ol>

</body></html>
"""

out = os.path.join(HERE, "Paper_A_review.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)
print(out)
