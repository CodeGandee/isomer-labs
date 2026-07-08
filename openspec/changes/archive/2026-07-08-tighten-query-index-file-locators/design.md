## Context

The query index is a derived SQL read model over Workspace Runtime research records. It currently walks structured payload JSON and treats any object with `path`, `file_path`, `artifact_path`, `output_path`, or `locator` as an indexed file attachment. That generic rule turns semantic path inventories and unresolved artifact names into `research_record_files` rows, so validation emits many `query_index_file_missing` diagnostics even when no concrete file attachment was intended.

The Project Web GUI consumes query export and file APIs for any selected Isomer Project root. It must not assume this repository's current `isomer-content/` topic layout, and it must not try to open a file just because a payload contains a string named `path`.

## Goals / Non-Goals

**Goals:**
- Keep `research_record_files` focused on concrete attachments with enough locator evidence to resolve or intentionally report a missing file.
- Preserve semantic path inventories, artifact manifests, and unresolved payload references as inspectable record data or facts without turning them into file-health warnings.
- Expose derived file openability metadata so GUI consumers can render preview/open actions dynamically.
- Reduce GUI diagnostic noise by grouping diagnostics while keeping full details available.

**Non-Goals:**
- Do not migrate or rewrite canonical payload JSON in existing Topic Workspaces.
- Do not add a new database table for unresolved references in this change.
- Do not auto-rebuild, cleanup, or repair the query index during read-only GUI requests.
- Do not bind the GUI to paths from `flash-attention-4-whitebox-runtime-model` or any other specific topic.

## Decisions

1. Restrict generic payload file extraction to high-confidence file objects.
   - A payload object only becomes a `research_record_files` row when it has explicit file semantics, such as a concrete file role, semantic label, operation-set id, locator kind, digest, media type, or an absolute/project-local path that resolves under accepted surfaces.
   - Alternative considered: keep indexing every path and downgrade diagnostics in the GUI. That hides noisy data in one client while leaving the query index misleading for CLI and future GUI consumers.

2. Keep unresolved references in existing generic fact/facet outputs.
   - Bare names such as `validation_metrics.json` remain visible in payload detail and generic facts, but they do not become missing file attachments unless paired with a resolvable base.
   - Alternative considered: add a new unresolved-reference table immediately. That is useful later, but the current generic fact table and payload detail are enough to fix false missing-file diagnostics without a schema migration.

3. Treat semantic path inventory entries as evidence, not attachments.
   - Checkpoint records may report paths that existed, did not exist, or represented expected surfaces at a moment in time. Those values should not become current file-index health failures.
   - Alternative considered: preserve inventory entries as missing files. That conflates historical readiness evidence with current attachment integrity.

4. Add openability metadata at query time rather than storing GUI state.
   - The backend can derive `resolved_path`, `exists`, `openable`, and `open_blocked_reason` from the indexed locator and current Topic Workspace context.
   - Alternative considered: let the frontend resolve paths. That would leak filesystem assumptions into TypeScript and make remote/local serving behavior harder to secure.

5. Summarize diagnostics for export views.
   - Export payloads can include a deterministic `diagnostic_summary` grouped by code and severity while retaining the full `diagnostics` list.
   - Alternative considered: suppress warnings in export payloads. That would reduce noise but hide maintenance signals from users.

## Risks / Trade-offs

- Some previously indexed loose payload paths will disappear from `research_record_files` after rebuild. Mitigation: payload detail and generic facts still expose the strings, and producers can add explicit file metadata when they want attachments.
- Historical index rows can remain noisy until rebuild or cleanup. Mitigation: validate and cleanup stay explicit; the implementation should not mutate read paths.
- The first openability metadata is conservative. Mitigation: only mark files openable when local resolution and existence are clear.
