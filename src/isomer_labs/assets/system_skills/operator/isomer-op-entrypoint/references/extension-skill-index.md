# Extension Skill Index

## Workflow

1. Determine whether the user task is domain-extension work, currently production DeepSci research or paper-companion work.
2. Check whether the task needs base Topic Workspace readiness, selected Topic Actor or Agent workspace readiness, production DeepSci bootstrap, latest-context preflight, placeholder bindings, or worker-output policy before a research-stage skill can run.
3. Route missing readiness to `isomer-op-topic-creator`, `isomer-op-topic-mgr`, `isomer-op-topic-team-specialize`, `isomer-srv-agent-env-setup` through its owner workflow, or `isomer-deepsci-workspace-mgr`.
4. Route prepared research-stage work to the matching `isomer-deepsci-*` skill or to `isomer-deepsci-pipeline` for a named pass.
5. Preserve the selected DeepSci skill's callbacks, latest-context preflight, worker-output policy, placeholder binding, accepted-record, and blocker rules.

If the user's task does not map cleanly to these steps, use your native planning tool to build a DeepSci route plan from the Research Topic context, readiness evidence, selected skill set, durable records, and missing inputs, then execute the plan or report the blocker.

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

Do not let ordinary DeepSci research-stage skills fabricate missing Topic Workspace, Topic Actor, Agent Workspace, or bootstrap readiness. Route setup first, then return to the selected extension skill.
