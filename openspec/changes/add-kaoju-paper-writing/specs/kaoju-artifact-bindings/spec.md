## ADDED Requirements

### Requirement: Kaoju Paper Writing Uses Bound Publication Records
The Kaoju artifact semantic registry and producer binding inventory SHALL define complete storage-neutral semantics and physical bindings for every accepted paper-writing record.

#### Scenario: Paper semantic inventory is complete
- **WHEN** the shared semantic registry and `isomer-kaoju-write/artifact-bindings.md` are inspected
- **THEN** they define `kaoju:paper-contract`, `kaoju:survey-manuscript`, `kaoju:paper-build-run`, `kaoju:paper-validation-report`, and `kaoju:publication-bundle`
- **AND** each semantic id has one producer, meaning, required content, consumers, update intent, storage item, record kind, semantic label, family-neutral profile, lineage policy, revision policy, query metadata, and lifecycle command shape

#### Scenario: Paper files remain referenced
- **WHEN** paper writing produces `.tex`, bibliography, LaTeX style or included source, figure, table, build log, page preview, or PDF files
- **THEN** canonical JSON records reference those files through accepted file refs and Provenance Records
- **AND** the files follow worker-output policy and are not treated as canonical survey state or embedded wholesale in structured payloads

#### Scenario: Publication manuscript binding identifies LaTeX inputs
- **WHEN** a `kaoju:survey-manuscript` or `kaoju:paper-build-run` is accepted
- **THEN** its bindings identify the `.tex` entry point, document class or template, bibliography, style, figure, table, and included source refs used by the build
- **AND** no Markdown file or Markdown-to-PDF command is bound as the accepted publication manuscript or publication build path

#### Scenario: Build and validation attempts preserve history
- **WHEN** a manuscript is rebuilt, repaired, or revalidated
- **THEN** each `kaoju:paper-build-run` and `kaoju:paper-validation-report` is a separate descendant of the exact manuscript and prior attempt when applicable
- **AND** revision does not erase failed builds, rejected validation, warnings, commands, logs, or output digests

## MODIFIED Requirements

### Requirement: Kaoju Binding Inventory Covers Core Survey Objects
The production Kaoju binding inventory SHALL cover every core durable object required by its procedures and helpers.

#### Scenario: Core semantic inventory is present
- **WHEN** the shared registry and binding pages are inspected
- **THEN** they cover workspace readiness, Survey Contract, Comparison Intent Document, Proceed Decision, Discovery Ledger, Related-Work Catalog and its deltas, curated intake delta, Source Digest, Source Access Blocker, Claim-Evidence Ledger, material acquisition, Topic Dataset Manifest, Generated Dataset, Method Trial, theory comparison, Comparison Matrix, Audit Report, Claim Status Table, Field Summary, Kaoju Dossier, paper contract, survey manuscript, paper-build Runs, paper validation reports, publication bundle, terminal report, method-trial Runs, and comparison Runs

#### Scenario: New durable output needs a disposition
- **WHEN** a later Kaoju skill adds an accepted durable output
- **THEN** it adds a semantic registry entry, binding row, and family-neutral profile or records an explicit non-structured binding disposition
- **AND** validation rejects an undocumented implicit storage choice
