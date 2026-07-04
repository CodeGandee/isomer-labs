## ADDED Requirements

### Requirement: Houmao Interop Service Skill Inventory
The repository SHALL provide the Houmao interop skill as a service skill named `isomer-srv-houmao-interop`.

#### Scenario: Service skill folder exists
- **WHEN** the packaged system skill inventory is inspected
- **THEN** it contains `service/isomer-srv-houmao-interop`
- **AND** it does not contain active `operator/isomer-op-houmao-interop` or `service/isomer-op-houmao-interop` folders

#### Scenario: Service skill identity is consistent
- **WHEN** `service/isomer-srv-houmao-interop` is inspected
- **THEN** its folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-srv-houmao-interop`
- **AND** its local references and scenarios invoke `isomer-srv-houmao-interop` when naming the skill directly

#### Scenario: Manifest lists service path
- **WHEN** `src/isomer_labs/assets/system_skills/manifest.toml` is inspected
- **THEN** it lists `service/isomer-srv-houmao-interop`
- **AND** it does not list `operator/isomer-op-houmao-interop`

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
