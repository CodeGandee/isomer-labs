## ADDED Requirements

### Requirement: Agent Self Query Context Packet
The system SHALL expose a process-local self query packet that composes Effective Topic Context, Topic Actor context, Effective Agent Context, recognized Isomer launch environment inputs, selected semantic paths, and Pixi execution hints without mutating Project, Topic Workspace, Workspace Runtime, launch material, or filesystem targets.

#### Scenario: Self query resolves topic from topic-main cwd and agent from environment
- **WHEN** `isomer-cli --print-json project self show` runs from inside the selected Topic Main Development Repository
- **AND** supported launch environment variables provide `ISOMER_RESEARCH_TOPIC_ID` and `ISOMER_AGENT_INSTANCE_ID` or `ISOMER_AGENT_NAME`
- **THEN** the self query packet includes the selected Effective Topic Context
- **AND** the packet includes Effective Agent Context with source metadata showing the environment or runtime-derived source
- **AND** the command does not infer Agent Workspace identity from the Topic Main Development Repository cwd

#### Scenario: Self query reports topic actor context
- **WHEN** supported environment variables, cwd, recorded context, or a single manifest default identify a Topic Actor
- **THEN** the self query packet includes the resolved Topic Actor name, workspace path, binding metadata when available, and source metadata

#### Scenario: Self query degrades without agent identity
- **WHEN** Effective Topic Context resolves but no explicit, environment-derived, cwd-derived, or recorded Effective Agent Context is available
- **THEN** the self query packet remains read-only and returns the topic context plus `agent` identity as unresolved
- **AND** it reports how to provide `--agent`, `--agent-instance`, `ISOMER_AGENT_NAME`, or `ISOMER_AGENT_INSTANCE_ID`

#### Scenario: Self query reports conflicts instead of guessing
- **WHEN** environment identity, explicit selectors, cwd inference, recorded runtime refs, or manifest defaults conflict
- **THEN** the self query reports diagnostics that name the conflicting sources
- **AND** it does not silently choose an Agent Name, Agent Instance, Topic Actor, Research Topic, or Topic Workspace from the conflicting inputs

#### Scenario: Self query reports only recognized safe environment inputs
- **WHEN** the process environment contains supported Isomer identity, path, or non-secret configuration variables
- **THEN** the self query packet reports the recognized variable names, values for safe non-secret refs, and whether each value influenced resolution
- **AND** it does not include arbitrary environment variables, credentials, tokens, API keys, passwords, or secret-like values

### Requirement: Agent Self Query Path and Pixi Summary
The system SHALL include a curated path and Pixi summary in the self query packet so coding agents can run commands and query detailed paths without hardcoding topic-specific values.

#### Scenario: Self query includes safe semantic path summary
- **WHEN** Effective Topic Context resolves
- **THEN** the self query packet includes resolved topic-scoped semantic paths for `topic.repos.main`, `topic.runtime`, and `topic.records` when available
- **AND** when Effective Agent Context resolves, it includes resolved agent-scoped paths for `agent.workspace`, `agent.private_artifacts`, `agent.scratch`, and `agent.logs` when available
- **AND** each path entry includes the semantic label, resolved path, source, storage profile metadata when available, and diagnostics

#### Scenario: Self query includes follow-up query commands
- **WHEN** the self query packet is produced
- **THEN** it includes safe follow-up command examples for `project context show`, `project paths get <semantic-label>`, `project paths explain <semantic-label>`, `project topic-actors show`, and topic or runtime inspection commands as applicable
- **AND** the command examples use `--print-json`

#### Scenario: Self query returns Pixi run hint for selected topic environment
- **WHEN** the selected Research Topic has a resolvable Project-root Pixi environment binding or standalone Topic Workspace Pixi binding
- **THEN** the self query packet includes the selected Pixi manifest path, Pixi environment name, binding source, and a Python command form using `pixi run --manifest-path <manifest_path> --environment <pixi_environment> python ...`

#### Scenario: Self query does not guess across ambiguous Pixi bindings
- **WHEN** multiple active Pixi bindings are available and no single binding can be selected for the self query
- **THEN** the self query packet reports the candidate bindings and a diagnostic instead of emitting a misleading single `pixi run` command

#### Scenario: Self query reports missing Pixi binding clearly
- **WHEN** no usable Pixi manifest or environment can be resolved for the selected topic
- **THEN** the self query packet includes a diagnostic and points the caller to `project doctor` or topic environment setup rather than using system Python or a local virtual environment
