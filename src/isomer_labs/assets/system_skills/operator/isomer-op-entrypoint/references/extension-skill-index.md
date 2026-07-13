# Extension Skill Index

## Workflow

1. Determine whether the task is production DeepSci hypothesis-driven work, DeepSci paper-companion work, or Kaoju evidence-led survey work.
2. Read the Project declaration and run `isomer-cli project system-extensions detect --target <operator-target>` before automatic routing. A route is available only when its extension is declared and the target observation is `ready` with `current` or `compatible_older` version status.
3. If compatible installation is detected but undeclared, advise `isomer-cli project system-extensions remember <extension-id>` without running it. For missing, partial, unversioned, malformed, drifted, obsolete, or newer-than-CLI observations, stop automatic routing and return detector advice.
4. Check base Topic Workspace, selected Topic Actor or Agent workspace, extension-specific readiness, required owner or Gate evidence, the selected route's latest-context preflight, and its worker-output policy before a research skill can run.
5. Route missing platform readiness to `isomer-op-topic-creator`, `isomer-op-topic-mgr`, `isomer-op-topic-team-specialize`, or the applicable service owner; route extension readiness to `isomer-deepsci-workspace-mgr` or `isomer-kaoju-workspace-mgr`.
6. Route prepared work to the matching `isomer-deepsci-*` or `isomer-kaoju-*` skill, using the family pipeline for a named procedure.
7. Preserve the selected family's callbacks, evidence, lineage, recording, owner, Gate, and blocker rules.

If the user's task does not map cleanly to these steps, use your native planning tool to build an extension route plan from the Research Topic context, readiness evidence, selected skill set, durable records, and missing inputs, then execute the plan or report the blocker.

## Kaoju Survey Skills

| Intent | Skill |
| --- | --- |
| Select and run one bounded landscape, curated intake, direction expansion, theory comparison, method trial, empirical comparison, or audit procedure. | `isomer-kaoju-pipeline` |
| Apply shared evidence depth, source identity, interaction, Gate, lineage, owner-routing, and terminal contracts. | `isomer-kaoju-shared` |
| Check Topic Workspace, existing survey, repository, registered dataset, and resource readiness. | `isomer-kaoju-workspace-mgr` |
| Freeze a Survey Contract or empirical Comparison Intent Document. | `isomer-kaoju-frame` |
| Discover version-aware papers, reports, repositories, datasets, and models. | `isomer-kaoju-discover` |
| Pin and route governed acquisition of selected materials. | `isomer-kaoju-acquire` |
| Inspect paper, report, code, dataset, or model evidence at exact locators. | `isomer-kaoju-examine` |
| Run one intended-data trial or explicit generated-data capability probe. | `isomer-kaoju-reproduce` |
| Build a source-grounded theory comparison or controlled empirical comparison. | `isomer-kaoju-compare` |
| Diagnose survey coverage, identity, evidence, lineage, and fairness without repair. | `isomer-kaoju-audit` |
| Write accepted survey conclusions from an accepted Audit Report. | `isomer-kaoju-synthesize` |

## DeepSci Bootstrap and Pipeline

| Intent | Skill |
| --- | --- |
| Prepare production DeepSci workspace bootstrap, semantic surface plan, placeholder bindings, worker access plan, and validation before durable research outputs. | `isomer-deepsci-workspace-mgr` |
| Run a named single-pass research procedure such as empirical-pass, hypothesis-pass, paper-pass, revision-pass, rebuttal-pass, polish-pass, or submission-pass. | `isomer-deepsci-pipeline` |
| Need shared DeepSci rules, route discipline, placeholder vocabulary, or storage-binding cautions before another DeepSci skill. | `isomer-deepsci-shared` |

## DeepSci Core Research Loop

| Intent | Skill |
| --- | --- |
| Clarify framing, metrics, benchmark context, literature orientation, or comparator direction. | `isomer-deepsci-scout` |
| Establish comparator, metric basis, accepted waiver, or blocker. | `isomer-deepsci-baseline` |
| Produce one falsifiable hypothesis, route, or algorithm-first brief. | `isomer-deepsci-idea` |
| Manage algorithm-first candidate frontiers, promotion, fusion, debug, plateau response, or route selection. | `isomer-deepsci-optimize` |
| Run one bounded implementation, measurement, or experiment for a selected route. | `isomer-deepsci-experiment` |
| Run follow-up evidence, ablation, robustness, failure, or limitation analysis after a parent result. | `isomer-deepsci-analysis` |
| Make an evidence-backed route, branch, stop, baseline reuse, writing, finalization, reset, or user-sensitive decision. | `isomer-deepsci-decision` |
| Close, pause, archive, publish, or hand off with final claims, limitations, recommendations, and resume path. | `isomer-deepsci-finalize` |
| Check scientific computation, data, package, simulation, HPC execution, claim type, or validity evidence. | `isomer-deepsci-science` |

## DeepSci Writing and Companion Skills

| Intent | Skill |
| --- | --- |
| Draft or revise a paper, report, research summary, oral-style package, or manuscript section from evidence. | `isomer-deepsci-write` |
| Build or repair a paper outline, claim boundary, method abstraction, evaluation plan, analysis plan, or writing plan. | `isomer-deepsci-paper-outline` |
| Turn structured numeric data into a first-pass publication-quality figure from bundled plotting templates. | `isomer-deepsci-paper-plot` |
| Style, inspect, revise, export, and record an already meaningful academic figure. | `isomer-deepsci-figure-polish` |
| Audit a substantial draft or paper-like bundle before finalization, rebuttal, or revision. | `isomer-deepsci-review` |
| Normalize reviewer feedback into manuscript deltas, evidence work, experiments, limitations, and response package. | `isomer-deepsci-rebuttal` |
| Prepare Nature-ready data availability, repository plan, dataset citation plan, FAIR metadata check, or data-sharing audit. | `isomer-deepsci-nature-data` |
| Create, revise, audit, or polish Nature-family figures with Python or R and evidence-linked export. | `isomer-deepsci-nature-figure` |
| Build a complete Chinese PPTX presentation from a scientific paper, abstract, legends, or notes. | `isomer-deepsci-nature-paper2ppt` |
| Polish, restructure, or translate academic prose into Nature-leaning English without inventing claims. | `isomer-deepsci-nature-polishing` |

Do not let ordinary DeepSci research-stage skills fabricate missing Topic Workspace, Topic Actor, Agent Workspace, extension readiness, dataset registration, or owner evidence. Route setup first, then return to the selected extension skill. Apply the same rule to ordinary Kaoju research-stage skills.
