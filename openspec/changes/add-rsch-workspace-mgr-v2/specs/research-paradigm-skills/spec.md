## ADDED Requirements

### Requirement: V2 Research Workspace Manager Skill
The research-paradigm skillset SHALL include an `isomer-rsch-workspace-mgr-v2` skill that performs research-specific Topic Workspace bootstrap after Topic Team Specialization and full Topic Workspace initialization.

#### Scenario: Workspace manager skill exists
- **WHEN** the v2 research-paradigm skillset is inspected
- **THEN** it contains `skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2/SKILL.md` with valid frontmatter, workflow, reference routing, fallback guidance, and an `agents/openai.yaml` manifest that invokes `$isomer-rsch-workspace-mgr-v2`

#### Scenario: Workspace manager runs after specialization
- **WHEN** the skill explains its entry conditions
- **THEN** it requires a selected Research Topic, a fully initialized Topic Workspace, completed Topic Team Specialization material, Workspace Runtime readiness, and Agent Workspace context before ordinary v2 research skills rely on its bootstrap outputs

#### Scenario: Workspace manager is distinct from operator topology management
- **WHEN** the skill describes its boundary
- **THEN** it states that `isomer-admin-topic-workspace-mgr` remains the operator topology helper while `isomer-rsch-workspace-mgr-v2` owns research placeholder binding and v2 storage bootstrap guidance

#### Scenario: Topic Service Master is optional
- **WHEN** the skill describes the actor that performs bootstrap
- **THEN** it names the Topic Service Master as the preferred topic-workspace manager when started and states that the Project Operator Session or Operator Agent performs the same bounded work when no Topic Service Master is running

### Requirement: V2 Research Storage Bootstrap Contract
The `isomer-rsch-workspace-mgr-v2` skill SHALL define consistent placeholders and outputs for research storage bootstrap, using the same placeholder registry style as the other v2 research skills.

#### Scenario: Manager placeholder registry exists
- **WHEN** `isomer-rsch-workspace-mgr-v2/migrate/placeholders.md` is inspected
- **THEN** it defines placeholders for workspace context, storage label planning, placeholder binding registry, storage bootstrap record, agent access plan, bootstrap validation report, and workspace blocker record

#### Scenario: Placeholder kinds use existing v2 storage mapping
- **WHEN** the manager placeholder registry is inspected
- **THEN** every placeholder has a `Kind` value from the existing v2 placeholder kind set and maps to the storage item mapping for evidence, report, handoff, decision, runtime state, or related accepted kinds

#### Scenario: Storage bootstrap names semantic labels
- **WHEN** the manager describes storage preparation
- **THEN** it names existing labels such as `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, and `topic.records.logs`, planned labels such as `topic.records.evidence`, `topic.records.provenance`, and `topic.records.packages`, and custom labels such as `custom.datasets.*` only when a placeholder needs distinct storage behavior

#### Scenario: Missing storage support becomes a blocker
- **WHEN** a required semantic label, directory, runtime record, or command surface is unavailable
- **THEN** the manager records a blocker placeholder instead of inventing a hard-coded path or claiming a missing storage surface exists

#### Scenario: Agent access plan preserves storage authority
- **WHEN** the manager prepares guidance for working agents
- **THEN** it uses `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links` as pre-promotion or convenience surfaces while preserving semantic labels and typed refs as the durable storage authority

### Requirement: Research Workspace Manager Validation
The research-paradigm validation harness SHALL recognize `isomer-rsch-workspace-mgr-v2` as an expected v2 skill and apply the normal v2 structure and placeholder checks to it.

#### Scenario: Validator expects workspace manager
- **WHEN** the research-paradigm validation harness runs against the repository skillset
- **THEN** it treats `isomer-rsch-workspace-mgr-v2` as part of the expected v2 skill set

#### Scenario: Validator checks manager placeholders
- **WHEN** active manager skill text uses migration placeholders
- **THEN** validation confirms those placeholders are registered in `isomer-rsch-workspace-mgr-v2/migrate/placeholders.md`
