## MODIFIED Requirements

### Requirement: Kaoju Ships Checked Packaged Writing-Template Defaults
Kaoju SHALL package immutable role-local `content/main` and `latex/main` template trees that pass the same applicable integrity and authored-metadata validation as topic-owned named stock, and the packaged `latex/main` SHALL contain the complete IEEE Transactions two-column tree adopted from the Predictive Memory Survey.

#### Scenario: Packaged defaults are validated
- **WHEN** package resources or the Kaoju contract are validated
- **THEN** validation checks exactly one content `main` tree and one LaTeX `main` tree for safe paths, reserved-file exclusion, deterministic digest, resource version, and role-specific metadata
- **AND** the LaTeX tree also passes entrypoint, composition-contract, build-profile, venue-provenance, license-posture, and required-tree-member validation

#### Scenario: Packaged content default is inspected
- **WHEN** an actor or service inspects the packaged content default
- **THEN** it finds a generic MyST-oriented survey-paper scaffold with checked entrypoint and use guidance
- **AND** the package does not encode a topic-specific evidence claim, Direction Set, Survey Contract, or publication venue

#### Scenario: Packaged LaTeX default is inspected
- **WHEN** an actor or service inspects the packaged LaTeX default
- **THEN** it finds the marker-based IEEE Transactions journal entrypoint derived from `bare_jrnl_new_sample4.tex` with `\documentclass[lettersize,journal]{IEEEtran}`
- **AND** authored metadata identifies the IEEE Transactions venue, checked composition contract, build profile, source archive provenance, and LPPL 1.3 posture

#### Scenario: Packaged IEEE style tree is consumed
- **WHEN** topic initialization, default export, or paper-local TeX initialization copies packaged `latex/main`
- **THEN** the copied managed tree includes the entrypoint, local `IEEEtran.cls`, retained upstream sample, referenced sample asset, and source metadata with their checked bytes
- **AND** selection and composition do not read the source ZIP, `tmp/`, another Topic Workspace, or a host-installed IEEE class in place of the vendored tree

#### Scenario: Packaged default is invalid
- **WHEN** a packaged default is missing, unsafe, digest-inconsistent, or invalid for its selected role
- **THEN** topic initialization and fallback for that role block with a stable package-resource diagnostic
- **AND** the system does not substitute an embedded string, another role, a topic from another workspace, or an unmanaged repository file
