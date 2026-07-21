## MODIFIED Requirements

### Requirement: Research Idea Status
The system SHALL represent Research Idea state through independent exploration, decision, evidence, visibility, and archive facets that preserve research history across proposal, investigation, selection, support, refutation, deferral, closure, reopening, and archival.

#### Scenario: Idea state facets are explicit
- **WHEN** a Research Idea is inspected
- **THEN** its exploration state is one of `unknown`, `unexplored`, `exploring`, or `explored`
- **AND** its decision state is one of `unknown`, `open`, `shortlisted`, `selected`, `deferred`, or `closed`
- **AND** its evidence state is one of `unknown`, `unassessed`, `inconclusive`, `supported`, `mixed`, or `refuted`
- **AND** its archive state is one of `active` or `archived`
- **AND** its visibility remains one of `primary`, `supporting`, or `hidden`

#### Scenario: Independent facets can coexist
- **WHEN** an idea is selected before focused investigation, explored without being selected, supported but deferred, refuted but reopened, or archived after selection
- **THEN** the system preserves that combination across independent facets
- **AND** it does not collapse the combination into one authoritative status value

#### Scenario: Closure carries a reason
- **WHEN** a Research Idea transitions to decision state `closed`
- **THEN** the transition records a reason code, rationale, actor, timestamp, and Decision Record or Provenance Record ref
- **AND** rejection, supersession, duplication, invalidation, and user closure remain distinguishable reasons rather than separate overloaded lifecycle facets

#### Scenario: Idea facet transition is recorded
- **WHEN** an agent, operator, repair command, accepted record write, or user steering action changes a Research Idea facet
- **THEN** the system records the affected facet, previous value, next value, actor, timestamp, reason code, rationale, and applicable Decision Record, Gate, Evidence Item, Finding, Artifact, Research Task, Run, or Provenance Record refs

#### Scenario: One action changes multiple facets
- **WHEN** one accepted action changes more than one Research Idea facet or more than one Research Idea
- **THEN** every transition shares an operation id or equivalent correlation ref
- **AND** the transitions and required decision context are committed atomically

#### Scenario: Terminal ideas remain visible
- **WHEN** a Research Idea is deferred, closed, refuted, superseded by closure reason, or archived
- **THEN** the system keeps the idea visible for provenance, comparison, future reopening, or contradiction analysis instead of deleting it silently

#### Scenario: Idea state changes require explicit write
- **WHEN** an experiment result, analysis finding, claim verdict, record payload, or query diagnostic suggests a Research Idea state has changed
- **THEN** the system does not mutate any Research Idea facet unless an agent, operator, repair command, accepted canonical record write, or explicit user action records the transition

#### Scenario: Legacy classification is ambiguous
- **WHEN** a legacy Research Idea status does not justify one or more canonical facets
- **THEN** migration sets those facets to `unknown`
- **AND** validation and Project Web expose the idea as needing classification instead of guessing or hiding it

#### Scenario: Legacy status remains compatibility-only
- **WHEN** a compatibility client reads the deprecated Research Idea status during the migration window
- **THEN** the system returns a deterministic projection from canonical facets or the preserved legacy value when facets are not migrated
- **AND** new canonical mutation paths do not treat that compatibility value as the source of truth
