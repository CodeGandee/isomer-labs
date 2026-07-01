# Main Experiment Plan Template

Use this reference before substantial code edits or the real main run. Treat it as the implementation-and-execution plan for the selected route, not just a metadata form. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **State the topic link**. Connect the run to the active Research Topic, Research Inquiry, route, selected hypothesis, and expected deliverable.
2. **Write the objective and hypotheses**. Capture user requirements, non-negotiable constraints, research question, null hypothesis, alternative hypothesis, and selected hypothesis in `1-2` sentences.
3. **Freeze baseline and comparability**. Record comparator id or variant, dataset, split, primary metric, required metric keys, evaluator assumptions, and comparability risks.
4. **Translate the idea into code**. Map concrete files or components to planned changes, reasons, and risks before editing.
5. **Design execution**. Define minimal experiment, smoke or pilot path, full run path, expected outputs, stop condition, abandonment condition, and strongest alternative hypothesis.
6. **Plan runtime and recovery**. Record command paths, expected budget, log and artifact locations, safe efficiency levers, health signals, kill or relaunch triggers, and fallbacks.
7. **Link the checklist and revise deliberately**. Keep <EXPERIMENT_CHECKLIST> synchronized with <EXPERIMENT_PLAN>, and log material changes with their effect on comparability or runtime.

## Preferences

- Prefer a one-screen plan for lightweight runs (if it preserves route, comparability, command path, outputs, and fallback, otherwise use the full template).
- Prefer explicit code-translation rows before edits (if the code path is obvious, otherwise state why no table is needed).
- Prefer safe efficiency levers that preserve comparator equivalence (if they affect comparability, otherwise record them as experiment changes).
- Prefer revising the plan before spending more compute after a material route change (if only a small note changes, otherwise update the revision log).

## Constraints

- <EXPERIMENT_PLAN> must lead with the selected hypothesis and comparator boundary.
- <EXPERIMENT_PLAN> must include required metrics, stop condition, abandonment condition, and fallback options for substantial runs.
- <EXPERIMENT_PLAN> should not hide user constraints, resource limits, or known comparability risks.
- Runtime strategy must not broaden resources, datasets, or metric definitions silently.

## Quality Gates

### Metrics

- Plan-section coverage: fraction of map link, objective, current tasks, baseline/comparability, code translation, execution design, runtime strategy, fallbacks, checklist link, and revision log sections completed; higher is better.
- Budget-ambiguity count: number of expected runtime, compute, fallback, or downscope decisions still unspecified before execution; lower is better.

### Checks

- Objective gate: selected hypothesis, user constraints, research question, null hypothesis, and alternative hypothesis are explicit.
- Comparability gate: comparator, dataset, split, metric keys, evaluator assumptions, and risks are visible.
- Implementation gate: planned code changes are mapped to mechanism and risk.
- Execution gate: smoke path, full run path, outputs, budget, stop condition, and abandonment condition are stated.
- Recovery gate: fallbacks and kill or relaunch triggers are concrete enough to act on during execution.
- Revision gate: material plan changes record why they changed and how they affect comparability or runtime.

## Template

### 1. Research Topic Link

- topic or workspace:
- route or inquiry:
- selected hypothesis:
- run id:
- deliverable:
- success condition:
- abandonment condition:
- next on success:
- next on failure:

### 2. Objective and Hypotheses

- selected hypothesis in `1-2` sentences:
- user's core requirements:
- non-negotiable user constraints:
- research question:
- null hypothesis:
- alternative hypothesis:
- research objective:
- research type:

### 3. Baseline and Comparability

- comparator id:
- comparator variant:
- dataset or source:
- split:
- primary metric:
- required metric keys:
- evaluator assumptions:
- comparability risks:

### 4. Code Translation Plan

| Path or Component | Current Role | Planned Change | Why This Is Needed | Risk |
| --- | --- | --- | --- | --- |
| | | | | |

### 5. Execution Design

- minimal experiment:
- smoke or pilot plan:
- full run plan:
- expected outputs:
- stop condition:
- abandonment condition:
- strongest alternative hypothesis:

### 6. Runtime Strategy

- smoke command path:
- main run command path:
- expected runtime or budget:
- log and artifact locations:
- safe efficiency levers:
- health signals that justify continuing:
- conditions that trigger kill or relaunch:

### 7. Fallbacks and Recovery

- if the intended model, endpoint, dependency, or download path fails:
- if hardware or memory is tighter than expected:
- if the code path is wrong after smoke:
- if the first full run becomes non-comparable:

### 8. Checklist Link

- checklist reference:
- next unchecked item:

### 9. Revision Log

| Time | What Changed | Why It Changed | Impact on Comparability or Runtime |
| --- | --- | --- | --- |
| | | | |
