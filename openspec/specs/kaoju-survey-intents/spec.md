# kaoju-survey-intents Specification

## Purpose
TBD - created by syncing change revise-kaoju-survey-process. Update Purpose after archive.
## Requirements
### Requirement: Kaoju Proposes and Records Survey Directions
The system SHALL derive candidate survey directions from the active Research Topic, SHALL return the final human-reviewed directions as one current `KAOJU:DIRECTION-SET` record distinct from `KAOJU:SURVEY-CONTRACT`, and SHALL project every durable proposal concept into the canonical Research Idea portfolio as part of the accepted write.

#### Scenario: Agent proposes bounded directions
- **WHEN** the actor asks for useful next survey directions from a Research Topic
- **THEN** the frame skill proposes three distinct directions by default and explains their relationship to the topic
- **AND** each direction contains a stable direction id, stable canonical idea identity for new writes, title, scoped question, boundary, expected source classes, coverage date, expected evidence depth, and deliverables

#### Scenario: Human controls the selected set
- **WHEN** the actor reviews proposed directions
- **THEN** the system permits multi-selection, non-selection without closure, explicit deferral, explicit closure, revision, and actor-authored custom directions
- **AND** it does not create the accepted Direction Set or promised canonical Research Idea effects until the actor confirms the authored option outcomes

#### Scenario: Current host affects empirical feasibility
- **WHEN** one or more proposed directions depend on empirical work whose feasibility varies with the current host hardware or environment
- **THEN** the system records a feasibility annotation with the relevant observed capability and limits
- **AND** it does not exclude or rank other directions solely because of the current host

#### Scenario: Direction set becomes discovery input
- **WHEN** the actor accepts one or more directions
- **THEN** the system creates or revises the current `KAOJU:DIRECTION-SET` with selection provenance, a distinct stable entry for each direction, and the accepted canonical Research Idea refs
- **AND** downstream reading-list discovery consumes selected direction and idea refs rather than inferring directions from the Survey Contract, rendered output, or chat history

#### Scenario: Confirmed direction proposals enter the canonical portfolio
- **WHEN** a new idea-bearing Direction Set is accepted
- **THEN** the same transaction writes one canonical Research Idea per durable proposal, an exact Idea Realization to its object-valued `$.sections.proposals[<index>]` path, one proposal-generation group, the Direction Set Decision Record, every authored decision option, and all justified state transitions
- **AND** the accepted result returns those canonical refs for terminal verification and Project Web indexing

#### Scenario: Non-selected direction remains available
- **WHEN** a direction participates in the confirmed decision but the actor neither selects, defers, nor closes it
- **THEN** its decision option outcome records that it was not selected by this decision while its canonical decision state remains `open`
- **AND** the system does not treat non-selection as rejection, deferral, closure, archival, or evidence refutation

#### Scenario: Direction is explicitly deferred or closed
- **WHEN** the actor explicitly defers or closes a proposed direction
- **THEN** the accepted Direction Set records its authored outcome, rationale, actor, and applicable reason code and commits the corresponding canonical decision-state transition
- **AND** a closed direction has the required closure reason and remains queryable for GUI review and later reopening

#### Scenario: Direction revision preserves or changes concept identity
- **WHEN** an accepted Direction Set revision changes wording, boundary detail, evidence depth, or deliverables without changing the direction concept
- **THEN** it retains the same `idea_id` and adds or refreshes an Idea Realization without creating an idea-level `revision_of` edge
- **AND** a concept-changing replacement creates a new Research Idea with explicit justified idea lineage while record revision lineage remains separate

#### Scenario: Kaoju operates without DeepSci
- **WHEN** a Topic Workspace installs Kaoju without the optional DeepSci extension
- **THEN** Kaoju resolves the paradigm-neutral Research Idea Recording contract and completes the same canonical writes and validation
- **AND** no Kaoju skill depends on `isomer-deepsci-shared` or a DeepSci payload profile

### Requirement: Kaoju Maintains One Reading List per Direction
The system SHALL maintain one scoped current `kaoju:reading-list` for each selected direction, SHALL preserve prior revisions, and SHALL derive and persist the effective priority and secondary target counts that bound discovery.

#### Scenario: Default reading-list target is applied
- **WHEN** the actor asks to collect online information for one accepted direction without specifying a count
- **THEN** the discover skill targets three priority items and three secondary items
- **AND** the Reading List records the default target, achieved counts, unresolved deficits, search boundaries, and why each selected item has its priority

#### Scenario: Actor specifies category targets
- **WHEN** the actor specifies a priority count, a secondary count, or both for one direction
- **THEN** the discover skill uses each supplied non-negative integer as that category's target and defaults each omitted category to three
- **AND** the combined effective target must contain at least one work
- **AND** the Reading List records the effective counts with a user-category derivation

#### Scenario: Actor specifies a total target
- **WHEN** the actor requests a positive integer total of `N` works without category counts
- **THEN** the discover skill targets `ceil(N / 2)` priority works and `floor(N / 2)` secondary works
- **AND** the Reading List records `N`, the derived category counts, and a user-total derivation

#### Scenario: Count request is invalid or ambiguous
- **WHEN** the actor supplies a negative or fractional count, a zero total, category counts whose effective sum is zero, or both total and category count modes
- **THEN** the system requests clarification before discovery
- **AND** it does not invent, clamp, or silently prioritize a count

#### Scenario: Shorter result is a warning
- **WHEN** bounded discovery cannot identify enough suitable priority or secondary items to meet the effective target
- **THEN** the system records the reachable list, achieved counts, category deficits, and a non-blocking coverage warning against that target
- **AND** the actor may approve the shorter list or request further discovery

#### Scenario: Candidate is blocked during discovery
- **WHEN** a selected candidate cannot be accessed or its identity cannot be resolved
- **THEN** the system preserves the candidate and blocker in discovery provenance without counting it toward the applicable reachable target
- **AND** it performs bounded backfill before reporting any remaining coverage deficit

#### Scenario: Legacy list omits target metadata
- **WHEN** the system validates a Reading List created before configurable target metadata was recorded
- **THEN** it interprets the missing target as three priority items and three secondary items
- **AND** it does not require migration or mutation of the existing Artifact

#### Scenario: Different directions do not collide
- **WHEN** a topic contains reading lists for two accepted directions
- **THEN** each list uses the applicable direction scope key and independently records its effective target
- **AND** a target or item revision for one direction does not supersede the other direction's list

### Requirement: Reading-List Discovery Preserves Search and Identity Evidence
Reading-list construction SHALL search across papers, technical reports, source-code repositories, datasets, and models while treating papers and technical reports as the primary works.

#### Scenario: Paper retrieval uses the centralized owner
- **WHEN** reading-list discovery needs paper identity resolution, paper query, citing-paper search, cited-paper exploration, citation-neighborhood traversal, or adjacent-paper search
- **THEN** the discover skill invokes `isomer-ext-kaoju-entrypoint->paper-search` with the direction, query or seed, bounds, expected normalized fields, and evidence-use intent
- **AND** repositories, datasets, models, selection, target counts, and cross-source-class coverage remain owned by discover and their existing owners

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

### Requirement: Kaoju Updates Direction-linked Research Ideas Explicitly
Kaoju downstream work SHALL update a direction-linked canonical Research Idea only when an accepted output explicitly justifies the applicable exploration, evidence, decision, visibility, archive, or lineage effect.

#### Scenario: Focused direction research begins or completes
- **WHEN** an accepted Kaoju operation establishes that focused work began or completed for a direction-linked Research Idea
- **THEN** it records the justified `exploring` or `explored` transition with exact Research Task, Run, Artifact, Evidence Item, or Provenance Record refs
- **AND** it does not change decision or evidence state unless the same accepted output independently justifies that effect

#### Scenario: Audit or synthesis assesses direction evidence
- **WHEN** an accepted Kaoju audit, comparison, or synthesis explicitly assesses the evidence for a direction-linked Research Idea
- **THEN** it records the justified evidence-state transition and exact supporting and challenging refs
- **AND** support does not imply selection and refutation does not imply closure

#### Scenario: Discovery identifies a new conceptual direction
- **WHEN** accepted discovery, comparison, audit, or synthesis authors a durable concept that differs from the current direction
- **THEN** it creates a new Research Idea, exact Idea Realization, and justified `derived_from`, `follow_up_to`, `alternative_to`, `merged_from`, or other supported lineage edge
- **AND** it does not overwrite the parent direction or infer idea lineage from record lineage alone

#### Scenario: Survey material is not an idea
- **WHEN** Kaoju records a reading-list item, Source Identity, repository, dataset, model, comparison candidate, Research Claim, audit repair route, paper structure, section, or output Artifact
- **THEN** it preserves that object's existing canonical type and relationship to the applicable direction
- **AND** it does not create a Research Idea unless the actor or accepted profile explicitly promotes a distinct durable concept

