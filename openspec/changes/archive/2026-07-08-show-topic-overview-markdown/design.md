## Context

The current topic overview panel fetches `/api/topics/{topic_id}` and `/api/topics/{topic_id}/runtime`, then renders both payloads as raw JSON blocks. The user-facing topic brief already exists as the semantic surface `topic.intent.overview`, whose default path is `<topic-workspace>/intent/src/topic-overview.md`.

The existing idea detail panel gives a useful interaction pattern: main content is readable Markdown, while exact JSON is available through a tabbed `View JSON` modal with copy support. This change applies that same pattern to topic overview.

## Goals / Non-Goals

**Goals:**
- Make `topic-overview.md` the main content of the topic overview tab.
- Resolve the Markdown file through `topic.intent.overview` on the backend.
- Keep Topic and Runtime JSON available through `View JSON`.
- Show a non-fatal warning when the overview file is missing.
- Keep all overview reads side-effect free.

**Non-Goals:**
- Do not create, repair, or migrate missing `topic-overview.md`.
- Do not add a general filesystem browser or direct project-root file endpoint.
- Do not change the topic creation skill or the topic overview Markdown template.
- Do not remove the existing runtime and topic summary panels.

## Decisions

Use a dedicated topic overview API endpoint. The endpoint should live near the existing topic read APIs and return Markdown content, overview source metadata, Topic JSON, Workspace Runtime JSON, and merged diagnostics in one response. This avoids making the frontend orchestrate several requests and avoids hard-coding the default filesystem layout in TypeScript.

Resolve the Markdown source through `resolve_semantic_binding(context, "topic.intent.overview", env=...)`. This keeps the feature aligned with Topic Workspace Manifest semantics and supports custom bindings or future layout changes without frontend changes.

Return missing overview as a successful topic response with a warning payload rather than an HTTP error. A missing topic overview is a content readiness issue, not a GUI failure: the endpoint should use HTTP 200, keep `ok: true` when the Topic context resolves, set `overview.exists: false`, omit Markdown content, and include a stable warning diagnostic. The panel should still be able to show topic/runtime JSON through `View JSON` and diagnostics to help the user fix the workspace.

Read the Markdown defensively. The backend should catch decoding, permission, and file read errors and return a warning diagnostic without crashing the endpoint. If a small size guard fits the local read-model pattern, cap the overview read and report a diagnostic when the file is too large; otherwise the implementation should at least keep read failures non-fatal.

Reuse `MarkdownView` for the page body and reuse `JsonModal` for supporting JSON. The topic overview modal should expose `Topic`, `Runtime`, and `Diagnostics` or `Source` tabs depending on what data is available. `JsonModal` should accept an optional accessible description so the same component works for idea data and topic overview data.

Disable `Copy Markdown` when Markdown is unavailable. The missing-overview warning should remain visible, and the copy action should either be disabled or report that no Markdown is available instead of copying warning text.

Keep openable descriptors lightweight. The descriptor for `topic:<topic_id>:overview` should continue to select the `topicOverview` tab component and should advertise the overview API URL, but it should not embed Markdown file contents.

## Risks / Trade-offs

- Reading Markdown from disk can fail due to encoding or permission issues. Mitigation: catch read errors and return diagnostics with no Markdown content.
- Combining topic/runtime data in the overview endpoint duplicates existing API calls. Mitigation: the backend can call existing read-model helpers and merge their diagnostics; this keeps frontend behavior simpler.
- The overview panel may need copy state similar to idea detail. Mitigation: keep copy handling local to the panel and reuse the existing button/modal components.
- Existing tests may assume topic overview renders raw JSON. Mitigation: update tests to assert Markdown-first rendering and JSON modal behavior.

## Migration Plan

1. Add `ProjectWebReadModel.topic_overview(topic_id)` that resolves `topic.intent.overview`, reads Markdown when present, and returns supporting Topic and Runtime payloads.
2. Add `GET /api/topics/{topic_id}/overview` to the FastAPI app.
3. Update the openable item descriptor for `topic:<topic_id>:overview` to include the overview API detail URL.
4. Add frontend API parsing for the topic overview response.
5. Replace raw JSON rendering in `TopicOverviewPanel` with Markdown content, `View JSON`, `Copy Markdown`, refresh, diagnostics, and warning states.
6. Generalize the shared JSON modal accessible description.
7. Add backend and frontend tests, then rebuild static assets.

## Resolved Questions

- The overview endpoint returns Markdown, overview source metadata, Topic JSON, Runtime JSON, and merged diagnostics in one payload.
- Missing `topic.intent.overview` uses HTTP 200 with `ok: true` when the Topic context resolves, `overview.exists: false`, no Markdown content, and a stable warning diagnostic.
- `View JSON` uses tabs for `Topic`, `Runtime`, and diagnostics or source metadata.
- `Copy Markdown` is disabled or reports no content when Markdown is unavailable.
- Project overview behavior stays out of scope for this change.
