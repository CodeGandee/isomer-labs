---
name: deepresearch-rebuttal-craft
description: Rebuttal flow for the rebuttal stage — turning reviewer feedback into a response through the review-matrix to action-plan to evidence-update to response-letter sequence, with the response-letter voice rules. Use when the writer is answering a review package: mapping each point to a planned action, tracking evidence updates, and drafting the response letter. Read-only methodology lookup; surfaces a reference pack and changes no state. (For producing the original review, see review-craft.)
---

# rebuttal-craft (read-only methodology lookup)

Surfaces the `rebuttal-craft` reference pack for the **writer** during the rebuttal stage of the loop.
The pack is the source of truth; this skill only indexes and points into it, and makes no state change.

## Use
1. Index the pack:
   `$HARNESS --via skill:deepresearch-rebuttal-craft:<your-role> knowledge cards --query rebuttal-flow`
   (or `knowledge query --kind reference`).
2. Read the relevant file under `execplan/packs/rebuttal-craft/references/` and apply the method:
   - `references/rebuttal-flow.md` — the review-matrix to action-plan to evidence-update to response-letter
     flow and the response-letter voice rules.
   - `references/review-matrix-template.md`, `references/action-plan-template.md`,
     `references/evidence-update-template.md`, `references/response-letter-template.md` — the stage templates.
3. Do the stage work and record outcomes through your role's normal skill/commands. The DB stays canonical;
   this craft is advisory, never an authoritative state surface. Map any external tool names in the
   files (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface.

## Audit / boundaries
- `--via skill:deepresearch-rebuttal-craft:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.

## Stop
- Return the method to the calling task and continue.
