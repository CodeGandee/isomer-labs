---
name: isomer-deepsci-shared
description: Use when a production DeepSci Isomer research skill needs shared coordination rules, semantic handoff vocabulary, route discipline, or storage-binding cautions before conducting research work.
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer Research Shared

## Overview

Accepted durable outputs named by this skill are structured research records. When a placeholder output must be recorded, follow this skill's `placeholder-bindings.md`: draft the JSON payload, validate it, create or update the record with `--payload-file`; render Markdown later with `ext research records render` only when a human-readable view or explicit export is needed.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Shared defines the coordination contract for production DeepSci research skills. It is not migrated from one upstream source skill; it exists to keep production DeepSci skill handoffs, route decisions, placeholder usage, and storage-binding cautions consistent across the refactor-migrated skills.

### Latest Context Preflight

Before a production DeepSci research skill writes or refreshes accepted durable research records, or makes durable route, claim, context, evidence, result, or publication-facing decisions, run `references/latest-context-preflight.md`. The preflight reconciles ambient location, prompt-selected task target, Effective Topic Context and manifest fallback, active acting posture, Workspace Runtime state, relevant durable records, duplicate-record posture, and prompt-versus-durable-context conflicts before producing the storage-neutral `DEEPSCI:LATEST-CONTEXT-SNAPSHOT` verdict. Pin the reconciled Research Topic and worker selectors on every applicable downstream CLI call before prompt memory, chat memory, prior prose, or remembered research state is trusted.

Standalone source-only reading may skip the latest-context preflight until accepted Isomer records are written or refreshed. Worker Output Policy still governs plain generated files; the preflight applies before those files are promoted or recorded as accepted durable records.

### Worker Output Policy

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
2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-shared --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
3. **Run latest-context preflight when needed**. If the question affects accepted durable record work or current research context, read `references/latest-context-preflight.md` before trusting prompt context, chat memory, old rendered prose, or remembered research state.
4. **Check the semantic registry**. Read `references/semantic-placeholders.md` and choose the closest existing semantic object.
5. **Plan canonical lineage for durable records**. If a durable record will be written or revised, identify immediate durable parents, lineage kind, and generation group before the write. Read `references/artifact-lineage-recording.md`.
6. **Plan canonical idea recording when concepts change**. If the work creates, selects, rejects, defers, closes, reopens, explores, supports, refutes, updates, follows up, merges, or subsumes research concepts, invoke `isomer-op-entrypoint->research-ideas`, then use `references/research-idea-recording.md` for DeepSci profile paths. Identify explicit facets, exact Idea Realizations, generation membership, complete decision options, justified transitions, terminal refs, and idea lineage before the durable write.
7. **Preflight target prerequisites**. Before target mutation, resolve required accepted inputs and known producer routes. For a producible gap, read `references/prerequisite-recovery.md`; pause an ordinary request before producer mutation, or use the native planning tool only after explicit target-scoped run-to authorization.
8. **Preserve skill ownership**. Route domain work back to the owning production DeepSci skill; use shared only for vocabulary and coordination consistency. During run-to, the current agent may coordinate owners but never inherits their mutation authority. Read `references/coordination-contract.md`.
9. **Route bootstrap questions**. Use `isomer-deepsci-workspace-mgr` when the issue is post-preparation placeholder binding, semantic record surfaces, Topic Actor Workspace access posture, formal Agent Workspace access posture, current cwd context, or missing bootstrap support. Read `references/coordination-contract.md`.
10. **Avoid premature storage binding**. Keep unresolved records semantic until an Isomer storage-binding pass assigns Artifact, Evidence Item, Run, Gate, Decision Record, Provenance Record, path, or schema bindings. Read `references/semantic-placeholders.md` and `references/coordination-contract.md`.
11. **Return the coordination result**. State the chosen semantic object, owning producer, intended consumer, prerequisite status, target resume point, and any unresolved binding or route question. Read `references/coordination-contract.md`.
12. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-shared --stage end`. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
13. **Close the operation set**. After end callbacks, follow the Operation Set Closeout contract in `references/operation-set-closeout.md` and invoke `isomer-op-entrypoint->operation-sets`. When material operation-set files exist, accept and verify every disposition, require a `complete` receipt, and return the receipt id with durable record refs; treat a path, rendered file, Git commit, or terminal prose as unavailable for handoff. When no operation set was opened and only durable records were used, return `closeout: not_applicable` with those refs. If closeout is partial, stale, or invalid, return `paused` with accepted refs, the partial receipt when present, diagnostics, and the exact resume command.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the shared registry, the relevant production DeepSci skill, and the user's request, then execute the plan.

### Operation Set Closeout

After end callbacks, every production DeepSci workflow that opened an operation set or wrote material plain files must follow `references/operation-set-closeout.md` before final response, handoff, pipeline progression, or success. The closeout route invokes `isomer-op-entrypoint->operation-sets`, requires a verified complete receipt and durable refs, or returns an explicit `not_applicable` result only when no operation set was opened and all relevant outputs were already durable.

## Guardrails

- DO NOT treat shared as the owner of research work rather than the owner of vocabulary consistency.
- DO NOT treat shared as the post-preparation bootstrap manager instead of routing to `isomer-deepsci-workspace-mgr`.
- DO NOT let a durable record write, refresh, route decision, or claim decision proceed from prompt memory before `references/latest-context-preflight.md` checks current Isomer context.
- DO NOT drop the reconciled `--topic` or applicable worker selector on later CLI calls, reuse a freshness verdict after a scope change, or treat a sole manifest actor as active posture.
- DO NOT recover from a context-bearing typed failure by searching sibling Topic Workspaces, selecting another default, adding an alternate output path, or copying files into a worker workspace or Topic Main unless the user explicitly requests a separate unmanaged copy.
- DO NOT bind placeholders to paths, database rows, or Artifact kinds before a storage-binding pass.
- DO NOT invent a new semantic object when an existing registry entry already fits.
- DO NOT let a route decision hide the evidence or blocker that made the route justified.
- DO NOT infer run-to authorization from an ordinary `do <task>` request, make it global or session-wide, or continue after the named target.
- DO NOT merge prerequisite Runs, skip callbacks or Gates, or add a backward edge to a single-pass recipe.
- DO NOT report a material operation-set file, Git commit, render, terminal summary, or worker path as a durable handoff without verified acceptance.

## Reference Routing

Read `references/latest-context-preflight.md` whenever a production DeepSci skill needs current topic context, runtime state, durable record freshness, duplicate-record handling, prompt-versus-durable-context conflict routing, or the storage-neutral `DEEPSCI:LATEST-CONTEXT-SNAPSHOT`. Read `references/artifact-lineage-recording.md` whenever a durable record is produced from, selected from, merged from, revised from, or follows up prior durable records. Invoke `isomer-op-entrypoint->research-ideas` and read `references/research-idea-recording.md` whenever a durable record creates or changes a research concept. Read `references/operation-set-closeout.md` after end callbacks whenever a production workflow opened an operation set or wrote material plain files. Read `references/semantic-placeholders.md` whenever a production DeepSci skill needs shared handoff vocabulary. Read `references/coordination-contract.md` whenever the question is about ownership, routing, unresolved storage binding, post-preparation bootstrap routing, cwd context, or handoff shape. Read `references/prerequisite-recovery.md` whenever a known producer can satisfy a target input or an explicitly authorized controller needs to consume a bounded terminal report.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Semantic-registry reuse rate: fraction of coordination questions resolved with an existing shared semantic object instead of a new invented term; higher is better.
- Premature-binding count: number of placeholder, handoff, route, or semantic object decisions bound to concrete paths, database rows, or final storage kinds before a storage-binding pass; lower is better.

### Checks

- Coordination check: the handoff, route, placeholder, or storage-binding ambiguity is named before shared rules are applied.
- Latest-context check: durable record work uses `references/latest-context-preflight.md` before prompt memory, chat memory, prior prose, or remembered research state is treated as current.
- Lineage check: durable record writes use `references/artifact-lineage-recording.md` to separate canonical parents and generation groups from query-index hints.
- Idea-recording check: idea-bearing acceptance invokes `isomer-op-entrypoint->research-ideas`, commits the durable record and promised canonical effects together, and verifies facets, exact realizations, generations, decision options, transitions, terminal refs, and lineage before completion.
- Operation-set closeout check: after end callbacks, material files have a verified complete receipt and durable refs, or a file-free durable workflow reports `closeout: not_applicable` with its refs; partial or invalid closeout pauses with diagnostics and a resume command.
- Registry check: the closest existing semantic object is chosen from `references/semantic-placeholders.md` before any new vocabulary is introduced.
- Ownership check: domain work is routed back to the owning production DeepSci skill rather than handled by shared.
- Bootstrap check: post-preparation workspace bootstrap questions route to `isomer-deepsci-workspace-mgr`, with the current cwd classified as Topic Workspace, Topic Actor Workspace, `topic.repos.main`, or formal Agent Workspace when possible.
- Binding check: unresolved storage bindings remain semantic until a later binding pass assigns durable labels, typed refs, paths, or schemas.
- Result check: the final coordination result states chosen semantic object, owning producer, intended consumer, and unresolved binding or route question.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
