## ADDED Requirements

### Requirement: System Skill Operations Report Resolved Scope
The system SHALL report the selected installation scope and resolved target bindings for every target-resolving system-skill operation.

#### Scenario: Concrete target reports scope
- **WHEN** a user runs `isomer-cli --print-json system-skills status --target kimi-code --scope user`
- **THEN** the result reports `user` as the selected scope
- **AND** it reports the normalized Kimi Code user skill root and the `kimi-code/user` binding

#### Scenario: Shared physical root reports all bindings
- **WHEN** `--target all --scope project` resolves both `codex` and `generic` to the same normalized physical skill root
- **THEN** JSON and human output report one physical-root result for that root
- **AND** the result includes both `codex/project` and `generic/project` bindings

## MODIFIED Requirements

### Requirement: Target Resolution
The system SHALL require an explicit `user` or `project` scope and resolve each supported system-skill target and scope to a deterministic skill root.

#### Scenario: Scope is required
- **WHEN** a user runs a target-resolving `system-skills` command without `--scope`
- **THEN** the command reports a missing required option
- **AND** it does not mutate any skill root

#### Scenario: Home override is removed
- **WHEN** a user supplies `--home` to a target-resolving `system-skills` command
- **THEN** the command rejects the unknown option
- **AND** it does not mutate any skill root

#### Scenario: Claude Code project scope uses current working directory
- **WHEN** a user supplies `--target claude-code --scope project`
- **THEN** the target skill root is `<cwd>/.claude/skills`

#### Scenario: Claude Code user scope honors configuration home
- **WHEN** a user supplies `--target claude-code --scope user` and `CLAUDE_CONFIG_DIR` is set and non-empty
- **THEN** the target skill root is `$CLAUDE_CONFIG_DIR/skills`

#### Scenario: Claude Code user scope falls back to user home
- **WHEN** a user supplies `--target claude-code --scope user` and `CLAUDE_CONFIG_DIR` is unset or empty
- **THEN** the target skill root is `~/.claude/skills`

#### Scenario: Codex project scope uses shared project skills
- **WHEN** a user supplies `--target codex --scope project`
- **THEN** the target skill root is `<cwd>/.agents/skills`

#### Scenario: Codex user scope honors Codex home
- **WHEN** a user supplies `--target codex --scope user` and `CODEX_HOME` is set and non-empty
- **THEN** the target skill root is `$CODEX_HOME/skills`

#### Scenario: Codex user scope preserves the Isomer personal fallback
- **WHEN** a user supplies `--target codex --scope user` and `CODEX_HOME` is unset or empty
- **THEN** the target skill root is `~/.codex/skills`

#### Scenario: Kimi Code project scope uses current working directory
- **WHEN** a user supplies `--target kimi-code --scope project`
- **THEN** the target skill root is `<cwd>/.kimi-code/skills`

#### Scenario: Kimi Code user scope honors Kimi Code home
- **WHEN** a user supplies `--target kimi-code --scope user` and `KIMI_CODE_HOME` is set and non-empty
- **THEN** the target skill root is `$KIMI_CODE_HOME/skills`

#### Scenario: Kimi Code user scope falls back to user home
- **WHEN** a user supplies `--target kimi-code --scope user` and `KIMI_CODE_HOME` is unset or empty
- **THEN** the target skill root is `~/.kimi-code/skills`

#### Scenario: Generic project scope uses shared project skills
- **WHEN** a user supplies `--target generic --scope project`
- **THEN** the target skill root is `<cwd>/.agents/skills`

#### Scenario: Generic user scope uses shared personal skills
- **WHEN** a user supplies `--target generic --scope user`
- **THEN** the target skill root is `~/.agents/skills`

#### Scenario: Project scope is anchored exactly at the current working directory
- **WHEN** the current working directory is nested below a Git root or initialized Isomer Project and the user selects `--scope project`
- **THEN** the resolver uses that current working directory as `<cwd>`
- **AND** it does not search parent directories for Git or Isomer metadata

#### Scenario: All target deduplicates shared physical roots
- **WHEN** a user supplies `--target all --scope project`
- **THEN** the command expands `claude-code`, `codex`, `kimi-code`, and `generic`
- **AND** it groups bindings with the same normalized absolute skill root before any filesystem operation
- **AND** it operates on each physical skill root exactly once

### Requirement: Skill Selection
The system SHALL select installable packaged skills by group, extension, all extensions, or explicit skill name after resolving an explicit target and scope.

#### Scenario: Install defaults to core group
- **WHEN** a user runs `isomer-cli system-skills install --target generic --scope project` without selectors
- **THEN** the command installs only the packaged `core` group

#### Scenario: Install selected extension
- **WHEN** a user runs `isomer-cli system-skills install --target generic --scope project --extension deepsci`
- **THEN** the command installs the packaged `core` group and the `deepsci` extension skills

#### Scenario: Install all extensions
- **WHEN** a user runs `isomer-cli system-skills install --target generic --scope project --all-extensions`
- **THEN** the command installs the packaged `core` group and every packaged extension group

#### Scenario: Install explicit skill
- **WHEN** a user runs `isomer-cli system-skills install --target generic --scope project --skill isomer-op-entrypoint`
- **THEN** the command installs `isomer-op-entrypoint` even if no group selector is provided

#### Scenario: Extension selector advertises packaged ids
- **WHEN** a user inspects help or shell completion for a `system-skills` command with `--extension`
- **THEN** the selector advertises the extension ids from the packaged manifest
- **AND** the selector does not require ids to be hardcoded separately from package metadata

#### Scenario: Unknown selector is rejected
- **WHEN** a user requests an unknown group, extension, or skill name
- **THEN** the command reports a deterministic error and does not mutate files

### Requirement: Skill Projection
The system SHALL project selected packaged skills into explicitly scoped target skill roots as flat skill directories or symlinks whose install slots are identified by packaged skill name.

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
- **AND** it does not overwrite, unlink, remove, or claim ownership of an untracked path

#### Scenario: Force replaces existing selected path
- **WHEN** a user installs a selected packaged skill with `--force` and `<skill-root>/<skill-name>` already exists as a file, directory, or symlink
- **THEN** the command removes exactly `<skill-root>/<skill-name>`
- **AND** it projects the packaged skill into `<skill-root>/<skill-name>` using the requested projection mode
- **AND** it reports that the path was replaced

#### Scenario: Force switches copy projection to symlink projection
- **WHEN** `<skill-root>/isomer-op-entrypoint` exists as a real directory
- **AND** a user runs `isomer-cli system-skills install --target generic --scope project --skill isomer-op-entrypoint --mode symlink --force`
- **THEN** the command removes the real directory
- **AND** it creates `<skill-root>/isomer-op-entrypoint` as a symlink to the packaged skill source

#### Scenario: Force switches symlink projection to copy projection
- **WHEN** `<skill-root>/isomer-op-entrypoint` exists as a symlink
- **AND** a user runs `isomer-cli system-skills install --target generic --scope project --skill isomer-op-entrypoint --mode copy --force`
- **THEN** the command unlinks the symlink without deleting the symlink target
- **AND** it creates `<skill-root>/isomer-op-entrypoint` as a real copied directory

### Requirement: Status and Uninstall
The system SHALL inspect and remove selected packaged skill install slots by packaged skill name under the explicit target and scope.

#### Scenario: Status reports installed and missing skills
- **WHEN** a user runs `isomer-cli system-skills status --target generic --scope project`
- **THEN** the output reports the target, project scope, and resolved skill root
- **AND** it reports selected packaged skills as installed when `<skill-root>/<skill-name>` exists
- **AND** it can report missing selected skills when selectors are supplied and `<skill-root>/<skill-name>` does not exist
- **AND** it reports target-root install manifest metadata when `isomer-labs-skill-manifest.json` exists

#### Scenario: Status reports projection path shape
- **WHEN** a selected packaged skill path exists under the explicitly resolved target skill root
- **THEN** status reports the installed skill name, projection path, packaged source path, and detected projection mode when the path is a real directory or symlink
- **AND** status reports a deterministic invalid projection diagnostic when the path exists but is neither a real directory nor a symlink directory projection

#### Scenario: Uninstall removes selected named projections
- **WHEN** a user runs `isomer-cli system-skills uninstall --target generic --scope project`
- **THEN** the command removes selected packaged skill paths under the resolved project skill root by packaged skill name
- **AND** it reports removed and absent skills

#### Scenario: Uninstall removes symlink projection without following it
- **WHEN** a selected packaged skill path under the explicitly resolved target skill root is a symlink
- **THEN** uninstall removes the symlink entry itself
- **AND** it does not delete the symlink target

### Requirement: Documentation
The system SHALL document released-package system skill installation through explicit `--target` and `--scope` selection.

#### Scenario: README describes scoped CLI skill installation
- **WHEN** the README is inspected
- **THEN** it recommends installing Isomer system skills through `isomer-cli system-skills install`
- **AND** it names the supported targets and the `user` and `project` scopes

#### Scenario: Manual CLI reference lists scoped system-skills commands
- **WHEN** the CLI reference is inspected
- **THEN** it documents `system-skills list`, `system-skills status`, `system-skills install`, `system-skills upgrade`, and `system-skills uninstall`
- **AND** its target matrix and examples use required scope syntax and contain no `--home` option

#### Scenario: Migration guidance explains the breaking syntax
- **WHEN** a caller migrates from the prior CLI contract
- **THEN** documentation explains how to replace an implicit default or `--home` invocation with the corresponding target and scope
- **AND** it states that arbitrary public install roots are no longer supported

### Requirement: Target Root Skill Manifest
The system SHALL maintain an `isomer-labs-skill-manifest.json` file in each physical skill root that records target-scope bindings and the Isomer system skills tracked in that root.

#### Scenario: Install writes scope-aware target root manifest
- **WHEN** `isomer-cli system-skills install` mutates an explicitly scoped target skill root
- **THEN** the command writes `<skill-root>/isomer-labs-skill-manifest.json` using `isomer-labs-skill-manifest.v3`
- **AND** the manifest records the normalized skill root path, Isomer CLI or package version, update timestamp, and a sorted set of target-scope bindings
- **AND** each tracked installed skill record includes skill name, manifest-relative source path, projection mode, and skill version

#### Scenario: Shared root manifest records multiple bindings
- **WHEN** one resolved physical root represents more than one target-scope binding in the same operation
- **THEN** the manifest records each binding exactly once
- **AND** the installer projects each selected skill exactly once

#### Scenario: Later mutation merges a compatible binding
- **WHEN** a v3 receipt exists and a later authorized operation reaches the same physical root through another target-scope binding
- **THEN** the writer preserves existing bindings and adds the current binding
- **AND** it does not duplicate per-skill records or discard prior ownership metadata

#### Scenario: Per-skill marker files are not required
- **WHEN** a selected packaged skill is installed as a copied directory or symlink
- **THEN** ownership and upgrade tracking are recorded in `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** the command does not require `.isomer-system-skill.json` inside the skill directory

#### Scenario: Legacy receipt remains readable without invented scope
- **WHEN** status reads a supported v1 or v2 receipt
- **THEN** it preserves the receipt as legacy evidence
- **AND** it reports the missing scope or binding metadata as unknown rather than inferring it from the path

#### Scenario: Authorized mutation upgrades a legacy receipt
- **WHEN** a supported legacy receipt exists at the root selected by an explicit target and scope and install, upgrade, or uninstall mutates that root
- **THEN** the command writes a v3 receipt with the current target-scope binding
- **AND** it preserves valid tracked skill records that remain installed

#### Scenario: Uninstall updates target root manifest
- **WHEN** `isomer-cli system-skills uninstall` removes one or more selected packaged skill paths
- **THEN** the command updates `<skill-root>/isomer-labs-skill-manifest.json`
- **AND** removed skill names are no longer listed as tracked installed skills

#### Scenario: Status reports unreadable manifest
- **WHEN** `<skill-root>/isomer-labs-skill-manifest.json` exists but cannot be parsed as a supported manifest
- **THEN** status reports a deterministic warning diagnostic
- **AND** status still derives selected skill path existence from the filesystem

### Requirement: System Skill Upgrade
The system SHALL provide `isomer-cli system-skills upgrade` to refresh installed packaged system skills and clean up stale manifest-tracked skill paths under an explicit target and scope after Isomer CLI or package upgrades.

#### Scenario: Upgrade refreshes current selected skills
- **WHEN** a user runs `isomer-cli system-skills upgrade --target generic --scope project`
- **THEN** the command resolves the current selected packaged skill set using the same selector rules as install
- **AND** it refreshes each selected skill path from the current package resources
- **AND** it updates `<skill-root>/isomer-labs-skill-manifest.json` with the current Isomer CLI or package version and target-scope binding

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
The system SHALL provide focused commands for discovering optional packaged system-skill extensions and their agent-facing entry surfaces using the scoped installer contract.

#### Scenario: Extension list summarizes available extensions
- **WHEN** a user runs `isomer-cli system-skills extensions list`
- **THEN** the output lists each packaged extension id, description, and entry skill in manifest order
- **AND** the output points to extension inspection for complete usage

#### Scenario: Extension show explains Kaoju usage
- **WHEN** a user runs `isomer-cli system-skills extensions show kaoju`
- **THEN** the output identifies `$isomer-kaoju-pipeline` as the entry skill
- **AND** it lists Kaoju's public procedure and helper command ids
- **AND** it provides install and status command templates that require target and scope selection

#### Scenario: JSON discovery is structured
- **WHEN** a user requests JSON output for extension list or show
- **THEN** each extension object includes its id, group, description, entry skill, commands, skills, scoped install command template, scoped status command template, and invocation
- **AND** the response reports `mutated` as false

#### Scenario: Unknown extension show fails safely
- **WHEN** a user runs `isomer-cli system-skills extensions show <unknown-id>`
- **THEN** the command reports a deterministic unknown-extension error
- **AND** it does not mutate files
