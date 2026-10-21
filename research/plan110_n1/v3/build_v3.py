"""Build FRONTIER_NEGATIVE_RESULT_DRAFT_v3.md from v2 by exact, counted string replacements.

Each replacement fixes one re-check defect N3-1..N3-8 (results/plan110_n1/recheck/RECHECK.md)
or is a consequential edit (title, source keys, provenance, Appendix B, changelog). Every
`old` string must occur exactly once in v2; v2 itself is only read, never written.

Run from the repo root:
  .context/frontier_t0_env/Scripts/python.exe -I -S -B research/plan110_n1/v3/build_v3.py
  (add --out PATH to write a preview elsewhere; the default target is created with
  exclusive create and the script refuses to overwrite it)

stdlib only. On a real build one row is appended to results/plan110_n1/v3/rows.jsonl.
"""
import hashlib
import json
import sys

V2 = "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v2.md"
V3 = "manuscript/advantage-frontier-2026-09-23/FRONTIER_NEGATIVE_RESULT_DRAFT_v3.md"
V2_SHA = "51dcf89b8ad127187843a1e734e2a9e7f59f45dc4b7d66571100ece5b8132d00"
ROWS = "results/plan110_n1/v3/rows.jsonl"

# (tag, old, new). Tags name the defect a replacement fixes, or "cons" for consequential edits.
R = [
("cons:title",
"""**Draft manuscript v2, branch N of plan110 (N2 revision).** 12 October 2026. Affiliation: VIT Vellore.""",
"""**Draft manuscript v3, branch N of plan110 (N2 re-check touch-up).** 12 October 2026. Affiliation: VIT Vellore."""),

("N3-8:front-matter",
"""14 minor defects. This version addresses each of them; the changelog at the end maps every
defect to its fix. This revision has not been re-checked by a reviewer, and it has not had
the user's sign-off that `research/plan110_n1/N1_CARD.md` requires.""",
"""14 minor defects. Version 2 (`FRONTIER_NEGATIVE_RESULT_DRAFT_v2.md`, unchanged) addressed
each of them. The AI-assisted N2 re-check of v2 (`results/plan110_n1/recheck/RECHECK.md`)
records all 21 as fixed and 129 of 129 number checks as passing, and lists 8 new minor,
text-only defects, N3-1 to N3-8. This version (v3) fixes those 8. The changelog at the end
maps every review defect (v1 → v2) and every re-check defect (v2 → v3) to its fix. The v3
edits have been checked only by the script `research/plan110_n1/v3/check_v3.py`, not by a
reviewer, and this draft has not had the sign-off that `research/plan110_n1/N1_CARD.md`
requires."""),

("cons:number-rule",
"""**Number rule.** Every number below comes from an N1 result file (wave 1 of branch N), from
the N2 review files, or is a product or ratio of such numbers computed by the drafter, review
or fixer scripts.""",
"""**Number rule.** Every number below comes from an N1 result file (wave 1 of branch N), from
the N2 review or re-check files, or is a product or ratio of such numbers computed by the
drafter, review, fixer, re-check or v3 scripts."""),

("cons:source-keys",
"""| [FX] | `results/plan110_n1/fixer/fixer_numbers.json` | this revision, `research/plan110_n1/fixer/fixer_numbers.py` |
| [FX2] | `results/plan110_n1/fixer/fixer_numbers_2.json` | this revision, `research/plan110_n1/fixer/fixer_numbers_2.py` |""",
"""| [FX] | `results/plan110_n1/fixer/fixer_numbers.json` | v2 revision, `research/plan110_n1/fixer/fixer_numbers.py` |
| [FX2] | `results/plan110_n1/fixer/fixer_numbers_2.json` | v2 revision, `research/plan110_n1/fixer/fixer_numbers_2.py` |
| [RK] | `results/plan110_n1/recheck/number_recheck.json` (`probes`) | N2 re-check, `research/plan110_n1/recheck/recheck_draft.py` (129 checks; probes all `modelled (derived)`) |
| [V3] | `results/plan110_n1/v3/v3_numbers.json` | this revision, `research/plan110_n1/v3/v3_numbers.py` |"""),

("cons:provenance",
"""**Provenance.** All N1, review and fixer scripts whose numbers appear here ran under
`.context/frontier_t0_env/Scripts/python.exe -I -S -B` (Python 3.12.4, standard library
only).""",
"""**Provenance.** All N1, review, fixer, re-check and v3 scripts whose numbers appear here ran
under `.context/frontier_t0_env/Scripts/python.exe -I -S -B` (Python 3.12.4, standard library
only)."""),

("N3-8:abstract-user",
"""the primary convention the user chose. Holding the classical side to the symmetric,""",
"""the primary convention fixed in [W0C]. Holding the classical side to the symmetric,"""),

("N3-5:abstract-caption",
"""mod) [HT], [HW], [DC], [FX]:""",
"""mod) [HT], [HW], [DC], [FX], [RK]:"""),

("N3-5:abstract-row",
"""| Best explicit worst-case constant (every conditional credit granted) | **232.0** | **6.29** (11.2 without the U1 mean credit) |""",
"""| Best explicit worst-case constant (U1 + U2 + non-dyadic M) | **232.0** (200.4 with direction-select) | **6.29** (11.2 without the U1 mean credit; about 5.43 with direction-select, derived) |"""),

("N3-4:abstract",
"""Grover iterate takes at most 9.9 reaction layers **and** at most 9.9e5 T gates; with
today's certified constant the limits are 2.9 layers and 2.9e5 T. The idealized all-free
oracle floor is 114 layers, so it would have to be beaten by a further 11.5× (explicit) or
40× (certified).""",
"""Grover iterate takes at most 9.9 reaction layers **and** at most 9.9e5 T gates; with
today's certified constant the limits are 2.9-5.7 layers and 2.9e5-5.7e5 T (the upper values
with direction-select, whose call-cost condition this paper's cost model meets). The
idealized all-free oracle floor is 114 layers, so it would have to be beaten by a further
11.5× (explicit) or 20-40× (certified)."""),

("N3-3+N3-4:scope-item-1",
"""   iterate at the binding cell costs more than about 10 reaction layers or more than about
   1e6 T (best explicit constant), or more than about 3 layers or 3e5 T (today's certified
   constant).""",
"""   iterate at the binding cell costs more than about 10 reaction layers or more than about
   1e6 T (best explicit constant), or more than 2.9-5.7 layers or 2.9e5-5.7e5 T (today's
   certified constant; the upper values apply with direction-select, whose call-cost
   condition this paper's cost model meets), and whose iterates are also above the
   corresponding per-cell limit in the other decision cells (B4x12 $0.001: 1.1 layers /
   1.1e5 T for the best explicit constant, lower for the certified constant; §3)."""),

("N3-7:conventions-table",
"""| B8x52 at $0.001 | Eligible on a modelled, uncertified clamp tightening: lowering the stock clamp 3 binades gives bias $0.000473 = 0.47ε ≤ 0.55ε [BD]. The primary therefore keeps e = 0.45ε (mod, q+). It needs an A02 bridge rerun and A07/A13 re-proofs |""",
"""| B8x52 at $0.001 | Eligible on a modelled, uncertified clamp tightening (admission: mod, q+): lowering the stock clamp 3 binades gives bias $0.000473 = 0.47ε ≤ 0.55ε [BD]. The primary therefore keeps e = 0.45ε, which is q− relative to the strict zero-bias reading. It needs an A02 bridge rerun and A07/A13 re-proofs |"""),

("N3-3:section-3",
"""   (114) then lies inside the explicit limit, which is the M = 0.31 of §5.3.""",
"""   (114) then lies inside the explicit limit, which is the M = 0.31 of §5.3.

   These limits are for the binding cell. Tenfold in any eligible decision cell would
   overturn the result, and each other decision cell has its own, lower limit for the same
   estimator class (mod, derived) [RK], [V3]. For the best explicit constant they are 1.14
   layers / 1.1e5 T at B4x12 $0.001, 0.53 / 5.3e4 at B4x12 $0.01 and 2.43 / 2.4e5 at
   B8x52 $0.01. For today's certified constant they are lower still (at B4x12 $0.001: 0.34
   layers, or 0.68 with direction-select). A design is covered by the claim only if its
   iterate is above the limit in every decision cell; for B4x12 the loosest limit is
   1.1 layers / 1.1e5 T at $0.001 (explicit). This changes nothing in practice: the B4x12
   all-free floor is 94 layers [HT]."""),

("N3-8:section-4.3-user",
"""  symmetric with the quantum side. It is the user's chosen primary that departs from
  symmetry.""",
"""  symmetric with the quantum side. It is the primary convention fixed in [W0C] that departs
  from symmetry."""),

("N3-8:table-k",
"""| Best explicit with direction-select | n/a | 200.4 | As above, plus the direction-select condition |""",
"""| Best explicit with direction-select | 170.7 | 200.4 | As above, plus the direction-select condition |"""),

("N3-1:readings-caption",
"""**Readings of the primary conventions** (mod) [HT], [ES], [FX]:""",
"""**Readings of the primary conventions** (mod) [HT], [ES], [FX]; the last row combines two
readings (mod, derived, q+) [RK], [DC]:"""),

("N3-1:readings-row",
"""| Binding cell ineligible (B4x12 $0.001 binds; q−) | 1,065 | 318.0 | 11.8 |""",
"""| Binding cell ineligible (B4x12 $0.001 binds; q−) | 1,065 | 318.0 | 11.8 |
| Strict zero-bias reading + direction-select (the lowest combination) | 200.4 | ≈ 90 (approximate; ≈ 66 at failure 0.01) | 3.88 (already uses it) |"""),

("N3-1:verdict",
"""Under every reading above, the certified class stays at M ≥ 400.7 and the best explicit
class at M ≥ 104.4 (76.6 at failure 0.01 under the zero-bias reading [HT]), both above the
30× threshold that justifies R1. The window class misses by 3.9-13.5× across these readings,
and it has no explicit constant.""",
"""Taken one at a time, the readings above keep the certified class at M ≥ 400.7 and the best
explicit class at M ≥ 104.4 (76.6 at failure 0.01 under the zero-bias reading [HT]). Two of
them combine: direction-select is satisfied in this paper's cost model, and the strict
zero-bias reading is a reading of the primary. Together they give the lowest values (mod,
derived, q+) [RK]: certified M = 200.4 (k = 379.3 at e = ε [ES]) and best explicit M ≈ 90,
or ≈ 66 at failure 0.01. The two explicit values are approximate: [HT] has no explicit k
with direction-select at e = ε, so they are the zero-bias values 104.4 and 76.6 multiplied
by the binding-cell direction-select ratio at e = 0.45ε, 0.864 [DC]. All of these are above
the 30× threshold that justifies R1. The window class misses by 3.9-13.5× across these
readings, and it has no explicit constant."""),

("N3-4:lever-2",
"""   cell must take at most 9.9 reaction layers and 9.9e5 T (explicit constant), or 2.9 layers
   and 2.9e5 T (certified) [FX].""",
"""   cell must take at most 9.9 reaction layers and 9.9e5 T (explicit constant), or 2.9-5.7
   layers and 2.9e5-5.7e5 T (certified; the upper values with direction-select) [FX]."""),

("N3-2:lever-3",
"""   - Any one of these, stacked with lever 2's all-free floor, reaches or nearly reaches
     M = 1 (§5.3).""",
"""   - Stacked with lever 2's all-free floor, the first two reach or nearly reach M = 1:
     0.31 (distribution-free) and 1.125 (one lane) (§5.3). The other two do not (mod,
     derived) [RK], [HT]: with 1e13 T/s the all-free M is 11.3, because D_eff only drops
     from 114 to 112 layers, and with a 10 ns layer it is 7.3, because the iterate becomes
     supply-bound at 724 layers of 10 ns."""),

("N3-6:remove-from-7.1",
"""- **Lanes, E20.** No lane credit at the binding cell (§4.2).
""",
""""""),

("N3-6:add-to-7.2",
"""  gives 0.31, so the bound holds only at the primary convention.

### 7.3 Outside the claim, not closed""",
"""  gives 0.31, so the bound holds only at the primary convention.
- **E20: entangled parallel amplitude estimation (lanes).** At W = 1e7 only one lane of the
  primary-width design fits, and the binding cell gets a lane credit of 1.00× under every
  modelled supply (§4.2). E20's own kill rule is "State the width bound … and stop" [REG].
  The register file keeps E20 at T2 ("credited screen value / branch-A lever"); this draft
  does not edit the register, and it records E20 as *bounded by the width budget at the
  primary conventions*, not closed. The register's optimistic estimate exceeds 10× only with
  at least 15× the logical width [REG].

### 7.3 Outside the claim, not closed"""),

("N3-3+N3-4:section-8-thresholds",
"""  takes at most 9.9 reaction layers and 9.9e5 T (explicit) or 2.9 layers and 2.9e5 T
  (certified). Any design above either limit is covered by the claim.""",
"""  takes at most 9.9 reaction layers and 9.9e5 T (explicit) or 2.9-5.7 layers and
  2.9e5-5.7e5 T (certified; the upper values with direction-select). Any design above either
  limit at the binding cell (for the certified class, the 5.7 / 5.7e5 values if
  direction-select is granted and 2.9 / 2.9e5 if not), and above the corresponding per-cell
  limit in the other decision cells (B4x12 $0.001: 1.1 layers / 1.1e5 T for the explicit
  constant; §3), is covered by the claim."""),

("N3-1:section-8-rigour",
"""  - The N1 card justifies R1 over R2 by the primary margin of at least 30×, which holds
    under every reading of the primary (≥ 104.4 explicit, ≥ 400.7 certified).""",
"""  - The N1 card justifies R1 over R2 by the primary margin of at least 30×. Taken one at a
    time, the readings of the primary give ≥ 104.4 (explicit) and ≥ 400.7 (certified). The
    lowest combination of two readings, the strict zero-bias reading with direction-select,
    gives certified 200.4 and explicit ≈ 90, or ≈ 66 at failure 0.01 (mod, derived, q+; the
    explicit values approximate) [RK]. The margin stays above 30× in each case (§5.1)."""),

("N3-8:section-8-heading",
"""- **Undisclosed-in-v1 quantum-favourable conventions** (each strengthens the negative):""",
"""- **Further quantum-favourable conventions** (each strengthens the negative):"""),

("N3-6:appendix-A-map",
"""- **§7.2 (bounded at the primary conventions):** F05 (T2 in the register).""",
"""- **§7.2 (bounded at the primary conventions):** F05 and E20 (both T2 in the register)."""),

("N3-6:appendix-A-count",
"""reads three dispositions differently from the register, and records one wording correction:""",
"""reads four dispositions differently from the register, and records one wording correction:"""),

("N3-6:appendix-A-E20",
"""  credit") no longer exists after run002; this draft treats it as open with F20 (§7.3).""",
"""  credit") no longer exists after run002; this draft treats it as open with F20 (§7.3).
- **E20** stays T2 in the register; this draft treats it as bounded by the width budget at
  the primary conventions (lane credit 1.00× at the binding cell), not closed (§7.2)."""),

("cons:appendix-B",
"""6. **This revision:** `research/plan110_n1/fixer/fixer_numbers.py` [FX], then
   `fixer_numbers_2.py` [FX2]. Rows are in `results/plan110_n1/fixer/rows.jsonl`, and the
   defect-to-fix map is `results/plan110_n1/fixer/fix_map.json`.""",
"""6. **v2 revision:** `research/plan110_n1/fixer/fixer_numbers.py` [FX], then
   `fixer_numbers_2.py` [FX2]. Rows are in `results/plan110_n1/fixer/rows.jsonl`, and the
   defect-to-fix map is `results/plan110_n1/fixer/fix_map.json`.
7. **N2 re-check of v2:** `research/plan110_n1/recheck/recheck_draft.py` [RK]. The report is
   `results/plan110_n1/recheck/RECHECK.md`.
8. **This revision (v3):** `research/plan110_n1/v3/v3_numbers.py` [V3]; then
   `research/plan110_n1/v3/build_v3.py`, which writes this file from v2 by exact, counted
   replacements; then the self-check `research/plan110_n1/v3/check_v3.py`. Outputs and rows
   are in `results/plan110_n1/v3/`."""),

("cons:changelog-v3",
"""| Review method note | n/a | §9.2 item 13 (now 15) says "confirmed by derived arithmetic" in [DC], not by a headline rerun | §9.2 item 15 |
""",
"""| Review method note | n/a | §9.2 item 13 (now 15) says "confirmed by derived arithmetic" in [DC], not by a headline rerun | §9.2 item 15 |

## Changelog v3 (v2 → v3)

Defect numbers N3-1 to N3-8 are those of `results/plan110_n1/recheck/RECHECK.md`, the
AI-assisted N2 re-check of v2. New numbers are from [RK] `probes`; the per-cell certified
limits with direction-select and the inputs 379.3 [ES], 0.864 [DC] and 114 / 112 / 724 [HT]
are collected in [V3], which re-derives every probe value it uses from the primary files and
matches it to float precision (largest relative difference 1.4e-16). No v3 change alters the
claim, the verdict or the R1 justification.

| Defect | Severity | Fix in v3 | Where |
|---|---|---|---|
| N3-1 | minor | The "under every reading" floors (≥ 400.7 certified, ≥ 104.4 explicit) are now stated as holding "taken one at a time". The lowest combination of two readings of the primary, the strict zero-bias reading with direction-select, is added (mod, derived, q+): certified M = 200.4 (k = 379.3 at e = ε); best explicit M ≈ 90, or ≈ 66 at failure 0.01, labelled approximate (the zero-bias values × the 0.864 direction-select ratio, since [HT] has no explicit direction-select k at e = ε). All stay above 30× | §5.1 readings table (new last row) and verdict; §8 "Rigour level" |
| N3-2 | minor | "Any one of these … reaches or nearly reaches M = 1" restricted to the first two items, distribution-free (0.31) and one lane (1.125). The other two are quoted: all-free + 1e13 T/s gives 11.3 (D_eff only 114 → 112 layers); all-free + 10 ns gives 7.3 (supply-bound at 724 layers of 10 ns) | §6 lever 3 |
| N3-3 | minor | The thresholds are marked as binding-cell limits. Per-cell explicit limits added (B4x12 $0.001: 1.14 layers / 1.1e5 T; B4x12 $0.01: 0.53 / 5.3e4; B8x52 $0.01: 2.43 / 2.4e5; certified lower still), and coverage now also requires the iterate to be above the corresponding per-cell limit in the other decision cells (B4x12 $0.001: 1.1 layers / 1.1e5 T). The B4x12 all-free floor (94 layers) is noted, so nothing changes in practice | §1 scope item 1; §3 item 3; §8 |
| N3-4 | minor | The certified-class threshold is quoted with its direction-select value, 2.9-5.7 layers and 2.9e5-5.7e5 T (all-free floor 20-40× above). §8 states which value applies for coverage (5.7 / 5.7e5 if direction-select is granted, 2.9 / 2.9e5 if not) | Abstract; §1 scope item 1; §6 lever 2; §8 |
| N3-5 | minor | Abstract row relabelled "Best explicit worst-case constant (U1 + U2 + non-dyadic M)", with the direction-select values added as in the certified row: 200.4 (primary) and about 5.43 (symmetric, derived) | Abstract table |
| N3-6 | minor | E20 moved out of §7.1 "Closed" into §7.2 "Bounded at the primary conventions": register T2 ("credited screen value / branch-A lever"), kill rule "State the width bound … and stop", lane credit 1.00× at the binding cell. Appendix A now says the draft reads four dispositions differently from the register and lists E20 | §7.1; §7.2; Appendix A |
| N3-7 | minor | The q+ label moved to the admission clause ("admission: mod, q+"); keeping e = 0.45ε is now marked q− relative to the strict zero-bias reading | §2 conventions table |
| N3-8 | minor | Two body sentences that attributed the primary convention to a person now say "the primary convention fixed in [W0C]"; the §8 heading that referred to draft history is now "Further quantum-favourable conventions"; the §5.1 k for "Best explicit with direction-select" is 170.7 [ES] instead of n/a; the front matter now records the re-check and says the v3 edits were checked only by `check_v3.py` | Front matter; Abstract; §4.3; §5.1 table; §8 |

Consequential edits, not defects: the title line (v3); the number rule and provenance
sentences now name the re-check and v3 scripts; source keys [RK] and [V3] added, and [FX] /
[FX2] relabelled "v2 revision"; Appendix B items 6-8.
"""),
]


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    out_path = V3
    if "--out" in sys.argv:
        out_path = sys.argv[sys.argv.index("--out") + 1]
    raw = open(V2, "rb").read()
    v2_sha = sha_bytes(raw)
    if v2_sha != V2_SHA:
        sys.exit(f"v2 sha256 {v2_sha} != expected {V2_SHA}; refusing to build")
    text = raw.decode("utf-8")
    applied = []
    for tag, old, new in R:
        n = text.count(old)
        if n != 1:
            sys.exit(f"{tag}: expected exactly 1 occurrence in the working text, found {n}")
        text = text.replace(old, new, 1)
        applied.append(tag)
    data = text.encode("utf-8")
    with open(out_path, "xb") as fh:  # exclusive create
        fh.write(data)
    v3_sha = sha_bytes(data)
    if out_path == V3:
        with open(ROWS, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"ws": "v3", "sub": "build_v3", "v2": V2, "v2_sha256": v2_sha,
                                 "v3": V3, "v3_sha256": v3_sha, "replacements": applied,
                                 "n_replacements": len(applied), "python": sys.version.split()[0],
                                 "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site,
                                           "dont_write_bytecode": sys.flags.dont_write_bytecode},
                                 "label": "text build"}) + "\n")
    print("wrote", out_path, "sha256", v3_sha, "replacements", len(applied))


if __name__ == "__main__":
    main()
