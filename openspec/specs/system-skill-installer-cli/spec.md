# system-skill-installer-cli Specification

## Purpose
TBD - created by archiving change add-system-skill-installer-cli. Update Purpose after archive.
## Requirements
### Requirement: System Skill CLI Surface
The system SHALL expose a top-level `isomer-cli system-skills` command group for packaged Isomer system-skill installation and inspection.

#### Scenario: Help lists system-skills command group
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `system-skills`

#### Scenario: System skill group lists supported subcommands
- **WHEN** a user runs `isomer-cli system-skills --help`
- **THEN** the command help lists `list`, `status`, `install`, and `uninstall`

### Requirement: Packaged Skill Listing
The system SHALL list packaged Isomer system-skill groups, extensions, and skills from the installed package resources.

#### Scenario: List reads package manifest
- **WHEN** a user runs `isomer-cli system-skills list`
- **THEN** the output includes the packaged `core` group
- **AND** the output includes the `deepsci` extension when it is present in the packaged manifest
- **AND** the output includes at least `isomer-op-entrypoint`

#### Scenario: JSON list includes source paths
- **WHEN** a user runs `isomer-cli --print-json system-skills list`
- **THEN** the JSON payload includes groups, extensions, and skills
- **AND** each skill includes its install name and manifest-relative source path

### Requirement: Target Resolution
The system SHALL resolve supported system-skill install targets to deterministic skill roots.

#### Scenario: Claude Code target uses project skill root
- **WHEN** a user installs or checks status with `--target claude-code` and no `--home`
- **THEN** the target skill root is `.claude/skills` relative to the current working directory

#### Scenario: Codex target uses Codex home
- **WHEN** a user installs or checks status with `--target codex` and `CODEX_HOME` is set
- **THEN** the target skill root is `$CODEX_HOME/skills`

#### Scenario: Codex target falls back to user home
- **WHEN** a user installs or checks status with `--target codex` and `CODEX_HOME` is unset or empty
- **THEN** the target skill root is `~/.codex/skills`

#### Scenario: Kimi Code target uses project skill root
- **WHEN** a user installs or checks status with `--target kimi-code` and no `--home`
- **THEN** the target skill root is `.kimi-code/skills` relative to the current working directory

#### Scenario: Generic target uses open skill root
- **WHEN** a user installs or checks status with `--target generic` and no `--home`
- **THEN** the target skill root is `.agents/skills` relative to the current working directory

#### Scenario: All target expands concrete targets
- **WHEN** a user runs `isomer-cli system-skills install --target all`
- **THEN** the command attempts installation for `claude-code`, `codex`, `kimi-code`, and `generic`

#### Scenario: Home override is single target only
- **WHEN** a user supplies `--home <path>` with `--target all`
- **THEN** the command rejects the invocation before mutating files

### Requirement: Skill Selection
The system SHALL select installable packaged skills by group, extension, all extensions, or explicit skill name.

#### Scenario: Install defaults to core group
- **WHEN** a user runs `isomer-cli system-skills install --target generic` without selectors
- **THEN** the command installs only the packaged `core` group

#### Scenario: Install selected extension
- **WHEN** a user runs `isomer-cli system-skills install --target generic --extension deepsci`
- **THEN** the command installs the packaged `core` group and the `deepsci` extension skills

#### Scenario: Install all extensions
- **WHEN** a user runs `isomer-cli system-skills install --target generic --all-extensions`
- **THEN** the command installs the packaged `core` group and every packaged extension group

#### Scenario: Install explicit skill
- **WHEN** a user runs `isomer-cli system-skills install --target generic --skill isomer-op-entrypoint`
- **THEN** the command installs `isomer-op-entrypoint` even if no group selector is provided

#### Scenario: Unknown selector is rejected
- **WHEN** a user requests an unknown group, extension, or skill name
- **THEN** the command reports a deterministic error and does not mutate files

### Requirement: Skill Projection
The system SHALL project selected packaged skills into target skill roots as flat skill directories.

#### Scenario: Copy projection writes flat skill directory
- **WHEN** a user installs `isomer-op-entrypoint` into a target skill root in copy mode
- **THEN** the command creates `<skill-root>/isomer-op-entrypoint/SKILL.md`
- **AND** it copies the skill's packaged support files
- **AND** it does not create `<skill-root>/operator/isomer-op-entrypoint`

#### Scenario: Symlink projection writes flat skill link
- **WHEN** a user installs `isomer-op-entrypoint` into a target skill root with `--mode symlink`
- **THEN** the command creates `<skill-root>/isomer-op-entrypoint` as a symlink to the packaged skill source when the package resource is filesystem-backed

#### Scenario: Projection records ownership metadata
- **WHEN** a packaged skill is installed
- **THEN** the projected skill directory contains an Isomer ownership marker
- **AND** the marker records the skill name, manifest-relative source path, target, and projection mode

#### Scenario: Unowned collision is refused
- **WHEN** a target skill directory already exists without a valid Isomer ownership marker
- **THEN** install reports an unmanaged collision for that skill
- **AND** it does not overwrite the directory

### Requirement: Status and Uninstall
The system SHALL inspect and remove only Isomer-owned packaged skill projections.

#### Scenario: Status reports installed and missing skills
- **WHEN** a user runs `isomer-cli system-skills status --target generic`
- **THEN** the output reports the target skill root
- **AND** it reports installed Isomer-owned packaged skills
- **AND** it can report missing selected skills when selectors are supplied

#### Scenario: Status reports unmanaged collisions
- **WHEN** a target skill directory exists with a packaged skill name but without Isomer ownership metadata
- **THEN** status reports the skill as an unmanaged collision

#### Scenario: Uninstall removes Isomer-owned projections
- **WHEN** a user runs `isomer-cli system-skills uninstall --target generic`
- **THEN** the command removes Isomer-owned packaged skill projections under the generic skill root
- **AND** it reports removed and absent skills

#### Scenario: Uninstall preserves unmanaged collisions
- **WHEN** a target skill directory exists without Isomer ownership metadata
- **THEN** uninstall does not delete it
- **AND** the output reports that it was preserved as unmanaged

### Requirement: Documentation
The system SHALL document released-package system skill installation through `isomer-cli`.

#### Scenario: README describes CLI skill installation
- **WHEN** the README is inspected
- **THEN** it recommends installing Isomer system skills through `isomer-cli system-skills install`
- **AND** it names the supported targets

#### Scenario: Manual CLI reference lists system-skills commands
- **WHEN** the CLI reference is inspected
- **THEN** it documents `system-skills list`, `system-skills status`, `system-skills install`, and `system-skills uninstall`

