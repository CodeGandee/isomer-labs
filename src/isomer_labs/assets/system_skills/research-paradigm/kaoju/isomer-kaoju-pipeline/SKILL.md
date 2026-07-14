---
name: isomer-kaoju-pipeline
description: Use when a user asks to choose survey directions, build or ingest a reading list, draft or build a paper, export a survey wiki, ingest source code, prepare an environment, run a code trial, or invoke a retained Kaoju compatibility procedure.
---

# Kaoju Pipeline

## Overview

Route one accepted survey intent to its bounded owner, preserve Gates and durable checkpoints, and stop at the selected terminal boundary. This skill never performs a focused owner's research or operational work.

## Workflow

1. **Resolve context**. Identify the Research Topic, Topic Workspace, user intent, clarification posture, accepted refs, and requested resume stage.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-pipeline --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Load the checked contract**. Treat `../contracts/survey-process.v2.json` as the exact skill, intent, compatibility, and manager inventory. Do not invent a public command.
4. **Route one intent**. Select the exact command page below. This skill coordinates stages but does not search, interpret evidence, mutate environments, execute trials, author canonical paper content, or write wiki files itself.
5. **Begin a Run**. Use `isomer-cli project runs begin` with the procedure id, control mode, input refs, expected outputs, and first stage.
6. **Honor clarification and Gates**. Ask one material choice at a time, preserve custom and multiple selections, and stop at every required human, publication, or network-exposure Gate.
7. **Dispatch focused owners**. Invoke only the skills and typed CLI services named by the command page. Operational support mutation uses a recorded Service Request; executable work uses an Execution Adapter Command Request.
8. **Checkpoint each stage**. Record completed refs, pending Gate, blockers, Service Requests, terminal status, and the first incomplete stage as the resume hint.
9. **Audit before synthesis or paper writing**. Accepted claim-bearing output never bypasses the audit boundary.
10. **Apply end callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-pipeline --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
11. **Return one terminal report**. Report `complete`, `paused`, or `blocked`; accepted refs; Run, Gate, Service Request, and blocker refs; limitations; and resume point. Do not choose another macro intent autonomously.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from this skill's constraints.

## When to Use

Use as the single public router for the ten current survey intents, retained compatibility procedures, and grouped managers. Call a focused Kaoju skill directly only when the caller already selected its bounded stage and supplies verified predecessors.

## Survey Intents

| Intent | Owner | Detail |
| --- | --- | --- |
| `choose-directions` | `isomer-kaoju-frame` | `commands/choose-directions.md` |
| `build-reading-list` | `isomer-kaoju-discover` | `commands/build-reading-list.md` |
| `ingest-reading-item` | `isomer-kaoju-acquire`, then `isomer-kaoju-examine` | `commands/ingest-reading-item.md` |
| `draft-paper` | `isomer-kaoju-write` | `commands/draft-paper.md` |
| `manage-paper-template` | `isomer-kaoju-write` | `commands/manage-paper-template.md` |
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
| `create-paper-template` | Write a canonical MyST structure and template, then optionally export | `commands/create-paper-template.md` |

## Grouped Managers

| Manager | Actions | Detail |
| --- | --- | --- |
| `manage-survey` | `list`, `show`, `status`, `export` | `commands/manage-survey.md` |
| `manage-dataset` | `register`, `list`, `show`, `refresh`, `remove` | `commands/manage-dataset.md` |
| `manage-paper-template` | `export`, `apply`, `inspect`, `status` | `commands/manage-paper-template.md` |

## Reference Routing

Use `$isomer-kaoju-shared` for Artifact, evidence, interaction, Gate, owner-routing, and terminal contracts. Use `$isomer-kaoju-workspace-mgr` when readiness is missing or stale, and load only the selected command page plus its named focused owners.

## Artifact Operations

Resolve `kaoju:proceed-decision` and `kaoju:survey-terminal-report` through `project artifacts describe`. Persist them only through typed `project artifacts put` or binding-permitted `revise`; use `project runs` for procedure checkpoints and terminal Run state.

## Miscellaneous

`help` lists this checked surface. It performs no durable mutation.

## Common Mistakes

- Treating resume as a fresh procedure. Verify durable refs and restart at the first incomplete stage.
- Asking an operational service skill to make a research decision.
- Using a directory scan when the state DB query is empty or ambiguous.
- Routing wiki work to an external skill checkout.
- Treating TeX or PDF as canonical paper state.

## Chat Response

Lead with the selected intent and current outcome. Use natural-language Markdown and name durable refs, blockers, limitations, and the exact resume stage. Keep machine schemas in Artifacts and JSON CLI output.
