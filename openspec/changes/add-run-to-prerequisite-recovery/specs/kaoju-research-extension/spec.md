## ADDED Requirements

### Requirement: Kaoju Pipeline Supports Authorized Run-To Recovery
The Kaoju pipeline SHALL keep each survey intent and compatibility procedure bounded while allowing a prompt-level controller to chain their producer and repair routes after explicit run-to authorization for a named target.

#### Scenario: Kaoju target lacks accepted artifacts
- **WHEN** a Kaoju target such as synthesis, drafting, PDF construction, comparison, or export lacks accepted prerequisite artifacts
- **AND** the required artifacts have known Kaoju or platform owner routes
- **THEN** the Kaoju pipeline's numbered workflow makes the bounded target report `paused` with exact missing semantic ids, producer routes, and resume point
- **AND** the user is offered inclusive run-to recovery before those producer routes execute

#### Scenario: Authorized Kaoju run-to chains bounded procedures
- **WHEN** the user authorizes run-to for a Kaoju target
- **THEN** the controller uses separate bounded Kaoju procedures to produce or repair the required inputs in dependency order
- **AND** it consumes each procedure's terminal report and accepted refs before selecting the next planned procedure or resuming the target
- **AND** every procedure retains its own Run, audit boundary, evidence semantics, and terminal report

#### Scenario: Kaoju audit recommends repair
- **WHEN** an audit procedure remains non-repairing and returns defects with bounded producer or repair routes inside an authorized target closure
- **THEN** the controller invokes those repair owners as separate procedures
- **AND** it starts a fresh audit after repair before allowing synthesis or paper writing to consume the repaired evidence

#### Scenario: Kaoju has no run-to authorization
- **WHEN** a bounded Kaoju procedure returns a terminal report without an active target-scoped run-to grant
- **THEN** the pipeline does not select another macro procedure autonomously
- **AND** it returns the recommended next procedure to the user as before

### Requirement: Kaoju Run-To Preserves Interaction and Gate Contracts
Kaoju run-to traversal SHALL automate only routine in-scope prerequisite routing and SHALL preserve every applicable clarification, Proceed Decision, resource, publication, and human Gate contract.

#### Scenario: Routine transitive prerequisite is discovered
- **WHEN** a Kaoju prerequisite procedure discovers another routine in-scope input needed for the same target
- **THEN** the controller adds the known producer route to the active plan without another routine confirmation
- **AND** the producer still resolves durable state through the state DB and writes through its typed Artifact bindings

#### Scenario: Kaoju traversal reaches a protected boundary
- **WHEN** the next stage requires a nondelegable Gate or a material choice that changes survey direction, evidence meaning, resource posture, or publication state
- **THEN** the controller checkpoints the active procedures and pauses
- **AND** it asks only for the decision needed to resume the named target
