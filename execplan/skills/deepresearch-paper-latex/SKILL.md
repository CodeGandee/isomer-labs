---
name: deepresearch-paper-latex
description: Compiles a finished Markdown manuscript into a publication PDF via LaTeX with BibTeX references, embedded figures, and an optional venue style. Use when the writer or operator needs to (re)build the paper PDF from already-recorded claims/figures/references — not for writing prose, running experiments, or finalizing. Thin wrapper over `render report` (paper-latex pack); emits an additive report artifact only.
---

# paper-latex (compile manuscript → PDF)

Trigger: "compile / recompile the paper / build the PDF" from a manuscript markdown that already exists.

## use
`$HARNESS --via skill:deepresearch-paper-latex:<role> render report --quest-id <q> --artifact-id <q>:paper-en \
  --ref runs/<q>/report/paper.pdf --input runs/<q>/report/paper.md \
  --bib runs/<q>/refs/references.bib --venue iclr2026`
- `--bib` triggers a real BibTeX pass (numbered References); `--venue` compiles against the venue suite; figures referenced as `.pdf` embed via `\includegraphics`. ZH edition: same without `--venue` (CJK auto).
- Confirm the produced PDF embeds figures and bibliography (not a text-only fallback).

## boundaries / audit
- Additive output only; assert only `supported` claims; keep loop/operator wording out (run `manuscript validate`). `--via` records a `skill-invocation` audit artifact. Quest-isolated. Never mutates results/claims or finalizes.

## stop
- Produce the PDF artifact(s); routing/finalize stay the orchestrator's.
