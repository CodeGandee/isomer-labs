---
name: isomer-kaoju-pipeline
description: Use when a user requests a bounded Kaoju survey, curated intake, direction expansion, theory comparison, paper-method trial, empirical comparison, survey audit, or survey and dataset management.
---

# Kaoju Pipeline

## Overview

Select and run one bounded survey procedure or grouped management action. Preserve stage handoffs, require audit before synthesis, and stop with explicit status instead of choosing the next macro procedure autonomously.

Read the shared artifact semantics and recording rules before dispatch, each producer skill's `artifact-bindings.md` before an accepted write, and this skill's binding page before creating `kaoju:survey-terminal-report`. An unavailable binding or record surface is a storage blocker; do not fall back to invented paths, profiles, canonical Markdown, or untracked JSON.

## Workflow

1. **Resolve context**. Identify the Research Topic, Research Inquiry, Topic Workspace, user request, clarification mode, accepted prior refs, and requested start stage.
2. **Apply begin callbacks**. Run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-pipeline --stage begin`; follow compatible instructions, while empty callback results continue normally and conflicts must be reported.
3. **Select one command**. Choose the procedure or helper whose trigger matches the request; use `help` only to explain the public interface.
4. **Honor clarification-first**. When requested, inspect read-only context, ask one A/B/C/D choice for each material ambiguity, and obtain the user's proceed choice before acquisition, mutation, or Runs.
5. **Validate predecessors**. Require the command page's accepted input refs; resume from an explicit starting stage only after identity, lineage, and audit-state checks.
6. **Execute one bounded recipe**. Invoke the focused Kaoju skills in the listed order, preserve handoff refs, and route governed operations to their platform owners.
7. **Audit before synthesis**. Every normal survey procedure invokes `$isomer-kaoju-audit`; invoke `$isomer-kaoju-synthesize` only from an accepted Audit Report.
8. **Apply end callbacks**. After tentative outputs exist, run `isomer-cli --print-json project skill-callbacks resolve --skill isomer-kaoju-pipeline --stage end`; apply compatible instructions, while empty callback results continue normally and conflicts must be reported.
9. **Return terminal report**. Report `complete`, `paused`, or `blocked`, accepted output refs, stage outcomes, resources, Gates, blockers, and a resume point when applicable.

If the task does not map cleanly to these steps, use the native planning tool to build and execute a step-by-step plan from the available commands and constraints without inventing a new public procedure.

## When to Use

Use for the seven named survey procedures and two grouped managers below. Do not use this skill for generic repository refresh, environment repair, standalone reproduction, source audit, list-passes, a full-Kaoju macro, or a generic resume procedure; keep those steps inside the active procedure or route them to their owner.

## Subcommands

### Procedural Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `landscape-pass` | Survey a field and produce related works plus a bounded summary. | `commands/landscape-pass.md` |
| `curated-intake-pass` | Digest user-nominated sources and apply an audited survey delta. | `commands/curated-intake-pass.md` |
| `direction-expansion-pass` | Trace seed works backward, nearby, forward, and after the seeds. | `commands/direction-expansion-pass.md` |
| `theory-comparison-pass` | Compare named works through source-grounded domain dimensions. | `commands/theory-comparison-pass.md` |
| `method-trial-pass` | Obtain and run one paper method on intended or generated data. | `commands/method-trial-pass.md` |
| `comparative-pass` | Plan and run a controlled empirical comparison after user approval. | `commands/comparative-pass.md` |
| `audit-survey-pass` | Audit accepted survey evidence and synthesize only when ready. | `commands/audit-survey-pass.md` |

### Helper Subcommands

| Subcommand | Actions | Detail |
| --- | --- | --- |
| `manage-survey` | `list`, `show`, `status`, `export` | `commands/manage-survey.md` |
| `manage-dataset` | `register`, `list`, `show`, `refresh`, `remove` | `commands/manage-dataset.md` |

Helpers group object operations and remain lower-level implementation commands. Ordinary users should enter through a survey procedure unless they explicitly request one management action.

### Misc Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | List the seven procedures, their triggers, and public support interface. | This entrypoint. |

## Clarification and Resume

Clarification-first is an interaction mode shared by all procedures. Use `$isomer-kaoju-shared` to present three concrete A/B/C options plus D for free form, mark one suggestion, then ask whether the user wants to clarify more or proceed.

Resume is accepted context: name durable input refs, verify them, state the starting stage, and preserve earlier failures and Decisions. If accepted refs cannot establish safe continuation, return `paused` or `blocked` rather than starting over silently.

## Reference Routing

Read the selected local command page, then use `$isomer-kaoju-shared` for cross-stage contracts. Invoke `$isomer-kaoju-workspace-mgr`, `$isomer-kaoju-frame`, `$isomer-kaoju-discover`, `$isomer-kaoju-acquire`, `$isomer-kaoju-examine`, `$isomer-kaoju-reproduce`, `$isomer-kaoju-compare`, `$isomer-kaoju-audit`, and `$isomer-kaoju-synthesize` only as required by that page.

## Foundational Principle

One command means one bounded user intent. Do not expand a completed pass into another macro procedure merely because the evidence suggests useful follow-up work.

## Rationalization Table

| Rationalization | Required response |
| --- | --- |
| “A full run is more helpful.” | Execute only the selected procedure and return possible next routes. |
| “Audit can wait until the final project.” | Audit every claim-bearing procedure before synthesis. |
| “Resume should be a command.” | Treat it as verified refs plus an explicit starting stage. |
| “Separate CRUD verbs are clearer.” | Keep survey and dataset actions grouped under their object managers. |

## Red Flags

- The command surface contains a generic maintenance task.
- A procedure synthesizes from an unaccepted Audit Report.
- Empirical preparation starts before a Proceed Decision.
- The terminal report starts another procedure.

## Common Mistakes

- Choosing `method-trial-pass` for several methods. Use `comparative-pass` when controlled cross-method numbers are the intent.
- Treating curated intake as automatic endorsement. Every item still needs identity, inspection, disposition, and audit.
- Exporting a survey as new evidence. Export changes representation, not evidence status or lineage.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
