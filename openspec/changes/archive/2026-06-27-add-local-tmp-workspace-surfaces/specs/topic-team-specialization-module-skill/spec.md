## ADDED Requirements

### Requirement: Topic Team Specialization Preserves Tmp Boundary
The Topic Team Specialization skill SHALL require delegated Git-backed workspace setup evidence to preserve the local tmp-label non-sharing contract.

#### Scenario: Setup evidence includes tmp contract
- **WHEN** `setup-agent-workspace` records delegated topic workspace manager evidence for Git-backed worktrees
- **THEN** the evidence includes whether `topic.main_repo.tmp` and `agent.tmp` surfaces are ignored and local-only
- **AND** it reports blockers when delegated setup found tracked tmp contents or missing ignore policy

#### Scenario: Validation rejects tmp as readiness evidence
- **WHEN** `validate-topic-team` inspects Agent Workspace setup evidence
- **THEN** it does not accept files under resolved tmp labels as durable readiness evidence, profile material, handoff material, generated-link material, or Peer Read Access

#### Scenario: Final summary separates tmp from sharing
- **WHEN** `finalize-topic-team` summarizes Agent Workspace layout
- **THEN** it distinguishes ignored local tmp labels from Git-tracked material, agent-owned public shares, topic-owned projections, generated links, and owner-preserved records

## MODIFIED Requirements

### Requirement: Static Readiness Checks Semantic Bindings
The Topic Team Specialization skill SHALL validate static setup using semantic path evidence before reporting the topic team as ready.

#### Scenario: Tmp posture is required only as local setup evidence
- **WHEN** Git-backed Agent Workspaces were requested
- **THEN** `validate-topic-team` requires delegated tmp posture evidence from the workspace setup flow
- **AND** it does not treat tmp contents as static material readiness
