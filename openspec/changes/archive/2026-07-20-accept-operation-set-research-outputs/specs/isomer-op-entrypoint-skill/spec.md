## ADDED Requirements

### Requirement: Entrypoint Routes Operation Set Acceptance
`isomer-op-entrypoint` SHALL make operation-set inspection, acceptance, verification, and legacy repair discoverable through the focused core recording skill and research CLI family.

#### Scenario: Research output closeout selects focused skill
- **WHEN** a user asks to persist, reconcile, close, verify, or repair files in a worker operation set
- **THEN** the entrypoint routes to `isomer-research-operation-set-recording` and proceeds with that workflow when context is sufficient

#### Scenario: Explicit CLI request uses operation-set commands
- **WHEN** a user explicitly asks for the CLI surface
- **THEN** entrypoint guidance names `isomer-cli ext research operation-sets inspect`, `accept`, and `verify` and preserves preview-before-apply behavior

#### Scenario: Project manager does not own research semantics
- **WHEN** an operation-set task requires record kinds, semantic bindings, artifact lineage, or Research Idea effects
- **THEN** the entrypoint does not treat generic Project lifecycle management as the recording authority

#### Scenario: Entrypoint validation checks route coverage
- **WHEN** operator skill validation inspects entrypoint research routes
- **THEN** it reports missing focused-skill or operation-set CLI coverage and stale guidance that treats plain worker files as accepted records
