## MODIFIED Requirements

### Requirement: Packaged System Skill Namespace Convention
The system SHALL reserve distinct namespaces for public pack entrypoints and protected logical capabilities while retaining the `isomer-` product prefix.

#### Scenario: Public namespace convention is documented
- **WHEN** packaged system-skill documentation is inspected
- **THEN** it defines `isomer-op-entrypoint` as the sole core public pack
- **AND** it defines `isomer-ext-<extension-id>-entrypoint` as the only public extension skill form
- **AND** it identifies `isomer-ext-deepsci-entrypoint` and `isomer-ext-kaoju-entrypoint` as active examples

#### Scenario: Protected namespace convention is documented
- **WHEN** documentation describes protected capabilities
- **THEN** it retains `isomer-op-<purpose>` for operator logical ids, `isomer-srv-<purpose>` for service logical ids, `isomer-misc-<purpose>` for shared helper logical ids, and `isomer-<extension-id>-<purpose>` for extension logical ids
- **AND** it states that these names are not ordinary top-level install or invocation surfaces

#### Scenario: Generic extension entrypoint suffix is bounded
- **WHEN** a new public extension pack is named
- **THEN** its name is exactly `isomer-ext-<extension-id>-entrypoint`
- **AND** `isomer-ext-*` is not used for protected members, arbitrary helpers, or a generic extension capability bucket

### Requirement: Active Namespace Inventory
The manifest SHALL list three public pack paths and SHALL map protected namespace identities to nested paths below their owning pack.

#### Scenario: Public pack paths use active names
- **WHEN** `manifest.toml` is inspected with all current extensions
- **THEN** the public paths end in `isomer-op-entrypoint`, `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-entrypoint`

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
The catalog SHALL use `isomer-ext-kaoju-entrypoint` for the public Kaoju pack and `isomer-kaoju-<purpose>` for its protected logical capabilities.

#### Scenario: Kaoju public and protected paths are distinct
- **WHEN** the packaged Kaoju extension is inspected
- **THEN** its public path ends in `isomer-ext-kaoju-entrypoint`
- **AND** every protected member path is below that pack's `subskills/` directory and ends in an `isomer-kaoju-<purpose>` logical id

#### Scenario: Kaoju identity is consistent
- **WHEN** a protected Kaoju bundle is inspected
- **THEN** its folder, `SKILL.md` frontmatter name, and private-projection identity use the same `isomer-kaoju-*` logical id
- **AND** its parent route uses the catalog-declared scoped member designator

#### Scenario: Namespace documentation includes Kaoju example
- **WHEN** namespace documentation describes extension packs
- **THEN** it identifies `isomer-ext-kaoju-entrypoint` as the public entrypoint and `isomer-kaoju-trial` as an example protected capability
- **AND** it keeps Kaoju distinct from core shared helpers
