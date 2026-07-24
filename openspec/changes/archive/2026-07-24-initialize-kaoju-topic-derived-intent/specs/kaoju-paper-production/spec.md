## ADDED Requirements

### Requirement: Kaoju Ships Checked Packaged Writing-Template Defaults
Kaoju SHALL package immutable role-local `content/main` and `latex/main` template trees that pass the same applicable integrity and authored-metadata validation as topic-owned named stock.

#### Scenario: Packaged defaults are validated
- **WHEN** package resources or the Kaoju contract are validated
- **THEN** validation checks exactly one content `main` tree and one LaTeX `main` tree for safe paths, reserved-file exclusion, deterministic digest, resource version, and role-specific metadata
- **AND** the LaTeX tree also passes entrypoint, composition-contract, and build-profile validation

#### Scenario: Packaged content default is inspected
- **WHEN** an actor or service inspects the packaged content default
- **THEN** it finds a generic MyST-oriented survey-paper scaffold with checked entrypoint and use guidance
- **AND** the package does not encode a topic-specific evidence claim, Direction Set, Survey Contract, or publication venue

#### Scenario: Packaged LaTeX default is inspected
- **WHEN** an actor or service inspects the packaged LaTeX default
- **THEN** it finds a neutral article-style presentation tree with an explicit composition contract
- **AND** the package does not claim compatibility with an unselected venue

#### Scenario: Packaged default is invalid
- **WHEN** a packaged default is missing, unsafe, digest-inconsistent, or invalid for its selected role
- **THEN** topic initialization and fallback for that role block with a stable package-resource diagnostic
- **AND** the system does not substitute an embedded string, another role, a topic from another workspace, or an unmanaged repository file

### Requirement: Kaoju Topic Initialization Ensures Default Writing-Template Stock
Explicit Kaoju `create-topic` SHALL initialize missing role-local content and LaTeX `main` records from checked packaged defaults and create their non-canonical editable exports after generic topic overview and Workspace Runtime readiness.

#### Scenario: New Kaoju topic is initialized
- **WHEN** `create-topic` resolves a concrete `topic.intent.overview`, ready Workspace Runtime, no topic-owned template stock, and no conflicting exchange content
- **THEN** the typed template service creates canonical `content/main` and `latex/main` records from the checked packaged defaults
- **AND** it exports them to `<topic.paper.template_exchange_root>/content/main/` and `<topic.paper.template_exchange_root>/latex/main/`

#### Scenario: Initialization preserves existing stock
- **WHEN** a valid ready `main` record already exists for one role
- **THEN** initialization preserves its stable ref, current tree, state token, metadata, and audit history
- **AND** it does not compare the tree with the packaged default to infer permission to replace it

#### Scenario: Initialization preserves edited exchange content
- **WHEN** a recognized role-local `main` export exists and is edited or observes an older canonical state
- **THEN** initialization reports its edited or canonical-changed posture and leaves it unchanged
- **AND** it does not refresh, merge, delete, or replace the working copy

#### Scenario: Initialization resumes after partial completion
- **WHEN** a prior initialization created one role or its export before another role blocked
- **THEN** retry revalidates and preserves each ready result and continues only the missing work
- **AND** the final result reports created, preserved, exported, invalid, and conflicting posture independently by role

#### Scenario: Existing state is invalid or conflicting
- **WHEN** a named `main` record is invalid or the intended export target contains unrecognized or identity-conflicting content
- **THEN** initialization blocks that role with exact record, path, and diagnostic evidence
- **AND** it does not overwrite the record, target, or another role's state

### Requirement: Default Paper Template Selection Falls Back to Packaged Stock
Kaoju SHALL use one role-aware resolver for omitted/default `main` consumption that prefers valid topic stock and otherwise selects the checked immutable packaged default without creating topic-owned intent.

#### Scenario: Topic main is ready
- **WHEN** a paper consumption or default export operation omits a template selector and a valid ready topic-owned `main` exists for the selected role
- **THEN** the resolver selects that named record and reports `selection_source` as `topic-stock`
- **AND** it records the stable ref, state token, tree digest, role, and name

#### Scenario: Topic main is absent
- **WHEN** a paper consumption or default export operation omits a template selector and verified topic-owned `main` is absent for the selected role
- **THEN** the resolver selects the corresponding checked packaged `main` and reports `selection_source` as `packaged-default`
- **AND** it records the packaged identity, resource version, digest, role, and name without creating a named topic record or topic-derived file

#### Scenario: Topic main exists but is unusable
- **WHEN** topic-owned `main` exists but is invalid, ambiguous, archived without a ready current state, or unsafe
- **THEN** the operation blocks with the topic-state diagnostic
- **AND** it does not classify the state as absent or hide it with packaged fallback

#### Scenario: Explicit name is missing
- **WHEN** a caller explicitly requests a template name or ref that cannot be resolved
- **THEN** the operation returns the exact missing-selection diagnostic
- **AND** it does not substitute role-local `main` or a packaged default

#### Scenario: Packaged fallback is consumed
- **WHEN** drafting or TeX composition selects a packaged default
- **THEN** the consumer snapshots the exact packaged tree into the normal paper-local Artifact and records packaged provenance
- **AND** later package changes do not rewrite the existing paper snapshot

#### Scenario: Packaged fallback is exported
- **WHEN** default export selects a packaged default because topic `main` is absent
- **THEN** it writes a non-canonical working copy with metadata identifying the packaged source, version, and digest
- **AND** promotion of the edited copy requires named-template create rather than update against a nonexistent topic state token

#### Scenario: Exchange directory is missing
- **WHEN** default paper consumption selects valid topic stock or packaged fallback while `topic.paper.template_exchange_root` or its role-local child is absent
- **THEN** paper consumption proceeds without materializing the exchange directory
- **AND** only an authorized export or explicit initialization materializes working-copy paths

### Requirement: Applying Edited Writing Templates Is Future-Facing
Kaoju SHALL promote an accepted edited writing-template working copy through its role-local named-template mutation boundary and SHALL preserve every paper artifact that already observed an earlier state.

#### Scenario: Edited topic-stock export is applied
- **WHEN** the agent assesses a changed content or LaTeX export whose source identity and expected state still match current named stock
- **THEN** the typed service atomically updates the same stable named record and returns a new state token, tree digest, and mutation audit ref
- **AND** later default selection resolves the updated state

#### Scenario: Edited packaged-default export is applied
- **WHEN** the agent assesses a changed export whose metadata identifies packaged fallback and no matching named topic record exists
- **THEN** the typed service creates role-local named stock from the accepted candidate and records packaged-source provenance
- **AND** it does not fabricate an expected state token or update a nonexistent record

#### Scenario: Export base is stale
- **WHEN** the edited export's recorded source state differs from current named stock
- **THEN** apply blocks that template and reports the base, current, and working identities
- **AND** it does not overwrite current stock until the agent reconciles the trees and submits a state-checked candidate

#### Scenario: Past paper artifacts observed older stock
- **WHEN** named stock changes after a paper draft, LaTeX snapshot, TeX draft, or PDF recorded an earlier template identity
- **THEN** those Artifacts retain their content, template refs, state tokens, digests, and provenance
- **AND** applying new stock does not revise, regenerate, or mark them compatible automatically

#### Scenario: User explicitly requests retrospective paper reconciliation
- **WHEN** the user names past paper artifacts and asks to apply newer template intent to them
- **THEN** Kaoju treats the request as separate paper revision or TeX regeneration work with ordinary Gates and provenance
- **AND** the result is a new revision or derived Artifact rather than an in-place rewrite of historical content

## MODIFIED Requirements

### Requirement: MyST Templates Can Be Exported for Manual Editing
The system SHALL export a selected named canonical or packaged-default content template tree to a stable actor-editable working directory with reserved synchronization metadata while retaining topic records as canonical when they exist.

#### Scenario: Template export succeeds
- **WHEN** the actor requests a template export and supplies an authorized path or accepts a resolved Topic Workspace path
- **THEN** the system assigns an automatic export revision, writes the MyST template as a `.md` file, writes `kaoju:paper-template-manifest`, and registers `kaoju:paper-template-export`
- **AND** the manifest records source identity and revision or packaged version, base digest, source-digest refs, paper line id, tied draft ref, export revision, export directory, template filename, and export time

#### Scenario: Managed export target is selected
- **WHEN** the actor accepts the default Topic Workspace export target
- **THEN** the service selects the resolved plural content-template exchange directory
- **AND** it does not overwrite an earlier unrecognized or edited export

#### Scenario: Export target is unsafe or ambiguous
- **WHEN** the target would overwrite unrecognized content, cannot be resolved, or lacks required authorization
- **THEN** the export stops before mutation and reports the exact target problem
- **AND** no successful export artifact is registered

#### Scenario: Default template export succeeds
- **WHEN** the actor requests content-template export without a name or target
- **THEN** the system resolves topic-owned or packaged-default content `main` and exports it to `<topic-workspace>/intent/derived/writing-templates/content/main/`
- **AND** the directory mirrors the selected tree, contains `.isomer-template-export.json`, and is reported as non-canonical

#### Scenario: Named template export succeeds
- **WHEN** the actor exports `<template-name>` without an explicit target
- **THEN** the system resolves the exchange root and writes `<resolved-root>/content/<template-name>/`
- **AND** metadata records the role, name, source identity, state token when applicable, selected and exported digests, actual path, and time

#### Scenario: Registered export status is inspected
- **WHEN** export status is queried
- **THEN** the system recomputes available tree digests excluding reserved metadata and reports unchanged, edited, missing, identity-invalid, and source-changed posture
- **AND** it does not interpret changed file meaning

#### Scenario: Clean target can be refreshed
- **WHEN** a recognized working tree has not changed since export
- **THEN** export can refresh it from the current selected source and update its metadata
- **AND** it does not create a version-numbered sibling directory

#### Scenario: Edited target is protected
- **WHEN** the working tree differs from its recorded exported digest
- **THEN** deterministic export stops and reports source and working state
- **AND** it does not overwrite or mechanically merge the edits

#### Scenario: Export reconciliation is agentic
- **WHEN** the actor asks to combine source changes with an edited working tree
- **THEN** the Kaoju agent interprets both arbitrary trees and prepares the desired working result
- **AND** recording that result as an export observation does not make it canonical

### Requirement: Canonical MyST Templates Are Mutable Named Topic Records
The system SHALL store each topic-owned canonical MyST-oriented paper template tree as one stable mutable `kaoju:paper-template-myst` record identified by a path-safe name within a Topic Workspace, while keeping packaged fallback outside the topic namespace.

#### Scenario: Named templates coexist in one namespace
- **WHEN** templates named `main`, `conference-a`, and `main-before-methodology-change` exist
- **THEN** each name resolves one independent current record and current tree
- **AND** the system assigns no special snapshot meaning to any name

#### Scenario: Canonical template has arbitrary tree shape
- **WHEN** a template contains one or more MyST, configuration, include, asset, or guidance files
- **THEN** the canonical record stores the current tree through a managed directory manifest with file integrity and path-safety metadata
- **AND** it does not require a fixed entrypoint, section set, or universal template schema

#### Scenario: Ordinary update preserves stable identity
- **WHEN** accepted content or allowed metadata changes for an existing name
- **THEN** the system atomically updates the same stable named record and returns a new state token and digest
- **AND** it does not create a historical template-content revision, `revision_of`, or `supersedes` record

#### Scenario: Omitted paper-use or export name resolves role-local main
- **WHEN** a paper drafting or export operation does not receive an explicit template name
- **THEN** it resolves valid topic-owned content `main` or, when that record is verified absent, packaged content `main`
- **AND** it does not select another named template by timestamp, paper line, path, record order, or another role

### Requirement: Underspecified Template Updates Use Ordered Source Discovery
The Kaoju agent SHALL discover a content-template source in a fixed order when the user asks to update the paper template in the current artifacts database without supplying a template name, canonical ref, template path, or export path.

#### Scenario: One registered export was edited
- **WHEN** exactly one eligible registered content export has a current tree digest different from its recorded exported digest
- **THEN** the agent selects that export directory and its recorded target name
- **AND** it does not fall through to the topic `content/main` directory

#### Scenario: Several registered exports were edited
- **WHEN** more than one eligible content export was edited or an edited export has ambiguous identity
- **THEN** the agent presents the concrete names, refs, and paths and asks the user which source to use
- **AND** it does not select by modification time or record order

#### Scenario: No edited export and topic main directory exists
- **WHEN** no eligible edited export exists and `<topic-workspace>/intent/derived/writing-templates/content/main/` exists in the current Topic Workspace
- **THEN** the agent uses that directory as source and targets name `main` unless consistent export metadata identifies it more precisely
- **AND** this fallback does not depend on a database template named `main` existing

#### Scenario: No discoverable source exists
- **WHEN** no eligible edited export exists and the current Topic Workspace has no content-template `main` directory
- **THEN** the agent asks the user which template or directory to use
- **AND** it does not use a packaged default as authorization to create or update mutable topic stock

#### Scenario: Explicit input bypasses discovery
- **WHEN** the update request supplies a template name, canonical ref, template path, or export path
- **THEN** the agent validates and uses that explicit selection
- **AND** it does not replace it through implicit discovery

### Requirement: LaTeX Composition Uses an Exact Stocked Template State
The system SHALL derive `KAOJU:PAPER-TEMPLATE-TEX` and `KAOJU:PAPER-DRAFT-TEX` from an exact canonical MyST draft and an exact observed topic-owned or packaged-default LaTeX template state.

#### Scenario: Default LaTeX composition succeeds
- **WHEN** a paper requests TeX composition without an explicit LaTeX name and `latex/main` is ready
- **THEN** the composer snapshots its complete tree and records the stable ref, name, state token, digest, entrypoint, composition contract, build profile, and source provenance
- **AND** the derived TeX draft is self-contained and linked separately to its canonical MyST draft and presentation snapshot

#### Scenario: No default LaTeX stock exists
- **WHEN** composition omits a LaTeX name and verified topic-owned `latex/main` is absent
- **THEN** the composer snapshots the checked packaged LaTeX `main` tree and records its packaged identity, resource version, digest, entrypoint, composition contract, and build profile
- **AND** it does not create topic-owned named stock or an exchange copy

#### Scenario: Explicit LaTeX selection is missing
- **WHEN** composition explicitly names a LaTeX template or ref that is unavailable
- **THEN** the workflow pauses with the exact missing named-template requirement and stock or adoption routes
- **AND** it does not use packaged fallback or select a paper-line TeX revision

#### Scenario: Content template changes
- **WHEN** the canonical content-template digest changes while the selected LaTeX stock and composition contract remain unchanged
- **THEN** the change can require a new MyST draft and TeX draft but does not itself revise the stocked LaTeX template or its presentation fingerprint
- **AND** content-template and LaTeX-template drift remain independently reportable

#### Scenario: Mechanical conversion requires repair
- **WHEN** MyST constructs cannot be composed faithfully through the selected LaTeX contract
- **THEN** the composer records file-located diagnostics and requires direct agent inspection of the paper-specific TeX tree
- **AND** repairs remain paper-local unless the actor explicitly authorizes a stocked LaTeX-template update
