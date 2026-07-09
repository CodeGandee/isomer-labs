## ADDED Requirements

### Requirement: Public System Skill Installation Documentation
The system SHALL document how users install packaged Isomer system skills into supported agent hosts from the published repository.

#### Scenario: Install docs prefer skills CLI
- **WHEN** a user follows public system-skill installation documentation
- **THEN** the docs SHALL recommend `npx skills add CodeGandee/isomer-labs` or an equivalent repository URL as the primary installation mechanism
- **AND** the docs SHALL show how to select skills with `--skill`

#### Scenario: Agent target is explicit
- **WHEN** docs show a skill installation command
- **THEN** the command SHALL include or explain `--agent <agent>` so users know which agent host receives the skills

#### Scenario: Entrypoint skill is discoverable
- **WHEN** docs explain operator skill installation
- **THEN** they SHALL identify `isomer-op-entrypoint` as the recommended first operator skill for users who already know the system
- **AND** they SHALL identify `isomer-op-welcome` as the orientation menu skill

#### Scenario: Extension skills are optional
- **WHEN** docs explain DeepSci skill installation
- **THEN** they SHALL state that DeepSci skills are optional extension skills and do not need to be installed for basic Project lifecycle CLI usage
