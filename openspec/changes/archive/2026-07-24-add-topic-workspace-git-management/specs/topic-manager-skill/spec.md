## ADDED Requirements

### Requirement: Topic Manager Delegates Topic Git Requests
The Topic Manager skill SHALL delegate explicit Source Topic Workspace local tracking and remote publication requests to `isomer-op-entrypoint->topic-git` without changing ordinary initialized-topic topology.

#### Scenario: Local Git request is delegated
- **WHEN** an initialized-topic management request asks to initialize root Git, choose local files to commit, update the root `.gitignore`, or create a local root commit
- **THEN** Topic Manager preserves selected context and routes to the Topic Git local operation group

#### Scenario: Publication request is delegated
- **WHEN** an initialized-topic management request asks to create a sanitized for-push copy, configure its remote, convert nested workspaces into publication submodules, or synchronize and push it
- **THEN** Topic Manager preserves selected context and routes to the Topic Git publish operation group

#### Scenario: Ordinary topic management remains unchanged
- **WHEN** Topic Manager performs storage, actor, team, environment, reset, or diagnostic work without explicit Topic Git intent
- **THEN** it does not initialize local tracking, create a Topic Publication Copy, or contact a publication remote

#### Scenario: Topic Manager does not wrap Git in Isomer CLI
- **WHEN** Topic Manager delegates a Topic Git request
- **THEN** it does not route to or introduce an Isomer CLI Git mutation command
- **AND** the Topic Git skill obtains Isomer information through read-only queries and runs Git directly
