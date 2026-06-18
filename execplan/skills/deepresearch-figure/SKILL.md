---
name: deepresearch-figure
description: Creates or polishes a publication figure from recorded quest data, routing to one of three compiler-pack-backed actions — plot (line/bar/scatter from numeric arrays/CSV), nature (Nature/high-impact figure), or polish (render-inspect-revise QA on an existing figure). Use when the writer needs a chart from data, a Nature-style figure, or a QA pass on a finished figure. Emits additive figure artifacts only; never mutates science or finalizes.
---

# figure (create / polish a figure)

Trigger: "make a figure/plot from this data", "Nature-style figure", or "polish/QA this figure". Pick the action; each is a thin wrapper over the existing render command. Always render to `.pdf` (vector, embeds via `\includegraphics`).

## actions
- `plot`   → `render plot`   (paper-plot)    — line/bar/scatter from data. See actions/plot.md.
- `nature` → `render figure` (nature-figure) — Nature/high-impact figure. See actions/nature.md.
- `polish` → `render polish` (figure-polish) — QA an existing figure. See actions/polish.md.

## audit / boundaries
- Invoke as `--via skill:deepresearch-figure/<action>:<role>` so the exact pack identity is preserved in the audit.
- Additive figure artifacts only; never mutates science or finalizes. Quest-isolated.
