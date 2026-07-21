## MODIFIED Requirements

### Requirement: Misc Tool Packs Skill Resolves Named Toolsets
The core public pack SHALL preserve logical capability `isomer-misc-tool-packs` as protected shared member `tool-packs` for resolving named dependency bundles.

#### Scenario: Protected tool-packs bundle exists
- **WHEN** core pack assets are inspected
- **THEN** `operator/isomer-op-entrypoint/subskills/isomer-misc-tool-packs/SKILL.md` exists
- **AND** its folder and frontmatter retain logical id `isomer-misc-tool-packs`

#### Scenario: User manually asks to install a named toolset
- **WHEN** a user explicitly invokes `isomer-misc-tool-packs` or directly asks to install or prepare a toolset such as `paper-writing`, `paper-figures-python`, `paper2ppt`, `cuda-build`, or `torch-gpu`
- **THEN** the skill resolves the request to one canonical pack name
- **AND** it reports the aliases that matched when aliases were used
- **AND** it returns a dependency contract for the canonical pack

#### Scenario: Named toolset is requested
- **WHEN** a user or owning workflow asks for one defined tool pack
- **THEN** the public parent or internal route invokes `isomer-op-entrypoint->tool-packs`
- **AND** the protected capability returns the existing dependency intent without applying package mutation itself

#### Scenario: Ambiguous toolset name blocks resolution
- **WHEN** a user-provided toolset name can plausibly match more than one canonical pack
- **THEN** the skill reports an ambiguity blocker
- **AND** it lists the candidate canonical pack names without choosing one silently

#### Scenario: Unknown toolset remains bounded
- **WHEN** a named toolset is absent from the tool-pack registry
- **THEN** the protected capability reports it as unknown and does not fabricate dependencies

#### Scenario: Unknown toolset name blocks resolution
- **WHEN** a user-provided toolset name does not match any canonical pack or alias
- **THEN** the skill reports an unknown-toolset blocker
- **AND** it lists the available canonical pack names

### Requirement: Tool Pack Skill Is Manual-Only Initially
The protected tool-packs member SHALL remain explicitly selected and SHALL NOT trigger solely from a package or research task.

#### Scenario: User names tool packs
- **WHEN** the user invokes `$isomer-op-entrypoint use tool-packs to <task>` or explicitly asks for a named tool pack
- **THEN** the parent may select the protected capability

#### Scenario: Implicit invocation is disabled
- **WHEN** the tool-pack skill agent metadata is inspected
- **THEN** `allow_implicit_invocation` is set to `false`

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

#### Scenario: Tool-pack skill name remains stable
- **WHEN** the misc skillset is inspected after the namespace rename
- **THEN** the tool-pack skill remains `isomer-misc-tool-packs`
- **AND** it is not renamed to `isomer-ext-tool-packs`

#### Scenario: Tool-pack helper routes remain current
- **WHEN** the tool-pack skill returns a pack contract
- **THEN** package-source concerns route to `isomer-srv-resolve-pkg-repo`
- **AND** NVIDIA/CUDA environment concerns route to `isomer-misc-nvidia-tools`
- **AND** PyTorch variant concerns route to `isomer-misc-pkg-specifics`
- **AND** heavy or unknown-risk setup work routes to `isomer-misc-bounded-run-tips`

#### Scenario: Toolbox remains distinct
- **WHEN** guidance compares tool packs and Project-local Toolboxes
- **THEN** it keeps protected `tool-packs` dependency intent distinct from protected `toolbox` configuration management

#### Scenario: Tool-pack skill avoids DeepSci coupling
- **WHEN** the tool-pack skill and its active references are inspected
- **THEN** they do not require or reference production DeepSci skill paths as consumers or dependencies
- **AND** domain extension families may consume tool-pack contracts without making the tool-pack skill part of that extension family
