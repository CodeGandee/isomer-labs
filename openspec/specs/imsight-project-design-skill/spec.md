# imsight-project-design-skill Specification

## Purpose
TBD - created by archiving change design-skill-first-level-subcommand. Update Purpose after archive.
## Requirements
### Requirement: design-skill is a first-level subcommand
The `imsight-project-design` skill SHALL expose `design-skill` as a first-level subcommand that generates a skill design overview for an agent-skill feature.

#### Scenario: User invokes design-skill
- **WHEN** the user asks to design a skill using `imsight-project-design use design-skill` or an equivalent invocation
- **THEN** the skill loads the `design-skill` command detail page and executes its workflow

### Requirement: design-interface no longer auto-routes skill targets
The `design-interface` subcommand SHALL NOT detect skill targets from `feature-requirement.md` wording, example-prompt sections, or implicit signals.

#### Scenario: User invokes design-interface on a skill-like feature
- **WHEN** the user invokes `design-interface` on a feature whose requirement document states it is an agent skill
- **THEN** the skill writes normal interface and contract artifacts (`design/public-interfaces.md`) in the resolved feature directory

### Requirement: design-skill reuses the resolved feature directory
The `design-skill` subcommand SHALL use the feature directory already resolved by the entry workflow and SHALL NOT re-resolve the directory against `.imsight-arts/feature-design/`.

#### Scenario: User points to an existing feature directory
- **WHEN** the user provides `context/features/2026-07-08-toolbox-creator-skill` as the feature location
- **THEN** `design-skill` writes `context/features/2026-07-08-toolbox-creator-skill/design/<slug>/design-overview.md`

### Requirement: SKILL.md lists design-skill
The `SKILL.md` file for `imsight-project-design` SHALL include `design-skill` in the subcommands table and describe its purpose.

#### Scenario: Agent reads SKILL.md
- **WHEN** an agent reads `SKILL.md` to choose a subcommand
- **THEN** it finds `design-skill` with a description of when to use it

### Requirement: help.md mentions design-skill
The `commands/help.md` file for `imsight-project-design` SHALL mention `design-skill` when listing available subcommands.

#### Scenario: User asks for help
- **WHEN** the user invokes the help subcommand
- **THEN** the response includes `design-skill` alongside other subcommands

### Requirement: design-skill command file is self-contained
The `commands/design-skill.md` file SHALL contain the full skill-design workflow previously located in `references/skill-design.md`.

#### Scenario: Agent loads design-skill
- **WHEN** an agent loads `commands/design-skill.md`
- **THEN** it can execute the skill-design workflow without loading `references/skill-design.md`

