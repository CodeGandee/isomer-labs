## ADDED Requirements

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

## MODIFIED Requirements

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

## REMOVED Requirements

### Requirement: Kaoju Lazily Ensures Mindset Sources Before Concrete Work
**Reason**: Concrete-action create-missing makes absence impossible to use as an owner-controlled opt-out and conflicts with the required durable skipped posture.

**Migration**: Use explicit Kaoju `create-topic` or an explicit topic-creator create-missing request to generate Sources. Concrete Runs inspect only the selected deterministic file and persist verified absence when it is missing.
