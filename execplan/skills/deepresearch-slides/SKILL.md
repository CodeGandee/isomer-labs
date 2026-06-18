---
name: deepresearch-slides
description: Builds a presentation deck from the quest's paper or report — a real .pptx via python-pptx, with an HTML fallback. Use when the writer or operator needs slides for the paper or a journal-club talk from already-recorded results. Thin wrapper over `render slides` (nature-paper2ppt pack); emits an additive bundle artifact only and never invents results.
---

# slides (paper → deck)

Trigger: "make slides / a deck / PPTX for the paper / journal-club talk."

## use
`$HARNESS --via skill:deepresearch-slides:<role> render slides --quest-id <q> --artifact-id <q>:slides \
  --ref runs/<q>/report/slides/deck --input runs/<q>/report/paper.md`
Produces a real `.pptx` via python-pptx (HTML fallback if python-pptx is unavailable). Consult nature-paper2ppt/references/procedure.md (argument spine, 12–16 slide structure, per-slide schema).

## boundaries / audit
- Additive bundle artifact only; `--via` audited; quest-isolated; selects story figures, never invents results.

## stop
- Produce the deck artifact, then stop.
