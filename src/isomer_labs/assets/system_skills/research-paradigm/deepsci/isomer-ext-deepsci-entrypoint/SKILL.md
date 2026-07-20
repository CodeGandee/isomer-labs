---
name: isomer-ext-deepsci-entrypoint
description: Use when a research task matches one of the named single-pass research procedures and you want to invoke it directly instead of choosing each production DeepSci skill by hand.
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Isomer DeepSci Entrypoint

## Plan First

Pipeline execution is a complex process. Before executing any pipeline task, use your internal todo list or planning tool to create a plan for the requested work. Keep the plan current as stages complete, blockers appear, or the requested scope changes.

## Overview

`isomer-ext-deepsci-entrypoint` is the public DeepSci execution entrypoint. It executes one named single-pass procedure or routes a concrete task to one protected DeepSci member while preserving automatic artifact handoffs. Empty invocation, `help`, and orientation-only requests delegate read-only output to the independent `$isomer-ext-deepsci-welcome` sibling.

Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

Before a pass accepts an idea-bearing output, invoke `isomer-op-entrypoint->research-ideas` and require the producing stage to commit and verify canonical facets, exact realizations, generations, complete decision options, justified transitions with terminal refs, and lineage. A pipeline terminal report cannot substitute for missing canonical effects.

Each pass is defined by a dedicated subcommand page under `commands/`. The recipe is embedded in that page so pass-specific customization can grow without complicating the main skill entrypoint.

## When to Use

Use this skill when a research task matches one named pass or a focused DeepSci stage. Prefer `$isomer-ext-deepsci-entrypoint use <subcommand> to <task>`; task-only invocation may select a pass or protected member.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Resolve the public request**. Accept `$isomer-ext-deepsci-entrypoint use <subcommand> to <task>`, a task-only request, or empty invocation. Empty invocation, `help`, and orientation-only requests delegate to `$isomer-ext-deepsci-welcome` with supplied context intact; otherwise select one declared pass or protected member and proceed.
2. **Run the latest context preflight**. Before accepting durable inputs or emitting durable records, load or create a `DEEPSCI:LATEST-CONTEXT-SNAPSHOT` for the active Research Topic. Compare prompt memory, chat memory, prior prose, and worker-local files against durable records. Report conflicts instead of silently overwriting durable state.
3. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-ext-deepsci-entrypoint --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
4. **Validate the recipe context**. Build `DEEPSCI:PIPELINE-RECIPE-CONTEXT` from the named pass, optional starting stage, input artifacts, parameters, and budget or checkpoint preferences.
5. **Preflight target prerequisites**. Resolve the recipe's accepted inputs and their known focused-skill or pass producers before target mutation. If an ordinary target request has a producible gap, return `paused` and present Run to the target, Execute the next prerequisite only, Inspect or choose another route, and Stop before invoking a producer.
6. **Plan authorized run-to recovery**. Only after explicit target-scoped run-to authorization, let the current agent act as the external controller and maintain an internal dependency plan with the native planning tool. Invoke prerequisites as separate focused-skill or pass executions, validate their terminal reports, refresh current state, and resume the original target when ready. Never add a loop or backward edge to a recipe.
7. **Invoke the pass subcommand**. Execute the workflow in `commands/<pass-name>.md`. Let the subcommand load its single-pass linear recipe, run the stages, verify each stage closeout, and prepare its own `DEEPSCI:PIPELINE-TERMINAL-REPORT` without merging prerequisite Runs.
8. **Prepare the terminal report**. Assemble the report with each stage's closeout status, applicable acceptance receipt id, accepted durable record refs, final durable artifact ref, and recommended next action. Do not surface a successful terminal result yet.
9. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill isomer-ext-deepsci-entrypoint --stage end`. Follow returned instructions within this skill, `isomer-ext-deepsci-entrypoint->shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow.
10. **Close pipeline operation sets**. After end callbacks, invoke `isomer-ext-deepsci-entrypoint->shared`, follow its Operation Set Closeout reference, and invoke `isomer-op-entrypoint->operation-sets`. Require every stage to carry either a verified `complete` receipt or `closeout: not_applicable` with durable record refs. Accept and verify any pipeline-level terminal-report or other material files before `status: complete`; if any stage or pipeline receipt is missing, `partial`, stale, or unverifiable, set `status: paused` and return accepted refs, the partial receipt when present, diagnostics, and the exact resume command.
11. **Return the verified terminal report**. Surface the durable report and closeout evidence to the caller or external controller. The bounded pass does not choose the next macro action. With explicit run-to authorization, the current agent may consume an in-closure recommended route only after recording this report, and it stops after the named target or at a nondelegable Gate.

Callback resolution returns a compact `callbacks` array. Process entries in returned order and read each absolute `instruction_path` as supplemental material according to `source_type`. For `skill_dir`, read the reported `SKILL.md` and any directly required relative resources; do not treat the directory as an installed system skill or execute its scripts solely because resolution returned it. During ordinary execution, do not request `--explain` or depend on registry, priority, scope, status, Toolbox registration, or gating fields. Use `--explain`, `list`, `show`, or `validate` only to diagnose or manage callback resolution. Preserve higher-priority instructions, the current user request, owning-skill and shared research rules, evidence discipline, required Gates, validation, and recording obligations; report any material conflict.

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

## Protected Subskills

| Member | Logical ID | When to Route Here | Internal Designator |
| --- | --- | --- | --- |
| `analysis` | `isomer-deepsci-analysis` | A parent result already exists and needs bounded follow-up evidence through ablations, robustness checks, failure analysis, or limitation analysis. | `isomer-ext-deepsci-entrypoint->analysis` |
| `baseline` | `isomer-deepsci-baseline` | Hypothesis or experiment work is blocked until a trustworthy comparator, metric contract, waiver, or explicit baseline blocker is established. | `isomer-ext-deepsci-entrypoint->baseline` |
| `decision` | `isomer-deepsci-decision` | Accumulated evidence requires an explicit route choice, stop, branch, baseline reuse, reset, writing, finalization, or user-sensitive decision. | `isomer-ext-deepsci-entrypoint->decision` |
| `experiment` | `isomer-deepsci-experiment` | A selected hypothesis or route, comparator basis, and evaluation contract are ready for one bounded implementation or measured run. | `isomer-ext-deepsci-entrypoint->experiment` |
| `figure-polish` | `isomer-deepsci-figure-polish` | An already meaningful figure needs general academic styling, render inspection, iterative revision, final export, and evidence-linked recording. | `isomer-ext-deepsci-entrypoint->figure-polish` |
| `finalize` | `isomer-deepsci-finalize` | The inquiry is ready to close, pause, archive, publish, or hand off with consolidated claims, limitations, recommendations, and a resume path. | `isomer-ext-deepsci-entrypoint->finalize` |
| `idea` | `isomer-deepsci-idea` | A framed topic and comparator basis are ready to become one falsifiable hypothesis, research route, or algorithm-first brief before experiments. | `isomer-ext-deepsci-entrypoint->idea` |
| `nature-data` | `isomer-deepsci-nature-data` | A manuscript needs Nature-ready data-availability language, repository or citation planning, FAIR metadata checks, or a data-sharing audit. | `isomer-ext-deepsci-entrypoint->nature-data` |
| `nature-figure` | `isomer-deepsci-nature-figure` | A Nature-family or other high-impact journal figure needs creation or revision in Python or R under an explicit evidence and export contract. | `isomer-ext-deepsci-entrypoint->nature-figure` |
| `nature-paper2ppt` | `isomer-deepsci-nature-paper2ppt` | A scientific paper or related source material must become a complete Chinese presentation deck with selected figures and speaker support. | `isomer-ext-deepsci-entrypoint->nature-paper2ppt` |
| `nature-polishing` | `isomer-deepsci-nature-polishing` | Existing academic prose needs Nature-leaning English polishing, restructuring, or translation without concealing evidence gaps or inventing claims. | `isomer-ext-deepsci-entrypoint->nature-polishing` |
| `optimize` | `isomer-deepsci-optimize` | Algorithm-first research needs candidate generation, frontier ranking, promotion, fusion, debugging, plateau response, or route selection around measured runs. | `isomer-ext-deepsci-entrypoint->optimize` |
| `paper-outline` | `isomer-deepsci-paper-outline` | Evidence exists, but the paper idea, claim boundary, method abstraction, evaluation, analysis, or writing plan must mature before drafting. | `isomer-ext-deepsci-entrypoint->paper-outline` |
| `paper-plot` | `isomer-deepsci-paper-plot` | Structured numeric data needs a first-pass publication figure produced from a bundled plotting template before later visual refinement. | `isomer-ext-deepsci-entrypoint->paper-plot` |
| `rebuttal` | `isomer-deepsci-rebuttal` | Reviewer feedback must become bounded manuscript deltas, evidence work, experiments, limitations, and a durable rebuttal or revision response. | `isomer-ext-deepsci-entrypoint->rebuttal` |
| `review` | `isomer-deepsci-review` | A substantial draft or paper-like bundle needs an independent skeptical audit before finalization, rebuttal, or revision. | `isomer-ext-deepsci-entrypoint->review` |
| `science` | `isomer-deepsci-science` | The work depends on scientific computation, data analysis, simulation, package checks, HPC execution, claim-type discipline, or validity evidence. | `isomer-ext-deepsci-entrypoint->science` |
| `scout` | `isomer-deepsci-scout` | The inquiry lacks enough framing, metric clarity, literature orientation, benchmark context, or comparator direction to choose its next research stage. | `isomer-ext-deepsci-entrypoint->scout` |
| `shared` | `isomer-deepsci-shared` | Another DeepSci member needs cross-stage coordination, semantic handoffs, latest-context, output, lineage, evidence, or storage-binding rules rather than a standalone research stage. | `isomer-ext-deepsci-entrypoint->shared` |
| `workspace` | `isomer-deepsci-workspace-mgr` | Topic Workspace and Topic Actor preparation is complete, and production DeepSci storage, placeholder bindings, worker access, or skill readiness must be bootstrapped before durable research work. | `isomer-ext-deepsci-entrypoint->workspace` |
| `write` | `isomer-deepsci-write` | Accepted evidence is sufficient to draft or revise a paper, report, research summary, oral-style package, or manuscript section without fabricating support. | `isomer-ext-deepsci-entrypoint->write` |

## Reference Routing

- Placeholder definitions: `references/placeholders.md`
- Storage bindings: `placeholder-bindings.md`
- Transition rules: `references/transition-rules.md`
- Terminal report template: `references/terminal-report-template.md`
- Operation Set Closeout: invoke `isomer-ext-deepsci-entrypoint->shared` and follow its shared Operation Set Closeout reference
- Prerequisite recovery: use `isomer-ext-deepsci-entrypoint->shared` and its shared Prerequisite Recovery reference

## Worker Output Policy

This skill writes durable records only through the `placeholder-bindings.md` commands and accepted operation sets. It does not create ad-hoc local files. When writing plain generated files such as reports or runtime state views, follow the project outputs policy, choose an operation-specific child set under the resolved worker root, and close that set after end callbacks. Git tracking and `commit_after_operation` do not replace acceptance.

## Common Stage Execution Rules

Every pass subcommand follows these rules unless its own page overrides them.

- Load the recipe from `commands/<pass-name>.md` and run the stages listed there.
- Hand only verified durable record refs from stage N to stage N+1; a worker path, rendered file, Git commit, or terminal prose is an unavailable artifact.
- Apply `references/transition-rules.md` after each stage to decide continue, pause, or block.
- Require each stage entry to report a verified complete receipt or `closeout: not_applicable` with durable refs before progression.
- Produce `DEEPSCI:PIPELINE-TERMINAL-REPORT` using `references/terminal-report-template.md`.
- Preserve each wrapped skill's callbacks, quality gates, and blocker semantics.

## Placeholders and Storage

- Placeholder definitions: `references/placeholders.md`
- Storage bindings: `placeholder-bindings.md`
- Transition rules: `references/transition-rules.md`
- Terminal report template: `references/terminal-report-template.md`

## Exit Criteria

This skill can end only when one of the following is durably true:

- The selected pass completed, every stage closeout is verified, pipeline-level material files are accepted, and `DEEPSCI:PIPELINE-TERMINAL-REPORT` has `status: complete` with closeout evidence.
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
- DO NOT advance a stage from a worker path, file-only claim, missing receipt, or partial acceptance.
- DO NOT report `status: complete` until pipeline-level material files have a verified complete receipt or the pipeline has explicit `closeout: not_applicable` evidence.
- DO NOT ask the user routine technical questions before checking durable local evidence.
- DO NOT hide blocked states behind vague progress language.
- DO NOT infer run-to authorization from an ordinary `do <task>` request or make it global or session-wide.
- DO NOT merge prerequisite Runs, skip callbacks or Gates, continue after the named target, or treat run-to as a Run-level Control Mode.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
