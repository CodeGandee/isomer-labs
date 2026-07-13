## MODIFIED Requirements

### Requirement: Research-Paradigm Validation Supports Kaoju
The research-paradigm validation harness SHALL validate Kaoju through family-specific rules while preserving all existing DeepSci checks.

#### Scenario: Valid Kaoju family passes validation
- **WHEN** the validator inspects the complete production Kaoju family
- **THEN** it accepts the exact twelve-skill inventory, valid frontmatter and manifests, near-top workflows, supported command inventory including `paper-pass` and `create-paper-template`, self-contained direct references, registered artifact bindings, and canonical namespace

#### Scenario: Invalid Kaoju family reports deterministic diagnostics
- **WHEN** a Kaoju skill is missing, uses the wrong namespace, has manifest identity drift, references a missing local file, hardcodes a local or provider-specific runtime path, exposes an unapproved procedure, or names an unbound publication output
- **THEN** validation fails with a deterministic diagnostic that names the file, line when available, and violated Kaoju rule

#### Scenario: Shared checks do not erase family-specific checks
- **WHEN** common frontmatter, manifest, reference, CLI-spelling, terminology, document-build, or publication-output checks are refactored for multiple families
- **THEN** DeepSci retains its inventory, placeholder, source-lineage, structured-output, and other existing family-specific validation
- **AND** the existing DeepSci validation tests continue to pass unchanged in meaning

#### Scenario: Validator tests cover Kaoju active and invalid zones
- **WHEN** unit tests exercise family-aware research-paradigm validation
- **THEN** they include valid Kaoju fixtures and failures for missing inventory, wrong namespace, manifest mismatch, broken direct references, stale domain terms, hard-coded provider or local paths, procedural-command drift, missing paper bindings, forbidden direct publication state, Markdown-to-PDF publication guidance, manually numbered LaTeX headings, and unrecorded engine fallback
- **AND** they retain regression fixtures for valid and invalid DeepSci material
