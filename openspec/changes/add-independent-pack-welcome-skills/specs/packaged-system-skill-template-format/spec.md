## MODIFIED Requirements

### Requirement: Active Packaged Skill Scope
The system SHALL derive current-template conformance scope from every public welcome, public entrypoint, and protected subskill declared by the packaged system-skill manifest.

#### Scenario: Manifest pack is audited
- **WHEN** template conformance validation reads manifest v4
- **THEN** it audits every declared public skill and every protected subskill regardless of whether the pack is core or optional
- **AND** it does not infer active scope only from the designated entrypoint

#### Scenario: Public welcome resources are audited
- **WHEN** a welcome skill owns active command or reference pages
- **THEN** validation classifies those pages as active newcomer guidance
- **AND** it validates them independently from the sibling entrypoint's resources

#### Scenario: Historical or passive material is present
- **WHEN** a declared skill contains provenance under `org/`, migration notes under `migrate/`, or passive output material under `templates/`
- **THEN** template conformance validation does not classify that material as active packaged skill instructions

### Requirement: Manifest-Aware Template Validation
The repository SHALL validate public skill roles, protected nesting, and role-specific formatting from the packaged manifest rather than a hard-coded skill inventory.

#### Scenario: Manifest public record drives validation
- **WHEN** a public skill record has role `welcome`
- **THEN** validation applies common skill structure plus the welcome teaching, command-map, read-only, and handoff rules
- **AND** it does not require the route-and-proceed execution contract

#### Scenario: Entrypoint record drives validation
- **WHEN** a public skill record has role `entrypoint`
- **THEN** validation applies route-and-proceed, protected inventory, public command, callback, and invocation-notation rules
- **AND** it does not require copied welcome teaching resources

#### Scenario: Protected record drives validation
- **WHEN** a protected capability record is encountered
- **THEN** validation recursively inspects its frontmatter, workflow, local resources, parent invocation designator, dependencies, and version
- **AND** it rejects a protected member that is also projected as an undeclared public skill

## ADDED Requirements

### Requirement: Welcome Skills Use a Newcomer Teaching Format
Every public welcome `SKILL.md` SHALL use a concise progressive-disclosure format that introduces typical use cases before exhaustive command detail.

#### Scenario: Welcome entrypoint is inspected
- **WHEN** a public welcome `SKILL.md` is inspected
- **THEN** it contains `## Overview`, `## When to Use`, a near-top numbered `## Workflow`, a typical-use-case surface, a complete command-map route, an output contract, and exactly one negative-only `## Guardrails`
- **AND** it links only the selected one-level command or reference resources needed for each route

#### Scenario: Typical use-case table is inspected
- **WHEN** a welcome use-case table or equivalent structured section is inspected
- **THEN** every row has a one-sentence use condition, representative routing cues, required context, canonical entrypoint route, exact example, expected action, mutation posture, and next step
- **AND** the prose is adapted to the welcome context instead of duplicating source metadata verbatim

#### Scenario: Complete map follows progressive disclosure
- **WHEN** a welcome skill documents the sibling entrypoint's full command inventory
- **THEN** the exhaustive map is loaded only through `show-command-map`, `help`, or an explicit complete-output request
- **AND** default welcome output remains a concise selection of high-value patterns
