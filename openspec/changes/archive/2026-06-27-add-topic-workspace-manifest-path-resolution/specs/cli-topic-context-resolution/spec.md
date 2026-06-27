## ADDED Requirements

### Requirement: Effective Agent Context
The system SHALL resolve an Effective Agent Context for agent-scoped commands and semantic path queries when enough validated agent identity information is available.

#### Scenario: Explicit agent selector wins
- **WHEN** a user provides an explicit Agent Name, Agent Workspace, or Agent Instance selector for an agent-scoped command
- **THEN** the system uses that selector before checking environment context or cwd inference

#### Scenario: Environment agent context is used
- **WHEN** no explicit agent selector is provided and supported agent identity environment variables select an Agent Name, Agent Workspace, or Agent Instance
- **THEN** the system uses the environment context after validating it against the selected Topic Workspace

#### Scenario: Cwd inside Agent Workspace infers agent
- **WHEN** no explicit or environment agent context is provided
- **AND** `isomer-cli` runs from a cwd inside a known Agent Workspace for the selected Topic Workspace
- **THEN** the system infers Effective Agent Context from that Agent Workspace

#### Scenario: Missing agent context is explicit
- **WHEN** an agent-scoped command cannot resolve explicit, environment-derived, cwd-derived, or recorded agent context
- **THEN** the system reports that the command requires an Agent Name or Agent Instance selector

### Requirement: Cwd-derived Agent Workspace Matching
The system SHALL infer agent context from cwd only when cwd matches a known or uniquely derivable Agent Workspace.

#### Scenario: Runtime path plan match wins
- **WHEN** Workspace Runtime contains Agent Workspace path plans and cwd is inside exactly one recorded Agent Workspace path
- **THEN** cwd inference uses the matching Agent Workspace record and may expose both Agent Name and Agent Instance id

#### Scenario: Manifest template match is used without runtime
- **WHEN** Workspace Runtime has no matching Agent Workspace record and the Topic Workspace Manifest has a unique `agent.workspace` template that matches cwd
- **THEN** cwd inference may derive Agent Name from the template without claiming an Agent Instance id

#### Scenario: Manifest template captures one agent segment
- **WHEN** cwd inference uses a manifest `agent.workspace` template
- **THEN** the system canonicalizes cwd and the template, captures exactly one path segment for `{agent_name}`, and treats the instantiated template path as the Agent Workspace root

#### Scenario: Unsupported template does not infer cwd agent
- **WHEN** a manifest `agent.workspace` template has no `{agent_name}` placeholder, more than one `{agent_name}` placeholder, or a placeholder that would capture multiple path segments
- **THEN** cwd-derived agent inference reports that the template cannot be used for reverse matching instead of guessing

#### Scenario: Default layout match is used when applicable
- **WHEN** no runtime or manifest match exists and the default layout profile is active
- **THEN** cwd inside `<topic-workspace>/agents/<agent-name>` may derive Agent Name from the default Agent Workspace path shape

#### Scenario: Topic Main Repository is not an Agent Workspace
- **WHEN** cwd is inside the Topic Main Repository owner checkout such as `repos/topic-main`
- **THEN** the system does not infer Effective Agent Context from cwd

#### Scenario: Nested cwd keeps owning agent
- **WHEN** cwd is inside a subdirectory of one Agent Workspace
- **THEN** cwd inference resolves to that owning Agent Workspace rather than requiring cwd to equal the workspace root

### Requirement: Agent Context Conflict Handling
The system SHALL report conflicts between explicit selectors, environment context, cwd inference, and runtime records instead of silently guessing.

#### Scenario: Explicit selector overrides cwd
- **WHEN** cwd is inside Agent Workspace `alice` and the user explicitly selects Agent Name `bob`
- **THEN** the command uses `bob` and reports source metadata showing the explicit selector won

#### Scenario: Environment and cwd conflict blocks implicit selection
- **WHEN** environment context selects Agent Name `alice` and cwd inference selects Agent Name `bob`
- **AND** the user does not provide an explicit agent selector
- **THEN** the system reports an agent context conflict diagnostic

#### Scenario: Ambiguous cwd match is rejected
- **WHEN** cwd matches more than one active Agent Workspace binding with incompatible Agent Names or Agent Instance ids
- **THEN** the system rejects cwd-derived agent context as ambiguous

#### Scenario: Cross-topic cwd conflict is rejected
- **WHEN** cwd matches an Agent Workspace under a different registered Topic Workspace than the selected Topic Workspace
- **THEN** the system reports a context mismatch instead of using the other topic's agent context

### Requirement: Effective Agent Context Output
The CLI SHALL expose agent context source metadata when a command resolves or displays Effective Topic Context.

#### Scenario: Context show reports inferred agent
- **WHEN** `isomer-cli project context show` runs from inside a known Agent Workspace and no explicit agent selector is supplied
- **THEN** the output includes the inferred Agent Name, Agent Workspace path, source `cwd`, and Agent Instance id when runtime records provide it

#### Scenario: Path query reports agent source
- **WHEN** an agent-scoped semantic path query resolves by cwd inference
- **THEN** the result includes the resolved Agent Name and source `cwd`

#### Scenario: Topic-only context remains topic-only
- **WHEN** cwd is inside a Topic Workspace but not inside an Agent Workspace
- **THEN** Effective Topic Context may be resolved without adding Effective Agent Context
