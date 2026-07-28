## MODIFIED Requirements

### Requirement: Kaoju Mindset Source JSON Is Closed and Reflective
A valid Mindset Source v2 SHALL contain a bounded reusable self-questioning catalog and question-set mappings without executable or authority-bearing fields.

#### Scenario: Valid Mindset Source v2 is inspected
- **WHEN** a v2 Source is validated
- **THEN** it contains `schema_version`, path-independent `mindset_key`, purpose, applicability, optional derivation metadata, an ordered fixed `questions` catalog, an ordered `question_sets` array, and one repeatable `additional_question_collector`
- **AND** each fixed question and collector has a unique noncolliding `question_id`, prompt, bounded `additional_notes`, required posture, answer expectation, and evidence expectation
- **AND** each question set has a unique `question_set_id`, one bounded nonempty `triggering_condition`, and `question_ids` equal to either `"all"` or an ordered nonempty array of question ids

#### Scenario: Many-to-many question membership is validated
- **WHEN** a v2 Source declares its question sets
- **THEN** `"all"` expands to every canonical question in catalog order, every explicit question-set reference resolves to one canonical question, every canonical question belongs to at least one expanded set, and a question may belong to multiple sets
- **AND** one explicit list cannot repeat a question id and exactly one set has the reserved id `default`

#### Scenario: Question notes are empty
- **WHEN** a fixed or collector question has `additional_notes` equal to `""`
- **THEN** the agent proceeds from the prompt, answer and evidence expectations, pinned survey context, and ordinary understanding
- **AND** it does not infer missing user-specific guidance

#### Scenario: Source content is low authority
- **WHEN** a Source question, question-set triggering condition, or `additional_notes` requests behavior that conflicts with instructions, procedure boundaries, Gates, or authorization
- **THEN** the higher-authority contract prevails and the Mindset Record marks the affected answer unresolved or not applicable with rationale when the question was materialized
- **AND** the Source cannot schedule a Workflow Stage, execute a tool or command, authorize a resource, satisfy a Gate, accept evidence, or override an instruction

#### Scenario: Invalid fields or bounds are supplied
- **WHEN** a Source contains undeclared command, tool, Workflow Stage, Gate, provider payload, system-prompt, instruction-priority, unsafe path, unresolved question reference, a `question_ids` string other than `"all"`, missing or duplicate `default` set, duplicate id, excessive content, or another unsupported field
- **THEN** semantic validation rejects the file with its path and affected field or limit
- **AND** no consumer uses a partial projection of the invalid file

### Requirement: Kaoju Ships Validated Default Mindset Seeds
The protected Kaoju topic-creation bundle SHALL own schema-valid v2 default JSON resources for `paper.deep-dive`, `paper.skimming`, and `source-code.ingest` under `assets/defaults/mindsets/`.

#### Scenario: Default catalog is validated
- **WHEN** packaged Kaoju validation runs
- **THEN** every default has a unique `mindset_key`, filename and body key equality, unique question ids, bounded content, valid applicability, empty `additional_notes` on every fixed and collector question, exactly one question set named `default`, and a deterministic digest
- **AND** each packaged `default` set has triggering condition “Use when no specialized question set matches the task and active Run context.” and uses `question_ids: "all"` to select all fixed questions in catalog order
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
The Kaoju topic-creation owner SHALL derive missing v2 Mindset Sources from `topic.intent.overview` and the packaged seeds after resolving the topic's semantic mindset root.

#### Scenario: New topic has a concrete overview
- **WHEN** Kaoju `create-topic` resolves one concrete `topic.intent.overview` and no Mindset Source exists for a required seed key
- **THEN** the owner reads the overview and seed, creates one validated v2 topic Source at `<mindset_key>.json`, and reports its semantic root, path, key, and digest
- **AND** it records optional derivation metadata identifying the overview label and digest and seed resource version and digest used

#### Scenario: Agent specializes a seed
- **WHEN** topic-specific concerns in the overview materially improve the self-questioning catalog or identify stable task variants
- **THEN** the agent preserves the `mindset_key`, collector contract, and one nonempty `default` set but may adapt, add, remove, or replace fixed questions, populate `additional_notes`, and add or edit specialized question sets
- **AND** reused question concepts retain stable ids, new or concept-changing questions receive unique stable ids, question sets select `"all"` or reference canonical questions many-to-many, and the resulting fixed count need not equal the seed's 8, 6, or 8 count

#### Scenario: Future survey context is not yet available
- **WHEN** the topic is created before a Direction Set or Survey Contract exists
- **THEN** generated questions and triggering conditions refer dynamically to the active task and survey context that will be pinned when used and may encode only stable topic concerns from the overview
- **AND** they do not invent or freeze a future direction, boundary, evidence portfolio, comparison contract, or Run task

#### Scenario: Topic offers no useful specialization
- **WHEN** the concrete overview provides no sound basis for changing a valid packaged seed
- **THEN** the owner may copy the seed unchanged into the resolved root
- **AND** the copied JSON is a valid directly editable v2 Mindset Source whose `default` set preserves existing behavior rather than a pointer to package content

#### Scenario: Required intent is missing
- **WHEN** no concrete overview or unambiguous Topic Workspace can be resolved
- **THEN** Kaoju delegates only the missing generic topic-intent prerequisite to `isomer-op-entrypoint->topic-create` when the concrete request authorizes it, otherwise it pauses with the missing stage and exact recovery route
- **AND** it passes no mindset schema, seed JSON, semantic path, generation rule, or other Kaoju-specific intent into the generic owner and does not generate from a generic topic id, conversation memory, or another topic

### Requirement: Mindset Records Preserve Answers and Evidence
Each Run that uses a Mindset Source SHALL maintain a revisioned `KAOJU:MINDSET-RECORD` current-state Artifact containing the immutable selected question-set snapshot, active survey context, answers, explicitly Record-targeted supplemental questions, evidence refs, Source-update disposition, collector posture, and unresolved questions.

#### Scenario: Mindset Record starts from a v2 Source
- **WHEN** a required v2 Source and one selected question set are validated for a Run
- **THEN** the entrypoint creates or resolves one current Mindset Record in Run scope with Source schema version, locator and digest, pinned Research Topic and Survey Contract refs, optional present survey-context refs, selected set id, selection kind, exact triggering condition, nonempty selection rationale, one materialized row per expanded question in the selected set, collector posture, and an initially empty supplemental list
- **AND** every row includes the exact canonical prompt and `additional_notes` and begins with an explicit unanswered posture rather than a fabricated answer

#### Scenario: Mindset Record starts from a v1 Source
- **WHEN** a required legacy v1 Source is validated for a new Run
- **THEN** the entrypoint materializes its complete ordered flat question list as implicit set `default` with selection kind `legacy-default`, a null triggering condition, and a compatibility rationale
- **AND** it does not rewrite the Source or omit any fixed question

#### Scenario: Reflective work progresses
- **WHEN** an answer state, rationale, collector posture, or evidence set changes during the action
- **THEN** the entrypoint revises the Run-scoped Mindset Record with optimistic concurrency and preserves the prior revision
- **AND** it does not re-read changed Source content or re-evaluate question-set triggering conditions to alter the current Run inventory

#### Scenario: Run reaches a terminal posture
- **WHEN** the action completes, pauses, or blocks
- **THEN** the terminal Record marks every materialized Source and explicitly assigned supplemental answer as answered, unresolved, or not applicable, records the collector as checked, and retains exact evidence refs and unresolved questions
- **AND** incomplete reflection remains visible rather than silently treated as satisfied

## ADDED Requirements

### Requirement: Kaoju Selects One Question Set for Each Mindset Record
For each Run that resolves a present Mindset Source v2, the Kaoju entrypoint SHALL select exactly one question set before creating the Mindset Record.

#### Scenario: One specialized question set matches
- **WHEN** one non-default question set's triggering condition best matches the concrete task and pinned Run context
- **THEN** the agent selects that set with selection kind `matched` and records a nonempty rationale
- **AND** the Record materializes only that set's expanded questions in explicit-list or canonical-catalog order plus the always-present additional-question collector

#### Scenario: Several specialized question sets appear applicable
- **WHEN** more than one non-default triggering condition appears to match
- **THEN** the agent selects the single closest match and explains why it fits the task better than the alternatives
- **AND** it does not union, intersect, or otherwise combine question sets

#### Scenario: No specialized question set matches
- **WHEN** no non-default triggering condition applies to the concrete task and pinned Run context
- **THEN** the agent selects question set `default` with selection kind `default-fallback` and records that no specialized set matched
- **AND** it does not treat fallback as a missing or ambiguous mindset resolution

#### Scenario: Default is the only question set
- **WHEN** a valid v2 Source contains no specialized question sets
- **THEN** the agent selects `default` without inventing another set or condition
- **AND** the resulting question inventory preserves the behavior declared by that Source

#### Scenario: Selection input is invalid
- **WHEN** materialization receives an unknown set id, `matched` for `default`, `default-fallback` for a specialized set, an empty rationale, or a triggering condition that differs from the selected v2 Source set
- **THEN** typed validation rejects Record creation with exact diagnostics
- **AND** the Run does not persist a `recorded` mindset resolution

#### Scenario: Selected question belongs to several sets
- **WHEN** the selected set references a question that also belongs to another set
- **THEN** the selected set materializes that canonical question once at its declared position
- **AND** membership in the unselected set does not add, remove, or duplicate a Record row

#### Scenario: Source or task changes after selection
- **WHEN** Source content, triggering conditions, task wording, or survey context changes after a Run creates its Mindset Record
- **THEN** the Run retains its selected set, rationale, and materialized question inventory
- **AND** a restarted or later Run performs a new selection from its current Source and context

### Requirement: Kaoju Preserves Legacy Flat Mindset Sources
Kaoju SHALL continue to accept a valid Mindset Source v1 as a default-only compatibility form while emitting v2 for new or explicitly regenerated Sources.

#### Scenario: Existing v1 Source survives package upgrade
- **WHEN** topic creation, create-missing, repair inspection, or package upgrade encounters an existing valid v1 Source
- **THEN** Kaoju preserves the file and reports it as valid current topic intent
- **AND** it does not rewrite the file merely to add explicit question sets

#### Scenario: Existing v1 Source is used
- **WHEN** an applicable later Run selects an existing valid v1 Source
- **THEN** Kaoju treats the complete flat question list as implicit set `default`
- **AND** no natural-language question-set selection is required

#### Scenario: Source is explicitly regenerated
- **WHEN** the user authorizes replacement or regeneration of a v1 Source
- **THEN** the topic-creation owner emits a validated v2 Source with exactly one explicit `default` set
- **AND** observed-digest checks and existing user-control requirements still govern replacement

#### Scenario: Historical Record predates question sets
- **WHEN** Kaoju reads or renders a valid historical Mindset Record without question-set selection fields
- **THEN** the Record remains valid and preserves its original immutable question snapshot
- **AND** Kaoju does not synthesize selection metadata into the historical revision
