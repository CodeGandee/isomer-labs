## MODIFIED Requirements

### Requirement: System Skill CLI Surface
The system SHALL expose a top-level `isomer-cli system-skills` command group for packaged Isomer system-skill discovery, installation, upgrade, and inspection.

#### Scenario: Help lists system-skills command group
- **WHEN** a user runs `isomer-cli --help`
- **THEN** the command help lists `system-skills`

#### Scenario: System skill group lists supported subcommands
- **WHEN** a user runs `isomer-cli system-skills --help`
- **THEN** the command help lists `extensions`, `list`, `status`, `install`, `upgrade`, and `uninstall`

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

## ADDED Requirements

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
- **AND** the CLI does not claim that `isomer-cli ext kaoju` exists
