## MODIFIED Requirements

### Requirement: Research Paradigm Skillset Layout
The packaged research-paradigm surface SHALL contain public extension entrypoint packs whose existing stage capabilities are protected nested subskills.

#### Scenario: Production DeepSci pack exists
- **WHEN** packaged research-paradigm assets are inspected
- **THEN** `research-paradigm/deepsci/isomer-ext-deepsci-entrypoint` exists
- **AND** all production `isomer-deepsci-*` capabilities are below its `subskills/` directory

#### Scenario: Retired v1 folders are absent
- **WHEN** active DeepSci assets are inspected
- **THEN** retired v1, `isomer-rsch-*`, and version-suffixed compatibility folders remain absent

#### Scenario: Production DeepSci protected folders exist
- **WHEN** the DeepSci public pack is inspected
- **THEN** its manifest-declared 21 protected member folders exist with valid `SKILL.md` and `agents/openai.yaml`

#### Scenario: Protected bundle remains self-contained
- **WHEN** one production DeepSci member is privately projected with its declared dependencies
- **THEN** its active resources resolve without repository siblings or family-root files

#### Scenario: Operator skills are excluded from extension pack
- **WHEN** DeepSci or Kaoju pack contents are inspected
- **THEN** they do not embed core operator or service bundles
- **AND** cross-pack routes use protected logical dependencies

### Requirement: Shared Research Contract
DeepSci shared procedure semantics SHALL remain owned by protected logical capability `isomer-deepsci-shared` and routed through the DeepSci public pack.

#### Scenario: DeepSci member references shared rules
- **WHEN** a protected DeepSci stage needs production shared semantics
- **THEN** it invokes `isomer-ext-deepsci-entrypoint->shared` or a declared shared command
- **AND** it does not use a sibling filesystem path

#### Scenario: Shared logical identity remains stable
- **WHEN** callback, binding, dependency, or provenance metadata names the shared owner
- **THEN** it uses `isomer-deepsci-shared`

#### Scenario: Private projection includes shared dependency
- **WHEN** a protected stage whose manifest metadata depends on shared is projected selectively
- **THEN** dependency closure includes `isomer-deepsci-shared`

### Requirement: Validation
Research-paradigm validation SHALL enumerate public packs and protected members from manifest v3 and enforce both common and family-specific contracts recursively.

#### Scenario: Structural validation runs
- **WHEN** the validation harness runs
- **THEN** it validates each public pack, every declared nested member, their route mappings, resources, invocation notation, versions, and dependencies

#### Scenario: Expected production inventory is validated
- **WHEN** a public extension pack has a missing, extra, duplicated, or misnamed protected member
- **THEN** validation reports the pack and logical id

#### Scenario: Naming validation runs
- **WHEN** a DeepSci or Kaoju public or protected identity violates its namespace rule
- **THEN** validation reports the invalid identity and expected form

#### Scenario: Coupling validation runs
- **WHEN** one protected member traverses into a sibling bundle or calls an undeclared dependency
- **THEN** validation reports the offending route or path

#### Scenario: Flat private projection is tested
- **WHEN** the validation fixture projects a protected member and dependency closure outside its parent tree
- **THEN** the bundle remains executable and its private resources resolve

#### Scenario: Repository command runs harness
- **WHEN** `pixi run validate-skills` executes
- **THEN** it covers the complete public and protected research-paradigm inventory

### Requirement: Production DeepSci User Skill Callback Participation
Each participating protected DeepSci member SHALL resolve callbacks by preserved logical id while the public parent controls routing.

#### Scenario: Top-level protected workflow includes callback steps
- **WHEN** a participating DeepSci member is inspected
- **THEN** its numbered workflow retains begin and end callback steps

#### Scenario: Begin callback runs before primary action
- **WHEN** the public parent invokes a protected member
- **THEN** that member resolves `begin` callbacks with `--skill <logical-id>` before its first capability-specific action

#### Scenario: End callback runs before completion
- **WHEN** tentative outputs exist
- **THEN** that member resolves `end` callbacks with the same logical id before terminal completion

#### Scenario: Empty callback resolution continues
- **WHEN** no callbacks match
- **THEN** the protected workflow continues normally

#### Scenario: Callback instructions remain subordinate
- **WHEN** callback material conflicts with DeepSci contracts
- **THEN** the protected member preserves its governing rules and reports the conflict

#### Scenario: Validation checks callback routing
- **WHEN** a member resolves callbacks with the public pack name or another logical id
- **THEN** validation reports the incorrect target

### Requirement: Production Kaoju Research-Paradigm Layout
The packaged research-paradigm documentation and assets SHALL present Kaoju through public pack `isomer-ext-kaoju-entrypoint` and thirteen protected members.

#### Scenario: Research-paradigm documentation lists both families
- **WHEN** family documentation is inspected
- **THEN** it lists `isomer-ext-deepsci-entrypoint` and `isomer-ext-kaoju-entrypoint` as optional public packs

#### Scenario: Kaoju active surface is concise and self-contained
- **WHEN** the Kaoju pack is inspected
- **THEN** its public entrypoint owns public commands and its protected members own stage-specific behavior and resources
- **AND** no old pipeline facade or top-level protected member remains

#### Scenario: Kaoju skills use canonical Isomer language
- **WHEN** public and protected Kaoju guidance is inspected
- **THEN** it retains canonical Isomer domain terms and provider boundaries

### Requirement: Research-Paradigm Validation Supports Kaoju
Research-paradigm validation SHALL validate the Kaoju public pack, protected member inventory, command surface, and family-specific evidence contracts.

#### Scenario: Valid Kaoju pack passes
- **WHEN** the public entrypoint and all thirteen declared protected members are valid
- **THEN** shared and Kaoju-specific checks pass

#### Scenario: Invalid Kaoju member reports diagnostics
- **WHEN** a protected member is missing, crosses a resource boundary, has a stale direct invocation, or violates identity mapping
- **THEN** validation reports its logical id, parent pack, file, and rule

#### Scenario: Shared checks preserve family rules
- **WHEN** common pack validation succeeds
- **THEN** trial versus reproduction, evidence, binding, artifact identity, and survey-process checks still run

### Requirement: Research Skill Validation Enforces Shared Resource Ownership
Research validation SHALL enforce bundle-local resources, package-owned machine resources, protected shared routing, and dependency closure.

#### Scenario: Protected member leaves its bundle
- **WHEN** a DeepSci or Kaoju member uses parent traversal or a sibling path
- **THEN** validation fails with the logical id and offending reference

#### Scenario: Shared contract file is named directly
- **WHEN** active guidance instructs an agent to open a family-root machine contract
- **THEN** validation requires the applicable `isomer-cli ext` query

#### Scenario: Cross-member process bypasses shared
- **WHEN** a known family-wide procedure is duplicated or loaded from a sibling
- **THEN** validation requires the corresponding public-parent `shared()` route

#### Scenario: Dependency closure fixture is incomplete
- **WHEN** selective projection omits a declared shared, recording, service, or helper dependency
- **THEN** validation reports every missing logical id
