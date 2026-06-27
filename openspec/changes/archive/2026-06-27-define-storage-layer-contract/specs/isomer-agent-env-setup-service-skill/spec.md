## ADDED Requirements

### Requirement: Agent Env Setup Consumes Storage Contract
The Agent Workspace environment setup service SHALL resolve every target path through Workspace Path Resolution before mutating Git state, writing support files, or claiming readiness.

#### Scenario: Agent workspace setup uses resolved labels
- **WHEN** the service prepares an Agent Workspace for a planned Agent Name
- **THEN** it resolves `agent.workspace`, `agent.isomer_managed`, `agent.runtime`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, `agent.links`, and `agent.tmp` through Workspace Path Resolution

#### Scenario: Default worktree path is not assembled directly
- **WHEN** the service creates or validates a Git worktree
- **THEN** it uses the resolved `agent.workspace` path and resolved `topic.repos.main` path rather than assembling `agents/<agent-name>` and `repos/topic-main`

#### Scenario: Custom agent support label is accepted
- **WHEN** the Topic Workspace Manifest declares a valid agent-required `custom.*` support label needed by agent setup
- **THEN** the service resolves that label for each relevant Agent Name and reports path, source, `storage_profile` id, storage-profile-derived traits, and blockers

#### Scenario: Missing custom agent label blocks dependent setup
- **WHEN** agent setup material names a custom semantic label that is not valid in the effective catalog
- **THEN** the service reports a Workspace Path Resolution blocker and avoids mutating a guessed fallback directory

### Requirement: Agent Env Setup Preserves Path Source Evidence
The Agent Workspace environment setup service SHALL include path source evidence in readiness output for every semantic surface it uses.

#### Scenario: Readiness output names path sources
- **WHEN** setup readiness succeeds or partially succeeds
- **THEN** the output includes each semantic label used, resolved path, source, source detail, scope ref, `storage_profile` id, and storage-profile-derived traits

#### Scenario: Default layout profile source remains explicit
- **WHEN** an agent setup path comes from `isomer-default.v1`
- **THEN** the readiness output identifies the default layout profile source instead of presenting the concrete path as an authored contract
