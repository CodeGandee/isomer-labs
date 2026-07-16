# kaoju-survey-intents Specification

## Purpose
TBD - created by syncing change revise-kaoju-survey-process. Update Purpose after archive.

## Requirements

### Requirement: Kaoju Proposes and Records Survey Directions
The system SHALL derive candidate survey directions from the active Research Topic and SHALL return the final human-selected directions as one current `kaoju:direction-set` artifact distinct from `kaoju:survey-contract`.

#### Scenario: Agent proposes bounded directions
- **WHEN** the actor asks for useful next survey directions from a Research Topic
- **THEN** the frame skill proposes three distinct directions by default and explains their relationship to the topic
- **AND** each direction contains a stable direction id, scoped question, boundary, expected source classes, coverage date, expected evidence depth, and deliverables

#### Scenario: Human controls the selected set
- **WHEN** the actor reviews proposed directions
- **THEN** the system permits multi-selection, rejection, revision, and actor-authored custom directions
- **AND** it does not create the accepted direction set until the actor confirms the selection

#### Scenario: Current host affects empirical feasibility
- **WHEN** one or more proposed directions depend on empirical work whose feasibility varies with the current host hardware or environment
- **THEN** the system records a feasibility annotation with the relevant observed capability and limits
- **AND** it does not exclude or rank other directions solely because of the current host

#### Scenario: Direction set becomes discovery input
- **WHEN** the actor accepts one or more directions
- **THEN** the system creates or revises the current `kaoju:direction-set` with selection provenance and a distinct stable entry for each direction
- **AND** downstream reading-list discovery consumes selected direction refs rather than inferring directions from the survey contract or chat history

### Requirement: Kaoju Maintains One Reading List per Direction
The system SHALL maintain one scoped current `kaoju:reading-list` for each selected direction and SHALL preserve prior revisions.

#### Scenario: Default reading-list target is applied
- **WHEN** the actor asks to collect online information for one accepted direction
- **THEN** the discover skill targets three priority items and three secondary items
- **AND** it records achieved counts, unresolved deficits, search boundaries, and why each selected item has its priority

#### Scenario: Shorter result is a warning
- **WHEN** bounded discovery cannot identify three suitable priority and three suitable secondary items
- **THEN** the system records the reachable list and a non-blocking coverage warning
- **AND** the actor may approve the shorter list or request further discovery

#### Scenario: Candidate is blocked during discovery
- **WHEN** a selected candidate cannot be accessed or its identity cannot be resolved
- **THEN** the system preserves the candidate and blocker in discovery provenance without counting it toward the reachable 3+3 target
- **AND** it performs bounded backfill before reporting any remaining coverage deficit

#### Scenario: Different directions do not collide
- **WHEN** a topic contains reading lists for two accepted directions
- **THEN** each list uses the applicable direction scope key and remains independently queryable and revisable
- **AND** a revision to one direction's list does not supersede the other direction's list

### Requirement: Reading-List Discovery Preserves Search and Identity Evidence
Reading-list construction SHALL search across papers, technical reports, source-code repositories, datasets, and models while treating papers and technical reports as the primary works.

#### Scenario: Candidate records query provenance
- **WHEN** a provider query or reference traversal yields a candidate
- **THEN** the discovery ledger records query text or seed ref, provider or access method, query time, searched-through date, discovery route, source class, and selection disposition
- **AND** provider ranking, citation count, or recency alone does not establish inclusion or authority

#### Scenario: Versions are grouped without inflating coverage
- **WHEN** multiple versions, mirrors, preprints, reports, or repository releases represent one source family
- **THEN** the reading list records a canonical Source Identity and version-family relationship
- **AND** variants do not count as independent priority or secondary works unless the recorded rationale establishes materially distinct evidence

#### Scenario: User-supplied source receives priority review
- **WHEN** the actor supplies a source for the direction
- **THEN** the system gives it priority review and records its terminal disposition
- **AND** user nomination does not grant automatic inclusion, correctness, or evidentiary authority

### Requirement: Actors Can Inspect, Refine, and Approve Reading Lists
The system SHALL expose reading-list inspection and revision before the list becomes accepted input to deep ingestion.

#### Scenario: Actor inspects a reading list
- **WHEN** the actor asks to inspect a direction's reading list
- **THEN** the system queries the scoped current artifact from the state DB and presents identity, source class, priority, relevance, access posture, version family, and provenance for each item

#### Scenario: Actor revises selection
- **WHEN** the actor requests additions, removals, reprioritization, or another bounded discovery pass
- **THEN** the system creates a reading-list revision with lineage to the prior list
- **AND** prior accepted or rejected entries retain their dispositions and rationale

#### Scenario: Actor approves ingestion input
- **WHEN** the actor approves the reading list
- **THEN** the system records acceptance metadata and makes its selected item refs eligible for `ingest-reading-item`
- **AND** unapproved list drafts are not treated as accepted synthesis evidence

### Requirement: Kaoju Ingests One Selected Reading Item in Depth
The system SHALL ingest one selected reading-list item at a time and SHALL produce a durable `kaoju:source-digest` or `kaoju:source-access-blocker`.

#### Scenario: Artifact library is checked first
- **WHEN** deep ingestion begins for a selected item
- **THEN** the acquire skill queries `kaoju:artifact-library` and relevant scoped source records through the state DB before downloading or registering material
- **AND** it reuses a verified matching artifact when identity, version, digest, access, and staleness policy remain compatible

#### Scenario: Source material is acquired according to type
- **WHEN** the selected item is a paper, report, repository, dataset, model, web page, or online documentation
- **THEN** papers and source code are stored or registered locally when permitted, external governed material is referenced through a manifest, and web or documentation sources may remain online with an optional snapshot
- **AND** all managed target paths are resolved through `isomer-cli`

#### Scenario: Provider restrictions preserve a fallback
- **WHEN** local download or snapshotting is prohibited but authorized online reading remains available
- **THEN** the system records the access restriction and continues through the online locator
- **AND** it does not claim a local copy exists

#### Scenario: Inaccessible source creates a blocker
- **WHEN** the source identity cannot be resolved or the required content cannot be accessed after bounded attempts
- **THEN** the system creates `kaoju:source-access-blocker` with attempted locators, failure evidence, impact, and resume condition
- **AND** it does not fabricate a source digest

### Requirement: Source Digests Preserve Claim-Level Evidence
An accepted `kaoju:source-digest` SHALL distinguish source statements, agent interpretation, and unresolved claims with exact evidence locators.

#### Scenario: Paper or report is digested
- **WHEN** a paper or report is read in depth
- **THEN** the source digest records identity and version, scope, method, assumptions, main claims, evidence, limitations, relationships, relevant artifacts, and exact page, section, figure, table, or quoted-span locators where available
- **AND** each claim-bearing finding links to the Claim-Evidence Ledger with an evidence verdict and verification depth

#### Scenario: A selected claim depends on a figure or table
- **WHEN** a paper figure or table supports a selected claim and automated extraction is useful
- **THEN** the system may extract the relevant visual or tabular evidence with an exact locator and mark the extraction provisional
- **AND** it does not accept the extracted evidence until it is verified against the original source or a human resolves an unreliable comparison

#### Scenario: Source code is digested
- **WHEN** a local source repository is inspected in depth
- **THEN** code-level statements cite the immutable commit, repository ref, file path, and line range
- **AND** observed implementation behavior remains distinct from paper claims and execution results

#### Scenario: Digest is refined or approved
- **WHEN** the actor requests correction, deeper inspection, or approval of a source digest
- **THEN** the system revises the scoped digest or records its acceptance with provenance
- **AND** the prior digest remains historical and synthesis consumes only accepted revisions

### Requirement: Associated Source Code Is Registered and Related
The system SHALL discover and register associated source code for a selected paper when an accessible and unambiguous repository can be established through externally executed acquisition and verification.

#### Scenario: Associated repository is found
- **WHEN** a paper, report, metadata page, or verified project reference identifies associated source code
- **THEN** the acting agent resolves the repository identity, runs the applicable external repository commands, verifies the resulting immutable identity, and registers the existing path as a Canonical External Repository
- **AND** it records `KAOJU:ASSOCIATED-SOURCE-CODE` with paper ref, semantic repository label, requested and resolved repository identity, immutable commit or digest, relationship basis, acquisition method, sanitized command evidence, and access provenance

#### Scenario: Repository relationship is uncertain
- **WHEN** multiple repositories plausibly correspond to the paper or the relationship cannot be verified
- **THEN** the system records the candidates and asks for clarification or creates a blocker
- **AND** it does not execute acquisition commands or register an arbitrary repository as associated source code

#### Scenario: Acquisition does not complete
- **WHEN** the selected external acquisition or identity-verification procedure fails
- **THEN** the system records a resumable source-access blocker and any safe partial-result posture
- **AND** it does not create a successful repository binding or associated-source-code record for the failed attempt

### Requirement: Claim-Bearing Survey Work Is Audited Before Synthesis
The system SHALL prevent claim-bearing survey records from becoming synthesis or paper inputs until the applicable audit accepts their identity, provenance, locator, evidence, and limitation posture.

#### Scenario: Unaudited records are present
- **WHEN** synthesis or paper drafting resolves source digests, ledgers, catalogs, comparisons, or trial results that lack an accepted audit disposition
- **THEN** the procedure pauses with the unresolved record refs and required audit route
- **AND** it does not silently treat those records as accepted evidence

#### Scenario: Audit is accepted
- **WHEN** the audit accepts the selected claim-bearing records
- **THEN** synthesis may consume the exact audited revisions
- **AND** contradictions, blockers, failures, and limitations remain visible in downstream artifacts

### Requirement: Survey Intents Are Resumable from Durable State
Each survey intent SHALL checkpoint completed stages and SHALL resume from state-DB records rather than conversation memory or directory discovery.

#### Scenario: Procedure pauses for selection or access
- **WHEN** a survey intent pauses for a human choice, Gate, blocker, or unavailable source
- **THEN** its Run checkpoint records procedure id, stage id, input refs, completed output refs, pending decision or blocker refs, and resume hint

#### Scenario: Procedure resumes
- **WHEN** the actor asks to continue a paused survey intent
- **THEN** the pipeline resolves the Run and referenced artifacts from Workspace Runtime, validates their current identities and checksums, and starts at the first incomplete stage
- **AND** it does not repeat a completed durable stage unless its inputs are stale or the actor requests refresh
