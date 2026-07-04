## MODIFIED Requirements

### Requirement: Operator Skillset Layout
The repository SHALL provide Project Operator Session and Operator Agent skills under `skillset/operator/` using the `isomer-op-<purpose>` naming convention.

#### Scenario: Operator skill folders exist
- **WHEN** the operator skillset is inspected
- **THEN** it contains active skill folders for project awareness, service request routing, template inspection, topic context resolution, placeholder reconciliation, topic profile drafting, profile review and approval, profile materialization, and team launch orchestration
- **AND** it does not contain an active `isomer-op-houmao-interop` folder

#### Scenario: Operator skill names are consistent
- **WHEN** an operator skill folder is inspected
- **THEN** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use the same `isomer-op-<purpose>` skill name

#### Scenario: Operator skillset is documented
- **WHEN** a developer reads skillset documentation
- **THEN** it identifies `skillset/operator/` as the installation source for Project Operator Session and Operator Agent skills and lists the supported `isomer-op-*` skills
- **AND** it does not list `isomer-op-houmao-interop` as a user-facing operator owner skill

#### Scenario: Houmao interop is routed to service
- **WHEN** operator guidance describes Houmao loop, runtime, launch profile, mailbox, gateway, or template-mapping support
- **THEN** it routes bounded support to `isomer-srv-houmao-interop`
- **AND** it keeps the visible first command on the appropriate user-facing operator workflow such as `isomer-op-project-mgr` or `isomer-op-topic-team-specialize`

### Requirement: Operator Skill Validation
The repository SHALL validate operator skill structure, command surfaces, and naming separately from research-paradigm and service skill validation.

#### Scenario: Operator validation checks structure
- **WHEN** the operator skill validation runs
- **THEN** it confirms each `skillset/operator/isomer-op-*` folder has a valid `SKILL.md`, valid frontmatter, expected manifest metadata, and directly linked local references when present
- **AND** it does not require or accept `skillset/operator/isomer-op-houmao-interop` as part of the active operator inventory

#### Scenario: Operator validation checks old active names
- **WHEN** the operator skill validation scans active docs, team profiles, fixtures, and skill manifests
- **THEN** it fails if a migrated operator skill is still referenced by its old active `isomer-deepsci-*` name outside historical provenance or archived change text
- **AND** it fails if current operator guidance presents `isomer-op-houmao-interop` as an active invokable skill outside historical provenance or migration-only text

#### Scenario: Repository skill validation covers operator skills
- **WHEN** a developer or agent runs the repository skill validation command
- **THEN** validation covers the research, operator, service, and misc skillsets or clearly prints the separate commands required to validate each skillset

#### Scenario: Operator validation checks Topic Creator finalization surface
- **WHEN** operator skill validation scans `skillset/operator/isomer-op-topic-creator`
- **THEN** it requires local `references/finalize.md`, `references/step-by-step.md`, and `references/run-to.md` subcommand pages, user-facing command guidance for `finalize`, `step-by-step`, and `run-to`, and references to `topic.workspace.summary`
- **AND** it rejects active Topic Creator command guidance that lists `start-manual-research` as a subcommand
- **AND** it rejects terminal Topic Creator guidance that includes next-step routing, manual research start-pack handoff, or production DeepSci research skill recommendations

#### Scenario: Operator validation checks Topic Creator guided execution
- **WHEN** operator skill validation scans Topic Creator `step-by-step` guidance
- **THEN** it requires wording that the subcommand follows the same main workflow order as `fast-forward`
- **AND** it requires per-step preview, option table, recommended choice, open question, and user acknowledgement guidance
- **AND** it fails if `step-by-step` can mutate a workflow step before user acknowledgement

#### Scenario: Operator validation checks Topic Creator run-to execution
- **WHEN** operator skill validation scans Topic Creator `run-to` guidance
- **THEN** it requires wording that the subcommand accepts a procedural subcommand target and follows the same readiness ladder as `fast-forward`
- **AND** it requires target exclusion by default, explicit inclusive execution behavior, invalid-target diagnostics, and missing-input blocker behavior
- **AND** it fails if `run-to` accepts helper, misc, unknown, or non-main-workflow targets as executable targets
