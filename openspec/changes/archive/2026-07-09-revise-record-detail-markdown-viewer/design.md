## Context

The Records table opens a `recordDetail` tab. Today that tab loads a viewer descriptor, canonical detail, optional Markdown render, lineage, siblings, files, and facets, then shows the primary content plus several JSON columns. Idea detail and topic overview tabs have a clearer pattern: render readable Markdown in the main surface, provide `View JSON`, `Copy Markdown`, and `Refresh`, and keep raw JSON in a modal.

Record details should follow that same pattern. Records still need richer provenance than ideas: users need the artifact path relative to the Topic Workspace, the absolute filepath for clipboard use, and the direct parent idea when the record expresses one.

## Goals / Non-Goals

**Goals:**

- Make record detail tabs Markdown-first for structured records.
- Move raw record JSON and supporting query payloads into a tabbed `View JSON` dialog.
- Show the record path relative to the Topic Workspace under the title when available.
- Show the direct parent idea under the title when available.
- Add `Copy Filepath` for the full absolute artifact path and keep `Copy Markdown` for rendered Markdown.
- Preserve read-only GUI behavior and existing lazy-loading boundaries.

**Non-Goals:**

- Change canonical Workspace Runtime storage or research-record schemas.
- Require generated Markdown files to exist before the GUI can show a record.
- Replace PDF, image, table, or file artifact viewers.
- Infer parent ideas from prose. Parent idea display should use structured lineage, facet, or payload metadata only.

## Decisions

1. Reuse the existing record detail query set and reorganize presentation. The frontend already has descriptor, detail, render, lineage, siblings, files, and facets queries. The implementation should use those sources to build the Markdown preview and JSON modal rather than adding another aggregate endpoint first. Alternative considered: create one backend endpoint that returns all record detail UI data. That would simplify the component but weaken lazy loading and duplicate existing read APIs.

2. Prefer rendered Markdown from the backend render endpoint. If Markdown rendering is unavailable, the GUI may show a safe empty state or a compact generated preview from title and summary metadata, but it must not parse generated Markdown files from disk. Alternative considered: read durable Markdown files directly. That conflicts with the current record contract that Markdown rendering is a view/export, not canonical state.

3. Treat path metadata as read-model fields. The descriptor or detail payload should expose `topic_workspace_relative_path` and `absolute_filepath` when the backend can derive them from managed payload, rendered Markdown, or primary file metadata. `Copy Filepath` is disabled when no absolute path is available. Alternative considered: compute absolute paths in the browser from relative paths. The browser does not own Project root or path policy.

4. Treat direct parent idea as optional structured metadata. The backend should expose compact fields such as `direct_parent_idea_id`, `direct_parent_idea_display_key`, and `direct_parent_idea_title` when they can be derived from record lineage, idea realization, parents JSON, facets, or structured payload refs. The GUI shows nothing or a muted unknown state when this is absent.

5. Keep raw JSON accessible but secondary. `View JSON` should include tabs for canonical/detail JSON, rendered response, lineage, siblings, files, facets, descriptor, and diagnostics. The primary record detail window should not show the current always-visible JSON columns.

## Risks / Trade-offs

- [Risk] Some record kinds may not render Markdown. → Mitigation: keep a clear empty or unsupported state, keep `View JSON` available, and do not crash.
- [Risk] A record may have multiple idea relationships. → Mitigation: show only the direct parent idea when structured metadata identifies one; put the full relationship payload in `View JSON`.
- [Risk] Absolute filepaths may expose local machine paths in the browser. → Mitigation: this is a local single-user GUI; expose only for the selected Project backend and preserve existing openability/path-safety checks where they apply.
- [Risk] Reorganizing the detail panel could accidentally fetch heavy data earlier. → Mitigation: keep existing query enablement and only load supporting payloads while the record tab is mounted.

## Migration Plan

No data migration is required. Implement read-model field additions, update GUI contracts, update the record detail component, rebuild static assets, and run focused backend/frontend tests. Rollback restores the previous multi-column record detail layout and omits the new path/parent metadata fields.

## Open Questions

None.
