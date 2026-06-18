---
name: deepresearch-intake-rubric
description: Intake-audit craft for quests that start from existing material instead of a blank state — auditing, trust-ranking, and reconciling pre-existing assets (baselines, results, drafts, review packages), the manuscript-visibility ranking, legacy-method separation, state buckets, and the current-board packet that recommends the next anchor. Use when the scout-ideator must take stock of prior work before choosing where the loop resumes. Read-only methodology lookup; surfaces a reference pack and changes no state.
---

# intake-rubric (read-only methodology lookup)

Surfaces the `intake-rubric` reference pack for the **scout-ideator** when a quest begins from pre-existing
material. The pack is the source of truth; this skill only indexes and points into it, and makes no state change.

## Use
1. Index the pack:
   `$HARNESS --via skill:deepresearch-intake-rubric:<your-role> knowledge cards --query intake-method`
   (or `knowledge query --kind reference`).
2. Read the relevant file under `execplan/packs/intake-rubric/references/` and apply the method:
   - `references/intake-method.md` — the four intake questions, trust ranking, manuscript-visibility
     ranking, state buckets, adoption/reconciliation rules, and the current-board packet.
   - `references/state-audit-template.md` — the asset-matrix layout
     (area x current-asset x trust x why x missing-proof x recommended-action).
3. Do the stage work and record outcomes through your role's normal skill/commands. The DB stays canonical;
   this craft is advisory, never an authoritative state surface. Map any external tool names in the
   files (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface.

## Audit / boundaries
- `--via skill:deepresearch-intake-rubric:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.

## Stop
- Return the method to the calling task and continue.
