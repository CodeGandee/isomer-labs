## MODIFIED Requirements

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

## ADDED Requirements

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
