---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Extension Skill Index

## Workflow

1. Determine whether the task is production DeepSci hypothesis-driven work, DeepSci paper-companion work, or Kaoju evidence-led survey work.
2. Read the Project declaration first. If the Project declares the selected extension, trust that state and attempt the extension route without preemptive filesystem verification.
3. If current-host readiness is unknown, delegate through `isomer-op-entrypoint->system-skills`. Its ordered evidence is Project declaration, current v4 receipt, explicit-root integrity, then limited live skill inventory. Use read-only detection for inspection; register only a complete current-v4 pack when the concrete request authorizes additive Project bookkeeping.
4. Check base Topic Workspace, selected Topic Actor or Agent workspace, extension-specific readiness, required owner or Gate evidence, the selected route's latest-context preflight, and its worker-output policy before a research skill can run.
5. Route missing base topic, Topic Actor, environment, runtime, or other platform readiness through `isomer-op-entrypoint->topic-create`, `isomer-op-entrypoint->topic-manage`, or the applicable scoped service route. Route missing formal-team readiness through `isomer-op-entrypoint->topic-team` only when the selected topology already includes a formal Agent Team layer established by a Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, selected formal-team material, or equivalent evidence. Route missing extension installation or compatibility through `isomer-op-entrypoint->system-skills`; route extension workspace readiness through the selected public extension's `workspace` member.
6. Route prepared work through the matching protected member designator of `isomer-ext-deepsci-entrypoint` or `isomer-ext-kaoju-entrypoint`, using the public entrypoint command for a named procedure.
7. Preserve the selected family's callbacks, evidence, lineage, recording, owner, Gate, and blocker rules.

If the user's task does not map cleanly to these steps, use your native planning tool to build an extension route plan from the Research Topic context, readiness evidence, selected skill set, durable records, and missing inputs, then execute the plan or report the blocker.

## Kaoju Survey Routes

| Intent | Route |
| --- | --- |
| Select and run one bounded landscape, curated intake, direction expansion, theory comparison, method trial, empirical comparison, or audit procedure. | `isomer-ext-kaoju-entrypoint` |
| Apply shared evidence depth, source identity, interaction, Gate, lineage, owner-routing, and terminal contracts. | `isomer-ext-kaoju-entrypoint->shared` |
| Check Topic Workspace, existing survey, repository, registered dataset, and resource readiness. | `isomer-ext-kaoju-entrypoint->workspace` |
| Freeze a Survey Contract or empirical Comparison Intent Document. | `isomer-ext-kaoju-entrypoint->frame` |
| Discover version-aware papers, reports, repositories, datasets, and models. | `isomer-ext-kaoju-entrypoint->discover` |
| Pin and route governed acquisition of selected materials. | `isomer-ext-kaoju-entrypoint->acquire` |
| Inspect paper, report, code, dataset, or model evidence at exact locators. | `isomer-ext-kaoju-entrypoint->examine` |
| Test a genuine source-grounded reproduction claim under the stronger fidelity contract. | `isomer-ext-kaoju-entrypoint->reproduce` |
| Prepare a code environment, run one approved source-code trial, or perform an explicit generated-data capability probe. | `isomer-ext-kaoju-entrypoint->trial` |
| Build a source-grounded theory comparison or controlled empirical comparison. | `isomer-ext-kaoju-entrypoint->compare` |
| Diagnose survey coverage, identity, evidence, lineage, and fairness without repair. | `isomer-ext-kaoju-entrypoint->audit` |
| Write accepted survey conclusions from an accepted Audit Report. | `isomer-ext-kaoju-entrypoint->synthesize` |
| Turn accepted audit and synthesis records into a publication-ready manuscript and bundle. | `isomer-ext-kaoju-entrypoint->write` |
| Export accepted state-DB records to a self-contained LLM wiki and operate the package-owned viewer. | `isomer-ext-kaoju-entrypoint->export` |

## DeepSci Bootstrap and Pipeline

| Intent | Skill |
| --- | --- |
| Prepare production DeepSci workspace bootstrap, semantic surface plan, placeholder bindings, worker access plan, and validation before durable research outputs. | `isomer-ext-deepsci-entrypoint->workspace` |
| Run a named single-pass research procedure such as empirical-pass, hypothesis-pass, paper-pass, revision-pass, rebuttal-pass, polish-pass, or submission-pass. | `isomer-ext-deepsci-entrypoint` |
| Need shared DeepSci rules, route discipline, placeholder vocabulary, or storage-binding cautions before another DeepSci member. | `isomer-ext-deepsci-entrypoint->shared` |

## DeepSci Core Research Loop Routes

| Intent | Route |
| --- | --- |
| Clarify framing, metrics, benchmark context, literature orientation, or comparator direction. | `isomer-ext-deepsci-entrypoint->scout` |
| Establish comparator, metric basis, accepted waiver, or blocker. | `isomer-ext-deepsci-entrypoint->baseline` |
| Produce one falsifiable hypothesis, route, or algorithm-first brief. | `isomer-ext-deepsci-entrypoint->idea` |
| Manage algorithm-first candidate frontiers, promotion, fusion, debug, plateau response, or route selection. | `isomer-ext-deepsci-entrypoint->optimize` |
| Run one bounded implementation, measurement, or experiment for a selected route. | `isomer-ext-deepsci-entrypoint->experiment` |
| Run follow-up evidence, ablation, robustness, failure, or limitation analysis after a parent result. | `isomer-ext-deepsci-entrypoint->analysis` |
| Make an evidence-backed route, branch, stop, baseline reuse, writing, finalization, reset, or user-sensitive decision. | `isomer-ext-deepsci-entrypoint->decision` |
| Close, pause, archive, publish, or hand off with final claims, limitations, recommendations, and resume path. | `isomer-ext-deepsci-entrypoint->finalize` |
| Check scientific computation, data, package, simulation, HPC execution, claim type, or validity evidence. | `isomer-ext-deepsci-entrypoint->science` |

## DeepSci Writing and Companion Routes

| Intent | Route |
| --- | --- |
| Draft or revise a paper, report, research summary, oral-style package, or manuscript section from evidence. | `isomer-ext-deepsci-entrypoint->write` |
| Build or repair a paper outline, claim boundary, method abstraction, evaluation plan, analysis plan, or writing plan. | `isomer-ext-deepsci-entrypoint->paper-outline` |
| Turn structured numeric data into a first-pass publication-quality figure from bundled plotting templates. | `isomer-ext-deepsci-entrypoint->paper-plot` |
| Style, inspect, revise, export, and record an already meaningful academic figure. | `isomer-ext-deepsci-entrypoint->figure-polish` |
| Audit a substantial draft or paper-like bundle before finalization, rebuttal, or revision. | `isomer-ext-deepsci-entrypoint->review` |
| Normalize reviewer feedback into manuscript deltas, evidence work, experiments, limitations, and response package. | `isomer-ext-deepsci-entrypoint->rebuttal` |
| Prepare Nature-ready data availability, repository plan, dataset citation plan, FAIR metadata check, or data-sharing audit. | `isomer-ext-deepsci-entrypoint->nature-data` |
| Create, revise, audit, or polish Nature-family figures with Python or R and evidence-linked export. | `isomer-ext-deepsci-entrypoint->nature-figure` |
| Build a complete Chinese PPTX presentation from a scientific paper, abstract, legends, or notes. | `isomer-ext-deepsci-entrypoint->nature-paper2ppt` |
| Polish, restructure, or translate academic prose into Nature-leaning English without inventing claims. | `isomer-ext-deepsci-entrypoint->nature-polishing` |

Do not let ordinary DeepSci or Kaoju protected members fabricate missing Topic Workspace, Topic Actor, Agent Workspace, extension readiness, dataset registration, or owner evidence. Route setup first, then return to the selected public extension pack.

Do not infer a formal Agent Team layer from missing readiness, missing `isomer-topic-summary.md`, missing Agent Workspace evidence, or generic topic preparation. If no formal Agent Team target is selected, use the owner of the missing base or extension layer instead of Topic Team Specialization.

If a Project-declared extension later fails to load, report stale user-controlled state and route through `isomer-op-entrypoint->system-skills`, selecting its repair routine. Never remove a declaration because one agent host has a different installed inventory.
