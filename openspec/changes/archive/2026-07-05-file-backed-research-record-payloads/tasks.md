## 1. Payload-file Runtime Model

- [x] 1.1 Add runtime record fields and schema migration support for structured payload locator, digest, media type, manifest locator, revision refs, current/latest refs, and legacy generated-view refs.
- [x] 1.2 Implement a managed payload-file layout for structured research records under the Topic Workspace, with deterministic paths and safe collision handling.
- [x] 1.3 Update structured record create/update to validate the input JSON, snapshot it into managed `payload.json`, and store only locator/digest/metadata as authoritative runtime state.
- [x] 1.4 Update record show/detail APIs to read payload content from the managed JSON file and verify the recorded digest before returning payload data.
- [x] 1.5 Update runtime validation to report missing payload files, invalid JSON files, digest mismatches, stale manifests, and broken revision refs.

## 2. Rendering and Export Semantics

- [x] 2.1 Replace default durable Markdown materialization in structured record create/update with on-demand render behavior.
- [x] 2.2 Add or update CLI/API commands for `show` or `render` so callers can render Markdown from a payload-backed record without writing a file.
- [x] 2.3 Add explicit Markdown export behavior that writes a generated artifact snapshot with source record id, payload digest, template ref, output digest, and provenance refs.
- [x] 2.4 Update artifact-format rendering internals so Jinja2 templates receive payload content from managed JSON files and remain view transforms only.
- [x] 2.5 Update DeepSci generic and topic-reset templates only as needed for readable on-demand display, not durable state files.

## 3. Query Index, Reset, and Migration

- [x] 3.1 Update query-index extraction and rebuild to read managed payload files, verify digests, and derive summaries, relationships, facets, scalar facts, and file refs from file content.
- [x] 3.2 Update query list/export/detail outputs to include payload locators, payload digests, current/latest pointers, and explicit generated-export locators when present.
- [x] 3.3 Update index cleanup so it removes derived rows and generated-export refs without deleting managed payload files unless explicit record deletion policy applies.
- [x] 3.4 Update topic-reset checkpoint, plan, and outcome persistence to write managed JSON payload files and render Markdown only on demand or explicit export.
- [x] 3.5 Add migration or runtime upgrade behavior that exports existing SQLite `payload_json` rows to managed JSON files, marks old Markdown views as legacy generated artifacts, and rebuilds indexes.

## 4. Skills, Bindings, and Validation

- [x] 4.1 Update packaged production DeepSci skill guidance to say accepted structured outputs are JSON payload-file records managed by `isomer-cli`.
- [x] 4.2 Update production DeepSci placeholder bindings to remove normal durable `--render markdown` expectations and point human review to on-demand render/show/export commands.
- [x] 4.3 Update operator topic-reset guidance to describe reset payload JSON files and explicit Markdown export boundaries.
- [x] 4.4 Extend the research-paradigm validation harness to reject generated Markdown as canonical state, Markdown growth instructions, and SQLite payload blobs as the only durable structured payload copy.

## 5. Tests and Verification

- [x] 5.1 Add unit tests for create/update writing managed payload files, storing locators/digests, preserving record identity, and reading payloads from files.
- [x] 5.2 Add unit tests for digest validation, missing-file diagnostics, and migration from existing SQLite payload rows.
- [x] 5.3 Add unit tests for on-demand Markdown rendering and explicit Markdown export provenance.
- [x] 5.4 Add unit tests for query-index rebuild from payload files and cleanup preserving payload files.
- [x] 5.5 Add skill validation tests for the payload-file record contract and no-default-durable-Markdown guidance.
- [x] 5.6 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
