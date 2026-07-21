# system-skill-namespaces Specification

## Purpose
Define active packaged system-skill namespace conventions and the inventory rules that keep public, operator, service, and domain-extension skill families distinct.
## Requirements
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

#### Scenario: Protected namespace convention is documented
- **WHEN** documentation describes protected capabilities
- **THEN** it retains `isomer-op-<purpose>` for operator logical ids, `isomer-srv-<purpose>` for service logical ids, `isomer-misc-<purpose>` for shared helper logical ids, and `isomer-<extension-id>-<purpose>` for extension logical ids
- **AND** it states that these names are not ordinary top-level install or invocation surfaces
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

#### Scenario: Protected paths retain logical-id folders
- **WHEN** a protected member path is inspected
- **THEN** its final directory name and `SKILL.md` frontmatter name equal its preserved logical id
- **AND** the path is below `<public-pack>/subskills/`

#### Scenario: Invocation designator uses scoped member
- **WHEN** protected capability metadata is inspected
- **THEN** its invocation designator begins with the owning public entrypoint and uses its unique scoped member name
- **AND** the terminal scoped member is a bare path component without `()`
- **AND** the scoped member name does not replace the protected logical id in callbacks, bindings, or provenance
### Requirement: No Active Legacy Namespace Shims
The system SHALL NOT keep top-level compatibility skill folders or duplicate nested shims for superseded operator, research, or pipeline public names.

#### Scenario: Old compatibility folders are absent
- **WHEN** public and protected package paths are inspected
- **THEN** no active path starts with `isomer-admin-*` or `isomer-rsch-*`
- **AND** no top-level `isomer-deepsci-pipeline` or `isomer-kaoju-pipeline` folder is present

#### Scenario: Catalog aliases preserve bounded compatibility
- **WHEN** catalog metadata is inspected
- **THEN** old pipeline ids may appear only as declared lookup aliases for the new extension entrypoints
- **AND** an alias does not create an independently invokable skill

#### Scenario: Historical material may preserve old names
- **WHEN** archived OpenSpec changes, provenance, source copies, or migration notes are inspected
- **THEN** they may retain historical names
- **AND** active validators do not treat those references as current public invocations

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

#### Scenario: Kaoju identity is consistent
- **WHEN** a protected Kaoju bundle is inspected
- **THEN** its folder, `SKILL.md` frontmatter name, and private-projection identity use the same `isomer-kaoju-*` logical id
- **AND** its parent route uses the catalog-declared scoped member designator

#### Scenario: Namespace documentation includes Kaoju example
- **WHEN** namespace documentation describes extension packs
- **THEN** it identifies `isomer-ext-kaoju-entrypoint` as the public entrypoint and `isomer-kaoju-trial` as an example protected capability
- **AND** it keeps Kaoju distinct from core shared helpers
