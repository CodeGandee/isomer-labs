## Why

`isomer-admin-topic-creator` currently blurs topic input, topic identity, registration, research intent, environment intent, and actor setup inside broad stages such as `define-topic`. A Topic Workspace cannot be safely named or initialized until the user supplies a concrete Research Topic, and each intent surface should be created at the point where the user can review the right kind of decision.

## What Changes

- Refine the Topic Creator initialization flow so concrete user-given Research Topic substance is a hard prerequisite before deriving a topic id, choosing a Topic Workspace path, or writing intent files.
- Replace the overloaded `define-topic` stage with clearer topic-input resolution and a narrow `create-research-intent` step that only creates or updates `topic.intent.overview`, which resolves by default to `<topic-workspace>/intent/src/topic-overview.md`.
- Add `define-topic-env` as the user-facing step that creates or refines `topic.intent.topic_env_requirements`, which resolves by default to `<topic-workspace>/intent/src/topic-env-gate.md`, and waits for user verification before setup unless running under `fast-forward`.
- Keep `setup-topic-env` responsible for reading the topic env gate, generating or validating derived topic environment gates such as `topic.env.topic_setup_target_spec`, and delegating installation/materialization work.
- Add `define-actors` as the user-facing step that creates or refines actor intent at `topic.intent.actor_definitions`, defaulting to `<topic-workspace>/intent/src/actor-definitions.md`, including each actor's duty, intended usage, and source env gate. If invoked without actor details, or with only "create the operator actor" style intent, it creates the default `operator` actor definition.
- Keep `setup-actors` responsible for materializing actor workspaces and support material, generating derived actor env gates at `topic.env.actor_env_gates`, defaulting to `<topic-workspace>/intent/derived/actor-env-gates.md`, and verifying actor env gates.
- Preserve semantic path resolution for all intent and derived env gate labels; skills must not hard-code the default paths except as explanatory default-layout documentation.
- Align the Topic Creator help, subcommand tables, reference pages, validator checks, and unit fixtures with the new flow.
- Keep lower-level registration, runtime, environment setup, actor setup, bootstrap, and start-pack responsibilities delegated to their existing owners.

## Capabilities

### New Capabilities
- `topic-creator-skill`: Topic Creator operator skill contract, including topic-input gating, staged topic intent, topic env intent, actor definition, setup subcommand routing, and manual-research-ready output.

### Modified Capabilities
- `manual-research-topic-workflow`: Manual research preparation must require concrete Research Topic substance, `topic.intent.overview` creation, topic env gate review or fast-forward acceptance, actor definition creation, topic setup readiness, and actor env verification before later readiness stages treat the Topic Workspace and default Topic Actor handoff as prepared.

## Impact

- Affected skill files: `skillset/operator/isomer-admin-topic-creator/**`.
- Affected validation and tests: `scripts/validate_skillsets.py` and `tests/unit/test_validate_skillsets.py`.
- Related existing patterns: `isomer-admin-topic-team-specialize` already separates topic seeding, topic env gate definition, and setup; this change adapts that separation for Topic Creator.
- Workspace Path Resolution must add `topic.intent.actor_definitions` with default binding `<topic-workspace>/intent/src/actor-definitions.md` and `topic.env.actor_env_gates` with default binding `<topic-workspace>/intent/derived/actor-env-gates.md`; `topic.intent.overview`, `topic.intent.topic_env_requirements`, and their default bindings already exist.
