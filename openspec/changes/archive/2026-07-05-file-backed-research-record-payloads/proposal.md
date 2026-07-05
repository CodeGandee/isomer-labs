## Why

Generated Markdown is a poor durable record surface because Jinja2 rendering creates snapshots, and growing those snapshots across research rounds requires repeatedly regenerating prior content plus new content. The durable research record should be the JSON payload file; SQLite should catalog files, relationships, and derived indexes rather than hide canonical content inside the database or durable generated Markdown.

## What Changes

- **BREAKING**: Structured research payload JSON becomes file-backed durable content under managed Topic Workspace record directories; SQLite stores file locators, digests, metadata, relationships, and derived indexes rather than treating `payload_json` as the canonical payload store.
- **BREAKING**: Generated Markdown is no longer written as the default durable review file for structured records; Jinja2 templates render Markdown on demand for CLI/API/GUI display or explicit export.
- Add a managed payload-file layout for accepted structured records, with stable `payload.json` and record metadata/manifest files per immutable record revision or snapshot.
- Replace normal `--render markdown` write behavior with on-demand render/show/export semantics; explicit Markdown exports are artifact snapshots, not living record state.
- Define research-round growth through new JSON record files, revision/snapshot links, and query-index relationships instead of appending to or overwriting generated Markdown files.
- Update query/index rebuild to validate JSON payload files by digest, extract facets and relationships from those files, and return file locators that the GUI can render on demand.
- Update DeepSci skills and placeholder bindings so agents author JSON payload files, write them through `isomer-cli`, and do not request durable Markdown views as normal accepted output.
- Add migration behavior for existing SQLite-stored payloads and generated Markdown views: export payload JSON into managed files, preserve legacy Markdown as non-canonical generated artifacts or cleanup candidates, and rebuild indexes from JSON files.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `research-recording-contracts`: Structured research records become durable JSON payload files; Markdown is a rendered view or explicit export, not source state.
- `workspace-runtime-persistence`: Workspace Runtime persists payload file locators, digests, revision refs, and index metadata in SQLite, with file-backed payloads as the canonical content.
- `research-record-query-index`: Query/index behavior rebuilds from payload files and stores derived relationships, facts, file refs, and current/latest pointers without owning payload content.
- `artifact-format-processing`: Jinja2 Markdown rendering becomes on-demand display/export behavior for JSON payload files rather than default durable Markdown materialization.
- `research-placeholder-bindings`: Active DeepSci placeholder bindings must instruct agents to create/update JSON payload records and avoid normal durable Markdown generation.
- `research-paradigm-skills`: Production DeepSci skills must teach payload-file authoring, record creation, revision/snapshot discipline, and on-demand rendering boundaries.
- `topic-workspace-reset-checkpoints`: Topic reset checkpoint, plan, and outcome records become file-backed JSON payloads; reset Markdown views are on-demand or explicit exports.

## Impact

Affected areas include `src/isomer_labs/records/store.py`, `src/isomer_labs/runtime/sqlite.py`, runtime record models, research record CLI commands, query-index extraction and maintenance, artifact-format render commands, DeepSci record-format templates, topic-reset persistence/rendering helpers, migration utilities for existing topic workspaces, packaged system skills under `src/isomer_labs/assets/system_skills/`, the symlinked `skillset/` authoring view, and CLI/skillset tests.
