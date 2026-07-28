## MODIFIED Requirements

### Requirement: Kaoju Ships Validated Default Mindset Seeds
The protected Kaoju topic-creation bundle SHALL own schema-valid v2 default JSON resources for `paper.deep-dive`, `paper.skimming`, `paper.lecture`, and `source-code.ingest` under `assets/defaults/mindsets/`.

#### Scenario: Default catalog is validated
- **WHEN** packaged Kaoju validation runs
- **THEN** every default has a unique `mindset_key`, filename and body key equality, unique question ids, bounded content, valid applicability, empty `additional_notes` on every fixed and collector question, exactly one question set named `default`, and a deterministic digest
- **AND** each packaged `default` set has triggering condition “Use when no specialized question set matches the task and active Run context.” and uses `question_ids: "all"` to select all fixed questions in catalog order
- **AND** `paper.deep-dive`, `paper.skimming`, `paper.lecture`, and `source-code.ingest` contain exactly 8, 6, 12, and 8 ordered fixed questions respectively plus one repeatable `additional-questions` collector

#### Scenario: Additional-question collector is inspected
- **WHEN** any packaged default is inspected
- **THEN** its collector id is `additional-questions` and its exact prompt is “Did the user explicitly assign any additional questions to this Mindset Record that the fixed Mindset Source questions do not cover?”
- **AND** its answer expectation is “Register only questions explicitly targeted to the Mindset Record. Save ordinary paper or source-code questions and findings in the applicable reading Artifacts. If no additional questions were explicitly assigned, record none.”
- **AND** the collector is repeatable, has empty `additional_notes`, and does not count toward the packaged fixed-question inventory

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

#### Scenario: Paper-lecture default is inspected
- **WHEN** the packaged `paper.lecture` default is inspected
- **THEN** its ordered question ids and exact prompts are:
  1. `survey-section-role`: Why does this paper warrant a dedicated detailed section in the active survey, and what role must that section play in the survey's argument?
  2. `reader-contract`: What should the intended reader understand after the section, and which prerequisites must the section introduce?
  3. `problem-setting-and-notation`: Which problem setting, assumptions, definitions, and notation must be established before explaining the method?
  4. `method-intuition`: What is the method's central intuition, and why do its major design choices follow from that intuition?
  5. `method-walkthrough`: What is the method's ordered algorithm, architecture, data flow, or reasoning process at enough detail for standalone comprehension?
  6. `worked-trace`: Which concrete example, worked derivation, or execution trace best helps a reader follow the method, and what source evidence supports it?
  7. `equation-teaching-plan`: Which equations are essential to understanding the method, what does every symbol mean, and how should each equation be interpreted or derived in the survey?
  8. `display-teaching-plan`: Which original figures or tables are essential, what does each show, and should the survey reproduce, adapt, redraw, describe, or omit each one?
  9. `evidence-and-results`: Which experiments, analyses, or theoretical results establish the method's main claims, and how strong is that evidence?
  10. `comparison-and-positioning`: How does the method differ from its closest alternatives along the survey's accepted comparison dimensions?
  11. `limitations-and-failure-modes`: Which assumptions, limitations, failure cases, contradictions, and unresolved details qualify the explanation?
  12. `section-outline-and-readiness`: What is the proposed dedicated-section sequence, and what evidence, explanation, display, permission, or interpretation gaps still block lecture-ready status?

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
- **AND** reused question concepts retain stable ids, new or concept-changing questions receive unique stable ids, question sets select `"all"` or reference canonical questions many-to-many, and the resulting fixed count need not equal the packaged seed count

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

### Requirement: Applicable Kaoju Actions Select and Snapshot a Mindset Source
The Kaoju entrypoint SHALL resolve one topic Mindset Source for each action whose checked process route requires one and SHALL either snapshot a valid current file into a Run-scoped Mindset Record or persist verified file absence on the Run before substantive action work starts.

#### Scenario: User selects an applicable key
- **WHEN** the user explicitly supplies a `mindset_key` whose applicability includes the selected action
- **THEN** the entrypoint resolves the deterministic file beneath `topic.intent.kaoju_mindsets` ahead of process-route defaults
- **AND** it records either the exact Source snapshot and Record ref or the verified missing-Source resolution for that key

#### Scenario: Process route selects a default key
- **WHEN** no explicit key is supplied and the checked process contract has an unambiguous action, source-kind, and depth route
- **THEN** lecture-depth paper examination selects `paper.lecture`, deep or full-text paper examination selects `paper.deep-dive`, skim or triage paper examination selects `paper.skimming`, and repository or source-tree examination selects `source-code.ingest`
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
