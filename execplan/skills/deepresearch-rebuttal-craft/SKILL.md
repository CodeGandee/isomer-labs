---
name: deepresearch-rebuttal-craft
description: Use when the writer role is in the rebuttal stage answering a reviewer feedback package — mapping each review point to a planned action, tracking evidence updates, and drafting a response letter (review-matrix, action-plan, evidence-update, response-letter; response-letter voice rules). Read-only methodology lookup over the rebuttal-craft methodology reference; surfaces method and changes no state. Not for producing the original review (use review-craft).
---

# rebuttal-craft

## Overview
A read-only methodology lookup for the **writer** during the rebuttal stage of the loop: it surfaces the `rebuttal-craft` methodology reference and guides turning reviewer feedback into a response through the review-matrix → action-plan → evidence-update → response-letter sequence (with response-letter voice rules). It indexes and applies method only; it makes no state change and the DB stays canonical.

## When to Use
- You are the **writer** in the **rebuttal stage**, answering a review package.
- You need to map each reviewer point to a planned action, track which evidence/results were updated, and draft the response letter in the right voice.
- You want the stage templates (review-matrix, action-plan, evidence-update, response-letter).

When NOT to use:
- You are producing the **original review** (use `review-craft`, not this skill).
- You expect this to finalize, mutate results, confirm GPU, or change quest state — it does none of those. It is advisory only, never an authoritative state surface.
- Wrong role (not the writer) or wrong stage.

## Workflow
1. Index the methodology reference:
   `$HARNESS --via skill:deepresearch-rebuttal-craft:<your-role> knowledge cards --query rebuttal-flow`
   (or `knowledge query --kind reference`).
2. Read the relevant file in this skill's own `references/` folder and apply the method (see **Reference Pages** below for which file covers what).
3. Build the rebuttal in sequence: review-matrix → action-plan → evidence-update → response-letter, applying the response-letter voice rules from `references/rebuttal-flow.md`.
4. Do the stage work and record outcomes through your role's normal skill/commands. Map any external tool names in the reference pages (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface.
5. Return the method to the calling task and continue. Make no state change here.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Reference Pages
Files live in this skill's own `references/` folder:
- [`references/rebuttal-flow.md`](references/rebuttal-flow.md) — the review-matrix → action-plan → evidence-update → response-letter flow and the response-letter voice rules.
- [`references/review-matrix-template.md`](references/review-matrix-template.md) — review-matrix stage template.
- [`references/action-plan-template.md`](references/action-plan-template.md) — action-plan stage template.
- [`references/evidence-update-template.md`](references/evidence-update-template.md) — evidence-update stage template.
- [`references/response-letter-template.md`](references/response-letter-template.md) — response-letter stage template.

These pages live in this skill's `references/` folder; the same craft is also available at runtime via `$HARNESS knowledge cards`.

## Common Mistakes
- **Treating this as a state surface.** It is read-only/advisory. Never finalize, mutate results, confirm GPU, or change quest state from here. The DB stays canonical.
- **Using it to author the original review.** That is `review-craft`'s job; this skill is for answering a review.
- **Dropping the audit stamp.** Always pass `--via skill:deepresearch-rebuttal-craft:<role>` for traceability (read-only, so it records no row).
- **Skipping the sequence.** Work the stages in order (review-matrix → action-plan → evidence-update → response-letter); don't jump straight to the response letter.
- **Leaving external tool names unmapped.** Map `artifact.*`, `memory.*`, `bash_exec` references in the reference pages onto the `$HARNESS` surface before acting.

## Audit / Boundaries
- `--via skill:deepresearch-rebuttal-craft:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.
- This craft is advisory, never an authoritative state surface.
