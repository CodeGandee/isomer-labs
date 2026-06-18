---
name: deepresearch-ideation-rubric
description: Idea-and-scoping craft for the scope/idea stages — the objective contract, the selection gate, the divergence-then-convergence (Diverge/Converge/Refine) workflow with a divergence-lens catalog and failure-mode-to-recovery taxonomy, candidate scoring, the eval contract, the baseline shortlist, and scout framing (four framing layers; attach/import/reproduce baseline routes; blocked-state handling). Use when the scout-ideator is generating, scoping, or selecting a research idea, or fixing its evaluation and baseline plan. Read-only methodology lookup; surfaces a reference pack and changes no state.
---

# ideation-rubric (read-only methodology lookup)

Surfaces the `ideation-rubric` reference pack for the **scout-ideator** during the scope/idea stages of the loop.
The pack is the source of truth; this skill only indexes and points into it, and makes no state change.

## Use
1. Index the pack:
   `$HARNESS --via skill:deepresearch-ideation-rubric:<your-role> knowledge cards --query selection-gate`
   (or `knowledge query --kind reference`).
2. Read the relevant file under `execplan/packs/ideation-rubric/references/` and apply the method:
   - `references/ideation-craft.md` — divergence-lens catalog, failure-mode-to-recovery taxonomy,
     Diverge/Converge/Refine workflow, framework-selection dispatch table, candidate scoring rubric.
   - `references/scout-framing.md` — four framing layers, attach/import/reproduce baseline routes,
     blocked-state handling.
   - The objective contract, selection gate, eval contract, and baseline shortlist each have their own
     template/playbook in the same directory (e.g. `objective-contract-template.md`, `selection-gate.md`,
     `eval-contract-template.md`, `baseline-shortlist-template.md`).
3. Do the stage work and record outcomes through your role's normal skill/commands. The DB stays canonical;
   this craft is advisory, never an authoritative state surface. Map any external tool names in the
   files (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface.

## Audit / boundaries
- `--via skill:deepresearch-ideation-rubric:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.

## Stop
- Return the method to the calling task and continue.
