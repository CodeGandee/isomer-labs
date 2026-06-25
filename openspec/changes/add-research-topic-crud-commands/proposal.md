## Why

Project initialization currently creates a Research Topic and Topic Workspace as part of bootstrap, which lets operators or agents accidentally turn a Project name such as `isomer-labs` into a topic id and create `isomer-content/topic-ws/isomer-labs/`. Project bootstrap should create only Project-level containers; Research Topic creation should be explicit, topic-focused, and impossible to infer from the repository name.

## What Changes

- **BREAKING**: Remove topic initialization from `isomer-cli project init`; it no longer accepts positional `<topic-id>`, `--topic-id`, or `--topic-statement`, and it no longer creates Research Topic Config files or Topic Workspace directories.
- Allow a freshly initialized Project Manifest to contain path defaults without any `[[research_topics]]`, `[[topic_workspaces]]`, or topic defaults.
- Add explicit Research Topic CRUD command surfaces under `isomer-cli project topics`.
- Add plan-first destructive behavior for topic deletion, including `--dry-run`, `--yes`, and default workspace preservation.
- Update operator skills so Project initialization cannot create or infer topics, while topic-team specialization routes authoritative registration through the new topic CRUD boundary.

## Capabilities

### New Capabilities

- `research-topic-crud`: Defines explicit creation, inspection, update, and deletion of Research Topic registrations, Research Topic Config files, and their associated Topic Workspace registrations.

### Modified Capabilities

- `isomer-cli-project-discovery`: Project initialization changes from "bootstrap plus first topic" to "Project-only bootstrap with empty topic registry support."
- `cli-topic-context-resolution`: Topic-scoped commands must report a clear no-topic diagnostic when a Project has no registered Research Topics, while project-scoped commands continue to work.
- `isomer-admin-project-manager-skill`: Project-manager guidance must stop passing topic ids to `project init` and must point users to `project topics create` for topic creation.
- `topic-team-specialization-module-skill`: `init-topic` and specialization workflows must use or reference the supported topic CRUD command when topic material must become authoritative Project Manifest state.

## Impact

- CLI command registration and help text under `src/isomer_labs/cli/commands/project.py` and `src/isomer_labs/cli/app.py`.
- Project initialization logic in `src/isomer_labs/init_project.py`, content layout handling, and Project Manifest rendering.
- Manifest parsing and validation so empty Research Topic registries are valid for Project-level commands.
- Topic context resolution diagnostics for topic-scoped commands in empty Projects.
- Unit tests for Project init, topic CRUD, validation, context resolution, cleanup safety, and operator skill validation.
- Documentation and operator skills that currently say Project init creates the first Research Topic or Topic Workspace.
