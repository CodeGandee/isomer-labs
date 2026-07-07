## 1. Dependencies and Types

- [x] 1.1 Add the frontend Markdown generation dependencies to `web/ui/package.json` and lockfile: `mdast-util-to-markdown`, `mdast-util-gfm`, `mdast-util-frontmatter`, and `unist-builder`.
- [x] 1.2 Add TypeScript schemas and types for idea detail payloads, source JSON metadata, realization summaries, and idea openable descriptors in `web/ui/src/types.ts`.
- [x] 1.3 Add API client helpers for `GET /api/topics/{topic_id}/ideas/{idea_id}` and explicit full-source fetches, ensuring Zod validation covers diagnostics, missing-source cases, and `source_json_truncated`.

## 2. Backend Idea Detail Read Model

- [x] 2.1 Add `ProjectWebReadModel.idea_detail(topic_id, idea_id)` and a helper that opens Workspace Runtime read-only and fetches canonical Research Idea rows by topic.
- [x] 2.2 Resolve realization history, latest realization, generation-group context, incoming/outgoing idea lineage edges, and source record refs for the selected idea.
- [x] 2.3 Resolve exact source JSON content or source JSON fragment using the selected-source order: latest Idea Realization `source_json_path`, latest realization record payload, then Research Idea source metadata.
- [x] 2.4 Return non-fatal diagnostics for missing idea id, cross-topic refs, missing source record, missing payload file, invalid JSON, oversized payload, unresolved JSON path, or `source_json_truncated` without rebuilding or repairing runtime state.
- [x] 2.5 Add `GET /api/topics/{topic_id}/ideas/{idea_id}` to `src/isomer_labs/web/app.py` and keep response headers/cache behavior consistent with existing web API routes.

## 3. Openable Item and Graph Routing

- [x] 3.1 Extend the semantic openable resolver to parse `idea:<topic_id>:<idea_id>` and return an `ideaDetail` descriptor with stable tab id, title, topic id, idea id, and detail URL.
- [x] 3.2 Add unknown or cross-topic idea descriptor diagnostics that do not fall back to a record descriptor.
- [x] 3.3 Add `ideaId` to Dockview panel params and panel option conversion without breaking existing record, graph, file, and diagnostics panels.
- [x] 3.4 Update idea-lineage graph node click handling so canonical idea nodes open `idea:` items while non-idea nodes keep the existing record/artifact behavior.
- [x] 3.5 Update workbench command/event plumbing if needed so idea tabs participate in URL-backed open-item history and browser Back behavior.

## 4. JSON-to-MDAST Markdown Generation

- [x] 4.1 Add a local frontend module, such as `web/ui/src/markdown-doc.ts`, that builds MDAST nodes from nested JSON values.
- [x] 4.2 Implement object-key-to-heading rendering with bounded heading depth, readable key labels, scalar paragraphs, list items, and fenced JSON fallbacks.
- [x] 4.3 Implement safe array and metadata handling: scalar arrays become lists, compatible arrays of same scalar-keyed objects become GFM tables, complex arrays become nested sections or fenced JSON, and system metadata moves to a secondary `Metadata` section.
- [x] 4.4 Serialize MDAST through `mdast-util-to-markdown` with GFM table support and no hand-concatenated Markdown syntax in feature code.
- [x] 4.5 Return both generated Markdown and exact normalized JSON strings from the preview helper so copy actions use the same source as the preview and modal.

## 5. Idea Detail UI

- [x] 5.1 Add an `IdeaDetailPanel` Dockview component that fetches idea detail only while the tab is mounted and renders title, status, lineage summary, realization history as side metadata, diagnostics, and a Markdown preview from the selected latest realization.
- [x] 5.2 Reuse the existing `MarkdownView` for generated Markdown preview so GFM, math, Mermaid, and preview styling remain consistent.
- [x] 5.3 Add toolbar actions for View JSON, Copy JSON, Copy Markdown, refresh, and latest realization record opening, using icons/buttons consistent with the existing workbench style.
- [x] 5.4 Add disabled and diagnostic states when exact source JSON or generated Markdown is unavailable.
- [x] 5.5 Preserve selected idea id and show a source digest changed notice when the active idea detail query refreshes with different source metadata.

## 6. JSON Modal and Clipboard Behavior

- [x] 6.1 Add an in-app JSON modal overlay that darkens the workbench, shows formatted exact JSON in a scrollable code area, and avoids `window.open`.
- [x] 6.2 Add close behavior through explicit close button, Escape key, and supported backdrop interaction with focus returning to the triggering control.
- [x] 6.3 Add copy JSON from both the idea detail tab and JSON modal with visible success/failure state.
- [x] 6.4 Add copy Markdown from the idea detail tab with visible success/failure state.
- [x] 6.5 Ensure clipboard failure keeps content visible and selectable for manual copy.

## 7. Tests

- [x] 7.1 Add Python unit tests for the idea detail read model, source JSON resolution, missing-source diagnostics, and read-only behavior.
- [x] 7.2 Add Python or web read-model tests for `idea:` openable descriptors and unknown/cross-topic idea errors.
- [x] 7.3 Add frontend unit tests for JSON-to-MDAST rendering, nested headings, table/list fallback behavior, and no raw JSON default preview.
- [x] 7.4 Add frontend component tests for idea detail loading, JSON modal open/close, copy action success/failure, and disabled unavailable states.
- [x] 7.5 Add graph routing tests showing canonical idea nodes open idea detail while non-idea nodes continue opening records.
- [x] 7.6 Add a Playwright smoke check for the flash-attention idea-lineage path: click a primary idea node, see Markdown preview, open JSON modal, copy JSON, and copy Markdown.

## 8. Validation

- [x] 8.1 Run frontend test/build commands for `web/ui` after dependency and UI changes.
- [x] 8.2 Run `pixi run lint`.
- [x] 8.3 Run `pixi run typecheck`.
- [x] 8.4 Run `pixi run test`.
- [x] 8.5 Restart the local GUI service and manually smoke-check `http://127.0.0.1:8765/?topic=flash-attention-4-whitebox-runtime-model&graph=idea-lineage`.
