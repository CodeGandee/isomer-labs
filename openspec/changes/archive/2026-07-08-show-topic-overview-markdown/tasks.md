## 1. Backend Read API

- [x] 1.1 Add a read-model helper that resolves `topic.intent.overview` through semantic binding and reports path/source metadata.
- [x] 1.2 Read the resolved Markdown file when it exists and return a non-fatal warning diagnostic when it is missing or unreadable.
- [x] 1.3 Return HTTP 200 with `ok: true`, `overview.exists: false`, no Markdown content, and a stable warning diagnostic when the Topic context resolves but the overview file is missing.
- [x] 1.4 Include supporting Topic and Workspace Runtime JSON, merged diagnostics, and overview source metadata in the topic overview payload without mutating Project, Workspace Runtime, or files.
- [x] 1.5 Add a small read size guard if it fits the read-model pattern; otherwise ensure decode, permission, and read errors produce stable warning diagnostics.
- [x] 1.6 Add `GET /api/topics/{topic_id}/overview` to the FastAPI app.
- [x] 1.7 Update the `topic:<topic_id>:overview` openable descriptor detail URLs to advertise the overview endpoint.

## 2. Frontend Topic Overview

- [x] 2.1 Add frontend API schema and client function for the topic overview response.
- [x] 2.2 Replace inline Topic and Runtime JSON blocks in `TopicOverviewPanel` with Markdown-first rendering through `MarkdownView`.
- [x] 2.3 Add `View JSON`, `Copy Markdown`, and refresh controls to the topic overview panel.
- [x] 2.4 Add a `View JSON` modal with `Topic`, `Runtime`, and `Diagnostics` or `Source` tabs depending on available response data.
- [x] 2.5 Render a warning/empty Markdown state when the overview file is missing and keep the panel usable.
- [x] 2.6 Disable `Copy Markdown`, or report no available Markdown, when the overview Markdown is unavailable.
- [x] 2.7 Generalize the shared JSON modal accessible description for non-idea uses.

## 3. Tests and Assets

- [x] 3.1 Add backend unit tests for existing overview Markdown, missing overview Markdown, route registration, and descriptor detail URLs.
- [x] 3.2 Add frontend tests for Markdown-first overview rendering, missing-overview warning, `View JSON`, and copy actions.
- [x] 3.3 Run Python tests covering the Project Web read model.
- [x] 3.4 Run frontend tests and TypeScript checks.
- [x] 3.5 Rebuild packaged frontend static assets.
- [x] 3.6 Run `openspec validate show-topic-overview-markdown`.
