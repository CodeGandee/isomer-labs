## MODIFIED Requirements

### Requirement: Callback CLI Surface
The system SHALL expose a generic `isomer-cli project skill-callbacks` command group for User Skill Callback management, resolution, and callback insertion-point discovery.

#### Scenario: Register command creates callback
- **WHEN** a user runs `isomer-cli project skill-callbacks register` with a target system skill, supported stage, scope, and exactly one source kind
- **THEN** the command validates the inputs, creates or updates the appropriate callback registry, and reports the callback id, target skill, stage, scope, status, and source summary

#### Scenario: Resolve command is read-only
- **WHEN** a user runs `isomer-cli project skill-callbacks resolve` for a system skill and callback stage
- **THEN** the command loads the selected Project and Effective Topic Context, returns the active callbacks in deterministic order, and does not mutate registry files or callback content

#### Scenario: List command summarizes callbacks
- **WHEN** a user runs `isomer-cli project skill-callbacks list`
- **THEN** the command lists callback ids, target skills, stages, scopes, statuses, priorities, and source summaries visible from the selected Project or topic context

#### Scenario: Insertion-points command lists meaningful points by default
- **WHEN** a user runs `isomer-cli project skill-callbacks insertion-points`
- **THEN** the command lists manifest-declared callback insertion points for core system skills and Project-declared operator system extensions
- **AND** the command does not claim that optional extension skill files were filesystem-verified

#### Scenario: Insertion-points command supports explicit catalog filters
- **WHEN** a user runs `isomer-cli project skill-callbacks insertion-points` with an explicit extension filter, all-catalog-extension filter, core-only filter, target skill filter, or stage filter
- **THEN** the command applies the filters to the packaged callback insertion-point catalog deterministically
- **AND** the command distinguishes Project-declared points from explicitly requested catalog-only extension points in JSON output

#### Scenario: Show command displays one callback
- **WHEN** a user runs `isomer-cli project skill-callbacks show <callback-id>`
- **THEN** the command displays the matching callback metadata and source reference while preserving redaction rules for secret-like material

#### Scenario: Disable command deactivates callback
- **WHEN** a user runs `isomer-cli project skill-callbacks disable <callback-id>`
- **THEN** the command marks the callback inactive in its registry and reports the previous and new status

#### Scenario: Validate command checks registries
- **WHEN** a user runs `isomer-cli project skill-callbacks validate`
- **THEN** the command validates reachable callback registries, source paths, manifest-declared callback insertion points, duplicate active ids, status values, priority values, and redaction-sensitive fields

## ADDED Requirements

### Requirement: Callback Target Validation Uses Insertion Point Catalog
The system SHALL validate User Skill Callback target skill and stage pairs against manifest-declared callback insertion points.

#### Scenario: Declared insertion point is accepted
- **WHEN** a User Skill Callback targets a system skill and callback stage pair declared in the packaged callback insertion-point catalog
- **THEN** validation accepts the target pair subject to the existing registry, source, scope, status, priority, and redaction rules

#### Scenario: Undeclared insertion point is rejected
- **WHEN** a User Skill Callback targets a packaged system skill and stage pair that is not declared as a callback insertion point
- **THEN** validation rejects the target pair with a deterministic diagnostic that names the missing insertion point
- **AND** the diagnostic directs users toward callback insertion-point discovery

#### Scenario: Optional extension target remains catalog based
- **WHEN** a User Skill Callback targets an insertion point belonging to a known optional system extension
- **THEN** validation uses the packaged catalog declaration rather than attempting to inspect the Project operator filesystem
- **AND** command output can report whether the extension is Project-declared or only catalog-known
