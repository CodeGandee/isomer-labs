## ADDED Requirements

### Requirement: Project Extension Detection Is Advisory and Target-Specific
The system SHALL provide read-only Project extension detection that reports installation and compatibility observations separately for each inspected agent target without modifying Project declarations or target skill roots.

#### Scenario: Default detection inspects Project-local targets
- **WHEN** a user runs `isomer-cli project system-extensions detect` without a target selector
- **THEN** the command inspects deterministic Project-local Claude Code, Kimi Code, and generic skill roots
- **AND** it does not inspect the user-global Codex root
- **AND** it reports results separately by target

#### Scenario: Explicit Codex detection inspects its resolved root
- **WHEN** a user runs Project extension detection with target `codex`
- **THEN** the command resolves `$CODEX_HOME/skills` or `~/.codex/skills` using system-skill target rules
- **AND** it reports Codex observations separately from Project-local targets

#### Scenario: Detection never remembers declarations
- **WHEN** detection finds a complete compatible extension that is not listed in `[operator.system_extensions]`
- **THEN** it reports `detected_undeclared`
- **AND** it advises `project system-extensions remember <extension-id>`
- **AND** it does not modify the Project Manifest

#### Scenario: Declared extension is absent or incompatible
- **WHEN** a Project-declared extension is missing, partial, unversioned, malformed, drifted, obsolete, or newer than the CLI for an inspected target
- **THEN** detection reports the target-specific state and evidence
- **AND** it provides bounded install, upgrade, repair, reload, or CLI-upgrade advice
- **AND** it does not mutate the installation

### Requirement: Extension Detection Aggregates Complete Family Readiness
Project extension detection SHALL evaluate the entry skill and every member skill declared by the packaged extension catalog before reporting a target extension ready.

#### Scenario: All extension members are compatible
- **WHEN** every catalog member exists in one target, carries valid consistent receipt and YAML metadata, and satisfies its compatibility floor
- **THEN** detection reports the extension as `ready` for that target
- **AND** it reports whether the extension is current or compatible older

#### Scenario: Only the entry skill is installed
- **WHEN** an extension entry skill exists but one or more catalog member skills are missing
- **THEN** detection reports `partial`
- **AND** it names the missing members and advises installing or upgrading the complete extension
