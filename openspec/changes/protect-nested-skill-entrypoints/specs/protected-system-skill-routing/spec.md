## ADDED Requirements

### Requirement: Protected Entrypoint Files Prevent Incidental Host Discovery
The system SHALL reserve `SKILL.md` for public host-discoverable system-skill roots and SHALL use `SKILL-MAIN.md` for protected subskills that are loaded only through their owning public entrypoint.

#### Scenario: Complete public pack is scanned recursively
- **WHEN** an agent host recursively scans an installed public Isomer pack for files named exactly `SKILL.md`
- **THEN** it finds the pack's public welcome and execution entrypoint roots only
- **AND** no protected member or preserved source snapshot is registered as a top-level skill

#### Scenario: Parent selects a protected member
- **WHEN** a public execution entrypoint routes to one manifest-declared protected member
- **THEN** it resolves that member below its own `subskills/` directory and explicitly loads `SKILL-MAIN.md`
- **AND** it does not scan or preload sibling protected members

#### Scenario: Flattened private projection is requested
- **WHEN** an internal adapter deliberately projects a protected capability as a top-level member of a bounded Agent Role skill root
- **THEN** materialization promotes that copied member's `SKILL-MAIN.md` to destination `SKILL.md`
- **AND** the canonical package source remains `SKILL-MAIN.md`

#### Scenario: Nested discovery filename is introduced
- **WHEN** a protected member or provenance subtree inside a public pack contains `SKILL.md`
- **THEN** packaged-skill validation fails with the nested path and owning public pack

## MODIFIED Requirements

### Requirement: Protected Capabilities Are Parent-Owned Subskills
Every manifest-declared non-entrypoint logical system-skill capability SHALL be a self-contained subskill below exactly one public pack at `subskills/<logical-id>/` and SHALL use `SKILL-MAIN.md` as its parent-scoped entrypoint.

#### Scenario: Protected capability is inspected
- **WHEN** a manifest-declared protected capability is inspected
- **THEN** its path is below its owning public pack's `subskills/` directory
- **AND** it contains `SKILL-MAIN.md` and every active bundle-local resource needed for its workflow
- **AND** it does not contain `SKILL.md` or appear as a public install unit

#### Scenario: Parent route table is inspected
- **WHEN** a public pack owns protected capabilities
- **THEN** its `SKILL.md` lists each scoped member name and route in a Subskills or Subcommands section
- **AND** every route resolves to one manifest-declared protected capability inside that pack and loads its `SKILL-MAIN.md`

#### Scenario: Existing workflow boundaries are preserved
- **WHEN** a flat skill becomes a protected subskill
- **THEN** its triggers, gates, callbacks, inputs, outputs, blockers, subcommands, and owner boundaries remain effective unless another accepted requirement changes them

### Requirement: Resource Ownership Determines Command or Subskill Form
The system SHALL model a procedure as a direct or nested subcommand when it uses resources owned by its containing skill or subskill, and SHALL model a capability as a subskill with `SKILL-MAIN.md` when it needs a private bundled-resource boundary. Private SHALL mean scoped ownership and lifecycle, not secrecy or access control.

#### Scenario: Procedure uses containing resources
- **WHEN** a procedure needs only the scripts, references, assets, templates, runtime metadata, and support files owned by its containing skill or subskill
- **THEN** it is authored as a direct or nested subcommand
- **AND** any command detail page or child command page remains owned by that containing bundle

#### Scenario: Capability needs privately owned resources
- **WHEN** a capability needs its own scripts, references, commands, assets, templates, runtime metadata, or other support files that should be maintained, loaded, validated, or projected as one scoped bundle
- **THEN** it is authored as a subskill with its own `SKILL-MAIN.md` and bundle boundary
- **AND** workflow size or complexity alone does not determine the form

#### Scenario: Existing protected capability is classified
- **WHEN** migration inspects an existing non-entrypoint system skill with its own standalone `SKILL.md`, `agents/openai.yaml`, and active support resources
- **THEN** it moves those private resources into one protected subskill bundle and renames the active entrypoint to `SKILL-MAIN.md`
- **AND** parent-owned command families without an independent resource bundle remain commands

### Requirement: Protected Projection Includes Dependency Closure
The system SHALL resolve protected logical capabilities and their declared dependencies for bounded internal or role-specific projection without turning those capabilities into public install units, except that deliberately flattened private roots SHALL expose only their selected copied members through promoted `SKILL.md` entrypoints.

#### Scenario: One protected capability is selected internally
- **WHEN** an Isomer adapter requests a protected logical id for an Agent Role, Agent Profile, Topic Actor, or Service Agent
- **THEN** catalog resolution returns the selected nested source path and the deterministic transitive dependency closure
- **AND** each result retains its logical id, owning pack, invocation designator, and canonical `SKILL-MAIN.md` source entrypoint

#### Scenario: Dependency crosses pack areas
- **WHEN** a protected research member depends on a core shared or service capability
- **THEN** the dependency graph records the cross-pack logical-id edge
- **AND** bounded projection includes the dependency without adding either member to an ordinary complete-pack public surface

#### Scenario: Private projection is materialized
- **WHEN** the dependency-closed protected selection is flattened into a private host skill root
- **THEN** each destination member contains top-level `SKILL.md` copied from its source `SKILL-MAIN.md`
- **AND** no destination member retains a sibling `SKILL-MAIN.md` or nested provenance `SKILL.md`

#### Scenario: Dependency graph is invalid
- **WHEN** a protected dependency names an unknown logical id or creates a cycle
- **THEN** manifest loading and skill validation fail with a deterministic diagnostic

### Requirement: Protected Members Remain Independently Verifiable
Every protected member SHALL retain enough identity and version metadata in its `SKILL-MAIN.md` bundle for package validation, callback lookup, explicit parent loading, and bounded private projection.

#### Scenario: Protected member metadata is inspected
- **WHEN** a nested protected bundle is inspected
- **THEN** its folder and `SKILL-MAIN.md` frontmatter retain the protected logical id
- **AND** its `agents/openai.yaml` version exactly matches the package project version

#### Scenario: Public pack integrity is checked
- **WHEN** status or explicit-root inspection verifies a public pack
- **THEN** it checks every declared protected member path, `SKILL-MAIN.md` identity, version, and required active resource
- **AND** one missing, mismatched, or nested-`SKILL.md` member prevents complete pack status
