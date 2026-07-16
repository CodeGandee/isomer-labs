## MODIFIED Requirements

### Requirement: Extension-backed Research Record CRUD
The system SHALL expose a transitional `isomer-cli ext research records` CRUD surface for topic-scoped research records before the native `project records ...` API exists.

#### Scenario: Record create stores runtime lifecycle row
- **WHEN** an actor creates a research record through `isomer-cli ext research records create`
- **THEN** the system writes a Workspace Runtime lifecycle record with record kind, status, topic refs, lifecycle refs, transition metadata, provenance refs, optional content path, and the exact uppercase semantic id when the record is extension-owned

#### Scenario: Record create writes optional body
- **WHEN** the create request includes inline body content or a body file
- **THEN** the system writes or copies the body under the resolved semantic label for that record class and stores the resulting content path on the lifecycle record

#### Scenario: Record show reads one record
- **WHEN** an actor calls `isomer-cli ext research records show <record-id>`
- **THEN** the system returns the selected runtime-backed record and includes body content only when explicitly requested

#### Scenario: Record list filters records
- **WHEN** an actor calls `isomer-cli ext research records list` with filters such as semantic id, record kind, profile, status, producer, or consumer
- **THEN** the system returns only matching records from the selected Topic Workspace

#### Scenario: Record update preserves identity
- **WHEN** an actor updates metadata, status, body, or lifecycle refs through `isomer-cli ext research records update`
- **THEN** the system preserves the record id and exact uppercase semantic id, updates the timestamp, records the mutation metadata, and does not silently rewrite prior provenance refs

#### Scenario: Record delete archives by default
- **WHEN** an actor deletes a research record through `isomer-cli ext research records delete`
- **THEN** the system archives the record by default and does not remove durable body files unless a later accepted contract defines destructive deletion

### Requirement: Topic Actor Research Recording
Research recording APIs SHALL accept records produced by Topic Actors, Project Operator Sessions, Operator Agents, or formal Agent Instances without requiring Agent Team Instance identity for human-orchestrated work.

#### Scenario: Topic Actor creates accepted artifact
- **WHEN** a Topic Actor creates or updates an accepted research artifact through `isomer-cli ext research records`
- **THEN** the recorded lifecycle row and body location include the Research Topic or Topic Workspace context, record kind, exact uppercase semantic id when extension-owned, semantic label, profile metadata, producer metadata, `topic_actor_name`, actor kind or runtime kind when known, controller metadata when known, and optional adapter refs
- **AND** Agent Team Instance, Agent Instance, and formal Agent Workspace refs remain absent unless the record was actually produced inside a launched team context

#### Scenario: Topic Actor records remain queryable with team records
- **WHEN** a later skill queries research records for the selected Topic Workspace
- **THEN** records created by Topic Actors are returned alongside records created by Operator Agents, Execution Adapters, Agent Instances, or Service Agent Instances when they match the same topic, exact uppercase semantic id, record kind, profile, semantic label, producer, or topic actor filters

#### Scenario: Formal adoption is out of scope
- **WHEN** a caller asks to adopt Topic Actor-produced work into a formal Agent Instance or Agent Team Instance identity
- **THEN** the system reports that formal adoption is unsupported by this change
- **AND** it preserves the original Topic Actor production metadata instead of rewriting, copying, or linking it as formal team output

### Requirement: Payload-first Research Record CRUD
The system SHALL expose payload-first validate, create, update, show, list, and render behavior through the transitional `isomer-cli ext research records` surface.

#### Scenario: Validate checks without mutation
- **WHEN** a caller runs `isomer-cli ext research records validate` with `--format-profile`, direct schema or template refs, or schema or template files and a payload file
- **THEN** the command validates the payload through the artifact-format processing engine and returns deterministic JSON diagnostics
- **AND** it does not mutate Workspace Runtime or write generated Markdown files

#### Scenario: Create records payload and lifecycle identity
- **WHEN** a caller runs `isomer-cli ext research records create` with record kind, format profile or schema or template inputs, payload file, valid topic context, and the required canonical identity
- **THEN** the command creates the lifecycle record and structured payload state in the selected Workspace Runtime as one accepted research record
- **AND** the command records the exact uppercase semantic id, skill, producer, consumer, lifecycle refs, Topic Actor metadata, and provenance refs when provided

#### Scenario: Create does not render implicitly
- **WHEN** a caller creates a valid structured research record without `--render markdown`
- **THEN** the command stores the lifecycle record and structured payload state
- **AND** it does not write a generated Markdown view merely because the selected profile contains a Markdown template

#### Scenario: Update preserves identity
- **WHEN** a caller updates a structured research record with a valid replacement payload
- **THEN** the system preserves the lifecycle record id and exact uppercase semantic id
- **AND** it stores the new payload digest, validation outcome, updated timestamp, rendered Markdown locator when rendered, and mutation provenance without silently rewriting prior provenance refs

#### Scenario: Show can separate payload and rendered body
- **WHEN** a caller shows a structured research record
- **THEN** the command can return lifecycle metadata, structured payload JSON, validation diagnostics, generated Markdown locator, and rendered body content as distinct fields

#### Scenario: List can filter structured records
- **WHEN** a caller lists research records
- **THEN** the command can filter or summarize records by exact uppercase semantic id, format profile ref, schema ref, template ref, source kind, validation status, render status, skill, record kind, status, producer, consumer, and lifecycle refs without parsing generated Markdown

#### Scenario: List returns bounded compact summaries by default
- **WHEN** a caller lists structured research records without requesting payload details
- **THEN** the command returns at most the most recent matching records according to `defaults.ext.research.records_list_limit` from the Project Manifest TOML
- **AND** when the Project Manifest does not set `defaults.ext.research.records_list_limit`, the built-in fallback limit is 20
- **AND** each row contains lifecycle identity and status fields plus compact structured metadata, including exact uppercase semantic id, format refs, source kind, validation status, render status, payload digest, generated Markdown locator when known, skill, producer, consumer, and core timestamps
- **AND** it omits full payload JSON, validation diagnostics, render diagnostics, and rendered Markdown content unless explicitly requested

#### Scenario: List limit is caller controlled
- **WHEN** a caller lists structured research records with an explicit limit
- **THEN** the command applies the requested limit to the ordered result set before returning records
- **AND** the explicit request overrides the Project Manifest default for that invocation

### Requirement: Research Record Revision Command
The research recording CLI SHALL provide a revision path that creates a new descendant record for content-changing revisions.

#### Scenario: Revise creates descendant
- **WHEN** a caller revises an accepted structured record with a new payload
- **THEN** the CLI creates a new record, stores the new payload, and creates a canonical `revision_of` lineage edge from the revised record to the new record

#### Scenario: Revise preserves semantic identity
- **WHEN** a caller revises a record with an exact uppercase semantic id
- **THEN** the new record preserves that exact semantic identity for latest-view resolution while retaining a distinct record id
- **AND** the revision path does not derive identity from placeholder metadata, lowercase values, or latest-view hints

#### Scenario: Update remains non-revision
- **WHEN** a caller updates status, actor metadata, file hints, query hints, or repair metadata without changing accepted content
- **THEN** the operation MAY update the existing record without creating a revision edge

### Requirement: Durable Records Support Family-Neutral Semantic Ids
The research recording API and CLI SHALL use `semantic_id` as the sole identity of a durable extension artifact independently of its producing skill and format profile.

#### Scenario: Create records canonical semantic id
- **WHEN** a caller creates a durable extension artifact with an exact value such as `DEEPSCI:MAIN-RUN-RECORD` or `KAOJU:SURVEY-CONTRACT`
- **THEN** Workspace Runtime validates the uppercase `EXTENSION-NAME:WHAT` grammar, confirms ownership through the lowercase extension catalog when available, stores that exact semantic id, and returns it through create, show, list, revision, and query responses
- **AND** structured validation checks it against the selected profile when the profile declares a semantic id

#### Scenario: Extension operation lacks canonical identity
- **WHEN** an extension-owned create, update, revision, list, show, or query request supplies a bare, angle-wrapped, double-bracket, lowercase, mixed-case, unknown, aliased, or missing required semantic id
- **THEN** the operation fails with a structured artifact-identity diagnostic
- **AND** it does not normalize, infer, derive, alias, or persist another identity

#### Scenario: Semantic id is filterable
- **WHEN** a caller lists or queries research records by exact uppercase semantic id
- **THEN** only topic-scoped records authored with that exact semantic id are returned in deterministic order
- **AND** the response preserves record kind, status, family, profile, title, summary, revision state, and content locator when known

#### Scenario: Revision preserves semantic identity
- **WHEN** a caller revises a record carrying an exact uppercase semantic id
- **THEN** the descendant carries the same exact semantic id unless the selected binding explicitly creates a different registered semantic object
- **AND** the prior record remains queryable through revision lineage

#### Scenario: Artifact family remains catalog-shaped
- **WHEN** a structured record contains both `artifact_family` and an uppercase semantic id
- **THEN** validation compares the lowercase `artifact_family` with the lowercase projection of the semantic-id namespace
- **AND** it does not rewrite either field

## REMOVED Requirements

### Requirement: Placeholder Metadata on Research Records
**Reason**: Placeholder transition metadata is an alternate artifact identity and conflicts with the sole uppercase `semantic_id` contract.

**Migration**: Remove `--placeholder`, placeholder filters, placeholder identity storage, and placeholder-derived indexing. No old-form read or write path remains.

### Requirement: Placeholder Compatibility Remains Available
**Reason**: Additive placeholder behavior would preserve two artifact identity systems and violate the requested clean break.

**Migration**: None. Exact uppercase `semantic_id` values are the only supported extension artifact identity for records and queries.
