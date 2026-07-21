---
name: isomer-kaoju-explore
description: Use when the user has a concrete Kaoju survey task but needs an interactive, read-only planning discussion to agree on intent, scope, evidence strategy, and the right command before any durable work.
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subcommand entrypoints.
---

# Kaoju Explore

## Overview

Turn a vague or uncertain Kaoju request into a confirmed plan and public invocation without creating files, artifacts, Runs, Gates, or Service Requests. The discussion stays in memory until the user and the agent agree on what to do next. Once consensus is reached, hand off to the selected Kaoju command or procedure and let that command own durable state.

## When to Use

Use when the user asks how to do something in Kaoju, is unsure which command fits, wants to scope a survey task, or needs to choose between directions, reading lists, intake strategies, comparisons, trials, paper plans, or wiki exports before starting work. Do not use this skill to perform discovery, acquisition, examination, execution, audit, synthesis, writing, or export itself.

## Workflow

1. **Resolve context**. Run `isomer-cli --print-json project self location`. If a Research Topic is named or implied, run `isomer-cli --print-json project self check --scope topic --topic <topic>`. Stop on unresolved or conflicting context and report the blocker.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-explore --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Select the context mode**. Load the appropriate subcommand page from the `commands/` directory:
   - `auto` when no specific Kaoju stage is given.
   - `directions` when the question is about framing or choosing survey directions.
   - `reading-list` when the question is about discovering or bounding a source set.
   - `intake` when the question is about acquiring or examining papers, reports, or code.
   - `comparison` when the question is about comparing theories, methods, or empirical candidates.
   - `trial` when the question is about preparing or running a bounded code trial.
   - `paper` when the question is about drafting, templating, or building a survey paper.
   - `wiki` when the question is about exporting survey records as a wiki.
   - `help` when the user wants to see available exploration modes.
4. **Run the interactive planning discussion**. Follow the selected subcommand page. Maintain an in-memory coverage map of intent, scope, evidence strategy, output form, risks, and candidate commands. Ask up to five clarification questions, one material choice at a time. Do not write files, artifacts, Runs, Gates, or Service Requests during exploration.
5. **Shape the agreed plan**. When the discussion reaches consensus, produce a plan summary containing the selected command or procedure, scope, evidence strategy, output form, risks, and the exact public invocation.
6. **Ask for explicit consent**. Present the plan summary and recommended invocation. If the user does not confirm, stop and return the plan as a paused recommendation.
7. **Hand off to the selected command**. On confirmation, load the selected command page and execute it with the pinned topic and any resolved context. Do not merge this planning exchange into the target procedure's Run.
8. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-explore --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

If the task does not map cleanly to these steps, use the native planning tool to build a bounded exploration plan from the available subcommands, context, and user goal, then execute it.

## Subcommand Routing

| Subcommand | When to Use | Public Invocation |
| --- | --- | --- |
| `auto` | General task; let the subskill pick the context mode. | `$isomer-ext-kaoju-entrypoint->explore()->auto()` |
| `directions` | Framing, scope, or direction questions. | `$isomer-ext-kaoju-entrypoint->explore()->directions()` |
| `reading-list` | Source discovery or reading-list planning. | `$isomer-ext-kaoju-entrypoint->explore()->reading-list()` |
| `intake` | Paper, report, or code intake planning. | `$isomer-ext-kaoju-entrypoint->explore()->intake()` |
| `comparison` | Theory or method comparison planning. | `$isomer-ext-kaoju-entrypoint->explore()->comparison()` |
| `trial` | Code trial or reproduction planning. | `$isomer-ext-kaoju-entrypoint->explore()->trial()` |
| `paper` | Paper drafting or template planning. | `$isomer-ext-kaoju-entrypoint->explore()->paper()` |
| `wiki` | Wiki export planning. | `$isomer-ext-kaoju-entrypoint->explore()->wiki()` |
| `help` | List modes and when to use them. | `$isomer-ext-kaoju-entrypoint->explore()->help()` |

## Reference Routing

Use `isomer-ext-kaoju-entrypoint->shared` for common evidence semantics, source identity, lineage, clarification, Gate, owner-routing, Artifact, and terminal-status rules. Use `isomer-ext-kaoju-entrypoint->workspace` when workspace readiness is missing or stale.

## Output Contract

Return one of the following:

- A confirmed public invocation for the next Kaoju command or procedure, with pinned topic and any resolved context.
- A paused recommendation if the user does not consent, including the plan summary and the exact invocation to use when ready.
- A blocker if context is unresolved, workspace readiness is missing, or a required planning question remains open.

## Gates, Blockers, and Resume

The consent step is mandatory. Context conflicts, missing workspace readiness, or an unresolved planning question pause at the explore subcommand. Resume by re-invoking `explore` with the same context; no durable Run is created for the planning phase.

## Guardrails

- DO NOT create files, artifacts, Runs, Gates, or Service Requests during exploration.
- DO NOT perform discovery, acquisition, examination, execution, audit, synthesis, writing, or export inside the explore subskill.
- DO NOT infer user consent from silence or an ordinary continuation request.
- DO NOT merge the planning exchange into the target procedure's Run.
- DO NOT treat the in-memory plan as a durable artifact.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the selected mode and current outcome. Summarize the agreed plan and the recommended invocation. If paused, state the missing decision or consent clearly.
