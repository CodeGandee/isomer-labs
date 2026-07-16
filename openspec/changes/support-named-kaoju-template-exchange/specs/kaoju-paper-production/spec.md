## ADDED Requirements

### Requirement: Canonical MyST Templates Are Mutable Named Topic Records
The system SHALL store each canonical MyST-oriented paper template tree as one stable mutable `kaoju:paper-template-myst` record identified by a path-safe name within a Topic Workspace.

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

#### Scenario: Omitted paper-use or export name resolves to main
- **WHEN** a paper drafting or export operation does not receive an explicit template name
- **THEN** it resolves canonical template `main`
- **AND** it does not select another named template by timestamp, paper line, path, or record order

### Requirement: Saved Template States Are Ordinary Named Copies
The system SHALL preserve a template state only through an explicit create operation that copies it to another ordinary name in the same template namespace.

#### Scenario: Agent explicitly preserves main
- **WHEN** the user or agent creates `main-before-change` from current template `main`
- **THEN** the system creates an ordinary named template with the exact source tree and allowed metadata observed at copy time
- **AND** both names remain independently mutable and usable

#### Scenario: Copy has no snapshot classification
- **WHEN** a caller lists or shows the copied template
- **THEN** it has the same semantic id, binding, fields, and operations as every other named template
- **AND** the database stores no snapshot type, flag, parent lifecycle, retention policy, or special list

#### Scenario: Ordinary update does not create a copy
- **WHEN** a user or agent updates a named template without first requesting another name
- **THEN** only the selected named current state changes
- **AND** the prior content is not retained as a restorable template by contract

#### Scenario: Known named state replaces another template
- **WHEN** the actor explicitly replaces target template `main` from named template `main-before-change`
- **THEN** the system copies the source tree and applicable authored metadata exactly into stable target `main`
- **AND** it performs no merge and leaves the source name unchanged

### Requirement: Underspecified Template Updates Use Ordered Source Discovery
The Kaoju agent SHALL discover a template source in a fixed order when the user asks to update the paper template in the current artifacts database without supplying a template name, canonical ref, template path, or export path.

#### Scenario: One registered export was edited
- **WHEN** exactly one eligible registered export has a current tree digest different from its recorded exported digest
- **THEN** the agent selects that export directory and its recorded target name
- **AND** it does not fall through to the topic `main` directory

#### Scenario: Several registered exports were edited
- **WHEN** more than one eligible export was edited or an edited export has ambiguous identity
- **THEN** the agent presents the concrete names, refs, and paths and asks the user which source to use
- **AND** it does not select by modification time or record order

#### Scenario: No edited export and topic main directory exists
- **WHEN** no eligible edited export exists and `<topic-workspace>/intent/derived/writing-template/main/` exists in the current Topic Workspace
- **THEN** the agent uses that directory as source and targets name `main` unless consistent export metadata identifies it more precisely
- **AND** this fallback does not depend on a database template named `main` existing

#### Scenario: No discoverable source exists
- **WHEN** no eligible edited export exists and the current Topic Workspace has no writing-template `main/` directory
- **THEN** the agent asks the user which template or directory to use
- **AND** it does not infer a source from an unrelated database record

#### Scenario: Explicit input bypasses discovery
- **WHEN** the update request supplies a template name, canonical ref, template path, or export path
- **THEN** the agent validates and uses that explicit selection
- **AND** it does not replace it through implicit discovery

## MODIFIED Requirements

### Requirement: MyST Templates Can Be Exported for Manual Editing
The system SHALL export a selected named canonical template tree to a stable actor-editable working directory with reserved synchronization metadata while retaining the artifacts-database record as canonical state.

#### Scenario: Default template export succeeds
- **WHEN** the actor requests export without a name or target
- **THEN** the system exports canonical `main` to `<topic-workspace>/intent/derived/writing-template/main/`
- **AND** the directory mirrors the current tree, contains `.isomer-template-export.json`, and is reported as non-canonical

#### Scenario: Named template export succeeds
- **WHEN** the actor exports `<template-name>` without an explicit target
- **THEN** the system resolves the exchange root and writes `<resolved-root>/<template-name>/`
- **AND** metadata records the stable canonical ref, state token, canonical and exported digests, actual path, and time

#### Scenario: Registered export status is inspected
- **WHEN** export status is queried
- **THEN** the system recomputes available tree digests excluding reserved metadata and reports unchanged, edited, missing, identity-invalid, and canonical-changed posture
- **AND** it does not interpret changed file meaning

#### Scenario: Clean target can be refreshed
- **WHEN** a recognized working tree has not changed since export
- **THEN** export can refresh it from current canonical state and update its metadata
- **AND** it does not create a version-numbered sibling directory

#### Scenario: Edited target is protected
- **WHEN** the working tree differs from its recorded exported digest
- **THEN** deterministic export stops and reports canonical and working state
- **AND** it does not overwrite or mechanically merge the edits

#### Scenario: Export reconciliation is agentic
- **WHEN** the actor asks to combine canonical changes with an edited working tree
- **THEN** the Kaoju agent interprets both arbitrary trees and prepares the desired working result
- **AND** recording that result as an export observation does not make it canonical

### Requirement: Revised MyST Templates Are Validated and Applied
The system SHALL expose low-level create and update operations for mutable named templates while requiring the Kaoju agent to construct or reconcile any candidate whose high-level meaning is not already known.

#### Scenario: Agent-prepared tree updates an existing name
- **WHEN** the agent prepares a clean candidate for target name `main` and supplies its expected current state token
- **THEN** the CLI verifies concurrency, path safety, tree integrity, reserved-file exclusion, actor, source, and change summary and atomically updates stable `main`
- **AND** it does not retain prior template content automatically

#### Scenario: Low-level file or metadata edit is applied
- **WHEN** an authorized caller puts or removes one safe relative file or patches allowed JSON metadata with the current state token
- **THEN** the CLI applies the edit atomically to the same named state and returns the new token and digest
- **AND** service-controlled identity, scope, digest, and audit fields cannot be patched

#### Scenario: Another named template replaces the target
- **WHEN** the caller updates target `<target-name>` from known named source `<source-name>` with the current target state token
- **THEN** the CLI copies exact source content and applicable metadata into the stable target state
- **AND** it does not invoke agentic merge or alter the source template

#### Scenario: Arbitrary source requires agent interpretation
- **WHEN** a user-edited directory must be combined with current target content
- **THEN** the Kaoju agent inspects both, resolves or asks about semantic choices, and constructs a candidate before invoking low-level update
- **AND** isomer-cli does not convert or merge the arbitrary source automatically

#### Scenario: Concurrent target change rejects update
- **WHEN** the supplied expected state token is stale
- **THEN** the mutation fails with current token and digest diagnostics
- **AND** the current tree and metadata remain unchanged

#### Scenario: Missing target requires explicit create
- **WHEN** an agent prepares content from topic `main/` but database template `main` does not exist
- **THEN** it invokes explicit create after explaining the initial registration
- **AND** update does not silently become create

#### Scenario: Template update does not silently revise drafts
- **WHEN** mutable named template state changes
- **THEN** existing drafts retain the template name, stable ref, and digest observed when they were produced
- **AND** consuming the new state requires an explicit drafting or reconciliation action
