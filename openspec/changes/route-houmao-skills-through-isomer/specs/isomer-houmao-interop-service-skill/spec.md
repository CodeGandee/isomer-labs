## ADDED Requirements

### Requirement: Houmao Interop Routes Through Isomer Skill Context
The Houmao interop service skill SHALL route Houmao-specific procedures through Isomer-provided skill context rather than assuming direct operator installation of Houmao system skills or implicit Houmao project discovery.

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

