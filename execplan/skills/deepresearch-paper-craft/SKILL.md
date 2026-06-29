---
name: deepresearch-paper-craft
description: Use when a writer is drafting or rewriting manuscript prose, building or validating an outline, or shaping how experiments/evidence read in the paper during the outline/write stages of the deepresearch loop. Keywords - paper-craft, oral_writing_principles, section_rewrite_checklist, outline-contract, paper-view, evidence-view, oral_package_patterns, experiments_analysis_patterns, LaTeX-safe authoring, Pandoc, venue_style, paper_spine, manuscript prose, writer role, knowledge cards. Read-only methodology lookup; changes no state.
---

# deepresearch-paper-craft

## Overview
A read-only methodology lookup for the **writer** during the outline/write stages of the deepresearch loop: it surfaces the `paper-craft` methodology reference (oral-writing principles, section-rewrite checklist, the paper-view/evidence-view outline contract, plus outline, oral-package, and experiment-analysis patterns) and enforces LaTeX-safe authoring conventions. It indexes and applies craft; it never mutates state.

## When to Use
- You are the **writer** drafting or rewriting manuscript prose.
- You are building or validating the **outline** (paper-view / evidence-view contract).
- You are shaping how **evidence / experiments / analysis** reads in the paper.
- You want the oral-writing principles or the section-rewrite checklist before editing a section.

**When NOT to use:**
- To compile the manuscript to PDF — use `paper-latex`.
- To produce or fix figures — use `figure`.
- For data-availability polish — use `manuscript-aux`.
- To finalize, mutate results, confirm GPU, or change quest state — this skill is advisory only and is not an authoritative state surface. The DB stays canonical.

## Workflow
1. **Index the methodology reference.** Run the audit-stamped lookup to find the relevant cards:
   `$HARNESS --via skill:deepresearch-paper-craft:<your-role> knowledge cards --query oral_writing_principles`
   (or `$HARNESS --via skill:deepresearch-paper-craft:<your-role> knowledge query --kind reference`).
2. **Read the relevant reference file** in this skill's own `references/` folder and apply the method (see "Reference Pages" below for the file-to-purpose map).
3. **Map external tool names** found in the reference pages (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface as you apply them.
4. **Author LaTeX-safe.** Follow "LaTeX-safe Authoring Conventions" below for every piece of prose — the markdown is compiled to PDF via `paper-latex` through Pandoc → LaTeX.
5. **Verify the compiled artifact, not just the markdown,** after `paper-latex` runs (no `Missing character`, exactly one non-empty References section, correctly rendered symbols/equations). Report `status=failed` on a broken PDF rather than claiming success.
6. **Do the stage work and record outcomes through your role's normal skill/commands.** This craft is advisory; the DB stays canonical.
7. **Return the method to the calling task and continue.**

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands and constraints in this skill, then execute it.

## Reference Pages
Read the relevant page in this skill's own `references/` folder and apply the method:
- [`references/oral_writing_principles.md`](references/oral_writing_principles.md) — the oral-writing principles.
- [`references/section_rewrite_checklist.md`](references/section_rewrite_checklist.md) — the section-rewrite checklist.
- [`references/outline-contract.md`](references/outline-contract.md) — the paper-view/evidence-view outline contract.
- [`references/outline-patterns.md`](references/outline-patterns.md) — supporting outline patterns.
- [`references/oral_package_patterns.md`](references/oral_package_patterns.md) — patterns for the oral package.
- [`references/experiments_analysis_patterns.md`](references/experiments_analysis_patterns.md) — patterns for writing up experiments/analysis.

These pages live in this skill's `references/` folder; the same craft is also available at runtime via `$HARNESS knowledge cards`. This skill makes no state change.

## LaTeX-safe Authoring Conventions (REQUIRED)
The manuscript is compiled to PDF via `paper-latex`; the markdown you write is rendered through Pandoc → LaTeX. Author it so it survives that path:
- **Math in math mode.** Every variable, Greek letter, inequality, arrow, and equation goes in `$…$`, display `$$…$$` / `\[…\]`, or an `equation`/`align` environment — with real subscripts/superscripts (`$T_{\mathrm{TC}}$`, `$\rho \to 1$`, `$S \ge 16384$`, `$\le 10\%$`). **Never** paste raw Unicode math (ρ ≤ ≥ ≈ ↔ × · −) into body text: the default LaTeX font drops those glyphs and they vanish from the PDF.
- **Cite with Pandoc `[@bibkey]`**, and let BibTeX build the bibliography. **Never** hand-write a `## References` list when a `.bib` is used — it produces a duplicate, and the real (bibtex) bibliography comes out empty because nothing was cited. Make sure each reference you intend to show is `[@cited]`.
- **Verify the compiled artifact, not just the markdown.** After paper-latex runs, confirm the PDF/`.log` have no `Missing character`, exactly one non-empty References section (no leaked `bibkey` text, no duplicate), and correctly rendered symbols/equations. Report defects (`status=failed`) rather than claiming success on a broken PDF. (paper-latex now fails the render on these defects — fix, don't bypass.)
- **Draft for a real venue template.** Papers compile inside a real venue template by default (auto-selected: explicit > paper_spine.venue_style > domain > `iclr2026`; systems work → a systems venue like `osdi2026`). Set `paper_spine.venue_style` to the intended venue family. Generic `article` is an explicit opt-out only (`--venue generic`). Author content the venue can typeset — e.g. two-column systems venues need wide tables as full-width `table*` floats, not `longtable`.

## Common Mistakes
- **Treating this craft as a state surface.** It is read-only and advisory; never finalize, mutate results, confirm GPU, or change quest state from here. Record outcomes through your role's normal skill/commands — the DB stays canonical.
- **Pasting raw Unicode math into body text.** Those glyphs drop from the PDF. Put all math in math mode with real subscripts/superscripts.
- **Hand-writing a `## References` list while a `.bib` is in use.** This produces a duplicate and an empty real bibliography. Cite with `[@bibkey]` and let BibTeX build it.
- **Claiming success on the markdown without checking the compiled PDF.** Verify the artifact: no `Missing character`, exactly one non-empty References section, correct symbols/equations. Report `status=failed` on a broken PDF.
- **Authoring for generic `article` by default.** Draft for a real venue template; set `paper_spine.venue_style`. Generic `article` is an explicit opt-out only. Give two-column systems venues full-width `table*` floats, not `longtable`.
- **Forgetting to map external tool names.** Map `artifact.*`, `memory.*`, `bash_exec` in the reference pages onto the `$HARNESS` surface.

## Audit / Boundaries
- `--via skill:deepresearch-paper-craft:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.
