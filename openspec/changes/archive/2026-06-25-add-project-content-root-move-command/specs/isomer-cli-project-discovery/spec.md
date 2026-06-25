## ADDED Requirements

### Requirement: Project Content Root Relocation CLI Surface
The system SHALL expose content-root relocation through a Project-scoped command surface.

#### Scenario: Project help lists content-root group
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the help lists a `content-root` command group for generated content-root operations

#### Scenario: Content-root help lists move command
- **WHEN** a user runs `isomer-cli project content-root --help`
- **THEN** the help lists a `move` command for relocating the Project generated content root

#### Scenario: Move help lists required controls
- **WHEN** a user runs `isomer-cli project content-root move --help`
- **THEN** the help lists `--to <content-dir>`, `--dry-run`, and `--yes`

#### Scenario: Canonical move command shape
- **WHEN** docs, help, diagnostics, or operator guidance mention content-root relocation
- **THEN** they use `isomer-cli project content-root move --to <content-dir>` as the canonical command shape

### Requirement: Project Content Root Relocation CLI Output
The system SHALL expose relocation plans and results through standard CLI text and JSON output conventions.

#### Scenario: Dry-run supports JSON output
- **WHEN** a user runs `isomer-cli --print-json project content-root move --to custom-content --dry-run`
- **THEN** the command emits the standard versioned JSON output wrapper with a relocation payload and deterministic diagnostics

#### Scenario: Confirmed move supports JSON output
- **WHEN** a user runs `isomer-cli --print-json project content-root move --to custom-content --yes`
- **THEN** the command emits the standard versioned JSON output wrapper with applied relocation results and deterministic diagnostics

#### Scenario: Missing destination is rejected
- **WHEN** a user runs `isomer-cli project content-root move --dry-run` without `--to`
- **THEN** Click validation or an Isomer diagnostic rejects the request before planning mutation

#### Scenario: Missing confirmation is non-mutating
- **WHEN** a user runs `isomer-cli project content-root move --to custom-content` without `--yes`
- **THEN** the command behaves as a non-mutating plan, reports `dry_run = true`, and explains that applying the move requires `--yes`

### Requirement: Project Content Root Relocation Discovery
The system SHALL resolve the target Project for content-root relocation using the canonical Project discovery rules.

#### Scenario: Ancestor discovery locates Project
- **WHEN** a user runs `isomer-cli project content-root move --to custom-content --dry-run` from a directory below a Project root
- **THEN** the command walks parent directories to find `.isomer-labs/manifest.toml` and plans relocation for that Project

#### Scenario: Root selector applies to relocation
- **WHEN** a user runs `isomer-cli project --root <project-root> content-root move --to custom-content --dry-run`
- **THEN** the command plans relocation for the selected Project root

#### Scenario: Manifest selector applies to relocation
- **WHEN** a user runs `isomer-cli project --manifest <manifest-path> content-root move --to custom-content --dry-run`
- **THEN** the command plans relocation for the Project described by that manifest
