## ADDED Requirements

### Requirement: Toolbox CLI Surface Presents Canonical Bundle Install
The system SHALL present `project toolboxes install` as the canonical command for installing an effective Toolbox bundle while keeping lower-level callback and runtime-param command groups discoverable as primitives.

#### Scenario: Project help exposes Toolbox commands
- **WHEN** a user runs `isomer-cli project --help`
- **THEN** the command help lists `toolboxes`, `skill-callbacks`, and `toolbox-params` command groups

#### Scenario: Toolboxes help names bundle install
- **WHEN** a user runs `isomer-cli project toolboxes --help`
- **THEN** the command help presents `install` as the operation for installing or updating an effective Toolbox bundle from a Toolbox directory

#### Scenario: Skill callbacks help names primitive role
- **WHEN** a user runs `isomer-cli project skill-callbacks --help`
- **THEN** the command help presents direct callback registration, resolution, validation, and callback-manifest installation as lower-level User Skill Callback operations rather than the canonical Toolbox bundle install path

#### Scenario: Runtime params help names primitive role
- **WHEN** a user runs `isomer-cli project toolbox-params --help`
- **THEN** the command help presents runtime-param definition, mutation, lookup, explanation, import management, and validation as direct configuration primitives that can be used with or without high-level Toolbox installation
