## Why

The `imsight-agent-skill-handling` skill currently supports `analyze`, `deep-inspect`, `create`, `test`, `harden`, and `format`, but it lacks a planning stage between understanding an existing skill and writing a new one. Designers often want to preview what a proposed skill would look like—its subcommands, process model, and file layout—before files are created. A `design` subcommand fills this gap by generating a self-contained design overview document from a user task, enabling review and iteration before implementation.

## What Changes

- Add a new `design` subcommand to `imsight-agent-skill-handling`.
- Create a `references/design.md` detail page that teaches the agent how to generate a design overview document for a proposed skill.
- Update `SKILL.md` to list `design` in the subcommand table, workflow, and invocation contract.
- Update the skill description to mention `design` alongside existing subcommands.
- Define the default output shape as a multi-subcommand skill with a `help` subcommand, following the preferred format documented in `references/create.md`.
- Establish the output location contract for `design`: user-provided path, then `IMSIGHT_SKILL_OUTPUT_DIR`, then `<project-dir>/.imsight-arts/skill-designs/<slug-of-skill-name-no-more-than-6-words>/design-overview.md`.
- The design document is read-only and intended for human review; it does not create `SKILL.md` or any skill files.

## Capabilities

### New Capabilities

- `imsight-agent-skill-handling-design`: Teach the `imsight-agent-skill-handling` skill to generate a `design-overview.md` document for a proposed skill from a user task, defaulting to a multi-subcommand design.

### Modified Capabilities

- None. This change adds a new subcommand and updates the skill entrypoint; it does not modify existing OpenSpec capability requirements.

## Impact

- Affects the `imsight-agent-skill-handling` skill in `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-agent-skill-handling/`.
- Updates `SKILL.md` frontmatter description to include the new `design` subcommand.
- Adds one new reference file: `references/design.md`.
- No impact on Isomer Labs runtime code, CLI, or existing OpenSpec specs.
