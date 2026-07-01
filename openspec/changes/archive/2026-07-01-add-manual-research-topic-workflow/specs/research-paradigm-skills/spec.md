## ADDED Requirements

### Requirement: Research Workspace Bootstrap Supports Actor Topology
The v2 research workspace bootstrap SHALL support base topic readiness, Topic Actor readiness, and optional formal team readiness as composable topology layers.

#### Scenario: Bootstrap accepts Topic Actor readiness
- **WHEN** `isomer-rsch-workspace-mgr-v2` or its successor runs for human-orchestrated research
- **THEN** it validates the selected Topic Workspace, Workspace Runtime, Research Topic overview, topic environment readiness, ready `topic.repos.main`, available research record labels, skill-local placeholder binding files, the topic-level placeholder binding index or readiness report, selected Topic Actor bindings, and selected Topic Actor Workspaces
- **AND** it does not require Topic Agent Team Profile material, formal Agent Workspace access plans, per-Agent Instance cwd proof, Agent Instance records, or Agent Team Instance records unless the selected topology includes a formal team layer

#### Scenario: Placeholder binding index points to skill-local authority
- **WHEN** research workspace bootstrap creates or validates a topic-level placeholder binding index
- **THEN** the index references relevant skill-local `placeholder-bindings.md` files and their selected placeholder groups
- **AND** the bootstrap treats skill-local files as authoritative when the index and skill-local binding content disagree

#### Scenario: Bootstrap keeps formal team checks when present
- **WHEN** the research workspace bootstrap runs in a Topic Workspace with formal team material selected for use
- **THEN** it keeps the existing post-specialization checks for topic team summary, profile material, formal Agent Workspace access, and worker-visible storage boundaries

### Requirement: V2 Skills Read Placeholder Bindings from Actor Workspaces
The v2 research skills SHALL use skill-local placeholder binding guidance to map workflow placeholders to Topic Workspace records from Topic Actor Workspaces, topic-main, or formal Agent Workspaces.

#### Scenario: Actor skill run resolves placeholders through bindings
- **WHEN** a Topic Actor runs a v2 research skill from its Topic Actor Workspace
- **THEN** the skill reads its `placeholder-bindings.md` and uses the listed record kind, semantic label, profile, topic actor metadata, and `isomer-cli ext research records` command shape for accepted research artifacts
- **AND** it does not replace workflow placeholders with hard-coded Topic Actor Workspace paths in `SKILL.md`

#### Scenario: Missing binding blocks accepted record write
- **WHEN** a v2 skill needs to write an accepted artifact but no binding exists for the placeholder
- **THEN** the skill reports the missing binding as a blocker instead of writing the artifact only to local scratch, a Topic Actor Workspace, a formal Agent Workspace, or an untracked repo path
