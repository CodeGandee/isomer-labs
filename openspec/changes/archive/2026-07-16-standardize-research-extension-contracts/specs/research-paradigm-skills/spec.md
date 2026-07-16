## ADDED Requirements

### Requirement: Research Skill Validation Enforces Shared Resource Ownership
The research-paradigm validation harness SHALL enforce the skill/shared-resource contract and canonical uppercase artifact identity contract for production research skill families without relying on repository symlink layout.

#### Scenario: Active extension artifact identity is validated
- **WHEN** the validator inspects an active DeepSci or Kaoju skill, registry, binding projection, generated summary, source declaration, or command example
- **THEN** it requires an exact registered `DEEPSCI:WHAT` or `KAOJU:WHAT` identifier owned by the skill's manifest extension
- **AND** it rejects angle-wrapped, double-bracket, bare, lowercase, mixed-case, wrong-family, unknown, duplicate, aliased, or lossy artifact identities without an old-form exemption

#### Scenario: Kaoju active reference leaves its bundle
- **WHEN** the validator finds parent traversal, a sibling-skill link, a family-root contract path, or an absolute source path in active Kaoju filesystem guidance
- **THEN** it fails with the skill, file, line when available, and offending reference
- **AND** it directs a private resource into the owning skill or a shared machine resource behind `isomer-cli ext kaoju`

#### Scenario: Kaoju guidance names a shared contract file
- **WHEN** active Kaoju guidance names `survey-process.v2.json`, `bindings.v2.json`, `bindings.v2.schema.json`, or their package locations as an agent-readable authority
- **THEN** validation fails and names the required `ext kaoju process` or `ext kaoju bindings` query
- **AND** internal package loader code and passive source-provenance material remain outside this active-guidance rule

#### Scenario: Local binding projection is valid
- **WHEN** a Kaoju skill bundles an `artifact-bindings.md` projection for its own semantic ids
- **THEN** validation accepts the page only when it contains no parent-relative registry dependency, does not repeat the full physical registry, uses exact uppercase identifiers, and routes current resolution through `ext kaoju bindings describe`

#### Scenario: Cross-skill process uses Kaoju shared
- **WHEN** a Kaoju stage needs the family-wide evidence, source identity, lineage, Gate, owner-routing, recording, or terminal process
- **THEN** validation requires routing to `isomer-kaoju-shared`
- **AND** it rejects active sibling-file traversal or a known duplicated full process that bypasses the shared skill

#### Scenario: Flat projection fixtures exercise the boundary
- **WHEN** unit tests validate the production Kaoju family or an invalid Kaoju fixture
- **THEN** they copy each skill to an ordinary non-symlink projection with no family-root contracts and test extension queries separately from skill-local links
- **AND** fixtures cover parent traversal, missing local resources, direct registry paths, missing extension-query routing, shared-procedure bypass, and every noncanonical artifact identity class

### Requirement: Production DeepSci Skills Use Canonical Artifact Identifiers
Active production DeepSci skills SHALL use exact uppercase `DEEPSCI:WHAT` artifact identifiers throughout their workflow, registry, binding, source, and record-operation guidance.

#### Scenario: Existing DeepSci registry is replaced
- **WHEN** a DeepSci migration registry or binding page is inspected
- **THEN** every registered artifact uses the deterministic canonical form obtained by removing the old wrapper, converting underscores to hyphens, retaining uppercase letters, and prefixing `DEEPSCI:`
- **AND** the replacement inventory is implementation-only, registry-to-binding coverage remains one-to-one, and no runtime conversion table remains

#### Scenario: Active DeepSci prose names an artifact
- **WHEN** a DeepSci workflow step names an expected input, output, control object, route decision, report, or handoff
- **THEN** it uses the exact registered `DEEPSCI:WHAT` identifier
- **AND** it does not use an angle-wrapped token, double-bracket form, bare object name, lowercase value, or mixed-case value

#### Scenario: DeepSci binding performs a record operation
- **WHEN** an active DeepSci binding page shows how to create, update, revise, list, show, or query a durable artifact
- **THEN** the command passes or filters by the canonical identifier through `--semantic-id`
- **AND** it does not use `--placeholder` or ask the agent or source code to translate between representations

#### Scenario: DeepSci pipeline control artifacts are qualified
- **WHEN** `isomer-deepsci-pipeline` produces or consumes recipe context, terminal report, run record, or resume packet state
- **THEN** it uses `DEEPSCI:PIPELINE-RECIPE-CONTEXT`, `DEEPSCI:PIPELINE-TERMINAL-REPORT`, `DEEPSCI:PIPELINE-RUN-RECORD`, or `DEEPSCI:PIPELINE-RESUME-PACKET` respectively
- **AND** the same identifiers appear in pipeline guidance, bindings, profiles when declared, source constants, record metadata, and tests

#### Scenario: DeepSci source and package mirrors agree
- **WHEN** validation compares the source DeepSci skill tree with packaged system-skill assets
- **THEN** every active artifact identifier and binding reference agrees exactly
- **AND** no source or packaged skill copy retains a superseded artifact identity

### Requirement: Research Skill Validation Preserves Unrelated Family Rules
Adding shared-resource and artifact-identity checks SHALL preserve existing DeepSci and Kaoju content, inventory, binding, evidence, and command-surface validation except where the uppercase clean break explicitly replaces artifact identity behavior.

#### Scenario: Shared boundary validation is introduced
- **WHEN** the research-paradigm validation suite runs after the resource and identifier refactor
- **THEN** existing valid DeepSci and Kaoju behavior continues to pass except for guidance or fixtures that use a removed artifact identity or violate the new ownership boundary
- **AND** family-specific diagnostics unrelated to artifact identity retain their existing meaning and deterministic identifiers where defined

## MODIFIED Requirements

### Requirement: Writing Artifacts Use Paper-Line Placeholder Bindings
The research-paradigm production DeepSci skillset SHALL map writing-related uppercase artifact identifiers to paper-line storage profiles through local `placeholder-bindings.md` pages while preserving the same identifiers in workflow prose.

#### Scenario: Paper contract binding uses a paper contract view
- **WHEN** a production DeepSci skill binds an uppercase artifact identifier that represents the active paper contract, selected outline, evidence view, paper view, section writing plan, or claim-evidence boundary
- **THEN** the binding maps it to an Isomer record kind and profile that preserves its paper-line role, such as `view_manifest` with `paper.contract.selected-outline`, `artifact` with `paper.outline.*`, or `view_manifest` with `paper.claim-evidence-map`

#### Scenario: Paper control surfaces use view records
- **WHEN** a production DeepSci skill binds an uppercase artifact identifier that represents the paper evidence ledger, experiment matrix, manuscript validation, outline validation, paper-line state, or another paper control surface
- **THEN** the binding uses `topic.records.views` with a paper-specific profile such as `paper.evidence-ledger`, `paper.experiment-matrix`, `paper.validation.*`, or `paper.line-state`

#### Scenario: Paper bodies use artifact records
- **WHEN** a production DeepSci skill binds an uppercase artifact identifier that represents manuscript drafts, LaTeX material, bibliography files, compile reports, PDFs, review reports, rebuttal packets, response letters, final summaries, or paper bundle manifests
- **THEN** the binding uses `topic.records.artifacts` with a paper, review, rebuttal, figure, release, or package profile rather than a generic report or handoff profile when a more precise profile exists

#### Scenario: Paper work queues use task records when resumable
- **WHEN** a production DeepSci skill binds an uppercase artifact identifier that represents a resumable writing plan, reviewer-linked evidence TODO, or paper-facing work queue
- **THEN** the binding uses `research_task` under `topic.records.tasks` when the item must be resumed, assigned, or queried as work, and may use `view_manifest` only when the item is a read-only board

#### Scenario: Binding commands include queryable paper metadata
- **WHEN** a production DeepSci skill binding provides an `isomer-cli ext research records` create or update command for a writing-related artifact
- **THEN** the command includes the exact uppercase `--semantic-id`, `--semantic-label`, `--profile`, `--skill`, producer, consumer, and natural query metadata such as `selected_outline_ref`, `paper_surface`, `package_type`, `section_id`, `claim_id`, or `reviewer_item_id`

#### Scenario: Binding convention avoids paper-specific semantic labels
- **WHEN** writing-related production DeepSci binding pages are updated
- **THEN** they use existing semantic labels such as `topic.records.views`, `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, and `topic.records.logs`
- **AND** they do not introduce paper-specific top-level semantic labels as required storage surfaces

#### Scenario: Workflow identifiers remain stable
- **WHEN** writing-related binding rows are updated
- **THEN** `SKILL.md` workflow prose keeps the exact registered uppercase identifiers and relies on `placeholder-bindings.md` for storage mapping

#### Scenario: Registry definitions change only for real drift
- **WHEN** implementation inspects writing-related migration registries
- **THEN** it changes semantic definitions only when an artifact is missing or its kind conflicts with the durable storage role that the binding page must express

## REMOVED Requirements

### Requirement: Production DeepSci Semantic Placeholder Contract
**Reason**: The double-bracket and lower-case placeholder grammar conflicts with the exact uppercase extension artifact identity used by skill prose, source code, record APIs, and other research extensions.

**Migration**: Replace every active DeepSci artifact reference with its registered `DEEPSCI:WHAT` identifier and remove old parsing, registry, and record behavior without a compatibility reader.

### Requirement: Binding Pages Preserve Workflow Flexibility
**Reason**: Preserving an angle-wrapped workflow token requires family-specific translation and makes workflow prose disagree with the durable artifact identity.

**Migration**: Keep storage choices in local binding pages, but use the same exact uppercase `DEEPSCI:WHAT` identifier in workflow prose, source declarations, and binding rows.

### Requirement: DeepSci Research Skill Behavior Remains Compatible
**Reason**: The old requirement protects placeholder behavior that this clean-break change intentionally removes.

**Migration**: Preserve DeepSci method, evidence, lineage, payload, display, profile, and validation behavior that is unrelated to artifact identity; replace artifact identity behavior with the uppercase contract only.
