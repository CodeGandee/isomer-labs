# isomer-houmao-interop-service-skill Specification

## Purpose
TBD - created by archiving change move-houmao-interop-to-service. Update Purpose after archive.
## Requirements
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

### Requirement: Houmao Interop Service Responsibility
The Houmao interop service skill SHALL provide bounded operational support for Houmao adapter/runtime explanation, customization guidance, template mapping, and runtime inspection at the command of a Project Operator Session, Operator Agent, or Service Request.

#### Scenario: Service skill preserves bounded modes
- **WHEN** `isomer-srv-houmao-interop` is invoked for Houmao support
- **THEN** it provides bounded modes for help, explaining the Houmao loop, listing customization points, mapping Domain Agent Team Templates to Houmao concepts, and inspecting Houmao runtime state
- **AND** it keeps Houmao terms as adapter or implementation details rather than Isomer core schema or user-facing operator language

#### Scenario: Service skill does not own operator decisions
- **WHEN** the service skill handles Houmao interop support
- **THEN** it does not own Project lifecycle, Research Topic creation, Topic Team Specialization, approval provenance, Topic Agent Team Profile materialization, Agent Team Instance launch orchestration, Gate decisions, Research Claims, or research task routing
- **AND** it routes those responsibilities back to the appropriate operator skill, generic Isomer CLI/API surface, or execution adapter boundary

#### Scenario: Operator workflow routes service support
- **WHEN** a user-facing operator workflow needs Houmao-specific explanation, mapping, customization guidance, or runtime inspection
- **THEN** the operator guidance may route that bounded support to `isomer-srv-houmao-interop`
- **AND** the visible first command remains the appropriate `isomer-op-*` operator workflow rather than a direct service skill recommendation

### Requirement: Houmao Interop Service Validation
The repository SHALL validate the Houmao interop service skill as part of active system skill validation.

#### Scenario: Service validation covers Houmao interop
- **WHEN** repository skill validation runs
- **THEN** it validates `isomer-srv-houmao-interop` with the same structural checks used for active service skills, including frontmatter, metadata, manifest path, local references, and active invocation names

#### Scenario: Stale operator identity is rejected
- **WHEN** active docs, manifests, skill metadata, validation fixtures, generated skill catalogs, or active OpenSpec guidance are scanned
- **THEN** current invokable guidance does not present `isomer-op-houmao-interop` as an active skill
- **AND** historical or migration-only references are allowed only when they are clearly passive provenance

#### Scenario: Compatibility shim is absent
- **WHEN** the active packaged skill inventory is inspected
- **THEN** no alias, wrapper, duplicate folder, or manifest entry keeps `isomer-op-houmao-interop` available as an active compatibility skill

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

### Requirement: Houmao Interop Uses Isomer Topic Service Master Identity
Houmao interop service guidance SHALL use Isomer-provided Topic Service Master names and bindings when routing to Houmao-owned procedures.

#### Scenario: Preparation passes suggested names
- **WHEN** `isomer-srv-houmao-interop` or `isomer-srv-topic-service-agent-support` routes to Houmao-owned preparation procedure
- **THEN** it passes the Isomer-provided specialist name, launch profile name, and managed agent name as context
- **AND** it does not ask the agent to invent those names

#### Scenario: Later lifecycle routes use binding
- **WHEN** launch, inspect, stop, or repair routes operate on a Topic Service Master
- **THEN** they first inspect the Topic Workspace Manifest binding or skill-context binding payload
- **AND** they use the recorded specialist, launch profile, and managed agent names when present

#### Scenario: Drift is reported in Isomer terms
- **WHEN** Houmao observations differ from the Topic Workspace Manifest binding
- **THEN** the service reports drift against the Topic Workspace and Topic Service Master identity
- **AND** it routes repair through `repair-topic-service-master` rather than silently choosing new Houmao names

