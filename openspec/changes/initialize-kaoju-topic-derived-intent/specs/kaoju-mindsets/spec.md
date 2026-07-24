## MODIFIED Requirements

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

## ADDED Requirements

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
