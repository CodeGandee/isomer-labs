## Why

`isomer-cli` is intended to be a system-level utility, but research execution is topic-scoped: each Research Topic can have its own Topic Workspace, Topic Agent Team Profile, Capability Binding refs, Gate policy refs, and execution defaults. Without a durable topic-context resolution contract, CLI commands and Execution Adapters must guess which topic they are operating on or hide topic-specific behavior in process-local environment variables.

## What Changes

- Define how `isomer-cli` discovers a Project, loads `.isomer-labs/manifest.toml`, and resolves an Effective Topic Context before running topic-scoped commands.
- Add Research Topic Config TOML files as project-registered, topic-specific configuration artifacts referenced by the Project Manifest.
- Specify the boundary between Project Manifest registration, Research Topic Config defaults, Topic Workspace state, Workspace Runtime records, and Execution Adapter launch-time environment.
- Allow Research Topic Config to select topic-specific Artifact Format Profiles and Artifact Extensions for expected outputs without changing the minimal core Artifact record.
- Define topic-context precedence for CLI flags, current directory, supported context environment variables, `.isomer-labs/local.toml` local active context, and Project Manifest defaults.
- Require resolved topic context to feed Workspace Path Resolution, Run creation, and future Execution Adapter command requests without making environment variables durable truth.
- Preserve unresolved command execution, scheduler policy, Skill Binding, baseline-waiver policy, and cost/privacy Gate policy placeholders for later contracts.

## Capabilities

### New Capabilities
- `cli-topic-context-resolution`: Defines Project discovery, Project Manifest topic registration, Research Topic Config TOML, Effective Topic Context resolution, validation, and `isomer-cli` topic-scoped command behavior.

### Modified Capabilities
- `workspace-path-resolution`: Clarifies that Workspace Path Resolution can consume an Effective Topic Context from `isomer-cli` or an Execution Adapter before resolving Topic Workspace and related path surfaces.
- `research-recording-contracts`: Clarifies that the core Artifact record is generic and minimal, while topic-specific Artifact Format Profiles and Artifact Extensions attach as optional records or refs.

## Impact

- Affected docs and specs: OpenSpec specs for CLI topic context resolution and Workspace Path Resolution.
- Affected future code: `isomer-cli` project discovery, manifest parsing, topic selection, topic config loading, artifact format default resolution, validation, Workspace Path Resolver inputs, Run initialization, and Execution Adapter launch preparation.
- Affected project files: `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/*.toml`, optional `.isomer-labs/artifact-formats/*.toml`, optional `.isomer-labs/artifact-extensions/*.toml`, optional untracked `.isomer-labs/local.toml`, and Topic Workspace Runtime records.
- No application code, runner implementation, scheduler loop, credential backend, Skill Binding schema, or command execution adapter is implemented by this change.
