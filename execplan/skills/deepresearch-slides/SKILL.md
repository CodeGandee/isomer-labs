---
name: deepresearch-slides
description: Use when a writer or operator needs a presentation deck (slides, PPTX, journal-club talk) built from a quest's already-recorded paper or report. Triggers on "make slides / a deck / PPTX for the paper / journal-club talk." Wraps the `$HARNESS render slides` command (backed by an internal runtime adapter); emits an additive bundle artifact, quest-isolated, never invents results.
---

# slides (paper → deck)

## Overview
Builds a presentation deck from the quest's already-written paper or report: a real `.pptx` via python-pptx, with an HTML fallback if python-pptx is unavailable. This is a thin wrapper over the `$HARNESS render slides` command (backed by an internal runtime adapter) that selects story figures and lays them out — it never produces new results.

## When to Use
- The writer or operator asks to "make slides / a deck / PPTX for the paper" or a "journal-club talk."
- The paper or report already exists at `runs/<q>/report/paper.md` (or equivalent) and results are already recorded.

When NOT to use:
- Results are not yet recorded — this skill does not run experiments or invent any results; it only renders what already exists in the paper/report.
- You are asked to author or edit the paper text itself — that is a different (writing) role, not this render step.
- The request belongs to a different quest — keep quest isolation: only render artifacts for the quest you were given (`--quest-id <q>`), and never pull figures or text from another quest.

## Workflow
1. Confirm the input paper/report exists for the target quest (e.g. `runs/<q>/report/paper.md`) and that results are already recorded.
2. Run the render command (see Command below), passing the quest id, the artifact id, the deck ref, and the input paper.
3. The verb produces a real `.pptx` via python-pptx, falling back to HTML if python-pptx is unavailable. It selects story figures from the existing results — it does not invent any.
4. For the argument spine, the 12–16 slide structure, and the per-slide schema, consult [`references/procedure.md`](references/procedure.md) (kept in this skill's `references/` folder).
5. Produce the deck artifact, then stop.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Command
Run verbatim, substituting the quest id `<q>` and your role `<role>`:

```
$HARNESS --via skill:deepresearch-slides:<role> render slides --quest-id <q> --artifact-id <q>:slides \
  --ref runs/<q>/report/slides/deck --input runs/<q>/report/paper.md
```

This produces a real `.pptx` via python-pptx (HTML fallback if python-pptx is unavailable). Consult [`references/procedure.md`](references/procedure.md) for the argument spine, the 12–16 slide structure, and the per-slide schema.

## Boundaries / Audit
- Additive bundle artifact only — the deck is added alongside, nothing existing is overwritten.
- `--via skill:deepresearch-slides:<role>` is audited; keep the audit stamp on the command exactly as written.
- Quest-isolated: only operate within the given `--quest-id <q>`; never reference another quest's artifacts or figures.
- Selects story figures from the existing paper/report; never invents results.

## Common Mistakes
- Inventing or fabricating results/figures to fill the deck. The skill only renders figures and content that already exist in the paper/report.
- Dropping or altering the `--via skill:deepresearch-slides:<role>` audit stamp, which breaks provenance auditing.
- Reaching across quests for figures or text — violates quest isolation. Stay within `--quest-id <q>`.
- Treating the deck as a replacement rather than an additive bundle artifact, or continuing past deck production instead of stopping.
- Running this before results are recorded or the paper exists — there is then nothing valid to render.
