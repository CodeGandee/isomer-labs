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
