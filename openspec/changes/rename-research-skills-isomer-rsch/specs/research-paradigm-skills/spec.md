## MODIFIED Requirements

### Requirement: Research Paradigm Skillset Layout
The project SHALL provide a reusable research-paradigm skillset under `skillset/research-paradigm/` using Codex skill folder layout and the `isomer-rsch-<purpose>` naming convention.

#### Scenario: Core skill folders exist
- **WHEN** the research-paradigm skillset is inspected
- **THEN** it contains `isomer-rsch-shared` and core research skill folders for intake, scout, baseline, idea, optimize, experiment, analysis, decision, finalize, write, review, rebuttal, paper-outline, paper-plot, figure-polish, and science

#### Scenario: Skill frontmatter is valid
- **WHEN** each extracted skill's `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields, and the `name` field matches the `isomer-rsch-<purpose>` folder name

#### Scenario: Skill manifest exists when a skill is packaged independently
- **WHEN** an extracted skill is packaged as a standalone skill bundle
- **THEN** it includes an `agents/openai.yaml` manifest with UI-facing metadata

#### Scenario: Standalone skill bundle is self-contained
- **WHEN** an extracted skill is packaged as a standalone skill bundle
- **THEN** its `SKILL.md` and directly linked references do not require files outside that skill's directory

#### Scenario: Old active skill names are removed
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** they do not use `isomer-labs-research-*` as active skill folder names, frontmatter names, manifests, or role mappings

### Requirement: Generic Agent Mapping
The team documentation SHALL map generic research agents to the extracted `isomer-rsch-*` skills without making the skills depend on one team topology.

#### Scenario: Generic role map exists
- **WHEN** the updated team documentation is inspected
- **THEN** it defines generic research roles and lists the `isomer-rsch-*` research-paradigm skills installed for each role

#### Scenario: Skill bundles are topology-neutral
- **WHEN** an extracted skill is inspected
- **THEN** it does not require a specific Houmao specialist name, mailbox route, gateway, credential, or agent topology to perform its research operation

### Requirement: Validation
The implementation SHALL include validation steps that check skill structure, naming consistency, and removal of runtime-specific coupling.

#### Scenario: Structural validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms each `isomer-rsch-*` skill folder has a `SKILL.md`, valid frontmatter, and expected supporting resources

#### Scenario: Naming validation runs
- **WHEN** the implementation is complete
- **THEN** validation confirms every renamed skill folder, `SKILL.md` frontmatter `name:`, manifest default prompt, and active role mapping uses `isomer-rsch-*`

#### Scenario: Coupling validation runs
- **WHEN** the implementation is complete
- **THEN** validation searches the research-paradigm skillset for DeepScientist-specific runtime terms, including continuation scheduling terms, and confirms any remaining matches are provenance or mapping text only

#### Scenario: Guessed concrete surfaces are checked
- **WHEN** the implementation is complete
- **THEN** validation searches for concrete DeepScientist-style paths, command wrappers, runner homes, and API calls, and confirms unsettled equivalents are marked `yet-to-be-determined`
