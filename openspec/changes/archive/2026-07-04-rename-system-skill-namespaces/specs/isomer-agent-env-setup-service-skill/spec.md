## ADDED Requirements

### Requirement: Agent Environment Service Keeps Protected Namespace
The Agent Workspace environment setup service SHALL keep the `isomer-srv-agent-env-setup` active skill name while routing user-facing control through operator skills.

#### Scenario: Service name remains stable
- **WHEN** the service skill bundle is inspected after the namespace rename
- **THEN** the folder name, `SKILL.md` frontmatter, agent metadata, and manifest path continue to use `isomer-srv-agent-env-setup`

#### Scenario: Repair routes use current service names
- **WHEN** `isomer-srv-agent-env-setup` finds missing, stale, blocked, or failed Topic Workspace dependency readiness
- **THEN** it reports a repair next action naming `isomer-srv-topic-env-setup`

#### Scenario: Operator-facing follow-up uses op names
- **WHEN** agent environment setup guidance names an operator follow-up for package mutation, topic management, or verification routing
- **THEN** it uses `isomer-op-topic-mgr` rather than old `isomer-admin-topic-mgr`

### Requirement: Agent Environment Service Uses Current Helper Names
The Agent Workspace environment setup service SHALL keep consuming public misc helpers by their stable `isomer-misc-*` names.

#### Scenario: Resource classification helper name remains stable
- **WHEN** agent environment setup classifies heavy or unknown-risk per-agent cwd verification work
- **THEN** it consults `isomer-misc-bounded-run-tips`

#### Scenario: Package-specific helper name remains stable
- **WHEN** per-agent cwd readiness depends on package-specific runtime verification behavior
- **THEN** `isomer-srv-agent-env-setup` consults or consumes `isomer-misc-pkg-specifics` evidence
