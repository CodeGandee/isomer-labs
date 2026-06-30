## ADDED Requirements

### Requirement: DeepScientist Compatibility Command Surface
The system SHALL expose a DeepScientist-flavored extension command surface at `isomer-cli ext deepsci`, including a canonical compatibility dispatcher `call <namespace.tool>` that accepts a JSON object using DeepScientist MCP argument names and can emit the DeepScientist-compatible tool result object without the normal Isomer CLI wrapper.

#### Scenario: Compatibility call preserves input names
- **WHEN** a caller invokes `isomer-cli ext deepsci call memory.list_recent` with input JSON `{"scope":"quest","limit":10}`
- **THEN** the extension passes `scope` and `limit` to the mock `memory.list_recent` implementation without renaming, nesting, or translating those fields into Isomer-specific argument names

#### Scenario: Compatibility call emits raw tool result
- **WHEN** a caller invokes a supported tool through the compatibility dispatcher in raw JSON mode
- **THEN** stdout contains the DeepScientist-compatible tool result object for that tool rather than an `isomer-cli-output.v1` wrapper

#### Scenario: Unsupported tool returns deterministic error
- **WHEN** a caller invokes `isomer-cli ext deepsci call artifact.unknown_tool`
- **THEN** the command returns a deterministic JSON error that names the unsupported tool and does not write compatibility storage rows

### Requirement: Source-discovered Tool Registry
The system SHALL recognize the DeepScientist source-discovered tool names for the initial compatibility mock: `memory.write`, `memory.read`, `memory.search`, `memory.list_recent`, `memory.promote_to_global`, `bash_exec.bash_exec`, and artifact tools `record`, `science`, `checkpoint`, `git`, `prepare_branch`, `activate_branch`, `submit_idea`, `list_research_branches`, `resolve_runtime_refs`, `get_paper_contract`, `get_paper_contract_health`, `validate_manuscript_coverage`, `validate_academic_outline`, `validate_manuscript_language`, `compile_outline_to_writing_plan`, `get_quest_state`, `get_global_status`, `get_research_map_status`, `get_benchstore_catalog`, `get_start_setup_context`, `get_method_scoreboard`, `get_optimization_frontier`, `read_quest_documents`, `get_conversation_context`, `get_analysis_campaign`, `record_main_experiment`, `create_analysis_campaign`, `submit_paper_outline`, `list_paper_outlines`, `submit_paper_bundle`, `record_analysis_slice`, `publish_baseline`, `attach_baseline`, `confirm_baseline`, `overwrite_baseline`, `waive_baseline`, `arxiv`, `refresh_summary`, `render_git_graph`, `interact`, and `complete_quest`.

#### Scenario: Memory tools are registered
- **WHEN** a caller asks the extension for supported `memory` tool names
- **THEN** the result includes exactly `write`, `read`, `search`, `list_recent`, and `promote_to_global`

#### Scenario: Artifact tools are registered
- **WHEN** a caller invokes one of the listed artifact tool names through `isomer-cli ext deepsci call artifact.<tool>`
- **THEN** the dispatcher routes the call to a recognized artifact mock instead of rejecting the name as unknown

#### Scenario: Bash exec tool is registered
- **WHEN** a caller invokes `isomer-cli ext deepsci call bash_exec.bash_exec`
- **THEN** the dispatcher routes the call to the `bash_exec` mock with the same JSON argument object

### Requirement: SQLite-backed Compatibility Storage
The system SHALL store DeepScientist compatibility mock state in extension-owned tables inside the selected Topic Workspace Workspace Runtime SQLite database.

#### Scenario: Runtime database is used for writes
- **WHEN** a compatibility command writes memory, artifact, or bash session state
- **THEN** the command writes rows to extension-owned tables in the selected Topic Workspace `state.sqlite`

#### Scenario: Compatibility state survives reopen
- **WHEN** a caller writes compatibility state, exits the CLI process, and later reopens the same Topic Workspace runtime
- **THEN** the previously written compatibility rows are available to later `ext deepsci` calls

#### Scenario: DeepScientist file layout is not created
- **WHEN** a compatibility command writes mock state
- **THEN** the command does not create DeepScientist quest markdown memory files, virtualenv directories, daemon state, or DeepScientist-specific storage layout as the source of truth

### Requirement: Mock Memory Tools
The system SHALL implement `memory.write`, `memory.read`, `memory.search`, `memory.list_recent`, and `memory.promote_to_global` as durable SQLite-backed mocks that preserve DeepScientist-compatible card and list response shapes.

#### Scenario: Write returns card shape
- **WHEN** a caller invokes `memory.write` with `kind`, `title`, `body` or `markdown`, `scope`, `tags`, and `metadata`
- **THEN** the result includes DeepScientist-compatible card fields including `id`, `title`, `type`, `scope`, `path`, `metadata`, `body`, `updated_at`, and `excerpt`

#### Scenario: Tags are normalized
- **WHEN** a caller invokes `memory.write` with tags as either a list or a comma-separated string
- **THEN** the stored card metadata exposes tags as a normalized list matching DeepScientist behavior

#### Scenario: Search returns count and items
- **WHEN** a caller invokes `memory.search` with `query`, `scope`, `limit`, and optional `kind`
- **THEN** the result includes `ok: true`, `count`, and `items`, and each item includes DeepScientist-compatible fields such as `id`, `title`, `type`, `path`, `document_id`, `excerpt`, `updated_at`, `writable`, `scope`, and `shared`

#### Scenario: Recent list uses Python query behavior
- **WHEN** a caller invokes `memory.list_recent` with `scope`, `limit`, and optional `kind`
- **THEN** Python service code queries SQLite rows and returns the newest matching cards in the DeepScientist-compatible `ok`, `count`, and `items` shape

#### Scenario: Promote updates global visibility
- **WHEN** a caller invokes `memory.promote_to_global` for an existing card by id or path
- **THEN** the result returns a DeepScientist-compatible card shape whose scope/global visibility reflects the promotion

### Requirement: Mock Artifact Tools
The system SHALL implement the registered `artifact` tools as mocks that record call input and return DeepScientist-compatible minimal result shapes without performing real Git operations, branch operations, external fetches, manuscript validation, baseline mutation, or research-record validation.

#### Scenario: Artifact call is recorded
- **WHEN** a caller invokes a registered `artifact` tool through the compatibility dispatcher
- **THEN** the extension persists the tool name, input JSON, output JSON, mock marker, timestamp, and selected runtime context in compatibility storage

#### Scenario: Quest state has source-shaped envelope
- **WHEN** a caller invokes `artifact.get_quest_state` with `detail`
- **THEN** the result includes `ok: true`, normalized `detail`, and a `quest_state` object with source-compatible high-level keys such as `quest_id`, `title`, `active_anchor`, `baseline_gate`, `active_run_id`, `runtime_status`, `display_status`, and `pending_user_message_count`

#### Scenario: Quest documents have source-shaped envelope
- **WHEN** a caller invokes `artifact.read_quest_documents` with `names`, `mode`, and `max_lines`
- **THEN** the result includes `ok: true`, normalized `mode`, `count`, and `items`, where each item includes `name`, `path`, `exists`, and `content`

#### Scenario: Unsafe artifact tools do not mutate external state
- **WHEN** a caller invokes artifact tools whose DeepScientist implementation would change Git, create branches, fetch arXiv, refresh summaries, publish baselines, submit bundles, or complete a quest
- **THEN** the mock returns a DeepScientist-compatible result with `mocked: true` and does not perform the external mutation

### Requirement: Mock Bash Exec Tool
The system SHALL implement `bash_exec.bash_exec` as a durable session-state mock that preserves DeepScientist-compatible mode arguments and result fields without launching subprocesses.

#### Scenario: Detach creates mock session
- **WHEN** a caller invokes `bash_exec.bash_exec` with `mode: "detach"` and a command string
- **THEN** the result includes DeepScientist-compatible session fields such as `id`, `bash_id`, `log_path`, `status`, `kind`, `comment`, `label`, `command`, `workdir`, `cwd`, `started_at`, `finished_at`, `exit_code`, `stop_reason`, and output sequence fields, with `mocked: true`

#### Scenario: Await creates completed mock session
- **WHEN** a caller invokes `bash_exec.bash_exec` with `mode: "await"` or `mode: "create"`
- **THEN** the result creates or updates a compatibility session row and returns a DeepScientist-compatible result without executing the command

#### Scenario: Read returns log window shape
- **WHEN** a caller invokes `bash_exec.bash_exec` with `mode: "read"` for a stored session
- **THEN** the result includes DeepScientist-compatible session fields and bounded log window metadata even when the mock log is empty

#### Scenario: List and history return collection shapes
- **WHEN** a caller invokes `bash_exec.bash_exec` with `mode: "list"` or `mode: "history"`
- **THEN** the result includes source-compatible collection fields such as `ok`, `count`, `items`, status summaries, or history lines as applicable

#### Scenario: Kill marks mock session stopped
- **WHEN** a caller invokes `bash_exec.bash_exec` with `mode: "kill"` for a stored session
- **THEN** the extension updates the mock session status without sending an operating-system signal or killing a real process

### Requirement: Compatibility Fixture Validation
The system SHALL validate the mock command surface against DeepScientist source-code fixtures and observed output shapes before treating the extension as ready for migration use.

#### Scenario: Source signatures are covered
- **WHEN** unit tests inspect the compatibility registry
- **THEN** the registered tool names and accepted top-level argument keys match the DeepScientist source signatures captured for the initial mock

#### Scenario: Response keys are covered
- **WHEN** unit tests invoke representative memory, artifact, and bash_exec mock calls
- **THEN** the returned objects contain the DeepScientist-compatible fields required by the captured fixtures

#### Scenario: No real execution occurs in tests
- **WHEN** unit tests invoke mocked artifact and bash_exec calls
- **THEN** the tests can assert that no subprocess, Git mutation, network fetch, or DeepScientist storage layout was created
