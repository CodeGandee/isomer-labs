## ADDED Requirements

### Requirement: Worker Output Policy Manifest Fields
The Topic Workspace Manifest SHALL support user configuration for Topic Actor and Agent worker output roots and post-operation commit preference without requiring users to edit generated output paths directly.

#### Scenario: Topic Actor binding can configure output policy
- **WHEN** a Topic Actor binding declares a worker output root or `commit_after_operation`
- **THEN** manifest loading preserves those fields as part of the Topic Actor's effective output policy
- **AND** topic actor inspection output exposes the effective output policy source and value

#### Scenario: Agent output defaults can be configured
- **WHEN** the Topic Workspace Manifest declares Agent output defaults
- **THEN** Agent Workspace setup and output-policy resolution use those defaults for agents that do not have an explicit override

#### Scenario: Agent output override can be configured
- **WHEN** the Topic Workspace Manifest declares an Agent-specific output root or `commit_after_operation` override
- **THEN** output-policy resolution uses the override for that Agent
- **AND** other Agents continue to use the applicable default policy

#### Scenario: Commit preference is boolean
- **WHEN** a manifest declares `commit_after_operation`
- **THEN** manifest validation accepts only a boolean value
- **AND** missing values resolve to the configured default or false

### Requirement: Worker Output Root Validation
The Topic Workspace Manifest SHALL validate configured worker output roots against worker workspace boundaries before exposing them through output-policy resolution.

#### Scenario: Relative output root is accepted
- **WHEN** a configured worker output root is a relative path beneath the selected Topic Actor or Agent Workspace
- **THEN** manifest validation accepts the path if all other storage safety checks pass

#### Scenario: Unsafe output root is rejected
- **WHEN** a configured worker output root is absolute, contains parent traversal, resolves inside `.isomer-labs/`, resolves outside the selected worker workspace, or resolves into another Research Topic's Topic Workspace
- **THEN** manifest validation rejects the binding before the path is exposed to agents

#### Scenario: Shared output root risk is diagnosed
- **WHEN** a configured default worker output root does not include a worker identity segment such as `{topic_actor_name}` or `{agent_name}`
- **THEN** manifest validation reports a merge-conflict risk diagnostic unless the configuration explicitly accepts a shared output root

### Requirement: Worker Output Materialization
Topic Actor materialization and Agent Workspace setup SHALL materialize the resolved worker output root and preserve generated Git ignore behavior without forcing output files to be tracked.

#### Scenario: Default output root is materialized for Topic Actor
- **WHEN** a Topic Actor Workspace is materialized
- **THEN** the system materializes the resolved default or configured worker output root for that actor
- **AND** it records or reports the root as part of the actor's support paths

#### Scenario: Default output root is materialized for Agent Workspace
- **WHEN** an Agent Workspace is created or repaired
- **THEN** the system materializes the resolved default or configured worker output root for that Agent
- **AND** it records or reports the root with the Agent Workspace support paths

#### Scenario: Git ignore remains source of tracking truth
- **WHEN** materialization prepares a worker output root
- **THEN** it does not add tracked placeholder files merely to force the directory into Git
- **AND** generated or user-edited `.gitignore` rules remain the source of truth for whether generated output files are tracked
