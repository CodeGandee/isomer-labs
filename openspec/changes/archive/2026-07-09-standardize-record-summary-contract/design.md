## Context

Research records and Research Ideas currently expose different display fields. Generic structured records already use `title` and `summary` in several query-index paths, while canonical Research Ideas still use `title` and `one_liner`. Some import paths also copy the same source text into both display slots, which makes the GUI timeline show duplicate main and secondary text and forces parsers to guess which field means what.

The GUI is now growing around idea-led navigation. The idea graph and idea timeline both need a concise, uniform display contract that works for canonical idea records, idea-bearing source fragments, query-index facets, and Project Web read models. DeepSci agents also need explicit authoring rules so new records keep the same shape as the runtime contract.

This change is intentionally breaking. Old API payloads, CLI flags, and GUI contracts that expose `one_liner` as a first-class field will be replaced rather than preserved as permanent compatibility behavior. Legacy `one_liner` data and `structured-record.v1` payloads may be read only by migration, validation, or repair code.

## Goals / Non-Goals

**Goals:**

- Make `title` and `summary` the required top-level display fields for accepted structured Research Record payloads.
- Introduce `structured-record.v2` as the supported display contract and treat `structured-record.v1` usage as unsupported for new writes.
- Replace Research Idea `one_liner` with `summary` across runtime models, SQLite persistence, query-index facets, CLI/API payloads, Project Web contracts, and TypeScript GUI models.
- Require idea-bearing payload objects that can become canonical Research Ideas to provide their own `title` and `summary`.
- Update DeepSci system-skill and placeholder-binding guidance so agents create records that satisfy this display contract.
- Surface missing, duplicated, or inconsistent display fields as deterministic validation diagnostics and GUI-safe warnings instead of crashing views.
- Migrate `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` after code can read and write the new `summary` interpretation.

**Non-Goals:**

- Preserve old `one_liner` URLs, request payloads, generated TypeScript contracts, or `structured-record.v1` usage as stable public interfaces.
- Change the previously selected idea `display_key` strategy, except to keep display keys independent from `title` and `summary`.
- Guarantee consecutive numeric GUI indexes for visible idea rows.
- Rewrite research meaning, lineage decisions, or idea content beyond the minimum display-field migration and diagnostics needed for this change.

## Decisions

1. Use `summary` as the canonical brief display field.

`summary` SHALL mean the short human-readable description shown under a title. It applies to payload roots, canonical Research Ideas, idea-bearing payload objects, query-index rows, and GUI read models. The main alternative was `brief_description`, but the existing record index and schemas already use `summary`, so `summary` avoids adding a third near-synonym. Keeping `one_liner` would preserve drift between idea records and other records, so it is rejected.

2. Introduce `structured-record.v2` and make v1 unsupported for new writes.

New structured record writes SHALL use `structured-record.v2` or v2-backed DeepSci profiles for the display contract. Existing `structured-record.v1` data may be read only for validation, repair, and migration. The main alternative was breaking v1 in place, but that would silently change the meaning of historical schema refs. A hybrid long-term support model was rejected because the user wants a clean breaking design, not ongoing v1 compatibility.

3. Treat `one_liner` as migration input only.

Runtime dataclasses, SQLite row mappers, web contract models, generated TypeScript types, CLI output, and GUI code SHALL expose `summary` for idea display text. Migration and repair code MAY read legacy `one_liner` values to populate `summary`, but normal read models SHALL NOT convert `I<index>` or `one_liner` shapes on the fly. This keeps the GUI simple and makes data quality visible.

4. Enforce required display fields at write and validation boundaries.

Accepted structured payloads SHALL contain non-empty `title` and `summary`. Idea-bearing sections that feed canonical Research Ideas SHALL contain non-empty `title` and `summary` on each accepted idea object. Create/update paths should reject new invalid payloads; validate and repair paths should report existing invalid data with deterministic diagnostics. The alternative was best-effort fallback from arbitrary keys such as `idea`, `text`, or `hypothesis`, but that makes malformed data look healthy.

5. Keep source-fragment resolution profile-aware.

Idea import, realization, and exact source preview resolution SHALL use the shared profile-aware source-fragment registry to find idea-bearing sections. Once an object is selected, it must satisfy the same `title` and `summary` contract as canonical ideas. This avoids generic key guessing and prevents context notes, filter notes, or record summaries from becoming idea content.

6. Keep the query index derived and rebuildable.

The query index SHALL derive record titles, record summaries, idea facets, and Project Web graph/timeline read models from payload files and canonical runtime rows. It SHALL NOT parse generated Markdown or silently synthesize display fields during ordinary reads. Rebuild and validation commands own backfill, stale-row detection, and display-contract diagnostics.

7. Remove `one_liner` from all Project Web graph/read contracts.

Project Web graph nodes, timeline rows, hover previews, detail payloads, and record summaries SHALL use `summary` as the brief display text across material kinds. The alternative was removing `one_liner` only from canonical idea nodes, but that would preserve two subtitle conventions in the same graph contract.

8. Rewrite affected SQLite schemas cleanly.

The canonical runtime and query-index schemas SHALL use `summary` columns for ideas and idea facets. Legacy `one_liner` columns may appear only in backup copies or explicit migration/repair input. The main alternative was adding `summary` while leaving old columns ignored, but that keeps stale schema language in the hot path.

9. Keep recent errors ephemeral for this change.

Project Web SHALL use the existing process-local recent-error buffer for recent read warnings and errors. Durable validation remains the responsibility of explicit validation and repair commands. A durable recent-error store is useful but larger than this display-contract change.

10. Teach agents through skills and enforce the teaching through validation.

Production DeepSci placeholder bindings and directly linked skill guidance SHALL tell agents to author `title` and `summary` at payload roots and in idea-bearing entries. The research-paradigm validation harness SHALL report stale `one_liner` guidance and missing display-field guidance in active production DeepSci materials. This makes the contract durable for future research runs, not only the current codebase.

## Risks / Trade-offs

- Legacy clients fail after the break -> Document the contract change, update generated types and GUI code together, and keep legacy handling limited to migration/repair commands.
- Existing records lack `summary` -> Validation reports the missing field, and the flash-attention migration scans all records and fixes stored payload content with meaningful authored summaries after code-level support lands.
- `title` and `summary` may still duplicate after migration -> Validation flags duplicate display text so operators can repair weak records without blocking all browsing.
- SQLite schema rewrites can damage old databases if interrupted -> Take a backup before migration, rebuild affected tables transactionally, and validate canonical `summary` values afterward.
- Damaged lineage or deleted records may make idea data non-interpretable -> Read models return partial payloads with diagnostics, and recent-error APIs expose recent warnings/errors instead of crashing the GUI.

## Migration Plan

1. Update code first: add `structured-record.v2`, update active DeepSci profile refs, and make new writes reject unsupported v1 usage.
2. Update runtime models, clean SQLite migrations, record store/import logic, query-index extraction, web contracts, generated TypeScript models, GUI graph/timeline rendering, CLI flags, and tests so all normal read/write paths understand canonical `summary`.
3. Keep temporary migration/repair logic that can read legacy `one_liner` and v1 payloads from existing SQLite rows or managed payload files and write canonical v2/`summary` data.
4. Update DeepSci placeholder bindings, skill guidance, and the validation harness so new agent-authored records include `title` and `summary` before this topic is migrated.
5. Take a backup or snapshot of `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model`.
6. Migrate topic data directly: scan all records, rewrite managed payload JSON files with meaningful stored summaries, update `state.sqlite` idea rows and query-index idea facets to use clean `summary` columns, preserve display keys, rebuild derived query-index rows, and remove ordinary GUI/runtime dependence on `one_liner`.
7. Run validation against the migrated topic workspace, including idea validation, query-index validation, source-fragment validation, recent-error inspection, and GUI smoke checks for graph, timeline, hover, and detail views.
8. Rollback for this breaking change is restore-from-backup plus previous code. Forward compatibility for old `one_liner` clients or v1 writes is not a goal.

## Open Questions

Resolved by Imsight exploration:

- Use new `structured-record.v2`; v1 usage is unsupported for new writes.
- Scan and fix all flash-attention records with meaningful stored summaries instead of heuristic GUI fallback.
- Rewrite affected SQLite tables cleanly to use `summary`.
- Remove `one_liner` from all Project Web graph/read contracts.
- Keep recent-error query capability ephemeral for this change.
