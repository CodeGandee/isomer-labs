## ADDED Requirements

### Requirement: System Skill Manager Selects Installation Scope Explicitly
The system-skill manager SHALL select a concrete host target and either `project` or `user` scope before invoking system-skill installation.

#### Scenario: Project Operator installation defaults to project scope
- **WHEN** a user authorizes extension installation from a Project Operator Session without requesting user-wide availability
- **THEN** the manager selects `project` scope anchored to the current working directory
- **AND** it states that the installation applies to the current agent-host project context

#### Scenario: User-wide installation requires explicit intent
- **WHEN** installation would use `user` scope
- **THEN** the manager requires an explicit user request or confirmation for user-wide installation
- **AND** it states that the installed skills can affect the selected host across Projects

#### Scenario: Unknown host target blocks installation
- **WHEN** the manager cannot identify a supported concrete target for the current host
- **THEN** it reports a blocker instead of guessing a target or arbitrary skill root
- **AND** it preserves Project declarations and existing skill projections

## MODIFIED Requirements

### Requirement: Operator-Managed Extension Installation Converges
The system-skill manager SHALL combine a user-authorized extension installation through an explicit target and scope with verification, Project registration, and activation guidance.

#### Scenario: Successful scoped installation is registered
- **WHEN** `install-extension <extension-id>` installs a complete family with `system-skills install --target <host-known-target> --scope <selected-scope> --extension <extension-id>`
- **THEN** the manager reads the resolved skill root from the installation result and verifies it with safe explicit-root CLI primitives
- **AND** it remembers the extension in the selected Project unless the user opted out

#### Scenario: Registration failure is partial
- **WHEN** scoped installation succeeds but Project registration fails
- **THEN** the manager reports a non-success partial outcome that distinguishes installed files from missing registration
- **AND** a retry can complete registration without reinstalling the extension

#### Scenario: New installation may require host refresh
- **WHEN** scoped installation succeeds but the extension is not observable in a refreshed live inventory
- **THEN** the manager reports `host_refresh_required`
- **AND** it advises a new turn, thread, or host-native refresh without claiming current-session availability

#### Scenario: Custom destination request is not translated to home override
- **WHEN** a user requests installation into an arbitrary plugin, extra, or custom skill directory
- **THEN** the manager explains that the scoped installer supports only target-defined `user` and `project` roots
- **AND** it does not reconstruct the removed `--home` behavior through path guessing
