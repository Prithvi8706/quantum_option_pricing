# L2 venue screen: verified conformance checklist

Date: 1 October 2026. All official pages below were accessed on 1 October 2026.

Prepared by Claude Code (an AI agent) at the author's request. This is agent work. The author has not
verified it yet, and it is not external review.

Paper: *What quadratic quantum speedups would need to beat strong classical option pricing: a measured
requirements frontier* (VIT Vellore). The verdict is fixed: no defensible significant quantum advantage
has been established yet.

**The venue decision belongs to the author.** This file recommends, and the author decides. Under
IMPLEMENTATION_PLAN.md (Day 2), the author records the choice in VENUE.md.

---

## 1. What was checked, and how

The input was `l2_venues.jsonl`, which has 13 venue records written by a search agent that stopped
before it finished. For each venue, this pass re-opened the publisher's own pages for scope, AI and
authorship policy, preprint and arXiv policy, fees and waivers, length and format, required statements,
and review time. Each record was confirmed, corrected, or marked unknown where the official page says
nothing. The audit trail is `l2_verification.jsonl`, with one line per venue holding the confirmed fields,
corrections, a paraphrase of the AI policy, official URLs and the access date.

Most pages were read with a web fetcher. Some sites refuse automated fetches: the ACM Digital Library,
acm.org, epubs.siam.org, risk.net, tandfonline.com and link.springer.com. Those were read as rendered
pages in the desktop browser pane. One ACM page first showed a bot-verification screen. It was not
bypassed. It loaded normally on a later visit. Two earlier gaps are now closed: the ACM TQC and SIAM
SIFIN pages, which the first agent could see only as search snippets, were read in full.

Limits. Publisher policies change. Every figure here is as of 1 October 2026 and must be checked again
on submission day. Logged-in submission forms were not seen. Where a fact rests on an inference, such as
India's World Bank income class for FY27, the table says so.

---

## 2. Short answers to the four questions

**Is a negative or requirements result in scope?** None of the 13 venues says anything explicit about
negative results. For the quantum journals the topic is clearly in scope. The finance threshold paper by
Chakrabarti et al. appeared in *Quantum* 5:463 (2021), and Manzano et al. (2025) appeared in EPJ Quantum
Technology. What differs is the significance bar:

- **High bar.** Quantum rules out correct but incremental work on a limited technique. PRX Quantum
  requires exceptional achievement. npj Quantum Information, Quantum Science and Technology and ACM TQC
  all ask for high impact.
- **No broad-significance bar.** Quantum Information Processing Regular Articles and EPJ Quantum
  Technology are judged on quality, validity and robustness. That suits a careful requirements result.
- **Finance journals** (Quantitative Finance, Journal of Computational Finance) fit only if the paper
  leads with the classical benchmark.
- **SIAM SIFIN** wants new methods that are significant rather than incremental. That is a poor fit.

**Is AI-assisted drafting with disclosure allowed, and where is it disclosed?** Yes at 12 of 13 venues.
The Journal of Computational Finance is unclear: its list of permitted AI uses does not include drafting
text. Where the disclosure goes differs by venue:

| Venue | Where AI-assisted drafting is disclosed | Extra conditions |
|---|---|---|
| Quantum | Author contribution statement (scope of use) | arXiv also requires reporting significant generative-AI use |
| PRX Quantum, PR Research, PR Applied (APS) | Acknowledgment for drafting; methods for research uses; figure captions for figures | Tool name and version, how it helped, how it was directed and verified |
| npj Quantum Information | Methods section | Amber use (verification and disclosure); red uses forbidden |
| Quantum Science and Technology (IOP) | Acknowledgements, with tool name and version | AI must not generate or modify the reference list or write responses to reviewers; prompt logs may be requested |
| IEEE TQE | Acknowledgments, naming the AI system and the sections affected | Section-level detail |
| ACM TQC | Writing help: no disclosure needed (policy of 14 May 2026). AI used in the research: methods section | Authors accountable; rejection or retraction for AI integrity problems |
| Journal of Computational Finance | Acknowledgement of each tool and its use | Drafting is not among the permitted uses: **unclear, ask the editor** |
| Quantitative Finance (T&F) | A dedicated "Declaration of generative AI use" statement | Full tool name and version, how and why; generated text must be thoroughly revised |
| SIAM SIFIN | Acknowledgements or Declarations, plus a sentence that the authors take responsibility for all content | Fabricated references bring a ban of at least one year |
| EPJ Quantum Technology, QIP (Springer) | Methods section | Extensive writing support is amber; presenting AI-generated conclusions as human work is red |

The project-specific consequence: AI_USE_LOG.md says the Codex runtime does not expose a model version,
and Claude's runtime reports `claude-opus-5-5`. APS, IOP and T&F ask for the tool version. Where it is
not known, the author should write "unknown" rather than guess. Quantum, Springer and IEEE ask for scope
of use, not version.

**Is arXiv posting required?** Only *Quantum* requires it: the paper must be on, or cross-listed to,
quant-ph before it is considered. The accepted version must also be uploaded to arXiv under CC BY 4.0.
All other venues allow preprints, with two exceptions:

- The Journal of Computational Finance does not address preprints. It forbids posting the published
  paper online and allows self-archiving only after 12 months.
- SIFIN does not state a preprint rule. It requires any earlier appearance, in any form, to be declared
  in the cover letter and in a first-page footnote.

**arXiv endorsement for a first-time quant-ph or q-fin submitter.** arXiv changed its policy on 21
January 2026. Automatic endorsement now needs both of the following:

- an institutional email address, and
- prior authorship of a paper accepted to arXiv in the same endorsement domain.

Otherwise the author needs a personal endorsement from an established arXiv author in that domain.
The policy post says arXiv staff cannot waive endorsement or give one. In physics, each subject class is
its own endorsement domain, so quant-ph is one. Endorsers need a subject-dependent number of papers
submitted between three months and five years ago.

A first-time submitter from VIT Vellore with no earlier quant-ph paper will therefore most likely need a
personal endorser, even with a VIT email address. Two points are not stated on the official pages and
are marked unknown:

- whether q-fin is a separate domain from quant-ph (it probably is, since q-fin is not a physics subject
  class, but this is unverified);
- whether cross-listing needs its own endorsement.

**Fees for an author based in India.** India is not on the APS waiver list, which follows Research4Life.
It is not among Springer Nature's lowest-income countries for automatic waivers. It is on ACM's list as
a World Bank lower-middle-income country, which earns 50% off. It qualifies for IEEE's 50%
lower-middle-income discount. The World Bank's FY27 update (1 July 2026) lists six countries that moved
up, and India is not among them. Costs for an unfunded corresponding author at VIT:

| Venue | Cost to publish (as of 1 Oct 2026) |
|---|---|
| Quantum | EUR 600 regular, EUR 100 reduced, or a full waiver with no justification needed. **Effectively 0** |
| QIP, QST, SIFIN, PR Applied (subscription routes) | **0** (PR Applied: no charge stated explicitly; confirm) |
| Journal of Computational Finance | No charge stated for the standard route |
| Quantitative Finance | **USD 162 submission fee**, non-refundable, paid by card at submission; no APC on the subscription route |
| ACM TQC | USD 725 (no ACM member among co-authors) or USD 475 (with a member), 2026 subsidised rates after the 50% India discount; 2027 rates unknown |
| IEEE TQE | About USD 998 (USD 1,995 less 50%) before any member discount |
| EPJ Quantum Technology | USD 2,190 plus tax, unless a discretionary waiver is requested **at submission** or an agreement covers VIT |
| PR Research | USD 2,910, mandatory; no India waiver |
| PRX Quantum | USD 3,590, mandatory; no India waiver |
| npj Quantum Information | USD 4,390 / GBP 3,090 / EUR 3,690, unless a discretionary waiver is requested **at submission** or an agreement covers VIT |

India's One Nation One Subscription (ONOS) scheme funds 100% of the APC for 113 fully open-access Springer
Nature journals at participating institutions. The government page lists central and state universities,
colleges and central government R&D institutions as eligible. It does not mention private universities.
Whether VIT participates, and whether EPJ QT or npj QI is on the list, is **unknown**. The author can check
both at onos.gov.in.

---

## 3. Recommendation (for the author to accept or change)

**Primary: Quantum (quantum-journal.org), on three conditions.**

Reasons:
- It is the natural readership. The closest prior work, the derivative-pricing threshold paper by
  Chakrabarti et al., was published there, and this paper answers it directly.
- The cost is effectively zero: there is a full waiver with no justification needed.
- Its AI policy allows AI-assisted drafting. Disclosure goes in the author contribution statement and
  covers the scope of use, so the missing Codex version does not block it.
- It has no length limit. It encourages releasing data and code under FOSS licences, which fits the
  frozen benchmark and the D_max calculator.
- Posting to arXiv is already on the author's list in plan section 8.

The conditions:
1. The L1 novelty checkpoint is a "go", meaning the frontier argument is not already published. Quantum
   treats incremental work as below its bar, so the paper must lead with the general frontier, the
   calculator and the checklist, as the plan already says.
2. The author obtains quant-ph endorsement in Week 1.
3. The author accepts public posting before review and the irrevocable CC BY 4.0 licence for the accepted
   version on arXiv.

Expected timing: at least 2 weeks to assign an editor, then 2 to 3 weeks to a first decision, then 2 to 4
months for referee reports if the paper goes to review.

**Fallback: Quantum Information Processing (Springer), subscription route.**

Reasons:
- It costs nothing.
- It needs no arXiv posting, so it still works if endorsement fails.
- Regular Articles may be any length and have no broad-significance bar, which suits a careful negative
  result.
- Review is single-blind, and the median time to first decision is 32 days.
- AI drafting is allowed with disclosure in Methods.
- It has finance precedent (Tanaka et al., 2021) and was the earlier first-choice target in
  docs/JOURNAL_REENGINEERING_RESEARCH_2026-09-09.md.

Its official guidelines contradict themselves twice, so the author should ask the editorial office before
submitting:
- the abstract is given as 80 to 100 words in one place and 150 to 250 words in another;
- one section accepts .docx or LaTeX, another says LaTeX. LaTeX satisfies both.

Its visibility is lower than Quantum's. An arXiv preprint and a Zenodo archive would offset that.

**When to switch.** If the L1 checkpoint triggers the plan's pre-committed fallback contribution, the
target becomes a benchmark or computational-finance venue. In that case Quantitative Finance is preferred
over the Journal of Computational Finance:
- its AI policy allows drafting with thorough revision and disclosure;
- it allows preprints;
- its Open Science badges include "Preregistered", which fits the prospective specifications.

It costs the USD 162 submission fee. JCF is weaker on two points: its AI policy does not clearly allow
drafting, and it forbids posting the published paper online.

**Not recommended, and why:**
- **PRX Quantum, PR Research, npj QI and EPJ QT:** mandatory APCs of USD 2,190 to 4,390 with no automatic
  waiver for India. EPJ QT is otherwise a reasonable fit if a waiver or agreement covers it.
- **QST:** free, but highly selective, and IOP forbids AI-generated reference lists and reviewer
  responses. It is a reasonable stretch alternative to Quantum if the author compiles the references and
  writes all responses personally.
- **IEEE TQE and ACM TQC:** USD 475 to 1,000, and an engineering or CS readership.
- **PR Applied:** risk that editors judge it out of scope.
- **SIFIN:** requires new methods.

---

## 4. Per-venue conformance tables

"Unknown" means the official pages read on 1 October 2026 do not say. "Not stated" means the same.

### 4.1 Quantum (quantum-journal.org)

| Item | Verified finding |
|---|---|
| Scope fit | Quantum science broadly; judged on correctness, significance and clarity; incremental work on a limited technique is below the bar; no statement on negative results. Topic in scope by precedent; significance is the risk. **Good fit, high bar** |
| Format and source | Submit only the arXiv reference (quant-ph primary or cross-list); quantumarticle class encouraged, not required; no format or length constraints; state main results and assumptions in the first couple of pages |
| Length | No limit |
| Abstract and keywords | No word limit; optional non-technical popular summary; keywords not mentioned |
| Required statements | Author contribution statement (mandatory, any level of detail), including AI disclosure; competing interests and funding not mentioned (acknowledge conventionally) |
| AI policy | Allowed. Disclose the scope of any LLM or AI use (grammar, text, images, code, bibliography, calculations) in the author contribution statement. arXiv: report significant generative-AI use; AI not an author; authors fully responsible |
| Data and code | FOSS release of data and analysis code strongly encouraged, not mandated |
| Preprint and arXiv | **arXiv quant-ph required.** Accepted version must go on arXiv under CC BY 4.0. Endorsement: see section 2 |
| Fees and waivers (India) | EUR 600 regular, EUR 100 reduced, or full waiver without justification (email info@quantum-journal.org). The two official pages disagree on when EUR 600 took effect (1 Jan 2024 vs Jan 2025) |
| Review model and time | Single-blind; at least 2 weeks to assign an editor, 2 to 3 weeks to first decision, 2 to 4 months for referee reports, 1 to 2 months after resubmission, about 1 week from acceptance to publication |
| Official URLs | quantum-journal.org/instructions/authors/ ; /editorial-policies/ ; /about/ ; /payment/ ; /updated-publication-charges/ ; info.arxiv.org/help/endorsement.html ; blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/ ; info.arxiv.org/help/moderation/index.html |
| Accessed | 2026-10-01 |

### 4.2 PRX Quantum (APS)

| Item | Verified finding |
|---|---|
| Scope fit | Interdisciplinary QIS; needs exceptional achievement in at least one of four categories; no statement on negative results. **Weak fit for a finance-specific negative result** |
| Format and source | LaTeX (REVTeX) preferred, or Word; a PDF is enough for review; can submit from an arXiv number |
| Length | Research Articles: no limit (Perspectives 7,500 words, Tutorials 37,500, Comments 3,500) |
| Abstract and keywords | No abstract limit found (unknown); mandatory popular summary of about 150 words (the general APS page says at most 250) |
| Required statements | Data Availability Statement (submissions from 11 Dec 2024); AI disclosure for substantive use; conflicts reported to editors, in-paper COI statement encouraged; author contributions optional (APS style) |
| AI policy | Allowed (APS policy updated 17 June 2026). Substantive uses, including drafting claims, must be disclosed with tool name and version, how it helped, how it was directed and verified. Drafting goes in the Acknowledgment; research uses in methods; figures in captions; light editing exempt |
| Data and code | DAS mandatory; code release not mandated |
| Preprint and arXiv | arXiv at any time; not required |
| Fees and waivers (India) | Gold OA CC BY 4.0; **USD 3,590 mandatory**; India not on the APS waiver list; no Indian institution in the APS OA agreements |
| Review model and time | 2025: desk decision 5 days, after review 58 days, to acceptance 166 days, to publication 211 days. Peer-review model not stated on the pages read |
| Official URLs | journals.aps.org/prxquantum/about ; /prxquantum/authors ; journals.aps.org/authors/ai-based-writing-tools ; aps.org news release 2026/06 ; /authors/apcs ; aps.org international journals waiver page ; /authors/editorial-policies ; /authors/web-submission-guidelines-physical-review ; /authors/funder-compliance-article-deposits |
| Accessed | 2026-10-01 |

### 4.3 Physical Review Research (APS)

| Item | Verified finding |
|---|---|
| Scope fit | All of physics plus interdisciplinary work with a connection to physics; must be significant and substantive. **Moderate fit** with hardware and QIS framing |
| Format and source | Single PDF; can submit from an arXiv number; REVTeX preferred |
| Length | No limit found |
| Abstract and keywords | Not stated |
| Required statements | DAS; COI to editors (in-paper statement encouraged); substantive AI disclosure |
| AI policy | Same APS policy as 4.2: drafting allowed with disclosure in the Acknowledgment |
| Data and code | DAS mandatory; code not mandated |
| Preprint and arXiv | Allowed at any time; not required |
| Fees and waivers (India) | Fully OA; **USD 2,910 mandatory**; no India waiver |
| Review model and time | 2025: desk decision 4 days, after review 56 days, to acceptance 126 days, to publication 165 days |
| Official URLs | journals.aps.org/prresearch/about plus the APS policy pages in 4.2 |
| Accessed | 2026-10-01 |

### 4.4 Physical Review Applied (APS)

| Item | Verified finding |
|---|---|
| Scope fit | Applied physics; QIS listed, finance not; must give fresh insight into applications-based physical phenomena. **Weak to moderate fit** (risk of desk rejection for scope) |
| Format and source | PDF for review; LaTeX preferred, or Word |
| Length | Regular Articles: no limit (Letters 4,500 words) |
| Abstract and keywords | No limit stated; optional non-technical summary |
| Required statements | DAS; AI disclosure in the paper; author contributions (APS style); **a 100-word justification of suitability** |
| AI policy | APS policy (4.2): drafting allowed with disclosure in the Acknowledgment |
| Data and code | DAS mandatory |
| Preprint and arXiv | Allowed; accepted manuscript may go on arXiv under arXiv's non-exclusive licence, not a CC licence, with the APS notice |
| Fees and waivers (India) | Hybrid: optional OA USD 2,910; subscription route likely free but not stated explicitly (confirm) |
| Review model and time | 2025: desk decision 7 days, after review 56 days, to acceptance 146 days, to publication 177 days |
| Official URLs | journals.aps.org/prapplied/about ; /prapplied/authors ; APS policy pages in 4.2 |
| Accessed | 2026-10-01 |

### 4.5 npj Quantum Information (Nature Portfolio)

| Item | Verified finding |
|---|---|
| Scope fit | Publishes what it calls the finest research on quantum information; no selectivity figure or negative-results statement. **Weak fit (high bar)** |
| Format and source | No formatting rules at first submission; single PDF or Word; LaTeX only after acceptance |
| Length | No limit stated |
| Abstract and keywords | No limit stated |
| Required statements | Data Availability section; Code availability statement (in Methods) where custom code is central; competing interests (even if none); author contributions with initials; LLM use in Methods |
| AI policy | Allowed. LLMs cannot be authors; document LLM use in Methods. Nature Portfolio framework: language polishing green; drafting summaries amber (verify and disclose); presenting AI-generated analyses or conclusions as human work red |
| Data and code | Data and code availability statements as above |
| Preprint and arXiv | Preprints do not affect novelty; not required |
| Fees and waivers (India) | **USD 4,390 / GBP 3,090 / EUR 3,690**; automatic waivers only for the lowest-income countries; discretionary waiver must be requested at submission; ONOS coverage unknown |
| Review model and time | Unknown |
| Official URLs | nature.com/npjqi/for-authors-and-referees/submission-guidelines ; /npjqi/apc ; /npjqi/journal-information ; nature.com/nature-portfolio/editorial-policies/ai |
| Accessed | 2026-10-01 |

### 4.6 Quantum Science and Technology (IOP)

| Item | Verified finding |
|---|---|
| Scope fit | Quantum computation, simulation, sensing and related areas; highly selective (essential reading for a sub-field and of broad interest). **Moderate fit, high bar** |
| Format and source | Single file; IOP templates; anonymised if double-anonymous review is chosen |
| Length | No limit stated |
| Abstract and keywords | Abstract normally at most 300 words, self-contained (may be returned if longer); keywords requested |
| Required statements | Competing interests and funding in Acknowledgements; CRediT suggested; ORCID recommended; DAS (the IOP data policy says required; the level for QST is not stated); AI statement in Acknowledgements |
| AI policy | Allowed, with limits. AI may draft text that the authors critically revise. It must not generate or modify reference lists or write responses to reviewers (language polishing of responses is allowed). Disclose in Acknowledgements with tool and version (template sentence provided). Prompt logs may be requested |
| Data and code | DAS; supplementary files get DOIs; code not mandated |
| Preprint and arXiv | Preprint allowed if authors keep copyright and grant no exclusive licence; not required |
| Fees and waivers (India) | **Subscription route free**; optional OA GBP 2,930 / USD 4,090 / EUR 3,335 |
| Review model and time | Single- or double-anonymous at the author's choice; time unknown |
| Official URLs | publishingsupport.iopscience.iop.org/journals/quantum-science-technology/about-quantum-science-technology/ ; /journals/quantum-science-technology/ ; /questions/generative-ai-tools/ ; /iop-publishing-data-availability-policy/ |
| Accessed | 2026-10-01 |

### 4.7 IEEE Transactions on Quantum Engineering

| Item | Verified finding |
|---|---|
| Scope fit | Engineering applications of quantum phenomena; subject areas include Quantum Software (compilers, stacks) and Quantum Computing (algorithms, architectures). **Moderate fit** via the compiled-oracle frontier |
| Format and source | IEEE templates; review and tutorial articles need the Editor-in-Chief's prior approval |
| Length | No page limit |
| Abstract and keywords | Unknown on TQE pages |
| Required statements | AI disclosure in Acknowledgments; others unknown |
| AI policy | Allowed. Disclose AI-generated content in Acknowledgments, naming the system and the sections affected; editing and grammar help generally outside the policy |
| Data and code | Unknown |
| Preprint and arXiv | Allowed. On submission the preprint must carry IEEE's notice; after acceptance replace it with the citation or the accepted manuscript (general IEEE rule; how it applies to CC BY articles is unknown) |
| Fees and waivers (India) | APC USD 1,995 (from 1 Jan 2024); 50% off for World Bank lower-middle-income countries, so **about USD 998**; IEEE member 5% or society member 20% (not combinable); CC BY per a search-indexed TQE page |
| Review model and time | Single-blind, at least two reviewers; time unknown |
| Official URLs | tqe.ieee.org/ ; /submission-process/ ; /faq/ ; /subject-areas/ ; journals.ieeeauthorcenter.ieee.org (submission and peer review policies) ; World Bank FY27 blog |
| Accessed | 2026-10-01 |

### 4.8 ACM Transactions on Quantum Computing

| Item | Verified finding |
|---|---|
| Scope fit | Theory and practice of quantum computing, incl. fault-tolerant methods and design automation; rejection grounds include breadth, impact, novelty or correctness. **Moderate fit** |
| Format and source | ACM template required at submission; Manuscript Central; CCS terms after acceptance |
| Length | No limit on the current guidelines page (the earlier search snippet about a page limit was not found) |
| Abstract and keywords | Unknown |
| Required statements | ORCID required at submission (all authors before production); AI used in the research described in the methods section |
| AI policy | Allowed. Under ACM's policy of 14 May 2026, writing help needs no disclosure; AI used in the research (code, analysis, figures and so on) must be described in the methods section; rejection or retraction possible for AI integrity problems |
| Data and code | Artifacts encouraged (badging); not mandated |
| Preprint and arXiv | An arXiv preprint is not prior publication; not required; CC BY or CC BY-NC-ND |
| Fees and waivers (India) | Fully OA from 2026; 2026 subsidised APC USD 1,450 (no member) or USD 950 (with a member); India gets 50% off, so **USD 725 or USD 475**; hardship waivers exist; 2027 rates unknown; ACM Open coverage for VIT unknown |
| Review model and time | Editorial screen for readability and scope; single-blind; three reviews as standard; revisions due within 30 days (minor) or 90 days (major); 6 to 8 weeks in production; may require professional copyediting |
| Official URLs | dl.acm.org/journal/tqc/about ; dl.acm.org/journal/tqc/author-guidelines ; acm.org/publications/policies/new-acm-policy-on-authorship ; /policy-on-geographic-apc-waivers-and-discounts ; /waiver-countries |
| Accessed | 2026-10-01 |

### 4.9 The Journal of Computational Finance (Risk.net)

| Item | Verified finding |
|---|---|
| Scope fit | Numerical and computational methods for pricing, hedging and risk, incl. Monte Carlo and quasi-Monte Carlo; quantum not mentioned. **Fits the classical half only** (the fallback-contribution route) |
| Format and source | Anonymised PDF; separate title page (running head of at most 50 characters, word count, figure and table counts); figures and tables also as editable vector files; TeX source after acceptance; Chicago author-date citations with an APA reference list |
| Length | Research papers at most about 10,000 words (not strict) |
| Abstract and keywords | 150 to 200 words, one paragraph, no references; 4 to 6 keywords; **3 to 4 key-message bullets of at most 85 characters each** |
| Required statements | Declarations of Interest (funding and conflicts, or a prescribed no-conflict sentence); Acknowledgements; AI acknowledgement; conclusions section; author biography and headshot after acceptance |
| AI policy | **Unclear.** AI use in drafting must be acknowledged tool by tool. The permitted uses listed are organising data, search-engine-like background research and grammar-tool-like editing. Drafting text is not listed. Ask the editor |
| Data and code | Code and data may be supplementary material; enough detail to repeat the work |
| Preprint and arXiv | Pre-submission preprints not addressed (unknown); published papers must not be posted online; the final version may be self-archived in an institutional repository after 12 months |
| Fees and waivers (India) | No charge stated; open access by arrangement, price unknown |
| Review model and time | Editor-in-Chief screen, then single-blind review; time unknown; impact factor 0.5 |
| Official URLs | risk.net/journal-of-computational-finance ; risk.net/static/risk-journals-submission-guidelines ; /static/editorial-policies ; /static/copyright-and-permissions |
| Accessed | 2026-10-01 |

### 4.10 Quantitative Finance (Taylor & Francis)

| Item | Verified finding |
|---|---|
| Scope fit | Interdisciplinary quantitative finance for a broad audience; derivatives pricing and financial engineering listed; quantum not mentioned. **Moderate fit if it leads with the classical benchmark** |
| Format and source | Word or LaTeX (PDF plus zipped source); templates; set section order; instructions updated 17 July 2026 |
| Length | Typical paper at most 35 pages including references and footnotes; word count required; Research Letters at most 12 pages |
| Abstract and keywords | Unstructured, 200 words; 4 to 6 keywords; optional graphical or video abstract |
| Required statements | Funding (or none); competing-interest disclosure; **Declaration of generative AI use (required even if none)**; DAS if a dataset exists; CRediT roles at submission |
| AI policy | Allowed with thorough revision. Disclose the full tool name and version, how and why it was used. Text or code generation without thorough revision is not permitted; AI cannot be an author |
| Data and code | Basic data-sharing policy (encouraged); Figshare supplements; Open Science badges (Open Data, Open Materials, Preregistered) |
| Preprint and arXiv | Original manuscript may be posted on arXiv at any time (not duplicate publication; review anonymity cannot be guaranteed); accepted manuscript to repositories after a 12-month embargo |
| Fees and waivers (India) | **USD 162 submission fee**, non-refundable, by card (Research Letters exempt for now); no APC on the subscription route; Open Select APC unknown |
| Review model and time | Editor screen, then single-blind review by two referees; 15 days to first decision, 98 days to first post-review decision, 23% acceptance; impact factor 1.9 (2025) |
| Official URLs | tandfonline.com/journals/rquf20/about-this-journal ; tandfonline.com/action/authorSubmission?show=instructions&journalCode=rquf20 ; taylorandfrancis.com/our-policies/ai-policy/ ; authorservices.taylorandfrancis.com (sharing versions of journal articles) |
| Accessed | 2026-10-01 |

### 4.11 SIAM Journal on Financial Mathematics

| Item | Verified finding |
|---|---|
| Scope fit | Financial mathematics; computational papers must introduce new methods that are significant rather than incremental. **Poor fit** |
| Format and source | Manuscript plus cover letter as PDFs; figures inline; SIAM online macros encouraged; TeX after acceptance; any earlier appearance declared in the cover letter and a title-page footnote |
| Length | No SIFIN limit found; short communications at most 12 pages |
| Abstract and keywords | One paragraph of at most 250 words; keywords and MSC codes required; running head of at most 50 characters |
| Required statements | AI statement in Acknowledgements or Declarations plus the responsibility sentence; others unknown |
| AI policy | Allowed under strict accountability (version 2.0, May 2026). Authors must have read every work they cite. Fabricated references bring a ban of at least one year (SIAM News, 1 May 2026). Grammar checking need not be disclosed |
| Data and code | No mandate; making AI-assisted code public is preferred |
| Preprint and arXiv | Preprint rule not stated (unknown); accepted manuscript may be deposited under CC BY at publication |
| Fees and waivers (India) | **Subscription route free**; optional OA USD 3,750 |
| Review model and time | Editor-in-Chief may reject without review; referees asked to report within about 2 months; average time to acceptance across SIAM journals about 10.5 months |
| Official URLs | epubs.siam.org/journal/sifin/instructions-for-authors ; /journal/sifin/editorial-policy ; epubs.siam.org/artificial-intelligence ; epubs.siam.org/journal-authors ; siam.org SIAM News article "A Contract of Trust" |
| Accessed | 2026-10-01 |

### 4.12 EPJ Quantum Technology (SpringerOpen)

| Item | Verified finding |
|---|---|
| Scope fit | Quantum technology; excludes non-technical "quantum economics" but not technical finance algorithms (Manzano et al. 2025 precedent); reviewers check validity and robustness. **Good fit** |
| Format and source | DOC/DOCX, RTF or TeX/LaTeX; editable source required; figure and table titles at most 15 words, legends at most 300 |
| Length | No limit stated |
| Abstract and keywords | Aim and findings, few abbreviations, no references; no word limit stated; 3 to 10 keywords |
| Required statements | "Declarations" section: Availability of data and materials, Competing interests, Funding, Authors' contributions, Acknowledgements ("Not applicable" where relevant); LLM use in Methods |
| AI policy | Allowed. LLMs cannot be authors; document LLM use in Methods. Springer framework: extensive writing support is amber; presenting AI-generated conclusions as human-derived is red |
| Data and code | Data availability statement mandatory; repository deposit mandatory for some data types |
| Preprint and arXiv | Preprints encouraged at any time; not counted against novelty; not required |
| Fees and waivers (India) | **USD 2,190 / GBP 1,790 / EUR 1,990 plus tax**; discretionary waiver only if requested at submission; ONOS coverage unknown |
| Review model and time | Single-anonymous, two or more reviewers; median 5 days to first decision; impact factor 4.5 (2025) |
| Official URLs | link.springer.com/journal/40507/submission-guidelines ; /submission-guidelines/research-articles ; link.springer.com/journal/40507 ; link.springer.com/brands/springer/journal-policies |
| Accessed | 2026-10-01 |

### 4.13 Quantum Information Processing (Springer)

| Item | Verified finding |
|---|---|
| Scope fit | All of QIS; Regular Articles of high quality, any length, on any aspect; no broad-significance bar. **Good fit** |
| Format and source | Single document with a title page (single-blind); one section accepts .docx or LaTeX, another says LaTeX (Springer Nature template); editable source each time; author contribution and competing-interest text entered in the submission system (only that text is published) |
| Length | No limit |
| Abstract and keywords | **Inconsistent on the official page: 80 to 100 words in one section, 150 to 250 in another**; 4 to 6 keywords |
| Required statements | "Statements and Declarations" (returned as incomplete if missing); DAS mandatory; competing interests; funding; contributions; LLM use in Methods |
| AI policy | Allowed. Document LLM use in Methods. Copy editing of human-written text is exempt, but generative editing and autonomous content creation are not. Springer amber and red rules apply |
| Data and code | Springer Nature research data policy; DAS mandatory; deposit strongly encouraged |
| Preprint and arXiv | Preprints encouraged; not required |
| Fees and waivers (India) | **Subscription route free**; optional OA USD 3,090 / GBP 2,190 / EUR 2,490 |
| Review model and time | Single-blind; median 32 days to first decision; impact factor 2.2 (2025) |
| Official URLs | link.springer.com/journal/11128/submission-guidelines ; /how-to-publish-with-us ; link.springer.com/journal/11128 ; link.springer.com/brands/springer/journal-policies |
| Accessed | 2026-10-01 |

---

## 5. Corrections to `l2_venues.jsonl`

The full list is in `l2_verification.jsonl`. The ones that matter for the decision:

- **Quantum.** The two official pages disagree on when the EUR 600 fee took effect (1 January 2024 vs
  January 2025). The statement that arXiv staff cannot endorse comes from the arXiv blog, not the help
  page. Two points are now marked unknown instead of inferred: whether cross-lists need endorsement, and
  whether q-fin and quant-ph are one domain.
- **PRX Quantum.** The popular summary is about 150 words per the journal page, not 250. Author
  contributions are optional. The peer-review model is not confirmed.
- **PR Applied.** Added the required 100-word justification. "Subscription route free" is downgraded to
  "likely; confirm".
- **IOP QST.** Competing interests and funding go in Acknowledgements. IOP allows AI to polish the
  language of review responses but not to write them. Prompt logs may be requested.
- **ACM TQC.** Pages now read directly. No page limit appears. Review is single-blind with three reviews.
  ORCID is required at submission. India's 50% discount is confirmed.
- **JCF.** Added the key-message bullets, the APA reference list and 12-month self-archiving. Code and
  data are allowed as supplements.
- **SIFIN.** Pages now read directly. The abstract limit is 250 words, with keywords and MSC codes. The
  claim that preprints are "not prohibited" was not found on the official pages, so it is now unknown.
  The one-year ban comes from SIAM News, not from the policy text.
- **EPJ QT and QIP.** Added the median times to first decision (5 and 32 days). QIP's guidelines also
  contradict themselves on file format.
- **npj QI, EPJ QT.** Added the ONOS route (eligibility unknown).

---

## 6. Actions only the author can take

1. **arXiv (Week 1).**
   - Log in or create an account, and link the VIT institutional email.
   - Claim any earlier co-authored arXiv papers.
   - Start a quant-ph submission to see whether endorsement is needed. If it is, ask an established
     quant-ph author, such as a supervisor or collaborator, to endorse. arXiv staff cannot.
   - If a q-fin primary category or a cross-list is planned, check endorsement for that category in the
     submission interface. The official pages do not say.
2. **Licence and timing.** Decide on public preprint timing relative to the two earlier companion drafts.
   If Quantum is chosen, accept that the accepted version goes on arXiv under CC BY 4.0, which cannot be
   undone.
3. **Venue choice.** Pick the primary and fallback and record them in VENUE.md. Confirm there is no
   concurrent submission.
4. **Fees.**
   - Quantum: choose the regular fee, the reduced fee or a waiver, and email info@quantum-journal.org if
     waiving.
   - Quantitative Finance: pay USD 162 personally by card at submission. The agent cannot do this.
   - Springer OA titles: any discretionary waiver must be requested at submission.
   - Check whether VIT takes part in ONOS (onos.gov.in), ACM Open, IOP transformative agreements or
     Springer Nature agreements.
5. **AI disclosure.**
   - Approve the wording for the chosen venue and the place it goes (section 2 table).
   - For APS, IOP or T&F, give the tool name and version. Write "unknown" for the Codex version, as
     AI_USE_LOG.md does.
   - For IEEE, list the affected sections.
6. **Citations.** Check every reference against its source personally. IOP forbids AI-generated
   reference lists, SIAM bans authors for fabricated references, and Springer and Nature classify
   fabricated citations as red.
7. **Questions to editorial offices.**
   - QIP: the abstract length (80 to 100 vs 150 to 250 words).
   - JCF, if it becomes relevant: whether AI-assisted drafting is acceptable, and whether an arXiv
     preprint is allowed.
8. **Identifiers.** Get an ORCID. ACM requires it at submission; the other venues recommend it.
9. **Human expert review** before submission, as plan section 8 already requires.
10. **Recheck on submission day.** Fees (ACM's subsidised rates are for 2026 acceptances only), India's
    World Bank income class, and the AI policies, since APS and ACM changed theirs in 2026.
