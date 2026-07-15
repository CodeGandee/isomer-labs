## MODIFIED Requirements

### Requirement: Current-Template Skill Entrypoints
Every active packaged Isomer `SKILL.md` SHALL have frontmatter whose description starts with `Use when` and describes trigger conditions without replacing explicit manual-invocation limits. Each entrypoint SHALL contain `## Overview`, `## When to Use`, a near-top `## Workflow`, and exactly one negative-only `## Guardrails` section whose top-level bullets begin with `DO NOT`.

#### Scenario: Packaged entrypoint is inspected
- **WHEN** a manifest-declared `SKILL.md` is validated
- **THEN** its frontmatter and required sections match the current entrypoint template and its Guardrails contain only `DO NOT ...` bullets

#### Scenario: Manual-only skill description is normalized
- **WHEN** an existing skill permits only explicit invocation
- **THEN** its description starts with `Use when` while retaining that explicit-invocation condition and its agent metadata continues to disallow implicit invocation

### Requirement: Template Migration Preserves Skill Interfaces
Current-template migration SHALL preserve each skill's purpose, explicit trigger boundary, public subcommands, command and reference paths, callback insertion points, domain terminology, approval rules, output contracts, evidence requirements, and stop conditions unless a separate accepted requirement authorizes a behavior change. Positive operational guidance removed from Guardrails SHALL remain in Workflow, Procedure, Core Pattern, Contract, or another authoritative substantive section unless it duplicates guidance already present there.

#### Scenario: Old-template content is rewritten
- **WHEN** an entrypoint or subpage is migrated to negative-only Guardrails
- **THEN** the resulting edit changes instruction structure without renaming or weakening its public interface or behavioral contract

#### Scenario: Positive guardrail duplicates authoritative guidance
- **WHEN** a positive Guardrails bullet repeats complete guidance already present in an authoritative substantive section
- **THEN** the duplicate bullet is removed without creating another copy

### Requirement: Manifest-Aware Template Validation
The repository's system-skill validator SHALL enforce current-template entrypoint, workflow, negative-only Guardrails, troubleshooting, and active-scope requirements through the existing all-skills validation command and SHALL report file-specific diagnostics for each violation.

#### Scenario: Non-prohibition Guardrails bullet is introduced
- **WHEN** an active packaged skill page contains a top-level Guardrails bullet that does not begin with `DO NOT`
- **THEN** `pixi run validate-skills` fails with the affected file and negative-only Guardrails rule

#### Scenario: Excluded source copy retains historical wording
- **WHEN** an excluded provenance, migration, or passive-template file contains wording that would fail the active template
- **THEN** `pixi run validate-skills` does not report a template violation for that file
