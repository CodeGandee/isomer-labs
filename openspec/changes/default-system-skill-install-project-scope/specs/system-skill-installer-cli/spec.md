## MODIFIED Requirements

### Requirement: System Skill Operations Report Resolved Scope
The system SHALL report the effective installation scope and resolved target bindings for every target-resolving system-skill operation, including an install whose scope came from the Project default.

#### Scenario: Concrete target reports scope
- **WHEN** a user runs `isomer-cli --print-json system-skills status --target kimi-code --scope user`
- **THEN** the result reports `user` as the selected scope
- **AND** it reports the normalized Kimi Code user skill root and the `kimi-code/user` binding

#### Scenario: Shared physical root reports all bindings
- **WHEN** `--target all --scope project` resolves both `codex` and `generic` to the same normalized physical skill root
- **THEN** JSON and human output report one physical-root result for that root
- **AND** the result includes both `codex/project` and `generic/project` bindings

#### Scenario: Omitted install scope reports effective Project scope
- **WHEN** a user runs `isomer-cli --print-json system-skills install --target generic` without `--scope`
- **THEN** the result reports `project` as the effective scope
- **AND** it reports the same normalized skill root, `generic/project` binding, diagnostics, and receipt metadata as an explicit `--scope project` install from the same current working directory

### Requirement: Target Resolution
The system SHALL require a target for every target-resolving system-skill command, SHALL default omitted scope to `project` for `system-skills install` only, SHALL require an explicit `user` or `project` scope for `status`, `upgrade`, and `uninstall`, and SHALL resolve each supported target and effective scope to a deterministic skill root.

#### Scenario: Install scope defaults to Project
- **WHEN** a user runs `isomer-cli system-skills install --target generic` without `--scope`
- **THEN** the command behaves as if `--scope project` were supplied
- **AND** it resolves the target from the exact current working directory
- **AND** it does not inspect or mutate the generic user skill root

#### Scenario: Non-install scope is required
- **WHEN** a user runs `system-skills status`, `system-skills upgrade`, or `system-skills uninstall` with a target but without `--scope`
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
- **WHEN** the current working directory is nested below a Git root or initialized Isomer Project and the user selects Project scope explicitly or through the install default
- **THEN** the resolver uses that current working directory as `<cwd>`
- **AND** it does not search parent directories for Git or Isomer metadata

#### Scenario: All target deduplicates shared physical roots
- **WHEN** a user supplies `--target all --scope project` or installs with `--target all` and omits scope
- **THEN** the command expands `claude-code`, `codex`, `kimi-code`, and `generic`
- **AND** it groups bindings with the same normalized absolute skill root before any filesystem operation
- **AND** it operates on each physical skill root exactly once

### Requirement: Skill Selection
The system SHALL select installable packaged skills by group, extension, all extensions, or explicit skill name after resolving a required target and an effective scope.

#### Scenario: Install defaults to core group
- **WHEN** a user runs `isomer-cli system-skills install --target generic` without selectors or scope
- **THEN** the command installs only the packaged `core` group into Project scope

#### Scenario: Install selected extension
- **WHEN** a user runs `isomer-cli system-skills install --target generic --extension deepsci`
- **THEN** the command installs the packaged `core` group and the `deepsci` extension skills into Project scope

#### Scenario: Install all extensions
- **WHEN** a user runs `isomer-cli system-skills install --target generic --all-extensions`
- **THEN** the command installs the packaged `core` group and every packaged extension group into Project scope

#### Scenario: Install explicit skill
- **WHEN** a user runs `isomer-cli system-skills install --target generic --skill isomer-op-entrypoint`
- **THEN** the command installs `isomer-op-entrypoint` into Project scope even if no group selector is provided

#### Scenario: Extension selector advertises packaged ids
- **WHEN** a user inspects help or shell completion for a `system-skills` command with `--extension`
- **THEN** the selector advertises the extension ids from the packaged manifest
- **AND** the selector does not require ids to be hardcoded separately from package metadata

#### Scenario: Unknown selector is rejected
- **WHEN** a user requests an unknown group, extension, or skill name
- **THEN** the command reports a deterministic error and does not mutate files

### Requirement: Skill Projection
The system SHALL project selected packaged skills into resolved target skill roots as flat skill directories or symlinks whose install slots are identified by packaged skill name.

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

### Requirement: Documentation
The system SHALL document released-package system skill installation through a required target, a Project-scope default when install scope is omitted, and an explicit scope for user-wide installation and all status, upgrade, and uninstall operations.

#### Scenario: README describes install scope default
- **WHEN** the README is inspected
- **THEN** it recommends installing Isomer system skills through `isomer-cli system-skills install`
- **AND** it states that an omitted install scope selects `project` at the exact current working directory
- **AND** it names the supported targets and the explicit `user` and `project` scopes

#### Scenario: Manual CLI reference distinguishes install from other operations
- **WHEN** the CLI reference is inspected
- **THEN** it documents `system-skills list`, `system-skills status`, `system-skills install`, `system-skills upgrade`, and `system-skills uninstall`
- **AND** its Project-install examples demonstrate the omitted-scope default or an explicit equivalent
- **AND** its user install, status, upgrade, and uninstall examples retain explicit scope
- **AND** its active command examples contain no `--home` option

#### Scenario: Migration guidance explains the relaxed install syntax
- **WHEN** a caller migrates from the prior CLI contract
- **THEN** documentation explains that an install without `--scope` now selects Project scope while explicit `--scope project` remains equivalent
- **AND** it states that user-wide install still requires `--scope user`
- **AND** it states that status, upgrade, and uninstall remain scope-explicit and arbitrary public install roots remain unsupported

### Requirement: Target Root Skill Manifest
The system SHALL maintain an `isomer-labs-skill-manifest.json` file in each physical skill root that records target-scope bindings and the Isomer system skills tracked in that root.

#### Scenario: Install writes effective-scope target root manifest
- **WHEN** `isomer-cli system-skills install` mutates a target skill root selected through omitted Project scope or an explicit scope
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
- **WHEN** a supported legacy receipt exists at the root selected by a required target and effective scope and install, upgrade, or uninstall mutates that root
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

### Requirement: Packaged Extension Discovery Commands
The system SHALL provide focused commands for discovering optional packaged system-skill extensions and their agent-facing entry surfaces using the Project-default install contract and scope-explicit status contract.

#### Scenario: Extension list summarizes available extensions
- **WHEN** a user runs `isomer-cli system-skills extensions list`
- **THEN** the output lists each packaged extension id, description, and entry skill in manifest order
- **AND** the output points to extension inspection for complete usage

#### Scenario: Extension show explains Kaoju usage
- **WHEN** a user runs `isomer-cli system-skills extensions show kaoju`
- **THEN** the output identifies `$isomer-kaoju-pipeline` as the entry skill
- **AND** it lists Kaoju's public procedure and helper command ids
- **AND** it provides an install command template that uses the omitted-scope Project default and a status command template that requires target and scope selection

#### Scenario: JSON discovery is structured
- **WHEN** a user requests JSON output for extension list or show
- **THEN** each extension object includes its id, group, description, entry skill, commands, skills, Project-default install command template, scope-explicit status command template, and invocation
- **AND** the response reports `mutated` as false

#### Scenario: Unknown extension show fails safely
- **WHEN** a user runs `isomer-cli system-skills extensions show <unknown-id>`
- **THEN** the command reports a deterministic unknown-extension error
- **AND** it does not mutate files
