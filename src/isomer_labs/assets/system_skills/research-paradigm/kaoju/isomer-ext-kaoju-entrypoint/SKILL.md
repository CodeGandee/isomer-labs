---
name: isomer-ext-kaoju-entrypoint
description: Use when a user asks to choose survey directions, build or ingest a reading list, draft or build a paper, export a survey wiki, ingest source code, prepare an environment, run a code trial, or invoke a retained Kaoju compatibility procedure.
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer Kaoju Entrypoint

## Plan First

Pipeline execution is a complex process. Before executing any pipeline task, use your internal todo list or planning tool to create a plan for the requested work. Keep the plan current as stages complete, blockers appear, or the requested scope changes.

## Overview

Use this public execution entrypoint as the route-and-proceed dispatcher for one accepted survey intent or task-only request. It selects a bounded parent command or protected Kaoju member, preserves Gates and durable checkpoints, and stops at the selected terminal boundary. Empty invocation, `help`, and orientation-only requests delegate read-only output to the independent `$isomer-ext-kaoju-welcome` sibling.

When a procedure creates or changes durable research concepts, invoke `isomer-op-entrypoint->research-ideas` and apply the Kaoju mapping reference exposed by `isomer-ext-kaoju-entrypoint->shared`. A pipeline checkpoint or terminal report cannot substitute for missing canonical idea effects.

## When to Use

Use as the single public router for the eleven current survey intents, retained compatibility procedures, grouped managers, and focused stage tasks. Prefer `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>`; task-only invocation may select a protected stage without exposing it as a top-level skill.

## Workflow

1. **Resolve the public request and context**. Accept `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>`, a task-only request, or empty invocation. Empty invocation, `help`, and orientation-only requests delegate to `$isomer-ext-kaoju-welcome` with supplied context intact; otherwise identify the Research Topic, Topic Workspace, survey intent or protected stage, clarification posture, accepted refs, and requested resume stage. Run `isomer-cli --print-json project self location`, then `isomer-cli --print-json project self check --scope topic --topic <prompt-topic>` when the prompt names a topic or the selector-free topic check when it does not. Stop on unresolved or conflicting context, report any default source, and pin the reconciled Research Topic as `--topic <topic>` on every applicable downstream command.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-ext-kaoju-entrypoint --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Load the checked contract**. Run `isomer-cli --print-json ext kaoju process show` and treat its versioned process data as the exact skill, intent, compatibility, and manager inventory. Do not invent a public command or read a package path directly.
4. **Route one intent**. Select the exact command page or manifest-declared protected member below. For a protected member, resolve its logical id to `subskills/<logical-id>/SKILL-MAIN.md`, then read only that entrypoint and its directly required local resources; do not scan or preload sibling subskills. This skill coordinates stages but does not search, interpret evidence, mutate environments, execute trials, author canonical paper content, or write wiki files itself.
5. **Preflight target prerequisites and mutation posture**. Resolve the command page's accepted inputs, audit state, readiness, known producer routes, and Gates before beginning the target Run. `create-topic` delegates generic state to `isomer-op-entrypoint->topic-create`, invokes `isomer-ext-kaoju-entrypoint->topic-creator`, and stops without a research Run. Installation, welcome, help, `explore`, and status-only management remain non-mutating: they may report uninitialized mindset intent and the exact `create-topic` route, but they do not enumerate topics, invoke create-missing, create a Run, or write a Source. If another producer can satisfy a gap and the user gave only an ordinary target request, return `paused` and present Run to the target, Execute the next prerequisite only, Inspect or choose another route, and Stop before prerequisite mutation.
6. **Resolve optional topic-owned Mindset Sources before concrete work**. For a research command with a checked mindset route, select its key and resolve the deterministic topic file without invoking `topic-creator`. A present valid Source is eligible for snapshot after Run creation. A missing file is an allowed no-mindset posture. Any existing but invalid, unreadable, mismatched, ambiguous, or unsafe Source blocks with exact diagnostics and the Kaoju `create-topic` repair route; never mark it missing, overwrite it, or substitute a packaged default. Explicit `create-topic` and explicitly requested create-missing work remain the only Source-generation routes.
7. **Plan authorized run-to recovery**. Only after explicit target-scoped run-to authorization, maintain an internal dependency plan with the native planning tool. The current agent acts as prompt-level controller, invokes each prerequisite as a separate bounded procedure Run, refreshes durable state after each terminal report, resumes the original target when ready, and stops after that target.
8. **Begin the selected procedure Run**. Use `isomer-cli project runs begin` with the procedure id, control mode, input refs, expected outputs, and first stage. Never merge prerequisite and target procedures into one Run.
9. **Persist the applicable Run mindset resolution**. Use checked process routes to select `paper.deep-dive` for deep or full-text paper examination, `paper.skimming` for skim or triage examination, and `source-code.ingest` for repository or source-tree examination. Pause on ambiguous paper depth. After Run creation, re-resolve the selected deterministic topic Source. For a present valid Source, pin the current Research Topic and one current Survey Contract, create the exact Run-scoped `KAOJU:MINDSET-RECORD` snapshot, then run `isomer-cli project runs resolve-mindset <run-id> --mindset-key <key> --record-ref <record-ref>`. For an absent file, run the same command with `--source-missing`; the service verifies absence and stores `skipped_source_missing` with no placeholder Artifact. Treat the first resolution as immutable and pass the Run ref, key, disposition, and Record ref only when present in every focused-owner handoff. Actions without a declared route continue unchanged.
10. **Honor clarification and Gates**. Ask one material choice at a time, preserve custom and multiple selections, and stop at every required human, publication, or network-exposure Gate. Run-to does not satisfy a Gate.
11. **Dispatch focused owners**. Invoke only the skills and typed CLI services named by the command page, retaining the pinned `--topic <topic>`, applicable worker selector, Run ref, mindset key, and persisted disposition across cwd changes. For `recorded`, also pass the Mindset Record ref; consumers answer and checkpoint its immutable materialized questions and do not re-read a changed Source during the active Run. For `skipped_source_missing`, consumers skip Record loading, mindset questions, collector checks, revisions, and terminal Record production while preserving the ordinary reading workflow. Operational support mutation uses a recorded Service Request and managed research execution uses an Execution Adapter Command Request. Repository acquisition and identity verification are the explicit exception: the acting user or agent runs prompt-sensitive commands externally, verifies the result, and only then invokes semantic registration and typed Artifact operations.
12. **Checkpoint each stage and mindset**. Record completed refs, pending Gate, blockers, Service Requests, terminal status, and the first incomplete stage as the resume hint while preserving the immutable Run mindset resolution. Before a `recorded` Run completes, pauses, or blocks, revise its Mindset Record with optimistic concurrency, mark every materialized or explicitly assigned supplemental question answered, unresolved, or not applicable, mark the collector checked, and retain evidence refs. A `skipped_source_missing` Run may complete without a Record and must report the key, missing Source posture, and absent Record ref. Reject applicable claim-bearing acceptance or `complete` when neither a terminal referenced Record nor a verified skipped resolution exists.
13. **Route mid-reading questions by explicit target**. Ordinary paper and source-code follow-up questions remain in Source Digest, Claim-Evidence Ledger, Associated Source Code, or another applicable reading Artifact. For `recorded`, add supplemental Record rows only under explicit Record or both targeting. Source-only requests directly validate and edit the topic Source without a Record row; Record-only requests use `record_only`; both requests move `source_update_requested` to `source_updated` with the new relative path and digest while the active Record keeps its original snapshot. A `skipped_source_missing` Run has no Record to target; report that posture and offer explicit `create-topic` followed by a later Run. Clarify an ambiguous bare-mindset mutation request.
14. **Audit before synthesis or paper writing**. Accepted claim-bearing output never bypasses the audit boundary.
15. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-ext-kaoju-entrypoint --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
16. **Return one terminal report**. Report `complete`, `paused`, or `blocked`; accepted refs; Run mindset key and disposition; Mindset Record ref or explicit absence; Gate, Service Request, and blocker refs; limitations; and resume point. A bounded procedure does not choose another macro intent. An explicitly authorized prompt-level controller may consume an in-closure recovery route only after this report is recorded.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, refine the existing plan into a step-by-step plan from this skill's constraints, then execute it.

## Protected Subskills

| Member | Logical ID | When to Route Here | Internal Designator |
| --- | --- | --- | --- |
| `acquire` | `isomer-kaoju-acquire` | Selected sources or materials need a governed checkout, full-text fetch, dataset or model acquisition, immutable revision, or access and license capture. | `isomer-ext-kaoju-entrypoint->acquire` |
| `audit` | `isomer-kaoju-audit` | Collected evidence, comparisons, trials, deltas, or draft conclusions need a non-mutating coverage, identity, provenance, traceability, or fairness audit before closeout. | `isomer-ext-kaoju-entrypoint->audit` |
| `compare` | `isomer-kaoju-compare` | Named works need theory comparison, an empirical comparison contract, or a controlled actual-run comparison with fairness and uncertainty limits. | `isomer-ext-kaoju-entrypoint->compare` |
| `discover` | `isomer-kaoju-discover` | The survey needs broad field discovery, curated-reference resolution, seed expansion, version-family mapping, query provenance, or bounded source selection before acquisition. | `isomer-ext-kaoju-entrypoint->discover` |
| `examine` | `isomer-kaoju-examine` | Acquired papers or code need full-text or source inspection, exact locators, paper-code mapping, Source Digests, contradiction tracking, or ledger updates. | `isomer-ext-kaoju-entrypoint->examine` |
| `explore` | `isomer-kaoju-explore` | The user has a concrete survey task but needs an interactive, read-only planning discussion to agree on intent, scope, evidence strategy, and the right command before any durable work. | `isomer-ext-kaoju-entrypoint->explore` |
| `export` | `isomer-kaoju-export` | Accepted survey records must become a self-contained LLM Wiki, a packaged local viewer, or a governed viewer launch after synthesis or writing. | `isomer-ext-kaoju-entrypoint->export` |
| `frame` | `isomer-kaoju-frame` | The request needs a bounded Survey Contract covering clarification choices, intent, scope, evidence depth, resources, Gates, or stop conditions before evidence work. | `isomer-ext-kaoju-entrypoint->frame` |
| `reproduce` | `isomer-kaoju-reproduce` | The user is making a genuine paper-reproduction claim that requires a source-grounded fidelity contract rather than an ordinary method trial or generated-data probe. | `isomer-ext-kaoju-entrypoint->reproduce` |
| `shared` | `isomer-kaoju-shared` | Another Kaoju member needs common evidence, identity, lineage, clarification, Gate, owner-routing, Artifact, or terminal-status rules rather than a standalone survey stage. | `isomer-ext-kaoju-entrypoint->shared` |
| `synthesize` | `isomer-kaoju-synthesize` | An accepted audit and evidence set are ready to produce survey conclusions such as a Field Summary, Survey Delta, Claim Status Table, or Kaoju Dossier. | `isomer-ext-kaoju-entrypoint->synthesize` |
| `topic-creator` | `isomer-kaoju-topic-creator` | Generic topic state is ready and Kaoju must derive, preserve, inspect, replace, or reconcile topic-owned Mindset Sources. | `isomer-ext-kaoju-entrypoint->topic-creator` |
| `trial` | `isomer-kaoju-trial` | A source-code method needs governed environment preparation, a task-critical smoke check, or one approved bounded trial without claiming full reproduction. | `isomer-ext-kaoju-entrypoint->trial` |
| `workspace` | `isomer-kaoju-workspace-mgr` | Survey work needs readiness checks for Topic Workspace state, registered datasets, repository posture, resource boundaries, or mutation ownership before a stage proceeds. | `isomer-ext-kaoju-entrypoint->workspace` |
| `write` | `isomer-kaoju-write` | An accepted audit and synthesis are ready for canonical MyST paper drafting, template exchange, derived Markdown or TeX, PDF construction, validation, and publication bundling. | `isomer-ext-kaoju-entrypoint->write` |

## Survey Intents

| Intent | Owner | Detail |
| --- | --- | --- |
| `create-topic` | `isomer-kaoju-topic-creator` after generic topic creation | `commands/create-topic.md` |
| `choose-directions` | `isomer-kaoju-frame` | `commands/choose-directions.md` |
| `build-reading-list` | `isomer-kaoju-discover` | `commands/build-reading-list.md` |
| `ingest-reading-item` | `isomer-kaoju-acquire`, then `isomer-kaoju-examine` | `commands/ingest-reading-item.md` |
| `draft-paper` | `isomer-kaoju-write` | `commands/draft-paper.md` |
| `manage-paper-template` | `isomer-kaoju-write` | Resolve content versus LaTeX role, then use `commands/manage-paper-template.md` |
| `build-paper-pdf` | `isomer-kaoju-write` | `commands/build-paper-pdf.md` |
| `export-survey-wiki` | `isomer-kaoju-export` | `commands/export-survey-wiki.md` |
| `ingest-source-code` | `isomer-kaoju-acquire`, then `isomer-kaoju-examine` | `commands/ingest-source-code.md` |
| `prepare-code-run` | `isomer-kaoju-trial` plus Service Team | `commands/prepare-code-run.md` |
| `run-code-trial` | `isomer-kaoju-trial` | `commands/run-code-trial.md` |

## Compatibility Procedures

| Procedure | Current Route | Detail |
| --- | --- | --- |
| `landscape-pass` | Frame, discover, acquire, examine, audit, synthesize | `commands/landscape-pass.md` |
| `curated-intake-pass` | Discover, acquire, examine, audit | `commands/curated-intake-pass.md` |
| `direction-expansion-pass` | Discover, acquire, examine, audit | `commands/direction-expansion-pass.md` |
| `theory-comparison-pass` | Examine, compare, audit, synthesize | `commands/theory-comparison-pass.md` |
| `method-trial-pass` | Trial for bounded execution; reproduce only for genuine reproduction | `commands/method-trial-pass.md` |
| `comparative-pass` | Frame, trial, compare, audit | `commands/comparative-pass.md` |
| `audit-survey-pass` | Audit, then synthesize if accepted | `commands/audit-survey-pass.md` |
| `paper-pass` | `draft-paper`, then optional `build-paper-pdf` | `commands/paper-pass.md` |
| `create-paper-template` | Construct a mutable named content-template tree, then optionally export | `commands/create-paper-template.md` |

## Exploration Procedures

| Procedure | Owner | Detail |
| --- | --- | --- |
| `explore` | `isomer-kaoju-explore` | `commands/explore.md` |

## Grouped Managers

| Manager | Actions | Detail |
| --- | --- | --- |
| `manage-survey` | `list`, `show`, `status`, `export` | `commands/manage-survey.md` |
| `manage-dataset` | `register`, `list`, `show`, `refresh`, `remove` | `commands/manage-dataset.md` |
| `manage-paper-template` | `list`, `show`, `create`, `copy`, `update`, `replace`, `merge`, `file`, `metadata`, `export`, `observe`, `archive`, `delete`, `migrate` | `commands/manage-paper-template.md` |

## Reference Routing

Use `isomer-ext-kaoju-entrypoint->shared` for Artifact, evidence, interaction, Gate, owner-routing, terminal, and prerequisite-recovery contracts. The shared Prerequisite Recovery reference defines ordinary pause, target-scoped run-to authorization, separate procedure Runs, and nondelegable boundaries. Use `isomer-ext-kaoju-entrypoint->workspace` when readiness is missing or stale, and load only the selected command page plus its named focused owners.

## Artifact Operations

Resolve `KAOJU:PROCEED-DECISION`, `KAOJU:MINDSET-RECORD`, and `KAOJU:SURVEY-TERMINAL-REPORT` through `ext kaoju bindings describe KAOJU:WHAT`. Persist them only through typed `project artifacts put` or binding-permitted `revise`; use `project runs resolve-mindset` for verified recorded or missing-Source posture and other `project runs` commands for checkpoints and terminal Run state. A Mindset Source is derived intent and never uses Artifact operations.

## Miscellaneous

`help` lists this checked surface. It performs no durable mutation.

## Operational Notes

- Verify durable refs and restart at the first incomplete stage.

## Guardrails

- DO NOT treat resume as a fresh procedure.
- DO NOT ask an operational service skill to make a research decision.
- DO NOT use a directory scan when the state DB query is empty or ambiguous.
- DO NOT route wiki work to an external skill checkout.
- DO NOT treat TeX or PDF as canonical paper state.
- DO NOT use generic Artifact revise, direct SQL, or managed-file edits for mutable named content or LaTeX templates.
- DO NOT discover or mutate a template before resolving its content or LaTeX role.
- DO NOT select a source for an unnamed database-template update outside the selected role's one-edited-export, `<exchange-root>/<kind>/main/`, then user-clarification order.
- DO NOT treat a typed not-found, wrong-scope, context-conflict, export, composition, or build failure as permission to change the pinned topic, search a sibling Topic Workspace, select another default, or copy material to a Topic Actor Workspace, Agent Workspace, Topic Main, or arbitrary directory. Compare returned selected-context metadata with the pinned target and correct selectors or route readiness instead.
- DO NOT reuse a preflight after an intentional Research Topic, worker, or operation-scope change; rerun context alignment and pin the new selectors.
- DO NOT infer run-to authorization from an ordinary `do <task>` request or make it global or session-wide.
- DO NOT skip required audits or Gates, merge prerequisite Runs, or continue after the named target.

## Chat Response

Present normal chat responses in natural-language Markdown. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat. Lead with the selected intent and current outcome. Name durable refs, blockers, limitations, and the exact resume stage.
