## Purpose

Define the current structural template and validation scope for active packaged Isomer system skills and their executable subpages.

## Requirements

### Requirement: Active Packaged Skill Scope
The system SHALL derive current-template conformance scope from every skill root declared in every group of the packaged system-skill manifest. The active scope SHALL include each declared `SKILL.md` and its active command, procedure, binding, scenario, and reference Markdown pages, while excluding immutable source provenance under `org/`, migration work under `migrate/`, and passive output material under `templates/`.

#### Scenario: Manifest group is audited
- **WHEN** template conformance validation reads the packaged system-skill manifest
- **THEN** it audits every declared core and extension skill root regardless of whether the group is always available

#### Scenario: Historical source copy is present
- **WHEN** a declared skill contains a copied upstream skill below `org/`, migration notes below `migrate/`, or passive output material below `templates/`
- **THEN** template conformance validation does not classify that material as active packaged skill instructions

### Requirement: Current-Template Skill Entrypoints
Every active packaged Isomer `SKILL.md` SHALL have frontmatter whose description starts with `Use when` and describes trigger conditions without replacing explicit manual-invocation limits. Each entrypoint SHALL contain `## Overview`, `## When to Use`, a near-top `## Workflow`, and exactly one `## Guardrails` section.

#### Scenario: Packaged entrypoint is inspected
- **WHEN** a manifest-declared `SKILL.md` is validated
- **THEN** its frontmatter and required sections match the current entrypoint template

#### Scenario: Manual-only skill description is normalized
- **WHEN** an existing skill permits only explicit invocation
- **THEN** its description starts with `Use when` while retaining that explicit-invocation condition and its agent metadata continues to disallow implicit invocation

### Requirement: Current-Template Workflows
Every active packaged skill entrypoint and executable subpage SHALL present `## Workflow` as ordered numbered steps, keep detailed branches in named detail sections or bounded nested lists, and end with a fallback that uses the agent's native planning tool when the request does not map cleanly to the default steps.

#### Scenario: Entrypoint workflow is validated
- **WHEN** validation inspects an active `SKILL.md`
- **THEN** the entrypoint has numbered workflow steps and a freeform fallback

#### Scenario: Executable subpage workflow is validated
- **WHEN** a parent skill routes a command or procedure to an active subpage, or an active subpage declares `## Workflow`
- **THEN** that page has numbered workflow steps and a freeform fallback

#### Scenario: Explanatory reference page is inspected
- **WHEN** an active reference page contains no routed command, procedure, or workflow
- **THEN** validation does not require artificial entrypoint or executable-workflow sections on that page

### Requirement: Template Migration Preserves Skill Interfaces
Current-template migration SHALL preserve each skill's purpose, explicit trigger boundary, public subcommands, command and reference paths, callback insertion points, domain terminology, approval rules, output contracts, evidence requirements, and stop conditions unless a separate accepted requirement authorizes a behavior change.

#### Scenario: Old-template content is rewritten
- **WHEN** an entrypoint or subpage is migrated to the current template
- **THEN** the resulting edit changes instruction structure without renaming or weakening its public interface or behavioral contract

### Requirement: Manifest-Aware Template Validation
The repository's system-skill validator SHALL enforce current-template entrypoint, workflow, Guardrails, troubleshooting, and active-scope requirements through the existing all-skills validation command and SHALL report file-specific diagnostics for each violation.

#### Scenario: Old-template section is introduced
- **WHEN** an active packaged skill page introduces a prohibited old-template heading or malformed current-template section
- **THEN** `pixi run validate-skills` fails with the affected file and rule

#### Scenario: Excluded source copy retains historical wording
- **WHEN** an excluded provenance, migration, or passive-template file contains wording that would fail the active template
- **THEN** `pixi run validate-skills` does not report a template violation for that file
