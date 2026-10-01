# AI assistance log

## 27 September 2026 — resumed implementation

Codex inspected the September 24 foundation, implementation plan, errata,
preregistration deviations and prior provenance receipt, and the compiler sources.
It authored the prospective Stage A specification, implemented and executed the source
compilation/accounting checks in a new versioned directory. No author or external
expert verification is implied. The runtime does not expose a reliable exact
model/version identifier; none is invented here.

Results, validation, deviations and any independent AI-agent review are recorded
in the Stage A report. Internal agent review is not external peer review.

Two independently tasked Codex subagents reviewed the implementation, evidence and
interpretation. Their findings and dispositions are in `STAGE_A_REVIEW.md`. The main
agent generated `STAGE_A_RESULTS.md` from the archived numeric results, corrected
overclaims in the foundation text and maintained the pending-work checklist.
No fresh literature or alternative-advantage search was performed.

## 1 October 2026 — Stage B (T0, Q0)

Claude Code (Anthropic; the runtime reports model ID `claude-opus-5-5`) worked at the
author's request. It wrote the prospective Stage B specification, the hash-pinned lock and the
replay runner, and committed them before execution. It then built the environment, ran the
replay, and ran and documented the attribution diagnostics, including two flawed ones.
The author approved the CUDA download and outside-model review in chat. Claude also drafted
the not-yet-committed Stage C specification. Two background agent workflows (literature
and venue sweep; Stage C spec critique) were interrupted by a usage limit and are re-run
separately; their outputs, when complete, are recorded with their own review notes.
Internal agent work is not external peer review.

## 1 October 2026 — L1/L2 literature screen and Stage C specification

Claude Code subagents ran plan items L1 (prior art) and L2 (venue compliance). Three
searchers saved rows incrementally; two were cut off by a usage limit after saving, and
two verifiers then re-opened the primary sources and wrote `literature/L1_PRIOR_ART.md`
(checkpoint recommendation GO_NARROWED) and `literature/L2_VENUES.md`. The venue verifier
read some official pages that block automated fetches in the desktop app's browser pane;
no bot wall was bypassed. The checkpoint and the venue choice are the author's decisions.
The main agent independently checked one load-bearing citation (Case, arXiv:2502.17731 v2)
before adding it to ERRATA E10.

Three critic subagents reviewed the Stage C specification draft, and a fourth checked
closure (`reviews/STAGE_C_SPEC_REVIEW.md`). The main agent wrote both specification
versions and the Stage C code. A reviewer's claim about SeedSequence key padding was
tested and found false, and the code follows the specification's five-word keys.
All of this is internal agent work, not peer review.
