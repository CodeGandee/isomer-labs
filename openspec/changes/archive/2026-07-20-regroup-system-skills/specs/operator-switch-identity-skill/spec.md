## MODIFIED Requirements

### Requirement: Switch Identity Operator Skill
The core public pack SHALL preserve protected logical capability `isomer-op-switch-identity` as member `identity` for switching a Project Operator's working posture to a selected Topic Actor or Agent.

#### Scenario: Protected bundle follows Imsight structure
- **WHEN** `operator/isomer-op-entrypoint/subskills/isomer-op-switch-identity` is inspected
- **THEN** it contains `SKILL.md` and `agents/openai.yaml`
- **AND** its folder and frontmatter retain logical id `isomer-op-switch-identity`
- **AND** its trigger description, numbered workflow, freeform fallback, and release version conform to current skill rules

#### Scenario: Command detail pages remain bounded
- **WHEN** the protected member exposes routines
- **THEN** it uses the Imsight collection-of-routines shape and links only required pages under `commands/`
- **AND** it does not create empty resource directories for symmetry

#### Scenario: Public identity route is used
- **WHEN** a user asks to switch identity posture
- **THEN** `$isomer-op-entrypoint use identity to <task>` invokes `isomer-op-entrypoint->identity`
- **AND** ordinary help does not advertise `$isomer-op-switch-identity` as a public skill
