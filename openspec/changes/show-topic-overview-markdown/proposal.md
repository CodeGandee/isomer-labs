## Why

The topic overview tab currently shows raw topic and runtime JSON as the page body, even though Isomer already stores the human-facing topic brief as `topic.intent.overview` at `intent/src/topic-overview.md`. Users should see the Markdown topic overview first and inspect supporting JSON only on demand.

## What Changes

- Add a topic overview read API that resolves `topic.intent.overview`, reads `topic-overview.md` when present, and returns warning diagnostics when it is missing.
- Change the Project Web topic overview panel to render the Markdown overview as the main content.
- Move the current Topic and Runtime JSON payloads into a `View JSON` modal with tabs, matching the idea detail page pattern.
- Keep the topic overview page read-only and resilient: missing `topic-overview.md` shows an inline warning instead of crashing.
- Generalize the existing JSON modal accessibility text so it can be reused outside idea detail.

## Capabilities

### New Capabilities
- `topic-overview-read-api`: Covers the backend read-only API that resolves and serves topic overview Markdown plus supporting topic/runtime JSON.
- `project-web-topic-overview`: Covers the frontend topic overview panel that renders Markdown first and exposes supporting JSON through `View JSON`.

### Modified Capabilities

## Impact

- Backend read model and FastAPI routes in `src/isomer_labs/web/`.
- Topic overview openable descriptor details in `src/isomer_labs/web/project_explorer.py`.
- Frontend API, types, and `TopicOverviewPanel` in `web/ui/src/`.
- Reusable JSON modal copy and accessibility behavior in `web/ui/src/App.tsx`.
- Unit tests for read-model/API behavior and frontend topic overview rendering.
