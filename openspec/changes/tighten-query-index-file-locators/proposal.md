## Why

The query index currently treats too many payload `path` fields as concrete files, so semantic inventories and unresolved artifact names become noisy `query_index_file_missing` diagnostics. The Project Web GUI should browse any selected Isomer Project dynamically and should not try to open or validate files that the backend cannot resolve as concrete attachments.

## What Changes

- Tighten query-index file extraction so `research_record_files` only contains concrete, resolvable file attachments or accepted historical locators.
- Keep unresolved artifact names, semantic path inventory entries, and display-only payload paths as facts/facets or record detail data instead of missing file rows.
- Add backend openability metadata for indexed files so the GUI can decide whether to show preview/open affordances dynamically.
- Group query-index diagnostics for GUI export views while preserving full diagnostic detail for inspection and maintenance actions.
- Preserve explicit rebuild, validate, and cleanup behavior; no read operation should repair or backfill index rows.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `research-record-query-index`: Clarify concrete file locator extraction, unresolved payload refs, file openability metadata, and diagnostic presentation expectations for GUI consumers.

## Impact

- Affected code: `src/isomer_labs/records/index_extractors.py`, `src/isomer_labs/records/index.py`, `src/isomer_labs/web/read_model.py`, `src/isomer_labs/web/static/assets/app.js`, and focused unit tests.
- Affected data: derived query-index rows in `research_record_files`; canonical lifecycle records and structured payload files remain unchanged.
- Affected APIs: query/export and files read models gain derived metadata useful for generic GUI rendering.
