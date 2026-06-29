---
name: deepresearch-paper-craft
description: Manuscript-writing craft for the outline/write stages — the oral-writing principles, the section-rewrite checklist, the paper-view/evidence-view outline contract, plus outline patterns, oral-package patterns, and experiment-analysis writing patterns. Use when the writer is drafting or rewriting manuscript prose, building or validating the outline, or shaping how evidence reads in the paper. Read-only methodology lookup; surfaces a reference pack and changes no state. (For compiling the manuscript to PDF use paper-latex; for figures use figure; for data-availability polish use manuscript-aux.)
---

# paper-craft (read-only methodology lookup)

Surfaces the `paper-craft` reference pack for the **writer** during the outline/write stages of the loop.
The pack is the source of truth; this skill only indexes and points into it, and makes no state change.

## Use
1. Index the pack:
   `$HARNESS --via skill:deepresearch-paper-craft:<your-role> knowledge cards --query oral_writing_principles`
   (or `knowledge query --kind reference`).
2. Read the relevant file under `execplan/packs/paper-craft/references/` and apply the method:
   - `references/oral_writing_principles.md` — the oral-writing principles.
   - `references/section_rewrite_checklist.md` — the section-rewrite checklist.
   - `references/outline-contract.md` — the paper-view/evidence-view outline contract;
     `references/outline-patterns.md` — supporting outline patterns.
   - `references/oral_package_patterns.md`, `references/experiments_analysis_patterns.md` — patterns for the
     oral package and for writing up experiments/analysis.
3. Do the stage work and record outcomes through your role's normal skill/commands. The DB stays canonical;
   this craft is advisory, never an authoritative state surface. Map any external tool names in the
   files (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface.

## LaTeX-safe authoring conventions (REQUIRED — the manuscript is compiled to PDF via paper-latex)
The markdown you write is rendered through Pandoc → LaTeX. Author it so it survives that path:
- **Math in math mode.** Every variable, Greek letter, inequality, arrow, and equation goes in `$…$`,
  display `$$…$$` / `\[…\]`, or an `equation`/`align` environment — with real subscripts/superscripts
  (`$T_{\mathrm{TC}}$`, `$\rho \to 1$`, `$S \ge 16384$`, `$\le 10\%$`). **Never** paste raw Unicode math
  (ρ ≤ ≥ ≈ ↔ × · −) into body text: the default LaTeX font drops those glyphs and they vanish from the PDF.
- **Cite with Pandoc `[@bibkey]`**, and let BibTeX build the bibliography. **Never** hand-write a
  `## References` list when a `.bib` is used — it produces a duplicate, and the real (bibtex) bibliography
  comes out empty because nothing was cited. Make sure each reference you intend to show is `[@cited]`.
- **Verify the compiled artifact, not just the markdown.** After paper-latex runs, confirm the PDF/`.log`
  have no `Missing character`, exactly one non-empty References section (no leaked `bibkey` text, no
  duplicate), and correctly rendered symbols/equations. Report defects (`status=failed`) rather than
  claiming success on a broken PDF. (paper-latex now fails the render on these defects — fix, don't bypass.)
- **Draft for a real venue template.** Papers compile inside a real venue template by default (auto-selected:
  explicit > paper_spine.venue_style > domain > `iclr2026`; systems work → a systems venue like `osdi2026`).
  Set `paper_spine.venue_style` to the intended venue family. Generic `article` is an explicit opt-out only
  (`--venue generic`). Author content the venue can typeset — e.g. two-column systems venues need wide tables
  as full-width `table*` floats, not `longtable`.

## Audit / boundaries
- `--via skill:deepresearch-paper-craft:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.

## Stop
- Return the method to the calling task and continue.
