---
name: isomer-deepsci-workspace-mgr
description: Use when Topic Workspace and Topic Actor preparation is complete, and optionally after Topic Team preparation, to own production DeepSci research workspace bootstrap, selected production DeepSci skill readiness, placeholder binding readiness, worker access posture, accepted research artifact guidance, and bootstrap validation before ordinary production DeepSci research skills write durable outputs.
---

# Isomer Research Workspace Mgr

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Latest-context reminder: before accepted durable record writes, record refreshes, or durable route, claim, context, evidence, result, or publication-facing decisions, follow `isomer-deepsci-shared` Latest Context Preflight. Resolve current Effective Topic Context and Workspace Runtime, inspect relevant durable records, capture or update `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`, and treat prompt memory, chat memory, prior prose, older rendered records, and worker-local files as candidate context until checked. Standalone source-only reading may skip this preflight until accepted Isomer records are written or refreshed.

Worker-output reminder: before writing JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, or other plain generated files, follow `isomer-deepsci-shared` Worker Output Policy: resolve `project outputs policy`, write under an operation-specific child set of the returned root, preserve durable records on their semantic bindings, and act on `commit_after_operation` as the post-action commit preference.

Lineage reminder: before accepted durable record writes that depend on prior durable records, follow `isomer-deepsci-shared` Artifact Lineage Recording. Pass canonical parents with `--parents-json` and `--lineage-kind`, use `--generation-id` for sibling candidate passes, keep query-index hints separate, and use `ext research records revise <record-id>` for content-changing accepted revisions.

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
- Formal team material is selected by the prompt or authoritative context but `isomer-topic-summary.md` is missing, blocked, stale, or not checked. Route back to `isomer-op-topic-team-specialize` or the relevant setup service first and name the selected Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, or equivalent evidence. Without a selected formal Agent Team layer, a missing summary does not establish Topic Team Specialization intent.
- Topic Actor Workspace readiness or formal Agent Workspace cwd proof has not completed for the selected topology. Route Topic Actor topology to `isomer-op-topic-mgr` and formal Agent Workspace cwd proof to `isomer-srv-agent-env-setup`.
- The user is asking for domain research work such as scouting, baseline selection, idea generation, experiment execution, analysis, writing, review, rebuttal, or finalization.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Confirm bootstrap entry**. Build DEEPSCI:RSCH-WORKSPACE-CONTEXT from minimal readiness signals across base Topic Workspace, selected Topic Actor, selected production DeepSci skill set, and optional formal team layers. Read `references/bootstrap-workflow.md`.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-workspace-mgr --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Inspect semantic surfaces**. Build DEEPSCI:RSCH-STORAGE-LABEL-PLAN by checking existing topic record labels, planned evidence/provenance/package labels, optional `custom.*` needs, and missing support. Read `references/semantic-surface-plan.md`.
4. **Bind production DeepSci placeholders by kind**. Produce DEEPSCI:RSCH-PLACEHOLDER-BINDING-REGISTRY from the production DeepSci placeholder kind table and the active skill set, preserving exact placeholder names as metadata. Read `references/placeholder-binding-registry.md`.
5. **Prepare worker access**. Produce DEEPSCI:RSCH-AGENT-ACCESS-PLAN for Topic Actor or formal Agent Workspace pre-promotion surfaces, generated conveniences, actor metadata, accepted research artifact guidance, and promotion boundaries. Read `references/agent-access-plan.md`.
6. **Record bootstrap result**. Produce DEEPSCI:RSCH-STORAGE-BOOTSTRAP-RECORD when the contract is usable, DEEPSCI:RSCH-BOOTSTRAP-VALIDATION-REPORT for readiness checks, or DEEPSCI:RSCH-WORKSPACE-BLOCKER-RECORD when required support is missing. Read `references/validation-and-blockers.md`.
7. **Update reset checkpoint when bootstrap should survive reset**. If the selected reset checkpoint should preserve production DeepSci bootstrap records, call `isomer-cli project topic-reset update-checkpoint --topic <research-topic-id> <checkpoint-id>` with the bootstrap record ids, structured payload ids, payload file paths, explicit export paths, semantic labels, support paths, source label, actor refs, and provenance refs.
8. **Return next route**. Hand control to the selected production DeepSci research skill only after the bootstrap outputs name durable semantic targets or explicit blockers, and after reset-survival intent has either been recorded in the checkpoint or explicitly left as redo-after-reset behavior.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-workspace-mgr --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

Do not infer a formal Agent Team layer from missing `isomer-topic-summary.md`, missing Agent Workspace or worker-access evidence, generic topic preparation, launch-facing language, or readiness gaps. Human-orchestrated Topic Actor topology continues through Topic Creator, Topic Manager, and the applicable setup services unless the user explicitly invokes specialization or the prompt or authoritative context establishes a formal Agent Team target.

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
- Unbound placeholder-kind count: number of production DeepSci placeholder kinds that lack a semantic target, access rule, planned support label, or explicit blocker in DEEPSCI:RSCH-PLACEHOLDER-BINDING-REGISTRY; lower is better.

### Checks

- Entry check: DEEPSCI:RSCH-WORKSPACE-CONTEXT confirms base Topic Workspace readiness, selected Topic Actor readiness, selected production DeepSci skill readiness, and optional formal team readiness using minimal readiness signals rather than broad fragile file detection.
- Surface check: DEEPSCI:RSCH-STORAGE-LABEL-PLAN distinguishes existing labels, planned labels, optional `custom.*` needs, and missing support.
- Binding check: DEEPSCI:RSCH-PLACEHOLDER-BINDING-REGISTRY maps production DeepSci placeholder kinds to semantic targets while preserving exact placeholder names as metadata.
- Access check: DEEPSCI:RSCH-AGENT-ACCESS-PLAN tells Topic Actors or formal agents where pre-promotion outputs belong, what metadata to preserve, and how accepted research artifacts should cite durable semantic refs.
- Validation check: DEEPSCI:RSCH-BOOTSTRAP-VALIDATION-REPORT states whether the production DeepSci research loop can start, or DEEPSCI:RSCH-WORKSPACE-BLOCKER-RECORD names what must be prepared first.
- Reset-survival check: production DeepSci bootstrap outputs that should survive Topic Workspace reset are added to the selected reset checkpoint; unrecorded bootstrap output is treated as redo-after-reset behavior.
- Route check: the next production DeepSci research skill is invoked only after durable semantic targets or explicit blockers are recorded.

## Exit Criteria

This skill can end only when all applicable checks are true:

- DEEPSCI:RSCH-WORKSPACE-CONTEXT identifies the Topic Workspace, Topic Creator summary or Topic Manager evidence, selected production DeepSci skill set, selected Topic Actors, actor workspace readiness, optional formal team material, runtime readiness, and worker context used for bootstrap.
- DEEPSCI:RSCH-STORAGE-LABEL-PLAN distinguishes existing semantic labels, planned labels, optional `custom.*` labels, and missing support.
- DEEPSCI:RSCH-PLACEHOLDER-BINDING-REGISTRY maps production DeepSci placeholder kinds to semantic targets without forcing hard-coded paths.
- DEEPSCI:RSCH-AGENT-ACCESS-PLAN tells working Topic Actors or formal agents where pre-promotion outputs belong, which actor metadata to preserve, and how durable refs should be cited after accepted research artifacts are promoted.
- DEEPSCI:RSCH-BOOTSTRAP-VALIDATION-REPORT says the production DeepSci research loop can start, or DEEPSCI:RSCH-WORKSPACE-BLOCKER-RECORD states what must be prepared first.

## Guardrails

- DO NOT treat this skill as a replacement for Topic Team Specialization or environment setup.
- DO NOT treat `isomer-op-topic-mgr` as the owner of production DeepSci placeholder binding.
- DO NOT require a Topic Service Master when the Project Operator Session or Operator Agent can perform the same bounded bootstrap work.
- DO NOT require formal Topic Team material for a human-orchestrated Topic Actor session.
- DO NOT treat a Topic Actor Workspace as an Agent Workspace or fabricate Agent Instance refs for Topic Actor records.
- DO NOT invent hard-coded paths when a semantic label, typed ref, or blocker is required.
- DO NOT let working agents cite generated links instead of semantic labels and typed refs.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
