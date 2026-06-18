---
name: deepresearch-review-craft
description: Reviewer craft for the review stage — the 13 review dimensions, the evidence-authenticity gate (catching invented or unsupported claims), the literature-positioning benchmark, and the review-report, revision-log, and experiment-todo templates. Use when the reviewer is critiquing a manuscript or experiment package, checking whether claims trace to real validated evidence, or writing up review findings and follow-up experiment requests. Read-only methodology lookup; surfaces a reference pack and changes no state.
---

# review-craft (read-only methodology lookup)

Surfaces the `review-craft` reference pack for the **reviewer** during the review stage of the loop.
The pack is the source of truth; this skill only indexes and points into it, and makes no state change.

## Use
1. Index the pack:
   `$HARNESS --via skill:deepresearch-review-craft:<your-role> knowledge cards --query authenticity-gate`
   (or `knowledge query --kind reference`).
2. Read the relevant file under `execplan/packs/review-craft/references/` and apply the method:
   - `references/review-dimensions.md` — the 13 review dimensions.
   - `references/authenticity-gate.md` — the evidence-authenticity gate.
   - `references/lit-benchmark.md` — the literature-positioning benchmark.
   - `references/review-report-template.md`, `references/revision-log-template.md`,
     `references/experiment-todo-template.md` — the output templates.
3. Do the stage work and record outcomes through your role's normal skill/commands. The DB stays canonical;
   this craft is advisory, never an authoritative state surface. Map any external tool names in the
   files (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface.

## Audit / boundaries
- `--via skill:deepresearch-review-craft:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.

## Stop
- Return the method to the calling task and continue.
