---
name: deepresearch-research-method
description: Cross-stage experimental-research methodology spanning baseline, experiment, analysis, decision, optimize, and finalize — the evidence ladder (minimum/solid/maximum), the comparability contract, campaign design, decision and route-selection criteria, exploration-depth and stop-loss/plateau playbooks, optimize-search playbooks, and the finalization checklist with belief-change and limitations closure. Use when the experimenter, analyst, scout-ideator, or orchestrator is planning or running experiments, judging evidence strength or comparability, deciding the next route, or closing out a quest. Read-only methodology lookup; surfaces a reference pack and changes no state.
---

# research-method (read-only methodology lookup)

Surfaces the `research-method` reference pack for the **experimenter, analyst, scout-ideator, and orchestrator**
across the loop's experimental stages. The pack is the source of truth; this skill only indexes and points into
it, and makes no state change.

## Use
1. Index the pack:
   `$HARNESS --via skill:deepresearch-research-method:<your-role> knowledge cards --query evidence-ladder`
   (or `knowledge query --kind reference`).
2. Read the relevant file under `execplan/packs/research-method/references/` and apply the method. Key entries:
   - `references/evidence-ladder.md` — minimum/solid/maximum evidence levels; `references/comparability-contract.md`
     — fair-comparison rules.
   - `references/campaign-design.md`, `references/decision-criteria.md`, `references/route-selection.md`,
     `references/research-route-criteria.md` — campaign design and decision/exploration-depth choices.
   - `references/plateau-response-playbook.md`, `references/execution-playbook.md`, `references/fusion-playbook.md`
     — stop-loss, execution, and optimize-search playbooks.
   - `references/finalize-craft.md`, `references/finalization-checklist.md`, `references/resume-packet-template.md`
     — closure, belief-change/limitations, and resume packet. (Plus the stage checklists and templates in the
     same directory for baseline/experiment/analysis/optimize.)
3. Do the stage work and record outcomes through your role's normal skill/commands. The DB stays canonical;
   this craft is advisory, never an authoritative state surface. Map any external tool names in the
   files (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface.

## Audit / boundaries
- `--via skill:deepresearch-research-method:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.

## Stop
- Return the method to the calling task and continue.
