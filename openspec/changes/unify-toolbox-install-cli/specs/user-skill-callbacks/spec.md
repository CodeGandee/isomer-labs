## MODIFIED Requirements

### Requirement: Callback CLI Surface
The system SHALL expose a generic `isomer-cli project skill-callbacks` command group for User Skill Callback management, resolution, and lower-level callback-material operations that are not necessarily installed as full Toolbox bundles.

#### Scenario: Register command creates callback
- **WHEN** a user runs `isomer-cli project skill-callbacks register` with a target system skill, supported stage, scope, and exactly one source kind
- **THEN** the command validates the inputs, creates or updates the appropriate callback registry, and reports the callback id, target skill, stage, scope, status, and source summary

#### Scenario: Register command supports loose callback material
- **WHEN** a user has callback material that is not packaged as a Toolbox manifest
- **THEN** the `register` command provides the direct mutation path for prompt, prompt-file, or skill-directory callback sources

#### Scenario: Install command is a callback-manifest primitive
- **WHEN** a user runs the lower-level callback-manifest install operation for a Toolbox directory
- **THEN** the command installs or refreshes callback records from the Toolbox manifest without being the canonical high-level Toolbox bundle install surface

#### Scenario: Resolve command is read-only
- **WHEN** a user runs `isomer-cli project skill-callbacks resolve` for a system skill and callback stage
- **THEN** the command loads the selected Project and Effective Topic Context, returns the active callbacks in deterministic order, and does not mutate registry files or callback content

#### Scenario: List command summarizes callbacks
- **WHEN** a user runs `isomer-cli project skill-callbacks list`
- **THEN** the command lists callback ids, target skills, stages, scopes, statuses, priorities, and source summaries visible from the selected Project or topic context

#### Scenario: Show command displays one callback
- **WHEN** a user runs `isomer-cli project skill-callbacks show <callback-id>`
- **THEN** the command displays the matching callback metadata and source reference while preserving redaction rules for secret-like material

#### Scenario: Disable command deactivates callback
- **WHEN** a user runs `isomer-cli project skill-callbacks disable <callback-id>`
- **THEN** the command marks the callback inactive in its registry and reports the previous and new status

#### Scenario: Validate command checks registries
- **WHEN** a user runs `isomer-cli project skill-callbacks validate`
- **THEN** the command validates reachable callback registries, source paths, target system skill names, stages, duplicate active ids, status values, priority values, and redaction-sensitive fields
