## ADDED Requirements

### Requirement: Entrypoint Routes Topic Workspace Git Work
The public core entrypoint SHALL route optional local Topic Workspace tracking and optional remote Topic Workspace publication through protected member `topic-git`, whose logical id is `isomer-op-topic-workspace-git`.

#### Scenario: Local tracking request selects topic-git local
- **WHEN** a concrete request asks to initialize, inspect, plan, ignore, or commit local Source Topic Workspace root history
- **THEN** the entrypoint selects the applicable `isomer-op-entrypoint->topic-git->local()` child operation
- **AND** it does not infer remote publication intent

#### Scenario: Remote publication request selects topic-git publish
- **WHEN** a concrete request asks to prepare, inspect, plan, or synchronize a sanitized Topic Workspace remote publication
- **THEN** the entrypoint selects the applicable `isomer-op-entrypoint->topic-git->publish()` child operation
- **AND** it does not require or initialize local root tracking

#### Scenario: Ambiguous tracking request preserves the distinction
- **WHEN** a user asks to track or version a Topic Workspace without saying whether the goal is local history or remote publication
- **THEN** the entrypoint routes to Topic Git overall status and explains both independent opt-in layers before mutation

#### Scenario: Entrypoint does not select a Topic Git CLI family
- **WHEN** the entrypoint routes a Topic Git operation
- **THEN** it delegates to the protected skill rather than constructing an `isomer-cli project topic-git ...` command
- **AND** the protected skill uses Isomer CLI only for read-only context queries before direct Git execution
