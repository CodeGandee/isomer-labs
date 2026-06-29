## Why

Topic-team specialization currently lets setup subcommands infer or create environment gate files while they are already preparing setup handoffs. That gives setup stages too much semantic responsibility and blurs the boundary between user-editable topic intent and implementation-specific verification plans.

## What Changes

- Add explicit topic intent resolution stages to `isomer-admin-topic-team-specialize`: `resolve-topic-intent`, `resolve-topic-env-gate`, and `resolve-agent-env-gate`.
- Make the canonical process order explicit: team specialization invoked, resolve project, resolve topic and create topic intent, resolve topic env requirements and create source intent, derive the topic env operational spec, materialize the topic env, resolve agent env requirements and create source intent, derive the agent env operational spec, materialize the agent env, then validate the topic team.
- Add first-class semantic storage labels for topic intent and env setup target specs: `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.agent_env_requirements`, `topic.env.topic_setup_target_spec`, and `topic.env.agent_setup_target_spec`.
- Keep the default `isomer-default.v1` layout mapping those labels to `<topic-workspace>/intent/src/topic-overview.md`, `<topic-workspace>/intent/src/topic-env-gate.md`, `<topic-workspace>/intent/src/agent-env-gate.md`, `<topic-workspace>/intent/derived/isomer-env-gate.md`, and `<topic-workspace>/intent/derived/isomer-agent-env-gate.md`, while requiring skills to resolve labels through Workspace Path Resolution instead of hard-coding those paths.
- Keep source intent files concise and high level. They should describe what the topic or agent workspaces need, such as "NVIDIA Nsight Compute (`ncu`) must be runnable", without listing concrete verification commands unless the user explicitly supplied those commands as intent.
- Treat derived gates as target specs for `isomer-srv-topic-env-setup` and `isomer-srv-agent-env-setup`; in the default layout those target specs live under `<topic-workspace>/intent/derived/`, but manual service invocation can also provide an explicit derived gate file, prompt, or context as input.
- **BREAKING**: Replace the old source gate paths `<topic-workspace>/user-intent/src/env-gate.md` and `<topic-workspace>/user-intent/src/agent-env-gate.md` with the semantic labels `topic.intent.topic_env_requirements` and `topic.intent.agent_env_requirements`.
- **BREAKING**: Replace the old topic overview path `<topic-dir>/topic-def/topic-overview.md` with the semantic label `topic.intent.overview` for team-specialization workflows.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `topic-team-specialization-module-skill`: Add intent-resolution subcommands, update the canonical process order around resolve, derive, and materialize stages, and require setup subcommands to consume pre-resolved source intent gates rather than inventing them during setup.
- `isomer-service-env-setup-skill`: Update the topic env service to consume a derived topic env target spec, either from `topic.env.topic_setup_target_spec`, from source intent derivation, or from an explicit manual input.
- `isomer-agent-env-setup-service-skill`: Update the agent env service to consume a derived agent env target spec, either from `topic.env.agent_setup_target_spec`, from source intent derivation, or from an explicit manual input.
- `isomer-service-env-setup-enclosure`: Update enclosure evidence references so package-source, fallback, and verification details are recorded in the resolved derived topic env target spec.
- `workspace-path-resolution`: Add built-in semantic labels for topic intent source files and env setup target specs, with default layout bindings and materialization behavior.
- `topic-workspace-manifest`: Add manifest/default-profile support for overriding the new reserved intent labels through accepted storage profiles.

## Impact

Affected material includes Workspace Path Resolution, the Topic Workspace Manifest storage surface catalog, the Topic Team Specialization operator skill, topic and agent env service skill docs, skill process design docs, call graph docs, and OpenSpec requirements that name old `topic-def/` or `user-intent/` paths. No new Python runtime APIs or dependency changes are required.
