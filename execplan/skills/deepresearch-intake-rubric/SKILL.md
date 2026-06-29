---
name: deepresearch-intake-rubric
description: Use when a scout-ideator must take stock of pre-existing quest material (baselines, prior results, drafts, review packages) before deciding where the research loop resumes. Keywords — intake audit, intake-rubric, intake-method, trust ranking, manuscript-visibility ranking, legacy-method separation, state buckets, asset matrix, state-audit-template, current-board packet, next-anchor recommendation, scout-ideator, knowledge cards. Read-only methodology lookup that changes no state.
---

# deepresearch-intake-rubric

## Overview
Read-only intake-audit craft for the **scout-ideator**: when a quest starts from existing material instead of a blank state, audit, trust-rank, and reconcile the pre-existing assets, then produce a current-board packet that recommends the next anchor where the loop resumes. This skill is advisory only and changes no canonical state.

## When to Use
- You are the **scout-ideator** and a quest begins from pre-existing material (baselines, prior results, partial drafts, review packages) rather than a blank state.
- You need to take stock of prior work, rank trust in each asset, separate legacy methods, bucket the current state, and recommend where the loop should resume.

When NOT to use:
- Not your role: only the scout-ideator runs intake. Other roles should use their own craft.
- Not an intake context: if the quest truly starts blank, there is nothing to audit.
- Never use this to finalize, mutate results, confirm GPU, or change quest state — it is read-only and advisory; the DB stays canonical.

## Workflow
1. Index the methodology reference for your role (traceability stamp required):
   `$HARNESS --via skill:deepresearch-intake-rubric:<your-role> knowledge cards --query intake-method`
   (or `knowledge query --kind reference`).
2. Apply the intake method (see **Intake Method** below): work through the four intake questions, apply the trust ranking and manuscript-visibility ranking, separate legacy methods, and assign each area to a state bucket.
3. Build the asset matrix using the state-audit template (see **Asset Matrix** below): one row per area with columns area x current-asset x trust x why x missing-proof x recommended-action.
4. Apply the adoption/reconciliation rules to decide what to adopt, repair, or discard, and assemble the current-board packet that recommends the next anchor.
5. Do the stage work and record outcomes through your role's normal skill/commands. Map any external tool names you encounter in the method (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface. The DB stays canonical; this craft is advisory, never an authoritative state surface.
6. Return the method/recommendation to the calling task and continue.

If the task does not map cleanly to these steps, use your native planning tool to build a plan from the commands/constraints in this skill, then execute it.

## Intake Method
Apply the following when taking stock of pre-existing material:
- **Four intake questions** — work each pre-existing asset through the intake questions before trusting it.
- **Trust ranking** — rank how much each asset can be relied upon.
- **Manuscript-visibility ranking** — rank assets by what is visible/claimed in any manuscript or write-up versus what is actually substantiated.
- **Legacy-method separation** — separate prior (legacy) methods from anything you would carry forward.
- **State buckets** — assign each area to a state bucket reflecting its current standing.
- **Adoption / reconciliation rules** — decide what to adopt, reconcile, repair, or discard.
- **Current-board packet** — the output: a packet summarizing the audited state and recommending the next anchor where the loop resumes.

## Asset Matrix (state-audit template)
Lay out the audit as a matrix, one row per area, with these columns:

| area | current-asset | trust | why | missing-proof | recommended-action |
|------|---------------|-------|-----|---------------|--------------------|

- **area** — the topic/component being audited.
- **current-asset** — the pre-existing material for that area.
- **trust** — the trust ranking assigned to it.
- **why** — justification for the trust level.
- **missing-proof** — what evidence is absent or unverified.
- **recommended-action** — adopt / reconcile / repair / discard, feeding the next-anchor recommendation.

## Audit / Boundaries
- `--via skill:deepresearch-intake-rubric:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.
- The DB is canonical; this craft is advisory and is never an authoritative state surface.

## Common Mistakes
- **Treating the audit as authoritative state.** It is advisory only — do not let the asset matrix or current-board packet stand in for a DB write. Record real outcomes through your role's normal skill/commands.
- **Mutating state from intake.** Never finalize, mutate results, confirm GPU, or change quest state from this skill; it is read-only.
- **Dropping the traceability stamp.** Always pass `--via skill:deepresearch-intake-rubric:<your-role>` on the knowledge command.
- **Trusting assets without ranking them.** Run every pre-existing asset through the four intake questions, trust ranking, and manuscript-visibility ranking before adopting it — manuscript claims are not proof.
- **Carrying legacy methods forward silently.** Keep legacy-method separation explicit so prior methods are not mistaken for adopted ones.
- **Leaving external tool names unmapped.** Map `artifact.*`, `memory.*`, and `bash_exec` references in the method to the `$HARNESS` surface.
