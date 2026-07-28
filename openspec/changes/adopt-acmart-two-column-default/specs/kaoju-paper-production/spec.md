## MODIFIED Requirements

### Requirement: Kaoju Ships Checked Packaged Writing-Template Defaults
Kaoju SHALL package immutable role-local `content/main` and `latex/main` template trees that pass the same applicable integrity and authored-metadata validation as topic-owned named stock, and the packaged `latex/main` SHALL contain the pinned ACM `acmart` two-column source tree selected for neutral survey presentation.

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
- **THEN** it finds a marker-based entrypoint derived from the pinned ACM `sigconf` sample with `\documentclass[sigconf,nonacm]{acmart}`
- **AND** authored metadata identifies venue `acm-sigconf`, marker composition, the Tectonic build profile, exact archive and commit provenance, and LPPL posture
- **AND** it omits fabricated ACM rights, DOI, conference, ISBN, CCS, affiliation, and researcher-identity metadata

#### Scenario: Packaged ACM style tree is consumed
- **WHEN** topic initialization, default export, or paper-local TeX initialization copies packaged `latex/main`
- **THEN** the copied managed tree includes the marker entrypoint, local `acmart.cls`, required `.dtx` sources, bibliography support, retained upstream `sigconf` sample, source metadata, license, and their checked bytes
- **AND** it excludes generated documentation PDFs, generated sample PDFs, Git configuration, and Git metadata
- **AND** selection and composition do not read the source ZIP, `tmp/`, another Topic Workspace, or a host-installed ACM class in place of the vendored tree

#### Scenario: ACM venue stock is validated
- **WHEN** packaged or topic-owned LaTeX stock declares venue `acm-sigconf`
- **THEN** venue validation requires document class `acmart` and title, author, abstract, and keywords constructs in the complete entrypoint
- **AND** a wrong class or missing required construct blocks stock acceptance with a stable diagnostic

#### Scenario: Existing topic stock changes venue
- **WHEN** an actor updates existing topic-owned LaTeX stock with a replacement tree and replacement authored metadata under the current state token
- **THEN** the service validates the tree against the replacement metadata
- **AND** commits both atomically or commits neither

#### Scenario: Packaged default is invalid
- **WHEN** a packaged default is missing, unsafe, digest-inconsistent, or invalid for its selected role
- **THEN** topic initialization and fallback for that role block with a stable package-resource diagnostic
- **AND** the system does not substitute an embedded string, another role, a topic from another workspace, or an unmanaged repository file

#### Scenario: Existing topic stock and paper history remain stable
- **WHEN** a Kaoju release changes the packaged LaTeX default
- **THEN** valid existing topic-owned `latex/main` stock, template snapshots, TeX drafts, build runs, and PDFs remain unchanged
- **AND** adopting the new default into an existing topic requires an explicit state-checked template update and creates new derived paper artifacts
