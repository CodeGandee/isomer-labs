## MODIFIED Requirements

### Requirement: Operator Admin Skillset Layout
The repository SHALL provide Project Operator Session and Operator Agent skills under `skillset/operator/` using the `isomer-op-<purpose>` naming convention.

#### Scenario: Operator skill folders exist
- **WHEN** the operator skillset is inspected
- **THEN** it contains active skill folders for Project lifecycle management, topic creation, initialized-topic management, Topic Team Specialization, and welcome routing
- **AND** each active operator skill folder uses an `isomer-op-<purpose>` name
- **AND** it does not contain an active `isomer-op-houmao-interop` folder

#### Scenario: Operator skill names are consistent
- **WHEN** an operator skill folder is inspected
- **THEN** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use the same `isomer-op-<purpose>` skill name

#### Scenario: Operator skillset is documented
- **WHEN** a developer reads skillset documentation
- **THEN** it identifies `skillset/operator/` as the installation source for Project Operator Session and Operator Agent skills
- **AND** it lists the supported `isomer-op-*` skills instead of `isomer-admin-*` skills
- **AND** it routes bounded Houmao interop support to `isomer-srv-houmao-interop` instead of listing a Houmao interop operator owner skill

### Requirement: Operator Skill Validation
The repository SHALL validate operator skill structure, command surfaces, and naming separately from research-paradigm skill validation.

#### Scenario: Operator validation checks structure
- **WHEN** the operator skill validation runs
- **THEN** it confirms each `skillset/operator/isomer-op-*` folder has a valid `SKILL.md`, valid frontmatter, expected manifest metadata, and directly linked local references when present

#### Scenario: Operator validation checks old active names
- **WHEN** the operator skill validation scans active docs, team profiles, fixtures, and skill manifests
- **THEN** it fails if a current operator skill is still referenced by an old active `isomer-admin-*` or `isomer-rsch-*` name outside historical provenance, migration notes, source copies, or archived change text

#### Scenario: Repository skill validation covers operator skills
- **WHEN** a developer or agent runs the repository skill validation command
- **THEN** validation covers the research, operator, service, and misc skillsets or clearly prints the separate commands required to validate each skillset

#### Scenario: Operator validation checks Topic Creator finalization surface
- **WHEN** operator skill validation scans `skillset/operator/isomer-op-topic-creator`
- **THEN** it requires local `references/finalize.md`, `references/step-by-step.md`, and `references/run-to.md` subcommand pages, user-facing command guidance for `finalize`, `step-by-step`, and `run-to`, and references to `topic.workspace.summary`
- **AND** it rejects active Topic Creator command guidance that lists `start-manual-research` as a subcommand
- **AND** it rejects terminal Topic Creator guidance that includes next-step routing, manual research start-pack handoff, or production DeepSci research skill recommendations

## ADDED Requirements

### Requirement: Operator Namespace Rename Inventory
The operator skillset SHALL expose the renamed active operator inventory without duplicate active compatibility wrappers.

#### Scenario: Active operator inventory uses op names
- **WHEN** the operator skillset is inspected
- **THEN** it contains `isomer-op-project-mgr`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, `isomer-op-topic-team-specialize`, and `isomer-op-welcome`
- **AND** it does not contain active `isomer-admin-project-mgr`, `isomer-admin-topic-creator`, `isomer-admin-topic-mgr`, `isomer-admin-topic-team-specialize`, `isomer-admin-welcome`, or `isomer-admin-houmao-interop` folders
- **AND** it does not contain active `isomer-op-houmao-interop`

#### Scenario: Active routing uses op names
- **WHEN** active operator guidance routes between operator skills
- **THEN** it invokes the renamed `isomer-op-*` skill names
- **AND** it routes bounded Houmao interop support to `isomer-srv-houmao-interop`
- **AND** it treats old `isomer-admin-*` names as historical or migration-only references
