## MODIFIED Requirements

### Requirement: Research Paradigm Skillset Layout
The project SHALL provide a reusable research-paradigm skillset under `skillset/research-paradigm/` using Codex skill folder layout and the `isomer-rsch-<purpose>` naming convention for research-stage method skills only.

#### Scenario: Core skill folders exist
- **WHEN** the research-paradigm skillset is inspected
- **THEN** it contains `isomer-rsch-shared` and core research skill folders for intake, scout, baseline, idea, optimize, experiment, analysis, decision, finalize, write, review, rebuttal, paper-outline, paper-plot, figure-polish, and science

#### Scenario: Skill frontmatter is valid
- **WHEN** each extracted research-stage skill's `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields, and the `name` field matches the `isomer-rsch-<purpose>` folder name

#### Scenario: Skill manifest exists when a skill is packaged independently
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** it includes an `agents/openai.yaml` manifest with UI-facing metadata

#### Scenario: Standalone skill bundle is self-contained
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** its `SKILL.md` and directly linked references do not require files outside that skill's directory

#### Scenario: Old active skill names are removed
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** they do not use `isomer-labs-research-*` as active skill folder names, frontmatter names, manifests, or role mappings

#### Scenario: Operator admin skills are excluded
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** Project Operator Session and Operator Agent orchestration skills are not stored or named as `isomer-rsch-*` skills and instead use the operator admin skillset

## ADDED Requirements

### Requirement: Research Paradigm Skillset References Operator Skills by Boundary
Research-paradigm documentation SHALL distinguish research-stage skills from operator/admin skills instead of presenting Project Operator Session orchestration as research method.

#### Scenario: Research docs point to operator skillset
- **WHEN** research-paradigm README or role mapping documentation mentions project operation, Topic Team Specialization orchestration, Service Request routing, profile materialization, approval, or team launch
- **THEN** it points to the `isomer-admin-*` operator skillset rather than listing those capabilities as `isomer-rsch-*` research-stage skills

#### Scenario: Research role mappings avoid admin skills
- **WHEN** generic research agent role mappings are inspected
- **THEN** ordinary research roles such as scout, baseline, experiment, analysis, writer, reviewer, or synthesis reviewer do not install `isomer-admin-*` skills unless the role is explicitly an Operator Agent role
