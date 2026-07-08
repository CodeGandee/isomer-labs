# topic-idea-iteration-fixture-data Specification

## Purpose
TBD - created by archiving change repair-flash-attention-topic-idea-iteration-data. Update Purpose after archive.
## Requirements
### Requirement: Repaired Topic Idea Iteration Fixture
The repaired Flash Attention Topic Workspace SHALL contain enough structured, topic-scoped data to render the topic idea iteration map without topic-specific GUI logic or generated Markdown parsing.

#### Scenario: Idea nodes are available
- **WHEN** a GUI or agent reads the repaired topic through query export, record detail, facets, and lineage APIs
- **THEN** it can identify raw idea slate items, serious candidate ideas, selected hypotheses, follow-up hypotheses, experiment outcomes, analysis conclusions, and route decisions with stable ids, concise text, status, source record id, producer or skill when known, and timestamps

#### Scenario: Serious candidates are durable
- **WHEN** a serious candidate from the historical candidate frontier is needed as a selectable idea node
- **THEN** the repaired topic stores that candidate in a durable structured record or an equally stable canonical runtime record with explicit idea id, family, one-liner, status, source candidate id, and source record refs

#### Scenario: Historical raw ideas remain inspectable
- **WHEN** the initial raw idea slate remains a multi-idea artifact
- **THEN** the repaired topic preserves the raw idea item ids and text in structured payload or normalized facets and does not require every raw idea item to become a separate lifecycle record

### Requirement: Idea Iteration Relationships
The repaired topic SHALL encode idea predecessor, successor, sibling, selection, rejection, revision, and follow-up relationships through structured metadata and canonical lineage.

#### Scenario: Selected path is traceable
- **WHEN** a caller inspects the selected combined predictor hypothesis
- **THEN** it can trace the path from raw idea slate to candidate frontier, selected serious candidate, pre-idea draft, selected hypothesis, experiment contract, run/result, analysis, and route decision

#### Scenario: Alternatives are visible
- **WHEN** a caller inspects the candidate frontier
- **THEN** it can distinguish selected, serious alternative, rejected, and deferred candidates with rationale or source decision refs when those were present in historical structured data

#### Scenario: Follow-up hypotheses are linked
- **WHEN** a caller inspects real-hardware validation, bottleneck-threshold calibration, bottleneck-saturation validation, or overlap-revision records
- **THEN** it can identify the prior hypothesis, result, analysis, or route decision that caused the follow-up

#### Scenario: Revisions stay linear
- **WHEN** a hypothesis, result, route decision, outline, draft, or final paper artifact has a later content-changing version
- **THEN** the repaired topic records a `revision_of` lineage edge from the immediate prior record to the later record

### Requirement: Idea Sibling Generation Groups
The repaired topic SHALL use canonical generation groups to represent sibling idea alternatives when durable records were produced from the same parent set.

#### Scenario: Serious candidate siblings are grouped
- **WHEN** serious candidate records C1, C2, and C3 are repaired from the candidate frontier
- **THEN** they share a generation group whose purpose describes the serious-candidate idea pass and whose lineage edges point back to the same parent set

#### Scenario: Sibling query works
- **WHEN** a caller asks for siblings of one repaired serious candidate through the current sibling query surface
- **THEN** the response returns the other candidates in the same generation group and reports no missing generation-group diagnostics

#### Scenario: Non-sibling follow-ups remain linear
- **WHEN** the topic contains a single follow-up hypothesis or amended result with no competing sibling alternative
- **THEN** the repaired topic records it with `follow_up_to` or `revision_of` lineage instead of inventing a generation group

### Requirement: Fixture Integrity for New Agents
The repaired topic SHALL look coherent to a new agent using the latest local `isomer-cli` and system skills.

#### Scenario: Validation is clean
- **WHEN** a new agent runs runtime validation, lineage validation, query-index validation, and idea export for the topic
- **THEN** the commands report no integrity errors and no missing-record, missing-generation-group, cross-topic, cycle, stale-index, or unsupported-relation diagnostics

#### Scenario: Read-only browsing does not repair
- **WHEN** the Project Web GUI or a new agent reads the topic through read-only APIs
- **THEN** the repaired topic does not require read-time rebuild, cleanup, backfill, or migration to produce the expected idea iteration data

#### Scenario: Repair provenance is explicit but non-disruptive
- **WHEN** a new agent inspects repaired records or lineage metadata
- **THEN** it can see repair provenance where useful without needing to special-case the data as manually generated

