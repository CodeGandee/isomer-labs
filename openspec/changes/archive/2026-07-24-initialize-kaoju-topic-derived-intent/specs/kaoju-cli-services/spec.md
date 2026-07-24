## ADDED Requirements

### Requirement: Typed Kaoju Services Resolve Checked Default Templates
The typed Kaoju template and paper services SHALL resolve omitted role-local `main` through one non-mutating selection boundary that distinguishes topic stock, packaged default, invalid topic state, and explicit-selection failure.

#### Scenario: Topic stock is selected
- **WHEN** a default-consuming command omits a template name and valid ready role-local `main` exists in the selected Topic Workspace
- **THEN** the result identifies `topic-stock`, stable ref, state token, digest, role, name, and selected context
- **AND** the service does not inspect sibling topics or exchange directories to replace canonical selection

#### Scenario: Packaged default is selected
- **WHEN** a default-consuming command omits a template name and role-local topic `main` is verified absent
- **THEN** the result identifies `packaged-default`, packaged resource version, digest, role, name, and selected context
- **AND** resolution writes no named record, audit, query-index row, Topic Workspace Manifest binding, or exchange directory

#### Scenario: Existing topic state is invalid
- **WHEN** role-local topic `main` exists but its current record, managed tree, metadata, or identity is invalid or ambiguous
- **THEN** resolution returns a stable topic-state diagnostic
- **AND** it does not use packaged fallback

#### Scenario: Explicit selection fails
- **WHEN** a caller supplies an unavailable explicit name or ref
- **THEN** resolution returns the exact selected-role missing-template diagnostic and context metadata
- **AND** it does not fall back to `main`, packaged resources, another role, or another topic

#### Scenario: Packaged resource validation fails
- **WHEN** packaged fallback is required but the selected packaged tree or metadata fails validation
- **THEN** the operation returns a stable package-resource diagnostic with the role and checked resource identity
- **AND** it does not continue with generated placeholder content

### Requirement: Typed Kaoju Services Ensure Topic Template Defaults
The typed Kaoju template service SHALL expose an idempotent selected-topic operation that creates missing content and LaTeX `main` stock from checked packaged defaults and exports safe editable copies.

#### Scenario: Both role defaults are missing
- **WHEN** ensure-defaults runs with ready Workspace Runtime and neither role-local `main` exists
- **THEN** the service creates both records through the existing atomic named-state boundary and exports them beneath the resolved plural exchange root
- **AND** the result reports stable refs, tokens, digests, audit refs, export paths, and per-role creation posture

#### Scenario: One role is already ready
- **WHEN** ensure-defaults finds a valid ready `main` in one role and absence in the other
- **THEN** it preserves the ready role and creates only the missing role
- **AND** a repeated call returns preserved posture without a new state token or mutation audit for unchanged stock

#### Scenario: Existing export cannot be refreshed safely
- **WHEN** the intended default export is edited, identity-invalid, canonical-changed, or contains unrecognized content
- **THEN** the service reports that exact posture and leaves the path unchanged
- **AND** it does not make successful canonical creation contingent on overwriting the working copy

#### Scenario: Runtime is unavailable
- **WHEN** ensure-defaults runs before selected-topic Workspace Runtime is ready
- **THEN** it returns the exact runtime prerequisite diagnostic without creating stock or exports
- **AND** the Kaoju topic creator retains the generic runtime owner as the recovery route

### Requirement: Template Migration Handles the Plural Exchange Root
The typed template migration service SHALL preview and explicitly apply migration from the known singular exchange root to the plural default without silently merging or overwriting content.

#### Scenario: Migration preview finds only a singular root
- **WHEN** an unbound Topic Workspace contains `intent/derived/writing-template` and the plural target is absent
- **THEN** preview reports recognized role/name trees, metadata posture, digests, registered observations, target paths, and proposed mutations
- **AND** it changes no files, bindings, records, or observations

#### Scenario: Migration apply succeeds
- **WHEN** the actor explicitly applies a preview whose source state remains current and every target is conflict-free
- **THEN** migration stages and verifies the plural tree, publishes it atomically, records applicable new export observations, and removes the singular tree only after successful verification
- **AND** historical observations retain their original paths and canonical named records remain unchanged

#### Scenario: Migration source changes after preview
- **WHEN** a source digest, target posture, binding, or registered observation changes before apply
- **THEN** migration rejects the stale plan and requires a new preview
- **AND** it leaves both roots unchanged

#### Scenario: Both roots contain conflicting content
- **WHEN** migration finds non-equivalent source and target content for any role and name
- **THEN** preview and apply report a deterministic conflict
- **AND** apply performs no partial move, merge, deletion, or record rewrite

## MODIFIED Requirements

### Requirement: Legacy Research Commands Remain Explicit Compatibility Surfaces
The existing `ext research records` commands SHALL remain available, while `ext research templates` SHALL stop owning or mutating either writing-template exchange directory and direct new MyST work to the named Kaoju CRUD and agentic workflow.

#### Scenario: Legacy record command is used
- **WHEN** a caller uses a supported `ext research records` operation
- **THEN** it preserves existing record and provenance meaning
- **AND** it does not become an alternate implementation of named mutable templates

#### Scenario: Legacy template is inspected
- **WHEN** a caller lists, shows, compiles, or archives an existing `kaoju:writing-template`
- **THEN** the compatibility command preserves its legacy LaTeX meaning and reports that it is non-canonical for new paper content
- **AND** it does not silently promote the template to `kaoju:paper-template-myst`

#### Scenario: New canonical paper work is requested through the legacy group
- **WHEN** a caller attempts to create new canonical paper state through `ext research templates`
- **THEN** the CLI returns a deprecation diagnostic and the corresponding `ext kaoju paper` command
- **AND** it does not create ambiguous dual canonical state

#### Scenario: Legacy template record requires inspection
- **WHEN** a caller inspects an existing `kaoju:writing-template` record
- **THEN** generic record reads preserve access to its legacy LaTeX payload and lineage
- **AND** it is never treated as a named mutable `kaoju:paper-template-myst`

#### Scenario: Legacy template command is invoked
- **WHEN** a caller invokes `ext research templates`
- **THEN** the CLI returns migration guidance naming the applicable Kaoju template CRUD, export, or agentic update entrypoint
- **AND** it does not mutate `intent/derived/writing-template` or `intent/derived/writing-templates`

#### Scenario: Legacy directory conflicts with a current working path
- **WHEN** export or exchange-root migration finds a legacy tree at its target
- **THEN** it reports non-destructive migration, move, or archive guidance
- **AND** it does not overwrite, reinterpret, or silently import the files

### Requirement: CLI Composes Stocked LaTeX Templates
The paper CLI SHALL compose canonical MyST content with an exact selected topic-owned or packaged-default LaTeX state rather than generating presentation state solely from document-class flags.

#### Scenario: Explicit LaTeX selection is composed
- **WHEN** `init-tex` receives an explicit LaTeX name or ref
- **THEN** it resolves and snapshots that exact topic-owned state, validates its composition contract, and creates a self-contained TeX draft
- **AND** the result reports separate content-template and LaTeX-template identities

#### Scenario: Default topic LaTeX selection is composed
- **WHEN** `init-tex` omits the LaTeX selector and valid ready topic-owned LaTeX `main` exists
- **THEN** it resolves and snapshots that named state
- **AND** the result identifies selection source `topic-stock`

#### Scenario: Default packaged LaTeX selection is composed
- **WHEN** `init-tex` omits the LaTeX selector and topic-owned LaTeX `main` is verified absent
- **THEN** it resolves and snapshots checked packaged LaTeX `main`
- **AND** the result identifies selection source `packaged-default`, resource version, and digest without creating topic stock

#### Scenario: Default topic LaTeX state is invalid
- **WHEN** `init-tex` omits the LaTeX selector and existing role-local `main` is invalid or ambiguous
- **THEN** it returns a stable non-mutating topic-state diagnostic
- **AND** it does not hide that state with packaged fallback
