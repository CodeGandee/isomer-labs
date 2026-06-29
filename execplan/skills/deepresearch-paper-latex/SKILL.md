---
name: deepresearch-paper-latex
description: Compiles a finished Markdown manuscript into a publication PDF via LaTeX with BibTeX references, embedded figures, and an optional venue style. Use when the writer or operator needs to (re)build the paper PDF from already-recorded claims/figures/references — not for writing prose, running experiments, or finalizing. Thin wrapper over `render report` (paper-latex pack); emits an additive report artifact only.
---

# paper-latex (compile manuscript → PDF)

Trigger: "compile / recompile the paper / build the PDF" from a manuscript markdown that already exists.

## use
`$HARNESS --via skill:deepresearch-paper-latex:<role> render report --quest-id <q> --artifact-id <q>:paper-en \
  --ref runs/<q>/report/paper.pdf --input runs/<q>/report/paper.md \
  --bib runs/<q>/refs/references.bib [--venue <name>]`
- `--bib` triggers a real BibTeX pass (numbered References); figures referenced as `.pdf` embed via `\includegraphics`. ZH edition: same flags (CJK auto).
- **The flag is `--venue <name>` (NOT `--params '{"venue":...}'`).** See the venue policy below — you normally OMIT it and let the policy choose.

## venue-template policy (DeepScientist — a paper is drafted in a REAL venue template by default)
- **Default-on.** `render report` ALWAYS compiles against a real venue template; it never silently emits a
  generic Pandoc `article`. Selection precedence: **explicit `--venue` > `paper_spine.venue_style` >
  `quest.domain` > `iclr2026`** (general ML/AI default).
- **Systems papers use a systems venue.** Architecture/GPU/kernel/OS/perf work resolves to a systems template
  (ASPLOS is ideal; if its `acmart` class is unavailable the closest renderable systems venue — USENIX
  `osdi2026`/`nsdi2027` — is chosen). General ML/AI with no stronger signal → `iclr2026`.
- **Generic is explicit-only.** Plain `article` requires `--venue generic`. Without it, a venue is enforced.
- **No silent fallback.** If the chosen venue fails to compile, the render FAILS LOUDLY (the command errors
  and records no artifact) with the LaTeX error — fix the template/source (e.g. two-column venues reject
  `longtable`; use full-width `table*` floats) or pass `--venue generic`. Do not paper over it.
- Renderable-in-this-toolchain venues: `iclr2026`, `neurips2025`, `osdi2026`, `nsdi2027` (others need extra
  CTAN/class packages; an explicit `--venue` to one of those will report the missing dependency, not silently
  downgrade).
- **CJK / ZH edition:** a Chinese manuscript renders in `ctexart`, and the venue suites are Latin-conference
  STYLE packages (Times/Helvetica fonts + `\@maketitle`/`\parskip`/header redefs for `article`). Bolting one
  onto `ctexart` **corrupts the layout** (title overprint, heading collisions, CJK fonts fight Times). So a
  CJK edition is rendered in clean `ctexart` WITHOUT the Latin venue style — recorded explicitly in the
  result meta (`cjk_venue_skipped`), not a silent downgrade. English-conference venues have no CJK edition.

## source conventions (the manuscript markdown MUST follow these — else the render is defective)
- **Math in math mode, never raw Unicode in body text.** Write `$\rho$`, `$\le 10\%$`, `$S \ge 16384$`,
  `$T_{\mathrm{TC}}$`, display equations in `$$…$$` / `\[…\]` / an `equation`/`align` env. Raw glyphs
  (ρ ≤ ≥ ≈ ↔ × · −) in plain text are dropped by the default font (the adapter injects a `newunicodechar`
  safety net, but math mode is the correct form and gives real subscripts/superscripts).
- **Cite with Pandoc `[@bibkey]`**, never hand-write the reference list. With `--bib`, BibTeX generates the
  References from the `.bib`; a hand-written `## References` section causes a **duplicate + empty** bibliography
  (the bibtex one is empty because nothing was `\cite`d). Cite every entry you want to appear at least once.

## verify (MANDATORY before reporting done — the adapter now fails a defective render, but check anyway)
- The adapter raises (command fails, no artifact recorded) on `Missing character` in the `.log` or an empty
  `.bbl` when a `.bib` was given. Treat a failed `render report` as a real defect to fix, not a flake.
- Open the produced PDF + read the `.log`: confirm (a) no `Missing character`, (b) exactly one non-empty
  References section (no leaked `bibkey` text, no duplicate), (c) equations/symbols render. Report defects
  (`status=failed` + which check) rather than claiming success on a broken PDF.

## boundaries / audit
- Additive output only; assert only `supported` claims; keep loop/operator wording out (run `manuscript validate`). `--via` records a `skill-invocation` audit artifact. Quest-isolated. Never mutates results/claims or finalizes.

## stop
- Produce the PDF artifact(s); routing/finalize stay the orchestrator's.
