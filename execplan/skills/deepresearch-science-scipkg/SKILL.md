---
name: deepresearch-science-scipkg
description: Scientific-software package routing plus the Science Evidence Graph, for natural-science and HPC quests — 169 per-package cards (which package fits, how to check it, evidence-path conventions, pitfalls) and the Science Evidence Graph contract (six node types, claim-type discipline, HPC-via-shell). Use when the experimenter or analyst is selecting or verifying a scientific/HPC software tool, or recording science evidence as graph nodes. Read-only methodology lookup; surfaces a reference pack and changes no state.
---

# science-scipkg (read-only methodology lookup)

Surfaces the `science-scipkg` reference pack for the **experimenter and analyst** on natural-science/HPC quests.
The pack is the source of truth; this skill only indexes and points into it, and makes no state change.

## Use
1. Index the pack:
   `$HARNESS --via skill:deepresearch-science-scipkg:<your-role> knowledge cards --query scipkg`
   (or `knowledge query --kind reference`).
2. Read the relevant file under `execplan/packs/science-scipkg/references/` and apply the method:
   - `references/science-evidence-graph.md` — the Science Evidence Graph contract (six node types,
     claim-type discipline, HPC-via-shell) and how science nodes map onto `$HARNESS record apply`.
     Read this first for a science/HPC quest.
   - `references/packages/<package_id>.md` — 169 per-package routing cards (which package, how to check it,
     evidence-path conventions, pitfalls).
   - `references/package-index.min.json`, `references/domain-index.md` — search the 169 cards by name or
     browse by domain.
   - `references/package-check-playbook.md`, `references/hpc-via-bash-exec.md`,
     `references/claim-type-discipline.md`, `references/science-task-brief-template.md`,
     `references/artifact-science-tool.md` — the operational reference set.
3. Do the stage work and record outcomes through your role's normal skill/commands. The DB stays canonical;
   this craft is advisory, never an authoritative state surface. Map any external tool names in the
   files (`artifact.*`, `memory.*`, `bash_exec`) to the `$HARNESS` surface.

## Audit / boundaries
- `--via skill:deepresearch-science-scipkg:<role>` is passed for traceability; read-only, so it records no row.
- Never finalize, mutate results, confirm GPU, or change quest state from here.

## Stop
- Return the method to the calling task and continue.
