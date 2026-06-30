## ADDED Requirements

### Requirement: Heavy Operation Classification Is Delegated Policy
The service environment setup enclosure workflow SHALL treat operation classification as delegated user-tunable policy from `isomer-misc-bounded-run-tips`.

#### Scenario: Shared enclosure policy consumes classification evidence
- **WHEN** topic env setup or agent env setup generates an operational env gate
- **THEN** the service guidance requires operation classification evidence from `isomer-misc-bounded-run-tips` before resource-check planning
- **AND** the generated gate records classification source, result, reason, and resource dimensions

#### Scenario: Core services avoid fixed normative heavy lists
- **WHEN** shared env setup policy describes resource-heavy work
- **THEN** it presents operation names only as examples
- **AND** it states that bounded-run tips owns the classification decision for the active project and host

#### Scenario: Classification remains separate from package and enclosure policy
- **WHEN** bounded-run tips classifies an operation as `heavy`, `unknown-risk`, `light`, or `not-applicable`
- **THEN** that classification controls resource-check and bounded-execution handling only
- **AND** dependency source choice, runtime wiring, Pixi enclosure, repository materialization, and privileged-operation blockers remain owned by their existing service policies
