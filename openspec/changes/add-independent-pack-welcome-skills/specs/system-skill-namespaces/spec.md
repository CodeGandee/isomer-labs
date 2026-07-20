## MODIFIED Requirements

### Requirement: Packaged System Skill Namespace Convention
The system SHALL define active packaged system-skill namespaces that distinguish public core and extension surfaces from protected capability families.

#### Scenario: Core public names are documented
- **WHEN** packaged system-skill namespace documentation is inspected
- **THEN** it defines `isomer-op-welcome` as the public core onboarding skill and `isomer-op-entrypoint` as the public core execution skill
- **AND** other `isomer-op-<purpose>` names remain protected operator logical ids unless separately declared public

#### Scenario: Extension public names are documented
- **WHEN** documentation explains optional extension public surfaces
- **THEN** it reserves `isomer-ext-<extension-id>-welcome` for the public onboarding skill and `isomer-ext-<extension-id>-entrypoint` for the public execution skill
- **AND** it retains `isomer-<extension-id>-<purpose>` for protected domain capability ids

#### Scenario: Service and shared namespaces remain distinct
- **WHEN** documentation explains protected support capabilities
- **THEN** it defines `isomer-srv-<purpose>` for service-routed support and `isomer-misc-<purpose>` for shared helper identities
- **AND** it does not present those protected names as peer public welcome or entrypoint skills

### Requirement: Active Namespace Inventory
The packaged system-skill manifest SHALL list public welcome and entrypoint paths plus protected capability paths that match their declared roles.

#### Scenario: Core public paths use active names
- **WHEN** the core pack is inspected
- **THEN** public paths end with `isomer-op-welcome` and `isomer-op-entrypoint`
- **AND** protected operator paths remain below `isomer-op-entrypoint/subskills/isomer-op-<purpose>`

#### Scenario: Extension public paths use active names
- **WHEN** DeepSci or Kaoju pack assets are inspected
- **THEN** public sibling paths end with `isomer-ext-<extension-id>-welcome` and `isomer-ext-<extension-id>-entrypoint`
- **AND** protected paths remain below the entrypoint and use `isomer-<extension-id>-<purpose>` logical folder names

#### Scenario: Public identity matches folder name
- **WHEN** a manifest-declared welcome or entrypoint is inspected
- **THEN** its folder, `SKILL.md` frontmatter name, `agents/openai.yaml` display name, and default-prompt public invocation use the same canonical name

### Requirement: Active Kaoju Namespace Inventory
The packaged Kaoju extension SHALL use `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint` for its public pair while retaining `isomer-kaoju-<purpose>` for protected capabilities.

#### Scenario: Kaoju public and protected paths are distinguished
- **WHEN** the packaged Kaoju extension is inspected
- **THEN** its two public paths use the `isomer-ext-kaoju-*` welcome and entrypoint names
- **AND** every protected Kaoju path has the form `isomer-ext-kaoju-entrypoint/subskills/isomer-kaoju-<purpose>`

#### Scenario: Kaoju identity matches declared role
- **WHEN** Kaoju skill metadata is validated
- **THEN** public welcome and entrypoint metadata use their `isomer-ext-kaoju-*` identities
- **AND** protected subskill metadata retains its `isomer-kaoju-*` logical identity and parent-scoped default prompt
