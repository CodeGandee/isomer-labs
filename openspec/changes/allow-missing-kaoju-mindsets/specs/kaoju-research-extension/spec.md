## MODIFIED Requirements

### Requirement: Kaoju Process Contract Declares Mindset Routes
The checked Kaoju survey-process contract SHALL expose deterministic mindset route and missing-Source resolution metadata for applicable actions without embedding topic Source bodies or treating packaged defaults as runtime fallback.

#### Scenario: Entrypoint loads the checked contract
- **WHEN** `isomer-ext-kaoju-entrypoint` runs `isomer-cli --print-json ext kaoju process show`
- **THEN** the response includes mindset schema version, required action routes, applicability selectors, selected keys, Source semantic label `topic.intent.kaoju_mindsets`, Record semantic id `KAOJU:MINDSET-RECORD`, the `topic-creator` repair designator, and resolution mode `record-or-skip-missing-per-run`
- **AND** it does not embed topic-owned questions, answers, a `KAOJU:MINDSET-SOURCE` id, or a package-default runtime fallback

#### Scenario: Process and seed inventories diverge
- **WHEN** package validation compares process routes, packaged seed keys, protected resource metadata, and Source validators
- **THEN** missing, extra, duplicated, unresolved, or inapplicable required seed keys fail validation
- **AND** the diagnostic names the route and affected key

### Requirement: Applicable Kaoju Workflows Enforce Mindset Injection
The public Kaoju entrypoint and every first-version consuming system-skill workflow SHALL resolve and persist either a verified Run-scoped Mindset Record or a verified missing-Source posture before focused work, and SHALL condition reflection and closeout on that persisted resolution.

#### Scenario: Concrete Kaoju action enters extension preflight
- **WHEN** one reconciled topic receives a concrete mutation-bearing Kaoju command whose checked route requires a mindset
- **THEN** the entrypoint selects the route key and inspects its deterministic topic Source without invoking create-missing
- **AND** it blocks on invalid existing state but treats verified file absence as an allowed Run posture

#### Scenario: Installed pack sees existing topics
- **WHEN** Kaoju installation or materialization completes while Research Topics already exist
- **THEN** no topic is scanned or mutated as part of installation or later concrete research preflight
- **AND** those topics may proceed with `skipped_source_missing` until the user explicitly invokes Kaoju topic preparation

#### Scenario: Read-only public route enters preflight
- **WHEN** welcome, help, `explore`, or a status-only management route observes missing mindset state
- **THEN** it reports the state and the explicit `create-topic` preparation route without invoking create-missing
- **AND** the read-only route begins no research Run and writes no Source, Run resolution, or Record

#### Scenario: Entrypoint begins an applicable procedure Run with a present Source
- **WHEN** the checked route requires a mindset and the selected topic Source validates
- **THEN** the entrypoint begins the Run, pins active survey context, snapshots the Source into a Mindset Record, records disposition `recorded`, and includes the verified Record ref in Run inputs and downstream handoffs before focused-owner dispatch
- **AND** it pauses without dispatch when the present Source, Record, or required survey-context state cannot be validated

#### Scenario: Entrypoint begins an applicable procedure Run with a missing Source
- **WHEN** the checked route requires a mindset and the deterministic selected Source file does not exist
- **THEN** the entrypoint begins the Run, records disposition `skipped_source_missing`, and dispatches the focused owner with the Run ref, selected key, and missing posture but no Mindset Record ref
- **AND** it does not create an empty Record, invoke the topic creator, or substitute packaged questions

#### Scenario: Reading-item workflow selects an inspection depth
- **WHEN** `commands/ingest-reading-item.md` resolves a paper to skim or triage depth or to deep or full-text depth
- **THEN** it selects `paper.skimming` or `paper.deep-dive` respectively and accepts either that key's verified Record ref or the Run's verified `skipped_source_missing` posture
- **AND** absent or ambiguous depth still pauses instead of selecting a key by guesswork

#### Scenario: Source-code workflow reaches examination
- **WHEN** `commands/ingest-source-code.md` is ready to dispatch repository or source-tree examination
- **THEN** it selects `source-code.ingest` and accepts either its verified Record ref or the Run's verified `skipped_source_missing` posture
- **AND** acquisition or registration evidence does not substitute for either resolution

#### Scenario: Examine consumes the Run mindset resolution
- **WHEN** `isomer-kaoju-examine/SKILL-MAIN.md` receives an applicable paper, repository, or source-tree task
- **THEN** it loads and answers a verified `recorded` snapshot or skips all mindset question, collector, revision, and terminal-Record work for verified `skipped_source_missing`
- **AND** it pauses when the resolution is missing, conflicting, mismatched, or references an invalid Record

#### Scenario: Ordinary follow-up question is asked
- **WHEN** the user asks a paper or source-code question without explicitly targeting a Mindset Source or Mindset Record
- **THEN** the applicable workflow saves the answer or unresolved posture in its existing reading Artifacts regardless of the Run's mindset resolution
- **AND** it does not infer Record association from timing, topic relevance, or the fact that a mindset is active or absent

#### Scenario: Applicable Run reaches closeout with a Record
- **WHEN** a `recorded` examination Run attempts completion or claim-bearing acceptance
- **THEN** it requires a terminal Mindset Record revision whose materialized Source and explicitly assigned supplemental rows have terminal answer states, whose collector is checked, and whose ref appears in the terminal report and applicable output lineage
- **AND** a missing or nonterminal referenced Record prevents `complete`

#### Scenario: Applicable Run reaches closeout without a Record
- **WHEN** a `skipped_source_missing` examination Run attempts completion or claim-bearing acceptance
- **THEN** it may complete without `KAOJU:MINDSET-RECORD` and reports the selected key, missing Source posture, and absent Record ref in the terminal report
- **AND** absence of both a Record and a verified skipped Run resolution prevents `complete`
