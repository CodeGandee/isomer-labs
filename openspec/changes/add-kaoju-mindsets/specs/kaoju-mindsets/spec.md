## ADDED Requirements

### Requirement: Kaoju Provides a Topic-Creation Owner
The packaged Kaoju extension SHALL provide protected capability `isomer-kaoju-topic-creator` as member `topic-creator` at invocation designator `isomer-ext-kaoju-entrypoint->topic-creator`, with the generic Topic Creator as its delegated platform owner rather than an embedded implementation dependency.

#### Scenario: Protected member is inspected
- **WHEN** the packaged Kaoju manifest and entrypoint are inspected
- **THEN** `isomer-kaoju-topic-creator` appears exactly once below the public entrypoint and has a context-aware protected routing row
- **AND** it owns packaged mindset defaults and Kaoju-specific derivation guidance without appearing as an independently discoverable public skill

#### Scenario: New Kaoju topic is requested
- **WHEN** the user invokes public Kaoju command `create-topic` with concrete topic substance
- **THEN** the protected owner delegates generic Project, Research Topic, Topic Workspace, and `topic.intent.overview` work to `isomer-op-entrypoint->topic-create`
- **AND** it derives Kaoju Mindset Sources only after one concrete overview and resolved Topic Workspace exist

#### Scenario: Generic topic creation is invoked directly
- **WHEN** a user creates a Research Topic through the generic Topic Creator without invoking Kaoju `create-topic`
- **THEN** generic creation remains complete according to its own contract and creates no Kaoju Mindset Source
- **AND** the first later concrete mutation-bearing Kaoju action runs extension-local create-missing ensure without adding a mindset contract to the generic creator

#### Scenario: Kaoju is installed after topic creation
- **WHEN** Kaoju skills are installed after one or more Research Topics already exist
- **THEN** installation registers or materializes the skill pack without enumerating topics or writing Mindset Sources
- **AND** each topic is initialized independently only when an explicit Kaoju `create-topic` request or its first concrete mutation-bearing Kaoju action selects that topic

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

### Requirement: Kaoju Lazily Ensures Mindset Sources Before Concrete Work
The public Kaoju entrypoint SHALL run an extension-local create-missing preflight before beginning the first concrete mutation-bearing Kaoju research Run for a selected topic whose Mindset Sources have not yet been initialized.

#### Scenario: Concrete Kaoju action finds missing Sources
- **WHEN** a mutation-bearing Kaoju command has one reconciled Research Topic and concrete `topic.intent.overview` but one or more packaged default keys have no Source file
- **THEN** the entrypoint routes `isomer-kaoju-topic-creator` in create-missing mode before beginning the research Run, preserves every existing valid Source, and generates and validates every missing default-key Source
- **AND** it proceeds to Run creation only after the selected action's required Source and all create-missing results are valid

#### Scenario: Topic was created before Kaoju installation
- **WHEN** the first concrete Kaoju action selects an existing topic after the Kaoju pack became available
- **THEN** the same extension-local preflight initializes missing Sources from the topic overview and packaged seeds
- **AND** neither the installer nor the generic Topic Creator needs a callback, extension descriptor, mindset path, or generation rule

#### Scenario: Read-only Kaoju request finds missing Sources
- **WHEN** welcome, help, `explore`, or a status-only management request observes missing Mindset Sources
- **THEN** it reports the uninitialized posture and exact `create-topic` or concrete-action route without writing files
- **AND** read-only intent does not authorize lazy create-missing mutation

#### Scenario: Selected topic or mutation authority is unavailable
- **WHEN** lazy ensure lacks one reconciled topic, enough concrete overview substance, or authority to create topic-local derived intent
- **THEN** it pauses before Run creation with the ambiguity or missing authority and exact resume route
- **AND** it does not scan sibling topics, generate in a guessed workspace, or open a research Run solely to record the failed ensure attempt

#### Scenario: Existing Source is invalid during lazy ensure
- **WHEN** create-missing preflight finds an existing Source with invalid filename, key, JSON, schema, or bounded content
- **THEN** it preserves the file and pauses before Run creation with exact diagnostics and repair route
- **AND** it does not overwrite the file, use a packaged default in its place, or create the research Run under partial mindset readiness

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
The Kaoju entrypoint SHALL resolve one topic Mindset Source for each action whose checked process route requires one, validate its current file, snapshot it into a Run-scoped Mindset Record, and hand the Record ref to every consumer before substantive action work starts.

#### Scenario: User selects an applicable key
- **WHEN** the user explicitly supplies a `mindset_key` whose applicability includes the selected action
- **THEN** the entrypoint resolves the deterministic file beneath `topic.intent.kaoju_mindsets` ahead of process-route defaults
- **AND** it records the semantic root, relative path, key, content digest, and exact question snapshot in the Mindset Record

#### Scenario: Process route selects a default key
- **WHEN** no explicit key is supplied and the checked process contract has an unambiguous action, source-kind, and depth route
- **THEN** deep or full-text paper examination selects `paper.deep-dive`, skim or triage paper examination selects `paper.skimming`, and repository or source-tree examination selects `source-code.ingest`
- **AND** selection resolves the topic file rather than reading the packaged seed

#### Scenario: Required Source remains missing after ensure
- **WHEN** extension-local create-missing preflight cannot produce the action's required topic Source
- **THEN** the action pauses before Run creation with the selected key, creation diagnostics, and exact Kaoju `create-topic` repair route
- **AND** it does not invent a Source, use conversation memory, or fall back to a packaged resource

#### Scenario: Required Source is invalid at final selection
- **WHEN** the exact topic file is ambiguous or invalid when the entrypoint revalidates it for Run snapshot
- **THEN** the Run does not proceed to focused-owner dispatch and reports the selected key, semantic path diagnostics, and repair route
- **AND** it does not overwrite the file or substitute packaged content

#### Scenario: Required active survey context is unavailable
- **WHEN** the canonical Research Topic or one unambiguous current `KAOJU:SURVEY-CONTRACT` revision cannot be resolved
- **THEN** the action pauses before substantive work with the missing, stale, conflicting, or ambiguous state and exact resume hint
- **AND** it does not answer the mindset against an unpinned survey frame

#### Scenario: Source changes during a Run
- **WHEN** the topic Source changes after the Run's Mindset Record starts
- **THEN** the active Run continues to answer its exact snapshotted questions and notes and cites the original digest
- **AND** the changed Source applies only to a restarted or later Run

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
