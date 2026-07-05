---
name: isomer-deepsci-workspace-mgr
description: Use after Topic Workspace and Topic Actor preparation, and optionally after Topic Team preparation, to own production DeepSci research workspace bootstrap, selected production DeepSci skill readiness, placeholder binding readiness, worker access posture, accepted research artifact guidance, and bootstrap validation before ordinary production DeepSci research skills write durable outputs.
---

# Isomer Research Workspace Mgr

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `latest-context-snapshot`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Workspace manager prepares the research-facing contract that production DeepSci skills use after topic setup is ready. It validates readiness as composable topology layers: base Topic Workspace readiness, Topic Actor readiness for human-orchestrated workers, selected production DeepSci skill readiness, placeholder binding readiness, and optional formal team readiness when a Topic Agent Team is selected. It first consumes Topic Creator summaries, Topic Manager topology evidence, Topic Workspace registration evidence, or final topic-team summary when present, then verifies that the selected Research Topic, Topic Workspace, Workspace Runtime, topic-main, record labels, placeholder bindings, selected Topic Actor Workspaces, and optional Agent Workspace context are ready enough for accepted research artifacts to land in durable topic-owned surfaces or become explicit blockers.

When production DeepSci bootstrap creates setup records, managed payload files, support files, semantic label evidence, or explicit Markdown exports that should survive a later Topic Workspace reset, this skill must call the checkpoint update API through `isomer-cli project topic-reset update-checkpoint` with its preserved record ids, structured payload ids, payload file paths, export paths, support paths, semantic labels, source label, actor refs, and provenance refs. If this skill does not update the selected reset checkpoint, those production DeepSci bootstrap outputs are ordinary post-checkpoint preparation state; a destructive reset can clear them and production DeepSci bootstrap must be redone after reset.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`.

## When to Use

Use this skill when:

- Topic Creator, Topic Manager, or Topic Team Specialization has produced enough base topic readiness for ordinary production DeepSci research work.
- A human-orchestrated Topic Actor research session needs production DeepSci bootstrap records, actor cwd guidance, and accepted-artifact command guidance.
- Topic Team Specialization has produced `isomer-topic-summary.md` and the team is about to start ordinary production DeepSci research work.
- A Topic Service Master, Project Operator Session, or Operator Agent needs to verify where production DeepSci placeholder outputs should be routed.
- Working Topic Actors need an access plan for `topic.actors.workspace`, `topic.actors.private_artifacts`, `topic.actors.logs`, and `topic.actors.links`, or formal team agents need an access plan for `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links`.
- A production DeepSci research skill is blocked because semantic record surfaces, placeholder binding, generated links, or pre-promotion rules are unclear.

Do not use this skill when:

- The task is only operator topology inspection, branch helper work, or legacy diagnostics. Use `isomer-op-topic-mgr` for that boundary.
- The selected Topic Workspace lacks base topic readiness, has only provisional registration evidence, or has missing topic environment, topic-main, runtime, or record-label readiness. Route back to `isomer-op-topic-creator`, `isomer-op-topic-mgr`, or the relevant setup service first.
- Formal team material is selected but `isomer-topic-summary.md` is missing, blocked, stale, or not checked. Route back to `isomer-op-topic-team-specialize` or the relevant setup service first.
- Topic Actor Workspace readiness or formal Agent Workspace cwd proof has not completed for the selected topology. Route Topic Actor topology to `isomer-op-topic-mgr` and formal Agent Workspace cwd proof to `isomer-srv-agent-env-setup`.
- The user is asking for domain research work such as scouting, baseline selection, idea generation, experiment execution, analysis, writing, review, rebuttal, or finalization.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Confirm bootstrap entry**. Build <RSCH_WORKSPACE_CONTEXT> from minimal readiness signals across base Topic Workspace, selected Topic Actor, selected production DeepSci skill set, and optional formal team layers. Read `references/bootstrap-workflow.md`.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-workspace-mgr --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Inspect semantic surfaces**. Build <RSCH_STORAGE_LABEL_PLAN> by checking existing topic record labels, planned evidence/provenance/package labels, optional `custom.*` needs, and missing support. Read `references/semantic-surface-plan.md`.
4. **Bind production DeepSci placeholders by kind**. Produce <RSCH_PLACEHOLDER_BINDING_REGISTRY> from the production DeepSci placeholder kind table and the active skill set, preserving exact placeholder names as metadata. Read `references/placeholder-binding-registry.md`.
5. **Prepare worker access**. Produce <RSCH_AGENT_ACCESS_PLAN> for Topic Actor or formal Agent Workspace pre-promotion surfaces, generated conveniences, actor metadata, accepted research artifact guidance, and promotion boundaries. Read `references/agent-access-plan.md`.
6. **Record bootstrap result**. Produce <RSCH_STORAGE_BOOTSTRAP_RECORD> when the contract is usable, <RSCH_BOOTSTRAP_VALIDATION_REPORT> for readiness checks, or <RSCH_WORKSPACE_BLOCKER_RECORD> when required support is missing. Read `references/validation-and-blockers.md`.
7. **Update reset checkpoint when bootstrap should survive reset**. If the selected reset checkpoint should preserve production DeepSci bootstrap records, call `isomer-cli project topic-reset update-checkpoint --topic <research-topic-id> <checkpoint-id>` with the bootstrap record ids, structured payload ids, payload file paths, explicit export paths, semantic labels, support paths, source label, actor refs, and provenance refs.
8. **Return next route**. Hand control to the selected production DeepSci research skill only after the bootstrap outputs name durable semantic targets or explicit blockers, and after reset-survival intent has either been recorded in the checkpoint or explicitly left as redo-after-reset behavior.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-workspace-mgr --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/bootstrap-workflow.md` for minimal Topic Workspace readiness detection from Topic Creator and Topic Manager evidence, entry conditions, Topic Actor fallback, optional formal team checks, and the post-preparation sequence.
- `references/semantic-surface-plan.md` for existing topic record labels, planned evidence/provenance/package labels, and `custom.*` escalation.
- `references/placeholder-binding-registry.md`, `references/placeholder-binding-index.md`, and each relevant skill's `placeholder-bindings.md` for mapping production DeepSci placeholder kinds to semantic targets while preserving placeholder names.
- `references/agent-access-plan.md` for Topic Actor Workspace and Agent Workspace pre-promotion surfaces, generated links, and promotion boundaries.
- `references/validation-and-blockers.md` for readiness checks, bootstrap reports, validation output, and blocker records.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Readiness-signal coverage: fraction of base Topic Workspace readiness, selected Topic Actor readiness, selected production DeepSci skill readiness, optional formal team readiness, Workspace Runtime readiness, record-label readiness, placeholder binding guidance, and worker identity checked before bootstrap; higher is better.
- Unbound placeholder-kind count: number of production DeepSci placeholder kinds that lack a semantic target, access rule, planned support label, or explicit blocker in <RSCH_PLACEHOLDER_BINDING_REGISTRY>; lower is better.

### Checks

- Entry check: <RSCH_WORKSPACE_CONTEXT> confirms base Topic Workspace readiness, selected Topic Actor readiness, selected production DeepSci skill readiness, and optional formal team readiness using minimal readiness signals rather than broad fragile file detection.
- Surface check: <RSCH_STORAGE_LABEL_PLAN> distinguishes existing labels, planned labels, optional `custom.*` needs, and missing support.
- Binding check: <RSCH_PLACEHOLDER_BINDING_REGISTRY> maps production DeepSci placeholder kinds to semantic targets while preserving exact placeholder names as metadata.
- Access check: <RSCH_AGENT_ACCESS_PLAN> tells Topic Actors or formal agents where pre-promotion outputs belong, what metadata to preserve, and how accepted research artifacts should cite durable semantic refs.
- Validation check: <RSCH_BOOTSTRAP_VALIDATION_REPORT> states whether the production DeepSci research loop can start, or <RSCH_WORKSPACE_BLOCKER_RECORD> names what must be prepared first.
- Reset-survival check: production DeepSci bootstrap outputs that should survive Topic Workspace reset are added to the selected reset checkpoint; unrecorded bootstrap output is treated as redo-after-reset behavior.
- Route check: the next production DeepSci research skill is invoked only after durable semantic targets or explicit blockers are recorded.

## Exit Criteria

This skill can end only when all applicable checks are true:

- <RSCH_WORKSPACE_CONTEXT> identifies the Topic Workspace, Topic Creator summary or Topic Manager evidence, selected production DeepSci skill set, selected Topic Actors, actor workspace readiness, optional formal team material, runtime readiness, and worker context used for bootstrap.
- <RSCH_STORAGE_LABEL_PLAN> distinguishes existing semantic labels, planned labels, optional `custom.*` labels, and missing support.
- <RSCH_PLACEHOLDER_BINDING_REGISTRY> maps production DeepSci placeholder kinds to semantic targets without forcing hard-coded paths.
- <RSCH_AGENT_ACCESS_PLAN> tells working Topic Actors or formal agents where pre-promotion outputs belong, which actor metadata to preserve, and how durable refs should be cited after accepted research artifacts are promoted.
- <RSCH_BOOTSTRAP_VALIDATION_REPORT> says the production DeepSci research loop can start, or <RSCH_WORKSPACE_BLOCKER_RECORD> states what must be prepared first.

## Common Mistakes

- Treating this skill as a replacement for Topic Team Specialization or environment setup.
- Treating `isomer-op-topic-mgr` as the owner of production DeepSci placeholder binding.
- Requiring a Topic Service Master when the Project Operator Session or Operator Agent can perform the same bounded bootstrap work.
- Requiring formal Topic Team material for a human-orchestrated Topic Actor session.
- Treating a Topic Actor Workspace as an Agent Workspace or fabricating Agent Instance refs for Topic Actor records.
- Inventing hard-coded paths when a semantic label, typed ref, or blocker is required.
- Letting working agents cite generated links instead of semantic labels and typed refs.
