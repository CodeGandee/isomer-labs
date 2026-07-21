## MODIFIED Requirements

### Requirement: Houmao Interop Service Skill Inventory
The core public pack SHALL preserve protected service logical capability `isomer-srv-houmao-interop` as scoped member `houmao`.

#### Scenario: Protected service bundle exists
- **WHEN** packaged core inventory is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/subskills/isomer-srv-houmao-interop`
- **AND** it does not contain active `isomer-op-houmao-interop` compatibility bundles

#### Scenario: Service identity is consistent
- **WHEN** the protected bundle is inspected
- **THEN** its folder, `SKILL.md` frontmatter, metadata, callbacks, and provenance identity use `isomer-srv-houmao-interop`
- **AND** ordinary user guidance uses the public core entrypoint rather than direct service invocation

#### Scenario: Manifest maps protected service
- **WHEN** `manifest.toml` is inspected
- **THEN** logical id `isomer-srv-houmao-interop` maps to member `houmao`, its nested path, and `isomer-op-entrypoint->houmao`
- **AND** no independent public service path is listed

### Requirement: Houmao Interop Routes Through Isomer Skill Context
The protected Houmao member SHALL preserve Isomer-managed Houmao context routing under the public parent.

#### Scenario: Houmao support is selected
- **WHEN** an owning operator workflow needs bounded Houmao behavior
- **THEN** it invokes `isomer-op-entrypoint->houmao`
- **AND** the protected member resolves the supported Isomer skill-context surface before using Houmao-owned procedures

#### Scenario: Integration is absent or disabled
- **WHEN** Houmao integration is not configured or disabled
- **THEN** the protected member reports that posture without requiring direct Houmao skill installation or live state

#### Scenario: Service requests skill context before routing
- **WHEN** `isomer-srv-houmao-interop` needs to delegate to a Houmao-owned procedure
- **THEN** it first obtains a Houmao skill context through the supported `isomer-cli` Project integration command
- **AND** it uses the returned `houmao_skill_path` and `houmao_project_path` in its routing instructions

#### Scenario: Service keeps Isomer language first
- **WHEN** the service reports a Houmao-backed support route to the Project Operator Session
- **THEN** it describes the requested work in Isomer terms such as Project, Topic Workspace, Topic Actor, Topic Service Master, and Service Request
- **AND** it presents Houmao terms only as internal provider context needed to follow the projected skill

#### Scenario: Disabled integration is skipped
- **WHEN** the returned Houmao skill context reports disabled integration
- **THEN** the service reports a skipped Houmao integration result
- **AND** it does not tell the agent to inspect Houmao credentials, launch profiles, mailboxes, gateways, or runtime state

#### Scenario: Explicit project dir is preserved
- **WHEN** the service instructs an agent to follow a projected Houmao skill
- **THEN** the instruction includes the exact Houmao Project path returned by Isomer
- **AND** it tells the agent not to rely on implicit `.houmao/` discovery from the current working directory
