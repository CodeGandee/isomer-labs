## Why

`isomer-cli` is a global executable, but most current root-level commands operate on a specific Isomer Project discovered from cwd or selectors. Moving Project-targeted commands under `isomer-cli project` makes the command surface clearer, leaves room for global commands, and aligns Project discovery with the Git-style mental model: start from cwd, walk parents until `.isomer-labs/manifest.toml` is found, or fail.

## What Changes

- Add a root-level `project` command group as the canonical home for Project-targeted commands.
- Move Project-scoped command shapes under `isomer-cli project <subcmd> ...`, including initialization, cleanup, validation, diagnostics, topic/workspace listing, context inspection, path preview, runtime commands, template/profile commands, team-instance commands, and handoff commands.
- Keep global commands, such as `schemas list`, at the root when they do not require an active Project.
- Preserve and document Git-style ancestor discovery for Project commands: default to cwd, search parent directories for `.isomer-labs/manifest.toml`, and fail when none is found.
- Make `isomer-cli project init` refuse nested initialization when cwd or `--root` sits inside an existing ancestor Project unless the user targets a directory outside that Project.
- Introduce `--root <project-root>` as the canonical Project selector on the `project` group while preserving `--project` as a compatibility alias during the refactor.
- Treat legacy root-level Project command forms as deprecated compatibility aliases or remove them according to the migration policy chosen during implementation; canonical docs and skills must use `isomer-cli project ...`.
- Coordinate with the active cleanup change so the canonical cleanup command is `isomer-cli project cleanup`, not root-level `isomer-cli cleanup`.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-cli-project-discovery`: Refactor the CLI command surface so Project-targeted commands live under `isomer-cli project`, preserve Git-style Project discovery, and clarify global versus Project-scoped command boundaries.
- `isomer-admin-project-manager-skill`: Update operator guidance and CLI-boundary examples to use `isomer-cli project ...` command shapes.

## Impact

- Affected CLI code: Click command registration, root help text, Project command group registration, selector option names and aliases, command tests, and output command labels.
- Affected Project discovery behavior: no algorithm rewrite is expected for ancestor lookup, but behavior must be documented and tested at the `project` group boundary.
- Affected active OpenSpec work: `add-project-cleanup-command` should be amended or implemented so cleanup registers as `isomer-cli project cleanup`.
- Affected docs and skills: CLI reference, workflow/troubleshooting docs, and `skillset/operator/isomer-admin-project-mgr` command examples.
- Affected tests: root help tests, Project command help tests, command invocation tests, backward-compatibility alias tests if aliases are retained, and nested-init refusal tests.
