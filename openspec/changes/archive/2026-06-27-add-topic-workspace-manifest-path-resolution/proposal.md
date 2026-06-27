## Why

The current Topic Workspace and Agent Workspace contract is too dependent on fixed directory names and path assembly. Projects may already have equivalent local directories, may not need every default Isomer-managed surface, or may want agents to query “where is my private artifact path?” without knowing the default layout.

## What Changes

- Introduce a topic-owned Topic Workspace Manifest that records semantic workspace surface labels and their concrete path bindings inside one Topic Workspace.
- Treat the current directory structure as the built-in `isomer-default.v1` layout profile, not as the only valid contract.
- Add semantic path query behavior so users, agents, skills, and adapters can resolve labels such as `topic.main_repo`, `topic.records.artifacts`, `agent.workspace`, `agent.private_artifacts`, `agent.scratch`, and later `agent.tmp` through `isomer-cli` instead of assembling paths.
- Add default-layout materialization behavior for users who choose to create the standard semantic directories at their default locations.
- Add Effective Agent Context inference so an agent running inside its own Agent Workspace can query agent-scoped semantic labels without passing an Agent Name.
- Preserve Workspace Runtime path plans as the durable historical path truth for records that already depend on a path, even if the Topic Workspace Manifest changes later.
- Reframe the pending local `tmp/` surfaces change so `tmp/` is introduced as semantic labels with default bindings rather than only as fixed paths.

## Capabilities

### New Capabilities

- `topic-workspace-manifest`: Defines the topic-owned manifest, semantic surface labels, default layout profile, path binding validation, and default materialization contract.

### Modified Capabilities

- `workspace-path-resolution`: Resolve semantic surface labels through recorded path plans, environment context, Topic Workspace Manifest bindings, Project Manifest defaults, and built-in defaults, and expose direct semantic path query behavior.
- `cli-topic-context-resolution`: Infer Effective Agent Context from cwd when the current directory is inside a known Agent Workspace and no explicit agent selector is supplied.
- `workspace-runtime-persistence`: Store manifest-sourced path plans before durable runtime records depend on paths, and preserve historical path plans when manifest bindings drift.
- `topic-workspace-manager-skill`: Prepare, validate, and summarize Git-backed Topic Workspace and Agent Workspace layouts through semantic labels and manifest bindings instead of hard-coded paths alone.
- `topic-team-specialization-module-skill`: Record and consume Agent Workspace setup evidence through semantic labels, including cwd-friendly agent-scoped queries.
- `isomer-service-env-setup-skill`: Resolve Topic Workspace and Agent Workspace setup targets through semantic labels rather than assuming the default directory structure.
- `isomer-documentation-system-guide`: Document the manifest-backed semantic path contract, default layout profile, cwd-derived agent inference, and the relationship to future `tmp/` labels.

## Impact

This affects Topic Workspace documentation, domain language, `isomer-cli project paths` behavior, Workspace Path Resolution, Effective Topic Context resolution, Workspace Runtime path-plan creation and validation, `src/isomer_labs` manifest/path models, unit tests for semantic resolution and cwd inference, and operator/service skill guidance. It does not remove the default layout or require every project to create every default Isomer-managed directory.
