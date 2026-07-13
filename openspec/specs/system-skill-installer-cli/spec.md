# system-skill-installer-cli Specification

## Purpose
TBD - created by archiving change add-system-skill-installer-cli. Update Purpose after archive.
## Requirements
### Requirement: System Skill CLI Surface
The system SHALL expose a top-level `isomer-cli system-skills` command group for packaged Isomer system-skill discovery, installation, upgrade, and inspection.

#### Scenario: Help lists system-skills command group
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `system-skills`

#### Scenario: System skill group lists supported subcommands
- **WHEN** a user runs `isomer-cli system-skills --help`
- **THEN** the command help lists `extensions`, `list`, `status`, `install`, `upgrade`, and `uninstall`

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

#### Scenario: Extension selector advertises packaged ids
- **WHEN** a user inspects help or shell completion for a `system-skills` command with `--extension`
- **THEN** the selector advertises the extension ids from the packaged manifest
- **AND** the selector does not require ids to be hardcoded separately from package metadata

#### Scenario: Unknown selector is rejected
- **WHEN** a user requests an unknown group, extension, or skill name
- **THEN** the command reports a deterministic error and does not mutate files

### Requirement: Skill Projection
The system SHALL project selected packaged skills into target skill roots as flat skill directories or symlinks whose install slots are identified by packaged skill name.

#### Scenario: Copy projection writes flat skill directory
- **WHEN** a user installs `isomer-op-entrypoint` into a target skill root in copy mode and `<skill-root>/isomer-op-entrypoint` does not exist
- **THEN** the command creates `<skill-root>/isomer-op-entrypoint/SKILL.md`
- **AND** it copies the skill's packaged support files
- **AND** it does not create `<skill-root>/operator/isomer-op-entrypoint`
- **AND** it does not create a per-skill Isomer ownership marker file

#### Scenario: Symlink projection writes flat skill link
- **WHEN** a user installs `isomer-op-entrypoint` into a target skill root with `--mode symlink` and `<skill-root>/isomer-op-entrypoint` does not exist
- **THEN** the command creates `<skill-root>/isomer-op-entrypoint` as a symlink to the packaged skill source when the package resource is filesystem-backed
- **AND** it does not write marker files through the symlink or into the packaged skill source

#### Scenario: Existing selected path is preserved without force
- **WHEN** a user installs a selected packaged skill and `<skill-root>/<skill-name>` already exists as a file, directory, or symlink
- **THEN** the command reports the existing selected path for that skill
- **AND** it does not overwrite, unlink, or remove that path

#### Scenario: Force replaces existing selected path
- **WHEN** a user installs a selected packaged skill with `--force` and `<skill-root>/<skill-name>` already exists as a file, directory, or symlink
- **THEN** the command removes exactly `<skill-root>/<skill-name>`
- **AND** it projects the packaged skill into `<skill-root>/<skill-name>` using the requested projection mode
- **AND** it reports that the path was replaced

#### Scenario: Force switches copy projection to symlink projection
- **WHEN** `<skill-root>/isomer-op-entrypoint` exists as a real directory
- **AND** a user runs `isomer-cli system-skills install --target generic --skill isomer-op-entrypoint --mode symlink --force`
- **THEN** the command removes the real directory
- **AND** it creates `<skill-root>/isomer-op-entrypoint` as a symlink to the packaged skill source

#### Scenario: Force switches symlink projection to copy projection
- **WHEN** `<skill-root>/isomer-op-entrypoint` exists as a symlink
- **AND** a user runs `isomer-cli system-skills install --target generic --skill isomer-op-entrypoint --mode copy --force`
- **THEN** the command unlinks the symlink without deleting the symlink target
- **AND** it creates `<skill-root>/isomer-op-entrypoint` as a real copied directory

### Requirement: Status and Uninstall
The system SHALL inspect and remove selected packaged skill install slots by packaged skill name.

#### Scenario: Status reports installed and missing skills
- **WHEN** a user runs `isomer-cli system-skills status --target generic`
- **THEN** the output reports the target skill root
- **AND** it reports selected packaged skills as installed when `<skill-root>/<skill-name>` exists
- **AND** it can report missing selected skills when selectors are supplied and `<skill-root>/<skill-name>` does not exist
- **AND** it reports target-root install manifest metadata when `isomer-labs-skill-manifest.json` exists

#### Scenario: Status reports projection path shape
- **WHEN** a selected packaged skill path exists under the target skill root
- **THEN** status reports the installed skill name, projection path, packaged source path, and detected projection mode when the path is a real directory or symlink
- **AND** status reports a deterministic invalid projection diagnostic when the path exists but is neither a real directory nor a symlink directory projection

#### Scenario: Uninstall removes selected named projections
- **WHEN** a user runs `isomer-cli system-skills uninstall --target generic`
- **THEN** the command removes selected packaged skill paths under the generic skill root by packaged skill name
- **AND** it reports removed and absent skills

#### Scenario: Uninstall removes symlink projection without following it
- **WHEN** a selected packaged skill path under the target skill root is a symlink
- **THEN** uninstall removes the symlink entry itself
- **AND** it does not delete the symlink target

### Requirement: Documentation
The system SHALL document released-package system skill installation through `isomer-cli`.

#### Scenario: README describes CLI skill installation
- **WHEN** the README is inspected
- **THEN** it recommends installing Isomer system skills through `isomer-cli system-skills install`
- **AND** it names the supported targets

#### Scenario: Manual CLI reference lists system-skills commands
- **WHEN** the CLI reference is inspected
- **THEN** it documents `system-skills list`, `system-skills status`, `system-skills install`, and `system-skills uninstall`

### Requirement: Target Root Skill Manifest
The system SHALL maintain an `isomer-labs-skill-manifest.json` file in each target skill root that records the Isomer CLI/package version and the Isomer system skills tracked in that root.

#### Scenario: Install writes target root manifest
- **WHEN** `isomer-cli system-skills install` mutates a target skill root
- **THEN** the command writes `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** the manifest records a schema version, target name, skill root path, Isomer CLI/package version, update timestamp, and the tracked installed skills
- **AND** each tracked installed skill record includes skill name, manifest-relative source path, and projection mode

#### Scenario: Per-skill marker files are not required
- **WHEN** a selected packaged skill is installed as a copied directory or symlink
- **THEN** ownership and upgrade tracking are recorded in `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** the command does not require `.isomer-system-skill.json` inside the skill directory

#### Scenario: Uninstall updates target root manifest
- **WHEN** `isomer-cli system-skills uninstall` removes one or more selected packaged skill paths
- **THEN** the command updates `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** removed skill names are no longer listed as tracked installed skills

#### Scenario: Status reports unreadable manifest
- **WHEN** `<skill-root>/isomer-labs-skill-manifest.json` exists but cannot be parsed as a supported manifest
- **THEN** status reports a deterministic warning diagnostic
- **AND** status still derives selected skill path existence from the filesystem

### Requirement: System Skill Upgrade
The system SHALL provide `isomer-cli system-skills upgrade` to refresh installed packaged system skills and clean up stale manifest-tracked skill paths after Isomer CLI/package upgrades.

#### Scenario: Upgrade refreshes current selected skills
- **WHEN** a user runs `isomer-cli system-skills upgrade --target generic`
- **THEN** the command resolves the current selected packaged skill set using the same selector rules as install
- **AND** it refreshes each selected skill path from the current package resources
- **AND** it updates `<skill-root>/isomer-labs-skill-manifest.json` with the current Isomer CLI/package version

#### Scenario: Upgrade removes stale manifest-tracked skills
- **WHEN** the target root manifest lists a previously installed skill name that is not in the current selected packaged skill set
- **AND** `<skill-root>/<old-skill-name>` exists
- **THEN** upgrade removes `<skill-root>/<old-skill-name>`
- **AND** it reports the stale skill path as removed

#### Scenario: Upgrade does not remove untracked paths
- **WHEN** a path exists under the target skill root but its name is not tracked in `isomer-labs-skill-manifest.json`
- **THEN** upgrade does not remove that path as a stale installed skill

#### Scenario: Upgrade preserves recorded projection mode by default
- **WHEN** the target root manifest records a projection mode for an installed selected skill
- **AND** the user runs upgrade without an explicit projection mode override
- **THEN** upgrade refreshes that skill using the recorded projection mode

#### Scenario: Upgrade can change projection mode explicitly
- **WHEN** the user runs upgrade with an explicit projection mode
- **THEN** upgrade refreshes selected skills using the requested projection mode
- **AND** it records that projection mode in the target root manifest

### Requirement: Packaged Extension Discovery Commands
The system SHALL provide focused commands for discovering optional packaged system-skill extensions and their agent-facing entry surfaces.

#### Scenario: Extension list summarizes available extensions
- **WHEN** a user runs `isomer-cli system-skills extensions list`
- **THEN** the output lists each packaged extension id, description, and entry skill in manifest order
- **AND** the output points to extension inspection for complete usage

#### Scenario: Extension show explains Kaoju usage
- **WHEN** a user runs `isomer-cli system-skills extensions show kaoju`
- **THEN** the output identifies `$isomer-kaoju-pipeline` as the entry skill
- **AND** it lists Kaoju's public procedure and helper command ids
- **AND** it provides commands to install and inspect the Kaoju extension

#### Scenario: JSON discovery is structured
- **WHEN** a user requests JSON output for extension list or show
- **THEN** each extension object includes its id, group, description, entry skill, commands, skills, install command, status command, and invocation
- **AND** the response reports `mutated` as false

#### Scenario: Unknown extension show fails safely
- **WHEN** a user runs `isomer-cli system-skills extensions show <unknown-id>`
- **THEN** the command reports a deterministic unknown-extension error
- **AND** it does not mutate files

### Requirement: CLI Extension Namespaces Are Distinguishable
The CLI SHALL distinguish native runtime or compatibility command surfaces from installable agent-skill extensions.

#### Scenario: Runtime extension help points to system-skill discovery
- **WHEN** a user runs `isomer-cli ext --help`
- **THEN** the help describes `ext` as runtime and compatibility command surfaces
- **AND** it points to `isomer-cli system-skills extensions` for installable agent-skill extensions

#### Scenario: Kaoju remains agent-skill driven
- **WHEN** a user inspects the Kaoju extension
- **THEN** the CLI directs the user to install and invoke `$isomer-kaoju-pipeline`
- **AND** the CLI does not claim that `isomer-cli ext kaoju` exists\n

### Requirement: Packaged Skills Carry Release-Aligned Versions
Every packaged Isomer system skill SHALL declare `metadata.version` in `agents/openai.yaml` using the exact PEP 440 Isomer CLI/package version that ships the skill, including release candidate versions.

#### Scenario: Packaged source version matches the CLI release
- **WHEN** packaged system-skill assets are validated for a release
- **THEN** every skill's `agents/openai.yaml` contains a valid PEP 440 `metadata.version`
- **AND** the version equals the Isomer CLI/package version
- **AND** `SKILL.md` frontmatter does not duplicate the skill version

#### Scenario: Release candidate version is accepted
- **WHEN** the Isomer CLI/package version is a valid release candidate such as `0.3.0rc1`
- **THEN** packaged skills declare that exact release candidate version
- **AND** validation uses PEP 440 ordering rather than ad hoc string comparison

### Requirement: Package Catalog Defines Skill Compatibility Floors
The package-owned system-skill catalog SHALL define a minimum compatible skill version for each system-skill group and SHALL allow a per-skill override for a skill that requires a newer floor.

#### Scenario: Group compatibility floor applies by default
- **WHEN** a packaged skill has no per-skill compatibility override
- **THEN** compatibility evaluation uses its group's minimum compatible skill version

#### Scenario: Per-skill compatibility floor overrides the group
- **WHEN** packaged skill metadata declares a minimum compatible version newer than its group default
- **THEN** compatibility evaluation uses the per-skill minimum

### Requirement: Installation Receipts Preserve Skill Versions
The system-skill installer SHALL snapshot each projected skill's release version in the target-root installation receipt and SHALL read legacy receipts without treating their unversioned records as verified.

#### Scenario: Install writes per-skill versions
- **WHEN** `isomer-cli system-skills install` projects selected skills
- **THEN** each tracked receipt record includes the skill name, source path, projection mode, and skill version read from packaged `agents/openai.yaml`

#### Scenario: Legacy receipt remains inspectable
- **WHEN** status or detection reads a supported legacy receipt without per-skill versions
- **THEN** it preserves the receipt as legacy evidence
- **AND** it reports affected skills as unversioned rather than inventing versions from the receipt package version

#### Scenario: Receipt and projected metadata disagree
- **WHEN** a tracked receipt version differs from the projected skill's `agents/openai.yaml` version
- **THEN** status reports receipt drift
- **AND** the installation is not reported as compatibility-verified

### Requirement: Status Classifies Skill Version Compatibility
System-skill status SHALL compare installed skill versions with the current CLI version and package-owned minimum compatibility floors using PEP 440 semantics.

#### Scenario: Compatible older skill is usable
- **WHEN** an installed skill version is at least its minimum compatible version and lower than the current CLI version
- **THEN** status reports `compatible_older`
- **AND** it may advise upgrade without classifying the skill as incompatible

#### Scenario: Obsolete skill is incompatible
- **WHEN** an installed skill version is lower than its minimum compatible version
- **THEN** status reports `obsolete_incompatible`
- **AND** it advises upgrading the target's system skills

#### Scenario: Newer skill has unknown compatibility
- **WHEN** an installed skill version is newer than the current CLI version
- **THEN** status reports `newer_than_cli`
- **AND** it advises upgrading the CLI instead of claiming compatibility

#### Scenario: Missing or malformed version is not verified
- **WHEN** projected `agents/openai.yaml` lacks `metadata.version` or contains an invalid PEP 440 version
- **THEN** status reports `unversioned` or `malformed_version`
- **AND** it does not claim compatibility
