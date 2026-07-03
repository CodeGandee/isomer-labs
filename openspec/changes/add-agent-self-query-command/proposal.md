## Why

Coding agents may run with the Topic Main Development Repository as their cwd, where cwd-based Agent Workspace inference is intentionally unavailable. They need safe, read-only `isomer-cli` self queries that reveal only the slice of identity, environment, path, or Pixi context they ask for, because dumping every self-related fact in one response wastes agent context tokens.

## What Changes

- Add a read-only agent-facing `project self` command family with selectable subcommands: `show`, `identity`, `pixi`, `env`, `paths`, and `queries`.
- Make `project self show` a tiny summary or index, not a full self packet. It reports only the selected topic/workspace, resolved actor or agent headline when available, diagnostic counts, and which more-specific self queries are available.
- Return detailed identity, Pixi, environment, semantic path, and follow-up query data only from explicit subcommands or explicit selectors such as `project self paths <label>...`.
- Ensure the command works from a Topic Main Development Repository cwd when launch-time `ISOMER_*` identity variables are present, and degrades clearly when no Agent Instance or Agent Name can be resolved.
- Update the topic-main guidance renderer so injected `AGENTS.md` and `CLAUDE.md` blocks tell coding agents to start with the small self summary and query only the needed slice before using lower-level context and path commands.
- Update CLI docs, command-surface help, and tests for the new command.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `cli-topic-context-resolution`: Add a first-class, progressive self query contract for resolving and selectively reporting the caller's process-local Isomer identity, launch environment inputs, Topic Actor context, Effective Agent Context, semantic paths, and Pixi execution hints.
- `isomer-cli-project-discovery`: Add the `project self` command family, JSON behavior, help text, documentation, and no-side-effect guarantees.

## Impact

- Affected code: `src/isomer_labs/cli/app.py`, `src/isomer_labs/cli/commands/project.py`, context/path/Pixi helper modules as needed, and the topic-main guidance renderer/template.
- Affected docs and specs: `docs/isomer-cli.md`, the topic-main guidance template, CLI command-surface tests, context-resolution tests, and OpenSpec specs for CLI discovery and topic context resolution.
- API impact: new read-only CLI command family and several small JSON payload shapes; no breaking changes to existing commands.
- Dependencies: no new external dependencies expected.
