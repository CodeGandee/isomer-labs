## ADDED Requirements

### Requirement: Production Kaoju Research-Paradigm Layout
The research-paradigm asset tree SHALL document and package Kaoju as a production family alongside DeepSci without changing DeepSci's active layout.

#### Scenario: Research-paradigm documentation lists both families
- **WHEN** `src/isomer_labs/assets/system_skills/research-paradigm/README.md` is inspected
- **THEN** it identifies `deepsci/` and `kaoju/` as separate optional domain-extension families
- **AND** it describes Kaoju as evidence-led survey work rather than hypothesis-driven new-method research

#### Scenario: Kaoju active surface is concise and self-contained
- **WHEN** a production Kaoju skill directory is inspected
- **THEN** active execution guidance is limited to `SKILL.md`, `agents/openai.yaml`, and directly useful local `commands/`, `references/`, `assets/`, or `scripts/`
- **AND** it does not require feature-design files, archived OpenSpec changes, external source checkouts, local absolute paths, or provider-specific credentials at runtime

#### Scenario: Kaoju skills use canonical Isomer language
- **WHEN** active Kaoju guidance names platform concepts
- **THEN** it uses Research Topic, Research Inquiry, Topic Workspace, Artifact, Evidence Item, Run, Finding, Decision Record, Gate, Provenance Record, and Workspace Path Resolution consistently
- **AND** it does not introduce a Kaoju-specific runtime database or lifecycle vocabulary

### Requirement: Research-Paradigm Validation Supports Kaoju
The research-paradigm validation harness SHALL validate Kaoju through family-specific rules while preserving all existing DeepSci checks.

#### Scenario: Valid Kaoju family passes validation
- **WHEN** the validator inspects the complete production Kaoju family
- **THEN** it accepts the exact eleven-skill inventory, valid frontmatter and manifests, near-top workflows, supported command inventory, self-contained direct references, and canonical namespace

#### Scenario: Invalid Kaoju family reports deterministic diagnostics
- **WHEN** a Kaoju skill is missing, uses the wrong namespace, has manifest identity drift, references a missing local file, hardcodes a local or provider-specific runtime path, or exposes an unapproved procedure
- **THEN** validation fails with a deterministic diagnostic that names the file, line when available, and violated Kaoju rule

#### Scenario: Shared checks do not erase family-specific checks
- **WHEN** common frontmatter, manifest, reference, CLI-spelling, or terminology checks are refactored for multiple families
- **THEN** DeepSci retains its inventory, placeholder, source-lineage, structured-output, and other existing family-specific validation
- **AND** the existing DeepSci validation tests continue to pass unchanged in meaning

#### Scenario: Validator tests cover Kaoju active and invalid zones
- **WHEN** unit tests exercise family-aware research-paradigm validation
- **THEN** they include valid Kaoju fixtures and failures for missing inventory, wrong namespace, manifest mismatch, broken direct references, stale domain terms, hard-coded provider or local paths, and procedural-command drift
- **AND** they retain regression fixtures for valid and invalid DeepSci material
