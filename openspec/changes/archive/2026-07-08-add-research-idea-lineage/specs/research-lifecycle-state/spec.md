## ADDED Requirements

### Requirement: Research Idea Lifecycle Concept
The system SHALL define Research Idea as a durable conceptual research direction under a Research Topic, distinct from Research Inquiry, Research Task, Run, and Artifact.

#### Scenario: Research Idea is named in domain language
- **WHEN** the platform domain language is inspected
- **THEN** it defines Research Idea, Primary Idea, Idea Realization, and Idea Lineage Edge with clear relationships to Research Topic, Artifact, Decision Record, Evidence Item, Finding, and Research Claim

#### Scenario: Research Idea does not replace inquiry
- **WHEN** a conceptual direction is recorded as a Research Idea
- **THEN** the system does not require it to become a Research Inquiry unless the team also needs a question-level work decomposition or lifecycle route

#### Scenario: Primary Idea is visibility
- **WHEN** a Research Idea is marked primary
- **THEN** the system treats primary as a user-facing visibility role for default inspection rather than as a separate execution level

### Requirement: Research Idea Status
The system SHALL use explicit statuses for Research Ideas that preserve research history across selection, in-place updates, support, refutation, deferral, rejection, and archival.

#### Scenario: Idea status is explicit
- **WHEN** a Research Idea is inspected
- **THEN** its status is one of `raw`, `candidate`, `selected`, `active`, `supported`, `refuted`, `deferred`, `rejected`, `superseded`, or `archived`, or a later accepted contract has explicitly extended the status set

#### Scenario: Terminal ideas remain visible
- **WHEN** a Research Idea is rejected, deferred, refuted, superseded, or archived
- **THEN** the system keeps the idea visible for provenance, comparison, future reopening, or contradiction analysis instead of deleting it silently

#### Scenario: Idea status changes require explicit write
- **WHEN** an experiment result, analysis finding, claim verdict, or query diagnostic suggests a Research Idea status has changed
- **THEN** the system does not mutate the Research Idea status unless an agent, operator, repair command, or accepted record write explicitly records the status update

### Requirement: Research Idea Relationships
The system SHALL represent relationships between Research Ideas as durable lineage graph edges and shall not infer those relationships solely from generated Markdown.

#### Scenario: Idea relationship is recorded
- **WHEN** one Research Idea is derived from, selected from, merged from, follows up, alternates with, or subsumes another Research Idea
- **THEN** the system records a typed Research Idea relationship with source idea ref, target idea ref, relation type, rationale, status, and supporting Decision Record, Evidence Item, Artifact, Finding, or Provenance refs when known

#### Scenario: Idea update is not a relationship
- **WHEN** an accepted record revision updates the content of an existing Research Idea
- **THEN** the system updates the same Research Idea and its realization history rather than creating a new Research Idea relationship

#### Scenario: Generated prose is not authoritative
- **WHEN** rendered Markdown describes idea ancestry but no canonical idea relationship exists
- **THEN** lifecycle and graph validation treat the prose as review material and report that canonical idea lineage is missing rather than making the prose authoritative
