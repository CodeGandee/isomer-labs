---
name: isomer-ext-kaoju-entrypoint
description: Use when a user asks to choose survey directions, build or ingest a reading list, draft or build a paper, export a survey wiki, ingest source code, prepare an environment, run a code trial, or invoke a retained Kaoju compatibility procedure.
skill_invocation_notation: >
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

Use as the single public router for the ten current survey intents, retained compatibility procedures, grouped managers, and focused stage tasks. Prefer `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>`; task-only invocation may select a protected stage without exposing it as a top-level skill.

## Workflow

1. **Resolve the public request and context**. Accept `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>`, a task-only request, or empty invocation. Empty invocation, `help`, and orientation-only requests delegate to `$isomer-ext-kaoju-welcome` with supplied context intact; otherwise identify the Research Topic, Topic Workspace, survey intent or protected stage, clarification posture, accepted refs, and requested resume stage.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-ext-kaoju-entrypoint --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Load the checked contract**. Run `isomer-cli --print-json ext kaoju process show` and treat its versioned process data as the exact skill, intent, compatibility, and manager inventory. Do not invent a public command or read a package path directly.
4. **Route one intent**. Select the exact command page below. This skill coordinates stages but does not search, interpret evidence, mutate environments, execute trials, author canonical paper content, or write wiki files itself.
5. **Preflight target prerequisites**. Resolve the command page's accepted inputs, audit state, readiness, known producer routes, and Gates before beginning the target Run. If a producer can satisfy a gap and the user gave only an ordinary target request, return `paused` and present Run to the target, Execute the next prerequisite only, Inspect or choose another route, and Stop before prerequisite mutation.
6. **Plan authorized run-to recovery**. Only after explicit target-scoped run-to authorization, maintain an internal dependency plan with the native planning tool. The current agent acts as prompt-level controller, invokes each prerequisite as a separate bounded procedure Run, refreshes durable state after each terminal report, resumes the original target when ready, and stops after that target.
7. **Begin the selected procedure Run**. Use `isomer-cli project runs begin` with the procedure id, control mode, input refs, expected outputs, and first stage. Never merge prerequisite and target procedures into one Run.
8. **Honor clarification and Gates**. Ask one material choice at a time, preserve custom and multiple selections, and stop at every required human, publication, or network-exposure Gate. Run-to does not satisfy a Gate.
9. **Dispatch focused owners**. Invoke only the skills and typed CLI services named by the command page. Operational support mutation uses a recorded Service Request and managed research execution uses an Execution Adapter Command Request. Repository acquisition and identity verification are the explicit exception: the acting user or agent runs prompt-sensitive commands externally, verifies the result, and only then invokes semantic registration and typed Artifact operations.
10. **Checkpoint each stage**. Record completed refs, pending Gate, blockers, Service Requests, terminal status, and the first incomplete stage as the resume hint.
11. **Audit before synthesis or paper writing**. Accepted claim-bearing output never bypasses the audit boundary.
12. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-ext-kaoju-entrypoint --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
13. **Return one terminal report**. Report `complete`, `paused`, or `blocked`; accepted refs; Run, Gate, Service Request, and blocker refs; limitations; and resume point. A bounded procedure does not choose another macro intent. An explicitly authorized prompt-level controller may consume an in-closure recovery route only after this report is recorded.

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
| `export` | `isomer-kaoju-export` | Accepted survey records must become a self-contained LLM Wiki, a packaged local viewer, or a governed viewer launch after synthesis or writing. | `isomer-ext-kaoju-entrypoint->export` |
| `frame` | `isomer-kaoju-frame` | The request needs a bounded Survey Contract covering clarification choices, intent, scope, evidence depth, resources, Gates, or stop conditions before evidence work. | `isomer-ext-kaoju-entrypoint->frame` |
| `reproduce` | `isomer-kaoju-reproduce` | The user is making a genuine paper-reproduction claim that requires a source-grounded fidelity contract rather than an ordinary method trial or generated-data probe. | `isomer-ext-kaoju-entrypoint->reproduce` |
| `shared` | `isomer-kaoju-shared` | Another Kaoju member needs common evidence, identity, lineage, clarification, Gate, owner-routing, Artifact, or terminal-status rules rather than a standalone survey stage. | `isomer-ext-kaoju-entrypoint->shared` |
| `synthesize` | `isomer-kaoju-synthesize` | An accepted audit and evidence set are ready to produce survey conclusions such as a Field Summary, Survey Delta, Claim Status Table, or Kaoju Dossier. | `isomer-ext-kaoju-entrypoint->synthesize` |
| `trial` | `isomer-kaoju-trial` | A source-code method needs governed environment preparation, a task-critical smoke check, or one approved bounded trial without claiming full reproduction. | `isomer-ext-kaoju-entrypoint->trial` |
| `workspace` | `isomer-kaoju-workspace-mgr` | Survey work needs readiness checks for Topic Workspace state, registered datasets, repository posture, resource boundaries, or mutation ownership before a stage proceeds. | `isomer-ext-kaoju-entrypoint->workspace` |
| `write` | `isomer-kaoju-write` | An accepted audit and synthesis are ready for canonical MyST paper drafting, template exchange, derived Markdown or TeX, PDF construction, validation, and publication bundling. | `isomer-ext-kaoju-entrypoint->write` |

## Survey Intents

| Intent | Owner | Detail |
| --- | --- | --- |
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

## Grouped Managers

| Manager | Actions | Detail |
| --- | --- | --- |
| `manage-survey` | `list`, `show`, `status`, `export` | `commands/manage-survey.md` |
| `manage-dataset` | `register`, `list`, `show`, `refresh`, `remove` | `commands/manage-dataset.md` |
| `manage-paper-template` | `list`, `show`, `create`, `copy`, `update`, `replace`, `merge`, `file`, `metadata`, `export`, `observe`, `archive`, `delete`, `migrate` | `commands/manage-paper-template.md` |

## Reference Routing

Use `isomer-ext-kaoju-entrypoint->shared` for Artifact, evidence, interaction, Gate, owner-routing, terminal, and prerequisite-recovery contracts. The shared Prerequisite Recovery reference defines ordinary pause, target-scoped run-to authorization, separate procedure Runs, and nondelegable boundaries. Use `isomer-ext-kaoju-entrypoint->workspace` when readiness is missing or stale, and load only the selected command page plus its named focused owners.

## Artifact Operations

Resolve `KAOJU:PROCEED-DECISION` and `KAOJU:SURVEY-TERMINAL-REPORT` through `ext kaoju bindings describe KAOJU:WHAT`. Persist them only through typed `project artifacts put` or binding-permitted `revise`; use `project runs` for procedure checkpoints and terminal Run state.

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
- DO NOT infer run-to authorization from an ordinary `do <task>` request or make it global or session-wide.
- DO NOT skip required audits or Gates, merge prerequisite Runs, or continue after the named target.

## Chat Response

Present normal chat responses in natural-language Markdown. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat. Lead with the selected intent and current outcome. Name durable refs, blockers, limitations, and the exact resume stage.
