---
name: deepresearch-figure
description: "Use when a writer or figure role needs to create or QA a publication figure from recorded quest data — line/bar/scatter plot from numeric arrays or CSV, a Nature/high-impact figure, or a render-inspect-revise polish/QA pass on an existing figure. Keywords: render plot, render figure, render polish, paper-plot, nature-figure, figure-polish, fig-<name>, runs/<q>/figures, .pdf figure, includegraphics, scatter/bar/line kind."
---

# deepresearch-figure

## Overview
Create or polish a publication figure from recorded quest data by routing to one of three render actions (plot, nature, polish), each a thin wrapper over the harness render command. Emits additive figure artifacts only; never mutates science or finalizes.

## When to Use
Trigger this skill when the request is one of:
- "make a figure/plot from this data" — numeric arrays or CSV → line/bar/scatter chart (`plot`).
- "Nature-style figure" / high-impact figure for a top venue (`nature`).
- "polish/QA this figure" — render-inspect-revise pass on an existing figure (`polish`).

When NOT to use:
- Do not use to mutate science, change recorded results, or finalize/dispatch a deliverable — this skill is additive and figure-only.
- Do not use across quest boundaries; every artifact is quest-isolated to the quest whose data you were given.
- If the task is not a figure create/QA request, use the appropriate science/writing skill instead.

## Workflow
1. Pick the action that matches the request: `plot`, `nature`, or `polish` (see Actions / Commands).
2. Always render to `.pdf` — it is vector and embeds into the manuscript via `\includegraphics`.
3. Choose artifact + ref paths by convention: artifact id `<q>:fig-<name>` (polish uses `<q>:fig-<name>-p`), output ref under `runs/<q>/figures/<name>.pdf`.
4. Run the action's harness command verbatim, substituting `<role>`, `<q>`, `<name>`, and inputs. Keep the `--via skill:deepresearch-figure/<action>:<role>` audit stamp exactly so the render-adapter identity is preserved in the audit.
5. For `plot`, pick `--kind` to match the data (predicted-vs-measured → `scatter`; ablation → `bar`; trend over a variable → `line`).
6. For `nature`, fill the figure-contract and run the qa-contract checklist — nature domain (see [`references/figure-contract.md`](references/figure-contract.md) and [`references/qa-contract.md`](references/qa-contract.md)).
7. For `polish`, run the self-review checklist (see [`references/figure-polish-checklist.md`](references/figure-polish-checklist.md)); the house style removes frames/spines.
8. If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Actions / Commands
Each action is a thin wrapper over the existing render command. Always render to `.pdf`.

### plot — paper-plot → matplotlib vector figure
Line/bar/scatter from numeric arrays or CSV.
```
$HARNESS --via skill:deepresearch-figure/plot:<role> render plot --quest-id <q> --artifact-id <q>:fig-<name> \
  --ref runs/<q>/figures/<name>.pdf --input <data.json|csv> --kind scatter|bar|line [--y-label <l>]
```
Render to `.pdf` so it embeds. Pick `--kind` to match the data (predicted-vs-measured → scatter; ablation → bar).

### nature — nature-figure → Nature/high-impact figure
```
$HARNESS --via skill:deepresearch-figure/nature:<role> render figure --quest-id <q> --artifact-id <q>:fig-<name> \
  --ref runs/<q>/figures/<name>.pdf --input <data>
```
Fill the figure-contract and run the qa-contract checklist (see [`references/figure-contract.md`](references/figure-contract.md) and [`references/qa-contract.md`](references/qa-contract.md)). Nature domain; render to `.pdf`.

### polish — figure-polish → render-inspect-revise QA on an existing figure
```
$HARNESS --via skill:deepresearch-figure/polish:<role> render polish --quest-id <q> --artifact-id <q>:fig-<name>-p \
  --ref runs/<q>/figures/<name>-polished.pdf --input runs/<q>/figures/<name>.pdf
```
Run the self-review checklist (see [`references/figure-polish-checklist.md`](references/figure-polish-checklist.md)); the house style removes frames/spines.

## Audit / Boundaries
- Always invoke with `--via skill:deepresearch-figure/<action>:<role>` so the exact render-adapter identity is preserved in the audit. Note the stamp namespace stays `deepresearch-figure/<action>` (the underlying render-adapter identity), not the skill folder name.
- Additive figure artifacts only; never mutates science or finalizes.
- Quest-isolated: artifact ids and figure paths are scoped to the single quest `<q>` you were given.

## Common Mistakes
- Rendering to a raster format (`.png`/`.jpg`) instead of `.pdf` — output must be vector so it embeds via `\includegraphics`.
- Dropping or altering the `--via skill:deepresearch-figure/<action>:<role>` audit stamp — keep it verbatim; without it the render-adapter identity is lost from the audit.
- Using the wrong `--kind` for plot (e.g. bar for a predicted-vs-measured relationship that should be scatter).
- Forgetting the `-p` suffix on the polish artifact id (`<q>:fig-<name>-p`) or overwriting the original figure ref instead of writing `<name>-polished.pdf`.
- Treating a figure pass as a chance to change science or finalize — this skill is additive and figure-only.
- Crossing quest boundaries by reusing another quest's `<q>`, figure paths, or data.

| Rationalization | Red flag — do NOT |
| --- | --- |
| "PNG is fine, it looks the same." | Always render `.pdf` (vector) so it embeds via `\includegraphics`. |
| "I'll simplify the audit stamp." | Preserve `--via skill:deepresearch-figure/<action>:<role>` exactly. |
| "I'll just fix the data while I'm in the figure." | Additive figure artifacts only; never mutate science or finalize. |
| "Reusing the other quest's figure saves time." | Quest-isolated — only the `<q>` you were given. |
