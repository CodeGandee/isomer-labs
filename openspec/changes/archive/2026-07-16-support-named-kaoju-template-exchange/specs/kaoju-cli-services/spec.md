## MODIFIED Requirements

### Requirement: Kaoju Paper Commands Are Deterministic Transformations
The CLI SHALL provide low-level `ext kaoju paper template` CRUD, exact named copy and replacement, export inspection, safe export, integrity validation, and state-token concurrency while leaving arbitrary template construction and merge decisions to Kaoju skills.

#### Scenario: Named templates are listed or shown
- **WHEN** `template list` or `template show` runs
- **THEN** the CLI queries the flat named-template namespace and returns stable ref, name, current tree digest, state token, status, authored metadata, and resolved default working path
- **AND** it exposes no snapshot classification or automatic revision history

#### Scenario: Template is created from prepared content
- **WHEN** `template create --name <name> --from <path>` receives a new path-safe name and integrity-valid prepared tree
- **THEN** it creates the stable named record, managed directory content, state token, and audit event
- **AND** it does not infer the tree's high-level template meaning

#### Scenario: Named template is copied explicitly
- **WHEN** `template create --name <new> --from-template <existing>` runs
- **THEN** the CLI creates an ordinary independent named template with exact source tree and allowed metadata
- **AND** it does not mark, list, retain, or manage the new name as a snapshot

#### Scenario: Prepared content updates mutable state
- **WHEN** `template update --name <name> --from <path> --expected-state <token>` receives valid low-level inputs
- **THEN** it atomically replaces current content in the stable named record and emits before-and-after digest provenance
- **AND** it does not create a superseding template-content record or preserve prior bytes by contract

#### Scenario: Known named template replaces target
- **WHEN** `template update --name <target> --from-template <source> --expected-state <token>` runs
- **THEN** the CLI copies exact source content and applicable metadata to the stable target and returns its new state token
- **AND** it performs no merge and leaves the source unchanged

#### Scenario: File and metadata CRUD remain low level
- **WHEN** `template file put`, `template file remove`, or `template metadata patch` receives a safe target, current token, and authorized input
- **THEN** the CLI atomically changes only the selected content or allowed authored metadata and recalculates managed state
- **AND** it rejects changes to service-controlled identity, scope, binding, digest, token, and audit fields

#### Scenario: Stale state is rejected
- **WHEN** any update, file edit, metadata patch, archive, or delete receives a stale state token
- **THEN** the CLI returns current-state diagnostics without mutation
- **AND** the caller must re-read before retrying

#### Scenario: Template removal is reference safe
- **WHEN** a caller archives or deletes a named template
- **THEN** the CLI applies the configured reference-safety and authorization policy and reports dependent paper state
- **AND** it does not silently remove a template still required by durable refs

#### Scenario: Registered exports are inspected or written
- **WHEN** `template exports` or `template export` runs
- **THEN** the CLI reports or writes stable working-copy metadata and tree digests through the resolved exchange surface
- **AND** it refuses to overwrite edited or unrecognized content

#### Scenario: High-level conversion is requested
- **WHEN** a caller asks the CLI to convert or merge an arbitrary user-edited directory into canonical template state
- **THEN** the CLI returns guidance to use the Kaoju agent to construct a candidate and then invoke low-level update
- **AND** canonical state remains unchanged

#### Scenario: Markdown or TeX is derived
- **WHEN** `derive-markdown` or `init-tex` runs
- **THEN** the CLI records selected template name, stable ref, observed digest, converter identity, outputs, warnings, checksums, and lineage
- **AND** it does not declare mechanically initialized TeX ready without agent inspection

#### Scenario: PDF is built
- **WHEN** `build-pdf` receives inspected TeX state
- **THEN** it dispatches the document-build extension point, records the Run and compile log, validates output, and registers the PDF
- **AND** it does not invoke an ambient compiler outside registered execution

### Requirement: Legacy Research Commands Remain Explicit Compatibility Surfaces
The existing `ext research records` commands SHALL remain available, while `ext research templates` SHALL stop owning or mutating the writing-template directory and direct new MyST work to the named Kaoju CRUD and agentic workflow.

#### Scenario: Legacy record command is used
- **WHEN** a caller uses a supported `ext research records` operation
- **THEN** it preserves existing record and provenance meaning
- **AND** it does not become an alternate implementation of named mutable templates

#### Scenario: Legacy template record requires inspection
- **WHEN** a caller inspects an existing `kaoju:writing-template` record
- **THEN** generic record reads preserve access to its legacy LaTeX payload and lineage
- **AND** it is never treated as a named mutable `kaoju:paper-template-myst`

#### Scenario: Legacy template command is invoked
- **WHEN** a caller invokes `ext research templates`
- **THEN** the CLI returns migration guidance naming the applicable Kaoju template CRUD, export, or agentic update entrypoint
- **AND** it does not mutate `intent/derived/writing-template`

#### Scenario: Legacy directory conflicts with a MyST working path
- **WHEN** export finds a legacy LaTeX tree at its target
- **THEN** it reports non-destructive move or archive guidance
- **AND** it does not overwrite, reinterpret, or silently import the files
