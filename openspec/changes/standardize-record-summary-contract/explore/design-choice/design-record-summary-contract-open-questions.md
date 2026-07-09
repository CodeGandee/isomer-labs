# Record Summary Contract Open Questions

## Context

This note records the decisions made during Imsight exploration for the OpenSpec change `standardize-record-summary-contract`. The change replaces `one_liner` with `summary`, makes display fields coherent across records and ideas, and migrates `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` after code support lands.

## Decisions

1. Use a new `structured-record.v2` display contract. Usage of `structured-record.v1` is unsupported for new structured records. v1 may be read only as legacy input for validation, repair, or migration.
2. Use exact migration for flash-attention data. The migration must scan all records and fix stored payload content so records and idea entries have meaningful authored `summary` values, rather than deriving GUI summaries on the fly.
3. Rewrite affected SQLite schemas cleanly. Canonical runtime and query-index tables use `summary`; `one_liner` survives only in migration input, backups, or explicit legacy repair code.
4. Remove `one_liner` from all Project Web graph/read contracts, not only canonical idea nodes. Graph nodes use `summary` as the brief display text across material kinds.
5. Keep recent-error query capability ephemeral for this change. Project Web uses the existing process-local recent-error buffer for read warnings and errors; durable validation remains owned by explicit validation and repair commands.

## Rejected Options

- Breaking `structured-record.v1` in place was rejected because it changes the meaning of historical schema refs.
- Heuristic summary fill was rejected because the migrated topic should contain meaningful stored summaries, not mechanically invented display text.
- Leaving old SQLite `one_liner` columns ignored was rejected because the user wants a clean breaking design.
- Removing `one_liner` only from idea nodes was rejected because it would preserve two graph subtitle conventions.
- Durable recent-error persistence was rejected as larger than this display-contract change.

## Implementation Consequences

- Add v2 schema/profile assets and update active DeepSci profile refs for new writes.
- Treat v1 profile usage as unsupported in normal create/update paths and route old data through validation, repair, or migration only.
- Migrate flash-attention payload JSON and `state.sqlite` directly after code support lands.
- Update graph, timeline, hover, detail, records, docs, tests, and TypeScript contracts to use `summary`.
- Keep recent-error API backed by the existing process-local ring buffer.
