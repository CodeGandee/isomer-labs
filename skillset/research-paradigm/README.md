# Research Paradigm Skills

This subtree contains portable research-stage skills for Isomer Labs agents. The skills capture reusable research practice: framing a problem, accepting a baseline, choosing ideas, running experiments, analyzing evidence, writing, reviewing, rebutting, finalizing, plotting, figure polishing, and scientific computation.

The skills are adapted from richer source research skills, but they are written as Isomer-native bundles. They use Isomer concepts such as Research Task, Research Branch, Run, Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, Operator Agent, Agent Team Instance, Capability Binding, Execution Adapter, and Workflow Stage.

## Skill Set

| Skill | Purpose |
| --- | --- |
| `isomer-rsch-shared` | Shared evidence, handoff, terminology, provenance, and TBD-surface rules. |
| `isomer-rsch-intake` | Audit and reconcile existing research state before choosing the next stage. |
| `isomer-rsch-scout` | Frame the task, narrow unknowns, inspect literature or local evidence, and route to baseline, idea, or blocker. |
| `isomer-rsch-baseline` | Establish a trustworthy comparator, metric contract, waiver, or blocker. |
| `isomer-rsch-idea` | Convert the evidence board into candidate hypotheses and one falsifiable route. |
| `isomer-rsch-optimize` | Manage algorithm-first candidates, frontier ranking, promotion, bounded attempts, fusion, or debug routes. |
| `isomer-rsch-experiment` | Turn a selected route into one trustworthy measured result. |
| `isomer-rsch-analysis` | Run follow-up evidence work such as ablations, robustness checks, error analysis, failure analysis, or review-linked slices. |
| `isomer-rsch-decision` | Make explicit go, stop, branch, write, finalize, reset, Gate, or blocker decisions from durable evidence. |
| `isomer-rsch-finalize` | Consolidate final claims, limitations, recommendations, and closure or handoff state. |
| `isomer-rsch-write` | Draft or refine reports, papers, or summaries from existing evidence. |
| `isomer-rsch-review` | Audit substantial drafts, reports, or paper-like artifacts skeptically. |
| `isomer-rsch-rebuttal` | Map reviewer feedback into evidence actions, text deltas, and revision responses. |
| `isomer-rsch-paper-outline` | Build or repair a paper-native outline with scoped claims and evidence boundaries. |
| `isomer-rsch-paper-plot` | Turn structured numeric evidence into first-pass academic figures. |
| `isomer-rsch-figure-polish` | Polish meaningful draft figures into durable milestone, manuscript, appendix, or review figures. |
| `isomer-rsch-science` | Support scientific computation, simulation, dataset analysis, validation, and evidence-backed claims. |

Stage and companion skills should read `isomer-rsch-shared/SKILL.md` first when common evidence, handoff, terminology, or unsettled-surface rules matter.

## Bundle Pattern

Each stage or companion skill should be usable as a self-contained bundle. `SKILL.md` is the concise entrypoint, `references/` holds source-derived playbooks and templates, `assets/` or `scripts/` are used only when a sanitized resource is directly useful, and `agents/openai.yaml` gives the UI manifest with `interface.display_name` equal to the skill name.

Long source details should move into one-level local references linked directly from `SKILL.md`. Active skill docs should not require `context/explore/`, `extern/orphan/`, archived OpenSpec paths, absolute local paths, or another skill folder outside this subtree.

Deferred resource decisions should be recorded inside the relevant skill's local references. Current deferrals include broad venue LaTeX templates for `isomer-rsch-write`, fixed-data plotting scripts for `isomer-rsch-paper-plot`, and the large generated science package-card catalog for `isomer-rsch-science`.

## Migration Contract

When migrating a source research skill into this subtree, preserve as much reusable research method as possible. Do not reduce a rich source skill to a thin checklist if the source contains portable judgment, route taxonomy, templates, examples, validation gates, boundary cases, or failure handling.

Preserve source richness by moving detail into bundled resources:

- Keep `SKILL.md` concise and procedural.
- Put long playbooks, examples, templates, checklists, boundary cases, and operational guidance under `references/`.
- Link every reference directly from `SKILL.md` and state when to read it.
- Keep references one level deep from `SKILL.md`.
- Prefer local reference files over references to source-tree paths.

Translate source concepts into Isomer terms:

- Source lifecycle work becomes Research Thread, Research Task, Research Branch, Run, or Workflow Stage, depending on scope.
- Source artifact APIs become Artifacts, Evidence Items, Decision Records, Gates, Provenance Records, or host Artifact APIs.
- Source memory APIs become Findings, Evidence Items, Artifacts, or durable context queries.
- Source command execution becomes Capability Binding through an Execution Adapter.
- Source worktree or workspace assumptions become Isomer Workspace, Workspace Runtime, Agent Workspace, or a TBD placeholder.
- Source scheduler and continuation terms become Workflow Stage recommendations, Gates, Decision Records, observations, or pauses for Operator Agent instruction.

Mark unsettled concrete surfaces explicitly. If the source skill depends on a path, filename, command wrapper, runtime API, storage root, runner home, prompt-injection mechanism, paper-search provider, generated layout, or schema that Isomer has not accepted, use `[[tbd-surface:<id>]]` and list the id in the relevant TBD registry.

## Skill Writing Constraints

Skill folders must be named `isomer-rsch-<purpose>`, and `SKILL.md` frontmatter `name:` must match the folder name. Frontmatter must contain only `name` and `description`.

For `agents/openai.yaml`, `interface.display_name` must be the skill name itself, such as `isomer-rsch-analysis`. The `default_prompt` should invoke the same skill with `$isomer-rsch-<purpose>`.

Do not make active skills depend on source repository paths, archived OpenSpec files, local absolute paths, or external skill folders. A standalone skill bundle must contain the references it needs under its own directory. Shared skills may be referenced only when the bundle is intentionally installed as part of this research-paradigm subtree.

Do not port source runtime APIs, concrete storage layouts, scheduler fields, credentials, mailbox routes, gateway routes, or team topology into skill requirements. Those belong in Isomer platform design, runtime profiles, or operator documentation.

Keep negative, partial, failed, blocked, infeasible, null, and contradictory results visible as evidence. Do not let polished prose, summaries, or route recommendations hide missing evidence or broken comparability.

Active skill docs should use `isomer-rsch-*` names. Historical archive files may mention older names only as migration history.
