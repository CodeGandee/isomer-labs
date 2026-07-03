## ADDED Requirements

### Requirement: Progressive Agent Self Query Context
The system SHALL expose process-local self queries as selectable, read-only slices rather than one large default packet.

#### Scenario: Self show is a small index
- **WHEN** `isomer-cli --print-json project self show` runs with resolvable Project context
- **THEN** the response includes only a minimal summary with selected Research Topic and Topic Workspace refs when available, resolved Topic Actor or Agent headline when available, diagnostic counts, and available self query subcommands
- **AND** it does not include full environment listings, broad semantic path lists, full Pixi binding candidates, or recommended query catalogs

#### Scenario: Identity query reports identity only
- **WHEN** `isomer-cli --print-json project self identity` runs from inside the selected Topic Main Development Repository
- **AND** supported launch environment variables provide `ISOMER_RESEARCH_TOPIC_ID` and `ISOMER_AGENT_INSTANCE_ID` or `ISOMER_AGENT_NAME`
- **THEN** the response includes Effective Topic Context identity, Topic Actor context when resolved, Effective Agent Context when resolved, and source metadata
- **AND** the command does not infer Agent Workspace identity from the Topic Main Development Repository cwd
- **AND** it does not include Pixi binding details, semantic path payloads beyond identity-adjacent refs, or broad environment listings

#### Scenario: Self query reports topic actor context only in identity slice
- **WHEN** supported environment variables, cwd, recorded context, or a single manifest default identify a Topic Actor
- **THEN** `project self identity` includes the resolved Topic Actor name, workspace path, binding metadata when available, and source metadata
- **AND** `project self show` includes at most the Topic Actor name and source headline

#### Scenario: Self query degrades without agent identity
- **WHEN** Effective Topic Context resolves but no explicit, environment-derived, cwd-derived, or recorded Effective Agent Context is available
- **THEN** `project self show` reports that Agent identity is unresolved without expanding a full diagnostic packet
- **AND** `project self identity` reports how to provide `--agent`, `--agent-instance`, `ISOMER_AGENT_NAME`, or `ISOMER_AGENT_INSTANCE_ID`

#### Scenario: Self query reports conflicts instead of guessing
- **WHEN** environment identity, explicit selectors, cwd inference, recorded runtime refs, or manifest defaults conflict
- **THEN** the relevant self subcommand reports diagnostics that name the conflicting sources
- **AND** it does not silently choose an Agent Name, Agent Instance, Topic Actor, Research Topic, or Topic Workspace from the conflicting inputs

### Requirement: Agent Self Environment Query
The system SHALL expose recognized Isomer launch environment inputs only through an explicit environment self query.

#### Scenario: Env query reports recognized safe names by default
- **WHEN** `isomer-cli --print-json project self env` runs
- **THEN** the response reports recognized Isomer identity, path, or non-secret configuration variable names, classes, presence, and whether each value influenced resolution
- **AND** it omits values by default
- **AND** it does not include arbitrary environment variables, credentials, tokens, API keys, passwords, or secret-like values

#### Scenario: Env query values require explicit safe-value request
- **WHEN** `project self env` supports a value-emitting option
- **THEN** values are emitted only for allowlisted non-secret identity, path, or configuration refs
- **AND** secret-like variables remain omitted or redacted even when value output is requested

### Requirement: Agent Self Path and Pixi Queries
The system SHALL expose semantic path and Pixi details only through explicit self query subcommands.

#### Scenario: Paths query resolves requested labels only
- **WHEN** a caller runs `isomer-cli --print-json project self paths topic.repos.main agent.workspace`
- **THEN** the response includes only the requested semantic labels and diagnostics needed to resolve them
- **AND** each path entry includes the semantic label, resolved path when available, source, storage profile metadata when available, and diagnostics
- **AND** the command does not include unrelated common paths or a full semantic path catalog

#### Scenario: Paths query requires at least one label
- **WHEN** a caller runs `project self paths` without a semantic label
- **THEN** the command reports that at least one label is required
- **AND** it points callers to `project self queries` or `project paths list` for discovery instead of dumping all paths

#### Scenario: Pixi query returns run hint for selected topic environment
- **WHEN** `isomer-cli --print-json project self pixi` runs for a selected Research Topic with a resolvable Project-root Pixi environment binding or standalone Topic Workspace Pixi binding
- **THEN** the response includes the selected Pixi manifest path, Pixi environment name, binding source, and a Python command form using `pixi run --manifest-path <manifest_path> --environment <pixi_environment> python ...`
- **AND** it does not include identity, environment, or semantic path details beyond what is needed to explain the Pixi selection

#### Scenario: Pixi query does not guess across ambiguous bindings
- **WHEN** multiple active Pixi bindings are available and no single binding can be selected for the Pixi query
- **THEN** the response reports the candidate bindings and a diagnostic instead of emitting a misleading single `pixi run` command

#### Scenario: Pixi query reports missing binding clearly
- **WHEN** no usable Pixi manifest or environment can be resolved for the selected topic
- **THEN** the response includes a diagnostic and points the caller to `project doctor` or topic environment setup rather than using system Python or a local virtual environment

### Requirement: Agent Self Query Catalog
The system SHALL expose safe follow-up commands through an explicit query catalog rather than embedding the catalog in every self response.

#### Scenario: Queries command lists follow-up commands
- **WHEN** `isomer-cli --print-json project self queries` runs
- **THEN** the response includes safe follow-up command examples for `project self identity`, `project self pixi`, `project self env`, `project self paths <semantic-label>`, `project context show`, `project paths get <semantic-label>`, `project paths explain <semantic-label>`, `project topic-actors show`, and topic or runtime inspection commands as applicable
- **AND** the command examples use `--print-json`

#### Scenario: Other self commands do not embed the full query catalog
- **WHEN** `project self show`, `project self identity`, `project self pixi`, `project self env`, or `project self paths` runs
- **THEN** the response may mention the next relevant self command
- **AND** it does not embed the full follow-up query catalog unless the caller explicitly invokes `project self queries`
