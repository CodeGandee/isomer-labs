## Why

Coding agents may run with the Topic Main Development Repository as their cwd, where cwd-based Agent Workspace inference is intentionally unavailable. They need one safe, read-only `isomer-cli` query that tells them who Isomer thinks they are, which Isomer launch/configuration environment variables were recognized, and how to discover their topic, actor, agent, workspace paths, and Pixi execution target without guessing.

## What Changes

- Add a read-only agent-facing self query command, tentatively `isomer-cli project self show`, that resolves Effective Topic Context plus optional Topic Actor and Effective Agent Context from selectors, environment, cwd, local context, runtime records, and Project Manifest defaults.
- Return a deterministic text and JSON payload with resolved identity, identity-source metadata, recognized Isomer environment inputs, missing or conflicting identity diagnostics, safe follow-up query commands, selected semantic paths, and Pixi command hints when the topic Pixi binding can be resolved.
- Ensure the command works from a Topic Main Development Repository cwd when launch-time `ISOMER_*` identity variables are present, and degrades clearly when no Agent Instance or Agent Name can be resolved.
- Update the topic-main guidance renderer so injected `AGENTS.md` and `CLAUDE.md` blocks tell coding agents to start with the new self query before using lower-level context and path commands.
- Update CLI docs, command-surface help, and tests for the new command.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cli-topic-context-resolution`: Add a first-class self query contract for resolving and reporting the caller's process-local Isomer identity, launch environment inputs, Topic Actor context, Effective Agent Context, semantic path summary, and Pixi execution hints.
- `isomer-cli-project-discovery`: Add the `project self show` command surface, JSON behavior, help text, documentation, and no-side-effect guarantees.

## Impact

- Affected code: `src/isomer_labs/cli/app.py`, `src/isomer_labs/cli/commands/project.py`, context/path/Pixi helper modules as needed, and the topic-main guidance renderer/template.
- Affected docs and specs: `docs/isomer-cli.md`, the topic-main guidance template, CLI command-surface tests, context-resolution tests, and OpenSpec specs for CLI discovery and topic context resolution.
- API impact: new read-only CLI command and JSON payload shape; no breaking changes to existing commands.
- Dependencies: no new external dependencies expected.
