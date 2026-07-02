## ADDED Requirements

### Requirement: Package Add Requests Route Through Topic Workspace Manager
The service environment setup skill SHALL not be the public bypass route for package-add requests from users or other skills.

#### Scenario: User package-add prompt routes to workspace manager
- **WHEN** a user asks to install, add, or repair packages for a selected Topic Workspace without requesting the full topic environment setup workflow
- **THEN** service guidance routes the request to `$isomer-admin-topic-workspace-mgr install-packages`
- **AND** it does not perform direct package mutation as a competing public entrypoint

#### Scenario: Research package handoff routes to workspace manager
- **WHEN** a research skill reports missing packages or runtime dependencies and asks for package installation
- **THEN** service guidance routes the request to `$isomer-admin-topic-workspace-mgr install-packages`
- **AND** it does not ask the research skill to call `isomer-srv-topic-env-setup install-topic-deps` directly

#### Scenario: Full environment setup remains explicit
- **WHEN** a user requests full gate-driven Topic Workspace environment setup from source intent or an explicit target spec
- **THEN** the service skill may still run its full setup workflow according to its existing gate contract
- **AND** any package-add surface exposed to users or other skills is aligned with the workspace manager route

#### Scenario: Service package guidance preserves enclosure policy
- **WHEN** service env setup guidance discusses package mutation after this change
- **THEN** it preserves Pixi-scoped Topic Workspace environment mutation, verification, no-sudo blockers, and no ambient virtualenv policy
- **AND** it does not recommend local `venv`, ambient `pip`, or system package manager mutation for package additions
