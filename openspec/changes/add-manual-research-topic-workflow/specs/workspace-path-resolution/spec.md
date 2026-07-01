## ADDED Requirements

### Requirement: Effective Topic Actor Context Input
Workspace Path Resolution SHALL support an Effective Topic Actor Context for Topic Actor Workspace semantic labels.

#### Scenario: Explicit actor selector resolves actor path
- **WHEN** a user resolves an actor-scoped semantic label with an explicit Topic Actor selector
- **THEN** the resolver uses the selected Topic Actor binding from the Topic Workspace Manifest to resolve the actor-scoped path

#### Scenario: Actor context is separate from agent context
- **WHEN** a command resolves `topic.actors.workspace`
- **THEN** it uses Topic Actor context and does not require formal `agent_name`, Agent Instance id, Agent Workspace record, or Agent Team Instance record

#### Scenario: Agent labels still require agent context
- **WHEN** a command resolves `agent.workspace` or another formal agent-scoped label
- **THEN** it continues to use Effective Agent Context and does not accept a Topic Actor selector as a substitute for `agent_name` or Agent Instance identity

### Requirement: Topic Actor Context Discovery
Workspace Path Resolution SHALL discover Topic Actor context through deterministic sources.

#### Scenario: Actor context precedence is deterministic
- **WHEN** multiple actor context sources are available
- **THEN** the resolver prefers explicit Topic Actor selector, then actor environment variable, then cwd-derived Topic Actor Workspace, then lifecycle refs, then manifest default when exactly one active actor is marked as default

#### Scenario: Cwd under Topic Actor Workspace selects actor
- **WHEN** the current directory is inside a resolved Topic Actor Workspace
- **THEN** Topic path commands can infer the matching Topic Actor context and report the inferred `topic_actor_name` and source

#### Scenario: Conflicting actor context is rejected
- **WHEN** explicit, environment, cwd, or lifecycle actor context sources select different Topic Actors
- **THEN** path resolution reports a deterministic conflict diagnostic instead of choosing one silently

### Requirement: Topic Actor Path CLI Surface
The CLI SHALL expose actor-aware path queries for human-orchestrated workers.

#### Scenario: Actor workspace can be queried
- **WHEN** a user runs a path query for `topic.actors.workspace` with a Topic Actor selector
- **THEN** the CLI returns the resolved Topic Actor Workspace path, semantic label, path source, topic actor name, storage profile, and existence status

#### Scenario: Actor labels appear in configured label listings
- **WHEN** a user lists semantic paths for a selected Topic Workspace with a Topic Actor selector
- **THEN** actor-scoped labels are included with resolved paths and actor context metadata
