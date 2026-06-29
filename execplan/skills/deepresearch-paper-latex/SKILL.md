---
name: deepresearch-paper-latex
description: "Use when a writer or operator needs to (re)build a quest's paper PDF from an already-recorded Markdown manuscript with BibTeX references, embedded figures, and a venue style — triggers like \"compile the paper\", \"recompile\", \"build the PDF\", \"render report\". Keywords: render report, paper-latex, --venue, --bib, paper-en artifact, BibTeX, includegraphics, iclr2026, osdi2026, ctexart, CJK/ZH edition, Missing character, empty .bbl. NOT for writing prose, running experiments, or finalizing."
---

# deepresearch-paper-latex (compile manuscript → PDF)

## Overview
Compiles a finished Markdown manuscript into a publication PDF via LaTeX, with a real venue style, BibTeX-generated numbered references, and embedded figures. It is a thin wrapper over the `$HARNESS render report` command (backed by an internal runtime adapter) that emits an additive report artifact only.

## When to Use
- Trigger: "compile / recompile the paper / build the PDF" from a manuscript markdown that **already exists** (claims/figures/references already recorded).
- Use when the writer or operator needs to (re)build the paper PDF from already-recorded claims/figures/references.
- **When NOT to use:** do not use for writing prose, running experiments, recording new claims, or finalizing/routing — those belong elsewhere. This skill is quest-isolated and never mutates results/claims or finalizes. If a defective render is detected, fix the manuscript/template (not this skill's scope to invent content).

## Workflow
1. Confirm the manuscript markdown exists at `runs/<q>/report/paper.md` and that claims/figures/references are already recorded (this skill does not author content).
2. Decide the venue: normally **OMIT `--venue`** and let the venue policy choose (see Venue-Template Policy). Pass `--venue <name>` only for an explicit override or `--venue generic` for a plain `article`.
3. Verify the manuscript follows the Source Conventions (math in math mode, Pandoc `[@bibkey]` citations, no hand-written reference list) — else the render is defective.
4. Run the `render report` command (see Command) with `--bib` to get a real BibTeX pass and numbered References; figures referenced as `.pdf` embed via `\includegraphics`. ZH edition uses the same flags (CJK auto).
5. **Verify (MANDATORY before reporting done):** open the produced PDF and read the `.log` — confirm no `Missing character`, exactly one non-empty References section, and equations/symbols render (see Verify gate).
6. Report the PDF artifact(s). If any verify check fails, report `status=failed` plus which check failed rather than claiming success on a broken PDF.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Command (the `use`)
```
$HARNESS --via skill:deepresearch-paper-latex:<role> render report --quest-id <q> --artifact-id <q>:paper-en \
  --ref runs/<q>/report/paper.pdf --input runs/<q>/report/paper.md \
  --bib runs/<q>/refs/references.bib [--venue <name>]
```
- `--bib` triggers a real BibTeX pass (numbered References); figures referenced as `.pdf` embed via `\includegraphics`. ZH edition: same flags (CJK auto).
- **The flag is `--venue <name>` (NOT `--params '{"venue":...}'`).** See the venue policy below — you normally OMIT it and let the policy choose.
- `--via skill:deepresearch-paper-latex:<role>` records a `skill-invocation` audit artifact. Keep this audit stamp exactly as written.

> Note: the `--via` stamp keeps the original `skill:deepresearch-paper-latex:<role>` id (the runtime-adapter identity), preserved verbatim from the source.

## Venue-Template Policy (DeepScientist — a paper is drafted in a REAL venue template by default)
- **Default-on.** `render report` ALWAYS compiles against a real venue template; it never silently emits a generic Pandoc `article`. Selection precedence: **explicit `--venue` > `paper_spine.venue_style` > `quest.domain` > `iclr2026`** (general ML/AI default).
- **Systems papers use a systems venue.** Architecture/GPU/kernel/OS/perf work resolves to a systems template (ASPLOS is ideal; if its `acmart` class is unavailable the closest renderable systems venue — USENIX `osdi2026`/`nsdi2027` — is chosen). General ML/AI with no stronger signal → `iclr2026`.
- **Generic is explicit-only.** Plain `article` requires `--venue generic`. Without it, a venue is enforced.
- **No silent fallback.** If the chosen venue fails to compile, the render FAILS LOUDLY (the command errors and records no artifact) with the LaTeX error — fix the template/source (e.g. two-column venues reject `longtable`; use full-width `table*` floats) or pass `--venue generic`. Do not paper over it.
- Renderable-in-this-toolchain venues: `iclr2026`, `neurips2025`, `osdi2026`, `nsdi2027` (others need extra CTAN/class packages; an explicit `--venue` to one of those will report the missing dependency, not silently downgrade).
- **CJK / ZH edition:** a Chinese manuscript renders in `ctexart`, and the venue suites are Latin-conference STYLE packages (Times/Helvetica fonts + `\@maketitle`/`\parskip`/header redefs for `article`). Bolting one onto `ctexart` **corrupts the layout** (title overprint, heading collisions, CJK fonts fight Times). So a CJK edition is rendered in clean `ctexart` WITHOUT the Latin venue style — recorded explicitly in the result meta (`cjk_venue_skipped`), not a silent downgrade. English-conference venues have no CJK edition.

## Source Conventions (the manuscript markdown MUST follow these — else the render is defective)
- **Math in math mode, never raw Unicode in body text.** Write `$\rho$`, `$\le 10\%$`, `$S \ge 16384$`, `$T_{\mathrm{TC}}$`, display equations in `$$…$$` / `\[…\]` / an `equation`/`align` env. Raw glyphs (ρ ≤ ≥ ≈ ↔ × · −) in plain text are dropped by the default font (the adapter injects a `newunicodechar` safety net, but math mode is the correct form and gives real subscripts/superscripts).
- **Cite with Pandoc `[@bibkey]`**, never hand-write the reference list. With `--bib`, BibTeX generates the References from the `.bib`; a hand-written `## References` section causes a **duplicate + empty** bibliography (the bibtex one is empty because nothing was `\cite`d). Cite every entry you want to appear at least once.

## Verify Gate (MANDATORY before reporting done — the adapter now fails a defective render, but check anyway)
- The adapter raises (command fails, no artifact recorded) on `Missing character` in the `.log` or an empty `.bbl` when a `.bib` was given. Treat a failed `render report` as a real defect to fix, not a flake.
- Open the produced PDF + read the `.log`: confirm (a) no `Missing character`, (b) exactly one non-empty References section (no leaked `bibkey` text, no duplicate), (c) equations/symbols render. Report defects (`status=failed` + which check) rather than claiming success on a broken PDF.

## Boundaries / Audit
- Additive output only; assert only `supported` claims; keep loop/operator wording out (run `manuscript validate`). `--via` records a `skill-invocation` audit artifact. Quest-isolated. Never mutates results/claims or finalizes.

## Stop
- Produce the PDF artifact(s); routing/finalize stay the orchestrator's.

## Common Mistakes
- **Passing `--params '{"venue":...}'` instead of `--venue <name>`.** The venue flag is `--venue <name>`; the params form is wrong.
- **Forcing `--venue` when you should omit it.** Normally OMIT `--venue` and let the policy choose; only override explicitly when needed.
- **Expecting a generic `article` by default.** A venue is always enforced; plain `article` is explicit-only via `--venue generic`.
- **Papering over a compile failure.** A failed render means fix the template/source (e.g. two-column venues reject `longtable` → use full-width `table*`) or pass `--venue generic` — never silently downgrade or accept no artifact.
- **Bolting a Latin venue style onto a CJK/ZH manuscript.** It corrupts the layout; render ZH in clean `ctexart` (recorded as `cjk_venue_skipped`), no English venue style.
- **Raw Unicode glyphs (ρ ≤ ≥ ≈ ↔ × · −) in body text.** They drop from the default font — use math mode.
- **Hand-writing the reference list.** With `--bib`, BibTeX generates References; a manual `## References` causes a duplicate + empty bibliography. Cite every wanted entry at least once with `[@bibkey]`.
- **Claiming success on a broken PDF.** Always run the verify gate; report `status=failed` + the failing check rather than reporting done.
- **Mutating results/claims, writing prose, or finalizing.** Out of scope — additive PDF render only; routing/finalize stay the orchestrator's.

## Rationalization / Red-Flags Table
| Rationalization an agent might make | Reality (do this instead) |
| --- | --- |
| "The venue failed to compile, I'll just let it fall back to `article`." | No silent fallback. Fix the template/source or pass `--venue generic` explicitly. |
| "I'll add `--venue iclr2026` to be safe." | Normally OMIT `--venue`; the policy chooses. Only override deliberately. |
| "ZH manuscript should still get the conference style for consistency." | A Latin venue style corrupts `ctexart` layout. Render clean `ctexart`, record `cjk_venue_skipped`. |
| "I'll hand-write a `## References` section so it's there for sure." | With `--bib` this duplicates + empties the bibliography. Cite with `[@bibkey]` only. |
| "A few raw ≤/ρ glyphs in text are fine; the safety net catches them." | Math mode is the correct form. Raw glyphs in body text are a defect. |
| "The PDF opened, that's good enough — skip the log." | Verify is MANDATORY: check no `Missing character`, one non-empty References, symbols render. |
| "render report errored — probably a flake, rerun and move on." | The adapter fails LOUDLY on real defects. Treat it as a defect to fix, not a flake. |
