## ADDED Requirements

### Requirement: Named Template Binding Uses Mutable State
The `kaoju:paper-template-myst` binding SHALL support one stable mutable current record per template name without automatic content revisions.

#### Scenario: Stable name owns one current record
- **WHEN** a template name is created
- **THEN** its Topic Workspace and template-name scope identify one stable record whose managed tree and authored metadata can be updated atomically
- **AND** ordinary lookup does not select among superseding candidates

#### Scenario: Update replaces current state
- **WHEN** content or allowed metadata changes with the expected state token
- **THEN** the binding updates the stable record's current managed tree, digest, metadata, token, and update time
- **AND** it creates no `revision_of`, `supersedes`, or historical template-content record

#### Scenario: Explicit saved state is another name
- **WHEN** the actor copies one template to a new name
- **THEN** the new record uses the same semantic id, binding, content mode, mutable-state behavior, and operations
- **AND** no binding field classifies it as a snapshot

#### Scenario: Canonical content supports arbitrary file trees
- **WHEN** a named template contains multiple files or no conventional main filename
- **THEN** its current content uses a managed directory manifest with checksummed safe relative paths
- **AND** the binding does not assert a universal internal template format

#### Scenario: Lightweight audit does not retain old content
- **WHEN** mutable named state changes
- **THEN** an audit event records name, stable ref, actor, operation, source refs, time, and before-and-after tokens and digests
- **AND** the event does not retain prior template bytes or become a restorable template

#### Scenario: Working directory remains non-canonical
- **WHEN** a named template is exported
- **THEN** the external working directory and export observation remain distinct from the mutable canonical record
- **AND** editing the directory does not change database state until explicit low-level CRUD succeeds

## MODIFIED Requirements

### Requirement: Kaoju Records Preserve Lineage and Revision Meaning
Kaoju bindings SHALL define canonical lineage, scope, update, and revision behavior for every semantic id, including explicit mutable-state exceptions.

#### Scenario: Ordinary scoped current-state object is revised
- **WHEN** accepted content changes for a direction set, direction-owned reading list, source-owned digest, artifact library, Topic Dataset Manifest, Claim-Evidence Ledger, Related-Work Catalog, paper structure, paper draft, current terminal status, or another binding marked as revisioned current state
- **THEN** the service creates a revision so the prior record remains historical and the new record becomes the explicit latest candidate for the same binding-defined scope
- **AND** records in another direction, source, paper line, or target scope remain independently current

#### Scenario: Mutable named template is updated
- **WHEN** accepted content or metadata changes for a binding-marked mutable named paper template
- **THEN** the service atomically updates its stable current record and lightweight audit evidence
- **AND** it does not apply the revisioned-current-state behavior used by other semantic ids

#### Scenario: Explicit named copy preserves template content
- **WHEN** a user or agent requires a restorable paper-template state
- **THEN** it creates another ordinary named template through the same binding
- **AND** no implicit historical revision or snapshot record is created

#### Scenario: Delta and audit remain separate records
- **WHEN** a curated intake, direction expansion, audit, follow-up, bounded repair, template export observation, template mutation audit, build attempt, wiki export, environment preparation, or trial produces event evidence
- **THEN** it creates the applicable separate evidence record with parent or subject refs
- **AND** it does not silently convert event evidence into restorable template content

#### Scenario: Run fidelity is not revised away
- **WHEN** a faithful Run fails and an adapted or repaired Run follows
- **THEN** each Run remains separate with its own purpose, inputs, outputs, timing, environment, and lineage
- **AND** the later Run does not replace the earlier verdict

#### Scenario: Competing revisioned candidates remain visible
- **WHEN** two non-superseded accepted records claim the same revisioned semantic id and scope
- **THEN** scoped latest lookup reports a conflict with both stable refs
- **AND** this candidate-selection rule is not used for binding-enforced unique mutable template names
