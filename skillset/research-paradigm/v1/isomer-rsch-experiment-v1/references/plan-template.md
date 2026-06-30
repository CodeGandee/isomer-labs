# Main Experiment Plan

Use this before substantial code edits or the real main Run. Treat it as the implementation-and-execution plan for the selected route, not just a metadata form. For lightweight Runs, a one-screen plan is enough if it preserves route, comparability boundary, Execution Adapter path, outputs, and fallback.

## Template

```md
# Main Experiment Plan

## Map Link

- parent_stage_or_decision:
- loop_id:
- node_objective:
- node_deliverable:
- success_condition:
- abandonment_condition:
- next_on_success:
- next_on_failure:

## Objective

- run_id:
- selected_route_in_one_or_two_sentences:
- user_requirements:
- non_negotiable_constraints:
- research_question:
- null_hypothesis:
- alternative_hypothesis:

## Current Node Tasks

- [ ] sync experiment status and current incumbent context
- [ ] confirm comparability and code translation plan
- [ ] run smoke or pilot path if needed
- [ ] launch or validate the main Run
- [ ] classify the result and update the next route

## Comparator and Comparability

- comparator_id:
- comparator_variant:
- dataset_or_split:
- primary_metric:
- required_metric_keys:
- comparability_risks:

## Code Translation Plan

| Path or component | Current role | Planned change | Why this is needed | Risk |
| --- | --- | --- | --- | --- |
| | | | | |

## Execution Design

- minimal_experiment:
- smoke_or_pilot_plan:
- full_run_plan:
- expected_outputs:
- stop_condition:
- abandonment_condition:
- strongest_alternative_hypothesis:

## Runtime Strategy

- Capability Binding:
- Execution Adapter:
- expected_runtime_or_budget:
- log_and_artifact_placeholders:
- safe_efficiency_levers:
- health_signals:
- kill_or_relaunch_conditions:

## Fallbacks and Recovery

- if intended dependency fails:
- if hardware or memory is tighter than expected:
- if code path is wrong after smoke:
- if first full Run becomes non-comparable:

## Checklist Link

- checklist Artifact:
- next unchecked item:

## Revision Log

| Time | What changed | Why it changed | Impact on comparability or runtime |
| --- | --- | --- | --- |
| | | | |
```

## Plan Rule

If the code path, comparability contract, runtime strategy, or execution route changes materially, revise the plan before spending more code or compute.
