## ADDED Requirements

### Requirement: Core Isomer Skills Include Internal Houmao Bridge Support
The packaged Isomer system-skill catalog SHALL keep Isomer-facing Houmao bridge and Topic Service Agent support available in the core skill set while keeping Houmao-owned projected skill material Project-local and opt-in.

#### Scenario: Core operator installation does not expose Houmao administration
- **WHEN** a user installs only the basic Isomer operator skill set
- **THEN** the installed user-facing skills do not require the user to install or invoke Houmao-owned system skills directly
- **AND** Houmao-specific procedures remain reachable only through Isomer-managed routing or an explicit advanced support path

#### Scenario: Core includes Isomer-facing bridge skills
- **WHEN** the packaged system-skill manifest is inspected
- **THEN** the core group may include Isomer-facing bridge/support skills such as `isomer-srv-houmao-interop` and `isomer-srv-topic-service-agent-support`
- **AND** those skills do not require Project-local Houmao skill projection, Houmao credentials, or live Houmao state merely to report disabled or not-configured integration

#### Scenario: Project-local projection remains opt-in
- **WHEN** a Project has not enabled Houmao integration
- **THEN** core Isomer skill installation does not create `.isomer-labs/houmao-skills/`
- **AND** projected Houmao-owned skill material is prepared only through explicit Project integration setup

#### Scenario: Public installation guidance keeps Isomer first
- **WHEN** public system-skill installation documentation describes Houmao-backed behavior
- **THEN** it describes Houmao as an internal Isomer integration provider
- **AND** it directs users to Isomer setup and Project integration commands instead of direct Houmao skill installation as the primary route
