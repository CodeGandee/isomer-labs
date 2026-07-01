# Isomer Admin Topic Prepare Help

## Deprecation Warning

Direct user invocation of this skill is deprecated. Use `isomer-admin-topic-creator` for end-to-end topic initialization. This skill remains available for compatibility and delegated common-preparation steps.

## What This Skill Does

This skill prepares the common Research Topic layer before either manual research or formal Topic Team Specialization. It resolves or creates topic registration, checks Workspace Runtime and topic environment readiness, treats `topic.repos.main` as the Git anchor, optionally creates the default `operator` Topic Actor, and returns a handoff route to the next operator workflow.

## Required Inputs

- Project root or Project Manifest context.
- Concrete Research Topic statement or registered Research Topic ref.
- Operator permission before creating topic registration, Workspace Runtime state, topic environment material, Topic Actor bindings, or research bootstrap records.
- Explicit opt-out if the default `operator` Topic Actor or Topic Actor Workspace should not be created.

## Subcommand Functionalities

| Subcommand | Functionality |
| --- | --- |
| `help` | Print what this skill does, required inputs, and subcommand functionalities. |
| `prepare-topic` | Run the full common topic preparation workflow and produce preparation evidence for later manual or team workflows. |
| `resolve-topic-intent` | Resolve or create the selected Research Topic and registered Topic Workspace through Project Manifest-backed Isomer context. |
| `prepare-common-topic-state` | Ensure Workspace Runtime, topic intent, topic environment readiness, topic-main readiness reporting, and research storage bootstrap inputs are present or clearly blocked. |
| `ensure-operator-actor` | Create or validate the reserved `operator` Topic Actor and Topic Actor Workspace unless the user explicitly opts out. |
| `summarize-preparation` | Report topic refs, runtime status, topic-main readiness, Topic Actor status, storage bootstrap status, blockers, and next handoff route. |
