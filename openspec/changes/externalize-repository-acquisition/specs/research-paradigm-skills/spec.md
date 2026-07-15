## MODIFIED Requirements

### Requirement: Research-Paradigm Validation Supports Kaoju
The research-paradigm validation harness SHALL validate the fourteen-skill Kaoju survey-process family through family-specific rules while preserving all existing DeepSci checks.

#### Scenario: Valid Kaoju family passes validation
- **WHEN** the validator inspects the complete production Kaoju family
- **THEN** it accepts the exact fourteen-skill inventory, valid frontmatter and manifests, near-top workflows, approved survey-intent and compatibility command inventory, self-contained direct references, canonical namespace, binding-registry use, and external-acquisition followed by semantic-registration guidance

#### Scenario: Invalid Kaoju family reports deterministic diagnostics
- **WHEN** a Kaoju skill is missing, uses the wrong namespace, has manifest identity drift, references a missing local file, hardcodes a local or provider-specific runtime path, scans for durable records, repeats a physical binding as independent authority, invokes an unregistered executable path other than an authorized external repository command, routes repository acquisition through `isomer-cli` or an Isomer execution request, registers before verification, treats Markdown or TeX as canonical paper content, invokes the external wiki skill, mutates Pixi state directly, or exposes an unapproved procedure
- **THEN** validation fails with a deterministic diagnostic that names the file, line when available, skill, semantic id when applicable, and violated Kaoju rule

#### Scenario: Shared checks do not erase family-specific checks
- **WHEN** common frontmatter, manifest, reference, CLI-spelling, terminology, repository-boundary, or binding checks are refactored for multiple families
- **THEN** DeepSci retains its inventory, artifact-identity, source-lineage, structured-output, and other existing family-specific validation
- **AND** the existing DeepSci validation tests continue to pass unchanged in meaning

#### Scenario: Validator tests cover Kaoju active and invalid zones
- **WHEN** unit tests exercise family-aware research-paradigm validation
- **THEN** they include valid Kaoju fixtures and failures for missing inventory, wrong namespace, manifest mismatch, broken direct references, stale domain terms, hard-coded provider or local paths, procedural-command drift, binding drift, directory scanning, canonical-format violations, external wiki routing, direct environment mutation, Isomer-owned repository acquisition, and pre-verification registration
- **AND** they retain regression fixtures for valid and invalid DeepSci material

### Requirement: Kaoju Skills Separate Research Judgment from Deterministic Operations
Production Kaoju skills SHALL make research and human-interaction decisions, SHALL delegate deterministic Isomer state operations to typed CLI and owner services, and SHALL execute repository commands through the acting agent's external command surface.

#### Scenario: Skill performs research judgment
- **WHEN** a procedure selects a direction, appraises a source, forms or qualifies a claim, audits evidence, writes paper prose, interprets code, repairs TeX semantics, selects a repository acquisition method, or recommends a trial design
- **THEN** the responsible Kaoju capability skill performs and records that judgment with evidence and actor provenance

#### Scenario: Skill needs deterministic Isomer mutation
- **WHEN** the procedure persists an artifact, resolves or registers a managed path, exports or applies a template, initializes a conversion, dispatches environment support, executes a trial, builds a PDF, exports a wiki, deploys a viewer, or launches a managed process
- **THEN** it invokes the applicable typed CLI or owner service and consumes returned durable refs
- **AND** it does not substitute prose instructions for a missing deterministic Isomer contract

#### Scenario: Skill needs repository acquisition
- **WHEN** the procedure needs to clone, fetch, copy, check out, deepen, repair, or inspect source-control state to obtain a repository
- **THEN** the acting agent runs user-supplied or task-appropriate commands outside Isomer APIs under the applicable authorization
- **AND** it uses typed Isomer operations only to plan a semantic target, register the verified existing path, and record Artifacts, provenance, checkpoints, or blockers
