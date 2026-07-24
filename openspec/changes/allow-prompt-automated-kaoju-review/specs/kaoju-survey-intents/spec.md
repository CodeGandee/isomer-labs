## MODIFIED Requirements

### Requirement: Kaoju Proposes and Records Survey Directions
The system SHALL derive candidate survey directions from the active Research Topic, SHALL return the final directions reviewed under the resolved human or prompt-delegated agent review mode as one current `KAOJU:DIRECTION-SET` record distinct from `KAOJU:SURVEY-CONTRACT`, and SHALL project every durable proposal concept into the canonical Research Idea portfolio as part of the accepted write.

#### Scenario: Agent proposes bounded directions
- **WHEN** the actor asks for useful next survey directions from a Research Topic
- **THEN** the frame skill proposes three distinct directions by default and explains their relationship to the topic
- **AND** each direction contains a stable direction id, stable canonical idea identity for new writes, title, scoped question, boundary, expected source classes, coverage date, expected evidence depth, and deliverables

#### Scenario: Human controls the selected set by default
- **WHEN** the actor reviews proposed directions and the prompt has not delegated direction review
- **THEN** the system permits multi-selection, non-selection without closure, explicit deferral, explicit closure, revision, and actor-authored custom directions
- **AND** it does not create the accepted Direction Set or promised canonical Research Idea effects until the actor confirms the authored option outcomes

#### Scenario: Prompt delegates direction review
- **WHEN** the current prompt explicitly delegates selection and acceptance of the proposed directions for the named target
- **THEN** the frame skill may revise proposals, choose one or more options, leave options open, defer or close options with justified reasons, and accept the resulting set without another user turn
- **AND** it records agent-review provenance, prompt basis, option outcomes, rationale, actor, and every required canonical Research Idea effect

#### Scenario: Current host affects empirical feasibility
- **WHEN** one or more proposed directions depend on empirical work whose feasibility varies with the current host hardware or environment
- **THEN** the system records a feasibility annotation with the relevant observed capability and limits
- **AND** it does not exclude or rank other directions solely because of the current host

#### Scenario: Direction set becomes discovery input
- **WHEN** the actor or explicitly delegated agent review accepts one or more directions
- **THEN** the system creates or revises the current `KAOJU:DIRECTION-SET` with selection provenance, a distinct stable entry for each direction, and the accepted canonical Research Idea refs
- **AND** downstream reading-list discovery consumes selected direction and idea refs rather than inferring directions from the Survey Contract, rendered output, or chat history

#### Scenario: Confirmed direction proposals enter the canonical portfolio
- **WHEN** a new idea-bearing Direction Set is accepted
- **THEN** the same transaction writes one canonical Research Idea per durable proposal, an exact Idea Realization to its object-valued `$.sections.proposals[<index>]` path, one proposal-generation group, the Direction Set Decision Record, every authored decision option, and all justified state transitions
- **AND** the accepted result returns those canonical refs for terminal verification and Project Web indexing

#### Scenario: Non-selected direction remains available
- **WHEN** a direction participates in the confirmed decision but the reviewing actor neither selects, defers, nor closes it
- **THEN** its decision option outcome records that it was not selected by this decision while its canonical decision state remains `open`
- **AND** the system does not treat non-selection as rejection, deferral, closure, archival, or evidence refutation

#### Scenario: Direction is explicitly deferred or closed
- **WHEN** the reviewing actor explicitly defers or closes a proposed direction
- **THEN** the accepted Direction Set records its outcome, rationale, actor, and applicable reason code and commits the corresponding canonical decision-state transition
- **AND** a closed direction has the required closure reason and remains queryable for GUI review and later reopening

#### Scenario: Direction revision preserves or changes concept identity
- **WHEN** an accepted Direction Set revision changes wording, boundary detail, evidence depth, or deliverables without changing the direction concept
- **THEN** it retains the same `idea_id` and adds or refreshes an Idea Realization without creating an idea-level `revision_of` edge
- **AND** a concept-changing replacement creates a new Research Idea with explicit justified idea lineage while record revision lineage remains separate

#### Scenario: Kaoju operates without DeepSci
- **WHEN** a Topic Workspace installs Kaoju without the optional DeepSci extension
- **THEN** Kaoju resolves the paradigm-neutral Research Idea Recording contract and completes the same canonical writes and validation
- **AND** no Kaoju skill depends on `isomer-deepsci-shared` or a DeepSci payload profile

### Requirement: Actors Can Inspect, Refine, and Approve Reading Lists
The system SHALL expose reading-list inspection and revision before the list becomes accepted input to deep ingestion and SHALL resolve acceptance through human review by default or explicit prompt-delegated agent review.

#### Scenario: Actor inspects a reading list
- **WHEN** the actor asks to inspect a direction's reading list
- **THEN** the system queries the scoped current artifact from the state DB and presents identity, source class, priority, relevance, access posture, version family, and provenance for each item

#### Scenario: Actor revises selection
- **WHEN** the actor requests additions, removals, reprioritization, or another bounded discovery pass
- **THEN** the system creates a reading-list revision with lineage to the prior list
- **AND** prior accepted or rejected entries retain their dispositions and rationale

#### Scenario: Human review remains the default
- **WHEN** a Reading List is ready and the current prompt has not delegated its review
- **THEN** the system presents it for actor approval
- **AND** it does not make selected item refs eligible for `ingest-reading-item` before approval

#### Scenario: Prompt delegates reading-list review
- **WHEN** the current prompt explicitly delegates refinement and acceptance of the Reading List for the named direction or target
- **THEN** the discover skill may inspect, revise, accept a justified shortage, and approve the list without another user turn
- **AND** it records agent-review provenance, prompt basis, rationale, target and achieved counts, warnings, and accepted item refs

#### Scenario: Reviewing actor approves ingestion input
- **WHEN** the human actor or explicitly delegated agent review approves the Reading List
- **THEN** the system records acceptance metadata and makes its selected item refs eligible for `ingest-reading-item`
- **AND** unapproved list drafts are not treated as accepted synthesis evidence
