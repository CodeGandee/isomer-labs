# DeepScientist Skill Analysis Index

This directory explains the inner workflow of each active builtin DeepScientist skill. Each linked file includes a Mermaid state diagram, a brief table explaining the states, durable outputs, and key constraints.

Source skill root:

```text
extern/orphan/DeepScientist/src/skills/
```

## Core Research Skills

These skills drive generic research work: framing a problem, reading papers, choosing ideas, setting up baselines, running experiments, comparing evidence, and analyzing scientific results.

| Skill | Main Use |
| --- | --- |
| [scout](scout.md) | Frame the problem, scout literature, clarify datasets or metrics, and discover baseline directions. |
| [baseline](baseline.md) | Attach, import, reproduce, verify, compare, confirm, or waive a baseline. |
| [idea](idea.md) | Generate and select hypotheses, candidate directions, and falsifiable research routes. |
| [optimize](optimize.md) | Manage algorithm-first candidate briefs, optimization frontier, branch promotion, and debug/fusion routes. |
| [experiment](experiment.md) | Implement one selected route, run the main experiment, validate metrics, and record the result. |
| [analysis-campaign](analysis-campaign.md) | Run follow-up ablations, robustness checks, error analysis, or failure analysis after a main result. |
| [science](science.md) | Route scientific software, simulations, dataset analysis, HPC execution, validation, and evidence-backed claims. |

## Paper Writing Skills

These skills focus on paper, manuscript, figure, review, rebuttal, data-availability, and presentation deliverables. If a quest is research-only and does not aim to produce a paper-like artifact, these are usually optional.

| Skill | Main Use |
| --- | --- |
| [write](write.md) | Draft or refine a paper, report, or research summary from existing evidence. |
| [paper-outline](paper-outline.md) | Build or repair a paper-native outline, scoped claims, method abstraction, and evidence boundaries. |
| [paper-plot](paper-plot.md) | Turn structured numeric results into a first-pass publication-quality figure using bundled templates. |
| [figure-polish](figure-polish.md) | Render, inspect, revise, and finalize durable milestone, paper, or appendix figures. |
| [review](review.md) | Audit a substantial draft or paper-like report before finalization or revision routing. |
| [rebuttal](rebuttal.md) | Map reviewer feedback into manuscript deltas, experiments, evidence updates, and response letters. |
| [nature-data](nature-data.md) | Prepare or audit Nature-ready Data Availability statements, repository plans, citations, and FAIR metadata. |
| [nature-figure](nature-figure.md) | Create, revise, audit, or polish Nature/high-impact journal figures in Python or R. |
| [nature-paper2ppt](nature-paper2ppt.md) | Build a Chinese PPTX presentation from a scientific paper or paper-derived notes. |
| [nature-polishing](nature-polishing.md) | Polish, restructure, or translate academic prose into Nature-leaning English. |

## System Management Skills

These skills manage DeepScientist quest state: auditing existing work, choosing the next route, and closing or pausing the research loop.

| Skill | Main Use |
| --- | --- |
| [intake-audit](intake-audit.md) | Audit and reconcile an existing quest state before choosing the next anchor. |
| [decision](decision.md) | Make and record explicit route decisions from durable evidence. |
| [finalize](finalize.md) | Consolidate final claims, limitations, recommendations, summary state, and handoff or completion state. |
