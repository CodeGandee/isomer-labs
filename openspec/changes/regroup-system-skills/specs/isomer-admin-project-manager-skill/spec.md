## MODIFIED Requirements

### Requirement: Project Manager Skill Bundle
The core public pack SHALL preserve a lean protected bundle with logical id `isomer-op-project-mgr` for Project initialization, inspection, validation, cleanup, relocation, and runtime preparation guidance.

#### Scenario: Protected bundle exists
- **WHEN** the core pack is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/subskills/isomer-op-project-mgr/SKILL.md` and `agents/openai.yaml`
- **AND** manifest member `project` maps to that logical id and path

#### Scenario: Frontmatter preserves logical identity
- **WHEN** the protected `SKILL.md` is inspected
- **THEN** its frontmatter contains `name: isomer-op-project-mgr`, a trigger-oriented description, and the standard invocation notation when object designators appear

#### Scenario: UI metadata is present
- **WHEN** the protected `agents/openai.yaml` is inspected
- **THEN** it contains display name, short description, release-aligned version, and a default prompt that routes ordinary users through `$isomer-op-entrypoint use project to <task>`

#### Scenario: Parent routes Project work
- **WHEN** a user asks the public core entrypoint for Project lifecycle work
- **THEN** it invokes `isomer-op-entrypoint->project` and preserves the Project Manager workflow

#### Scenario: Eval scaffolding is absent
- **WHEN** the protected bundle is inspected
- **THEN** it does not contain an `evals/` directory or auxiliary documentation that is not needed to execute the capability
