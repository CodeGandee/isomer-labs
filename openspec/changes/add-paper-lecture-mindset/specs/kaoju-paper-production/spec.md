## MODIFIED Requirements

### Requirement: Paper Drafting Requires Accepted Audit and Synthesis
The system SHALL start canonical paper drafting only from an accepted Audit Report and the exact accepted synthesis revisions needed for the paper, including the complete active lecture-section commitment inventory.

#### Scenario: Required inputs are ready
- **WHEN** `draft-paper` resolves an accepted Audit Report, Field Summary, Related-Work Catalog, and Claim Status Table for the requested paper line
- **THEN** it records those exact revisions as paper input refs
- **AND** it reconciles every active, blocked, or explicitly superseded lecture-section commitment carried by the accepted synthesis
- **AND** optional source digests, ledgers, dossiers, comparisons, and trial results are included only when they have the required accepted audit disposition

#### Scenario: Required input is missing or ambiguous
- **WHEN** a required input or lecture-section commitment inventory is missing, unaudited, stale, or has competing accepted candidates
- **THEN** drafting pauses with the affected refs and required resolution
- **AND** the system does not recover by parsing an arbitrary rendered Markdown file, inferring lecture intent from prose, or choosing solely by timestamp

#### Scenario: Accepted synthesis has no lecture commitments
- **WHEN** the exact accepted synthesis explicitly contains no active or blocked lecture-section commitments
- **THEN** drafting proceeds under the existing adaptive structure and evidence rules without inventing a dedicated paper section
- **AND** deep-dive, full-text, citation frequency, or paper prominence does not imply `paper.lecture`

## ADDED Requirements

### Requirement: Lecture-Read Papers Receive Dedicated Detailed Sections
For every active lecture-section commitment in accepted synthesis, Kaoju paper production SHALL create and preserve one dedicated, substantial, evidence-grounded section that enables the intended reader to understand the paper's method without consulting the original paper for basic method comprehension.

#### Scenario: Paper structure includes an active lecture commitment
- **WHEN** `isomer-kaoju-write` creates or revises `KAOJU:PAPER-STRUCTURE-MYST` from accepted synthesis containing an active lecture-ready commitment
- **THEN** it maps that paper to one dedicated named section with the paper as the primary subject and records the Source Digest, lecture Run, section job, evidence boundary, required equation jobs, and required display jobs
- **AND** it does not satisfy the commitment with only a citation, list item, short shared related-work paragraph, or an unnamed placeholder

#### Scenario: Dedicated lecture section is drafted
- **WHEN** the write skill fills a dedicated lecture section in `KAOJU:PAPER-DRAFT-MYST`
- **THEN** the section explains the paper's survey role, problem and prerequisites, definitions and notation, core intuition, ordered method or architecture, applicable worked trace, essential equations and displays, supporting results, comparison, limitations, failure modes, and unresolved boundaries from accepted evidence
- **AND** the explanation is detailed enough for standalone method comprehension while identifying the original paper as the authority for full proof, audit, and reproduction

#### Scenario: Essential equation is included
- **WHEN** the lecture exposition identifies an equation as essential to method comprehension
- **THEN** writing authors the equation in canonical MyST, defines every used symbol, explains its role and interpretation, and records exact source and accepted evidence refs in `KAOJU:CITATION-MAP`
- **AND** it does not copy an equation without the surrounding assumptions, notation, or qualification needed to interpret it

#### Scenario: Essential figure or table is included
- **WHEN** the lecture exposition identifies a figure or table for treatment `reproduce`, `adapt`, or `redraw` and accepted handling evidence permits that treatment
- **THEN** writing creates a separate file-backed `KAOJU:PAPER-DISPLAY`, references it through a typed MyST placeholder, and records its teaching role, source, transformation posture, caption or interpretation status, insertion locator, and evidence refs in `KAOJU:CITATION-MAP`
- **AND** the paper does not embed an untracked source asset or imply that an adapted or redrawn display is the original

#### Scenario: Essential display cannot be reproduced
- **WHEN** direct reproduction is unsupported but accepted evidence supports adaptation, redraw, or textual description
- **THEN** writing uses the supported treatment while preserving the display's required teaching role and attribution
- **AND** it does not omit the underlying explanation merely because the original asset cannot be embedded

#### Scenario: A media type is not applicable
- **WHEN** accepted lecture evidence establishes that a paper has no pedagogically necessary equation, figure, table, or worked trace of one type
- **THEN** the section may omit that type with the not-applicable rationale and evidence retained in its structure or citation state
- **AND** the workflow does not fabricate content or impose a fixed media count

#### Scenario: Lecture commitment remains blocked
- **WHEN** accepted synthesis carries a blocked lecture commitment or required evidence cannot support the dedicated section
- **THEN** writing pauses acceptance of the affected structure or retains an explicit unresolved section obligation with the missing evidence, display, interpretation, or authorization and its recovery route
- **AND** it does not silently omit, merge, shorten, or represent the affected paper as having received lecture-level treatment

#### Scenario: Lecture commitment was explicitly superseded
- **WHEN** accepted synthesis contains an actor-approved supersession that names the prior lecture Run or Source Digest and records its rationale and provenance
- **THEN** writing may omit or change the dedicated section according to the replacement posture while preserving the supersession ref in the paper contract and revision history
- **AND** a later shorter draft, non-lecture reading Run, or structure preference does not count as supersession

#### Scenario: Lecture section is validated and revised
- **WHEN** a dedicated lecture section is accepted or later revised
- **THEN** paper validation checks its section job, source and claim refs, equation coverage, display placeholders, limitations, readiness blockers, and Citation Map entries
- **AND** `KAOJU:PAPER-REVISION-LOG` records the affected commitment, input revisions, section changes, actor rationale, and validation result
