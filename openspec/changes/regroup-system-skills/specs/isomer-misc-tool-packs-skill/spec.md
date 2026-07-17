## MODIFIED Requirements

### Requirement: Misc Tool Packs Skill Resolves Named Toolsets
The core public pack SHALL preserve logical capability `isomer-misc-tool-packs` as protected shared member `tool-packs` for resolving named dependency bundles.

#### Scenario: Protected tool-packs bundle exists
- **WHEN** core pack assets are inspected
- **THEN** `operator/isomer-op-entrypoint/subskills/isomer-misc-tool-packs/SKILL.md` exists
- **AND** its folder and frontmatter retain logical id `isomer-misc-tool-packs`

#### Scenario: Named toolset is requested
- **WHEN** a user or owning workflow asks for one defined tool pack
- **THEN** the public parent or internal route invokes `isomer-op-entrypoint->tool-packs`
- **AND** the protected capability returns the existing dependency intent without applying package mutation itself

#### Scenario: Unknown toolset remains bounded
- **WHEN** a named toolset is absent from the tool-pack registry
- **THEN** the protected capability reports it as unknown and does not fabricate dependencies

### Requirement: Tool Pack Skill Is Manual-Only Initially
The protected tool-packs member SHALL remain explicitly selected and SHALL NOT trigger solely from a package or research task.

#### Scenario: User names tool packs
- **WHEN** the user invokes `$isomer-op-entrypoint use tool-packs to <task>` or explicitly asks for a named tool pack
- **THEN** the parent may select the protected capability

#### Scenario: Package mutation is requested
- **WHEN** a user asks only to install, update, or remove packages
- **THEN** the entrypoint routes to the applicable owner workflow
- **AND** it does not infer tool-pack selection

### Requirement: Tool Packs Remain Misc Helper Interface
Tool packs SHALL remain cross-domain dependency intent rather than becoming a public pack or research-paradigm version.

#### Scenario: Public skill inventory is inspected
- **WHEN** ordinary Isomer host discovery runs
- **THEN** it does not list `isomer-misc-tool-packs`
- **AND** core help may expose `tool-packs` as an explicit public subcommand of `isomer-op-entrypoint`

#### Scenario: Toolbox remains distinct
- **WHEN** guidance compares tool packs and Project-local Toolboxes
- **THEN** it keeps protected `tool-packs` dependency intent distinct from protected `toolbox` configuration management
