## ADDED Requirements

### Requirement: Entrypoint Operator Skill Inventory
The operator/admin skillset SHALL include `isomer-op-entrypoint` as the informed-user system-skill and CLI routing surface for Project Operator Sessions and Operator Agents.

#### Scenario: Entrypoint skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-op-entrypoint/` as an active operator skill folder
- **AND** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-op-entrypoint`

#### Scenario: Operator docs list entrypoint separately from welcome
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-op-entrypoint`
- **AND** it describes the skill as an informed-user dispatcher that indexes operator, service, misc, extension, and Isomer CLI surfaces
- **AND** it distinguishes `isomer-op-entrypoint` from `isomer-op-welcome`, which remains the read-only welcome menu and path chooser

#### Scenario: Active operator inventory includes entrypoint
- **WHEN** active operator inventory guidance is inspected
- **THEN** it contains `isomer-op-project-mgr`, `isomer-op-switch-identity`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, `isomer-op-topic-team-specialize`, `isomer-op-welcome`, and `isomer-op-entrypoint`
- **AND** it does not reintroduce retired or old admin compatibility names

#### Scenario: Operator validation covers entrypoint
- **WHEN** operator skill validation runs
- **THEN** it validates the entrypoint skill with frontmatter, UI metadata, local-reference, workflow, routing, output-contract, extension-index, CLI-index, service-boundary, retired-route, and global Isomer CLI invocation checks

#### Scenario: Entrypoint does not own specialized workflows
- **WHEN** entrypoint guidance routes Project lifecycle, Topic creation, initialized-topic management, identity switching, Topic Team Specialization, service setup, or DeepSci research-stage work
- **THEN** it names the owner skill or CLI family that owns the work
- **AND** it does not claim ownership of lower-level mutation that belongs to those surfaces
