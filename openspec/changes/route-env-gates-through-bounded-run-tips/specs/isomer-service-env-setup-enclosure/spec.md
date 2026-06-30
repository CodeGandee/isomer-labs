## ADDED Requirements

### Requirement: Heavy Operation Resource Strategy Routes Through Bounded Run Tips First
The service environment setup enclosure workflow SHALL treat bounded-run tips as the first routing surface for resource-heavy setup and verification planning across topic env and agent env gates.

#### Scenario: Heavy-operation policy is shared
- **WHEN** topic env setup or agent env setup generates an operational env gate with a resource-heavy setup or verification item
- **THEN** the service guidance routes the item to `isomer-misc-bounded-run-tips` before using local generic resource judgment
- **AND** the generated gate records the bounded-run guidance source in its `Resource Check Plan`
- **AND** the gate records generic best-effort judgment only when no specific bounded-run guidance applies

#### Scenario: Bounded run guidance does not replace dependency policy
- **WHEN** a heavy operation also needs package installation, CUDA/C++ Pixi environment setup, NVIDIA runtime wiring, package repository resolution, or package-specific caveat handling
- **THEN** bounded-run tips provide only the resource-safe execution strategy
- **AND** package installation, runtime wiring, and repository source choices remain routed to their existing package-specific, NVIDIA, repository-resolution, and enclosure policy surfaces

#### Scenario: Readiness still requires real-path evidence
- **WHEN** a generated env gate includes a heavy source-intent path
- **THEN** readiness requires passing evidence from the bounded real-path command or a named blocker with resource evidence
- **AND** a smoke test that misses the critical build, inference, dataset, benchmark, or cwd command path does not satisfy the checklist item unless the user explicitly downgraded the gate
