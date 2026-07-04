## MODIFIED Requirements

### Requirement: Service Routes Ad Hoc Environment Requests to Topic Manager
The service environment setup skill SHALL route ad hoc package mutation and package verification requests to `isomer-op-topic-mgr` while preserving full gate-driven setup in the service.

#### Scenario: Ad hoc package install routes to topic manager
- **WHEN** a user, operator skill, or research skill asks only to add or repair packages for a selected Topic Workspace
- **THEN** service guidance routes the request to `$isomer-op-topic-mgr env-install-packages`
- **AND** it does not treat `install-topic-deps` as a competing public package-add entrypoint

#### Scenario: Ad hoc package update routes to topic manager
- **WHEN** a user, operator skill, or research skill asks only to update packages for a selected Topic Workspace
- **THEN** service guidance routes the request to `$isomer-op-topic-mgr env-update-packages`

#### Scenario: Ad hoc package removal routes to topic manager
- **WHEN** a user, operator skill, or research skill asks only to remove packages from a selected Topic Workspace
- **THEN** service guidance routes the request to `$isomer-op-topic-mgr env-remove-packages`

#### Scenario: Topic environment verification remains service compatible
- **WHEN** `isomer-op-topic-mgr env-verify-topic` routes full gate-driven verification to this service
- **THEN** the service accepts the selected Research Topic, Topic Workspace, topic env target spec, semantic path expectations, and verification intent as ordinary setup or verification context
- **AND** it returns command evidence, changed paths, blockers, and next action without claiming actor, formal agent, or runtime launch readiness

#### Scenario: Full setup still uses install-topic-deps
- **WHEN** the service is executing the complete topic env setup workflow from source gate through derived gate verification
- **THEN** it may still run `install-topic-deps` as an internal procedural step

## ADDED Requirements

### Requirement: Topic Environment Service Keeps Protected Namespace
The topic environment setup service SHALL keep the `isomer-srv-topic-env-setup` active skill name while routing user-facing control through operator skills.

#### Scenario: Service name remains stable
- **WHEN** the service skill bundle is inspected after the namespace rename
- **THEN** the folder name, `SKILL.md` frontmatter, agent metadata, and manifest path continue to use `isomer-srv-topic-env-setup`

#### Scenario: Service guidance avoids user-facing operator claims
- **WHEN** service guidance describes ordinary user-facing package mutation or verification requests
- **THEN** it routes those requests through `isomer-op-topic-mgr`
- **AND** it treats direct service invocation as protected or delegated operational support
