## ADDED Requirements

### Requirement: Topic Workspace Identity for Agents and Actors
The CLI SHALL expose the selected Topic Workspace id to agents and Topic Actors running inside a Topic Workspace.

#### Scenario: Self identity includes Topic Workspace id
- **WHEN** an agent or Topic Actor runs `isomer-cli --print-json project self identity` from inside a registered Topic Workspace
- **THEN** the JSON output includes the selected `topic_workspace_id`
- **AND** it includes the selected `research_topic_id` and Topic Workspace path

#### Scenario: Self show includes compact Topic Workspace identity
- **WHEN** an agent or Topic Actor runs `isomer-cli --print-json project self show` from inside a registered Topic Workspace
- **THEN** the summary includes the selected Topic Workspace id
- **AND** it does not require the agent to parse Project Manifest TOML directly

#### Scenario: Topic Service Master identity is available to agents
- **WHEN** a selected Topic Workspace has suggested Topic Service Master names or a recorded binding
- **THEN** self/context output includes a Topic Service Master identity block with suggested names and current binding status
- **AND** the output omits credentials and live runtime state

#### Scenario: Environment-selected workspace is reported
- **WHEN** `ISOMER_TOPIC_WORKSPACE_ID` selects the Topic Workspace
- **THEN** self/context output reports the environment source
- **AND** downstream records store validated refs rather than treating the environment value as durable truth
