---
name: isomer-deepsci-pipeline
description: Use when a research task matches one of the named single-pass research procedures and you want to invoke it directly instead of choosing each production DeepSci skill by hand.
---

# Isomer Research Pipeline

## Plan First

Pipeline execution is a complex process. Before executing any pipeline task, use your internal todo list or planning tool to create a plan for the requested work. Keep the plan current as stages complete, blockers appear, or the requested scope changes.

## Overview

`isomer-deepsci-pipeline` executes one named single-pass research procedure. Each procedure (called a "pass") is a linear sequence of production DeepSci skills with automatic artifact handoffs. The skill does not loop, retry, or make macro-strategy decisions; it runs the selected pass once and produces a `DEEPSCI:PIPELINE-TERMINAL-REPORT` for an external controller.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Each pass is defined by a dedicated subcommand page under `commands/`. The recipe is embedded in that page so pass-specific customization can grow without complicating the main skill entrypoint.

## When to Use

Use this skill when a research task matches one named single-pass procedure and the caller wants automatic artifact handoffs across its fixed production DeepSci stages without starting an external macro loop.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Resolve the pipeline name**. Read the user request and determine which pass to run. See **Subcommands**.
2. **Run the latest context preflight**. Before accepting durable inputs or emitting durable records, load or create a `DEEPSCI:LATEST-CONTEXT-SNAPSHOT` for the active Research Topic. Compare prompt memory, chat memory, prior prose, and worker-local files against durable records. Report conflicts instead of silently overwriting durable state.
3. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-pipeline --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
4. **Validate the recipe context**. Build `DEEPSCI:PIPELINE-RECIPE-CONTEXT` from the named pass, optional starting stage, input artifacts, parameters, and budget or checkpoint preferences.
5. **Preflight target prerequisites**. Resolve the recipe's accepted inputs and their known focused-skill or pass producers before target mutation. If an ordinary target request has a producible gap, return `paused` and present Run to the target, Execute the next prerequisite only, Inspect or choose another route, and Stop before invoking a producer.
6. **Plan authorized run-to recovery**. Only after explicit target-scoped run-to authorization, let the current agent act as the external controller and maintain an internal dependency plan with the native planning tool. Invoke prerequisites as separate focused-skill or pass executions, validate their terminal reports, refresh current state, and resume the original target when ready. Never add a loop or backward edge to a recipe.
7. **Invoke the pass subcommand**. Execute the workflow in `commands/<pass-name>.md`. Let the subcommand load its single-pass linear recipe, run the stages, and produce its own `DEEPSCI:PIPELINE-TERMINAL-REPORT` without merging prerequisite Runs.
8. **Return the terminal report**. Surface the report to the caller or external controller; the bounded pass does not choose the next macro action. With explicit run-to authorization, the current agent may consume an in-closure recommended route only after recording this report, and it stops after the named target or at a nondelegable Gate.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-deepsci-pipeline --stage end`. Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.

If the user's task does not map cleanly to these steps, refine the existing plan into a step-by-step plan from this skill, its subcommands, and the user's request, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `empirical-pass` | Run the full empirical loop from framing to analysis | `commands/empirical-pass.md` |
| `hypothesis-pass` | Run a selected hypothesis through experiment and analysis | `commands/hypothesis-pass.md` |
| `paper-pass` | Turn analysis findings into a reviewed paper bundle | `commands/paper-pass.md` |
| `revision-pass` | Self-review a draft, fill evidence gaps, and revise | `commands/revision-pass.md` |
| `rebuttal-pass` | Turn formal reviewer feedback into revised text and evidence | `commands/rebuttal-pass.md` |
| `polish-pass` | Polish figures and prose before external review | `commands/polish-pass.md` |
| `submission-pass` | Finalize a reviewed paper bundle for submission or archive | `commands/submission-pass.md` |
| `list-passes` | List available pipeline passes | `commands/list-passes.md` |
| `help` | Explain this skill and list public subcommands | This entrypoint |

## Reference Routing

- Placeholder definitions: `references/placeholders.md`
- Storage bindings: `placeholder-bindings.md`
- Transition rules: `references/transition-rules.md`
- Terminal report template: `references/terminal-report-template.md`
- Prerequisite recovery: use `$isomer-deepsci-shared` and its shared Prerequisite Recovery reference

## Worker Output Policy

This skill writes durable records only through the `placeholder-bindings.md` commands. It does not create ad-hoc local files. When writing plain generated files such as reports or runtime state views, follow the project outputs policy: choose an operation-specific child set under the Topic Workspace, respect `.gitignore` rules, and run `commit_after_operation` only when the operation genuinely produced durable project outputs.

## Common Stage Execution Rules

Every pass subcommand follows these rules unless its own page overrides them.

- Load the recipe from `commands/<pass-name>.md` and run the stages listed there.
- Hand artifacts from stage N to stage N+1 automatically.
- Apply `references/transition-rules.md` after each stage to decide continue, pause, or block.
- Produce `DEEPSCI:PIPELINE-TERMINAL-REPORT` using `references/terminal-report-template.md`.
- Preserve each wrapped skill's callbacks, quality gates, and blocker semantics.

## Placeholders and Storage

- Placeholder definitions: `references/placeholders.md`
- Storage bindings: `placeholder-bindings.md`
- Transition rules: `references/transition-rules.md`
- Terminal report template: `references/terminal-report-template.md`

## Exit Criteria

This skill can end only when one of the following is durably true:

- The selected pass completed and `DEEPSCI:PIPELINE-TERMINAL-REPORT` has `status: complete`.
- A stage paused the pipeline and `DEEPSCI:PIPELINE-TERMINAL-REPORT` has `status: paused` with a `resume_point`.
- A stage blocked the pipeline and `DEEPSCI:PIPELINE-TERMINAL-REPORT` has `status: blocked` with a `resume_point` and blocker record.
- The requested pass is unknown and a help or `list-passes` response was returned.

## Operational Notes

- Looping and run-to traversal are external control. A recipe remains single-pass.

## Guardrails

- DO NOT treat the pipeline skill as a loop manager.
- DO NOT silently continue after a stage blocker or unexpected route decision.
- DO NOT skip a wrapped skill's callbacks or quality gates.
- DO NOT bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- DO NOT ask the user routine technical questions before checking durable local evidence.
- DO NOT hide blocked states behind vague progress language.
- DO NOT infer run-to authorization from an ordinary `do <task>` request or make it global or session-wide.
- DO NOT merge prerequisite Runs, skip callbacks or Gates, continue after the named target, or treat run-to as a Run-level Control Mode.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
