# kaoju-mindsets Specification

## Purpose
TBD - created by archiving change add-kaoju-mindsets. Update Purpose after archive.
## Requirements
### Requirement: Kaoju Treats a Missing Mindset Source as Optional Run State
For an applicable action, Kaoju SHALL treat verified absence of the selected deterministic Mindset Source file as permission to proceed without mindset reflection, persist that decision on the Run, and create no Mindset Record.

#### Scenario: Selected Source file is absent
- **WHEN** an applicable action resolves one mindset key and its deterministic direct-child Source file does not exist
- **THEN** the entrypoint begins the Run, records disposition `skipped_source_missing` with Source status `missing`, Record status `absent`, and reason `source_missing`, and proceeds without producing `KAOJU:MINDSET-RECORD`
- **AND** it does not create the Source, read a packaged seed, invent questions, or use conversation memory as a substitute

#### Scenario: Existing Source file is invalid
- **WHEN** the selected deterministic path exists but its file is unreadable, malformed, unsafe, mismatched, ambiguous, or schema-invalid
- **THEN** the action blocks with exact diagnostics and the explicit Kaoju `create-topic` repair route
- **AND** it cannot record the file as missing or proceed under `skipped_source_missing`

#### Scenario: Source appears after absence was recorded
- **WHEN** a Source is added after an active Run recorded `skipped_source_missing`
- **THEN** that Run continues without a Mindset Record and preserves its original absence posture
- **AND** a restarted or later Run re-evaluates the deterministic path and may materialize the new Source

#### Scenario: User explicitly requests Source generation
- **WHEN** the user invokes Kaoju `create-topic` or explicitly asks the topic-creation owner to create missing Sources
- **THEN** the topic-creation workflow may generate and validate the requested Source files from packaged defaults and topic intent
- **AND** concrete research execution does not invoke that mutation implicitly

### Requirement: Applicable Kaoju Runs Persist One Mindset Resolution
Each applicable Kaoju Run SHALL persist exactly one immutable mindset resolution before focused-owner dispatch so later stages can distinguish a usable Mindset Record from verified Record absence.

#### Scenario: Run uses a Mindset Record
- **WHEN** the selected Source validates and its Run-scoped Mindset Record is created
- **THEN** the Run records disposition `recorded`, Source status `present`, Record status `available`, the selected key, deterministic Source locator, and verified Record ref
- **AND** the Record ref is included in the Run input refs and downstream handoffs

#### Scenario: Run has no Mindset Record
- **WHEN** the selected deterministic Source file is absent
- **THEN** the Run records disposition `skipped_source_missing`, Source status `missing`, Record status `absent`, selected key, deterministic Source locator, and reason `source_missing`
- **AND** downstream handoffs carry the Run ref and skipped resolution without a placeholder Record ref

#### Scenario: Resolution is repeated
- **WHEN** a caller repeats the exact persisted mindset resolution
- **THEN** the operation is idempotent and returns the current Run posture
- **AND** a different key, disposition, or Record ref is rejected as a conflicting mid-Run rewrite

#### Scenario: Applicable Run has no resolution
- **WHEN** a focused consumer receives an applicable Run with neither a verified `recorded` nor `skipped_source_missing` resolution
- **THEN** it pauses as an orchestration error
- **AND** it does not infer optionality merely from an absent Record ref

### Requirement: Kaoju Provides a Topic-Creation Owner
The packaged Kaoju extension SHALL provide protected capability `isomer-kaoju-topic-creator` as member `topic-creator` at invocation designator `isomer-ext-kaoju-entrypoint->topic-creator`, with the generic Topic Creator as its delegated platform owner and typed Kaoju template services as its deterministic template-state boundary rather than embedded implementation dependencies.

#### Scenario: Protected member is inspected
- **WHEN** the packaged Kaoju manifest and entrypoint are inspected
- **THEN** `isomer-kaoju-topic-creator` appears exactly once below the public entrypoint and has a context-aware protected routing row
- **AND** it owns packaged mindset defaults and Kaoju-specific derived-intent orchestration without appearing as an independently discoverable public skill or taking ownership of writing-template semantics

#### Scenario: New Kaoju topic is requested
- **WHEN** the user invokes public Kaoju command `create-topic` with concrete topic substance
- **THEN** the protected owner delegates generic Project, Research Topic, Topic Workspace, Workspace Runtime, and `topic.intent.overview` work to `isomer-op-entrypoint->topic-create`
- **AND** after generic readiness it derives missing Kaoju Mindset Sources and invokes the typed ensure-defaults boundary for content and LaTeX `main` stock and plural-path exports

#### Scenario: Generic topic creation is invoked directly
- **WHEN** a user creates a Research Topic through the generic Topic Creator without invoking Kaoju `create-topic`
- **THEN** generic creation remains complete according to its own contract and creates no Kaoju Mindset Source, named writing-template record, or writing-template export
- **AND** later ordinary Kaoju research actions do not create missing Mindset Sources or named topic stock implicitly

#### Scenario: Generic topic begins Kaoju research without initialization
- **WHEN** an ordinary Kaoju action selects a generic topic whose Mindset Source and default named template are both absent
- **THEN** the Run records `skipped_source_missing` for the applicable mindset and proceeds without mindset reflection
- **AND** a default-consuming paper operation may use its checked packaged writing-template fallback without creating topic-derived intent

#### Scenario: Kaoju is installed after topic creation
- **WHEN** Kaoju skills are installed after one or more Research Topics already exist
- **THEN** installation registers or materializes the skill pack without enumerating topics, writing Mindset Sources, creating named template records, or exporting templates
- **AND** each topic acquires topic-owned Kaoju derived intent only through explicit `create-topic` or an explicit repair request

### Requirement: Kaoju Distinguishes Mindset Source and Mindset Record
Kaoju SHALL use **Mindset Source** for one current topic-derived question-list JSON file beneath `topic.intent.kaoju_mindsets` and **Mindset Record** for the Run-scoped materialized-answer Artifact `KAOJU:MINDSET-RECORD`.

#### Scenario: Mindset Source is inspected
- **WHEN** an agent or user reads a topic Mindset Source
- **THEN** it is owner-editable derived intent with a path, `mindset_key`, and content digest but no Artifact semantic id, stable Artifact ref, current-state record, or revision chain
- **AND** its “Source” term does not mean the paper, repository, or evidence source under examination

#### Scenario: Mindset Record is inspected
- **WHEN** an agent or user reads a Mindset Record
- **THEN** it is a revisioned Run-scoped Artifact containing the exact question-and-note snapshot, materialized answers, evidence, active survey context, supplemental rows, and unresolved posture used by that Run
- **AND** its “Record” term does not replace the generic Artifact Core Record term

#### Scenario: Bare mindset mutation is requested
- **WHEN** the user asks to update or add to “the mindset” without identifying the Mindset Source, Mindset Record, or both
- **THEN** the agent pauses for Source-versus-Record clarification before mutation
- **AND** it does not infer the target from the currently loaded file or Artifact

### Requirement: Kaoju Mindset Source JSON Is Closed and Reflective
A valid Mindset Source SHALL contain a bounded reusable self-questioning list without executable or authority-bearing fields.

#### Scenario: Valid Mindset Source is inspected
- **WHEN** a Source is validated
- **THEN** it contains `schema_version`, path-independent `mindset_key`, purpose, applicability, optional derivation metadata, an ordered fixed `questions` array, and one repeatable `additional_question_collector`
- **AND** each fixed question and collector has a unique noncolliding `question_id`, prompt, bounded `additional_notes`, required posture, answer expectation, and evidence expectation

#### Scenario: Question notes are empty
- **WHEN** a fixed or collector question has `additional_notes` equal to `""`
- **THEN** the agent proceeds from the prompt, answer and evidence expectations, pinned survey context, and ordinary understanding
- **AND** it does not infer missing user-specific guidance

#### Scenario: Source content is low authority
- **WHEN** a Source question or `additional_notes` requests behavior that conflicts with instructions, procedure boundaries, Gates, or authorization
- **THEN** the higher-authority contract prevails and the Mindset Record marks the affected answer unresolved or not applicable with rationale
- **AND** the Source cannot schedule a Workflow Stage, execute a tool or command, authorize a resource, satisfy a Gate, accept evidence, or override an instruction

#### Scenario: Invalid fields or bounds are supplied
- **WHEN** a Source contains undeclared command, tool, Workflow Stage, Gate, provider payload, system-prompt, instruction-priority, unsafe path, duplicate id, excessive content, or another unsupported field
- **THEN** semantic validation rejects the file with its path and affected field or limit
- **AND** no consumer uses a partial projection of the invalid file

### Requirement: Kaoju Ships Validated Default Mindset Seeds
The protected Kaoju topic-creation bundle SHALL own schema-valid default JSON resources for `paper.deep-dive`, `paper.skimming`, and `source-code.ingest` under `assets/defaults/mindsets/`.

#### Scenario: Default catalog is validated
- **WHEN** packaged Kaoju validation runs
- **THEN** every default has a unique `mindset_key`, filename and body key equality, unique question ids, bounded content, valid applicability, empty `additional_notes` on every fixed and collector question, and a deterministic digest
- **AND** `paper.deep-dive`, `paper.skimming`, and `source-code.ingest` contain exactly 8, 6, and 8 ordered fixed questions respectively plus one repeatable `additional-questions` collector

#### Scenario: Additional-question collector is inspected
- **WHEN** any packaged default is inspected
- **THEN** its collector id is `additional-questions` and its exact prompt is “Did the user explicitly assign any additional questions to this Mindset Record that the fixed Mindset Source questions do not cover?”
- **AND** its answer expectation is “Register only questions explicitly targeted to the Mindset Record. Save ordinary paper or source-code questions and findings in the applicable reading Artifacts. If no additional questions were explicitly assigned, record none.”
- **AND** the collector is repeatable, has empty `additional_notes`, and does not count toward the 8, 6, or 8 fixed-question inventory

#### Scenario: Paper deep-dive default is inspected
- **WHEN** the packaged `paper.deep-dive` default is inspected
- **THEN** its ordered question ids and exact prompts are:
  1. `survey-role`: How does this paper relate to the active survey question, accepted boundary, and selected direction, and what role could it play in the survey?
  2. `survey-relevant-claims`: Which of the paper's claims directly answer, support, challenge, refine, or fall outside the active survey question?
  3. `portfolio-novelty`: Relative to works already represented in the survey, what is genuinely new, duplicative, complementary, or contradictory?
  4. `comparison-mechanism`: Which mechanisms, assumptions, definitions, and method components matter to the survey's comparison dimensions?
  5. `survey-claim-evidence`: Which exact sections, equations, figures, tables, or appendices support or challenge the survey-relevant claims, and what is my interpretation rather than a source statement?
  6. `evaluation-transferability`: Do the datasets, metrics, baselines, controls, and ablations test the claims under conditions that fit the survey's scope and intended comparisons?
  7. `boundary-limitations`: Which limitations, failure modes, contradictions, missing implementation details, or reproducibility gaps restrict how this paper can be used in the survey?
  8. `survey-update-and-gaps`: What updates to the survey taxonomy, comparison structure, Claim-Evidence Ledger, or reading path should I recommend, and which survey questions remain unresolved?

#### Scenario: Paper-skimming default is inspected
- **WHEN** the packaged `paper.skimming` default is inspected
- **THEN** its ordered question ids and exact prompts are:
  1. `survey-fit`: What exact work and version am I inspecting, and how does it fit the active survey question, boundary, and selected direction?
  2. `topic-relevant-claim`: What survey-relevant problem and principal claim can I establish at the inspection depth actually achieved?
  3. `portfolio-relation`: Does this work add a new contribution, duplicate known work, complement a current category, or challenge an existing survey claim?
  4. `survey-evidence-signal`: What is the strongest visible evidence relevant to the survey, where is it located, and what evidence depth have I actually achieved?
  5. `scope-and-credibility-risk`: Which assumptions, evaluation settings, missing comparisons, contradictions, or identity and access uncertainties limit its relevance to this survey?
  6. `survey-triage`: What survey disposition should I recommend: deep dive, defer, or exclude from the current boundary, what gap would it fill, and what must be verified first?

#### Scenario: Source-code ingestion default is inspected
- **WHEN** the packaged `source-code.ingest` default is inspected
- **THEN** its ordered question ids and exact prompts are:
  1. `survey-role-and-identity`: How does this exact repository revision relate to the active survey question, selected direction, and associated works, and what are its source, license, and access posture?
  2. `survey-relevant-architecture`: Which entrypoints and modules implement the concepts, methods, data paths, or evaluators that matter to the survey?
  3. `claim-code-map`: Which survey-relevant paper claims, equations, or algorithms map to exact files and symbols, and what remains unmatched?
  4. `behavior-path`: How do inputs, preprocessing, method logic, evaluation, and outputs connect for the behavior relevant to the survey?
  5. `comparison-sensitive-configuration`: Which defaults, flags, seeds, thresholds, dependencies, hardware, datasets, or services could change the survey's interpretation or comparison?
  6. `survey-evidence-surfaces`: What do tests, examples, benchmarks, and existing logs establish about the survey-relevant claims without executing the repository?
  7. `paper-code-divergence`: What is missing, stale, stubbed, inconsistent, or divergent from the associated paper or the role assigned to this source in the survey?
  8. `survey-readiness-and-risks`: What further source inspection, environment preparation, bounded trial, or reproduction should I recommend for the survey, and what blockers, side effects, or resource risks qualify that recommendation?

#### Scenario: Pack is materialized without a repository checkout
- **WHEN** an installed package materializes the Kaoju pack
- **THEN** all default JSON and generation guidance remain available within `isomer-kaoju-topic-creator`
- **AND** validation and topic derivation do not require a repository checkout or undeclared family-root file

### Requirement: Kaoju Topic Creation Derives Topic-Specific Mindset Sources
The Kaoju topic-creation owner SHALL derive missing Mindset Sources from `topic.intent.overview` and the packaged seeds after resolving the topic's semantic mindset root.

#### Scenario: New topic has a concrete overview
- **WHEN** Kaoju `create-topic` resolves one concrete `topic.intent.overview` and no Mindset Source exists for a required seed key
- **THEN** the owner reads the overview and seed, creates one validated topic Source at `<mindset_key>.json`, and reports its semantic root, path, key, and digest
- **AND** it records optional derivation metadata identifying the overview label and digest and seed resource version and digest used

#### Scenario: Agent specializes a seed
- **WHEN** topic-specific concerns in the overview materially improve the self-questioning list
- **THEN** the agent preserves the `mindset_key` and collector contract but may adapt, add, remove, or replace fixed questions and populate `additional_notes`
- **AND** reused question concepts retain stable ids, new or concept-changing questions receive unique stable ids, and the resulting fixed count need not equal the seed's 8, 6, or 8 count

#### Scenario: Future survey context is not yet available
- **WHEN** the topic is created before a Direction Set or Survey Contract exists
- **THEN** generated questions refer dynamically to the active survey context that will be pinned when used and may encode only stable topic concerns from the overview
- **AND** they do not invent or freeze a future direction, boundary, evidence portfolio, or comparison contract

#### Scenario: Topic offers no useful specialization
- **WHEN** the concrete overview provides no sound basis for changing a valid packaged seed
- **THEN** the owner may copy the seed unchanged into the resolved root
- **AND** the copied JSON is a valid directly editable Mindset Source rather than a pointer to package content

#### Scenario: Required intent is missing
- **WHEN** no concrete overview or unambiguous Topic Workspace can be resolved
- **THEN** Kaoju delegates only the missing generic topic-intent prerequisite to `isomer-op-entrypoint->topic-create` when the concrete request authorizes it, otherwise it pauses with the missing stage and exact recovery route
- **AND** it passes no mindset schema, seed JSON, semantic path, generation rule, or other Kaoju-specific intent into the generic owner and does not generate from a generic topic id, conversation memory, or another topic

### Requirement: Existing Mindset Sources Remain User-Controlled
Kaoju SHALL preserve an existing valid topic Mindset Source across explicit topic creation, lazy create-missing preflight, repair, retry, and package upgrade until the user explicitly edits, regenerates, replaces, or reconciles it.

#### Scenario: Create-missing repeats
- **WHEN** explicit `create-topic` or lazy ensure runs again and a valid Source already exists for a seed key
- **THEN** it reports the existing path and digest as preserved and creates only missing keys
- **AND** it does not compare seed wording to infer permission to overwrite user content

#### Scenario: User edits a Source directly
- **WHEN** a user changes questions or bounded `additional_notes` in a Source and the result validates
- **THEN** the edited file becomes the current authoritative Source for later Runs
- **AND** no export, import, Artifact revise, or specialized mindset CLI operation is required

#### Scenario: User copies a packaged default
- **WHEN** a user copies a default resource to its deterministic path beneath the resolved root and the filename, body key, and schema validate
- **THEN** the file becomes the topic's current Source for that key
- **AND** later package updates do not replace it automatically

#### Scenario: User explicitly requests regeneration
- **WHEN** the user asks the Kaoju topic-creation owner to regenerate, replace, or reconcile one existing Source
- **THEN** the owner re-reads the current file and digest, prepares and validates the proposed replacement, and writes it atomically only while the observed base remains current
- **AND** it reports old and new digests and preserves the active Run snapshots that cite the old digest

#### Scenario: Overview derivation has drifted
- **WHEN** optional Source provenance cites an older `topic.intent.overview` digest
- **THEN** status or an applicable workflow may report advisory derivation drift and the explicit reconcile route
- **AND** it does not regenerate or block solely because the overview changed when the Source remains valid

#### Scenario: Existing Source is invalid
- **WHEN** a Source path exists but JSON, filename, key, schema, bounds, or content validation fails
- **THEN** creation and applicable use block with the exact path, field diagnostics, and repair route
- **AND** no packaged default silently replaces or masks the invalid file

### Requirement: Applicable Kaoju Actions Select and Snapshot a Mindset Source
The Kaoju entrypoint SHALL resolve one topic Mindset Source for each action whose checked process route requires one and SHALL either snapshot a valid current file into a Run-scoped Mindset Record or persist verified file absence on the Run before substantive action work starts.

#### Scenario: User selects an applicable key
- **WHEN** the user explicitly supplies a `mindset_key` whose applicability includes the selected action
- **THEN** the entrypoint resolves the deterministic file beneath `topic.intent.kaoju_mindsets` ahead of process-route defaults
- **AND** it records either the exact Source snapshot and Record ref or the verified missing-Source resolution for that key

#### Scenario: Process route selects a default key
- **WHEN** no explicit key is supplied and the checked process contract has an unambiguous action, source-kind, and depth route
- **THEN** deep or full-text paper examination selects `paper.deep-dive`, skim or triage paper examination selects `paper.skimming`, and repository or source-tree examination selects `source-code.ingest`
- **AND** selection resolves the topic file rather than reading the packaged seed

#### Scenario: Required Source is missing
- **WHEN** the selected deterministic topic Source file does not exist
- **THEN** the action records `skipped_source_missing` on the Run and proceeds to focused-owner dispatch without a Mindset Record
- **AND** it reports the selected key, missing path, and explicit Kaoju `create-topic` route for enabling the mindset in a later Run

#### Scenario: Required Source is invalid at final selection
- **WHEN** the exact topic file exists but is ambiguous, unreadable, mismatched, unsafe, or invalid when the entrypoint revalidates it for Run snapshot
- **THEN** the Run does not proceed to focused-owner dispatch and reports the selected key, semantic path diagnostics, and repair route
- **AND** it does not overwrite the file, mark it missing, or substitute packaged content

#### Scenario: Required active survey context is unavailable
- **WHEN** a present Source must be materialized but the canonical Research Topic or one unambiguous current `KAOJU:SURVEY-CONTRACT` revision cannot be resolved
- **THEN** the action pauses before substantive work with the missing, stale, conflicting, or ambiguous state and exact resume hint
- **AND** it does not answer the mindset against an unpinned survey frame

#### Scenario: Source changes during a Run
- **WHEN** the topic Source changes or appears after the Run's recorded mindset resolution starts
- **THEN** a `recorded` Run continues to answer its exact snapshot while a `skipped_source_missing` Run continues without mindset reflection
- **AND** the changed or new Source applies only to a restarted or later Run

### Requirement: Mindset Records Preserve Answers and Evidence
Each Run that uses a Mindset Source SHALL maintain a revisioned `KAOJU:MINDSET-RECORD` current-state Artifact containing the exact Source snapshot, active survey context, answers, explicitly Record-targeted supplemental questions, evidence refs, Source-update disposition, collector posture, and unresolved questions.

#### Scenario: Mindset Record starts
- **WHEN** a required Source is validated for a Run
- **THEN** the entrypoint creates or resolves one current Mindset Record in Run scope with Source locator and digest, pinned Research Topic and Survey Contract refs, optional present survey-context refs, one materialized row per Source question, collector posture, and an initially empty supplemental list
- **AND** every row includes the exact prompt and `additional_notes` and begins with an explicit unanswered posture rather than a fabricated answer

#### Scenario: Reflective work progresses
- **WHEN** an answer state, rationale, collector posture, or evidence set changes during the action
- **THEN** the entrypoint revises the Run-scoped Mindset Record with optimistic concurrency and preserves the prior revision
- **AND** it does not re-read changed Source content to alter the current Run inventory

#### Scenario: Run reaches a terminal posture
- **WHEN** the action completes, pauses, or blocks
- **THEN** the terminal Record marks every materialized Source and explicitly assigned supplemental answer as answered, unresolved, or not applicable, records the collector as checked, and retains exact evidence refs and unresolved questions
- **AND** incomplete reflection remains visible rather than silently treated as satisfied

### Requirement: Explicit Targeting Controls Mindset Source and Record Updates
Applicable Kaoju reading and source-examination workflows SHALL preserve ordinary reading Artifacts as the default destination and SHALL update a Mindset Source, Mindset Record, or both only when the user explicitly targets that object.

#### Scenario: User asks an ordinary follow-up question
- **WHEN** the user asks a paper or source-code question without naming the Mindset Source or Mindset Record
- **THEN** the consumer records the answer or unresolved posture in the applicable `KAOJU:SOURCE-DIGEST`, `KAOJU:CLAIM-EVIDENCE-LEDGER`, `KAOJU:ASSOCIATED-SOURCE-CODE`, or other reading Artifact
- **AND** it does not add a supplemental Record row or edit the Source file

#### Scenario: User targets the Mindset Record
- **WHEN** the user explicitly assigns an uncovered question to the current Mindset Record
- **THEN** the consumer appends one bounded supplemental row with a Record-local id, exact prompt, empty-by-default `additional_notes`, origin, explicit Record association basis, current workflow stage, disposition `record_only`, answer state, answer or rationale, and evidence refs
- **AND** it leaves the Source file unchanged

#### Scenario: User targets the Mindset Source
- **WHEN** the user explicitly adds or edits a Source question or `additional_notes` without targeting the current Record
- **THEN** the authorized agent validates and safely updates the derived-intent file against its observed digest
- **AND** the current Record receives no supplemental row and remains pinned to its original snapshot

#### Scenario: User targets both Source and Record
- **WHEN** the user explicitly assigns a question to the current Record and requests its reuse in the Source
- **THEN** the Record first stores `source_update_requested`, and the authorized agent validates and safely updates the Source file
- **AND** the Record changes the row to `source_updated` with the new Source path and digest after success while retaining its original active snapshot

#### Scenario: Agent-generated additions are authorized
- **WHEN** the user explicitly asks the agent to add questions it identifies to the Mindset Record or both objects
- **THEN** supplemental rows may use origin `agent` and retain the explicit user association basis
- **AND** source-driven observations without that instruction remain in ordinary reading Artifacts

#### Scenario: Collector is evaluated at closeout
- **WHEN** an applicable examination reaches closeout
- **THEN** the consumer evaluates `additional-questions`, verifies that every explicitly Record-targeted question has a separate supplemental row, and records that the collector was checked even when no additions were assigned
- **AND** it does not sweep ordinary conversation questions or source-driven observations into the Mindset Record

### Requirement: First-Version Mindset Management Uses Topic Files
The first version SHALL use the resolved derived-intent directory and Kaoju topic-creation workflow instead of a specialized mindset manager or CLI command group.

#### Scenario: User wants to view or modify a Source
- **WHEN** a user asks to inspect or edit one Mindset Source
- **THEN** the agent resolves `topic.intent.kaoju_mindsets`, selects the deterministic key file, and performs the authorized read or direct validated edit
- **AND** it does not require `mindsets list`, `show`, `export`, `import`, `reset`, or `bootstrap`

#### Scenario: Command inventories are validated
- **WHEN** public commands, protected members, and typed Kaoju CLI groups are inspected
- **THEN** there is no public `manage-mindset`, no protected `isomer-kaoju-mindsets` manager or eight-leaf management tree, and no `isomer-cli ext kaoju mindsets` group
- **AND** generic Artifact operations remain available only for Mindset Records

### Requirement: Applying Edited Mindset Sources Preserves Run History
Kaoju SHALL treat a valid direct Mindset Source edit as current topic intent for later applicable Runs and SHALL use an apply request to validate and report that state without manufacturing or rewriting Artifact records.

#### Scenario: Edited Mindset Source validates
- **WHEN** a user edits a deterministic Mindset Source and asks the agent to apply modified derived material
- **THEN** the agent validates the filename, `mindset_key`, closed schema, and current digest and reports the Source as accepted current intent
- **AND** it does not create a Mindset Source Artifact, import record, or redundant named state

#### Scenario: Later Run selects the edited Source
- **WHEN** a later applicable Run begins after a valid Source edit
- **THEN** it resolves and snapshots the edited current Source according to the ordinary mindset-selection contract
- **AND** its Mindset Record preserves the new Source digest and exact question content independently of earlier Runs

#### Scenario: Existing Run already resolved a mindset
- **WHEN** an active or completed Run already recorded `recorded` or `skipped_source_missing` before the edit
- **THEN** applying the edited Source leaves that Run's resolution and Mindset Record unchanged
- **AND** the agent does not retarget, synthesize, or revise the historical snapshot

#### Scenario: Edited Source is invalid
- **WHEN** the apply request finds an unreadable, mismatched, unsafe, malformed, or schema-invalid Mindset Source
- **THEN** it reports the exact path, key, digest when available, and validation diagnostics
- **AND** it does not classify the file as missing, use the packaged seed at Run time, or mutate any Mindset Record
