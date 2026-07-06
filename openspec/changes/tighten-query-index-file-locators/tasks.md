## 1. Query-index Extraction

- [x] 1.1 Tighten payload-derived file extraction so bare payload paths and semantic path inventory entries do not create `research_record_files` rows.
- [x] 1.2 Preserve explicit file hints, structured payload locators, rendered Markdown locators, generated exports, and accepted attachment metadata as file-index rows.

## 2. Query Read Model

- [x] 2.1 Add conservative derived openability metadata to file rows returned by query export and record file APIs.
- [x] 2.2 Add deterministic diagnostic summary data to query export responses while preserving full diagnostics.

## 3. Web GUI

- [x] 3.1 Render grouped export diagnostics from API data without topic-specific or path-specific logic.
- [x] 3.2 Render file rows so missing or unresolved files do not produce open/preview affordances.

## 4. Verification

- [x] 4.1 Add unit coverage for payload path extraction, semantic inventory exclusion, file openability metadata, and diagnostic summaries.
- [x] 4.2 Run focused tests and OpenSpec validation for the change.
