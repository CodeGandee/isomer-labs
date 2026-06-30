# skill-output-contracts Specification

## Purpose
Defines the shared Essential Output and Complete Output convention for non-research-paradigm skills.

## Requirements

### Requirement: Skills Split Output Contracts by Audience
Non-research-paradigm skills SHALL define output contracts with separate Essential Output and Complete Output sections.

#### Scenario: Essential and complete sections are present
- **WHEN** a skill outside `skillset/research-paradigm/*` has an output contract
- **THEN** the output contract includes an `Essential Output` section for default user-facing chat output
- **AND** it includes a `Complete Output` section for full handoff, audit, debug, or JSON-oriented detail

#### Scenario: Research paradigm skills are excluded
- **WHEN** a skill is under `skillset/research-paradigm/*`
- **THEN** this split-output requirement does not apply to that skill
- **AND** its research evidence reporting conventions remain governed by research-paradigm skill requirements

### Requirement: Essential Output Is the Default Chat Report
Skills SHALL print Essential Output by default when reporting to the chat session.

#### Scenario: Default output is concise
- **WHEN** a user invokes a skill without asking for complete output
- **THEN** the skill reports only the essential user-facing fields needed to understand the result
- **AND** those fields include status, what happened, important paths or refs, readiness or validation result when relevant, blockers, and next action when applicable

#### Scenario: Bookkeeping stays out of default output
- **WHEN** a default chat report is produced
- **THEN** semantic path diagnostics, storage profiles, provenance refs, full command logs, full readiness matrices, and complete evidence payloads are omitted unless they are essential to explain a blocker or user-facing result

#### Scenario: Complete output availability is discoverable
- **WHEN** important handoff or audit detail is omitted from Essential Output
- **THEN** the skill tells the user that Complete Output is available on request

### Requirement: Complete Output Is Available on Request
Skills SHALL print Complete Output when the user explicitly requests complete or audit-oriented output.

#### Scenario: Natural language requests trigger complete output
- **WHEN** the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output
- **THEN** the skill reports the Complete Output fields
- **AND** it may still start with a short Essential Output summary before the complete details

#### Scenario: Complete output preserves handoff detail
- **WHEN** Complete Output is requested
- **THEN** the skill includes all fields needed by downstream operators or services to reconstruct the run, including relevant semantic labels, path diagnostics, evidence, command logs, mutation summaries, blockers, warnings, and next action

### Requirement: Complete Output Is Grouped by Purpose
Complete Output SHALL be grouped by purpose instead of being a single unstructured list of bookkeeping fields.

#### Scenario: Complete fields are grouped
- **WHEN** a skill documents Complete Output
- **THEN** it groups fields into readable categories such as identity, paths, readiness, operations, mutations, diagnostics, and next action
- **AND** it keeps field names available for machine-readable handoff where needed

#### Scenario: Essential output remains human-first
- **WHEN** a skill documents Essential Output
- **THEN** it uses concise labels that help the user understand what happened
- **AND** it avoids exposing low-level storage-profile or path-source detail unless that detail is the result or blocker the user needs to see
