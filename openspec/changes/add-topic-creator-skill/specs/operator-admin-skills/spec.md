## ADDED Requirements

### Requirement: Topic Creator Operator Skill Inventory
The operator/admin skillset SHALL include `isomer-admin-topic-creator` as the canonical user-facing skill for topic initialization to manual-research readiness.

#### Scenario: Topic creator skill is active
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-creator/` as an active operator skill folder

#### Scenario: Operator docs list topic creator first for topic initialization
- **WHEN** a developer reads `skillset/operator/README.md`
- **THEN** it lists `isomer-admin-topic-creator`
- **AND** it describes the skill as the front door for creating or preparing a Research Topic from empty or partial Project state to manual-research-ready Topic Workspace

#### Scenario: Operator validation covers topic creator
- **WHEN** operator skill validation runs
- **THEN** it validates the topic creator skill with the same frontmatter, UI metadata, local-reference, workflow, and naming checks used for other active operator skills

### Requirement: Deprecated Compatibility Operator Skills
The operator/admin skillset SHALL keep selected compatibility skills available while marking them deprecated for direct user invocation.

#### Scenario: Topic prepare is compatibility-only
- **WHEN** `isomer-admin-topic-prepare` is inspected
- **THEN** its frontmatter marks it deprecated for direct user invocation and names `isomer-admin-topic-creator` as its replacement
- **AND** operator documentation describes it as retained for compatibility and delegated common preparation

#### Scenario: Manual research session is compatibility-only
- **WHEN** `isomer-admin-manual-research-session` is inspected
- **THEN** its frontmatter marks it deprecated for direct user invocation and names `isomer-admin-topic-creator` as its replacement
- **AND** operator documentation describes it as retained for compatibility and delegated start-pack finalization

#### Scenario: Deprecated compatibility skills remain installable during transition
- **WHEN** the core operator skill group is installed
- **THEN** deprecated compatibility skills may remain installed with visible replacement guidance
- **AND** their presence does not make them the recommended front door for new topic initialization
