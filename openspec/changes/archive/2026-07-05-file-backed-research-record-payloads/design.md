## Context

Current structured research records write validated JSON into `structured_research_payloads.payload_json` and often materialize generated Markdown under `records/artifacts/research-records/...`. In the observed topic workspace, the durable record tree contains many Markdown files and no visible payload JSON files, so canonical research content is hard to audit, move, diff, or recover without SQLite.

The previous design tried to make generated Markdown readable and link it to SQLite payload rows. That still makes a rendered snapshot look like durable state, and it encourages either appending to generated Markdown or overwriting fixed Markdown names across rounds. Both patterns fight Jinja2: a template can render a full view from current data, but it is not a good append-only or living-state editor.

## Goals / Non-Goals

**Goals:**

- Make accepted structured research payloads durable as managed JSON files in the Topic Workspace.
- Make SQLite the catalog, relationship graph, validation ledger, and rebuildable query index for those files.
- Render Markdown from JSON through Jinja2 on demand for CLI/API/GUI display or explicit export.
- Model research growth through new payload files, revision links, snapshot refs, and derived query views rather than growing Markdown files.
- Migrate existing SQLite-stored payloads into managed JSON files and classify existing generated Markdown as legacy generated views or cleanup candidates.
- Update DeepSci skills so agents author JSON payloads and do not request durable generated Markdown as normal accepted output.

**Non-Goals:**

- Do not build the GUI in this change.
- Do not make SQLite store canonical payload content as the primary source of truth.
- Do not preserve `--render markdown` as default durable-file creation for structured records.
- Do not force one fixed file per placeholder when the research process naturally produces many event records.
- Do not require agents to hand-author Markdown views, SQL rows, or query-index tables.

## Decisions

### JSON payload files are the durable record content

Each accepted structured record SHALL snapshot its validated payload into a managed record directory such as `records/research-records/<record-kind>/<record-id>/payload.json`. The runtime MAY write a small manifest beside it for file-level metadata, but the JSON payload file is the durable content that a human can inspect, copy, diff, and recover.

Alternative considered: keep JSON canonical only in SQLite. That makes SQLite a content store rather than a catalog and hides the most important research artifact from the workspace filesystem.

### SQLite is the map and index, not the content owner

Workspace Runtime SQLite SHALL store lifecycle identity, payload file paths, digests, schema/profile refs, producer/consumer metadata, revision links, current/latest pointers, relationship edges, file attachments, validation diagnostics, and derived query rows. It SHALL NOT be the only durable copy of accepted structured payload JSON.

Alternative considered: store payloads both in SQLite and files as equal copies. That creates reconciliation ambiguity. SQLite may cache derived scalar facts, but file digests decide whether the index is current.

### Markdown is rendered on demand or exported explicitly

Jinja2 templates SHALL render Markdown from payload JSON when a caller asks to show, preview, or export a record. Default record creation SHALL NOT write generated Markdown files. If a caller explicitly exports Markdown, that file is a generated artifact snapshot with provenance and digest metadata; it is not a living record view and is not parsed as source.

Alternative considered: keep generated Markdown with front matter as the durable review file. That still asks generated output to behave like state and makes fixed-name updates tempting.

### Research rounds create record files or revision snapshots

Historical work such as experiment results, route decisions, evidence items, and attempt records SHALL create new payload-backed records. Current-state concepts such as candidate boards, frontiers, latest context, or resume packets SHALL use snapshots, revision links, or query-derived views rather than mutating a generated Markdown file.

Alternative considered: one fixed JSON file per semantic placeholder that grows forever. That improves over Markdown but still creates large merge-prone documents and makes history implicit.

### Query and GUI views are assembled from indexed payload files

The query index SHALL rebuild from payload files and their manifest/runtime metadata. GUI views can ask the CLI/API for indexed summaries, related records, latest snapshots, and on-demand rendered Markdown, but they do not need Markdown files to exist on disk.

Alternative considered: make the GUI read raw payload files directly. That bypasses Workspace Runtime validation, relationship indexing, and topic-scoped policy checks.

### Migration exports existing payload rows before changing authority

Migration SHALL walk existing structured payload rows, write each `payload_json` into the managed payload-file layout, store payload locators and digests, and rebuild indexes from files. Existing generated Markdown remains available as legacy generated-view artifacts only when useful; it is no longer the canonical review or query surface.

Alternative considered: drop generated Markdown immediately and trust SQLite rows until new records are written. That risks losing human-auditable continuity for current topic workspaces.

## Target Flow

```text
Agent drafts payload JSON
        |
        v
isomer-cli validates schema/profile
        |
        v
managed payload file is written
        |
        v
SQLite records locator, digest, refs, links
        |
        v
query index derives summaries and relationships
        |
        v
CLI/API/GUI renders Markdown through Jinja2 on demand
```

## Risks / Trade-offs

- Existing commands and skills assume `--render markdown` writes files -> Change command semantics carefully, add explicit export options, and update skill validation so agents stop relying on durable Markdown.
- File and SQLite writes can drift -> Store digests, validate file existence and digest match, and make rebuild repair derived index rows from files.
- JSON file count will grow during research -> Use record-kind directories, stable record ids, query views, and cleanup/archive commands rather than pretending one Markdown file should absorb all history.
- Existing topic workspaces have SQLite-only payloads -> Provide migration that exports payload files and marks legacy generated Markdown as non-canonical.
- Some users may want shareable Markdown reports -> Support explicit Markdown export as a generated artifact with provenance, not as default record state.

## Migration Plan

1. Add managed payload-file layout and runtime fields for payload locator, payload digest, manifest locator, revision refs, and current/latest pointers.
2. Change structured record create/update so validated payloads are written to JSON files and SQLite stores only locators, metadata, validation results, and derived indexes.
3. Replace default durable Markdown materialization with on-demand render/show/export commands backed by Jinja2 templates.
4. Update query-index extraction, validation, cleanup, and rebuild to read payload files, validate digests, and refresh derived rows.
5. Update topic-reset checkpoint, plan, and outcome persistence to use file-backed payloads and on-demand Markdown rendering.
6. Update DeepSci skills, placeholder bindings, and validation harness rules to describe JSON payload records and explicit Markdown export only.
7. Add a migration command or runtime upgrade path that exports existing SQLite payloads into managed JSON files, marks legacy Markdown as generated artifacts, and rebuilds indexes.

Rollback should keep exported JSON payload files intact. If the new runtime schema must be disabled, the migration can rehydrate SQLite payload rows from the managed JSON files, but new generated Markdown defaults should remain disabled unless explicitly restored.

## Open Questions

- Should the managed payload directory use one folder per `record_id`, or one folder per semantic placeholder with revision children?
- Should current/latest pointers live only in SQLite, or should each semantic stream also get a small `latest.json` pointer file for easier filesystem browsing?
- Should explicit Markdown export write under `records/exports/`, `records/generated/`, or the existing artifact records directory with a generated-file role?
