# research-idea-steering Specification

## Purpose
TBD - synced from change add-research-idea-portfolio-workflow. Update Purpose after archive.
## Requirements
### Requirement: Explicit Research Idea Steering Actions
The system SHALL provide explicit actions for starting focused exploration of a Research Idea alongside current work or instead of named currently selected ideas.

#### Scenario: User explores an idea alongside current work
- **WHEN** a user invokes `Explore this idea` for a canonical Research Idea and supplies any required prompt context
- **THEN** the system records the target exploration state as `exploring`
- **AND** it creates or resolves an idea-focused Research Inquiry and bounded Research Task
- **AND** it does not change the decision state of other Research Ideas

#### Scenario: User explores an idea instead of current selections
- **WHEN** a user invokes `Explore instead` with a target Research Idea, the exact selected Research Idea ids being replaced, and a rationale
- **THEN** the system records a Decision Record whose option set contains the target and every named replaced idea
- **AND** it changes the target decision state to `selected` and exploration state to `exploring`
- **AND** it changes each named replaced idea to the user-confirmed disposition, defaulting to `deferred` rather than `closed`
- **AND** it creates or resolves an idea-focused Research Inquiry and bounded Research Task for the target

#### Scenario: No current selection is inferred
- **WHEN** `Explore instead` omits the selected Research Idea ids it intends to replace
- **THEN** the system rejects the request with an actionable validation error
- **AND** it does not infer replacements from graph selection, timestamps, generation membership, or a global selected status

### Requirement: Steering Mutation Is Atomic and Provenance-backed
The system SHALL record the canonical effects of one steering action atomically before attempting external actor dispatch.

#### Scenario: Steering mutation commits
- **WHEN** a valid steering action is accepted
- **THEN** one Workspace Runtime transaction records the Decision Record when required, decision option membership, state transitions, Research Inquiry or Research Task refs, Provenance Record refs, and planned handoff or dispatch state
- **AND** every created or changed object is linked by one operation id or equivalent idempotent correlation ref

#### Scenario: Canonical mutation fails
- **WHEN** any required Decision Record, option membership, state transition, Research Inquiry, Research Task, provenance, or planned dispatch write fails
- **THEN** the system rolls back all canonical effects of that steering action
- **AND** it does not dispatch a prompt to a topic research actor

#### Scenario: Duplicate request is retried
- **WHEN** a client retries a steering action with the same idempotency key and equivalent input
- **THEN** the system returns the original action result and durable refs
- **AND** it does not create duplicate decisions, transitions, tasks, or handoffs

#### Scenario: Concurrent state changed
- **WHEN** the action's expected index revision or expected idea states no longer match Workspace Runtime
- **THEN** the system returns a conflict with the current states and refs
- **AND** it performs no partial mutation

### Requirement: Closed and Deferred Ideas Require Explicit Reopening
The system SHALL require a user-confirmed reopening decision before steering work to an idea whose decision state is `closed` or `deferred`.

#### Scenario: User confirms reopening
- **WHEN** a user chooses to explore a closed or deferred idea and confirms a rationale
- **THEN** the system records a Decision Record and transition that reopen the idea before or within the same atomic steering operation
- **AND** the prior closure or deferral reason remains queryable

#### Scenario: Reopening is not confirmed
- **WHEN** a steering request targets a closed or deferred idea without the required confirmation or rationale
- **THEN** the system returns a confirmation requirement or policy Gate
- **AND** it does not change canonical idea state or dispatch work

### Requirement: Project Operator Routes Exact Steering Context
The Project Operator SHALL route an accepted steering action to the configured topic research actor with durable, unambiguous Research Idea context.

#### Scenario: Steering prompt is dispatched
- **WHEN** canonical steering effects commit and the configured topic research actor is available
- **THEN** the Project Operator sends an instruction containing the target `idea_id`, display key, title, summary, latest exact Idea Realization refs, Decision Record ref when present, Research Inquiry ref, Research Task ref, and the user's prompt
- **AND** the instruction does not depend on the actor inferring intent from a skill name or generated Markdown alone

#### Scenario: Adapter dispatch succeeds
- **WHEN** an execution adapter delivers the Project Operator instruction
- **THEN** Workspace Runtime records handoff or dispatch provenance and the accepted adapter result refs
- **AND** adapter-specific terms remain outside canonical Research Idea and GUI contracts

#### Scenario: Adapter dispatch is unavailable
- **WHEN** the configured topic research actor or execution adapter cannot accept the instruction after canonical steering effects commit
- **THEN** the system keeps the Decision Record, transitions, Research Inquiry, and Research Task durable
- **AND** it marks dispatch or handoff state pending or blocked with actionable diagnostics and an idempotent retry path

### Requirement: Steering Respects Gate Policy
Research Idea steering SHALL obey configured Gate policy without making unrelated inspection wait for the governed action.

#### Scenario: Gate is required
- **WHEN** configured policy requires a Gate for replacing current selected ideas, reopening a closed idea, or another governed steering consequence
- **THEN** the action records or returns the open Gate and pauses the governed mutation
- **AND** ordinary graph, timeline, detail, decision, and lineage inspection remains available

#### Scenario: Human action resolves ordinary choice
- **WHEN** the authenticated user explicitly confirms a steering choice and no additional policy Gate is required
- **THEN** the system can record the Decision Record and perform the action without adding a redundant approval step

### Requirement: Browsing and Steering Remain Separate
Project Web SHALL distinguish read-only idea browsing state from canonical Research Idea steering actions.

#### Scenario: User selects or filters ideas
- **WHEN** a user selects nodes, changes focus, applies a portfolio preset, filters facets, changes layout, opens details, or traverses lineage
- **THEN** the operation reports `mutated: false`
- **AND** it does not create a Decision Record, state transition, Research Inquiry, Research Task, Run, or handoff

#### Scenario: User invokes a steering action
- **WHEN** a user activates `Explore this idea` or `Explore instead`
- **THEN** Project Web presents the target, consequences, affected ideas, and required rationale before submitting the separate mutating action
- **AND** the action response returns created or changed durable refs and dispatch state

