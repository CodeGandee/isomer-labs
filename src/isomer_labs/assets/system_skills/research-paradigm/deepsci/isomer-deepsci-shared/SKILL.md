---
name: isomer-deepsci-shared
description: Use when a production DeepSci Isomer research skill needs shared coordination rules, semantic handoff vocabulary, route discipline, or storage-binding cautions before conducting research work.
---

# Isomer Research Shared

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`, and request `--render markdown` only for the generated review view.

Shared defines the coordination contract for production DeepSci research skills. It is not migrated from one upstream source skill; it exists to keep production DeepSci skill handoffs, route decisions, placeholder usage, and storage-binding cautions consistent across the refactor-migrated skills.

## Latest Context Preflight

Before a production DeepSci research skill writes or refreshes accepted durable research records, or makes durable route, claim, context, evidence, result, or publication-facing decisions, run `references/latest-context-preflight.md`. The preflight resolves current Effective Topic Context, Workspace Runtime state, relevant durable records, duplicate-record posture, prompt-versus-durable-context conflicts, and the storage-neutral `latest-context-snapshot` verdict before prompt memory, chat memory, prior prose, or remembered research state is trusted.

Standalone source-only reading may skip the latest-context preflight until accepted Isomer records are written or refreshed. Worker Output Policy still governs plain generated files; the preflight applies before those files are promoted or recorded as accepted durable records.

## Worker Output Policy

Before a production DeepSci research skill writes plain generated files, resolve the current worker output policy with `isomer-cli --print-json project outputs policy --topic <research-topic-id> --agent <agent-name>` for a formal Agent Workspace or `isomer-cli --print-json project outputs policy --topic <research-topic-id> --topic-actor <topic-actor-name>` for a Topic Actor Workspace. Use the returned `absolute_root`, `worker_relative_root`, `operation_set_pattern`, `tracking_authority`, and `commit_after_operation`.

Write operation-local plain text outputs under an operation-specific child set of the resolved root, using the operation-set pattern, for example `<absolute_root>/sets/<timestamp>-<operation>-<shortid>/`. This applies to JSON payload staging files, Markdown drafts, CSVs, figures, paper builds, previews, reports, local summaries, deck assets, and other plain files that are not yet accepted durable records.

Do not invent a separate tracking policy. `.gitignore` and Git status control whether files under the output root are tracked or committable. After a file-writing research operation, check `commit_after_operation`; when it is true, commit the changed worker workspace according to the current Git status, and when it is false, leave the files uncommitted and report their paths.

Preserve durable record guidance: accepted Artifacts, Evidence Items, Runs, Decision Records, View Manifests, Provenance Records, and other structured research records still use their record bindings, `topic.records.*`, or the skill's placeholder-binding instructions. Worker output roots are for pre-promotion or operation-local plain files, not a replacement for durable semantic records.

## When to Use

Use this skill when:

- A production DeepSci research skill needs the shared semantic placeholder registry.
- A handoff object needs a stable meaning before Isomer storage binding exists.
- Two production DeepSci skills disagree about whether an object is evidence, a decision, a handoff, a run record, runtime state, a report, a draft, code, a dataset, or a figure.
- A route decision should be expressed in a common form before dispatching to another production DeepSci skill.
- A production DeepSci skill needs the latest-context preflight before durable record work trusts prompt context, chat memory, old rendered prose, or remembered research state.
- A prepared Topic Workspace, Topic Actor Workspace, `topic.repos.main`, or formal Agent Workspace needs a production DeepSci research bootstrap pass before ordinary production DeepSci skills write durable outputs.

Do not use this skill as a substitute for a domain skill such as workspace-mgr, scout, baseline, idea, optimize, experiment, analysis, science, decision, or finalize.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify the coordination question**. Name the handoff, route, placeholder, or storage-binding ambiguity that needs shared rules. Read `references/coordination-contract.md`.
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-shared --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Run latest-context preflight when needed**. If the question affects accepted durable record work or current research context, read `references/latest-context-preflight.md` before trusting prompt context, chat memory, old rendered prose, or remembered research state.
4. **Check the semantic registry**. Read `references/semantic-placeholders.md` and choose the closest existing semantic object.
5. **Preserve skill ownership**. Route domain work back to the owning production DeepSci skill; use shared only for vocabulary and coordination consistency. Read `references/coordination-contract.md`.
6. **Route bootstrap questions**. Use `isomer-deepsci-workspace-mgr` when the issue is post-preparation placeholder binding, semantic record surfaces, Topic Actor Workspace access posture, formal Agent Workspace access posture, current cwd context, or missing bootstrap support. Read `references/coordination-contract.md`.
7. **Avoid premature storage binding**. Keep unresolved records semantic until an Isomer storage-binding pass assigns Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, path, or schema bindings. Read `references/semantic-placeholders.md` and `references/coordination-contract.md`.
8. **Return the coordination result**. State the chosen semantic object, owning producer, intended consumer, and any unresolved binding or route question. Read `references/coordination-contract.md`.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-shared --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the shared registry, the relevant production DeepSci skill, and the user's request, then execute the plan.

## Common Mistakes

- Treating shared as the owner of research work rather than the owner of vocabulary consistency.
- Treating shared as the post-preparation bootstrap manager instead of routing to `isomer-deepsci-workspace-mgr`.
- Letting a durable record write, refresh, route decision, or claim decision proceed from prompt memory before `references/latest-context-preflight.md` checks current Isomer context.
- Binding placeholders to paths, database rows, or Artifact kinds before a storage-binding pass.
- Inventing a new semantic object when an existing registry entry already fits.
- Letting a route decision hide the evidence or blocker that made the route justified.

## Reference Routing

Read `references/latest-context-preflight.md` whenever a production DeepSci skill needs current topic context, runtime state, durable record freshness, duplicate-record handling, prompt-versus-durable-context conflict routing, or the storage-neutral `latest-context-snapshot`. Read `references/semantic-placeholders.md` whenever a production DeepSci skill needs shared handoff vocabulary. Read `references/coordination-contract.md` whenever the question is about ownership, routing, unresolved storage binding, post-preparation bootstrap routing, cwd context, or handoff shape.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Semantic-registry reuse rate: fraction of coordination questions resolved with an existing shared semantic object instead of a new invented term; higher is better.
- Premature-binding count: number of placeholder, handoff, route, or semantic object decisions bound to concrete paths, database rows, or final storage kinds before a storage-binding pass; lower is better.

### Checks

- Coordination check: the handoff, route, placeholder, or storage-binding ambiguity is named before shared rules are applied.
- Latest-context check: durable record work uses `references/latest-context-preflight.md` before prompt memory, chat memory, prior prose, or remembered research state is treated as current.
- Registry check: the closest existing semantic object is chosen from `references/semantic-placeholders.md` before any new vocabulary is introduced.
- Ownership check: domain work is routed back to the owning production DeepSci skill rather than handled by shared.
- Bootstrap check: post-preparation workspace bootstrap questions route to `isomer-deepsci-workspace-mgr`, with the current cwd classified as Topic Workspace, Topic Actor Workspace, `topic.repos.main`, or formal Agent Workspace when possible.
- Binding check: unresolved storage bindings remain semantic until a later binding pass assigns durable labels, typed refs, paths, or schemas.
- Result check: the final coordination result states chosen semantic object, owning producer, intended consumer, and unresolved binding or route question.
