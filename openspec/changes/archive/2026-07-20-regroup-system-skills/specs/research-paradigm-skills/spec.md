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

#### Scenario: Migrated production DeepSci companion skills keep bounded traceability material
- **WHEN** a refactor-migrated production DeepSci companion skill is inspected
- **THEN** it MAY contain `migrate/`, `org/analysis/`, `org/src/`, and passive `templates/` material for migration review and provenance
- **AND** active execution guidance remains in `SKILL.md`, `agents/openai.yaml`, directly linked `references/`, active `assets/`, and active `scripts/`

#### Scenario: Skill frontmatter is valid
- **WHEN** each production DeepSci research-stage skill's `SKILL.md` is inspected
- **THEN** the YAML frontmatter contains `name` and `description` fields
- **AND** the `name` field matches the suffixless `isomer-deepsci-<purpose>` folder name

#### Scenario: Skill manifest exists when a skill is packaged independently
- **WHEN** an extracted research-stage skill is packaged as a standalone skill bundle
- **THEN** it includes an `agents/openai.yaml` manifest with UI-facing metadata

#### Scenario: Old active skill names are removed
- **WHEN** active research-paradigm skill folders and docs are inspected
- **THEN** they do not use `isomer-labs-research-*` as active skill folder names, frontmatter names, manifests, or role mappings

#### Scenario: Protected bundle remains self-contained
- **WHEN** one production DeepSci member is privately projected with its declared dependencies
- **THEN** its active resources resolve without repository siblings or family-root files

#### Scenario: Operator skills are excluded from extension pack
- **WHEN** DeepSci or Kaoju pack contents are inspected
- **THEN** they do not embed core operator or service bundles
- **AND** cross-pack routes use protected logical dependencies

### Requirement: Shared Research Contract
DeepSci shared procedure semantics SHALL remain owned by protected logical capability `isomer-deepsci-shared` and routed through the DeepSci public pack.

#### Scenario: Production DeepSci shared contract defines semantic placeholders
- **WHEN** `skillset/research-paradigm/deepsci/isomer-ext-deepsci-entrypoint/subskills/isomer-deepsci-shared/SKILL.md` and its directly linked references are inspected
- **THEN** they define the production DeepSci research loop, placeholder syntax, placeholder registry location, and rule that placeholders are not storage bindings

#### Scenario: Production DeepSci shared registry defines placeholder semantics
- **WHEN** the production DeepSci semantic-placeholder registry is inspected
- **THEN** each placeholder entry defines id, meaning, minimum content, producer skills, consumer skills, and storage-binding status

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

#### Scenario: Imsight workflow formatting is validated
- **WHEN** the validation harness inspects an enriched active `SKILL.md`
- **THEN** validation confirms it has a near-top `## Workflow`, numbered workflow steps, concise reference routing, and a fallback for tasks that do not map cleanly to the default steps

#### Scenario: File roles are classified before strict checks
- **WHEN** the validation harness runs against `skillset/research-paradigm`
- **THEN** validation classifies Markdown, YAML, scripts, assets, templates, migration notes, provenance notes, source-analysis files, and source-copy files by role before applying active-guidance checks or rule-specific allow zones

#### Scenario: Production DeepSci storage binding remains deferred
- **WHEN** the validation harness inspects active production DeepSci skill text
- **THEN** validation reports active requirements to create concrete Artifact storage, concrete host API records, or source-runtime storage paths unless they are explicitly framed as unsettled, optional source-compatible bridges, provenance, or migration notes

#### Scenario: Self-containment validation runs
- **WHEN** the validation harness inspects enriched skill entrypoints and linked active references
- **THEN** validation confirms they do not actively depend on files outside their own skill directory, except for intentional shared-skill references when the bundle is installed as part of the research-paradigm subtree

#### Scenario: Guessed concrete surfaces are checked
- **WHEN** the validation harness inspects active research-paradigm skill text
- **THEN** validation searches for concrete DeepScientist-style paths, command wrappers, runner homes, and API calls, and confirms unsettled equivalents are marked `yet-to-be-determined`, represented by registered unresolved TBD-surface placeholders, or confined to non-active traceability material

#### Scenario: Whole bundle validation surface is scanned
- **WHEN** the validation harness runs against `skillset/research-paradigm`
- **THEN** validation inspects Markdown, YAML, active scripts, active assets, passive templates, migration notes, provenance notes, source-analysis files, and source-copy files in the subtree with role-aware rule application

#### Scenario: Allow zones preserve explanatory mapping text
- **WHEN** stale source terms, former TBD ids, source-runtime names, or source-local paths appear inside configured provenance files, license notices, deferred-resource notes, source-term mapping sections, rejected-runtime sections, resolved-surface mapping tables, migration notes, source-analysis files, source-copy files, or passive templates
- **THEN** validation allows those occurrences only for the matching rule and continues to reject the same terms when they appear as active skill guidance

#### Scenario: Stale lifecycle and workspace terms are reported
- **WHEN** active research-paradigm skill text uses Research Goal, Research Thread, Research Branch, or Isomer Workspace as current Isomer domain terms
- **THEN** validation reports the stale term and directs the skill text to use Research Topic, Research Inquiry, Research Inquiry Relationship, or Topic Workspace

#### Scenario: Resolved workspace path TBDs are reported
- **WHEN** active research-paradigm skill text emits an ordinary workspace path TBD placeholder such as `[[tbd-surface:path-topic-workspace]]`, `[[tbd-surface:path-agent-workspace]]`, `[[tbd-surface:path-run-logs]]`, `[[tbd-surface:path-experiment-output]]`, `[[tbd-surface:path-analysis-output]]`, `[[tbd-surface:path-paper-layout]]`, or `[[tbd-surface:path-figure-output]]`
- **THEN** validation reports the placeholder as resolved and directs the skill text to use Workspace Path Resolution, semantic workspace scopes, or semantic Artifact kinds

#### Scenario: Unregistered TBD surface is reported
- **WHEN** active research-paradigm skill text emits a `[[tbd-surface:<id>]]` placeholder whose id is absent from the directly linked TBD registry
- **THEN** validation reports the unregistered id and identifies the file and line that emitted it

#### Scenario: Shared TBD registry is canonical
- **WHEN** the validation harness validates `[[tbd-surface:<id>]]` placeholders or resolved former IDs anywhere in active research-paradigm guidance
- **THEN** validation treats `isomer-deepsci-shared/references/tbd-surface-registry.md` as the canonical registry for the subtree

#### Scenario: Local TBD registry mirror drift is reported
- **WHEN** a directly loaded local contract file contains a `## TBD Surface Registry` mirror section
- **THEN** validation confirms the local mirror has exact resolved-ID coverage and normalized resolution text matching the shared registry, and reports missing IDs, extra IDs, or changed resolution meaning

#### Scenario: Hard-coded local and source-analysis paths are reported
- **WHEN** active research-paradigm skill text depends on local absolute paths, source-analysis paths, archived OpenSpec change paths, `extern/orphan` paths, DeepScientist runtime paths, or concrete runner homes outside an allowed provenance, migration, source-copy, passive-template, or deferred-resource zone
- **THEN** validation reports the hard-coded path and directs the skill text to use self-contained references, accepted Isomer contracts, or registered unresolved TBD-surface placeholders

#### Scenario: Concrete broken local reference is reported
- **WHEN** a `SKILL.md` references a concrete local `references/`, `assets/`, or `scripts/` path that does not exist inside the same skill directory
- **THEN** validation reports the broken reference with the referring `SKILL.md` file and line

#### Scenario: Pattern reference is not treated as a concrete broken path
- **WHEN** a `SKILL.md` describes a placeholder path pattern such as `references/packages/<package_id>.md` or `scripts/<script>.py`
- **THEN** validation treats the pattern as documentation of a route-specific resource shape rather than a literal required local file

#### Scenario: Manifest mismatch is reported
- **WHEN** a skill's `agents/openai.yaml` `interface.display_name` does not equal the skill folder and `SKILL.md` frontmatter name, or `interface.default_prompt` does not invoke the same `$isomer-deepsci-*` skill
- **THEN** validation reports the manifest mismatch and identifies the affected manifest field

#### Scenario: Validator tests cover active and non-active zones
- **WHEN** unit tests exercise the research-paradigm validation harness
- **THEN** they include fixtures for expanded production DeepSci inventory, migrated companion-skill traceability directories, passive templates, active stale-term failures, allow-zone acceptance, concrete broken references, pattern references, placeholder registration, storage-binding deferral, and deterministic CLI output

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

#### Scenario: Kaoju template roles remain explicit
- **WHEN** public manager, paper drafting, TeX composition, PDF build, or protected write guidance is inspected
- **THEN** it distinguishes named content templates from named LaTeX templates, including their independent `main` defaults and semantic ids
- **AND** role selection remains explicit command context rather than a new skill boundary

#### Scenario: Kaoju write resources remain protected
- **WHEN** the protected `write` member is inspected after relocation
- **THEN** its entrypoint, artifact bindings, paper references, and role-aware workflow remain inside the `isomer-kaoju-write` bundle
- **AND** public paper commands route to that member without duplicating its private procedure resources

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
- **THEN** trial versus reproduction, evidence, binding, artifact identity, survey-process, content-template, LaTeX-template, composition, build-entrypoint, drift, and historical-record checks still run

#### Scenario: Validator tests cover Kaoju active and invalid zones
- **WHEN** unit tests exercise family-aware research-paradigm validation
- **THEN** they include valid Kaoju fixtures and failures for missing inventory, wrong namespace, manifest mismatch, broken direct references, stale domain terms, hard-coded provider or local paths, procedural-command drift, binding drift, directory scanning, canonical-format violations, external wiki routing, direct environment mutation, Isomer-owned repository acquisition, and pre-verification registration
- **AND** they retain regression fixtures for valid and invalid DeepSci material

### Requirement: Research Skill Validation Enforces Shared Resource Ownership
Research validation SHALL enforce bundle-local resources, package-owned machine resources, protected shared routing, and dependency closure.

#### Scenario: Active extension artifact identity is validated
- **WHEN** the validator inspects an active DeepSci or Kaoju skill, registry, binding projection, generated summary, source declaration, or command example
- **THEN** it requires an exact registered `DEEPSCI:WHAT` or `KAOJU:WHAT` identifier owned by the skill's manifest extension
- **AND** it rejects angle-wrapped, double-bracket, bare, lowercase, mixed-case, wrong-family, unknown, duplicate, aliased, or lossy artifact identities without an old-form exemption

#### Scenario: Protected member leaves its bundle
- **WHEN** a DeepSci or Kaoju member uses parent traversal or a sibling path
- **THEN** validation fails with the logical id and offending reference

#### Scenario: Shared contract file is named directly
- **WHEN** active guidance instructs an agent to open a family-root machine contract
- **THEN** validation requires the applicable `isomer-cli ext` query

#### Scenario: Local binding projection is valid
- **WHEN** a Kaoju skill bundles an `artifact-bindings.md` projection for its own semantic ids
- **THEN** validation accepts the page only when it contains no parent-relative registry dependency, does not repeat the full physical registry, uses exact uppercase identifiers, and routes current resolution through `ext kaoju bindings describe`

#### Scenario: Cross-member process bypasses shared
- **WHEN** a known family-wide procedure is duplicated or loaded from a sibling
- **THEN** validation requires the corresponding bare protected `shared` member route or one of that member's declared subcommands

#### Scenario: Dependency closure fixture is incomplete
- **WHEN** selective projection omits a declared shared, recording, service, or helper dependency
- **THEN** validation reports every missing logical id

#### Scenario: Flat projection fixtures exercise the boundary
- **WHEN** unit tests validate the production Kaoju family or an invalid Kaoju fixture
- **THEN** they copy each skill to an ordinary non-symlink projection with no family-root contracts and test extension queries separately from skill-local links
- **AND** fixtures cover parent traversal, missing local resources, direct registry paths, missing extension-query routing, shared-procedure bypass, and every noncanonical artifact identity class
